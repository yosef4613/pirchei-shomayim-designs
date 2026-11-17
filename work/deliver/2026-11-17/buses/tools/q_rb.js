// q_rb.js <game.html> <out.json> [warm=420] [secs=1500] — buses (17.11, הבעלים 10:45: "הכיכרות לא מספיק מסונכרנים למנוע הרכבים"): מדידה בכל כיכר (RB2).
// הרצה מהירה (__TC_SIM_STEP_QA), כל שנייה: כל רכב של V2 ליד כיכר — בגישה (בנתיב שנכנס לכיכר, עד 260 פיקס׳ לפני הקצה), בטבעת (בתנועה של הכיכר), ביציאה
// (בנתיב שיוצא, עד 120 פיקס׳) — עומד (מהירות < 0.5) או נוסע. לכל עמידה רצופה: האורך, הסיבה (c2.limit של V2), והמקום. בסוף, לכל כיכר: כמה עמידות מעל 5 שנ׳ ומעל 30,
// לפי המקום ולפי הסיבה; העמידה הארוכה; כמה רכבים עברו (נכנסו לטבעת); והתשובות של rbYield2 / ‏movementReady2 לכל כיכר (עטיפה בזמן הבדיקה בלבד).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const INSTR = `(()=>{const Q=window.__RBQ={y:{},m:{},b:{},bl:{},sp:{}};const inc=(o,k)=>{o[k]=(o[k]||0)+1};
 /* who the entry gives way to (the same arithmetic as rbYield2, 071): the ring part / a granted one on its way in; moving or standing; and what the standing one waits for */
 const who=(v,mv,node)=>{const R=mv.rb,cfg=node.rb;for(const o of node.inside){if(o.v===v||o.remote||o.ghost||o.standing)continue;const c=o.v&&o.v.c2;if(!c)continue;let th,pre=0,post=0,rem,ph;
   if(c.mv&&c.mv.rb&&c.mv.node===node.id){const q=rbTheta2(c);th=q.th;pre=q.pre;post=q.post;ph=['in-curve','ring','out-curve'][q.phase];rem=q.phase===0?c.mv.rb.D:q.phase===1?q.th-c.mv.rb.a1:0}
   else{const m2=(c.next&&c.next.rb&&c.next.node===node.id)?c.next:(c.gate&&c.gate.mv&&c.gate.mv.rb&&c.gate.node===node.id?c.gate.mv:null);if(!m2||!c.lane||c.lane!==m2.from)continue;th=m2.rb.a0;pre=m2.rb.Le+Math.max(0,m2.sStart-c.s);rem=m2.rb.D;ph='granted-lane'}
   const sp=o.v.speed||0,mo=sp>2?'mov':'stop';const up=rbMod2(th-R.a0);if(up<=rem+.02&&up*R.Rc+pre<cfg.win+sp*1.1)return[ph+':'+mo+':up',c,o.v,Math.round(up*R.Rc+pre)];
   const dn=rbMod2(R.a0-th)*R.Rc;if(pre<1&&dn<c.hl+v.c2.hl+14-post)return[ph+':'+mo+':dn',c,o.v,Math.round(dn)]}return null};
 try{const y0=rbYield2;rbYield2=function(v,mv,node){const r=y0.apply(this,arguments);if(r&&node){const k=node.id+'|'+String(r).replace(/[0-9]+/g,'#').replace(/^(PC|AI|A4|VH|LV)-.*/,'veh:$1');inc(Q.y,k);
   if(r==='rb-yield'){try{const w=who(v,mv,node);const lane=mv.from.id;if(w){inc(Q.b,node.id+'|'+lane+'|'+w[0]+'|'+(o=>o.ln?'bus':'car')(w[2]));if(w[0].includes(':stop'))inc(Q.bl,node.id+'|'+w[0].split(':')[0]+'|'+String(w[1].limit||'?').replace(/[0-9]+/g,'#')+'|to:'+(w[1].mv?w[1].mv.to.id:(w[1].next?w[1].next.to.id:'?')))}else inc(Q.b,node.id+'|'+lane+'|?')}catch(e){Q.e9=String(e)}}}return r}}catch(e){Q.e1=String(e)}
 try{const m0=movementReady2;movementReady2=function(v,mv,node,opts){const r=m0.apply(this,arguments);if(r&&node&&node.rb){inc(Q.m,node.id+'|'+String(r).replace(/[0-9]+/g,'#'));if(r==='space'||r==='queue')inc(Q.sp,node.id+'|'+r+'|'+mv.from.id+'>'+mv.to.id)}return r}}catch(e){Q.e2=String(e)}
 return Object.keys(Q).filter(k=>k.startsWith('e')).map(k=>Q[k])})()`;
const SAMPLE = `(()=>{const o=[];const T=(v)=>v.ln?'bus':(/^AI-CAR|^A4-CIV/.test(String(v.id))?'car':'oth');
 for(const v of TRAFFIC_CARS){const c=v.c2;if(!c||v.ghost)continue;let rb=null,where=null;
  if(c.mv&&RB2[c.mv.node]){rb=c.mv.node;where='ring'}
  else if(c.lane&&RB2[c.lane.nodeTo]&&c.s>c.lane.len-260){rb=c.lane.nodeTo;where='approach'}
  else if(c.lane&&RB2[c.lane.nodeFrom]&&c.s<120){rb=c.lane.nodeFrom;where='exit'}
  if(!rb)continue;let why=String(c.limit||'?');if(why.startsWith('contact:')){const w=VEH_BY_ID2.get(why.slice(8));why='contact:'+(w?T(w):'sub')}else why=why.replace(/[0-9]+/g,'#');
  o.push([String(v.id),rb,where,+(v.speed||0).toFixed(1),why,T(v),Math.round(v.x),Math.round(v.y),c.lane?c.lane.id:(c.mv?c.mv.id:''),c.mv?1:0])}
 const ins={};for(const id in RB2){const n=NODES2.get(id);ins[id]=n?n.inside.filter(q=>!q.remote&&!q.ghost).length:null}
 return{clk:gameClock().hhmm,o,ins}})()`;
(async () => {
  const [file, out, warmA, secsA] = process.argv.slice(2); const warm = +warmA || 420, secs = +secsA || 1500;
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const step = s => p.evaluate(s => { window.__TC_SIM_STEP_QA({ seconds: s, warmup: 0, every: s }); return 1 }, s);
  const t0 = Date.now(); await step(warm); const ie = await ev(INSTR);
  const S = {}; const run = {}; let clk0 = null, clk1 = null;
  const R = id => S[id] = S[id] || { veh: new Set(), ringVeh: new Set(), stops5: 0, stops30: 0, stopS: 0, moveS: 0, byWhere: {}, byWhy: {}, longest: [], insMax: 0, ringStops5: 0 };
  const close = (k, r) => { const s = R(r.rb); if (r.n > 5) { s.stops5++; s.byWhere[r.where] = (s.byWhere[r.where] || 0) + 1; s.byWhy[r.why] = (s.byWhy[r.why] || 0) + 1; if (r.where === 'ring') s.ringStops5++; if (r.n > 30) s.stops30++;
    s.longest.push([r.n, r.id, r.where, r.why, r.t, r.x, r.y, r.lane]); s.longest.sort((a, b) => b[0] - a[0]); if (s.longest.length > 8) s.longest.length = 8 } };
  for (let i = 0; i < secs; i++) {
    await step(1); const r = await ev(SAMPLE); if (!clk0) clk0 = r.clk; clk1 = r.clk; const seen = new Set();
    for (const id in r.ins) { const s = R(id); s.insMax = Math.max(s.insMax, r.ins[id] || 0) }
    for (const q of r.o) {
      const [id, rb, where, sp, why, t, x, y, lane, inRing] = q; const s = R(rb); s.veh.add(id); if (inRing) s.ringVeh.add(id); const k = id; seen.add(k);
      if (sp < 0.5) { s.stopS++; const cur = run[k]; if (cur && cur.rb === rb) cur.n++; else { if (cur) close(k, cur); run[k] = { id, rb, where, why, n: 1, t: r.clk, x, y, lane } } }
      else { s.moveS++; if (run[k]) { close(k, run[k]); delete run[k] } }
    }
    for (const k in run) if (!seen.has(k)) { close(k, run[k]); delete run[k] }
    if (i % 250 === 0) console.log('t', i, r.clk, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  for (const k in run) close(k, run[k]);
  const Y = await ev('window.__RBQ');
  const F = (o, id) => Object.fromEntries(Object.entries(o || {}).filter(([k]) => k.startsWith(id + '|')).map(([k, v]) => [k.slice(id.length + 1), v]).sort((a, b) => b[1] - a[1]).slice(0, 25));
  const res = {}; for (const id in S) { const s = S[id]; res[id] = { vehicles: s.veh.size, through: s.ringVeh.size, stops5: s.stops5, stops30: s.stops30, ringStops5: s.ringStops5, stopShare: +(s.stopS / Math.max(1, s.stopS + s.moveS)).toFixed(3), insideMax: s.insMax, byWhere: s.byWhere,
    byWhy: Object.fromEntries(Object.entries(s.byWhy).sort((a, b) => b[1] - a[1])), longest: s.longest,
    rbYield: Object.fromEntries(Object.entries(Y.y || {}).filter(([k]) => k.startsWith(id + '|')).map(([k, v]) => [k.slice(id.length + 1), v]).sort((a, b) => b[1] - a[1])),
    ready: Object.fromEntries(Object.entries(Y.m || {}).filter(([k]) => k.startsWith(id + '|')).map(([k, v]) => [k.slice(id.length + 1), v]).sort((a, b) => b[1] - a[1])),
    yieldTo: F(Y.b, id), standingWaits: F(Y.bl, id), space: F(Y.sp, id) } }
  let aud = null; try { aud = await ev("typeof rbsAudit==='function'?rbsAudit():null") } catch (e) { aud = String(e).slice(0, 200) }
  let stuckEnd = null; try { stuckEnd = await ev("(()=>{const o={};for(const v of TRAFFIC_CARS){const s=+(v.stuck||0);if(s<=60)continue;const k=String(v.edgeId||(v.c2&&v.c2.lane&&v.c2.lane.edge)||'?');(o[k]=o[k]||[]).push([String(v.id),Math.round(s)])}return o})()") } catch (e) { stuckEnd = String(e).slice(0, 200) }
  const O = { build: path.basename(file), warm, secs, clk0, clk1, instrErr: ie, rb: res, aud, stuckEnd, errs, wallS: ((Date.now() - t0) / 1000) | 0 };
  fs.writeFileSync(out, JSON.stringify(O, null, 1));
  for (const id in res) { const x = res[id]; console.log(id, 'veh', x.vehicles, 'through', x.through, 'stops>5', x.stops5, '>30', x.stops30, 'ring>5', x.ringStops5, 'share', x.stopShare, 'insMax', x.insideMax, JSON.stringify(x.byWhy).slice(0, 300), '| long', JSON.stringify(x.longest.slice(0, 2))) }
  console.log('errs', errs.length, errs.slice(0, 2).join(' | ')); await b.close();
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
