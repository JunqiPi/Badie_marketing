"""把 content/threads.json 里用户确认过的文字帖排进 Buffer，到点由 Buffer 自动发到 Threads。

- 只排 "approved": true 的：帖子先给用户看，用户确认了才标。
- "approved" 改回 false 的：如果还在队列里没发，就撤下来。
- 可以带一张图："image" 写仓库里的路径（放在 content/media/），"alt" 写给看不见图的人的说明。
- 可以带一条自己的回复："reply" 写文字，"reply_image" 和 "reply_alt" 是回复里的图。用来放 App 的名字、截图和链接。
- 改了已经排上的帖子的图或回复：加 "replace": true 推一次，换完把它去掉。
- "when" 是洛杉矶时间。已经过了时间的不补发，只提示。
- 同样的文字已经排着或发过的，跳过。所以这个脚本重复跑是安全的。
环境变量：BUFFER_API_KEY。
"""
import datetime
import json
import os
import sys
import zoneinfo
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buffer

ROOT = Path(__file__).resolve().parent.parent
LA = zoneinfo.ZoneInfo("America/Los_Angeles")


def main():
    entries = json.loads((ROOT / "content/threads.json").read_text(encoding="utf-8"))
    threads = [c for c in buffer.channels() if c["service"] == "threads"]
    if len(threads) != 1:
        raise SystemExit(f"::error::Buffer 里应该正好有一个 Threads 频道，现在是 {len(threads)} 个")
    channel = threads[0]
    have = buffer.existing_texts(channel)
    now = datetime.datetime.now(LA)
    failed = False
    for e in entries:
        label = e["text"][:12]
        if e.get("approved") is not True:
            # 没确认（或者确认后又撤回）的：如果还排在队列里，就撤下来
            h = have.get(e["text"])
            if h and h["status"] == "scheduled":
                try:
                    buffer.delete_post(h["id"])
                    print(f"::notice title=撤下来了::{label} 原定 dueAt={h['dueAt']}")
                except Exception as err:
                    failed = True
                    print(f"::error title=没撤成::{label}: {err}")
            elif h:
                print(f"::warning title=已经发出去了，撤不了::{label} status={h['status']}")
            else:
                print(f"::notice title=没确认，不排::{label}")
            continue
        when = datetime.datetime.strptime(e["when"], "%Y-%m-%d %H:%M").replace(tzinfo=LA)
        def media_url(path):
            if not (ROOT / path).is_file():
                raise FileNotFoundError(path)
            # 用这次提交的固定网址，之后分支再变，图也还在
            return f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{os.environ['GITHUB_SHA']}/{path}"

        try:
            image_url = media_url(e["image"]) if e.get("image") else None
            reply = None
            if e.get("reply"):
                reply = {"text": e["reply"], "alt": e.get("reply_alt"),
                         "image_url": media_url(e["reply_image"]) if e.get("reply_image") else None}
        except FileNotFoundError as err:
            failed = True
            print(f"::error title=图片不在仓库里::{label}: {err}")
            continue
        if e["text"] in have:
            h = have[e["text"]]
            # "replace": true：这条的图或回复改过了，把队列里的旧版撤掉重排。换完要把这个标记去掉。
            wants_swap = e.get("replace") is True or (image_url and not h.get("assets"))
            if wants_swap and h["status"] == "scheduled":
                buffer.delete_post(h["id"])
                print(f"::notice title=撤掉旧版重排::{label}")
            else:
                print(f"::notice title=已经有了::{label} status={h['status']} dueAt={h['dueAt']} 图={len(h.get('assets') or [])}")
                continue
        if when <= now:
            print(f"::warning title=时间已过，没排::{label} when={e['when']}")
            continue
        due = when.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        try:
            post = buffer.schedule_text(channel, e["text"], due, image_url, e.get("alt"), reply)
            print(f"::notice title=排上了::{label} 洛杉矶 {e['when']} dueAt={post['dueAt']} status={post['status']} 图={len(post.get('assets') or [])} 回复={'有' if reply else '无'}")
        except Exception as err:
            failed = True
            print(f"::error title=没排上::{label}: {err}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
