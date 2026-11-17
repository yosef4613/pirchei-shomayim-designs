// q_fcamph.js — fieldcalc: האמפיבי של השדה (074zs) — האודיט של 074zm על המופע, הים לאורך ההקפה, ומצב השגיאות; וגם האמפיבי של 074zm (שלא השתנה) ופרופיל השרוולים
return (()=>{const o={st:window.FCAMPH_ST||null};try{const A=FCAMPH.audit();o.fc=A.rows.map(r=>(r.ok?'✓ ':'✗ ')+r.id+': '+String(r.det).slice(0,260))}catch(e){o.fcErr=String(e).slice(0,300)}
 try{const A=AMPH.audit();o.zm=A.rows.map(r=>(r.ok?'✓ ':'✗ ')+r.id+': '+String(r.det).slice(0,160))}catch(e){o.zmErr=String(e).slice(0,300)}
 try{const G=FCAMPH.G,bad=[];for(const [k,g] of Object.entries(G)){if(!g||!g.P)continue;for(let d=0;d<=g.len;d+=20){const P=g.P;let j=1;const c=g.c;while(j<c.length-1&&c[j]<d)j++;const a=P[j-1],b=P[j],f=(d-c[j-1])/Math.max(1e-6,c[j]-c[j-1]),x=a[0]+(b[0]-a[0])*f,y=a[1]+(b[1]-a[1])*f;let s=null;try{s=w3IsSea(x,y)}catch(e){}if(!s&&bad.length<20)bad.push(k+' '+Math.round(x)+','+Math.round(y))}}o.land=bad}catch(e){o.landErr=String(e).slice(0,200)}
 try{const r=roadAudit();const L=r.checks||r.results||[];o.audit=L.filter(c=>/^(fc_|amph_water|s15j_terminal|s15j_layout|s15c_ground)/.test(c.id||c.name||'')).map(c=>({id:c.id||c.name,ok:!!(c.ok||c.pass),d:String(c.detail||'').slice(0,900)}));o.failed=L.filter(c=>!(c.ok||c.pass)).map(c=>c.id||c.name);o.total=L.length}catch(e){o.auditErr=String(e).slice(0,300)}
 try{o.info=FCAMPH.info()}catch(e){}
 return o})()
