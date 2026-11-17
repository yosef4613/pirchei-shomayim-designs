// שאילתה: מה חוסם את המדרכה של הגשר (s13_bridge_drivable) — העמודים ברשת של G78 ליד נקודות המדרכה, ומצב המפתח
return (()=>{const R={st:S13LB.st,h:S13LB.h,pc:window.__TC_PC?__TC_PC():null,pts:[]};try{
 for(let s=10;s<S13_DK.s1-10;s+=40){const w=s13Deck(s,-74),b=personBlockedAt(w[0],w[1],3);if(!b)continue;const near=[];
  try{const G=G78_PC.grid,C=G78_PC.cell,cx=Math.floor(w[0]/C),cy=Math.floor(w[1]/C);for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++){const a=G.get((cx+i)+','+(cy+j));if(a)for(const p of a){const d=Math.hypot(w[0]-p[0],w[1]-p[1]);if(d<12)near.push([p[3],+d.toFixed(1),Math.round(p[0]),Math.round(p[1])])}}}catch(e){}
  R.pts.push([s,Math.round(w[0]),Math.round(w[1]),b,near])}
 const L=[];for(const n of ['STREET_LIGHTS','SIGNAL_POLES']){try{for(const o of eval(n)){const q=poleFit(o);for(const p of R.pts)if(Math.hypot(q.x-p[1],q.y-p[2])<14)L.push([n,o.id,o.roadId||o.node||'',Math.round(q.x),Math.round(q.y),Math.round(o.x),Math.round(o.y)])}}catch(e){L.push(n+':'+e)}}R.lights=L.slice(0,20)}catch(e){R.err=String(e)}return R})()
