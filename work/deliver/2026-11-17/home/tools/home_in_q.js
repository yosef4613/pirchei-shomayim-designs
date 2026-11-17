// home_in_q.js — home (17.11): הבדיקה של פנים הבית (HOME-02) במשחק עצמו — בכל רמה: F בדלת → "היכנס הביתה" → הליכה לדלת → בפנים; תנועה
// עם התנגשות; מיטה (שינה), ארון (חדר ההלבשה), מטבח (בישול), שולחן (אכילה), מדרגות, יציאה; האגפים והסטודיו; 0 שגיאות; הזמן לפריים בפנים.
// node home_in_q.js <game.html> <out.json> [shots_dir]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outF, shots] = process.argv.slice(2); if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 300)) });
  const R = { file: path.basename(file), lv: {}, bad: [] }; const bad = s => { R.bad.push(s); console.log('✗ ' + s) };
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(2500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const evj = async s => { const v = await ev(s); try { return JSON.parse(v) } catch (e) { return v } };
  const shot = async n => { if (shots) await p.screenshot({ path: path.join(shots, n + '.png') }) };
  const H = 'window.__TC_HOME.in.H';
  const st = () => evj(`JSON.stringify({on:${H}.on,b:${H}.b,f:${H}.f,x:+${H}.x.toFixed(2),y:+${H}.y.toFixed(2),busy:${H}.busy&&${H}.busy.k,panel:!!${H}.panel,near:${H}.near&&${H}.near.k,phone:State.phoneOpen,app:State.phoneApp,err:${H}.err})`);
  const to = async (k, pick) => evj(`(()=>{const G=${H}.G;const L=G.items.filter(i=>i.act===${JSON.stringify(k)}&&i.ap);const it=L[${pick || 0}]||L[0];if(!it)return JSON.stringify({no:1});${H}.x=it.ap[0];${H}.y=it.ap[1];return JSON.stringify({k:it.k,ap:it.ap})})()`);
  const key = async (k, ms) => { await p.keyboard.down(k); await p.waitForTimeout(ms || 80); await p.keyboard.up(k) };
  try {
    // (0) the in-game check: every level, building, floor — the rooms, the action points, the drawing; the pantry and the upgrade
    R.check = await evj('JSON.stringify(window.__TC_HOME.in.check())'); console.log('check', R.check.ok, R.check.rows && R.check.rows.length); if (!R.check.ok) bad('check: ' + JSON.stringify(R.check.bad).slice(0, 600));
    await ev(`PlayerProfile.money=Math.max(PlayerProfile.money,500000);PlayerProfile.inventory=Object.assign(PlayerProfile.inventory||{},{'super-eggs':3,'b4-bread':3,'b4-vegcrate':2,'rest-soup':1,'mall-city-backpack':1});1`);
    for (let n = 1; n <= 8; n++) {
      const r = R.lv[n] = {}; await ev(`(()=>{PlayerProfile.home.homeLevel=${n};PlayerProfile.mode='walk';try{if(State.phoneOpen)setPhoneOpen(false)}catch(e){}const q=playerHomeServicePoint();PlayerPed.x=q.x+30;PlayerPed.y=q.y+24;Camera.x=q.x;Camera.y=q.y;Camera.zoom=1.1;return 1})()`);
      await p.waitForTimeout(300);
      // the F mark at the door (outside), then F → straight in (the walk to the door, then inside)
      await ev(`(()=>{const q=playerHomeServicePoint();PlayerPed.x=q.x;PlayerPed.y=q.y+10;return 1})()`); await p.waitForTimeout(900);
      const dm = await evj(`JSON.stringify(${H}.n.doorMarks||0)`); if (!(dm > 0)) bad('L' + n + ': אין F בדלת בחוץ'); if (n === 1) await shot('door_F_L1');
      const diag = `JSON.stringify({walkIn:!!${H}.walkIn,on:${H}.on,paused:!!State.paused,phone:!!State.phoneOpen,map:!!State.mapOpen,mode:PlayerProfile.mode,mission:PlayerProfile.activeMission&&PlayerProfile.activeMission.id||null,near:!!nearbyPlayerHome(92),chunk:currentChunkId(PlayerPed.x,PlayerPed.y),tco:(typeof TCO!=='undefined'?{m:TCO.mode,ui:!!TCO.ui}:null),tut:(window.__TC_TUT?__TC_TUT.state():null),busy:(typeof TCBUSY!=='undefined'?TCBUSY.top():''),sleep:!!window.__TC_HOME.sleep.S.busy,peek:!!window.__TC_HOME.peek.P.on,err:${H}.err})`;
      r.d0 = await evj(diag); r.fRet = await evj('JSON.stringify(interactNearbyPoi())'); await p.waitForTimeout(400); r.d1 = await evj(diag);
      const hasBtn = await p.$('button[data-hin-enter="H"]'); if (hasBtn && await evj('JSON.stringify(State.phoneOpen)')) { r.viaScreen = 1; await p.evaluate(()=>document.querySelector('button[data-hin-enter="H"]').click()) }
      await p.waitForTimeout(2200); let s = await st(); r.in = s;
      if (!s.on) { bad('L' + n + ': F בדלת לא הכניס — ' + JSON.stringify({ d0: r.d0, ret: r.fRet, d1: r.d1 }).slice(0, 500)); await ev(`${H}.walkIn=null;window.__TC_HOME.in.enter('H',{instant:true})`); await p.waitForTimeout(500); s = await st(); if (!s.on) { bad('L' + n + ': לא נכנס גם ישירות'); continue } } if (n === 1 || n === 4 || n === 8) await shot('in_L' + n + '_f0');
      // the walk: up for a second — moved, not through a wall
      const a0 = await st(); await key('ArrowUp', 900); await key('ArrowLeft', 500); const a1 = await st(); r.walk = [a0.x, a0.y, a1.x, a1.y];
      if (Math.hypot(a1.x - a0.x, a1.y - a0.y) < .5) bad('L' + n + ': השחקן לא זז בפנים');
      const blk = await evj(`JSON.stringify(!!window.__TC_HOME.hin.blocked(${H}.G,${H}.x,${H}.y,.2))`); if (blk) bad('L' + n + ': השחקן בתוך קיר / רהיט');
      // the actions on the ground floor: the wardrobe (if here), the kitchen, the table
      const actOn = async (k, then) => { const t = await to(k); if (t.no) return null; await p.waitForTimeout(250); const s1 = await st(); if (s1.near == null) { bad('L' + n + ' ' + k + ': אין F ליד ' + t.k); return null }
        const mk = await evj(`JSON.stringify((${H}.marks||[]).filter(m=>m.show).map(m=>({k:m.it.k,t:m.txt,hot:m.hot})))`); if (!mk.some(m => m.hot && m.t)) bad('L' + n + ' ' + k + ': אין F צהוב עם כיתוב'); r.marks = (r.marks || 0) + mk.length; await key('KeyF', 60); await p.waitForTimeout(350); const s2 = await st(); return s2 };
      if (n === 1 || n === 5) {
        const sc = await actOn('cook'); if (sc) { if (!sc.panel) bad('L' + n + ': הבישול לא פתח לוח'); else { const btn = await p.$('[data-hin-cook="omelet"]:not([disabled])'); if (!btn) bad('L' + n + ': אין חביתה (המזווה?)'); else { await btn.evaluate(e=>e.click()); await p.waitForTimeout(1200); if (n === 5) await shot('cook_L5'); await p.waitForTimeout(3000); const m = await evj(`JSON.stringify(window.__TC_HOME.in.pantry())`); r.pantry = m; if (!(m['meal:omelet'] > 0)) bad('L' + n + ': אין מנה אחרי בישול') } } }
        const se = await actOn('eat'); if (se) { const btn = await p.$('[data-hin-eat]'); if (!btn) bad('L' + n + ': אין מה לאכול'); else { await btn.evaluate(e=>e.click()); await p.waitForTimeout(1500); await shot('eat_L' + n); const sb = await st(); if (sb.busy !== 'eat') bad('L' + n + ': לא יושב לאכול'); await p.waitForTimeout(3300); } }
      }
      // the stairs (if any): up — the upper floor — down
      const nf = await evj(`JSON.stringify(${H}.G.nf)`); r.nf = nf;
      if (nf > 1) { const t = await to('stairs'); await p.waitForFunction(() => { const h = window.__TC_HOME.in.H; return h.near && h.near.k === 'stairs' }, null, { timeout: 4000, polling: 50 }).catch(() => {}); await key('KeyF', 60); await p.waitForTimeout(250); let s2 = await st(); if (s2.panel) { await p.evaluate(()=>document.querySelector('[data-hin-stairs="up"]').click()); } await p.waitForTimeout(700); s2 = await st(); r.up = s2.f; if (s2.f !== 1) bad('L' + n + ': לא עלה במדרגות (' + JSON.stringify(t) + ')'); else if (n === 2 || n === 6 || n === 8) await shot('in_L' + n + '_f1') }
      // the wardrobe and the bed (on the floor they are)
      for (const k of ['dress', 'sleep']) { let t = await to(k); if (t.no && nf > 1) { const s0 = await st(); if (s0.f !== 0) { await ev(`window.__TC_HOME.in.setFloor(0,'stairs');1`); t = await to(k) } } if (t.no) { bad('L' + n + ': אין ' + k); continue }
        await p.waitForFunction(k => { const h = window.__TC_HOME.in.H; return !!(h.near && h.near.act === k) }, k, { timeout: 4000, polling: 50 }).catch(() => {}); await p.waitForTimeout(120); await key('KeyF', 60); await p.waitForTimeout(450); const s3 = await st();
        if (k === 'dress') { if (!(s3.phone && s3.app === 'wardrobe')) bad('L' + n + ': הארון לא פתח את חדר ההלבשה (' + s3.app + ')'); if (n === 3) await shot('dress_L3'); await key('KeyF', 60); await p.waitForTimeout(300); const s4 = await st(); if (s4.phone || !s4.on) bad('L' + n + ': אחרי חדר ההלבשה לא חזר הביתה') }
        if (k === 'sleep') { if (!s3.panel) { bad('L' + n + ': המיטה לא פתחה את השינה'); continue } if (n === 2 || n === 7) { const c0 = await evj('JSON.stringify(gameClock())'); await p.evaluate(()=>document.querySelector('#tcHomeIn [data-home-sleep="h2"]').click()); await p.waitForTimeout(700); if (n === 2) await shot('sleep_bed_L2'); await p.waitForFunction(() => !window.__TC_HOME.sleep.S.busy, null, { timeout: 8000, polling: 100 }); await p.waitForTimeout(300); const c1 = await evj('JSON.stringify(Object.assign(gameClock(),{last:window.__TC_HOME.sleep.S.last}))'); const dm = (c1.day - c0.day) * 1440 + c1.min - c0.min; r.sleep = [c0.hhmm, c1.hhmm, dm]; if (dm < 119 || dm > 125 || !c1.last || !c1.last.saved) bad('L' + n + ': שינה מהמיטה ' + JSON.stringify(r.sleep)); const s5 = await st(); if (!s5.on) bad('L' + n + ': אחרי השינה לא בבית') } else { await key('KeyF', 60); await p.waitForTimeout(300) } } }
      // out: Esc → by the door outside
      await ev(`${H}.panel&&window.__TC_HOME.in.closePanel();1`); await p.evaluate(()=>document.querySelector('#tcHomeIn [data-hin="exit"]').click()); await p.waitForTimeout(800); const so = await st(); const pos = await evj('JSON.stringify({x:PlayerPed.x,y:PlayerPed.y,mode:PlayerProfile.mode,d:(()=>{const q=playerHomeServicePoint();return Math.hypot(PlayerPed.x-q.x,PlayerPed.y-q.y)})()})'); r.out = pos;
      if (so.on) bad('L' + n + ': Esc לא הוציא'); if (pos.d > 40) bad('L' + n + ': אחרי היציאה לא ליד הדלת (' + Math.round(pos.d) + ')');
      const tc = await evj('JSON.stringify(typeof TCO!=="undefined"?!!TCO.ui:false)'); if (tc) bad('L' + n + ': התפריט של המשחק נפתח');
      const pf = await evj(`JSON.stringify({f:${H}.n.frames,ms:${H}.n.ms})`); r.frameMs = pf.f ? +(pf.ms / pf.f).toFixed(2) : null;
    }
    // the wings (7, 8) and the studio (6): F at their own door
    for (const [n, b] of [[7, 'W'], [8, 'W1'], [8, 'W2'], [6, 'S']]) {
      await ev(`(()=>{PlayerProfile.home.homeLevel=${n};PlayerProfile.mode='walk';try{if(State.phoneOpen)setPhoneOpen(false)}catch(e){}const L=C3LV[${n}-1],q=L.buildings.find(x=>x.id.endsWith('-${b}'));PlayerPed.x=q.ent[0];PlayerPed.y=q.ent[1]+10;Camera.x=q.ent[0];Camera.y=q.ent[1];return 1})()`); await p.waitForTimeout(300);
      await ev('interactNearbyPoi()'); await p.waitForTimeout(400);
      if (b === 'S') { const btn = await p.$('button[data-hin-enter="S"]'); if (!btn) { bad('L6: F בסטודיו לא פתח את מסך הסטודיו'); continue } await shot('studio_F'); await btn.evaluate(e=>e.click()); await p.waitForTimeout(2200) } else await p.waitForTimeout(1800);
      const s = await st(); R['site_' + n + b] = s; if (!s.on || s.b !== b) { bad('L' + n + ' ' + b + ': לא נכנס'); continue } await shot('in_L' + n + '_' + b);
      if (b === 'S') { const t = await to('design'); await p.waitForTimeout(150); await key('KeyF', 60); await p.waitForTimeout(300); const btn = await p.$('[data-hin-design="wall"]'); if (!btn) bad('L6: אין עיצוב הבית'); else { await btn.evaluate(e=>e.click()); await p.waitForTimeout(500); const d = await evj('JSON.stringify(PlayerProfile.home.design||null)'); if (!d || !d.wall) bad('L6: העיצוב לא נשמר'); await shot('studio_design'); await p.evaluate(()=>document.querySelector('[data-hin-design="reset"]').click()) } }
      await ev(`${H}.panel&&window.__TC_HOME.in.closePanel();1`); await p.evaluate(()=>document.querySelector('#tcHomeIn [data-hin="exit"]').click()); await p.waitForTimeout(800); const so = await st(); if (so.on) bad('L' + n + ' ' + b + ': לא יצא');
    }
    R.errors = errs.slice(0, 30); if (errs.length) bad(errs.length + ' שגיאות בדף');
    R.mem = await evj('JSON.stringify(performance.memory?{used:Math.round(performance.memory.usedJSHeapSize/1048576)}:null)');
  } catch (e) { bad('חריגה: ' + String(e).slice(0, 400)); R.errors = errs.slice(0, 30) }
  R.ok = !R.bad.length; fs.writeFileSync(outF, JSON.stringify(R, null, 1)); console.log(R.ok ? 'עבר' : 'נכשל: ' + R.bad.length); await b.close(); process.exit(R.ok ? 0 : 1);
})();
