// tb_test.js <game.html> <outdir> — מסך הטעינה מול TCBUSY של missions (סדר השכבות): על ניסיון מיזוג שיש בו 009_tcbusy
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [f, outd] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true }); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  const R = { checks: [] }, ok = (n, c, d) => { R.checks.push({ n, ok: !!c, d }); console.log((c ? 'ok   ' : 'FAIL ') + n + (d !== undefined ? ' · ' + JSON.stringify(d).slice(0, 400) : '')) };
  const ev = s => p.evaluate(s => __TC_DEV.ev(s), s);
  await p.goto('file://' + path.resolve(f) + '#dev&opening&loading', { waitUntil: 'commit' });
  await p.waitForSelector('#tcldRoot.on', { timeout: 60000 });
  const b0 = await p.evaluate(() => ({ has: typeof TCBUSY !== 'undefined', st: typeof TCBUSY !== 'undefined' ? TCBUSY.state() : null, ld: TCLD.state().view }));
  ok('TCBUSY קיים; מסך הטעינה (boot) — השכבה העליונה "loading"', b0.has && b0.st.top === 'loading' && b0.st.n.set >= 1, b0);
  let T0 = Date.now(), m = '';
  while (Date.now() - T0 < 240000) { m = await ev('TCO.mode').catch(() => ''); if (m === 'open') break; await p.waitForTimeout(500) }
  const b1 = await p.evaluate(() => ({ top: TCBUSY.top(), blkCard: TCBUSY.blocks('card'), ld: TCLD.state().view }));
  ok('מסך הפתיחה — "loading" חוסם כרטיס', m === 'open' && b1.top === 'loading' && b1.blkCard, b1);
  // into the game
  // (the primary button, then whatever confirms; a film that starts — Esc; then until the loading screen is down)
  await p.screenshot({ path: path.join(outd, 'home.png'), timeout: 20000 }).catch(() => { });
  const btns = await p.evaluate(() => [...document.querySelectorAll('#tcoRoot button, #tcoRoot .tcoBtn')].map(b => (b.className + ' | ' + b.innerText).slice(0, 80))); R.btns = btns;
  T0 = Date.now(); let g = null, clicks = 0;
  while (Date.now() - T0 < 150000) {
    g = await p.evaluate(() => ({ mode: __TC_DEV.ev('TCO.mode'), ld: TCLD.state().on, show: !!__TC_DEV.ev('typeof TCSHOW!=="undefined"&&TCSHOW.on') })).catch(() => null);
    if (!g) { await p.waitForTimeout(500); continue }
    if (g.show) { await p.keyboard.press('Escape'); await p.waitForTimeout(600); continue }
    if (g.mode === 'game') { if (!g.ld) break; await p.waitForTimeout(500); continue }
    if (g.mode === 'open' && clicks < 12) { clicks++; const bs = await p.$$('#tcoRoot .tcoBtn:not([disabled])'); let hit = null; for (const b2 of bs) { const tx = await b2.innerText().catch(() => ''); if (/משחק חדש כאן|מתחילים|המשך|לשחק בה|משחק חדש/.test(tx)) { hit = b2; break } } if (hit) await hit.click().catch(() => { }); else await p.click('#tcoRoot .tcoBtn.pri:not([disabled])', { timeout: 3000 }).catch(() => { }) }
    await p.waitForTimeout(700) }
  R.enter = { g, clicks }; await p.screenshot({ path: path.join(outd, 'entered.png'), timeout: 20000 }).catch(() => { });
  await p.waitForTimeout(1500);
  const g1 = await p.evaluate(() => ({ mode: __TC_DEV.ev('TCO.mode'), ld: TCLD.state(), busy: TCBUSY.state() }));
  ok('במשחק, מסך הטעינה סגור — "loading" לא על המסך', g1.mode === 'game' && !g1.ld.on && g1.busy.on.indexOf('loading') < 0, { mode: g1.mode, last: g1.ld.last, busy: g1.busy });
  // F7: the full screen → loading on top; a card that waits (TCBUSY.when) comes right when the screen goes down (the clear, not the 250 ms poll)
  await p.evaluate(() => { try { __TC_DEV.ev("SaveManager.save('manual',{silent:true})") } catch (e) { } }); await p.waitForTimeout(500);
  await p.evaluate(() => { __TC_DEV.ev('SaveManager.load({silent:true})'); window.__tbW = { at: 0 }; window.__tbW.now = TCBUSY.when('card', () => { window.__tbW.at = performance.now(); window.__tbW.ld = TCLD.state().on }) });
  const f1 = await p.evaluate(() => ({ ld: TCLD.state(), top: TCBUSY.top(), sets: TCBUSY.state().n.set, w: window.__tbW }));
  ok('F7 → מסך מלא, "loading" למעלה, כרטיס מחכה', f1.ld.on && f1.ld.view === 'full' && f1.top === 'loading' && f1.w.now === false, f1);
  T0 = Date.now(); let f2; while (Date.now() - T0 < 40000) { f2 = await p.evaluate(() => ({ ld: TCLD.state(), w: window.__tbW, t: performance.now() })); if (!f2.ld.on && f2.w.at) break; await p.waitForTimeout(100) }
  const f3 = await p.evaluate(() => ({ hidAt: (TCLD.st.shows, null), last: TCLD.state().last, w: window.__tbW, busy: TCBUSY.state() }));
  ok('המסך ירד → הכרטיס שחיכה עולה (מסך הטעינה כבר לא על המסך)', !f2.ld.on && f3.w.at > 0 && f3.w.ld === false && f3.busy.on.indexOf('loading') < 0, f3);
  // a scene / a film on top: the far zoom does not open the full screen under it
  await p.evaluate(() => { TCBUSY.set('cutscene', { why: 'tb_test', ttl: 20000 }); __TC_DEV.ev('LDH.lastArea=-1e9;LDH.hidAt=-1e9;Camera.zoom=0.46') });
  let z1 = null; T0 = Date.now(); while (Date.now() - T0 < 5000) { z1 = await p.evaluate(() => TCLD.state()); if (z1.on) break; await p.waitForTimeout(150) }
  ok('סצנה על המסך (TCBUSY cutscene) → הזום הרחוק לא פותח מסך טעינה', !z1.on, z1.last);
  // the tiles of 0.46 were built during the scene (no screen needed) — back to 1, then a zoom farther than before, with no scene
  await p.evaluate(() => { TCBUSY.clear('cutscene'); __TC_DEV.ev('Camera.zoom=1') }); await p.waitForTimeout(2500);
  await p.evaluate(() => __TC_DEV.ev('LDH.lastArea=-1e9;LDH.hidAt=-1e9;LDH.bad.clear();Camera.zoom=0.34'));
  T0 = Date.now(); while (Date.now() - T0 < 6000) { z1 = await p.evaluate(() => TCLD.state()); if (z1.on) break; await p.waitForTimeout(150) }
  ok('הסצנה ירדה → הזום הרחוק שבונה — המסך עולה (כמו קודם)', z1.on && (z1.kind === 'zoom' || z1.kind === 'area'), { kind: z1.kind, view: z1.view, line: z1.line });
  T0 = Date.now(); while (Date.now() - T0 < 40000) { z1 = await p.evaluate(() => TCLD.state()); if (!z1.on) break; await p.waitForTimeout(300) }
  await p.evaluate(() => __TC_DEV.ev('Camera.zoom=1'));
  const e = await p.evaluate(() => TCBUSY.state()); ok('TCBUSY בלי שגיאות', !e.err && e.n.err === 0, e);
  ok('0 שגיאות בדף', errs.length === 0, errs.slice(0, 5));
  R.pass = R.checks.filter(c => c.ok).length; R.total = R.checks.length; fs.writeFileSync(path.join(outd, 'tb_test.json'), JSON.stringify(R, null, 1));
  console.log('TB', R.pass + '/' + R.total); await b.close();
})().catch(e => { console.error(String(e).slice(0, 500)); process.exit(1) });
