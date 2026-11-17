// ng_play.js — סוכן newgame (17.11): בדיקת מסירה משמירה נקייה (§8), כמו שחקן: בלי hash, navigator.webdriver מוסתר.
// מסך הפתיחה ← "משחק חדש" ← מקום 1 ← שם ← "סיפור" ← מתחילים ← ההדרכה במקשים בלבד (W A S D, ‏Space, ‏E, ‏F, ‏T, ‏M) ← הסיפור מתחיל (O‑1).
// node ng_play.js <build.html> <out.json> [skip]   — skip: לוחצים "דלג על ההדרכה" בצעד הראשון.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, how] = process.argv.slice(2); const SKIP = how === 'skip', RESUME = how === 'resume', OPEN = how === 'open';  // וגם: filmskip
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  await ctx.addInitScript(() => { try { Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true }) } catch (e) { } });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  const t0 = Date.now(), R = { file: path.basename(file), skip: SKIP, log: [], steps: {}, ok: false };
  const log = s => { const l = Math.round((Date.now() - t0) / 1000) + 's ' + s; R.log.push(l); console.error(l) };
  const st = () => p.evaluate(() => ({ tut: window.__TC_TUT && window.__TC_TUT.state(), pos: window.__TC_TUT && window.__TC_TUT.pos(), story: window.__TC_STORY && window.__TC_STORY.state(), cur: (() => { try { const c = window.__TC_STORY.cur(); return c && { mi: c.mi, step: c.step } } catch (e) { return null } })(), card: (() => { const d = document.getElementById('tcTut'); return d && d.style.display !== 'none' ? d.textContent.slice(0, 160) : '' })(), zones: (() => { try { const S = window.__TC_S9STORY; return Object.keys(S.ST).filter(id => S.step(id) > 0) } catch (e) { return 'err' } })(), nm: !!(window.__G77NM && window.__G77NM.open) }));
  const key = async (k, ms) => { await p.keyboard.down(k); await p.waitForTimeout(ms || 120); await p.keyboard.up(k) };
  const waitStep = async (id, ms) => { const end = Date.now() + (ms || 15000); while (Date.now() < end) { const s = await st(); if (!s.tut.on || s.tut.id !== id) return s; await p.waitForTimeout(250) } return await st() };
  const walkTo = async (tx, ty, near, maxMs) => { const end = Date.now() + (maxMs || 30000); while (Date.now() < end) { const s = (await st()).pos; const dx = tx - s.x, dy = ty - s.y; if (Math.hypot(dx, dy) < near) return true; const ks = []; if (Math.abs(dx) > 6) ks.push(dx > 0 ? 'KeyD' : 'KeyA'); if (Math.abs(dy) > 6) ks.push(dy > 0 ? 'KeyS' : 'KeyW'); for (const k of ks) await p.keyboard.down(k); await p.waitForTimeout(Math.min(400, Math.max(80, Math.hypot(dx, dy) / 52 * 600))); for (const k of ks) await p.keyboard.up(k) } return false };
  try {
    await p.goto('file://' + path.resolve(file), { waitUntil: 'commit' });
    await p.waitForFunction(() => { const x = document.querySelector('#tcoRoot [data-act="new"]'); return x && !x.disabled }, null, { timeout: 600000, polling: 1000 });
    log('מסך הפתיחה'); await p.waitForTimeout(1000);
    // מסך הפתיחה מצויר מחדש כל הזמן (הרקע החי) — לוחצים מתוך הדף, ומחכים למסך הבא
    const tap = async (sel, next) => { for (let i = 0; i < 40; i++) { const ok = await p.evaluate(([a, b]) => { if (b && document.querySelector(b)) return 2; const x = document.querySelector(a); if (x && !x.disabled) { x.click(); return 1 } return 0 }, [sel, next]); if (ok === 2) return true; await p.waitForTimeout(500) } return false };
    if (!await tap('#tcoRoot [data-act="new"]', '#tcoRoot [data-tcs="new:1"]')) throw new Error('אין מסך המקומות');
    if (!await tap('#tcoRoot [data-tcs="new:1"]', '#tcsName')) throw new Error('אין הטופס של משחק חדש');
    if (OPEN) { await tap('#tcoRoot [data-tcs="mode:open"]', '#tcoRoot .tcoOpt.on[data-tcs="mode:open"]') }
    await p.evaluate(() => { const i = document.getElementById('tcsName'); i.value = 'דני'; const b = document.querySelector('#tcoRoot [data-tcs="start:1"]'); b.click() });
    log('משחק חדש · ' + (OPEN ? 'הכול פתוח' : 'סיפור') + ' · "דני"');
    await p.waitForFunction(() => !document.body.classList.contains('tco-open') && window.__TC_TUT, null, { timeout: 600000, polling: 500 });
    log('בתוך המשחק');
    // הכרטיס של ההדרכה
    // 17.11 (החלק השני; 10:15 — הסרטון / מסך הטעינה מזוהים גם לפי ה-DOM: ‎#tcShow / ‎#tcldRoot — TCSHOW / TCLD לא גלובליים בלי ‎#dev): סרטון הפתיחה / מסך הטעינה / חלון השם — הכרטיס של ההדרכה רק אחריהם (filmskip — Enter בסרטון אחרי 4 שנ׳)
    { const F = R.film = { seen: false, ms: 0, overlap: 0, loading: false, shownAt: null, why: {}, auto: null, samples: 0, stepWhileFilm: false }; const tf = Date.now(); let fOn = 0, i0 = null;
      while (Date.now() - tf < 150000) {
        const q = await p.evaluate(() => { const t = window.__TC_TUT.state(); let film = false, ld = false, of = null; try { film = !!TCSHOW.on } catch (e) { } if (!film) film = !!document.getElementById('tcShow'); try { ld = !!(TCLD.st && TCLD.st.on) } catch (e) { } if (!ld) { const r = document.getElementById('tcldRoot'); ld = !!(r && !r.classList.contains('out') && getComputedStyle(r).display !== 'none') } try { of = TCOF.st ? { plays: TCOF.st.plays, auto: TCOF.st.auto, done: TCOF.st.done, skipped: TCOF.st.skipped, why: TCOF.st.why } : null } catch (e) { } return { t, film, ld, of } });
        F.samples++; F.why[q.t.why || '-'] = (F.why[q.t.why || '-'] || 0) + 1; F.auto = q.of; if (q.ld) F.loading = true;
        if (q.film) { if (!F.seen) { F.seen = true; fOn = Date.now(); i0 = q.t.i; log('סרטון הפתיחה רץ · ההדרכה: on=' + q.t.on + ' shown=' + q.t.shown + ' why=' + q.t.why) } if (q.t.shown) F.overlap++; if (q.t.on && q.t.i !== i0) F.stepWhileFilm = true;
          if (how === 'filmskip' && Date.now() - fOn > 4000) { await p.keyboard.press('Enter'); await p.waitForTimeout(400) } }
        else if (F.seen && fOn && !F.ms) { F.ms = Date.now() - fOn; log('הסרטון נגמר אחרי ' + Math.round(F.ms / 1000) + ' שנ׳ · ' + JSON.stringify(q.of)) }
        if (q.t.on && q.t.shown && !q.film) { F.shownAt = Math.round((Date.now() - tf) / 1000); break }
        await p.waitForTimeout(400) }
      log('הכרטיס של ההדרכה הופיע אחרי ' + F.shownAt + ' שנ׳ · סרטון: ' + (F.seen ? 'כן' : 'לא') + ' · חפיפה: ' + F.overlap + ' · טעינה: ' + F.loading + ' · ' + JSON.stringify(F.why)) }
    await p.waitForFunction(() => window.__TC_TUT.state().on, null, { timeout: 30000, polling: 250 });
    let s = await st(); log('ההדרכה התחילה · ' + s.card.slice(0, 90)); R.start = s; R.storyBefore = s.story;
    await p.screenshot({ path: out.replace(/\.json$/, '_1.png') });
    if (SKIP) { await p.evaluate(() => document.querySelector('#tcTut [data-tut="skip"]').click()); await p.waitForTimeout(800); s = await st(); R.steps.skip = s.tut.st; log('דילוג → ' + s.tut.st) }
    else {
      // 1 נהיגה: W / S לסירוגין
      for (let i = 0; i < 20; i++) { s = await st(); if (s.tut.id !== 'drive') break; await key(i % 2 ? 'KeyS' : 'KeyW', 1300) }
      s = await waitStep('drive', 4000); R.steps.drive = s.tut.id; log('נהיגה → ' + s.tut.id + ' · ' + s.card.slice(0, 60));
      // 2 עצירה ויציאה
      await key('Space', 900); await p.waitForTimeout(400); await key('KeyE'); s = await waitStep('exit', 5000); R.steps.exit = s.tut.id; log('E → ' + s.tut.id + ' · מצב ' + s.pos.mode + ' · ניווט ' + s.pos.nav);
      // 3 הליכה לדלת
      await walkTo(s.pos.door.x, s.pos.door.y, 30, 40000); s = await waitStep('walk', 4000); R.steps.walk = s.tut.id; log('הליכה → ' + s.tut.id + ' · ' + JSON.stringify(s.pos).slice(0, 120));
      if (RESUME) { // שמירה באמצע (F6), טעינה מחדש של הדף, "המשך" — ההדרכה ממשיכה מאותו צעד
        await key('F6'); await p.waitForTimeout(2500); const before = s.tut.id; await p.reload({ waitUntil: 'commit' });
        await p.waitForFunction(() => { const x = document.querySelector('#tcoRoot [data-act="continue"]'); return x && !x.disabled }, null, { timeout: 600000, polling: 1000 });
        await p.waitForTimeout(1000); await p.evaluate(() => document.querySelector('#tcoRoot [data-act="continue"]').click());
        await p.waitForFunction(() => !document.body.classList.contains('tco-open') && window.__TC_TUT && window.__TC_TUT.state().on, null, { timeout: 120000, polling: 500 });
        s = await st(); R.steps.resume = s.tut.id; R.resumeOk = s.tut.id === before && s.story && s.story.none; log('אחרי טעינה: ' + s.tut.id + ' (לפני: ' + before + ') · הסיפור ' + JSON.stringify(s.story).slice(0, 40));
        if (s.pos.mode !== 'walk' || Math.hypot(s.pos.x - s.pos.door.x, s.pos.y - s.pos.door.y) > 60) await walkTo(s.pos.door.x, s.pos.door.y, 30, 40000) }
      // 4 F — נפתח, F — נסגר
      await key('KeyF'); await p.waitForTimeout(900); s = await st(); R.steps.fOpen = s.pos.iid; log('F → ' + s.pos.iid + ' · טלפון ' + s.pos.phone);
      await p.screenshot({ path: out.replace(/\.json$/, '_2.png') });
      await key('KeyF'); s = await waitStep('door', 4000); R.steps.door = s.tut.id; log('F שוב → ' + s.tut.id);
      // 5 T
      await key('KeyT'); await p.waitForTimeout(900); await p.screenshot({ path: out.replace(/\.json$/, '_3.png') }); await key('KeyT'); s = await waitStep('phone', 4000); R.steps.phone = s.tut.id; log('T, T → ' + s.tut.id);
      // 6 M
      await key('KeyM'); await p.waitForTimeout(1200); await key('KeyM'); s = await waitStep('map', 4000); R.steps.map = s.tut.id; log('M, M → ' + s.tut.id);
      // 7 חזרה לרכב
      await walkTo(s.pos.car.x, s.pos.car.y, 34, 40000); await key('KeyE'); s = await waitStep('enter', 5000); R.steps.enter = s.tut.st; log('E → ' + s.tut.st + ' · מצב ' + s.pos.mode);
    }
    // הסיפור מתחיל: O‑1
    await p.waitForTimeout(1500); await p.screenshot({ path: out.replace(/\.json$/, '_4.png') });
    const end = Date.now() + 20000; while (Date.now() < end) { s = await st(); if (s.story && !s.story.none && s.cur) break; await p.waitForTimeout(500) }
    R.after = s; log('הסיפור: ' + JSON.stringify(s.story).slice(0, 120) + ' · ' + JSON.stringify(s.cur) + ' · אזורים שהתחילו: ' + JSON.stringify(s.zones));
    await p.waitForTimeout(4000); s = await st(); R.after2 = s; log('אחרי 4 שנ׳: ' + JSON.stringify(s.cur) + ' · כרטיס: ' + s.card.slice(0, 60));
    await p.screenshot({ path: out.replace(/\.json$/, '_5.png') });
    // המשימה הראשונה (O‑1): השיחות עם שמעון ליד הבית — Enter (הלאה) ו-1 (בחירה), במקשים בלבד
    { const end2 = Date.now() + 120000; let n = 0; while (Date.now() < end2) { s = await st(); if (s.story && Array.isArray(s.story.done) && s.story.done.includes('O-1')) break; await key(n % 3 === 2 ? 'Digit1' : 'Enter', 80); n++; await p.waitForTimeout(500) }
      R.o1 = s.story; R.o1Done = !!(s.story && Array.isArray(s.story.done) && s.story.done.includes('O-1')); R.o1Keys = n; log('O‑1: ' + (R.o1Done ? 'הושלמה' : 'לא הושלמה') + ' · ' + n + ' לחיצות · ' + JSON.stringify(s.story).slice(0, 140) + ' · אזורים: ' + JSON.stringify(s.zones)); R.zonesAfterO1 = s.zones }
    await p.screenshot({ path: out.replace(/\.json$/, '_6.png') });
    const want = SKIP ? R.steps.skip === 'skip' : (R.steps.drive === 'exit' && R.steps.exit === 'walk' && R.steps.walk === 'door' && R.steps.fOpen === 'PLAYER-HOME' && R.steps.door === 'phone' && R.steps.phone === 'map' && R.steps.map === 'enter' && R.steps.enter === 'done');
    R.storyBegan = !!(R.after.story && !R.after.story.none && R.after.cur && R.after.cur.mi === 'O-1');
    R.noStoryBefore = !!(R.storyBefore && R.storyBefore.none);
    R.zonesDuring = R.after.zones;
    R.ok = want && (!RESUME || R.resumeOk) && R.storyBegan && R.noStoryBefore && Array.isArray(R.after.zones) && R.after.zones.length === 0 && R.o1Done && !errs.length && !(R.film && (R.film.overlap || R.film.stepWhileFilm || R.film.shownAt == null));
  } catch (e) { R.error = String(e).slice(0, 500); log('שגיאה: ' + R.error) }
  R.errs = errs; fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.error((R.ok ? 'עובר' : 'נכשל') + ' · שגיאות דף: ' + errs.length + (errs.length ? ' · ' + errs.slice(0, 3).join(' | ') : ''));
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
