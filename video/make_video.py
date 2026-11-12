"""把一个视频脚本（JSON）做成 9:16 的成片：AI 配音 + 品牌画面 + 字幕。

用法：python make_video.py <脚本.json> <输出.mp4>
需要：node（装好 playwright）、requirements.txt 里的 Python 依赖（配音用 Qwen3-TTS，见 voice.py）。
ffmpeg 用系统里的；没有就用 imageio-ffmpeg 自带的。

脚本格式见 scripts/ 里的例子：
{
  "lang": "zh" 或 "en",
  "voice": "zh" / "en" / "en-male"（固定的配音声音，见 voices/README.md；不写就按 lang 选 zh 或 en），
  "scenes": [{"say": "配音念的话", "caption": "画面上方的大字，**重点词**", "text": "大字卡片"}]
}
每个场景四选一：
  shot  App Store 上 Badie 自己的截图（真实的 App 界面，自带标题），写名字，比如 "4-dayCards"
  text  大字卡片
  url   自动截网站手机版
  image 本地图片
"""
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import soundfile as sf

from voice import Voice

HERE = Path(__file__).resolve().parent
APP_ID = "6825569793"
STORE = {"zh": "country=sg&lang=zh_cn", "en": "country=us"}  # 用哪个区的截图


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def fetch_shots(spec, work):
    """把场景里的 shot 名字换成下载好的整屏图片路径（full）。"""
    if not any("shot" in s for s in spec["scenes"]):
        return
    with urllib.request.urlopen(f"https://itunes.apple.com/lookup?id={APP_ID}&{STORE[spec['lang']]}", timeout=60) as r:
        urls = json.load(r)["results"][0]["screenshotUrls"]
    by_name = {u.split("/")[-2].rsplit(".", 1)[0]: u.rsplit("/", 1)[0] + "/1080x2340bb.jpg" for u in urls}
    for s in spec["scenes"]:
        if "shot" in s:
            if s["shot"] not in by_name:
                raise SystemExit(f"App Store 上没有截图 {s['shot']}，现有：{sorted(by_name)}")
            path = work / f"shot-{s['shot']}.jpg"
            if not path.exists():
                urllib.request.urlretrieve(by_name[s["shot"]], path)
            s["full"] = str(path)


def tts(spec, work):
    v = Voice(spec.get("voice") or spec["lang"])
    durations = []
    for i, scene in enumerate(spec["scenes"]):
        audio, sr = v.say(scene["say"])
        sf.write(work / f"scene-{i:02d}.wav", audio, sr)
        durations.append(len(audio) / sr + 0.3)  # 每段之间留一点气口
    return durations


def main(spec_path, out_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    ff = ffmpeg()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        fetch_shots(spec, work)
        resolved = work / "spec.json"
        resolved.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        durations = tts(spec, work)
        subprocess.run(["node", str(HERE / "render.cjs"), str(resolved), str(work)], check=True)
        parts = []
        for i, d in enumerate(durations):
            part = work / f"part-{i:02d}.mp4"
            frames = int(d * 30)
            # 慢慢推近一点，画面不死板
            zoom = (f"scale=2160:3840,zoompan=z='1+0.04*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                    f":d={frames}:s=1080x1920:fps=30,format=yuv420p")
            subprocess.run([
                ff, "-v", "error", "-y",
                "-i", str(work / f"scene-{i:02d}.png"),
                "-i", str(work / f"scene-{i:02d}.wav"),
                "-vf", zoom, "-af", "apad", "-t", f"{d:.2f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", str(part),
            ], check=True)
            parts.append(part)
        listing = work / "list.txt"
        listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts))
        subprocess.run([ff, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                        "-c", "copy", "-movflags", "+faststart", str(out_path)], check=True)
    print(f"{out_path}  {sum(durations):.1f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
