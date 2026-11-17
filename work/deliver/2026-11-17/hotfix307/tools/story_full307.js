// story_full307.js <game.html> <out.json> — hotfix307 (18.11): עותק של story56/tools/story_full56.js (כלל 19א) שלוחץ את המקש של השלב — G (actions2: שום שלב לא מתחיל בלי הפעלה; hotfix307: G במקום F).
// כשהמנוע של הסיפור "פותח" שיחה / עבודה / סרט — actions2 מחכה (טבעת, __TC_SACT.MS.cur): הכלי לוחץ G (מקלדת אמיתית), ואם לא התחיל (רחוק מהטבעת) — מקרב את השחקן ולוחץ שוב (עד 4 פעמים). הכול נרשם ב-how.
// המקור: story_full56.js <game.html> <out.json> — story56 (17.11): עותק של story2/tools/story_full.js (כלל 19א) עם הצעדים של פרקים 5, 6 והסוף (pen3 / fish63 / flight55 / tug57),
// הסצנות מפרק 5 והלאה מתנגנות באמת (TCCUT.auto(true)) והבדיקה מחכה להן; בסוף — סצנת הסיום (end:F) מתנגנת עד הסוף. המקור: story2: הבירור "למה הסיפור לא מסתיים" — כל הסיפור הראשי משמירה נקייה, מצב "סיפור" (הנעילות), הלוח של המשימות פועל.
// מבוסס על deliver/2026-11-11/story/tools/story_e2e.js (כלל 19א). המנוע רץ במצב אמיתי (לא E.qa): כל שלב מחכה לתנאי האמיתי שלו (near / stopped / hours / activeMission / busy / cool).
// התנועה מקוצרת: הרכב / השחקן מוזז לנקודה של השלב (TCSTORY.bring — הנקודה הקרובה בכביש), השעון קדימה בהמתנה בין משימות. קיצורים (נרשמים ב-how): סוף עבודה (missionComplete),
// מבחן רישיון (finishLicenseTrial(true)), דגים (המונים של LIC570 / מלאי), שלבי סיפורי אזור (S9STORY.advance), סוף הסרט (TCSHOW.close(true)).
// על כל שלב: כמה זמן, איך עבר, ואם נתקע — האבחון (התנאי שלא מתקיים) לפני הדילוג. בסוף: איפה הסיפור נגמר ומה רואים (הפרק, היומן, הלוח, משימת ההמשך).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2); const MAXSEC = +(process.env.MAXSEC || 1800);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => v === undefined ? null : JSON.parse(JSON.stringify(v))), s);
  const R = { file: path.basename(file), log: [], steps: [], stalls: [], waits: [], t0: Date.now() }; const L = t => { R.log.push(((Date.now() - R.t0) / 1000).toFixed(1) + ' ' + t); console.log(R.log.at(-1)) };
  const sleep = ms => p.waitForTimeout(ms);
  async function talk() {
    for (let i = 0; i < 80; i++) {
      const o = await ev('(()=>{const O=g77S().open;if(!O)return null;const r=g77S().dlgs[O.id].rows[O.node],ch=(r.choices||[]).filter(c=>g77StCond(c.cond));let j=ch.findIndex(c=>c.rel||c.set||c.story);if(j<0)j=0;return{id:O.id,node:O.node,full:O.full,n:ch.length,j}})()');
      if (!o) return true;
      try { if (o.n && o.full) await p.click('#g77Dlg [data-st-ch="' + o.j + '"]', { timeout: 3000 }); else await p.click('#g77Dlg .tx', { timeout: 3000 }) } catch (e) { await ev('(()=>{const O=g77S().open;if(O)g77DlgClose&&g77DlgClose();return 1})()') }
      await sleep(160);
    }
    return false;
  }
  async function waitFor(expr, ms) { const t = Date.now(); while (Date.now() - t < ms) { if (await ev(expr)) return true; await sleep(350) } return false }
  // hotfix307: G — השלב שמחכה לשחקן (הסיפור הראשי: MS.cur). מחכה לחימוש, לוחץ G; אם לא התחיל — מקרב (ברגל: ליד הדמות / המקום; ברכב: לנקודה) ושוב.
  async function gStart(ms) {
    const armed = await waitFor('!!(window.__TC_SACT&&__TC_SACT.MS.cur)||!!g77S().open||!!(PlayerProfile.activeMission)||!!(typeof TCSHOW!=="undefined"&&TCSHOW.on)', ms || 20000);
    if (!armed) return 'G: לא חומש'; if (!(await ev('!!(__TC_SACT.MS.cur)'))) return 'G: לא צריך (נפתח לבד)';
    for (let k = 0; k < 4; k++) {
      try { await p.keyboard.press('KeyG') } catch (e) { } await sleep(700);
      const g = await ev('(()=>{const A=__TC_SACT;return{r:!!(A.GK.last&&A.GK.last.r),why:A.GK.last&&A.GK.last.why,ps:!!A.PS.q,cur:!!A.MS.cur}})()');
      if (g.r || g.ps || !g.cur) { R.gPress = (R.gPress || 0) + 1 + k; return 'G (' + (k + 1) + ')' }
      await ev(`(()=>{const A=__TC_SACT,q=A.MS.cur;if(!q||!q.at)return 0;const f=q.who?A.FIG[q.who]:null,P=f&&f.pt&&!f.hide?f.pt:q.at;if(PlayerProfile.mode==='walk'){PlayerPed.x=P.x+${10 + k * 6};PlayerPed.y=P.y+${18 + k * 4}}else{PlayerCar.speed=0;try{TCSTORY.bringNow()}catch(e){}}return 1})()`); await sleep(900) }
    R.gFail = (R.gFail || 0) + 1; return 'G: לא התחיל אחרי 4 לחיצות' }
  // the diagnosis of a step that does not move: every condition of runStep (074ze), as the engine sees it
  const DIAG = `(()=>{const m=TCSTORY.D&&g77St().main,c=TCSTORY.cur();if(!c||!c.s)return{none:true,st:TCSTORY.state()};const s=c.s,id=s.at||s.go||s.nav,P=navPoiRegistry()[id];let a=null;try{a=playerActor()}catch(e){}
    const d=P&&a?Math.round(Math.hypot(a.x-P.x,a.y-P.y)):null;let lk=null;try{lk=TCSTORY.locked('place',id)}catch(e){}let lz=null;try{lz=a?TCSTORY.locked('zone',currentChunkId(a.x,a.y)):null}catch(e){}
    let reach=null;try{if(typeof TCLOCK!=='undefined'&&TCLOCK.ptReach&&P)reach=TCLOCK.ptReach(P.x,P.y)}catch(e){}
    const busy=(()=>{const o=[];try{if(typeof TCCUT!=='undefined'&&TCCUT.on())o.push('cut')}catch(e){}try{if(typeof TCO!=='undefined'&&(TCO.ui||TCO.lock||TCO.mode==='boot'||TCO.mode==='open'))o.push('tco:'+TCO.mode)}catch(e){}try{if(TCSHOW.on)o.push('show')}catch(e){}try{if(g77Nm().open)o.push('name')}catch(e){}if(State.paused)o.push('paused');if(State.mapOpen)o.push('map');return o})();
    return{mi:c.mi,step:c.step,s,poi:id,poiOk:!!P,dist:d,r:s.r||150,mode:PlayerProfile.mode,kmh:(()=>{try{return +carKmh().toFixed(1)}catch(e){return null}})(),am:PlayerProfile.activeMission&&PlayerProfile.activeMission.id,exam:!!State.licenseExam,dlg:!!g77S().open,phone:!!State.phoneOpen,
     hour:+(gameClock().min/60).toFixed(2),lockPlace:lk,lockHere:lz,reach,busy,err:TCSTORY.E.err,errs:TCSTORY.E.errs,open:TCSTORY.open?TCSTORY.open().map(q=>q.id+'/'+q.step):null,
     job:s.job?{def:!!MISSION_DEFS[s.job],hidden:(()=>{try{return d5MissionHidden(s.job)}catch(e){return 'err'}})(),lock:(()=>{try{return TCSTORY.locked('job',s.job)}catch(e){return 'err'}})(),lic:(MISSION_DEFS[s.job]||{}).license||null,licOk:(MISSION_DEFS[s.job]||{}).license?licenseOwned(MISSION_DEFS[s.job].license):true}:null,
     area:s.area?{st:S9STORY.step(s.area),done:S9STORY.done(s.area),lock:(()=>{try{return TCSTORY.locked('area',s.area)}catch(e){return 'err'}})()}:null}})()`;
  // setup: the story mode (the locks), the board of the missions, a clean story
  L('setup: ' + JSON.stringify(await ev('(()=>{try{c34Night(0)}catch(e){}TCSTORY.E.modeOv="story";const f=(typeof MBOARD!=="undefined")?MBOARD.force(true):null;const s=g77St();delete s.main;delete s.board;TCSTORY.begin();return{mode:TCSTORY.mode(),board:f,lvl:TCSTORY.state(),bringHome:TCSTORY.bringNow()}})()')));
  await sleep(2500);
  let guard = 0, lastKey = '', same = 0, idle = 0;
  while (guard++ < 700 && (Date.now() - R.t0) / 1000 < MAXSEC) {
    // a call — "ענה", and the dialog
    if (await ev('!!(g77Sp().ring)')) { try { await p.click('#g77Ring .ok', { timeout: 3000 }) } catch (e) { } await sleep(500); const w = await ev('g77S().open&&g77S().open.id'); await talk(); L('שיחה נכנסת — נענתה: ' + w); R.calls = (R.calls || 0) + 1; continue }
    if (await ev('(()=>{try{return TCCUT.playing()}catch(e){return false}})()')) { const id = await ev('TCCUT.ST.on&&TCCUT.ST.on.id'); const t = Date.now(); await waitFor('!TCCUT.playing()', 70000); R.scenes = R.scenes || []; R.scenes.push({ id, sec: Math.round((Date.now() - t) / 1000) }); L('סצנה: ' + id + ' · ' + Math.round((Date.now() - t) / 1000) + ' שנ׳'); continue }
    { const ch = await ev('(()=>{const m=TCSTORY.M();return m&&m.ch})()'); if (['5', '6', 'F'].includes(ch) && !R.autoCut) { R.autoCut = await ev('TCCUT.auto(true)'); L('הסצנות מתנגנות מעכשיו: ' + R.autoCut) } }
    if (await ev('!!g77S().open')) { const w = await ev('g77S().open.id'); await talk(); L('שיחה פתוחה — נסגרה: ' + w); continue }
    const st = await ev('TCSTORY.state()'); const c = await ev('TCSTORY.cur()');
    if (!st || st.none) { L('אין סיפור: ' + JSON.stringify(st)); break }
    if (st.soon || st.end) { L('סוף מה שנבנה: ' + JSON.stringify(st).slice(0, 300)); R.endState = st; break }
    if (!c || !c.s) {   // between the missions: why (delay / hours / busy) — the clock forward, like a wait
      const nx = await ev('TCSTORY.next&&TCSTORY.next()'); idle++;
      if (idle % 4 === 1) R.waits.push({ at: st.ch + ' ' + JSON.stringify(st.done.slice(-1)), next: nx });
      if (idle > 60) { L('ממתין יותר מדי: ' + JSON.stringify({ st, nx })); R.stalls.push({ key: 'wait:' + (nx && nx.id), why: 'אין משימה פתוחה אחרי 60 המתנות', nx, st }); break }
      await ev('(()=>{const c=gameClock(),t=c.min+25;gameClockSet(Math.floor(t/60)%24,Math.floor(t%60));return 1})()'); await sleep(1200); continue }
    idle = 0;
    const s = c.s, key = c.mi + '/' + c.step;
    if (key === lastKey) same++; else { same = 0; lastKey = key }
    if (same >= 3) {   // stuck: the diagnosis, then the skip (to see what comes after)
      const dg = await ev(DIAG); R.stalls.push({ key, diag: dg }); L('תקוע ' + key + ' — ' + JSON.stringify(dg).slice(0, 700)); await ev('TCSTORY.skip()'); same = 0; await sleep(800); continue }
    const t1 = Date.now(); let ok = false, how = '';
    const moved = `(()=>{const c=TCSTORY.cur();return !c||c.mi!=="${c.mi}"||c.step!==${c.step}})()`;
    if (s.talk) { await ev('(()=>{if(PlayerProfile.mode!=="walk"){PlayerCar.speed=0}return TCSTORY.bringNow()})()'); const gh = await gStart(26000); const op = await waitFor('!!g77S().open||' + moved, 40000); if (op && await ev('!!g77S().open')) { await sleep(300); ok = await talk(); how = 'שיחה · ' + gh } else how = 'השיחה לא נפתחה · ' + gh; ok = await waitFor(moved, 4000) }
    else if (s.go) { await ev('TCSTORY.bringNow()'); ok = await waitFor(moved, 5000); how = 'הגעה' }
    else if (s.state === 'vanFixed') {
      await ev("TCSTORY.bring('D3-GARAGE')"); await sleep(600); await ev('(()=>{try{repairAtGarage()}catch(e){}return 1})()'); await sleep(400); await ev("TCSTORY.bring('D3-FUEL')"); await sleep(600); await ev('(()=>{try{refuelAtStation()}catch(e){}return 1})()');
      ok = await waitFor(moved, 5000); how = 'מוסך + דלק' }
    else if (s.state === 'boughtFood') {
      await ev("TCSTORY.bring('C2-MALL')"); await sleep(600);
      const r = await ev("(()=>{const id=Object.keys(SHOP_CATALOG).find(k=>!SHOP_CATALOG[k].exclusive&&/כריך|ארוחה|קפה/.test(SHOP_CATALOG[k].name));openPoiPhone('shop','C2-MALL');State.shopId='C2-MALL';State.interactionId='C2-MALL';const n0=ensureEconomySchema().purchases.length;buyShopItem(id);const n1=ensureEconomySchema().purchases.length;setPhoneOpen(false);return{id,bought:n1>n0}})()");
      how = 'קנייה: ' + JSON.stringify(r); ok = await waitFor(moved, 5000) }
    else if (s.state === 'zoomOut') { await ev('(()=>{Camera.zoom=(typeof ZOOM_MIN!=="undefined"?ZOOM_MIN:.45);return 1})()'); ok = await waitFor(moved, 6000); await ev('(()=>{Camera.zoom=1;return 1})()'); how = 'זום החוצה' }
    else if (s.state === 'lake15' || s.state === 'coast10') {
      const k = s.state === 'lake15' ? 'lake' : 'coastal', n = s.state === 'lake15' ? 15 : 10;
      how = 'דגים (קיצור — המונה): ' + JSON.stringify(await ev(`(()=>{const C=(typeof LIC570!=='undefined'&&LIC570.counts)?LIC570.counts():(ensureFishingSchema().counts||(ensureFishingSchema().counts={}));const f=ensureFishingSchema();f.counts=f.counts||{};f.counts['${k}']=Math.max(f.counts['${k}']||0,${n});try{if(C&&C!==f.counts)C['${k}']=Math.max(C['${k}']||0,${n})}catch(e){}return{c:(typeof LIC570!=='undefined'&&LIC570.counts)?LIC570.counts():f.counts}})()`));
      ok = await waitFor(moved, 5000) }
    else if (s.state === 'pen3') { await ev('TCSTORY.bringNow()'); how = 'פנדלים 4/5 (קיצור — האימון האחרון)'; await ev("(()=>{const a=ensureA4Sports();a.last={kind:'penalty',score:4,outOf:5,at:new Date(Date.now()+2000).toISOString()};return 1})()"); ok = await waitFor(moved, 6000) }
    else if (s.state === 'fish63') { await ev('TCSTORY.bringNow()'); how = '3 דגים (קיצור — מלאי)'; await ev("(()=>{const f=ensureFishingSchema();f.inventory=f.inventory||[];for(let i=0;i<3;i++)f.inventory.push({id:'FS-S56-'+i,habitat:'coastal',sizeIndex:1,caughtAt:new Date(Date.now()+2000).toISOString(),name:'בדיקה'});return 1})()"); ok = await waitFor(moved, 6000) }
    else if (s.watch === 'flight55' || s.watch === 'tug57') { const t = Date.now(); ok = await waitFor(moved, 300000); how = 'תצפית ' + s.watch + ' (במשחק, בלי קיצור): ' + Math.round((Date.now() - t) / 1000) + ' שנ׳' }
    else if (s.state === 'seaBig') { how = 'דג גדול בים (קיצור — מלאי)'; await ev("(()=>{const f=ensureFishingSchema();f.inventory=f.inventory||[];f.inventory.push({id:'FS-SEA-QA',habitat:'sea',sizeIndex:3,caughtAt:new Date(Date.now()+2000).toISOString(),name:'בדיקה'});return 1})()"); ok = await waitFor(moved, 5000) }
    else if (s.license === 'LIC-12') { await ev('TCSTORY.bringNow()'); await sleep(600); await ev("(()=>{PlayerProfile.licenses['LIC-12']={state:'owned',acquiredAt:new Date().toISOString(),bestScore:null,source:'e2e'};return 1})()"); how = 'רישיון הדיג העמוק (קיצור — נקנה; במשחק: F במועדון השייט)'; ok = await waitFor(moved, 6000) }
    else if (s.license === 'LIC-16') { await ev('TCSTORY.bringNow()'); await sleep(600); const fly = await ev("(()=>{try{return !!(window.__TC_FLY&&LICENSE_TRIALS['LIC-16'])}catch(e){return false}})()");
      await ev("(()=>{PlayerProfile.licenses['LIC-16']={state:'owned',acquiredAt:new Date().toISOString(),bestScore:null,source:'e2e'};return 1})()"); how = 'מבחן המסוק (קיצור — הרישיון ניתן; המבחן עצמו בשדה, 074zv): ' + fly; ok = await waitFor(moved, 6000) }
    else if (s.license) {
      await ev('TCSTORY.bringNow()'); await sleep(600); const ex = await ev(`(()=>{try{if(!licenseOwned('${s.license}'))startLicenseTrial('${s.license}')}catch(e){return 'err '+e}return State.licenseExam&&State.licenseExam.id})()`); await sleep(1200);
      await ev('(()=>{try{if(State.licenseExam)finishLicenseTrial(true)}catch(e){}return 1})()'); how = 'מבחן (קיצור — עבר): ' + ex; ok = await waitFor(moved, 5000) }
    else if (s.watch) { const real = await waitFor('(()=>{try{return LN.bus.some(b=>String(b.L)==="3"&&b.v&&b.ph!=="park"&&currentChunkId(b.v.x,b.v.y)==="D6")}catch(e){return false}})()', 60000);
      how = real ? 'אוטובוס אמיתי של קו 3 ב-D6' : 'לא הגיע ב-60 שנ׳ — דילוג (במשחק: עובר לבד אחרי maxSec)'; if (!real) await ev('TCSTORY.skip()'); ok = await waitFor(moved, 6000) }
    else if (s.show) {
      await ev('(()=>{const c=gameClock();if(c.min/60<17||c.min/60>23)gameClockSet(17,0);return TCSTORY.bringNow()})()'); const gh = await gStart(30000); const on = await waitFor('!!TCSHOW.on', 40000); R.showG = gh;
      if (on) { await sleep(3000); await ev('TCSHOW.close(true)') } how = 'הסרט נפתח: ' + on + ' (קיצור — סוף)'; ok = await waitFor(moved, 6000) }
    else if (s.job) {
      const hr = s.hours; if (hr) await ev(`(()=>{const h=gameClock().min/60;const H=${JSON.stringify(hr)};const inH=H[0]<=H[1]?h>=H[0]&&h<H[1]:h>=H[0]||h<H[1];if(!inH)gameClockSet(Math.floor(H[0]),Math.round((H[0]%1)*60)+2);return 1})()`);
      await ev('TCSTORY.bringNow()'); if (s.walk) await ev('(()=>{try{if(PlayerProfile.mode==="vehicle")exitVehicle()}catch(e){}return 1})()'); else await ev('(()=>{PlayerCar.speed=0;return 1})()');
      const gh = await gStart(20000); let st0 = await waitFor(`!!(PlayerProfile.activeMission&&PlayerProfile.activeMission.id==="${s.job}")||${moved}`, 40000);
      if (!st0 && await ev('PlayerProfile.mode==="walk"')) { await ev('(()=>{PlayerPed.x=PlayerCar.x+8;PlayerPed.y=PlayerCar.y+8;return 1})()'); await sleep(300); try { await p.keyboard.press('KeyE') } catch (e) { } st0 = await waitFor(`!!(PlayerProfile.activeMission&&PlayerProfile.activeMission.id==="${s.job}")||${moved}`, 15000) }   /* "המסמכים אצלך — E לרכב" */
      const def = await ev(`(()=>{const d=MISSION_DEFS["${s.job}"];return d?{type:d.type,stops:(d.stops||[]).length,pickup:d.pickup||null,dropoff:d.dropoff||null}:null})()`);
      if (await ev(`!!(PlayerProfile.activeMission&&PlayerProfile.activeMission.id==="${s.job}")`)) { await sleep(1500); await ev('(()=>{try{missionComplete()}catch(e){return "err "+e}return 1})()'); how = 'העבודה התחילה (' + gh + ' · ' + JSON.stringify(def) + ') · סוף (קיצור — missionComplete)' }
      else how = 'העבודה לא התחילה (' + gh + '): ' + JSON.stringify(def);
      ok = await waitFor(moved, 6000) }
    else if (s.area) {
      let n0 = await ev(`S9STORY.step("${s.area}")`), k = 0; const tr = [];
      for (k = 0; k < 14; k++) {
        const z = await ev(`(()=>{const S=S9STORY.ST["${s.area}"],n=S9STORY.step("${s.area}")||0;if(S9STORY.done("${s.area}"))return{done:true};const st=n>0?S.steps[n-1]:null;return{n,len:S.steps.length,poi:st&&st.poi||S.start,drive:st&&st.drive||null,kinds:st?Object.keys(st).filter(x=>typeof st[x]!=='string').join(','):'',hours:S.hours||null}})()`);
        if (!z || z.done) break; tr.push(z.n + ':' + (z.poi || '') + (z.drive ? '(drive)' : ''));
        if (!z.n) { await ev(`(()=>{try{S9STORY.start("${s.area}")}catch(e){}return 1})()`); await sleep(500); continue }
        if (z.poi) await ev(`TCSTORY.bring("${z.poi}")`); else if (z.drive) await ev(`(()=>{PlayerCar.x=${z.drive && z.drive[0]};PlayerCar.y=${z.drive && z.drive[1]};return 1})()`);
        await sleep(700); await ev(`(()=>{try{S9STORY.advance("${s.area}")}catch(e){}return 1})()`); await sleep(300) }
      how = 'סיפור אזור ' + s.area + ' (קיצור — advance): ' + tr.join(' → '); ok = await waitFor(moved, 6000) }
    else { how = 'לא מוכר: ' + JSON.stringify(s); }
    R.steps.push({ key, ok, how, sec: +((Date.now() - t1) / 1000).toFixed(1), ch: st.ch }); L(key + ' ' + (ok ? '✓' : '✗') + ' ' + how);
    await sleep(400);
  }
  await sleep(1500);
  { const t = Date.now(); const st0 = await ev('(()=>{const m=TCSTORY.M();return{end:!!(m&&m.end),seen:!!g77St().flags["cut:end:F"],played:TCCUT.ST.played}})()'); await ev("TCCUT.play('end:F',{why:'e2e'})"); const on = await waitFor('TCCUT.playing()', 15000); await waitFor('!TCCUT.playing()', 60000);
    R.endScene = { before: st0, started: on, sec: Math.round((Date.now() - t) / 1000), after: await ev('({played:TCCUT.ST.played,ended:TCCUT.ST.ended,err:TCCUT.ST.err,lvl:TCSTORY.locked("zone","H9")})') }; L('סצנת הסיום: ' + JSON.stringify(R.endScene)) }
  R.final = await ev('(()=>{const s=g77St(),m=s.main;let jr="";try{jr=g77JrApp().replace(/<[^>]+>/g," ").replace(/\\s+/g," ").slice(0,1500)}catch(e){}let mb=null;try{mb={counts:MBOARD.counts(),board:MBOARD.board()}}catch(e){}return{state:TCSTORY.state(),stats:TCSTORY.stats&&TCSTORY.stats(),done:m?Object.keys(m.done):[],msgs:s.msgs.length,journal:s.journal.map(j=>j.id+":"+j.state),jr,mb,err:TCSTORY.E.err}})()');
  R.gk = await ev('JSON.parse(JSON.stringify(__TC_SACT.GK))'); R.errors = errs; R.sec = Math.round((Date.now() - R.t0) / 1000); fs.writeFileSync(out, JSON.stringify(R, null, 1)); L('סוף · ' + JSON.stringify(R.final).slice(0, 1500) + ' · שגיאות ' + errs.length);
  await b.close();
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
