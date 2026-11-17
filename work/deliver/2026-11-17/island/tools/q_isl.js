// שאילתה: הרכבל הסובב (ISL17) — מצב, מיקומי 10 התאים, השגיאות, ובדיקת האי (s13Audit)
return (()=>{const t=performance.now()/1000,R={};
 R.ok=ISL17.ok;R.err=ISL17.err;R.N=ISL17.N;R.T=Math.round(ISL17.T);R.oneWayM=ISL17.oneWayM;R.L=Math.round(ISL17.LREAL);
 R.poses=Array.from({length:ISL17.N},(_,k)=>{const p=ISL17.pose(k,t,true);return[Math.round(p.x),Math.round(p.y),+p.z.toFixed(1),p.at,p.dir]});
 const pts=R.poses.map(p=>p[0]+','+p[1]);R.distinct=new Set(pts).size;
 let minGap=1e9;for(let i=0;i<R.poses.length;i++)for(let j=i+1;j<R.poses.length;j++){const d=Math.hypot(R.poses[i][0]-R.poses[j][0],R.poses[i][1]-R.poses[j][1]);if(d<minGap)minGap=d}R.minGapPx=Math.round(minGap);
 /* רציפות: תא 0 לאורך 300 שנ׳ — הקפיצה הגדולה בין שתי דגימות של 0.5 שנ׳ */
 let jump=0,prev=null;for(let s=0;s<300;s+=.5){const p=ISL17.pose(0,1000+s,true,false);if(prev)jump=Math.max(jump,Math.hypot(p.x-prev.x,p.y-prev.y));prev=p}R.maxStepPx_half_s=+jump.toFixed(1);
 /* בכל תחנה — כמה זמן תא נמצא בה בסיבוב אחד */
 const inSt={A:0,B:0,C:0};for(let s=0;s<ISL17.T;s+=.5){const p=ISL17.pose(0,s,true,false);if(p.at)inSt[p.at]+=.5}R.dwell_s=inSt;
 /* עקיפה: הסדר של התאים על הלולאה לא משתנה */
 R.lifeErr=S13LIFE.err();R.placesErr=S13P.err;R.bld=C4_BUILDINGS.some(b=>b.id==='IS-CABLE-W-B');R.poi=!!S13_POIS['IS-CABLE-W'];
 try{R.fW=s13Now('IS-CABLE-W');R.fLow=s13Now('IS-CABLE-LOW')}catch(e){R.fErr=String(e)}
 try{const A=s13Audit();R.auditOk=A.ok;R.auditBad=A.checks.filter(q=>!q.ok)}catch(e){R.auditErr=String(e)}
 try{R.blockW=personBlockedAt(6760,7606,3);R.blockSt=personBlockedAt(6740,7712,3)}catch(e){}
 return R})()
