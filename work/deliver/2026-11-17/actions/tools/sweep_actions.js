// סריקה בעין של כל הפעולות (actions, 17.11): לכל שלב בטבלה — השחקן ליד החפץ, שלוש תמונות: לפני (a), באמצע הפעולה (b), התוצאה בעולם (c).
// התמונות — רק לבדיקה בעין (לא לדף, לא למשחק). גם: איפה החפץ עומד (חסום / על נתיב נסיעה), ושגיאות.
// node sweep_actions.js <game.html> <out_dir> [מסנן — חלק משם הסיפור]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outDir, filt] = process.argv.slice(2); fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const list = await ev(`(()=>{const L=[];for(const [id,M] of Object.entries(SA_SPEC))for(const n of Object.keys(M))L.push([id,+n,0]);for(const [id,M] of Object.entries(SA_DRIVE))for(const n of Object.keys(M))if(Array.isArray(M[n]))L.push([id,+n,1]);return L})()`);
  await ev(`(()=>{window.__SW_KEEP=JSON.stringify(g77St());window.__SW_M=PlayerProfile.money;return 1})()`);
  const R = { n: 0, rows: [], pe };
  for (const [id, n, isD] of list) {
    if (filt && id.indexOf(filt) < 0) continue;
    const tag = id + '_' + n; const r = { id, n, drive: isD };
    try {
      r.arm = await ev(`(()=>{const A=__TC_SACT,f=g77St().flags;if(State.phoneOpen)setPhoneOpen(false);f['s9:${id}']=${n};delete f['s9:${id}:done'];A.SA.cur=null;A.SA.carry=null;
        const sp=A.spec('${id}',${n});if(['give','via','plant','hang'].includes(sp.k)||sp.opt.use){const prev=[...Array(${n}-1).keys()].map(k=>k+1).reverse().map(k=>A.spec('${id}',k)).find(q=>q&&(q.k==='take'||q.k==='pick'||q.k==='find'||q.opt.then));if(prev){const t=prev.opt.then;A.SA.carry=t?{id:'${id}',o:t[0],c:t[1],nm:t[2],u:0}:{id:'${id}',o:prev.opt.into||prev.o,c:prev.c,nm:prev.nm,u:0}}}
        const P=(()=>{const s=S9STORY.ST['${id}'].steps[${n}-1];if(s.__saDrive)return{x:s.__saDrive[0],y:s.__saDrive[1]};const q=navPoiRegistry()[s.poi];return q?{x:q.x,y:q.y}:null})();
        if(P){PlayerProfile.mode='walk';PlayerPed.x=P.x;PlayerPed.y=P.y+4}
        const c=A.arm('${id}',true);if(!c)return null;PlayerProfile.mode='walk';PlayerPed.x=c.pt.x;PlayerPed.y=c.pt.y+7;Camera.x=c.pt.x;Camera.y=c.pt.y;Camera.zoom=2.4;
        let blk=null,road=null;try{blk=!!personBlockedAt(c.pt.x,c.pt.y,3)}catch(e){}
        return{k:c.k,nm:c.nm,pt:[Math.round(c.pt.x),Math.round(c.pt.y)],poi:[Math.round(c.poi.x),Math.round(c.poi.y)],blk,hud:String(hudGoalText()).slice(0,90)}})()`);
      if (!r.arm) { r.ok = false; r.why = 'לא נחמש'; R.rows.push(r); continue }
      const clip = { x: 640 - 260, y: 400 - 190, width: 520, height: 380 };
      await p.waitForTimeout(350); await p.screenshot({ path: path.join(outDir, tag + '_a.jpg'), clip, type: 'jpeg', quality: 70 });
      r.work = await ev(`(()=>{const A=__TC_SACT,c=A.SA.cur;if(c.k==='via'){A.tick(performance.now());return{via:1,phase:c.phase}}const ok=A.F();if(c.phase==='work')c.t0=performance.now()-c.dur*.6;return{f:ok,phase:c.phase}})()`);
      await p.waitForTimeout(200); await p.screenshot({ path: path.join(outDir, tag + '_b.jpg'), clip, type: 'jpeg', quality: 70 });
      r.end = await ev(`(()=>{const A=__TC_SACT,c=A.SA.cur;if(!c)return{gone:1};const q=c.k==='sort'?c.q:1;for(let i=0;i<q;i++){if(c.phase==='go')A.F();if(c.phase==='work'){c.t0-=c.dur+50;A.tick(performance.now());if(c.phase==='work'){c.t0-=20050;A.tick(performance.now())}}}
        return{phase:c.phase,step:S9STORY.step('${id}'),carry:A.SA.carry&&A.SA.carry.nm,res:A.SA.res.length}})()`);
      await p.waitForTimeout(400); await p.screenshot({ path: path.join(outDir, tag + '_c.jpg'), clip, type: 'jpeg', quality: 70 });
      r.ok = !!(r.end && (r.end.phase === 'done' || r.end.gone));
    } catch (e) { r.ok = false; r.err = String(e).slice(0, 200) }
    finally { try { await ev(`(()=>{PlayerProfile.story=JSON.parse(window.__SW_KEEP);PlayerProfile.money=window.__SW_M;__TC_SACT.SA.cur=null;__TC_SACT.SA.carry=null;__TC_SACT.SA.wear=null;__TC_SACT.SA.res.length=0;__TC_SACT.SA.fx.length=0;return 1})()`) } catch (e) { } }
    R.n++; R.rows.push(r);
  }
  R.engineErr = await ev(`__TC_SACT.err()`);
  R.ok = R.rows.every(r => r.ok) && !pe.length && !R.engineErr;
  fs.writeFileSync(path.join(outDir, 'sweep.json'), JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ ok: R.ok, n: R.n, bad: R.rows.filter(r => !r.ok).map(r => r.id + '#' + r.n + ' ' + (r.why || r.err || JSON.stringify(r.end))), blocked: R.rows.filter(r => r.arm && r.arm.blk).map(r => r.id + '#' + r.n), pe: pe.length, err: R.engineErr }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
