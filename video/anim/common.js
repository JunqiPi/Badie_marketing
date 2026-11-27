// 战术动画（站位题系列）共用的代码：镜头、球场、勾叉、球、文字（标题、字幕、章节卡、场景小标签）。
// 每条视频的页面先加载这个文件，再写自己的场景（人站哪、球怎么飞、什么时候出什么）。
// 页面要自己定义：FULL（全场镜头，ZF 按它算粗细），T（时间点，至少有 loop、dur、end、title）。
// 坐标都是“米”：原点 = 网的中点，x 向右、y 向我方为正。镜头 = (cx, cy, s)：把 (cx, cy) 米放在屏幕 (540, 857)，每米 s 像素。
'use strict';
const NS = 'http://www.w3.org/2000/svg';
const $ = (id) => document.getElementById(id);
const LIME = '#D4F33F', WARM = '#FF6A3D', PALE = '#E6F0E2';
// 安全区（2026-11-21）：手机上 Shorts / Reels / TikTok 的界面会盖住顶上、底下和右边。
// 字、人、球、标签都要在这个框里；球场线和背景可以伸出去。顶栏（Badie、系列名、问题）在 y 300–396。
const SAFE = { left: 60, top: 300, right: 940, bottom: 1500 };
const TEXT_W = 2 * (SAFE.right - 540) - 20;            // 居中的字最多这么宽（780），右边不进右侧 140 px

// ---- 镜头 ----
const SCX = 540, SCY = 857;
let CAM = { cx: 0, cy: 0, s: 100 };
const X = (x) => SCX + (x - CAM.cx) * CAM.s;
const Y = (y) => SCY + (y - CAM.cy) * CAM.s;
const ZF = () => Math.pow(CAM.s / FULL.s, 0.45);      // 点、线粗细跟镜头轻微变大
const HK = () => 0.16 * CAM.s;                          // 球高 1 米 = 屏幕上移 0.16 米

// 镜头在 t 秒的位置。moves = [[开始, 结束, 从, 到], ...]，按时间排好；循环段（T.loop 之后）从 1.05 倍缩回全场
function camAt(t, moves) {
  if (t >= T.loop) {
    const k = tw(t, T.loop, T.dur - 0.05);
    return { cx: FULL.cx, cy: FULL.cy, s: FULL.s * lerp(1.05, 1, k) };
  }
  let c = FULL;
  for (const [t0, t1, a, b] of moves) {
    if (t >= t1) c = b;
    else if (t > t0) {
      const k = easeInOut((t - t0) / (t1 - t0));
      // 缩放按对数插值，推拉速度看起来均匀
      return { cx: lerp(a.cx, b.cx, k), cy: lerp(a.cy, b.cy, k), s: Math.exp(lerp(Math.log(a.s), Math.log(b.s), k)) };
    } else break;
  }
  return c;
}

// ---- 数学 ----
// 杀球的速度：只有阻力的减速模型 s(t) = L ln(1 + v0 t / L)。数值只用来排先后，不上屏。
const L0 = 4.6, V0 = 60;
const sOf = (t) => L0 * Math.log(1 + V0 * Math.max(0, t) / L0);
const tOf = (s) => (Math.exp(s / L0) - 1) * L0 / V0;
const dist = (a, b) => Math.hypot(b[0] - a[0], b[1] - a[1]);
const lerp = (a, b, k) => a + (b - a) * k;
const lerp2 = (p, q, k) => [lerp(p[0], q[0], k), lerp(p[1], q[1], k)];
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const easeOutCubic = (t) => 1 - (1 - t) ** 3;
const easeInOut = (t) => (t < .5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2);
const easeOutBack = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2; };
const lin = (x) => x;
const tw = (t, t0, t1, e = easeOutCubic) => e(clamp01((t - t0) / (t1 - t0)));
const vis = (t, t0, t1, d = 0.3, d2 = 0.2) => Math.min(tw(t, t0, t0 + d), 1 - tw(t, t1 - d2, t1, lin));
const angW = (p, q) => Math.atan2(q[1] - p[1], q[0] - p[0]) * 180 / Math.PI;   // 米坐标和屏幕同向

// ---- SVG ----
function el(tag, attrs, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function setLine(path, from, to, p, op, w) {          // 从 from 画到 to，p = 画出来的比例
  const x1 = X(from[0]), y1 = Y(from[1]), x2 = X(to[0]), y2 = Y(to[1]);
  path.setAttribute('d', `M${x1},${y1} L${x2},${y2}`);
  const L = Math.hypot(x2 - x1, y2 - y1);
  path.style.strokeDasharray = `${L} ${L}`;
  path.style.strokeDashoffset = L * (1 - clamp01(p));
  path.setAttribute('opacity', op);
  path.setAttribute('stroke-width', w);
}
function setSeg(line, x1, y1, x2, y2, op, w) {        // 屏幕像素的线段
  line.setAttribute('x1', x1); line.setAttribute('y1', y1); line.setAttribute('x2', x2); line.setAttribute('y2', y2);
  line.setAttribute('opacity', op); line.setAttribute('stroke-width', w);
}
function pulse(c, at, t, t0) {                          // 落点上扩散的一圈
  const k = (t - t0) / 0.7;
  if (k < 0 || k > 1) { c.setAttribute('opacity', 0); return; }
  c.setAttribute('cx', X(at[0])); c.setAttribute('cy', Y(at[1]));
  c.setAttribute('r', (8 + 26 * easeOutCubic(k)) * ZF()); c.setAttribute('opacity', 1 - k);
}

// ---- 球场 ----
// mode = 'singles'：单打边线亮、双打边线和双打后发球线暗、两边的细带更暗；
// mode = 'doubles'：双打边线亮、单打边线和双打后发球线暗（打双打时，场地两边以双打边线为界）
const court = {};
function buildCourt(mode) {
  const g = $('court');
  court.floor = el('rect', { fill: '#0F2218', stroke: 'rgba(226,242,220,.08)', 'stroke-width': 2, rx: 18 }, g);   // 场边地面，一直铺到画面底下
  court.alley = el('rect', { fill: mode === 'doubles' ? '#132A1D' : '#0C1912' }, g);
  court.singles = el('rect', { fill: '#132A1D' }, g);
  court.lit = el('g', { stroke: 'rgba(226,242,220,.8)', fill: 'none', filter: 'url(#g1)' }, g);
  court.dim = el('g', { stroke: 'rgba(226,242,220,.32)', fill: 'none' }, g);
  const X2 = 3.05, X1 = 2.59, Yb = 6.7, SS = 1.98, LSV = 5.94;
  court.lines = [];
  const L = (grp, a, b, c, d) => court.lines.push([el('line', {}, grp), a, b, c, d]);
  const side = mode === 'doubles' ? [court.lit, court.dim] : [court.dim, court.lit];   // [双打边线, 单打边线]
  L(side[0], -X2, -Yb, -X2, Yb); L(side[0], X2, -Yb, X2, Yb);
  L(court.dim, -X2, -LSV, X2, -LSV); L(court.dim, -X2, LSV, X2, LSV);
  L(side[1], -X1, -Yb, -X1, Yb); L(side[1], X1, -Yb, X1, Yb);
  L(court.lit, -X2, -Yb, X2, -Yb); L(court.lit, -X2, Yb, X2, Yb);
  L(court.lit, -X2, -SS, X2, -SS); L(court.lit, -X2, SS, X2, SS);
  L(court.lit, 0, -Yb, 0, -SS); L(court.lit, 0, SS, 0, Yb);
  court.net = el('line', { stroke: '#EEF6EA', filter: 'url(#g1)' }, g);
  court.p1 = el('circle', { fill: '#EEF6EA' }, g);
  court.p2 = el('circle', { fill: '#EEF6EA' }, g);
  court.tag = el('text', { 'text-anchor': 'end', 'font-family': 'BLAB', 'font-weight': 600, 'letter-spacing': '0.25em', fill: 'rgba(230,240,226,.55)' }, g);
}
function drawCourt() {
  const z = ZF();
  const X2 = 3.05, X1 = 2.59, Yb = 6.7;
  const rect = (r, x0, y0, x1, y1) => { r.setAttribute('x', X(x0)); r.setAttribute('y', Y(y0)); r.setAttribute('width', X(x1) - X(x0)); r.setAttribute('height', Y(y1) - Y(y0)); };
  rect(court.floor, -X2 - 2.2, -Yb - 2.2, X2 + 2.2, Yb + 3.2);
  rect(court.alley, -X2, -Yb, X2, Yb); rect(court.singles, -X1, -Yb, X1, Yb);
  court.lit.setAttribute('stroke-width', 2.6 * Math.sqrt(z)); court.dim.setAttribute('stroke-width', 2 * Math.sqrt(z));
  for (const [e, a, b, c, d] of court.lines) { e.setAttribute('x1', X(a)); e.setAttribute('y1', Y(b)); e.setAttribute('x2', X(c)); e.setAttribute('y2', Y(d)); }
  const n0 = X(-X2) - 10 * z, n1 = X(X2) + 10 * z, ny = Y(0);
  court.net.setAttribute('x1', n0); court.net.setAttribute('x2', n1); court.net.setAttribute('y1', ny); court.net.setAttribute('y2', ny);
  court.net.setAttribute('stroke-width', 3 * Math.sqrt(z));
  for (const [p, x] of [[court.p1, n0], [court.p2, n1]]) { p.setAttribute('cx', x); p.setAttribute('cy', ny); p.setAttribute('r', 5 * Math.sqrt(z)); }
  court.tag.setAttribute('x', X(-X2) - 14); court.tag.setAttribute('y', Y(0) + 26 * z);
  court.tag.setAttribute('font-size', 19 * Math.sqrt(z));
  const tagW = court.tag._w || (court.tag._w = court.tag.getComputedTextLength() || 60);
  court.tag.setAttribute('opacity', clamp01((X(-X2) - 14 - tagW - SAFE.left) / 30));   // 推近时标签会出安全区，就不显示
}

// ---- 勾和叉 ----
function mark(kind, color, size) {
  const g = el('g', { opacity: 0 }, $('marks'));
  el('circle', { r: size, fill: '#0E1A14', stroke: color, 'stroke-width': 3, filter: 'url(#g1)' }, g);
  const s = size * 0.5;
  const d = kind === 'ok' ? `M${-s * .9},${s * .05} L${-s * .25},${s * .65} L${s},${-s * .6}` : `M${-s * .7},${-s * .7} L${s * .7},${s * .7} M${s * .7},${-s * .7} L${-s * .7},${s * .7}`;
  el('path', { d, fill: 'none', stroke: color, 'stroke-width': size * 0.22, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  return g;
}
function showMark(m, x, y, t, t0, t1) {
  const k = clamp01((t - t0) / 0.3), out = 1 - clamp01((t - t1) / 0.2);
  const sc = t < t0 ? 0 : easeOutBack(k) * ZF();
  m.setAttribute('opacity', t < t0 ? 0 : Math.min(1, k * 2) * out);
  m.setAttribute('transform', `translate(${x},${y}) scale(${Math.max(0.001, sc)})`);
}

// ---- 球 ----
// 球的状态：{ p: 地面位置（米）, h: 高度（米）, fly: 在飞（画拖尾）, op: 透明度 }。阴影走地面，球 = 阴影往上偏 HK × 高度
const shuttles = {};
function buildShuttle(id) {
  const g = $(id);
  const shadow = el('ellipse', { fill: 'rgba(0,0,0,.55)' }, g);
  const trail = [];
  for (let i = 0; i < 8; i++) trail.push(el('circle', { fill: '#F6FFE8' }, g));
  const head = el('circle', { fill: '#FFFFFF', filter: 'url(#g2)' }, g);
  shuttles[id] = { g, shadow, trail, head };
}
function drawShuttle(id, fn, t) {
  const s = shuttles[id], z = ZF(), hk = HK();
  const cur = fn(t);
  if (!cur || cur.op <= 0) { s.g.setAttribute('opacity', 0); return; }
  const x = X(cur.p[0]), y = Y(cur.p[1]);
  // 球飞进顶上的安全区外（顶栏后面）时淡掉，不和顶栏抢
  s.g.setAttribute('opacity', cur.op * clamp01((y - hk * cur.h - (SAFE.top + 100)) / 30));   // 顶栏底边 y≈398，球到 430 才完全出来
  s.shadow.setAttribute('cx', x); s.shadow.setAttribute('cy', y + 2);
  s.shadow.setAttribute('rx', 6 * z); s.shadow.setAttribute('ry', 3 * z);
  s.shadow.setAttribute('opacity', 0.9 - Math.min(0.6, cur.h * 0.1));
  s.head.setAttribute('cx', x); s.head.setAttribute('cy', y - hk * cur.h); s.head.setAttribute('r', 7 * z);
  for (let i = 0; i < s.trail.length; i++) {
    const p = fn(t - (i + 1) * 0.03);
    const c = s.trail[i];
    if (!p || !cur.fly || !p.fly) { c.setAttribute('opacity', 0); continue; }
    c.setAttribute('cx', X(p.p[0])); c.setAttribute('cy', Y(p.p[1]) - hk * p.h);
    c.setAttribute('r', (5 - i * 0.45) * z); c.setAttribute('opacity', 0.55 * (1 - i / 8));
  }
}
const smashH = (f) => 2.8 * (1 - f ** 3);              // 杀球从 2.8 米高打下来，俯视几乎是直线
function smashAt(from, to, realT, len) {                // 真实时间 realT 秒时杀球在哪（len = from 到 to 的距离）
  const f = Math.min(1, sOf(realT) / len);
  return { p: lerp2(from, to, f), h: smashH(f), fly: f < 1, f };
}
function blockAt(from, h0, to, k) {                     // 挡回去：k 从 0 到 1
  return { p: lerp2(from, to, easeOutCubic(k)), h: lerp(h0, 0.4, k) + 1.4 * Math.sin(Math.PI * k), fly: k < 1 };
}

// ---- 文字 ----
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, '<span class="hl">$1</span>');   // **词** = 荧光绿重点词
function measureW(e) {
  const prev = e.style.display; e.style.display = 'inline-block'; e.style.width = 'auto';
  const w = e.getBoundingClientRect().width; e.style.display = prev; e.style.width = '';
  return w;
}
function fitText(e, size, maxW) {                       // 从 size 开始缩，直到宽度放得下
  let s = size;
  e.style.fontSize = s + 'px';
  while (measureW(e) > maxW && s > 20) { s -= 2; e.style.fontSize = s + 'px'; }
  return s;
}
// 场景里的小标签（文字在脚本 JSON 的 labels 里）：贴在它说的东西旁边，align = 'l' / 'r' / 'c' 是 (x, y) 在标签的哪一边
let LBL = {};
function placeLabel(k, t, t0, t1, x, y, align) {
  const e = LBL[k];
  const v = vis(t, t0, t1, 0.25, 0.2);
  if (v <= 0) { e.style.opacity = 0; return; }
  const sc = lerp(0.8, 1, easeOutBack(clamp01((t - t0) / 0.25)));
  // 按标签宽度算出左边，再夹在安全区里（右边不进右侧 140 px）
  const w = e._w || (e._w = e.offsetWidth), h = e._h || (e._h = e.offsetHeight);
  let left = align === 'r' ? x - w : align === 'c' ? x - w / 2 : x;
  left = Math.min(SAFE.right - w, Math.max(SAFE.left, left));
  const top = Math.min(SAFE.bottom - h, Math.max(SAFE.top + 100, y - h / 2));
  e.style.opacity = v;
  e.style.transform = `translate(${left}px,${top}px) scale(${sc})`;
}
function hideLabels() { for (const e of Object.values(LBL)) e.style.opacity = 0; }

// 排好所有的字。cfg = { sizes, cardY, bigY, labelStyle }：每种语言的字号、每张卡的中心 y、开头大字的中心 y、标签颜色
let TX, SUBS = [], CARDS = [], BIG_Y = 540;
function setupText(spec, lang, cfg) {
  TX = spec.text[lang];
  document.body.className = TX.font;
  const Z = cfg.sizes[TX.font];
  BIG_Y = cfg.bigY;
  $('series').textContent = TX.series;
  $('title').innerHTML = md(TX.title.replace(/\n/g, ' ')); fitText($('title'), Z.title, TEXT_W);
  $('titleBig').innerHTML = md(TX.titleBig || TX.title); fitText($('titleBig'), Z.big, TEXT_W);
  const bigH = $('titleBig').getBoundingClientRect().height;
  $('titleBig').style.top = (BIG_Y - bigH / 2) + 'px';
  for (const [k, cls] of Object.entries(cfg.labelStyle)) {
    const e = document.createElement('div'); e.className = 'lbl ' + cls; e.textContent = TX.labels[k];
    $('labels').appendChild(e); LBL[k] = e;
  }
  const subs = $('subs');
  SUBS = spec.subs.map(([t0, t1, key]) => {
    const e = document.createElement('div'); e.className = 't sub'; e.innerHTML = '<span class="cap">' + md(TX[key]) + '</span>';
    subs.appendChild(e); fitText(e, Z.sub, 780);
    return { t0, t1, e };
  });
  const cards = $('cards');
  CARDS = spec.cards.map(([t0, t1, key]) => {
    const [label, text] = TX[key];
    const l = document.createElement('div'); l.className = 't lab clab'; l.textContent = label;
    const c = document.createElement('div'); c.className = 't ctxt'; c.innerHTML = md(text);
    cards.appendChild(l); cards.appendChild(c);
    const lines = text.split('\n').length;
    const fs = fitText(c, lines > 1 ? Math.round(Z.card * 0.78) : Z.card, TEXT_W);
    const h = fs * 1.18 * lines, cy = cfg.cardY[key];
    c.style.top = (cy - h / 2 + 18) + 'px'; l.style.top = (cy - h / 2 - 34) + 'px';
    return { t0, t1, l, c, key, cy };
  });
}

// 每一帧的字：章节卡（带后面的暗圈）、字幕（顶边在 capTop）、开头的大字问题缩进顶部、片尾 Badie 大字
function renderText(t, capTop) {
  let scrim = 0, scrimY = 790;
  for (const c of CARDS) {
    const v = vis(t, c.t0, c.t1, 0.3, 0.2);
    const k = clamp01((t - c.t0) / 0.3);
    const sc = t < c.t0 ? 0.9 : lerp(0.9, 1, easeOutBack(k));
    c.l.style.opacity = v; c.c.style.opacity = v;
    c.c.style.transform = `scale(${sc})`;
    c.l.style.transform = `translateY(${(1 - easeOutCubic(k)) * 12}px)`;
    if (v > scrim) { scrim = v; scrimY = c.cy; }
  }
  $('scrim').setAttribute('opacity', scrim);
  // 网旁的“单打/双打”在卡片、开头大字底下时先藏起来，免得字叠字
  const tbV = t >= T.title && t < 3.1 ? 1 : 0;
  if (court.tag) court.tag.setAttribute('opacity', parseFloat(court.tag.getAttribute('opacity') || 1) * (1 - Math.min(1, 10 * Math.max(scrim, tbV))));
  $('scrim').setAttribute('cy', scrimY);

  for (const s of SUBS) {
    const v = vis(t, s.t0, s.t1, 0.3, 0.2);
    const k = clamp01((t - s.t0) / 0.3);
    s.e.style.opacity = v;
    s.e.style.top = capTop + 'px';
    s.e.style.transform = `scale(${lerp(0.94, 1, easeOutBack(k))})`;
  }
  // 开头的问题：先大字压在球场中间，2.7–3.1 秒缩进顶部，之后一直挂在顶上
  const tk = clamp01((t - T.title) / 0.3);
  const up = tw(t, 2.7, 3.1, easeInOut);
  const tb = $('titleBig');
  tb.style.opacity = t < T.title ? 0 : Math.min(1, tk * 1.5) * (1 - up);
  const smallC = $('title').offsetTop + 24;                    // 顶部那行的中心 y（跟着页面里 #title 的位置）
  tb.style.transform = `translateY(${(smallC - BIG_Y) * up}px) scale(${(t < T.title ? 0.9 : lerp(0.9, 1, easeOutBack(tk))) * lerp(1, 0.5, up)})`;
  $('title').style.opacity = tw(t, 2.95, 3.25) * (1 - tw(t, T.end, T.end + 0.25));
  const ek = clamp01((t - (T.end + 0.15)) / 0.3);
  const eOut = tw(t, T.loop, T.dur - 0.1);
  $('endmark').style.opacity = t < T.end + 0.15 ? 0 : Math.min(1, ek * 1.5) * (1 - eOut);
  $('endmark').style.transform = `scale(${(t < T.end + 0.15 ? 0.85 : lerp(0.85, 1, easeOutBack(ek))) * (1 - 0.12 * eOut)})`;
}

// ---- 冲击效果（2026-11-23，可选）----
// 只有脚本 JSON 里有 "impact" 才开；没有这个字段时下面几个函数什么都不做（impactWarp 原样返回 t），旧集画面不变。
// impact.events = [{ type: 'smash'|'block'|'land', at: 秒, p: [x, y] 米, h: 高度米, dur: 杀球飞行秒（smash 才要）,
//                    stop: 停 2 帧, shake: 镜头震 4 帧, slow: 慢放段（声音放慢，画面不用管）, quiet: 不出声 }]
// 页面要做三件事：setup 里调 setupImpact(spec)；render 里 ts = impactWarp(ts)；画完球之后调 renderImpact(ts, 球的函数)。
// 时间都按帧对齐：事件落在 at 之后的第一帧（声音在 make_anim.py 里用同样的取整），冲击绝不提前。
let IMP = null;
const IMP_FPS = 30, IMP_STOP = 2, IMP_SHAKE = 4;
const impFrame = (at) => Math.ceil(at * IMP_FPS - 1e-6) / IMP_FPS;
function setupImpact(spec) {
  if (!spec.impact || !spec.impact.events || !spec.impact.events.length) return;
  const w = $('world'), g = el('g', { id: 'impact' }, w);
  // 冲击层不压顶栏：顶栏下沿（SAFE.top + 100）往下 40 px 渐显，上面的白光、冲击圈都看不见
  const defs = document.querySelector('#svg defs');
  if (defs) {
    const mk = el('mask', { id: 'impMask', maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: 1080, height: 1920 }, defs);
    const gr = el('linearGradient', { id: 'impFade', gradientUnits: 'userSpaceOnUse', x1: 0, y1: SAFE.top + 100, x2: 0, y2: SAFE.top + 140 }, defs);
    el('stop', { offset: 0, 'stop-color': '#000' }, gr); el('stop', { offset: 1, 'stop-color': '#fff' }, gr);
    el('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: 'url(#impFade)' }, mk);
    g.setAttribute('mask', 'url(#impMask)');
  }
  IMP = { ev: spec.impact.events.map((e) => ({ ...e, f: impFrame(e.at) })), g };
  IMP.trail = [];
  for (let i = 0; i < 10; i++) IMP.trail.push(el('line', { stroke: '#FFFFFF', 'stroke-linecap': 'round' }, g));
  IMP.speed = [el('line', { stroke: '#F6FFE8', 'stroke-linecap': 'round' }, g), el('line', { stroke: '#F6FFE8', 'stroke-linecap': 'round' }, g)];
  for (const e of IMP.ev) {
    if (e.type === 'smash') {
      e.flash = el('circle', { fill: '#FFFFFF', filter: 'url(#g2)' }, g);
      e.ring = el('circle', { fill: 'none', stroke: '#FFFFFF', filter: 'url(#g1)' }, g);
      e.spikes = [];
      for (let i = 0; i < 8; i++) e.spikes.push(el('line', { stroke: '#FFFFFF', 'stroke-linecap': 'round' }, g));
    } else {
      e.ring = el('circle', { fill: 'none', stroke: e.type === 'land' ? '#E6F0E2' : '#D4F33F', filter: 'url(#g1)' }, g);
    }
  }
}
// 停帧：事件那一帧之后 2 帧，画面停在事件那一刻（字、镜头照常走，只有球场里的人和球停）
function impactWarp(t) {
  if (!IMP) return t;
  for (const e of IMP.ev) if (e.stop && t >= e.f && t < e.f + IMP_STOP / IMP_FPS) return e.f;
  return t;
}
// 镜头震：4 帧，像素偏移逐帧减小，方向固定（每次结果一样）
function impactShake(t) {
  if (!IMP) return [0, 0];
  const pat = [[7, -5], [-6, 4], [4, -2], [-2, 1]];
  for (const e of IMP.ev) {
    if (!e.shake) continue;
    const n = Math.round((t - e.f) * IMP_FPS);
    if (n >= 0 && n < IMP_SHAKE) { const k = e.type === 'land' ? 0.6 : 1; return [pat[n][0] * k, pat[n][1] * k]; }
  }
  return [0, 0];
}
function renderImpact(t, shFn, rawT) {                 // t = 停帧后的时间；rawT = 真实时间（镜头震按它算）
  if (!IMP) return;
  const z = ZF(), hk = HK();
  const [dx, dy] = impactShake(rawT === undefined ? t : rawT);
  $('world').setAttribute('transform', dx || dy ? `translate(${dx},${dy})` : '');
  for (const l of IMP.trail) l.setAttribute('opacity', 0);
  for (const l of IMP.speed) l.setAttribute('opacity', 0);
  for (const e of IMP.ev) {
    const px = X(e.p[0]), py = Y(e.p[1]) - hk * (e.h || 0);
    const k = (t - e.f) / 0.22;
    if (e.type === 'smash') {
      // 击球点：前 2 帧一团白光，再散成一圈和 8 根短刺
      const on = k >= 0 && k < 1;
      const core = t >= e.f && t < e.f + 3 / IMP_FPS ? 1 - (t - e.f) * IMP_FPS / 3 : 0;
      e.flash.setAttribute('cx', px); e.flash.setAttribute('cy', py);
      e.flash.setAttribute('r', (18 + 10 * core) * z); e.flash.setAttribute('opacity', 0.95 * core);
      e.ring.setAttribute('cx', px); e.ring.setAttribute('cy', py);
      e.ring.setAttribute('r', on ? (14 + 58 * easeOutCubic(k)) * z : 0); e.ring.setAttribute('opacity', on ? 0.9 * (1 - k) : 0);
      e.ring.setAttribute('stroke-width', on ? (5 - 3 * k) * z : 0);
      e.spikes.forEach((s, i) => {
        const a = (i / 8) * Math.PI * 2 + 0.2, r0 = (20 + 40 * easeOutCubic(k)) * z, r1 = r0 + (18 - 10 * k) * z;
        setSeg(s, px + Math.cos(a) * r0, py + Math.sin(a) * r0, px + Math.cos(a) * r1, py + Math.sin(a) * r1, on ? 0.85 * (1 - k) : 0, 3 * z);
      });
      // 飞行中：更长更亮的拖尾（往回取 0.14 秒的位置，越往后越细越淡）+ 两根细速度线
      if (shFn && t >= e.f && t < e.f + (e.dur || 0.4)) {
        const pts = [];
        for (let i = 0; i <= 10; i++) {
          const tt = t - i * 0.014;
          if (tt < e.at) break;
          const s = shFn(tt); if (!s) break;
          pts.push([X(s.p[0]), Y(s.p[1]) - hk * s.h]);
        }
        for (let i = 0; i + 1 < pts.length; i++) {
          const f = i / 10;
          setSeg(IMP.trail[i], pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 0.95 * (1 - f), (11 - 9 * f) * z);
        }
        if (pts.length > 3) {
          const a = pts[0], b = pts[pts.length - 1], L = Math.hypot(a[0] - b[0], a[1] - b[1]) || 1;
          const nx = -(a[1] - b[1]) / L, ny = (a[0] - b[0]) / L, off = 16 * z;
          for (const [j, sgn] of [[0, 1], [1, -1]]) {
            const m = 0.25 + 0.15 * j;
            setSeg(IMP.speed[j], lerp(a[0], b[0], m) + nx * off * sgn, lerp(a[1], b[1], m) + ny * off * sgn,
              lerp(a[0], b[0], 1.25) + nx * off * sgn, lerp(a[1], b[1], 1.25) + ny * off * sgn, 0.5, 2.2 * z);
          }
        }
      }
    } else {
      // 接杀 / 挡网：拍面上一个小冲击圈；落地：地上一圈淡的
      const on = k >= 0 && k < 1, big = e.type === 'land' ? 34 : 28;
      e.ring.setAttribute('cx', px); e.ring.setAttribute('cy', py);
      e.ring.setAttribute('r', on ? (8 + big * easeOutCubic(k)) * z : 0);
      e.ring.setAttribute('opacity', on ? (e.type === 'land' ? 0.6 : 0.95) * (1 - k) : 0);
      e.ring.setAttribute('stroke-width', on ? (4 - 2 * k) * z : 0);
    }
  }
}
