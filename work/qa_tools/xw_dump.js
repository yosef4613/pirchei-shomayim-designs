// 3.11 23:30 · xw_dump — the junctions, their arms and the crossings of the game, for xw_gate.py (the review 23:16: a crossing on every arm; the map against the game)
// node xw_dump.js <game.html> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const o={nodes:[],edges:[],xw:[],zebra:[],signals:[],tRule:[],inter:[]};
   const R=v=>Math.round(v*10)/10;
   for(const n of NODES)o.nodes.push({id:n.id,x:R(n.x),y:R(n.y),kind:n.kind||n.type||''});
   for(const e of EDGES)o.edges.push({id:e.id,a:e.a,b:e.b,name:e.name||'',cls:e.cls||'',future:!!e.future,half:(typeof _ROAD_HALF==='function'?R(_ROAD_HALF(e)):null),
     p1:(e.pts&&e.pts.length>1)?[R(e.pts[1].x??e.pts[1][0]),R(e.pts[1].y??e.pts[1][1])]:null,pn:(e.pts&&e.pts.length>1)?[R(e.pts[e.pts.length-2].x??e.pts[e.pts.length-2][0]),R(e.pts[e.pts.length-2].y??e.pts[e.pts.length-2][1])]:null});
   for(const c of CROSSWALKS)o.xw.push({id:c.id,road:c.roadId,node:c.signalNode||null,x:R(c.x),y:R(c.y),sig:!!c.signalized});
   try{for(const z of ZEBRA_XW)o.zebra.push({id:z.id,road:z.roadId,node:z.node||(String(z.id).split('-').length>2?null:null),x:R(z.x),y:R(z.y)})}catch(e){o.zebraErr=String(e)}
   o.drawn=[];for(const k of ['A34D','A34_BASE','D3ND','C3D','C4ND','D4ND','C5ND','D5ND','B4G','B3LOOKD','B3NG','A5ND','A5G','B5ND','E3ND','P560D','P560']){let D;try{D=eval(k)}catch(e){D=undefined}if(!D||!Array.isArray(D.zebra))continue;
    for(const z of D.zebra){const cx=(z[0]+z[2])/2,cy=(z[1]+z[3])/2;let r=null,bd=1e9;for(const q of EDGES){const a=_NODE_BY_ID[q.a],b=_NODE_BY_ID[q.b];if(!a||!b)continue;const L=Math.hypot(b.x-a.x,b.y-a.y)||1,t=((cx-a.x)*(b.x-a.x)+(cy-a.y)*(b.y-a.y))/(L*L);if(t<0||t>1)continue;const d=Math.abs((b.x-a.x)*(cy-a.y)-(b.y-a.y)*(cx-a.x))/L;if(d<bd){bd=d;r=q.id}}
     o.drawn.push({id:k+'.zebra@'+Math.round(cx)+','+Math.round(cy),road:r,node:null,x:R(cx),y:R(cy),drawnOnly:true})}}
   o.signals=[...SIGNAL_NODE_IDS];o.inter=INTERSECTION_NODES.map(n=>n.id);
   try{o.tRule=P523.tRule.map(q=>[q[0],q[1]])}catch(e){o.tRuleErr=String(e)}
   try{o.zones={};for(const n of NODES)o.zones[n.id]=r76Zone(n.x,n.y)}catch(e){}
   try{o.build=document.title}catch(e){}
   return o})()`));
  fs.writeFileSync(out, JSON.stringify(r)); console.log('nodes', r.nodes.length, 'edges', r.edges.length, 'xw', r.xw.length, 'zebra', r.zebra.length, 'signals', r.signals.length, 'tRule', r.tRule.length);
  await b.close();
})();
