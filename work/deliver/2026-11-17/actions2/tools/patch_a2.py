import sys,io
P=sys.argv[1];B=sys.argv[2]
s=open(P,encoding='utf-8').read();block=open(B,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: raise SystemExit('MISS (%d): %s'%(n,old[:90]))
    s=s.replace(old,new)
# (1) SA_DRIVE: 3 more arrivals (meet), the boat; comment
rep("var SA_DRIVE={'S9-ST-E4':{3:{car:1}},","var SA_DRIVE={'F3-ST-FISH3':{2:{car:1,boat:1}},'S9-ST-E4':{3:{car:1}},")
rep("'ZS-B3':{4:['work','dev'","'ZS-B3':{2:{meet:1},4:['work','dev'")
rep("'ZS-B2':{2:['give','bag','#c9a46a','הארוחה של עזריאל']},","'ZS-B2':{2:['give','bag','#c9a46a','הארוחה של עזריאל'],3:{meet:1}},")
rep("   (מוסרים / לוקחים / מחליפים / סופרים / מרכיבים) קורית כשמגיעים: החפץ והטבעת במקום, F, ורק אז התקדמות (במקום ההתקדמות לבד בקרבה) */",
    "   (מוסרים / לוקחים / מחליפים / סופרים / מרכיבים) קורית כשמגיעים: החפץ והטבעת במקום, F, ורק אז התקדמות (במקום ההתקדמות לבד בקרבה)\n   actions2: {car / meet / boat} — הגעה: הטבעת כשמגיעים (car — רק כשהגעת ברכב / במונית; boat — בסירה), F (ברכב — יוצאים), הולכים לדמות, לוחצים יד ומדברים — ורק אז ההתקדמות */")
# (2) verbs
rep("via:'להמשיך'};","via:'להמשיך',meet:'לגשת'};")
rep("hang:2.2,plant:3};","hang:2.2,plant:3,meet:1};")
# (3) spec: the arrivals
rep("const spec=(id,n)=>{let a=SA_SPEC[id]&&SA_SPEC[id][n];if(!a){const d=SA_DRIVE[id]&&SA_DRIVE[id][n];if(Array.isArray(d))a=d}if(!a)return null;",
    "const spec=(id,n)=>{let a=SA_SPEC[id]&&SA_SPEC[id][n];if(!a){const d=SA_DRIVE[id]&&SA_DRIVE[id][n];if(Array.isArray(d))a=d;else if(d){let t='';try{const s=ST()[id].steps[n-1];t=String(s.who||ST()[id].who||s.title||'').split(/\\s*[—(]/)[0]}catch(e){}a=['meet','none','#2f6fd0',t||'המקום',d]}}if(!a)return null;")
# (4) drvInstall: radius 0 always (no engine advances by proximity); drvTick: arm the arrivals
old_inst="try{Object.defineProperty(s,'drive',{configurable:true,enumerable:true,get(){return car&&(!walk()||State.taxiRide&&State.taxiRide.phase==='riding')?real:[real[0],real[1],0]},set(v){}});DRV.push({id,n,real,car,s})}catch(e){err('drv',e)}}}}"
new_inst="try{Object.defineProperty(s,'drive',{configurable:true,enumerable:true,get(){return[real[0],real[1],0]},set(v){}});DRV.push({id,n,real,car,meet:!Array.isArray(d),boat:!Array.isArray(d)&&!!d.boat,s})}catch(e){err('drv',e)}}}}   /* actions2: גם ברכב — רדיוס 0; ההגעה — כאן (drvTick), וההתקדמות רק אחרי F */"
rep(old_inst,new_inst)
old_tick="function drvTick(){for(const q of drvNow()){const a=me(),d=Math.hypot(a.x-q.real[0],a.y-q.real[1]);if(q.car){q.near=d<q.real[2];continue}"
new_tick=("function drvTick(){const T=pnow();for(const q of drvNow()){const a=me(),d=Math.hypot(a.x-q.real[0],a.y-q.real[1]),inV=!walk()||!!(State.taxiRide&&State.taxiRide.phase==='riding')||!!(q.boat&&isAboard());q.near=d<q.real[2];if(inV&&q.near)q.carT=T;"
 "if(q.meet){const o=SA.cur;if(PS.q||o&&o.id===q.id&&o.n===q.n)continue;if(o&&o.phase!=='go')continue;const ok=q.car?q.near&&(inV||T-(q.carT||-1e9)<90000):d<Math.max(q.real[2],46);if(ok){if(o)SA.cur=null;const c=arm(q.id,false);if(c)c.R=Math.max(c.R,q.real[2]+20)}continue}")
rep(old_tick,new_tick)
# (5) F: after F — the player's sequence (walk + the poses of the kind), from the car — out first
old_F_start="function F(){const c=SA.cur;if(!c||c.phase!=='go'||c.k==='via'||cut())return false;"
new_F_start="function F(){const c=SA.cur;if(!c||c.phase!=='go'||cut()||PS.q)return false;if(c.k==='via'){const m=me();if(Math.hypot(m.x-c.poi.x,m.y-c.poi.y)>Math.max(90,c.R))return false;return actGo(c)}"
rep(old_F_start,new_F_start)
old_F_end="  if(!walk()){try{toast('E — לצאת מהרכב, ואז F: '+c.v)}catch(e){}return true}\n  if(c.k==='sort'&&c.opt.car&&!carNear(c)){try{toast('הרכב שלך רחוק — מביאים אותו עד 15 מ׳ מהארגזים')}catch(e){}return true}\n  c.phase='work';c.t0=pnow();c.prog=0;c.ax=PlayerPed.x;c.ay=PlayerPed.y;c.hd=Math.atan2(c.pt.y-PlayerPed.y,c.pt.x-PlayerPed.x);if(c.k==='look'){c.tg=lookTgt(c);if(c.tg){c.dur=Math.max(c.dur,3800);c.hd=Math.atan2(c.tg.y-PlayerPed.y,c.tg.x-PlayerPed.x);E.lookReal=(E.lookReal||0)+1}}E.f++;return true}"
new_F_end=("  if(c.k==='sort'&&c.opt.car&&!carNear(c)){try{toast('הרכב שלך רחוק — מביאים אותו עד 15 מ׳ מהארגזים')}catch(e){}return true}\n"
 "  return actGo(c)}\n"
 " /* actions2: F → (ברכב — יוצאים קודם) → הרצף: הולכים אל החפץ / הדמות, והתנוחות של הסוג; ההתקדמות (finish → advance) רק בסוף הרצף */\n"
 " function actGo(c){const boat=c.opt.boat&&isAboard();if(!walk()&&!boat){let ok=false;try{ok=!!exitVehicle()}catch(e){}if(!ok)return true}\n"
 "  c.t0=pnow();c.prog=0;c.ax=PlayerPed.x;c.ay=PlayerPed.y;c.hd=Math.atan2(c.pt.y-PlayerPed.y,c.pt.x-PlayerPed.x);if(c.k==='look'){c.tg=lookTgt(c);if(c.tg){c.dur=Math.max(c.dur,3800);c.hd=Math.atan2(c.tg.y-PlayerPed.y,c.tg.x-PlayerPed.x);E.lookReal=(E.lookReal||0)+1}}\n"
 "  c.ps=1;c.phase='walk';E.f++;psRun(actSteps(c),{tag:c.id+'#'+c.n,fig:null,hud:c.v+' — '+c.nm,done:T=>{if(c.fig)psFig(c.fig,null);if(SA.cur===c&&c.phase!=='done')finish(c,T)},\n"
 "   cancel:w=>{if(c.fig)psFig(c.fig,null);c.inHand=0;if(c.phase!=='done'){c.phase='go';c.prog=0;c.ps=0;E.cancel++;if(w!=='replace'&&!E.qa)try{toast('הפעולה נעצרה — F כדי להתחיל שוב')}catch(e){}}}});\n"
 "  const q=PS.q;if(q&&c.fig)q.o.fig=c.fig;return true}\n"
 " function isAboard(){try{return!!((PlayerProfile.worldPersistent||{}).fish3||{}).aboard}catch(e){return false}}")
rep(old_F_end,new_F_end)
# (6) tick: 'via' — not by itself any more; the old 'work' — only without the sequence
rep("  if(c.phase==='go'&&c.k==='via'){const m=me();if(walk()&&Math.hypot(m.x-c.poi.x,m.y-c.poi.y)<70){c.phase='done';E.via++;S9STORY.advance(c.id);SA.cur=null}return}\n  if(c.phase!=='work')return;",
    "  if(c.k==='via'&&c.phase==='go')return;   /* actions2: לא מתקדם לבד כשמגיעים — F במקום */\n  if(c.phase!=='work'||c.ps)return;")
rep("function tick(now){load();carryOk();wearOk();","function tick(now){load();carryOk();wearOk();try{msTick(now)}catch(e){err('msTick',e)}")
# (7) drawWorld: via ring, sort (the crates — in the hands of the player), the ring of the main story
rep("  if(q.k==='via'){ring(c,q.poi.x,q.poi.y,40,now,'→');return}",
    "  if(q.k==='via'){if(q.phase==='go'&&!cut()){const m=me();ring(c,q.poi.x,q.poi.y,40,now,Math.hypot(m.x-q.poi.x,m.y-q.poi.y)<90?'F':'→')}return}")
rep("  if(q.k==='sort'){const left=q.q-q.cnt-(w>0?1:0);","  if(q.k==='sort'){const left=q.q-q.cnt-(q.ps?(q.inHand?1:0):w>0?1:0);")
rep("   if(w>0){const a=q.src,b=dst,f=w*w*(3-2*w),x=a.x+(b.x-a.x)*f,y=a.y+(b.y-a.y)*f;thing(c,q.o,q.c,x,y,10+Math.sin(Math.PI*f)*6,now)}}",
    "   if(w>0&&!q.ps){const a=q.src,b=dst,f=w*w*(3-2*w),x=a.x+(b.x-a.x)*f,y=a.y+(b.y-a.y)*f;thing(c,q.o,q.c,x,y,10+Math.sin(Math.PI*f)*6,now)}}")
rep(" function drawWorld(now){const c=ctx;if(!(Camera.zoom>=.32))return;",
    " function drawWorld(now){const c=ctx;if(!(Camera.zoom>=.32))return;\n  {const mq=MS.cur;if(mq&&mq.at&&!PS.q&&!cut()){const f=mq.who?FIG[mq.who]:null,P=f&&f.pt&&!f.hide?f.pt:mq.at,m=me();if(inView(P.x,P.y,60)&&Math.hypot(m.x-P.x,m.y-P.y)<800)ring(c,P.x,P.y+5,f?16:26,now,'F')}}   /* actions2: הסיפור הראשי — F ליד הדמות / המקום */")
# (8) lookEx: sort — the crate only when it is in the hands
rep("   else if(q.k==='sort'){o='crate';col=q.c;pose='carry'}","   else if(q.k==='sort'){o=q.ps&&!q.inHand?null:'crate';col=q.c;pose=o?'carry':'stand'}")
# (9) the hooks: draw (the player in the poses), F, E, HUD, the card
rep(" {const D0=drawPlayerPed;drawPlayerPed=function(now){const t=pnow();try{tick(t);drawWorld(t);drawWho(t)}catch(e){err('draw',e)}if(VIS.v&&VIS.v.hide)return;const r=D0.apply(this,arguments);",
    " {const D0=drawPlayerPed;drawPlayerPed=function(now){const t=pnow();try{tick(t);if(PS.q&&!walk())psTick(t);drawWorld(t);drawWho(t)}catch(e){err('draw',e)}if(VIS.v&&VIS.v.hide)return;\n   if(PS.q){let ok=false;try{ok=psDraw(t)}catch(e){err('psdraw',e)}if(ok){try{drawFx(t)}catch(e){}return}}   /* actions2: השחקן בתנוחה של הרצף */\n   const r=D0.apply(this,arguments);")
rep(" {const I0=interactNearbyPoi;interactNearbyPoi=function(){try{if(VIS.v){visExit();return true}if(F())return true}catch(e){err('F',e)}return I0.apply(this,arguments)}}",
    " {const I0=interactNearbyPoi;interactNearbyPoi=function(){try{if(VIS.v){visExit();return true}if(PS.q)return true;if(msF())return true;if(F())return true}catch(e){err('F',e)}return I0.apply(this,arguments)}}")
rep(" {const H0=hudGoalText;hudGoalText=function(){try{const vh=visHud();if(vh)return vh;const q=SA.cur;if(q){",
    " {const H0=hudGoalText;hudGoalText=function(){try{const vh=visHud();if(vh)return vh;const q=SA.cur;\n    if(PS.q){const s=PS.q.steps[PS.q.i],c=q&&q.ps?q:null;return(c?c.v+(c.phase==='work'?'… '+Math.round(c.prog*100)+'%':'')+' — '+c.nm+(c.q>1?' · '+Math.min(c.q,c.cnt+1)+' מתוך '+c.q:''):(PS.q.o.hud||'…'))+(s&&s.k==='walk'?' · הולך':'')+' · חץ / E — לעצור'}\n    {const mh=msHud();if(mh)return mh}\n    if(q){")
rep("return(walk()?'':'E — לצאת מהרכב · ')+'F · '+q.v+' — '+q.nm","return'F · '+(walk()||q.opt.boat?'':'לצאת מהרכב ו')+q.v+' — '+q.nm")
rep("if(q.k==='via')return'להמשיך עם '+q.nm+' — עד המקום (ברגל)';","if(q.k==='via'){const m=me();return Math.hypot(m.x-q.poi.x,m.y-q.poi.y)<90?'F · להגיע עם '+q.nm+' ולהראות':'להמשיך עם '+q.nm+' — עד המקום (ברגל), ושם F'}")
rep("const qd=walk()&&drvNow().find(q=>q.car&&q.near);if(qd)return'השלב הזה — ברכב: E לרכב, ונוסעים עד הטבעת';",
    "const qd=walk()&&drvNow().find(q=>q.car&&q.near&&!q.boat&&!(pnow()-(q.carT||-1e9)<90000));if(qd)return'השלב הזה — ברכב: E לרכב, ונוסעים עד הטבעת';")
# the card: a plain step — "← במשחק" and a line of what happens
rep("    h=h.slice(0,i+b.length)+lab+h.slice(j);if(k>=0&&k<i)h=h.slice(0,k)+note+h.slice(k);else h=h.slice(0,i)+note+h.slice(i)}}catch(e){err('card',e)}return h}}",
    "    h=h.slice(0,i+b.length)+lab+h.slice(j);if(k>=0&&k<i)h=h.slice(0,k)+note+h.slice(k);else h=h.slice(0,i)+note+h.slice(i)}\n"
    "   for(const [id,S] of Object.entries(ST())){const n=step(id);if(n<1||SA_SPEC[id]&&SA_SPEC[id][n])continue;const s=S.steps[n-1];if(!s||s.poi!==poiId||!plainOk(id,n))continue;const b='<button class=\"primary\" data-s9-step=\"'+id+'\">',i=h.indexOf(b);if(i<0)continue;const j=h.indexOf('</button>',i),f=figFor(id,n);   /* actions2 */\n"
    "    const note=pnote('בעולם: '+(f?'ניגשים אל '+f.name+', לוחצים יד ומדברים':'ניגשים למקום ומדברים')+' — ואז השלב הבא'),k=h.lastIndexOf('<div class=\"phoneActions\">',i);h=h.slice(0,i+b.length)+h.slice(i+b.length,j)+' ← במשחק'+h.slice(j);if(k>=0&&k<i)h=h.slice(0,k)+note+h.slice(k);else h=h.slice(0,i)+note+h.slice(i)}}catch(e){err('card',e)}return h}}")
rep("const id=a.dataset.s9Step,n=step(id),sp=n>0&&spec(id,n);if(!sp)return;\n   if(sp.k==='via'&&carried()&&carried().id===id){const s=ST()[id].steps[n-1];const p=poiPt(id,n),m=me();if(Math.hypot(m.x-p.x,m.y-p.y)<90)return}",
    "const id=a.dataset.s9Step,n=step(id),sp=n>0&&spec(id,n);\n   if(!sp){if(n>0&&plainOk(id,n)){e.stopPropagation();e.preventDefault();try{setPhoneOpen(false)}catch(x){}plainGo(id,n)}return}   /* actions2: שלב בלי פעולה — הליכה, לחיצת יד ודיבור, ואז ההתקדמות */")
# (10) who: the arrivals too (the person waits at the end of the drive); the idle; the poses of the sequence
rep("function whoNow(){const L=[];for(const [id,S] of Object.entries(ST())){const n=step(id);if(n<1)continue;const s=S.steps[n-1];if(!s||s.__saDrive||s.drive)continue;",
    "function whoNow(){const L=[];for(const [id,S] of Object.entries(ST())){const n=step(id);if(n<1)continue;const s=S.steps[n-1];if(!s||(s.__saDrive||s.drive)&&!(isMeet(id,n)&&!(SA_DRIVE[id][n]||{}).boat))continue;")
rep("   if(!inView(x,y,40))continue;const d=Math.hypot(m.x-x,m.y-y),hd=walkHd!=null?walkHd:q.hd!=null?q.hd:d<90?Math.atan2(m.y-y,m.x-x):Math.PI/2;\n   try{P34.draw(ctx,x,y,q.look,{k:walkK||q.k||(d<60?'wait':'stand')},hd,walkK?((now/700)%1):(now/2400)%1,res)}",
    "   if(!inView(x,y,40))continue;const d=Math.hypot(m.x-x,m.y-y),I=walkK?null:figIdle(q,now,d,m,x,y),hd=walkHd!=null?walkHd:q.hd!=null?q.hd:I.hd,kk=walkK||q.k||I.k,ph=walkK?((now/700)%1):q.k?(SAP_ACT[q.k]?(now/900)%1:(now/2400)%1):I.ph;   /* actions2: המתנה חיה */\n   try{P34.draw(ctx,x,y,q.look,{k:kk},hd,ph,res)}")
# (11) updatePed / toggleVehicle: the sequence holds the player; E stops it
rep("try{const U0=updatePed;updatePed=function(dt){if(VIS.v){","try{const U0=updatePed;updatePed=function(dt){if(PS.q){try{psTick(pnow())}catch(e){err('ps',e);psStop('err')}return}if(VIS.v){")
rep("try{const V0=toggleVehicle;toggleVehicle=function(){if(VIS.v){visExit();return true}","try{const V0=toggleVehicle;toggleVehicle=function(){if(PS.q){psStop('E');return true}if(VIS.v){visExit();return true}")
# (12) check(): every step — not by itself (25 ticks + the engines' proximity, on foot and in a car), then F → the sequence (fast) → the animation and the progress
rep("drvInstall();out.drive={hand:0,car:0,bad:[]};","drvInstall();out.drive={hand:0,car:0,meet:0,bad:[]};out.anim={steps:0,walk:0,poses:{}};out.noAuto=0;")
rep("PlayerProfile.mode='vehicle';const b=q.s.drive[2];PlayerProfile.mode=m;if(!(a<.01&&b===q.real[2]))out.drive.bad.push(q.id+'#'+q.n+': '+a+' / '+b)}",
    "PlayerProfile.mode='vehicle';const b=q.s.drive[2];PlayerProfile.mode=m;if(!(a<.01&&b<.01))out.drive.bad.push(q.id+'#'+q.n+': '+a+' / '+b)}")
rep("...Object.keys(SA_DRIVE).map(id=>[id,Object.keys(SA_DRIVE[id]).filter(ns=>Array.isArray(SA_DRIVE[id][ns])),1])]","...Object.keys(SA_DRIVE).map(id=>[id,Object.keys(SA_DRIVE[id]),1])]")
rep("const n=+ns,sp=spec(id,n),tag=id+'#'+n+(isD?' (נסיעה)':'');out.n++;if(isD)out.drive.hand++;",
    "const n=+ns,sp=spec(id,n),tag=id+'#'+n+(isD?(sp.k==='meet'?' (הגעה)':' (נסיעה)'):'');out.n++;if(isD)out.drive[sp.k==='meet'?'meet':'hand']++;")
old_loop=("      PlayerProfile.mode='walk';PlayerPed.x=c.pt.x;PlayerPed.y=c.pt.y+6;if(sp.k==='look'&&sp.opt.tgt){const T=out.lookT||(out.lookT={n:0,real:0,none:[]});T.n++;if(lookTgt(c))T.real++;else T.none.push(tag)}\n"
 "      if(c.k==='sort'&&c.opt.car){PlayerCar.__sx=PlayerCar.x;PlayerCar.__sy=PlayerCar.y;PlayerCar.x=c.pt.x+40;PlayerCar.y=c.pt.y}\n"
 "      if(c.k==='via'){tick(pnow())}\n"
 "      else for(let r=0;r<(c.k==='sort'?c.q:1);r++){if(!F()){out.bad.push(tag+': F לא התחיל ('+r+')');break}if(c.phase!=='work'){out.bad.push(tag+': לא בעבודה');break}c.t0-=c.dur+50;tick(pnow());\n"
 "       if(c.k==='look'&&c.opt.tgt==='span'){const Q=out.span={cars:spanCars(),waited:c.phase==='work',tg:!!c.tg};if(Q.cars>0&&!Q.waited)out.bad.push(tag+': המפתח לא ריק ('+Q.cars+') — והתצפית לא חיכתה');if(c.phase==='work'){c.t0-=20050;tick(pnow())}}}\n"
 "      if(c.k==='sort'&&c.opt.car&&PlayerCar.__sx!=null){PlayerCar.x=PlayerCar.__sx;PlayerCar.y=PlayerCar.__sy;delete PlayerCar.__sx;delete PlayerCar.__sy}\n")
new_loop=("      {const B=c.k==='via'?c.poi:c.pt,w=walkNear({x:B.x+(c.k==='find'?12:28),y:B.y+6});PlayerProfile.mode='walk';PlayerPed.x=w.x;PlayerPed.y=w.y}if(sp.k==='look'&&sp.opt.tgt){const T=out.lookT||(out.lookT={n:0,real:0,none:[]});T.n++;if(lookTgt(c))T.real++;else T.none.push(tag)}\n"
 "      const car0={x:PlayerCar.x,y:PlayerCar.y,h:PlayerCar.heading,sp:PlayerCar.speed};if(c.k==='sort'&&c.opt.car){PlayerCar.x=c.pt.x+40;PlayerCar.y=c.pt.y}\n"
 "      /* actions2 (א): בלי הפעלה — 25 פעימות, והקרבה של המנועים (038a / 074zs: 'מרחק < drive[2]') ברגל וברכב — השלב לא זז והפעולה לא מתחילה */\n"
 "      {const n0=step(id);for(let i=0;i<25;i++)tick(pnow());let eng=false;const dr=s.drive;if(Array.isArray(dr)){const ps={x:PlayerPed.x,y:PlayerPed.y};for(const md of['walk','vehicle']){PlayerProfile.mode=md;const A=md==='walk'?PlayerPed:PlayerCar,ax=A.x,ay=A.y;A.x=s.__saDrive[0];A.y=s.__saDrive[1];if(Math.hypot(A.x-s.drive[0],A.y-s.drive[1])<s.drive[2])eng=true;A.x=ax;A.y=ay}PlayerProfile.mode='walk';PlayerPed.x=ps.x;PlayerPed.y=ps.y}\n"
 "       if(step(id)!==n0||eng||SA.cur!==c||c.phase!=='go'||PS.q){out.bad.push(tag+': מתקדם / מתחיל בלי הפעלה');continue}out.noAuto++}\n"
 "      /* (ב): F (בהגעה ברכב — מתוך הרכב: יוצאים) → הרצף בזמן מדומה: הליכה ותנוחה של פעולה — ורק בסוף ההתקדמות */\n"
 "      if(c.k==='meet'&&c.opt.car&&!c.opt.boat){let ok=false;try{ok=!!TCSTORY.bring(s.poi)}catch(e){}if(!ok){PlayerCar.x=c.pt.x;PlayerCar.y=c.pt.y}PlayerCar.speed=0;PlayerProfile.mode='vehicle'}\n"
 "      if(c.k==='find'&&!c.found){PlayerPed.x=c.pt.x+6;PlayerPed.y=c.pt.y+4;tick(pnow())}\n"
 "      if(!F()){out.bad.push(tag+': F לא התחיל');continue}if(step(id)!==n&&!(sp.k==='meet'&&false)){out.bad.push(tag+': התקדם לפני הרצף');continue}\n"
 "      const LL=psFast();if(!LL){out.bad.push(tag+': הרצף לא נגמר ('+(PS.why||'')+')');continue}{const A=out.anim;A.steps++;if(LL.dist>2)A.walk++;const pz=LL.seen.filter(k=>SAP_ACT[k]||k==='marshal');for(const k of pz)A.poses[k]=(A.poses[k]||0)+1;if(!pz.length)out.bad.push(tag+': בלי אנימציה של השחקן');if(sp.k==='meet'&&c.opt.car&&!c.opt.boat&&!LL.seen.includes('exit'))out.bad.push(tag+': לא יצא מהרכב')}\n"
 "      if(c.k==='look'&&c.opt.tgt==='span')out.span={cars:spanCars(),tg:!!c.tg,ms:LL.ms};\n"
 "      PlayerCar.x=car0.x;PlayerCar.y=car0.y;PlayerCar.heading=car0.h;PlayerCar.speed=car0.sp;PlayerProfile.mode='walk';\n")
rep(old_loop,new_loop)
# the layer test: after F — the sequence (walk / work)
rep("L.cutOff=cut();L.fOff=F();L.phaseOff=c.phase;if(!(L.cutOn&&!L.fOn&&L.phaseOn==='go'&&!L.cutOff&&L.fOff&&L.phaseOff==='work'))out.bad.push('השכבות: '+JSON.stringify(L))}",
    "L.cutOff=cut();L.fOff=F();L.phaseOff=c.phase;psStop('qa');if(!(L.cutOn&&!L.fOn&&L.phaseOn==='go'&&!L.cutOff&&L.fOff&&(L.phaseOff==='work'||L.phaseOff==='walk')))out.bad.push('השכבות: '+JSON.stringify(L))}")
rep("  finally{E.qa--;PlayerProfile.money=m0;PlayerProfile.mode=mode;","  finally{psStop('qa');E.qa--;PlayerProfile.money=m0;PlayerProfile.mode=mode;")
# (13) the block itself + the export
rep(" window.__TC_SACT={SA,E,spec,arm,F,tick,check,table,carried,demo,VIS,visStart,visExit,visCheck,FIG,tcStepFig,figCheck,",
    block+" window.__TC_SACT={SA,E,spec,arm,F,tick,check,table,carried,demo,VIS,visStart,visExit,visCheck,FIG,tcStepFig,figCheck,PS,MS,psRun,psStop,psFast,msCheck,plainCheck,poseCheck,plainGo,SAP_ACT,")
open(P,'w',encoding='utf-8').write(s)
print('ok',len(s))
