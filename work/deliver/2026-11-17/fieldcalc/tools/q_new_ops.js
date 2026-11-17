// q_new_ops.js — fieldcalc 17.11: מלאי של השדה החדש (S7F298) מהמשחק עצמו — S15SIM כפי שהוא אחרי כל העטיפות (074p / 074r / 074n …), קריאה בלבד.
return (()=>{const out={};const S=S15SIM,D=S15D,r1=x=>Math.round(x*10)/10;
 out.T=S.T;out.nFlights=S.flights.length;out.nVeh=S.veh.length;out.sched=S.sched;
 out.flights=S.flights.map(f=>{const L=f.legs.filter(g=>!g.att);const o={id:f.id,model:f.model,home:f.home,airline:f.airline,L:f.L,W:f.W,kind:f.kind};
  const air=L.filter(g=>g.f===4);const roll=L.find(g=>g.f===1&&g.v1>=500);const land=L.find(g=>g.f===1&&g.v0>=500);
  o.push=r1(L[0].t0);o.rollStart=roll&&r1(roll.t0);o.liftoff=roll&&r1(roll.t1);o.climbEnd=air[0]&&r1(air[0].t1);o.appStart=air[1]&&r1(air[1].t0);o.touch=air[1]&&r1(air[1].t1);o.rollEnd=land&&r1(land.t1);
  const st=L.filter(g=>g.h!=null&&g.f===0);const park=st.sort((a,b)=>(b.t1-b.t0)-(a.t1-a.t0))[0];o.onblock=park&&r1(park.t0);o.offblock=park&&r1(park.t1);
  // הכניסה למסלול (y בתוך המסלול) והפינוי — לפי הדגימה
  const R=D.rwy;let enter=null,leave=null,enter2=null,leave2=null;for(let t=0;t<2*S.T;t+=.25){const P=s15PoseAt(f,t%S.T);const on=P&&P[3]<1&&P[1]>=R[1]-5&&P[1]<=R[3]+5&&P[0]>=R[0]-50&&P[0]<=R[2]+50;if(on&&enter==null)enter=t;if(!on&&enter!=null&&leave==null){leave=t}}
  o.rwyOcc=[enter,leave];return o});
 out.veh=S.veh.map(v=>({id:v.id,model:v.model,home:v.home,svc:v.legs.filter(g=>g.h!=null&&g.f===8).map(g=>[r1(g.t0),r1(g.t1),g.p&&g.p[0]&&g.p[0].map(Math.round)])}));
 out.tows=(S.tows||[]).map(t=>({id:t.id,model:t.model,t0:t.legs[0].t0,t1:t.legs[t.legs.length-1].t1}));
 out.heli=(S.heli||[]).map(h=>({id:h.id,model:h.model,home:h.home,legs:h.legs.length,t0:h.legs[0].t0}));
 out.stands=Object.fromEntries(Object.entries(D.stands).map(([k,s])=>[k,{rect:s.rect,type:s.type,zone:s.zone,parked:D.parked[k]}]));
 out.spots=Object.keys(D.spots).length;out.spotTypes={};for(const k in D.spots){const t=D.spots[k].t;out.spotTypes[t]=(out.spotTypes[t]||0)+1}
 try{out.S15K={n:S15K.n,done:S15K.done,before:S15K.before,after:S15K.after}}catch(e){out.S15Kerr=String(e)}
 try{out.hall=S15I_HALL}catch(e){}
 try{const P=S15J.plan;out.term={keys:P?Object.keys(P):null,flights:P&&P.flights?P.flights.map(f=>({code:f.code,g:f.g,nA:f.nA,nD:f.nD,dur:f.dur})):null};out.termN=S15J.n;
   const seats=(S15J_L.seats||[]);out.seatsL=Array.isArray(seats)?seats.length:Object.keys(seats).length;out.S15J_L_keys=Object.keys(S15J_L)}catch(e){out.termErr=String(e)}
 try{out.tcS15=typeof __TC_S15!=='undefined'&&__TC_S15.flights?__TC_S15.flights():null}catch(e){out.tcS15err=String(e)}
 try{out.parkedStatic=s15StaticList().length}catch(e){}
 try{const a=s15SimAudit(1);out.simAudit={ok:a.ok,issues:a.issues.length,pairs:a.pairs,cycles:a.cycles}}catch(e){out.simAuditErr=String(e)}
 return out})()
