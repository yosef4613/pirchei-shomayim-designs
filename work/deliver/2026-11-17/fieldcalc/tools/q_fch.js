// q_fch.js — fieldcalc: מצב 5 עמדות הכבודה (074zr) והבדיקות של השדה מתוך roadAudit
return (()=>{const F=window.__TC_FCH||{};const out={on:F.on,err:F.err,n:F.n,trains:F.trains,fc:window.__TC_FC&&__TC_FC.halls()};
 try{const r=roadAudit();const L=r.checks||r.results||[];out.audit=L.filter(c=>/^(s15i|s15j|fc_|s15k|s15c|s15bag|s15_sim)/.test(c.id||c.name||'')).map(c=>({id:c.id||c.name,ok:!!(c.ok||c.pass),d:String(c.detail||c.det||'').slice(0,400)}));out.total=L.length;out.failed=L.filter(c=>!(c.ok||c.pass)).map(c=>c.id||c.name)}catch(e){out.auditErr=String(e).slice(0,300)}
 return out})()
