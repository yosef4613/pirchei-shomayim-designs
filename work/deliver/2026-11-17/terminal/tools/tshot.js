// tshot.js — terminal: צילומים מהמשחק לבדיקה בעין (לעצמי בלבד — לא לדף ולא לבעלים)
// node tshot.js <game.html> <out_prefix> '<json: [[name,x,y,zoom,tc|null], ...]>'   (השחקן עובר ברגל לנקודה, המצלמה עליה; tc — שעון המחזור של השדה)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [f, o, js] = process.argv.slice(2); const shots = JSON.parse(js);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(f) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  for (const [n, x, y, z, tc] of shots) {
    await ev(`try{PlayerProfile.mode='walk'}catch(e){};try{PlayerPed.x=${x};PlayerPed.y=${y}}catch(e){};Camera.x=${x};Camera.y=${y};Camera.zoom=${z};try{${tc != null ? 'S15X.ovr={tc:' + tc + '}' : 'delete S15X.ovr'}}catch(e){};1`);
    await p.waitForTimeout(2500); await ev(`Camera.x=${x};Camera.y=${y};Camera.zoom=${z};1`); await p.waitForTimeout(900);
    await p.evaluate(() => { const cs = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height), c = cs[0]; for (const el of document.body.querySelectorAll('*')) if (el !== c && !el.contains(c)) el.style.visibility = 'hidden' });
    await p.screenshot({ path: o + '_' + n + '.png' });
    await p.evaluate(() => { for (const el of document.body.querySelectorAll('*')) el.style.visibility = '' });
  }
  let info = ''; try { info = await ev('JSON.stringify({term:window.__TC_TERM&&{err:__TC_TERM.err,n:__TC_TERM.n},s15j:S15J.err,cam:[Camera.x,Camera.y,Camera.zoom]})') } catch (e) { info = String(e).slice(0, 200) }
  console.log('errors', errs.length, errs.slice(0, 3).join(' | '), info);
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
