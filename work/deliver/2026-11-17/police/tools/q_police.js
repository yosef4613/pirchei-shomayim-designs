// q_police.js (police 17.11, עותק של q_qa51 של citysvc; D‑691: בריחה — בלי קנס ובלי חוב) — QA‑51 בתוך המשחק (שירותי העיר, 11.11): עבירות אמיתיות (רכב השחקן נוסע אל הולך רגל / אל ניידת), התגובה, הקנס, המרדף, השמירה.
// 09:20 (אחרי ההפעלה מחדש): ped — גם 'late' (הניידת לא הגיעה) נבדק: בלי קנס ובלי חוב (D‑691); ‏lost — עד 360 שנ׳ (המרדף מתחיל לפעמים אחרי ~76 שנ׳)
// 10:35: chase — המקום הרחוק נבחר הכי רחוק מהניידות (שלא תפגוש אותו ישר בלי מרדף); lost — הולך רגל רחוק מהניידות (כמו chase), שלא תהיה ניידת במקום
// node qa_tools/probe_c2.js <build> deliver/2026-11-11/citysvc/tools/q_qa51.js <out.json>
return (()=>{const L=SIM_LOOP,H=L.h;if(L.simNow==null)L.simNow=performance.now();
 const step=s=>{const n=Math.max(1,Math.round(s/H));for(let i=0;i<n;i++){simStep(H,L.simNow+H*1000);L.simNow+=H*1000}};
 const S=()=>window.__TC_SVC.state(),P=()=>PlayerProfile.worldPersistent.police||{},out={t0:Date.now(),steps:[]};
 const note=(k,v)=>{out[k]=v};State.mapQa=false;PlayerProfile.mode='vehicle';PlayerProfile.money=5000;step(4);
 const hlOf=(a,r)=>{try{return vehicleCollisionShape(a,r||'Sedan',0,0,0).halfLength||28}catch(e){return 28}};const myHl=hlOf(PlayerCar.asset,PlayerCar.ref);
 const place=(x,y,h,sp)=>{PlayerCar.x=x;PlayerCar.y=y;PlayerCar.heading=h;PlayerCar.speed=sp||0;PlayerCar.hitCooldown=0};
 const free=(x,y,h)=>!playerStaticBodyBlockedAt(x,y,h)&&!dynamicVehicleBlockedAt(x,y,h);
 /* drive into a target until a collision is counted (or 1.6 s); the speed is held (like holding W) */
 const ram=(sp)=>{const c0=PlayerCar.collisions||0;for(let i=0;i<32;i++){PlayerCar.speed=sp;step(.05);if((PlayerCar.collisions||0)>c0){PlayerCar.speed=0;return true}}PlayerCar.speed=0;return false};
 const runTill=(f,max)=>{let t=0;while(t<max){step(1);t+=1;if(f())return t}return -1};
 /* 0 — legal: 300 s of the world with the player in his car — 0 offences, 0 fines */
 {const a=S();step(300);const b=S();note('legal',{offenses:b.police.offenses-a.police.offenses,fines:b.police.fines-a.police.fines,disp:b.disp,ok:b.police.offenses===a.police.offenses&&!b.disp})}
 /* 1 — a civilian car (not an offence, D‑24): drive into a car that stands */
 {let done=null;for(let tr=0;tr<40&&!done;tr++){for(const v of TRAFFIC_CARS){if(v.kind!=='civilian'||Math.abs(v.speed||0)>.5||!v.c2)continue;const h=v.heading||0,d=hlOf(v.asset,v.ref)+myHl+5,x=v.x-Math.cos(h)*d,y=v.y-Math.sin(h)*d;if(!free(x,y,h))continue;
   const a=S();place(x,y,h,0);const hit=ram(110);step(2);const b=S();done={car:v.id,hit,notOffense:b.st.notOffense-a.st.notOffense,offenses:b.police.offenses-a.police.offenses,disp:!!b.disp,ok:hit&&b.police.offenses===a.police.offenses&&!b.disp};break}if(!done)step(3)}
  note('civilian',done||{skip:'no standing car'})}
 /* 3 — a patrol car at ~10 km/h (the first time — a warning; the same car stops on the spot) */
 {let r=null;const tEnd=CITYSVC.t+240;while(!r&&CITYSVC.t<tEnd){for(const v of TRAFFIC_CARS){if(!csvcIsPol(v)||v.csvc||Math.abs(v.speed||0)>.5||!v.c2)continue;const h=v.heading||0,d=hlOf(v.asset,v.ref)+myHl+5,x=v.x-Math.cos(h)*d,y=v.y-Math.sin(h)*d;if(!free(x,y,h))continue;
    const a=S(),m0=PlayerProfile.money;place(x,y,h,0);if(!ram(60))continue;const t=runTill(()=>!S().disp,120),b=S();r={car:v.id,closed:t,warn:b.police.warnings-a.police.warnings,offenses:b.police.offenses-a.police.offenses,money:PlayerProfile.money-m0,why:CITYSVC.done.slice(-1)[0],ok:b.police.warnings===a.police.warnings+1&&PlayerProfile.money===m0};break}if(!r)step(2)}
  note('policeWarn',r||{skip:'no standing patrol car'})}
 /* 2 — a pedestrian at ~17 km/h: the nearest patrol car comes, the player waits in his car — a fine, no wanted level */
 const polD=(x,y)=>{let m=1e9;for(const v of TRAFFIC_CARS)if(csvcIsPol(v))m=Math.min(m,Math.hypot(v.x-x,v.y-y));return m};
 const pedHit=(sp,road,far)=>{try{activeVehicleEco().damage=0}catch(e){}for(let tr=0;tr<60;tr++){for(const n of NPC_PEDESTRIANS){if(n.ghost>0)continue;if(road&&!pointRoad(n.x,n.y))continue;if(far&&polD(n.x,n.y)<far)continue;for(let k=0;k<8;k++){const h=k*Math.PI/4,d=myHl+7+8,x=n.x-Math.cos(h)*d,y=n.y-Math.sin(h)*d;if(!free(x,y,h))continue;if(road&&!pointRoad(x,y))continue;const a=S(),m0=PlayerProfile.money;place(x,y,h,road?sp:0);if(ram(sp)){const b=S();if(b.police.offenses>a.police.offenses)return{ped:n.id,a,m0,x:Math.round(x),y:Math.round(y)};}}}step(2)}return null};
 {const pd0=P().debt||0;const r=pedHit(100);if(!r)note('ped',{skip:'no pedestrian'});else{const D0=S().disp;const t=runTill(()=>!S().disp,260),b=S();const last=b.st.resp.slice(-1)[0];
   note('ped',{ped:r.ped,disp0:D0,closed:t,resp:last,why:CITYSVC.done.slice(-1)[0],money:PlayerProfile.money-r.m0,wanted:b.police.wanted,fines:P().fines.slice(-1),ok:t>0&&(CITYSVC.done.slice(-1)[0].why==='done'?PlayerProfile.money<r.m0&&b.police.wanted===0:CITYSVC.done.slice(-1)[0].why==='late'&&PlayerProfile.money===r.m0&&(P().debt||0)===pd0)})}}
 /* 4 — serious and repeated (~29 km/h, second offence in 10 min): wanted 2, the player leaves — the chase; he stops — caught (fine + 20%); the helicopter */
 {step(20);const r0=pedHit(100,false,1500);step(.5);const r=r0&&pedHit(100,false,1200);if(!r)note('chase',{skip:'no pedestrian far from the patrol cars'});else{const w=S().police.wanted;
   /* away: a road 800 px from the place (beyond the 600 px of the chase), the car stands there */
   let far=null,farD=-1;for(let k=0;k<16;k++){const a=k*Math.PI/8,px=r.x+Math.cos(a)*800,py=r.y+Math.sin(a)*800,pos=nearestRoadPosition(px,py,e=>!e.future&&!e.oneway);if(pos&&pos.d<60){const e=pos.edge,A=byNode[e.a],B=byNode[e.b],h=Math.atan2(B.y-A.y,B.x-A.x),q=trafficEdgePoint(e.id,1,pos.u);const lx=q.x+Math.cos(h+Math.PI/2)*14,ly=q.y+Math.sin(h+Math.PI/2)*14;if(free(lx,ly,h)){const pd=polD(lx,ly);if(pd>farD){farD=pd;far={x:lx,y:ly,h}}}}}
   if(far)place(far.x,far.y,far.h,0);const ph=[];let still=0,maxStill=0,lastPos=null,heliUp=false,t=0,mx=0;const m0=PlayerProfile.money;
   while(t<300){step(1);t++;const s=S();if(s.disp)ph.push(s.disp.ph);if(s.heli.pol&&s.heli.pol.busy)heliUp=true;const v=CITYSVC.disp&&CITYSVC.disp.car;
    if(v){if(lastPos&&Math.hypot(v.x-lastPos[0],v.y-lastPos[1])<2&&!(v.taxiRoute&&v.taxiRoute.hold))still++;else still=0;maxStill=Math.max(maxStill,still);lastPos=[v.x,v.y]}
    if(!s.disp&&!(s.heli.pol&&s.heli.pol.busy))break}
   const b=S(),dn=CITYSVC.done.slice(-1)[0];note('chase',{wanted0:w,far:!!far,phases:[...new Set(ph)],why:dn,money:PlayerProfile.money-m0,heliUp,heli:b.heli.pol,maxStillPol:maxStill,secs:t,wanted:b.police.wanted,ok:w>=2&&dn&&dn.why==='done'&&ph.includes('chase')&&heliUp&&b.heli.pol.done===b.heli.pol.ok&&b.heli.pol.done>=1})}}
 /* 4b — serious on the road (a crosswalk): over 25 km/h — the wanted level goes up by one (if there is a pedestrian on a crosswalk now) */
 {step(130);const w0=S().police.wanted;const r=pedHit(400,true);if(!r)note('serious',{skip:'no pedestrian on a road'});else{const o=CITYSVC.ev.slice(-1)[0];note('serious',{kmh:o.kmh,up:o.up,rep:o.rep,amt:o.amt,ok:o.kmh>25?o.up>=1:true});runTill(()=>!S().disp,200)}}
 /* 5 — lost: serious again, the player keeps moving away (jumps 400 px every 5 s) — after 60 s the chase ends; D‑691: no fine and no debt, only the wanted level */
 {const r0=pedHit(100,false,1500);step(4);const r=r0&&pedHit(100,false,1200);if(!r)note('lost',{skip:'no pedestrian'});else{let t=0;const d0=P().debt,m0=PlayerProfile.money,f0=(P().fines||[]).length;while(t<360){step(1);t++;const v=CITYSVC.disp&&CITYSVC.disp.car;if(v&&t%3===0){const dx=PlayerCar.x-v.x,dy=PlayerCar.y-v.y,d=Math.hypot(dx,dy)||1;if(d<1400){for(let k=0;k<12;k++){const a=Math.atan2(dy,dx)+(k%2?1:-1)*Math.ceil(k/2)*.3,px=v.x+Math.cos(a)*1700,py=v.y+Math.sin(a)*1700,pos=nearestRoadPosition(px,py,e=>!e.future&&!e.oneway);if(pos&&pos.d<80){const q=trafficEdgePoint(pos.edge.id,1,pos.u);PlayerCar.x=q.x;PlayerCar.y=q.y;PlayerCar.speed=0;break}}}}if(!S().disp)break}
   const dn=CITYSVC.done.slice(-1)[0];note('lost',{why:dn,debt:P().debt-d0,wanted:P().wanted,money:PlayerProfile.money-m0,fines:(P().fines||[]).length-f0,offs:dn&&dn.offs,ok:dn&&dn.why==='lost'&&P().debt===d0&&PlayerProfile.money===m0&&(P().fines||[]).length===f0&&dn.offs.every(x=>/:(escaped|warn-absent)$/.test(x))})}}
 /* 6 — the save: the police part goes out and comes back as it was */
 {const before=JSON.stringify(P());let ok=false,err=null;try{const sv=SaveManager.save('qa',{backup:false,silent:true});out.saveRes=sv;PlayerProfile.worldPersistent.police={v:1,wanted:3,debt:9,paid:0,fines:[],warnings:0,offenses:0,lastOff:0,clock:0,wantT:0};const r=SaveManager.load({silent:true});ok=JSON.stringify(PlayerProfile.worldPersistent.police)===before;note('save',{load:r&&r.ok,ok,wanted:P().wanted,debt:P().debt,fines:(P().fines||[]).length})}catch(e){err=String(e);note('save',{ok:false,err})}}
 /* 7 — the debt at the station: F at the door of A5 pays it, the place opens on the big screen */
 {if(!(P().debt>0))P().debt=320;PlayerProfile.money=Math.max(PlayerProfile.money,2000);const d0=P().debt,m0=PlayerProfile.money;PlayerProfile.mode='walk';PlayerPed.x=659;PlayerPed.y=3672;let open=null;try{interactNearbyPoi();open=window.__TC_PLACE?window.__TC_PLACE():null}catch(e){open={err:String(e)}}
  note('station',{debt0:d0,debt:P().debt,paid:m0-PlayerProfile.money,place:open,ok:d0>0?P().debt===0&&m0-PlayerProfile.money===d0:true});try{setPhoneOpen(false)}catch(e){}PlayerProfile.mode='vehicle'}
 const s=S();out.final=s;out.audit=window.__TC_SVC.audit();out.ms=Date.now()-out.t0;out.allOk=['legal','civilian','policeWarn','ped','chase','serious','lost','save','station'].every(k=>out[k]&&(out[k].ok||out[k].skip));
 return out})()
