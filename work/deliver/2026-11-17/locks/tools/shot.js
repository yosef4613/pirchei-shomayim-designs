// shot.js <game.html> <out_prefix> — צילום לעצמי (כלל 8): מצב 'story', פתיחה, הגבול C3/D3 והגבול C2/B2, אחרי ניסיון נסיעה לתוך הקיר
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{TCSTORY.E.modeOv='story';g77StRestore({name:'בודק'});TCSTORY.begin({silent:true});const m=TCSTORY.M();m.ch='O';TCLOCK.sig();
    PlayerProfile.mode='vehicle';PlayerCar.x=3480;PlayerCar.y=2271;PlayerCar.heading=0;PlayerCar.speed=0;Camera.x=3560;Camera.y=2250;Camera.zoom=1.1;return {b:TCLOCK.bounds().signs.length}})()`));
  await p.keyboard.down('KeyW'); await p.waitForTimeout(2500); await p.keyboard.up('KeyW'); await p.waitForTimeout(400);
  const s1 = await p.evaluate(() => window.__TC_DEV.ev(`({x:Math.round(PlayerCar.x),y:Math.round(PlayerCar.y),z:currentChunkId(PlayerCar.x,PlayerCar.y),n:TCLOCK.E.n,err:TCLOCK.E.err})`));
  await p.screenshot({ path: out + '_c3d3.png' });
  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{PlayerProfile.mode='walk';PlayerPed.x=2300;PlayerPed.y=1760;Camera.x=2300;Camera.y=1650;Camera.zoom=.8;return 1})()`));
  await p.waitForTimeout(1200); await p.screenshot({ path: out + '_b2.png' });
  console.log(JSON.stringify({ r, s1, errs })); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
