// pshot.js — terminal: צילום של דף הציור לבדיקה בעין (לעצמי בלבד): node pshot.js <page.html> <out_prefix>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [f, o] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()) });
  await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(400);
  const figs = await p.$$('svg'); let i = 0; for (const el of figs) { await el.screenshot({ path: o + '_svg' + (i++) + '.png' }) }
  await p.setViewportSize({ width: 390, height: 900 }); await p.waitForTimeout(200); await p.screenshot({ path: o + '_phone.png' });
  const sw = await p.evaluate(() => document.documentElement.scrollWidth);
  console.log('phone scrollWidth', sw, 'errors', errs.length, errs.slice(0, 3).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e)); process.exit(1) });
