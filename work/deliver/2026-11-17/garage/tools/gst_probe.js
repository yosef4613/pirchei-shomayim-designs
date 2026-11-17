// gst_probe.js — הבדיקה של מסך המוסך (garage, 17.11): פותח את המשחק (#dev), מסך F במוסך / בסוכנות / בבית, תצוגה מקדימה, קנה, ביטול, וצילומים לבדיקה פנימית.
// node gst_probe.js <game.html> <out_dir> [shots=1]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots0] = process.argv.slice(2); const shots = shots0 !== '0'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const R = {};
  const shot = async n => { if (shots) await p.screenshot({ path: path.join(out, n + '.png') }) };
  R.money0 = await ev('PlayerProfile.money=20000,PlayerProfile.money');
  R.openG = await ev('__TC_GST.open("garage")');
  await p.waitForTimeout(1800); R.auditG = JSON.parse(await ev('__TC_GST.audit()')); R.lastG = await ev('__TC_GST.GST.last'); await shot('g1_garage');
  // the preview: a colour, rims, an upgrade
  R.cur = await ev('GSTUI.curCar()&&GSTUI.curCar().st');
  await p.click('#gstRoot [data-gst-c="4"]').catch(e => R.clickErr = String(e).slice(0, 200)); await p.waitForTimeout(500);
  await p.click('#gstRoot [data-gst-tab="r"]').catch(() => 0); await p.waitForTimeout(300);
  const rimBtn = await p.$('#gstRoot [data-gst-r]:not(.on)'); if (rimBtn) await rimBtn.click(); await p.waitForTimeout(400);
  await p.click('#gstRoot [data-gst-tab="up"]').catch(() => 0); await p.waitForTimeout(300);
  await p.click('#gstRoot [data-gst-up="engine:1"]').catch(() => 0); await p.waitForTimeout(600);
  R.lookPre = await ev('GSTUI.look()'); R.basket = await ev('GSTUI.basket()'); R.world0 = await ev('({c:PlayerCar.state.c,r:PlayerCar.state.r,m:PlayerProfile.money})');
  await shot('g2_preview');
  // the hand: stop and drag
  await p.click('#gstRoot [data-gst-auto]'); const bb = await (await p.$('#gstMain')).boundingBox();
  await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.mouse.down(); await p.mouse.move(bb.x + bb.width / 2 + 160, bb.y + bb.height / 2, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(400);
  R.angAfterDrag = await ev('+GSTUI.U.ang.toFixed(3)'); await shot('g3_drag');
  // cancel → back; then pick again and buy
  await p.click('#gstRoot [data-gst-cancel]'); await p.waitForTimeout(300); R.lookCancel = await ev('GSTUI.look()'); R.basketCancel = await ev('GSTUI.basket().L.length');
  await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.waitForTimeout(200); await p.click('#gstRoot [data-gst-c="5"]'); await p.waitForTimeout(200);
  R.beforeBuy = await ev('({m:PlayerProfile.money,c:activeOwnedVehicle().colorIndex,pc:PlayerCar.state.c})');
  await p.click('#gstRoot [data-gst-buy]'); await p.waitForTimeout(900);
  R.afterBuy = await ev('({m:PlayerProfile.money,c:activeOwnedVehicle().colorIndex,pc:PlayerCar.state.c,basket:GSTUI.basket().L.length,fx:!!GSTUI.U.fx})'); await shot('g4_bought');
  R.legacyG = await ev('document.querySelectorAll("#phoneBody [data-garage-color],#phoneBody [data-upgrade-buy]").length');
  R.timing = await ev('(()=>{const U=GSTUI.U,c=GSTUI.curCar();const t0=performance.now();let n=0;for(let k=0;k<12;k++){U.ang+=Math.PI/36;U.dirty=1}return {cache:U.cache.size,MB:+(U.bytes/1048576).toFixed(1),last:__TC_GST.GST.last}})()');
  await ev('setPhoneOpen(false)'); await p.waitForTimeout(300); R.closed = await ev('({mode:GSTUI.U.mode,cache:GSTUI.U.cache.size})');
  // the dealer
  R.openD = await ev('__TC_GST.open("dealer")'); await p.waitForTimeout(1500); R.auditD = JSON.parse(await ev('__TC_GST.audit()')); await shot('d1_dealer');
  await ev('PlayerProfile.home.garageCapacity=6;1');
  await p.click('#gstRoot [data-gst-tab="models"]').catch(() => 0); await p.waitForTimeout(300);
  const mid = await ev('(()=>{const L=Object.entries(VEHICLE_CATALOG).filter(([id,c])=>!c.license||licenseOwned(c.license));return L.length>1?L[1][0]:L[0][0]})()');
  await p.click('#gstRoot [data-gst-model="' + mid + '"]').catch(e => R.dErr = String(e).slice(0, 160)); await p.waitForTimeout(500); R.modelD = await ev('GSTUI.U.model');
  await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.waitForTimeout(200); await p.click('#gstRoot [data-gst-c="6"]').catch(() => 0); await p.waitForTimeout(600); await shot('d2_model');
  R.dealerBefore = await ev('({m:PlayerProfile.money,n:ensureGarageSchema().vehicles.length,basket:GSTUI.basket()})');
  await p.click('#gstRoot [data-gst-buy]').catch(e => R.dBuyErr = String(e).slice(0, 160)); await p.waitForTimeout(900);
  R.dealerAfter = await ev('(()=>{const g=ensureGarageSchema(),v=g.vehicles[g.vehicles.length-1];return{m:PlayerProfile.money,n:g.vehicles.length,last:{id:v.vehicleId,c:v.colorIndex,color:v.color,r:v.rimIndex}}})()'); await shot('d3_bought');
  await ev('setPhoneOpen(false)');
  // the home garage
  R.openH = await ev('__TC_GST.open("home")'); await p.waitForTimeout(1500); R.auditH = JSON.parse(await ev('__TC_GST.audit()')); await shot('h1_home');
  await p.click('#gstRoot [data-gst-tab="cars"]').catch(() => 0); await p.waitForTimeout(300); const cb = await p.$$('#gstRoot [data-gst-car]'); if (cb.length > 1) await cb[cb.length - 1].click(); await p.waitForTimeout(700);
  R.homeCar = await ev('GSTUI.curCar()&&GSTUI.curCar().asset'); await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.click('#gstRoot [data-gst-c="8"]').catch(() => 0); await p.waitForTimeout(500);
  R.homeBasket = await ev('({b:GSTUI.basket(),buyBtn:!!document.querySelector("#gstRoot [data-gst-buy]"),nav:!!document.querySelector("#gstRoot [data-nav-target]")})'); await shot('h2_home_preview');
  await ev('setPhoneOpen(false)');
  R.gst = await ev('__TC_GST.GST'); R.errs = errs;
  fs.writeFileSync(path.join(out, 'gst_probe.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
