"""把 content/threads.json 里用户确认过的文字帖排进 Buffer，到点由 Buffer 自动发到 Threads。

- 只排 "approved": true 的：帖子先给用户看，用户确认了才标。
- "approved" 改回 false 的：如果还在队列里没发，就撤下来。
- "when" 是洛杉矶时间。已经过了时间的不补发，只提示。
- 同样的文字已经排着或发过的，跳过。所以这个脚本重复跑是安全的。
环境变量：BUFFER_API_KEY。
"""
import datetime
import json
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
        if e["text"] in have:
            h = have[e["text"]]
            print(f"::notice title=已经有了::{label} status={h['status']} dueAt={h['dueAt']}")
            continue
        if when <= now:
            print(f"::warning title=时间已过，没排::{label} when={e['when']}")
            continue
        due = when.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        try:
            post = buffer.schedule_text(channel, e["text"], due)
            print(f"::notice title=排上了::{label} 洛杉矶 {e['when']} dueAt={post['dueAt']} status={post['status']}")
        except Exception as err:
            failed = True
            print(f"::error title=没排上::{label}: {err}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
