// בדיקת הדף: 0 שגיאות, מספר הפריטים, סינון ותיבת סימון; צילום לעצמי (scratchpad). node page_check.js <ledger.html> <shot.png>
const { chromium } = require('playwright');
const path=require('path');
(async()=>{const [f,shot]=process.argv.slice(2);const b=await chromium.launch();const r={};
 for(const [w,h,sch] of [[1280,900,'light'],[390,800,'dark']]){
  const p=await b.newPage({viewport:{width:w,height:h},colorScheme:sch});const errs=[];p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto('file://'+path.resolve(f));await p.waitForTimeout(400);
  const n=await p.$$eval('.it',x=>x.length);const planRows=await p.$$eval('#planT tbody tr',x=>x.length);const ownRows=await p.$$eval('#ownT tbody tr',x=>x.length);
  await p.click('#fSt .chip[data-v="N"]');const nNo=await p.$$eval('.it',x=>x.length);
  await p.click('#fSt .chip[data-v="N"]');
  await p.check('.it input[type=checkbox] >> nth=0');const chk=await p.$$eval('.it.chk',x=>x.length);
  const sw=await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  await p.screenshot({path:shot.replace('.png','_'+w+'.png')});
  r[w]={items:n,planRows,ownRows,filtered_no:nNo,checked:chk,hscroll:sw,errors:errs};await p.close()}
 console.log(JSON.stringify(r));await b.close()})();
