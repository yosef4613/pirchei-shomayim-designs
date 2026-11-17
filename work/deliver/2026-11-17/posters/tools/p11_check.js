// בדיקת סט 11 בתוך המשחק: node p11_check.js <build> <out.json> <shot.png>  (הצילום — לבדיקה בעין שלי בלבד)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shot] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const t0 = Date.now();
  await p.waitForFunction(() => window.__TC_POSTERS && window.__TC_POSTERS.ready(), null, { timeout: 120000, polling: 500 }).catch(() => {});
  const r = await p.evaluate(() => {
    const o = { ready: __TC_POSTERS.ready(), p11: __TC_POSTERS11 && __TC_POSTERS11.stats(), po: __TC_POSTERS.stats() };
    const box = document.createElement('div'); box.id = 'p11box'; box.style.cssText = 'position:fixed;inset:0;z-index:99999;background:#222;display:flex;flex-wrap:wrap;gap:6px;padding:6px;overflow:hidden';
    for (const [k, v] of __TC_POSTERS.TCPO.src) { const c = v.cv; c.style.cssText = 'width:160px;height:240px'; box.appendChild(c) }
    const sc = [['film', 0], ['film', 3], ['play', 1]].map(([k, i]) => { const c = document.createElement('canvas'); c.style.cssText = 'width:320px;height:240px'; box.appendChild(c); return [c, k, i] });
    for (const t of ['תערוכה חדשה', 'אוסף הטבע']) { const c = __TC_POSTERS.banner(t, 120, 180); c.style.cssText = 'width:120px;height:180px'; box.appendChild(c) }
    document.body.appendChild(box); for (const [c, k, i] of sc) __TC_DEV.ev('TCSHOW').poster(c, k, i);
    o.after = __TC_POSTERS11.stats().n; return o });
  r.waitMs = Date.now() - t0; r.errs = errs;
  if (shot) await p.screenshot({ path: shot });
  fs.writeFileSync(out, JSON.stringify(r, null, 1)); console.log(JSON.stringify({ ready: r.ready, n: r.p11 && r.p11.n, err: r.p11 && r.p11.err, poErr: r.po.err, errs: errs.length }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
