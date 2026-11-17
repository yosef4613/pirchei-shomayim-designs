// headshot.js <lab.html> <outDir> — closezoom: צילום פנימי של דף הניסוי (דף קטן, בלי המשחק; המתאם התיר מחוץ לתור): "עמידה מול המצלמה" והליכה, בזום 16,
// בשני גדלי ראש להשוואה, ומדידה של רוחב הראש בפיקסלים מתוך הקנבס.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 1500 }, deviceScaleFactor: 2 }); const errs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file)); await p.waitForTimeout(1500);
  const shoot = async (tag, k, mode) => {
    const r = await p.evaluate(([k, mode]) => { const L = window.__LAB; if (k) L.TCCZ.headK = k; L.P34.clear(); for (const c of L.cells) c.look = Object.assign({}, c.look); document.querySelector('button[data-m="' + mode + '"]').click(); return { headK: L.TCCZ.headK } }, [k, mode]);
    await p.waitForTimeout(1600);
    const cv = await p.$$('canvas'); const boxes = [];
    for (const i of [2, 5, 8]) boxes.push(await cv[i].boundingBox());
    for (let j = 0; j < 3; j++) { const bb = boxes[j]; await p.screenshot({ path: path.join(out, tag + '_' + j + '.png'), clip: { x: bb.x + bb.width * .25, y: bb.y, width: bb.width * .5, height: bb.height * .55 } }) }
    const w = await p.evaluate(() => { const L = window.__LAB, o = []; for (const i of [2, 5, 8]) { const c = L.cells[i].cv, g = c.getContext('2d'), W = c.width, H = c.height, d = g.getImageData(0, 0, W, H).data; let top = -1;
      const isFig = (x, y) => { const k = (y * W + x) * 4, r = d[k], gg = d[k + 1], bl = d[k + 2]; return !(r > 150 && gg > 140 && bl > 120 && Math.abs(r - gg) < 30) };
      for (let y = 0; y < H * .6 && top < 0; y++) for (let x = W * .35 | 0; x < W * .65; x++) if (isFig(x, y)) { top = y; break }
      const rows = []; for (let y = top; y < top + H * .2; y++) { let n = 0; for (let x = W * .3 | 0; x < W * .7; x++) if (isFig(x, y)) n++; rows.push(n) }
      o.push({ top, rows: rows.filter((_, i) => i % 6 === 0) }) } return o });
    return { tag, ...r, w };
  };
  const res = [];
  res.push(await shoot('front118', 1.18, 'front'));
  res.push(await shoot('front136', 1.36, 'front'));
  res.push(await shoot('walk136', 1.36, 'walk'));
  console.log(JSON.stringify({ res, errs })); await b.close();
})().catch(e => { console.error(e); process.exit(1) });
