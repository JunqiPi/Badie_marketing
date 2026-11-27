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


# ---------- 冲击音效（2026-11-23，可选：脚本 JSON 有 impact 才加）----------
# 杀球“啪”、杀球飞行 whoosh、接杀/挡网“嗒”、落地“咚”。和上面四个音效一样是干声、没有混响。
# 冲击类对齐到事件之后的第一帧（和 common.js 的 impFrame 一样取整），whoosh 只在击球之后响，不提前。
def imp_smash():
    """杀球击球：又脆又重。2 ms 的起音，高频 crack 8 ms 散掉，下面垫一个 110→55 Hz 的短低音。"""
    t = _t(0.35)
    n = len(t)
    crack = _f("bandpass", rng.standard_normal(n), [1800, 9000]) * np.exp(-t / 0.008)
    snap = _f("bandpass", rng.standard_normal(n), [600, 2400]) * np.exp(-t / 0.02) * 0.6
    f = 55 + 55 * np.exp(-t / 0.02)
    low = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07) * 0.8
    return np.tanh(1.6 * (crack * 1.2 + snap + low) * np.clip(t / 0.0015, 0, 1)) * 0.95


def imp_whoosh(dur):
    """杀球飞行：dur 秒，噪声从亮到暗扫下来，中间最响，到拍面前收掉。"""
    t = _t(dur)
    n = len(t)
    k = t / dur
    noise = rng.standard_normal(n)
    hi, mid = _f("bandpass", noise, [2500, 8000]), _f("bandpass", noise, [700, 2500])
    env = np.sin(np.pi * np.clip(k, 0, 1)) ** 1.5 * np.clip(t / 0.01, 0, 1)
    return (hi * (1 - k) + mid * k) * env * 0.55


def imp_block():
    """接杀 / 挡网：轻的“嗒”，短促的中高频 + 一点 700 Hz 的木头感。"""
    t = _t(0.18)
    n = len(t)
    tick = _f("bandpass", rng.standard_normal(n), [1500, 5000]) * np.exp(-t / 0.005)
    body = np.sin(2 * np.pi * 720 * t) * np.exp(-t / 0.025) * 0.5
    return np.tanh(1.8 * (tick + body) * np.clip(t / 0.001, 0, 1)) * 0.7


def imp_land():
    """落地：闷的“咚”，比转折点那个 miss 短、轻。"""
    t = _t(0.3)
    f = 60 + 40 * np.exp(-t / 0.02)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08)
    dull = _f("lowpass", rng.standard_normal(len(t)), 500) * np.exp(-t / 0.025) * 0.7
    return np.tanh(1.3 * (body + dull) * np.clip(t / 0.002, 0, 1)) * 0.6


IMP_GAIN = {"smash": 0.9, "whoosh": 0.4, "block": 0.6, "land": 0.6}


def slowdown(x, k=2.0):
    """慢放段的声音：拉长 k 倍（音调也跟着降），和画面上 0.5× 的动作对得上。"""
    n = int(len(x) * k)
    return np.interp(np.arange(n) / k, np.arange(len(x)), x)


def frame_at(at, fps):
    return np.ceil(at * fps - 1e-6) / fps


def impact_track(spec):
    """把所有冲击音效按帧放进一条和片子一样长的单声道轨。没有 impact 返回 None。"""
    ev = (spec.get("impact") or {}).get("events") or []
    if not ev:
        return None
    fps = spec["fps"]
    out = np.zeros(int(spec["duration"] * SR) + SR)

    def put(sig, at):
        i = int(round(at * SR))
        j = min(len(out), i + len(sig))
        if j > i:
            out[i:j] += sig[: j - i]

    for e in ev:
        if e.get("quiet"):
            continue
        at = frame_at(e["at"], fps)
        g = e.get("gain", 1.0)   # 单个事件的音量（默认 1）；和音乐重拍叠在一起太响时调小
        if e["type"] == "smash":
            put(imp_smash() * IMP_GAIN["smash"] * g, at)
            put(imp_whoosh(e.get("dur", 0.4)) * IMP_GAIN["whoosh"] * g, at + 0.004)
        else:
            sig = (imp_block() if e["type"] == "block" else imp_land()) * IMP_GAIN[e["type"]] * g
            put(slowdown(sig) * 0.85 if e.get("slow") else sig, at)
    return out[: int(spec["duration"] * SR)]


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
    for e in (spec.get("impact") or {}).get("events") or []:   # 杀球那一下音乐让开约 5 dB，0.35 秒回来
        if e["type"] == "smash" and not e.get("quiet"):
            at = frame_at(e["at"], spec["fps"])
            parts.append(f"(1-0.45*clip((t-{at - 0.01})/0.01,0,1)*clip(({at + 0.45}-t)/0.3,0,1))")
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
    imp = impact_track(spec)
    if imp is not None:
        path = work / "sfx-impact.wav"
        sf.write(path, stereo(imp), SR, subtype="PCM_24")
        inputs += ["-i", path]
        k = len(labels)
        chains.append(f"[{k}:a]anull[s{k}]")
        labels.append(f"[s{k}]")
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
    ap.add_argument("--tag", default="", help="成片名后面加一段，比如 --tag impact → out/<名>-<语言>-impact.mp4（试验版不覆盖原片）")
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
        sfx_ = f"-{a.tag}" if a.tag else ""
        silent = work / f"{name}-{lang}{sfx_}-video.mp4"
        if not (a.audio_only and silent.exists()):
            run(["node", HERE / "anim" / "render_anim.cjs", Path(a.page).resolve(), spec_path, lang, silent],
                env={**__import__("os").environ, "FFMPEG": ff})
        final = out / f"{name}-{lang}{sfx_}.mp4"
        run([ff, "-v", "error", "-y", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
             "-c:a", "aac", "-b:a", "384k", "-ar", str(SR), "-shortest", "-movflags", "+faststart", final])
        sheet(ff, final, spec["sheet"], out / f"{name}-{lang}{sfx_}-sheet.png", spec["fps"])
        print(f"{final}: {measure(ff, final)}")


if __name__ == "__main__":
    main()
