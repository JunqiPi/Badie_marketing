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
- **密钥不进聊天、不进仓库**：让用户填到 GitHub Secrets（比如 `GEMINI_API_KEY`）。不在任何地方写用户的私人邮箱。
- **不做**：买粉刷量、开小号、冒充普通球友、批量私信或评论、破解验证码、在小红书放外链或导流到微信、用 AI 托管工具自动发小红书、AI 配音不打标签、编造用户评价和对话。
- 遇到验证码、短信码、限流、违规提示、登录失效，停下来告诉用户，不自己绕。
- **调研**：分辨营销和事实；更看重真实用户的反馈（社交媒体）。有论文支持可以加分。没有论文但被广泛认可的产品也算合理，不要过于悲观。
- **依赖版本写死**，用发布满两周的版本。
- **推送**：说“推到 main”才推 main，平时推会话指定的开发分支。不开 PR，除非用户要。

## 每天自动跑的任务

- **Claudia 每天逛羽毛球圈**（云端定时任务，在用）：每天 UTC 04:30（洛杉矶冬令时晚上 8:30，夏令时会变成 9:30）。管理页面：https://claude.ai/code/routines/trig_018cQQGyCJEEAvhxyKuct2ro
  - 只读公开页面：看我们自己帖子的数据、逛 Threads 上的羽毛球帖子、学新的梗和什么内容有流量、挑最多一条值得回的帖子写回复草稿、写两三条新帖草稿。不登录、不发帖、不留言、不动发布队列。草稿照常要用户确认才发。
  - 产出：每次运行的最后一条消息；文件推到 `claude/surf` 分支的 `notes/surf/日期.md` 和 `docs/TRENDS.md`（这个分支不触发发布）。**开工前先 `git fetch origin claude/surf` 看有没有新笔记。**
  - 2026-11-12 实测过：它在云端读得到 Threads 搜索页上的真实帖子和互动数，一次约两三分钟。读不到的：不登录时，带地名或多个词的搜索返回“无结果”，所以搜不到洛杉矶的帖子；每个搜索页只看得到前三四条。
  - 模型是用户指定的；每天的用量是写在任务说明里的软上限（最多 15 次网页搜索或抓取、约 20 分钟），系统不强制，也没有地方设思考强度。
  - 回复别人的帖子：用户同意“特别适合的可以回”，但 Threads 官方接口要过审核才能回别人的帖子，Buffer 也不行，所以只出草稿和链接，由用户自己贴。
- **托管 Agent 版（`agents/`、`environments/`、`deployments/`，用 `ant apply` 管）：已暂停。** 它能设 medium 和每次运行的美元硬上限（2.50），但 Anthropic 服务器端的网页抓取工具屏蔽 Threads（返回 `url_not_allowed`），读不了帖子，所以不能用来逛 Threads。留着备用，适合不需要读 Threads 的定时任务。恢复：`ant beta:deployments unpause --deployment-id depl_01VRD68Q5E7ccivkcJQZcv1h`。
- 这台电脑上装了 `ant` 命令行（在用户目录的 `bin/ant.exe`），用用户的 Anthropic 账号登录过。登录会过期，过期了要用户重新授权（`ant auth login --no-browser`，用户在手机上拿验证码）。

## 已经验证过的

- 2026-11-12 晚 7:30（洛杉矶）第一条 Threads 帖按时发出：Buffer 到点自动发，带图也行。未登录看主页，帖子上没有 AI 标签。

- **看帖子的数据**：`git push -f origin claude/publish:claude/buffer-check` 会跑一次只读检查，结果在那次运行的提示里：每条已发帖子的浏览、赞、评论、转发（Buffer 从平台取回来的，有几小时延迟）。未登录的网页只看得到粉丝数和帖子，看不到赞和浏览。
- 2026-11-13 第一次读数：粉丝 0；第一条（看教学）发出 13 小时后 3 次浏览、0 赞。
- Buffer 的接口发 Threads 帖子时不能带话题标签（只有链接卡片、地点、串帖）；Instagram 可以带第一条评论。

## 待办

- **等级卡**（2026-11-13 卡片已上线）：Claudia 的卡是 `content/media/claudia-card.png`（3−、Iron wall；按她的设定答题，用网站同一套算法算的；人物剪影换成了她，是只有她有的特别版，用户选的）。
  - 第一次用：11-13 中午那条 "everyone says they're intermediate" 下面的自己回复。
  - 卡片是在本机用 Badie 仓库 `web/src/app/levelCard.ts` 渲染的，没有在 App 里给 Claudia 建账号。卡片改版后要重新渲染。
  - 更新宣传帖（“主人居然做了个等级卡”）：用户 2026-11-13 确认了英文版，排在 11-14 中午，Threads 和 Instagram 各一条。
- **Instagram 图文**（用户 2026-11-13 同意）：带图的帖子同步到 Instagram，在 `content/threads.json` 的那一条里加 `"instagram": {"text": 配文}`。第一条是 11-14 中午的等级卡；Buffer 已经接受排期，**发出去以后要去主页看一眼才算验证过**。配文里的链接点不了，写 link in bio，简介里的链接由用户放。
- **Product Hunt**（2026-11-13）：用户账号下有一条 “Badie” 的草稿，已填好：主链接是网站，App Store 是附加链接，4 张展示图（封面加 3 张用商店截图拼的三联图），介绍、创始人留言、分类。**没有提交，没有定日期**：等 iPhone 1.0.5 上架后再定；提交前把全文给用户看，用户说可以才提交。连接方式是 Product Hunt 的 MCP 服务，登录凭证只在本机临时目录，过期了要用户重新点一次登录链接。预期：那里是做产品的人，带不来多少球友，图的是外链和反馈。
- **价格帖**（“LABC 一天十块 Elite 十五 SGVBC 十四 你们常去哪家”）：Elite $15、SGVBC $14 在 2026-11-12 对过球馆自己的订场系统；LABC 官网写 $9/$10，没说哪天是 9。等用户说清楚再发。
- **英文帖**：草稿在本机 `queue/threads-batch-01-en.md`，等用户看。

## 仓库结构

- `docs/GROWTH_PLAN.md`：到 2027 年中的增长方案（2026-11-08 重写）。
- `docs/WRITING.md`：帖子怎么写才像创始人本人、禁用词、发前检查。
- `docs/MASCOT.md`：品牌账号的人设 Claudia（虚拟萌妹人格，不藏着是虚拟的）：口气、句子库、评论区回复。形象是简笔画（用户 2026-11-12 确认），参照图是 `content/media/claudia-sheet.png`。
- `docs/TEXT_STUDY.md`、`docs/IMAGE_TEXT_STUDY.md`、`docs/VIDEO_STUDY.md`：真人和成功案例的拆解（文字帖、图文和引流、视频）。写任何内容之前先看对应的那份。
- `video/`：做竖版宣传视频。`scripts/*.json` 是视频脚本（配音、画面大字、画面来源），`make_video.py` 合成，`render.cjs` 画每个画面。
- `setup.sh`：旧的 Mac 安装脚本（还是 Kokoro 配音），要改成 Qwen3-TTS 后再用。
- `queue/`：待用户确认的草稿（不进 git）。
- `content/threads.json`：用户确认过的 Threads 文字帖和发布时间；`publish/text.py` 把它们排进 Buffer。

## 素材

- **iOS 界面**：宣传画面用 App 的真实界面，不用网站截图。来源是 Badie 仓库的两个 GitHub Actions：
  - `review-walkthrough.yml`：模拟器录屏（演示数据），可以按语言重新跑。
  - `app-store-screenshots.yml`：10 种语言、每种 8 张带标题的截图。
  - 演示数据里的聊天记录和排行榜名字是编的，宣传里不要用这两页。
- **配音**：2026-11-08 用户选定 3 个固定声音，用开源的 Qwen3-TTS（Apache-2.0，可商用）在本地生成：`video/voices/` 里是参考音，`video/voice.py` 照着参考音念，每条都是同一个声音。`zh` 中文（软萌少女音）、`en` 英文（甜美可爱）、`en-male` 英文备用（阳光男生）。都是 AI 设计的声音，没有克隆真人。每条都标“AI 配音”。试听用 `python video/say.py zh out.wav "台词"`。
