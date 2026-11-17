p = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/garage/tools/gst_probe.js'
s = open(p).read()
a = """  await p.click('#gstRoot [data-gst-model]:nth-child(3)').catch(() => 0); await p.waitForTimeout(800); R.modelD = await ev('GSTUI.U.model'); await shot('d2_model');"""
b = """  await ev('PlayerProfile.home.garageCapacity=6;1');
  await p.click('#gstRoot [data-gst-tab="models"]').catch(() => 0); await p.waitForTimeout(300);
  const mid = await ev('(()=>{const L=Object.entries(VEHICLE_CATALOG).filter(([id,c])=>!c.license||licenseOwned(c.license));return L.length>1?L[1][0]:L[0][0]})()');
  await p.click('#gstRoot [data-gst-model="' + mid + '"]').catch(e => R.dErr = String(e).slice(0, 160)); await p.waitForTimeout(500); R.modelD = await ev('GSTUI.U.model');
  await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.waitForTimeout(200); await p.click('#gstRoot [data-gst-c="6"]').catch(() => 0); await p.waitForTimeout(600); await shot('d2_model');
  R.dealerBefore = await ev('({m:PlayerProfile.money,n:ensureGarageSchema().vehicles.length,basket:GSTUI.basket()})');
  await p.click('#gstRoot [data-gst-buy]').catch(e => R.dBuyErr = String(e).slice(0, 160)); await p.waitForTimeout(900);
  R.dealerAfter = await ev('(()=>{const g=ensureGarageSchema(),v=g.vehicles[g.vehicles.length-1];return{m:PlayerProfile.money,n:g.vehicles.length,last:{id:v.vehicleId,c:v.colorIndex,color:v.color,r:v.rimIndex}}})()'); await shot('d3_bought');"""
assert s.count(a) == 1
s = s.replace(a, b)
a = """  R.openH = await ev('__TC_GST.open("home")'); await p.waitForTimeout(1500); R.auditH = JSON.parse(await ev('__TC_GST.audit()')); await shot('h1_home');"""
b = """  R.openH = await ev('__TC_GST.open("home")'); await p.waitForTimeout(1500); R.auditH = JSON.parse(await ev('__TC_GST.audit()')); await shot('h1_home');
  await p.click('#gstRoot [data-gst-tab="cars"]').catch(() => 0); await p.waitForTimeout(300); const cb = await p.$$('#gstRoot [data-gst-car]'); if (cb.length > 1) await cb[cb.length - 1].click(); await p.waitForTimeout(700);
  R.homeCar = await ev('GSTUI.curCar()&&GSTUI.curCar().asset'); await p.click('#gstRoot [data-gst-tab="c"]').catch(() => 0); await p.click('#gstRoot [data-gst-c="8"]').catch(() => 0); await p.waitForTimeout(500);
  R.homeBasket = await ev('({b:GSTUI.basket(),buyBtn:!!document.querySelector("#gstRoot [data-gst-buy]"),nav:!!document.querySelector("#gstRoot [data-nav-target]")})'); await shot('h2_home_preview');"""
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w').write(s)
print('ok')
