// probe_mx.js — fieldfix: התחזוקה — מצב הזוגות, הבדיקה, וצילום ההאנגרים (המכונאים). node probe_mx.js <build> <outdir> <tag>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, tag, off] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + (off ? '?ffeast=0' : '') + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) { } await p.waitForTimeout(300) }
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const fn = (f, a) => ev('JSON.stringify((' + f.toString() + ')(' + JSON.stringify(a || {}) + '))').then(s => { try { return JSON.parse(s) } catch (e) { return s } });
  const R = {};
  R.mx = await fn(() => { const o = {}; try { o.maint = window.__TC_FIELDFIX.maint(); o.audit = window.__TC_FIELDFIX.maintAudit(); o.r3 = ffR3Audit().ok; o.live = tcLiveAddAudit(); o.hg = FFR3.build().map(m => [m.id, m.ac, m.key, Math.round(m.start[0]), Math.round(m.start[1])]); o.fl = window.__TC_FIELDFIX.flights() } catch (e) { o.e = String(e) } return o });
  fs.writeFileSync(path.join(out, tag + '_mx.json'), JSON.stringify(R, null, 1));
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e); for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  const L = (R.mx.hg || []).filter(h => /^MX-/.test(h[2])).map(h => [h[0], h[3], h[4] - 40, 1.4]);
  for (const [nm, x, y, z] of L) {
    await ev('(' + ((o) => { try { State.mapQa = true } catch (e) { } try { c34Night(0) } catch (e) { } Camera.x = o.x; Camera.y = o.y; Camera.zoom = o.z; return 1 }).toString() + ')(' + JSON.stringify({ x, y, z }) + ')');
    await p.waitForTimeout(6000); await p.screenshot({ path: path.join(out, tag + '_' + nm + '.png') });
  }
  R.errs = errs; fs.writeFileSync(path.join(out, tag + '_mx.json'), JSON.stringify(R, null, 1)); console.log('ok', errs.length);
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
