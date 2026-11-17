// q_of_busy.js (leftovers 17.11) — סרטון הפתיחה מול TCBUSY של missions: "משחק חדש" (tcsave · new) → הסרטון במסך מלא, TCBUSY.top()==='opening' וחוסם כרטיס / הדרכה / אירוע; בסוף הסרטון — 'opening' יורד. node probe_c2.js <build> q_of_busy.js <out.json>
return new Promise(res=>{const W=ms=>new Promise(r=>setTimeout(r,ms));const o={};(async()=>{try{
 o.has={tcbusy:typeof TCBUSY!=='undefined',tcof:typeof TCOF!=='undefined'&&!!TCOF.play,len:typeof TCOF!=='undefined'?TCOF.len:null};
 const sk=window.__TCO_SKIP;window.__TCO_SKIP=false;window.dispatchEvent(new CustomEvent('tcsave',{detail:{slot:1,mode:'story',how:'new'}}));await W(1300);window.__TCO_SKIP=sk;
 const S=TCSHOW.on;o.during={on:!!S,full:!!(S&&S.full),id:S&&S.prod&&S.prod.id,top:TCBUSY.top(),card:TCBUSY.blocks('card'),tut:TCBUSY.blocks('tutorial'),ev:TCBUSY.blocks('event'),isOpening:TCBUSY.is('opening'),auto:TCOF.st.auto};
 let fired=0;TCBUSY.when('card',()=>{fired=performance.now()},'lo-of-busy');o.whenQueued=!fired;
 if(S)S.t=S.total-0.6;for(let i=0;i<40&&TCSHOW.on;i++)await W(250);await W(600);
 o.after={on:!!TCSHOW.on,top:TCBUSY.top(),isOpening:TCBUSY.is('opening'),done:TCOF.st.done,last:TCOF.st.last,whenFired:!!fired,err:TCOF.st.err,busyErr:TCBUSY.state().err};
 o.ok=o.has.tcbusy&&o.has.tcof&&o.during.on&&o.during.full&&o.during.id==='tc-opening'&&o.during.top==='opening'&&o.during.card&&o.during.tut&&o.whenQueued&&!o.after.on&&!o.after.isOpening&&o.after.top!=='opening'&&o.after.done>=1&&!o.after.err;
}catch(e){o.err=String(e&&e.message||e)}res(o)})()})
