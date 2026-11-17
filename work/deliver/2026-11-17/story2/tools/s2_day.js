// s2_day.js <game.html> <out.json> [steps=288] — story2 (17.11): יום משחק — הספירה כולל הצעות, המפה שלי, התזכורת. מבוסס על missions/tools/mb_day.js (כלל 19א).
// 288 צעדים של 5 דקות משחק (06:00 → 06:00), בכל צעד ~1.1 שנ׳ אמיתיות (הטיימרים של המשחק רצים), ו-10 שנ׳ של "משחק פעיל" לתזכורת (5 דק׳ משחק = 10 שנ׳ אמיתיות).
// "השחקן" (כמו mb_day): כל 90 דק׳ משחק משלים משימת צד; מקבל הצעה אחת מכל שתיים (והשנייה — "אחר כך"); כל שעה — שלב בסיפור (TCSTORY.skip); כל 3 שעות — בוחר משימה ב"המפה שלי" (pick).
// בכל צעד: סיפור 1–3 · על המפה 4–6 · על המפה + הצעות ≤ 6 · המפה שלי = הלוח (כל פריט של הלוח בשטח הפתוח — במפה, ושום דבר אחר) · התזכורות ≤ הזמן הפעיל / 6 דק׳ + 1 ·
// אף תזכורת כשיש שכבה (בכל צעד שמונה עשר — אירוע של TCBUSY ל-30 שנ׳ פעילות).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, nS] = process.argv.slice(2); const STEPS = +(nS || 288);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const init = await ev(`(()=>{try{c34Night(0)}catch(e){}MBOARD.force(true);TCSTORY.E.modeOv='story';const s=g77St();delete s.board;try{TCSTORY.begin({silent:true});TCSTORY.jump('1-3')}catch(e){}
    window.__S2D={offers:0,acc:0,later:0,done:0,skips:0,picks:0,layerReminds:0};const R=TCMYMAP.E.R;R.act=0;R.last=0;R.gap=TCMYMAP.T.first;R.n=0;R.hist=[];R.per={};R.prog={};R.sig={};R.skip={};
    gameClockSet(6,0);return JSON.stringify({story:TCSTORY.state(),c:MBOARD.counts(),clock:gameClock().hhmm})})()`);
  const rows = []; const t0 = Date.now();
  for (let i = 0; i < STEPS; i++) {
    const h = 6 + Math.floor(i * 5 / 60), mi = (i * 5) % 60;
    await ev(`gameClockSet(${h % 24},${mi})`);
    await p.waitForTimeout(1100);
    const r = await ev(`(()=>{const MB=MBOARD,D=window.__S2D,o={i:${i},hm:'${String(h % 24).padStart(2, '0')}:${String(mi).padStart(2, '0')}'},bad=[];
     /* the reminder: 10 s of active play (a layer every 18th step — none may come under it) */
     const n0=TCMYMAP.E.R.n;if(${i}%18===9&&typeof TCBUSY!=='undefined'){TCBUSY.set('event',{why:'s2day',ttl:20000});TCMYMAP.remindTick(30);if(TCMYMAP.E.R.n>n0){D.layerReminds++;bad.push('remind-under-layer')}TCBUSY.clear('event')}
     MB.E.cardQ=MB.E.cardQ.filter(q=>q.why!=='remind');if(MB.E.card)MB.E.card=null;TCMYMAP.remindTick(10);o.remind=TCMYMAP.E.R.n>n0?TCMYMAP.E.R.hist.at(-1).key:null;o.reminds=TCMYMAP.E.R.n;o.act=Math.round(TCMYMAP.E.R.act);
     const S=MB.state(),C=MB.counts();o.story=C.story;o.side=C.side;o.offer=C.offer;o.total=C.total;
     if(C.story<1)bad.push('story<1');if(C.story>3)bad.push('story>3');if(C.side<4)bad.push('side<4');if(C.side>6)bad.push('side>6');if(C.total>6)bad.push('total>6 '+C.side+'+'+C.offer);if(C.offer>1)bad.push('offer>1');
     /* the map of mine = the board (only the open area) */
     const L=TCMYMAP.items(),keys=new Set(L.map(q=>q.key)),b=MB.board();o.map=L.length;
     for(const q of b.side){const I=MB.info(q.key);if(I&&isFinite(I.x)&&!keys.has(q.key))bad.push('map-miss '+q.key)}if(b.offer&&!keys.has(b.offer.key))bad.push('map-offer');
     for(const it of L){if(it.grp==='side'&&!b.side.some(q=>q.key===it.key)&&!(b.offer&&b.offer.key===it.key))bad.push('map-extra '+it.key);if(it.kind!=='n'&&isFinite(it.x)&&TCSTORY.mode()==='story'){const z=currentChunkId(it.x,it.y);if(TCSTORY.locked('zone',z)&&!(typeof TCLOCK!=='undefined'&&TCLOCK.ptReach&&TCLOCK.ptReach(it.x,it.y)))bad.push('map-locked '+it.key+'@'+z)}}
     if(L.filter(q=>q.grp==='side').length!==C.total)bad.push('map-count '+L.filter(q=>q.grp==='side').length+'/'+C.total);
     if(o.reminds>Math.floor(o.act/TCMYMAP.T.gapMin)+1)bad.push('remind-rate '+o.reminds+'@'+o.act);
     /* the player */
     if(${i}>0&&${i}%18===0){const it=S.items.find(q=>q.key[0]==='z')||S.items[0];if(it){const id=it.key.slice(2);if(it.key[0]==='z'){if(S9STORY.step(id)<1)MB.act('acc',it.key);let g=0;while(!S9STORY.done(id)&&g++<12)S9STORY.advance(id);}else{MB.E.jobsDone.push(id);PlayerProfile.progression.completedMissions.push(id)}D.done++;o.did='done '+it.key}}
     if(S.offer){D.offers++;if(D.offers%2){MB.act('acc',S.offer);D.acc++;o.did=(o.did||'')+' acc '+S.offer}else{MB.act('later',S.offer);D.later++;o.did=(o.did||'')+' later '+S.offer}}
     if(${i}>0&&${i}%36===18){const L2=TCMYMAP.items().filter(q=>q.kind!=='n'&&q.poi&&!(q.kind==='z'&&S9STORY.done(q.key.slice(2)))&&!(q.kind==='j'&&MB.E.jobsDone.includes(q.key.slice(2))));   /* not one that the player finished in this same step (the board takes it out at its next step) */const it=L2[${i}%Math.max(1,L2.length)];if(it){State.navigation=null;const ok=TCMYMAP.pick(it.key,'day');D.picks++;o.did=(o.did||'')+' pick '+it.key;
       if(!ok)bad.push('pick-fail '+it.key);else{if(!(State.navigation&&State.navigation.targetId===it.poi)&&!PlayerProfile.activeMission)bad.push('pick-nav '+it.key);if(!((MB.E.card&&MB.E.card.key===it.key)||MB.E.cardQ.some(q=>q.key===it.key&&q.why==='pick')))bad.push('pick-card '+it.key)}}}
     if(${i}>0&&${i}%12===0){try{TCSTORY.skip();D.skips++}catch(e){}}
     /* after the player: the count again (an accept / a start must not go over 6) */
     const C2=MB.counts();if(C2.total>6)bad.push('after total>6 '+C2.side+'+'+C2.offer);
     o.bad=bad;return JSON.stringify(o)})()`);
    try { rows.push(JSON.parse(r)) } catch (e) { rows.push({ i, raw: String(r).slice(0, 300) }) }
  }
  const fin = await ev(`JSON.stringify({mb:MBOARD.state(),story:TCSTORY.state(),D:window.__S2D,mm:TCMYMAP.state(),mbE:{err:MBOARD.E.err}})`);
  const S = { file: path.basename(file), steps: rows.length, sec: Math.round((Date.now() - t0) / 1000), init: JSON.parse(init), fin: JSON.parse(fin), errors: errs.length, errs: errs.slice(0, 6) };
  const num = k => rows.map(r => r[k]).filter(v => typeof v === 'number');
  for (const k of ['story', 'side', 'offer', 'total', 'map']) { const v = num(k); if (v.length) S[k] = { min: Math.min(...v), max: Math.max(...v) } }
  S.reminds = rows.length ? rows.at(-1).reminds : 0; S.activeSec = rows.length ? rows.at(-1).act : 0; S.remindKeys = rows.filter(r => r.remind).map(r => r.hm + ' ' + r.remind);
  S.badSteps = rows.filter(r => r.bad && r.bad.length).length; S.badFirst = rows.filter(r => r.bad && r.bad.length).slice(0, 10).map(r => r.hm + ' ' + r.bad.slice(0, 4).join(', '));
  S.ok = S.errors === 0 && S.badSteps === 0 && !S.fin.mm.err && !S.fin.mbE.err;
  fs.writeFileSync(out, JSON.stringify({ summary: S, rows }, null, 1));
  console.log(JSON.stringify(S));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
