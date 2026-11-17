// 2.11 · liveAudit (D‑339; הבעלים 18:21): הבדיקה הקבועה של הפרטים החיים — בכל מסירה.
// (1) liveAudit() של המשחק: לכל אזור שנבנה מחדש — הדברים שזזים לפי סוג; כישלון על פחות מ-8, על פחות מ-4 הסוגים (מים, רוח, אנשים, רכב),
//     על דבר שזז בלי פעולה אמיתית (act / when ריקים); אזור שעוד לא שודרג — רק אם הוא ברשימת החריגים, עם סיבה.
// (2) לכל אזור עם רשימה: השכבה החיה לבד, על קנבס משלה, ברגעים לאורך כל המחזור שלו (ביום ובלילה) — כל דבר ברשימה צריך באמת להשתנות
//     במלבן שלו; דבר שתלוי במצב שאין עכשיו (כשיש מכלית…) — לא נבדק, ונרשם.
// (3) הזמן לפריים איתם: חציון ואחוזון 90 מעל כל אזור עם רשימה ומעל D4 (אותו זום), והעלות של השכבה החיה לבד.
// node tools/dev/live_audit.js <game.html> [out.json]      (Chromium — דרך tools_pack/nolock.sh; לא תחת PERF_LOCK). יציאה 1 — כישלון.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outArg] = process.argv.slice(2); if (!file) { console.error('usage: node live_audit.js <game.html> [out.json]'); process.exit(2) }
  if (fs.existsSync('/home/user/tc_root/tc/pkg/work/PERF_LOCK')) { console.error('PERF_LOCK — not now'); process.exit(2) }
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(3000); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(400) }
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s), J = async s => JSON.parse(await ev(`JSON.stringify(${s})`)),
    JA = async s => JSON.parse(await p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => JSON.stringify(v)), s));
  /* 10.11 (S10 א — המקור מוכח): מחכים שהדמויות (P34) יידלקו לפני בדיקת הפיקסלים; בלי זה הדייגים, הדגים והסירה של B2 / B1 מצוירים בלי תנועה, לפי מהירות המכונה */
  try { await p.waitForFunction(() => window.__TC_DEV.ev("typeof P34!=='undefined'"), null, { timeout: 120000, polling: 500 }) } catch (e) {}
  const R = { build: path.basename(file), at: new Date().toISOString() };
  R.audit =await J(`(typeof liveAudit==='function')?liveAudit():{ok:false,fails:['אין liveAudit במשחק']}`);
  // (2) every listed mover really changes in its box over its cycle — day and night
  R.pixels = await J(`(()=>{const out={};const Z=(window.__TC_LIVE||{zones:{}}).zones,c34=typeof c34Live==='function'?c34Live:null;try{if(c34)c34Live=()=>false;
   for(const z in Z){const Q=Z[z],[x0,y0,x1,y1]=Q.box,W=x1-x0,H=y1-y0,cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d'),t0=1000,T=[];
    for(let k=0;k<32;k++)T.push(t0+Q.cycle*k/32);T.push(t0+.3,t0+.7,t0+1.2,t0+2.1);
    for(const nt of [0,1]){const ids={},st={};
     for(const t of T){g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);g.setTransform(1,0,0,1,-x0,-y0);try{Q.render(g,t*1000,nt)}catch(e){out.err=String(e)}
      for(const m of Q.movers(t*1000,true)){if(m.when&&/^כשיש מכלית/.test(m.when))continue;if(!nt&&m.when==='לילה')continue;const b=m.box,X0=Math.max(0,b[0]-x0),Y0=Math.max(0,b[1]-y0),X1=Math.min(W,b[2]-x0),Y1=Math.min(H,b[3]-y0);if(X1<=X0||Y1<=Y0)continue;
       const d=g.getImageData(X0,Y0,X1-X0,Y1-Y0).data;let n=0,h=0;for(let i=0;i<d.length;i+=4){if(d[i+3]>8)n++;h=(h*31+d[i]+d[i+1]*7+d[i+2]*13+d[i+3]*17+i)>>>0}
       const s=st[m.id]||(st[m.id]={kind:m.kind,act:m.act,when:m.when,drawn:0,hashes:new Set(),pos:new Set()});s.drawn=Math.max(s.drawn,n);if(n>3)s.hashes.add(h);s.pos.add(b.join(','))}}
     const rows=Object.entries(st).map(([id,s])=>({id,kind:s.kind,when:s.when,drawnPx:s.drawn,looks:s.hashes.size,places:s.pos.size,moves:s.drawn>3&&(s.hashes.size>1)}));
     out[z+(nt?'-night':'-day')]={listed:rows.length,moving:rows.filter(r=>r.moves).length,still:rows.filter(r=>!r.moves).map(r=>r.id+'('+r.drawnPx+')'),kinds:[...new Set(rows.filter(r=>r.moves).map(r=>r.kind))]}}}}
   finally{if(c34)c34Live=c34}return out})()`);
  // (3) the frame time with them, at the same zoom, over each listed zone and over D4; the live layer's own cost
  R.cost = await J(`(()=>{const out={},Z=(window.__TC_LIVE||{zones:{}}).zones,c34=typeof c34Live==='function'?c34Live:null;try{if(c34)c34Live=()=>false;for(const z in Z){const Q=Z[z],[x0,y0,x1,y1]=Q.box,cv=document.createElement('canvas');cv.width=x1-x0;cv.height=y1-y0;const g=cv.getContext('2d');g.setTransform(1,0,0,1,-x0,-y0);
    const t0=performance.now();for(let i=0;i<200;i++)Q.render(g,1e6+i*16.7,0);out[z]=+((performance.now()-t0)/200).toFixed(3)}}finally{if(c34)c34Live=c34}return out})()`);
  await ev(`(()=>{try{__TC_C34.arm()}catch(e){}State.paused=false;State.mapQa=true;PlayerProfile.mode='walk';window.__TC_NIGHT=0;return 1})()`);
  const frame = async (x, y) => { await ev(`(()=>{Camera.x=${x};Camera.y=${y};Camera.zoom=1.15;PlayerPed.x=${x};PlayerPed.y=${y};return 1})()`); await p.waitForTimeout(4000);
    return JA(`new Promise(res=>{const L=[];let p0=performance.now();const f=()=>{const t=performance.now();L.push(t-p0);p0=t;if(L.length<120)requestAnimationFrame(f);else{L.shift();L.sort((a,b)=>a-b);res({med:+L[L.length>>1].toFixed(1),p90:+L[Math.floor(L.length*.9)].toFixed(1)})}};requestAnimationFrame(f)})`) };
  R.frame = { D4: await frame(3990, 2900) }; const centers = await J(`Object.fromEntries(Object.entries((window.__TC_LIVE||{zones:{}}).zones).map(([z,Q])=>[z,Q.center]))`);
  for (const z in centers) R.frame[z] = await frame(centers[z][0], centers[z][1]);
  R.liveErr = await J(`(window.__TC_C5D5&&window.__TC_C5D5.liveErr)?window.__TC_C5D5.liveErr():null`); R.errs = errs.slice(0, 6);
  const pixOk = Object.values(R.pixels).filter(v => v && typeof v === 'object').every(v => !v.still.length);
  R.ok = !!(R.audit && R.audit.ok) && pixOk && !R.liveErr && !errs.length;
  const out = path.resolve(outArg || path.join('qa', 'live_audit.json')); fs.writeFileSync(out, JSON.stringify(R, null, 1));
  const Z = R.audit.zones || {}; console.log('liveAudit ' + (R.ok ? 'עובר' : 'נכשל') + ' · ' + Object.entries(Z).map(([z, v]) => z + ': ' + (v.exception ? 'חריג' : v.count + '/' + v.core + (v.ok ? '' : ' ✗'))).join(' · '));
  for (const k in R.pixels) if (R.pixels[k] && R.pixels[k].listed != null) console.log('  ' + k + ': ' + R.pixels[k].moving + '/' + R.pixels[k].listed + ' זזים' + (R.pixels[k].still.length ? ' · עומדים: ' + R.pixels[k].still.join(', ') : ''));
  console.log('  פריים (חציון / 90%): ' + Object.entries(R.frame).map(([k, v]) => k + ' ' + v.med + '/' + v.p90).join(' · ') + ' · השכבה החיה לבד: ' + JSON.stringify(R.cost));
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1) });
