// צילום לבדיקה פנימית בלבד (לא לדף): node shot.js <html> <out.png> [w] [h] [waitms]
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const [f,o,w,h,wt]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w||1600,height:+h||900}});
const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,300)));p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text().slice(0,300))});
await p.goto('file://'+path.resolve(f));await p.waitForTimeout(+wt||1500);
const r=await p.evaluate(()=>window.__res||null);console.log(JSON.stringify({r,errs}));await p.screenshot({path:o,fullPage:true});await b.close()})();
