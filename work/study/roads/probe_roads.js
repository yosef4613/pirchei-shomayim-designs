// probe_roads.js — R-15 (the owner 29.10 12:00): the whole road network as the game has it (the eval copy, read only) → game_roads.json
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const game = '/home/claude/work/exp34/kit/dev/_game_eval.html';
  const b = await chromium.launch({ args: ['--disable-gpu', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1200, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + game + '#noauto', { timeout: 240000 }); await p.waitForTimeout(5000);
  const rs = await p.evaluate(() => window.__TC_EVAL(`(()=>{
    const r2=v=>typeof v==='number'?Math.round(v*100)/100:v;
    const out={};
    out.nodes=Object.values(byNode).map(n=>({id:n.id,x:r2(n.x),y:r2(n.y),type:n.type,label:n.label,signal:!!(n.signal||n.signals||n.light),r:typeof nodeRadius==='function'?r2(nodeRadius(n)):null}));
    out.edges=Object.values(byEdge).map(e=>{const t=roadType(e)||{};const o={id:e.id,a:e.a,b:e.b,cls:e.cls,name:e.name,future:!!e.future,oneway:!!(e.oneway||e.oneWay),width:t.width,lanes:t.lanes,sidewalk:t.sidewalk,corridor:e.corridor||null};if(Array.isArray(e.pts))o.pts=e.pts.map(q=>Array.isArray(q)?q.map(r2):[r2(q.x),r2(q.y)]);return o});
    out.edgeKeys=Object.keys(Object.values(byEdge)[0]||{});out.nodeKeys=Object.keys(Object.values(byNode)[0]||{});
    out.chunks=typeof MAP_CHUNKS!=='undefined'?MAP_CHUNKS.map(c=>({id:c.id,x:c.x,y:c.y,w:c.w,h:c.h,label:c.label||c.name})):null;
    out.world=typeof WORLD!=='undefined'?{w:WORLD.w,h:WORLD.h}:null;
    return JSON.stringify(out)})()`));
  const r = JSON.parse(rs); fs.writeFileSync(path.join(__dirname, 'game_roads.json'), JSON.stringify(r, null, 1));
  console.log('nodes', r.nodes.length, 'edges', r.edges.length, 'edgeKeys', r.edgeKeys.join(','), 'nodeKeys', r.nodeKeys.join(','), 'chunks', r.chunks && r.chunks.length, 'world', JSON.stringify(r.world));
  console.log('errors', errs.length, errs.slice(0, 2)); await b.close();
})();
