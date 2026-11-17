// 8.11 · vis_mem.js — הבדיקה בעין של שינויי הזיכרון (ענף mem): אותו מקום, אותו זום, ביום ובלילה — לפני ואחרי.
// המשחק נפתח במצב הדטרמיניסטי (#qa-freeze: שעון קבוע, Math.random עם זרע, בלי לולאת פריימים), והפריים מצויר ביד (render) עם תקציב
// בלי גבול לאריחים — כך שתי בניות שמציירות אותו דבר נותנות אותם פיקסלים. הסדר: כל המקומות פעם אחת, ואחר כך שוב, אחרי סיבוב
// ברחבי העיר (כדי שמטמון שהשתחרר ונבנה מחדש ייבדק גם הוא). נשמר PNG של הקנבס של המשחק לכל צילום (לעין של הבונה, לא לדפים).
// node qa_tools/vis_mem.js <out_dir> <tag> <build.html>     ואחר כך: python3 qa_tools/vis_mem_cmp.py <dirA> <dirB>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const PLACES = [['E4', 5400, 2975, 1.162], ['F3', 6600, 2125, 1.162], ['F4', 6600, 2975, 1.162], ['F5', 6600, 3825, 1.162], ['E5', 5400, 3825, 1.162], ['F6', 6600, 4725, 1.162],
  ['D4', 4200, 2975, 1.162], ['C5', 3000, 3825, 1.162], ['E3', 5400, 2125, 1.162], ['A4', 600, 2975, 1.162], ['E4z', 5400, 2975, 2.4], ['F3z', 6650, 2050, 2.4], ['E4far', 5400, 2975, .5], ['D2', 4200, 1275, 1.162]];
const TOUR = [[600, 425], [3000, 425], [6600, 425], [8400, 2975], [3000, 5625], [600, 7325], [6600, 7325], [4200, 5625]];
(async () => {
  const [out, tag, file] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 953 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  // גם השעון של Date קבוע (האורות והחלונות בלילה תלויים בו), ולפני כל צילום Math.random מתחיל מאותו זרע
  await p.addInitScript(() => { const D0 = Date, T = D0.UTC(2026, 10, 8, 10, 0, 0); class FD extends D0 { constructor(...a) { if (!a.length) super(T); else super(...a) } static now() { return T } }
    window.Date = FD; window.__visSeed = r => { let s = r >>> 0; Math.random = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296 } } });
  await p.goto('file://' + path.resolve(file) + '#qa-freeze&clock=100000&rng=7&dev', { waitUntil: 'commit', timeout: 240000 });
  await p.waitForFunction(() => window.__TC_DEV && typeof window.__TC_DEV.ev === 'function', null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  await ev(`(()=>{WTC.budgetMs=1e9;FS.budgetMs=1e9;try{FS.sbcMaxMs=1e9;FS.famMaxMs=1e9}catch(e){}return 1})()`);
  const shot = async (name, x, y, z, night) => {
    const url = await ev(`(()=>{window.__TC_NIGHT=${night};perfCamera({x:${x},y:${y},zoom:${z}});const now=performance.now();for(let i=0;i<59;i++)render(now);window.__visSeed(4242);render(now);return GAME_CTX.canvas.toDataURL('image/png')})()`);
    fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(url.split(',')[1], 'base64')) };
  const log = [];
  for (const round of [1, 2]) {
    // יום ואחר כך לילה, כל אחד במעבר משלו: אחרי ההחלפה — ביטול האריחים (המפתח שלהם לא כולל את הלילה), כמו בשני הצדדים
    for (const n of [0, 1]) { await ev(`(()=>{window.__TC_NIGHT=${n};wtcInvalidate();return 1})()`);
      for (const [k, x, y, z] of PLACES) { await shot(`r${round}_${k}_${n ? 'night' : 'day'}`, x, y, z, n); log.push([round, k, n]) } }
    if (round === 1) for (const [x, y] of TOUR) await ev(`(()=>{perfCamera({x:${x},y:${y},zoom:1.162});const now=performance.now();for(let i=0;i<30;i++)render(now);return 1})()`);
  }
  fs.writeFileSync(path.join(out, 'run.json'), JSON.stringify({ tag, file: path.resolve(file), shots: log.length, errors: errs }, null, 1));
  console.log(tag, 'צילומים', log.length, 'שגיאות', errs.length, errs.slice(0, 3).join(' | ')); await b.close();
})().catch(e => { console.error(e); process.exit(1) });
