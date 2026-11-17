/* ==== SIGNS12 · סט 12 מהמעצב — "זהות ושילוט לכל העיר" (17.11.2026; ‏HANDOFF_NEXT שורה 39, ‏Review_part2 §F: F‑02, ‏F‑09, ‏F‑10) ====
   מצאתי (כלל 19): הכותרת של מסך המקום נקבעת ב-renderPhone (058) — לאפליקציה business: g7BrandName ← A6_POIS ← APT_INTERACTIONS ← 'עסקי C4',
   ו-g7Ui הופך את C4 ל"תעשייה קלה". כל מקום של E3 / E4 / E5 / הנמל / D4 / D5 / S15 / S16 שאין לו מותג ישן — קיבל "עסקי תעשייה קלה".
   placeMeta (029) לוקח את השם מהכותרת, את הסוג "עסק" ואת הלוגו — האות הראשונה (placeMono, "ע׳"). ‏074n (TCBR_BY_PLACE) מחבר את הלוגו החדש רק
   למקום הראשי של מותג ול-at שלו — לכן S16-RENT בלי הלוגו של rental (שמחובר ל-APT-RENT), ו-B2-KIOSK / E3-KIOSK על המותג הישן בלבד.
   מה כאן — שדרוג של הקיים (כלל 19א), בלי מנגנון חדש:
   (1) השם: אותו מקור כמו המפה והניווט — navPoiRegistry (039) לפי המזהה; אם אין — השם מהקטלוג של סט 12. רק כשהכותרת היא ברירת המחדל.
   (2) מסך המקום: placeMeta עטוף — הסוג (שם המותג / סוג המקום), הלוגו המאושר מטבלת המותגים (TC_BRANDS, אותו צייר TCB של 074n / econ)
       לכל מקום שהקטלוג של סט 12 מחבר למותג; למקום בלי מותג (תצפית, בית, שער) — הסימן של המקום בצבע מהקטלוג, והסוג שלו (לא "עסק").
   (3) הטבלה: TCS12_ROWS — 471 המקומות של הקטלוג: [מזהה, שם, מפתח מותג, צבע, סוג (אות הסיווג + אות התפקיד), מספר משטחי השלט שמופו].
   ציור בלבד ושם בלבד: שום דבר כאן לא כותב לסימולציה ולא לשמירה. אין תמונות (כלל 17). הבדיקה: window.__TC_SIGNS12. */
var TCS12={on:true,err:null,n:{title:0,meta:0,tcb:0,mono:0,name:0},reg:null,regT:0,nm:{}};
function tcs12Err(e){TCS12.err=TCS12.err||String(e&&e.stack||e).slice(0,300)}
const TCS12_ROWS=@@ROWS@@;
const TCS12_BY={};for(const r of TCS12_ROWS)TCS12_BY[r[0]]=r;
const TCS12_KIND={r:'מגורים',m:'נקודת עבודה',a:'פעילות בעיר',v:'תצפית על השדה',o:'שירות עירוני',h:'אזור בעיר',d:'אזור בעיר',P:'פארק ונוף',F:'חקלאות',W:'סדנה',T:'שירותים'};
const TCS12_GENERIC=new Set(['עסקי C4','עסקי תעשייה קלה','תעשייה כבדה C5','קריית הספורט A4','קמפוס ותרבות B5']);
function tcs12Reg(){const t=performance.now();if(!TCS12.reg||t-TCS12.regT>8000){try{TCS12.reg=navPoiRegistry()||{}}catch(e){tcs12Err(e);TCS12.reg=TCS12.reg||{}}TCS12.regT=t}return TCS12.reg}
/* the name of a place: the old brand, else the label of the navigation (the map and the missions use it), else the catalog of set 12 */
function tcs12Name(id){if(!id)return null;if(TCS12.nm[id]!==undefined)return TCS12.nm[id];let nm=null;
 try{nm=(typeof G7_SHOP_BRAND!=='undefined'&&G7_SHOP_BRAND[id]?.name)||null}catch(e){}
 if(!nm){try{const p=tcs12Reg()[id];if(p&&p.label)nm=String(p.label)}catch(e){tcs12Err(e)}}
 if(!nm&&TCS12_BY[id])nm=TCS12_BY[id][1];
 if(nm)TCS12.n.name++;return TCS12.nm[id]=nm}
function tcs12Kind(r,B,name,generic){if(B)return B.name&&B.name!==name?B.name:(B.kind||B.name);const c=r[4]||'';return TCS12_KIND[c[1]]||TCS12_KIND[c[0]]||'טורבו סיטי'}
/* (1) the title: only when it is the default of the app ('עסקי C4' and the like) */
if(typeof g7BrandTitle==='function'){const f=g7BrandTitle;g7BrandTitle=function(app){const r=f.apply(this,arguments);if(r||!TCS12.on)return r;
 try{const t=$('phoneTitle'),raw=t?String(t.textContent||'').trim():'';if(TCS12_GENERIC.has(raw)){const nm=tcs12Name(State.interactionId);if(nm){TCS12.n.title++;return nm}}}catch(e){tcs12Err(e)}return r}}
/* (2) the place's screen */
if(typeof placeMeta==='function'){const f=placeMeta;placeMeta=function(){const m=f.apply(this,arguments);try{const o=typeof PLACE!=='undefined'&&PLACE.on;
 if(!m||!o||!TCS12.on||(typeof PLACE_ID!=='undefined'&&PLACE_ID[o.id]))return m;const id=o.id,r=TCS12_BY[id],generic=((typeof PLACE_APP!=='undefined'&&(PLACE_APP[o.app]||PLACE_APP.business))||['עסק'])[0];
 if(!m.brand){const nm=tcs12Name(id);if(nm&&(!m.name||m.name===generic||TCS12_GENERIC.has(m.name)))m.name=nm}
 if(!r)return m;const k=r[2],B=k&&typeof TC_BRANDS!=='undefined'?TC_BRANDS[k]:null;
 if(B&&B.parts&&B.parts.logo&&!m.tcb){m.tcb=k;m.c1=B.deep||m.c1;m.c2=B.accent||m.c2;m.logo='';TCS12.n.tcb++}
 if(!m.brand){if(!m.kind||m.kind===generic)m.kind=tcs12Kind(r,B,m.name,generic);
  if(!B&&!m.tcb&&r[3]){m.c1=r[3];m.c2=plLum(r[3])>.5?'#13202b':'#f2e6c4';m.logo=placeMono(m.name,m.c1,m.c2);TCS12.n.mono++}}
 m.s12=id;TCS12.n.meta++}catch(e){tcs12Err(e)}return m}}
window.__TC_SIGNS12={TCS12,rows:TCS12_ROWS,by:TCS12_BY,name:tcs12Name,
 stats:()=>({n:TCS12.n,err:TCS12.err,rows:TCS12_ROWS.length,brands:TCS12_ROWS.filter(r=>r[2]&&typeof TC_BRANDS!=='undefined'&&TC_BRANDS[r[2]]).length}),
 /* for every id: the name it gets, from where, and the brand of the logo */
 audit:(ids)=>{const reg=tcs12Reg(),out=[];for(const id of ids||TCS12_ROWS.map(r=>r[0])){const r=TCS12_BY[id],g=(typeof G7_SHOP_BRAND!=='undefined'&&G7_SHOP_BRAND[id])||null;
  out.push({id,name:tcs12Name(id),from:g?'g7':reg[id]?.label?'nav':r?'s12':'none',brand:r&&r[2]&&typeof TC_BRANDS!=='undefined'&&TC_BRANDS[r[2]]?r[2]:(g?'g7:'+g.b:null)})}return out}};
/* ---- (4) שלב 2: שלט לכל חזית — המשטחים שהמעצב מיפה בסט 12 (catalog.js, ‏face_NN) ----
   מצאתי: s9Sign (019b — "שלט על הפאה": פס בצבע של הקו, עיגול הסמל של העיר והשם) מצייר את שלטי הזהות של E4 / E5 / E6 / C6 / D6 / A6 / האי;
   ‏074n מחליף ב-tcbrSign רק 2 + 20 כיתובים (TCBR_S9). כאן — עוד הכיתובים שהקטלוג מחבר למותג אחד: אותו פס, באותו מקום ובאותו גודל, בצבע
   של המותג, עם הלוגו המאושר מימין (tcbrTile, הצייר של 074n) ואותו כיתוב מקומי משמאל — "הכיתוב המקומי מותאם למקום" (הערת המעצב). בלילה —
   כמו s9Sign: הפס מואר. ובציורי BLD40 — שלושה כיתובים שהם שם המותג עצמו (ארגז הכלים, דלק טורבו, משטרה) → המנגנון של 074n (TCBR_SIGN_TEXT). */
const TCS12_FACE=@@FACES@@;
function tcs12Band(c,key,t,x0,x1,yt,yb,N){const B=TC_BRANDS[key],h=yb-yt,w=x1-x0,s=h*.84;c.save();
 c.fillStyle='rgba(0,0,0,.25)';c.fillRect(x0+1.2,yt+1.2,w,h);c.fillStyle=N?plMix(B.deep,'#ffffff',.2):B.deep;c.fillRect(x0,yt,w,h);
 const ah=Math.max(.5,h*.08);c.fillStyle=B.accent;c.fillRect(x0,yb-ah,w,ah);
 {const cx=x1-h/2,cy=(yt+yb)/2-ah/2,r=s/2+.8;c.fillStyle=B.light||'#f4f1e8';c.beginPath();if(c.roundRect)c.roundRect(cx-r,cy-r,2*r,2*r,r*.3);else c.rect(cx-r,cy-r,2*r,2*r);c.fill();tcbrTile(c,key,cx,cy,s)}   /* the logo on a light square, as the round mark of s9Sign */
 const tw=w-h-3,tx=x0+1.5+tw/2,ty=(yt+yb)/2+.4,px=h*.62;
 if(typeof s9Txt==='function')s9Txt(c,t,tx,ty,px,'#fff',tw);else{c.font='700 '+px+'px Arial,sans-serif';c.textAlign='center';c.textBaseline='middle';c.fillStyle='#fff';c.fillText(t,tx,ty,tw)}
 c.strokeStyle='rgba(255,255,255,.6)';c.lineWidth=.6;c.strokeRect(x0+.3,yt+.3,w-.6,h-.6);
 if(N){c.globalCompositeOperation='lighter';c.fillStyle='rgba(255,236,190,.14)';c.fillRect(x0-1,yt-1,w+2,h+2)}
 c.restore();TCS12.n.band=(TCS12.n.band||0)+1;try{tcbrMark(key,'sign')}catch(e){}}
if(typeof s9Sign==='function'&&typeof TC_BRANDS!=='undefined'&&typeof tcbrTile==='function'){const f=s9Sign;s9Sign=function(c,t,cx,cy,w,col,N){
 const k=TCS12.on&&TCS12_FACE.s9[t];if(k&&TC_BRANDS[k]&&!(typeof TCBR_S9!=='undefined'&&TCBR_S9[t])){try{tcs12Band(c,k,t,cx-w/2,cx+w/2,cy-5.5,cy+5.5,N);return}catch(e){tcs12Err(e)}}return f.apply(this,arguments)};TCS12.n.hookS9=1}
if(typeof TCBR_SIGN_TEXT!=='undefined'){let n=0;for(const t in TCS12_FACE.bld)if(!TCBR_SIGN_TEXT[t]&&TC_BRANDS[TCS12_FACE.bld[t]]){TCBR_SIGN_TEXT[t]=TCS12_FACE.bld[t];n++}
 if(n){TCS12.n.bld=n;try{if(typeof BLD40!=='undefined'&&BLD40&&BLD40.clear)BLD40.clear()}catch(e){tcs12Err(e)}}}
window.__TC_SIGNS12.faces=TCS12_FACE;
