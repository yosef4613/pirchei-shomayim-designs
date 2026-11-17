// q_hit.js — terminal: איפה AB-R1 / AB-R2 נוגעים במטוס החונה (s15SimAudit) — המצב והקופסאות
return (()=>{const o={};try{const q=s15SimAudit(1);o.issues=q.issues.slice(0,30)}catch(e){o.err=String(e)}
 const act=new Set(S15SIM.sched.map(q=>q[0])),s=S15D.stands.GA4,ac=S15D.parked.GA4;o.ga4={ac,act:act.has('GA4'),stand:s};
 const P=[s.cx,s.nose-(S15SIM.ngf[ac]||.12)*91,Math.PI/2,0];o.pkBoxes=s15Boxes({kind:'ac',model:ac,L:91,W:112},P);
 for(const id of ['AB-R1','AB-R2']){const v=S15SIM.veh.find(w=>w.id===id);if(!v)continue;o[id]={L:v.L,W:v.W,poses:[]};for(let t=0;t<720;t+=.5){const q=s15PoseAt(v,t);if(!q)continue;const B=s15Boxes(v,q);if(B.some(b=>o.pkBoxes.some(x=>s15ObbHit(x,b))))o[id].poses.push([t,q.map(z=>+(+z).toFixed(2)),B])}
  o[id].legs=v.legs.map(g=>[g.t0,g.t1,g.f,g.r||0,g.h!=null?+g.h.toFixed(2):null,g.p.length,g.p[0].map(Math.round),g.p[g.p.length-1].map(Math.round)])}
 try{const T=S15SIM.T;o.ffr3=FFR3.build().map(A=>({id:A.id,ac:A.ac,tOut:A.tOut??FFR3.tOut,tBack:A.tBack??FFR3.tBack,out:{dur:A.out.dur,pts:A.out.legs.map(g=>[g.t0,g.t1,g.p[0].map(Math.round),g.p[g.p.length-1].map(Math.round)])},back:{dur:A.back.dur,pts:A.back.legs.map(g=>[g.t0,g.t1,g.p[0].map(Math.round),g.p[g.p.length-1].map(Math.round)])},r3:S15_HGR.r3}));
  const r=ffR3Audit();o.ffr3Audit=r.members.map(m=>[m.id,m.hits,m.with]);
  // לכל חבר: באילו tc הגרירה נוגעת באוטובוסים
  o.ffHits=[];for(const A of FFR3.build()){for(const [L,m0] of [[A.out,A.tOut??FFR3.tOut],[A.back,A.tBack??FFR3.tBack]]){const tc0=((m0*2)%T+T)%T;for(let t=0;t<=L.dur;t+=1){let P=null;for(const g of L.legs)if(t>=g.t0-1e-6&&t<=g.t1+1e-6){P=s15PoseLeg(g,t);break}if(!P)continue;const tc=(tc0+t)%T,MB=ffBoxes('ac',A.ac,A.Lpx,FF_W[A.ac]||150,P);
    for(const id of ['AB-R1','AB-R2']){const v=S15SIM.veh.find(w=>w.id===id);if(!v)continue;const Q=s15PoseAt(v,tc);if(!Q)continue;const OB=ffBoxes('veh',v.model,v.L,v.W||22,Q);if(MB.some(p=>OB.some(q=>ffObb(p,q))))o.ffHits.push([A.id,id,+tc.toFixed(1),P.map(z=>Math.round(z)),Q.map(z=>Math.round(z))])}}}}}catch(e){o.ffErr=String(e).slice(0,300)}
 return o})()
