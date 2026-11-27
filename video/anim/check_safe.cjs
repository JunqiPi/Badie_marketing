// 逐 0.1 秒量字、标签、人、球的框，报出出了安全区（x 60–940、y 300–1500）的东西。用法：node check_safe.cjs page.html spec.json lang
const path = require('path'); const fs = require('fs'); const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const [, , pagePath, specPath, lang] = process.argv;
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
(async () => {
  const browser = await chromium.launch(process.env.BADIE_BROWSER_CHANNEL ? { channel: process.env.BADIE_BROWSER_CHANNEL } : {});
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto(pathToFileURL(path.resolve(pagePath)).href);
  await page.evaluate(async () => { await Promise.all(['BZH','BJA','BKO','BEN','BLAB'].map((f) => document.fonts.load(`900 40px ${f}`, 'Badie'))); await document.fonts.ready; });
  await page.evaluate(([s, l]) => window.setup(s, l), [spec, lang]);
  const bad = await page.evaluate(() => {
    const out = {};
    const S = { l: 58, t: 298, r: 942, b: 1502 };
    for (let i = 0; i <= 376; i++) {
      const t = i / 10; window.render(t);
      const els = [...document.querySelectorAll('#subs .cap, #cards .t, #labels .lbl, #titleBig, #title, #series, #wordmark, #players > g, #opps > g, #sh1 circle, #sh2 circle, #marks > g, #opts > g')];
      for (const e of els) {
        let op = 1, n = e; while (n && n !== document.body) { const o = parseFloat(getComputedStyle(n).opacity); const a = n.getAttribute && n.getAttribute('opacity'); op *= o * (a !== null && a !== '' ? parseFloat(a) : 1); n = n.parentNode; }
        if (op < 0.15) continue;
        const r = e.getBoundingClientRect(); if (r.width === 0) continue;
        if (r.left < S.l || r.right > S.r || r.top < S.t || r.bottom > S.b) {
          const id = (e.id || e.className.baseVal || e.className || e.tagName) + ':' + (e.textContent || '').slice(0, 14);
          const k = id + ` [${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}]`;
          (out[id] = out[id] || []).push(t.toFixed(1) + ' ' + `[${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}]`);
        }
      }
    }
    return out;
  });
  for (const [k, v] of Object.entries(bad)) console.log(k, v.length, v[0], '...', v[v.length - 1]);
  await browser.close();
})();
