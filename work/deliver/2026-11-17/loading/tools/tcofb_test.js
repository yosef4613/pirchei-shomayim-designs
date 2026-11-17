// tcofb_test.js <game.html> <outdir> [film|nofilm] — האריח "סרטון הפתיחה" במסך הפתיחה (TCOF) + הפס של מסך הטעינה לא חוזר אחורה
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [f, outd, exp = 'film'] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true }); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  const R = { checks: [], pct: [] }, ok = (n, c, d) => { R.checks.push({ n, ok: !!c, d }); console.log((c ? 'ok   ' : 'FAIL ') + n + (d !== undefined ? ' · ' + JSON.stringify(d).slice(0, 400) : '')) };
  const shot = async n => { try { await p.screenshot({ path: path.join(outd, n + '.png'), timeout: 20000 }) } catch (e) { } };
  const ev = () => p.evaluate(() => { const T = window.__TCO && __TCO.st; const top = T && T.stack[T.stack.length - 1]; let mf = null; try { mf = window.__TC_MAPFIX ? __TC_MAPFIX() : null } catch (e) { }
    return { mode: T && T.mode, ui: T && T.ui, scr: top && top.screen, ld: window.TCLD ? TCLD.state() : null, fb: window.__TC_TCOFB ? __TC_TCOFB() : null, show: (() => { try { return !!__TC_DEV.ev('TCSHOW.on') } catch (e) { return null } })(), mf, t: Math.round(performance.now()) } }).catch(e => ({ err: String(e) }));
  const sample = s => { if (s.ld && s.ld.on) { if (s.ld.n === lastN && s.ld.pct + 1e-6 < last) back.push({ t: s.t, from: last, to: s.ld.pct, line: s.ld.line }); last = s.ld.pct; lastN = s.ld.n; R.pct.push([s.t, s.ld.view, s.ld.pct, s.ld.line, s.mf && s.mf.n && s.mf.n.rebake]) } };
  let s = null, back = [], last = -1, lastN = -1;
  await p.goto('file://' + path.resolve(f) + '#dev&opening&loading', { waitUntil: 'commit' });
  // until the menu is ready; the bar of the loading screen sampled all the time (it must not go back within one load)
  const T0 = Date.now();
  while (Date.now() - T0 < 300000) { s = await ev(); if (s.err) { await p.waitForTimeout(500); continue } sample(s);
    if (s.mode === 'open' && s.scr === 'home' && s.fb && (s.fb.btn || s.fb.why === 'no-tcof') && Date.now() - T0 > 20000) break; await p.waitForTimeout(500) }
  // the strip a little longer (the second bake of mapfix comes later)
  const T1 = Date.now(); while (Date.now() - T1 < 60000) { s = await ev(); if (s.err) { await p.waitForTimeout(500); continue } sample(s); if (s.ld && !s.ld.on) break; await p.waitForTimeout(700) }
  ok('הפס של מסך הטעינה לא חוזר אחורה', back.length === 0, { back: back.slice(0, 3), n: R.pct.length, last: s && s.ld && s.ld.last, sawRemap: R.pct.some(x => /עדכון המפה/.test(x[3] || '')), rebake: s && s.mf && s.mf.n });
  ok('מסך הפתיחה מוכן (open · home)', s.mode === 'open' && s.scr === 'home', { mode: s.mode, scr: s.scr }); await shot('01_home');
  if (exp === 'nofilm') { ok('בלי TCOF — אין אריח, ומסך הבית כמו קודם', !s.fb.btn && s.fb.why === 'no-tcof' && !s.fb.err, s.fb) }
  else {
    const g = await p.evaluate(() => { const b = document.querySelector('#tcoRoot .tiles [data-act="tcofHome"]'), tl = b && b.parentElement, r = b && b.getBoundingClientRect(); return { btn: !!b, txt: b && b.innerText, n: tl && tl.children.length, cols: tl && getComputedStyle(tl).gridTemplateColumns, r: r && [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)], svg: b && b.querySelectorAll('svg').length, img: document.querySelectorAll('img').length } });
    ok('האריח "סרטון הפתיחה" בשורת האריחים (SVG בקוד)', g.btn && /סרטון הפתיחה/.test(g.txt) && g.svg === 1 && g.img === 0 && g.r && g.r[3] > 40 && g.cols && g.cols.split(' ').length === g.n, g);
    await p.evaluate(() => { const b = document.querySelector('#tcoRoot .tcoBtn.pri'); if (b) b.focus() }); let reach = false;
    for (let i = 0; i < 8 && !reach; i++) { await p.keyboard.press('ArrowDown'); reach = await p.evaluate(() => !!(document.activeElement && document.activeElement.dataset.act === 'tcofHome')) }
    ok('אפשר להגיע אליו בחצים', reach);
    await p.click('#tcoRoot [data-act="tcofHome"]'); await p.waitForTimeout(2500); let a = await ev();
    ok('לחיצה → הסרטון רץ מעל מסך הפתיחה', a.show && a.fb.plays === 1 && a.mode === 'open', { show: a.show, fb: a.fb, mode: a.mode }); await shot('02_film');
    await p.waitForTimeout(6000); await shot('03_film8'); const fs1 = await p.evaluate(() => { try { return __TC_DEV.ev('TCSHOW.stats()') } catch (e) { return String(e) } });
    ok('הסרטון מתקדם (פריימים)', fs1 && fs1.frames > 30, fs1);
    await p.keyboard.press('Escape'); await p.waitForTimeout(900); a = await ev();
    ok('Esc → דילוג; חוזרים למסך הבית, לא נכנסים למשחק', !a.show && a.mode === 'open' && a.ui && a.scr === 'home' && a.fb.btn, { show: a.show, mode: a.mode, scr: a.scr, last: a.fb.st && a.fb.st.last });
    const foc = await p.evaluate(() => document.activeElement && document.activeElement.dataset.act); ok('הפוקוס חוזר לאריח', foc === 'tcofHome', foc);
    await p.keyboard.press('Enter'); await p.waitForTimeout(2500); a = await ev(); ok('Enter על האריח → הסרטון', a.show && a.fb.plays === 2, { show: a.show, plays: a.fb.plays });
    await p.keyboard.press('Enter'); await p.waitForTimeout(900); a = await ev();
    ok('Enter בזמן הסרטון — לא נכנס למשחק מאחור', a.mode === 'open', { show: a.show, mode: a.mode, scr: a.scr });
    if (a.show) { await p.keyboard.press('Escape'); await p.waitForTimeout(900); a = await ev() }
    ok('אחרי הסרטון — מסך הבית', !a.show && a.mode === 'open' && a.scr === 'home', { show: a.show, mode: a.mode, scr: a.scr }); await shot('04_back');
    await p.setViewportSize({ width: 420, height: 820 }); await p.waitForTimeout(600);
    const nw = await p.evaluate(() => { const b = document.querySelector('#tcoRoot [data-act="tcofHome"]'), r = b && b.getBoundingClientRect(); return { r: r && [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)], w: innerWidth, h: innerHeight, sx: document.documentElement.scrollWidth } });
    ok('מסך צר — האריח בתוך המסך', nw.r && nw.r[0] >= 0 && nw.r[0] + nw.r[2] <= nw.w + 1 && nw.r[1] + nw.r[3] <= nw.h, nw); await shot('05_narrow'); await p.setViewportSize({ width: 1280, height: 800 }); await p.waitForTimeout(400);
    await p.click('#tcoRoot .tcoBtn.pri:not([disabled])').catch(() => { }); await p.waitForTimeout(800);
    for (let i = 0; i < 4; i++) { const m = await p.evaluate(() => __TCO.st.mode); if (m === 'game') break; const bs = await p.$$('#tcoRoot .tcoBtn:not([disabled])'); let hit = null; for (const b2 of bs) { const tx = await b2.innerText(); if (/משחק חדש כאן|מתחילים|המשך|לשחק בה/.test(tx)) { hit = b2; break } } if (hit) await hit.click().catch(() => { }); await p.waitForTimeout(300) }
    // into the game: the film of a new game (TCOF, how=new) and the loading screen are never one under the other; the name window is never under the full screen
    let t2 = Date.now(), both = 0, nmUnder = 0, sawShow = false, skipped = false; while (Date.now() - t2 < 90000) { a = await ev(); const nm = await p.evaluate(() => { const e = document.getElementById('g77Nm'); return !!(e && getComputedStyle(e).display !== 'none') }).catch(() => false);
      if (a.show) { sawShow = true; if (a.ld && a.ld.on) both++ } if (nm && a.ld && a.ld.on && a.ld.view === 'full') nmUnder++;
      if (a.show && Date.now() - t2 > 9000 && !skipped) { skipped = true; await shot('06_newfilm'); await p.keyboard.press('Escape'); await p.waitForTimeout(400) }
      if (a.mode === 'game' && !(a.ld && a.ld.on) && !a.show && Date.now() - t2 > 4000) break; await p.waitForTimeout(400) }
    const lh = await p.evaluate(() => window.__TC_LDH ? __TC_LDH() : null);
    ok('"המשך" / "משחק חדש" עדיין נכנס למשחק', a.mode === 'game', { mode: a.mode, ld: a.ld && a.ld.last, show: a.show });
    ok('מסך הטעינה לא מתחת לסרטון (יורד כשהסרטון נפתח, חוזר רק אם העיר לא מוכנה)', both <= 1, { both, sawShow, defers: lh && lh.defers, log: lh && lh.log.slice(-6) });
    ok('חלון השם לא מתחת למסך המלא', nmUnder === 0, { nmUnder, nmWait: lh && lh.nmWait });
  }
  ok('0 שגיאות בדף', errs.length === 0, errs.slice(0, 5));
  R.errs = errs; fs.writeFileSync(path.join(outd, 'tcofb.json'), JSON.stringify(R, null, 1)); await b.close(); process.exit(R.checks.every(c => c.ok) ? 0 : 1)
})().catch(e => { console.log('CRASH', e); process.exit(2) });
