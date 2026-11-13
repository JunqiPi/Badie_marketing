"""Buffer API（GraphQL）：查频道、发视频帖。密钥从环境变量 BUFFER_API_KEY 读，不打印。

用法：
  python publish/buffer.py channels
"""
import json
import os
import sys
import urllib.request

API = "https://api.buffer.com"


def gql(query, variables=None):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["BUFFER_API_KEY"],
            "User-Agent": "badie-marketing",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if out.get("errors"):
        raise SystemExit("Buffer 报错：" + "; ".join(e.get("message", "") for e in out["errors"]))
    return out["data"]


def org_ids():
    return [o["id"] for o in gql("query { account { organizations { id } } }")["account"]["organizations"]]


def channels():
    found = []
    for oid in org_ids():
        chans = gql(
            "query($id: OrganizationId!) { channels(input: {organizationId: $id}) "
            "{ id name displayName service isQueuePaused } }",
            {"id": oid},
        )["channels"]
        for c in chans:
            c["organizationId"] = oid
        found += chans
    return found


def existing_texts(channel):
    """这个频道里已经排着或已经发出去的帖子的文字，用来防止重复发。"""
    data = gql(
        "query($input: PostsInput!) { posts(first: 100, input: $input) "
        "{ edges { node { id text status dueAt assets { mimeType } } } } }",
        {"input": {"organizationId": channel["organizationId"],
                   "filter": {"channelIds": [channel["id"]], "status": ["scheduled", "sending", "sent"]}}},
    )["posts"]["edges"]
    return {e["node"]["text"]: e["node"] for e in data}


def _assets(image_url, alt):
    if not image_url:
        return []
    image = {"url": image_url}
    if alt:
        image["metadata"] = {"altText": alt}
    return [{"image": image}]


def schedule_text(channel, text, due_at_utc, image_url=None, alt=None, reply=None):
    """排一条帖子，到点自动发（不是提醒）。可以带一张图，也可以带一条自己的回复。
    due_at_utc 形如 2026-11-13T03:30:00.000Z。图片要是公开网址，Buffer 到发的时候才去取。
    reply 是 {"text": ..., "image_url": ..., "alt": ...}：发在主帖下面的第一条回复，
    用来放 App 的名字、截图和链接（主帖本身不放链接，带链接的帖子互动最低）。
    不设 aiAssisted：文字帖平台不要求标 AI，用户定了没人问不主动说（MASCOT.md 第 1 节）。"""
    assets = _assets(image_url, alt)
    payload = {"text": text, "channelId": channel["id"], "schedulingType": "automatic",
               "mode": "customScheduled", "dueAt": due_at_utc, "assets": assets}
    if channel["service"] == "instagram":
        # 图文帖（不是 Reels）。不标 AI：和 Threads 的图一样，用户定了没人问不主动说
        payload["metadata"] = {"instagram": {"type": "post", "shouldShareToFeed": True}}
    if reply:
        # Buffer 的要求：thread 里要列出全部帖子，第一项是主帖，文字和上面的 text 一样
        payload.setdefault("metadata", {})[channel["service"]] = {"thread": [
            {"text": text, "assets": assets},
            {"text": reply["text"], "assets": _assets(reply.get("image_url"), reply.get("alt"))},
        ]}
    data = gql(
        """mutation($input: CreatePostInput!) { createPost(input: $input) {
             ... on PostActionSuccess { post { id dueAt status assets { mimeType } } }
             ... on MutationError { message } } }""",
        {"input": payload},
    )["createPost"]
    if "message" in data:
        raise RuntimeError(data["message"])
    return data["post"]


def delete_post(post_id):
    """删掉一条还没发出去的帖子。"""
    data = gql(
        "mutation($input: DeletePostInput!) { deletePost(input: $input) "
        "{ __typename ... on VoidMutationError { message } } }",
        {"input": {"id": post_id}},
    )["deletePost"]
    if data.get("message") or data["__typename"] != "DeletePostSuccess":
        raise RuntimeError(data.get("message") or data["__typename"])


def metadata(service, title):
    """各平台的设置。都声明用了 AI（配音是 AI 的）。"""
    if service == "instagram":
        return {"instagram": {"type": "reel", "shouldShareToFeed": True, "isAiGenerated": True}}
    if service == "youtube":
        return {"youtube": {"title": title[:100], "categoryId": "17", "madeForKids": False, "isAiGenerated": True}}
    if service == "tiktok":
        return {"tiktok": {"isAiGenerated": True}}
    return {}


def post_video(channel, video_url, text, title):
    """马上发一条视频帖（自动发布，不是提醒）。channel 是 channels() 返回的一项。"""
    data = gql(
        """mutation($input: CreatePostInput!) { createPost(input: $input) {
             ... on PostActionSuccess { post { id dueAt status } }
             ... on MutationError { message } } }""",
        {"input": {
            "text": text,
            "channelId": channel["id"],
            "schedulingType": "automatic",
            "mode": "shareNow",
            "aiAssisted": True,
            "metadata": metadata(channel["service"], title),
            "assets": [{"video": {"url": video_url, "metadata": {"thumbnailOffset": 1000}}}],
        }},
    )["createPost"]
    if "message" in data:
        raise RuntimeError(data["message"])
    return data["post"]


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "channels":
        for c in channels():
            # GitHub Actions 的 notice 备注：公开仓库不登录也能读到
            print(f"::notice title=buffer channel::{c['service']} | {c['displayName'] or c['name']} | "
                  f"paused={c['isQueuePaused']} | id={c['id']}")
    if cmd == "stats":
        # 只读：已经发出去的帖子的互动数据（Buffer 从平台取回来的）
        for c in channels():
            if c["service"] not in ("threads", "instagram"):
                continue
            edges = gql(
                "query($input: PostsInput!) { posts(first: 50, input: $input) { edges { node "
                "{ text sentAt externalLink metricsUpdatedAt metrics { name value } } } } }",
                {"input": {"organizationId": c["organizationId"], "filter": {"channelIds": [c["id"]], "status": ["sent"]}}},
            )["posts"]["edges"]
            for e in edges:
                n = e["node"]
                numbers = ", ".join(f"{m['name']}={m['value']:g}" for m in (n.get("metrics") or []) if m.get("value") is not None) or "还没有数据"
                first_line = (n["text"] or "").splitlines()[0][:40]
                print(f"::notice title={c['service']} {n.get('sentAt')}::{first_line} | {numbers} | 更新于 {n.get('metricsUpdatedAt')} | {n.get('externalLink')}")
