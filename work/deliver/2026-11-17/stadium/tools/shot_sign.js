// shot_sign.js — צילום לבדיקה פנימית בלבד (לא לדף): השלט של האצטדיון לפני / אחרי מחזור. node shot_sign.js <build> <outprefix>
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [file, pre] = process.argv.slice(2); const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
 const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
 await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
 const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s);
 const cam = `(()=>{State.mapQa=true;Camera.x=770;Camera.y=2420;Camera.zoom=4.5;return 1})()`;
 await ev(cam); await p.waitForTimeout(2500); await p.screenshot({ path: pre + '_a.png' });
 const r = await ev(`(async()=>{for(let i=0;i<3*48;i++){G84_CLOCK.base+=30;LEAGUE4.tick();await new Promise(r=>setTimeout(r,10))}const c=gameClock();return c.day+' '+c.hhmm+' r'+LEAGUE4.st().round})()`);
 await ev(cam); await p.waitForTimeout(2500); await p.screenshot({ path: pre + '_b.png' }); console.log(r, 'errs', errs.length, errs.slice(0, 3).join(' | ')); await b.close(); })();
