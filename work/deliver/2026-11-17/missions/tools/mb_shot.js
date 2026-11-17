// mb_shot.js — צילומים לבדיקה בעין (רק לעצמי, לא לדף — כלל 17): הכרטיס הקופץ, היומן והשרשור של הלוח. node mb_shot.js <game.html> <outdir>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outd] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const o = {};
  o.a = await ev(`(()=>{const MB=__TC_MB;MB.force(true);try{__TC_STORY.jump('1-3')}catch(e){}delete g77St().board;MB.tick();return JSON.stringify(MB.state())})()`);
  await p.waitForTimeout(2500); await p.screenshot({ path: path.join(outd, 'card.png') });
  o.card = await ev(`(()=>{const d=document.getElementById('tcMbCard');return d?d.style.display+' | '+d.innerText.slice(0,300):'none'})()`);
  o.b = await ev(`(()=>{setPhoneOpen(true);openPhoneApp('journal');return document.getElementById('phoneBody').innerText.slice(0,900)})()`);
  await p.waitForTimeout(800); await p.screenshot({ path: path.join(outd, 'journal.png') });
  o.c = await ev(`(()=>{const m=g77St().msgs.filter(q=>q.mb).pop();if(!m)return 'no msg';g77Sp().thread=m.who;g77Sp().keep=1;openPhoneApp('msgs');return document.getElementById('phoneBody').innerText.slice(0,600)})()`);
  await p.waitForTimeout(800); await p.screenshot({ path: path.join(outd, 'thread.png') });
  o.d = await ev(`(()=>{setPhoneOpen(false);try{setMapOpen(true)}catch(e){return 'map '+e}return 'map'})()`);
  await p.waitForTimeout(1200); await p.screenshot({ path: path.join(outd, 'map.png') });
  o.errs = errs; fs.writeFileSync(path.join(outd, 'shot.json'), JSON.stringify(o, null, 1)); console.log(JSON.stringify(o).slice(0, 3000));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
