// בדיקה קצרה: טוען ניסיון, מחכה ל-ready, ומריץ ביטויים מקובץ (שורה לכל ביטוי). node probe.js <build> <exprs.txt> [waitSec]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, exf, waitS] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  console.log('ready', ((Date.now() - t0) / 1000).toFixed(1), 's');
  if (+waitS) await p.waitForTimeout(+waitS * 1000);
  for (const line of fs.readFileSync(exf, 'utf8').split('\n')) { if (!line.trim() || line.startsWith('#')) continue;
    if (line.startsWith('@wait ')) { await p.waitForTimeout(+line.slice(6) * 1000); continue }
    let r; try { r = await p.evaluate(x => { try { const v = window.__TC_DEV.ev(x); return JSON.stringify(v) } catch (e) { return 'ERR ' + e.message } }, line) } catch (e) { r = 'EVALERR ' + e.message }
    console.log('>> ' + line.slice(0, 120) + '\n' + String(r).slice(0, 3000)) }
  console.log('pageerrors', JSON.stringify(pe));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
