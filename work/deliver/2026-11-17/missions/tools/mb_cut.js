// mb_cut.js — הכרטיס של הלוח מול סצנה של הסיפור (הממצא של המיזוג 17.11: "1-van"). צילומים רק לעצמי (כלל 17). node mb_cut.js <game.html> <outdir>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outd] = process.argv.slice(2); fs.mkdirSync(outd, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const vis = `(()=>{const d=document.getElementById('tcMbCard'),M=__TC_MB;return JSON.stringify({card:!!M.E.card,q:M.E.cardQ.length,disp:d?d.style.display:'-',vis:d?getComputedStyle(d).visibility:'-',cutOn:document.body.classList.contains('tcCutOn'),playing:TCCUT.playing(),scene:(TCCUT.ST.on||{}).id||null})})()`;
  const o = {};
  /* the board on, a card up */
  o.a = await ev(`(()=>{const M=__TC_MB;M.force(true);delete g77St().board;M.tick();const k=M.board().side[0].key;M.E.card=null;M.E.cardQ=[{key:k,why:'side'}];M.tick();return k})()`);
  await p.waitForTimeout(1200); o.before = await ev(vis); await p.screenshot({ path: path.join(outd, 'before.png') });
  /* the scene of the van (done:1-2), and the three story cards that the group 1-3 · 1-4 · 1-5 queues */
  o.b = await ev(`(()=>{const r=TCCUT.play('1-van');const M=__TC_MB,k=M.board().side[1].key;M.E.cardQ.push({key:k,why:'side'});return String(r)})()`);
  await p.waitForTimeout(600); o.cut0 = await ev(vis); await p.screenshot({ path: path.join(outd, 'cut_0.png') });
  await p.waitForTimeout(2500); o.cut1 = await ev(vis); await p.screenshot({ path: path.join(outd, 'cut_1.png') });
  /* the scene ends → the card comes back */
  o.c = await ev(`(()=>{TCCUT.end();return 'end'})()`);
  await p.waitForTimeout(2500); o.after = await ev(vis); await p.screenshot({ path: path.join(outd, 'after.png') });
  const J = s => { try { return JSON.parse(s) } catch (e) { return {} } };
  const c0 = J(o.cut0), c1 = J(o.cut1), af = J(o.after), bf = J(o.before);
  o.ok = !!(bf.card && bf.vis === 'visible' && c0.playing && (c0.vis === 'hidden' || c0.disp === 'none') && (c1.vis === 'hidden' || c1.disp === 'none') && !af.playing && af.card && af.vis === 'visible' && af.disp === 'block' && !errs.length);
  o.errs = errs; fs.writeFileSync(path.join(outd, 'cut.json'), JSON.stringify(o, null, 1)); console.log(JSON.stringify(o).slice(0, 3000));
  await b.close(); process.exit(o.ok ? 0 : 2);
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
