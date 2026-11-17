// island 17.11: עותק של deliver/2026-11-11/line5c/tools/l5c_run.js (line5c) — לקו 5א על דרך המזרח; בלי שינוי בלוגיקה
// l5c_run.js <game.html> <out.json> [secs=2880] [chunk=10] [query] — line5c (11.11): הסימולציה מהר (__TC_SIM_STEP_QA), ובכל קטע:
//  · באי (קטעי IS-* והגשר BR-I13/14 — המלבן שלהם + 30): כל רכב שעומד יותר מ-5 שנ׳ — המקסימום והסיבה של המנוע ברגע הזה (השדות של stuckmax_why), ומצב הצמתים ISE-0 ו-IL כשמישהו עומד יותר מ-60 שנ׳;
//  · הקווים (__TC_LINES.audit: ok / err / frz), ‏frozenMax, הגשר המתרומם, וקו 5 (__TC_L5RUN) אם קיים;
//  · כל עצירה של קואץ׳ של קו 5 ברציף (עטיפה של lnBayStart): התחנה, הזמן, המרחק מהמפרץ, הדלתות — והסבבים.  יום במשחק = 2,880 שנ׳.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, secS, chS, q] = process.argv.slice(2); const SEC = +(secS || 2880), CH = +(chS || 10);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + (q ? '?' + q : '') + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  if (process.env.PRE) console.log('pre', JSON.stringify(await ev(process.env.PRE)));
  const init = await ev(`(()=>{const G=window.__L5C={isl:{},snaps:[],stops:[],t0:LN.t};let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
   for(const L of LANE_LIST2){if(!/^(IS-|BR-I1[34])/.test(L.edge||''))continue;for(const [x,y] of [[L.ax,L.ay],[L.ax+L.ux*L.len,L.ay+L.uy*L.len]]){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y)}}
   G.box=[x0-30,y0-30,x1+30,y1+30];
   if(typeof lnBayStart==='function'){const f=lnBayStart;lnBayStart=function(B,S){const r=f.apply(this,arguments);try{if(B&&B.L&&String(B.L.id)==='5'){const d=B.v?Math.hypot(B.v.x-S.C.x,B.v.y-S.C.y):null;G.stops.push({no:B.no,st:S.id,t:+LN.t.toFixed(1),clock:gameClock().hhmm,d:d==null?null:+d.toFixed(1),door:!B.nodoor,dh:!!B.deadhead})}}catch(e){G.err=String(e)}return r};G.hook=1}
   return{box:G.box,hook:!!G.hook,l5:!!window.__TC_L5RUN,lines:(typeof LN_LINES!=='undefined'?LN_LINES.map(L=>L.id):null)}})()`);
  console.log('init', JSON.stringify(init));
  const STEP = `(ch=>{const G=window.__L5C,q=window.__TC_SIM_STEP_QA({seconds:ch,warmup:0,every:ch});const a=window.__TC_LINES.audit();let l5=null;try{l5=window.__TC_L5RUN?window.__TC_L5RUN():null}catch(e){l5={err:String(e)}}let lift=null;try{lift=window.__TC_S13LIFT()}catch(e){}
   const B=G.box,inB=v=>v.x>B[0]&&v.x<B[2]&&v.y>B[1]&&v.y<B[3];
   const W=v=>{const c=v.c2;if(!c)return null;return{t:+SIM.t.toFixed(1),x:Math.round(v.x),y:Math.round(v.y),limit:c.limit||null,lead:c.limitLead||null,gap:c.limitGap!=null?Math.round(c.limitGap):null,hardBy:c.hardBy||null,granted:!!c.granted,gate:c.gate?c.gate.node:null,why:c.why||null,chain:c.chainWant?c.chainWant.node+':'+c.chainWant.why:null,lock:v.junctionLock||null,mv:c.mv?c.mv.id:null,ms:c.mv?Math.round(c.ms):null,lane:c.mv?null:c.lane&&c.lane.id,s:c.mv?null:Math.round(c.s),backout:!!c.backout}};
   const N=id=>{const n=NODES2.get(id);return n?{inside:(n.inside||[]).map(z=>z.v.id+(z.remote?'(r)':'')+':'+(z.mv&&z.mv.id)),waiting:(n.waiting||[]).map(z=>z.id+':'+((z.c2&&z.c2.why)||''))}:null};
   G.loop=G.loop||{};for(const v of [...TRAFFIC_CARS,...BUS_VEHICLES])if(/^IS-L/.test(v.edgeId||'')&&!(v.ln&&String(v.ln.L.id)==='5')&&!G.loop[v.id])G.loop[v.id]={t:+LN.t.toFixed(0),edge:v.edgeId,fy:!!v.fy,c5:v.c5&&v.c5.purpose||null,prof:v.c2&&v.c2.profile};
   let worst=0,n5=0;for(const v of [...TRAFFIC_CARS,...BUS_VEHICLES]){if(!(v.x>-9e3)||!inB(v))continue;const s=+(v.stuck||0);if(s<=5)continue;n5++;worst=Math.max(worst,s);const k=(v.ln?'L'+v.ln.L.id+':':'')+v.id;const M=G.isl[k];if(!M||s>M.max)G.isl[k]={max:+s.toFixed(1),edge:v.edgeId,clock:gameClock().hhmm,why:W(v)}}
   if(worst>60&&G.snaps.length<12&&(!G.lastSnap||LN.t-G.lastSnap>300)){G.lastSnap=LN.t;G.snaps.push({t:+LN.t.toFixed(0),clock:gameClock().hhmm,E0:N('ISE-0'),IL:N('IL'),ISE1:N('ISE-1'),st:[...TRAFFIC_CARS,...BUS_VEHICLES].filter(v=>v.x>-9e3&&inB(v)&&(v.stuck||0)>30).map(v=>[(v.ln?'L'+v.ln.L.id+':':'')+v.id,v.edgeId,Math.round(v.stuck),(v.c2&&v.c2.why)||null,(v.c2&&v.c2.limitLead)||null])})}
   const SL=[];for(const n of NODES2.values()){for(const o of (n.inside||[])){if(o.ghost)continue;const v=o.v,c=v&&v.c2;let bad=null;if(!c)bad='no-c2';else if(o.remote){if(!(c.remotes||[]).some(r=>r.node===n.id))bad='remote-not-held'}else if(!o.standing&&!(c.granted&&c.gate&&c.gate.node===n.id)&&!(c.mv&&c.mv.node===n.id)&&c.insideNode!==n.id&&c.exitBoxNode!==n.id)bad='not-granted';
     if(bad){const k=n.id+'|'+(v&&v.id)+'|'+(o.mv&&o.mv.id);const S=G.stale=G.stale||{};if(!S[k])S[k]={node:n.id,id:v&&v.id,mv:o.mv&&o.mv.id,bad,t0:+LN.t.toFixed(0),fy:!!(v&&v.fy),fyLast:v&&v.fyLast!=null?+v.fyLast.toFixed(0):null,c5:v&&v.c5&&v.c5.purpose||null,live:TRAFFIC_CARS.includes(v)||BUS_VEHICLES.includes(v)};S[k].t1=+LN.t.toFixed(0);SL.push(k)}}}
   return{stale:SL.length,frozenMax:q.frozenMax,clock:gameClock().hhmm,ok:a.ok,err:a.err,frz:a.frz&&{n:a.frz.n,max:a.frz.max},islN5:n5,islWorst:+worst.toFixed(0),lift:lift&&{st:lift.st,opens:lift.opens,maxOnSpan:lift.maxOnSpan},
     l5:l5&&{on:l5.on,why:l5.why,err:l5.err,st:l5.st,buses:(l5.buses||[]).map(x=>x.no+':'+x.ph+'@'+(x.edge||'')+'>'+(x.to||''))}}})`;
  const rows = [];
  for (let t = 0; t < SEC; t += CH) {
    const r = await ev(STEP + '(' + CH + ')'); rows.push(Object.assign({ t: t + CH }, r));
    if ((t + CH) % 300 === 0 || t + CH >= SEC) { const l = r.l5 || {}; console.log(`t=${t + CH} ${r.clock} ok=${r.ok} err=${r.err} frz=${r.frz && r.frz.n}/${r.frz && r.frz.max} frozen=${r.frozenMax} stale=${r.stale} isl>5=${r.islN5} worst=${r.islWorst} lift=${r.lift && r.lift.st}/${r.lift && r.lift.opens}/${r.lift && r.lift.maxOnSpan} l5=${l.on} ${l.why || ''} ${(l.buses || []).join(' ')}`) }
  }
  const fin = await ev(`(()=>{const G=window.__L5C;let l5=null;try{l5=window.__TC_L5RUN?window.__TC_L5RUN():null}catch(e){}let F=null;try{F=LN5.F.slice()}catch(e){}
    const top=Object.entries(G.isl).sort((a,b)=>b[1].max-a[1].max).slice(0,25);return{box:G.box,F,l5,top,over60:Object.values(G.isl).filter(v=>v.max>60).length,over300:Object.values(G.isl).filter(v=>v.max>300).length,snaps:G.snaps,stops:G.stops,stale:Object.values(G.stale||{}).filter(s=>s.t1-s.t0>=20).slice(0,40),staleAll:Object.keys(G.stale||{}).length,loopCars:G.loop||{},l5c7:window.__TC_L5C7?window.__TC_L5C7():null,fy:typeof FY!=='undefined'?{on:FY.on,stats:FY.stats,err:FY.err}:null,hookErr:G.err||null,linesAudit:window.__TC_LINES.audit()}})()`);
  // הסבבים של קו 5: רצף התחנות לכל קואץ׳ (בלי חזרות צמודות)
  const laps = {}; for (const s of fin.stops || []) { const a = laps[s.no] = laps[s.no] || []; if (!a.length || a[a.length - 1].st !== s.st) a.push(s) }
  fin.seq = Object.fromEntries(Object.entries(laps).map(([k, a]) => [k, a.map(s => s.st + '@' + s.clock + (s.door ? '' : '(בלי דלתות)') + (s.d > 25 ? '!d' + s.d : '')).join(' → ')]));
  fs.writeFileSync(out, JSON.stringify({ init, rows, fin, errs }, null, 1));
  console.log('island over60', fin.over60, 'over300', fin.over300, 'top', JSON.stringify(fin.top.slice(0, 6).map(([k, v]) => [k, v.max, v.edge, v.why && v.why.why, v.why && v.why.lead])));
  console.log('loopCars', JSON.stringify(fin.loopCars).slice(0, 600), 'l5c7', JSON.stringify(fin.l5c7));
  console.log('stops', (fin.stops || []).length, JSON.stringify(fin.seq).slice(0, 2000));
  console.log('errs', JSON.stringify(errs)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
