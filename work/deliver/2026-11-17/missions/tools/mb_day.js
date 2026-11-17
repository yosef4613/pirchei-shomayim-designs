// mb_day.js — יום משחק של לוח המשימות (D‑693), סבב 17.11 (missions).
// node mb_day.js <game.html> <out.json> [steps=288]   — דרך התור: bash W/tools_pack/bslot.sh node ...
// 288 צעדים של 5 דקות משחק (06:00 → 06:00 למחרת), בכל צעד ~1.1 שנ׳ אמיתיות (כדי שהטיימרים של המשחק ירוצו: הסיפורים לפי השעה — 700 מ"ש, הלוח — 1000 מ"ש).
// "השחקן": כל 90 דקות משחק משלים משימת צד אחת מהלוח (סיפור אזור — בשלבים של המנוע עצמו, S9STORY.advance; עבודה — כמו missionComplete),
//   מקבל הצעה אחת מכל שתיים (והשנייה — "אחר כך"), וכל שעת משחק מקדם שלב בסיפור (TCSTORY.skip — כמו הכפתור ב-F9).
// בכל צעד: הספירות (סיפור 1–3, צד 4–6, הצעות ≤1) ולכל משימה פעילה — הודעה, שורה ביומן, סמן במפה ויעד ניווט קיים (מאותו מצב).
// בבנייה בלי הלוח (הבסיס) — רושם כמה סיפורי אזור רצים, כמה הודעות הגיעו וכמה נקודות במפה — להשוואה.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, nS] = process.argv.slice(2); const STEPS = +(nS || 288);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const init = await ev(`(()=>{const MB=window.__TC_MB;if(MB)MB.force(true);try{__TC_STORY.jump('1-3')}catch(e){}   /* the story from the first group (1-3 · 1-4 · 1-5) */window.__MBD={m0:g77St().msgs.length,lastDone:0,offers:0,acc:0,later:0,done:0,skips:0};
    gameClockSet(6,0);return JSON.stringify({mb:!!MB,story:__TC_STORY.state(),msgs:g77St().msgs.length,clock:gameClock()})})()`);
  const rows = []; const t0 = Date.now();
  for (let i = 0; i < STEPS; i++) {
    const h = 6 + Math.floor(i * 5 / 60), mi = (i * 5) % 60;
    await ev(`gameClockSet(${h % 24},${mi})`);
    await p.waitForTimeout(1100);
    const r = await ev(`(()=>{const MB=window.__TC_MB,D=window.__MBD,o={i:${i},hm:'${String(h % 24).padStart(2, '0')}:${String(mi).padStart(2, '0')}'},bad=[];
     const zRun=Object.keys(S9STORY.ST).filter(id=>S9STORY.step(id)>0&&!S9STORY.done(id));o.zRun=zRun.length;o.msgs=g77St().msgs.length-D.m0;
     let L=[];try{__TC_MMIS.tick(true);L=__TC_MMIS.S.list}catch(e){}o.mk={};for(const m of L)o.mk[m.kind]=(o.mk[m.kind]||0)+1;
     try{o.nav=State.navigation?State.navigation.targetId:null}catch(e){}
     const so=__TC_STORY.open?__TC_STORY.open():[];o.storyOpen=so.length;
     if(MB){const S=MB.state();o.story=S.story;o.side=S.side;o.offer=S.offer?1:0;o.run=S.running;o.acc=S.acc;
      const jh=MB.jr(),msgs=g77St().msgs,R=navPoiRegistry();
      for(const it of S.items){const I=MB.info(it.key);if(!I||!I.poi||!R[I.poi])bad.push('nav '+it.key);if(!msgs.some(m=>m.mb===it.key))bad.push('msg '+it.key);if(jh.indexOf('data-mb-row="'+it.key+'"')<0)bad.push('card '+it.key);
       const id=it.key.slice(2),k=it.key[0];if(!L.some(m=>m.id===id&&(k==='z'?(m.kind==='zone'||m.kind==='friend'):(m.kind==='side'||m.kind==='job'))))bad.push('marker '+it.key)}
      for(const m of L){if((m.kind==='zone'||m.kind==='friend')&&!S.items.some(q=>q.key==='z:'+m.id)){let st=false;if(m.kind==='friend')try{for(const c of __TC_STORY.D.chapters)for(const q of c.missions||[])for(const s of q.steps)if(s.area===m.id)st=true}catch(e){}if(!st)bad.push('extra-marker '+m.kind+':'+m.id)}
       if((m.kind==='side'||m.kind==='job')&&!S.items.some(q=>q.key==='j:'+m.id)&&!(PlayerProfile.activeMission&&PlayerProfile.activeMission.id===m.id))bad.push('extra-marker '+m.kind+':'+m.id)}
      for(const q of so){if(q.at&&!R[q.at])bad.push('story-nav '+q.id);if(q.at&&!L.some(m=>m.kind==='story'&&m.id===q.id))bad.push('story-marker '+q.id)}
      if(o.story<1)bad.push('story<1');if(o.story>3)bad.push('story>3');if(o.side<4)bad.push('side<4');if(o.side>6)bad.push('side>6');if(o.offer>1)bad.push('offer>1');
      /* the player */
      if(${i}>0&&${i}%18===0){const it=S.items.find(q=>q.key[0]==='z')||S.items[0];if(it){const id=it.key.slice(2);if(it.key[0]==='z'){if(S9STORY.step(id)<1)MB.act('acc',it.key);let g=0;while(!S9STORY.done(id)&&g++<12)S9STORY.advance(id);}else{MB.E.jobsDone.push(id);PlayerProfile.progression.completedMissions.push(id)}D.done++;o.did='done '+it.key}}
      if(S.offer){D.offers++;if(D.offers%2){MB.act('acc',S.offer);D.acc++;o.did=(o.did||'')+' acc '+S.offer}else{MB.act('later',S.offer);D.later++;o.did=(o.did||'')+' later '+S.offer}}
      if(${i}>0&&${i}%12===0){try{__TC_STORY.skip();D.skips++}catch(e){}}}
     o.bad=bad;return JSON.stringify(o)})()`);
    try { rows.push(JSON.parse(r)) } catch (e) { rows.push({ i, raw: String(r).slice(0, 300) }) }
  }
  const fin = await ev(`(()=>{const MB=window.__TC_MB;return JSON.stringify({mb:MB?MB.state():null,story:__TC_STORY.state(),D:window.__MBD,mbE:MB?{err:MB.E.err,log:MB.E.log.slice(-20)}:null})})()`);
  const S = { file: path.basename(file), steps: rows.length, sec: Math.round((Date.now() - t0) / 1000), init: JSON.parse(init), fin: JSON.parse(fin), errors: errs.length, errs: errs.slice(0, 6) };
  const num = k => rows.map(r => r[k]).filter(v => typeof v === 'number');
  for (const k of ['story', 'storyOpen', 'side', 'offer', 'zRun', 'msgs']) { const v = num(k); if (v.length) S[k] = { min: Math.min(...v), max: Math.max(...v) } }
  S.markersMax = Math.max(...rows.map(r => Object.entries(r.mk || {}).filter(([k]) => k !== 'story' && k !== 'trial').reduce((a, [, v]) => a + v, 0)));
  S.badSteps = rows.filter(r => r.bad && r.bad.length).length; S.badFirst = rows.filter(r => r.bad && r.bad.length).slice(0, 8).map(r => r.hm + ' ' + r.bad.slice(0, 4).join(', '));
  S.ok = S.errors === 0 && S.badSteps === 0 && !!(S.fin.mb);
  fs.writeFileSync(out, JSON.stringify({ summary: S, rows }, null, 1));
  console.log(JSON.stringify(S));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
