# Badie 宣传

Badie（免费的羽毛球找搭子 App，网站 https://badie.rsvp）的宣传仓库，**私有**。产品代码在公开仓库 [JunqiPi/Badie](https://github.com/JunqiPi/Badie)，不在这里。

## 先读

- 能说什么：Badie 仓库的 [`Badie-iOS/docs/STORY.md`](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/STORY.md)。只说做到了的事。
- 怎么说：[`Badie-iOS/docs/VOICE.md`](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/VOICE.md)。社交平台的帖子和视频按最后一节“社交平台的帖子和视频”写，App 和网站的平实规则不适用于帖子。
- 宣传规矩、品牌素材、平台现状：[`Badie-iOS/docs/MARKETING_BRIEF.md`](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/MARKETING_BRIEF.md)。
- 打法和日程：本仓库 `docs/GROWTH_PLAN.md`。
- 这几份和本仓库冲突时，以 Badie 仓库为准；要改口径，先改 Badie 仓库里的那份。

## 和用户合作

- **用中文回复**，话要短，给推荐，不列一长串选项。
- **发帖前给用户确认一次**：每天的帖子、视频、评论回复、私信、邮件整理成一批，用户回“发”之后才发。确认后再改任何一个字，要重新确认那一条。
- **密钥不进聊天、不进仓库**：让用户填到 GitHub Secrets（比如 `GEMINI_API_KEY`）。不在任何地方写用户的私人邮箱。仓库里不写模型名。
- **不做**：买粉刷量、开小号、冒充普通球友、批量私信或评论、爬商业平台、破解验证码、在小红书放外链或导流到微信、用 AI 托管工具自动发小红书、AI 配音不打标签、编造用户评价和对话。
- 遇到验证码、短信码、限流、违规提示、登录失效，停下来告诉用户，不自己绕。
- **调研**：分辨营销和事实；更看重真实用户的反馈（社交媒体）。有论文支持可以加分。没有论文但被广泛认可的产品也算合理，不要过于悲观。
- **依赖版本写死**，用发布满两周的版本。
- **推送**：说“推到 main”才推 main，平时推会话指定的开发分支。不开 PR，除非用户要。

## 仓库结构

- `docs/GROWTH_PLAN.md`：第一个月的增长方案。
- `video/`：做竖版宣传视频。`scripts/*.json` 是视频脚本（配音、画面大字、画面来源），`make_video.py` 合成，`render.cjs` 画每个画面。
- `setup.sh`：在 Mac 上装好 ffmpeg、Node、Python 依赖和配音模型，并做一条样片。
- `queue/`：每天待发的批次和发帖记录（不进 git）。

## 素材

- **iOS 界面**：宣传画面用 App 的真实界面，不用网站截图。来源是 Badie 仓库的两个 GitHub Actions：
  - `review-walkthrough.yml`：模拟器录屏（演示数据），可以按语言重新跑。
  - `app-store-screenshots.yml`：10 种语言、每种 8 张带标题的截图。
  - 演示数据里的聊天记录和排行榜名字是编的，宣传里不要用这两页。
- **配音**：目前用的是本地的 Kokoro，只用来试流程。正式配音用 Gemini 3.8 Flash TTS（真人盲听的排行榜上排在前五，API 有免费额度），中文效果不好就换 Qwen-Audio 对比。每条都标“AI 配音”。
