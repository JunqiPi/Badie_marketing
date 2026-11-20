# 无人声动画讲解短视频：怎么做

> 2026-11-19。用户：先学好“不露脸、不配音”的动画讲解短视频（动态图形 + 字 + 音乐 + 音效）是怎么做的，再做 Badie 面向日本、韩国的羽毛球战术短视频（先发 YouTube Shorts；30 秒；SVG 球场图，球员是圆点，有球的弧线和箭头；提问 → 三个选项 → 揭晓 → 带理由的回放 → 常见错误 → 一句话规则 + Badie 片尾）。
> 规矩：只读文字材料（教程、文档、文章），不下载视频和文件，不登录。
> 证据标注沿用 `IMAGE_TEXT_STUDY.md`：**[论文]** 同行评审；**[官方]** 平台或标准组织的文档；**[数据]** 有样本量的统计；**[调查]** 问卷，是创作者的看法不是平台数据；**[博主]** 从业者和工具厂商的经验，没有公开数据。

## 0. 缺口

- **没看过一条日韩的羽毛球战术 Shorts。** 按规矩不下载视频，文字页面又看不到画面节奏。下面的节奏、版式是从通用资料推出来的。做完第一条样片后，最好请用户在手机上刷 5–10 条日韩同类视频（搜「バドミントン ダブルス 立ち位置」「배드민턴 복식 로테이션」），记下每条几秒切一次、字多大、有没有音乐，再回来改模板。
- **日文、韩文的羽毛球术语和文案要母语的人看一遍。** 下面列的术语只有一部分有出处。
- 各平台的安全区、响度目标都**没有官方像素和数值**，只有第三方测量。发之前用手机看一遍真实界面。

## 1. 动画本身

### 1.1 时长和缓动

| 用途 | 时长 | 30fps 帧数 | 出处 |
|---|---|---|---|
| 小反馈（勾选、闪一下） | 约 100 ms | 3 帧 | [官方] NN/g |
| 一般界面动画 | 100–500 ms，超过 500 ms 就“拖” | 3–15 帧 | [官方] NN/g |
| 大块变化（弹窗进场） | 200–300 ms；出场比进场短（300 进 / 200–250 出） | 6–9 帧 | [官方] NN/g |
| Material 的“强调”动画 | 500–600 ms | 15–18 帧 | [博主] 第三方整理的 M3 token |

NN/g 的数字是给**用户自己点出来的界面动画**定的：用户在等，所以要快。讲解视频里观众不操作，要看清东西从哪来、到哪去，可以放慢一点。我们的起点：**元素进场 9–12 帧，出场 6 帧，球员跑位 12–18 帧，球的飞行按真实时间、回放时放慢一半**。

缓动：
- **[官方] NN/g**：直线匀速“看着别扭”；**默认用 ease-out**（先快后慢，眼睛能落在终点上）；ease-in / ease-in-out 用在离场。
- **[博主] Willenskomer《UX in Motion》**：缓动“什么时候都要用”。
- **过冲（overshoot，easeOutBack）**：只给“弹出来”的东西用（选项标签、正确答案的高亮），球员和球不要过冲，不然像在抖。
- 常用函数（`t` 是 0–1 的进度）：
  ```js
  const easeOutCubic   = t => 1 - (1 - t) ** 3;
  const easeInOutCubic = t => t < .5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2;
  const easeOutBack    = t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2; };
  const clamp01 = x => Math.min(1, Math.max(0, x));
  const tween = (t, t0, t1, ease = easeOutCubic) => ease(clamp01((t - t0) / (t1 - t0)));  // 秒 → 0..1
  ```
  Remotion 的 `spring()` 默认 mass 1、damping 10、stiffness 100、可以过冲；要不过冲就开 `overshootClamping`。我们不用 Remotion 也可以照这个思路，把弹簧写成只依赖 t 的函数。

### 1.2 一拍一件事（staging）

- **[博主] IxDF 拿迪士尼十二原则对照界面动画**，对我们有用的几条：
  - **Staging**：用动画告诉观众看哪；不重要的东西别动。→ 同一时刻只有一个主角在动（球，或者一个球员），其他东西静止或变淡。
  - **Follow through / overlapping**：相关的东西错开一点出场，先主后次。→ 三个选项**依次弹出**，间隔 4 帧（约 130 ms）。Willenskomer 叫它 offset & delay：错开的时间本身就在说“这几个是一组、但各是各的”。
  - **Slow in / slow out**：就是缓动。
  - **Arc**：东西沿弧线走更自然。→ 球员跑位用轻微的弧线，球本来就是弧线。
  - **Timing**：速度本身带信息。→ 杀球快、挑球慢，观众一眼看出区别。
  - **Exaggeration**：可以夸张，但“好的动画是看不出来的”。
  - **Solid drawing**：阴影、透视要统一，画错了像坏掉了。→ 球的阴影始终在同一方向。
- 迪士尼的另外几条（squash & stretch、anticipation）用在球拍击球那一下就够，别处不用。

### 1.3 字在屏幕上停多久

字幕行业的阅读速度上限（**[官方] Netflix 字幕规范**）：

| 语言 | 每秒字数（成人） | 每行 | 怎么数 |
|---|---|---|---|
| 日文 | **4 字/秒**（翻译字幕）；日语原声的听障字幕 7 字/秒 | 横排 13 个全角字（听障字幕 16），最多 2 行 | 半角字、空格、标点算 0.5 |
| 韩文 | **12 字/秒**（听障字幕 14） | 16 字，最多 2 行 | 拉丁字母、空格、标点算 0.5 |
| 英文 | 20 字符/秒（第三方转述，官方页没打开） | 42 字符 | |
| 通用 | 每条最短 5/6 秒（日文 0.5 秒），最长 7 秒 | | |

- **[官方] TikTok 广告指南**写“每秒 5–10 个词”，比字幕快很多。那是广告口号，不是让人读懂的速度，我们不用。
- 我们的情况比字幕难：观众同时要看球场图，而且没有声音帮忙。所以按字幕的**下限**算：
  - **日文按 5 字/秒，韩文按 10 字/秒**（日文取 4 和 7 之间偏慢；韩文比 12 慢一点）。
  - **停留时间 = max(1.5 秒, 字数 ÷ 速度 + 0.5 秒)**。一句 12 个字的日文：12 ÷ 5 + 0.5 = 2.9 秒。
  - 每行日文 ≤13 字、韩文 ≤16 字，最多 2 行。
- 30 秒里能放的字：扣掉纯看图的时间，**日文全片约 80–100 字，韩文约 120–150 字**。超了就删字，不加速。

### 1.4 动态文字（kinetic typography）

[博主] 几篇教程的共同点（没有研究）：讲解类用“慢、清楚”的文字动画，促销类才用快切；每个动作要服务意思，不是每个字都要动；关掉声音看一遍，读不完就延长停留。

我们的做法：
- 字只做三种动作：**弹出**（scale 0.9→1 + 透明度，9 帧，easeOutBack）、**重点词变色**（沿用现有的荧光绿底 `#d4f33f`）、**淡出**（6 帧）。不逐字蹦，不旋转。
- 句子出现时球场上的动作暂停或变慢，让眼睛有时间读。

### 1.5 9:16 画面的层级和安全区

各平台界面会盖住的地方（1080×1920）：

| 平台 | 上 | 下 | 右 | 左 | 出处 |
|---|---|---|---|---|---|
| YouTube Shorts | 120–180 px | 250–380 px | 120–164 px | 50–60 px | [博主] 第三方实测，YouTube 不公布 |
| Instagram Reels | 14%（约 270 px） | 35%（约 670 px） | 6%（约 65 px） | 6% | [博主] 转述 Meta 广告规格（广告版，自然流量可能宽一点） |
| TikTok | 120–200 px | 250–370 px | 120–164 px | 50–60 px | [博主] 第三方实测；官方只给 Ads Manager 里的模板 |

**先发 YouTube，按 YouTube 排版**：重要的东西放在 **x 60–920、y 200–1520** 里。将来转发 Reels 时，下面 35% 会被盖住，要单独出一版（球场缩小上移），不能直接转。

版面层级（从上到下）：
1. y 200–260：系列名 + 编号（小字，比如「ダブルス立ち位置 #01」）。
2. y 270–420：题目，最多两行，最大的字。
3. y 440–1500：球场（见第 5 节的尺寸）。选项、箭头、理由都画在球场上或紧贴球场。
4. y 1500 以下：不放任何要读的东西。
5. 右下角 Badie 小标全程挂着，但放在 x < 920 以内。

### 1.6 颜色和对比

- **[官方] WCAG**：正文字和背景对比 ≥4.5:1，大字 ≥3:1；看懂内容必须要的图形（箭头、圆点、线）和旁边颜色对比 ≥3:1（1.4.11）。
- **红绿色弱**：两队、对错都不能只靠红绿区分。Okabe–Ito 色盲友好色：橙 `#E69F00`、天蓝 `#56B4E9`、蓝绿 `#009E73`、黄 `#F0E442`、蓝 `#0072B2`、朱红 `#D55E00`、紫红 `#CC79A7`。规则：**颜色之外再加一个区别**（对的打勾、错的打叉；我方实心、对方空心）。
- 和现有品牌色（`render.cjs`：米白 `#f5f0e6`、墨黑 `#17140f`、荧光绿 `#d4f33f`、淡紫 `#c8beff`、粗黑边 + 错位阴影）的搭配建议：
  - 背景米白，球场用低饱和的绿底白线（一眼认出是球场）。
  - 我方：墨黑描边的荧光绿实心点；对方：墨黑描边的淡紫空心点。
  - 正确：荧光绿 + 勾；错误：朱红 `#D55E00` + 叉。
  - 球：白色 + 墨黑描边 + 灰色阴影。
  - 第一条样片出来后，用对比度工具量一遍荧光绿和球场绿之间是不是 ≥3:1，不够就加粗黑描边。

### 1.7 一个系列要一致

同一套：字体（拉丁字 Nunito 900，日文 Noto Sans JP 800/900，韩文 Noto Sans KR 800/900，都是 Google Fonts 的开源字体）、颜色、球场尺寸和位置、音效、片头片尾的样子、编号的位置。**模板做成代码**，每条视频只换一份 JSON（题目、选项、球的路线、文案），这样不会越做越走样。

### 1.8 循环（最后一帧接第一帧）

- **[官方，二手转述]** 2025-03-31 起 YouTube Shorts 每次开始播放或重播都算一次观看，不要求最短观看时长；原来的算法改名“engaged views”，仍然用来判断能不能赚钱。所以循环会多算观看次数。
- **[博主]** 循环做法：最后一帧和第一帧几乎一样（画面循环），或者结尾那句话让人想回头再看（叙事循环）。结尾黑屏哪怕半秒，循环就断了；结尾“完全讲完了”的片子没人重看。
- 我们的做法：**最后 0.5 秒从片尾卡缩回开场那一帧的构图**（同一个球场、同样的球员站位、题目重新出现），音乐也剪成能接上的长度。

## 2. 没有人声的声音

### 2.1 音乐

- 没找到关于节奏的研究。[博主] 讲解视频多用不抢戏的器乐。我们选**无歌词的器乐**（观众要读字），**100–120 BPM**。
- 选能让帧数整除的速度，事件就能卡在拍子上：120 BPM = 15 帧一拍，100 BPM = 18 帧，90 BPM = 20 帧。倒计时的“嘀”放在拍子上。
- TikTok 说“带歌词的歌让广告记忆度 +2%”只在第三方博客里看到，没核实，而且是广告。

### 2.2 音效贴在画面事件上

[博主] 几家的共同说法：
- 小提示音（弹出、点击、轻 whoosh）让元素“落地”；大的冲击只留给揭晓。全程塞满音效，听 30 秒就麻木了。**克制是重点。**
- whoosh **比动作早一点开始**；撞击、落地声**正好在接触那一帧**。几十毫秒就听得出来。
- 音效的空间感要统一（都干一点，或者都有一样的混响），不然像拼起来的。

我们的音效表：

| 画面事件 | 音效 | 时间 |
|---|---|---|
| 选项弹出 | pop（短、高） | 正好在出现那一帧 |
| 球员跑位、箭头画出 | 轻 whoosh | 提前 2–3 帧开始 |
| 击球 | 短促的“嗒” | 击球那一帧 |
| 倒计时 3-2-1 | tick | 在拍子上 |
| 揭晓正确答案 | ding（全片最响的一下） | 高亮那一帧；音乐同时压低 |
| 常见错误、球落空地 | 低沉的 thud / buzz | 落地那一帧 |
| 片尾 | 无，或者一个很轻的收尾音 | |

### 2.3 同步的容忍度

- **[官方] ITU-R BT.1359**：声音比画面早约 45 ms、或者晚约 125 ms，普通观众就能察觉；能接受的范围是早 90 ms 到晚 185–190 ms。
- 30fps 一帧是 33 ms，所以：**冲击类音效对齐到同一帧，绝不提前超过 1 帧**（人对声音提前更敏感）；whoosh 这种有渐强的可以提前 2–3 帧。

### 2.4 闪避（ducking）

没有人声时，音乐就是底，音效要“穿出来”。揭晓那一下把音乐压低约 6 dB（音量 ×0.5），0.2 秒压下、1–1.5 秒后回来。时间点是我们自己定的，所以**直接写音量曲线**，比侧链压缩更准、每次结果一样。（厂商博客说讲解视频的音乐要比人声低 20–25 dB，那是有人声的情况，不适用。）

### 2.5 响度

- **[博主，各家一致]** YouTube（含 Shorts）把响的视频降到约 **−14 LUFS**，只降不升，太小声的就一直小声。TikTok、Reels 不公布，第三方建议 −14 到 −16。没找到平台官方页面。
- 目标：**整片 −14 LUFS，真峰值 −1 dBTP**。用 ffmpeg loudnorm 两遍做（第 4 节）。

### 2.6 避开 Content ID

- **[官方] YouTube**：
  - Shorts 自带音乐库里的歌会自动挂一个看不见、不能申诉的版权声明。
  - **YouTube 音频库（Audio Library）里的免版税音乐不会被 Content ID 认领**。部分曲目要在简介里署名（CC 协议）。
  - 超过 1 分钟、有版权声明的 Short 会被屏蔽。我们 30 秒，不碰这条线，但也说明别用来路不明的音乐。
- **[博主]** 音频库标准许可的曲目可能**只能用在 YouTube**；转发 TikTok、Reels 要看每首的许可（CC-BY 的可以，署名）。
- **[博主]** Pixabay 一类的“免费音乐”，有些作者把曲子登记了 Content ID，有许可证也会先被认领，要事后申诉。
- **我们的做法**：
  - 音效**全部自己用 ffmpeg 合成**（第 4 节），完全是自己的，不会被认领。
  - 音乐：YouTube 版用音频库里不需要署名、许可写明可以用的曲子。要转发 TikTok、Reels 时，要么换成该平台 App 里的音乐，要么用 CC-BY 的曲子并署名。每首曲子记下名字和许可。

## 3. 让人看完的做法

### 3.1 哪些有证据

| 说法 | 证据 |
|---|---|
| 开头 3 秒内交代内容 | **[官方] TikTok 广告指南**：前 3 秒交代内容，记得更牢；“钩子”放前 6 秒。只是建议，没公布数据 |
| YouTube 看“观看 vs 划走” | **[官方]** YouTube Studio 有“Viewed (vs. swiped away)”这项指标。官方没给及格线；网上的“70–80%”是创作者自己报的 |
| 重播算观看 | **[官方，二手转述]** 2025-03-31 起每次重播都算 |
| 先猜再看答案，记得更牢 | **[论文]** Kornell, Hays & Bjork 2009；Richland, Kornell & Kao 2009：先试着回答（哪怕答错）再看答案，比直接看答案记得牢，**答错后马上给正确答案**效果最好。这说明“先猜后揭晓”能帮人学会，不说明能让人看完或者被推荐 |
| Shorts 30 秒以内最好 | **[调查]** Adobe Express 问了 507 个创作者：53% 认为 30 秒以内播放最好。是看法，不是平台数据 |
| 1–2 秒钩子、每 2–3 秒一个变化、结尾催评论 | **[博主]** 到处都这么说，没有公开数据。“1.3 秒注意力”“71% 在前 3 秒决定”这类数字都找不到原始出处，不引用 |

### 3.2 我们怎么用

- **开头 1 秒内**：第一帧就是有内容的画面（球场 + 球员 + 球正飞在半空），不要片头、不要 logo、不要从黑场淡入。题目在 0.3 秒弹出。第一帧也是信息流里的预览画面。
- **先猜再揭晓**：三个选项停 3 秒（倒计时 3-2-1），揭晓**马上**接理由（论文说错了马上纠正最有用）。
- **每 2–3 秒一个新的视觉事件**：模板的分段天然就是这样（球飞、选项弹出、倒计时、揭晓、回放、错误示范、规则），不用另加花样。
- **评论**：在选项出现时就放一行小字「A・B・C どれ？」/「A·B·C 뭐 골랐어요?」，不放在片尾。揭晓后会有人来说“我选了 B”或者不服，这就是评论。置顶评论写一段更细的说明。
- **系列名和编号**：固定的系列名 + #编号放在画面上方和标题里。同一个系列建一个播放列表。

## 4. 我们的制作流程

### 4.1 现在有什么

- `video/make_video.py`：读 JSON 脚本，用 Qwen3-TTS 配音；每个场景调 `render.cjs` 画**一张静态 PNG**，再用 ffmpeg `zoompan` 慢慢推近，按配音长度出片段；最后 `concat` 拼起来。H.264 `-crf 20 -preset medium`，AAC 160k / **44.1 kHz**。ffmpeg 先找系统的，没有就用 `imageio-ffmpeg` 自带的（本机没有系统 ffmpeg）。
- `video/render.cjs`：Playwright（锁定 1.56.1）开 1080×1920 的页面，`setContent` 后截一张图。有品牌样式（Nunito 900、米白底、荧光绿 `mark`、粗黑边 + 错位阴影）和“AI 配音”标。
- **能复用的**：Playwright、ffmpeg 的查找方式、品牌样式。**要新写的**：逐帧动画、音效合成、混音、响度。这是一个新脚本（比如 `video/tactics/`），不改旧的。
- 新片子没有配音，“AI 配音”标去掉。**[官方] YouTube**：明显不真实的内容（动画）不用勾“合成内容”声明。

### 4.2 逐帧渲染：原则

**[官方] Remotion 文档**说清了为什么会闪、怎么才能每次一样：
- 动画只能由“当前是第几帧”算出来；同一帧算多少次都一样；不依赖按顺序渲染；不用随机数（要用就用带种子的）。
- 不用 CSS 动画、`transition`、`requestAnimationFrame`、`Date.now()`。
- 等字体、图片都加载完再截图，不然会截到加载中的样子。

### 4.3 逐帧渲染：步骤

1. **一个 HTML 页面**，里面是 1080×1920 的 `<svg>`。字体用本地 `@font-face`（woff2 文件放进仓库，不在渲染时走网络）。
2. 页面里暴露一个函数 `window.render(t)`（t 是秒），它**只根据 t** 设置每个元素的属性（位置、透明度、`stroke-dashoffset`、文字）。场景数据（时间表、坐标）在加载时传进去。
3. Node 脚本：
   ```js
   const FPS = 30, N = Math.round(30 * FPS);              // 900 帧
   await page.setViewportSize({ width: 1080, height: 1920 });
   await page.setContent(html, { waitUntil: 'load' });
   await page.evaluate(() => document.fonts.ready);
   const ff = spawn(FFMPEG, args, { stdio: ['pipe', 'inherit', 'inherit'] });
   for (let i = 0; i < N; i++) {
     await page.evaluate((t) => window.render(t), i / FPS);
     const png = await page.screenshot({ type: 'png', animations: 'disabled', caret: 'hide' });
     if (!ff.stdin.write(png)) await once(ff.stdin, 'drain');   // 别把内存撑爆
   }
   ff.stdin.end();
   ```
   - 用 PNG 不用 JPEG：细线和字边缘不会糊。1080×1920 一帧截图大约一两百毫秒，900 帧几分钟，可以接受。
   - ffmpeg 路径：Node 里没有 `imageio-ffmpeg`，由 Python 那边 `imageio_ffmpeg.get_ffmpeg_exe()` 查出来，用环境变量传给 Node。
   - 想用 CSS / Web Animations 写动画的话，也能做到每次一样：每帧先 `document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; })` 再截图。Playwright 的 `page.clock` 也能控制 `requestAnimationFrame`。但最简单可靠的还是 `render(t)`。
   - Remotion 本身也能做这些（React 写画面，自动多开浏览器渲染）。许可：个人和 3 人以内的团队免费，商用也可以。它要装一套新依赖，我们已经有 Playwright，先不用。
4. **ffmpeg 把帧编码成视频**（只有画面，没有声音）：
   ```
   ffmpeg -y -f image2pipe -framerate 30 -c:v png -i - \
     -vf "scale=out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p" \
     -c:v libx264 -preset slow -crf 18 -tune animation -profile:v high \
     -g 15 -bf 2 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
     -movflags +faststart video.mp4
   ```
   - **颜色的坑**：截图是 RGB，ffmpeg 转 YUV 时默认按 BT.601 的矩阵，而 YouTube 按 BT.709 解读，荧光绿、黄色会偏。所以要指定 `out_color_matrix=bt709` 并打上 bt709 标签。有报告说 `scale` 这条路仍有小偏差，改用 `colorspace` 或 `zscale` 滤镜更准。**第一次先拿一张纯色图试一下**，量出来的颜色和原图一样再用。
   - `-g 15`：YouTube 建议关键帧间隔为帧率的一半；`-bf 2`：连续两个 B 帧；x264 默认就是 closed GOP。

### 4.4 箭头慢慢画出来（stroke-dashoffset）

```js
const L = path.getTotalLength();                   // 只在加载时算一次
path.style.strokeDasharray = `${L} ${L}`;
path.style.strokeDashoffset = L * (1 - p);         // p: 0 → 1
```
**坑**：SVG 的 `marker-end` 箭头不管线画了多少，一开始就会出现在终点。所以箭头尖要单独画：
```js
const a = path.getPointAtLength(L * p), b = path.getPointAtLength(Math.max(0, L * p - 1));
head.setAttribute('transform', `translate(${a.x},${a.y}) rotate(${Math.atan2(a.y - b.y, a.x - b.x) * 180 / Math.PI})`);
```
Remotion 的 `evolvePath()` 也是这个做法（dasharray = 长度，dashoffset = 长度 × (1 − 进度)）。

### 4.5 球的弧线（二次贝塞尔 + 阴影）

俯视图里看不到高度，所以用**地上的阴影表示球在哪，用球和阴影之间的距离表示多高**：
- 阴影沿地面直线从击球点 P0 走到落点 P2。
- 球 = 阴影的位置往屏幕上方偏移 `k × 高度`。屏幕上画出来就是一条弧线；阴影越小越淡，说明球越高。
- 画轨迹线用二次贝塞尔：`<path d="M P0 Q P1 P2">`，曲线上的点 B(t) = (1−t)²P0 + 2(1−t)t·P1 + t²P2。
- **羽毛球不是抛物线**。**[论文] Cohen、Quéré、Clanet 等（2013–2015）**：羽毛球只受阻力、没有升力，轨迹明显不对称，接近三角形（Tartaglia 曲线），最后几乎是垂直掉下来的。所以：
  - 高球、挑球：顶点放在全程的 **60–70%** 处（P1 靠近落点），水平速度先快后慢（`easeOutQuad`），下落段陡。
  - 杀球：近乎直线向下，没有顶点。
  - 画成对称的抛物线，打球的人会觉得不对。
- 飞行时间（估计，没有找到可引用的数字）：杀球零点几秒，高远球一秒多。正片按接近真实的速度演，回放时放慢到 0.5×。

### 4.6 音效：自己合成

用 ffmpeg 的 `lavfi` 生成，完全是自己的。下面是起点，要靠耳朵调：
```
pop    : ffmpeg -f lavfi -i "aevalsrc='0.6*sin(2*PI*(900-2500*t)*t)*exp(-30*t)':d=0.15:s=48000" pop.wav
tick   : ffmpeg -f lavfi -i "aevalsrc='0.5*sin(2*PI*2000*t)*exp(-80*t)':d=0.06:s=48000" tick.wav
ding   : ffmpeg -f lavfi -i "aevalsrc='0.4*sin(2*PI*1318*t)*exp(-4*t)+0.2*sin(2*PI*2637*t)*exp(-6*t)':d=1.2:s=48000" ding.wav
thud   : ffmpeg -f lavfi -i "aevalsrc='0.5*sin(2*PI*120*t)*exp(-9*t)':d=0.4:s=48000" thud.wav
whoosh : ffmpeg -f lavfi -i "anoisesrc=d=0.4:c=pink:a=0.5:r=48000" -af "bandpass=f=1500:width_type=h:w=1200,afade=t=in:d=0.15,afade=t=out:st=0.15:d=0.25" whoosh.wav
```

### 4.7 混音：按时间点放音效（adelay + amix）

时间表来自同一份场景 JSON（帧号 ÷ 30 = 秒），画面和声音用的是同一组时间点，不会错位。
```
ffmpeg -i music.wav -i pop.wav -i pop.wav -i ding.wav ... -filter_complex "
 [0:a]atrim=0:30,volume='1-0.5*clip((t-11.8)/0.2,0,1)*clip((13.3-t)/0.2,0,1)':eval=frame[m];
 [1:a]adelay=2000:all=1[s1];
 [2:a]adelay=2133:all=1[s2];
 [3:a]adelay=12000:all=1[s3];
 [m][s1][s2][s3]amix=inputs=4:normalize=0:duration=first[out]" -map "[out]" -ar 48000 mix.wav
```
- `adelay` 的单位是毫秒，`all=1` 让两个声道一起延迟。
- **`amix` 默认 `normalize=1`**，会按输入数量把每路音量压低，音效越多整体越小，要设 `normalize=0`（之后由 loudnorm 统一调响度）。
- 同一个音效用几次，就把那个文件当几个输入传（或者用 `asplit`）。
- 音乐那一行的 `volume` 表达式就是 2.4 节的闪避：11.8–12.0 秒压到一半，13.3–13.5 秒回来。

### 4.8 响度：loudnorm 两遍

```
# 第一遍：测
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
# 第二遍：把测到的 input_i / input_tp / input_lra / input_thresh / target_offset 填进去
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true:print_format=json -ar 48000 mix_norm.wav
```
- **[官方] ffmpeg 文档**：默认值是 I=−24、LRA=7、TP=−2，要自己改成 −14 / 11 / −1。
- loudnorm 内部会升到 192 kHz，**一定要加 `-ar 48000`**，不然输出 192 kHz 的文件。
- `linear=true` 只是请求：要是目标 LRA 小于实际，或者真峰值放不下，它会悄悄改成动态处理。看第二遍输出的 JSON 里 `normalization_type` 是不是 `linear`。

### 4.9 合成和导出

```
ffmpeg -i video.mp4 -i mix_norm.wav -c:v copy -c:a aac -b:a 384k -ar 48000 -shortest -movflags +faststart out.mp4
```
**[官方] YouTube 上传建议**：MP4，moov 放在开头（faststart），不要 edit list；H.264 High Profile、逐行、CABAC、两个连续 B 帧、closed GOP、GOP 为帧率一半、4:2:0、可变码率；1080p30 SDR 约 8 Mbps（我们用 CRF 18，平面图形实际码率会低很多，YouTube 也会重新编码，够了）；SDR 用 BT.709；音频 AAC-LC，48 kHz，立体声 384 kbps。尺寸 1080×1920、30fps，帧率按原样上传。

## 5. 羽毛球图怎么画才对

### 5.1 球场尺寸（[官方] 规则，转自 Wikipedia）

全长 13.4 m；双打宽 6.1 m，单打宽 5.18 m（单打边线在双打边线内 0.46 m）；前发球线离网 1.98 m；双打后发球线在底线内 0.76 m；网高边上 1.55 m、中间 1.524 m。

线的位置和比例画错，打球的人一眼就看出来。**按比例算，不要凭感觉画**。竖着放全场：球场高 1060 px（y 440–1500）→ 每米 79 px → 宽 482 px，前发球线离网 156 px，双打后发球线离底线 60 px。球场看起来会比较窄，第一条样片出来后在手机上看；太窄就改成“我方半场 + 网 + 对方前半场”的放大版（只适合不需要看对方后场的题）。

### 5.2 摆放和画法

- **我方在下，对方在上**，网横在中间。观众代入“我”。（[博主] 一篇教程的示意图就是自己在下；Downey 的双打书写的是“进攻方在上半场”。两种都有，我们统一用“我方在下”，系列里不变。）
- **球员**：圆点，我方实心、对方空心，点上写字母（A/B，或者「自分」「パートナー」/「나」「파트너」）。可以加一个小三角表示面朝哪。
- **球的路线**：实线弧线 + 阴影（4.5 节）；**球员跑位**：虚线箭头。没有找到羽毛球统一的图例规范（[博主] 多数教练图是靠颜色和文字说明），实线是球、虚线是人是团体球类战术板的常见习惯。**系列第一条放一次图例**。
- **负责区域**：半透明色块，表示“这块归谁”，不是精确站位（[博主] shuttleselect：“不是确切位置，是责任区域”）。

### 5.3 双打的基本规则（出题用）

有共识的：
- **进攻 = 前后站位**（日：トップアンドバック，韩：앞뒤 / 공격 대형）：后场的人杀球、吊球，前场的人封网、截击。**防守 = 左右站位**（日：サイドバイサイド，韩：사이드 바이 사이드 / 수비 대형）：在中场稍后，各管半边，覆盖整个宽度。（[官方] Wikipedia、Wikibooks；[博主] 多家教练网站）
- **转换看球往哪走**：我方挑高了 → 左右；对方挑高了 → 前后；平抽、没人挑高 → 左右、稍往前站。轮转发生在球在空中那一秒左右。口诀：“看球，不看搭档。”（[博主] shuttleselect、马来西亚 ST 羽毛球学院）
- 杀球打直线或打中路，斜线杀很冒险（[博主] Badminton Bible）；打两人中间让对方犹豫（Wikibooks）。
- 混双：女前男后是传统做法，不是规则。
- 常见错误（可以当“常见错误”那一段）：杀完球还站左右，网前没人；挑完球还站前后，后面一个人防；两个人都去看杀球，斜线挡网从中间漏过去；网前的人回头看后场；没喊“我的/你的”；被杀就慌着挑高球。

**有分歧的，不出题，或者在题目里写明前提**：
- 中路球谁接：一种说法是“正手位的人接”（shuttleselect），韩国一份资料说“对角那个人优先”。
- 防守时两人一前一后错开多少。
- 有一个博客说“杀中路是错误”，和 Badminton Bible、Wikibooks 相反，不采用。

术语：日文的「トップアンドバック」「サイドバイサイド」「ロブ」（挑球）、韩文的「사이드 바이 사이드」「하이클리어」「스매시」有出处或很常见；其他词（比如韩文的挑球怎么说）要母语的人确认。

## 6. 对原模板的修改

原模板：提问 → 三个选项 → 揭晓 → 带理由的回放 → 常见错误 → 一句话规则 + Badie 片尾。结构保留，改这几处：

1. **没有片头**。第一帧就是球在空中的球场，题目 0.3 秒内出现。
2. **选项画在球场上**（A/B/C 三个半透明的“影子站位”或三条路线），不是一列文字。读的字少，日文版和韩文版只换字。
3. **评论提示放在选项出现时**，不放在片尾。
4. **揭晓后马上讲理由**；“常见错误”就演最多人会选的那个错误选项会怎样（球落在空地），不另外再讲一个错误。时间不够时，把回放和错误合成一段。
5. **片尾卡 ≤1.5 秒**，最后 0.5 秒缩回开场构图，接上循环；Badie 的小标全程在角落挂着，不靠片尾才出现。
6. **不出有分歧的题**，或者在题目里写明前提（“两人都是右手”）。
7. **字数有预算**：日文全片约 80–100 字，韩文约 120–150 字；每句停留 = max(1.5 秒, 字数 ÷ 速度 + 0.5 秒)。
8. **去掉“AI 配音”标**；音效全部自己合成；音乐用 YouTube 音频库，记下许可。

建议的 30 秒分段（900 帧）：

| 时间 | 帧 | 内容 | 声音 |
|---|---|---|---|
| 0.0–2.0 | 0–60 | 球已在空中，落下；题目弹出（0.3 秒） | 击球“嗒”、whoosh |
| 2.0–6.0 | 60–180 | A/B/C 依次弹出（间隔 4 帧），评论提示，倒计时 3-2-1 | pop ×3、tick ×3 |
| 6.0–7.5 | 180–225 | 揭晓：对的高亮打勾，错的变淡打叉 | ding，音乐压低 |
| 7.5–16.5 | 225–495 | 0.5× 回放：跑位虚线箭头、球的弧线、2–3 句理由 | whoosh、轻 pop |
| 16.5–22.5 | 495–675 | 常见错误：最多人选的错误选项演一遍，球落在空地 | thud |
| 22.5–27.5 | 675–825 | 一句话规则（最大的字，停 4 秒以上） | 音乐回来 |
| 27.5–29.0 | 825–870 | Badie 片尾卡 | |
| 29.0–30.0 | 870–900 | 缩回开场构图，接循环 | 音乐接回开头 |

---

## 每条视频的检查清单

**做之前**
- [ ] 题目只讲一件事；规则有共识（第 5.3 节），有分歧的写明前提
- [ ] 场景 JSON 写好：题目、三个选项、正确答案、球的路线（击球点、落点、球种）、跑位、理由、常见错误、规则句、系列编号
- [ ] 日文、韩文文案按字数预算：每行日文 ≤13 字、韩文 ≤16 字，最多 2 行；全片日文 ≤100 字、韩文 ≤150 字
- [ ] 每句停留 ≥ max(1.5 秒, 字数 ÷ 速度 + 0.5 秒)，速度日文 5、韩文 10
- [ ] 母语的人看过文案和术语

**画面**
- [ ] 第一帧就有内容（球场 + 球员 + 球在空中），没有片头、没有黑场
- [ ] 球场按比例：13.4 × 6.1 m，前发球线 1.98 m，双打后发球线 0.76 m，单打边线 0.46 m
- [ ] 我方在下；我方实心、对方空心；球 = 实线弧 + 阴影；跑位 = 虚线箭头
- [ ] 高球的顶点在 60–70% 处、下落陡；杀球近乎直线
- [ ] 同一时刻只有一个主角在动；选项错开 4 帧出现
- [ ] 进场 9–12 帧 ease-out，出场 6 帧；只有弹出的标签用 easeOutBack
- [ ] 要读的东西都在 x 60–920、y 200–1520 里
- [ ] 对错除了颜色还有勾和叉；图形对比 ≥3:1，字 ≥4.5:1
- [ ] 箭头尖跟着线头走，不是一开始就在终点
- [ ] 片尾卡 ≤1.5 秒，最后一帧接得回第一帧

**声音**
- [ ] 无歌词器乐，100–120 BPM，许可已记录（YouTube 音频库；转发别的平台要另查）
- [ ] 音效都是自己合成的；冲击类对齐同一帧，whoosh 提前 2–3 帧
- [ ] 揭晓时 ding 最响，音乐压低约 6 dB
- [ ] `amix` 用了 `normalize=0`
- [ ] loudnorm 两遍：−14 LUFS、−1 dBTP，`normalization_type` 是 `linear`，输出 48 kHz

**导出**
- [ ] 1080×1920、30fps、900 帧、H.264 High、yuv420p、BT.709 标签、GOP 15、faststart；AAC 48 kHz
- [ ] 纯色测试图的颜色和原图一致
- [ ] 在手机上关掉声音看一遍：字读得完吗？再开声音看一遍：音效对得上吗？
- [ ] 在手机上的 YouTube 界面下看一遍：有没有东西被按钮和标题挡住
- [ ] 标题里有系列名 + 编号，加进播放列表；置顶评论写详细解释
- [ ] 先发给用户确认，确认后才标 `approved`

---

## 来源

动画和文字
- [NN/g：Executing UX Animations: Duration and Motion Characteristics](https://www.nngroup.com/articles/animation-duration/)
- [UX Magazine：Creating Usability with Motion: The UX in Motion Manifesto（Willenskomer）](https://uxmag.com/articles/creating-usability-with-motion-the-ux-in-motion-manifesto)
- [IxDF：UI Animation: How to Apply Disney's 12 Principles of Animation to UI Design](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design)
- [Material Design（M1）：Duration & easing](https://m1.material.io/motion/duration-easing.html)
- [Netflix：Japanese Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215767517)
- [Netflix：Korean Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/216001127)
- [Netflix：Timed Text Style Guide: General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617)
- [TikTok Ads：Creative best practices for performance ads](https://ads.tiktok.com/help/article/creative-best-practices?lang=en)
- [W3C：Understanding SC 1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast)
- [Okabe–Ito 色盲友好配色（NYU Siegal Lab 整理）](https://siegal.bio.nyu.edu/color-palette/)

安全区
- [Adaptly：Social media safe zones 2026](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide)
- [adnova：Meta ad safe zones guide](https://adnova.ai/blogs/meta-ad-safe-zones-guide)
- [Relevant Audience：TikTok video size and safe zones](https://www.relevantaudience.com/tiktok-ads/tiktok-video-size-ad-specs/)

声音和版权
- [Wikipedia：Audio-to-video synchronization（ITU-R BT.1359）](https://en.wikipedia.org/wiki/Audio-to-video_synchronization)
- [ITU-R BT.1359-1](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1359-1-199811-I!!PDF-S.pdf)
- [Open Design：How to use sound effects without overloading a product video](https://open-design.ai/blog/sound-design-product-videos/)
- [Morphic：Sound effects for explainer videos](https://morphic.com/resources/use-cases/sound-effects-for-explainer-videos)
- [OpenClip：Audio normalization: LUFS targets by platform](https://openclip.app/learn/audio-normalization)
- [YouTube 帮助：Music eligibility for YouTube Shorts](https://support.google.com/youtube/answer/13486873)
- [YouTube 帮助：Manage Shorts as a rights holder](https://support.google.com/youtube/answer/13053317)
- [YouTube 帮助：Disclosing use of altered or synthetic content](https://support.google.com/youtube/answer/14328491)
- [licenseorg：YouTube Audio Library 许可说明](https://licenseorg.com/guide/music-audio/youtube-audio-library)
- [Thematic：Thematic vs Pixabay（Content ID）](https://hellothematic.com/thematic-vs-pixabay/)

留存
- [YouTube 帮助：Understand your YouTube content performance](https://support.google.com/youtube/answer/12220281)
- [TechCrunch：YouTube is changing how Shorts views are counted（2025-03）](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted)
- [YouTube 官方博客：Five tips to master Shorts](https://blog.youtube/creator-and-artist-stories/five-tips-to-master-shorts/)
- [ContentGrip：Adobe Express study on Shorts length](https://www.contentgrip.com/youtube-shorts-length-study/)
- [Kornell, Hays & Bjork 2009, Unsuccessful retrieval attempts enhance subsequent learning（Scientific American 介绍）](https://www.scientificamerican.com/article/the-pluses-of-getting-it-wrong/)
- [Richland, Kornell & Kao 2009, The Pretesting Effect](https://learninglab.uchicago.edu/Pre-Testing_files/RichlandKornellKao.pdf)
- [vidIQ：How to loop YouTube Shorts](https://vidiq.com/blog/post/double-youtube-watch-time-looping-shorts)
- [ShortsFast：Write a loop ending for YouTube Shorts](https://shortsfast.com/blog/write-a-loop-ending-for-youtube-shorts/)

技术
- [Remotion：The fundamentals](https://www.remotion.dev/docs/the-fundamentals)
- [Remotion：Flickering](https://www.remotion.dev/docs/flickering)
- [Remotion：interpolate()](https://www.remotion.dev/docs/interpolate)
- [Remotion：spring()](https://www.remotion.dev/docs/spring)
- [Remotion：evolvePath()](https://www.remotion.dev/docs/paths/evolve-path)
- [Remotion：Encoding guide](https://www.remotion.dev/docs/encoding)
- [Remotion：License FAQ](https://www.remotion.dev/docs/license/faq)
- [Playwright：Clock](https://playwright.dev/docs/clock)
- [Playwright：page.screenshot](https://playwright.dev/docs/api/class-page#page-screenshot)
- [FFmpeg Filters Documentation（adelay、amix、loudnorm、sidechaincompress）](https://ffmpeg.org/ffmpeg-filters.html)
- [DEV：Two-pass loudness normalization with ffmpeg loudnorm](https://dev.to/masonwritescode/two-pass-loudness-normalization-with-ffmpeg-loudnorm-the-right-way-1nm3)
- [FFmpeg trac #6570：loudnorm 输出 192 kHz](https://trac.ffmpeg.org/ticket/6570)
- [FFmpeg trac #979：RGB→YUV 颜色矩阵](https://trac.ffmpeg.org/ticket/979)
- [YouTube 帮助：Recommended upload encoding settings](https://support.google.com/youtube/answer/1722171)

羽毛球
- [Wikipedia：Badminton（场地尺寸、双打战术）](https://en.wikipedia.org/wiki/Badminton)
- [Wikibooks：Badminton/Strategy](https://en.wikibooks.org/wiki/Badminton/Strategy)
- [The Badminton Bible：Doubles tactics](https://www.badmintonbible.com/tactics/doubles)
- [Badminton Fanatiker：Positioning and formations in doubles](https://badmintonfanatiker.com/positioning-and-formations-in-doubles/)
- [ShuttleSelect：Doubles formations and rotation](https://shuttleselect-website.pages.dev/articles/doubles-formations-rotation-guide.html)
- [ST Badminton Academy：Doubles rotation and positioning 101](https://stbadmintonacademy.my/?p=72955)
- [Daum 카페：복식 대형（사이드 바이 사이드）](https://m.cafe.daum.net/sungsa/59uL/50)
- [Daum 카페：복식 운영（중앙공격 리시브）](https://m.cafe.daum.net/sungsa/59uL/65)
- [Cohen et al. 2015, The physics of badminton（New J. Phys.）](https://core.ac.uk/download/47088083.pdf)
- [Darbois-Texier et al. 2014, On the size of sports fields（New J. Phys.，Tartaglia 曲线）](https://orbi.uliege.be/bitstream/2268/173915/1/Onsize_NJP.pdf)

---

## 附：在浏览器里逐帧看的三条（2026-11-19）

用户要求先看真视频再动手。在 Chrome 里打开、静音、暂停后按时间点逐帧截图看的，没有下载。听不到声音，所以音效和音乐的部分只能看不到。

### 1. Y.B.CJr 公式「相手が後ろからスマッシュを打ちそう。Bはどこが基本？」（日本，24.7 秒）
- **固定框架**：顶部一整段一直不动：品牌条（BADO TACTICS）、黄色大字问题「この場面、どこに動く？」、一行白字场景说明。下面是球场，最下面一块文字区随时间换内容。只换底部文字和球场上的东西，观众不用重新找视线。
- **球场**：深绿底、透视的立体球场（不是俯视平面），球员是带字母的圆头大头针（自己蓝 A/B，对手红 C/D），球路是虚线加一个羽毛球图标。
- **时间线**：0–2 秒出题；约 2–7 秒在球场上画出ア/イ/ウ三个虚线圆圈，右上角黄圈倒数 5→1，底部「ア・イ・ウ どれ？ 一時停止して考えよう。当たったかはコメントで！」；约 9 秒「正解：ウ」+ 一句理由，B 走到正确位置；约 15–21 秒逐个讲错的选项（「解説：ア はなぜ ×？」），B 走过去，场上弹出黑色小标签「空く」指出空出来的区域；约 24 秒结尾「全286問・解説つき 動きで覚えるバドミントンの戦術 「BADO TACTICS」で検索」。
- **导流**：Shorts 链接点不了，所以结尾让人**搜名字**。

### 2. 배드민턴 여행「복식 서브 띄우기만 하면 파트너가 웁니다」（韩国，24.9 秒）
- 不是动画，是真人实拍（带配音，屏幕上有小号黄色字幕）。
- **标题大字**：画面上方黑底上两行超大粗体，第一行绿/红两色强调（「라켓 드는 거라고」），第二行白字（「무시하면 계속 당합니다」），全程不动。这是韩国短视频常见的“顶部大标题 + 黑边”版式，可以借用到动画上。

### 3. バドミントンの極意「【サークルの困りごと#13】最後のゲームは点数を先に決める」（日本，34.6 秒，2026-11-19 发，933 播放，2 赞）
- YouTube 标了「由 AI 生成」（内容是加工或 AI 生成）。说明这类号公开标注后照常发。
- **画风**：夜间体育馆、观众席灯光的立体球场；球员是发光的编号圆球（1/2 自己，对手白球）；字幕是日本综艺式「テロップ」：白字黑描边，关键词黄色（「点数は先に決める」）；顶部固定两行标题 + 黄底系列标签「サークルの困りごと #13」。
- **讲法**：不只讲技术，讲**社团里的麻烦事**（最后一局不定分数就打不完、等的人一直等），中间插一张信息卡片（「コート 1 2 / 待ち 3 4 5 6 / 終わりが決まらない」、「規則にある短いゲーム（付録）15点×3 / 11点×5 / 21点×1」），再回到球场演示。
- **结尾就是导流**：最后 1.5 秒切到一张 App 截图（我的页面、排名、积分），大字「仲間もラリーに入れば自分の戦績・レートが見られる」，红色按钮「プロフのLINEから」，再画出主页上的「公式LINE｜戦績・組み合わせ」位置。描述里也写「サークルの戦績・組み合わせは、プロフィールのLINEから」。
- **这就是“技术/社团视频 → 工具”的真实例子，而且是日本的直接竞品**：卖的是社团的战绩和配对，和我们的球群、当晚排场、比赛几乎重合。走的是 LINE，不是下载 App。

### 对我们模板的影响
1. 版式定成三段：**顶部固定（品牌 + 大字问题 + 系列标签和编号）／中间球场／底部文字区按节拍换**。韩国版顶部用两行超大粗体、两色强调。
2. 选项画在球场上（虚线圆圈 + ア/イ/ウ 或 가/나/다），倒数用右上角黄圈数字。错误选项逐个演：人走过去 → 弹出黑色小标签（「空く」/「빈다」）。
3. 字幕用日本「テロップ」风格：白字粗黑描边，关键词黄色。
4. 题目不只讲技术，也讲**社团里的麻烦事**（排队太久、最后一局、生面孔怎么融入），这类题直接对上我们的功能。
5. 结尾导流：Shorts 链接点不了，用「プロフのリンクから」+ 画出主页链接的位置，或者让人搜「Badie」。日本对手导到 LINE，我们导到网页（免下载就能测水平、看球群），这点是我们的优势。
6. 标注：描述里照实写用了 AI 制作（YouTube 也会自动标），不影响发布。

---

## 附：用户给的参考视频（抖音 @灰象 Shawn《Vibe知识大赏》第 3 集，AI 为什么会“涌现”，64 秒；2026-11-19 拆解）

屏幕录像，作者声明“内容由 AI 生成”。录屏时的数据：5,115 赞、312 评论、2,103 收藏、1,052 转发，合集「认知宇宙」。画面按每秒 1 帧拆开看；声音听不到，用程序分析音轨（响度、起音点、节拍）。

### 画面
- **统一的高级感**：近黑的暖棕底，金色发光的线条和粒子；英文小号字母做栏目标签（SCALING LAW、MORE IS DIFFERENT、KAPLAN ET AL. · OPENAI · 2020），中文大标题金色带辉光（涌现、规模定律、尺子太粗）。论文和人名用小字标出处，显得可信。
- **一次只讲一样东西**：每一段画面上只有一个主体：一条正在画出来的曲线、一个计数器（1.0M → 69B → 979B）、一个水分子 → 一大片分子、两根进度条（10% → 68%）。
- **字幕在底部**：两行中文，关键词换成金色（「More is different」「湿」「越聪明」「笔直的线」「突然」「每一位都对」「尺子太粗」「看不见」）。字幕大约**每 4 秒换一句**。
- **章节卡**：换章时整屏只出现一个金色大标题（涌现 / 规模定律 / 尺子太粗），停 2–3 秒，再接内容。

### 叙事结构（64 秒）
钩子问题（AI 为什么会突然开窍？）→ 一个历史故事（1972 年安德森“More is different”）→ 生活类比（一个水分子不湿，亿万个聚在一起才湿）→ 机制（规模定律：loss 在对数坐标上是一条直线，跨 7 个数量级）→ 反转（loss 稳稳降，有些能力却几乎是 0，过了某个规模突然会了）→ 质疑（2023 斯坦福论文：涌现是不是错觉？）→ 具体例子（345 + 234，三位对两位算 0 分，数对了几位就是平滑曲线）→ 收束比喻（尺子太粗）→ 一句结论（能力一直在长，只是那把尺子看不见）。

### 声音和画面的配合（程序测出来的）
- **开头 0–3 秒**：密集的短促起音，约 0.25–0.35 秒一个，和计数器数字往上跳对得上（像“滴答/闪光”音效跟着数字走）。
- **3 秒白光转场前**：响度先掉一下（−13 dB），白光出来时再起。
- **4–11 秒（水分子段）**：整体偏低沉、偏安静（重心频率 400–1,000 Hz），起音很稀，大约 **每 2.1 秒一下低沉的“咚”**，跟着分子一步步变多（1 个 → 10¹⁸ → 10²³）。
- **11.0–11.9 秒：几乎静音（−15 dB）**，紧接着 **11.97 秒画面切到“规模定律”大标题，同一帧音乐整个砸进来**（响度跳到 −7 dB），从这里起是稳定的 **120 BPM**，0.25 秒一格的节拍一直到结尾。
- **之后**：字幕大约每 4 秒（= 2 小节）换一句，跟着节拍走；画面上一串点逐个出现、数字逐位打勾时，有成串的高频短音（约 26–29 秒、46–50 秒）。
- **55.5 秒又空了一下（−14 dB）**，56 秒进入最后的结论段（两根进度条往上长）。
- 规律：**每次换章，先空半秒到一秒，再在切画面的那一帧砸下去**；平时音乐只当节拍器，给字幕和动画定速；具体的小动作（数字跳、点出现、打勾）配短促音效。

### 我们能学的（用到 Badie 的羽毛球动画上）
1. 整套视频定一个统一的“材质”：我们用深色球场绿底 + 柠檬绿发光线条，英文小号栏目标签（DEFENSE · SMASH · SINGLES），保留 Badie 的颜色。
2. 一段只讲一件事；每 4 秒换一句字幕，跟 120 BPM 的两小节走。
3. 换章用整屏大标题，前面空半秒，切画面那一帧下重音（比如“答案：B”、口诀出现时）。
4. 小动作配短音：选项圈弹出、倒数、球落地、打叉各有一个音。
5. 叙事比“出题—揭晓”多一层：问题 → 生活类比 → 机制（直线短、斜线长，用两条线的长度和到达时间画出来）→ 反转（站中间看起来最安全，其实最慢）→ 具体例子 → 一句话口诀。
6. 长度：它 64 秒能撑住，是因为每 4 秒都有新画面。我们第一条先做 30–40 秒。
