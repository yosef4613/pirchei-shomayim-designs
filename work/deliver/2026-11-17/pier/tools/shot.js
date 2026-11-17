// צילום לבדיקה בעין בלבד (לא לדפים): node shot.js <build> <outdir> "<שם>|x|y|zoom[|ביטוי לפני[|המתנה במ״ש]]" ...
// כל צילום: מציב את המצלמה (מצב מפה, בלי לעקוב אחרי השחקן), ממתין, ושומר PNG. הביטוי רץ ב-__TC_DEV.ev לפני הצילום.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, outdir, ...shots] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => { try { return window.__TC_DEV.ev(x) } catch (e) { return 'ERR ' + e } }, s);
  await p.waitForTimeout(1500);
  for (const s of shots) {
    const [name, x, y, z, pre, wait] = s.split('|');
    if (pre) { const r = await ev(pre); if (r !== undefined && r !== null) console.log(name, 'pre →', typeof r === 'string' ? r.slice(0, 600) : JSON.stringify(r).slice(0, 600)) }
    if (x !== '' && x != null && x !== '-') await ev(`(()=>{State.mapQa=true;Camera.x=${+x};Camera.y=${+y};Camera.zoom=${+z || 1};return 1})()`);
    await p.waitForTimeout(+wait || 1200);
    await p.screenshot({ path: path.join(outdir, name + '.png') });
    console.log('shot', name);
  }
  console.log(JSON.stringify({ pageErrors: pe }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
