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

## 目标和打法（2026-11-17 用户定）

- 目标：**2027 年中每日千人活跃**。当天 34 个账号、每天新增两三个，来源标记全空。
- 主线：拉“组局的人”用球群（每周报名、候补自动递补），对象是大学羽毛球社、Meetup 群、本地社群。外联话术面向组织者，结尾问愿不愿意合作。
- 底盘：球馆和价格页的搜索流量。访问数在 Cloudflare Web Analytics，要用户的 Cloudflare 账号，我没有登录。
- 报数时 App 活跃和网站访问分开。
- 1 月底检查点：10 个球群在真实使用；网站每天 300 个搜索访问。不达标就换打法。

## 已经验证过的

- 2026-11-12 晚 7:30（洛杉矶）第一条 Threads 帖按时发出：Buffer 到点自动发，带图也行。未登录看主页，帖子上没有 AI 标签。

- **看帖子的数据**：`git push -f origin claude/publish:claude/buffer-check` 会跑一次只读检查，结果在那次运行的提示里：每条已发帖子的浏览、赞、评论、转发（Buffer 从平台取回来的，有几小时延迟）。未登录的网页只看得到粉丝数和帖子，看不到赞和浏览。
- 2026-11-13 第一次读数：粉丝 0；第一条（看教学）发出 13 小时后 3 次浏览、0 赞。
- Buffer 的接口发 Threads 帖子时不能带话题标签（只有链接卡片、地点、串帖）；Instagram 可以带第一条评论。
- **Threads 改成用浏览器发**（2026-11-17 用户定）：没挂话题的帖子几乎没人看得到（8 条帖子 30 天一共 14 次浏览）。现在用 Claude in Chrome 在 threads.com 上发，发帖框里点“社群或话题”选 **Badminton**；图片用 file_upload 传；链接放在串文的第二条。旧帖 11-17 全部删了，按“上线帖、价格表、等级卡、Claudia 的碎碎念（只发英文的）”的顺序每天重发一条，上线帖已发（球馆数改成 13,000+ courts in 126 countries，数据库当天是 13,290 家、126 个国家）。Instagram 还是走 Buffer。
- **外联**（2026-11-17）：品牌号已关注 @usc.badminton、@uclabadminton、@sgv_badminton_club、@baddixxla，前两个各留了一条评论。私信用 Claudia 的口气，每条发之前给用户看。目标是全美，不只洛杉矶；高中社团不发。11-17 已给这四个账号各发了一条私信（结尾请对方试用、转给 group），等回复；以后的私信结尾加一句愿不愿意合作。
  - 11-17 晚又关注并私信了 @husky.badminton（UW）、@nyubadminton、@stanford_badminton，用的是面向组织者的写法（用户改过的版本：报名、候补自动递补；不提记账，球群没有“谁付了钱”的功能；不说替对方建演示群）。
  - Meetup 账号已登录，名字改成 Claudia from Badie。不加群也能看到组织者的 Message 按钮，但新账号给没有共同群的人发消息发不出去（点发送没反应，收件箱是空的）；加入同一个群后就能发。11-17 加入了 NYC Outdoor Badminton（公开群），给组织者 William Young 发了消息。南加州那两个群（`/badminton-61`、`/labadminton`）是私密群，申请时要填水平、一张能看清脸的本人照片等，Claudia 是虚拟人物，不能编答案、不能用别人的照片，所以没申请。
  - 11-18 早上 Threads 发了价格表（挂 Badminton 话题）。前一天重发的上线帖 23 小时只多了约 2 次浏览，话题基本没带来人。
  - 第三批候选（11-18 看过，都在更新，没关注没发）：Instagram 的 @badminton_ucd（UC Davis，1483，刚打进全国赛）、@ucsdbadminton（2044）、@rutgersbadminton（1644）；Meetup 公开群 Badminton Net-flix and Kill（`/badminton-net-flix-and-kill`，Fremont，组织者 Lee，13 场待办）、Smash Badminton Boston（`/smash-badminton-boston`，MIT，组织者 kamehamehon）。Boston Badminton Westboro 是私密群。其他城市的 Meetup 群大多停办了。
  - 11-18 第三批：Instagram 关注并私信了 UC Davis、UCSD、Rutgers（加了用户要的一句：we really want to help badminton communities grow…）。Meetup 加入了 Badminton Net-flix and Kill，但给组织者 Lee 的消息被 Meetup 的反垃圾保护拦下（提示让改写再发）：按规矩停了，没改写重试，Boston 那条也没发。纽约那条和这条内容几乎一样，可能是同样的文字发第二次被判成群发。以后 Meetup 每条要按对方的群单独写，一天最多一两条。
  - **11-18 第一个回复：BADDIXX LA 说 “Hello yes we're interested”**。回了：问他们周二在 SGVBC 怎么收报名、多少人；教他们 “+ → Regular games · Groups” 建每周场次；照实说现在要注册、12 月初有免注册的链接报名；提了正在做的循环赛工具请他们给意见。等回复。
  - 找群主的办法：关键词搜效果很差；看本地球馆（SGVBC）关注了谁最有效。11-18 关注了 @pbca2026（Philippine Badminton Club of America，在 SGVBC 打，办杯赛；刚和圣地亚哥的 SBBS 办了友谊赛），私信草稿给用户看了，还没发。其他：@pickleballbadmintoncenter（Lakewood 球馆）、@joy_badminton（用品店，以后谈合作）。
  - 其他候选：@uiuc.badminton（1042）和 @utbadmintonclub（929）主页上没看到“发消息”按钮，@ucibadminton 也是。
  - Meetup（11-17 看过，都还在办活动）：NYC Outdoor Badminton（`/nyc-outdoor-badminton`，1 万人，每周六中央公园 70 人到场）、Southern California Badminton Meetup Group（`/badminton-61`，2643 人，周末在 LABC）、Badminton in Bay Area（`/badmintoninbayarea`，2153 人，收费入门课）、Los Angeles Badminton Meetup（`/labadminton`，1417 人）。Meetup 还没登录：用品牌邮箱走 Google 登录时，扩展不能操作 Google 的登录页，要用户自己点一下账号。

## 待办

- **等级卡**（2026-11-13 卡片已上线）：Claudia 的卡是 `content/media/claudia-card.png`（3−、Iron wall；按她的设定答题，用网站同一套算法算的；人物剪影换成了她，是只有她有的特别版，用户选的）。
  - 第一次用：11-13 中午那条 "everyone says they're intermediate" 下面的自己回复。
  - 卡片是在本机用 Badie 仓库 `web/src/app/levelCard.ts` 渲染的，没有在 App 里给 Claudia 建账号。卡片改版后要重新渲染。
  - 更新宣传帖（“主人居然做了个等级卡”）：用户 2026-11-13 确认了英文版，排在 11-14 中午，Threads 和 Instagram 各一条。
- **Instagram 图文**（用户 2026-11-13 同意）：带图的帖子同步到 Instagram，在 `content/threads.json` 的那一条里加 `"instagram": {"text": 配文}`。第一条是 11-14 中午的等级卡；Buffer 已经接受排期，**发出去以后要去主页看一眼才算验证过**。配文里的链接点不了，写 link in bio，简介里的链接由用户放。
- **上线帖**（用户 2026-11-13 确认）：排在 11-15 中午，Threads 和 Instagram 各一条，8 张图（`content/media/launch/`，封面是 Claudia，后面是 App Store 截图的上半截）。这是第一次发多图，也是第一次发 Instagram 多图，**发出后要去两个主页看一眼**。发出后提醒用户：手动置顶；每月 20 美元的推广用这条（在电脑网页上点推广，不在 iPhone 的 App 里付，苹果抽 30%；目标是访问网站，链接带 `?ref=ig_ad`，人群是洛杉矶周边 25 英里、对羽毛球感兴趣，每天 5 美元跑 4 天）。
- 正式宣发帖说 we，不说 boss；Instagram 配文末尾带 `#badminton #badmintonlovers #badmintonplayer`，Threads 不带。
- **Product Hunt**：2026-11-14 已提交，**排在 11-17 太平洋时间零点上线**（用户确认了全文）。主链接是网站，App Store 是附加链接；封面加 7 张网站截图；介绍和创始人留言是按用户本人口气写的那版（“I made this because I'm bad at saying hi.”）。编辑页：https://www.producthunt.com/posts/badie/edit 。上线当天有人留言时，回复稿先写给用户，由用户自己贴。提交后再改公开内容要用户再确认一次。预期：那里是做产品的人，带不来多少球友，图的是外链和反馈。连接用 Product Hunt 的 MCP 服务（用户已在 Claude Code 里加好）。
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
