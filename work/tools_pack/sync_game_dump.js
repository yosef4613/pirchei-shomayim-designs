// 8.11.2026 · sync_game_dump — מה שבנוי במשחק, לבדיקת הסנכרון (tools_pack/sync_check.py — R-83 סעיף ט, ‏R-87 סעיף ה).
// קורא בלבד: הכותרות, הרשת (צמתים, קטעים), הרמזורים, מעברי החצייה, התחנות, מסלולי הקווים ומשימת M-BUS-01.
// node sync_game_dump.js <game.html> <out.json>   (דפדפן אחד, קצר)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const o={err:{}};const R=v=>Math.round(v*10)/10;
   const tryv=(k,f)=>{try{o[k]=f()}catch(e){o.err[k]=String(e).slice(0,160)}};
   tryv('title',()=>document.title);
   tryv('h1',()=>[...document.querySelectorAll('h1')].map(h=>h.textContent.trim()).filter(Boolean).slice(0,5));
   tryv('BUILD',()=>BUILD); tryv('FILE_SCOPE',()=>FILE_SCOPE);
   tryv('nodes',()=>NODES.map(n=>({id:n.id,x:R(n.x),y:R(n.y),kind:n.kind||n.type||''})));
   tryv('edges',()=>EDGES.map(e=>({id:e.id,a:e.a,b:e.b,name:e.name||'',cls:e.cls||'',future:!!e.future,pts:(e.pts||[]).map(t=>[R(t.x??t[0]),R(t.y??t[1])])})));
   tryv('signals',()=>[...SIGNAL_NODE_IDS]);
   tryv('xw',()=>CROSSWALKS.map(c=>({id:c.id,road:c.roadId,node:c.signalNode||null,x:R(c.x),y:R(c.y),sig:!!c.signalized})));
   tryv('zebra',()=>ZEBRA_XW.map(z=>({id:z.id,road:z.roadId,node:z.node||null,x:R(z.x),y:R(z.y)})));
   tryv('stops',()=>ALL_BUS_STOPS.map(s=>{const q={};for(const k of Object.keys(s))if(['number','string','boolean'].includes(typeof s[k]))q[k]=typeof s[k]==='number'?R(s[k]):s[k];return q}));
   tryv('term',()=>Object.fromEntries(Object.entries(BUS_TERMINAL_STOPS).map(([l,s])=>[l,{id:s.id,x:R(s.x),y:R(s.y),chunk:s.chunk}])));
   tryv('lines',()=>BUS_LINES.slice());
   o.routes={};try{for(const l of BUS_LINES){const rt=busRouteForLine(l);o.routes[l]=rt.map(s=>({edgeId:s.edgeId,dirSign:s.dirSign}))}}catch(e){o.err.routes=String(e).slice(0,160)}
   tryv('busVehicles',()=>BUS_VEHICLES.length);
   tryv('mbus',()=>{const m=MISSION_DEFS['M-BUS-01'];const q={};for(const k of Object.keys(m))if(['number','string','boolean'].includes(typeof m[k]))q[k]=m[k];return q});
   return o})()`));
  r.pageErrors = errs.slice(0, 20); r.file = path.basename(file);
  fs.writeFileSync(out, JSON.stringify(r));
  console.log('צמתים', (r.nodes || []).length, 'קטעים', (r.edges || []).length, 'מעברים', (r.xw || []).length, 'תחנות', (r.stops || []).length, 'שגיאות', Object.keys(r.err).length);
  await b.close();
})();
