// h8_q.js — בדיקת בית השחקן (house8, 17.11): עלייה מרמה 1 עד 8 דרך buyHomeUpgrade (ליד הדלת, עם כסף) — המחיר שנגבה, הרמה, מקומות המוסך,
// המבנים של כל רמה (רמה 8 בלי המבנה למסוק), המנחת של רמה 8 (המסוק עליו — הצייר הקיים), מסך הבית, ו-0 שגיאות בדף.
// node h8_q.js <game.html> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const R = { steps: [] }; const WANT = { 2: 4200, 3: 9000, 4: 17000, 5: 28000, 6: 35000, 7: 55000, 8: 80000 }, CAP = { 1: 1, 2: 2, 3: 4, 4: 5, 5: 7, 6: 8, 7: 10, 8: 12 };
  R.audit0 = await ev('window.__TC_H8?__TC_H8.audit():null');
  await ev('PlayerProfile.home.homeLevel=1;PlayerProfile.home.garageCapacity=1;PlayerProfile.money=500000;1');
  for (let n = 2; n <= 8; n++) {
    await ev(`PlayerProfile.mode='walk';const q=playerHomeServicePoint();PlayerPed.x=q.x;PlayerPed.y=q.y+10;Camera.x=q.x+300;Camera.y=q.y;Camera.zoom=1;1`); await p.waitForTimeout(700);
    const s = JSON.parse(await ev(`(()=>{const m0=PlayerProfile.money;buyHomeUpgrade();return {lv:c3Lv(),paid:m0-PlayerProfile.money,cap:PlayerProfile.home.garageCapacity,bld:C3PH_B[c3Lv()-1].map(o=>o.id),near:!!nearbyPlayerHome(170)}})()`));
    s.n = n; s.ok = s.lv === n && s.paid === WANT[n] && s.cap === CAP[n] && (n < 8 || !s.bld.some(id => /-HG$/.test(id))); R.steps.push(s);
  }
  // the helicopter on the pad (level 8): the camera on the pad, a few frames
  await ev('Camera.x=3470;Camera.y=2405;Camera.zoom=1.2;PlayerPed.x=3300;PlayerPed.y=2560;1'); await p.waitForTimeout(2000);
  R.heliFrames = +(await ev('C3LV[c3Lv()-1].pad&&C3CUR&&C3CUR.pad?1:0')); R.solidAtHangar = await ev('c3PhSolidAt(3298,2340,6)');
  R.phone = JSON.parse(await ev(`(()=>{const q=playerHomeServicePoint();PlayerPed.x=q.x;PlayerPed.y=q.y+10;const h=phoneHouse();return {top:/הארמון עם המנחת והמסוק/.test(h),old:/מבנה למסוק/.test(h),l8:/ארמון עם מנחת — 12 חניות/.test(h),lv:/8 \\/ 8/.test(h)}})()`));
  R.visual = await ev(`c3Lv()===clamp(PlayerProfile.home.homeLevel||1,1,8)`);
  R.audit = await ev('__TC_H8.audit()'); R.errs = errs;
  R.pass = R.steps.every(s => s.ok) && R.heliFrames > 0 && (R.solidAtHangar === 'null' || R.solidAtHangar == null) && R.phone.top === true && !R.phone.old && R.phone.l8 && R.visual === 'true' && !errs.length && !JSON.parse(R.audit).err;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ pass: R.pass, steps: R.steps.map(s => [s.n, s.lv, s.paid, s.cap, s.ok]), heliFrames: R.heliFrames, solidAtHangar: R.solidAtHangar, phone: R.phone, errs }).slice(0, 2000));
  await b.close(); process.exit(R.pass ? 0 : 2);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
