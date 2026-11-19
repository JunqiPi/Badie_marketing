"""做无人声的动画短视频：逐帧渲染画面 + 合成音效 + 背景音乐，混音到 −14 LUFS / −1 dBTP，再出一张审片图（脚本 JSON 的 sheet 里列的帧）。

用法：
  python make_anim.py scripts/smash-defense.json anim/smash-defense.html --lang zh,en,ja,ko
  python make_anim.py ... --music 别的曲子.wav      # 换音乐只换这一个参数（不给就用 make_music.py 现生成）
  python make_anim.py ... --audio-only               # 只重做声音，画面用上次渲染好的
输出：out/<脚本名>-<语言>.mp4 和 out/<脚本名>-<语言>-sheet.png（out/ 不进 git）。

画面：anim/render_anim.cjs（Playwright 逐帧截图 → ffmpeg，BT.709）。
声音：音效全部在这里用 numpy 合成，只放在转折点（脚本 JSON 的 sfx 一节）；
     音乐在 dips 那几段压到几乎无声，音效响的时候让 4 dB；amix normalize=0；loudnorm 两遍，-ar 48000。
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

HERE = Path(__file__).resolve().parent
SR = 48000
rng = np.random.default_rng(11)


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


# ---------- 音效（自己合成）----------
def _f(kind, x, hz, order=2):
    return sosfilt(butter(order, hz, kind, fs=SR, output="sos"), x)


def _t(sec):
    return np.arange(int(sec * SR)) / SR


def sfx_transition():
    """开场转场：0.55 秒越来越亮的 whoosh，落在转场那一帧上一个软的低音冲击。返回 (声音, 相对事件的起点秒数)。"""
    pre = 0.55
    t = _t(pre + 0.9)
    n = len(t)
    noise = rng.standard_normal(n)
    lo, mid, hi = _f("bandpass", noise, [250, 700]), _f("bandpass", noise, [700, 2200]), _f("bandpass", noise, [2200, 6000])
    k = np.clip(t / pre, 0, 1)
    swell = np.where(t < pre, k ** 2.2, np.exp(-(t - pre) / 0.06))
    whoosh = (lo * (1 - k) + mid * np.sin(np.pi * np.clip(k, 0, 1)) + hi * k ** 2) * swell * 0.35
    ti = np.clip(t - pre, 0, None)
    f = 42 + 70 * np.exp(-ti / 0.05)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-ti / 0.35) * (t >= pre) * 0.75
    thump = _f("lowpass", rng.standard_normal(n), 900) * np.exp(-ti / 0.03) * (t >= pre) * 0.35
    return np.tanh(whoosh + boom + thump), -pre


def sfx_reveal():
    """揭晓：全片最响的一下。低音冲击 + 短促的高频 + 两个亮的音（A5、E6）慢慢散掉。"""
    t = _t(1.6)
    n = len(t)
    f = 45 + 110 * np.exp(-t / 0.04)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.42) * 0.9
    crack = _f("bandpass", rng.standard_normal(n), [1500, 7000]) * np.exp(-t / 0.025) * 0.5
    bell = (np.sin(2 * np.pi * 880 * t) * 0.18 + np.sin(2 * np.pi * 1318.5 * t) * 0.12 + np.sin(2 * np.pi * 1760 * t) * 0.05) * np.exp(-t / 0.5)
    att = np.clip(t / 0.002, 0, 1)
    return np.tanh(1.2 * (boom + crack + bell) * att), 0.0


def sfx_miss():
    """球落空地：闷的低音 thud。"""
    t = _t(0.7)
    f = 38 + 45 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)
    dull = _f("lowpass", rng.standard_normal(len(t)), 350) * np.exp(-t / 0.05) * 0.8
    return np.tanh(1.4 * (body + dull) * np.clip(t / 0.002, 0, 1)) * 0.8, 0.0


def sfx_rule():
    """规则卡：轻的 shimmer，四个高音依次亮起（A5 C6 E6 A6）。"""
    t = _t(2.2)
    out = np.zeros(len(t))
    for i, hz in enumerate((880, 1046.5, 1318.5, 1760)):
        d = i * 0.045
        tt = np.clip(t - d, 0, None)
        trem = 1 + 0.15 * np.sin(2 * np.pi * 6 * tt)
        out += np.sin(2 * np.pi * hz * tt) * np.exp(-tt / 0.6) * (t >= d) * np.clip(tt / 0.004, 0, 1) * trem * 0.14
    air = _f("highpass", rng.standard_normal(len(t)), 6000) * np.exp(-t / 0.25) * np.clip(t / 0.08, 0, 1) * 0.05
    return out + air, 0.0


SFX = {"transition": (sfx_transition, 0.9), "reveal": (sfx_reveal, 1.0), "miss": (sfx_miss, 0.85), "rule": (sfx_rule, 0.7)}


def stereo(x, width=0.0):
    return np.stack([x, x], axis=1)


def build_audio(spec, music, work, ff):
    dur = spec["duration"]
    inputs, chains, labels = ["-stream_loop", "-1", "-i", music], [], []
    # 音乐：裁到片长；dips 再压 10 dB（换成别的曲子时，这就是“空”的那一下）；每个音效响时让 4 dB
    parts = []
    for a, b in spec["music"]["dips"]:
        parts.append(f"(1-0.7*clip((t-{a})/0.08,0,1)*clip(({b}-t)/0.004,0,1))")
    for name, at in spec["sfx"].items():
        parts.append(f"(1-0.37*clip((t-{at - 0.02})/0.02,0,1)*clip(({at + 0.9}-t)/0.4,0,1))")
    vol = "*".join(parts)
    chains.append(f"[0:a]aresample={SR},atrim=0:{dur},asetpts=N/SR/TB,volume='{vol}':eval=frame[m]")
    labels.append("[m]")
    for i, (name, at) in enumerate(spec["sfx"].items(), start=1):
        fn, gain = SFX[name]
        sig, off = fn()
        path = work / f"sfx-{name}.wav"
        sf.write(path, stereo(sig * gain), SR, subtype="PCM_24")
        inputs += ["-i", path]
        ms = max(0, round((at + off) * 1000))
        chains.append(f"[{i}:a]adelay={ms}:all=1[s{i}]")
        labels.append(f"[s{i}]")
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{dur}[out]")
    mix = work / "mix.wav"
    run([ff, "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[out]", "-ar", SR, "-c:a", "pcm_s24le", mix])

    # loudnorm 两遍
    target = "I=-14:TP=-1:LRA=11"
    p1 = subprocess.run([ff, "-hide_banner", "-i", mix, "-af", f"loudnorm={target}:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = json.loads(re.findall(r"\{[^{}]*\}", p1.stderr)[-1])
    norm = work / "mix-norm.wav"
    p2 = subprocess.run([ff, "-hide_banner", "-y", "-i", mix, "-af",
                         f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                         f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json",
                         "-ar", str(SR), "-c:a", "pcm_s24le", str(norm)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p2.returncode:
        sys.exit(p2.stderr)
    m2 = json.loads(re.findall(r"\{[^{}]*\}", p2.stderr)[-1])
    print(f"loudnorm: in {m['input_i']} LUFS / {m['input_tp']} dBTP -> {m2['output_i']} LUFS / {m2['output_tp']} dBTP, {m2['normalization_type']}")
    return norm


def measure(ff, path):
    p = subprocess.run([ff, "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = p.stderr[p.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1)
    lra = re.search(r"LRA:\s+(-?[\d.]+) LU", tail).group(1)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1)
    return f"I {i} LUFS, LRA {lra} LU, true peak {tp} dBTP"


def sheet(ff, video, times, out, fps):
    frames = [round(t * fps) for t in times]
    sel = "+".join(f"eq(n\\,{f})" for f in frames)
    cols = 4 if len(frames) > 6 else 3
    rows = (len(frames) + cols - 1) // cols
    run([ff, "-v", "error", "-y", "-i", video, "-vf",
         f"select='{sel}',scale=360:640:flags=lanczos,tile={cols}x{rows}:padding=6:color=0x050806",
         "-frames:v", "1", "-fps_mode", "vfr", out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("page")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--music", help="背景音乐文件；不给就用 make_music.py 按脚本生成")
    ap.add_argument("--out", default=str(HERE / "out"))
    ap.add_argument("--audio-only", action="store_true")
    a = ap.parse_args()
    spec_path = Path(a.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    name = spec_path.stem
    out = Path(a.out)
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    ff = ffmpeg()

    music = a.music
    if not music:
        music = work / f"{name}-music.wav"
        run([sys.executable, HERE / "make_music.py", music, "--spec", spec_path])
    audio = build_audio(spec, music, work, ff)

    for lang in a.lang.split(","):
        silent = work / f"{name}-{lang}-video.mp4"
        if not (a.audio_only and silent.exists()):
            run(["node", HERE / "anim" / "render_anim.cjs", Path(a.page).resolve(), spec_path, lang, silent],
                env={**__import__("os").environ, "FFMPEG": ff})
        final = out / f"{name}-{lang}.mp4"
        run([ff, "-v", "error", "-y", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
             "-c:a", "aac", "-b:a", "384k", "-ar", str(SR), "-shortest", "-movflags", "+faststart", final])
        sheet(ff, final, spec["sheet"], out / f"{name}-{lang}-sheet.png", spec["fps"])
        print(f"{final}: {measure(ff, final)}")


if __name__ == "__main__":
    main()
