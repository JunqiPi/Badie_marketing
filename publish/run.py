"""每天运行一次：把 content/schedule.json 里到期的视频做出来，发到品牌账号。

- 日期按洛杉矶时间。只处理今天和昨天的（漏跑一天能补上，不会把旧的一口气全发出去），一次最多发一条。
- 成片传到本仓库的 Release（公开网址，Buffer 从那里取）。
- 每个平台发成功后，在 Release 里留一个 posted-<平台>.txt。重跑只补没发成的平台。
环境变量：BUFFER_API_KEY、GH_TOKEN、GITHUB_REPOSITORY。
"""
import datetime
import json
import os
import subprocess
import sys
import tempfile
import zoneinfo
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buffer

ROOT = Path(__file__).resolve().parent.parent
REPO = os.environ["GITHUB_REPOSITORY"]


def gh(*args, check=True):
    return subprocess.run(["gh", *args, "-R", REPO], check=check, capture_output=True, text=True)


def notice(title, msg):
    print(f"::notice title={title}::{msg}", flush=True)


def main():
    today = datetime.datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles")).date()
    due = [e for e in json.loads((ROOT / "content/schedule.json").read_text(encoding="utf-8"))
           if 0 <= (today - datetime.date.fromisoformat(e["date"])).days <= 1]
    channels = buffer.channels()
    for entry in sorted(due, key=lambda e: e["date"]):
        script = ROOT / entry["script"]
        spec = json.loads(script.read_text(encoding="utf-8"))
        tag = f"post-{entry['date']}-{script.stem}"
        name = f"{script.stem}.mp4"
        view = gh("release", "view", tag, "--json", "assets", check=False)
        assets = [a["name"] for a in json.loads(view.stdout)["assets"]] if view.returncode == 0 else []
        todo = [c for c in channels if f"posted-{c['service']}.txt" not in assets]
        if not todo:
            continue
        if name not in assets:
            out = Path(tempfile.mkdtemp()) / name
            subprocess.run([sys.executable, str(ROOT / "video/make_video.py"), str(script), str(out)],
                           check=True, cwd=ROOT / "video")
            if view.returncode != 0:
                gh("release", "create", tag, "--title", f"{entry['date']} {spec['post']['title']}",
                   "--notes", "自动发布的成片。配音是 AI 的。")
            gh("release", "upload", tag, str(out))
        url = f"https://github.com/{REPO}/releases/download/{tag}/{name}"
        failed = False
        for c in todo:
            try:
                post = buffer.post_video(c, url, spec["post"]["text"], spec["post"]["title"])
                marker = Path(tempfile.mkdtemp()) / f"posted-{c['service']}.txt"
                marker.write_text(json.dumps(post))
                gh("release", "upload", tag, str(marker))
                notice("发出去了", f"{c['service']} {tag} status={post['status']} id={post['id']}")
            except Exception as e:  # 一个平台失败不影响其他平台
                failed = True
                print(f"::error title=没发成::{c['service']} {tag}: {e}", flush=True)
        if failed:
            raise SystemExit(1)
        return  # 一次最多发一条
    notice("今天没有要发的", str(today))


if __name__ == "__main__":
    main()
