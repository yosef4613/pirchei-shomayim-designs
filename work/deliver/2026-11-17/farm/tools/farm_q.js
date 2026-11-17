// farm · 17.11 — הבדיקה של החקלאות בתוך המשחק: farmAudit, כל חלקה נפתחת ב-F עם הכרטיס, מחזור מלא בצפון (קטיף → זרעים בבית האריזה → שתילה → גדילה → קטיף → מכירה בחנות הכפר),
// והאריח של הקרקע: אחרי קטיף ב-A6-VEG — האם הפיקסלים של השדה השתנו בלי wtcInvalidate (ההוכחה של התקלה הישנה, ושל התיקון).
return (async()=>{const R={build:BUILD,steps:[]},T=ms=>new Promise(r=>setTimeout(r,ms)),F=window.__TC_FARM,has2=!!(F&&F.FARM2);
 const px=(wx,wy)=>{const g=GAME_CTX,cvs=g.canvas,d=window.devicePixelRatio||1,sx=Math.round((wx-Camera.x)*Camera.zoom*d+cvs.width/2),sy=Math.round((wy-Camera.y)*Camera.zoom*d+cvs.height/2);
   const a=CanvasRenderingContext2D.prototype.getImageData.call(g,sx-20,sy-20,40,40).data;let r=0,gg=0,n=0;for(let i=0;i<a.length;i+=4){r+=a[i];gg+=a[i+1];n++}return Math.round((gg-r)/n)};
 const until=async(f,ms)=>{const t=performance.now();while(performance.now()-t<ms){if(f())return true;await T(250)}return false};
 try{R.audit=F.audit();R.plots=has2?F.plots().length:Object.keys(FARM_FIELDS).length}catch(e){R.audit={error:String(e)}}
 PlayerProfile.money+=20000;
 /* (1) האריח: A6-VEG — קטיף, ובדיקה של הפיקסלים */
 try{const f=A6_FIELDS.find(q=>q.id==='A6-VEG'),cx=f.x+f.w/2,cy=f.y+f.h/2,cam=()=>{Camera.zoom=1.2;Camera.x=cx;Camera.y=cy;try{State.camFollow=false}catch(e){}};F.demo.at('A6-VEG');setPhoneOpen(false);cam();await T(2500);cam();await T(600);
  const a=px(cx,cy),p=a6FarmPersistent();p.crops['A6-VEG']={crop:null,empty:true,harvestedAt:p.clock};farmSyncAll();cam();await T(2500);cam();await T(400);const b=px(cx,cy);
  wtcInvalidate();cam();await T(2500);cam();await T(400);const c=px(cx,cy);
  R.tile={greenMinusRed:{full:a,emptyNoInvalidate:b,emptyAfterInvalidate:c},staleWithoutInvalidate:Math.abs(a-b)<3&&Math.abs(b-c)>=3,updatedWithoutInvalidate:Math.abs(a-b)>=3,dirty:has2?F.FARM2.n.dirty:null}}catch(e){R.tile={error:String(e&&e.stack||e).slice(0,300)}}
 if(!has2){R.farmErr=FARM.err;return R}
 /* (2) כל חלקה בצפון: F → הכרטיס */
 R.cards={};for(const id of Object.keys(F.FARM2.plots)){try{const ok=F.demo.at2(id);await T(60);const h=document.querySelector('#phone, .phone, [id*=phone]')?.innerText||'';const html=phoneS12Business(id);
   R.cards[id]={open:ok,card:/בוחרים גידול|מוכן לקטיף|גדל —/.test(html),held:farmHeld(id),stage:F.stage(id)}}catch(e){R.cards[id]={error:String(e).slice(0,160)}}}
 try{setPhoneOpen(false)}catch(e){}
 /* (3) מחזור מלא — החממה של התותים */
 const G='D1-GH-E-S',S=(k,v)=>R.steps.push([k,v]);
 try{F.demo.at2(G);setPhoneOpen(false);S('ready',F.ready(G));S('start',F.start(G,'hand'));S('done1',await until(()=>!State.farmWork,60000));S('afterHarvest',F.state(G));S('inv',PlayerProfile.inventory['a6-strawberry']||0);S('stage0',F.stage(G));
  F.demo.at2('D1-PACK');S('heldMarket',farmHeld('A6-MARKET'));S('buy',F.buy('strawberry',1));S('pepperBuy',F.buy('pepper',1));S('packCard',/זרעים לשדות/.test(phoneS12Business('D1-PACK')));
  F.demo.at2(G);S('sow',F.sow(G,'strawberry'));S('stage1',F.stage(G));F.demo.grow(150);await T(1600);S('dirtyAfterGrow',F.FARM2.n.dirty);S('stage2',F.stage(G));F.demo.grow(400);await T(1300);S('stage3',F.stage(G));
  setPhoneOpen(false);S('start2',F.start(G,'hand'));S('done2',await until(()=>!State.farmWork,60000));const n=PlayerProfile.inventory['a6-strawberry']||0;S('inv2',n);
  F.demo.at2('C1-SHOP');const m0=PlayerProfile.money;S('sell',F.sell('a6-strawberry',true));S('earned',PlayerProfile.money-m0);
  /* שדה נמוך: תירס לא נשתל ליד אורות הגישה */
  F.demo.at2('D0-POTATO');setPhoneOpen(false);S('potReady',F.ready('D0-POTATO'));S('potStart',F.start('D0-POTATO','machine'));S('done3',await until(()=>!State.farmWork,60000));S('potEmpty',F.state('D0-POTATO'));F.buy('corn',1);
  const inv0=PlayerProfile.inventory['a6-seed-corn']||0;F.demo.at2('C1-SHOP');F.buy('corn',1);F.demo.at2('D0-POTATO');S('cornOnLow',F.sow('D0-POTATO','corn'));S('cornSeedsKept',(PlayerProfile.inventory['a6-seed-corn']||0));
  S('lowCardNoCorn',!/<b>תירס<\/b>/.test(phoneS12Business('D0-POTATO')));
 }catch(e){S('error',String(e&&e.stack||e).slice(0,300))}
 try{setPhoneOpen(false)}catch(e){}
 /* (4) הצייר: ציור של החלקה בכל שלב בקנבס צדדי — בלי שגיאה */
 try{const cv=document.createElement('canvas');cv.width=400;cv.height=300;const g=cv.getContext('2d');const L={};for(const c of FARM_CROPS){L[c.id]=[];for(let st=0;st<4;st++){g.clearRect(0,0,400,300);farm2Paint(g,[Camera.x-100,Camera.y-60,Camera.x+100,Camera.y+60],'X',c.id,st,false);L[c.id].push(st)}}R.painter='ok '+Object.keys(L).length}catch(e){R.painter='err '+String(e).slice(0,200)}
 R.audit2=F.audit();R.farmErr=FARM.err;R.farm2Err=F.FARM2.err;R.n2=F.FARM2.n;return R})()
