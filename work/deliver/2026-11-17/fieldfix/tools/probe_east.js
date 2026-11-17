// probe_east.js — fieldfix: G3 / H0–H3 באזורים החיים — הבדיקה, צמתים בשטח, ומבט בעין (עם / בלי, ‎?ffeast=0). node probe_east.js <build> <outdir> <tag> [off]
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
  R.audit = await fn(() => { try { return ffEastAudit() } catch (e) { return String(e) } });
  R.info = await fn(() => { const o = { regions: ACTIVE_REGIONS.length, live: MAP_ACTIVE_IDS.size, on: typeof FFEAST !== 'undefined' && FFEAST.on };
    const cells = [[7200, 1700], [8400, -850], [8400, 0], [8400, 850], [8400, 1700]], inC = (x, y) => cells.some(([a, c]) => x >= a && x < a + 1200 && y >= c && y < c + 850);
    o.nodes = NODES.filter(n => inC(n.x, n.y)).map(n => n.id + ' ' + Math.round(n.x) + ',' + Math.round(n.y) + ' ' + (blockedAt(n.x, n.y, 8) || '-')).slice(0, 40);
    o.fieldNodes = NODES.filter(n => n.x >= 4800 && n.y < 2550 && s15InPoly(n.x, n.y)).length;
    o.why = {}; for (const [x, y] of [[7800, 2100], [9000, -400], [9000, 400], [9000, 1300], [9000, 2100], [9590, 1000], [7000, 2100], [8000, 1200]]) o.why[x + ',' + y] = [inActiveRegion(x, y), blockedAt(x, y, 8), personBlockedAt(x, y)];
    try { o.water = window.__TC_WATERWALK ? window.__TC_WATERWALK.audit && window.__TC_WATERWALK.audit() : null } catch (e) { o.water = String(e) }
    try { o.mapfix = window.__TC_MAPFIX && window.__TC_MAPFIX() } catch (e) { }
    try { o.w3 = [w3KindAt(7800, 2100), w3KindAt(9000, 400), w3KindAt(7800, 1200)] } catch (e) { o.w3 = String(e) }
    try { o.f9 = window.__TC_F9AUDIT && (({ ok, zones, zoneBodies, why }) => ({ ok, zones, zoneBodies, why }))(window.__TC_F9AUDIT()) } catch (e) { o.f9 = String(e) }
    return o });
  fs.writeFileSync(path.join(out, tag + '_east.json'), JSON.stringify(R, null, 1));
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e); for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  const L = [['seam', 8400, 1700, .35], ['h1', 8800, 300, .5], ['g3', 7900, 2150, .6], ['h3', 9000, 2150, .6], ['far', 7800, 800, .18]];
  for (const [nm, x, y, z] of L) {
    await ev('(' + ((o) => { try { State.mapQa = true } catch (e) { } try { c34Night(0) } catch (e) { } Camera.x = o.x; Camera.y = o.y; Camera.zoom = o.z; return 1 }).toString() + ')(' + JSON.stringify({ x, y, z }) + ')');
    await p.waitForTimeout(6000); await p.screenshot({ path: path.join(out, tag + '_' + nm + '.png') });
  }
  R.errs = errs; fs.writeFileSync(path.join(out, tag + '_east.json'), JSON.stringify(R, null, 1)); console.log('ok', errs.length);
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
