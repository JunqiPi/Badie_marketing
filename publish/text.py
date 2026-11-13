"""把 content/threads.json 里用户确认过的帖子排进 Buffer，到点由 Buffer 自动发到 Threads（带图的可以同步到 Instagram）。

- 只排 "approved": true 的：帖子先给用户看，用户确认了才标。
- "approved" 改回 false 的：如果还在队列里没发，就撤下来。
- 可以带一张图："image" 写仓库里的路径（放在 content/media/），"alt" 写给看不见图的人的说明。
- 多张图（能左右滑）："images": [{"path": ..., "alt": ...}, …]，顺序就是发出去的顺序。
- 可以带一条自己的回复："reply" 写文字，"reply_image" 和 "reply_alt" 是回复里的图。用来放 App 的名字、截图和链接。
- 改了已经排上的帖子的图或回复：加 "replace": true 推一次，换完把它去掉。改时间不用加，脚本自己会重排。
- 同步到 Instagram："instagram": {"text": 配文, "when": 可选的另一个时间}。必须有图；配文里的链接点不了，写 link in bio。
- 改了已经排上的帖子的文字：直接改，脚本会把同一时间排着的旧文字撤掉。
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


# 已经在 Buffer 里的帖子的状态，最后合成一条提示（GitHub 每一步最多显示 10 条提示）
STATUS = []


def parse_due(text):
    return datetime.datetime.strptime(text[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)


def sync(channel, have, wanted, label, approved, text, when_text, images, reply, replace, now):
    """把一条帖子在一个频道上排好（或撤下来）。出错返回 True。"""
    name = channel["service"]
    h = have.get(text)
    if not approved:
        # 没确认（或者确认后又撤回）的：如果还排在队列里，就撤下来
        if h and h["status"] == "scheduled":
            try:
                buffer.delete_post(h["id"])
                print(f"::notice title=撤下来了::{name} {label} 原定 dueAt={h['dueAt']}")
            except Exception as err:
                print(f"::error title=没撤成::{name} {label}: {err}")
                return True
        elif h:
            print(f"::warning title=已经发出去了，撤不了::{name} {label} status={h['status']}")
        return False
    when = datetime.datetime.strptime(when_text, "%Y-%m-%d %H:%M").replace(tzinfo=LA)
    if h:
        # 改了时间、补了图，或者标了 "replace": true（图或回复改过）：把队列里的旧版撤掉重排
        moved = h["status"] == "scheduled" and h.get("dueAt") and parse_due(h["dueAt"]) != when.astimezone(datetime.timezone.utc)
        wants_swap = replace or moved or (images and not h.get("assets"))
        if wants_swap and h["status"] == "scheduled":
            buffer.delete_post(h["id"])
            print(f"::notice title=撤掉旧版重排::{name} {label}")
        else:
            STATUS.append(f"{name} {label} {h['status']} {h.get('dueAt')}")
            return False
    if when <= now:
        print(f"::warning title=时间已过，没排::{name} {label} when={when_text}")
        return False
    due = when.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # 文字改过的帖子：队列里同一时间还排着旧文字的那条（清单里已经没有它了），先撤掉，不然会发两条
    for old_text, old in list(have.items()):
        if old["status"] == "scheduled" and old_text not in wanted and old.get("dueAt") and parse_due(old["dueAt"]) == when.astimezone(datetime.timezone.utc):
            try:
                buffer.delete_post(old["id"])
                del have[old_text]
                print(f"::notice title=撤掉旧文字::{name} {old_text[:12]}")
            except Exception as err:
                print(f"::error title=旧文字没撤成::{name} {old_text[:12]}: {err}")
                return True
    try:
        post = buffer.schedule_text(channel, text, due, images, reply)
        print(f"::notice title=排上了::{name} {label} 洛杉矶 {when_text} status={post['status']} 图={len(post.get('assets') or [])} 回复={'有' if reply else '无'}")
    except Exception as err:
        print(f"::error title=没排上::{name} {label}: {err}")
        return True
    return False


def main():
    entries = json.loads((ROOT / "content/threads.json").read_text(encoding="utf-8"))
    by_service = {}
    for c in buffer.channels():
        by_service.setdefault(c["service"], []).append(c)
    if len(by_service.get("threads", [])) != 1:
        raise SystemExit(f"::error::Buffer 里应该正好有一个 Threads 频道，现在是 {len(by_service.get('threads', []))} 个")
    threads = by_service["threads"][0]
    have = buffer.existing_texts(threads)
    # Instagram 只在有帖子要同步时才用到
    instagram = by_service["instagram"][0] if len(by_service.get("instagram", [])) == 1 else None
    have_instagram = buffer.existing_texts(instagram) if instagram else {}
    now = datetime.datetime.now(LA)
    failed = False

    def media_url(path):
        if not (ROOT / path).is_file():
            raise FileNotFoundError(path)
        # 用这次提交的固定网址，之后分支再变，图也还在
        return f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{os.environ['GITHUB_SHA']}/{path}"

    # 每个频道上确认过、应该在队列里的文字（用来认出“文字改过、旧的还排着”的帖子）
    wanted = {e["text"] for e in entries if e.get("approved") is True}
    wanted_instagram = {e["instagram"]["text"] for e in entries if e.get("approved") is True and e.get("instagram")}

    for e in entries:
        label = e["text"][:12]
        approved = e.get("approved") is True
        try:
            # "image" + "alt" 是一张图；"images" 是多张，每项 {"path": ..., "alt": ...}
            images = [{"url": media_url(e["image"]), "alt": e.get("alt")}] if e.get("image") else []
            images += [{"url": media_url(item["path"]), "alt": item.get("alt")} for item in e.get("images", [])]
            reply = None
            if e.get("reply"):
                reply = {"text": e["reply"],
                         "images": [{"url": media_url(e["reply_image"]), "alt": e.get("reply_alt")}] if e.get("reply_image") else []}
        except FileNotFoundError as err:
            failed = True
            print(f"::error title=图片不在仓库里::{label}: {err}")
            continue
        replace = e.get("replace") is True
        failed |= sync(threads, have, wanted, label, approved, e["text"], e["when"], images, reply, replace, now)
        ig = e.get("instagram")
        if ig:
            if not instagram:
                failed = True
                print(f"::error title=Buffer 里没有唯一的 Instagram 频道::{label}")
            elif not images:
                failed = True
                print(f"::error title=Instagram 的帖子必须有图::{label}")
            else:
                failed |= sync(instagram, have_instagram, wanted_instagram, label, approved, ig["text"], ig.get("when", e["when"]),
                               images, None, replace, now)
    if STATUS:
        print("::notice title=已经在 Buffer 里的::" + " | ".join(STATUS))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
