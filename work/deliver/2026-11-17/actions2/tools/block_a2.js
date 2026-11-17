 /* ==== actions2 (17.11 ~12:55, הבעלים: "רואים אותו ממתין לי אבל בשניה שאני מגיע זה מתחיל ללא לחיצה שלי / הייתי ברכב / צריך שאני יפעיל ואז נראה אותי
    הולך לוחץ יד מדבר קונה לוקח מרים") — שדרוג של מה שכאן (כלל 19א; הציור: deliver/2026-11-17/actions2/draw/Story_actions2_plan.html):
    (1) שום שלב לא מתחיל לבד כשמגיעים — רק F (ברכב: F מוציא מהרכב וממשיך) או הכפתור בכרטיס: כל 22 שלבי הנסיעה (המנועים 038a / 074zs לא מקדמים בקרבה),
        "להמשיך עם החפץ", ובסיפור הראשי (074ze — בלי שינוי בו) השיחה / העבודה / הסרט שנפתחו לבד כשעוצרים ליד (עטיפה של g77DlgOpen / startMission / TCSHOW.open);
    (2) אחרי ההפעלה — השחקן עצמו (P34, הצייר של המשחק) הולך אל הדמות / החפץ ועושה: לוחץ יד, מדבר (בועה, וקול כשיש הקלטה), משלם, מתכופף, מרים, נושא, מניח,
        מושיט — ורק בסוף ההתקדמות (PS — הרצף של השחקן); חץ / WASD / E — עוצר;
    (3) הדמות שמחכה — בתנועת המתנה (לא קפואה), מסתובבת אל השחקן כשהוא מתקרב, ומנופפת לו. ==== */
 /* (1) התנוחות החדשות — באותו צייר (P34X.pose בשרשור, כמו W17 / s15bag), והמספר של התמונות ב-P34.FR.
    המפתחות (מ׳): a — הידיים לפני הרגליים, s — חצי הרווח, z — הגובה, lean — ההטיה, drop — הברכיים, pitch — הראש */
 const SAP_KEY={R:{a:.24,s:.19,z:.98,lean:.04,drop:0,pitch:.05},G:{a:.46,s:.17,z:.52,lean:.5,drop:.2,pitch:.42},H:{a:.3,s:.16,z:1.1,lean:.02,drop:0,pitch:.1},
  P:{a:.55,s:.14,z:1.05,lean:.14,drop:.02,pitch:.12},T:{a:.44,s:.17,z:.86,lean:.24,drop:.06,pitch:.32},C:{a:.22,s:.1,z:1.52,lean:0,drop:0,pitch:-.04},U:{a:.22,s:.22,z:1.78,lean:-.04,drop:0,pitch:-.3}};
 /* k → ['2', מ-, אל-, תמונות, 1 תנודה / 2 הלוך-חזור] (שתי ידיים, כל הגוף) · ['1', u → {a, s, z} של יד ימין, תמונות] · ['W' — כמו 1, והשמאלית מחזיקה לוח] */
 const SAP_ACT={saDn:['2','R','G',6],saUp:['2','G','H',6],saDnT:['2','R','T',6],saUpT:['2','T','H',6],saGive:['2','H','P',6],saCam:['2','C','C',1],saWork:['2','T','T',8,1],saFix:['2','P','P',8,1],saPick:['2','R','G',8,2],saHang:['2','H','U',6],
  saShake:['1',u=>({a:.42,s:.04,z:1+.035*Math.sin(u*TAU*2)}),8],saTalk:['1',u=>({a:.3+.06*Math.sin(u*TAU),s:.26,z:1.14+.07*Math.sin(u*TAU+1.2)}),8],saPhone:['1',()=>({a:.08,s:.12,z:1.62}),1],
  saWave:['1',u=>({a:.14,s:.3+.1*Math.sin(u*TAU),z:1.86}),8],saPay:['1',()=>({a:.5,s:.06,z:1.08}),1],saStamp:['1',u=>({a:.42,s:.12,z:.92+.12*Math.abs(Math.sin(u*Math.PI))}),8],
  saWrite:['W',u=>({a:.32+.02*Math.sin(u*TAU*2),s:.02,z:1.1+.015*Math.cos(u*TAU*2)}),8]};
 const sapF=k=>{const A=SAP_ACT[k];return A?(A[0]==='2'?A[3]:A[2])||1:1};
 function sapPose(S,L,act,fr,X){const A=SAP_ACT[act.k],F=sapF(act.k),{comb,ik,add,sub,mul,nrm,Z}=X,D=S.D,f=S.f,l=S.l,O=[0,0,0],hk=D.h/1.76,u=F>1?fr/F:0;
  const arm=(side,tg,fU,lU,bob)=>{const sh=add(add(S.torsoAt(D.shZ+bob),[0,0,D.shZ+bob]),add(mul(lU,side*D.armS),mul(fU,-.008))),grip=comb(O,f,tg.a*hk,l,side*tg.s*hk,tg.z*hk),wd0=nrm(sub(grip,sh)),wrT=sub(grip,mul(wd0,.05*D.hs));
   const j=ik(sh,wrT,D.uarm,D.farm,nrm(add(add(mul(lU,side*.7),[0,0,-1]),mul(fU,-.3)))),wr=j.ank,wd=nrm(sub(grip,wr));return{side,sh,el:j.knee,wr,hand:add(wr,mul(wd,.052*D.hs)),wd}};
  if(A[0]!=='2'){const bob=S.dz||0,R=arm(-1,A[1](u),S.fU,S.lU,bob),Lf=A[0]==='W'?arm(1,{a:.3,s:.06,z:1.06},S.fU,S.lU,bob):S.arms[0];S.arms=[Lf,R];return}
  /* שתי ידיים: האגן, הרגליים והגו — כמו 074r2:s15bagPose, עם המפתחות שכאן */
  const t=A[4]===2?.5-.5*Math.cos(u*TAU):F>1?Math.min(1,fr/(F-1)):0,k0=SAP_KEY[A[1]],k1=SAP_KEY[A[2]],m=x=>k0[x]+(k1[x]-k0[x])*t,osc=A[4]===1?Math.sin(u*TAU):0;
  const lean=m('lean'),pitch=m('pitch'),pelZ=D.hipZ-m('drop')*hk,pel=comb(O,f,-lean*.12,l,0,pelZ),toeA=(L.shoes&&L.shoes.t==='leather'?.082:.072)*D.hs;S.pel=pel;S.legs=[];
  for(const side of [1,-1]){const hip=comb(pel,f,0,l,side*D.hipS,0),ank=comb(O,f,side>0?.06:-.05,l,side*(D.hipS+.04),D.ankZ),j=ik(hip,ank,D.thigh,D.shin,f),
   toe=add(j.ank,add(mul(f,toeA),[0,0,-D.ankZ+.028])),heel=add(j.ank,add(mul(f,-.028*D.hs),[0,0,-D.ankZ+.03]));toe[2]=Math.max(.025,toe[2]);heel[2]=Math.max(.028,heel[2]);S.legs.push({side,hip,knee:j.knee,ank:j.ank,toe,heel,y:l[1]*side})}
  const fU=S.fU,lU=S.lU,tc=comb(O,fU,-lean*.1,lU,0,0);S.torsoAt=z=>comb(tc,fU,lean*(z-pelZ),lU,0,0);S.pelZ=pelZ;S.lean=lean;const bob=pelZ-D.hipZ;S.dz=bob;
  S.neck=[add(S.torsoAt(D.neck0+bob),[0,0,D.neck0+bob]),add(S.torsoAt(D.neck1+bob),[fU[0]*.012,fU[1]*.012,D.neck1+bob])];
  const ef=nrm(add(mul(fU,Math.cos(pitch)),mul(Z,-Math.sin(pitch)))),ez=nrm(add(mul(Z,Math.cos(pitch)),mul(fU,Math.sin(pitch))));
  S.head={c:add(add(S.torsoAt(D.headZ+bob),[0,0,D.headZ+bob]),add(mul(fU,.016*D.hs),mul(ef,.01*D.hs))),ax:[lU,ef,ez],r:D.head};
  S.arms=[1,-1].map(side=>arm(side,{a:m('a')+.03*osc,s:m('s'),z:m('z')+.04*osc*side},fU,lU,bob))}
 function sapInstall(){try{if(typeof P34==='undefined'||!P34.FR)return false;const X=window.P34X||(window.P34X={});if(X.__sap)return true;for(const k in SAP_ACT)P34.FR[k]=sapF(k);
   const p0=X.pose;X.pose=function(S,L,act,fr,PX){if(act&&SAP_ACT[act.k]){try{sapPose(S,L,act,fr,PX)}catch(e){err('pose',e)}return}if(p0)return p0.apply(this,arguments)};X.__sap=1;return true}catch(e){err('sapInstall',e);return false}}
 sapInstall();
 /* (2) הרצף של השחקן (PS): הליכה (walk, במהירות של המשחק — 028:updatePed, ‏52 פיק׳ לשנייה), תנוחה (pose — בזמן, עם בועה / הדמות השנייה), יציאה מהרכב / כניסה (exit / enter),
    ופעולה (fn). השחקן בשליטה של הרצף (updatePed — כמו הביקור); חץ / WASD / Esc / E — עוצר. מצויר כאן בתנוחות החדשות (P34.draw), ובהליכה — הציור הרגיל. */
 const PS={q:null,n:0,done:0,cancel:0,poses:{},last:null,why:null},WSP=52;
 const psOn=()=>!!PS.q;
 function clearTo(x0,y0,x1,y1){const L=Math.hypot(x1-x0,y1-y0),n=Math.max(1,Math.ceil(L/6));let last={x:x0,y:y0};for(let i=1;i<=n;i++){const x=x0+(x1-x0)*i/n,y=y0+(y1-y0)*i/n;let b=false;try{b=!!personBlockedAt(x,y)}catch(e){}if(b)return last;last={x,y}}return last}
 /* איפה לעמוד כדי לעשות משהו ב-P: d פיק׳ לפניו, מהצד של השחקן, במקום שהולכים בו */
 function standAt(P,d){const a0=Math.atan2(PlayerPed.y-P.y,PlayerPed.x-P.x);for(const da of[0,.6,-.6,1.2,-1.2,1.9,-1.9,Math.PI]){const a=a0+da,q={x:P.x+Math.cos(a)*d,y:P.y+Math.sin(a)*d};let b=false;try{b=!!personBlockedAt(q.x,q.y)}catch(e){}if(!b)return q}return{x:PlayerPed.x,y:PlayerPed.y}}
 function psRun(steps,o){if(PS.q)psStop('replace');PS.q={steps,i:-1,o:o||{},t0:pnow(),seen:[],dist:0,t:0};PS.n++;psNext(pnow());return PS.q}
 function faceOf(s){const F=typeof s.face==='function'?s.face():s.face;if(F&&Number.isFinite(F.x)){s.hd=Math.atan2(F.y-PlayerPed.y,F.x-PlayerPed.x);PlayerPed.heading=s.hd;try{PlayerPed.dir=personDirection(Math.cos(s.hd),Math.sin(s.hd))}catch(e){}}}
 function psNext(now){const q=PS.q;if(!q)return;if(q.i>=0)q.t+=now-q.t0;q.i++;q.t0=now;const s=q.steps[q.i];
  if(!s){PS.q=null;PS.done++;PS.last={tag:q.o.tag,seen:q.seen,dist:Math.round(q.dist),ms:Math.round(q.t)};psFig(q.o.fig,null);try{q.o.done&&q.o.done(now)}catch(e){err('ps-done',e)}return}
  q.seen.push(s.k==='pose'?(s.p||'car'):s.k);if(s.k==='pose'&&s.p)PS.poses[s.p]=(PS.poses[s.p]||0)+1;
  if(s.k==='fn'){try{s.fn(now)}catch(e){err('ps-fn',e)}return psNext(now)}
  if(s.k==='exit'){let ok=PlayerProfile.mode!=='vehicle';if(!ok)try{ok=!!exitVehicle()}catch(e){}if(!ok){psStop('exit');return}return psNext(now)}
  if(s.k==='enter'){let ok=PlayerProfile.mode==='vehicle';if(!ok)try{ok=!!enterVehicle()}catch(e){}if(!ok&&s.must){psStop('enter');return}return psNext(now)}
  if(s.k==='walk'){const to=typeof s.to==='function'?s.to():s.to;if(!to||!walk())return psNext(now);const e=clearTo(PlayerPed.x,PlayerPed.y,to.x,to.y);s.a={x:PlayerPed.x,y:PlayerPed.y};s.b=e;s.L=Math.hypot(e.x-s.a.x,e.y-s.a.y);if(s.L<2)return psNext(now);s.hd=Math.atan2(e.y-s.a.y,e.x-s.a.x)}
  if(s.k==='pose'){PlayerPed.moving=false;if(s.face)faceOf(s);if(q.o.fig)psFig(q.o.fig,s.fig||null)}
  if(s.bub&&!E.qa)try{bubble(s.bub)}catch(e){}
  if(s.on)try{s.on(now)}catch(e){err('ps-on',e)}}
 function psTick(now){const q=PS.q;if(!q)return;if(VIS.v||State.ferryRide||State.taxiRide&&State.taxiRide.phase==='riding'){psStop('busy');return}const s=q.steps[q.i];if(!s){psNext(now);return}const t=Math.max(0,(now-q.t0)/1000);
  if(s.k==='walk'){if(!walk()){psStop('mode');return}const d=Math.min(s.L,t*(s.sp||WSP)),f=s.L?d/s.L:1,x=s.a.x+(s.b.x-s.a.x)*f,y=s.a.y+(s.b.y-s.a.y)*f;q.dist+=Math.hypot(x-PlayerPed.x,y-PlayerPed.y);
   PlayerPed.x=x;PlayerPed.y=y;PlayerPed.heading=s.hd;PlayerPed.moving=d<s.L;PlayerPed.pose='walking';try{PlayerPed.dir=personDirection(Math.cos(s.hd),Math.sin(s.hd))}catch(e){}if(d>=s.L){PlayerPed.moving=false;psNext(now)}return}
  if(s.k==='pose'){PlayerPed.moving=false;if(s.face&&walk())faceOf(s);const f=s.d>0?Math.min(1,t/s.d):1;if(s.prog)try{s.prog(f)}catch(e){err('ps-prog',e)}if(s.hold&&s.hold(now))return;if(t>=s.d)psNext(now)}}
 function psStop(why){const q=PS.q;if(!q)return;PS.q=null;PS.cancel++;PS.why=why;PlayerPed.moving=false;psFig(q.o.fig,null);try{q.o.cancel&&q.o.cancel(why)}catch(e){err('ps-cancel',e)}}
 /* בדיקה: הרצף כולו בזמן מדומה (בלי לחכות) — מה שנראה בו (הליכה, התנוחות) */
 function psFast(lim){const q=PS.q;if(!q)return PS.last;let T=pnow();for(let i=0;i<(lim||4000)&&PS.q===q;i++){T+=40;psTick(T)}if(PS.q===q){psStop('qa-long');return null}return PS.last}
 /* הדמות השנייה ברצף: מחזיקים אותה (hold — בלי השם, פונה לשחקן) בתנוחה של הרגע; משחררים בסוף — רק אם אנחנו החזקנו (לא סצנה של cutscenes) */
 function psFig(f,k){if(!f)return;if(k){if(!f.hold||f.__saHold){f.hold=true;f.__saHold=1;f.k=k;f.hd=null}}else if(f.__saHold){f.hold=false;f.__saHold=0;f.k=null;f.hd=null}}
 function voiceLine(who,t){try{if(!who||typeof TCVREC==='undefined'||typeof TCVOICE==='undefined')return;const v=TCVREC.voiceFor(who,t)||(typeof TCVREC_ST!=='undefined'?TCVREC_ST.voiceOf(t,who):'');if(!v||!TCVREC.rec(t,v))return;TCVOICE.speak(t,who,'story',1);E.voice=(E.voice||0)+1}catch(e){}}
 /* בועה: [מי, טקסט, מ"ש] — מי: 'player' · דמות (FIG) · מזהה איש קשר (מעל השחקן, עם השם — בטלפון) */
 function bubble(b){const [w,t,ms]=b;if(!t)return;let anc='player',who='';if(w&&typeof w==='object'){const f=w;anc=()=>f.pt?{x:f.pt.x,y:f.pt.y-30}:null;who=String(f.id||'').indexOf('n:')===0?f.name:f.id}else if(w&&w!=='player')who=w;
  try{g77Bubble(anc,t,{who:who||undefined,ms:ms||2200})}catch(e){}if(who)voiceLine(who,t);E.bub=(E.bub||0)+1}
 /* המראה של השחקן לציור הישיר (כמו 074zu:p34Player — אותו גוף, עם החפץ / האפוד) */
 const PLK={key:'',look:null};
 function plLook(item,vest){let pl=null;try{pl=p672Pl()}catch(e){}if(!pl)return null;const key=(typeof P672!=='undefined'?P672.k:'')+'|'+(item?item.k+'.'+[].concat(item.c).join('.'):'')+'|'+(vest||'');
  if(PLK.key!==key){const L=JSON.parse(JSON.stringify(pl,(k,v)=>k.slice(0,2)==='__'?undefined:v));if(item)L.item=item;else delete L.item;if(vest)L.vest=vest;PLK.key=key;PLK.look=L}return PLK.look}
 /* הציור של השחקן בתנוחה של הרגע (רק בזמן תנוחה של הרצף; בהליכה — הציור הרגיל של המשחק). החפץ בשתי הידיים — מצויר כאן, ליד הידיים */
 function psDraw(now){const q=PS.q,s=q&&q.steps[q.i];if(!s||s.k!=='pose'||!s.p||!walk()||!p34Live()||typeof P34==='undefined'||!P34.draw)return false;
  const c=SA.cur&&SA.cur.ps?SA.cur:null,h=carried(),w=wearOk(),two=SAP_ACT[s.p]&&SAP_ACT[s.p][0]==='2';let o=h&&h.o,col=h&&h.c;
  if(c&&s.held){o=c.k==='pick'?(c.opt.into||c.o):c.k==='sort'?c.o:(h&&h.o)||c.o;col=c.k==='give'&&h?h.c:c.c}else if(c&&c.k!=='via')o=c.k==='take'||c.k==='find'||c.k==='sort'||c.k==='give'?null:o;
  if(s.empty)o=null;const item=o&&!two?itemOf(o,col):null,vest=w?w.vest:(c&&c.k==='wear'&&c.prog>=.6?c.c:null),look=plLook(item,vest);if(!look)return false;
  const t=(now-q.t0)/1000;let ph=s.cyc?(t/s.cyc)%1:Math.min(.999,t/Math.max(.05,s.d));if(s.rev&&!s.cyc)ph=Math.max(0,.999-ph);const hd=Number.isFinite(PlayerPed.heading)?PlayerPed.heading:0;
  let res=2;try{res=p599Res(Camera.zoom*(window.devicePixelRatio||1))}catch(e){}
  let H=null;if(two&&o&&o!=='none'&&s.held){const A=SAP_ACT[s.p],k0=SAP_KEY[A[1]],k1=SAP_KEY[A[2]],F=sapF(s.p),fr=Math.floor(ph*F),tt=A[4]===2?.5-.5*Math.cos(ph*TAU):F>1?Math.min(1,fr/(F-1)):0,a=(k0.a+(k1.a-k0.a)*tt)*10,z=(k0.z+(k1.z-k0.z)*tt)*10;
   H={x:PlayerPed.x+Math.cos(hd)*a,y:PlayerPed.y+Math.sin(hd)*a,z:Math.max(.5,z-3)}}
  const oo=o==='plants'?'crate':o,front=Math.sin(hd)>-.2;if(H&&!front)thing(ctx,oo,col,H.x,H.y,H.z,now);
  ctx.save();try{P34.draw(ctx,PlayerPed.x,PlayerPed.y,look,{k:s.p},hd,ph,res)}finally{ctx.restore()}if(H&&front)thing(ctx,oo,col,H.x,H.y,H.z,now);E.psDrawn=(E.psDrawn||0)+1;return true}
 /* השיחה עם דמות: לחיצת יד (פעם ב-3 דקות לאותו אדם) ודיבור — בועה של השחקן ובועה של הדמות */
 function talkSteps(f,hi,line,shakeOk){const S=[],shake=shakeOk!==false&&!(f.shook&&pnow()-f.shook<180000);
  if(shake)S.push({k:'pose',p:'saShake',d:1.2,cyc:.6,face:()=>f.pt,fig:'saShake',bub:hi?['player',hi,1900]:null,on:()=>{f.shook=pnow()}});
  S.push({k:'pose',p:'saTalk',d:line?2:1.3,cyc:1.1,face:()=>f.pt,fig:'saTalk',bub:line?[f,line,2600]:(!shake&&hi?['player',hi,1700]:null)});return S}
 function soloSteps(P,hi,line,phone,from){const S=[{k:'pose',p:phone?'saPhone':'saWave',d:phone?1.6:1.2,cyc:.8,face:()=>P,bub:hi?['player',hi,1800]:null}];if(line)S.push({k:'pose',p:phone?'saPhone':'saTalk',d:1.8,cyc:1,face:()=>P,bub:[from||'player',line,2400]});return S}
 function meetSteps(o){const f=o.fig&&o.fig.pt?o.fig:null,P=f?f.pt:o.at,m=me(),S=[];if(P&&Math.hypot(m.x-P.x,m.y-P.y)<(o.walkMax||450))S.push({k:'walk',to:()=>standAt(f?f.pt:P,f?9:12)});
  if(f)S.push(...talkSteps(f,o.hi,o.line,o.shake));else S.push(...soloSteps(P||m,o.hi,o.line,o.phone,o.from));return S}
 /* הדמות של השלב (מי כאן) */
 function figFor(id,n){try{const w=whoNow().find(q=>q.id===id&&q.n===n);const f=w&&whoPt(w).fig;return f&&f.pt?f:null}catch(e){return null}}
 const isMeet=(id,n)=>{const d=SA_DRIVE[id]&&SA_DRIVE[id][n];return!!d&&!Array.isArray(d)};
 const carBack=()=>{const a=PlayerCar.heading||0;return{x:PlayerCar.x-Math.cos(a)*16,y:PlayerCar.y-Math.sin(a)*16}};
 /* הפעולה אחרי F (140 השלבים + 8 ההגעות): הולכים אל החפץ / הדמות, ואז התנוחות של הסוג — ההתקדמות של הטבעת (c.prog) לפי הרצף */
 function actSteps(c){const P=c.pt,S=[],D=c.dur/1000,desk=c.o==='paper'||c.o==='small',up=desk?'saUpT':'saUp',dn=desk?'saDnT':'saDn',face=()=>c.k==='look'&&c.tg?c.tg:c.k==='via'?c.poi:P;
  const go=(p,d,o)=>Object.assign({k:'pose',p,d:Math.max(.35,d),face,on:()=>{c.phase='work'}},o||{}),pr=(a,b)=>f=>{c.prog=a+(b-a)*f},m=me(),far=Math.hypot(m.x-P.x,m.y-P.y);
  if(c.k==='via')S.push({k:'walk',to:()=>standAt(c.poi,12)});
  else if(c.k==='meet'){}
  else if(c.k!=='sort'&&(!(c.k==='look'||c.k==='photo')||far>60))S.push({k:'walk',to:()=>standAt(P,['dev','board','rack','flag','pole','post','tripod'].includes(c.o)?8:7)});
  switch(c.k){
   case'take':case'find':S.push(go(dn,D*.5,{prog:pr(0,.54)}),go(up,D*.5,{prog:pr(.56,1),held:1}));break;
   case'give':{S.push(go(up,D*.55,{prog:pr(0,.54),held:1,rev:1}),go(dn,D*.45,{prog:pr(.56,1),rev:1}));const f=figFor(c.id,c.n);if(f&&Math.hypot(f.pt.x-P.x,f.pt.y-P.y)<220)S.push({k:'walk',to:()=>standAt(f.pt,9)},...talkSteps(f,'בבקשה — '+c.nm,null,true));c.fig=f;break}
   case'pick':case'plant':S.push(go('saPick',D,{cyc:.9,prog:pr(0,1)}));break;
   case'work':{const fx=c.opt.fx,p=fx==='stamp'?'saStamp':fx==='radio'?'saPhone':fx==='marshal'?'marshal':['dev','flag','post','tripod','pole'].includes(c.o)?'saFix':'saWork';S.push(go(p,D,{cyc:p==='marshal'?1.6:.8,prog:pr(0,1)}));break}
   case'check':S.push(go('saWrite',D,{cyc:.9,prog:pr(0,1)}));break;
   case'photo':S.push(go('saCam',D,{prog:pr(0,1)}));break;
   case'look':S.push(go('saCam',D,{prog:f=>{c.prog=f;if(c.tg){const g=lookTgt(c);if(g)c.tg=g}},hold:now=>c.opt.tgt==='span'&&(c.cars=spanCars())>0&&now-c.t0<20000&&(c.prog=Math.min(c.prog,.95),true)}));break;
   case'wear':S.push(go('saGive',D*.4,{prog:pr(0,.4)}),go('saHang',D*.6,{prog:pr(.4,1)}));break;
   case'hang':S.push(go('saHang',D,{prog:pr(0,1),held:1}));break;
   case'via':S.push(go('saGive',.9,{prog:pr(0,1),held:1}));break;
   case'sort':{const src=c.src,dstOf=()=>c.opt.car?carBack():c.dst;for(let i=c.cnt;i<c.q;i++)S.push({k:'walk',to:()=>standAt(src,8)},go('saDn',.45,{face:()=>src,on:()=>{c.phase='work'}}),go('saUp',.45,{face:()=>src,held:1,on:()=>{c.phase='work';c.inHand=1}}),
     {k:'walk',to:()=>standAt(dstOf(),8)},go('saUp',.45,{face:dstOf,held:1,rev:1}),{k:'fn',fn:T=>{c.inHand=0;c.cnt++;c.prog=c.cnt/c.q;const d=dstOf();SA.fx.push({k:'land',x:d.x,y:d.y,t0:T||pnow()});if(c.cnt<c.q&&!E.qa)try{toast(c.v+' — '+c.cnt+' מתוך '+c.q)}catch(e){}}});break}
   case'meet':{const s=ST()[c.id].steps[c.n-1],line=s.msg&&s.msg[1]?String(s.msg[1]).slice(0,130):'';
    if(c.opt.boat){S.push(go('saWave',1.3,{cyc:.8,face:()=>c.poi,prog:pr(0,1),bub:['player','הגעתי — '+(s.title||c.nm),1800]}));break}
    const f=figFor(c.id,c.n);c.fig=f;S.push(...meetSteps({fig:f,at:c.poi,hi:'הגעתי — '+(s.title||''),line,from:s.msg&&s.msg[0]}));S.push({k:'fn',fn:()=>{c.prog=1}});break}}
  return S}
 /* (3) שלב בכרטיס בלי פעולה (שיחה / המתנה שהגיעה): הכפתור → הטלפון נסגר → הולכים לדמות של השלב, לוחצים יד ומדברים (הכפתור — מה שהשחקן אומר, ההודעה — מה שהדמות עונה) → ההתקדמות */
 function plainOk(id,n){const S=ST()[id],s=S&&S.steps[n-1];return!!(s&&s.btn&&!s.fix&&!s.drive&&!s.__saDrive&&!spec(id,n))}
 function plainGo(id,n){const S=ST()[id],s=S&&S.steps[n-1];if(!s)return false;const f=figFor(id,n),P=poiPt(id,n),inCar=PlayerProfile.mode==='vehicle',nm=String(s.who||S.who||''),phone=/טלפון|בקשר/.test(nm);
  const line=s.msg&&s.msg[1]?String(s.msg[1]).slice(0,130):'',hi=s.btn||'',steps=[];let stay=false;try{stay=!!s.startJob&&!(MISSION_DEFS[s.startJob]||{}).walk}catch(e){}
  if(inCar&&(stay||Math.hypot(PlayerCar.x-P.x,PlayerCar.y-P.y)>450))steps.push({k:'pose',p:null,d:1.1,bub:['player',hi,1800]});   /* עבודה שמתחילה ברכב — נשארים ברכב */
  else{if(inCar)steps.push({k:'exit'});steps.push(...meetSteps({fig:phone?null:f,at:P,hi,line,phone,from:s.msg&&s.msg[0]}))}
  steps.push({k:'fn',fn:()=>{if(step(id)!==n)return;E.plain=(E.plain||0)+1;try{S9STORY.advance(id)}catch(e){err('advance',e)}try{if(State.phoneOpen)renderPhone()}catch(e){}}});
  psRun(steps,{tag:'card:'+id+'#'+n,fig:phone?null:f,hud:(hi||'הלאה')+(f?' — '+f.name:''),cancel:w=>{if(w!=='replace'&&!E.qa)try{toast('נעצר — הכפתור בכרטיס שוב, כשמוכנים')}catch(e){}}});return true}
 /* (4) הסיפור הראשי (074ze — בלי שינוי בו): השיחה / העבודה / הסרט של השלב — לא נפתחים כשעוצרים ליד; טבעת F ליד הדמות (הנותן) / המקום;
    F (ברכב — יוצא) → הולך, לוחץ יד, מדבר / מקבל את המסמכים וחוזר לרכב / קונה כרטיס → ואז אותה קריאה בדיוק */
 const MS={cur:null,allow:null,dry:null,n:{talk:0,job:0,show:0},go:0,armed:0};
 const stCur=()=>{try{return typeof TCSTORY!=='undefined'?TCSTORY.cur():null}catch(e){return null}},stQa=()=>{try{return!!(TCSTORY.E&&TCSTORY.E.qa)}catch(e){return false}};
 const poiAt=id=>{try{const p=navPoiRegistry()[id];return p?{x:p.x,y:p.y}:null}catch(e){return null}};
 function msWho(kind,key,C){try{const D=TCSTORY.D;if(kind==='talk')return(D.dialogs[key]||{}).who||'';for(const ch of D.chapters||[])for(const m of ch.missions||[])if(m.id===C.mi)return m.giver||''}catch(e){}return''}
 function msArm(kind,key,s,args){const C=stCur();if(!C)return;const q=MS.cur;if(q&&q.kind===kind&&q.key===key&&q.mi===C.mi&&q.step===C.step)return;
  const who=msWho(kind,key,C);let name='';try{name=who?(g77S().chars[who]||{}).name||'':''}catch(e){}let label='';try{if(kind==='job')label=(MISSION_DEFS[key]||{}).name||key;if(kind==='show'){const [kd,fid]=key.split(':'),L=kd==='film'?TCSHOW.FILMS:TCSHOW.PLAYS;label=((L||[]).find(f=>f.id===fid)||{}).title||''}}catch(e){}
  MS.cur={kind,key,s,mi:C.mi,step:C.step,args,at:poiAt(s.at||s.nav),r:s.r||150,who,name,label,born:pnow()};MS.armed++;if(!E.qa)try{toast(msHud(true)||'F')}catch(e){}}
 {const O=g77DlgOpen;g77DlgOpen=function(id,mode,at,resume){try{if(mode==='talk'&&!resume&&MS.allow!==id&&!stQa()){const C=stCur();if(C&&C.s&&C.s.talk===id){msArm('talk',id,C.s);return false}}}catch(e){err('dlg',e)}return O.apply(this,arguments)}}
 {const O=startMission;startMission=function(id){try{if(MS.allow!==id&&!stQa()&&typeof TCSTORY!=='undefined'&&TCSTORY.E&&TCSTORY.E.allowJob===id){const C=stCur();if(C&&C.s&&C.s.job===id){msArm('job',id,C.s);return}}}catch(e){err('job',e)}return O.apply(this,arguments)}}
 try{if(typeof TCSHOW!=='undefined'&&TCSHOW.open){const O=TCSHOW.open;TCSHOW.open=function(kind,i){try{const ev=window.event;if(MS.allow!=='show'&&!stQa()&&!(ev&&ev.isTrusted&&ev.type==='click')){const C=stCur(),L=kind==='film'?TCSHOW.FILMS:TCSHOW.PLAYS,f=L&&L[i];
    if(C&&C.s&&C.s.show&&f&&C.s.show===kind+':'+f.id){msArm('show',C.s.show,C.s,[...arguments]);return false}}}catch(e){err('show',e)}return O.apply(this,arguments)}}}catch(e){err('show-w',e)}
 function msTick(now){const q=MS.cur;if(!q)return;const C=stCur();if(!C||!C.s||C.mi!==q.mi||C.step!==q.step||C.s!==q.s){if(!(PS.q&&String(PS.q.o.tag).indexOf('ms:')===0))MS.cur=null;return}
  if(q.kind==='job'&&PlayerProfile.activeMission&&PlayerProfile.activeMission.id===q.key){MS.cur=null;return}
  if(q.who&&q.kind==='job'&&!PS.q&&q.at&&now-(q.figT||0)>1000){q.figT=now;const m=me();if(Math.hypot(m.x-q.at.x,m.y-q.at.y)<900)try{tcStepFig(q.who,q.at,{src:'sa-job',until:2500,r:14})}catch(e){}}}   /* הנותן מחכה ליד המקום (הדמות האחת) */
 function msFig(q){if(!q.who)return null;let f=null;try{f=tcStepFig(q.who);if(!f&&q.at)f=tcStepFig(q.who,q.at,{src:'sa-ms',until:20000,r:14})}catch(e){}return f&&f.pt?f:null}
 function msHud(arm){const q=MS.cur;if(!q||!q.at)return'';const m=me(),d=Math.hypot(m.x-q.at.x,m.y-q.at.y);if(!arm&&d>Math.max(q.r,120)*2.2)return'';const out=walk()?'':'לצאת מהרכב ו';
  return q.kind==='talk'?'F · '+out+'לגשת ולדבר עם '+(q.name||'הדמות'):q.kind==='job'?'F · '+out+'לקבל את העבודה'+(q.name?' מ'+q.name:'')+(q.label?' — '+q.label:''):'F · '+out+'לקנות כרטיס'+(q.label?' — '+q.label:'')}
 function msF(){const q=MS.cur;if(!q||PS.q||cut()||!q.at)return false;const m=me(),f=q.who?FIG[q.who]:null,P=f&&f.pt||q.at,d=Math.min(Math.hypot(m.x-q.at.x,m.y-q.at.y),Math.hypot(m.x-P.x,m.y-P.y));if(d>Math.max(q.r,120))return false;
  if(q.kind==='job'&&!q.s.walk&&walk()&&Math.hypot(PlayerCar.x-PlayerPed.x,PlayerCar.y-PlayerPed.y)>400){try{toast('העבודה מתחילה ברכב — חוזרים לרכב, ואז F')}catch(e){}return true}
  msGo(q);return true}
 function msGo(q){const inCar=PlayerProfile.mode==='vehicle',f=q.kind==='show'?null:msFig(q),steps=[];if(inCar)steps.push({k:'exit'});
  if(q.kind==='show')steps.push({k:'walk',to:()=>standAt(q.at,12)},{k:'pose',p:'saPay',d:1.4,face:()=>q.at,bub:['player','כרטיס אחד, בבקשה'+(q.label?' — '+q.label:''),1900]},{k:'fn',fn:T=>{SA.fx.push({k:'land',x:q.at.x,y:q.at.y,t0:T||pnow()})}});
  else{steps.push(...meetSteps({fig:f,at:q.at,hi:'שלום'+(q.name?', '+q.name:'')+'!',line:q.kind==='job'?'הנה המסמכים — יוצאים לדרך.':'',walkMax:600}));
   if(q.kind==='job'){steps.push({k:'pose',p:'saGive',d:.8,rev:1,face:()=>f&&f.pt||q.at,fig:'saGive'},{k:'fn',fn:()=>{MS.paper=1}});
    if(!q.s.walk)steps.push({k:'walk',to:()=>standAt({x:PlayerCar.x,y:PlayerCar.y},14),carry:1},{k:'enter',must:true})}}
  steps.push({k:'fn',fn:()=>msFire(q)});MS.cur=q;
  psRun(steps,{tag:'ms:'+q.kind,fig:f,hud:msHud(true).replace(/^F · (לצאת מהרכב ו)?/,''),cancel:w=>{MS.paper=0;if(w!=='replace'&&!E.qa)try{toast('נעצר — F כדי להתחיל שוב')}catch(e){}}})}
 function msFire(q){MS.cur=null;MS.paper=0;MS.go++;MS.n[q.kind]++;if(MS.dry){MS.dry.push({kind:q.kind,key:q.key,mode:PlayerProfile.mode});return}
  if(q.kind==='talk'){MS.allow=q.key;try{g77DlgOpen(q.key,'talk')}finally{MS.allow=null}}
  else if(q.kind==='job'){const E2=TCSTORY.E;MS.allow=q.key;E2.allowJob=q.key;try{const m=TCSTORY.M();if(m&&m.race)m.race.t0=Date.now();startMission(q.key)}finally{E2.allowJob=null;MS.allow=null}}
  else if(q.kind==='show'){MS.allow='show';try{TCSHOW.open.apply(TCSHOW,q.args||[])}finally{MS.allow=null}}}
 /* (5) הדמות שמחכה: תנועת המתנה ('wait' של P34 — המשקל, מבט בשעון), מסתובבת לאט אל השחקן (מ-30 מ׳), מנופפת כשהוא מגיע (13 מ׳), ומדברת בזמן השיחה שלה */
 function figIdle(q,now,d,m,x,y){const tgt=Math.atan2(m.y-y,m.x-x);if(q.hdS==null)q.hdS=d<300?tgt:Math.PI/2;const want=d<300?tgt:Math.PI/2+.55*Math.sin(now/2600+(hsh(q.id)%7));
  const dt=Math.min(.12,Math.max(0,(now-(q.idT||now))/1000));q.idT=now;q.hdS+=Math.atan2(Math.sin(want-q.hdS),Math.cos(want-q.hdS))*Math.min(1,dt*3.5);
  if(d<130&&!q.waved&&q.arrived!==false){q.waved=1;q.wave=now}if(d>260)q.waved=0;let k='wait',ph=(now/4800+(hsh(q.id)%10)/10)%1;if(q.wave&&now-q.wave<1500){k='saWave';ph=((now-q.wave)/700)%1}
  try{const O=g77S().open;if(O&&O.mode==='talk'&&d<140&&typeof TCSTORY!=='undefined'&&(TCSTORY.D.dialogs[O.id]||{}).who===q.id){k='saTalk';ph=(now/1100)%1}}catch(e){}
  return{k,hd:q.hdS,ph}}
 /* (6) הבדיקות */
 /* הסיפור הראשי: כל שלב שיחה / עבודה / סרט — כשעוצרים ליד (ברכב ורגל) כמו המנוע, לא נפתח; F — הרצף (יציאה, הליכה, לחיצת יד) ואז אותה קריאה (כאן בלי לפתוח — נרשם) */
 function msCheck(){const out={ok:true,bad:[],n:{talk:0,job:0,show:0},fired:{talk:0,job:0,show:0},walk:0,shake:0,exit:0};if(typeof TCSTORY==='undefined'||!TCSTORY.D){out.note='אין TCSTORY';return out}
  const keep=JSON.stringify(g77St()),mode=PlayerProfile.mode,px=PlayerPed.x,py=PlayerPed.y,cx=PlayerCar.x,cy=PlayerCar.y,ch0=PlayerCar.heading,csp=PlayerCar.speed,am=PlayerProfile.activeMission,keepCur=MS.cur,E2=TCSTORY.E,cool0=JSON.stringify(E2.cool||{}),cam={x:Camera.x,y:Camera.y,z:Camera.zoom},keepN=State.navigation;
  MS.dry=[];E.qa++;
  try{for(const ch of TCSTORY.D.chapters||[])for(const mi of ch.missions||[])mi.steps.forEach((s,k)=>{const kind=s.talk?'talk':s.job?'job':s.show?'show':null;if(!kind)return;const tag=mi.id+'#'+(k+1)+' '+kind;out.n[kind]++;
    try{const at=poiAt(s.at);if(!at){out.bad.push(tag+': אין מקום');return}
     for(const md of['vehicle','walk']){const st=g77St();st.main={v:1,on:true,ch:ch.id,mi:mi.id,step:k,st:{},done:{},rows:[],sent:{},q:[],pc:[],news:[],van:null,began:0};if(s.talk)delete st.flags['st:'+s.talk];MS.cur=null;PlayerProfile.activeMission=null;
      if(md==='vehicle'){let ok=false;try{ok=!!TCSTORY.bring(s.at)}catch(e){}if(!ok){PlayerProfile.mode='vehicle';PlayerCar.x=at.x;PlayerCar.y=at.y}PlayerCar.speed=0}else{PlayerProfile.mode='walk';const w=walkNear({x:at.x+20,y:at.y+12});PlayerPed.x=w.x;PlayerPed.y=w.y}
      if(kind==='talk')g77DlgOpen(s.talk,'talk');else if(kind==='job'){E2.allowJob=s.job;try{startMission(s.job)}finally{E2.allowJob=null}}else{const [kd,fid]=s.show.split(':'),L=kd==='film'?TCSHOW.FILMS:TCSHOW.PLAYS;TCSHOW.open(kd,L.findIndex(f=>f.id===fid),{place:'qa',onEnd(){}})}   /* כמו 074ze:runStep כשעוצרים ליד */
      const opened=kind==='talk'?!!g77S().open:kind==='job'?!!PlayerProfile.activeMission:!!TCSHOW.on;
      if(opened){out.bad.push(tag+' ('+md+'): נפתח בלי הפעלה');try{if(kind==='talk')g77DlgClose(true);else if(kind==='job')PlayerProfile.activeMission=null;else TCSHOW.close()}catch(e){}continue}
      if(!MS.cur||MS.cur.kind!==kind){out.bad.push(tag+' ('+md+'): אין טבעת F');continue}
      const d0=MS.dry.length;if(!msF()){out.bad.push(tag+' ('+md+'): F לא התחיל');continue}const L=psFast();
      if(MS.dry.length!==d0+1){out.bad.push(tag+' ('+md+'): לא נפתח אחרי F ('+(PS.why||'')+')');continue}out.fired[kind]++;if(L&&L.dist>2)out.walk++;if(L&&L.seen.includes('saShake'))out.shake++;if(L&&L.seen.includes('exit'))out.exit++;
      if(md==='vehicle'&&!L.seen.includes('exit'))out.bad.push(tag+': לא יצא מהרכב');if(kind==='job'&&!s.walk&&MS.dry[MS.dry.length-1].mode!=='vehicle')out.bad.push(tag+': העבודה לא מהרכב')}}
    catch(e){out.bad.push(tag+': '+String(e&&e.message||e).slice(0,100))}})}
  catch(e){out.bad.push('שגיאה: '+String(e&&e.message||e).slice(0,120))}
  finally{psStop('qa');MS.dry=null;MS.cur=keepCur;E.qa--;try{if(g77S().open)g77DlgClose(true)}catch(e){}PlayerProfile.story=JSON.parse(keep);PlayerProfile.mode=mode;PlayerPed.x=px;PlayerPed.y=py;PlayerCar.x=cx;PlayerCar.y=cy;PlayerCar.heading=ch0;PlayerCar.speed=csp;PlayerProfile.activeMission=am;
   try{E2.cool=JSON.parse(cool0)}catch(e){}E2.last=null;Camera.x=cam.x;Camera.y=cam.y;Camera.zoom=cam.z;State.navigation=keepN;loadedFrom=g77St()}
  out.ok=!out.bad.length;return out}
 /* שלבי הכרטיס בלי פעולה: לא זזים לבד; הכפתור → הרצף (הליכה, לחיצת יד, דיבור) → ההתקדמות רק בסוף */
 function plainCheck(){const out={ok:true,n:0,adv:0,walk:0,shake:0,talk:0,phone:0,car:0,bad:[]};const keep=JSON.stringify(g77St()),m0=PlayerProfile.money,mode=PlayerProfile.mode,px=PlayerPed.x,py=PlayerPed.y,am=PlayerProfile.activeMission,keepN=State.navigation,keepI=State.interactionId;
  let tx0=0,cert0='{}';try{tx0=ensureEconomySchema().transactions.length;cert0=JSON.stringify(ensureActivitySchema().certs||{})}catch(e){}E.qa++;PlayerProfile.activeMission={id:'qa-actions2'};   /* עבודה שמתחילה בשלב (startJob) — לא מתחילה בבדיקה */
  try{for(const [id,S] of Object.entries(ST()))S.steps.forEach((s,k)=>{const n=k+1;if(!plainOk(id,n))return;out.n++;const tag=id+'#'+n;
    try{const f=fl();f['s9:'+id]=n;delete f['s9:'+id+':done'];SA.cur=null;const P=poiPt(id,n),w=walkNear({x:P.x+20,y:P.y+14});PlayerProfile.mode='walk';PlayerPed.x=w.x;PlayerPed.y=w.y;
     const n0=step(id);for(let i=0;i<5;i++)tick(pnow());if(step(id)!==n0){out.bad.push(tag+': זז לבד');return}
     if(!plainGo(id,n)){out.bad.push(tag+': לא התחיל');return}if(step(id)!==n0){out.bad.push(tag+': התקדם לפני הרצף');return}
     const L=psFast(),n2=step(id),last=n>=S.steps.length;if(last?!(done(id)||n2===0):n2!==n+1){out.bad.push(tag+': לא התקדם ('+(PS.why||'')+')');return}out.adv++;
     if(L){if(L.dist>2)out.walk++;if(L.seen.includes('saShake'))out.shake++;if(L.seen.includes('saTalk'))out.talk++;if(L.seen.includes('saPhone'))out.phone++;if(!L.seen.some(q=>SAP_ACT[q]))out.bad.push(tag+': בלי אנימציה')}}
    catch(e){out.bad.push(tag+': '+String(e&&e.message||e).slice(0,90))}finally{try{PlayerProfile.story=JSON.parse(keep)}catch(e){}loadedFrom=g77St()}})}
  finally{psStop('qa');E.qa--;PlayerProfile.activeMission=am;PlayerProfile.money=m0;PlayerProfile.mode=mode;PlayerPed.x=px;PlayerPed.y=py;State.navigation=keepN;State.interactionId=keepI;try{PlayerProfile.story=JSON.parse(keep)}catch(e){}
   try{const w=ensureEconomySchema();w.transactions.splice(tx0);ensureActivitySchema().certs=JSON.parse(cert0)}catch(e){}SA.cur=null;loadedFrom=g77St()}
  out.ok=!out.bad.length;return out}
 /* התנוחות: כל אחת נבנית באמת בצייר (P34.sprites) — בלי שגיאה, ושונה מעמידה */
 function poseCheck(){const out={ok:true,bad:[],n:0};try{const L=plLook(null,null)||{h:1.76};if(!(window.P34X&&P34X.__sap))out.bad.push('השרשור של P34X.pose לא הותקן');const st=JSON.stringify(P34.parts(L,{k:'stand'},2,0).parts.map(p=>p.pts).slice(0,40));
   for(const k of Object.keys(SAP_ACT)){out.n++;const F=sapF(k);if(P34.FR[k]!==F)out.bad.push(k+': FR');const A=P34.parts(L,{k},2,F>1?Math.floor(F/2):0).parts;if(!A||!A.length){out.bad.push(k+': ריק');continue}if(JSON.stringify(A.map(p=>p.pts).slice(0,40))===st)out.bad.push(k+': כמו עמידה')}
   if(P34X.err)out.bad.push('P34X.err: '+P34X.err)}catch(e){out.bad.push(String(e&&e.message||e).slice(0,120))}out.ok=!out.bad.length;return out}
 /* קיצורים לאחרים / לבדיקה */
 window.addEventListener('keydown',e=>{try{if(!PS.q||e.repeat)return;if(/^(KeyW|KeyA|KeyS|KeyD|ArrowUp|ArrowDown|ArrowLeft|ArrowRight|Escape)$/.test(e.code||''))psStop('key')}catch(x){}},true);
