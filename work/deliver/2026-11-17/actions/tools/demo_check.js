// בדיקת ההדגמה לבעלים: פותחים את המשחק עם ‎#dev&sact=<סיפור>:<שלב>‎ ובודקים שהשחקן במקום והמסך של המקום פתוח עם הכפתור "← במשחק"
// node demo_check.js <game.html> <out.json> [shots_dir]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2); const R = { cases: [] };
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  for (const tag of ['S12-ST-C1:2', 'S9-ST-E5:1']) {
    const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 200)));
    await p.goto('file://' + path.resolve(file) + '#dev&sact=' + tag, { waitUntil: 'commit' });
    await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
    await p.waitForTimeout(4000);
    const r = await p.evaluate(() => window.__TC_DEV.ev(`({demo:__TC_SACT.E.demo||null,phone:!!State.phoneOpen,btn:(document.querySelector('[data-s9-step]')||{}).innerText||null})`));
    r.tag = tag; r.pe = pe; r.ok = !!(r.demo && r.demo.opened && r.phone && r.btn && /במשחק/.test(r.btn)) && !pe.length;
    if (shots) await p.screenshot({ path: path.join(shots, 'demo_' + tag.replace(':', '_') + '.png') });
    R.cases.push(r); await p.close();
  }
  R.ok = R.cases.every(c => c.ok); fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify(R)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
