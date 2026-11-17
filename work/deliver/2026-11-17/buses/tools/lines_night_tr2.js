// lines_night.js <game.html> <out.json> — יום, חזרה בלילה (00:35), שטיפה ותדלוק, ויציאה בבוקר (05:29): הסדר בחניון.
// (עותק של linesA, ‏deliver/2026-11-10/linesA/tools; ‏buses 17.11: בסוף גם busesAudit() — הספירה של ‏074zu, כשיש)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const step = (s) => p.evaluate(s => { window.__TC_SIM_STEP_QA({ seconds: s, warmup: 0, every: s }); const a = window.__TC_LINES.audit(); return { clock: window.__TC_CLOCK().hhmm, a } }, s);
  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{window.__L2TR=[];const o=lnTermSample;lnTermSample=function(){o.apply(this,arguments);const A=LN.aud;if(!A.tm)return;const R=v=>Math.round(v);for(const b of LN.bus){const v=b.v;if(!v)continue;const k=A.tm.roadT[b.id]||0;if(k>=2&&window.__L2TR.length<40){const ah=TRAFFIC_CARS.filter(q=>q!==v&&Math.hypot(q.x-v.x,q.y-v.y)<70).map(q=>[q.id,R(q.x),R(q.y),+(q.speed||0).toFixed(1),q.ln?q.ln.no+':'+q.ln.ph:null,q.junctionLock||null]);window.__L2TR.push({t:+LN.t.toFixed(1),clock:gameClock().hhmm,cnt:k,no:b.no,ph:b.ph,dir:b.dir,tgt:b.target,gOut:b.gOut||null,gIn:b.gIn||null,dh:b.deadhead?1:0,edge:v.edgeId,ds:v.dirSign,et:+(v.t||0).toFixed(3),x:R(v.x),y:R(v.y),sp:+(v.speed||0).toFixed(2),wait:v.wait,jl:v.junctionLock||null,route:(v.c5&&v.c5.route||[]).map(q=>q.edgeId+':'+q.dirSign).join('>'),ri:v.routeIndex,fin:v.c5&&v.c5.finalT,near:ah,sig:(()=>{try{const r=v.c5.route||[],i=v.routeIndex||0,nx=r[i+1],L=lane2(v.edgeId,v.dirSign,v.lane||0);if(!L||!nx)return 'no-next';const mv=L.moves.find(m=>m.to.edge===nx.edgeId&&m.to.dir===nx.dirSign);if(!mv)return 'no-move';const nd=NODES2.get(mv.node),ph=SignalCore2.phaseOf(mv.node);return{node:mv.node,signal:!!(nd&&nd.signal),kind:mv.kind,allowed:SignalCore2.movementAllowed(mv,ph),phase:JSON.stringify(ph).slice(0,90),toEnd:Math.round(L.len*(1-(v.t||0)))}}catch(e){return 'err '+String(e).slice(0,60)}})()})}}};return 1})()`));
  const rows = []; const show = (tag, r) => { const a = r.a; rows.push({ tag, ...r }); console.log(`${tag} ${r.clock} ok=${a.ok} out=${a.inService} depot=${a.inDepot} tgt=${a.target} ret=${a.stats.ret} wash=${a.stats.wash} fuel=${a.stats.fuel} park=${a.stats.parked} dep=${a.stats.dep} fifo=${a.fifo.join(',')} off=${a.off.length} pax=${a.paxOk} yields=${a.stats.yields || 0}`); console.log('   ' + a.buses_.map(x => x.no + ':' + x.ph + (x.slot ? '[' + x.slot + ']' : '') + (x.blk ? '(' + x.blk + ')' : '')).join(' ')) };
  show('day', await step(420));
  await p.evaluate(() => window.__TC_DEV.ev('gameClockSet(0,35)'));
  for (let i = 1; i <= 8; i++) show('night' + i, await step(150));
  // the morning: the clock runs on from the night (05:30 — out by the order they came in)
  for (let i = 1; i <= 3; i++) show('day2-' + i, await step(200));
  const fin = await p.evaluate(() => ({ tr: window.__L2TR, log: window.__TC_LINES.log(), audit: window.__TC_LINES.audit(), d5: (() => { try { return window.__TC_D5DEPOT33() } catch (e) { return String(e) } })() }));
  let bsv = null; try { bsv = await p.evaluate(() => window.__TC_DEV.ev("typeof busesAudit==='function'?busesAudit():null")) } catch (e) { bsv = String(e).slice(0, 200) }
  fs.writeFileSync(out, JSON.stringify({ rows, fin, bsv, errs }, null, 1)); console.log('bsv', JSON.stringify(bsv && bsv.first || bsv).slice(0, 400)); console.log('d5', JSON.stringify(fin.d5).slice(0, 300)); console.log('errs', errs.length, errs.slice(0, 3).join(' | ')); await b.close();
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
