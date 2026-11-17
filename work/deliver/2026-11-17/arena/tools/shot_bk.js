// shot_bk.js — צילום לבדיקה פנימית בלבד (לא לדף) של אולם הכדורסל באי + הבדיקות. node shot_bk.js <build> <outdir>
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => { const [file, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
 const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
 const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
 await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
 const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s); const R = { shots: [] };
 R.day = await ev(`(()=>{try{gameClockSet(13,0)}catch(e){}return gameClock().hhmm})()`);
 R.land = await ev(`TCARENA.land()`); R.audit = await ev(`(()=>{const t=performance.now();const a=TCARENA.bkAudit();a.ms=Math.round(performance.now()-t);return a})()`); R.lg = await ev(`LEAGUEBK.audit()`);
 R.go = await ev(`(()=>{const r=TCARENA.go('match');return r})()`);
 for (const [u, z, tag] of [[-40, 1.3, 'wide'], [8, 2.4, 'walkin'], [80, 2.4, 'h1'], [150, 3.2, 'h1z'], [261, 2.6, 'show'], [266, 3.2, 'showz'], [330, 2.4, 'h2'], [500, 2.4, 'end']]) {
  const info = await ev(`(()=>{const g=A34PLAY.gm(),O=TCARENA.OV;O.K=g-(${u})/2;State.mapQa=true;Camera.x=5405;Camera.y=${z < 2 ? 7470 : 7505};Camera.zoom=${z};const I=TCARENA.info();return {u:I.u,line:I.line,sc:I.sc,clock:I.clock,err:TCARENA.err()}})()`);
  await p.waitForTimeout(1500); const f = path.join(out, 'bk_' + tag + '.png'); await p.screenshot({ path: f }); R.shots.push({ u, tag, info }); }
 R.bkht = await ev(`(()=>{const r=TCARENA.go('half');const O=TCARENA.OV;O.K=A34PLAY.gm()-(256+7)/2;return {r,line:TCARENA.info().line}})()`); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(out, 'bk_half2.png') });
 R.phone = await ev(`(()=>{try{return PHONE_VIEWS.news().replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').slice(0,600)}catch(e){return 'err '+e.message}})()`);
 R.f9 = await ev(`(()=>{try{if(!PERF.hud)perfHudToggle();tcF9Show('events');const c=TCF9.el.querySelector('[data-arena-bk]');const t=c?c.innerText:null;perfHudToggle();return t}catch(e){return 'err '+e.message}})()`);
 R.err = await ev(`TCARENA.err()`); R.errs = errs; console.log(JSON.stringify(R, null, 1)); await b.close(); })();
