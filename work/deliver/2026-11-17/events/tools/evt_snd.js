// בדיקת הסירנה: node evt_snd.js <build> <out.json> — הדף ב-#dev&snd (השמע חי), לחיצה (ההקשר נוצר רק בלחיצה), אדם נופל ליד השחקן → האמבולנס בדרך עם סירנה
// (TCSFX.state().list — לולאה 'siren' עם עוצמה), ובזירה — בלי סירנה; 0 שגיאות שמע ו-0 שגיאות דף.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox', '--autoplay-policy=no-user-gesture-required'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev&snd', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => { try { return window.__TC_DEV.ev(x) } catch (e) { return { ERR: String(e && e.message || e) } } }, s);
  await ev(`(typeof p34LibInit==='function'&&!window.P34&&p34LibInit(),1)`); await p.waitForTimeout(2000);
  await p.mouse.click(640, 400); await p.waitForTimeout(1500);
  const R = { build: path.basename(file), snd0: await ev(`(()=>{const s=TCSFX.state();return{off:s.off,ctx:s.ctx,loops:s.loops}})()`), recipe: await ev(`typeof TCSFXLIB.LOOP.siren`) };
  await ev(`(EVT.next.fire=EVT.next.fall=EVT.next.flee=1e9,1)`);
  const id = await ev(`(()=>{const e=evtStart('fall',{near:true,f9:true});if(e)evtF9Watch(e);return e?e.id:null})()`); R.id = id;
  const seen = []; let heard = 0, atScene = null; const t0 = Date.now();
  while ((Date.now() - t0) / 1000 < 150) {
    await p.waitForTimeout(700);
    const s = await ev(`(()=>{const S=__TC_EVT.state(),a=S.act.find(e=>e.id===${JSON.stringify(id)}),T=TCSFX.state(),L=T.list.filter(q=>q[1]==='siren');return{ph:a&&a.ph,sirens:S.sirens,list:L,errs:T.errs||0,err:T.err||null,ctx:T.ctx}})()`);
    if (s.ERR) { R.err = s.ERR; break }
    seen.push([s.ph, s.sirens.length, s.list.map(q => q[2])]); if (s.list.some(q => q[2] > 0.003)) heard++;
    if (s.ph === 'load') { atScene = s; break } }
  R.samples = seen.slice(-30); R.heard = heard; R.atScene = atScene; R.snd1 = await ev(`(()=>{const s=TCSFX.state();return{ctx:s.ctx,by:s.by,errs:s.errs,err:s.err,dropped:s.dropped}})()`);
  R.pageErrors = pe;
  R.ok = R.recipe === 'function' && heard > 0 && !!atScene && atScene.sirens.length === 0 && !pe.length && !(R.snd1 && R.snd1.errs);
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, ctx: R.snd0 && R.snd0.ctx, recipe: R.recipe, heard, atScene: atScene && atScene.sirens, by: R.snd1 && R.snd1.by && R.snd1.by.siren, errs: R.snd1 && R.snd1.errs, pe: pe.length }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
