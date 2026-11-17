// q_dump.js — terminal: מצב הכבודה, R2 והשאטל (בירור)
return (()=>{const o={};const T=S15SIM.T;o.T=T;
 o.flights=S15SIM.flights.map(f=>{const L=f.legs[f.legs.length-1];return [f.id,f.home,f.model,+L.t0.toFixed(1),+L.t1.toFixed(1)]});
 const ab=S15SIM.veh.find(v=>v.id==='AB-R1');o.ab=ab&&ab.legs.map(g=>[g.t0,g.t1,g.f,g.h!=null?+g.h.toFixed(2):null,g.p.length,g.p[0].map(Math.round),g.p[g.p.length-1].map(Math.round)]);
 try{o.r2plan=S15W4R.plan&&{g2:S15W4R.plan.g2&&{open:S15W4R.plan.g2.open,close:S15W4R.plan.g2.close,arr:S15W4R.plan.g2.arr,dep:S15W4R.plan.g2.dep}}}catch(e){o.r2planErr=String(e)}
 o.bt=S15SIM.veh.filter(v=>/^BT/.test(v.id)).map(v=>[v.id,v.legs.filter(g=>g.hallId!=null).map(g=>[g.hallId,+g.t0.toFixed(0),+g.t1.toFixed(0)])]);
 try{o.fch=__TC_FCH&&{trains:__TC_FCH.trains,assign:__TC_FCH.assign,halls:__TC_FCH.halls.map(h=>[h.id,h.r,h.toCar,h.fromCI,h.belt,h.serves])}}catch(e){}
 try{const H=s15jHall();o.hall=H&&Object.fromEntries(Object.entries(H).map(([k,v])=>[k,{n:v.n,unload:v.unload.map(q=>+q.t.toFixed(0))}]))}catch(e){o.hallErr=String(e)}
 try{const P=S15J.plan||s15jPlan();o.plan={agents:P.agents.length,bagsCar:P.bagsCar.length,bagsCI:P.bagsCI.length,issues:P.issues.slice(0,10),flights:P.flights&&P.flights.length,byFlight:{}};for(const b of P.bagsCar){o.plan.byFlight[b.flight]=(o.plan.byFlight[b.flight]||0)+1}
  o.plan.kinds={};for(const a of P.agents){o.plan.kinds[a.kind]=(o.plan.kinds[a.kind]||0)+1}}catch(e){o.planErr=String(e).slice(0,200)}
 try{o.path=s15jPath('TE9150','AD').length}catch(e){o.pathErr=String(e).slice(0,200)}
 try{o.fidsRows=S15GR.last&&{arr:S15GR.last.arr.map(r=>r.gate+' '+r.code),dep:S15GR.last.dep.map(r=>r.gate+' '+r.code)}}catch(e){}
 try{o.svc=S15D.service.map(s=>s.id)}catch(e){}
 o.veh=S15SIM.veh.map(v=>v.id);
 try{o.s15k=typeof s15kAudit==='function'?JSON.stringify(s15kAudit()).slice(0,600):null}catch(e){o.s15kErr=String(e).slice(0,200)}
 o.clock=s15Clock();o.tc=s15Tc(s15Clock().abs);
 return o})()
