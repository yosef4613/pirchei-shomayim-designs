// mapfix: node mrun.js <build> <steps.json> <outdir> — steps: {ev}, {shot,clip?}, {wait}, {key}, {click:[x,y]}, {vp:[w,h]}
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, stepsF, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const steps = JSON.parse(fs.readFileSync(stepsF, 'utf8'));
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const vp = steps.vp || [1280, 800];
  const p = await b.newPage({ viewport: { width: vp[0], height: vp[1] }, hasTouch: !!steps.touch, isMobile: !!steps.touch });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') pe.push('console: ' + m.text().slice(0, 200)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const res = [];
  for (const s of steps.list) {
    try {
      if (s.ev) res.push({ ev: s.ev.slice(0, 80), r: await ev(s.ev) });
      else if (s.wait) await p.waitForTimeout(s.wait);
      else if (s.key) await p.keyboard.press(s.key);
      else if (s.click) { if (steps.touch) await p.touchscreen.tap(s.click[0], s.click[1]); else await p.mouse.click(s.click[0], s.click[1]) }
      else if (s.shot) await p.screenshot({ path: path.join(out, s.shot + '.png'), clip: s.clip });
      else if (s.waitfor) await p.waitForFunction(x => window.__TC_DEV.ev(x), s.waitfor, { timeout: s.t || 120000, polling: 500 });
    } catch (e) { res.push({ step: s, err: String(e).slice(0, 300) }) }
  }
  console.log(JSON.stringify({ res, pe }, null, 1));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
