// film_flow.js — סרטון הפתיחה: הבדיקה של הזרימה (בלי צילומים). node film_flow.js <game.html> <out.json>
// (1) ב-#dev הסרטון לא קופץ לבד ("משחק חדש" של בדיקה); (2) "משחק חדש" אמיתי (האירוע tcsave · new, בלי הדגל של #dev) → הסרטון במסך מלא,
// הקולות המוקלטים, המשחק לא מושהה, הסיפור מחכה; Esc מדלג; (3) תפריט Esc → "סרטון הפתיחה" → המשחק מושהה בזמן הסרטון, Enter מדלג → חוזר כמו שהיה;
// (4) עד הסוף: הסרטון נסגר לבד (done) ושום שגיאה; 0 שגיאות בדף.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const EV = (x) => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), x);
  const R = { checks: {} }; const ck = (k, v, info) => { R.checks[k] = { ok: !!v, info } };
  // 1
  await EV("(window.dispatchEvent(new CustomEvent('tcsave',{detail:{slot:1,mode:'story',how:'new'}})),1)"); await p.waitForTimeout(900);
  let s = await EV("({on:!!TCSHOW.on,why:TCOF.st.why,skip:!!window.__TCO_SKIP})"); ck('dev_no_auto', !s.on && s.why === 'hash', s);
  // 2
  await EV("(window.__TCO_SKIP_SAVE=window.__TCO_SKIP,window.__TCO_SKIP=false,window.dispatchEvent(new CustomEvent('tcsave',{detail:{slot:1,mode:'story',how:'new'}})),1)"); await p.waitForTimeout(1200);
  s = await EV("({on:!!TCSHOW.on,full:!!(TCSHOW.on&&TCSHOW.on.full),id:TCSHOW.on&&TCSHOW.on.prod.id,paused:!!State.paused,auto:TCOF.st.auto,lines:TCSHOW.on&&TCSHOW.on.lines.map(l=>l.who),pre:typeof TCVREC!=='undefined'?TCVREC.st.pre:null,skipBtn:(document.querySelector('#tcShow .tsClose')||{}).textContent,storyBusy:(()=>{try{return TCSTORY&&typeof TCSTORY.busy==='function'?TCSTORY.busy():null}catch(e){return 'x'}})()})");
  await EV("(window.__TCO_SKIP=window.__TCO_SKIP_SAVE,1)");
  ck('new_game_plays', s.on && s.full && s.id === 'tc-opening' && s.auto === 1 && !s.paused, s);
  ck('recorded_voices', s.pre === 2 && JSON.stringify(s.lines) === '["st-aharon","st-shimon"]', { pre: s.pre, lines: s.lines });
  await p.waitForTimeout(3000);
  s = await EV("({t:TCSHOW.on&&+TCSHOW.on.t.toFixed(2),playing:TCSHOW.on&&TCSHOW.on.playing,err:TCSHOW.ST.err})"); ck('runs', s.t > 0.2 && s.playing && !s.err, s);   // (בדפדפן בלי כרטיס גרפי הפריים איטי — הזמן של הסרט מתקדם לאט; בודקים שהוא זז)
  await p.keyboard.press('Escape'); await p.waitForTimeout(500);
  s = await EV("({on:!!TCSHOW.on,last:TCOF.st.last,skipped:TCOF.st.skipped,paused:!!State.paused})"); ck('esc_skips', !s.on && s.skipped === 1 && s.last && s.last.how === 'new' && !s.paused, s);
  // 3
  s = await EV("({menu:(window.TCO_EXT&&TCO_EXT.menu?TCO_EXT.menu():'').includes('tcofReplay')})"); ck('menu_button', s.menu, s);
  await EV("(__TCO.go('menu'),1)"); await p.waitForTimeout(500);
  const btn = await p.$('#tcoRoot [data-act="tcofReplay"]'); let clicked = false; if (btn) { await btn.click(); clicked = true }
  await p.waitForTimeout(900);
  s = await EV("({on:!!TCSHOW.on,paused:!!State.paused,menu:TCOF.st.menu,ui:TCO.ui})"); ck('menu_replay_plays_paused', clicked && s.on && s.paused && s.menu === 1 && !s.ui, s);
  await p.keyboard.press('Enter'); await p.waitForTimeout(500);
  s = await EV("({on:!!TCSHOW.on,paused:!!State.paused,last:TCOF.st.last})"); ck('enter_skips_unpauses', !s.on && !s.paused && s.last.how === 'menu', s);
  // 4
  await EV("(TCOF.play('api'),1)"); await p.waitForTimeout(1500);
  await EV("(TCSHOW.on.t=TCSHOW.on.total-0.8,1)"); for (let i = 0; i < 40; i++) { await p.waitForTimeout(500); if (!(await EV('!!TCSHOW.on'))) break }
  s = await EV("({on:!!TCSHOW.on,last:TCOF.st.last,done:TCOF.st.done,err:TCSHOW.ST.err,ferr:TCOF.st.err,logo:TCOF.st.logo,LG:!!TCOF.LG.R})"); ck('ends_by_itself', !s.on && s.done === 1 && s.last.done && !s.err && !s.ferr && !s.LG, s);
  // the cinema is as before: film 0 in the hall
  s = await EV("(()=>{const r=TCSHOW.open('film',0,{});const S=TCSHOW.on;const o={r,full:S&&S.full,total:S&&+S.total.toFixed(1),btn:(document.querySelector('#tcShow .tsClose')||{}).textContent};TCSHOW.close(false);return o})()");
  ck('cinema_unchanged', s.r && !s.full && /חזרה לקולנוע/.test(s.btn || ''), s);
  ck('page_errors_0', errs.length === 0, errs.slice(0, 5));
  R.ok = Object.values(R.checks).every(c => c.ok); R.n = Object.keys(R.checks).length; R.pass = Object.values(R.checks).filter(c => c.ok).length;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log('film_flow', R.pass + '/' + R.n, R.ok ? 'עבר' : 'נכשל');
  for (const [k, v] of Object.entries(R.checks)) if (!v.ok) console.log(' נכשל:', k, JSON.stringify(v.info).slice(0, 300));
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(String(e).slice(0, 500)); process.exit(2) });
