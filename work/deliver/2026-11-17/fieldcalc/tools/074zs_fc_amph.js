/* ==== fieldcalc 17.11 · האמפיבי של השדה — נוחת על המים מדרום לשדה, מסיע וקושר במזח צף (הבעלים 13.11: "האמפיבי: בדרום, על המים ליד השדה — מקום נחיתה, הסעה ועגינה … בנוסף למה שיש היום") ====
   הציור: deliver/2026-11-17/fieldcalc/Fieldcalc_plan.html, סעיף 11. כלל 19א: אותו מנגנון של 074zm (AMPH — המטוס של G6 / H6, ‏ICON A5, ‏AC-AM-01) — מופע שני של amphMake
   עם התצורה של השדה (074zm: amphMake(CFG) — בלי CFG הוא בדיוק כמו קודם): אותו צייר (s15DrawAc), אותה פיזיקה, אותן ההמתנות וההקפה לפי כלי השיט שבאמת שם (busy()),
   אותה בדיקה (audit). כאן רק: התצורה, המזח הצף והרמפה והשער בגדר (ציור 3/4 בקוד), החיבורים (הצעד, הציור, הסירות של השחקן, F9, roadAudit), ובדיקה נוספת —
   המרחק מנתיב הסירות של המספנה (074g: G.lane) חוץ מהחצייה. בלי אנשים במופע הזה (הטייס במטוס — כמו מטוסי ה-GA של S15); הנוסעים — עם הלוח החדש (סעיף 11). */
var FCAMPH=null,FCAMPH_ST={err:'',n:0,draws:0};
(function(){'use strict';
 const er=(w,e)=>{FCAMPH_ST.n++;if(!FCAMPH_ST.err)FCAMPH_ST.err=w+': '+String(e&&e.stack||e).slice(0,220)};
 if(typeof amphMake!=='function'){FCAMPH_ST.err='אין amphMake (074zm)';return}
 const PI=Math.PI;
 const H1=[8300,2860],H2=[8300,2985],MOOR=[8330,2662,PI];
 const CFG={
  RWY:{y:3110,x0:7300,x1:9450,half:50,td:9200,stop:8500,lineup:9300,lift:8300},            // ממריא ונוחת מערבה (אותו כיוון — כמו מסלול אמיתי)
  DECK:[8180,2600,8470,2640],MOOR,H1,H2,
  TAXI_OUT:[[8330,2662],[8262,2664],[8226,2700],[8240,2750],[8300,2790],[8300,2860]],
  CROSS_OUT:[H1,H2],
  TAXI_LU:[H2,[8300,3008],[8344,3030],[9300,3030],[9396,3054],[9400,3090],[9364,3110],[9300,3110]],
  TAXI_IN1:[[8500,3110],[8420,3110],[8352,3082],[8312,3034],[8300,2985]],
  CROSS_IN:[H2,H1],
  TAXI_IN2:[H1,[8300,2800],[8330,2742],[8400,2702],[8412,2676],[8392,2662],[8330,2662]],
  FLIGHT:[[8300,3110,0],[7600,3110,110],[7150,3260,200],[7250,3680,300],[8000,3770,330],[9800,3770,330],[10350,3600,300],[10450,3300,230],[10150,3130,140],[9900,3110,80],[9200,3110,0]],
  FINAL_AT:[10450,3300],ORBIT_R:300,
  SPOT:{wait:[8300,2620],watch:[8280,2612],side:[8330,2645],pilot:[8320,2630]},WALK:[[8448,2552],[8448,2600],[8300,2620]],
  TOURS:[420,540,660,780,900,1020],                                                                    // 07:00 · 09:00 · 11:00 · 13:00 · 15:00 · 17:00 — דקות משחק
  ZONES:{cross:[8200,2850,8400,2995],rwy:[7240,3030,9500,3190]},
  noPeople:true,
  CAM:{land:[9400,3060,1.15,'האמפיבי של השדה — הנחיתה במים מדרום לשדה'],dock:[8330,2700,1.7,'ההסעה אל המזח הצף והקשירה'],board:[8330,2650,2.4,'במזח הצף'],
       takeoff:[9000,3060,1.15,'ההמראה מהמים — מערבה'],cross:[8300,2920,1.4,'החצייה של נתיב הסירות של המספנה — H2 ← H1, רק כשפנוי'],night:[8330,2660,2.2,'לילה — קשור במזח הצף'],tour:[9000,3600,.6,'ההקפה מעל הים']}};
 try{FCAMPH=amphMake(CFG)}catch(e){er('make',e);return}
 /* ---- המזח הצף, הרמפה והשער (3/4: הגובה כלפי מעלה במסך × S15_K) ---- */
 const PIER=CFG.DECK,RAMP=[8433,2548,8463,2602],GATE=[8428,2546,8468,2554];
 const ZK=()=>typeof S15_K!=='undefined'?S15_K:.6,night=()=>Math.max(0,Math.min(1,+window.__TC_NIGHT||0));
 function drawPier(c,now){if(!e3InView(PIER[0]-40,2520,PIER[2]-PIER[0]+80,PIER[3]-2520+50,20))return;FCAMPH_ST.draws++;const N=night(),k=ZK(),hz=6*k,[x0,y0,x1,y1]=PIER;
  // המצופים (פונטונים) — כהים, מתחת לסיפון, נראים בחזית
  c.fillStyle=N>.5?'#1d2328':'#3a434a';c.fillRect(x0+4,y1-1,x1-x0-8,4);
  // החזית של הסיפון (הגובה מעל המים) והסיפון — קרשים
  c.fillStyle=N>.5?'#4a3a2a':'#7a5c3c';c.fillRect(x0,y1-hz,x1-x0,hz);
  c.fillStyle=N>.5?'#6b5640':'#b08a5c';c.fillRect(x0,y0-hz,x1-x0,y1-y0);
  c.strokeStyle=N>.5?'rgba(0,0,0,.35)':'rgba(70,45,20,.35)';c.lineWidth=.6;for(let x=x0+6;x<x1;x+=6){c.beginPath();c.moveTo(x,y0-hz);c.lineTo(x,y1-hz);c.stroke()}
  // הקצה הצהוב (בטיחות) והמתקנים: עמודי קשירה, גלגלי הצלה, פנסים
  c.strokeStyle='#e6c84b';c.lineWidth=1.2;c.strokeRect(x0+.6,y0-hz+.6,x1-x0-1.2,y1-y0-1.2);
  for(const x of [x0+20,x0+90,x0+160,x0+230,x1-14]){c.fillStyle='#2b3136';c.beginPath();c.arc(x,y1-hz-3,2.2,0,2*PI);c.fill()}
  for(const x of [x0+55,x1-60]){c.strokeStyle='#e8562a';c.lineWidth=2;c.beginPath();c.arc(x,y0-hz+6,3.2,0,2*PI);c.stroke()}
  for(const x of [x0+8,(x0+x1)/2,x1-8]){const top=y0-hz-k*30;c.strokeStyle='#59646a';c.lineWidth=1.2;c.beginPath();c.moveTo(x,y0-hz+3);c.lineTo(x,top);c.stroke();c.fillStyle=N>.25?'#fff4c8':'#cfd6da';c.beginPath();c.arc(x,top,1.8,0,2*PI);c.fill();
   if(N>.25){c.save();c.globalCompositeOperation='lighter';const g=c.createRadialGradient(x,top,0,x,top,26);g.addColorStop(0,'rgba(255,236,180,'+(.5*N).toFixed(2)+')');g.addColorStop(1,'rgba(255,236,180,0)');c.fillStyle=g;c.fillRect(x-26,top-26,52,52);c.restore()}}
  // הרמפה (גשר הולכי רגל) מהשער בגדר אל המזח — יורדת, עם מעקות
  {const [a0,b0,a1,b1]=RAMP;c.fillStyle=N>.5?'#5a5f63':'#9aa3a8';c.beginPath();c.moveTo(a0,b0);c.lineTo(a1,b0);c.lineTo(a1,b1-hz);c.lineTo(a0,b1-hz);c.closePath();c.fill();
   c.strokeStyle=N>.5?'#2b3136':'#4d565c';c.lineWidth=.6;for(let y=b0+5;y<b1-hz;y+=5){c.beginPath();c.moveTo(a0,y);c.lineTo(a1,y);c.stroke()}
   c.strokeStyle='#d5dadd';c.lineWidth=1.1;for(const x of [a0,a1]){c.beginPath();c.moveTo(x,b0-k*10);c.lineTo(x,b1-hz-k*10);c.stroke();for(let y=b0;y<=b1-hz;y+=12){c.beginPath();c.moveTo(x,y);c.lineTo(x,y-k*10);c.stroke()}}}
  // השער בגדר: שני עמודים ושער סגור (סורג)
  {const [g0,h0,g1]=GATE,top=h0-k*24;c.strokeStyle='#3d4448';c.lineWidth=2.2;for(const x of [g0,g1]){c.beginPath();c.moveTo(x,h0+4);c.lineTo(x,top);c.stroke()}
   c.strokeStyle='#7d878c';c.lineWidth=.8;for(let x=g0+4;x<g1;x+=4){c.beginPath();c.moveTo(x,h0+3);c.lineTo(x,top+3);c.stroke()}c.beginPath();c.moveTo(g0,top+4);c.lineTo(g1,top+4);c.stroke();
   c.fillStyle='#b3261e';c.fillRect((g0+g1)/2-6,top-9,12,5)}}
 /* ---- החיבורים (כמו של 074zm) ---- */
 try{S9_HOOKS.live.push((c,now,N)=>{try{drawPier(c,now)}catch(e){er('pier',e)}try{FCAMPH.step(now);FCAMPH.drawWater(c,now)}catch(e){er('water',e)}})}catch(e){er('hook live',e)}
 try{const pO=wtcOverLive;wtcOverLive=function(now){const r=pO.apply(this,arguments);try{FCAMPH.step(now);FCAMPH.drawAir(now)}catch(e){}return r}}catch(e){}
 try{const pA=drawAptOverhead;drawAptOverhead=function(now){const r=pA.apply(this,arguments);try{FCAMPH.step(now);FCAMPH.drawAir(now)}catch(e){}return r}}catch(e){}
 try{if(typeof FISH3!=='undefined'&&FISH3.HOOK){const pH=FISH3.HOOK.hit;FISH3.HOOK.hit=function(b,x,y,h){const r=pH?pH.apply(this,arguments):null;if(r)return r;
   try{const n=FCAMPH.nowS(),p=FCAMPH.poseAt(n.s,n.d);if(p.z>0||Math.abs(p.x-x)>160||Math.abs(p.y-y)>160){
     // המזח הצף והרמפה — כמו מזח (סירה לא עוברת דרכם)
     const H=FISH3.obb(x,y,h,b.L*.97,b.B*.92),R=(r0)=>FISH3.obb((r0[0]+r0[2])/2,(r0[1]+r0[3])/2,0,r0[2]-r0[0],r0[3]-r0[1]);if(Math.abs(y-2620)<120&&Math.abs(x-8325)<260&&(FISH3.sat(H,R(PIER))||FISH3.sat(H,R(RAMP))))return 'המזח הצף של השדה';return null}
    const H=FISH3.obb(x,y,h,b.L*.97,b.B*.92),c=Math.cos(p.h),sn=Math.sin(p.h),Rb=(l,w,ox)=>FISH3.obb(p.x+c*ox,p.y+sn*ox,p.h,l,w);
    if(FISH3.sat(H,Rb(FCAMPH.L,30,0))||FISH3.sat(H,Rb(16,FCAMPH.WS,FCAMPH.L*.08)))return 'המטוס האמפיבי של השדה'}catch(e){}return null}}}catch(e){er('fish3',e)}
 try{PERF_LOOK.push({label:'האמפיבי של השדה — הנחיתה במים',go:()=>FCAMPH.scene('land')},{label:'האמפיבי של השדה — ההסעה והקשירה במזח הצף',go:()=>FCAMPH.scene('dock')},
  {label:'האמפיבי של השדה — החצייה של נתיב הסירות',go:()=>FCAMPH.scene('cross')},{label:'האמפיבי של השדה — ההמראה',go:()=>FCAMPH.scene('takeoff')},{label:'האמפיבי של השדה — לילה במזח',go:()=>FCAMPH.scene('night')})}catch(e){}
 /* ---- הבדיקה: האודיט של 074zm על המופע הזה + המרחק מנתיב הסירות של המספנה (חוץ מהחצייה) + מעל השדה אף פעם ---- */
 function laneAudit(){const out=[];let bad=[],minD=1e9,at='';try{const G=(typeof BSHOP!=='undefined'&&BSHOP.G)||{stage:[7120,2880],edge:[9420,2960]},A=G.stage,B=G.edge;
   const dSeg=(x,y)=>{const dx=B[0]-A[0],dy=B[1]-A[1],u=Math.max(0,Math.min(1,((x-A[0])*dx+(y-A[1])*dy)/(dx*dx+dy*dy)));return Math.hypot(A[0]+u*dx-x,A[1]+u*dy-y)};
   const DY=FCAMPH.DAY,sv={d:DY.d,D:DY.D,sc:DY.sc};try{DY.d=null;FCAMPH.dayScript(-555);const R=(typeof G84_CLOCK!=='undefined'&&G84_CLOCK.rate)||.5;
    for(let s=0;s<1440/R;s+=.5){const p=FCAMPH.poseAt(s,-555);if(p.z>0)continue;
     if(Math.hypot(p.x-H1[0],p.y-H1[1])<100||Math.hypot(p.x-H2[0],p.y-H2[1])<100||p.ph==='cross'||p.ph==='crossIn')continue;   // החצייה ונקודות ההמתנה שלה
     const d=dSeg(p.x,p.y)-FCAMPH.WS/2;if(d<minD){minD=d;at=p.ph+' '+Math.round(p.x)+','+Math.round(p.y)}if(d<30&&bad.length<4)bad.push(p.ph+' '+Math.round(s)+'s '+d.toFixed(0))}}
   finally{DY.d=sv.d;DY.D=sv.D;DY.sc=sv.sc}
  }catch(e){bad.push('שגיאה '+e)}
  return{ok:!bad.length,det:bad.length?'✗ קרוב לנתיב הסירות: '+bad.join(' · '):'מחוץ לחצייה (100 פיקס׳ סביב H1 / H2) — לפחות '+(minD/10).toFixed(1)+' מ׳ (קצה הכנף) מנתיב הסירות של המספנה ('+at+')'}}
 (function(){try{const base=roadAudit;roadAudit=function(){const r=base.apply(this,arguments);try{const A=FCAMPH.audit(),Ln=laneAudit(),L=r.checks||r.results;const ok=A.ok&&Ln.ok&&!FCAMPH_ST.err;
   if(Array.isArray(L))L.push({name:'fc_amph_water',id:'fc_amph_water',ok,pass:ok,detail:A.rows.map(q=>(q.ok?'✓ ':'✗ ')+q.id+': '+q.det).join(' | ')+' | '+(Ln.ok?'✓ ':'✗ ')+'fc_amph_lane: '+Ln.det+(FCAMPH_ST.err?' | ✗ '+FCAMPH_ST.err:'')});
   if(!ok){r.ok=false;(r.issues||(r.issues=[])).push('fc_amph_water')}}catch(e){}return r}}catch(e){}})();
 try{window.__TC_FCAMPH=FCAMPH}catch(e){}
})();
