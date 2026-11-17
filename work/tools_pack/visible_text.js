// visible_text.js <page.html> — מדפיס את הטקסט הגלוי של דף (innerText, וגם title, aria-label ו-<title> של SVG), כדי להריץ עליו heb_check.py
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto('file://' + path.resolve(process.argv[2]), { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const t = await p.evaluate(() => [document.title, document.body.innerText,
    ...[...document.querySelectorAll('[title],[aria-label]')].map(e => (e.getAttribute('title') || '') + ' ' + (e.getAttribute('aria-label') || '')),
    ...[...document.querySelectorAll('svg title, svg text')].map(e => e.textContent)].join('\n'));
  process.stdout.write(t); await b.close();
})();
