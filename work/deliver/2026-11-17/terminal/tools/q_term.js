// q_term.js — terminal: הבדיקה של המסועים והשאטל (term_bags / term_shuttle) + s15j + fc_bag_halls + s15k
return (()=>{const o={};const T=window.__TC_TERM;o.on=T&&T.on;o.err=T&&T.err;o.n=T&&T.n;
 try{o.audit=tmnlAudit()}catch(e){o.auditErr=String(e).slice(0,300)}
 try{o.shuttle=typeof tmnlShAudit==='function'?tmnlShAudit():null}catch(e){o.shErr=String(e).slice(0,300)}
 try{const H=s15jHall();o.hall=H&&Object.fromEntries(Object.entries(H).map(([k,v])=>[k,{n:v.n,car:v.car,hall:v.hall,L:v.chainL&&Math.round(v.chainL)}]))}catch(e){o.hallErr=String(e).slice(0,200)}
 try{const P=s15jPlan();o.plan={agents:P.agents.length,bagsCar:P.bagsCar.length,issues:P.issues.slice(0,8),flights:P.flights.map(f=>f.g+' '+f.code)}}catch(e){o.planErr=String(e).slice(0,200)+' '+S15J.planErr}
 try{const r=roadAudit();const L=r.checks||r.results||[];o.checks=L.filter(c=>/^(s15j|s15i|fc_|term|s15k|s15c|s15bag|s15_)/.test(c.id||c.name||'')).map(c=>({id:c.id||c.name,ok:!!(c.ok||c.pass),d:String(c.detail||c.det||'').slice(0,500)}));o.failed=L.filter(c=>!(c.ok||c.pass)).map(c=>c.id||c.name)}catch(e){o.raErr=String(e).slice(0,300)}
 try{o.s15j=s15jAudit().checks.map(c=>[c.id,c.ok,c.det.slice(0,300)])}catch(e){o.s15jErr=String(e).slice(0,200)}
 o.errs={s15j:S15J.err,fch:typeof FCH!=='undefined'&&FCH.err,s15i:typeof S15I!=='undefined'&&S15I.err};
 return o})()
