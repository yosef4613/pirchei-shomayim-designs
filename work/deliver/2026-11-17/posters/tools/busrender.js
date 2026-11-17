// ציור של אוטובוס עירוני וקואץ׳ בתוך הדף (דרך BX — אותו צייר ואותם מדבקות), לבדיקה בעין שלי: node busrender.js <build> <shot.png>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, shot] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(3000);
  const r = await p.evaluate(() => __TC_DEV.ev(`(()=>{const out={};try{
   const box=document.createElement('div');box.style.cssText='position:fixed;inset:0;z-index:99999;background:#6b6f73;display:flex;flex-wrap:wrap;gap:4px';document.body.appendChild(box);
   const T=tcbrBusTable();let ent=null,wr=null;for(const v of T.values()){if(v.mode==='plaque'&&!ent&&v.line!==5)ent=v;if(v.mode==='plaque'&&v.line===5&&!out.l5)out.l5=v}
   out.ent=ent;const N=32,Z=3;
   for(const [kindId,e] of [['city',ent],['line5',out.l5]]){if(!e)continue;const K=BX.kinds.find(q=>q.id===kindId);if(!K){out['no_'+kindId]=1;continue}
    const d={line:e.line,col:BX.col[e.line],look:'c'+e.line,serial:e.no,num:e.line,txt:'בדיקה',door:0,B:null,lit:false};
    for(const k of [0,4,8,16,20,24]){const s=K.sprite(d,k,N,Z,false,0);if(!s){out['nos_'+kindId]=1;continue}const cv=document.createElement('canvas');cv.width=440;cv.height=290;cv.style.cssText='width:440px;height:290px;flex:none';const c=cv.getContext('2d');
     c.translate(220,150);c.scale(Z,Z);c.drawImage(s.cv,-s.ox/s.res,-s.oy/s.res,s.cv.width/s.res,s.cv.height/s.res);out.st=(out.st||0)+K.stickers(c,d,s.k,N,{night:false,px:Z,res:s.res});box.appendChild(cv)}}
   out.b4=__TC_BUSAD4.stats();out.err=TCBR.err}catch(e){out.e=String(e.stack||e).slice(0,500)}return out})()`));
  await p.screenshot({ path: shot });
  console.log(JSON.stringify(r).slice(0, 1500), 'errs', errs.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
