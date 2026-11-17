// evalq.js — פותח בנייה עם #dev, מחכה ל-ready, ומריץ ביטויים מקובץ (ביטוי אחד בכל שורה שמתחילה ב->), מדפיס JSON.
//   node evalq.js <game.html> <exprs.txt> [simSecBefore=0]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, qf, pre] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e && e.stack || e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready() && window.__S10C, null, { timeout: 600000, polling: 500 });
  if (+pre) { let d = 0; while (d < +pre) { await p.evaluate((n) => window.__TC_DEV.ev(`(()=>{const L=SIM_LOOP,H=L.h;if(L.simNow==null)L.simNow=performance.now();let k=0;while(k<${n}*60){simStep(H,L.simNow+H*1000);L.simNow+=H*1000;k++}return 1})()`), 30); d += 30; } }
  const Q = fs.readFileSync(qf, 'utf8').split('\n').filter(l => l.startsWith('>')).map(l => l.slice(1));
  for (const q of Q) { let r; try { r = await p.evaluate((s) => window.__TC_DEV.ev(s), q) } catch (e) { r = 'ERR ' + e } console.log(JSON.stringify(r)) }
  console.log(JSON.stringify({ pageErrors: pe })); await b.close();
})();
