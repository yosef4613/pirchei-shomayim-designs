const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  await p.goto('file://' + __dirname + '/roads_r15.html'); await p.waitForTimeout(400);
  await p.screenshot({ path: __dirname + '/r15.png', fullPage: false }); await b.close(); })();
