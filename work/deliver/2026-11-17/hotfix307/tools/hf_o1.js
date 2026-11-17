// ng_play.js — סוכן newgame (17.11): בדיקת מסירה משמירה נקייה (§8), כמו שחקן: בלי hash, navigator.webdriver מוסתר.
// מסך הפתיחה ← "משחק חדש" ← מקום 1 ← שם ← "סיפור" ← מתחילים ← ההדרכה במקשים בלבד (W A S D, ‏Space, ‏E, ‏F, ‏T, ‏M) ← הסיפור מתחיל (O‑1).
// node ng_play.js <build.html> <out.json> [skip]   — skip: לוחצים "דלג על ההדרכה" בצעד הראשון.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, how] = process.argv.slice(2); const SKIP = how === 'skip', RESUME = how === 'resume', OPEN = how === 'open';  // וגם: filmskip
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  await ctx.addInitScript(() => { try { Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true }) } catch (e) { } try { Object.defineProperty(window, '__TC_DEVH', { get: () => true, set: () => { }, configurable: true }) } catch (e) { } });   /* hotfix307: __TC_DEV.ev בלי ‎#dev בכתובת — כדי לקרוא את המצב; המשחק עצמו כמו לשחקן */
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
    // hotfix307 (מבוסס על newgame/tools/ng_play.js — כלל 19א): משחק חדש → הסרטון → דילוג על ההדרכה → O‑1: יוצאים מהרכב, הולכים לשמעון ליד הבית (כמו בצילום של הבעלים) →
    // F (המקום: נכנס הביתה) → יוצאים → G → הולך, לוחץ יד, מדבר → השיחה d-O-shimon → המכתב (G) → O‑1 נגמרת. במקשים אמיתיים בלבד (חוץ מהיציאה מהבית — HOMEIN.exit).
    await p.waitForFunction(() => window.__TC_TUT && window.__TC_TUT.state().on, null, { timeout: 200000, polling: 500 });
    await p.waitForFunction(() => { const d = document.getElementById('tcTut'), b = d && d.querySelector('[data-tut="skip"]'); return b && d.style.display !== 'none' }, null, { timeout: 240000, polling: 400 });   /* אחרי הסרטון — הכרטיס של ההדרכה מוצג */
    await p.waitForTimeout(600); await p.evaluate(() => { const b = document.querySelector('#tcTut [data-tut="skip"]'); if (b) b.click() }); await p.waitForTimeout(1200); log('דילוג על ההדרכה · ' + JSON.stringify((await st()).tut).slice(0, 120));
    const S = () => p.evaluate(src => JSON.parse(JSON.stringify(window.__TC_DEV.ev(src))), `(()=>{ const A = window.__TC_SACT, q = A && A.MS.cur, f = A && A.FIG['st-shimon']; let c = null; try { const k = TCSTORY.cur(); c = k && { mi: k.mi, step: k.step } } catch (e) { }
      let dlg = null; try { dlg = g77S().open && g77S().open.id } catch (e) { } let home = null; try { home = typeof HOMEIN !== 'undefined' ? { on: !!HOMEIN.H.on, walkIn: !!HOMEIN.H.walkIn } : null } catch (e) { }
      let hud = ''; try { hud = String(hudGoalText()).slice(0, 90) } catch (e) { }
      return { cur: c, ms: q ? { kind: q.kind, key: q.key, who: q.who, at: q.at && [q.at.x | 0, q.at.y | 0] } : null, fig: f && f.pt ? [f.pt.x | 0, f.pt.y | 0] : null, me: [PlayerPed.x | 0, PlayerPed.y | 0], car: [PlayerCar.x | 0, PlayerCar.y | 0], mode: PlayerProfile.mode,
        dlg, home, phone: !!State.phoneOpen, ps: !!(A && A.PS.q), psLast: A && A.PS.last ? { tag: A.PS.last.tag, seen: A.PS.last.seen } : null, gk: A && A.GK ? JSON.parse(JSON.stringify(A.GK)) : 'אין G', hud,
        story: (() => { try { return TCSTORY.state() } catch (e) { return null } })(), graph: !!State.graph } })()`);
    const walkTo = async (tx, ty, near, maxMs) => { const end = Date.now() + (maxMs || 30000); while (Date.now() < end) { const s = await S(); const dx = tx - s.me[0], dy = ty - s.me[1]; if (Math.hypot(dx, dy) < near) return true; const ks = []; if (Math.abs(dx) > 5) ks.push(dx > 0 ? 'KeyD' : 'KeyA'); if (Math.abs(dy) > 5) ks.push(dy > 0 ? 'KeyS' : 'KeyW'); for (const k of ks) await p.keyboard.down(k); await p.waitForTimeout(Math.min(350, Math.max(70, Math.hypot(dx, dy) / 52 * 600))); for (const k of ks) await p.keyboard.up(k) } return false };
    const waitS = async (fn, ms) => { const end = Date.now() + ms; let s; while (Date.now() < end) { s = await S(); if (fn(s)) return s; await p.waitForTimeout(400) } return s };
    const talkKeys = async (until, ms) => { const end = Date.now() + ms; let n = 0, s; while (Date.now() < end) { s = await S(); if (until(s)) return { s, n }; if (s.dlg) { await key(n % 3 === 2 ? 'Digit1' : 'Enter', 80); n++ } await p.waitForTimeout(450) } return { s, n } };
    let s = await waitS(s => s.cur && s.cur.mi === 'O-1', 60000); R.o1Start = s; log('O‑1: ' + JSON.stringify(s.cur) + ' · ' + s.mode + ' · ms ' + JSON.stringify(s.ms));
    // ברכב ליד הבית — עוצרים; המנוע "פותח" את השיחה → actions2 מחכה (טבעת)
    s = await waitS(s => s.ms || s.dlg, 30000); R.armed = s; log('מחכה: ' + JSON.stringify({ ms: s.ms, dlg: s.dlg, hud: s.hud }));
    if (s.mode !== 'walk') { await key('KeyE'); await p.waitForTimeout(1200) }
    s = await S(); const tg = s.fig || (s.ms && s.ms.at); log('ברגל · שמעון ב-' + JSON.stringify(tg) + ' · אני ב-' + JSON.stringify(s.me));
    if (tg) await walkTo(tg[0], tg[1] + 24, 14, 40000);
    await p.waitForTimeout(2500); s = await S(); R.near = s; log('ליד שמעון: ' + JSON.stringify({ me: s.me, fig: s.fig, dlg: s.dlg, ms: s.ms && s.ms.kind, hud: s.hud, cap: s.gk && s.gk.capN }));
    await p.screenshot({ path: out.replace(/\.json$/, '_a_near.png') });
    // F — מה שבעל הבית לחץ
    await key('KeyF'); await p.waitForTimeout(2500); s = await S(); R.afterF = { dlg: s.dlg, home: s.home, phone: s.phone, ps: s.ps, gk: s.gk }; log('F → ' + JSON.stringify(R.afterF));
    await p.screenshot({ path: out.replace(/\.json$/, '_b_F.png') });
    if (s.home && (s.home.on || s.home.walkIn)) { await waitS(s => s.home && s.home.on, 6000); await p.evaluate(() => window.__TC_DEV.ev('(()=>{try{HOMEIN.exit()}catch(e){}return 1})()')); await p.waitForTimeout(1500); log('יציאה מהבית (HOMEIN.exit)') }
    if ((await S()).phone) { await key('KeyF'); await p.waitForTimeout(800) }
    s = await S(); if (s.fig && Math.hypot(s.fig[0] - s.me[0], s.fig[1] - s.me[1]) > 40) await walkTo(s.fig[0], s.fig[1] + 24, 14, 20000);
    // G — המקש החדש
    await key('KeyG'); await p.waitForTimeout(1300); s = await S(); R.midG = { ps: s.ps, dlg: s.dlg, gk: s.gk, mode: s.mode, hud: s.hud }; log('G → ' + JSON.stringify(R.midG));
    await p.screenshot({ path: out.replace(/\.json$/, '_c_G.png') });
    s = await waitS(s => s.dlg, 15000); R.dlg1 = { dlg: s.dlg, psLast: s.psLast }; log('השיחה: ' + JSON.stringify(R.dlg1));
    await p.screenshot({ path: out.replace(/\.json$/, '_d_dlg.png') });
    // השיחה במקשים → השלב השני (המכתב) → G → השיחה → O‑1 נגמרת
    let r = await talkKeys(s => !s.dlg && s.cur && (s.cur.mi !== 'O-1' || s.cur.step >= 1), 60000); log('אחרי השיחה: ' + JSON.stringify(r.s.cur) + ' · ' + r.n + ' מקשים');
    s = await waitS(s => s.ms || s.dlg || !(s.cur && s.cur.mi === 'O-1'), 30000); R.letterArm = { ms: s.ms, cur: s.cur }; log('המכתב: ' + JSON.stringify(R.letterArm));
    if (s.ms && !s.dlg) { if (s.ms.at) await walkTo(s.ms.at[0], s.ms.at[1] + 20, 30, 20000); await key('KeyG'); s = await waitS(s => s.dlg, 15000); R.dlg2 = s.dlg; log('G → ' + s.dlg) }
    r = await talkKeys(s => !s.dlg && s.story && Array.isArray(s.story.done) && s.story.done.includes('O-1'), 60000); R.o1Done = !!(r.s.story && r.s.story.done && r.s.story.done.includes('O-1')); log('O‑1: ' + (R.o1Done ? 'הושלמה' : 'לא הושלמה') + ' · ' + JSON.stringify(r.s.story).slice(0, 160));
    // 1‑1 (שיחה בבית) — G שוב, אם מתחילה בזמן
    s = await waitS(s => s.ms || s.dlg, 25000); R.next = { cur: s.cur, ms: s.ms }; if (s.ms && !s.dlg) { const t = s.fig && s.ms.who === 'st-shimon' ? s.fig : s.ms.at; if (t) await walkTo(t[0], t[1] + 22, 30, 20000); await key('KeyG'); s = await waitS(s => s.dlg, 15000); R.dlg3 = s.dlg; log('1‑1: G → ' + s.dlg) }
    await p.screenshot({ path: out.replace(/\.json$/, '_e_end.png') });
    R.final = await S();
    R.ok = !R.near.dlg && !!R.near.ms && R.dlg1.dlg === 'd-O-shimon' && R.o1Done && !errs.length;
  } catch (e) { R.error = String(e).slice(0, 500); log('שגיאה: ' + R.error) }
  R.errs = errs; fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.error((R.ok ? 'עובר' : 'נכשל') + ' · שגיאות דף: ' + errs.length + (errs.length ? ' · ' + errs.slice(0, 3).join(' | ') : ''));
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
