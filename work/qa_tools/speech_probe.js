// בדיקה של הדיבור בסרט עם קול מדומה (כמו כרום עם אסף בלבד): נשלחות שורות, מסתיימות, אין שגיאות, והכול נעצר בסגירה
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  await ctx.addInitScript(() => {
    const voices = [{ name: 'Microsoft Asaf - Hebrew (Israel)', lang: 'he-IL', localService: true, default: false, voiceURI: 'asaf' }];
    const q = []; let cur = null; window.__fakeSpoken = [];
    const fake = { speaking: false, pending: false, paused: false, getVoices: () => voices, addEventListener() {}, removeEventListener() {},
      speak(u) { q.push(u); if (!cur) next() }, cancel() { q.length = 0; cur = null; }, pause() {}, resume() {} };
    function next() { cur = q.shift(); if (!cur) return; window.__fakeSpoken.push([cur.text.length, cur.voice && cur.voice.name, cur.pitch]);
      setTimeout(() => { cur.onstart && cur.onstart(); setTimeout(() => { const c = cur; cur = null; c && c.onend && c.onend(); next() }, 40 * cur.text.length / 10) }, 5) }
    Object.defineProperty(window, 'speechSynthesis', { value: fake, configurable: true });
    window.SpeechSynthesisUtterance = function (t) { this.text = t; };
  });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(process.argv[2]) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{try{TCVOICE.reset();TCSHOW.open('film',0,{place:'קולנוע',onEnd(){}});return 1}catch(e){return String(e)}})()`));
  await p.waitForTimeout(75000);
  const r = await p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify({st:TCVOICE.st,spoken:window.__fakeSpoken.length,show:(()=>{try{return TCSHOW.st||null}catch(e){return String(e)}})()})`));
  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{try{TCSHOW.close&&TCSHOW.close()}catch(e){}return 1})()`));
  console.log(r, 'שגיאות:', JSON.stringify(errs)); await b.close();
})();
