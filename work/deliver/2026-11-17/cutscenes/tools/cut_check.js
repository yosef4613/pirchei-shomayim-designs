// 17.11 · cutscenes — בדיקה של סצנות הסיפור בתוך המשחק: node cut_check.js <build> <out.json> [shotsDir]
// (1) TCCUT.qa() — הנתונים, המקומות, המעברים, וכל הסצנות עד הסוף בזמן ידני; (2) ריצה אמיתית: הסיפור מתחיל → הסצנה של הפתיחה מתנגנת לבד,
// המצלמה זזה, הדמות מצוירת, דילוג ב-Esc מחזיר הכול; (3) הטנדר (1-van) מ-F9; (4) הנחיתה — הזמן עד הנחיתה הבאה; (5) 0 שגיאות בדף.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(300) }
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const R = { file: path.basename(file), t: new Date().toISOString() };
  const shot = async n => { if (!shots) return; try { fs.mkdirSync(shots, { recursive: true }); await p.screenshot({ path: path.join(shots, n + '.png') }) } catch (e) {} };
  R.qa = await ev('TCCUT.qa()');
  R.audit = await ev("(()=>{const r=roadAudit();const L=r.checks||r.results||[];const c=L.find(q=>q.id==='story_cutscenes');const s1=L.find(q=>q.id==='story_main_chapter1');const s2=L.find(q=>q.id==='story_locks');return{ok:r.ok,n:L.length,fails:L.filter(q=>!(q.ok||q.pass)).map(q=>q.id||q.name||String(q.detail||'').slice(0,60)),cut:c&&{ok:c.ok,detail:c.detail},ch1:s1&&s1.ok,locks:s2&&s2.ok}})()");
  // (2) the story begins → the scene of the opening plays by itself (the dev page: an active mission of its own and a pause — cleared first)
  R.dev = await ev("({paused:State.paused,am:PlayerProfile.activeMission&&PlayerProfile.activeMission.id,mode:PlayerProfile.mode,tco:typeof TCO!=='undefined'?TCO.mode:''})");
  await ev("(()=>{if(PlayerProfile.activeMission)try{missionFail('qa')}catch(e){PlayerProfile.activeMission=null}PlayerProfile.activeMission=null;State.paused=false;return 1})()");
  R.auto = await ev('TCCUT.auto(true)');
  await ev("(()=>{TCSTORY.begin({silent:true});TCSTORY.bringNow();return 1})()");
  const samp = [];
  for (let i = 0; i < 40; i++) { await p.waitForTimeout(500); const s = await ev('TCCUT.state()'); samp.push(s); if (i === 6) await shot('o_home_title'); if (i === 14) await shot('o_home_actor'); if (s.on && s.on.shot >= 2) { await shot('o_home_wave'); break } }
  R.opening = { started: samp.some(s => s.on && s.on.id === 'O-home'), shots: [...new Set(samp.filter(s => s.on).map(s => s.on.shot))], cams: samp.filter(s => s.on).map(s => s.on.cam).filter((c, i, a) => i % 4 === 0), actors: [...new Set(samp.filter(s => s.on).flatMap(s => s.on.actors))], busy: samp.map(s => s.busy).slice(0, 3), q: samp[0] && samp[0].q };
  R.storyBusy = await ev("(()=>{const m=TCSTORY.M();return m?{mi:m.mi,step:m.step}:null})()");
  R.beforeSkip = await ev("(()=>{const s=TCCUT.state();return{on:s.on&&s.on.id,shot:s.on&&s.on.shot,log:s.log}})()");
  await p.keyboard.press('Escape'); await p.waitForTimeout(800);
  R.afterSkip = await ev("(()=>{const s=TCCUT.state(),a=playerActor();return{on:!!s.on,skipped:s.skipped,body:document.body.classList.contains('tcCutOn'),camToPlayer:Math.round(Math.hypot(Camera.x-a.x,Camera.y-a.y)),zoom:+Camera.zoom.toFixed(2),seen:!!g77St().flags['cut:O-home'],paused:State.paused,tcoUi:typeof TCO!=='undefined'&&TCO.ui,tcoStack:typeof TCO!=='undefined'?TCO.stack.slice():null,dlg:(g77S().open||{}).id||null,log:s.log}})()");
  await ev("(()=>{try{if(typeof TCO!=='undefined'&&TCO.ui)window.__TCO.close()}catch(e){}State.paused=false;if(g77S().open)g77DlgClose(true);return 1})()");
  // (3) the van (F9) — the engine, the puffs, Shimon next to it
  await ev("(()=>{TCCUT.play('1-van');return 1})()");
  const vs = []; for (let i = 0; i < 90; i++) {   /* up to ~45 s: under load the frames are few (dt up to 0.1 s a frame) — try6535: the van was still on after 24 */ await p.waitForTimeout(500); const s = await ev('TCCUT.state()'); vs.push(s); if (i === 6) await shot('van_engine'); if (!s.on) break }
  R.vanBusy = vs.slice(0,3).map(s=>s.busy); R.van = { played: vs.some(s => s.on && s.on.id === '1-van'), ended: !vs[vs.length - 1].on, actors: [...new Set(vs.filter(s => s.on).flatMap(s => s.on.actors))], shots: [...new Set(vs.filter(s => s.on).map(s => s.on.shot))] };
  // (4) the landing: the time to the next one, and the tug / the bus
  R.land = await ev("(()=>{const L=TCCUT.landInfo();return L?{flight:L.f.id,dt:+L.dt.toFixed(1)}:null})()");
  // (4b) the landing for real, when the next one is near enough (up to 150 s): the scene waits, then follows the real flight to the ground
  R.land = await ev("(()=>{const L=TCCUT.landInfo();return L?{flight:L.f.id,dt:+L.dt.toFixed(1)}:null})()");
  if (R.land && R.land.dt < 150 && !process.env.NOLAND) { await ev("(()=>{g77St().main=null;if(g77S().open)g77DlgClose(true);try{if(TCO.ui)window.__TCO.close()}catch(e){}State.paused=false;TCCUT.play('3-landing');return 1})()"); R.landT = []; const ls = []; const t0 = Date.now();
    while (Date.now() - t0 < (R.land.dt * 2.5 + 90) * 1000) {   /* try6535: under load the window of 1.5 ended in the shot of Eliyahu */ await p.waitForTimeout(500); const s = await ev("(()=>{const s=TCCUT.state(),S=TCCUT.ST.on;let P=null;try{if(S&&S.land)P=s15PoseAt(S.land.f,s15Tc(s15Clock().abs))}catch(e){}return{on:s.on&&s.on.id,shot:s.on&&s.on.shot,cam:s.on&&s.on.cam,P:P&&[Math.round(P[0]),Math.round(P[1]),Math.round(P[3]||0)]}})()"); ls.push(s); if (ls.length % 10 === 1) R.landT.push(await ev("(()=>{const L=TCCUT.landInfo(),s=TCCUT.state();return[Date.now()%100000,L?+L.dt.toFixed(1):null,s.busy,s.q.join()]})()"));
      if (s.shot === 1 && !ls.some(q => q.snap)) { s.snap = 1; await shot('land_follow') } if (s.shot === 2 && !ls.some(q => q.snap2)) { s.snap2 = 1; await shot('land_eliyahu') } if (ls.length > 4 && !s.on && ls.some(q => q.on)) break }
    const on = ls.filter(q => q.on === '3-landing'); R.landing = { planeEnd: await ev("TCCUT.ST.planeEnd||null"), played: on.length > 0, shots: [...new Set(on.map(q => q.shot))], minZ: Math.min(...on.filter(q => q.P).map(q => q.P[2])), maxZ: Math.max(...on.filter(q => q.P).map(q => q.P[2])), camNearPlane: on.filter(q => q.shot === 1 && q.P && q.cam).map(q => Math.round(Math.hypot(q.cam.x - q.P[0], q.cam.y - (q.P[1] - .6 * q.P[2])))), ended: !ls[ls.length - 1].on } }
  // (4d) the takeoff for real (done:3-6), when the next one is near enough (up to 200 s): the title until the roll begins, then the same flight on the runway and into the air
  R.toff = await ev("(()=>{const L=TCCUT.takeoffInfo&&TCCUT.takeoffInfo();return L?{flight:L.f.id,dt:+L.dt.toFixed(1)}:null})()");
  if (R.toff && R.toff.dt < 200 && !process.env.NOTOFF) { await ev("(()=>{g77St().main=null;if(g77S().open)g77DlgClose(true);try{if(TCO.ui)window.__TCO.close()}catch(e){}State.paused=false;TCCUT.play('3-takeoff');return 1})()"); const ts = []; const t0 = Date.now();
    while (Date.now() - t0 < (R.toff.dt * 2.5 + 90) * 1000) {   /* the clock of S15 is the time of the game — under load it runs slower than the wall clock */ await p.waitForTimeout(500); const s = await ev("(()=>{const s=TCCUT.state(),S=TCCUT.ST.on;let P=null;try{if(S&&S.land)P=s15PoseAt(S.land.f,s15Tc(s15Clock().abs))}catch(e){}return{on:s.on&&s.on.id,shot:s.on&&s.on.shot,cam:s.on&&s.on.cam,P:P&&[Math.round(P[0]),Math.round(P[1]),Math.round(P[3]||0)]}})()"); ts.push(s);
      if (s.shot === 1 && !ts.some(q => q.snap)) { s.snap = 1; await shot('toff_roll') } if (s.shot === 1 && s.P && s.P[2] > 100 && !ts.some(q => q.snap2)) { s.snap2 = 1; await shot('toff_air') } if (s.shot === 2 && !ts.some(q => q.snap3)) { s.snap3 = 1; await shot('toff_eliyahu') } if (ts.length > 4 && !s.on && ts.some(q => q.on)) break }
    const on = ts.filter(q => q.on === '3-takeoff'), f1 = on.filter(q => q.shot === 1 && q.P);
    R.takeoff = { planeEnd: await ev("TCCUT.ST.planeEnd||null"), played: on.length > 0, shots: [...new Set(on.map(q => q.shot))], x0: f1.length ? f1[0].P[0] : null, x1: f1.length ? f1[f1.length - 1].P[0] : null, maxZ: Math.max(0, ...f1.map(q => q.P[2])), camNearPlane: f1.filter(q => q.cam).map(q => Math.round(Math.hypot(q.cam.x - q.P[0], q.cam.y - (q.P[1] - .6 * q.P[2])))), ended: !ts[ts.length - 1].on } }
  // (4e) the look of portraits (TCPOR.look) on the people of the scenes, and the light of the scene at night (074d: the light map)
  R.looks = await ev("(()=>{const o={};for(const w of ['st-shimon','st-aharon','st-eliyahu','s9-yossi']){const L=TCCUT.look(w);o[w]=L?{por:!!L.por,skin:L.skin,hair:L.hair&&L.hair.t,hat:L.hat&&L.hat.t,beard:!!L.beard,top:L.top&&L.top.c}:null}return o})()");
  try { await ev("(()=>{c34Night(1);return 1})()"); await p.waitForTimeout(800); await ev("(()=>{TCCUT.play('2-backstage');return 1})()"); await p.waitForTimeout(6500);
    R.night = await ev("(()=>{const S=TCCUT.ST.on;return{on:S&&S.id,shot:S&&S.i,lights:S&&S.lights,wldLights:window.__TC_WLD?window.__TC_WLD.sky().n.lights:null,night:+window.__TC_NIGHT,busy:typeof TCBUSY!=='undefined'?TCBUSY.state():null}})()"); await shot('night_backstage');
    await p.keyboard.press('Escape'); await p.waitForTimeout(600); await ev("(()=>{try{if(typeof TCO!=='undefined'&&TCO.ui)window.__TCO.close()}catch(e){}State.paused=false;c34Night('auto');return 1})()");
    R.nightAfter = await ev("(()=>({on:TCCUT.playing(),busy:typeof TCBUSY!=='undefined'?TCBUSY.state():null}))()") } catch (e) { R.night = { error: String(e).slice(0, 160) } }
  // (4c) the journal (the scenes you reached — ▶) and the row of F9
  R.journal = await ev("(()=>{const F=g77St().flags;F['cut:O-home']=1;F['cut:1-van']=1;const h=g77JrApp();return{card:h.includes('הסצנות של הסיפור'),play:(h.match(/data-cut-play=/g)||[]).length}})()");
  // the real F9 panel (the key), the row of the scenes in it — then closed again
  try { await p.keyboard.press('F9'); await p.waitForTimeout(1500); R.f9 = await ev("(()=>{const s=document.querySelector('[data-cut9=\"sel\"]');return{select:!!s,options:s?s.options.length:0,panel:!!document.getElementById('tcF9')}})()"); await p.keyboard.press('F9'); await p.waitForTimeout(500) } catch (e) { R.f9 = { error: String(e).slice(0, 160) } }
  // the card of the mission board (missions) and the box of the tutorial (newgame) — hidden while a scene plays (the merge 17.11: #tcMbCard over 1-van)
  await ev("(()=>{TCCUT.play('1-van');return 1})()"); await p.waitForTimeout(1200);
  R.overlay = await ev("(()=>{const o={on:TCCUT.playing(),made:[]};for(const id of ['tcMbCard','tcTut','playerHud','miniWrap']){let e=document.getElementById(id);if(!e&&id.startsWith('tc')){e=document.createElement('div');e.id=id;e.dataset.qaTmp='1';e.style.cssText='position:fixed;top:150px;right:18px';document.body.appendChild(e);o.made.push(id)}o[id]=e?getComputedStyle(e).visibility:null}for(const e of document.querySelectorAll('[data-qa-tmp]'))e.remove();o.fig=typeof window.tcStepFig==='function'?(()=>{const f=tcStepFig('st-shimon'),A=TCCUT.ST.on&&TCCUT.ST.on.actors.shimon;return f?{hold:f.hold,k:f.k,same:!!(A&&A.fig===f),drawn:(window.__TC_SACT&&__TC_SACT.E&&__TC_SACT.E.figDrawn)||null}:null})():'noapi';return o})()"); await shot('van_overlay');
  await p.keyboard.press('Escape'); await p.waitForTimeout(600); R.overlayAfter = await ev("(()=>{const o={on:TCCUT.playing()};if(typeof window.tcStepFig==='function'){const f=tcStepFig('st-shimon');o.figHold=f?!!f.hold:null}for(const id of ['tcMbCard','tcTut']){const e=document.getElementById(id);o[id]=e?getComputedStyle(e).visibility:null}return o})()");
  await ev("(()=>{try{if(typeof TCO!=='undefined'&&TCO.ui)window.__TCO.close()}catch(e){}State.paused=false;return 1})()");
  R.tug = await ev('TCCUT.tugPose()'); R.tugInfo = await ev('TCCUT.tugInfo?TCCUT.tugInfo():null'); R.bus3 = await ev("(()=>{const b=TCCUT.bus3();return b?{id:b.id,x:Math.round(b.v.x),y:Math.round(b.v.y),ph:b.ph}:null})()");
  R.presence = await ev("(()=>{const s=TCCUT.state();return{presence:s.presence,cur:(TCSTORY.cur()||{}).mi}})()");
  // (5) the end: nothing left
  R.final = await ev("(()=>{const s=TCCUT.state();return{on:!!s.on,err:s.err,errs:s.errs,played:s.played,ended:s.ended,body:document.body.classList.contains('tcCutOn'),storyErr:TCSTORY.state().err}})()");
  R.pageErrors = pe;
  R.ok = !!(R.qa && R.qa.ok && R.audit.cut && R.audit.cut.ok && R.opening.started && !R.afterSkip.on && !R.afterSkip.body && R.afterSkip.camToPlayer < 80 && R.van.played && R.van.ended && R.overlay.on && R.overlay.tcMbCard !== 'visible' && R.overlay.tcTut !== 'visible' && !R.overlayAfter.on && !R.overlayAfter.figHold && (R.overlay.fig === 'noapi' || !R.overlay.fig || R.overlay.fig.same) && R.looks['st-shimon'] && R.looks['st-shimon'].por && R.night && R.night.on === '2-backstage' && R.night.lights > 0 && !R.nightAfter.on && (!R.takeoff || (R.takeoff.played && (R.takeoff.maxZ >= 200 || (R.takeoff.planeEnd && R.takeoff.planeEnd.why === 'until' && R.takeoff.planeEnd.z >= 200)) && R.takeoff.ended)) && !R.final.err && !pe.length);
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, qa: R.qa && R.qa.ok, why: R.qa && R.qa.why, audit: R.audit, opening: R.opening.started, skip: R.afterSkip, van: R.van, land: R.land, landing: R.landing, takeoff: R.takeoff, toff: R.toff, overlay: R.overlay, overlayAfter: R.overlayAfter, qaFig: R.qa && R.qa.fig, f9: R.f9, looks: R.looks, night: R.night, tugInfo: R.tugInfo, errs: pe.length, final: R.final }));
  await b.close();
})().catch(e => { console.error(e); process.exit(1) });
