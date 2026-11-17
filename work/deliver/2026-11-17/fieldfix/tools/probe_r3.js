// probe_r3.js — fieldfix: R3 והמחזור של ההאנגרים (הבדיקה ffR3Audit + צילומים לעצמי) + s15pax. node probe_r3.js <build> <outdir> <tag>
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
  { const sd = await p.evaluate(() => window.__TC_DEV.ev('JSON.stringify({T:S15SIM.T,flights:S15SIM.flights,veh:S15SIM.veh,tows:S15SIM.tows,heli:S15SIM.heli,sched:S15SIM.sched,ngf:S15SIM.ngf,spots:S15D.spots,stands:S15D.stands,parked:S15D.parked,bridges:S15D.bridges,stat:(FFR3.l0||s15StaticList)().map(o=>({id:o.id,key:o.key,x:o.x,y:o.y,th:o.th,heli:!!o.heli,al:o.al||null})),ffr3:typeof FFR3!=="undefined"?FFR3.M.flatMap(A=>[{id:"FF-"+A.id+"-OUT",kind:"ac",model:A.ac,home:A.id,L:A.Lpx,W:150,legs:A.out.legs.map(g=>Object.assign({},g,{t0:(FFR3.tOut*2%720)+g.t0,t1:(FFR3.tOut*2%720)+g.t1}))},{id:"FF-"+A.id+"-BACK",kind:"ac",model:A.ac,home:A.id,L:A.Lpx,W:150,legs:A.back.legs.map(g=>Object.assign({},g,{t0:(FFR3.tBack*2%720)+g.t0,t1:(FFR3.tBack*2%720)+g.t1}))}]):[]})'));
    fs.writeFileSync(path.join(out, tag + '_sim.json'), sd) }
  R.r3 = await fn(() => { try { return window.__TC_FIELDFIX.r3() } catch (e) { return String(e) } });
  R.pax = await fn(() => { try { const a = window.__TC_S15PAX.audit(); return a.checks.map(c => (c.ok ? '✓ ' : '✗ ') + c.id + ': ' + c.det.slice(0, 600)) } catch (e) { return String(e) } });
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e); for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  // [שם, יום, דקה, x, y, זום]
  const L = [['day_r3', 3, 720, 9369, 2250, 1.1], ['day_hgr', 3, 720, 8650, 1520, .9], ['n_A_run', 3, 22 * 60, 9369, 2250, 1.1], ['n_B_run', 4, 22 * 60, 9369, 2250, 1.1], ['n_C_run', 5, 22 * 60, 9369, 2250, 1.1],
    ['n_B_hgr', 4, 22 * 60, 8650, 1520, .9], ['B_towC', 4, 18 * 60 + 25, 8900, 1820, .8], ['C_out0', 5, 18 * 60 + 12, 8243, 1650, 1.2], ['A_out', 3, 18 * 60 + 25, 9200, 1600, .8]];
  for (const [nm, d, m, x, y, z] of L) {
    await ev('(' + ((o) => { try { State.mapQa = true } catch (e) { } try { G77_ASV.on = false } catch (e) { } try { c34Night(o.m >= 1200 || o.m < 300 ? 1 : 0) } catch (e) { } S15X.ovr = { tc: 2 * (1440 * o.d + o.m), min: o.m }; Camera.x = o.x; Camera.y = o.y; Camera.zoom = o.z; return 1 }).toString() + ')(' + JSON.stringify({ d, m, x, y, z }) + ')');
    await p.waitForTimeout(7000); await p.screenshot({ path: path.join(out, tag + '_' + nm + '.png') });
  }
  R.ff = await fn(() => ({ n: FFR3.n, err: FFR3.err, cur: FFR3.cur, a34: (() => { try { return { err: A34G.n.err, last: A34G.n.last } } catch (e) { return 0 } })() }));
  R.errs = errs; fs.writeFileSync(path.join(out, tag + '_r3.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
