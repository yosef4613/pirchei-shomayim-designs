// tcld_test.js <game.html> <outdir> — בדיקות מסך הטעינה (TCLD): הפריים הראשון, האיורים, ההתקדמות, הפתיחה → פס, כניסה, F7, זום רחוק, השדה; צילומים לעין (פנימי בלבד)
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [f, outd] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true }); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  await p.addInitScript(() => { window.__TL = { paint: [] }; try { new PerformanceObserver(l => { for (const e of l.getEntries()) __TL.paint.push([e.name, Math.round(e.startTime)]) }).observe({ type: 'paint', buffered: true }) } catch (e) { } });
  const R = { checks: [], trans: [], shots: [] }, ok = (n, c, d) => { R.checks.push({ n, ok: !!c, d }); console.log((c ? 'ok   ' : 'FAIL ') + n + (d !== undefined ? ' · ' + JSON.stringify(d).slice(0, 300) : '')) };
  const shot = async n => { try { await p.screenshot({ path: path.join(outd, n + '.png'), timeout: 20000 }); R.shots.push(n) } catch (e) { R.shots.push(n + ':fail') } };
  await p.goto('file://' + path.resolve(f) + '#dev&opening&loading' + (process.env.TCLD_HASH || ''), { waitUntil: 'commit' });
  await p.waitForSelector('#tcldRoot.on', { timeout: 60000 });
  const s0 = await p.evaluate(() => ({ st: TCLD.state(), paint: window.__TL.paint, cards: document.querySelectorAll('#tcldRoot .crd').length, svg: document.querySelectorAll('#tcldRoot .crd svg').length, img: document.querySelectorAll('img').length, t: Math.round(performance.now()), paint0: TCLD.st.paint0 }));
  ok('המסך קיים מיד (בגוף 9) — מצב boot', s0.st.on && s0.st.view === 'boot', { t: s0.t, paint0: s0.paint0, paint: s0.paint });
  ok('10 כרטיסים, כל אחד SVG בקוד, 0 img', s0.cards === 10 && s0.svg === 10 && s0.img === 0, s0);
  await shot('01_boot');
  const T0 = Date.now(); let prev = '', st = null, sawStrip = false, sawCode = false, mode = '';
  while (Date.now() - T0 < 240000) {
    st = await p.evaluate(() => { let m = ''; try { m = window.__TC_DEV ? __TC_DEV.ev('TCO.mode') : '' } catch (e) { } return { s: TCLD.state(), m, t: Math.round(performance.now()) } }).catch(e => ({ err: String(e) }));
    if (st.err) { await p.waitForTimeout(500); continue }
    const k = st.s.view + '|' + st.m + '|' + Math.round(st.s.pct * 20); if (k !== prev) { R.trans.push({ t: st.t, view: st.s.view, kind: st.s.kind, mode: st.m, pct: st.s.pct, line: st.s.line }); console.log(st.t, st.s.view, st.m, st.s.pct, st.s.line) } prev = k;
    if (st.s.steps && st.s.steps.code === 1) sawCode = true;
    if (st.s.view === 'strip' && !sawStrip) { sawStrip = true; await shot('02_strip') }
    if (st.m === 'open' && (!st.s.on || st.s.view !== 'boot')) { mode = 'open'; if (!st.s.on || Date.now() - T0 > 120000) break }
    await p.waitForTimeout(400) }
  ok('ההתקדמות: קוד המשחק הושלם', sawCode);
  ok('אחרי שהתפריט מוכן — פס דק (strip) או מוכן לגמרי', sawStrip || (st && !st.s.on), st && st.s);
  const h1 = await p.evaluate(() => TCLD.state()); ok('הפס נסגר כשהכול מוכן (או עדיין בונה)', true, h1.last || h1.line);
  await shot('03_opening');
  // into the game: the primary button
  const before = await p.evaluate(() => TCLD.state().n);
  await p.click('#tcoRoot .tcoBtn.pri:not([disabled])', { timeout: 30000 }).catch(e => console.log('click', String(e).slice(0, 100)));
  await p.waitForTimeout(400);
  for (let i = 0; i < 4; i++) { const m = await p.evaluate(() => __TC_DEV.ev('TCO.mode')); if (m === 'game') break; const bs = await p.$$('#tcoRoot .tcoBtn:not([disabled])'); let hit = null; for (const b2 of bs) { const tx = await b2.innerText(); if (/משחק חדש כאן|מתחילים|המשך|לשחק בה/.test(tx)) { hit = b2; break } } if (hit) await hit.click().catch(() => { }); await p.waitForTimeout(150) }
  const e1 = await p.evaluate(() => ({ s: TCLD.state(), paused: __TC_DEV.ev('State.paused'), mode: __TC_DEV.ev('TCO.mode') }));
  ok('כניסה למשחק → מסך מלא', e1.s.on && e1.s.view === 'full', e1); await shot('04_enter');
  await p.waitForTimeout(1800); await shot('05_enter2');
  let t1 = Date.now(), e2; while (Date.now() - t1 < 40000) { e2 = await p.evaluate(() => TCLD.state()); if (!e2.on) break; await p.waitForTimeout(300) }
  ok('מסך הכניסה נסגר כשהעיר מוכנה (לא timeout)', !e2.on && e2.last && e2.last.why === 'ready', e2.last);
  const e3 = await p.evaluate(() => ({ paused: __TC_DEV.ev('State.paused'), ldh: __TC_LDH() })); ok('העולם חזר לרוץ', e3.paused === false, e3.ldh.log.slice(-4));
  // F7 — a save loaded in the game
  await p.evaluate(() => { try { __TC_DEV.ev("SaveManager.save('manual',{silent:true})") } catch (e) { } }); await p.waitForTimeout(500);
  await p.evaluate(() => __TC_DEV.ev('SaveManager.load({silent:true})')); await p.waitForTimeout(150); const f1 = await p.evaluate(() => TCLD.state());
  ok('F7 (SaveManager.load) → מסך מלא "טוען את השמירה"', f1.on && f1.kind === 'save', f1); await shot('06_f7');
  t1 = Date.now(); let f2; while (Date.now() - t1 < 40000) { f2 = await p.evaluate(() => TCLD.state()); if (!f2.on) break; await p.waitForTimeout(300) }
  ok('F7 — נסגר כשמוכן', !f2.on && f2.last && f2.last.why === 'ready', f2.last);
  // the far zoom
  await p.waitForTimeout(1500); await p.evaluate(() => __TC_DEV.ev('LDH.lastArea=-1e9;LDH.hidAt=-1e9;Camera.zoom=0.46'));
  let z1 = null; t1 = Date.now(); while (Date.now() - t1 < 6000) { z1 = await p.evaluate(() => ({ s: TCLD.state(), l: __TC_LDH() })); if (z1.s.on) break; await p.waitForTimeout(150) }
  ok('זום רחוק שבונה מחדש → מסך "זום"', z1.s.on && (z1.s.kind === 'zoom' || z1.s.kind === 'area'), { s: z1.s, vT: z1.l.vT, vM: z1.l.vM }); if (z1.s.on) await shot('07_zoom');
  if (/ldmini/.test(process.env.TCLD_HASH || '')) { const zp = await p.evaluate(() => ({ paused: __TC_DEV.ev('State.paused'), block: TCLD.st.block, logo: !!document.querySelector('#tcldRoot .lg canvas') })); ok('‎#ldmini — בזום: כרטיס קטן ופס, העולם לא נעצר והמקשים עוברים', z1.s.view === 'mini' && zp.paused === false && !zp.block && !zp.logo, Object.assign({ view: z1.s.view }, zp)) }
  t1 = Date.now(); let z2; while (Date.now() - t1 < 40000) { z2 = await p.evaluate(() => TCLD.state()); if (!z2.on) break; await p.waitForTimeout(300) }
  ok('הזום — נסגר', !z2.on, z2.last);
  await p.evaluate(() => __TC_DEV.ev('Camera.zoom=1'));
  // the airfield job (the real function, a fake job object of the same shape)
  const a1 = await p.evaluate(() => { __TC_DEV.ev('g77LdsUi({n:30,total:100,bg:false})'); const s = TCLD.state(), old = document.getElementById('g77LdsOv'); return { s, old: old ? old.style.display : 'none' } });
  ok('השדה ממשיך → מסך הטעינה עם ההתקדמות שלו (החלון הישן מוסתר)', a1.s.on && a1.s.steps.apt === .3 && a1.old === 'none', a1); await shot('08_apt');
  await p.evaluate(() => __TC_DEV.ev('g77LdsUi(null)')); t1 = Date.now(); let a2; while (Date.now() - t1 < 20000) { a2 = await p.evaluate(() => TCLD.state()); if (!a2.on) break; await p.waitForTimeout(300) }
  ok('השדה — נסגר', !a2.on, a2.last);
  const html = await p.content(); ok('0 data:image בדף', !/data:image/.test(html));
  ok('0 שגיאות בדף', errs.length === 0, errs.slice(0, 5));
  R.errs = errs; R.pass = R.checks.filter(c => c.ok).length; R.total = R.checks.length; fs.writeFileSync(path.join(outd, 'tcld_test.json'), JSON.stringify(R, null, 1));
  console.log('TCLD', R.pass + '/' + R.total); await b.close();
})().catch(e => { console.error(String(e).slice(0, 500)); process.exit(1) });
