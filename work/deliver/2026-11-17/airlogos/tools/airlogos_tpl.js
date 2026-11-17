/* ==== AIRLOGOS · הלוגואים והשילוט של השדה מחבילת המותגים (17.11.2026; הבעלים ~12:20: "יש המון לוגואים חדשים לכל השדה") ====
   מצאתי (כלל 19): חבילת המותגים (deliver/2026-11-17/set7_share/airport — catalog.js ‏30 רשומות, renderer.js) מגדירה 26 שלטים במידות של
   המשטחים שכבר קיימים במשחק: 13 שלטי החנויות והמזנונים בטרמינל (074x:s15jSignSprite — היום פס צבע + שם), 6 לוחות חברות התעופה מעל איי
   הצ׳ק-אין (074x:s15jTop — מלבן צבע + השם באנגלית), שתי חזיתות הטרמינל (074k:s15bPlate ← 074n:tcbrSign — רק הלוגו), מלון השדה וקיוסק
   ההשכרה (019b:s9Sign). ועוד משטחי זהות בשדה בלי לוגו: ההאנגרים, חוות הדלק, הסדנה, אגף השערים, הכבאות, המשטרה (s15bPlate), שער המטען,
   שער העובדים, המודיעין (s9Sign) — והמגדל, שאין עליו לוח זהות בכלל (074k:s15bTower).
   מה כאן — שדרוג של הקיים (כלל 19א), בלי מנגנון חדש: אותם משטחים, באותו מקום ובאותו גודל; הציור — של המעצב כמו שהוא (renderer.js:
   emblem / sign, מוכנס כאן על ידי tools/gen_airlogos.py), והלוגו של נמל התעופה וההשכרה — מטבלת המותגים האחת (TC_BRANDS, הצייר TCB).
   לוחות הזהות בלי עיצוב בחבילה — הפס של סט 12 (074v_signs12:tcs12Band) עם הלוגו המאושר (נמל התעופה / הכבאות / המשטרה).
   שלטי ההכוונה, לוחות הטיסות, מסכי השערים וסימוני המסלול — בלי שינוי (החבילה: "שומרים על המידע התפעולי").
   שמות חברות התעופה — באנגלית (הבעלים 17.11 12:55: "חברות תעופה באנגלית"). ציור בלבד: שום דבר כאן לא כותב לסימולציה ולא לשמירה. אין תמונות (כלל 17).
   הבדיקה: window.__TC_AIRLOGOS (stats, audit, sample). */
var TCAL={on:true,err:null,n:{shop:0,air:0,plate:0,band:0,s9:0,tower:0,gate:0,e4:0,tail:0,spr:0,hooks:0},spr:new Map(),seen:{}};
function tcalErr(e){TCAL.err=TCAL.err||String(e&&e.stack||e).slice(0,300)}
/* הטבלה (מ-catalog.js): [מזהה, שם, קבוצה, צבע, דיו, סוג הסמל, רוחב, גובה, המשטחים במשחק] */
const TCAL_ROWS=/*@CAT@*/;
const TCAL_BY={};for(const r of TCAL_ROWS)TCAL_BY[r[0]]={id:r[0],name:r[1],group:r[2],color:r[3],ink:r[4],signType:r[5],w:r[6],h:r[7],src:r[8]};
/* המשטחים: הכיתוב שהמשחק מצייר היום → הרשומה בחבילה */
const TCAL_SHOP={};for(const r of TCAL_ROWS)if(r[2]==='shops'&&r[0]!=='hotel'&&r[0]!=='rental')TCAL_SHOP[r[1]]=r[0];
const TCAL_AIR={'Sunbeak':'sunbeak','Aurelia Air':'aurelia','Skyline Regional':'skyline','Coral Coast':'coral','Tidewind Air':'tidewind','Zebrano':'zebrano','Mirage Jet':'mirage','Confetti Air':'confetti'};
const TCAL_AIR_NAME={};for(const nm in TCAL_AIR)TCAL_AIR_NAME[TCAL_AIR[nm]]=nm;
const TCAL_PLATE={'טרמינל טורבו סיטי':'terminal-east','טרמינל טורבו סיטי · יציאות':'terminal-west'};
const TCAL_S9={'מלון השדה':'hotel','השכרת רכב':'rental'};
/* לוחות הזהות בלי עיצוב בחבילה → הפס של סט 12 עם הלוגו המאושר */
const TCAL_BAND={'האנגר א׳':'airport','האנגר ב׳':'airport','האנגר ג׳':'airport','חוות הדלק':'airport','סדנת רכבי השירות':'airport','אגף השערים P1–P6':'airport',
 'כבאות והצלה — השדה':'fire','משטרה · מד״א':'police'};
const TCAL_S9B={'שער המטען':'airport','שער עובדים':'airport','מודיעין':'airport'};
const TCAL_BOX=[4800,700,9700,1800];   /* השדה (S15 / S16) — שלטי s9Sign מתחלפים רק כאן */
function tcalIn(x,y){return x>=TCAL_BOX[0]&&x<=TCAL_BOX[2]&&y>=TCAL_BOX[1]&&y<=TCAL_BOX[3]}
function tcalHeb(nm){try{const a=typeof S15GR_AL!=='undefined'&&S15GR_AL[nm];if(a)return a[0]}catch(e){}return nm}
/* הלוגו מטבלת המותגים (אותו צייר של 074n:tcbrSign) — contain בתוך המלבן */
function tcalLogo(key,c,x,y,w,h,fill){if(typeof TC_BRANDS==='undefined'||!TC_BRANDS[key]||!TC_BRANDS[key].parts||typeof TCB==='undefined')return false;const P=TC_BRANDS[key].parts.logo;
 let k=1;try{const m=c.getTransform();k=Math.hypot(m.a,m.b)||1}catch(e){}const s=Math.min(w/P.w,h/P.h),lw=P.w*s,lh=P.h*s;
 const e=TCB.pic('logo|'+key,P,TCB.bucket(Math.max(4,lw*k)),TCB.bucket(Math.max(4,lh*k)),'contain');c.drawImage(e.cv,x+(w-lw)/2,y+(h-lh)/2,lw,lh);return true}
/* הציור של המעצב (renderer.js), בלי שינוי חוץ מהלוגו והעברית — ראו tools/gen_airlogos.py */
const TCAL_D=(function(){const logo=tcalLogo;
/*@DRAW@*/
return{sign,emblem}})();
/* ספרייט לכל שלט (כמו 074x:s15jSignSprite — קנבס פנימי, נבנה פעם אחת) */
function tcalSpr(id,w,h,N,txt){w=Math.round(w*4)/4;h=Math.round(h*4)/4;const key=id+'|'+w+'|'+h+'|'+(N?1:0)+'|'+(txt||'');let o=TCAL.spr.get(key);if(o)return o;
 const m=Object.assign({},TCAL_BY[id]);if(!m.id)return null;/* שמות חברות התעופה — באנגלית, כמו בעולם (הבעלים 17.11 12:55) */if(m.group==='airlines')m.signText=TCAL_AIR_NAME[id]||m.name;if(txt)m.signText=txt;
 const sc=Math.max(3,Math.min(10,Math.round(48/h))),cv=document.createElement('canvas');cv.width=Math.max(1,Math.min(2048,Math.ceil(w*sc)));cv.height=Math.max(1,Math.ceil(h*sc));
 const g=cv.getContext('2d');g.scale(cv.width/w,cv.height/h);TCAL_D.sign(g,m,w,h,!!N);o={cv,w,h,id};TCAL.spr.set(key,o);TCAL.n.spr++;return o}
function tcalMark(what,id){TCAL.n[what]++;TCAL.seen[id]=(TCAL.seen[id]||0)+1}
/* (1) לוחות חברות התעופה מעל איי הצ׳ק-אין (074x:s15jTop קורא לכאן; false → הציור הישן) */
function tcalAirBoard(c,x,y,nm,N){const id=TCAL.on&&TCAL_AIR[nm];if(!id)return false;try{const s=tcalSpr(id,28,6,N);if(!s)return false;c.drawImage(s.cv,x-14,y-6,28,6);tcalMark('air',id);return true}catch(e){tcalErr(e);return false}}
/* (2) שלטי החנויות והמזנונים בטרמינל — אותו ספרייט, באותו רוחב שהמשחק מחשב */
if(typeof s15jSignSprite==='function'){const f=s15jSignSprite;s15jSignSprite=function(txt,kind,N){const id=TCAL.on&&TCAL_SHOP[txt];
 if(id){try{const o=f.apply(this,arguments),s=tcalSpr(id,o.w,o.h,N);if(s){tcalMark('shop',id);return s}}catch(e){tcalErr(e)}}return f.apply(this,arguments)};TCAL.n.hooks++}
/* (3) חזיתות הטרמינל (העיצוב של החבילה) ולוחות הזהות של המבנים (הפס של סט 12) — s15bPlate */
if(typeof s15bPlate==='function'){const f=s15bPlate;s15bPlate=function(c,t,x,y,px,bg,fg){const id=TCAL.on&&TCAL_PLATE[t],bk=TCAL.on&&TCAL_BAND[t];
 if(id||bk){try{c.font='800 '+px+'px Arial,Helvetica,sans-serif';const w=c.measureText(t).width+px*1.4,h=px*1.5,N=typeof s9Night==='function'&&s9Night();
  if(id){const s=tcalSpr(id,w,h,N);if(s){c.drawImage(s.cv,x-w/2,y-px*.75,w,h);tcalMark('plate',id);return}}
  else if(TC_BRANDS[bk]&&typeof tcs12Band==='function'){c.save();c.font='800 '+px+'px Arial,Helvetica,sans-serif';tcs12Band(c,bk,t,x-w/2-h/2,x+w/2+h/2,y-h/2,y+h/2,N);c.restore();tcalMark('band',bk+':'+t);return}}catch(e){tcalErr(e)}}
 return f.apply(this,arguments)};TCAL.n.hooks++}
/* (4) הצד היבשתי: מלון השדה וקיוסק ההשכרה (העיצוב של החבילה), שער המטען / העובדים / המודיעין (הפס של סט 12) — s9Sign, רק בשדה */
if(typeof s9Sign==='function'){const f=s9Sign;s9Sign=function(c,t,cx,cy,w,col,N){if(TCAL.on&&(TCAL_S9[t]||TCAL_S9B[t])&&tcalIn(cx,cy)){try{
  if(TCAL_S9[t]){const s=tcalSpr(TCAL_S9[t],w,11,N);if(s){c.fillStyle='rgba(0,0,0,.25)';c.fillRect(cx-w/2+1.5,cy-5.5+1.5,w,11);c.drawImage(s.cv,cx-w/2,cy-5.5,w,11);tcalMark('s9',TCAL_S9[t]);return}}
  else if(TC_BRANDS[TCAL_S9B[t]]&&typeof tcs12Band==='function'){tcs12Band(c,TCAL_S9B[t],t,cx-w/2,cx+w/2,cy-5.5,cy+5.5,N);tcalMark('band',TCAL_S9B[t]+':'+t);return}}catch(e){tcalErr(e)}}
 return f.apply(this,arguments)};TCAL.n.hooks++}
/* (5) המגדל: לוח זהות של נמל התעופה על הפיר (החבילה: "אין לוח זהות במגדל — הצעה") — מעל הציור הקיים (074k:s15bTower, 074q שקוף 60%) */
if(typeof s15bTower==='function'){const f=s15bTower;s15bTower=function(c,N){const r=f.apply(this,arguments);if(!TCAL.on)return r;try{
  const [x,y]=S15D.twr,K=typeof S15_K!=='undefined'?S15_K:.6,H0=K*100,H=K*240;if(!e3InView(x-80,y-H-110,160,H+130,10))return r;
  const B=TC_BRANDS.airport;if(!B)return r;const yc=y-H0-(H-H0)*.58,hw=20-8*.58-2.5,ph=hw*1.5;c.save();c.globalAlpha*=.9;
  c.fillStyle=B.deep;c.fillRect(x-hw,yc-ph/2,2*hw,ph);tcalLogo('airport',c,x-hw+.8,yc-ph/2+.8,2*hw-1.6,ph-2.6);c.fillStyle=B.accent;c.fillRect(x-hw,yc+ph/2-1.2,2*hw,1.2);
  if(N){c.globalCompositeOperation='lighter';c.fillStyle='rgba(255,236,190,.12)';c.fillRect(x-hw,yc-ph/2,2*hw,ph)}c.restore();tcalMark('tower','airport')}catch(e){tcalErr(e)}return r};TCAL.n.hooks++}
/* (6) מסכי השערים (44×14, ‏074k:s15grGate — וגם העטיפה של 074x3): מעל המסך — השלט של חברת התעופה של הטיסה הבאה מהשער (28×6, אותו עיצוב של הצ׳ק-אין) */
let TCAL_HEB2ID=null;function tcalIdOfHeb(h){if(!TCAL_HEB2ID){TCAL_HEB2ID={};try{for(const en in S15GR_AL)if(TCAL_AIR[en])TCAL_HEB2ID[S15GR_AL[en][0]]=TCAL_AIR[en]}catch(e){}}return TCAL_HEB2ID[h]||TCAL_AIR[h]||null}
if(typeof s15grGate==='function'){const f=s15grGate;s15grGate=function(c,b,rows){const r=f.apply(this,arguments);if(!TCAL.on||!rows)return r;try{const S=s15grBrStand(b);if(!S)return r;const x=S.T[0]*S.Sk,y=S.T[1]*S.Sk;if(!e3InView(x-40,y-80,80,90,10))return r;
  const q=(rows.dep||[]).find(r=>r.gate===b.stand)||(rows.arr||[]).find(r=>r.gate===b.stand),id=q&&tcalIdOfHeb(q.al);if(!id)return r;
  const yy=y-s15grK()*5.2*S15GR.PX,s=tcalSpr(id,28,6,typeof s9Night==='function'&&s9Night());if(!s)return r;c.drawImage(s.cv,x-14,yy-11-6.4,28,6);tcalMark('gate',id)}catch(e){tcalErr(e)}return r};TCAL.n.hooks++}
/* (7) הלוחות התפעוליים בשדה (019b:e4Plate — השערים, החניונים, ההסעה, מסוף הרכבת–אוויר): הכיתוב בלי שינוי; בקצה — אריח הלוגו המאושר
   (נמל התעופה; מסוף הרכבת–אוויר — הרכבת; ההשכרה — ההשכרה), באותו גובה של הלוח (16) */
const TCAL_E4K=t=>/רכבת–אוויר|רכבת-אוויר/.test(t)?'rail':/השכרת רכב/.test(t)?'rental':'airport';
if(typeof e4Plate==='function'){const f=e4Plate;e4Plate=function(txt,cx,cy,w){const r=f.apply(this,arguments);if(!TCAL.on||!tcalIn(cx,cy))return r;try{
  const c=ctx,t=typeof g77Heb==='function'?g77Heb(txt):txt;c.save();c.font='700 9.5px Segoe UI,Arial';const W=Math.max(w==null?92:w,c.measureText(t).width+14),k=TCAL_E4K(String(txt)),B=TC_BRANDS[k];
  if(B){const x0=cx+W/2+1;c.fillStyle=B.deep;c.fillRect(x0,cy-8,16,16);tcalLogo(k,c,x0+1,cy-7,14,14);c.strokeStyle='rgba(255,255,255,.55)';c.lineWidth=1;c.strokeRect(x0+.5,cy-7.5,15,15);tcalMark('e4',k)}c.restore()}catch(e){tcalErr(e)}return r};TCAL.n.hooks++}
/* (8) המטוסים (הבעלים 12:40: "חברות תעופה מגוונות… יש לוגואים לכל החברות"): הסמל של חברת התעופה מהחבילה (emblem 'airline') במקום הסימן
   הישן על הזנב — מלמעלה (013:logo, הספרייה של המטוסים) וב-3/4 (068:drawDecor, ‏decor.mark) — בצבע הסמל של הצבעים הקיימים (LIV, ‏lv.m).
   הצבעים והסגנון של הגוף — בלי שינוי (LIV של 013 — כבר הצבעים של החבילה, וריאנט 0). חברות המטען וה-GA — הסימן הישן (אין להן לוגו בחבילה). */
let TCAL_AL=null;function tcalAlId(n){if(!n)return null;if(TCAL_AIR[n])return TCAL_AIR[n];if(!TCAL_AL){TCAL_AL={};try{const H=window.__A34LIV&&window.__A34LIV.MK_HE;if(H)for(const en in H)if(TCAL_AIR[en])TCAL_AL[H[en]]=TCAL_AIR[en]}catch(e){}
 try{for(const en in S15GR_AL)if(TCAL_AIR[en])TCAL_AL[S15GR_AL[en][0]]=TCAL_AIR[en]}catch(e){}}return TCAL_AL[n]||null}
window.__TCAL_MARK=function(c,al,x,y,s,col){if(!TCAL.on)return false;const id=tcalAlId(al);if(!id||!(s>0))return false;try{c.save();const z=s*1.12;TCAL_D.emblem(c,'airline',x-z/2,y-z/2,z,col||'#ffffff',{id});c.restore();tcalMark('tail',id);return true}catch(e){try{c.restore()}catch(e2){}tcalErr(e);return false}};
/* הבדיקה */
window.__TC_AIRLOGOS={stats:()=>({on:TCAL.on,err:TCAL.err,n:Object.assign({},TCAL.n),seen:Object.assign({},TCAL.seen),rows:TCAL_ROWS.length,sprites:TCAL.spr.size}),
 audit:()=>{const R=[],push=(id,ok,det)=>R.push({id,ok:!!ok,det:String(det||'')});
  push('brands',typeof TC_BRANDS!=='undefined'&&TC_BRANDS.airport&&TC_BRANDS.rental&&TC_BRANDS.fire&&TC_BRANDS.police,'airport / rental / fire / police');
  for(const t in TCAL_SHOP){const id=TCAL_SHOP[t];let ok=false,det='';try{const s=tcalSpr(id,40,11,false);ok=!!(s&&s.cv.width>0);det=id}catch(e){det=String(e)}push('shop:'+t,ok,det)}
  for(const nm in TCAL_AIR){let ok=false,det='';try{const s=tcalSpr(TCAL_AIR[nm],28,6,false);ok=!!s;det=nm}catch(e){det=String(e)}push('air:'+nm,ok,det)}
  for(const t in TCAL_PLATE){let ok=false;try{ok=!!tcalSpr(TCAL_PLATE[t],170,19.5,false)}catch(e){}push('plate:'+t,ok,TCAL_PLATE[t])}
  for(const t in TCAL_S9){let ok=false;try{ok=!!tcalSpr(TCAL_S9[t],TCAL_S9[t]==='rental'?14:81.4,11,false)}catch(e){}push('s9:'+t,ok,TCAL_S9[t])}
  push('tailHook',typeof window.__TCAL_MARK==='function'&&tcalAlId('Sunbeak')==='sunbeak'&&tcalAlId(tcalHeb('Zebrano'))==='zebrano','');push('hooks',TCAL.n.hooks>=6,TCAL.n.hooks);push('err',!TCAL.err,TCAL.err||'');return{ok:R.every(r=>r.ok),n:R.length,fail:R.filter(r=>!r.ok)}},
 airlines:()=>{const L=window.__A34LIV,out=[];for(const en in TCAL_AIR){const id=TCAL_AIR[en],v=L?L.LIV.pax.filter(q=>q.n===en).map(q=>[q.b,q.s,q.t,q.m]):[];out.push({id,en,he:tcalHeb(en),sign:!!TCAL_BY[id],liveries:v.length,colors:v})}return out},
 sample:(id,w,h,N)=>{const s=tcalSpr(id,w||TCAL_BY[id].w,h||TCAL_BY[id].h,N);return s?{w:s.cv.width,h:s.cv.height}:null}};
