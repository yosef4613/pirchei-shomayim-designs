// q_fwhm.js — merge3 (17.11): הוכחה דטרמיניסטית לבאג העיגול של לוח הטיסות (g77FwHM מול gameClock().hhmm) — אותה השוואה של q_stadium3,
// בשעות משחק עם חלק עשרוני ידוע של הדקה (07:00 + ‎.1 / .3 / .45 / .55 / .7 / .9). הרצה: node W/qa_tools/probe_c2.js <build> q_fwhm.js <out.json>
return (async()=>{const C=G84_CLOCK,out=[];const w=g84WorldS();const keep=C.base;
 for(const f of [.1,.3,.45,.55,.7,.9]){C.base=(420+f)-g84WorldS()*C.rate;let fw=null,e=null;try{fw=g77FwHM()}catch(x){e=String(x).slice(0,120)}
  const c=gameClock();out.push({frac:f,clock:c.hhmm,min:c.min,board:fw,same:fw===c.hhmm,e})}
 C.base=keep;return{build:(window.TC_BUILD_ID||(document.title||'')).toString().slice(0,60),fidsOn:(()=>{try{return s15paxFidsOn()}catch(x){return 'ERR '+x.message}})(),rows:out,mismatch:out.filter(r=>!r.same).map(r=>r.frac)}})()
