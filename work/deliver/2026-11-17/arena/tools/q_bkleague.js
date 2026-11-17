// q_bkleague.js — בדיקה חוסמת (arena 17.11): ליגת הכדורסל של האי לפי שעון המשחק — 3 ימי משחק של כדורסל (9 ימים) → לפחות מחזור אחד נרשם
// (ובפועל 3), הטלפון ("חדשות העיר" — כדורסל באי) והשלט מתעדכנים, אין יום עם כדורגל וכדורסל, המשחק החי באולם מסתיים בתוצאה שנכנסת לטבלה.
// הרצה: node W/qa_tools/probe_c2.js <build> q_bkleague.js <out.json>
return (async()=>{const why=[],bad=w=>why.push(w),R={};const strip=h=>String(h||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
 try{R.audit=LEAGUEBK.audit();if(!R.audit.ok)bad('audit: '+R.audit.why.join(' | '))}catch(e){bad('audit: '+e.message)}
 try{const t0=performance.now();R.arena=TCARENA.bkAudit();R.arenaMs=Math.round(performance.now()-t0);if(!R.arena.ok)bad('arena: '+R.arena.why.join(' | '))}catch(e){bad('arena: '+e.message)}
 try{R.draw=TCARENA.drawTest();if(R.draw.err)bad('ציור האולם: '+R.draw.err);if(R.draw.frames<24)bad('ציור האולם: '+R.draw.frames+' פריימים')}catch(e){bad('drawTest: '+e.message)}
 // המשחק החי מ-F9 (נכנס לטבלה): קפיצה לסוף — התוצאה בטבלה
 try{const L0=LEAGUEBK.st(),r0=L0.season*10+L0.round,g=A34PLAY.gm(),r=LEAGUEBK.f9('match');TCARENA.go&&0;const M=TCARENA.sess(r.idx);const sc=TCARENA.score(M,M.dur);
  window.__TC_DEVBK={idx:r.idx};LEAGUEBK.finish(r.idx,sc,sc[0]===sc[1]?M.ftCand:null);const L1=LEAGUEBK.st();R.live={idx:r.idx,score:sc,round:[r0,L1.season*10+L1.round]};if(L1.season*10+L1.round<=r0)bad('משחק חי שנגמר לא נכנס לטבלה')}catch(e){bad('live: '+e.message)}
 const view=()=>{const c=gameClock(),L=LEAGUEBK.st();let ph='';try{ph=strip(PHONE_VIEWS.news())}catch(e){bad('הטלפון: '+e.message)}return {day:c.day,hhmm:c.hhmm,season:L.season,round:L.round,lastDay:L.lastDay,sign:LEAGUEBK.signLine(),phone:ph}};
 const A=view(),day0=A.day,r0=A.season*10+A.round,seen=[];let prev=A;
 for(let i=0;i<9*144;i++){G84_CLOCK.base+=10;LEAGUEBK.tick();if(i%12===11){const v=view();seen.push(v);if(v.round!==prev.round&&v.sign===prev.sign&&v.season===prev.season)bad('המחזור התקדם והשלט לא: '+v.sign);prev=v}if(i%24===0)await new Promise(r=>setTimeout(r,2))}
 const Z=seen[seen.length-1],rounds=(Z.season*10+Z.round)-r0;R.days=[day0,Z.day];R.rounds=rounds;R.end={round:Z.round,season:Z.season,sign:Z.sign,lastDay:Z.lastDay};
 if(Z.day-day0<9)bad('השעון לא התקדם 9 ימים: '+day0+'→'+Z.day);if(rounds<1)bad('3 ימי משחק בלי מחזור: '+A.round+'→'+Z.round);if(rounds<3)bad('פחות מ-3 מחזורים ב-3 ימי משחק: '+rounds);
 if(!/כדורסל באי/.test(Z.phone))bad('הטלפון בלי הפרק של הכדורסל');if(!/טבלת הכדורסל/.test(Z.phone))bad('הטלפון בלי טבלת הכדורסל');if(!/מחזור \d+ באולם באי/.test(Z.phone))bad('הטלפון בלי תוצאת מחזור');
 R.phone=Z.phone.slice(0,300);R.err=LEAGUEBK.err()||TCARENA.err()||null;if(R.err)bad('err: '+R.err);
 return Object.assign({ok:!why.length,why:why.slice(0,12)},R)})()
