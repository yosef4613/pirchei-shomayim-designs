// q_old_svc.js — fieldsvc 17.11: בשדה הישן (המתכנן AO, ‏044/045 — S7F272), לכל טיסה שהגיעה לעמדה בחלון: אילו רכבי שירות הגיעו אליה (המשימות של AO.fleet עם הקוד שלה),
// מתי (רגלי ה-svc ביחס לעצירה), האם לפני הדחיפה; ומה הסוג שלה היה אמור לקבל בישן (G77_AC.svc + g77Need). קריאה בלבד (כמו q_old_ops.js של fieldcalc).
return (async()=>{
 const W=+(window.__FS_W||1800),SEED=window.__FS_SEED||777,out={W,seed:SEED,fl:[],fleet:{}};
 try{APT_OPS.on=false}catch(e){}
 if(!APTT_SPEC){APTT_SPEC=aptBuildSpec();APTT_C=aptBuildC()} if(!APL)APL=aplBuild();
 const t0w=performance.now();AO.sliced=false;AO.useClock=false;AO.keep=true;AO.budget=1e9;aoInit(0,SEED);
 let t=0;for(;t<=W+700;t+=1){aoStep(t);if(performance.now()-t0w>300000)break}out.reached=t;out.ms=Math.round(performance.now()-t0w);
 const tasks=[];for(const v of AO.fleet){for(const q of (v.hist||[]).concat(v.tasks||[])){let a=null,b=null,c=0;try{const L=q.tr&&q.tr.seq&&q.tr.seq.legs;if(L){for(const g of L){if(g.kind==='svc'){if(a==null)a=q.t0+c;b=q.t0+c+g.dur}c+=g.dur}}}catch(e){}
   tasks.push({v:v.id,type:v.type,role:q.role||'',code:String(q.code==null?'':q.code),t0:+(+q.t0).toFixed(1),t1:+(+q.t1).toFixed(1),s0:a==null?null:+a.toFixed(1),s1:b==null?null:+b.toFixed(1)})}
  const r=out.fleet[v.type]||(out.fleet[v.type]={n:0});r.n++}
 const fl=AO.hist.concat(AO.flights).filter(f=>!f.never&&!f.heli);
 for(const f of fl){const st=f.states||[],at=n=>{const q=st.find(s=>s[1]===n);return q?+(+q[0]).toFixed(1):null};const onb=at('ON_BLOCK'),push=at('PUSHBACK');
  if(onb==null||onb>W)continue;const P=(typeof g77Prof==='function'?g77Prof(f.sd,f.ac):G77_AC[f.ac])||{svc:[]};
  const want=P.svc.filter(s=>{try{return g77Need(f.code,s,f.ac)}catch(e){return true}});
  const mine=tasks.filter(q=>q.code.split('/').includes(f.code)||q.code===f.code);
  out.fl.push({code:f.code,ac:f.ac,sd:f.sd&&f.sd.id,kind:f.sd&&f.sd.kind,remote:!!(f.sd&&f.sd.remote),bridge:!!(f.sd&&f.sd.tpl==='bridge'),parked:!!f.parked,init:!!f.init,onb,push,dep:at('DEPARTED'),
   paxA:f.paxA!=null?f.paxA:(f.pax&&f.pax.a),paxD:f.paxD!=null?f.paxD:(f.pax&&f.pax.d),svcAll:P.svc,want,amb:f.amb?{at:f.amb.at,done:f.amb.done}:null,g2:!!f.g2,fm:!!f.fm,
   svcQ:(f.svcQ||[]).map(q=>({svc:q.svc,at:q.at!=null?+(+q.at).toFixed(1):null,done:q.done!=null?+(+q.done).toFixed(1):null})),skipped:f.skipped||null,tasks:mine})}
 out.nTasks=tasks.length;out.noCode=tasks.filter(q=>!q.code).length;
 try{out.amb={want:0,...JSON.parse(JSON.stringify(g77AmbAudit(fl)))}}catch(e){out.ambErr=String(e).slice(0,160)}
 return out})()
