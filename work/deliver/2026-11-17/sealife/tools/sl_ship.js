// sl_ship.js <game.html> <out.json> — sealife: האם האוניות SH-L5 / SH-L5B מצוירות כשהמפתח למעלה והמצלמה רחוקה מהגשר (הביקורת חלק 2 סעיף 1)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500); const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  await ev(`(()=>{window.__SLC={};const o=BOAT34.paint;BOAT34.paint=function(c,spec){try{if(spec&&spec.id)window.__SLC[spec.id]=(window.__SLC[spec.id]||0)+1}catch(e){}return o.apply(this,arguments)};return 1})()`);
  let st = null, t = 0;
  for (; t < 900; t += 10) { await ev(`window.__TC_SIM_STEP_QA({seconds:10,warmup:0,every:10})`); st = await ev(`(()=>{const L=window.__TC_S13LIFT();return{st:L.st,h:L.h}})()`); if (st.h > 0.3) break }
  const res = { simS: t, lift: st, views: [] };
  const cams = [['ship', .5], ['ship', .25], ['ship', 1.0]];
  for (const id of ['SH-L5', 'SH-L5B']) for (const [k, z] of cams) {
    const pose = await ev(`(()=>{const S=S13_SHIPS.find(s=>s.id==='${id}');const p=s13ShipPose(S);return{x:Math.round(p.x),y:Math.round(p.y)}})()`);
    await ev(`perfCamera({x:${pose.x},y:${pose.y},zoom:${z}})`); await p.waitForTimeout(400);
    await ev(`(window.__SLC={},1)`); await p.waitForTimeout(1500);
    const r = await ev(`(()=>{const L=window.__TC_S13LIFT();return{h:L.h,st:L.st,bridgeInView:e3InView(6500,5700,1700,1300,300),paints:window.__SLC['${id}']||0,inView:(()=>{const S=S13_SHIPS.find(s=>s.id==='${id}'),p=s13ShipPose(S);return e3InView(p.x-700,p.y-700,1400,1400,0)})()}})()`);
    res.views.push(Object.assign({ id, zoom: z, pose }, r));
  }
  res.ok = res.views.every(v => !v.inView || v.paints > 0);
  fs.writeFileSync(out, JSON.stringify({ res, errs }, null, 1)); console.log(JSON.stringify(res)); console.log('errs', JSON.stringify(errs)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
