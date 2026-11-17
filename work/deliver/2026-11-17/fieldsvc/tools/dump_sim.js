// טוען את 019l (S15D / S15SIM) ומדפיס סיכום של הטיסות והרכבים
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const f=new Function(src+';return {S15D,S15SIM}');const {S15D,S15SIM}=f();
const out={T:S15SIM.T,keys:Object.keys(S15SIM),flights:S15SIM.flights.map(fl=>({id:fl.id,home:fl.home,model:fl.model,kind:fl.kind,L:fl.L,nlegs:fl.legs.length,keys:Object.keys(fl),legs:fl.legs.map(g=>[g.f,g.t0,g.t1,g.h,g.att?1:0, g.p?g.p.length:0].join(','))})),
veh:S15SIM.veh.map(v=>({id:v.id,keys:Object.keys(v),n:v.legs.length,f8:v.legs.filter(g=>g.f===8).map(g=>[g.t0,g.t1,g.h,g.p&&g.p[0]].join('|')),fs:[...new Set(v.legs.map(g=>g.f))].join(',')}))};
console.log(JSON.stringify(out,null,1));
