// q_stadium3.js — בדיקה חוסמת (stadium 17.11): 3 ימי משחק לפי שעון המשחק → לפחות מחזור אחד נרשם, והשלט / הדף החי / הטלפון / F9 מתעדכנים
// ולא מציגים תאריך אמיתי. הרצה: node W/qa_tools/probe_c2.js <build> q_stadium3.js <out.json>
// השעון מתקדם בצעדים של 10 דקות משחק, ובכל צעד LEAGUE4.tick() (כמו הטיימר של כל שנייה); בלי קפיצה מעל יום שלם.
return (async()=>{
 const strip=h=>String(h||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim(), realDate=/\b\d{1,2}\.(1[0-2]|[1-9])\b|ראשון|שני |שלישי|רביעי|חמישי|שישי|שבת/;
 const why=[],bad=w=>why.push(w);
 const view=()=>{const c=gameClock(),L=LEAGUE4.st();let ph='',pl='',f9='',N=null,D=null;try{ph=strip(PHONE_VIEWS.news())}catch(e){bad('הטלפון: '+e.message)}
  try{pl=strip(plcStadium())}catch(e){bad('הדף של האצטדיון: '+e.message)}try{N=A34PLAY.nextMatch();D=N&&A34PLAY.dateOf(N.day)}catch(e){}const m=plcNextMatch();
  return {day:c.day,hhmm:c.hhmm,season:L.season,round:L.round,lastDay:L.lastDay,sign:LEAGUE4.signLine(),signDay:D&&D.lbl,plc:m&&m.lbl,plcLabel:m&&m.label,fx:LEAGUE4.fxLabel(L),phone:ph,place:pl}};
 const A=view(),day0=A.day,r0=A.season*10+A.round,seen=[];let prev=A;
 for(let i=0;i<3*144;i++){G84_CLOCK.base+=10;LEAGUE4.tick();if(i%6===5){const v=view();seen.push(v);
   if(realDate.test(v.signDay||'')||realDate.test(v.plc||''))bad('תאריך אמיתי בשלט / בדף: '+v.signDay+' / '+v.plc);
   if(/חדשות העיר [^ ]+ \d+\.\d+/.test(v.phone)||/יום (ראשון|שני|שלישי|רביעי|חמישי|שישי|שבת) \d/.test(v.phone))bad('תאריך אמיתי בטלפון: '+v.phone.slice(0,80));
   if(v.plcLabel!==v.fx)bad('הדף החי והליגה לא על אותו משחק: '+v.plcLabel+' / '+v.fx);
   if(v.round!==prev.round&&v.sign===prev.sign&&v.season===prev.season)bad('המחזור התקדם והשלט לא: '+v.sign);prev=v}
  await new Promise(r=>setTimeout(r,4))}
 const Z=seen[seen.length-1],rounds=(Z.season*10+Z.round)-r0;
 if(Z.day-day0<3)bad('השעון לא התקדם 3 ימים: '+day0+'→'+Z.day);
 if(rounds<1)bad('3 ימי משחק בלי מחזור: '+A.round+'→'+Z.round);
 if(!/יום \d+ · \d\d:\d\d/.test(Z.phone))bad('הטלפון בלי יום המשחק');
 if(!/מחזור \d/.test(Z.phone))bad('הטלפון בלי תוצאת מחזור');
 if(!/משחקים/.test(Z.place))bad('הטבלה בדף האצטדיון חסרה');
 let tonight=null;try{tonight=tcpoTonight();const n=TCSHOW.PLAYS.length,d=gameClock().day;if(n&&tonight!==((d-1)%n))bad('ההצגה של הערב לא לפי יום המשחק: '+tonight)}catch(e){}
 let fw=null;try{fw=g77FwHM();if(fw!==gameClock().hhmm)bad('לוח הטיסות לא לפי שעון המשחק: '+fw+' / '+gameClock().hhmm)}catch(e){bad('לוח הטיסות: '+e.message)}
 return {ok:!why.length,why:why.slice(0,12),days:[day0,Z.day],rounds,start:{round:A.round,sign:A.sign,signDay:A.signDay},end:{round:Z.round,sign:Z.sign,signDay:Z.signDay,plc:Z.plc,phone:Z.phone.slice(0,220)},tonight,flights:fw,err:LEAGUE4.err()}})()
