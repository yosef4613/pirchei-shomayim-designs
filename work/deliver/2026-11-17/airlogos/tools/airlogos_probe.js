// airlogos_probe.js <game.html> <out.json> [shotsdir] — airlogos 17.11: הבדיקה של השילוט החדש בשדה.
//  __TC_AIRLOGOS.audit() (כל הרשומות מצוירות, שמות חברות התעופה בעברית, 5 העטיפות), ואז המצלמה עוברת על המשטחים (ביום ובלילה)
//  ובכל נקודה — כמה שלטים חדשים צוירו בפריים (TCAL.seen). צילומים — לבדיקה פנימית בלבד (לא לדפים, כלל 8 / 17).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const SPOTS = [['checkin', 6350, 1060, 2.2], ['shopsW', 6705, 1090, 2.2], ['food', 8660, 1120, 2.0], ['shopsE', 8590, 1150, 2.0], ['gatecafe', 7370, 1010, 2.2],
  ['termW', 6451, 1104, 1.4], ['termE', 8640, 1130, 1.4], ['hangars', 8550, 1560, 1.1], ['fire', 8580, 1450, 1.4], ['hotel', 5135, 1069, 1.8], ['rent', 5408, 1350, 2.4],
  ['cargo', 5661, 1057, 2.0], ['staff', 7830, 1462, 2.0], ['info', 7023, 1591, 2.0], ['parking', 6630, 1560, 1.4], ['gates', 7170, 930, 1.6], ['gates2', 7800, 930, 1.6], ['tower', 0, 0, 1.3]];
(async () => {
  const [file, out, shots] = process.argv.slice(2); if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(3000);
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const R = { audit: JSON.parse(await ev(`JSON.stringify(__TC_AIRLOGOS.audit())`)), spots: {} };
  const tw = JSON.parse(await ev(`JSON.stringify(S15D.twr)`)); SPOTS[SPOTS.length - 1][1] = tw[0]; SPOTS[SPOTS.length - 1][2] = tw[1] - 120;
  for (const night of [0, 1]) for (const [nm, x, y, z] of SPOTS) {
    await ev(`(()=>{try{setPhoneOpen(false)}catch(e){}State.paused=false;PlayerProfile.mode='walk';window.__TC_NIGHT=${night};PlayerPed.x=${x};PlayerPed.y=${y};Camera.x=${x};Camera.y=${y};Camera.zoom=${z};TCAL.seen={};return 1})()`);
    await p.waitForTimeout(1800);
    await ev(`(()=>{Camera.x=${x};Camera.y=${y};Camera.zoom=${z};TCAL.seen={};return 1})()`); await p.waitForTimeout(700);
    R.spots[nm + (night ? '_n' : '')] = JSON.parse(await ev(`JSON.stringify(TCAL.seen)`));
    if (shots) await p.screenshot({ path: path.join(shots, nm + (night ? '_n' : '') + '.png') });
  }
  // המטוסים: מטוס על הקרקע — קרוב (הסמל על הזנב), ב-3/4 ומלמעלה (F10)
  const pl = JSON.parse(await ev(`(()=>{const tc=S15GR&&S15GR.tc!=null?S15GR.tc:0,o=[];for(const a of S15SIM.flights){const P=s15PoseAt(a,tc);if(P&&P[3]<1&&P[1]<900)o.push([a.id,a.airline,P[0],P[1]])}return JSON.stringify(o.slice(0,3))})()`));
  R.planes = [];
  for (const [i, q] of pl.entries()) { await ev(`(()=>{window.__TC_NIGHT=0;TCAL.seen={};Camera.x=${q[2]};Camera.y=${q[3]};Camera.zoom=2.6;return 1})()`); await p.waitForTimeout(1500);
    R.planes.push({ id: q[0], al: q[1], seen: JSON.parse(await ev(`JSON.stringify(TCAL.seen)`)) }); if (shots) await p.screenshot({ path: path.join(shots, 'plane' + i + '.png') }) }
  R.stats = JSON.parse(await ev(`JSON.stringify(__TC_AIRLOGOS.stats())`)); R.errs = errs.slice(0, 8);
  const need = ['checkin', 'shopsW', 'food', 'shopsE', 'termW', 'termE', 'hangars', 'hotel', 'rent', 'tower', 'parking'];
  R.missing = need.filter(k => !Object.keys(R.spots[k] || {}).length);
  R.ok = R.audit.ok && (R.stats.n.tail === undefined || R.stats.n.tail > 0) && !R.missing.length && !errs.length && !R.stats.err;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, audit: R.audit.ok, fail: R.audit.fail, missing: R.missing, errs: errs.length, n: R.stats.n, err: R.stats.err }));
  await b.close();
})().catch(e => { console.error(e); process.exit(2) });
