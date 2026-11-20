// 逐帧渲染动画页面（window.setup / window.render(t)），把 PNG 帧直接喂给 ffmpeg 编码成无声的 H.264。
// 用法：
//   node render_anim.cjs <page.html> <spec.json> <lang> <out.mp4>          整片
//   node render_anim.cjs <page.html> <spec.json> <lang> <dir> --png 2.6,9.3  只截这几个时间点的 PNG
// ffmpeg 路径从环境变量 FFMPEG 来（make_anim.py 用 imageio_ffmpeg 查出来传进来）。
// 浏览器：默认用 Playwright 自带的 Chromium；BADIE_BROWSER_CHANNEL=msedge 可以换成本机的 Edge。
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { once } = require('events');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const [, , pagePath, specPath, lang, out, flag, times] = process.argv;
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const FPS = spec.fps || 30;
const N = Math.round(spec.duration * FPS);

(async () => {
  const browser = await chromium.launch(process.env.BADIE_BROWSER_CHANNEL ? { channel: process.env.BADIE_BROWSER_CHANNEL } : {});
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('page error:', e.message); process.exit(1); });
  await page.goto(pathToFileURL(path.resolve(pagePath)).href, { waitUntil: 'load' });
  // 先等字体，再排字（排字时要量宽度）
  await page.evaluate(async () => {
    await Promise.all(['BZH', 'BJA', 'BKO', 'BEN', 'BLAB'].map((f) => document.fonts.load(`900 40px ${f}`, 'Badie 杀球スマッシュ스매시')));
    await document.fonts.ready;
  });
  const info = await page.evaluate(([s, l]) => window.setup(s, l), [spec, lang]);
  await page.evaluate(() => document.fonts.ready);
  console.error(`[${lang}] fonts loaded: ${info.fonts.join(', ')}`);

  if (flag === '--png') {
    fs.mkdirSync(out, { recursive: true });
    for (const t of times.split(',').map(Number)) {
      await page.evaluate((x) => window.render(x), t);
      await page.screenshot({ path: path.join(out, `${lang}-${t.toFixed(2)}.png`), animations: 'disabled', caret: 'hide' });
    }
    await browser.close();
    return;
  }

  const ff = spawn(process.env.FFMPEG || 'ffmpeg', [
    '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-tune', 'animation', '-profile:v', 'high',
    '-g', '15', '-bf', '2', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-movflags', '+faststart', out,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < N; i++) {
    await page.evaluate((x) => window.render(x), i / FPS);
    const png = await page.screenshot({ type: 'png', animations: 'disabled', caret: 'hide' });
    if (!ff.stdin.write(png)) await once(ff.stdin, 'drain');
    if (i % 150 === 0) console.error(`[${lang}] frame ${i}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  const [code] = await once(ff, 'close');
  await browser.close();
  if (code !== 0) { console.error('ffmpeg failed'); process.exit(1); }
  console.error(`[${lang}] done ${out}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})();
