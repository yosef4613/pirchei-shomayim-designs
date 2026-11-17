// צילום של אוטובוס (לבדיקה בעין שלי בלבד): node busshot.js <build> <outdir> [n]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outd, nn] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(8000);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => JSON.stringify(v)), s).then(JSON.parse);
  const info = await ev(`(()=>{State.mapQa=true;try{G77_ASV.on=false}catch(e){}const o=[];try{for(const B of LN.bus){const x=B.x!=null?B.x:(B.p&&B.p.x),y=B.y!=null?B.y:(B.p&&B.p.y);o.push({no:B.no,line:B.L&&B.L.line,x,y,keys:Object.keys(B).slice(0,30)})}}catch(e){o.push(String(e))}return o.slice(0,40)})()`);
  fs.writeFileSync(outd + '/buses.json', JSON.stringify(info, null, 1));
  let k = 0;
  for (const B of info) { if (!B || B.x == null || k >= (+nn || 4)) continue;
    await ev(`(()=>{Camera.x=${B.x};Camera.y=${B.y};Camera.zoom=3.2;return 1})()`); await p.waitForTimeout(700);
    const B2 = await ev(`(()=>{const B=LN.bus.find(q=>q.no==${JSON.stringify(B.no)});return B?{x:B.x,y:B.y}:null})()`);
    if (B2 && B2.x != null) { await ev(`(()=>{Camera.x=${B2.x};Camera.y=${B2.y};return 1})()`); await p.waitForTimeout(300) }
    await p.screenshot({ path: outd + '/bus_' + B.no + '.png', clip: { x: 300, y: 200, width: 600, height: 400 } }); k++ }
  const st = await ev(`(()=>({b4:window.__TC_BUSAD4&&__TC_BUSAD4.stats(),br:TCBR.n,err:TCBR.err}))()`);
  console.log(JSON.stringify({ st, errs })); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
