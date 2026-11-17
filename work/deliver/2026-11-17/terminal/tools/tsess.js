// tsess.js — terminal: דפדפן אחד — השאילתה (q_term.js) ואחריה צילומים לבדיקה בעין (לעצמי בלבד)
// node tsess.js <game.html> <out_prefix> '<json shots: [[name,x,y,zoom,tc|null], ...]>'
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [f, o, js] = process.argv.slice(2); const shots = JSON.parse(js || '[]');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(f) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(3000);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  let q = fs.readFileSync(path.join(__dirname, 'q_term.js'), 'utf8'); q = '(()=>{' + q + '\n})()';
  try { fs.writeFileSync(o + '_q.json', await ev(q)) } catch (e) { fs.writeFileSync(o + '_q.json', JSON.stringify({ err: String(e).slice(0, 500) })) }
  for (const [n, x, y, z, tc] of shots) {
    await ev(`try{PlayerProfile.mode='walk'}catch(e){};try{PlayerPed.x=${x};PlayerPed.y=${y}}catch(e){};Camera.x=${x};Camera.y=${y};Camera.zoom=${z};try{${tc != null ? 'S15X.ovr={tc:' + tc + ',min:s15Clock().min,abs:s15Clock().abs}' : 'delete S15X.ovr'}}catch(e){};1`);
    await p.waitForTimeout(2200); await ev(`Camera.x=${x};Camera.y=${y};Camera.zoom=${z};1`); await p.waitForTimeout(800);
    await p.evaluate(() => { const cs = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height), c = cs[0]; for (const el of document.body.querySelectorAll('*')) if (el !== c && !el.contains(c)) el.style.visibility = 'hidden' });
    await p.screenshot({ path: o + '_' + n + '.png' });
    await p.evaluate(() => { for (const el of document.body.querySelectorAll('*')) el.style.visibility = '' });
  }
  let info = ''; try { info = await ev('JSON.stringify({term:window.__TC_TERM&&{err:__TC_TERM.err,n:__TC_TERM.n},sh:window.__TC_TERM_SH&&{err:__TC_TERM_SH.err,n:__TC_TERM_SH.n},s15j:S15J.err})') } catch (e) { info = String(e).slice(0, 200) }
  console.log('errors', errs.length, errs.slice(0, 3).join(' | '), info);
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
