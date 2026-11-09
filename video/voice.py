"""固定的配音声音：Qwen3-TTS Base 照着 voices/ 里的参考音念，每条都是同一个声音。

声音（2026-11-08 用户选定）：zh 中文、en 英文、en-male 英文备用。见 voices/README.md。
"""
import json
from pathlib import Path

import numpy as np
import torch
from qwen_tts import Qwen3TTSModel

VOICES = Path(__file__).resolve().parent / "voices"
MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"


class Voice:
    def __init__(self, name):
        ref = json.loads((VOICES / "refs.json").read_text(encoding="utf-8"))[name]
        self.language = ref["language"]
        cuda = torch.cuda.is_available()
        self.model = Qwen3TTSModel.from_pretrained(
            MODEL,
            device_map="cuda:0" if cuda else "cpu",
            dtype=torch.bfloat16 if cuda else torch.float32,
            attn_implementation="sdpa",
        )
        self.prompt = self.model.create_voice_clone_prompt(
            ref_audio=str(VOICES / ref["audio"]), ref_text=ref["text"]
        )

    def say(self, text):
        """念一句，返回 (float32 波形, 采样率)。"""
        wavs, sr = self.model.generate_voice_clone(
            text=text, language=self.language, voice_clone_prompt=self.prompt
        )
        return wavs[0].astype(np.float32), sr
