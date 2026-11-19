"""合成短视频的背景音乐（无人声的电子乐底），全部用 numpy 现算，不用任何采样或下载的素材。

按创始人给的参考视频（ANIMATION_STUDY.md 附录）做的形状：
  intro   开头到第一个“空”：低沉的脉冲（每半小节一下）+ 暖色 pad，没有鼓
  dip     0.5–1 秒几乎无声
  groove  在转场那一帧整个砸进来：kick 1、3 拍，闭镲反拍八分，sub bass 跟和弦根音，闷的 pluck 琶音，pad 垫底
  full    揭晓那一帧再满一档：加 2、4 拍的 clap，闭镲改十六分，pluck 改十六分
  resolve 规则卡那一帧回到主和弦，鼓只剩 1 拍的 kick，越来越松
  tail    和开头同一个织体（pad + 脉冲），所以循环时末尾能接回开头
和弦：小调 i–VI–III–VII（A 小调 = Am–F–C–G），一小节一个；120 BPM 时一小节 2 秒，两小节 = 字幕换一句的 4 秒。
pad 和 bass 跟着 kick 做轻微的“侧链”压缩（直接写音量曲线）。

用法：
  python make_music.py out.wav --spec scripts/smash-defense.json            # 用脚本里的 music 一节
  python make_music.py out.wav --bpm 120 --key D --duration 40 --drop 3 --full 15 --resolve 33 --tail 38.3 \
        --first-downbeat 1 --dips 2.4-3,14.2-15,32.4-33
不同语言版本时长不同时，只改这些时间点重新生成。
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
KEYS = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
# 小调里的 i、VI、III、VII：(根音相对主音的半音数, 三音)
PROG = [(0, 3), (8, 4), (3, 4), (10, 4)]
RESOLVE = [(0, 3), (8, 4), (0, 3)]


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x, axis=0)


def hp(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x, axis=0)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x, axis=0)


class Track:
    def __init__(self, dur):
        self.n = int(round(dur * SR))
        self.buses = {k: np.zeros((self.n, 2)) for k in ("pad", "bass", "pluck", "drums", "pulse", "send")}

    def add(self, bus, t, sig, pan=0.0, send=0.0):
        i = int(round(t * SR))
        if i >= self.n or len(sig) == 0:
            return
        if i < 0:
            sig, i = sig[-i:], 0
        sig = sig[: self.n - i]
        l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        st = np.stack([sig * l, sig * r], axis=1) * math.sqrt(2)
        self.buses[bus][i:i + len(sig)] += st
        if send:
            self.buses["send"][i:i + len(sig)] += st * send


# ---------- 乐器 ----------
rng = np.random.default_rng(7)


def saw(f, n, phase=0.0, top=3200):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, max(2, int(top / f)) + 1):
        out += np.sin(2 * np.pi * k * f * t + phase * k) / k
    return out * 0.55


def tri(f, n, top=5000):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for j, k in enumerate(range(1, int(top / f) + 1, 2)):
        out += ((-1) ** j) * np.sin(2 * np.pi * k * f * t) / k ** 2
    return out * 0.8


def adsr(n, a, r, total):
    """a 秒起音，持续到 total 秒，然后 r 秒释放；n 是总采样数（含释放）。"""
    t = np.arange(n) / SR
    env = np.clip(t / max(a, 1e-4), 0, 1)
    env *= np.where(t < total, 1.0, np.clip(1 - (t - total) / max(r, 1e-3), 0, 1))
    return env


def pad_note(m, dur, a, r, cutoff):
    n = int((dur + r) * SR)
    f = midi_hz(m)
    x = sum(saw(f * 2 ** (c / 1200), n, phase=p) for c, p in ((-7, 0.0), (0, 1.3), (7, 2.1)))
    x = lp(x, cutoff, 2)
    return x * adsr(n, a, r, dur) * 0.16


def kick(vel=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 47 + 105 * np.exp(-t / 0.032)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.2) * (1 - np.exp(-t / 0.0015))
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t / 0.003) * 0.12
    return np.tanh(1.4 * (body + click)) * 0.85 * vel


def hat(vel=1.0, tau=0.018):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 7500, 4) * np.exp(-t / tau)
    return x * 0.11 * vel


def clap(vel=1.0):
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    env = np.zeros(n)
    for d in (0.0, 0.009, 0.019):
        env += np.where(t >= d, np.exp(-(t - d) / 0.005), 0)
    env += np.where(t >= 0.025, np.exp(-(t - 0.025) / 0.07), 0) * 0.6
    x = bp(rng.standard_normal(n), 1000, 3200) * env
    return x * 0.16 * vel


def bass_note(m, dur, vel=1.0):
    n = int((dur + 0.03) * SR)
    t = np.arange(n) / SR
    f = midi_hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    env = np.clip(t / 0.004, 0, 1) * (0.65 + 0.35 * np.exp(-t / 0.12)) * np.clip((dur + 0.03 - t) / 0.03, 0, 1)
    return np.tanh(1.3 * x) * env * 0.42 * vel


def pluck(m, vel=1.0, tau=0.09):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    x = tri(midi_hz(m), n) * np.clip(t / 0.002, 0, 1) * np.exp(-t / tau)
    return lp(x, 3200, 2) * 0.2 * vel


def pulse(m, vel=1.0):
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    f = midi_hz(m) * (1 + 0.06 * np.exp(-t / 0.05))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.3 * np.sin(2 * ph)
    return lp(x * np.clip(t / 0.012, 0, 1) * np.exp(-t / 0.42), 400) * 0.55 * vel


# ---------- 编曲 ----------
def build(p):
    bpm, dur = p["bpm"], p["duration"]
    beat = 60.0 / bpm
    bar = 4 * beat
    tonic = 45 + ((KEYS[p["key"]] - 9) % 12)        # 主音放在 A2 附近
    if tonic > 50:
        tonic -= 12
    fd, drop, full, res, tail = p["first_downbeat"], p["drop"], p["full"], p["resolve"], p["tail"]
    tr = Track(dur)

    def chord(t):
        if t < drop or t >= tail:
            return PROG[0]
        if t < full:
            return PROG[int((t - drop + 1e-6) // bar) % 4]
        if t < res:
            return PROG[int((t - full + 1e-6) // bar) % 4]
        return RESOLVE[min(len(RESOLVE) - 1, int((t - res + 1e-6) // bar))]

    # 和弦段：每小节一个，段落交界处也切开
    cuts = {0.0, dur, drop, full, res, tail}
    k = math.ceil((0 - fd) / bar)
    while fd + k * bar < dur:
        if fd + k * bar > 0:
            cuts.add(round(fd + k * bar, 6))
        k += 1
    cuts = sorted(c for c in cuts if 0 <= c <= dur)
    segs = [(a, b, chord(a)) for a, b in zip(cuts, cuts[1:]) if b - a > 1e-3]

    # pad：一直在；intro / tail 更暗
    for a, b, (root, third) in segs:
        dark = a < drop or a >= tail
        cutoff = 900 if dark else (1500 if a < full or a >= res else 1900)
        att = 0.02 if a == 0 else 0.18
        vol = 0.45 if dark else (0.8 if a < full else 1.0)
        for m in (tonic + root, tonic + root + 7, tonic + root + 12 + third, tonic + root + 19):
            if m - tonic > 22:
                m -= 12
            tr.add("pad", a, pad_note(m, b - a, att, 0.35 if b < dur else 0.0, cutoff) * vol, pan=0.0, send=0.35)

    # 网格上的每一个十六分音符
    s16 = beat / 4
    j0 = math.ceil((0 - fd) / s16)
    kicks = []
    j = j0
    while fd + j * s16 < dur - 1e-6:
        t = fd + j * s16
        pos = (j % 16 + 16) % 16                  # 小节里的第几个十六分
        root, third = chord(t + 1e-4)
        groove = drop <= t < res
        fullsec = full <= t < res
        if (t < drop or t >= tail) and pos % 8 == 0:            # 每半小节一下低脉冲
            tr.add("pulse", t, pulse(tonic - 12, 1.0 if pos == 0 else 0.75))
        if groove:
            if pos in (0, 8):
                tr.add("drums", t, kick(1.0 if pos == 0 else 0.9)); kicks.append(t)
            if fullsec and pos in (4, 12):
                tr.add("drums", t, clap(0.9), pan=0.0, send=0.5)
            if fullsec:
                tr.add("drums", t, hat([0.55, 0.25, 1.0, 0.3][pos % 4]), pan=0.25)
            elif pos % 4 == 2:
                tr.add("drums", t, hat(0.8), pan=0.25)
            if pos % 2 == 0:                                     # 八分 bass，跟根音
                oct_ = 12 if pos in (6, 14) else 0
                tr.add("bass", t, bass_note(tonic - 12 + root + oct_, beat / 2 - 0.03, (0.85 if pos % 4 else 1.0) * (1.0 if fullsec else 0.8)))
            tones = [tonic + 12 + root, tonic + 12 + root + 7, tonic + 24 + root, tonic + 24 + root + third]
            order = [0, 2, 1, 3, 2, 1, 3, 0]
            if fullsec or pos % 2 == 0:
                vel = (0.9 if pos % 4 == 0 else 0.6) * (1.0 if fullsec else 0.75)
                tr.add("pluck", t, pluck(tones[order[(pos // (1 if fullsec else 2)) % 8]], vel),
                       pan=0.35 if pos % 2 == 0 else -0.35, send=0.3)
        elif res <= t < tail:
            if pos == 0 and t < tail - bar / 2:
                tr.add("drums", t, kick(0.8)); kicks.append(t)
            if pos == 0:
                tr.add("bass", t, bass_note(tonic - 12 + root, min(bar, tail - t) - 0.05, 0.9))
            if pos % 2 == 0:
                tones = [tonic + 12 + root, tonic + 12 + root + 7, tonic + 24 + root, tonic + 24 + root + third]
                fade = 1 - (t - res) / max(1e-3, tail - res) * 0.5
                tr.add("pluck", t, pluck(tones[[0, 2, 1, 3][(pos // 2) % 4]], 0.6 * fade, tau=0.14), pan=0.3 if pos % 4 else -0.3, send=0.45)
        j += 1

    # 侧链：kick 之后 pad、bass 让一下
    tt = np.arange(tr.n) / SR
    duck = np.ones(tr.n)
    for k_ in kicks:
        i = int(k_ * SR)
        seg = tt[i:] - k_
        duck[i:] = np.minimum(duck[i:], 1 - 0.5 * np.exp(-seg / 0.11))
    tr.buses["pad"] *= (0.55 + 0.45 * duck)[:, None]
    tr.buses["bass"] *= duck[:, None]

    # 混响：一段指数衰减的噪声做卷积
    irn = int(1.8 * SR)
    ti = np.arange(irn) / SR
    ir = np.stack([rng.standard_normal(irn), rng.standard_normal(irn)], axis=1) * np.exp(-ti / 0.38)[:, None]
    ir = lp(ir, 5000) * 0.03
    send = hp(tr.buses["send"], 200)
    wet = np.stack([fftconvolve(send[:, c], ir[:, c])[: tr.n] for c in range(2)], axis=1)

    mix = (tr.buses["pad"] * 0.9 + tr.buses["bass"] * 0.9 + tr.buses["pluck"] * 0.8 +
           tr.buses["drums"] * 1.0 + tr.buses["pulse"] * 0.9 + wet * 0.8)

    # “空”的地方：0.08 秒压到 −15 dB（混音时再压 −10 dB，合起来约 −25 dB，还听得见一点 pad 的尾巴），落拍那一下马上回来
    g = np.ones(tr.n)
    for a, b in p["dips"]:
        g = np.minimum(g, np.interp(tt, [a, a + 0.08, b - 0.004, b], [1, 0.18, 0.18, 1], left=1, right=1))
    mix *= g[:, None]
    mix = np.tanh(mix * 1.1) / 1.1
    peak = np.max(np.abs(mix))
    return mix / peak * 10 ** (-3 / 20)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--spec", help="视频脚本 JSON，用里面的 duration 和 music")
    ap.add_argument("--bpm", type=float); ap.add_argument("--key"); ap.add_argument("--duration", type=float)
    ap.add_argument("--first-downbeat", type=float); ap.add_argument("--drop", type=float)
    ap.add_argument("--full", type=float); ap.add_argument("--resolve", type=float); ap.add_argument("--tail", type=float)
    ap.add_argument("--dips", help="形如 2.4-3,14.2-15")
    a = ap.parse_args()
    p = {"bpm": 120, "key": "A", "duration": 38.0, "first_downbeat": 1.0, "drop": 3.0, "full": 15.0,
         "resolve": 31.0, "tail": 36.3, "dips": [[2.4, 3.0], [14.2, 15.0], [30.4, 31.0]]}
    if a.spec:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        p.update(spec.get("music", {}))
        p["duration"] = spec["duration"]
    for k in ("bpm", "key", "duration", "first_downbeat", "drop", "full", "resolve", "tail"):
        v = getattr(a, k)
        if v is not None:
            p[k] = v
    if a.dips:
        p["dips"] = [[float(x) for x in d.split("-")] for d in a.dips.split(",")]
    audio = build(p)
    sf.write(a.out, audio, SR, subtype="PCM_24")
    print(f"{a.out}  {len(audio) / SR:.2f}s  {p['bpm']} BPM  key {p['key']} minor")


if __name__ == "__main__":
    main()
