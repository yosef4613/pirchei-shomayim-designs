// q_ingame.js — הבדיקות שבתוך המשחק, בשאילתה אחת (בונה S7F266): roadAudit כולו (כמה עברו, כמה נכשלו ואילו),
// ובנפרד הבדיקות של E3, ‏E4, ‏C5, ‏D5, המסילות, הפרטים החיים והרכבים המזויפים, וגם הבדיקות החדשות של S7F266 (אם הן קיימות).
// node qa_tools/probe_c2.js <game.html> qa_tools/q_ingame.js <out.json>
(()=>{const R={build:(typeof BUILD!=='undefined'?BUILD:null),errors:[]};
const run=(k,f)=>{try{const v=f();R[k]=v}catch(e){R[k]={ok:false,error:String(e&&e.message||e).slice(0,300)}}};
run('roadAudit',()=>{const a=roadAudit(false);const ch=a.checks||[];return{ok:!!a.ok,total:ch.length,passed:ch.filter(c=>c.ok).length,failed:ch.filter(c=>!c.ok).map(c=>c.name+' — '+String(c.detail||'').slice(0,300)),skipped:(a.skipped||[]).length}});
const one=(k,fn)=>run(k,()=>{let F=null;try{F=eval(fn)}catch(e){}if(typeof F!=='function')return{missing:true};const q=eval(fn+'()');if(q&&typeof q==='object'){const o={ok:q.ok!==false};for(const x of ['issues','issueCount','bad','hits','detail','fails','roofed','platforms','railTracks','cars','platformSpan','bypass','x','z','clearM','columns','crossedOverhead','offsetM','build','scope','title','line1','label'])if(q[x]!=null)o[x]=Array.isArray(q[x])?q[x].slice(0,14):q[x];return o}return{value:q}});
for(const [k,fn] of [['e3','e3GeometryAudit'],['e4','e4GeometryAudit'],['c5','c5GeometryAudit'],['c5trucks','c5TrucksAudit'],['pgC5','pgC5Audit'],['pgStructure','pgStructureAudit'],['d5','d5GeometryAudit'],['d3','d3GeometryAudit'],['railNet','railNetAudit'],['rl','rlAudit'],['fakeLive','p691FakeLiveAudit'],['special','specialAudit'],['vehInBld','vehInBldAudit'],['zebra','zebraAudit'],['signalSync','signalPhaseSyncAudit'],['pipe','s266PipeAudit'],['texts','s266TextAudit']])one(k,fn);
return JSON.stringify(R)})()
