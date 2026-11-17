// שאילתה: רכבת המשא של האי (FRT-ISL) — הבדיקה של החלק, הבלוקים של GATE-76, מפגשים (rlSweepAudit), ‏rlAudit, והמצב עכשיו
return (()=>{const R={};try{R.f=__TC_ISLF()}catch(e){R.fErr=String(e)}
 for(const [k,f] of [['rlAudit',()=>rlAudit()],['railNet',()=>railNetAudit()],['block',()=>g76BlockAudit(2,.5)],['g76',()=>{const r=roadAudit(false);const c=(r.checks||[]).filter(q=>/gate76|g76|rail|island|isl17/i.test(q.name||q.id||''));return{ok:c.every(q=>q.ok),issues:c.filter(q=>!q.ok).map(q=>(q.name||q.id)+': '+String(q.detail||'').slice(0,200))}}]])try{const q=f();R[k]={ok:q.ok,issues:(q.issues||[]).slice(0,8)}}catch(e){R[k]={err:String(e).slice(0,200)}}
 try{const T=rlTrain('FRT-ISL');const S=rlState(T,performance.now());R.now=S?{stop:S.R.stop,moving:S.moving,dwellLeft:Math.round(S.dwellLeft),cars:rlCars(S).map(c=>[Math.round(c.x),Math.round(c.y)])}:null}catch(e){R.nowErr=String(e)}
 try{const q=rlSweepAudit(.5,2);R.sweep={ok:q.ok,issues:(q.issues||[]).filter(x=>/FRT-ISL/.test(x)).slice(0,6),other:(q.issues||[]).filter(x=>!/FRT-ISL/.test(x)).length}}catch(e){R.sweepErr=String(e).slice(0,200)}
 return R})()
