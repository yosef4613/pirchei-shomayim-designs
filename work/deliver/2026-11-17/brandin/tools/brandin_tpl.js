/* ==== BRANDIN · מה שבעל הבית סימן "טוב — לשמור" נכנס למשחק (17.11.2026, הבעלים ~17:20; owner_marks_1117.json) ====
   מצאתי (כלל 19): הציור של המעצב לשילוט התפעולי של השדה (set7_share/airport-ops/renderer.js, ‏89 משטחים) ולזהויות ולשלטים של העיר
   (city-signs/renderer.js) — לא במשחק. המשחק מצייר באותם משטחים את הציור הישן שלו: השלטים התלויים בטרמינל (074x:s15jSignSprite), לוחות
   הטיסות (074k:s15grBoard), מסכי השערים (074k:s15grGate), שלטי המסלול (074k:s15bProps ← 019m:s15T), לוחות הזהות של המבנים (074k:s15bPlate),
   הלוחות התפעוליים (019b:e4Plate), שלטי הצד היבשתי (019b:s9Sign), סימני ה-P (074v_S16d:s16pP), הדלפקים ולוח התדריך (074x:s15jText);
   ובעיר — שלטי החזית של C2 / D2 (060:c2Sign, ‏019:d2Sign), s9Sign ו-e4Plate; ובמסך המקום (F) — הלוגו של המותג בלבד (074v_econ:placeApply).
   מה כאן — שדרוג של הקיים (כלל 19א): אותם משטחים, באותו מקום ובאותו גודל; הציור — של המעצב כמו שהוא (הקוד שלו, למטה, בלי שינוי חוץ
   מהטעינה / הייצוא שהוסרו ושורת חיבור אחת ללוגו), והלוגואים — מטבלת המותגים האחת (TC_BRANDS, הצייר TCB). רק פריטים שסומנו keep.
   פריט redo — לא נוגעים (הציור שלו נשאר כמו שהוא). שלטי airlogos (074v_airlogos — redo) נשארים במשחק כזמניים.
   מקום בלי משטח שלט (הצעה 120×24): לפי D‑631 לא מוסיפים שלט חדש על מבנה — ההצעה מוצגת במסך המקום (F), מתחת לכותרת. הזהות המקומית
   (900×600) — הלוגו של מסך המקום. ציור בלבד: שום דבר כאן לא כותב לסימולציה ולא לשמירה. אין תמונות (כלל 17).
   נוצר בכלי deliver/2026-11-17/brandin/tools/gen_brandin.py. הבדיקה: window.__TC_BRANDIN (stats, audit, keep). */
var TCBI={on:true,okToo:false,err:null,n:{way:0,fids:0,gate:0,rwy:0,plate:0,s9:0,e4:0,p:0,counter:0,brief:0,c2:0,d2:0,b4:0,f:0,prop:0,spr:0,hooks:0},spr:new Map(),seen:{},fail:[]};
function tcbiErr(e,w){const s=(w?w+': ':'')+String(e&&e.stack||e).slice(0,300);TCBI.err=TCBI.err||s;if(TCBI.fail.length<40)TCBI.fail.push(s)}
const TCBI_R={document:typeof document!=='undefined'?document:undefined};
/* הטבלאות (רק מה שסומן keep): השילוט התפעולי של השדה, והזהויות / השלטים של העיר */
TCBI_R.TC_AIRPORT_OPS_CATALOG=/*@OPS@*/;
TCBI_R.TC_CITY_CATALOG=/*@CITY@*/;
const TCBI_KEYS=/*@KEYS@*/;
function TCBI_LIBN(k){try{const a={restaurant:'table',pharmacy:'vine',bank:'bay'}[k]||k;return typeof TC_BRANDS!=='undefined'&&TC_BRANDS[a]&&TC_BRANDS[a].name||null}catch(e){return null}}
/* מה שהמשחק כבר יודע על המקום (074v_signs12: TCS12_ROWS — השם, המותג, הצבע) לא נכתב כאן שוב — משלימים ממנו */
for(const m of TCBI_R.TC_CITY_CATALOG){const r=typeof TCS12_BY!=='undefined'&&TCS12_BY[m.placeId];if(m.name==null)m.name=r?r[1]:m.placeId;
 if(m.bk12)m.brandKey=r&&r[2]||null;else if(typeof m.brandKey==='number')m.brandKey=TCBI_KEYS[m.brandKey];if(m.color==null)m.color=r&&r[3]||'#30474d';if(m.role==null)m.role='city';
 if(m.brandName==null){const b=m.bnB&&m.brandKey&&TCBI_LIBN(m.brandKey);m.brandName=b||m.name}for(const k in m.formats){const f=m.formats[k];if(f.text==null&&k!=='logo')f.text=m.name}}
const TCBI_ALIAS=/*@ALIAS@*/;
const TCBI_KEEP=/*@KEEP@*/;
/* המותגים: הקוד של המעצב קורא ל-root.TURBO_CITY_BRANDS[key].parts.logo — כאן אותו לוגו מטבלת המותגים של המשחק (TCB, ‏074m) */
function tcbiBK(k){if(typeof TC_BRANDS==='undefined'||!k)return null;if(TC_BRANDS[k]&&TC_BRANDS[k].parts&&TC_BRANDS[k].parts.logo)return k;const a=TCBI_ALIAS[k];return a&&TC_BRANDS[a]&&TC_BRANDS[a].parts&&TC_BRANDS[a].parts.logo?a:null}
function tcbiLogoDraw(key,c,x,y,w,h){const P=TC_BRANDS[key].parts.logo;let k=1;try{const m=c.getTransform();k=Math.hypot(m.a,m.b)||1}catch(e){}
 const e=TCB.pic('logo|'+key,P,TCB.bucket(Math.max(4,w*k)),TCB.bucket(Math.max(4,h*k)),'contain');c.drawImage(e.cv,x,y,w,h)}
TCBI_R.TURBO_CITY_BRANDS={};
(function(){if(typeof TC_BRANDS==='undefined')return;const keys=new Set(Object.keys(TC_BRANDS).concat(Object.keys(TCBI_ALIAS)));
 for(const k of keys){const g=tcbiBK(k);if(!g)continue;const P=TC_BRANDS[g].parts.logo,s=Math.min(1,320/Math.max(P.w,P.h)),lw=Math.max(8,Math.round(P.w*s)),lh=Math.max(8,Math.round(P.h*s));
  const lg={w:lw,h:lh,__draw:(c,x,y,w,h)=>tcbiLogoDraw(g,c,x,y,w,h)};TCBI_R.TURBO_CITY_BRANDS[k]={key:k,name:TC_BRANDS[g].name,parts:{logo:lg},draw:(c,f,x,y,w,h)=>lg.__draw(c,x,y,w,h)}}})();
/* ---- הקוד של המעצב (set7_share), root = TCBI_R ---- */
/*@FAVICON@*/
/*@OPSR@*/
/*@CITYR@*/
/* ---- ספרייט לכל שלט (קנבס פנימי, נבנה פעם אחת לכל מידה / לילה / נתונים — כמו 074x:s15jSignSprite) ---- */
/* בזמן הציור של הספרייט — בלי ההחלפות של ציור הבניין (074n / 074n3 / כאן): הקנבס הפנימי הוא של המעצב בלבד */
function tcbiSpr(api,id,fmt,w,h,N,data,dk){w=Math.round(w*4)/4;h=Math.round(h*4)/4;const key=api+'|'+id+'|'+fmt+'|'+w+'|'+h+'|'+(N?1:0)+'|'+(dk||'');let o=TCBI.spr.get(key);if(o)return o;
 const b4=typeof TCBR!=='undefined'?TCBR.inB4:false,mk=typeof TCPO!=='undefined'?TCPO.mk:null;TCBI.inSpr=true;try{if(typeof TCBR!=='undefined')TCBR.inB4=false;if(typeof TCPO!=='undefined')TCPO.mk=null;o=tcbiSpr0(api,id,fmt,w,h,N,data,key)}
 finally{TCBI.inSpr=false;if(typeof TCBR!=='undefined')TCBR.inB4=b4;if(typeof TCPO!=='undefined')TCPO.mk=mk}return o}
function tcbiSprMem(cv){TCBI.sprB=(TCBI.sprB||0)+cv.width*cv.height*4;if(TCBI.sprB>24*1048576||TCBI.spr.size>700){TCBI.spr.clear();TCBI.sprB=cv.width*cv.height*4;TCBI.n.sprClear=(TCBI.n.sprClear||0)+1}}
function tcbiSpr0(api,id,fmt,w,h,N,data,key){let o;const sc=Math.max(3,Math.min(10,Math.round(64/h))),cv=document.createElement('canvas');cv.width=Math.max(1,Math.min(2048,Math.ceil(w*sc)));cv.height=Math.max(1,Math.min(1024,Math.ceil(h*sc)));
 const g=cv.getContext('2d');(api==='ops'?TCBI_R.TC_AIRPORT_OPS:TCBI_R.TC_CITY).draw(g,id,fmt,0,0,cv.width,cv.height,{night:!!N,data:data||undefined});tcbiSprMem(cv);o={cv,w,h,id};TCBI.spr.set(key,o);TCBI.n.spr++;return o}
function tcbiMark(what,id){TCBI.n[what]++;TCBI.seen[id]=(TCBI.seen[id]||0)+1}
function tcbiNight(){try{return typeof s9Night==='function'&&!!s9Night()}catch(e){return false}}
const TCBI_OPS={};for(const m of TCBI_R.TC_AIRPORT_OPS_CATALOG)TCBI_OPS[m.id]=m;
const tcbiNorm=t=>String(t==null?'':t).replace(/[‎‏⁦-⁩‪-‮]/g,'').replace(/\s+/g,' ').trim();
/* הכיתוב שהמשחק מצייר היום → המשטח בחבילה, לכל משפחה */
const TCBI_BY={};for(const m of TCBI_R.TC_AIRPORT_OPS_CATALOG){const f=m.family,t=tcbiNorm(m.sourceText);(TCBI_BY[f]||(TCBI_BY[f]={}))[t]=TCBI_BY[f][t]||m.id;
 if(m.source&&m.source.night_text)TCBI_BY[f][tcbiNorm(m.source.night_text)]=TCBI_BY[f][tcbiNorm(m.source.night_text)]||m.id}
function tcbiOps(fam,t){const B=TCBI_BY[fam];if(!B||!TCBI.on)return null;const id=B[tcbiNorm(t)];if(id)return id;if(fam==='operational_e4_plate'&&/^חניון ארוך · פנויים/.test(tcbiNorm(t))&&TCBI_OPS['S16P-FREE'])return 'S16P-FREE';return null}
const TCBI_BOX=[4800,-600,9800,1800];function tcbiInAir(x,y){return x>=TCBI_BOX[0]&&x<=TCBI_BOX[2]&&y>=TCBI_BOX[1]&&y<=TCBI_BOX[3]}
/* העיר: הכיתוב של משטח (s9Sign / e4Plate) → [מזהה בקטלוג, הפורמט]; ו-c2Sign / d2Sign — לפי המקום של המותג (G7_SHOP_BRAND) */
const TCBI_CT={s9:{},e4:{},c2:{},d2:{},b4:{},mq:{}};const TCBI_CITY={};
for(const m of TCBI_R.TC_CITY_CATALOG){TCBI_CITY[m.id]=m;for(const k in m.formats){const f=m.formats[k];if(!f.src)continue;const ty=f.src;if(!TCBI_CT[ty])continue;if(f.ok&&!TCBI.okToo)continue;
 if(ty==='b4'||ty==='mq')TCBI_CT.b4[m.placeId+'|'+tcbiNorm(f.text)]=TCBI_CT.b4[m.placeId+'|'+tcbiNorm(f.text)]||[m.id,k];else if(ty==='c2'||ty==='d2')TCBI_CT[ty][m.placeId]=TCBI_CT[ty][m.placeId]||[m.id,k];else TCBI_CT[ty][tcbiNorm(f.text)]=TCBI_CT[ty][tcbiNorm(f.text)]||[m.id,k]}}
let TCBI_G7P=null;function tcbiPidOfG7(k){if(!TCBI_G7P){TCBI_G7P={};try{for(const p in G7_SHOP_BRAND){const b=G7_SHOP_BRAND[p].b;if(!TCBI_G7P[b])TCBI_G7P[b]=p}}catch(e){}}return TCBI_G7P[k]||null}
const TCBI_PLACE={};for(const m of TCBI_R.TC_CITY_CATALOG)if(m.placeId&&(m.formats.logo||m.formats.proposal))TCBI_PLACE[m.placeId]=TCBI_PLACE[m.placeId]||m.id;
function tcbiCityDraw(c,ty,key,x,y,w,h,N,what){const r=TCBI.on&&TCBI_CT[ty][key];if(!r)return false;try{const s=tcbiSpr('city',r[0],r[1],w,h,N);c.drawImage(s.cv,x,y,w,h);tcbiMark(what,r[0]+':'+r[1]);return true}catch(e){tcbiErr(e,what);return false}}

/* (1) השלטים התלויים בטרמינל (23) — אותו ספרייט, באותו גודל */
if(typeof s15jSignSprite==='function'){const f=s15jSignSprite;s15jSignSprite=function(txt,kind,N){const id=tcbiOps('terminal_hanging',txt);
 if(id){try{const M=TCBI_OPS[id].formats.sign,s=tcbiSpr('ops',id,'sign',M.w,M.h,N);tcbiMark('way',id);return s}catch(e){tcbiErr(e,'way')}}return f.apply(this,arguments)};TCBI.n.hooks++}
/* (2) לוחות הטיסות בפנים (11) — המסגרת של המעצב באותו מלבן, עם הנתונים החיים של הלוח (S15GR) */
function tcbiRow(q){if(!q)return null;let st='';try{st=(S15GR_ST[q.st]||S15GR_ST.ontime)[0]}catch(e){}let tm='';try{tm=s15grHM(q.m)}catch(e){}return{time:tm,flight:q.code,destination:q.city,gate:q.gate,status:st}}
/*    הלוחות הגדולים (יציאות · נחיתות, יציאות ×2, נחיתות): המסגרת של המעצב מציגה 2 טיסות לכל רשימה, והלוח של היום (074x3) — עד 8; כדי לא לאבד טיסות
      (הבעלים: "הרבה יותר טיסות") הם נשארים כמו שהם — לאישורך (TCBI.bigFids=true מחליף גם אותם). לוחות השער / הסרט / ההסעה (טיסה אחת) — של המעצב. */
const TCBI_BIG=new Set(['S15J-FIDS-01','S15J-FIDS-09','S15J-FIDS-10','S15J-FIDS-11']);TCBI.bigFids=false;
if(typeof s15grBoard==='function'){const f=s15grBoard;s15grBoard=function(c,x,y,Wb,Hb,z,rows,title){const id=title&&tcbiOps('interior_fids',title);if(!id||(TCBI_BIG.has(id)&&!TCBI.bigFids))return f.apply(this,arguments);
 try{const r=f.call(this,c,x,y,Wb,Hb,z,rows,null),K=s15grK(),X=S15GR.PX,y0=y-K*z*X-Hb,x0=x-Wb/2,dep=(rows&&rows.dep||[]).slice(0,2).map(tcbiRow),arr=(rows&&rows.arr||[]).slice(0,2).map(tcbiRow);
  const data={departures:dep,arrivals:arr,rows:dep.length?dep:arr,flight:dep[0]||arr[0]||null},s=tcbiSpr('ops',id,'sign',Wb,Hb,tcbiNight(),data,JSON.stringify(data));c.drawImage(s.cv,x0,y0,Wb,Hb);tcbiMark('fids',id);return r}
 catch(e){tcbiErr(e,'fids');return f.apply(this,arguments)}};TCBI.n.hooks++}
/* (3) מסכי השערים על השרוולים (6) — באותו מלבן (44×14; עם הלוח של 074x3 — ‏48×16); השלט של חברת התעופה מעליו (airlogos, זמני) נשאר */
if(typeof s15grGate==='function'){const f=s15grGate;s15grGate=function(c,b,rows){const r=f.apply(this,arguments);try{const id=b&&tcbiOps('bridge_gate_screen','שער '+b.stand);if(!id)return r;
  const S=s15grBrStand(b);if(!S)return r;const x=S.T[0]*S.Sk,y=S.T[1]*S.Sk;if(!e3InView(x-40,y-80,80,90,10))return r;const yy=y-s15grK()*5.2*S15GR.PX;
  const q=rows&&((rows.dep||[]).find(r=>r.gate===b.stand)||(rows.arr||[]).find(r=>r.gate===b.stand)),data={flight:tcbiRow(q)},s=tcbiSpr('ops',id,'sign',44,14,tcbiNight(),data,JSON.stringify(data));
  const px=typeof S15PAX!=='undefined'&&S15PAX.on&&S15PAX.board;if(px)c.drawImage(s.cv,x-24,yy-11,48,16);else c.drawImage(s.cv,x-22,yy-11,44,14);tcbiMark('gate',id)}catch(e){tcbiErr(e,'gate')}return r};TCBI.n.hooks++}
/* (4) שלטי המסלול והמסלולונים (17) — s15bProps מצייר אותם עם s15T (גופן 14): הלוח של המעצב במקום הרקע והכיתוב (18 + 12 לכל אות × 20) */
if(typeof s15T==='function'){const f=s15T;s15T=function(c,t,x,y,px,col,w,rot){if(px===14&&!rot){const id=tcbiOps('runway_taxiway',t);if(id){try{const W=18+String(t).length*12,s=tcbiSpr('ops',id,'sign',W,20,tcbiNight());
  c.drawImage(s.cv,x-W/2,y-11,W,20);tcbiMark('rwy',id);return}catch(e){tcbiErr(e,'rwy')}}}return f.apply(this,arguments)};TCBI.n.hooks++}
/* (5) לוחות הזהות של המבנים בשדה (11) — אותו מלבן של s15bPlate */
if(typeof s15bPlate==='function'){const f=s15bPlate;s15bPlate=function(c,t,x,y,px){const id=tcbiOps('building_plate',t);if(id){try{c.font='800 '+px+'px Arial,Helvetica,sans-serif';const w=c.measureText(t).width+px*1.4,h=px*1.5,s=tcbiSpr('ops',id,'sign',w,h,tcbiNight());
  c.drawImage(s.cv,x-w/2,y-px*.75,w,h);tcbiMark('plate',id);return}catch(e){tcbiErr(e,'plate')}}return f.apply(this,arguments)};TCBI.n.hooks++}
/* (6) s9Sign: שלטי הצד היבשתי של השדה (3) — ובעיר: המשטחים של הקטלוג שעוד לא במשחק */
if(typeof s9Sign==='function'){const f=s9Sign;s9Sign=function(c,t,cx,cy,w,col,N){try{const id=tcbiInAir(cx,cy)&&tcbiOps('landside_building_sign',t);
  if(id){const s=tcbiSpr('ops',id,'sign',w,11,N);c.drawImage(s.cv,cx-w/2,cy-5.5,w,11);tcbiMark('s9',id);return}
  if(tcbiCityDraw(c,'s9',tcbiNorm(t),cx-w/2,cy-5.5,w,11,N,'s9'))return}catch(e){tcbiErr(e,'s9')}return f.apply(this,arguments)};TCBI.n.hooks++}
/* (7) הלוחות התפעוליים (e4Plate): בשדה (11) — הלוח של המעצב באותו מלבן (בלי האריח של airlogos — העיצוב המלא מחליף אותו); בעיר — לוחות המתקנים */
if(typeof e4Plate==='function'){const f=e4Plate;e4Plate=function(txt,cx,cy,w){try{const c=ctx,air=tcbiInAir(cx,cy),id=air&&tcbiOps('operational_e4_plate',txt),cr=!id&&TCBI.on&&TCBI_CT.e4[tcbiNorm(txt)];
  if(id||cr){const t=typeof g77Heb==='function'?g77Heb(txt):txt;c.save();c.font='700 9.5px Segoe UI,Arial';const W=Math.max(w==null?92:w,c.measureText(t).width+14);c.restore();const N=tcbiNight();
   if(id){let data;if(id==='S16P-FREE'){const a=(tcbiNorm(txt).match(/\d+/g)||[]).slice(-3).map(Number);data={free:a}}const s=tcbiSpr('ops',id,'sign',W,16,N,data,data?a2s(data):'');c.drawImage(s.cv,cx-W/2,cy-8,W,16);tcbiMark('e4',id);return}
   if(tcbiCityDraw(c,'e4',tcbiNorm(txt),cx-W/2,cy-8,W,16,N,'e4'))return}}catch(e){tcbiErr(e,'e4')}return f.apply(this,arguments)};TCBI.n.hooks++}
function a2s(d){try{return JSON.stringify(d)}catch(e){return ''}}
/* (8) סימני ה-P של החניונים (3) */
if(typeof s16pP==='function'){const f=s16pP;s16pP=function(c,x,y,s){if(TCBI.on&&TCBI_OPS['S16P-P-ENTRY']){try{const id=s>=18?'S16P-P-ROOF':s<=12?'S16P-P-STAFF':'S16P-P-ENTRY',m=TCBI_OPS[id]?id:'S16P-P-ENTRY',sp=tcbiSpr('ops',m,'sign',s,s,tcbiNight());
  c.drawImage(sp.cv,x-s/2,y-s/2,s,s);tcbiMark('p',m);return}catch(e){tcbiErr(e,'p')}}return f.apply(this,arguments)};TCBI.n.hooks++}
/* (9) הדלפקים (3, תווית מוצעת — על חזית הדלפק, בגובה הכיתוב הקיים) ולוח התדריך של הצוות (58×10) — s15jText בציור הפנים של הטרמינל */
if(typeof s15jText==='function'){const f=s15jText;s15jText=function(g,t,x,y,px,col,w){if(TCBI.on){try{
  if(px===4.5){const id=tcbiOps('counter_label',t);if(id){const h=6.6,W=Math.min(h*120/18,44),s=tcbiSpr('ops',id,'sign',W,h,tcbiNight());g.drawImage(s.cv,x-W/2,y-h/2,W,h);tcbiMark('counter',id);return}}
  if(px===3.6){const id=tcbiOps('crew_briefing_board',t);if(id){const s=tcbiSpr('ops',id,'sign',58,10,tcbiNight());g.drawImage(s.cv,x-29,y+3,58,10);tcbiMark('brief',id);return}}}catch(e){tcbiErr(e,'s15jText')}}
 return f.apply(this,arguments)};TCBI.n.hooks++}
/* (10) העיר — שלטי החזית של C2 ו-D2 (לפי המותג של המקום): הלוח של המעצב באותו מלבן */
if(typeof c2Sign==='function'){const f=c2Sign;c2Sign=function(c,key,x0,x1,yt,yb,N){const p=tcbiPidOfG7(key);if(p&&tcbiCityDraw(c,'c2',p,x0,yt,x1-x0,yb-yt,N,'c2'))return;return f.apply(this,arguments)};TCBI.n.hooks++}
if(typeof d2Sign==='function'){const f=d2Sign;d2Sign=function(c,k,x0,x1,yt,yb,N){const p=tcbiPidOfG7(k);if(p&&tcbiCityDraw(c,'d2',p,x0,yt,x1-x0,yb-yt,N,'d2'))return;return f.apply(this,arguments)};TCBI.n.hooks++}
/* (10ב) העיר — שלטים בתוך ציור הבניין (BLD40: השוק, בית החולים, המחסנים, המרקיזה של התיאטרון): הכיתוב נכתב בקנבס של הבניין (fillText, כמו המנגנון
   של 074n / 074n3) — כאן, רק בסוג הבניין של מקום keep (לפי המקום הקרוב ב-BLD40.draw), הלוח של המעצב במידה שלו, על אותה נקודת עיגון */
const TCBI_B4T={},TCBI_B4P=[];let TCBI_B4R=0;
/* המקום של כל בניין BLD40 (המערכים של הבניינים — כמו 074n3:tcpoPlace): הסוג והסיבוב → המקום */
const TCBI_B4POS={};
function tcbiB4Scan(){const want=new Set(Object.keys(TCBI_CT.b4).map(k=>k.split('|')[0]));for(const f of [()=>B4_BUILDINGS,()=>C4_BUILDINGS,()=>B5_BUILDINGS,()=>A2_BLD,()=>C5N_BLD,()=>C5_BUILDINGS,()=>A4_BUILDINGS])
 {let A=null;try{A=f()}catch(e){}if(!Array.isArray(A))continue;for(const o of A){const b=o&&o.bld40;if(!b||!want.has(o.id))continue;const k=b.type+'|'+(b.rot|0);if(!TCBI_B4T[k])TCBI_B4T[k]=o.id;if(!TCBI_B4T[b.type])TCBI_B4T[b.type]=o.id;TCBI_B4POS[o.id]=[o.x,o.drawY!=null?o.drawY:o.y]}}}
try{tcbiB4Scan()}catch(e){tcbiErr(e,'b4scan')}
function tcbiB4Places(){if(TCBI_B4P.length||TCBI_B4R++>3)return TCBI_B4P;try{tcbiB4Scan()}catch(e){}try{const reg=navPoiRegistry()||{},seen=new Set();for(const k in TCBI_CT.b4){const pid=k.split('|')[0];if(seen.has(pid))continue;seen.add(pid);const q=reg[pid];if(q&&q.x!=null)TCBI_B4P.push([pid,q.x,q.y])}}catch(e){tcbiErr(e,'b4reg')}return TCBI_B4P}
if(typeof BLD40!=='undefined'&&BLD40&&typeof BLD40.draw==='function'&&typeof HTMLCanvasElement!=='undefined'){
 const dr=BLD40.draw;BLD40.draw=function(c,x,y,id,rot){try{if(TCBI.on){const k=id+'|'+(rot|0);if(!TCBI_B4T[k]){let best=null,bd=260;for(const q of tcbiB4Places()){const d=Math.hypot(q[1]-x,q[2]-y);if(d<bd){bd=d;best=q[0]}}
   if(best){const had=TCBI_B4T[k]===null;TCBI_B4T[k]=best;TCBI_B4T[id]=TCBI_B4T[id]||best;if(had&&BLD40.clear)BLD40.clear()}else if(TCBI_B4T[k]===undefined)TCBI_B4T[k]=null}}}catch(e){tcbiErr(e,'b4map')}return dr.apply(this,arguments)};
 for(const C of [HTMLCanvasElement,typeof OffscreenCanvas!=='undefined'?OffscreenCanvas:null]){if(!C)continue;const gc0=C.prototype.getContext;
  C.prototype.getContext=function(t){const g=gc0.apply(this,arguments);if(g&&t==='2d'&&!g.__tcbi&&typeof TCBR!=='undefined'&&TCBR.inB4){g.__tcbi=1;const ft=g.fillText;
   g.fillText=function(tx,x,y){if(TCBI.inSpr)return ft.apply(this,arguments);try{const mk=TCBR.b4mk,pid=TCBI.on&&mk&&(TCBI_B4T[mk[0]+'|'+((mk[1]|0))]||TCBI_B4T[mk[0]]),r=pid&&TCBI_CT.b4[pid+'|'+tcbiNorm(tx)];
    if(r){const f=TCBI_CITY[r[0]].formats[r[1]],w=f.w,h=f.h,al=this.textAlign,bl=this.textBaseline,cx=al==='center'?x:(al==='right'||al==='end')?x-w/2:x+w/2,cy=bl==='middle'?y:bl==='top'?y+h/2:y-h*.3;
     let data;if(f.kind==='dynamic_marquee'){try{const i=tcpoTonight(),P=i>=0?TCSHOW.PLAYS[i]:null;if(P)data={title:'הערב: '+P.name}}catch(e){}}
     const s=tcbiSpr('city',r[0],r[1],w,h,false,data,data?data.title:'');this.drawImage(s.cv,cx-w/2,cy-h/2,w,h);tcbiMark('b4',r[0]+':'+r[1]);return}}catch(e){tcbiErr(e,'b4')}return ft.apply(this,arguments)}}return g}}
 try{if(BLD40.clear)BLD40.clear()}catch(e){}TCBI.n.hooks++}
/* (11) מסך המקום (F): הזהות המקומית של המעצב (900×600) במקום הלוגו, וההצעה לשלט (120×24) מתחת לכותרת — למקום שסומן keep */
function tcbiPlaceCv(cv,id,fmt,cw,ch){const d=Math.min(2,window.devicePixelRatio||1);cv.width=Math.round(cw*d);cv.height=Math.round(ch*d);cv.style.width=cw+'px';cv.style.height=ch+'px';
 const g=cv.getContext('2d');TCBI_R.TC_CITY.draw(g,id,fmt,0,0,cv.width,cv.height,{night:false});cv.dataset.tcbi=id+':'+fmt}
if(typeof placeApply==='function'){const f=placeApply;placeApply=function(){const r=f.apply(this,arguments);try{const hd=$('placeHead');if(!TCBI.on||!hd||!PLACE.on||!State.phoneOpen)return r;const id=TCBI_PLACE[PLACE.on.id];if(!id)return r;
  const sig=hd.__k+'|'+id;if(hd.__tcbi===sig&&hd.querySelector('[data-tcbi]'))return r;hd.__tcbi=sig;const m=TCBI_CITY[id],sm=window.innerWidth<720;
  if(m.formats.logo){const cv=hd.querySelector('canvas.plLogo');if(cv){const h=sm?64:96,w=Math.round(h*1.5);cv.removeAttribute('data-tcb-logo');cv.classList.remove('tcbLogo');cv.dataset.tcp='tcbi:'+id;cv.dataset.tcpDone='tcbi:'+id;
   cv.style.flexBasis=w+'px';cv.style.borderRadius='10px';tcbiPlaceCv(cv,id,'logo',w,h);tcbiMark('f',id+':logo')}}
  if(m.formats.proposal&&!hd.querySelector('.tcbiSign')){const hdr=hd.querySelector('.plHd');if(hdr){const dv=document.createElement('div');dv.className='tcbiSign';dv.style.cssText='display:flex;justify-content:center;padding:6px 0 2px';
   const cv=document.createElement('canvas');cv.style.borderRadius='4px';cv.style.boxShadow='0 3px 10px #0006';dv.appendChild(cv);hdr.insertAdjacentElement('afterend',dv);const h=sm?34:46;tcbiPlaceCv(cv,id,'proposal',h*5,h);tcbiMark('prop',id+':proposal')}}}
 catch(e){tcbiErr(e,'place')}return r};TCBI.n.hooks++}
/* (12) "חידוש 01 · מזנוני השדה" (הבעלים 19:00 — אושר): ששת המזנונים — השלט והלוגו המאוירים של המעצב (set7_watch/refined_1825) במקום הזמניים של
   airlogos. הציור של המעצב מקודד כמלבנים צבעוניים בקבצים של 470–720 ק"ב; כאן — אותו ציור, מוקטן לגודל של השלט במשחק (8 נקודות ליחידת עולם;
   הלוגו 120×96), לוח של 48 צבעים, רצועות אופקיות באלפבית בלי תנועות (tools/gen_refined.py) — ומצויר פעם אחת לקנבס קטן ונשמר. הציור הסופי —
   כמו draw של המעצב (refinedDrawingFactory): רקע, contain, מסגרת דקה כשיש שוליים, והילה בלילה. השלט — במקום השלט התלוי של המזנון (s15jSignSprite);
   הלוגו (5:4) — במרכז לוח התפריט הקיים מעל הדלפק (074x:s15jShopInside), בגובה הלוח (6). */
const TCBI_RF=/*@REFINED@*/;
const TCBI_RF_IX={};{const A=TCBI_RF.alpha;for(let i=0;i<A.length;i++)TCBI_RF_IX[A.charCodeAt(i)]=i}
const TCBI_RF_NAME={};for(const id in TCBI_RF.brands)TCBI_RF_NAME[TCBI_RF.brands[id].name]=id;
const TCBI_RF_CV=new Map();
function tcbiRfTex(id,fmt){const k=id+'|'+fmt;let cv=TCBI_RF_CV.get(k);if(cv)return cv;const p=TCBI_RF.brands[id].parts[fmt],B=TCBI_RF.base,IX=TCBI_RF_IX;
 cv=document.createElement('canvas');cv.width=p.w;cv.height=p.h;const g=cv.getContext('2d');g.fillStyle=p.bg;g.fillRect(0,0,p.w,p.h);
 for(const [col,s] of p.L){g.fillStyle=col;let i=0,pos=0;const n=s.length,rd=()=>{let v=0,m=1;for(;;){const d=IX[s.charCodeAt(i++)];if(d<B)return v+d*m;v+=(d-B)*m;m*=B}};
  while(i<n){pos+=rd();const L=rd()+1;g.fillRect(pos%p.w,Math.floor(pos/p.w),L,1);pos+=L}}
 TCBI_RF_CV.set(k,cv);return cv}
function tcbiRfDraw(c,id,fmt,x,y,w,h,N){const p=TCBI_RF.brands[id].parts[fmt],cv=tcbiRfTex(id,fmt);c.save();c.beginPath();c.rect(x,y,w,h);c.clip();
 const s=Math.min(w/p.w,h/p.h),dw=p.w*s,dh=p.h*s,ox=x+(w-dw)/2,oy=y+(h-dh)/2,pad=w-dw>1||h-dh>1;c.fillStyle=p.back||p.bg||'#082f30';c.fillRect(x,y,w,h);c.imageSmoothingEnabled=true;c.drawImage(cv,ox,oy,dw,dh);
 if(pad){const col=p.trim||'#c08a52';c.strokeStyle=col;c.lineWidth=Math.max(.6,Math.min(w,h)*.004);c.strokeRect(x+1.5,y+1.5,w-3,h-3);c.globalAlpha=.28;c.strokeRect(x+4,y+4,w-8,h-8);c.globalAlpha=1}
 if(N){c.save();c.globalCompositeOperation='screen';c.strokeStyle=p.trim||'#d6c49b';c.globalAlpha=.24;c.lineWidth=Math.max(1,Math.min(w,h)*.012);c.strokeRect(x+1.5,y+1.5,w-3,h-3);c.restore()}c.restore()}
function tcbiRfSpr(id,fmt,w,h,N){const key='rf|'+id+'|'+fmt+'|'+(Math.round(w*4)/4)+'|'+(Math.round(h*4)/4)+'|'+(N?1:0);let o=TCBI.spr.get(key);if(o)return o;
 const sc=fmt==='sign'?8:16,cv=document.createElement('canvas');cv.width=Math.max(1,Math.ceil(w*sc));cv.height=Math.max(1,Math.ceil(h*sc));tcbiRfDraw(cv.getContext('2d'),id,fmt,0,0,cv.width,cv.height,N);
 tcbiSprMem(cv);o={cv,w,h,id};TCBI.spr.set(key,o);TCBI.n.spr++;return o}
TCBI.n.rf=0;TCBI.n.rfLogo=0;
if(typeof s15jSignSprite==='function'){const f=s15jSignSprite;s15jSignSprite=function(txt,kind,N){const id=TCBI.on&&TCBI_RF_NAME[txt];if(!id)return f.apply(this,arguments);
 try{const o=f.apply(this,arguments),s=tcbiRfSpr(id,'sign',o.w,o.h,N);tcbiMark('rf',id+':sign');return s}catch(e){tcbiErr(e,'rf');return f.apply(this,arguments)}};TCBI.n.hooks++}
if(typeof s15jShopInside==='function'){const f=s15jShopInside;s15jShopInside=function(g,it,N){const r0=f.apply(this,arguments);const id=TCBI.on&&it&&TCBI_RF_NAME[it.name];if(!id)return r0;
 try{const r=it.r,K=s15jK(),back=it.open==='N'?r[3]-5:r[1]+2,lh=6,lw=7.5,s=tcbiRfSpr(id,'logo',lw,lh,N);g.drawImage(s.cv,(r[0]+r[2])/2-lw/2,back-K*24-6,lw,lh);tcbiMark('rfLogo',id+':logo')}catch(e){tcbiErr(e,'rfLogo')}return r0};TCBI.n.hooks++}
/* הבדיקה: כל פריט keep — מצויר בלי שגיאה (בקנבס בדיקה), ומה כבר צויר בעולם / במסך (seen) */
window.__TC_BRANDIN={TCBI,rf:TCBI_RF_NAME,rfDraw:tcbiRfDraw,big:[...TCBI_BIG],b4pos:TCBI_B4POS,b4t:TCBI_B4T,keep:TCBI_KEEP,ops:TCBI_OPS,city:TCBI_CITY,place:TCBI_PLACE,ct:TCBI_CT,
 stats:()=>({on:TCBI.on,err:TCBI.err,sprMB:+((TCBI.sprB||0)/1048576).toFixed(1),n:Object.assign({},TCBI.n),seen:Object.keys(TCBI.seen).length,sprites:TCBI.spr.size,fail:TCBI.fail.slice(0,10)}),
 audit:()=>{const R=[],cv=document.createElement('canvas');cv.width=240;cv.height=120;const g=cv.getContext('2d');
  const one=(kind,id,fn)=>{let ok=false,det='';try{g.clearRect(0,0,240,120);fn();const px=g.getImageData(0,0,240,120).data;let n=0;for(let i=3;i<px.length;i+=16)if(px[i])n++;ok=n>20;det=ok?'':'ריק'}catch(e){det=String(e&&e.message||e).slice(0,120)}R.push({kind,id,ok,det})};
  for(const id in TCBI_OPS)one('ops',id,()=>TCBI_R.TC_AIRPORT_OPS.draw(g,id,'sign',0,0,240,120*Math.min(1,TCBI_OPS[id].formats.sign.h/TCBI_OPS[id].formats.sign.w*2),{night:false}));
  for(const id in TCBI_CITY){const m=TCBI_CITY[id];for(const k in m.formats)one('city',id+':'+k,()=>TCBI_R.TC_CITY.draw(g,id,k,0,0,240,k==='logo'?120:60,{night:false}))}
  for(const k of TCBI_KEEP.library)one('library',k,()=>{const b=tcbiBK(k);if(!b)throw Error('אין בטבלת המותגים');tcbiLogoDraw(b,g,0,0,240,120)});
  for(const id in TCBI_RF.brands)for(const fm of ['logo','sign'])one('refined',id+':'+fm,()=>tcbiRfDraw(g,id,fm,0,0,fm==='logo'?150:240,120,false));
  if(window.TC_EVENT_POSTERS)for(const k of TCBI_KEEP.poster)for(const fm of ['facade','screen'])one('poster',k+':'+fm,()=>window.TC_EVENT_POSTERS.draw(g,k,fm,0,0,fm==='facade'?80:192,120,{night:false}));else R.push({kind:'poster',id:'TC_EVENT_POSTERS',ok:false,det:'חסר'});
  return{ok:R.every(r=>r.ok)&&!TCBI.err,n:R.length,byKind:R.reduce((o,r)=>(o[r.kind]=(o[r.kind]||0)+1,o),{}),fail:R.filter(r=>!r.ok).slice(0,30),err:TCBI.err}},
 on:v=>{TCBI.on=!!v;TCBI.spr.clear();try{if(typeof BLD40!=='undefined'&&BLD40.clear)BLD40.clear()}catch(e){}return TCBI.on}};
