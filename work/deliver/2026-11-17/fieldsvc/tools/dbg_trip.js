// dbg_trip.js — בונה נסיעה אחת דרך ה-harness ומדפיס את הפינות והפגיעה הקבועה הראשונה
const fs=require('fs');process.env.FSONLY='NONE';
const H=fs.readFileSync(__dirname+'/fs_harness.js','utf8').replace("FSV.dbg=[];if(process.env.FSONLY)FSV.only=process.env.FSONLY.split(\",\");fsvPlan();return{FSV,audit:fsvAudit(1800),veh:S15SIM.veh.filter(v=>v.fsv)};",
 "FSV.dbg=[];const AS=fsvStands();const A=AS.find(a=>a.f.id===process.env.FID);const c=process.env.CODE;const S=fsvSpot(A,c);const out=[];out.push('S '+JSON.stringify(S));"+
 "const [L,W]=fsvDims(c);const tm=fsvTiming(A,c);for(const src of fsvSources(A,c).slice(0,3)){const HA=fsvHomeAccess(src.H);for(const ha of HA)for(const ap of fsvApproaches(S,A,S.th!=null).slice(0,4)){FSV.why='';const tr=fsvTrip(src.H,ha,ap,S,tm.hold,A.ob+30,40);"+
 "if(!tr){out.push(src.id+' '+ha.s.id+'→'+ap.s.id+' null '+FSV.whyF);continue}const hit=fsvStaticHit(tr,L,W,src.kind!=='bay'?src.id:null);out.push(src.kind+':'+(src.id||src.pk)+' H'+[src.H.x,src.H.y,src.H.h.toFixed(2)]+' '+ha.s.id+'→'+ap.s.id+' hit='+hit+' '+FSV.why+' | '+tr.legs.filter(g=>g.f===1).map(g=>(g.r?'R':'F')+'['+g.p[0].map(Math.round)+'→'+g.p[g.p.length-1].map(Math.round)+']').join(' '))}}console.log(out.join('\\n'));return{FSV,audit:{full:0,flights:0,missing:[],wheelchairW:0},veh:[]};");
fs.writeFileSync(__dirname+'/.dbg_h.js',H);
