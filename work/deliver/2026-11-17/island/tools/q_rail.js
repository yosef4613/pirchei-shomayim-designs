// שאילתה (לתכנון רכבת המשא של האי): הקטעים של הנמל, מסילת המזרח והאי; הרכבות — מחזור, זמני הריצות, ואיזה קטעים כל רכבת תופסת לאורך המחזור (כל 2 שנ׳)
return (()=>{const R={segs:{},trains:[],occ:{}};const want=/^(EAST-|ISL-|B-J|B-LINK|B-3|Q-|Q2-|P1|P2|X-|END-)/;
 for(const g of RAIL_SEGS)if(want.test(g.id))R.segs[g.id]=[g.from,g.to,Math.round(g.len),g.kind,g.port?1:0,g.track];
 for(const T of RL_TRAINS){if(T.err){R.trains.push({id:T.id,err:T.err});continue}R.trains.push({id:T.id,cycle:Math.round(T.cycle),off:Math.round(T.off||0),L:Math.round(T.L),runs:T.runs.map(r=>[r.stop,Math.round(r.t0),Math.round(r.t1),Math.round(r.tEnd),r.legs[0][0],r.legs[r.legs.length-1][0]])})}
 const near=(x,y)=>{let best=null,bd=40;for(const g of RAIL_SEGS){if(!want.test(g.id))continue;for(let i=0;i<g.pts.length;i+=1){const d=Math.hypot(g.pts[i][0]-x,g.pts[i][1]-y);if(d<bd){bd=d;best=g.id}}}return best};
 const C=1480;for(const T of RL_TRAINS){if(T.err)continue;const o={};for(let s=0;s<C;s+=4){const S=rlState(T,s*1000);if(!S)continue;const cs=rlCars(S);for(const c of [cs[0],cs[cs.length-1]]){const g=near(c.x,c.y);if(!g)continue;(o[g]=o[g]||[]).push(s)}}
  for(const g in o){const a=o[g],iv=[];let s0=a[0],p=a[0];for(const t of a.slice(1)){if(t-p>8){iv.push([s0,p]);s0=t}p=t}iv.push([s0,p]);o[g]=iv.slice(0,12)}R.occ[T.id]=o}
 try{R.lift={span:S13_SPANX||null}}catch(e){}
 return R})()
