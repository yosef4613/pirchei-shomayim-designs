// node ev.js <build> <expr-file> [waitSec] — opens the build with #dev, waits ready (+waitSec), evaluates the expression file in the page, prints JSON
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, exprFile, wait] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  if (+wait) await p.waitForTimeout(+wait * 1000);
  const src = fs.readFileSync(exprFile, 'utf8');
  const r = await p.evaluate(x => window.__TC_DEV.ev(x), src);
  console.log(JSON.stringify({ r, pe }, null, 0));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 500)); process.exit(1) });
