// rails 17.11 — שאילתה: כל רשת המסילות (צמתים, קטעים, מסוטים מצוירים, רכבות ומסלוליהן) — לתיעוד ולמדידה מחוץ לדפדפן
return (()=>{const R={nodes:[],segs:[],tct:[],bridges:[],trains:[],extra:{},errs:[]};
 const r3=v=>Math.round(v*10)/10;
 try{for(const n of RAIL_NODES)R.nodes.push({id:n.id,x:n.x,y:n.y,type:n.type||'',chunk:n.chunk||''})}catch(e){R.errs.push('nodes:'+e)}
 try{for(const g of RAIL_SEGS){const o={};for(const k in g){if(k[0]==='_')continue;const v=g[k];if(k==='pts'){o.pts=v.map(p=>[r3(p[0]),r3(p[1])]);continue}if(typeof v==='function')continue;if(v&&typeof v==='object'&&!Array.isArray(v))continue;o[k]=v}R.segs.push(o)}}catch(e){R.errs.push('segs:'+e)}
 try{for(const J of TCT_J){R.tct.push({id:J.id,main:J.main,div:J.div.map(d=>d.seg?{seg:d.seg,rev:!!d.rev}:{pts:(tctDivPts(d)||[]).map(p=>[r3(p[0]),r3(p[1])])}),half:J.half||0,deck:!!J.deck})}}catch(e){R.errs.push('tct:'+e)}
 try{R.bridges=RL_BRIDGES.slice()}catch(e){R.errs.push('br:'+e)}
 try{for(const T of RL_TRAINS){if(T.err){R.trains.push({id:T.id,err:String(T.err)});continue}R.trains.push({id:T.id,label:T.label||'',cycle:r3(T.cycle),L:r3(T.L),runs:T.runs.map(r=>({stop:r.stop,thru:!!r.thru,legs:(r.legs||[]).map(l=>l[0]),len:r3(r.P&&r.P.len||0)}))})}}catch(e){R.errs.push('trains:'+e)}
 const tryPts=(name,f)=>{try{const v=f();if(v)R.extra[name]=v}catch(e){}};
 tryPts('F56_SIDING',()=>F56_SIDING.pts.map(p=>[r3(p[0]),r3(p[1])]));
 tryPts('RL_COAST_X',()=>RL_COAST_X);tryPts('RL_DECK_W',()=>RL_DECK_W);tryPts('PORT_SIDING_Y',()=>PORT_SIDING_Y);
 tryPts('S13_SPANX',()=>S13_SPANX);tryPts('G74_BRIDGE',()=>G74_BRIDGE);
 tryPts('audit',()=>{const a=rlAudit();return{ok:a.ok,issues:a.issues,trains:a.trains,minR:a.minR}});
 return R})()
