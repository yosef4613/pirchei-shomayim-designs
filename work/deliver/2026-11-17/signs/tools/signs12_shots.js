// signs12_shots.js <game.html> <outdir> <id,id,...> — צילומי מסך לבדיקה פנימית בלבד (לא לדפים): השחקן ליד כל מקום, ביום ובלילה.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outd, ids] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(3000);
  for (const id of ids.split(',')) {
    const r = await p.evaluate(id => window.__TC_DEV.ev(`(()=>{const q=navPoiRegistry()[${JSON.stringify(id)}];if(!q)return 'none';try{setPhoneOpen(false)}catch(e){}PlayerProfile.mode='walk';PlayerPed.x=q.x;PlayerPed.y=q.y+40;return q.label})()`), id);
    await p.waitForTimeout(2500); await p.screenshot({ path: path.join(outd, id + '.png') }); console.log(id, r);
  }
  const st = await p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify(__TC_SIGNS12.stats())`)); console.log(st, 'errs', errs.length, errs.slice(0, 3).join(' | '));
  await b.close();
})().catch(e => { console.error(e); process.exit(2) });
