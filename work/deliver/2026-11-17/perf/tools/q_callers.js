// q_callers.js — perf 17.11: מי קורא ל-navPoiRegistry ~100 פעמים בשנייה (navday: 15,555 קריאות ב-2.5 דק׳; השיאים של איסוף הזבל — בתוכה).
// node qa_tools/probe_c2.js <game.html> q_callers.js <out.json> — 20 שנ׳ של משחק רגיל (בלי הלוח המאולץ), ואחר כך 20 שנ׳ עם הלוח והסיפור (כמו mb_day): לכל קריאה — 3 הפונקציות שמעליה;
// וגם: כמה בתים מוקצים לכל קריאה (performance.memory לפני / אחרי, על 200 קריאות ברצף) — והאם התוצאה זהה בין שתי קריאות באותו פריים (כדי לדעת אם מטמון לפריים בטוח).
return (async()=>{const o={};const f0=navPoiRegistry;let on=false;const C={};
 navPoiRegistry=function(){if(on){const st=String(new Error().stack).split('\n').slice(2,5).map(l=>{const m=l.match(/at (?:async )?([\w$.<>]+)/);return m?m[1]:'?'}).join(' < ');C[st]=(C[st]||0)+1}return f0.apply(this,arguments)};
 const run=async(ms)=>{for(const k in C)delete C[k];on=true;const t=performance.now();await new Promise(r=>setTimeout(r,ms));on=false;const s=(performance.now()-t)/1000,n=Object.values(C).reduce((a,b)=>a+b,0);
  return{sec:+s.toFixed(1),perSec:+(n/s).toFixed(1),top:Object.entries(C).sort((a,b)=>b[1]-a[1]).slice(0,10).map(([k,v])=>[k,+(v/s).toFixed(1)])}};
 try{o.idle=await run(20000);
  try{const MB=window.__TC_MB;if(MB){MB.force(true);try{__TC_STORY.jump('1-3')}catch(e){}}}catch(e){}
  o.story=await run(20000);
  navPoiRegistry=f0;
  const N=200,h0=performance.memory.usedJSHeapSize,t0=performance.now();let x=null;for(let i=0;i<N;i++)x=navPoiRegistry();o.each={ms:+((performance.now()-t0)/N).toFixed(3),kb:Math.round((performance.memory.usedJSHeapSize-h0)/N/1024),pois:Object.keys(x).length};
  const a=navPoiRegistry(),b=navPoiRegistry();o.same=JSON.stringify(a)===JSON.stringify(b);
 }catch(e){o.err=String(e&&e.stack||e).slice(0,400)}finally{navPoiRegistry=f0}
 return o})()
