// R-55: מוציא את הטקסט הגלוי של דף (כולל כותרות, תוויות וכיתובים) כדי לבדוק אותו בבודק העברית.
// שימוש: node page_text.js <page.html>  → הטקסט יוצא לפלט
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.goto('file://' + require('path').resolve(process.argv[2]), { waitUntil: 'load', timeout: 120000 });
  await p.waitForTimeout(1500);
  const t = await p.evaluate(() => {
    const parts = [document.title, document.body.innerText];
    for (const e of document.querySelectorAll('[title],[aria-label],[alt],[placeholder]')) for (const a of ['title', 'aria-label', 'alt', 'placeholder']) if (e.getAttribute(a)) parts.push(e.getAttribute(a));
    for (const e of document.querySelectorAll('svg text')) parts.push(e.textContent);
    return parts.join('\n');
  });
  process.stdout.write(t); await b.close();
})();
