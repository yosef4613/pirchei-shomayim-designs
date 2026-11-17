// memcmp.js — perf 17.11: הזיכרון של הדף באותו כלי בדיוק כמו people_on_road (הממצא של merge2: על S7F300 — שיא של 2.96 ג"ב, OOM עם 8 דפדפנים).
// node memcmp.js <out.json> <a.html> [b.html …]   — דרך התור: bash W/tools_pack/bslot.sh node ...   משתנים: T=300 (שניות המשחק, כמו ברירת המחדל של people_on_road)
// לכל בנייה, אחת אחרי השנייה: Chromium כמו של people_on_road (swiftshader, ‏1920×1080, ‎#dev), ואותה שאילתה — נקראת מתוך qa_tools/people_on_road.js עצמו
// (לא עותק), ונוסף לה רק רישום הזיכרון בסוף כל מעבר ציור. מבחוץ — כל 2 שנ׳: ה-RSS (ו-RssAnon, מה שה-OOM סופר) של כל תהליך של הדפדפן הזה, לפי הסוג.
// בתוך הדף: בטעינה, בכל מעבר ציור ובסוף (לפני / אחרי gc): הערימה של JS, הקנבסים לפי הבעלים (__TC_CANVAS_MEM('by')), המטמונים (g77OtCaches), ההקלטות (TCVREC.st).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const W = '/home/user/tc_root/tc/pkg/work';
const src = fs.readFileSync(path.join(W, 'qa_tools/people_on_road.js'), 'utf8');
const qa = src.indexOf('const Q = `') + 11, qb = src.indexOf('`;\n  const R = JSON.parse');
if (qa < 11 || qb < 0) { console.error('people_on_road.js: לא נמצאה השאילתה'); process.exit(2) }
const QSRC = src.slice(qa, qb);
const SNAP = `(()=>{const o={};try{o.heapMB=+(performance.memory.usedJSHeapSize/1048576).toFixed(1);o.heapTotMB=+(performance.memory.totalJSHeapSize/1048576).toFixed(1)}catch(e){}
 try{const c=window.__TC_CANVAS_MEM('by');o.canvasMB=c.mb;o.canvases=c.live;o.by=c.by}catch(e){}try{o.caches=g77OtCaches()}catch(e){}
 try{const s=TCVREC.st;o.vrec={n:s.n,bytes:s.bytes,decoded:s.decoded,bufN:s.bufN,bufMB:+((s.bufBytes||0)/1048576).toFixed(1)}}catch(e){}
 try{o.wtc={tiles:WTC.tiles.size,pool:WTC.pool.length}}catch(e){}try{o.sbc={n:SBC.map.size,mb:Math.round(SBC.bytes/1048576)}}catch(e){}
 try{o.k34=KIT34.stats?KIT34.stats():null}catch(e){}try{o.dom=document.getElementsByTagName('*').length}catch(e){}return o})()`;
function procs(root) {   // the browser and every process under it (pid → ppid from /proc)
  const kids = {}; for (const d of fs.readdirSync('/proc')) { if (!/^\d+$/.test(d)) continue; try { const st = fs.readFileSync('/proc/' + d + '/stat', 'utf8'); const pp = +st.slice(st.lastIndexOf(')') + 2).split(' ')[1]; (kids[pp] = kids[pp] || []).push(+d) } catch (e) {} }
  const out = []; const q = [root]; while (q.length) { const p = q.shift(); out.push(p); for (const k of (kids[p] || [])) q.push(k) } return out;
}
function rss(root) {
  const r = { total: 0, anon: 0, by: {} };
  for (const p of procs(root)) { if (p === root) continue; try { const s = fs.readFileSync('/proc/' + p + '/status', 'utf8'), cl = fs.readFileSync('/proc/' + p + '/cmdline', 'utf8');
    const v = +((s.match(/VmRSS:\s+(\d+)/) || [])[1] || 0) / 1024, a = +((s.match(/RssAnon:\s+(\d+)/) || [])[1] || 0) / 1024; const t = (cl.match(/--type=([\w-]+)/) || [])[1] || (cl.includes('chrom') ? 'browser' : 'other');
    r.total += v; r.anon += a; const e = r.by[t] || (r.by[t] = { rss: 0, anon: 0, n: 0 }); e.rss += v; e.anon += a; e.n++ } catch (e) {} }
  r.total = Math.round(r.total); r.anon = Math.round(r.anon); for (const k in r.by) { r.by[k].rss = Math.round(r.by[k].rss); r.by[k].anon = Math.round(r.by[k].anon) } return r;
}
async function one(file, T) {
  const R = { build: path.basename(file), bytes: fs.statSync(file).size, T, rss: [], peak: { total: 0, anon: 0, renderer: 0, rendererAnon: 0, gpu: 0, at: null } };
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--enable-precise-memory-info', '--js-flags=--expose-gc'] });
  const root = process.pid, t0 = Date.now();   // the browser is a child of this node process (chromium.launch); everything under it, without node itself
  const tick = () => { const m = rss(root); m.s = Math.round((Date.now() - t0) / 1000); m.ph = R.ph; R.rss.push(m); const ren = m.by.renderer || { rss: 0, anon: 0 }, gpu = m.by['gpu-process'] || { rss: 0 };
    if (m.total > R.peak.total) { R.peak.total = m.total; R.peak.at = m.s + ' ' + R.ph } if (m.anon > R.peak.anon) R.peak.anon = m.anon; if (ren.rss > R.peak.renderer) R.peak.renderer = ren.rss; if (ren.anon > R.peak.rendererAnon) R.peak.rendererAnon = ren.anon; if (gpu.rss > R.peak.gpu) R.peak.gpu = gpu.rss };
  const iv = setInterval(tick, 2000);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
    R.ph = 'load'; await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
    R.readyS = Math.round((Date.now() - t0) / 1000);
    await p.waitForTimeout(3000); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(400) }
    const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
    tick(); R.atLoad = { rss: R.rss[R.rss.length - 1], page: JSON.parse(await ev('JSON.stringify(' + SNAP + ')')) };
    let Q = eval('`' + QSRC + '`');
    const k = 'Camera.x=cam0.x;Camera.y=cam0.y;Camera.zoom=cam0.zoom;State.mapQa=mq};';
    if (Q.indexOf(k) < 0) throw new Error('people_on_road: לא נמצא סוף המעבר');
    Q = Q.replace(k, k.slice(0, -2) + ';try{(out.mem||(out.mem=[])).push(Object.assign({s},' + SNAP + '))}catch(e){}};');
    R.ph = 'people'; const t1 = Date.now(); const P = JSON.parse(await ev(Q)); R.peopleS = Math.round((Date.now() - t1) / 1000);
    tick(); R.atEnd = { rss: R.rss[R.rss.length - 1], page: JSON.parse(await ev('JSON.stringify(' + SNAP + ')')) };
    await ev('(window.gc&&(gc(),gc()),1)'); await p.waitForTimeout(1500); tick(); R.afterGc = { rss: R.rss[R.rss.length - 1], page: JSON.parse(await ev('JSON.stringify(' + SNAP + ')')) };
    R.people = { ok: P.ok, samples: P.samples, sweeps: P.sweeps, views: P.views, people: P.people, drawn: P.drawn, hits: (P.hits || []).length, renderErr: P.renderErr || null };
    R.sweepMem = (P.mem || []).map(m => ({ s: m.s, heap: m.heapMB, canvas: m.canvasMB, canvases: m.canvases, by: m.by, caches: m.caches, vrec: m.vrec, sbc: m.sbc, wtc: m.wtc }));
    R.errs = errs.slice(0, 6);
  } catch (e) { R.err = String(e && e.stack || e).slice(0, 500) }
  finally { clearInterval(iv); R.wallS = Math.round((Date.now() - t0) / 1000); try { await b.close() } catch (e) {} }
  return R;
}
(async () => {
  const [out, ...files0] = process.argv.slice(2); const T = +(process.env.T || 300);
  let files = files0; try { if (fs.existsSync(out + '.also')) files = fs.readFileSync(out + '.also', 'utf8').split('\n').map(x => x.trim()).filter(Boolean).concat(files0) } catch (e) {}   // <out>.also — more builds first (one line each)
  if (!out || !files.length) { console.error('usage: node memcmp.js <out.json> <a.html> [b.html …]'); process.exit(2) }
  const all = [];
  for (const f of files) { console.log('== ' + path.basename(f) + ' · ' + new Date().toISOString()); const r = await one(f, T); all.push(r); fs.writeFileSync(out, JSON.stringify(all, null, 1));
    const L = r.atLoad && r.atLoad.page, E = r.atEnd && r.atEnd.page, G = r.afterGc && r.afterGc.page;
    console.log(JSON.stringify({ build: r.build, bytes: r.bytes, readyS: r.readyS, peopleS: r.peopleS, peak: r.peak, rssLoad: r.atLoad && r.atLoad.rss.total, rssEnd: r.atEnd && r.atEnd.rss.total, rssGc: r.afterGc && r.afterGc.rss.total,
      heap: [L && L.heapMB, E && E.heapMB, G && G.heapMB], canvas: [L && L.canvasMB, E && E.canvasMB, G && G.canvasMB], byEnd: E && E.by, vrecEnd: E && E.vrec, people: r.people, err: r.err || null })) }
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
