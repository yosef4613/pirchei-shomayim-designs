// שאילתה (island4, שלב 2ג-2א): הדרך אל E9 ומסוף המעבורת — isl17E9RoadAudit, ‏isl17E9Audit, ‏FY.audit, השגיאות של החלקים, ומצב המעבורת והרכבים שלה
return (()=>{const R={};const t=(k,f)=>{try{R[k]=f()}catch(e){R[k+'Err']=String(e&&e.message||e).slice(0,200)}};
 t('road',()=>__TC_ISL17E9R());t('land',()=>__TC_ISL17E9());
 t('errs',()=>({e9:ISL17E9.err,ft:ISL17FT.err,ftok:ISL17FT.ok,r:ISL17E9R.err,ron:ISL17E9R.on,fy:FY.err,stops:ISL17E9R.stops,lamps:ISL17E9R.lamps,counts:[NODES.length,EDGES.length],g73:G73_LOCK.roads}));
 t('fy',()=>{const a=FY.audit();return{ok:a.ok,issues:(a.issues||[]).slice(0,8),q:a.q,stats:FY.stats,log:FY.log.slice(-12)}});
 t('ra',()=>{const a=roadAudit(false);const ch=a.checks||[];return{ok:a.ok,n:ch.length,failed:ch.filter(c=>!c.ok).map(c=>c.name+' — '+String(c.detail||'').slice(0,260))}});
 t('s14',()=>{const A=s14Audit();return A.rows.filter(q=>!q.ok)});
 t('s13',()=>{const A=s13Audit();return A.checks.filter(q=>!q.ok)});
 t('la',()=>{const a=window.__TC_LIVEADD.audit();return{ok:a.ok,issues:a.issues}});
 return R})()
