# Badie 增长方案：让大量羽毛球人进来，并且留得住

> **2026-11-10 改向**（用户定的）：目标从“洛杉矶一片慢慢滚”改成“大量羽毛球人涌入”；市场扩到英文、中文、日文、韩文；允许用邮件联系组织者；主钩子换成“你是几级”。第 0–3、5–7 节按这个改过。
> 2026-11-08 重写（同日加上：品牌账号由 AI 吉祥物小羽来发，自动发不用问），取代 11-03 那版（那版靠创始人联系群主、每天手动发帖，和现在的条件不符）。
> 口径以 Badie 仓库的 [STORY.md](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/STORY.md) 为准，做事的规矩以 [MARKETING_BRIEF.md](https://github.com/JunqiPi/Badie/blob/main/Badie-iOS/docs/MARKETING_BRIEF.md) 和本仓库 `CLAUDE.md` 为准。写法见 `docs/WRITING.md`。
> 证据分三档：**[论文]** 同行评审；**[公认]** 平台官方规则或被很多产品验证过；**[个案]** 单个案例或自述。

## 0. 条件和目标

**条件**（用户 2026-11-08 定的）
- 创始人自己不出面：不出镜、不发私信、不上门找人。
- **邮件可以发**（2026-11-10）：由我起草，用创始人的第一人称和真人口吻（`docs/WRITING.md`），每批他确认一次才发。规矩见第 3 节 C。
- 每天花的时间尽量是 0。
- 预算 50–100 美元。
- 住在大洛杉矶，平时在那里打球。
- 现有的小红书、TikTok、Instagram、Reddit 都是**私人账号**。

**目标：大量羽毛球人进来，并且留得住。** 每月月初对一次，看三层数字：
1. **进来**：每周测完级的人数、等级卡片带回的访问数（Badie 仓库 `LEVEL_CARD.md` 第 8 节）。
2. **留下**：每周有人报名的球群数。球群是留人的地方：一个群 20 个人就能转，不用等全城有密度。
3. **约成**：主场（圣盖博谷）每周成局数，2027-06-30 前到 30。一对一匹配只在有密度的地方才成立，所以只在主场考核。
注册数只作参考：注册涨、球群和成局不涨，说明人来了没留下。

**要先说清楚的**：
- 这次不写编出来的注册目标。同类产品靠球群长到几十万人用了几年（Reclub 自称 38.9 万，PlayTime Scheduler 约 57 万）。
- 一个月内的涌入只能靠等级卡片出爆款。爆款没法计划，只能多给机会：每周都有新的“这球是几级”内容，每个市场都有。
- 邮件联系组织者是把人留下来的那条线。没有它，进来的人没有群可去。

## 1. 底层逻辑

| 原则 | 依据 | 对 Badie 的意思 |
|---|---|---|
| **1. 宣传藏在产品本来就要产出的东西里** | **[论文]** Aral & Walker 2011（Management Science，Facebook 上的随机实验）：自动发给朋友的被动通知让同伴采用率提高 246%，再加上主动邀请只多 98%。**[公认]** Partiful 每张邀请都是一个落地页，靠口碑做到约 500 万用户。 | 群主每周往微信群里贴的报名链接，就是 Badie 最好的广告，而且不用你开口。这条要让工程 agent 把报名页做好（第 5 节）。 |
| **2. 不去找组织者，让组织者自己找上门** | **[个案]** Pickleheads 先做球场搜索页，每月 10 万访问后才加组织球局；PlayTime Scheduler 从萨克拉门托一个组织者的网站做到约 57 万球员；Reclub 主打“替代群聊和表格的一个报名链接”。 | 做一个“替代微信接龙”的免费工具页，让组织者在 Google、小红书、报名页底部自己看到。一个组织者带来 20–50 人。 |
| **3. 先密度，后广度；选人会主动搜的渠道** | **[论文]** Cullen & Farronato 2021（Management Science）：TaskRabbit 的撮合效率取决于本地密度。**[个案]** RacketPal 10 万用户里约一半在伦敦；用户差评最多的是“人太少”。 | 洛杉矶只选一片打透。主力渠道是人会主动搜的：Google 球馆页、小红书搜索、App Store。全国性的短视频播放量只是辅助。 |
| **4. 平台惩罚的是“没有人”，不是 AI** | **[公认]** 小红书 2026-03 起封禁 AI 托管账号，但说 AI 标签“不会影响流量”；YouTube 把 AI 写脚本列为不用声明的“轻微”用法。**[论文]** Jakesch 等 2023（PNAS）：读者分辨不出 AI 文字；Altay & Gilardi 2024：标了 AI 的内容可信度下降，原因是读者以为全程没有人参与。**[公认]** Reddit 用 AI 抓 AI 写的“自然推广”，苏黎世大学偷偷用 AI 账号发评论被全网封禁。 | “像真人”靠的不是文风技巧，而是只有你知道的真实细节：哪家球馆、星期几、谁没来。AI 负责量和格式，真实素材来自你。账号上写明“配音是 AI，App 和故事是我的”。 |

**2026-11-10 加的三条**

| 原则 | 依据 | 对 Badie 的意思 |
|---|---|---|
| **5. 钩子要一个人就能用** | **[个案]** 匹克球的 DUPR 评分 2021 年出现，现在自称约 200 万有评分的球员、1.2 万个俱乐部（它自己的数字，二手来源）。**[论文]** Aral & Walker 2011：产品自带的被动分享让同伴采用率提高 246%。 | 找搭子要附近有人才有用；“你是几级”当天就有收获，还能晒、能比。主钩子是不用注册的测级和等级卡片。 |
| **6. 球群自己就是一个小网络** | **[公认]** Andrew Chen 的“atomic network”。**[个案]** Reclub、PlayTime Scheduler 都是一个群一个群铺开的，不靠全城密度。 | 可以同时进很多城市和语言，只要人落在球群里。一对一匹配留给主场。 |
| **7. 先找认识人多的人** | **[论文]** Hinz 等 2011（Journal of Marketing，20 万人的实验）：先找人脉广的人，推荐数比随机找多一半以上；他们不是更有说服力，只是接触的人多。 | 组织者、俱乐部、大学社团、教练。创始人不出面，就由邮件去找（第 3 节 C）。 |

## 2. 打哪里

**按语言铺开，在球群里落地，圣盖博谷是主场。**

| 语言 | 先打哪里 | 球馆数据 | 当地在哪找球局（**都没核实**，进场前要查） |
|---|---|---|---|
| 中文 | 北美华人、马来西亚、新加坡、香港、台湾 | 都有 | 北美：小红书、微信群。台湾：LINE 群、脸书社团（只搜到一篇本地 App 的文章这么说）。马新：Reclub、ShuttleMatch，其余不清楚。 |
| 英文 | 美国、英国、马来西亚、新加坡 | 都有 | Facebook 群、Meetup、WhatsApp、Reclub、RacketPal（英国） |
| 日文 | 日本 | 有 | 我的印象是 X、LINE 和社团募集网站，没查过 |
| 韩文 | 韩国 | **没有** | 我的印象是 Naver Band、KakaoTalk、동호회，没查过 |

- **每进一个市场先做三件事**：查当地球友怎么说（论坛、社交媒体上的真实帖子，不只看 App 自己的介绍）；查当地的等级叫法能不能和 1–9 级对上；确认那里有球馆数据。韩国没有球馆数据，要先请工程 agent 解决（用户可以自己加球馆，但一个空目录留不住人）。
- **日文、韩文我能写，但你没法校对。** 每条发之前我自己按当地的习惯检查一遍（敬语、称呼），头几批邮件建议找一个母语球友看一眼。
- 主场的安排不变：

- **洛杉矶，先选一片**：精选球馆数据里大洛杉矶 + 橙县有 20 家，分成两片：
  - **圣盖博谷**：Los Angeles Badminton Club、San Gabriel Valley Badminton Club（El Monte）、Elite Rally（Irwindale）、Walnut、Alhambra、Pomona。华人多。
  - **橙县**：Irvine 两处、Orange County Badminton Club、Royal Badminton Academy（Lake Forest）、Fountain Valley。
  - **定了：先打圣盖博谷**（用户常去 Elite Rally、LABC，都在这片；还有 San Gabriel Valley Badminton Club 等，球馆密）。用户也常去 OCBC，所以**橙县是第二片**：第一片每周成局到 15 后再开始。
  - 宣传里讲到的球馆优先用 Elite Rally、LABC、OCBC：用户真的在那打，空镜和细节都是真的。
- **语言**：英文、中文、日文、韩文都做（见上表）。中文有创始人自己的写法，是最像真人的一条线。
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
| **等级卡片和“这球是几级”**（主钩子，2026-11-10） | 不用注册测级、结果卡片、每一档一个页面（Badie 仓库 `LEVEL_CARD.md`）。小羽每周发“这球是几级”“3 级和 5 级差在哪”，结尾都是“测测你几级”。素材用等级表、App 录屏和球友自愿投稿的片段。四种语言都发。 | 原则 5。这是唯一能在没有密度的地方当天给人东西的内容。 |
| **球馆页和“在哪打球”搜索**（主力） | 洛杉矶那片的球馆页补上 drop-in 价格、开放时间、本周在这里打的球群、中文版。Google 和 ChatGPT 这类 AI 会引用。 | 原则 2、3。要 3–9 个月才见效，所以现在就做。**[个案]** Pickleheads 上线球场搜索后自然流量涨了 10 倍。 |
| **球群报名页**（主力） | 免登录能看、在微信里显示正式的卡片（群名、球馆、时间、已报名人数），页面底部写“你也在组织？免费建一个”。 | 原则 1：每个用 Badie 的群主，每周都在免费替我们做广告。 |
| **“替代微信接龙”页** | `/organize`，中英文：30 秒演示、把接龙名单粘进来就能建群、爽约规则、可打印的二维码海报。 | 原则 2：组织者自己找上门。 |
| **App Store 的 App 内活动** | 发每周固定的活动（比如“圣盖博谷周三晚双打 4–6 级”），会出现在 App Store 搜索里。 | **[公认]** Apple 官方免费入口，最多同时挂 10 个。 |
| **Instagram Reels + YouTube Shorts** | 新开的 Badie 品牌账号，由吉祥物小羽（公开说明是 AI，可爱的语气，见 `docs/MASCOT.md`）来发。GitHub Actions 每天自动生成并用官方接口发 1 条：小羽 + App 真实录屏 + 你拍的球馆空镜，打开 AI 标签，发前不用问（用户 2026-11-08 同意）。 | 辅助，主要用来让人“搜到你的时候看起来是真的”，也带来一些全国流量。 |
| **TikTok** | 先提交 Content Posting API 审核（网上说要 2–6 周，未核实）；通过后和 Instagram 同一套流水线。 | 没通过审核时，用接口发的视频只有自己能看到，所以先等审核。 |
| **评论区的常见问题** | Instagram 和 YouTube 上，**自己帖子下面**的问题（免费吗、有安卓吗、哪些城市），用你写过的固定回答自动回。其他评论不回，每周把清单放进 `queue/`，想回你就回。 | 官方接口允许，只答事实，不会乱承诺。 |

### B. 每周 15 分钟（推荐，但由你决定）

**小红书**：我每周日把 5–7 篇笔记做好（图、文字、话题），放在 `queue/xhs/` 里。你在小红书创作服务平台用**官方的定时发布**一次排完。
- 这是北美华人找球局的地方，也是最可能让洛杉矶的组织者找到 Badie 的地方。放弃它，中文这条线基本就断了。
- **每周其中一篇是更新日志**（2026-11-10 加）：“独立开发的羽毛球 App，这周改了什么”，只写真的上线了的改动，结尾问大家还缺什么。小红书上独立开发者的这类笔记粉丝少也有人讨论（小红书官方说站内有 5 万多名独立开发者，是平台自己的数字）。只有真的有人提过，才能写“按大家说的改了”。
- 不能做成自动：小红书没有开放发帖接口，第三方自动发帖工具 2026-03 起会被封号。这是你的私人账号，风险太大。

### C. 邮件联系组织者（2026-11-10 用户同意）

**找谁**：在自己的网站或公开页面上留了联系邮箱的俱乐部、球馆、大学羽毛球社、教练、羽毛球媒体和博主。只读对方自己公开的页面，不爬平台，不买名单。

**怎么写**
- 用创始人的第一人称，真人口吻，按 `docs/WRITING.md`：短；先说自己是谁、为什么写给他；至少一个只和对方有关的细节（他的球馆、哪天的活动、哪条视频）；不用营销词；一封只提一件事。
- 给对方的东西要具体：球群报名链接代替接龙、教练带课的球群、他的球馆页补全、等级卡片给会员用。不要求对方发帖。
- 每封都不一样，不群发同一段话。日文、韩文按当地写信的规矩来。
- 说的事只能是真的（STORY.md）。被问到是不是 AI 写的，照实说：“邮件是我用 AI 帮忙起草的，内容我都看过。”

**怎么发**
- 每批（5–15 封）整理好给用户看一次，回“发”才发。回信也一样：我起草，进下一批确认。只有要他拍板的事单独提醒。
- 同一个人最多追一次，隔一周。说了不感兴趣或没回，就不再发。
- 每封带退订的一句话和通信地址（美国对商业邮件的要求）。退订的地址永久记在 `queue/outreach/unsubscribed.txt`。
- **用单独的发信子域**（比如 `mail.badie.rsvp`），不用现在发注册验证码的那个。验证码走的 Resend 账号投诉率超过 0.08% 会被停号，不能连累注册。
- 记录在 `queue/outreach/log.md`：发给谁、哪天、回了什么、带来了什么（建了群没有）。

**顺序**：先圣盖博谷和橙县的俱乐部、南加的大学羽毛球社（主场），再按第 2 节的市场一个一个加。每个市场头一批只发 5 封，看回信率再决定要不要继续。

### D. 不做

- **私信**：官方接口只允许回复先来信的人，不能主动发给陌生人；操控浏览器替人发属于平台禁止的自动私信，封的是用户的私人账号。联系人只走邮件（C）。
- **X**：新开发者没有免费接口额度（第三方说每条约 1.5 美分），英文和中文圈里看的人主要是开发者。**日本可能是例外**，查完日本球友在哪找局再定。
- **Reddit 机器人**：Reddit 在专门抓 AI 写的推广，r/badminton 禁止自我推广。用私人账号跑机器人，大概率被封。
  可以做的：到 2027 年中，你最多手动发 2 条“这是我做的”介绍帖（我写好，你复制粘贴），其余时间不碰。
- 自动发小红书、在别人的帖子下面自动评论、批量私信、小号、冒充普通球友、AI 生成的假人和假球场。

## 4. “100% 像真人”怎么保证

不能保证 100%。真正能做到的是让每条都**有真东西**，再加三道检查：
1. **素材库**：只用你提供的真实经历和真实画面（第 7 节）。AI 不编经历、对话和数据，缺素材就不发那一类。
2. **文风锚点**：用你自己写的 10 段以上文字做样本，写法规则在 `docs/WRITING.md`。
3. **发之前自动检查**：查禁用词和 AI 腔句式（中英文各一份清单）；对照 STORY.md 核对每一句说法；同一个模板不连发三天（YouTube 2025-07 起会处理“大量重复的内容”）。
没通过检查的不发，留在 `queue/rejected/` 里，每周汇总一句话给你。

## 5. 要工程 agent 做的事（请转给 Badie 仓库那边，按重要性）

0. **等级卡片**（和第 1 项并列第一，2026-11-10）：不用注册测级、结果卡片、每一档一个页面、静态页扩到 10 种语言。需求在 Badie 仓库 `Badie-iOS/docs/LEVEL_CARD.md`。
1. **球群报名页**：免登录能看名单、水平、球馆、时间、候补；在微信、iMessage 里显示正式的分享卡片；一点就报名；页面底部写“你也在组织？免费建一个”。
2. **`/organize` 页**（中英）：替代微信接龙；粘贴接龙名单导入；可打印的二维码海报（每个球馆一个码，能区分来源）。
3. **洛杉矶那片的球馆页**：drop-in 价格、开放时间（`us_venues.json` 里已经有）、本周在这里打的球群、中文版本。
4. **空状态不空**：附近配不到人时，显示附近已知的 drop-in 时段（精选数据里有时间表），不显示一个空页面。**[个案]** 约球 App 的差评最多的是“人太少”。
5. **注册后问“你从哪里知道 Badie 的”**（如果还没做）。
6. **App 内活动**：用 App Store Connect 接口发布每周固定的活动。

## 6. 时间表

| 时间 | 做什么 |
|---|---|
| **11 月** | 工程：等级卡片和球群报名页。我：发信子域和退订流程准备好后，发主场的第一批邮件（5 封）；各市场的调研。你：一次性设置（第 7 节，约 1–2 小时）。我：写好素材库、`WRITING.md`、前 30 条内容；搭好自动发布流水线。工程：第 5 节第 1–3 项。小红书开始每周排。 |
| **12 月** | 等级卡片上线，四种语言的“这球是几级”开始发。邮件扩到第二个市场。Instagram、YouTube 自动发上线；提交 TikTok 审核。圣诞假期内容。12 月底前球馆页和 `/organize` 必须上线，赶 1 月的窗口。 |
| **1 月** | 全年最重要的一个月：所有渠道同一周发“新年测测你几级”，加新年开练内容 + App 内活动。发一次 Product Hunt 和 Hacker News（仓库是公开的；带来的是外链和 AI 引用，不是球友）。第一次花钱测试（见第 8 节）。 |
| **2 月** | 春节（02-06）新春球局内容。月底复盘：哪个渠道带来了成局，没用的停掉。 |
| **3–4 月** | 加倍投入有效的渠道。如果第一片区域每周成局到了 15，开始给第二片做球馆页。 |
| **5–6 月** | “刚搬来洛杉矶”内容。6 月底对目标。 |

每周一我在 `queue/` 写一句话总结：发了什么、哪条最好、网站来源（Cloudflare Web Analytics 的 `?ref=`）、成局数。不需要你回复。

## 7. 需要你提供的（都是一次性的）

1. **你自己写的文字，10 段以上**：以前的小红书、朋友圈、和朋友的聊天（别人的名字删掉）。英文的也要几段（短信、Discord 都行）。这是“像你”的唯一来源。
2. **3–5 个真实经历**，一两句话就行，比如“有一次约好 4 个人只来了我一个”“刚搬到 XX 的第一个月一直一个人对墙打”。只用你说过的。
3. **球馆空镜**：下次去打球时用手机拍 10 段，每段 3–5 秒：球场、球、鞋、记分牌，不拍人脸。拍一次能用很久。
4. **品牌账号**（已定新开）：Instagram、YouTube、TikTok 各注册一个 `badiebadminton`，头像用小羽。注册要手机号或邮箱验证，只能你来点；密码不要发给我。
5. **一次性设置**：开发者账号和令牌（Meta、Google、TikTok）由你登录点确认，密钥填进 GitHub Secrets。我会写一步一步的说明。

6. **发邮件要的三样**（2026-11-10）：
   - 一个能写在邮件末尾的通信地址（邮政信箱就行，不用家里的地址）。
   - 一个收回信的 Badie 邮箱，和单独的发信子域。域名记录和发信服务的密钥由你来填，我写步骤。
   - 你写过的英文（短信、邮件都行）几段。现在一段英文样本都没有，英文邮件只能按通用的规矩写。

## 8. 50–100 美元怎么花

先不花，等第 5 节的报名页和球馆页上线、内容跑满一个月，知道哪条笔记最好之后：
- **1 月，30 美元**：给表现最好的那条小红书笔记投“薯条”，只投洛杉矶（海外账号能不能投还没核实，到时候在 App 里看一下）。
- **2 月，30–50 美元**：Apple Ads，精确匹配 “badminton partner” “羽毛球”，只投你选的那片。**[公认]** 运动类每次下载要 14–20 美元，所以只是测试，不指望靠它拉人。
- **剩下的留着**，给效果最好的那个再加一次。
- 不投 Reddit 广告（起投门槛高、地区定向粗）。

## 来源

- Aral & Walker (2011). Creating Social Contagion Through Viral Product Design. *Management Science* 57(9). https://econpapers.repec.org/RePEc:inm:ormnsc:v:57:y:2011:i:9:p:1623-1639
- Cullen & Farronato (2021). Outsourcing Tasks Online: Matching Supply and Demand on Peer-to-Peer Internet Platforms. *Management Science* 67(7). https://econpapers.repec.org/RePEc:inm:ormnsc:v:67:y:2021:i:7:p:3985-4003
- Jakesch, Hancock & Naaman (2023). Human heuristics for AI-generated language are flawed. *PNAS*. https://arxiv.org/abs/2206.07271
- Altay & Gilardi (2024). People are skeptical of headlines labeled as AI-generated. *PNAS Nexus*. https://www.eurekalert.org/news-releases/1060210
- Hinz, Skiera, Barrot & Becker (2011). Seeding Strategies for Viral Marketing. *Journal of Marketing* 75(6). https://ama.org/2019/01/16/seeding-strategies-for-viral-marketing-an-empirical-comparison
- DUPR 的规模（二手，DUPR 自己的数字）：https://tournamentpickle.com/blog/dupr-rating-explained
- 新加坡 ShuttleMatch：https://apps.apple.com/sg/app/shuttlematch/id6757417927 ；台湾找球友的渠道（一家本地 App 的文章）：https://grass.camp/blog/badminton-beginner-guide-find-partners-taiwan
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
