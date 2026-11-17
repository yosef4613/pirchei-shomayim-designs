// q_s2.js <game.html> <out.json> [shots] — story2 (17.11): בדיקה מהירה — TCMYMAP.qa (המפה שלי, הספירה כולל הצעות, התזכורת), MBOARD.qa (הלוח), TCSTORY.qa (הסיפור),
// ואז במשחק עצמו (הלוח מופעל, מצב "סיפור", הסיפור בקבוצה הראשונה): פתיחת "המפה שלי" מהטלפון (האייקון), נגיעה בסימון, "בחר" → הטלפון נסגר, ניווט, כרטיס 'pick'.
// shots — צילומים לבדיקה בעין (רק לעצמי, לא לדף).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => v === undefined ? null : JSON.parse(JSON.stringify(v))), s);
  const R = { file: path.basename(file) }; const t0 = Date.now();
  R.mymap = await ev('TCMYMAP.qa()'); console.log('mymap', JSON.stringify(R.mymap));
  R.board = await ev('(()=>{const q=MBOARD.qa();return{ok:q.ok,why:q.why,s2:q.s2,max:q.max,ms:q.ms,error:q.error}})()'); console.log('board', JSON.stringify(R.board));
  R.story = await ev('(()=>{try{const q=TCSTORY.qa();return{ok:q.ok,why:(q.why||[]).slice(0,8),ms:q.ms}}catch(e){return{err:String(e)}}})()'); console.log('story', JSON.stringify(R.story).slice(0, 400));
  // the game itself: the board on, the story mode, the story at the first group
  R.setup = await ev('(()=>{try{c34Night(0)}catch(e){}TCSTORY.E.modeOv="story";MBOARD.force(true);const s=g77St();delete s.board;TCSTORY.begin({silent:true});TCSTORY.jump("1-3");gameClockSet(10,0);MBOARD.step();return{c:MBOARD.counts(),open:TCSTORY.open().map(q=>q.id)}})()');
  console.log('setup', JSON.stringify(R.setup)); await p.waitForTimeout(2500);
  await ev('(()=>{const b=g77St().board;b.t=-1e9;MBOARD.step();MBOARD.E.cardQ=[];MBOARD.E.card=null;if(MBOARD.E.el)MBOARD.E.el.style.display="none";return 1})()');
  // the phone → the icon "המפה שלי"
  await p.keyboard.press('KeyT'); await p.waitForTimeout(800);
  R.icon = await p.evaluate(() => { const x = document.querySelector('#phoneBody [data-phone-app="mymap"]'); return x ? x.textContent.trim() : null });
  if (R.icon) { await p.click('#phoneBody [data-phone-app="mymap"]'); await p.waitForTimeout(1200) }
  R.app = await ev('(()=>{const c=document.getElementById("tcMyMapCv");return{app:State.phoneApp,cv:!!c,w:c&&c.width,items:TCMYMAP.E.items.map(q=>q.key+(q.offer?"?":"")),hits:TCMYMAP.E.hits.length,rows:document.querySelectorAll("#phoneBody [data-mm-row]").length,c:MBOARD.counts(),st:TCMYMAP.state()}})()');
  console.log('app', JSON.stringify(R.app));
  if (shots) await p.screenshot({ path: out.replace(/\.json$/, '_app.png') });
  // a tap on the first marker of a side mission
  const hit = await ev('(()=>{const h=TCMYMAP.E.hits.find(x=>/^[jz]:/.test(x.key))||TCMYMAP.E.hits[0];if(!h)return null;const r=document.getElementById("tcMyMapCv").getBoundingClientRect();return{key:h.key,x:r.left+h.x,y:r.top+h.y}})()');
  if (hit) { await p.mouse.click(hit.x, hit.y); await p.waitForTimeout(600) }
  R.tap = { hit, sel: await ev('TCMYMAP.E.sel'), info: await p.evaluate(() => { const i = document.getElementById('tcMmInfo'); return i ? i.textContent.slice(0, 200) : null }) };
  R.tap.lit = await ev('(()=>{const c=document.getElementById("tcMyMapCv");if(!c)return -1;const d=c.getContext("2d").getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<d.length;i+=400)if(d[i]+d[i+1]+d[i+2]>60)n++;return n})()');
  console.log('tap', JSON.stringify(R.tap));
  if (shots) await p.screenshot({ path: out.replace(/\.json$/, '_sel.png') });
  R.btn = await p.evaluate(() => { const x = document.querySelector('#tcMmInfo [data-mm-pick]'); if (x) { x.click(); return true } return false }); await p.waitForTimeout(2200)
  R.pick = await ev('(()=>{const M=MBOARD;return{phone:State.phoneOpen,nav:State.navigation&&State.navigation.targetId,card:M.E.card&&M.E.card,cardTxt:M.E.el&&M.E.el.style.display==="block"?M.E.el.textContent.slice(0,160):null}})()');
  console.log('pick', JSON.stringify(R.pick));
  if (shots) await p.screenshot({ path: out.replace(/\.json$/, '_card.png') });
  // "במפה שלי ›" in the card → the app again, on the same mission
  R.lk = await p.evaluate(() => { const x = document.querySelector('#tcMbCard [data-mymap]'); if (x) { x.click(); return true } return false }); await p.waitForTimeout(1000)
  R.link = await ev('({phone:State.phoneOpen,app:State.phoneApp,sel:TCMYMAP.E.sel})'); console.log('link', JSON.stringify(R.link));
  await ev('(()=>{setPhoneOpen(false);return 1})()'); await p.waitForTimeout(400);
  // J
  await p.keyboard.press('KeyJ'); await p.waitForTimeout(800); R.keyJ = await ev('({phone:State.phoneOpen,app:State.phoneApp})'); await p.keyboard.press('KeyJ'); await p.waitForTimeout(500); R.keyJ2 = await ev('State.phoneOpen');
  // the journal: the button
  await p.keyboard.press('KeyT'); await p.waitForTimeout(500); await ev('(()=>{openPhoneApp("journal");return 1})()'); await p.waitForTimeout(600);
  R.jr = await p.evaluate(() => { const b = document.querySelector('#phoneBody [data-mymap]'); const t = document.querySelector('#phoneBody'); return { btn: !!b, txt: t ? t.textContent.replace(/\s+/g, ' ').slice(0, 400) : '' } });
  if (shots) await p.screenshot({ path: out.replace(/\.json$/, '_jr.png') });
  await ev('(()=>{setPhoneOpen(false);return 1})()');
  R.final = await ev('({mm:TCMYMAP.state(),mb:{err:MBOARD.E.err,errs:MBOARD.E.errs},st:{err:TCSTORY.E.err}})');
  R.errors = errs; R.sec = Math.round((Date.now() - t0) / 1000);
  R.ok = !!(R.mymap && R.mymap.ok && R.board && R.board.ok && R.icon && R.app && R.app.cv && R.tap.sel && R.tap.lit > 50 && R.pick && !R.pick.phone && R.pick.nav && R.pick.card && R.pick.card.why === 'pick' && R.link.app === 'mymap' && R.keyJ.app === 'mymap' && R.keyJ2 === false && R.jr.btn && !errs.length && !R.final.mm.err && !R.final.mb.err);
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log('ok', R.ok, 'errors', errs.length, JSON.stringify(R.final).slice(0, 400));
  await b.close();
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
