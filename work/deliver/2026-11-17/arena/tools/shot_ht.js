// shot_ht.js — צילום לבדיקה פנימית בלבד (לא לדף) של מופעי המחצית + הבדיקה TCARENA.audit. node shot_ht.js <build> <outdir> [ks=0,1,2,3] [ss=2,6.5,8.5]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => { const [file, out, ksA, ssA] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true }); const KS = (ksA || '0,1,2,3').split(',').map(Number), SS = (ssA || '2,6.5,8.5').split(',').map(Number);
 const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
 const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
 await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
 const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s); const R = { shots: [] };
 R.day = await ev(`(()=>{try{gameClockSet(13,0)}catch(e){}return gameClock().hhmm})()`);
 R.audit = await ev(`TCARENA.audit()`);
 for (const k of KS) { const r = await ev(`SPORT2.dev.half(${k})`); for (const s of SS) {
   const info = await ev(`(()=>{const g=A34PLAY.gm(),M=window.__TC_A3_MATCH;M.K=g-(194+${s})/2;State.mapQa=true;Camera.x=625;Camera.y=2205;Camera.zoom=${s < 3 ? 3.2 : 4.2};const I=A34PLAY.matchInfo(),S=SPORT2.a3Info(M.idx,I.u);return {u:I.u,ht:S.ht,err:SPORT2.err()}})()`);
   await p.waitForTimeout(1600); const f = path.join(out, 'ht' + k + '_' + String(s).replace('.', '_') + '.png'); await p.screenshot({ path: f }); R.shots.push({ k, s, r, info, f }); } }
 R.f9 = await ev(`(()=>{try{if(!PERF.hud)perfHudToggle();tcF9Show('events');const c=TCF9.el.querySelector('[data-arena-card]');const t=c?c.innerText:null;perfHudToggle();return t}catch(e){return 'err '+e.message}})()`);
 R.plc = await ev(`(()=>{try{return plcStadium().replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').slice(-400)}catch(e){return 'err '+e.message}})()`);
 R.errs = errs; console.log(JSON.stringify(R, null, 1)); await b.close(); })();
