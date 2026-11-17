// prof_start.js — perf 17.11: מה יש ב-190 מ"ש של startMission הראשונה (navday על try7163: M-E3-PARCEL 189.7 מ"ש, ובתוכה setNavigationTarget 1.4 ו-g77MsgIn 1.2 בלבד).
// node prof_start.js <out.json> <a.html> [b.html …]   — דרך התור. לכל בנייה: ‎#dev, ‏1280×800 (כמו navday), עוטף לזמן המדידה: TCVOICE.speak, ‏TCSND.ensure,
// window.atob, ‏AudioContext.decodeAudioData, ‏tcNv64 (אם יש), ‏g77MsgIn, ‏setNavigationTarget, ‏setTemporaryVehicle, ‏SaveManager.save / log, ‏toast; ופרופיל CPU (CDP, דגימה כל 100 מיקרו-שנ׳)
// סביב הקריאה הראשונה (קר) ואחר כך סביב השנייה (אותה משימה, אחרי ביטול) ושלישית (משימה אחרת): זמן עצמי לפי הפונקציה והשורה, והשרשרת של העטיפות של startMission.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const WRAP = `(()=>{const T=window.__PS={acc:{},cnt:{},log:[]};const wrap=(name,get,set)=>{let f;try{f=get()}catch(e){return 0}if(typeof f!=='function'||f.__ps)return 0;
  const w=function(){const t=performance.now();try{return f.apply(this,arguments)}finally{const d=performance.now()-t;T.acc[name]=(T.acc[name]||0)+d;T.cnt[name]=(T.cnt[name]||0)+1;if(d>2)T.log.push([name,+d.toFixed(1)])}};w.__ps=1;try{set(w)}catch(e){return 0}return 1};
 let k=0;const G=n=>{k+=wrap(n,()=>eval(n),f=>{eval(n+'=f')})};for(const n of ['g77MsgIn','setNavigationTarget','setTemporaryVehicle','toast','tcNv64','g77SpBadge','renderPhone'])try{G(n)}catch(e){}
 try{k+=wrap('TCVOICE.speak',()=>TCVOICE.speak,f=>{TCVOICE.speak=f})}catch(e){}try{k+=wrap('TCSND.ensure',()=>TCSND.ensure,f=>{TCSND.ensure=f})}catch(e){}
 try{k+=wrap('SaveManager.save',()=>SaveManager.save,f=>{SaveManager.save=f});k+=wrap('SaveManager.log',()=>SaveManager.log,f=>{SaveManager.log=f})}catch(e){}
 k+=wrap('atob',()=>window.atob,f=>{window.atob=f});
 try{const P=(window.AudioContext||window.webkitAudioContext).prototype;k+=wrap('decodeAudioData',()=>P.decodeAudioData,f=>{P.decodeAudioData=f})}catch(e){}

 const chain=[];let f=startMission;for(let i=0;i<12&&f;i++){chain.push(String(f).slice(0,90).replace(/\\s+/g,' '));f=null}T.chain=chain;T.wrapped=k;return 'ok '+k})()`;
const CALL = skip => `(()=>{const T=window.__PS;T.acc={};T.cnt={};T.log=[];const ids=Object.keys(MISSION_DEFS).filter(id=>!/^M-ST-/.test(id)&&!MISSION_DEFS[id].retired);const sk=new Set(${JSON.stringify(skip)});const tries=[];let got=null;
 for(const id of ids){if(sk.has(id))continue;PlayerProfile.activeMission=null;State.navigation=null;const t=performance.now();let er=null;try{startMission(id)}catch(e){er=String(e).slice(0,160)}const ms=+(performance.now()-t).toFixed(1);
  if(PlayerProfile.activeMission){got={id,ms,er};try{cancelActiveMission()}catch(e){}break}tries.push([id,ms])}
 return JSON.stringify({id:got&&got.id,ms:got&&got.ms,started:!!got,er:got&&got.er,before:tries.length,beforeMs:+tries.reduce((a,q)=>a+q[1],0).toFixed(1),acc:Object.fromEntries(Object.entries(T.acc).map(([k,v])=>[k,+v.toFixed(1)+'×'+T.cnt[k]])),log:T.log.slice(0,20),
  ac:(()=>{try{return{ctx:!!(TCSND.st&&TCSND.st.ctx),state:TCSND.st&&TCSND.st.ctx&&TCSND.st.ctx.state}}catch(e){return null}})(),vs:(()=>{try{return window.TCVSIDE?{st:TCVSIDE.st}:null}catch(e){return null}})()})})()`;
function selfTop(prof, n) {   // only the samples under a frame named startMission (the wrappers of startMission are all named so)
  const byId = new Map(prof.nodes.map(x => [x.id, x])); const self = new Map(); const dt = prof.timeDeltas; let tot = 0;
  const parent = new Map(); for (const x of prof.nodes) for (const c of (x.children || [])) parent.set(c, x.id);
  const under = new Map(); const isUnder = id => { if (under.has(id)) return under.get(id); let p = id, r = false; while (p !== undefined) { if (byId.get(p).callFrame.functionName === 'startMission') { r = true; break } p = parent.get(p) } under.set(id, r); return r };
  for (let i = 0; i < prof.samples.length; i++) { if (!isUnder(prof.samples[i])) continue; const d = (dt[i + 1] !== undefined ? dt[i + 1] : 0) / 1000; tot += d; self.set(prof.samples[i], (self.get(prof.samples[i]) || 0) + d) }
  const fk = x => (x.callFrame.functionName || '(anon)') + ':' + (x.callFrame.lineNumber + 1);
  const S = {}, I = {}; for (const [id, ms] of self) { const x = byId.get(id); const k = fk(x); S[k] = (S[k] || 0) + ms; const seen = new Set(); let p = id; while (p !== undefined) { const q = byId.get(p); const kk = fk(q); if (!seen.has(kk)) { seen.add(kk); I[kk] = (I[kk] || 0) + ms } p = parent.get(p) } }
  const r = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n).map(([k, v]) => [k, +v.toFixed(1)]);
  return { totalMs: +tot.toFixed(1), self: r(S), incl: r(I).filter(([k]) => !/^\((root|program|idle)\)/.test(k)).slice(0, n) };
}
(async () => {
  const [out, ...files] = process.argv.slice(2); const all = [];
  for (const file of files) {
    const R = { build: path.basename(file) }; const b = await chromium.launch({ args: ['--enable-precise-memory-info'] });
    try {
      const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
      await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(1500);
      const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
      R.wrap = await ev(WRAP);
      R.ids = JSON.parse(await ev(`JSON.stringify(Object.keys(MISSION_DEFS).filter(id=>!/^M-ST-/.test(id)&&!MISSION_DEFS[id].retired).slice(0,6))`));
      const cdp = await p.context().newCDPSession(p); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', { interval: 100 });
      R.calls = [];
      const skip = [];
      for (let k = 0; k < 3; k++) {   // the first mission that starts (cold), then the next one that starts, then the next
        await cdp.send('Profiler.start'); const r = JSON.parse(await ev(CALL(skip))); const { profile } = await cdp.send('Profiler.stop'); r.prof = selfTop(profile, 18); R.calls.push(r); if (r.id) skip.push(r.id); await p.waitForTimeout(800) }
      R.errs = errs.slice(0, 5);
    } catch (e) { R.err = String(e && e.stack || e).slice(0, 400) } finally { await b.close() }
    all.push(R); fs.writeFileSync(out, JSON.stringify(all, null, 1));
    console.log(JSON.stringify({ build: R.build, err: R.err, calls: (R.calls || []).map(c => ({ id: c.id, ms: c.ms, started: c.started, before: c.before, beforeMs: c.beforeMs, acc: c.acc, ac: c.ac, self: c.prof.self.slice(0, 6), incl: c.prof.incl.slice(0, 8) })) }, null, 1));
  }
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 500)); process.exit(1) });
