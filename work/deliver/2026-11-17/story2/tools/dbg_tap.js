// dbg_tap.js — story2: למה הקנבס של "המפה שלי" שחור אחרי נגיעה (בדיקה לעצמי)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => v === undefined ? null : JSON.parse(JSON.stringify(v))), s);
  await ev('(()=>{TCSTORY.E.modeOv="story";MBOARD.force(true);const s=g77St();delete s.board;TCSTORY.begin({silent:true});TCSTORY.jump("1-3");MBOARD.step();return 1})()');
  await p.waitForTimeout(1500);
  await ev('(()=>{window.__dbg={rp:0,draw:0};const r0=renderPhone;return 1})()');
  await p.keyboard.press('KeyT'); await p.waitForTimeout(600); await p.click('#phoneBody [data-phone-app="mymap"]'); await p.waitForTimeout(1200);
  const px = async (tag) => console.log(tag, JSON.stringify(await ev('(()=>{const c=document.getElementById("tcMyMapCv");if(!c)return{none:1};const g=c.getContext("2d"),d=g.getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<d.length;i+=400)if(d[i]+d[i+1]+d[i+2]>30)n++;window.__cv0=window.__cv0||c;return{w:c.width,h:c.height,lit:n,same:window.__cv0===c,draws:TCMYMAP.E.draws,V:TCMYMAP.E.V,err:TCMYMAP.E.err,html:document.getElementById("phoneBody").__tcHtml.length}})()')));
  await px('open');
  const hit = await ev('(()=>{const h=TCMYMAP.E.hits.find(x=>/^[jz]:/.test(x.key));const r=document.getElementById("tcMyMapCv").getBoundingClientRect();return{key:h.key,x:r.left+h.x,y:r.top+h.y}})()');
  await p.mouse.click(hit.x, hit.y); await px('tap+0'); await p.waitForTimeout(100); await px('tap+100'); await p.waitForTimeout(1200); await px('tap+1300');
  console.log('errs', errs); await b.close();
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
