// שאילתה (island4): היציאה של "צוק הים" ב-L2 — המעגן, הסיבוב במקום, "עוז" בדופן ולפני החרטום, השחרור והחזרה; ו-s14Audit כולו (vessels_day, ‏tugs, ‏buoys …)
return (()=>{const R={};try{const D=S14D;R.anch=[D.anch.x,D.anch.y];R.l2=!!(D.isl17Exit&&D.isl17Exit.l2);R.isl=typeof ISL17E9S!=='undefined'?{ok:ISL17E9S.ok,err:ISL17E9S.err,l2:ISL17E9S.l2}:null;
 const out=[];for(let t=D.ship.leave-60;t<D.ship.leave+160;t+=2){const P=S14.poseOf('ship',t),T=S14.poseOf('TUG-1',t);out.push([t,Math.round(P.x),Math.round(P.y),+P.h.toFixed(2),P.g&&P.g.mode,Math.round(T.x),Math.round(T.y),+T.h.toFixed(2),T.g&&T.g.mode])}R.dep=out;
 const A=s14Audit();R.s14ok=A.ok;R.s14=A.rows.map(q=>[q.id,q.ok,String(q.det).slice(0,260)]);
 try{R.tugx=window.__TC_TUGX?window.__TC_TUGX.stats():null}catch(e){}
}catch(e){R.e=String(e&&e.stack||e).slice(0,400)}return R})()
