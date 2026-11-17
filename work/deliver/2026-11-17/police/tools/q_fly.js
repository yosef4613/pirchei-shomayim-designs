// q_fly.js (police 17.11, D‑691) — רישיון טיס והטסה בתוך המשחק: מבחן המטוס הקל (LIC-14) ומבחן המסוק (LIC-16) עם הטייס האוטומטי של הבדיקה,
// טיסה חופשית, החזרה של המטוס ל-GA3, ההסתרה של כלי הטיס בחניה, השמירה והטעינה באמצע טיסה, הלוח בגדר.
// node qa_tools/probe_c2.js <build> deliver/2026-11-17/police/tools/q_fly.js <out.json>
return (async()=>{const F=window.__TC_FLY,out={t0:Date.now()},note=(k,v)=>{out[k]=v};if(!F)return{allOk:false,err:'no __TC_FLY'};
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));const poi=id=>S15_POIS[id];
 const at=id=>{PlayerProfile.mode='walk';State.mapQa=false;try{setPhoneOpen(false)}catch(e){}const p=poi(id);PlayerPed.x=p.x+6;PlayerPed.y=p.y;Camera.x=p.x;Camera.y=p.y};
 const run=(maxS,until)=>{const dt=1/30,tr=[];let t=0,zMax=0,vMax=0,lastI=-1;const c0=F.S.c;while(t<maxS){F.step(dt);t+=dt;const c=F.S.c;if(c){zMax=Math.max(zMax,c.z);vMax=Math.max(vMax,c.v)}const E=F.S.exam;if(E&&E.i!==lastI){tr.push([+t.toFixed(1),E.i,c?Math.round(c.x):null,c?Math.round(c.y):null,c?Math.round(c.z):null]);lastI=E.i}if(until())break}return{t:+t.toFixed(1),zMax:Math.round(zMax),vMax:Math.round(vMax),tr}};
 note('audit0',F.audit());
 PlayerProfile.money=5000;PlayerProfile.activeMission=null;delete PlayerProfile.licenses['LIC-14'];delete PlayerProfile.licenses['LIC-16'];
 /* 0 — הסטטוס בטלפון: LIC-14 זכאי, LIC-16 נעול (קודם LIC-14); מבחן מחוץ לשדה — ניווט אל הגדר, בלי אגרה */
 {at('S15-FENCE-GA');PlayerPed.x=2000;PlayerPed.y=2000;const m0=PlayerProfile.money,r=startLicenseTrial('LIC-14');note('far',{r,st14:licenseTrialStatus('LIC-14'),st16:licenseTrialStatus('LIC-16'),money:PlayerProfile.money-m0,nav:State.navigation&&State.navigation.targetId,ok:r&&r.err==='far'&&PlayerProfile.money===m0&&licenseTrialStatus('LIC-14')==='eligible'&&licenseTrialStatus('LIC-16')==='locked'})}
 /* 1 — הלוח בגדר (F — המסך הגדול) */
 {at('S15-FENCE-GA');let ok=false,h='';try{interactNearbyPoi();h=($('phoneBody')&&$('phoneBody').innerHTML)||'';ok=/data-fly="exam\|plane"/.test(h)&&/בית הספר לטיסה/.test(h)}catch(e){h=String(e)}note('card',{ok,len:h.length,place:window.__TC_PLACE?window.__TC_PLACE():null});try{setPhoneOpen(false)}catch(e){}}
 /* 2 — מבחן המטוס הקל: ההסעה, ההמראה, ארבע הטבעות, הנחיתה והעצירה — ואז E: המטוס חוזר ל-GA3 */
 {at('S15-FENCE-GA');const m0=PlayerProfile.money,r=startLicenseTrial('LIC-14');F.S.auto=true;const hidden=F.hide('PK-GA3');
  const x=run(900,()=>F.S.exam&&F.S.exam.res&&F.S.c&&F.S.c.z<=0&&F.S.c.v<10);const E=F.S.exam||{},res=E.res,why=E.why;const ex=F.exit();const back=run(300,()=>!F.S.c);F.S.auto=false;
  note('plane',{r,fee:m0-PlayerProfile.money,hidden,res,why,...x,exit:ex,back:back.t,home:!F.S.c,owned:F.lic('LIC-14'),ped:[Math.round(PlayerPed.x),Math.round(PlayerPed.y)],ok:!!(r&&r.ok&&res==='pass'&&F.lic('LIC-14')&&!F.S.c&&!F.hide('PK-GA3')&&m0-PlayerProfile.money===400)})}
 /* 3 — מבחן המסוק: ריחוף מעל H2, שתי טבעות, נחיתה ב-H2 */
 {at('S15-FENCE-HELI');const m0=PlayerProfile.money,r=startLicenseTrial('LIC-16');F.S.auto=true;const x=run(600,()=>F.S.exam&&F.S.exam.res&&F.S.c&&F.S.c.z<=0);const E=F.S.exam||{};const ex=F.exit();F.S.auto=false;
  note('heli',{r,fee:m0-PlayerProfile.money,res:E.res,why:E.why,...x,exit:ex,gone:!F.S.c,owned:F.lic('LIC-16'),ok:!!(r&&r.ok&&E.res==='pass'&&F.lic('LIC-16')&&!F.S.c&&m0-PlayerProfile.money===500)})}
 /* 4 — טיסה חופשית במסוק: השכרה, המראה, טיסה מעל העיר (מערבה), חזרה ונחיתה ב-H2; לא יורדים באוויר; הציור (פריימים אמיתיים) והסתרת המסוק בחניה */
 {at('S15-FENCE-HELI');const m0=PlayerProfile.money,r=F.start('heli');F.S.ctl={up:1};run(6,()=>false);F.S.ctl={up:1,f:1};run(4,()=>F.S.c.z>200);F.S.ctl={f:1,l:1};run(1.2,()=>false);F.S.ctl={f:1};const a=run(5,()=>false);
  const c=F.S.c,far=c?Math.round(Math.hypot(c.x-F.DEF.heli.home.x,c.y-F.DEF.heli.home.y)):0,z=c?Math.round(c.z):0;const ex0=F.exit();const still=!!F.S.on;
  F.S.ctl={};const d0=F.S.st.draw,h0=F.S.st.hide;await sleep(2500);const drawn=F.S.st.draw-d0;F.S.ctl=null;F.S.auto=true;const back=run(300,()=>F.S.c&&F.S.c.z<=0&&Math.hypot(F.S.c.x-F.DEF.heli.home.x,F.S.c.y-F.DEF.heli.home.y)<=60&&F.S.c.v<20);F.S.auto=false;
  const cam=[Math.round(Camera.x),Math.round(Camera.y)];const ex=F.exit();
  note('free',{r,fee:m0-PlayerProfile.money,far,z,airExitRefused:ex0===true&&still,drawn,hideCalls:F.S.st.hide-h0,cam,back:back.t,exit:ex,gone:!F.S.c,ok:!!(r&&r.ok&&far>500&&z>150&&still&&drawn>0&&!F.S.c&&m0-PlayerProfile.money===250)})}
 /* 5 — simStep מריץ את הטיסה (החיבור למשחק) */
 {at('S15-FENCE-HELI');F.start('heli');F.S.ctl={up:1};const t0=F.S.c.t,L=SIM_LOOP,H=L.h;if(L.simNow==null)L.simNow=performance.now();for(let i=0;i<30;i++){simStep(H,L.simNow+H*1000);L.simNow+=H*1000}const t1=F.S.c.t;F.S.ctl=null;
  /* 6 — שמירה וטעינה באמצע טיסה: הטיסה נגמרת, השחקן בגדר, המסוק בחניה */
  let sv=null,ld=null;try{sv=SaveManager.save('qa',{backup:false,silent:true});ld=SaveManager.load({silent:true})}catch(e){ld={err:String(e)}}
  note('sim',{dt:+(t1-t0).toFixed(3),ok:t1-t0>.2});note('saveLoad',{saved:!!sv,load:ld&&(ld.ok!=null?ld.ok:ld),flying:!!F.S.on,c:!!F.S.c,ok:!F.S.on&&!F.S.c})}
 /* 7 — בלי רישיון: אין השכרה */
 {const L16=PlayerProfile.licenses['LIC-16'];delete PlayerProfile.licenses['LIC-16'];at('S15-FENCE-HELI');const r=F.start('heli');note('noLic',{r,ok:r&&r.err==='lic'&&!F.S.c});if(L16)PlayerProfile.licenses['LIC-16']=L16}
 out.audit=F.audit();out.ms=Date.now()-out.t0;out.allOk=['far','card','plane','heli','free','sim','saveLoad','noLic'].every(k=>out[k]&&out[k].ok)&&out.audit.ok;return out})()
