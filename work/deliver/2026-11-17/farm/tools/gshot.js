// צילומים לבדיקה בעין בלבד (לא נכנסים לשום דף). node gshot.js <game.html> <outdir> <tag>
// לכל נקודה: מצב (ביטוי JS), מצלמה (x, y, zoom) — ומצלם.
const { chromium } = require('playwright'); const path=require('path'),fs=require('fs');
const SPOTS=[
 ['a6veg_straw',"(()=>{const F=window.__TC_FARM,s=a6FarmPersistent();s.crops['A6-VEG']={crop:'strawberry',plantedAt:s.clock-999,readyAt:s.clock-1};farmSyncAll();try{farm2Check(true)}catch(e){}wtcInvalidate();return 1})()",414,4380,2.2],
 ['a6veg_flower',"(()=>{const s=a6FarmPersistent();s.crops['A6-VEG']={crop:'strawberry',plantedAt:s.clock-200,readyAt:s.clock+160};farmSyncAll();wtcInvalidate();return 1})()",414,4380,2.2],
 ['a6_fields',"1",300,4620,1.0],
 ['d1_gh',"1",4270,470,0.9],
 ['d1_gh_close',"1",4560,560,2.0],
 ['c0_d0',"1",3500,-330,0.45],
 ['c1_fields',"1",2640,210,1.2],
 ['d0_close',"1",3900,-200,1.8],
];
(async()=>{const [file,out,tag]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
 await p.goto('file://'+path.resolve(file)+'#dev',{waitUntil:'commit'});await p.waitForFunction(()=>window.__TC_DEV&&window.__TC_DEV.ready(),null,{timeout:600000,polling:500});await p.waitForTimeout(1500);
 for(const [n,ex,x,y,z] of SPOTS){try{await p.evaluate(([ex,x,y,z])=>{const D=window.__TC_DEV;D.ev(ex);D.ev(`try{setPhoneOpen(false)}catch(e){};PlayerProfile.mode='walk';PlayerPed.x=${x};PlayerPed.y=${y}+40;Camera.x=${x};Camera.y=${y};Camera.zoom=${z};State.camFollow=false`)},[ex,x,y,z]);
  await p.waitForTimeout(2500);await p.evaluate(([x,y,z])=>window.__TC_DEV.ev(`Camera.x=${x};Camera.y=${y};Camera.zoom=${z}`),[x,y,z]);await p.waitForTimeout(1200);await p.screenshot({path:path.join(out,tag+'_'+n+'.png')})}catch(e){console.log('spot',n,String(e).slice(0,200))}}
 console.log('errors',errs.length,errs.slice(0,3).join(' | '));await b.close()})();
