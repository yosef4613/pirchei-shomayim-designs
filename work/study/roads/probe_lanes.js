// probe_lanes.js — R-16: every movement at every junction (MOVES2) with its approach lane — read only → game_lanes.json
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const game = '/home/claude/work/exp34/kit/dev/_game_eval.html';
  const b = await chromium.launch({ args: ['--disable-gpu', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1200, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + game + '#noauto', { timeout: 240000 }); await p.waitForTimeout(6000);
  const rs = await p.evaluate(() => window.__TC_EVAL(`(()=>{
    const out={has:typeof MOVES2!=='undefined'};
    if(!out.has)return JSON.stringify(out);
    const one=MOVES2.values().next().value; out.moveKeys=Object.keys(one||{}); out.fromKeys=Object.keys((one&&one.from)||{});
    out.moves=[...MOVES2.values()].map(m=>({id:m.id,kind:m.kind,node:m.node||m.nodeId||(m.from&&m.from.nodeTo),fk:m.from&&m.from.k,fc:m.from&&m.from.cnt,fe:m.from&&(m.from.edge||m.from.edgeId),tk:m.to&&m.to.k,tc:m.to&&m.to.cnt,te:m.to&&(m.to.edge||m.to.edgeId)}));
    out.signals=[...NODES2.values()].filter(n=>n.signal).length;
    return JSON.stringify(out)})()`));
  const r = JSON.parse(rs); fs.writeFileSync(path.join(__dirname, 'game_lanes.json'), JSON.stringify(r, null, 1));
  console.log('has', r.has, 'moves', r.moves && r.moves.length, 'keys', (r.moveKeys || []).join(','), '| from', (r.fromKeys || []).join(','), 'signals', r.signals);
  console.log('errors', errs.length, errs.slice(0, 2)); await b.close();
})();
