// q_npr.js — perf 17.11: NPR בדפדפן — כמה בניות של navPoiRegistry בזמן ציורי המפה, וכמה קריאות קיבלו את הרשימה הקיימת (15 שנ׳ של משחק רגיל, ועוד 15 עם הלוח והסיפור).
// node qa_tools/probe_c2.js <game.html> q_npr.js <out.json>
return (async()=>{const N=window.__TC_PERFX&&window.__TC_PERFX.npr;if(!N)return{err:'אין __TC_PERFX.npr'};const s=()=>({b:N.builds,h:N.hits});const o={wrapped:N.wrapped,on:N.on,err:N.err};
 const a=s();await new Promise(r=>setTimeout(r,15000));const b=s();o.idle={builds:b.b-a.b,hits:b.h-a.h,perSec:+((b.b-a.b+b.h-a.h)/15).toFixed(1)};
 try{const MB=window.__TC_MB;if(MB){MB.force(true);try{__TC_STORY.jump('1-3')}catch(e){}}}catch(e){}
 const c=s();await new Promise(r=>setTimeout(r,15000));const d=s();o.story={builds:d.b-c.b,hits:d.h-c.h};
 try{const op=State.phoneOpen;if(typeof setPhoneOpen==='function'){setPhoneOpen(true);const e=s();await new Promise(r=>setTimeout(r,5000));const f=s();setPhoneOpen(!!op);o.phone={builds:f.b-e.b,hits:f.h-e.h}}}catch(e){o.phoneErr=String(e).slice(0,120)}
 return o})()
