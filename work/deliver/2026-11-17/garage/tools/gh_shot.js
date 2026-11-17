// gh_shot.js — המוסך בעולם (garage, 17.11): צילומים לבדיקה פנימית במבט 3/4 בכמה זומים, ביום ובלילה, ודגימה של מי שעובר באזור הקבלה (רכבים, אנשים).
// node gh_shot.js <game.html> <out_dir> [sampleSec=0]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, sec0] = process.argv.slice(2); const sec = +sec0 || 0; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const R = {};
  // the player on foot west of the garage, the camera on the hall
  await ev('PlayerProfile.mode="walk";PlayerPed.x=4228;PlayerPed.y=2330;PlayerCar.x=4228;PlayerCar.y=2250;1');
  for (const [n, z, x, y] of [['z1', 1.0, 4340, 2420], ['z2', 2.2, 4355, 2430], ['z35', 3.5, 4380, 2440], ['z35w', 3.5, 4285, 2445]]) {
    await ev(`PlayerProfile.mode='walk';PlayerPed.x=${x};PlayerPed.y=${y+70};Camera.x=${x};Camera.y=${y};Camera.zoom=${z};1`); await p.waitForTimeout(2500);
    await ev(`Camera.x=${x};Camera.y=${y};Camera.zoom=${z};1`); await p.waitForTimeout(600); await p.screenshot({ path: path.join(out, n + '.png') }) }
  R.state = await ev('typeof GHALL!=="undefined"?GHALL:null'); R.audit = await ev('window.__TC_GHALL?__TC_GHALL.audit():null'); R.tow = await ev('window.__TC_TOW?__TC_TOW.audit():null');
  if (sec > 0) {   // who passes through the rectangle of the reception (cars of the simulation, people) — rule 4: measured, not guessed
    R.sample = await ev(`(async()=>{const RC=[4248,2426,4308,2482],hit={cars:0,peds:0,ids:new Set(),pts:[]};const inR=(x,y)=>x>=RC[0]&&x<=RC[2]&&y>=RC[1]&&y<=RC[3];
      const t0=performance.now();while(performance.now()-t0<${sec * 1000}){try{for(const c of (TRAFFIC_CARS||[])){if(inR(c.x,c.y)){hit.cars++;hit.ids.add(c.id);if(hit.pts.length<20)hit.pts.push(['car',c.id,Math.round(c.x),Math.round(c.y)])}}
        for(const q of (NPC_PEDESTRIANS||[])){if(inR(q.x,q.y)){hit.peds++;if(hit.pts.length<20)hit.pts.push(['ped',q.id,Math.round(q.x),Math.round(q.y)])}}}catch(e){hit.err=String(e)}
        await new Promise(r=>setTimeout(r,250))}return{cars:hit.cars,peds:hit.peds,ids:[...hit.ids],pts:hit.pts,err:hit.err||null,nCars:(TRAFFIC_CARS||[]).length}})()`);
  }
  R.errs = errs; fs.writeFileSync(path.join(out, 'gh_shot.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 2500));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
