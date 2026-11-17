// save_reload.js — הליגה אחרי שמירה, טעינה מחדש של הדף וטעינת השמירה, ואז עוד 3 ימי משחק (סוכן stadium, 17.11)
// node save_reload.js <game.html> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const SNAP = `(()=>{const c=gameClock(),L=LEAGUE4.st();let N=null;try{N=A34PLAY.nextMatch()}catch(e){}return {day:c.day,hhmm:c.hhmm,season:L.season,round:L.round,lastDay:L.lastDay,res:L.res.map(r=>r&&r.day),sign:LEAGUE4.signLine(),next:N&&N.day,err:LEAGUE4.err(),bench:!!window.__TC_BENCH}})()`;
const ADV = d => `(async()=>{for(let i=0;i<${d}*48;i++){G84_CLOCK.base+=30;LEAGUE4.tick();await new Promise(r=>setTimeout(r,20))}return 1})()`;
(async () => {
  const [file, out] = process.argv.slice(2); const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s);
  const open = async () => { await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(1500) };
  const R = {}; await open(); R.a_start = await ev(SNAP); await ev(ADV(7)); R.b_day8 = await ev(SNAP);
  R.save = await ev(`(()=>{const r=SaveManager.save('manual');return {ok:r&&r.ok,clock:gameClockSave()}})()`);
  await open(); R.c_reload = await ev(SNAP);
  R.load = await ev(`(()=>{const r=SaveManager.load({silent:true});return {ok:r&&r.ok,src:r&&r.source,err:r&&r.error}})()`); await p.waitForTimeout(2500); R.d_loaded = await ev(SNAP);
  await ev(ADV(3)); R.e_plus3 = await ev(SNAP); R.errs = errs;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
