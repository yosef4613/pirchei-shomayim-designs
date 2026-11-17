// ng_observe.js — סוכן newgame (17.11): משחק חדש כמו שחקן אמיתי — מסך הפתיחה ← "משחק חדש" ← מקום 1 ← שם ← "סיפור" ← מתחילים, ואז צפייה.
// node ng_observe.js <build.html> <hash|-> <out.json> [שניות=90] [mode=story|open]
//   hash '-' = בלי hash (משחק רגיל לגמרי). navigator.webdriver מוסתר (כמו דפדפן של שחקן).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, hash0, out, secS, mode0] = process.argv.slice(2); const hash = hash0 === '-' ? '' : hash0, SEC = +(secS || 90), MODE = mode0 || 'story';
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  await ctx.addInitScript(() => { try { Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true }) } catch (e) { } });
  const p = await ctx.newPage(); const errs = [], cons = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') cons.push(m.text().slice(0, 200)) });
  const t0 = Date.now(); const R = { file: path.basename(file), hash, mode: MODE, steps: [], samples: [] }; const log = s => { R.steps.push(Math.round((Date.now() - t0) / 1000) + 's ' + s); console.error(R.steps[R.steps.length - 1]) };
  await p.goto('file://' + path.resolve(file) + (hash ? '#' + hash : ''), { waitUntil: 'commit' });
  // מחכים שכפתור "משחק חדש" יהיה פעיל (TCO.mode==='open')
  await p.waitForFunction(() => { const x = document.querySelector('#tcoRoot [data-act="new"]'); return x && !x.disabled }, null, { timeout: 600000, polling: 1000 });
  log('מסך הפתיחה מוכן');
  await p.waitForTimeout(1500);
  await p.click('#tcoRoot [data-act="new"]'); await p.waitForTimeout(1200);
  const slotBtn = await p.$('#tcoRoot [data-tcs="new:1"]'); if (slotBtn) { await slotBtn.click(); log('מקום 1') } else log('אין כפתור מקום 1');
  await p.waitForTimeout(800);
  if (await p.$('#tcsName')) { await p.fill('#tcsName', 'דני'); if (MODE === 'open') await p.click('#tcoRoot [data-tcs="mode:open"]'); await p.waitForTimeout(300); await p.click('#tcoRoot [data-tcs="start:1"]'); log('מתחילים · ' + MODE) }
  // מחכים למשחק (אחרי טעינה מחדש אם צריך)
  await p.waitForFunction(() => !document.body.classList.contains('tco-open') && window.__TC_STORY, null, { timeout: 600000, polling: 1000 });
  log('בתוך המשחק');
  const snap = async () => p.evaluate(() => {
    const o = {}; try { o.story = window.__TC_STORY.state() } catch (e) { o.story = 'err ' + e }
    try { o.cur = window.__TC_STORY.cur(); if (o.cur) o.cur = { mi: o.cur.mi, step: o.cur.step, text: o.cur.s && o.cur.s.text } } catch (e) { }
    try { const S = window.__TC_S9STORY; o.zoneStarted = Object.keys(S.ST).filter(id => S.step(id) > 0 || S.done(id)) } catch (e) { o.zoneStarted = 'err' }
    try { o.nm = window.__G77NM ? { open: window.__G77NM.open } : null } catch (e) { }
    try { const h = document.getElementById('tcStHud'); o.hud = h && h.style.display !== 'none' ? h.textContent.slice(0, 160) : '' } catch (e) { }
    try { const t = document.getElementById('toast'); o.toast = t ? t.textContent.slice(0, 120) : '' } catch (e) { }
    try { const t = document.getElementById('tcTut'); o.tut = t && t.style.display !== 'none' ? t.textContent.slice(0, 200) : '' } catch (e) { }
    try { if (window.__TC_TUT) o.tutState = window.__TC_TUT.state() } catch (e) { }
    try { if (window.__TC_DEV) o.dev = window.__TC_DEV.ev("({msgs:g77St().msgs.length,lastMsgs:g77St().msgs.slice(-4).map(m=>m.who+': '+String(m.text).slice(0,50)),name:g77St().name,nameAsked:g77St().nameAsked,mode:PlayerProfile.mode,chunk:currentActorChunk(),nav:State.navigation&&State.navigation.targetId||null,am:PlayerProfile.activeMission&&PlayerProfile.activeMission.id||null,clock:gameClock().hour+':'+gameClock().minute,phone:State.phoneOpen,map:State.mapOpen,tsave:TCSAVE.mode()})") } catch (e) { o.dev = 'err ' + e }
    return o });
  const end = Date.now() + SEC * 1000; let i = 0;
  while (Date.now() < end) { const s = await snap(); s.t = Math.round((Date.now() - t0) / 1000); R.samples.push(s); if (i++ % 3 === 0) console.error(JSON.stringify(s).slice(0, 400)); await p.waitForTimeout(5000) }
  await p.screenshot({ path: out.replace(/\.json$/, '.png') });
  R.errs = errs; R.cons = cons.slice(0, 20); R.last = R.samples[R.samples.length - 1];
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.error('שגיאות דף: ' + errs.length + (errs.length ? ' · ' + errs.slice(0, 3).join(' | ') : ''));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
