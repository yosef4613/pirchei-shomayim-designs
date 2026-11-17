// rails 17.11 — הבדיקה של המסילות בתוך המשחק: צמתים בלי מסוט מכוסים בציור של צומת, כל מסוט מצויר בצייר של מסוט, הרכבות (rlAudit), ורכבות לאורך מחזור — בלי עצירה לא מתוכננת
return (()=>{const R={ok:true,fail:[],err:{rjx:(typeof RJX!=='undefined'?RJX.err:'no-RJX'),tct:window.__TCT_ERR||null,rlp:(typeof RLP!=='undefined'?RLP.err:null),rli:(typeof RLI!=='undefined'?RLI.err:null)}};
 const F=m=>{R.ok=false;R.fail.push(m)};
 if(R.err.rjx)F('RJX.err '+R.err.rjx);if(R.err.tct)F('TCT '+R.err.tct);if(R.err.rlp)F('RLP '+R.err.rlp);if(R.err.rli)F('RLI '+R.err.rli);
 try{R.rjx=rjxAudit();if(!R.rjx.ok)F('rjxAudit')}catch(e){F('rjxAudit:'+e)}
 try{const t=tcTurnoutAudit();R.tct={ok:t.ok,bad:t.bad};if(!t.ok)F('tcTurnoutAudit '+t.bad.join(','))}catch(e){F('tct:'+e)}
 try{const a=rlAudit();R.rl={ok:a.ok,issues:a.issues,trains:a.trains,trainsOk:a.trainsOk,minR:a.minR};if(!a.ok)F('rlAudit '+a.issues.slice(0,4).join(' | '))}catch(e){F('rlAudit:'+e)}
 /* 0. the existing day checks (19א — שדרוג הקיים): tcRailPaxAudit (D‑536 — יום משחק שלם של כל הרכבות: בלי שתי רכבות בבלוק, בלי קפיצה, בלי עמידה של יותר מ-60 שנ׳ מחוץ לתחנה / עצירה / אות), rliAudit (רכבת האי), railNetAudit */
 try{const a=tcRailPaxAudit();R.pax={ok:a.ok,issues:a.issues,samples:a.samples,dayS:a.dayS,stops:a.stops,runTimes:a.runTimes};if(!a.ok)F('tcRailPaxAudit '+a.issues.slice(0,4).join(' | '))}catch(e){F('tcRailPaxAudit:'+e)}
 try{const a=rliAudit();R.rli={ok:a.ok,issues:(a.issues||[]).slice(0,8)};if(!a.ok)F('rliAudit '+(a.issues||[]).slice(0,3).join(' | '))}catch(e){F('rliAudit:'+e)}
 try{const a=railNetAudit();R.net={ok:a.ok,issues:(a.issues||[]).slice(0,8)};if(!a.ok)F('railNetAudit '+(a.issues||[]).slice(0,3).join(' | '))}catch(e){F('railNetAudit:'+e)}
 try{const a=rlSweepAudit();R.sweep={ok:a.ok,issues:(a.issues||[]).slice(0,8),minGap:a.minGap,n:a.n};const tt=(a.issues||[]).filter(s=>/^train-(train|stock)/.test(s));if(tt.length)F('sweep '+tt.slice(0,3).join(' | '))}catch(e){R.sweep={err:String(e).slice(0,200)}}   /* רכבת על רכבת / על קרון עומד — חוסם; self-overlap (קרונות של אותה רכבת בקשת) — מידע, היה גם ב-S7F303 */
 /* 1. every crossing of two tracks away from a node: inside a junction drawing (RJX zone) with its frogs */
 const X=[],nodes=RAIL_NODES.map(n=>[n.x,n.y]);
 for(let i=0;i<RAIL_SEGS.length;i++)for(let j=i+1;j<RAIL_SEGS.length;j++){const A=RAIL_SEGS[i].pts,B=RAIL_SEGS[j].pts;for(const f of rjxInter(A,B)){if(nodes.some(q=>Math.hypot(q[0]-f.x,q[1]-f.y)<3))continue;const Z=RJX.zones.find(z=>f.x>z.box[0]&&f.x<z.box[2]&&f.y>z.box[1]&&f.y<z.box[3]);
   const fl=Z&&Z.swap?{x:f.y,y:f.x}:f,fr=Z?rjxPrep(Z).frogs.filter(q=>Math.hypot(q.x-fl.x,q.y-fl.y)<45).length:0;X.push({a:RAIL_SEGS[i].id,b:RAIL_SEGS[j].id,x:Math.round(f.x),y:Math.round(f.y),zone:Z?Z.id:null,frogs:fr});if(!Z||fr<4)F('crossing-not-drawn:'+RAIL_SEGS[i].id+'x'+RAIL_SEGS[j].id)}}
 R.crossings=X;
 /* 2. every turnout (a node with 3 track ends, or the end of a track in the middle of another): drawn by a turnout painter */
 const ends={};for(const g of RAIL_SEGS)for(const id of[g.from,g.to])ends[id]=(ends[id]||0)+1;
 const on=(n,g)=>{for(let i=1;i<g.pts.length;i++){const a=g.pts[i-1],b=g.pts[i],dx=b[0]-a[0],dy=b[1]-a[1],L2=dx*dx+dy*dy||1,u=Math.max(0,Math.min(1,((n.x-a[0])*dx+(n.y-a[1])*dy)/L2));if(Math.hypot(a[0]+dx*u-n.x,a[1]+dy*u-n.y)<.6&&u>0&&u<1)return true}return false};
 const T=[];for(const n of RAIL_NODES){const mid=ends[n.id]===1&&RAIL_SEGS.some(g=>g.from!==n.id&&g.to!==n.id&&on(n,g));if(!(ends[n.id]>=3||mid))continue;
  const segs=RAIL_SEGS.filter(g=>g.from===n.id||g.to===n.id).map(g=>g.id);let by=null;
  for(const J of TCT_J){const [a,b]=J.main,inMain=Math.min(a[0],b[0])-1<=n.x&&n.x<=Math.max(a[0],b[0])+1&&Math.min(a[1],b[1])-1<=n.y&&n.y<=Math.max(a[1],b[1])+1;if(inMain&&J.div.some(d=>d.seg?segs.includes(d.seg):true)){by=J.id;break}}
  if(!by)for(const Z of RJX.zones)if(Z.sw.some(s=>s.node===n.id))by=Z.id;
  if(!by&&n.port&&n.y>=4960)by='port-flush';
  if(!by&&/^ISL-X/.test(n.id))by='island4-bridge';
  T.push({id:n.id,by});if(!by)F('turnout-not-drawn:'+n.id)}
 R.turnouts=T;
 /* 3. the trains over a whole cycle (1 s): the stops of every run are reached, and the train never stands still in the middle of a run */
 R.trains=[];for(const Tr of RL_TRAINS){if(Tr.err){F('train-err:'+Tr.id);continue}const o={id:Tr.id,cycle:Math.round(Tr.cycle),stops:[],stall:0};let still=0;const seen=new Set();
  for(let s=0;s<Tr.cycle;s+=1){const S=rlState(Tr,(s-(Tr.off||0))*1000);if(!S)continue;if(!S.moving)seen.add(S.k+':'+(S.R.stop||''));if(S.moving&&S.v<1e-3&&S.tin>2&&S.tin<S.R.tm-2){still++;if(still===4)o.stall++}else still=0}
  o.stops=[...seen].sort();if(seen.size<Tr.runs.length)F('train-misses-stop:'+Tr.id);if(o.stall)F('train-stalls:'+Tr.id+':'+o.stall);R.trains.push(o)}
 return R})()
