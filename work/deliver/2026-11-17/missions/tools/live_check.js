// live_check.js — הדף החי: נטען, הכפתורים עובדים, הספירה מתעדכנת, 0 שגיאות. node live_check.js <live.html> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file), { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500); const o = { hash: await p.evaluate(() => location.hash) };
  const click = async t => { const h = await p.$$('#mbBtns button'); for (const x of h) { if ((await x.textContent()).startsWith(t)) { await x.click(); return true } } return false };
  o.b1 = await click('להפעיל'); await p.waitForTimeout(2500); o.cnt1 = await p.textContent('#mbCnt');
  o.b2 = await click('הסיפור'); await p.waitForTimeout(3000); o.cnt2 = await p.textContent('#mbCnt');
  o.b3 = await click('להשלים'); await p.waitForTimeout(2500); o.cnt3 = await p.textContent('#mbCnt');
  o.b4 = await click('הצעה'); await p.waitForTimeout(2500); o.cnt4 = await p.textContent('#mbCnt');
  o.b5 = await click('הטלפון · יומן'); await p.waitForTimeout(1000); o.jr = (await p.textContent('#phoneBody')).slice(0, 200);
  o.card = await p.evaluate(() => { const d = document.getElementById('tcMbCard'); return d ? d.style.display : 'none' });
  await click('סגירה'); await p.waitForTimeout(800);
  const cv = () => p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify({playing:TCCUT.playing(),card:!!__TC_MB.E.card,q:__TC_MB.E.cardQ.length,vis:(()=>{const d=document.getElementById('tcMbCard');return d?getComputedStyle(d).visibility+'/'+d.style.display:'-'})()})`));
  o.b6 = await click('סצנה'); await p.waitForTimeout(1500); o.cutOn = await cv();
  await p.evaluate(() => window.__TC_DEV.ev('TCCUT.end()')); await p.waitForTimeout(3000); o.cutOff = await cv();
  o.b7 = await click('שכבה גבוהה'); await p.waitForTimeout(2000); o.busyOn = await cv(); o.cntBusy = await p.textContent('#mbCnt');
  await p.waitForTimeout(10500); o.busyOff = await cv(); o.cntFree = await p.textContent('#mbCnt');
  o.b8 = await click('סוף מה שנבנה'); await p.waitForTimeout(2500); o.cntEnd = await p.textContent('#mbCnt');
  o.errs = errs; const J = x => { try { return JSON.parse(x) } catch (e) { return {} } }, c1 = J(o.cutOn), c2 = J(o.cutOff), u1 = J(o.busyOn), u2 = J(o.busyOff);
  o.ok = !errs.length && /סיפור [123] \/ 3 · משימות צד [4-6] \/ 6/.test(o.cnt4) && c1.playing && !/^visible\/block/.test(c1.vis || '') && !c2.playing && c2.card && c2.vis === 'visible/block' && !/^visible\/block/.test(u1.vis || '') && u2.card && u2.vis === 'visible/block' && /שכבה: event/.test(o.cntBusy || '') && /שכבה: (—|card)/.test(o.cntFree || '') && /סיפור 1 \/ 3/.test(o.cntEnd || '') && /משימת ההמשך/.test(o.cntEnd || '');
  fs.writeFileSync(out, JSON.stringify(o, null, 1)); console.log(JSON.stringify(o)); await b.close(); process.exit(o.ok ? 0 : 2)
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
