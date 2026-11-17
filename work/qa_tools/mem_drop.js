// 8.11 · mem_drop.js — אבחון בלבד (בונה הזיכרון): כמה JS heap וכמה קנבסים מחזיק כל מטמון אחרי סיבוב.
// פתיחה → סיבוב מהיר בכל האזורים (בלי ניקוי באמצע) → עצירה של לולאת הפריימים → ניקוי ומדידה → ריקון של מטמון אחד בכל פעם,
// ניקוי ומדידה אחרי כל אחד: ההפרש הוא מה שהמטמון החזיק. המשחק אחרי זה לא שמיש — רק למדידה. המספרים — לאבחון, לא לדוח.
// node qa_tools/mem_drop.js <build.html> <out.json> [sec=1.5]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const STEPS = [
  ['P34 — האנשים ב-3/4 (תמונות + גאומטריה)', "P34.clear()"],
  ['P34G — המנהל של האנשים', "(()=>{for(const k in P34G){const v=P34G[k];if(v instanceof Map||v instanceof Set)v.clear();else if(Array.isArray(v))v.length=0}})()"],
  ['A34 — המודלים של המטוסים', "(()=>{window.__A34ST=JSON.stringify(window.__TC_A34.stats());A34G.M.clear()})()"],
  ['A34 — התמונות המוכנות של המטוסים', "(()=>{A34G.S.clear();A34G.bytes=0})()"],
  ['C34 — הרכבים ב-3/4', "C34.clear()"],
  ['KIT34 — ערכת הרחוב', "KIT34.clear()"],
  ['K34C — רשת ערכת הרחוב', "(()=>{K34C.grid.clear();K34C.info.clear();K34C.need.clear();K34C.list.length=0})()"],
  ['PORT_CACHE — הנמל', "(()=>{for(const e of PORT_CACHE.values())try{e.cv.width=0}catch(x){}PORT_CACHE.clear()})()"],
  ['WTC — האריחים', "(()=>{wtcInvalidate();for(const c of WTC.pool)try{c.width=0}catch(x){}WTC.pool.length=0;WTC_EMPTY.clear();WTC.anim.clear()})()"],
  ['WTC — רשימות הציור החי והמטרות', "(()=>{WTC.sprites=[];WTC.sprites2=[];WTC.targets=[];WTC.xKey='';Targets.items=[];try{WTC_LPL.targets=null;WTC_LPL.xKey='';WTC_XL.targets=null;WTC_XL.xKey=''}catch(e){}})()"],
  ['SBC — ציורים קטנים כתמונות', "(()=>{for(const e of SBC.map.values())try{e.cv.width=0}catch(x){}SBC.map.clear();SBC.fam.clear();SBC.bytes=0;SBCN.root.clear();SBCN.fx.clear();SBCL.fam.clear()})()"],
  ['SBCT — מצבים', "(()=>{SBCT.map.clear();SBCT.str.clear();SBCT.streak.clear();SBCT.bytes=0})()"],
  ['G77_ANIM / CROWD / G371 — העצים והקהל', "(()=>{G77_ANIM.map.clear();G77_ANIM.bytes=0;G77_CROWD.map.clear();G77_CROWD.bytes=0;G371.map.clear();G371.bytes=0})()"],
  ['AO — תכנון התנועה בשדה', "(()=>{AO.B&&AO.B.clear&&AO.B.clear();AO.LOG&&(AO.LOG.length=0)})()"],
  ['S9 — הגרגרים ותיאורי הגגות', "(()=>{for(const k in S9_SPECK)delete S9_SPECK[k];S9_VIS.clear()})()"],
  ['Dbg — יומן', "(()=>{Dbg.events.length=0;Dbg.errors.length=0})()"],
  ['G79_IN / FL_YARD_X / D5TK / PG_STATE', "(()=>{G79_IN.clear();FL_YARD_X=null;try{PG_STATE.log.length=0;PG_STATE.byId.clear()}catch(e){}})()"],
];
const PLAN = [];
for (let j = 0; j < 10; j++) for (let i = 0; i < 8; i++) PLAN.push([600 + 1200 * i, [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750].slice(j, j + 2).reduce((a, b) => a + b) / 2]);
(async () => {
  const [file, out, secA] = process.argv.slice(2); const sec = +(secA || 1.5);
  const b = await chromium.launch({ args: ['--js-flags=--expose-gc', '--enable-precise-memory-info'] }); const p = await b.newPage({ viewport: { width: 1920, height: 953 } });
  await p.addInitScript(() => { const raf = window.requestAnimationFrame.bind(window); window.__STOP = false; window.requestAnimationFrame = cb => raf(t => { if (!window.__STOP) cb(t) });
    const reg = new Set(); window.__CV = reg; for (const C of [window.HTMLCanvasElement, window.OffscreenCanvas]) { if (!C) continue; const g = C.prototype.getContext; C.prototype.getContext = function () { if (!this.__r) { this.__r = 1; reg.add(new WeakRef(this)) } return g.apply(this, arguments) } } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit', timeout: 240000 });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(3000);
  for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(400) }
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const meas = async () => { for (let i = 0; i < 3; i++) { await p.evaluate(() => window.gc()); await p.waitForTimeout(200) }
    return p.evaluate(() => { let n = 0, bts = 0; for (const w of window.__CV) { const c = w.deref(); if (!c) continue; const s = c.width * c.height * 4; if (s) { n++; bts += s } } return { js: +(performance.memory.usedJSHeapSize / 1048576).toFixed(1), cv: +(bts / 1048576).toFixed(1), n } }) };
  const R = { file: path.resolve(file), open: await meas(), steps: [] };
  const z = await p.evaluate(() => Math.min(Math.max(Math.min(innerWidth / 1150, innerHeight / 820), .62), 1.55));
  if (process.env.STAY) { // אבחון של גדילה בזמן: המצלמה עומדת באזור אחד (ברירת מחדל C5), מדידה כל 30 שניות
    const [x, y] = (process.env.AT || '3000,3825').split(',').map(Number); await ev(`(window.__TC_DEV.cam({x:${x},y:${y},zoom:${z}}),1)`); R.stay = [];
    for (let t = 0; t < +process.env.STAY; t += 30) { await p.waitForTimeout(30000); const q = await meas(); const ao = await ev('JSON.stringify({B:AO.B.size,n:(()=>{let n=0;for(const b of AO.B.values())n+=b.length;return n})(),fl:AO.flights.length,clk:Math.round(APT_OPS.clk)})'); R.stay.push([t + 30, q.js, q.cv, ao]); console.log('  ', t + 30, 'ש׳', 'JS', q.js, 'קנבס', q.cv, ao) } }
  else for (const [x, y] of PLAN) { await ev(`(window.__TC_DEV.cam({x:${x},y:${y},zoom:${z}}),1)`); await p.waitForTimeout(sec * 1000) }
  await p.waitForTimeout(1500); await p.evaluate(() => { window.__STOP = true }); await p.waitForTimeout(500);
  R.after = await meas(); let prev = R.after; console.log('פתיחה', JSON.stringify(R.open), 'אחרי סיבוב', JSON.stringify(R.after));
  for (const [name, code] of STEPS) { let err = null; try { await ev(code) } catch (e) { err = String(e).slice(0, 120) } const m = await meas();
    const row = { name, js: m.js, cv: m.cv, dJs: +(prev.js - m.js).toFixed(1), dCv: +(prev.cv - m.cv).toFixed(1), err }; R.steps.push(row); prev = m;
    console.log(name.padEnd(42), 'JS', String(row.dJs).padStart(6), 'קנבס', String(row.dCv).padStart(6), err ? 'שגיאה: ' + err : '') }
  R.a34 = await p.evaluate(() => window.__A34ST || null); console.log('A34', R.a34); R.left = prev; fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log('נשאר', JSON.stringify(prev)); await b.close();
})().catch(e => { console.error(e); process.exit(1) });
