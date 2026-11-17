// shot_fly.js (police 17.11) — צילומים לבדיקה בעין בלבד (לא לדף): המסוק במנחת ובאוויר, המטוס בהסעה ובאוויר, הטבעת.
// node shot_fly.js <game.html> <outdir>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, od] = process.argv.slice(2); fs.mkdirSync(od, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev('(()=>{'+s+'\n})()')).then(v => JSON.stringify(v)), s);
  const shots = [
    ['heli_pad', `const F=__TC_FLY;PlayerProfile.money=9000;PlayerProfile.licenses['LIC-14']={state:'owned'};delete PlayerProfile.licenses['LIC-16'];PlayerProfile.mode='walk';const q=S15_POIS['S15-FENCE-HELI'];PlayerPed.x=q.x;PlayerPed.y=q.y;Camera.zoom=1.6;const r=F.start('heli',{exam:true});F.S.ctl={};for(let i=0;i<60;i++)F.step(1/30);return r`],
    ['heli_air', `const F=__TC_FLY;F.S.ctl={up:1};for(let i=0;i<120;i++)F.step(1/30);F.S.ctl={};Camera.zoom=1.3;return F.audit().c`],
    ['heli_ring', `const F=__TC_FLY;F.S.ctl=null;F.S.auto=true;for(let i=0;i<30*7;i++){F.step(1/30);if(F.S.exam.i>=2&&F.S.c.z>150)break}F.S.auto=false;F.S.ctl={};Camera.zoom=1;return F.audit()`],
    ['plane_stand', `const F=__TC_FLY;F.S.auto=true;for(let i=0;i<30*120;i++){F.step(1/30);if(F.S.exam&&F.S.exam.res&&F.S.c.z<=0)break}F.exit();F.S.auto=false;F.S.ctl=null;delete PlayerProfile.licenses['LIC-14'];PlayerProfile.mode='walk';const q=S15_POIS['S15-FENCE-GA'];PlayerPed.x=q.x;PlayerPed.y=q.y;const r=F.start('plane',{exam:true});F.S.ctl={};Camera.zoom=1.6;return [r,F.audit()]`],
    ['plane_taxi', `const F=__TC_FLY;F.S.ctl=null;F.S.auto=true;for(let i=0;i<30*12;i++)F.step(1/30);F.S.auto=false;F.S.ctl={};Camera.zoom=1.3;return F.audit().c`],
    ['plane_air', `const F=__TC_FLY;F.S.ctl=null;F.S.auto=true;for(let i=0;i<30*60;i++){F.step(1/30);if(F.S.exam.i>=6)break}F.S.auto=false;F.S.ctl={};Camera.zoom=1;return F.audit()`],
  ];
  const log = {};
  for (const [n, s] of shots) { try { log[n] = await ev(s); } catch (e) { log[n] = 'ERR ' + String(e).slice(0, 300) } await p.waitForTimeout(2500); await p.screenshot({ path: path.join(od, n + '.png') }); }
  try { log.hud = await ev(`return [$('hudGoal')&&$('hudGoal').textContent,$('hudSpeed')&&$('hudSpeed').textContent,__TC_FLY.ERR.e]`) } catch (e) { }
  log.errs = errs; fs.writeFileSync(path.join(od, 'shots.json'), JSON.stringify(log, null, 1)); await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
