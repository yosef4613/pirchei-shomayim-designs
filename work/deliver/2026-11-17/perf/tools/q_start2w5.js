// q_start2.js — perf 17.11: startMission הראשונה אחרי התיקון (074zv: הקול אחרי הקליק + חימום; 029a: ההד והרעשים רק בהצגה). ‏probe_c2. WARM=1 בשם הקובץ השני (q_start2w.js) — קודם "מגע" של השחקן.
// מודד: startMission הראשונה שמתחילה באמת (הזמן הסינכרוני של הקליק), ואחרי 1.5 שנ׳ — כמה זמן לקח TCSND.ensure (בכל קריאה), TCVOICE.speak, ההודעה הקולית נשמעה ונשמרה;
// השנייה (חם); ואז הצגה אחת (TCSHOW.open film 0) — הזמן של בניית ההד והרעשים (TCSND.st.fx). הכול מוחזר למצב הקודם ככל האפשר.
return (async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms)),o={},T={};const WARM=/*WARM*/1;
 const wrap=(n,get,set)=>{let f;try{f=get()}catch(e){return}if(typeof f!=='function')return;set(function(){const t=performance.now();try{return f.apply(this,arguments)}finally{(T[n]=T[n]||[]).push(+(performance.now()-t).toFixed(1))}})};
 wrap('TCSND.ensure',()=>TCSND.ensure,f=>{TCSND.ensure=f});wrap('TCVOICE.speak',()=>TCVOICE.speak,f=>{TCVOICE.speak=f});
 o.ctx0=!!TCSND.st.ctx;o.audio=PlayerProfile.settings.audio;o.voiceMode=TCVREC.mode;
 if(WARM){window.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));await w(5500);o.afterWarm={ctx:!!TCSND.st.ctx,state:TCSND.st.ctx&&TCSND.st.ctx.state,ensure:(T['TCSND.ensure']||[]).slice(),fx:TCSND.st.fx||null}}
 const ids=Object.keys(MISSION_DEFS).filter(id=>!/^M-ST-/.test(id)&&!MISSION_DEFS[id].retired);o.calls=[];
 for(let k=0;k<2;k++){for(const id of ids){if(o.calls.some(c=>c.id===id))continue;PlayerProfile.activeMission=null;State.navigation=null;const m0=TCVSIDE.st.missions,n0=g77St().msgs.length,e0=(T['TCSND.ensure']||[]).length;
   const t=performance.now();try{startMission(id)}catch(e){}const ms=+(performance.now()-t).toFixed(1);if(!PlayerProfile.activeMission)continue;
   const c={id,ms,voiceGiver:!!(TCVSIDE.S.mis||{})[id]};await w(1500);c.ensure=(T['TCSND.ensure']||[]).slice(e0);c.voiced=TCVSIDE.st.missions-m0;c.msgs=g77St().msgs.length-n0;c.ctx=!!TCSND.st.ctx;
   try{cancelActiveMission()}catch(e){}o.calls.push(c);break}}
 o.fx0=TCSND.st.fx||null;
 try{TCVOICE.stop()}catch(e){}
 try{const ok=TCSHOW.open('film',0);o.showOpen=!!ok;await w(3500);o.fx=TCSND.st.fx||null;o.sessions=TCSND.st.sessions;try{TCSHOW.close&&TCSHOW.close()}catch(e){o.closeErr=String(e).slice(0,80)}}catch(e){o.showErr=String(e).slice(0,160)}
 o.speak=T['TCVOICE.speak']||[];o.ensureAll=T['TCSND.ensure']||[];o.err={vrec:TCVREC.st.err,side:TCVSIDE.st.err,snd:TCSND.st.err};return o})()
