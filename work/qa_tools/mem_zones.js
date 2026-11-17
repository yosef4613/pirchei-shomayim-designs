// 8.11 · mem_zones.js — הזיכרון לפי אזור (R-89, ‏K‑239). בונה הזיכרון, ענף mem.
// לכל בנייה, אחת אחרי השנייה באותה ריצה (דפדפן חדש לכל בנייה, אף פעם לא שניים יחד):
//   פתיחה → ניקוי זיכרון (gc) → מדידה; סיבוב בכל האזורים (80, או רק הבנויים) — אחרי כל אזור ניקוי ומדידה;
//   חזרה לנקודת הפתיחה → ניקוי → מדידה סופית ("אחרי סיבוב, אחרי ניקוי זיכרון" — המספר שהיעד של 140 מ״ב חל עליו).
// מה נמדד: ה-JS heap (performance.memory אחרי gc), הקנבסים החיים (מספר וגודל — רוחב × גובה × 4, לפי הפונקציה שיצרה אותם
//   ולפי האזור שבו נוצרו), התמונות, הזיכרון של תהליכי הדפדפן (PSS), והמטמונים של המשחק (WTC, ‏SBC, ‏C34 …).
//   המספר שהיעד (140 מ״ב, ‏K‑239) והתקציב חלים עליו: ה-JS heap אחרי ניקוי — "total" (כמו במדידה של הביקורת: 105 מ״ב בפתיחה של S7F265).
//   הקנבסים (שם "cv") והתמונות נמדדים לידו ומדווחים, אבל לא נכנסים ליעד — הם בזיכרון של הציור, מחוץ ל-heap; "all" = JS + קנבסים + תמונות.
// אופציות (משתני סביבה):
//   ZONES=all|built|A0,B3,…   (ברירת מחדל all — 80 האזורים של TC_GRID)
//   SEC=3                      שניות מינימום בכל אזור (ועד 9 שניות, עד שבניית האריחים נרגעת)
//   SAMPLE=1                   דגימה של ה-heap (HeapProfiler) מהפתיחה עד הסוף — מי הקצה את מה שנשאר
//   CENSUS=1                   ספירה של כל המבנים הגלובליים (Map, ‏Set, מערכים) בפתיחה ובסוף — מה גדל
//   PERF=1                     הזמן לפריים (חציון ואחוזון 90 של זמן ה-JS בכל פריים) בשישה מקומות קבועים ובנסיעה, באותו זום
//   BUDGET=<json>              בדיקת התקציב (qa_tools/mem_budget.json): נכשל כשהסך אחרי הסיבוב מעל היעד או כשאזור עובר את התקציב שלו
//   NAMES=<manifest.json>      מאיפה לקחת את השמות לספירה (ברירת מחדל: src_game_mem/manifest.json)
//   DIAG=1                     אבחון בלבד: לא מחכה לדפדפנים אחרים (המספרים לא נכנסים לדוח — רק מי מחזיק מה); מסומן בפלט diag:true
// לבד: לפני כל בנייה — מחכה עד שאין דפדפן אחר במכונה; בזמן המדידה — בודק כל 2 שניות, ורושם אם דפדפן זר הופיע (foreign).
// node qa_tools/mem_zones.js <out.json> <build1.html> [build2.html …]      יציאה 1 — התקציב נכשל.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const W = '/home/user/tc_root/tc/pkg/work';
const ENV = process.env, SEC = +(ENV.SEC || 3), ZSEL = ENV.ZONES || 'all';
const MB = b => +(b / 1048576).toFixed(1);
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ---- דפדפנים אחרים: כל תהליך chrome / headless_shell שאינו צאצא של הדפדפן שלנו
function procs() {
  const out = execSync('ps -eo pid=,ppid=,comm=', { encoding: 'utf8' }).trim().split('\n').map(l => l.trim().split(/\s+/));
  return out.map(([pid, ppid, comm]) => ({ pid: +pid, ppid: +ppid, comm: comm || '' }));
}
function treeOf(root, P) { const kids = new Map(); for (const p of P) { if (!kids.has(p.ppid)) kids.set(p.ppid, []); kids.get(p.ppid).push(p.pid) }
  const s = new Set(), q = [root]; while (q.length) { const x = q.pop(); if (s.has(x)) continue; s.add(x); for (const k of kids.get(x) || []) q.push(k) } return s }
function foreign(ourPid) { const P = procs(), mine = ourPid ? treeOf(ourPid, P) : new Set();
  return P.filter(p => /chrom|headless_shell/i.test(p.comm) && !mine.has(p.pid)).map(p => p.pid) }
async function waitAlone(tag) { if (ENV.DIAG) return 0; let n = 0; for (;;) { const f = foreign(process.pid); if (!f.length || n * 5 >= +(ENV.MAXWAIT_OPEN || 600)) { if (n) console.log('  לבד מ-' + new Date().toTimeString().slice(0, 8)); return n * 5 }
  if (n % 12 === 0) console.log('  ' + tag + ': דפדפן אחר רץ (' + f.length + ' תהליכים) — מחכה'); n++; await sleep(5000) } }
function pssMB(ourPid) { const P = procs(), mine = treeOf(ourPid, P); let tot = 0, max = 0;
  for (const pid of mine) { try { const t = fs.readFileSync('/proc/' + pid + '/smaps_rollup', 'utf8'); const m = t.match(/^Pss:\s+(\d+) kB/m); if (m) { const v = +m[1] / 1024; tot += v; if (v > max) max = v } } catch (e) {} }
  return { total: Math.round(tot), renderer: Math.round(max) } }

// ---- מה שנכנס לדף לפני הקוד של המשחק: רישום הקנבסים והתמונות, ומדידת הזמן של כל פריים
const INIT = () => {
  const reg = new Set(), imgs = new Set(); const M = window.__MZ = { reg, imgs, zone: 'open', ft: [], ftOn: false };
  const own = () => { const L = (new Error().stack || '').split('\n').slice(2); for (const l of L) { if (/__MZ|getContext|at new Image|INIT/.test(l)) continue; const m = l.match(/at (?:new )?([\w$.<>\[\] ]+?)? ?\(?(?:[^()]*?):(\d+):\d+\)?$/); if (m) return (m[1] || '(anon)').trim() + ':' + m[2] } return '?' };
  for (const C of [window.HTMLCanvasElement, window.OffscreenCanvas]) { if (!C || !C.prototype.getContext) continue; const g = C.prototype.getContext;
    C.prototype.getContext = function () { if (!this.__mzOwn) { this.__mzOwn = own(); this.__mzZone = M.zone; this.__mzKind = String(arguments[0]); reg.add(new WeakRef(this)) } return g.apply(this, arguments) } }
  const I0 = window.Image; window.Image = function (w, h) { const im = w === undefined ? new I0() : new I0(w, h); im.__mzOwn = own(); imgs.add(new WeakRef(im)); return im }; window.Image.prototype = I0.prototype;
  M.canvases = (top) => { const by = {}, byZ = {}, big = []; let b = 0, n = 0, gl = 0;
    for (const w of reg) { const c = w.deref(); if (!c) { reg.delete(w); continue } const s = (c.width | 0) * (c.height | 0) * 4; if (!s) continue; n++; b += s; if (/webgl/.test(c.__mzKind)) gl++;
      const k = c.__mzOwn, e = by[k] || (by[k] = { n: 0, b: 0 }); e.n++; e.b += s; const z = byZ[c.__mzZone] || (byZ[c.__mzZone] = { n: 0, b: 0 }); z.n++; z.b += s;
      if (s >= 1048576) big.push([k, c.width, c.height, c.__mzZone]) }
    const r = o => Object.entries(o).map(([k, v]) => [k, v.n, +(v.b / 1048576).toFixed(2)]).sort((a, b) => b[2] - a[2]);
    return { n, gl, mb: +(b / 1048576).toFixed(1), by: r(by).slice(0, top || 40), byZone: r(byZ), big: big.slice(0, 60) } };
  M.images = () => { let b = 0, n = 0; const seen = new Set(); const add = im => { if (seen.has(im)) return; seen.add(im); const s = (im.naturalWidth | 0) * (im.naturalHeight | 0) * 4; if (s) { n++; b += s } };
    for (const w of imgs) { const im = w.deref(); if (!im) { imgs.delete(w); continue } add(im) } for (const im of document.images) add(im); return { n, mb: +(b / 1048576).toFixed(1) } };
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) { return raf(function (t) { if (!M.ftOn) return cb(t); const t0 = performance.now(); try { return cb(t) } finally { M.ft.push(performance.now() - t0) } }) };
};

// ---- המטמונים של המשחק (כל אחד אם קיים בבנייה)
const CACHES = `(()=>{const o={},T=(k,f)=>{try{const v=f();if(v!==undefined)o[k]=v}catch(e){}};const mb=b=>+(b/1048576).toFixed(1);
 T('WTC',()=>({tiles:WTC.tiles.size,pool:WTC.pool.length,anim:WTC.anim.size,T:WTC.T,maxTiles:WTC.maxTiles,dpr:typeof dpr!=='undefined'?dpr:null}));
 T('SBC',()=>({n:SBC.map.size,mb:mb(SBC.bytes),budgetMB:mb(SBC.budget),fam:SBC.fam.size}));
 T('SBCT',()=>({n:SBCT.map.size,mb:mb(SBCT.bytes),str:SBCT.str.size}));
 T('ANIM',()=>({n:G77_ANIM.map.size,mb:mb(G77_ANIM.bytes)}));T('CROWD',()=>({n:G77_CROWD.map.size,mb:mb(G77_CROWD.bytes)}));T('G371',()=>({n:G371.map.size,mb:mb(G371.bytes)}));
 T('A34G',()=>({M:A34G.M.size,S:A34G.S.size,mb:mb(A34G.bytes||0)}));T('C34',()=>window.__TC_C34&&window.__TC_C34.stats().cache);
 T('EMPTY',()=>WTC_EMPTY.size);T('FWC',()=>G77_FWC.map.size);T('VB',()=>G77_VB.m.size);T('SIGN',()=>G7_SIGN.map.size);T('CAT',()=>G77_CAT.cache.size);
 T('SBCN',()=>SBCN.root.size);T('SBCL',()=>SBCL.fam.size);
 T('cam',()=>({x:Math.round(Camera.x),y:Math.round(Camera.y),z:+Camera.zoom.toFixed(3)}));T('night',()=>!!window.__TC_NIGHT);return o})()`;

// ---- ספירה של כל המבנים הגלובליים: לכל שם — כמה איברים יש בו (Map/Set/מערך, ועוד רמה אחת פנימה)
const CENSUS = names => `(()=>{const N=${JSON.stringify(names)},o={};const cnt=v=>{if(v instanceof Map||v instanceof Set)return v.size;if(Array.isArray(v))return v.length;if(ArrayBuffer.isView(v))return Math.round(v.byteLength/8);return 0};
 for(const k of N){let v;try{v=eval(k)}catch(e){continue}if(!v||typeof v!=='object')continue;let s=cnt(v);if(!(v instanceof Map||v instanceof Set||Array.isArray(v)||ArrayBuffer.isView(v))){let i=0;for(const q in v){if(++i>4000)break;let w;try{w=v[q]}catch(e){continue}if(w&&typeof w==='object')s+=cnt(w)}s+=i}
  else if(v instanceof Map){let i=0;for(const w of v.values()){if(++i>3000)break;if(w&&typeof w==='object')s+=cnt(w)}}
  if(s>0)o[k]=s}return o})()`;

const PLACES = [['E4', 5400, 2975], ['F3', 6600, 2125], ['F5', 6600, 3825], ['D4', 4200, 2975], ['C5', 3000, 3825], ['E3', 5400, 2125]];

async function one(file, opt) {
  const tag = (path.basename(file).match(/(S7F\d+|try\d+)/) || [path.basename(file)])[0];
  const waited = await waitAlone(tag);
  const t0 = Date.now();
  const browser = await chromium.launch({ args: ['--js-flags=--expose-gc', '--enable-precise-memory-info'] });
  const bpid = process.pid;   // הדפדפן הוא צאצא של התהליך הזה
  const page = await browser.newPage({ viewport: { width: 1920, height: 953 } });
  const errs = []; page.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  let foreignSeen = 0, pausedS = 0; const watch = setInterval(() => { try { if (foreign(bpid).length) foreignSeen++ } catch (e) {} }, 2000);
  // לבד: לפני כל מדידה — אם דפדפן זר רץ, מחכים (בדיקה כל 5 שניות) עד שהוא נגמר, ורק אז מודדים
  // ברירת מחדל (לאישורך): מדידת זיכרון מחכה עד MAXWAIT שניות (ברירת מחדל 90) לדפדפן אחר שייגמר, ואז מודדת ונרשמת כ"לא לבד" (notAlone);
  // הזמן לפריים — תמיד לבד (perf, ‏strict). שני סוכנים אחרים מריצים דפדפנים כמעט ברצף, והמדידה לא התקדמה בלי זה.
  let notAlone = 0; const MAXW = +(ENV.MAXWAIT || 90);
  const alone = async (strict) => { let n = 0; while (!ENV.DIAG && foreign(bpid).length) { if (!strict && n * 5 >= MAXW) { notAlone++; break } if (n % 12 === 0) console.log('  דפדפן אחר רץ — המדידה מחכה'); n++; await sleep(5000) } pausedS += n * 5; return n };
  await page.addInitScript(INIT);
  await page.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit', timeout: 240000 });
  await page.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await page.waitForTimeout(3000);
  for (let i = 0; i < 4; i++) { try { if (await page.evaluate(() => !!document.getElementById('g77AsChoose'))) await page.keyboard.press('Enter') } catch (e) {} await page.waitForTimeout(400) }
  const cdp = await page.context().newCDPSession(page);
  const ev = s => page.evaluate(s => window.__TC_DEV.ev(s), s), J = async s => JSON.parse(await ev('JSON.stringify(' + s + ')'));
  const gc = async () => { for (let i = 0; i < 3; i++) { await page.evaluate(() => { try { window.gc() } catch (e) {} }); await page.waitForTimeout(250) } };
  // שלוש דגימות (כל אחת אחרי ניקוי), ‏0.7 שנייה זו מזו — המספר הוא הקטנה שבהן: עבודה זמנית (תכנון של טיסה בשדה, תמונות שנוצרות
  // באותו רגע) לא נספרת כזיכרון שהאזור השאיר; הגדולה נשמרת ליד (jsMax) כדי לראות את הרעש
  const snap = async (label) => { await alone(); const S3 = []; for (let i = 0; i < (+ENV.SAMPLES || 3); i++) { if (i) await page.waitForTimeout(700); await gc(); S3.push(await page.evaluate(() => performance.memory.usedJSHeapSize)) }
    const js = Math.min(...S3), jsMax = Math.max(...S3); const hu = await cdp.send('Runtime.getHeapUsage');
    const cv = await page.evaluate(() => window.__MZ.canvases(40)), im = await page.evaluate(() => window.__MZ.images()), ca = await J(CACHES), ps = pssMB(bpid);
    return { label, js: MB(js), jsMax: MB(jsMax), heapUsed: MB(hu.usedSize), cv, img: im, total: MB(js), all: +(MB(js) + cv.mb + im.mb).toFixed(1), caches: ca, pss: ps, t: Math.round((Date.now() - t0) / 1000) } };
  const gameZoom = await page.evaluate(() => Math.min(Math.max(Math.min(innerWidth / 1150, innerHeight / 820), .62), 1.55));
  const ZOOM = ENV.ZOOM ? +ENV.ZOOM : gameZoom;
  const grid = await J(`(()=>{const C=TC_GRID.cols,R=TC_GRID.rows,L=window.__TC_LIVE||{zones:{}},A=typeof ACTIVE_REGIONS!=='undefined'?ACTIVE_REGIONS:[],z=[];
    const built=new Set(Object.keys(L.zones||{}));for(const r of A){const x=r.x+r.w/2,y=r.y+r.h/2;for(let i=0;i<C.length-1;i++)for(let j=0;j<R.length-1;j++)if(x>=C[i]&&x<C[i+1]&&y>=R[j]&&y<R[j+1])built.add('ABCDEFGH'[i]+j)}
    for(let j=0;j<R.length-1;j++)for(let i=0;i<C.length-1;i++){const k='ABCDEFGH'[i]+j;z.push({z:k,x:(C[i]+C[i+1])/2,y:(R[j]+R[j+1])/2,built:built.has(k),live:!!(L.zones||{})[k]})}return z})()`);
  let zones = grid; if (ZSEL === 'built') zones = grid.filter(z => z.built); else if (ZSEL !== 'all') { const S = new Set(ZSEL.split(',')); zones = grid.filter(z => S.has(z.z)) }
  const res = { file: path.resolve(file), tag, sha1: execSync('sha1sum ' + JSON.stringify(path.resolve(file))).toString().slice(0, 12), bytes: fs.statSync(file).size,
    viewport: [1920, 953], zoom: ZOOM, waitedAloneS: waited, zones: [], errors: errs, diag: !!ENV.DIAG };
  const start = await J(`({x:Camera.x,y:Camera.y,zoom:Camera.zoom})`);
  res.start = start;
  // הפתיחה נמדדת בזמן קבוע אחרי הטעינה (3 שניות), בלי לחכות באמצע: אם דפדפן זר רץ עכשיו — סוגרים, מחכים, ומתחילים מחדש
  if (!ENV.DIAG && foreign(bpid).length && (opt.retry || 0) < 3) { clearInterval(watch); await browser.close(); console.log('  ' + tag + ': דפדפן אחר נכנס בזמן הפתיחה — מתחילים מחדש (' + ((opt.retry || 0) + 1) + ')'); await sleep(5000); return one(file, { retry: (opt.retry || 0) + 1 }) }
  const openAlone = !foreign(bpid).length;
  res.open = await snap('open'); console.log(tag, 'פתיחה', JSON.stringify({ js: res.open.js, cv: res.open.cv.mb, n: res.open.cv.n, all: res.open.all, pss: res.open.pss.total }));
  let names = []; if (ENV.CENSUS) { try { const m = JSON.parse(fs.readFileSync(ENV.NAMES || path.join(W, 'src_game_mem', 'manifest.json'), 'utf8')); for (const p of m.parts) for (const d of (p.defines || [])) if (/^[A-Za-z_$][\w$]*$/.test(d)) names.push(d) } catch (e) {}
    res.census0 = await J(CENSUS(names)) }
  if (ENV.SAMPLE) { await cdp.send('HeapProfiler.enable'); await cdp.send('HeapProfiler.startSampling', { samplingInterval: 16384 }) }
  let prev = res.open;
  for (const z of zones) {
    await page.evaluate(k => { window.__MZ.zone = k }, z.z);
    await ev(`(window.__TC_DEV.cam({x:${z.x},y:${z.y},zoom:${ZOOM}}),1)`);
    const tz = Date.now(); let last = -1, still = 0;
    for (;;) { await page.waitForTimeout(500); const b = await ev(`WTC.stats.built+WTC.stats.prefetched`); if (b === last) still++; else still = 0; last = b;
      const el = (Date.now() - tz) / 1000; if ((el >= SEC && still >= 2) || el >= SEC + 6) break }
    const s = await snap(z.z); const d = k => +(s[k] - prev[k]).toFixed(1);
    const row = { z: z.z, built: z.built, live: z.live, js: s.js, jsMax: s.jsMax, cv: s.cv.mb, cvN: s.cv.n, img: s.img.mb, total: s.total, all: s.all, dJs: d('js'), dCv: +(s.cv.mb - prev.cv.mb).toFixed(1), dTotal: d('total'), dAll: d('all'), pss: s.pss.total, caches: s.caches };
    res.zones.push(row); prev = s;
    console.log(' ', z.z.padEnd(3), z.built ? 'בנוי' : '    ', 'JS', String(s.js).padStart(6), 'קנבס', String(s.cv.mb).padStart(6), '(' + s.cv.n + ')', 'Δ JS', (row.dJs >= 0 ? '+' : '') + row.dJs, 'Δ קנבס', (row.dCv >= 0 ? '+' : '') + row.dCv);
  }
  await page.evaluate(() => { window.__MZ.zone = 'back' });
  await ev(`(window.__TC_DEV.cam({x:${start.x},y:${start.y},zoom:${start.zoom}}),1)`); await page.waitForTimeout(SEC * 1000 + 1500);
  res.final = await snap('final');
  if (ENV.SAMPLE) { const pr = await cdp.send('HeapProfiler.getSamplingProfile'); await cdp.send('HeapProfiler.stopSampling'); res.sample = summarizeSampling(pr.profile) }
  if (ENV.CENSUS) res.census1 = await J(CENSUS(names));
  console.log(tag, 'אחרי סיבוב', JSON.stringify({ js: res.final.js, cv: res.final.cv.mb, n: res.final.cv.n, all: res.final.all, pss: res.final.pss.total }));
  if (ENV.PERF) res.perf = await perf(page, ev, ZOOM, bpid, alone);
  res.foreignSeen = foreignSeen; res.pausedS = pausedS; res.notAlone = notAlone; res.openAlone = openAlone; res.secs = Math.round((Date.now() - t0) / 1000);
  clearInterval(watch); await browser.close(); return res;
}

// הזמן לפריים: זמן ה-JS של כל קריאה ל-requestAnimationFrame — חציון ואחוזון 90, בשישה מקומות ובנסיעה בין E3 ל-F5
async function perf(page, ev, ZOOM, bpid, alone) {
  const out = { places: {}, foreign: 0, redone: 0 };
  const rec = async (ms) => { let a; for (let k = 0; k < 6; k++) { await alone(true); await page.evaluate(() => { window.__MZ.ft.length = 0; window.__MZ.ftOn = true }); let bad = 0;
      for (let t = 0; t < ms; t += 500) { await page.waitForTimeout(500); if (foreign(bpid).length) bad++ }
      a = await page.evaluate(() => { window.__MZ.ftOn = false; return window.__MZ.ft.slice() }); if (!bad) break; out.redone++ }
    a.sort((x, y) => x - y);
    const q = p => +(a[Math.min(a.length - 1, Math.floor(a.length * p))] || 0).toFixed(2); return { n: a.length, med: q(.5), p90: q(.9), max: +(a[a.length - 1] || 0).toFixed(1) } };
  for (const [k, x, y] of PLACES) { await ev(`(window.__TC_DEV.cam({x:${x},y:${y},zoom:${ZOOM}}),1)`); await page.waitForTimeout(4000); out.places[k] = await rec(6000) }
  // הנסיעה: המצלמה זזה ברצף מ-E3 דרך E4 ל-F5 ובחזרה (‏~120 יחידות בשנייה), כמו נהיגה — כאן נראית העלות של בנייה מחדש של מטמונים
  let a; for (let k = 0; k < 6; k++) { await ev(`(window.__TC_DEV.cam({x:5400,y:2125,zoom:${ZOOM}}),1)`); await page.waitForTimeout(3000); await alone(true);
    await page.evaluate(() => { window.__MZ.ft.length = 0; window.__MZ.ftOn = true }); let bad = 0;
    const steps = 160; for (let i = 0; i <= steps; i++) { const u = i / steps, v = u < .5 ? u * 2 : 2 - u * 2, x = 5400 + (6600 - 5400) * v, y = 2125 + (3825 - 2125) * v; await ev(`(Camera.x=${x},Camera.y=${y},1)`); await page.waitForTimeout(100); if (i % 5 === 0 && foreign(bpid).length) bad++ }
    a = await page.evaluate(() => { window.__MZ.ftOn = false; return window.__MZ.ft.slice() }); if (!bad) break; out.redone++ }
  a.sort((x, y) => x - y);
  const q = p => +(a[Math.min(a.length - 1, Math.floor(a.length * p))] || 0).toFixed(2); out.places.drive = { n: a.length, med: q(.5), p90: q(.9), max: +(a[a.length - 1] || 0).toFixed(1) };
  return out;
}

function summarizeSampling(profile) {
  const byF = new Map(), byTop = new Map(); let tot = 0;
  const walk = (n, stack) => { const cf = n.callFrame, k = (cf.functionName || '(anon)') + ':' + (cf.lineNumber + 1); const st = stack.concat([k]);
    if (n.selfSize) { tot += n.selfSize; byF.set(k, (byF.get(k) || 0) + n.selfSize);
      // the first frame from the game's own file, from the leaf up (not the anonymous wrappers)
      const top = [...st].reverse().find(s => !/^\(anon\):|^\(root\)|^\(program\)/.test(s)) || k; byTop.set(top, (byTop.get(top) || 0) + n.selfSize) }
    for (const c of n.children || []) walk(c, st) };
  walk(profile.head, []);
  const s = m => [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 40).map(([k, v]) => [k, MB(v)]);
  return { totalMB: MB(tot), self: s(byF), named: s(byTop) };
}

function budgetCheck(r, B) {
  const fails = [], fin = r.final.total, lim = B.totalMB || 140;
  if (fin > lim) fails.push('ה-JS heap אחרי הסיבוב ' + fin + ' מ״ב — מעל ' + lim);
  for (const z of r.zones) { const cap = (B.zones && B.zones[z.z] != null) ? B.zones[z.z] : (B.newZoneMB || 3); const add = z.dTotal;
    if (add > cap + (B.noiseMB || 0)) fails.push(z.z + ' מוסיף ' + add + ' מ״ב — התקציב ' + cap + (B.zones && B.zones[z.z] != null ? '' : ' (אזור חדש)')) }
  return { ok: !fails.length, fails, limitMB: lim };
}

(async () => {
  const [out, ...files] = process.argv.slice(2);
  if (!out || !files.length) { console.error('usage: node mem_zones.js <out.json> <build.html>...'); process.exit(2) }
  const all = { at: new Date().toISOString(), sec: SEC, zonesSel: ZSEL, runs: [] }; let bad = 0;
  for (const f of files) { const r = await one(f, {}); if (ENV.BUDGET) { r.budget = budgetCheck(r, JSON.parse(fs.readFileSync(ENV.BUDGET, 'utf8'))); if (!r.budget.ok) bad++;
      console.log(r.tag, 'התקציב', r.budget.ok ? 'עובר' : 'נכשל', r.budget.fails.slice(0, 8).join(' · ')) }
    all.runs.push(r); fs.writeFileSync(out, JSON.stringify(all, null, 1)) }
  console.log('\n| בנייה | JS בפתיחה | קנבסים בפתיחה | JS אחרי סיבוב (היעד 140) | קנבסים אחרי סיבוב | PSS אחרי סיבוב |');
  for (const r of all.runs) console.log('|', r.tag, '|', r.open.js, '|', r.open.cv.mb, '(' + r.open.cv.n + ')', '|', r.final.js, '|', r.final.cv.mb, '(' + r.final.cv.n + ')', '|', r.final.pss.total, '|');
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(3) });
