// brandin_probe.js <game.html> <out.json> [shotsdir] — brandin 17.11: הבדיקה החוסמת של פריטי keep שנכנסו.
//  (1) __TC_BRANDIN.audit(): כל פריט keep (89 התפעוליים, הזהויות / ההצעות / המשטחים של העיר, 62 הלוגואים, 10 הפוסטרים × 2) מצויר בקנבס בדיקה בלי שגיאה ולא ריק.
//  (2) המצלמה עוברת על המשטחים בשדה ובעיר (ביום ובלילה) — כל משטח keep שנכנס צויר במקומו (TCBI.seen) ובלי שגיאה.
//  (3) מסך המקום (F) לכל מקום keep — הזהות המקומית / ההצעה מצוירות (data-tcbi). צילומים — לבדיקה פנימית בלבד (כלל 8 / 17).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const SPOTS = [['rfW', 6705, 1066, 2.4], ['rfGate', 7370, 1020, 2.6], ['rfJuice', 8215, 1020, 2.6], ['rfFood', 8616, 1125, 2.2], ['termW', 6400, 1090, 1.8], ['termW2', 6900, 1100, 1.8], ['termM', 7350, 1060, 1.8], ['termE', 7950, 1000, 1.8], ['termE2', 8450, 1110, 1.8], ['termE3', 8850, 1120, 1.8],
  ['gatesW', 7000, 930, 1.5], ['gatesE', 7900, 900, 1.5], ['gateP6', 8874, 990, 1.6], ['brief', 8014, 1112, 2.4], ['ctr1', 7034, 1045, 2.6], ['ctr2', 7808, 1075, 2.6], ['ctr3', 8190, 1191, 2.6],
  ['rwyW', 5250, -420, 1.0], ['rwyM', 7150, -420, 1.0], ['rwyE', 9250, -420, 1.0], ['twyA', 9515, 40, 1.4], ['twyB', 9515, 600, 1.4], ['twyC', 8000, 1670, 1.4], ['twyC2', 9285, 1655, 1.4],
  ['hangars', 8550, 1560, 1.2], ['hangar3', 8243, 1565, 1.4], ['fuel', 8048, 1495, 1.4], ['police', 8523, 1371, 1.4], ['workshop', 8243, 1328, 1.4], ['wing', 7812, 831, 1.4], ['plateT', 6330, 1104, 1.4], ['plateT2', 7200, 1100, 1.4],
  ['e4staff', 7764, 1495, 1.2], ['e4cargo', 5717, 800, 1.2], ['e4pax', 5510, 1704, 1.2], ['e4air1', 5105, 1453, 1.2], ['e4entry', 6205, 1352, 1.4], ['e4exit', 6688, 1336, 1.4], ['e4pstaff', 7330, 1294, 1.4],
  ['e4ap3', 6752, 1670, 1.4], ['e4free', 6630, 1577, 1.4], ['e4shuttle', 7648, 1306, 1.4], ['e4rmg', 5850, 800, 1.4], ['s9cargo', 5661, 1057, 1.8], ['s9staff', 7830, 1462, 1.8], ['s9info', 7023, 1591, 1.8]];
(async () => {
  const [file, out, shots] = process.argv.slice(2); if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(3000);
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const R = { audit: JSON.parse(await ev(`JSON.stringify(__TC_BRANDIN.audit())`)), spots: {} };
  // the city surfaces of keep faces that were not in the game: their places' positions (the map's registry)
  const city = JSON.parse(await ev(`(()=>{const B=__TC_BRANDIN,reg=navPoiRegistry()||{},o=[],FX={'E4-SOLAR-PANELS':{x:5640,y:2920},'E4-INVERTER':{x:5640,y:2920}};for(const ty of ['c2','d2','s9','e4','b4'])for(const k in B.ct[ty]){const [id,f]=B.ct[ty][k],m=B.city[id],P=B.b4pos[m.placeId],q=(ty==='b4'&&P)?{x:P[0],y:P[1]-40}:(reg[m.placeId]||FX[m.placeId]||(P&&{x:P[0],y:P[1]-40}));if(q&&q.x!=null)o.push([id+':'+f,q.x,q.y,1.6,m.placeId+':'+f])}return JSON.stringify(o)})()`));
  const spots = SPOTS.concat(city.map(c => ['c:' + c[0], c[1], c[2], c[3]]));
  const seen = {};
  for (const night of [0, 1]) for (const [nm, x, y, z] of spots) {
    if (night && nm.startsWith('c:')) continue;
    await ev(`(()=>{try{setPhoneOpen(false)}catch(e){}State.paused=false;window.__TC_NIGHT=${night};__TC_DEV.cam({x:${x},y:${y},zoom:${z}});__TC_BRANDIN.TCBI.seen={};return 1})()`);
    await p.waitForTimeout(nm.startsWith('c:') ? 1200 : 1500);
    await ev(`(()=>{__TC_DEV.cam({x:${x},y:${y},zoom:${z}});__TC_BRANDIN.TCBI.seen={};return 1})()`); await p.waitForTimeout(700);
    const s = JSON.parse(await ev(`JSON.stringify(__TC_BRANDIN.TCBI.seen)`)); R.spots[nm + (night ? '_n' : '')] = s; for (const k in s) seen[k] = (seen[k] || 0) + s[k];
    if (shots && !nm.startsWith('c:')) await p.screenshot({ path: path.join(shots, nm + (night ? '_n' : '') + '.png') });
  }
  // what must be seen: one surface per (family, text) of the ops; every city face that was not in the game (c2 / d2 / s9 / e4)
  const exp = JSON.parse(await ev(`(()=>{const B=__TC_BRANDIN,o=new Set();for(const id in B.ops){const m=B.ops[id];o.add(m.id)}return JSON.stringify([...o])})()`));
  const rep = JSON.parse(await ev(`(()=>{const B=__TC_BRANDIN,o={};const N=t=>String(t).replace(/[\\u200e\\u200f\\u2066-\\u2069]/g,'').replace(/\\s+/g,' ').trim();const F={};for(const id in B.ops){const m=B.ops[id],k=m.family+'|'+N(m.sourceText);if(!F[k])F[k]=id;o[id]=F[k]}return JSON.stringify(o)})()`));
  const repSet = [...new Set(exp.map(i => rep[i]))];
  const big = JSON.parse(await ev(`JSON.stringify(__TC_BRANDIN.TCBI.bigFids?[]:__TC_BRANDIN.big)`)); R.bigKept = big;
  R.opsMissing = repSet.filter(i => !seen[i] && !big.includes(i));
  const rfIds = JSON.parse(await ev(`JSON.stringify(Object.values(__TC_BRANDIN.rf))`)); R.rfMissing = []; for (const id of rfIds) for (const f of ['sign', 'logo']) if (!seen[id + ':' + f]) R.rfMissing.push(id + ':' + f);
  R.cityMissing = city.filter(c => !seen[c[0]]).map(c => c[4]);
  R.cityNoPos = JSON.parse(await ev(`(()=>{const B=__TC_BRANDIN,reg=navPoiRegistry()||{},o=[];for(const ty of ['c2','d2','s9','e4','b4'])for(const k in B.ct[ty]){const [id,f]=B.ct[ty][k];if(!reg[B.city[id].placeId]&&!B.b4pos[B.city[id].placeId]&&!/^E4-(SOLAR-PANELS|INVERTER)$/.test(B.city[id].placeId))o.push(B.city[id].placeId+':'+f)}return JSON.stringify(o)})()`));
  await ev(`(()=>{if(State.mapQa)toggleMapQa();return 1})()`);
  // (3) the place's screen (F) for every keep place
  R.place = JSON.parse(await ev(`(()=>{const B=__TC_BRANDIN,o={n:0,ok:0,noScreen:[],bad:[]};for(const pid in B.place){o.n++;try{openPoiPhone('business',pid);if(!State.phoneOpen||!PLACE.on){o.noScreen.push(pid);continue}placeApply();const hd=$('placeHead'),m=B.city[B.place[pid]],need=(m.formats.logo?1:0)+(m.formats.proposal?1:0),got=hd?hd.querySelectorAll('[data-tcbi]').length:0;if(got>=need&&need)o.ok++;else o.bad.push(pid+':'+got+'/'+need)}catch(e){o.bad.push(pid+':'+String(e).slice(0,60))}}try{setPhoneOpen(false)}catch(e){}return JSON.stringify(o)})()`));
  if (shots) { for (const pid of ['C2-BANK', 'A4-CLUB', 'APT-RENT']) { await ev(`(()=>{openPoiPhone('business','${pid}');return 1})()`); await p.waitForTimeout(800); await p.screenshot({ path: path.join(shots, 'F_' + pid + '.png') }); await ev(`(()=>{setPhoneOpen(false);return 1})()`) } }
  R.stats = JSON.parse(await ev(`JSON.stringify(__TC_BRANDIN.stats())`)); R.errs = errs.slice(0, 8);
  R.ok = R.audit.ok && !R.rfMissing.length && !R.opsMissing.length && !R.cityMissing.length && !errs.length && !R.stats.err && R.place.ok === R.place.n - R.place.noScreen.length && !R.place.bad.length;
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ ok: R.ok, audit: R.audit.ok, auditN: R.audit.n, byKind: R.audit.byKind, fail: R.audit.fail.slice(0, 6), opsMissing: R.opsMissing, rfMissing: R.rfMissing, cityMissing: R.cityMissing, cityNoPos: R.cityNoPos, place: { n: R.place.n, ok: R.place.ok, noScreen: R.place.noScreen.length, bad: R.place.bad.slice(0, 6) }, errs: errs.slice(0, 3), n: R.stats.n, err: R.stats.err }));
  await b.close();
})().catch(e => { console.error(e); process.exit(2) });
