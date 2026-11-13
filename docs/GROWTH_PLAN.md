# Badie 到 2027 年中的增长方案

> 2026-11-08 重写（同日加上：品牌账号由 AI 吉祥物小羽来发，自动发不用问），取代 11-03 那版（那版靠创始人联系群主、每天手动发帖，和现在的条件不符）。
> 口径以 Badie 仓库的 [STORY.md](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/STORY.md) 为准，做事的规矩以 [MARKETING_BRIEF.md](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/MARKETING_BRIEF.md) 和本仓库 `CLAUDE.md` 为准。写法见 `docs/WRITING.md`。
> 证据分三档：**[论文]** 同行评审；**[公认]** 平台官方规则或被很多产品验证过；**[个案]** 单个案例或自述。

## 0. 条件和目标

**条件**（用户 2026-11-08 定的）
- 创始人不主动联系任何人：不找群主、不私信、不发邮件、不出镜。
- 每天花的时间尽量是 0。
- 预算 50–100 美元。
- 住在大洛杉矶，平时在那里打球。
- 现有的小红书、TikTok、Instagram、Reddit 都是**私人账号**。

**目标：2027-06-30 前，在洛杉矶的一片区域里，Badie 成为羽毛球人真的在用的工具。**
数字定义（每月月初对一次）：
- 这片区域每周成局 ≥ 30（双方确认的球局 + 球群报名的场次）。
- 至少 3 个球群每周用 Badie 报名，替代原来的微信接龙或表格。
- 注册数只作参考，不作目标：注册涨、成局不涨，说明人来了约不到。

**要先说清楚的**：不找群主，等于放弃了最快的那条路。11-03 那版预计的注册里，一半以上来自群主和社团。所以这版的节奏是 **8 个月慢慢滚起来**，不是一个月冲 1 万。8 个月的时间正好适合搜索、球馆页这类越做越多的渠道。

## 1. 底层逻辑：调研后的 4 条

| 原则 | 依据 | 对 Badie 的意思 |
|---|---|---|
| **1. 宣传藏在产品本来就要产出的东西里** | **[论文]** Aral & Walker 2011（Management Science，Facebook 上的随机实验）：自动发给朋友的被动通知让同伴采用率提高 246%，再加上主动邀请只多 98%。**[公认]** Partiful 每张邀请都是一个落地页，靠口碑做到约 500 万用户。 | 群主每周往微信群里贴的报名链接，就是 Badie 最好的广告，而且不用你开口。这条要让工程 agent 把报名页做好（第 5 节）。 |
| **2. 不去找组织者，让组织者自己找上门** | **[个案]** Pickleheads 先做球场搜索页，每月 10 万访问后才加组织球局；PlayTime Scheduler 从萨克拉门托一个组织者的网站做到约 57 万球员；Reclub 主打“替代群聊和表格的一个报名链接”。 | 做一个“替代微信接龙”的免费工具页，让组织者在 Google、小红书、报名页底部自己看到。一个组织者带来 20–50 人。 |
| **3. 先密度，后广度；选人会主动搜的渠道** | **[论文]** Cullen & Farronato 2021（Management Science）：TaskRabbit 的撮合效率取决于本地密度。**[个案]** RacketPal 10 万用户里约一半在伦敦；用户差评最多的是“人太少”。 | 洛杉矶只选一片打透。主力渠道是人会主动搜的：Google 球馆页、小红书搜索、App Store。全国性的短视频播放量只是辅助。 |
| **4. 平台惩罚的是“没有人”，不是 AI** | **[公认]** 小红书 2026-03 起封禁 AI 托管账号，但说 AI 标签“不会影响流量”；YouTube 把 AI 写脚本列为不用声明的“轻微”用法。**[论文]** Jakesch 等 2023（PNAS）：读者分辨不出 AI 文字；Altay & Gilardi 2024：标了 AI 的内容可信度下降，原因是读者以为全程没有人参与。**[公认]** Reddit 用 AI 抓 AI 写的“自然推广”，苏黎世大学偷偷用 AI 账号发评论被全网封禁。 | “像真人”靠的不是文风技巧，而是只有你知道的真实细节：哪家球馆、星期几、谁没来。AI 负责量和格式，真实素材来自你。账号上写明“配音是 AI，App 和故事是我的”。 |

## 2. 打哪里

- **洛杉矶，先选一片**：精选球馆数据里大洛杉矶 + 橙县有 20 家，分成两片：
  - **圣盖博谷**：Los Angeles Badminton Club、San Gabriel Valley Badminton Club（El Monte）、Elite Rally（Irwindale）、Walnut、Alhambra、Pomona。华人多。
  - **橙县**：Irvine 两处、Orange County Badminton Club、Royal Badminton Academy（Lake Forest）、Fountain Valley。
  - **定了：先打圣盖博谷**（用户常去 Elite Rally、LABC，都在这片；还有 San Gabriel Valley Badminton Club 等，球馆密）。用户也常去 OCBC，所以**橙县是第二片**：第一片每周成局到 15 后再开始。
  - 宣传里讲到的球馆优先用 Elite Rally、LABC、OCBC：用户真的在那打，空镜和细节都是真的。
- **语言**：先做中文（小红书，北美华人找球局主要在这里搜），英文短视频辅助。
- **时间点**（未确认的标了）：
  - 12 月中到 1 月初：放假，学生回家。
  - **1 月**：新年计划，一年里最好拉新的窗口，内容和球馆页要在 12 月底前准备好。
  - **2027-02-06 春节**：新春球局内容。
  - 2–4 月：高中羽毛球季，可以对家长讲。
  - 5–6 月：毕业生搬到新城市，讲“刚搬来谁也不认识”。
  - 2027 年 7 月 BWF US Open 可能在洛杉矶（只有第三方网站这么写，未确认），确认后作为目标之后的第一个高峰。

## 3. 渠道：按你要花的时间分三档

### A. 你 0 分钟（全自动，或由工程 agent 做一次）

| 渠道 | 怎么做 | 为什么 |
|---|---|---|
| **球馆页和“在哪打球”搜索**（主力） | 洛杉矶那片的球馆页补上 drop-in 价格、开放时间、本周在这里打的球群、中文版。Google 和 ChatGPT 这类 AI 会引用。 | 原则 2、3。要 3–9 个月才见效，所以现在就做。**[个案]** Pickleheads 上线球场搜索后自然流量涨了 10 倍。 |
| **球群报名页**（主力） | 免登录能看、在微信里显示正式的卡片（群名、球馆、时间、已报名人数），页面底部写“你也在组织？免费建一个”。 | 原则 1：每个用 Badie 的群主，每周都在免费替我们做广告。 |
| **“替代微信接龙”页** | `/organize`，中英文：30 秒演示、把接龙名单粘进来就能建群、爽约规则、可打印的二维码海报。 | 原则 2：组织者自己找上门。 |
| **App Store 的 App 内活动** | 发每周固定的活动（比如“圣盖博谷周三晚双打 4–6 级”），会出现在 App Store 搜索里。 | **[公认]** Apple 官方免费入口，最多同时挂 10 个。 |
| **Instagram Reels + YouTube Shorts** | 新开的 Badie 品牌账号，由吉祥物小羽（公开说明是 AI，可爱的语气，见 `docs/MASCOT.md`）来发。GitHub Actions 每天自动生成 1 条，通过 Buffer（免费版：3 个频道、每个频道排 10 条，有官方 API，自己已过各平台审核，发出去是公开的）同时发到 Instagram、TikTok、YouTube Shorts：小羽 + App 真实录屏 + 你拍的球馆空镜，打开 AI 标签，发前不用问（用户 2026-11-08 同意）。 | 辅助，主要用来让人“搜到你的时候看起来是真的”，也带来一些全国流量。 |
| **TikTok** | 先提交 Content Posting API 审核（网上说要 2–6 周，未核实）；通过后和 Instagram 同一套流水线。 | 没通过审核时，用接口发的视频只有自己能看到，所以先等审核。 |
| **评论区的常见问题** | Instagram 和 YouTube 上，**自己帖子下面**的问题（免费吗、有安卓吗、哪些城市），用你写过的固定回答自动回。其他评论不回，每周把清单放进 `queue/`，想回你就回。 | 官方接口允许，只答事实，不会乱承诺。 |

### B. 每周 15 分钟（推荐，但由你决定）

**小红书**：我每周日把 5–7 篇笔记做好（图、文字、话题），放在 `queue/xhs/` 里。你在小红书创作服务平台用**官方的定时发布**一次排完。
- 这是北美华人找球局的地方，也是最可能让洛杉矶的组织者找到 Badie 的地方。放弃它，中文这条线基本就断了。
- **每周其中一篇是更新日志**（2026-11-10 加）：“独立开发的羽毛球 App，这周改了什么”，只写真的上线了的改动，结尾问大家还缺什么。小红书上独立开发者的这类笔记粉丝少也有人讨论（小红书官方说站内有 5 万多名独立开发者，是平台自己的数字）。只有真的有人提过，才能写“按大家说的改了”。
- 不能做成自动：小红书没有开放发帖接口，第三方自动发帖工具 2026-03 起会被封号。这是你的私人账号，风险太大。

### C. 不做

- **主动给博主、教练发私信或邮件**（2026-11-10 复盘后定）：和“创始人不主动联系任何人”冲突；官方接口也不允许主动给陌生人发私信，只能本人手动发。例外是 Badie 仓库 `COACHING.md` 第 2 节：先问用户认识的那一位教练。
- **X**：新开发者没有免费接口额度，看的人主要是开发者不是球友。品牌账号的自动发布流水线搭好以后，如果用户想要，再把 X 接上（按条付费，第三方说每条约 1.5 美分）。
- **Reddit 机器人**：Reddit 在专门抓 AI 写的推广，r/badminton 禁止自我推广。用私人账号跑机器人，大概率被封。
  可以做的：到 2027 年中，你最多手动发 2 条“这是我做的”介绍帖（我写好，你复制粘贴），其余时间不碰。
- 自动发小红书、在别人的帖子下面自动评论、批量私信、小号、冒充普通球友、AI 生成的假人和假球场。

## 3.5 发帖方式：像人，不像机器（用户 2026-11-12 定）

一直按点发同一种帖子很难成功。品牌账号（Instagram、YouTube、TikTok、Threads）按下面的做：

- **不追求每天一条**：一周 3–4 条视频，每条换一个钩子；数据差的钩子不再用，好的做成系列。Threads 发短文字，像随口说的话，可以一天几条也可以一天不发。
- **每条先有一个“值得发的理由”**：新功能、一个真实的球馆细节、一个能站队的问题。没有理由就不发。
- **照着被验证过的模式做，不自己发明**：
  - **测试结果卡**（MBTI、年度听歌报告那一类）：定级做简单以后，“我是羽毛球 X 级”的结果卡要能一键分享。这是产品自己传播，比任何帖子都有用。内容上发“你是几级”，让人去测、回来晒。
  - **一句话就懂的定位**：资料卡上线后，说法是“像交友软件一样刷附近的球友卡片，看谁哪天有空，右滑约球”。不提别家产品的名字。
  - **晒卡**：让球友晒自己的球友卡片（卡片背景、等级），我们转发（征得同意）。
- **蹭热点**（用户 2026-11-12 提的）：每次发帖前先看最近一周羽毛球圈什么最火，能接上就接。
  - 怎么找：YouTube 官方接口按播放量查近 7 天的羽毛球视频；网页搜索；BWF 赛历（大赛的决赛、名场面是可以提前知道的高峰）；用户刷到爆款时把链接丢过来。不爬小红书、TikTok、Instagram。
  - 怎么蹭：用自己的话和自己的画面接这个话题，当天先发 Threads 文字，值得的话第二天出视频。不在结尾总结卖点（见 `WRITING.md` 的“功能总结句”）。
  - 不做：搬运别人的视频或比赛画面（版权，会被下架）；用机器人去爆款帖子下面评论。
- **跟着产品走**：接下来两件事是内容的主线：(1) 定级变简单；(2) 像交友软件一样的资料卡、看附近的人和空闲时间、直接约球。上线前不说“已经有”。

## 4. “100% 像真人”怎么保证

不能保证 100%。真正能做到的是让每条都**有真东西**，再加三道检查：
1. **素材库**：只用你提供的真实经历和真实画面（第 7 节）。AI 不编经历、对话和数据，缺素材就不发那一类。
2. **文风锚点**：用你自己写的 10 段以上文字做样本，写法规则在 `docs/WRITING.md`。
3. **发之前自动检查**：查禁用词和 AI 腔句式（中英文各一份清单）；对照 STORY.md 核对每一句说法；同一个模板不连发三天（YouTube 2025-07 起会处理“大量重复的内容”）。
没通过检查的不发，留在 `queue/rejected/` 里，每周汇总一句话给你。

## 5. 要工程 agent 做的事（请转给 Badie 仓库那边，按重要性）

1. **球群报名页**：免登录能看名单、水平、球馆、时间、候补；在微信、iMessage 里显示正式的分享卡片；一点就报名；页面底部写“你也在组织？免费建一个”。
2. **`/organize` 页**（中英）：替代微信接龙；粘贴接龙名单导入；可打印的二维码海报（每个球馆一个码，能区分来源）。
3. **洛杉矶那片的球馆页**：drop-in 价格、开放时间（`us_venues.json` 里已经有）、本周在这里打的球群、中文版本。
4. **空状态不空**：附近配不到人时，显示附近已知的 drop-in 时段（精选数据里有时间表），不显示一个空页面。**[个案]** 约球 App 的差评最多的是“人太少”。
5. **注册后问“你从哪里知道 Badie 的”**（如果还没做）。
6. **App 内活动**：用 App Store Connect 接口发布每周固定的活动。

## 6. 时间表

| 时间 | 做什么 |
|---|---|
| **11 月** | 你：一次性设置（第 7 节，约 1–2 小时）。我：写好素材库、`WRITING.md`、前 30 条内容；搭好自动发布流水线。工程：第 5 节第 1–3 项。小红书开始每周排。 |
| **12 月** | Instagram、YouTube 自动发上线；提交 TikTok 审核。圣诞假期内容。12 月底前球馆页和 `/organize` 必须上线，赶 1 月的窗口。 |
| **1 月** | 全年最重要的一个月：新年开练内容 + App 内活动。第一次花钱测试（见第 8 节）。 |
| **2 月** | 春节（02-06）新春球局内容。月底复盘：哪个渠道带来了成局，没用的停掉。 |
| **3–4 月** | 加倍投入有效的渠道。如果第一片区域每周成局到了 15，开始给第二片做球馆页。 |
| **5–6 月** | “刚搬来洛杉矶”内容。6 月底对目标。 |

每周一我在 `queue/` 写一句话总结：发了什么、哪条最好、网站来源（Cloudflare Web Analytics 的 `?ref=`）、成局数。不需要你回复。

## 7. 需要你提供的（都是一次性的）

1. **你自己写的文字，10 段以上**：以前的小红书、朋友圈、和朋友的聊天（别人的名字删掉）。英文的也要几段（短信、Discord 都行）。这是“像你”的唯一来源。
2. **3–5 个真实经历**，一两句话就行，比如“有一次约好 4 个人只来了我一个”“刚搬到 XX 的第一个月一直一个人对墙打”。只用你说过的。
3. **球馆空镜**：下次去打球时用手机拍 10 段，每段 3–5 秒：球场、球、鞋、记分牌，不拍人脸。拍一次能用很久。
4. **品牌账号**：2026-11-11 已建好 Instagram、TikTok、YouTube，用品牌专用邮箱注册。发布走 Buffer：自己直连 YouTube 和 TikTok 的接口要先过平台审核（没过审核时，YouTube 用接口传的视频会被锁成私密，TikTok 只能自己看到），Buffer 已经过了审核。
5. **一次性设置**：开发者账号和令牌（Meta、Google、TikTok）由你登录点确认，密钥填进 GitHub Secrets。我会写一步一步的说明。

## 8. 50–100 美元怎么花

先不花，等第 5 节的报名页和球馆页上线、内容跑满一个月，知道哪条笔记最好之后：
- **1 月，30 美元**：给表现最好的那条小红书笔记投“薯条”，只投洛杉矶（海外账号能不能投还没核实，到时候在 App 里看一下）。
- **2 月，30–50 美元**：Apple Ads，精确匹配 “badminton partner” “羽毛球”，只投你选的那片。**[公认]** 运动类每次下载要 14–20 美元，所以只是测试，不指望靠它拉人。
- **剩下的留着**，给效果最好的那个再加一次。
- 不投 Reddit 广告（起投门槛高、地区定向粗）。

## 台湾的同类 App（2026-11-12 粗查，没有逐个核实）

逛 Threads 时看到一条“這個臨打app超方便的，好誇張”（1.6K 赞、2.9K 分享），帖子没写是哪个 App，后来再搜没找到这条。台湾做羽球臨打的 App 有好几个：
- **羽球總站**：臨打报名、场地租借、排点管理、教练课预约、找附近团的地图。在 App Store 上架。
- **羽你速配 Matchminton**：免费，臨打行事历、报名链接、排点程序，名单自动递补。https://matchminton.tw/
- **愛羽球 AI badminton**：找团、订场、战绩。https://www.aibadminton.com.tw/
- 羽球GO（2023 年的报道，现在还在不在不清楚）、PlayOne 零打快查。

和 Badie 的关系：
- **重合的**：它们的臨打报名，就是 Badie 的球群和附近球局。
- **Badie 有、它们没主打的**：按水平给个人配对、按天刷附近的人、爽约记录。
- **它们有、Badie 没有的**：排点（开放场上谁下一个上、上哪块场地）、订场。
- 它们都做台湾。有没有美国的球馆和用户，没查。我们先打的是洛杉矶，眼下不是正面竞争；但中文帖在 Threads 上主要被推给台湾的人，那边已经有这些 App，这也是 Threads 以英文为主的一个理由。
- 可以学的：那边火起来的入口是给团主用的工具（报名、排点），和方案第 1 节“让组织者自己找上门”是一回事。

来源：https://grass.camp/blog/group-meetup-apps-taiwan-2026 （作者自家产品也在名单里，有立场），https://www.cna.com.tw/news/afe/202306030033.aspx

### 羽球總站的 Threads 账号拆解（2026-11-12，未登录只读到 12 条帖子和 8 条 Instagram 配文，评论区读不到）

- **规模**：Threads 844 粉，Instagram 574 粉；10 月大约每周一条。原生 App 2026-03 上架，台湾区 4.5 分、22 个评分。美国区能下载，全中文，没查到美国球馆。
- **最大的一次传播不是它自己发的**：一位羽球教练发了一句“這個臨打app超方便的，好誇張”加一张截图，22.3 万浏览、1.6K 赞、2.9K 分享。原帖没写 App 名；这条在它的转发页里，第二天另一位用户点名说是羽球總站，所以很可能说的是它。它自己最好的一条是 5.1K 浏览。
- **它自己互动最高的做法**：去别人的找球帖下面，按对方的城市回一条带筛选截图的回复（5.1K 浏览、20 分享）。11 月改成贴模板回复后只有 1–4 赞，其中两条原帖已经看不到了。
- **互动最低的**：节日贺图（1–4 赞）、纯功能海报。Instagram 上真人球场照（41、17、16 赞）明显高于功能图（4–9 赞）。
- **怎么提 App**：每条都直接点名，链接放简介、自己的回帖里。两个吉祥物（河狸小狸、狮子大獅）“做事”来宣布新功能：“小狸幫大家辦好護照啦”。口气甜，没有幽默。
- **我们照着做的**：
  1. 让用户容易自己晒图。等级分享卡就是干这个的，是优先级最高的一件事。
  2. 按城市给具体信息，做成我们自己的主帖，不去别人帖子下面贴。
  3. 多用真人球场照，少用功能海报。
  4. 新功能让 Claudia “亲手做”来宣布。
  5. 链接放自己的回帖里；转发用户的好评（征得同意）。
- **不照着做的**：去陌生人帖下贴模板回复；节日贺图；纯官方的甜腔加一堆标签（它 844 粉、功能帖 13 赞，说明这种写法带不来传播）。

## 美国的同类 App（2026-11-12 查的）

查法：用 12 个关键词搜美国区 App Store，去掉游戏，留下介绍里提到羽毛球的，共 30 个；按评分数看谁有人用。评分数只是粗略的指标，搜索也不保证全，安卓没查。

结论：**美国还没有一个做起来的羽毛球找球友 App。**

| App | 是什么 | 美国区评分数 | 上线 |
|---|---|---|---|
| ConnectPlayers | 24 种运动通用的找搭子 | 258 | 2023 |
| Playo、Hudle | 印度的多运动约球 | 各 162 | 2016、2018 |
| RacketPal | 英国的球拍类运动找搭子，差评说人太少 | 91 | 2019 |
| Kotofit | 自家球馆的订场和门禁，不是找球友 | 62 | 2026-04 |
| TournMate | 匹克球、羽毛球、网球的比赛和开放场 | 2 | 2026-05 |
| **Shuttlers** | **专做羽毛球：团主发每周场次，球友一点就报名** | **0** | **2026-07** |
| Badie | | 0 | 2026-11-05 |

**最该盯的是 Shuttlers**（shuttlers.com，App Store 上的开发者是 NextShark, Inc.）：
- 模式是团主发场次、球友报名，有候补、嘉宾名额、场次群聊，场次标明水平。不经手钱，球友用 Venmo 等直接付给团主。免费。有 iPhone、安卓和网页。
- 还在测试期。网站上列了 4 个球馆、4 个城市：Houston、Menlo Park、Mukilteo、Pomona。Pomona 就在洛杉矶东边。
- 和 Badie 重合的是球群报名。它没提按水平给个人配对，也没提爽约记录。它有安卓，Badie 没有。
- 另外 Buddy Finder（湾区，2021 年起测试版）看起来没在更新。

真正在被用的不是 App，是 Facebook 群、Meetup、微信群和球馆前台。匹克球那边已经有做大的（Pickleheads），说明这个模式在美国跑得通。

## 来源

- Aral & Walker (2011). Creating Social Contagion Through Viral Product Design. *Management Science* 57(9). https://econpapers.repec.org/RePEc:inm:ormnsc:v:57:y:2011:i:9:p:1623-1639
- Cullen & Farronato (2021). Outsourcing Tasks Online: Matching Supply and Demand on Peer-to-Peer Internet Platforms. *Management Science* 67(7). https://econpapers.repec.org/RePEc:inm:ormnsc:v:67:y:2021:i:7:p:3985-4003
- Jakesch, Hancock & Naaman (2023). Human heuristics for AI-generated language are flawed. *PNAS*. https://arxiv.org/abs/2206.07271
- Altay & Gilardi (2024). People are skeptical of headlines labeled as AI-generated. *PNAS Nexus*. https://www.eurekalert.org/news-releases/1060210
- Kim, Heo & Kim (2014). 韩国移民在羽毛球俱乐部里的社会支持. *IJQSHW*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4038719
- Partiful：https://sacra.com/chat/h/ca6c792b-7d6d-42a9-ae5f-0970a819c66c/
- Pickleheads：https://thefourthquarter.beehiiv.com/p/the-4th-quarter-latest-in-sports-b18 ，https://www.formula4media.com/articles/pickleheads-debuts-court-finder-for-pickleballers ，https://www.pickleheads.com/guides/complete-group-guide
- PlayTime Scheduler：https://playtimescheduler.com/about.php
- Reclub：https://pickleball.reclub.co/for-organizers ，https://weekender.thejakartapost.com/the-weekend-digest/2025/09/07/courts-clubs-and-connections-the-rise-of-community-sports-apps.html
- RacketPal 用户分布和差评：https://startupsmagazine.co.uk/article-where-are-they-now-racketpal ，https://apps.apple.com/us/app/-/id1453817491
- Andrew Chen “atomic network”：https://www.lennysnewsletter.com/p/atomic-network
- Google 对批量低质页面的处理：https://developers.google.com/search/blog/2024/03/core-update-spam-policies
- Apple App 内活动：https://developer.apple.com/app-store/in-app-events
- Apple Ads 运动类价格：https://www.mobileaction.co/report/apple-search-ads-2025-benchmark-report/cost-per-tap/
- 小红书 AI 托管账号治理：https://m.gmw.cn/2026-03/10/content_1304371172.htm ，https://www.thepaper.cn/newsDetail_forward_32599956 ，https://www.stdaily.com/web/gdxw/2026-04/27/content_508976.html
- TikTok 未审核接口只能私密发布：https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- YouTube AI 内容声明：https://support.google.com/youtube/answer/14328491 ；重复内容：https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/
- Reddit 打击 AI 推广：https://thenextweb.com/news/reddit-ai-marketing-slop-geo-crackdown ，https://www.nbcnews.com/news/rcna203597
- “Larry” TikTok 自动化（自述，有带货链接）：https://www.stack-junkie.com/blog/how-to-automate-tiktok-marketing-with-openclaw-larry-skill-deep-dive ；自动发只比手动多约 7% 播放：https://growwstacks.com/blog/openclaw-social-media-automation-hard-truths
- US Open 2027 洛杉矶（第三方，未确认）：https://allsportdb.com/Events/2027-BWF-Badminton-World-Tour-US-Open-20451
