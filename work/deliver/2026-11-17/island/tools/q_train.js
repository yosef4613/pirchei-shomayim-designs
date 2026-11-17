// שאילתה: רכבת האי (RL-PS-02) — 4 קרונות: הבדיקה של החלק (__TC_RLI.audit), בדיקות המסילות של המשחק (rlAudit, ‏railNetAudit, ‏tcRailPaxAudit),
// מפגשים בין רכבות לאורך 2 מחזורים (rlSweepAudit), הבלוקים של GATE-76, והזמן על המפתח המתרומם; וגם מיקום הקרונות בשתי התחנות
return (()=>{const R={},t0=performance.now();const T=rlTrain('RL-PS-02');R.err=RLI.err;R.cars=T&&T.cars.length;R.L=T&&Math.round(T.L);R.carLen=T&&Math.round(T.cars[0].len);
 try{R.rli=__TC_RLI.audit()}catch(e){R.rliErr=String(e)}
 for(const [k,f] of [['rlAudit',()=>rlAudit()],['railNet',()=>railNetAudit()],['pax',()=>tcRailPaxAudit()]])try{const q=f();R[k]={ok:q.ok,issues:(q.issues||[]).slice(0,10)}}catch(e){R[k]={err:String(e).slice(0,200)}}
 try{const q=rlSweepAudit(.5,2);R.sweep={ok:q.ok,issues:(q.issues||[]).slice(0,10),minGap:q.minGap}}catch(e){R.sweep={err:String(e).slice(0,200)}}
 try{const q=g76BlockAudit(2,.5);R.block={ok:q.ok,issues:(q.issues||[]).slice(0,10)}}catch(e){R.block={err:String(e).slice(0,200)}}
 try{const out={};for(const Rr of T.runs){const S={T,R:Rr,u:Rr.P.len,fwd:true,moving:false,dwellDone:10,dwellLeft:10,g:0};out[Rr.at]=rlCars(S).map(c=>[Math.round(c.x),Math.round(c.y)])}R.stopCars=out}catch(e){R.stopErr=String(e)}
 try{let on=0;for(let s=0;s<T.cycle;s+=1){const S=rlState(T,s*1000);if(!S)continue;if(rlCars(S).some(c=>s13InPoly(S13_LF.poly,c.x,c.y)))on++}R.onSpanS=on;R.cycle=Math.round(T.cycle)}catch(e){R.spanErr=String(e)}
 try{R.s13=s13Audit().ok}catch(e){}
 R.ms=Math.round(performance.now()-t0);return R})()
