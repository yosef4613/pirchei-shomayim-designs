// q_btlegs.js — fieldcalc: מבנה הרגליים של רכבות הכבודה אחרי s15kRun (הסופי) ולפניו (S15K.plan.orig), וההפעלה של s15k
return (()=>{const sm=g=>[+(g.t0||0).toFixed(1),+(g.t1||0).toFixed(1),g.h==null?'-':'h',g.f,g.hall?('H'+(g.hallId||'')):'',g.p?g.p.length:0,g.p?g.p[0].map(Math.round).join(','):'',g.s15k?'k':''].join(' ');
 const out={known:S15K.known,pre:S15K.pre,n:S15K.n,ms:S15K.ms,log:(S15K.log||[]).map(s=>String(s).slice(0,160))};
 for(const id of ['BT-P2','BT-P3','BT-P4','BL-P2']){const v=S15SIM.veh.find(w=>w.id===id);if(!v)continue;const P=S15K.plan&&S15K.plan.get(id);
  out[id]={fin:v.legs.map(sm),orig:P?P.orig.map(sm):null,trips:P?P.trips.map(t=>[t.i,t.j,t.F?+t.F.d.toFixed(1):null,+(t.o||0).toFixed(2),+(t.slack||0).toFixed(1)]):null}}
 try{const A=s15kAudit({dt:.25});out.pairs=A.pairs.slice(0,6)}catch(e){out.aerr=String(e)}
 return out})()
