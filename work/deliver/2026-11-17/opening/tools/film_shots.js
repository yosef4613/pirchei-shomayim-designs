// film_shots.js — סרטון הפתיחה (TCOF): פותח את הבנייה ב-#dev, מפעיל את הסרטון ומצלם פריימים בזמנים שנבחרו (צילום לבדיקה פנימית בלבד — לא לדפים).
// node film_shots.js <game.html> <outdir> [t1,t2,...] [WxH]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, ts, vp] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const [W, H] = (vp || '1280x800').split('x').map(Number);
  const times = (ts || '3,10,17,24,31,37,43,49,55,61,68').split(',').map(Number);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500);
  const EV = (x) => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), x);
  const ok = await EV("(()=>{const r=TCOF.play('api');return{r,st:TCOF.st,on:!!TCSHOW.on,full:TCSHOW.on&&TCSHOW.on.full,total:TCSHOW.on&&TCSHOW.on.total,lines:TCSHOW.on&&TCSHOW.on.lines.length}})()");
  console.log('play', JSON.stringify(ok));
  await p.waitForTimeout(2500);
  const res = [];
  for (const t of times) {
    await EV('(()=>{const S=TCSHOW.on;if(S){S.t=' + (t - 1.2) + ';S.playing=true}return 1})()');
    await p.waitForTimeout(1300);
    const f = path.join(out, 'f' + String(t).padStart(2, '0') + '.png'); await p.screenshot({ path: f });
    res.push(await EV('({t:TCSHOW.on?+TCSHOW.on.t.toFixed(2):null,err:TCSHOW.ST.err,ferr:TCOF.st.err,city:TCCITY.st,logo:TCOF.st.logo})'));
  }
  const fin = await EV("({stats:TCSHOW.stats(),vrec:typeof TCVREC!=='undefined'?{pre:TCVREC.st.pre,played:TCVREC.st.played,mode:TCVREC.st.mode,err:TCVREC.st.err}:null,voice:TCSHOW.ST.voice})");
  console.log(JSON.stringify(res)); console.log(JSON.stringify(fin));
  // skip with Enter
  await p.keyboard.press('Enter'); await p.waitForTimeout(500);
  console.log('after Enter', JSON.stringify(await EV('({on:!!TCSHOW.on,last:TCSHOW.ST.last,st:TCOF.st,paused:State.paused})')));
  console.log('errors', errs.length, errs.slice(0, 5).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 500)); process.exit(1) });
