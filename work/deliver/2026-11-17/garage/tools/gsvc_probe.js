// gsvc_probe.js — הבדיקה של העבודה הנראית בתא (garage, 17.11, ‏074zz4): קנה במסך המוסך → סוגרים → הרכב שלך על המתקן, הצוות, המראה משתנה רק בסוף, E חסום, מוכן.
// המקרים: (א) הרכב בנקודת השירות (תא 2) עם צבע + חישוקים + מנוע + תיקון; (ב) הרכב לפני תא 2 — נכנס בנסיעה; (ג) אחרי גרירה — בתא 3, ברגל; (ד) הרכב זז באמצע — העבודה נעצרת; (ה) הסל מהבית; (ו) הסוכנות עם מוסך מלא; (ז) היציאה — המכוון והחצים (בתוך א).
// node gsvc_probe.js <game.html> <out_dir> [shots=1]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots0] = process.argv.slice(2); const shots = shots0 !== '0'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const J = async s => { const v = await ev(s); try { return JSON.parse(v) } catch (e) { return v } };
  const R = { cases: {} }; const shot = async n => { if (shots) await p.screenshot({ path: path.join(out, n + '.png') }) };
  const cam = 'Camera.x=4400;Camera.y=2440;Camera.zoom=3.2;1';
  // follow one job: sample every 0.4 s until it ends (or 45 s); try E once while the car is up; screenshots at the lift, the paint, the end
  async function follow(tag, eAt) {
    const S = { phases: [], zMax: 0, shownSeq: [], crewWork: [false, false], exited: false, mode: [], blockedE: null, samples: 0 }; let lastShown = '', t0 = Date.now(), shotUp = false, shotPaint = false;
    while (Date.now() - t0 < 45000) {
      await ev(cam); const s = await J('__TC_GSVC.state()'); S.samples++;
      if (!s.phase) { S.end = s; break }
      if (s.phase === 'run') {
        if (!S.phases.includes(s.seg)) S.phases.push(s.seg); S.zMax = Math.max(S.zMax, s.z); const sh = JSON.stringify(s.shown); if (sh !== lastShown) { S.shownSeq.push([s.T, s.shown]); lastShown = sh }
        (s.crew || []).forEach((c, i) => { if (c && c.work) S.crewWork[i] = true }); if (s.exited) S.exited = true; if (!S.mode.includes(s.mode)) S.mode.push(s.mode);
        if (eAt && S.blockedE == null && s.z > 1) { S.blockedE = await J('(()=>{const n0=GSVC.n.blocked;PlayerPed.x=PlayerCar.x+16;PlayerPed.y=PlayerCar.y;const r=enterVehicle();return{r,mode:PlayerProfile.mode,blocked:GSVC.n.blocked-n0}})()') }
        if (!shotUp && s.z > 1.5) { shotUp = true; await shot(tag + '_lift') }
        if (!shotPaint && s.seg === 'c' && s.crew && s.crew[0] && s.crew[0].work) { shotPaint = true; await shot(tag + '_paint') }
      }
      await p.waitForTimeout(400);
    }
    await shot(tag + '_end'); return S;
  }
  R.audit0 = await J('__TC_GSVC.audit()');
  await ev('PlayerProfile.money=40000;1');
  // (א) at the service point: colour + rims + engine + repair
  {
    const C = {}; await ev('activeVehicleEco().damage=30;1');
    C.open = await ev('__TC_GST.open("garage")'); await p.waitForTimeout(1500);
    C.before = await J('({c:PlayerCar.state.c,r:PlayerCar.state.r,m:PlayerProfile.money,x:PlayerCar.x,y:PlayerCar.y,dmg:activeVehicleEco().damage})');
    await p.click('#gstRoot [data-gst-c="4"]').catch(e => C.e1 = String(e).slice(0, 120)); await p.waitForTimeout(300);
    await p.click('#gstRoot [data-gst-tab="r"]').catch(() => 0); await p.waitForTimeout(300); const rb = await p.$('#gstRoot [data-gst-r]:not(.on)'); if (rb) await rb.click(); await p.waitForTimeout(300);
    await p.click('#gstRoot [data-gst-tab="up"]').catch(() => 0); await p.waitForTimeout(300); await p.click('#gstRoot [data-gst-up="engine:1"]').catch(() => 0); await p.waitForTimeout(300);
    await p.click('#gstRoot [data-gst-tab="fix"]').catch(() => 0); await p.waitForTimeout(300); await p.click('#gstRoot [data-gst-fix]').catch(e => C.eFix = String(e).slice(0, 120)); await p.waitForTimeout(300);
    C.basket = await J('GSTUI.basket()');
    await p.click('#gstRoot [data-gst-buy]'); await p.waitForTimeout(900); await shot('a0_bought');
    C.queued = await J('__TC_GSVC.state()'); C.afterBuy = await J('({c:PlayerCar.state.c,r:PlayerCar.state.r,m:PlayerProfile.money,dmg:activeVehicleEco().damage,fx:GSTUI.U.fx&&GSTUI.U.fx.text})');
    await ev('setPhoneOpen(false)');
    C.run = await follow('a', true);
    C.after = await J('({c:PlayerCar.state.c,r:PlayerCar.state.r,x:PlayerCar.x,y:PlayerCar.y,h:+PlayerCar.heading.toFixed(2),mode:PlayerProfile.mode,last:GSVC.last})');
    C.enterAfter = await J('(()=>{PlayerPed.x=PlayerCar.x+16;PlayerPed.y=PlayerCar.y;const r=enterVehicle();return{r,mode:PlayerProfile.mode}})()');
    // (ז) the way out: in the car → the tyre fitter walks out to the sidewalk and waves, the arrows on the floor; you drive out along them → he walks back
    await p.waitForTimeout(400); C.out1 = await J('__TC_GSVC.state()');
    await p.waitForTimeout(3000); await ev(cam); await p.waitForTimeout(300); C.out2 = await J('({st:__TC_GSVC.state(),gd:GSVC.n.guideDraw})'); await shot('a_guide');
    for (let k = 1; k <= 14; k++) { await ev('(()=>{const o=GSVC.out||{at:{x:4395,y:2450,h:-Math.PI/2},bay:2};const X=__TC_GSVC.exitPath(o),q=__TC_GSVC.bez(X,' + (k / 14) + ');PlayerCar.x=q.x;PlayerCar.y=q.y;PlayerCar.heading=q.h+Math.PI;PlayerCar.speed=0;return 1})()'); await p.waitForTimeout(160) }
    C.out3 = await J('__TC_GSVC.state()'); await shot('a_out'); await p.waitForTimeout(3200); C.out4 = await J('({st:__TC_GSVC.state(),n:GSVC.n})');
    R.cases.a = C;
  }
  // (ב) in front of bay 2, the nose to the hall: it drives in
  {
    const C = {}; await ev('setPhoneOpen(false);PlayerProfile.mode="vehicle";PlayerCar.x=4362;PlayerCar.y=2496;PlayerCar.heading=-Math.PI/2+0.35;PlayerCar.speed=0;' + cam);
    await p.waitForTimeout(500); C.plan = await J('__TC_GSVC.plan()&&{bay:__TC_GSVC.plan().bay,roll:!!__TC_GSVC.plan().roll}');
    C.open = await ev('openPoiPhone("garage","D3-GARAGE"),State.phoneApp');
    await p.waitForTimeout(1200); await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.click('#gstRoot [data-gst-c="6"]').catch(e => C.e1 = String(e).slice(0, 120)); await p.waitForTimeout(300);
    await p.click('#gstRoot [data-gst-buy]').catch(e => C.eBuy = String(e).slice(0, 120)); await p.waitForTimeout(800);
    C.queued = await J('__TC_GSVC.state()'); await ev('setPhoneOpen(false)');
    await p.waitForTimeout(700); await shot('b_in');
    C.run = await follow('b', false);
    C.after = await J('({c:PlayerCar.state.c,x:PlayerCar.x,y:PlayerCar.y,h:+PlayerCar.heading.toFixed(2),last:GSVC.last})');
    R.cases.b = C;
  }
  // (ג) after a tow: the car in bay 3, you on foot
  {
    const C = {}; await ev('setPhoneOpen(false);PlayerProfile.mode="vehicle";PlayerCar.x=4100;PlayerCar.y=2540;PlayerCar.heading=0;PlayerCar.speed=0;activeVehicleEco().damage=60;1');
    await p.waitForTimeout(400); C.tow = await J('(()=>{const r=__TC_TOW.tow();return{r,car:[PlayerCar.x,PlayerCar.y],ped:[PlayerPed.x,PlayerPed.y],mode:PlayerProfile.mode}})()');
    C.plan = await J('__TC_GSVC.plan()&&{bay:__TC_GSVC.plan().bay,roll:!!__TC_GSVC.plan().roll}');
    C.open = await ev('openPoiPhone("garage","D3-GARAGE"),State.phoneApp'); await p.waitForTimeout(1200);
    await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.click('#gstRoot [data-gst-c="9"]').catch(e => C.e1 = String(e).slice(0, 120)); await p.waitForTimeout(300);
    await p.click('#gstRoot [data-gst-buy]').catch(e => C.eBuy = String(e).slice(0, 120)); await p.waitForTimeout(800);
    C.queued = await J('__TC_GSVC.state()'); await ev('setPhoneOpen(false)');
    C.run = await follow('c', false);
    C.after = await J('({c:PlayerCar.state.c,x:PlayerCar.x,y:PlayerCar.y,last:GSVC.last,mode:PlayerProfile.mode})');
    R.cases.c = C;
  }
  // (ד) the car is moved away in the middle (a jump of the dev / a mission) — the job stops, the car shows its new look
  {
    const C = {}; await ev('setPhoneOpen(false);PlayerProfile.mode="vehicle";PlayerCar.x=4395;PlayerCar.y=2450;PlayerCar.heading=-Math.PI/2;PlayerCar.speed=0;1');
    C.open = await ev('openPoiPhone("garage","D3-GARAGE"),State.phoneApp'); await p.waitForTimeout(1200);
    await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.click('#gstRoot [data-gst-c="1"]').catch(() => 0); await p.waitForTimeout(300);
    await p.click('#gstRoot [data-gst-buy]').catch(() => 0); await p.waitForTimeout(700); await ev('setPhoneOpen(false)'); await p.waitForTimeout(2500);
    C.mid = await J('__TC_GSVC.state()'); await ev('PlayerCar.x=4100;PlayerCar.y=2540;1'); await p.waitForTimeout(600);
    C.after = await J('({st:__TC_GSVC.state(),c:PlayerCar.state.c,n:GSVC.n})');
    R.cases.d = C;
  }
  // (ה) the basket of the home garage goes with you to the city garage (the same car) — the reviewer, 17.11
  {
    const C = {}; await ev('setPhoneOpen(false)'); C.openH = await ev('__TC_GST.open("home")'); await p.waitForTimeout(1300);
    await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.click('#gstRoot [data-gst-c="8"]').catch(e => C.e1 = String(e).slice(0, 120)); await p.waitForTimeout(400);
    C.btn = await ev('(document.querySelector("#gstRoot [data-nav-target]")||{}).textContent||null');
    await p.click('#gstRoot [data-nav-target]').catch(e => C.eNav = String(e).slice(0, 120)); await p.waitForTimeout(500);
    C.carry = await J('GSTUI.U.carry&&{id:GSTUI.U.carry.id,pre:GSTUI.U.carry.pre}'); await ev('setPhoneOpen(false)'); await p.waitForTimeout(300);
    C.openG = await ev('__TC_GST.open("garage")'); await p.waitForTimeout(1300);
    C.inGarage = await J('({basket:GSTUI.basket(),carried:!!GSTUI.U.carried,carry:GSTUI.U.carry||null,note:!!Array.from(document.querySelectorAll("#gstRoot small")).find(e=>/הסל מהמוסך שבבית/.test(e.textContent))})');
    await p.click('#gstRoot [data-gst-cancel]').catch(() => 0); await ev('setPhoneOpen(false)'); R.cases.e = C;
  }
  // (ו) the dealer with a full home garage: "buy" is off, and the reason is in the basket before the click
  {
    const C = {}; await ev('PlayerProfile.home.garageCapacity=ensureGarageSchema().vehicles.length;1'); C.openD = await ev('__TC_GST.open("dealer")'); await p.waitForTimeout(1300);
    await p.click('#gstRoot [data-gst-tab="models"]').catch(() => 0); await p.waitForTimeout(300); const mb = await p.$$('#gstRoot [data-gst-model]'); if (mb.length > 1) await mb[1].click(); await p.waitForTimeout(500);
    C.basket = await J('({b:GSTUI.basket().L.length,buyOff:!!document.querySelector("#gstRoot [data-gst-buy][disabled]"),why:(document.querySelector("#gstRoot .gstWhy")||{}).textContent||null})');
    await shot('f_dealer_full'); await ev('PlayerProfile.home.garageCapacity=6;setPhoneOpen(false)'); R.cases.f = C;
  }
  R.audit = await J('__TC_GSVC.audit()'); R.ghall = await J('__TC_GHALL.audit()'); R.gst = await J('__TC_GST.GST'); R.errs = errs;
  fs.writeFileSync(path.join(out, 'gsvc_probe.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 4000));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
