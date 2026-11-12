# Badie 宣传

Badie（免费的羽毛球找搭子 App，网站 https://badie.rsvp）的宣传仓库，**2026-11-12 起公开**：不写任何邮箱、密钥、私人信息，`queue/` 不进 git。产品代码在公开仓库 [JunqiPi/Badie](https://github.com/JunqiPi/Badie)，不在这里。

## 先读

- 能说什么：Badie 仓库的 [`Badie-iOS/docs/STORY.md`](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/STORY.md)。只说做到了的事。
- 怎么说：[`Badie-iOS/docs/VOICE.md`](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/VOICE.md)。社交平台的帖子和视频按最后一节“社交平台的帖子和视频”写，App 和网站的平实规则不适用于帖子。
- 宣传规矩、品牌素材、平台现状：[`Badie-iOS/docs/MARKETING_BRIEF.md`](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/MARKETING_BRIEF.md)。
- 打法和日程：本仓库 `docs/GROWTH_PLAN.md`。
- 这几份和本仓库冲突时，以 Badie 仓库为准；要改口径，先改 Badie 仓库里的那份。

## 和用户合作

- **用中文回复**，话要短，给推荐，不列一长串选项。
- **品牌账号也要先给用户看**（用户 2026-11-12 改的，取代 11-08 的“自动发不用问”）：每条视频、帖子做好后先发给用户，用户确认质量后，才在 `content/schedule.json` 里标 `"approved": true`，发布任务只发标过的。用户说“这类以后不用看”之前，都这样。
- **品牌账号**：Instagram、TikTok、YouTube 都叫 badiebadminton，用品牌专用邮箱注册（邮箱不写进仓库：本仓库 2026-11-12 起是公开的）。发布通过 Buffer 的 API，密钥在 GitHub Secrets 的 `BUFFER_API_KEY`。
- **其他的发之前还是先问**：用户私人账号（小红书、Reddit 等）上的任何东西、私信、邮件、花钱，整理成一批，用户回“发”之后才发。确认后再改任何一个字，要重新确认那一条。
- **密钥不进聊天、不进仓库**：让用户填到 GitHub Secrets（比如 `GEMINI_API_KEY`）。不在任何地方写用户的私人邮箱。仓库里不写模型名。
- **不做**：买粉刷量、开小号、冒充普通球友、批量私信或评论、破解验证码、在小红书放外链或导流到微信、用 AI 托管工具自动发小红书、AI 配音不打标签、编造用户评价和对话。
- 遇到验证码、短信码、限流、违规提示、登录失效，停下来告诉用户，不自己绕。
- **调研**：分辨营销和事实；更看重真实用户的反馈（社交媒体）。有论文支持可以加分。没有论文但被广泛认可的产品也算合理，不要过于悲观。
- **依赖版本写死**，用发布满两周的版本。
- **推送**：说“推到 main”才推 main，平时推会话指定的开发分支。不开 PR，除非用户要。

## 仓库结构

- `docs/GROWTH_PLAN.md`：到 2027 年中的增长方案（2026-11-08 重写）。
- `docs/WRITING.md`：帖子怎么写才像创始人本人、禁用词、发前检查。
- `docs/MASCOT.md`：品牌账号的人设 Claudia（虚拟萌妹人格，不藏着是虚拟的）：口气、句子库、评论区回复。没有形象图。
- `docs/TEXT_STUDY.md`、`docs/IMAGE_TEXT_STUDY.md`、`docs/VIDEO_STUDY.md`：真人和成功案例的拆解（文字帖、图文和引流、视频）。写任何内容之前先看对应的那份。
- `video/`：做竖版宣传视频。`scripts/*.json` 是视频脚本（配音、画面大字、画面来源），`make_video.py` 合成，`render.cjs` 画每个画面。
- `setup.sh`：旧的 Mac 安装脚本（还是 Kokoro 配音），要改成 Qwen3-TTS 后再用。
- `queue/`：每天待发的批次和发帖记录（不进 git）。

## 素材

- **iOS 界面**：宣传画面用 App 的真实界面，不用网站截图。来源是 Badie 仓库的两个 GitHub Actions：
  - `review-walkthrough.yml`：模拟器录屏（演示数据），可以按语言重新跑。
  - `app-store-screenshots.yml`：10 种语言、每种 8 张带标题的截图。
  - 演示数据里的聊天记录和排行榜名字是编的，宣传里不要用这两页。
- **配音**：2026-11-08 用户选定 3 个固定声音，用开源的 Qwen3-TTS（Apache-2.0，可商用）在本地生成：`video/voices/` 里是参考音，`video/voice.py` 照着参考音念，每条都是同一个声音。`zh` 中文（软萌少女音）、`en` 英文（甜美可爱）、`en-male` 英文备用（阳光男生）。都是 AI 设计的声音，没有克隆真人。每条都标“AI 配音”。试听用 `python video/say.py zh out.wav "台词"`。
