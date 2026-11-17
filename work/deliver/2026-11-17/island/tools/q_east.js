// שאילתה: דרך המזרח ולולאת המזרח (ISL17E) וקו 5א — הבדיקות של החלקים, s13Audit / s16cAudit, המפרצים של 5א, ומצב הקו
return (()=>{const R={};try{R.east=__TC_ISL17E()}catch(e){R.eastErr=String(e)}try{R.l5a=__TC_ISL5A()}catch(e){R.l5aErr=String(e)}
 try{const A=s13Audit();R.s13ok=A.ok;R.s13bad=A.checks.filter(q=>!q.ok)}catch(e){R.s13Err=String(e)}
 try{const A=s16cAudit();R.s16c={ok:A.ok,issues:A.issues.slice(0,8),err:A.err}}catch(e){R.s16cErr=String(e)}
 try{const A=s267BaysAudit();R.bays=A.bays.filter(b=>/^I5A/.test(b.id));R.baysOk=A.ok;R.baysBad=A.bad.slice(0,6)}catch(e){R.baysErr=String(e)}
 try{R.l5={on:L5R.on,why:L5R.why,err:L5R.err,F:LN5.F,seeded:LN.seeded}}catch(e){}
 try{R.stops=['I5A-7E','I5A-7W','I5A-8N','I5A-8S','I5A-9T'].map(id=>{const s=S6_MAP_STOPS.find(q=>q.id===id);return s?[id,Math.round(s.x),Math.round(s.y),+s.t.toFixed(2),s.site]:null})}catch(e){}
 try{R.light=[S13_LIGHT.x,S13_LIGHT.y];R.heli=S13D.lots.find(l=>l.id==='IS-HELI').c;R.places=['IS-LIGHTHOUSE','IS-LIGHT-HOUSE','IS-HELI'].map(id=>{const p=S13_POIS[id];return p?[id,p.x,p.y,personBlockedAt(p.x,p.y,3)]:null})}catch(e){}
 return R})()
