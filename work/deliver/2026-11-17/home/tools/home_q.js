// home_q.js — home (17.11): הבדיקה של HOME-01 (שינה), "הצץ", המסוק העומד ומסך הבית בכל 8 הרמות — במשחק עצמו.
// node home_q.js <game.html> <out.json> [shots_dir]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outF, shots] = process.argv.slice(2); if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 300)) });
  const R = { file: path.basename(file), steps: {}, bad: [] }; const bad = s => { R.bad.push(s); console.log('✗ ' + s) };
  const go = async () => { await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(2500) };
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const evj = async s => { const v = await ev(s); try { return JSON.parse(v) } catch (e) { return v } };
  const shot = async n => { if (shots) await p.screenshot({ path: path.join(shots, n + '.png') }) };
  const home = (n) => ev(`(()=>{PlayerProfile.home.homeLevel=${n};PlayerProfile.mode='walk';try{if(State.phoneOpen)setPhoneOpen(false)}catch(e){}const q=playerHomeServicePoint();PlayerPed.x=q.x;PlayerPed.y=q.y+8;Camera.x=q.x;Camera.y=q.y-40;Camera.zoom=1.1;return 1})()`);
  try {
    await go();
    // (1) the in-game check: every option, the light, the save/load of the clock, the hotel, the peek
    R.steps.check = await evj('JSON.stringify(window.__TC_HOME.check())'); if (!R.steps.check.ok) bad('check: ' + JSON.stringify(R.steps.check.bad));
    console.log('check', R.steps.check.ok, (R.steps.check.sleep || []).length);
    // (2) F at the door of every level: the card of sleep, the peek and the drawing (1–7), no "המבנה למסוק"
    R.steps.levels = [];
    for (let n = 1; n <= 8; n++) {
      await home(n); await p.waitForTimeout(400);
      const r = await evj(`(()=>{const ok=(window.__TC_HOME.in?(openPoiPhone('house','PLAYER-HOME'),true):interactNearbyPoi());const h=document.querySelector('#phoneOverlay')?document.querySelector('#phoneOverlay').innerHTML:'';return JSON.stringify({ok,app:State.phoneApp,open:State.phoneOpen,sleep:(h.match(/data-home-sleep=/g)||[]).length,peek:h.indexOf('data-home-peek')>=0,svg:h.indexOf('<svg')>=0,hangar:h.indexOf('המבנה למסוק')>=0,saba:h.indexOf('הבית של סבא')>=0,player:h.indexOf('בית השחקן')>=0,lvl:(h.match(/(\\d) \\/ 8/)||[])[1]||null})})()`);
      R.steps.levels.push(Object.assign({ n }, r));
      if (r.app !== 'house' || !r.open) bad('L' + n + ': F לא פתח את מסך הבית'); if (r.sleep < 5) bad('L' + n + ': אין 5 כפתורי שינה (' + r.sleep + ')');
      if (n < 8 && (!r.peek || !r.svg)) bad('L' + n + ': אין הצץ / ציור'); if (r.hangar) bad('L' + n + ': "המבנה למסוק"'); if (!r.saba) bad('L' + n + ': אין "הבית של סבא" במסך הבית');
      if (n === 1 || n === 6) await shot('f_house_L' + n);
      await ev('setPhoneOpen(false)');
    }
    // (3) a real sleep with the transition: 22:30 → "עד 07:00", by the button
    await home(3); await ev('gameClockSet(22,30);1'); await ev("openPoiPhone('house','PLAYER-HOME')"); await p.waitForTimeout(300);
    const before = await evj('JSON.stringify(gameClock())'); const t0 = Date.now();
    await p.evaluate(()=>document.querySelector('#phoneOverlay button[data-home-sleep="morning"]').click()); await p.waitForTimeout(900); await shot('sleep_mid');
    await p.waitForFunction(() => !window.__TC_HOME.sleep.S.busy, null, { timeout: 8000, polling: 100 });
    const dur = Date.now() - t0; await p.waitForTimeout(500); await shot('sleep_after');
    const after = await evj('JSON.stringify(Object.assign(gameClock(),{last:window.__TC_HOME.sleep.S.last,night:window.__TC_NIGHT,phone:State.phoneOpen,held:window.__TC_HOME.sleep.S.n.held,heldLog:window.__TC_HOME.sleep.S.heldLog}))');
    R.steps.real = { before, after, ms: dur }; console.log('real', before.hhmm, before.day, '→', after.hhmm, after.day, dur + 'ms');
    if (after.hhmm.slice(0, 2) !== '07' || after.day !== before.day + 1) bad('שינה אמיתית: ' + after.hhmm + ' יום ' + after.day);
    if (!after.last || !after.last.saved) bad('שינה אמיתית: לא נשמר'); if (after.phone) bad('המסך לא נסגר'); const tr = after.last && after.last.at ? after.last.at - t0 : dur; R.steps.real.tr = tr; if (tr > 4500) bad('המעבר ארוך: ' + tr);
    if (after.night > .2) bad('התאורה עדיין לילה: ' + after.night);
    // (4) 8 hours from 15:00 — the evening and the night light
    await ev('gameClockSet(15,0);1'); const b8 = await evj('JSON.stringify(gameClock())'); await ev("window.__TC_HOME.sleep.go('h8',{where:'home'})");
    await p.waitForFunction(() => !window.__TC_HOME.sleep.S.busy, null, { timeout: 8000, polling: 100 }); await p.waitForTimeout(400);
    const a8 = await evj('JSON.stringify(Object.assign(gameClock(),{night:window.__TC_NIGHT}))'); R.steps.h8 = { b8, a8 };
    if (a8.hhmm !== '23:00' && a8.hhmm !== '23:01') bad('8 שעות: ' + a8.hhmm); if (a8.night < .9) bad('8 שעות: אין לילה ' + a8.night); await shot('after_h8_night');
    // (5) until the next match
    const m = await evj(`(()=>{const N=A34PLAY.nextMatch();const T=window.__TC_HOME.sleep.target('match');return JSON.stringify({N,T})})()`); R.steps.matchT = m;
    if (m.T && !m.T.why) { await ev("window.__TC_HOME.sleep.go('match',{where:'home'})"); await p.waitForFunction(() => !window.__TC_HOME.sleep.S.busy, null, { timeout: 8000, polling: 100 });
      const am = await evj('JSON.stringify(gameClock())'); R.steps.match = am; if (am.day !== m.N.day || am.hhmm.slice(0, 2) !== '19') bad('עד המשחק: ' + am.hhmm + ' יום ' + am.day + ' במקום יום ' + m.N.day + ' 19:00'); }
    // (6) the reload: the saved hour and day come back
    await ev("window.__TC_HOME.sleep.go('h2',{where:'home'})"); await p.waitForFunction(() => !window.__TC_HOME.sleep.S.busy, null, { timeout: 8000, polling: 100 });
    const sv = await evj('JSON.stringify(gameClock())'); await go(); const ld = await evj('JSON.stringify(gameClock())'); R.steps.reload = { saved: sv, loaded: ld };
    const dm = (ld.day - sv.day) * 1440 + ld.min - sv.min; console.log('reload', sv.hhmm, sv.day, '→', ld.hhmm, ld.day, dm);
    if (dm < -1 || dm > 20) bad('אחרי טעינה: ' + ld.hhmm + ' יום ' + ld.day + ' (נשמר ' + sv.hhmm + ' יום ' + sv.day + ')');
    // (7) the hotel: the same action (pay, 07:00, saved)
    const ho = await evj(`(()=>{const id='A5-HOTEL',P=(typeof PLC_POIS!=='undefined'&&PLC_POIS[id])||null;if(!P)return JSON.stringify({no:1});PlayerProfile.mode='walk';PlayerProfile.money=Math.max(PlayerProfile.money,1000);PlayerPed.x=P.x;PlayerPed.y=P.y+4;gameClockSet(23,0);try{if(State.phoneOpen)setPhoneOpen(false)}catch(e){}interactNearbyPoi();const m0=PlayerProfile.money,here=plcHere(id);plcAct('night');return JSON.stringify({here,m0,P:Object.keys(P)})})()`);
    await p.waitForTimeout(200); await p.waitForFunction(() => !window.__TC_HOME.sleep.S.busy, null, { timeout: 8000, polling: 100 });
    const ha = await evj('JSON.stringify(Object.assign(gameClock(),{money:PlayerProfile.money,last:window.__TC_HOME.sleep.S.last}))'); R.steps.hotel = { ho, ha };
    if (ho.here) { if (ha.hhmm.slice(0, 2) !== '07' || !ha.last || ha.last.where !== 'hotel' || ha.money !== ho.m0 - 120) bad('המלון: ' + JSON.stringify(ha)) } else R.steps.hotel.skip = 'לא ליד הדלפק';
    // (8) the peek: the next level drawn, the camera back, the level and the money untouched
    await home(4); await ev('PlayerProfile.money=100;1'); await ev("openPoiPhone('house','PLAYER-HOME')"); await p.waitForTimeout(300);
    await p.evaluate(()=>document.querySelector('button[data-home-peek]').click()); await p.waitForTimeout(2500); await shot('peek_L5');
    const pk = await evj('JSON.stringify({c3:c3Lv(),lv:PlayerProfile.home.homeLevel,on:window.__TC_HOME.peek.P.on,money:PlayerProfile.money})');
    await p.keyboard.press('Escape'); await p.waitForTimeout(500);
    const pk2 = await evj('JSON.stringify({c3:c3Lv(),lv:PlayerProfile.home.homeLevel,on:window.__TC_HOME.peek.P.on})'); R.steps.peek = { pk, pk2 };
    if (pk.c3 !== 5 || !pk.on) bad('הצץ: ' + JSON.stringify(pk)); if (pk2.c3 !== 4 || pk2.on || pk2.lv !== 4) bad('הצץ חזרה: ' + JSON.stringify(pk2)); if (pk.money !== 100) bad('הצץ חייב כסף');
    // (9) the helicopter on the pad (L7, L8): still
    for (const n of [7, 8]) { await home(n); await ev(`(()=>{const P=C3LV[${n}-1].pad;Camera.x=P.c[0];Camera.y=P.c[1];Camera.zoom=1.4;return 1})()`); await p.waitForTimeout(1500);
      const h = await evj('JSON.stringify(window.__TC_HOMEHELI.n)'); if (!(h.still > 0)) bad('L' + n + ': המסוק לא צויר עומד'); R.steps['heli' + n] = h; await shot('heli_L' + n) }
    R.errors = errs.slice(0, 30); if (errs.length) bad(errs.length + ' שגיאות בדף');
  } catch (e) { bad('חריגה: ' + String(e).slice(0, 400)); R.errors = errs.slice(0, 30) }
  R.ok = !R.bad.length; fs.writeFileSync(outF, JSON.stringify(R, null, 1)); console.log(R.ok ? 'עבר' : 'נכשל: ' + R.bad.length); await b.close();
  // the rest of the chain in the same slot of the queue (the interior on the next build, the blocking gates on this one)
  try { const A = path.basename(file, '.html'), nx = 'try' + (+A.replace('try', '') + 1); if (process.env.HOME_CHAIN !== '0') require('child_process').spawnSync('bash', [path.join(__dirname, 'chain_in_slot.sh'), A, process.env.HOME_CHAIN_B || nx], { stdio: 'inherit' }) } catch (e) { console.log('chain', e) }
  process.exit(R.ok ? 0 : 1);
})();
