// 17.11 · cutscenes — בדיקה של הדף החי: node live_check.js <live.html> <out.json> [shotsDir] — כל כפתור של סצנה מנגן אותה (או מכניס לתור),
// "הסיפור מההתחלה" מנגן את הפתיחה לבד, 0 שגיאות בדף.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file), { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(300) }
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const btns = await p.$$eval('#tcCutBtns button', L => L.map(b => b.textContent));
  const R = { file: path.basename(file), buttons: btns.length, res: [] };
  for (let i = 0; i < btns.length; i++) {
    const name = btns[i]; if (/קפיצה לפרק 3|מטוס נוחת/.test(name)) { R.res.push({ name, skipped: 'מחכה לנחיתה' }); continue }
    await p.$$eval('#tcCutBtns button', (L, i) => L[i].click(), i); await p.waitForTimeout(1600);
    const s = await ev("(()=>{const s=TCCUT.state();return{on:s.on&&s.on.id,q:s.q,err:s.err}})()"); R.res.push({ name, ...s });
    if (shots && s.on && i % 3 === 0) { try { fs.mkdirSync(shots, { recursive: true }); await p.screenshot({ path: path.join(shots, 'live_' + i + '.png') }) } catch (e) {} }
    await ev("(()=>{TCCUT.end();return 1})()"); await p.waitForTimeout(300) }
  R.msg = await p.$eval('#tcCutMsg', e => e.textContent).catch(() => ''); R.line = await p.$eval('#tcCutLine', e => e.textContent).catch(() => '');
  R.img = await p.evaluate(() => document.querySelectorAll('img').length);
  R.pageErrors = pe; R.ok = !pe.length && R.res.filter(r => !r.skipped).every(r => r.on || (r.q && r.q.length) || /^קפיצה|^הסיפור/.test(r.name));
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, buttons: R.buttons, played: R.res.filter(r => r.on).length, res: R.res.map(r => (r.on || r.skipped || (r.q || []).join() || '-')), errs: pe.length, line: R.line }));
  await b.close();
})().catch(e => { console.error(e); process.exit(1) });
