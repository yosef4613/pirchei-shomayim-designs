// probe_inv.js — fieldfix: המלאי בדפדפן (הצבעים ב-3/4 מול מלמעלה, הטיסות והעמדות, R3 / ההאנגרים, חניוני S16) + צילומים לעצמי. node probe_inv.js <build> <outdir> <tag>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, tag] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) { } await p.waitForTimeout(300) }
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const fn = (f, a) => ev('JSON.stringify((' + f.toString() + ')(' + JSON.stringify(a || {}) + '))').then(s => { try { return JSON.parse(s) } catch (e) { return s } });
  const inv = await fn(() => { const R = {};
    try { R.flights = S15SIM.flights.map(a => ({ id: a.id, model: a.model, al: a.airline, home: a.home, kind: a.kind, n: a.legs.length })) } catch (e) { R.flights = String(e) }
    try { R.sched = S15SIM.sched } catch (e) { R.sched = String(e) }
    try { R.parked = S15D.parked; R.stands = Object.keys(S15D.stands) } catch (e) { R.parked = String(e) }
    try { R.stat = s15StaticList().map(o => [o.key, o.id, o.al, o.lv, o.stand]) } catch (e) { R.stat = String(e) }
    try { R.hgr = { ac: S15_HGR.ac, day: S15_HGR.day, r3: S15_HGR.r3, tows: S15SIM.tows.map(t => t.id) } } catch (e) { R.hgr = String(e) }
    try { R.heli = S15SIM.heli.map(h => h.id + ':' + h.model) } catch (e) { }
    // הצבעים: מלמעלה (s15DrawAc → state.c) מול 3/4 (s15A3F → a34Liv)
    const L = window.__A34LIV, cmp = [];
    try { const all = []; for (const a of S15SIM.flights) all.push({ id: a.model, key: a.id, al: a.airline, lv: S15_LV[a.airline], stand: a.home }); for (const o of s15StaticList()) if (!o.heli) all.push(o);
      all.push({ id: S15_HGR.ac, key: 'HGR', al: 'Skyline Regional', lv: S15_LV['Skyline Regional'] });
      for (const o of all) { const m = TurboCity.get(o.id) || { id: o.id }, cTop = (o.al != null && S15_LV[o.al] != null ? S15_LV[o.al] : s15Hash(o.key) % 16), top = L.livOf(m, { c: cTop, k: /^AC-(CG|HC|TB)/.test(o.id) ? 1 : 0 });
        const f = s15A3F(o.key, o.lv, o.stand), q = a34Liv(o.id, f);
        cmp.push({ key: o.key, id: o.id, al: o.al, lvTop: cTop, fLv: f.lv, a34key: q.key, top: top && [top.n, top.w, top.b, top.s, top.t].join(' '), a34: q.lv && [q.lv.n, q.lv.w, q.lv.b, q.lv.s, q.lv.t].join(' '), mty: m.ty || '' }) } } catch (e) { cmp.push(String(e)) }
    R.cmp = cmp;
    try { R.A3F = [...S15A3.F.entries()].map(([k, f]) => [k, f.lv, f.stand]) } catch (e) { }
    try { R.a3 = { on: S15A3.on, c34: C34G.on, armed: C34G.armed, ok: s15A3Ok('ground') } } catch (e) { R.a3 = String(e) }
    try { R.lots = typeof S16D !== 'undefined' ? Object.keys(S16D) : null } catch (e) { }
    try { R.s16fn = ['s16dLots', 'S16DL', 'S16D_LOTS'].filter(n => { try { return typeof eval(n) !== 'undefined' } catch (e) { return false } }) } catch (e) { }
    return R });
  fs.writeFileSync(path.join(out, tag + '_inv.json'), JSON.stringify(inv, null, 1));
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e); for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  const shots = [['apron', 7700, 700, 1.0], ['p2p4', 7560, 700, 1.7], ['r3', 9369, 2150, 1.4], ['hgr', 9150, 1500, 1.2], ['cargo', 8400, 1000, 1.2]];
  for (const md of ['a34', 'top']) for (const [nm, x, y, z] of shots) {
    await ev('(' + ((o) => { try { State.mapQa = true } catch (e) { } try { G77_ASV.on = false } catch (e) { } try { c34Night(0) } catch (e) { } try { S15A3.on = o.md === 'a34' } catch (e) { } Camera.x = o.x; Camera.y = o.y; Camera.zoom = o.z; return 1 }).toString() + ')(' + JSON.stringify({ x, y, z, md }) + ')');
    await p.waitForTimeout(md === 'a34' ? 6000 : 2500); await p.screenshot({ path: path.join(out, tag + '_' + md + '_' + nm + '.png') });
  }
  fs.writeFileSync(path.join(out, tag + '_errs.json'), JSON.stringify(errs, null, 1)); console.log('ok', errs.length, JSON.stringify(inv).length);
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
