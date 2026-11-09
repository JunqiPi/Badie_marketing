# 单独配一段音，试听用。
# 用法：python video/say.py <声音: zh|en|en-male> <输出.wav> "台词" ["台词2" ...]
# 多句按顺序拼成一个文件，句子之间停 0.25 秒。
import sys

import numpy as np
import soundfile as sf

from voice import Voice

name, out, *lines = sys.argv[1:]
v = Voice(name)
parts = []
for line in lines:
    wav, sr = v.say(line)
    parts += [wav, np.zeros(int(sr * 0.25), dtype=np.float32)]
audio = np.concatenate(parts)
sf.write(out, audio, sr)
print(f"wrote {out} {len(audio) / sr:.1f}s")
