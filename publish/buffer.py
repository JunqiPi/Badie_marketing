"""Buffer API（GraphQL）：查频道、发视频帖。密钥从环境变量 BUFFER_API_KEY 读，不打印。

用法：
  python publish/buffer.py channels
  python publish/buffer.py post <频道id> <视频公开网址> <文案文件>
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


def post_video(channel_id, video_url, text):
    data = gql(
        """mutation($input: CreatePostInput!) { createPost(input: $input) {
             ... on PostActionSuccess { post { id dueAt status } }
             ... on MutationError { message } } }""",
        {"input": {
            "text": text,
            "channelId": channel_id,
            "schedulingType": "automatic",
            "mode": "addToQueue",
            "assets": [{"video": {"url": video_url, "metadata": {"thumbnailOffset": 1000}}}],
        }},
    )["createPost"]
    if "message" in data:
        raise SystemExit("Buffer 没收：" + data["message"])
    return data["post"]


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "channels":
        for c in channels():
            # GitHub Actions 的 notice 备注：公开仓库不登录也能读到
            print(f"::notice title=buffer channel::{c['service']} | {c['displayName'] or c['name']} | "
                  f"paused={c['isQueuePaused']} | id={c['id']}")
    elif cmd == "post":
        _, _, cid, url, textfile = sys.argv
        print(post_video(cid, url, open(textfile, encoding="utf-8").read()))
