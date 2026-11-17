// live_check.js <live.html> <outdir> — fieldfix: הדף החי — לוחצים על כל כפתור, 0 שגיאות בדף, צילום לעצמי (לא לבעלים)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file), { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready() && window.__FFL, null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) { } await p.waitForTimeout(300) }
  const ids = ['lvOld', 'lvNew', 'lvTop', 'lvNew', 'r3Day', 'r3Run', 'r3Tow', 'r3Back', 'gaPark', 'tcStop', 'tcNight', 'tcDay'], R = [];
  const places = await p.$$eval('#tcBtnsA button', bs => bs.length);
  for (let i = 0; i < places; i++) { await p.click('#tcBtnsA button:nth-child(' + (i + 1) + ')'); await p.waitForTimeout(1500) }
  for (const id of ids) { await p.click('#' + id); await p.waitForTimeout(id.startsWith('r3') ? 5000 : 2500); const info = await p.$eval('#tcInfo', e => e.textContent); R.push([id, info]); if (/^r3|^lv/.test(id)) await p.screenshot({ path: path.join(out, 'live_' + id + '.png') }) }
  const o = { places, R, errs }; fs.writeFileSync(path.join(out, 'live_check.json'), JSON.stringify(o, null, 1)); console.log(JSON.stringify(o)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
