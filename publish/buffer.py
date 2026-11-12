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


def channels():
    orgs = gql("query { account { organizations { id } } }")["account"]["organizations"]
    found = []
    for o in orgs:
        found += gql(
            "query($id: OrganizationId!) { channels(input: {organizationId: $id}) "
            "{ id name displayName service isQueuePaused } }",
            {"id": o["id"]},
        )["channels"]
    return found


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
