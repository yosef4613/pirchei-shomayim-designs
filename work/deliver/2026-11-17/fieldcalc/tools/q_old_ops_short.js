// q_old_ops.js — fieldcalc 17.11: הרצה של המתכנן הישן (AO, ‏044/045) בלי חיתוך, בבנייה הישנה (S7F272), לחלון של 1800 שנ׳ סימולציה, בכמה זרעים.
// קריאה בלבד: לא משנה קובץ; ‏APT_OPS.on=false כדי שהלולאה של המשחק לא תתכנן במקביל. מחזיר: התנועות, התמהיל, העמדות, הזמנים, הצי, הדחיות.
return (async()=>{
 const W=300,SEEDS=[777],DTs=1,out={cfg:JSON.parse(JSON.stringify(AO.cfg)),W,seeds:[]};
 try{APT_OPS.on=false}catch(e){}
 if(!APTT_SPEC){APTT_SPEC=aptBuildSpec();APTT_C=aptBuildC()} if(!APL)APL=aplBuild();
 out.stands=APL.stands.map(s=>({id:s.id,kind:s.kind,tpl:s.tpl,live:s.live,rate:s.rate||1,accepts:s.accepts,first:s.first,remote:!!s.remote,large:!!s.large,cx:s.cx,ngy:s.ngy}));
 out.helis=APL.helis.map(h=>({id:h.id,ac:h.aircraft,live:h.live,x:h.x,y:h.y}));
 out.fleetDef={};for(const v of APL.fleet)out.fleetDef[v.type]=(out.fleetDef[v.type]||0)+1;
 try{const R=APTT_C.RWY;out.rwy={cy:R.cy,w:R.w,x0:R.x0,x1:R.x1,len:R.len};out.links={A1:APTT_X.A1,A2:APTT_X.A2,A3:APTT_X.A3}}catch(e){out.rwyErr=String(e)}
 const T0=performance.now();
 for(const seed of SEEDS){
  const t0w=performance.now();
  AO.sliced=false;AO.useClock=false;AO.keep=true;AO.budget=1e9;
  aoInit(0,seed);
  let t=0;for(;t<=W+400;t+=DTs){aoStep(t);if(performance.now()-t0w>200000)break}
  const fl=AO.hist.concat(AO.flights).filter(f=>!f.never);
  const S={seed,reached:t,ms:Math.round(performance.now()-t0w),nFlights:fl.length,stats:JSON.parse(JSON.stringify(AO.stats)),fl:[]};
  for(const f of fl){const st=f.states||[];const at=n=>{const q=st.find(s=>s[1]===n);return q?+q[0].toFixed(1):null};
   S.fl.push({code:f.code,ac:f.ac,sd:f.sd&&f.sd.id,kind:f.sd&&f.sd.kind,heli:!!f.heli,parked:!!f.parked,init:!!f.init,
    app:at('APPROACH'),land:at('LANDING_ROLL'),vac:at('VACATE_RUNWAY'),onb:at('ON_BLOCK'),rdy:at('TURNAROUND_READY'),push:at('PUSHBACK'),taxo:at('TAXI_OUT'),hold:at('HOLD_SHORT'),lu:at('LINE_UP'),to:at('TAKEOFF_ROLL'),dep:at('DEPARTED'),ga:at('GO_AROUND'),
    paxA:f.paxA!=null?f.paxA:(f.pax&&f.pax.a),paxD:f.paxD!=null?f.paxD:(f.pax&&f.pax.d),svc:(f.svcQ||[]).map(q=>q.svc+':'+(q.at!=null?(+q.at).toFixed(0):'')+'-'+(q.done!=null?(+q.done).toFixed(0):'')).join(' ')})}
  const fv={};for(const v of AO.fleet){const k=v.type;const r=fv[k]||(fv[k]={n:0,used:0,tasks:0,busy:0});r.n++;const L=(v.hist||[]).concat(v.tasks||[]);let u=0;for(const q of L){const a=Math.max(0,q.t0),b=Math.min(W,q.t1);if(b>a){r.tasks++;r.busy+=b-a;u=1}}r.used+=u}
  for(const k in fv)fv[k].busy=Math.round(fv[k].busy);
  S.fleet=fv;
  try{S.af=Object.keys(AF||{}).slice(0,40)}catch(e){}
  out.seeds.push(S);
 }
 out.totalMs=Math.round(performance.now()-T0);
 return out;
})()
