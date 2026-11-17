// צילום של דף לבדיקה בעין בלבד (לא נכנס לשום דף). node pageshot.js <page.html> <out.png> [width] [fullPage 0/1]
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const [f,o,w,fp]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:+(w||1200),height:900}});
const errs=[];p.on('pageerror',e=>errs.push(String(e)));await p.goto('file://'+path.resolve(f));await p.waitForTimeout(500);
await p.screenshot({path:o,fullPage:fp!=='0'});console.log('errors',errs.length,errs.slice(0,3).join('|'));await b.close()})();
