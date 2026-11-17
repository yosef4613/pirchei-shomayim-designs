// q_lines.js — מה שבנוי במשחק לטבלת המוכנות של הקווים (R-88): הרשת, התחנות של הקווים, תחנות המפה, המפרצים והקווים. בונה S7F267.
// node qa_tools/probe_c2.js <game.html> qa_tools/q_lines.js <out.json>
return (()=>{const R=v=>Math.round(v*10)/10,o={build:(typeof BUILD!=='undefined'?BUILD:''),lines:BUS_LINES.slice(),paused:(typeof BUS_LINES_PAUSED!=='undefined'?BUS_LINES_PAUSED:null),buses:BUS_VEHICLES.length};
 o.nodes=NODES.map(n=>({id:n.id,x:R(n.x),y:R(n.y),type:n.type||n.kind||''}));
 o.edges=EDGES.map(e=>({id:e.id,a:e.a,b:e.b,cls:e.cls||'',future:!!e.future,name:e.name||'',pts:(e.pts||[]).map(t=>[R(t.x??t[0]),R(t.y??t[1])])}));
 const bayC=(F,bay)=>{const h=F.roadW/2,d=bay?h+BUS_BAY.depth/2:h;return[R(F.rx+F.nx*d),R(F.ry+F.ny*d)]};
 o.bays=[...BUS_PHYS.map(p=>({id:p.id,kind:'line',bay:!!p.bay,lines:p.lines.slice(),stops:p.stops.slice(),edge:p.edgeId,dir:p.dirSign,c:bayC(p.F,p.bay),chunk:currentChunkId(p.F.rx+p.F.nx*(p.F.roadW/2+15),p.F.ry+p.F.ny*(p.F.roadW/2+15))})),
  ...S6_MAP_STOPS.map(s=>({id:s.id,kind:'map',bay:!!s.bay,lines:(s.mapLines||[]).map(Number),stops:[s.id],st:s.st,edge:s.edgeId,dir:s.dirSign,c:bayC(s.F,s.bay),noBay:s.noBay||'',chunk:s.chunk}))];
 o.term=Object.fromEntries(BUS_LINES.map(l=>[l,{id:BUS_TERMINAL_STOPS[l].id,x:R(BUS_TERMINAL_STOPS[l].x),y:R(BUS_TERMINAL_STOPS[l].y)}]));
 o.routes=Object.fromEntries(BUS_LINES.map(l=>[l,busRouteForLine(l).map(q=>q.edgeId+':'+q.dirSign)]));
 o.routeText=Object.fromEntries(BUS_LINES.map(l=>[l,busRouteText(l)]));
 o.left=(typeof S267_BAYS_LEFT!=='undefined')?S267_BAYS_LEFT:{};
 o.rb=Object.keys((typeof RB2!=='undefined'&&RB2)||{});
 return JSON.stringify(o)})()
