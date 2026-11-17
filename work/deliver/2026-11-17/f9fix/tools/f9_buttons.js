// f9_buttons.js — f9fix (17.11): לוח הבדיקה F9 — לחיצה על כל כפתור בלשוניות "אירועים" ו"אזורים", ולכל כפתור: שגיאות בדף, הודעה (toast),
// ושינוי המצב המצופה (המצלמה זזה / הלוח זז הצידה / מסך נפתח מעל הכול / סיפור מתחיל מההתחלה / תוצאה מופיעה).
// node f9_buttons.js <game.html> <out.json> [shots_dir]      — יוצא 1 כשיש כפתור שנכשל או שגיאה בדף.
// F9_ZONES=all|N — כמה אזורים לפתוח (ברירת מחדל: כולם). F9_PIX=all|N — כמה כפתורי "זזים בפועל" להריץ (ברירת מחדל: כולם).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  if (!file || !out) { console.error('usage: node f9_buttons.js <game.html> <out.json> [shots_dir]'); process.exit(2) }
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push('pageerror: ' + String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 300)) });
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)), s);
  const loadErrs = errs.length;
  // the helpers inside the game: every toast is recorded; the state of the screen
  await ev(`(()=>{const H=window.__F9H={T:[]};const t0=toast;toast=function(m){try{H.T.push(String(m).replace(/<[^>]*>/g,'').slice(0,200))}catch(e){}return t0.apply(this,arguments)};
   H.top=()=>{const L=[];for(const [x,y] of [[innerWidth/2,innerHeight/2],[innerWidth*.3,innerHeight*.4],[innerWidth*.7,innerHeight*.6]]){const e=document.elementFromPoint(x,y);L.push(!e?'-':e.closest('#tcF9')?'tcF9':e.closest('#tcVoiceTest')?'voicetest':e.closest('#phoneOverlay')?'phone':(e.id||e.tagName.toLowerCase()))}return L};
   H.st=()=>{let ck='';try{const c=gameClock();ck=c.hour+':'+String(c.minute).padStart(2,'0')}catch(e){}let show=false;try{show=!!TCSHOW.on}catch(e){}
    const chip=document.getElementById('tcF9Chip');return{cx:Math.round(Camera.x),cy:Math.round(Camera.y),z:+(+Camera.zoom).toFixed(2),mapQa:!!State.mapQa,hud:!!PERF.hud,phone:!!State.phoneOpen,app:State.phoneApp||null,show,
     vt:!!document.getElementById('tcVoiceTest'),chip:!!(chip&&chip.style.display==='block'),sofs:JSON.stringify(TCF9.sofs||{}),ck,top:H.top(),toasts:H.T.length}};
   H.clean=()=>{try{if(TCSHOW.on)TCSHOW.close()}catch(e){}try{const v=document.getElementById('tcVoiceTest');if(v)v.remove()}catch(e){}try{if(State.phoneOpen)setPhoneOpen(false)}catch(e){}try{speechSynthesis.cancel()}catch(e){}};
   H.open=k=>{H.clean();if(!PERF.hud)tcF9Open();tcF9Show(k);return TCF9.tab};return 1})()`);
  const R = { build: path.basename(file), loadErrs: errs.slice(0, loadErrs), tabs: {}, events: [], zones: [], zoneButtons: [], summary: {} };
  const shot = async n => { if (shots) try { await p.screenshot({ path: path.join(shots, n + '.png') }) } catch (e) {} };
  // 1. F9 from the keyboard, and the two tabs from the mouse
  await p.keyboard.press('F9'); await p.waitForTimeout(600);
  R.f9key = await ev(`({hud:PERF.hud,display:TCF9.el&&TCF9.el.style.display,top:__F9H.top()})`); await shot('00_f9');
  for (const k of ['events', 'zones']) {
    const e0 = errs.length; await p.click('#tcF9Tabs button[data-tab="' + k + '"]'); await p.waitForTimeout(800);
    R.tabs[k] = Object.assign(await ev(`(()=>{const s=tcF9P('${k}');return{buttons:s.querySelectorAll('button').length,details:s.querySelectorAll('details').length,cards:s.querySelectorAll('.tcF9Card').length,bad:[...s.querySelectorAll('.tcF9Bad')].map(x=>x.textContent.slice(0,160)),text:s.textContent.length}})()`), { errs: errs.slice(e0) });
    await shot('01_tab_' + k);
  }
  // a second open of the events tab must show the same (not more, not less)
  { await ev(`__F9H.open('perf')`); await p.waitForTimeout(200); await ev(`__F9H.open('events')`); await p.waitForTimeout(300); R.tabs.events.buttonsSecondOpen = await ev(`tcF9P('events').querySelectorAll('button').length`) }
  // 2. the events: every button, one by one, by a real mouse click
  const evList = await ev(`[...tcF9P('events').querySelectorAll('button')].map((b,i)=>{const r=b.closest('.tcF9Row'),c=b.closest('.tcF9Card');return{i,data:Object.assign({},b.dataset),label:b.textContent.trim().slice(0,60),row:(r?r.textContent:'').replace(/\\s+/g,' ').trim().slice(0,140),card:(c&&c.querySelector('h4')?c.querySelector('h4').textContent:'').slice(0,60)}})`);
  for (const B of evList) {
    await ev(`__F9H.open('events')`); await p.waitForTimeout(150);
    const pre = await ev(`__F9H.st()`), e0 = errs.length; try { B.evtOn0 = await ev(`typeof EVT!=='undefined'?!!EVT.on:null`); B.evtN0 = await ev(`typeof EVT!=='undefined'?EVT.act.length:0`) } catch (e) {}
    let clickErr = null;
    try { /* by its data + label (not by index): the card of events (int300) adds a button for each active event, and the indices move */
      const K = evList.slice(0, evList.indexOf(B)).filter(o => JSON.stringify(o.data) === JSON.stringify(B.data) && o.label === B.label).length;
      const found = await ev(`(()=>{document.querySelectorAll('[data-f9t]').forEach(b=>b.removeAttribute('data-f9t'));const X=${JSON.stringify(JSON.stringify(B.data))},LB=${JSON.stringify(B.label)};const L=[...tcF9P('events').querySelectorAll('button')].filter(b=>JSON.stringify(Object.assign({},b.dataset))===X&&b.textContent.trim().slice(0,60)===LB);const b=L[${K}];if(b)b.setAttribute('data-f9t','1');return !!b})()`);
      if (!found) throw new Error('הכפתור לא נמצא בלשונית (לפי הנתונים והשם)');
      const L = p.locator('#tcF9 section[data-pane="events"] button[data-f9t="1"]'); await L.scrollIntoViewIfNeeded({ timeout: 3000 }); await L.click({ timeout: 4000 }) } catch (e) { clickErr = String(e).slice(0, 200) }
    await p.waitForTimeout(150); const mid = await ev(`__F9H.st()`);
    await p.waitForTimeout(B.data.show || B.data.act === 'voicetest' || B.data.wdrF9 ? 1050 : 750);
    const post = await ev(`__F9H.st()`), toasts = await ev(`__F9H.T.slice(${pre.toasts})`);
    if (shots && (B.data.show || B.data.wdrF9 || B.data.act)) await shot('02_ev_' + String(B.i).padStart(2, '0'));
    const moved = Math.hypot(post.cx - pre.cx, post.cy - pre.cy) > 3 || Math.abs(post.z - pre.z) > .01, drift = Math.round(Math.hypot(post.cx - mid.cx, post.cy - mid.cy)), drifts = drift > 3 && !B.data.cl;
    const phase = B.data.story ? await ev(`(()=>{const s=tcF9StoryList().find(q=>q.id==='${B.data.story}'),m=TCF9_MOD[s.zone];if(!m||!TCF9.sofs||!TCF9.sofs[m[0]])return null;const u=((tcF9Now()-TCF9.sofs[m[0]])/1000-(s.t0||0));return +((((u%s.T)+s.T)%s.T).toFixed(1))})()`) : null;
    const D = B.data; let expect = '', ok = false;
    const onTop = w => post.top.filter(x => x === w).length >= 2, f9Top = post.top.filter(x => x === 'tcF9').length >= 2;
    if (D.story) { expect = 'הסיפור מההתחלה + המצלמה אליו'; ok = phase != null && phase < 5 && moved && !post.hud && !drifts }
    else if (D.show) { expect = 'ההצגה נפתחת במסך מלא מעל הכול'; ok = post.show && !f9Top }
    else if (D.act === 'voicetest') { expect = 'בדיקת הקולות נפתחת מעל הכול'; ok = post.vt && onTop('voicetest') }
    else if (D.act === 'sofs0') { expect = 'הודעה: כל הסיפורים בזמן הרגיל'; ok = toasts.some(t => /בזמן הרגיל/.test(t)) }
    else if (D.act === 'water' && toasts.some(t => /בזמן משחק|אימון/.test(t))) { expect = 'השקיה — או הסבר למה לא עכשיו (משחק / אימון)'; ok = true }
    else if (D.act) { expect = 'האירוע מתחיל + המצלמה אליו'; ok = (moved || (pre.hud && !post.hud && post.chip)) && !post.hud && !drifts }   // the camera may already be there (the final after the league match)
    else if (D.ln) { expect = 'הקו / החניון — הודעה (+ המצלמה)'; ok = toasts.length > 0 && (D.ln === 'pax0' || moved) }
    else if (D.evtgo === 'pause') { expect = 'האירועים האקראיים — עצירה / המשך (EVT.on מתהפך)'; const on = await ev(`typeof EVT!=='undefined'?EVT.on:null`); ok = on === !B.evtOn0; await ev(`(()=>{if(typeof EVT!=='undefined'&&EVT.on!==${!!B.evtOn0}){EVT.on=${!!B.evtOn0};try{evtF9Card()}catch(e){}}})()`) }   /* events (int300): הכרטיס "אירועים אקראיים בעולם" */
    else if (D.evtgo) { expect = 'אירוע אקראי מתחיל + המצלמה אליו (או: "לא נמצא מקום פתוח")'; const n = await ev(`typeof EVT!=='undefined'?EVT.act.length:0`); ok = (n > (B.evtN0 || 0) && moved) || toasts.some(t => /לא נמצא מקום/.test(t)); B.evtNone = toasts.some(t => /לא נמצא מקום/.test(t)) }
    else if (D.evtcam) { expect = 'המצלמה לאירוע הפעיל'; ok = moved || !!(await ev(`(()=>{const e=EVT.act.find(q=>q.id==='${D.evtcam}');return e&&Math.hypot(Camera.x-e.x,Camera.y-e.y)<40})()`)) }
    else if (D.cl === 'leave') { expect = 'השריקה — יש מי שיוצא מהיציע (לא 0)'; ok = toasts.some(t => /השריקה — [1-9]\d* יוצאים/.test(t)) }   /* הבקר 17.11: "0 יוצאים" = לא עובד */
    else if (D.cl) { expect = 'העיר החיה — האירוע מתחיל (הודעה)'; ok = toasts.length > 0 }
    else if (D.wdrF9) { expect = D.wdrF9 === 'all' ? 'הודעה: כל הבגדים בארון' : 'המסך נפתח מעל הלוח'; ok = D.wdrF9 === 'all' ? toasts.some(t => /הבגדים/.test(t)) : (post.phone && onTop('phone')) }
    else { expect = '?'; ok = errs.length === e0 }
    const E = errs.slice(e0); if (E.length || clickErr) ok = false;
    R.events.push({ i: B.i, card: B.card, label: B.label, row: B.row, data: D, expect, ok, moved, drift, phase, toasts, errs: E, clickErr, pre: { cam: [pre.cx, pre.cy, pre.z], hud: pre.hud }, post: { cam: [post.cx, post.cy, post.z], hud: post.hud, chip: post.chip, phone: post.phone, app: post.app, show: post.show, vt: post.vt, top: post.top, sofs: post.sofs !== pre.sofs } });
    await ev(`__F9H.clean()`);
  }
  // 3. the zones: open every zone (a real click on its line), the list of the live items must open; then every button inside
  await ev(`__F9H.open('zones')`); await p.waitForTimeout(400);
  const zl = await ev(`[...tcF9P('zones').querySelectorAll('details')].map(d=>d.dataset.zone)`);
  const nz = process.env.F9_ZONES && process.env.F9_ZONES !== 'all' ? +process.env.F9_ZONES : zl.length;
  for (const z of zl.slice(0, nz)) {
    await ev(`__F9H.open('zones')`); const e0 = errs.length; let clickErr = null;
    try { const L = p.locator('#tcF9 section[data-pane="zones"] details[data-zone="' + z + '"] > summary'); await L.scrollIntoViewIfNeeded({ timeout: 3000 }); await L.click({ timeout: 4000 }) } catch (e) { clickErr = String(e).slice(0, 200) }
    await p.waitForTimeout(250);
    const r = await ev(`(()=>{const d=tcF9P('zones').querySelector('details[data-zone="${z}"]'),body=d.lastElementChild,h=[...body.querySelectorAll('h4')].map(x=>x.textContent);const live=L=>{const m=/\\((\\d+)\\)/.exec(L||'');return m?+m[1]:null};
      return{open:d.open,bodyLen:body.innerHTML.length,head:(d.querySelector('summary').textContent||'').replace(/\\s+/g,' ').slice(0,120),liveRows:body.querySelectorAll('table tr').length?body.querySelectorAll('table tr').length-1:0,liveN:live(h.find(x=>/הפרטים החיים/.test(x))),stories:live(h.find(x=>/הסיפורים/.test(x))),quests:live(h.find(x=>/סיפורי המשחק/.test(x))),questRows:body.querySelectorAll('[data-q]').length,
       bad:[...body.querySelectorAll('.tcF9Bad')].map(x=>x.textContent.slice(0,160)).filter(t=>/שגיאה/.test(t)),hasLayer:!!(window.__TC_LIVE&&window.__TC_LIVE.zones&&window.__TC_LIVE.zones['${z}']),buttons:[...body.querySelectorAll('button')].map(b=>Object.assign({label:b.textContent.trim().slice(0,40)},b.dataset))}})()`);
    const E = errs.slice(e0); r.zone = z; r.errs = E; r.clickErr = clickErr;
    r.questsWant = await ev(`tcF9Quests('${z}').length`);
    r.ok = r.open && r.bodyLen > 0 && !E.length && !clickErr && !r.bad.length && (!r.hasLayer || (r.liveN != null && r.liveN === r.liveRows)) && r.questRows === r.questsWant && (!r.questsWant || r.quests === r.questsWant);
    R.zones.push(r);
  }
  if (shots) { await ev(`(()=>{__F9H.open('zones');const d=tcF9P('zones').querySelector('details[open]');if(d)d.scrollIntoView();return 1})()`); await p.waitForTimeout(300); await shot('03_zones_open') }
  // the buttons inside the zones: every "camera" / "jump" / "from the start" — inside the page (the same click event), the camera must move there
  const npx = process.env.F9_PIX && process.env.F9_PIX !== 'all' ? +process.env.F9_PIX : 1e9; let pixDone = 0;
  for (const Z of R.zones) {
    for (let k = 0; k < Z.buttons.length; k++) {
      const B = Z.buttons[k]; if (B.act === 'pixz' && pixDone >= npx) continue;
      const e0 = errs.length;
      const r = await ev(`(()=>{__F9H.open('zones');const d=tcF9P('zones').querySelector('details[data-zone="${Z.zone}"]');if(!d.open)d.open=true;const bt=d.lastElementChild.querySelectorAll('button')[${k}];if(!bt)return{missing:true};const pre=__F9H.st();bt.click();return{pre,now:__F9H.st()}})()`);
      if (r.missing) { R.zoneButtons.push({ zone: Z.zone, k, data: B, ok: false, why: 'הכפתור לא נמצא' }); continue }
      await p.waitForTimeout(B.act === 'pixz' ? 60 : 200);
      let post = await ev(`__F9H.st()`), extra = null;
      if (B.act === 'pixz') { pixDone++; for (let w = 0; w < 100; w++) { extra = await ev(`(()=>{const o=tcF9P('zones').querySelector('[data-out="pixz-${Z.zone}"]');return o?o.textContent.slice(0,400):''})()`); if (extra && !/מריץ/.test(extra)) break; await p.waitForTimeout(200) } }
      const toasts = await ev(`__F9H.T.slice(${r.pre.toasts})`), E = errs.slice(e0);
      let ok = !E.length, expect = '';
      const at = (q, x, y) => Math.abs(q.cx - x) < 2 && Math.abs(q.cy - y) < 2;
      if (B.cam) { const v = B.cam.split(',').map(Number); expect = 'המצלמה לאזור (ונשארת שם)'; ok = ok && at(r.now, v[0], v[1]) && at(post, v[0], v[1]) && !post.hud }
      else if (B.box) { const v = B.box.split(',').map(Number), x = (v[0] + v[2]) / 2, y = (v[1] + v[3]) / 2; expect = 'המצלמה לפרט (ונשארת שם)'; ok = ok && at(r.now, x, y) && at(post, x, y) && !post.hud }
      else if (B.story) { expect = 'הסיפור מההתחלה + המצלמה'; extra = await ev(`(()=>{const s=tcF9StoryList().find(q=>q.id==='${B.story}'),m=TCF9_MOD[s.zone];if(!m||!TCF9.sofs||!TCF9.sofs[m[0]])return null;const u=((tcF9Now()-TCF9.sofs[m[0]])/1000-(s.t0||0));return 'שלב '+((((u%s.T)+s.T)%s.T).toFixed(1))+' שנ׳ מתוך '+s.T})()`); const ph = extra ? parseFloat(extra.slice(4)) : null; ok = ok && ph != null && ph < 5 && !post.hud }
      else if (B.act === 'pixz') { expect = 'תוצאת "זזים בפועל"'; ok = ok && /זזים/.test(extra || '') }
      /* f9fix (17.11): the stories of the game in the zone — to the place / start now / the check from the start to the end */
      else if (B.qcam) { expect = 'המצלמה למקום של הסיפור (ונשארת)'; extra = await ev(`(()=>{const p=tcF9QuestPlace('${B.qcam}');return p?[Math.round(p.x),Math.round(p.y)]:null})()`); ok = ok && !!extra && Math.abs(post.cx - extra[0]) < 2 && Math.abs(post.cy - extra[1]) < 2 && !post.hud && toasts.length > 0; extra = extra && extra.join(',') }
      else if (B.qgo) { expect = 'הסיפור מתחיל (שלב 1 + ניווט) — או הסבר למה לא'; extra = await ev(`(()=>{const S=tcF9S9();return{step:S.step('${B.qgo}'),done:S.done('${B.qgo}'),nav:State.navigation&&State.navigation.targetId||null}})()`); ok = ok && (extra.step > 0 || extra.done || toasts.some(t => /נעול|הושלם/.test(t))); extra = JSON.stringify(extra) }
      else if (B.qqa) { expect = 'הבדיקה של הסיפור — ✓'; extra = await ev(`(()=>{const o=tcF9P('zones').querySelector('[data-qout="${B.qqa}"]');return o?o.textContent:''})()`); ok = ok && /^✓/.test(extra || '') }
      R.zoneButtons.push({ zone: Z.zone, k, data: B, expect, ok, toasts, errs: E, cam: [post.cx, post.cy, post.z], cam0: [r.now.cx, r.now.cy, r.now.z], out: extra ? extra.slice(0, 200) : undefined });
    }
  }
  await ev(`__F9H.clean()`);
  // 4. the summary
  const cnt = L => ({ total: L.length, ok: L.filter(x => x.ok).length, bad: L.filter(x => !x.ok).length });
  R.summary = { events: cnt(R.events), zones: cnt(R.zones), zoneButtons: cnt(R.zoneButtons), pageErrors: errs.length - loadErrs, loadErrors: loadErrs, seconds: Math.round((Date.now() - t0) / 1000),
    eventsTabErrors: (R.tabs.events.errs || []).length + (R.tabs.events.bad || []).length, zonesTabErrors: (R.tabs.zones.errs || []).length + (R.tabs.zones.bad || []).length };
  R.summary.stories = { live: R.zones.reduce((a, z) => a + (z.stories || 0), 0), game: R.zones.reduce((a, z) => a + (z.quests || 0), 0), zonesWith: R.zones.filter(z => z.stories || z.quests).length, zonesWithout: R.zones.filter(z => !z.stories && !z.quests).map(z => z.zone) };
  R.allErrs = errs.slice(0, 80);
  R.ok = R.summary.events.bad === 0 && R.summary.zones.bad === 0 && R.summary.zoneButtons.bad === 0 && R.summary.pageErrors === 0 && R.summary.eventsTabErrors === 0 && R.summary.zonesTabErrors === 0 && R.tabs.events.buttons > 0 && R.tabs.events.buttons === R.tabs.events.buttonsSecondOpen;
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ ok: R.ok, build: R.build, f9key: R.f9key, tabs: { events: { buttons: R.tabs.events.buttons, second: R.tabs.events.buttonsSecondOpen, bad: R.tabs.events.bad, errs: R.tabs.events.errs.length }, zones: { details: R.tabs.zones.details, bad: R.tabs.zones.bad, errs: R.tabs.zones.errs.length } }, summary: R.summary,
    badEvents: R.events.filter(x => !x.ok).map(x => x.i + ' ' + x.label + ' [' + JSON.stringify(x.data) + '] ' + (x.errs[0] || x.clickErr || '') + ' · ' + (x.toasts[0] || '')).slice(0, 40),
    badZones: R.zones.filter(x => !x.ok).map(x => x.zone + ' ' + (x.errs[0] || x.clickErr || ('rows ' + x.liveRows + '/' + x.liveN))).slice(0, 20),
    badZoneButtons: R.zoneButtons.filter(x => !x.ok).map(x => x.zone + ' ' + JSON.stringify(x.data) + ' ' + (x.errs && x.errs[0] || x.why || '')).slice(0, 20) }));
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(2) });
