// probe_liv.js — fieldfix: הצבעים ב-3/4 (FFLIV חדש / ישן / מלמעלה) על המטוסים החונים + פרטי s15pax_flow. node probe_liv.js <build> <outdir> <tag>
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
  const R = {};
  R.pax = await fn(() => { const o = {}; try { o.audit = window.__TC_S15PAX ? window.__TC_S15PAX.audit() : 'אין' } catch (e) { o.audit = String(e) }
    try { o.q = []; for (const b of S15D.bridges) { const f0 = S15SIM.flights.find(q => q.home === b.stand); if (!f0) continue; const Ls = f0.legs[f0.legs.length - 1], t0 = s15jMd(Ls.t0), dur = Ls.t1 - Ls.t0, fa = s15jFlightAt(b, t0 + Math.max(60, dur - 70)); if (!fa) continue; const p = fa.f.pax;
      o.q.push({ st: b.stand, count: p.count, gap: p.gap, gD: p.gD, cap: p.cap, travel: p.travel, tot: g2PathLen(p.points), arr: p.arr, dep: p.dep, W: g77BcWin(fa.f) }) } } catch (e) { o.qe = String(e) } return o });
  R.stands = await fn(() => { const o = {}; for (const [k, s] of Object.entries(S15D.stands)) o[k] = [s.cx, s.nose]; return o });
  fs.writeFileSync(path.join(out, tag + '_liv.json'), JSON.stringify(R, null, 1));
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e); for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  const S = R.stands, L = [];
  for (const st of ['P5', 'P1', 'P6', 'R1', 'C1']) if (S[st]) L.push([st, S[st][0], S[st][1] - 120, st[0] === 'P' && st !== 'P5' ? .8 : 1.1]);
  for (const md of ['new', 'old', 'top']) for (const [nm, x, y, z] of L) {
    await ev('(' + ((o) => { try { State.mapQa = true } catch (e) { } try { G77_ASV.on = false } catch (e) { } try { c34Night(0) } catch (e) { } try { S15A3.on = o.md !== 'top' } catch (e) { } window.FFLIV = window.FFLIV || {}; const want = o.md !== 'old'; if (window.FFLIV.on !== want) { window.FFLIV.on = want; try { A34G.S.clear() } catch (e) { } } Camera.x = o.x; Camera.y = o.y; Camera.zoom = o.z; return 1 }).toString() + ')(' + JSON.stringify({ x, y, z, md }) + ')');
    await p.waitForTimeout(md === 'top' ? 2500 : 9000); await p.screenshot({ path: path.join(out, tag + '_' + md + '_' + nm + '.png') });
  }
  R.a34 = await fn(() => { try { return { err: A34G.n.err, last: A34G.n.last, sets: A34G.S.size } } catch (e) { return String(e) } });
  R.errs = errs; fs.writeFileSync(path.join(out, tag + '_liv.json'), JSON.stringify(R, null, 1)); console.log('ok', errs.length);
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
