// story56 · הבדיקה המהירה: הסיפור כולו במנוע (story_main_chapter1), story56 (המקומות / הנעילות / הקישוריות), הסצנות, הנעילות, ההקלטות
return (()=>{const R={};const T=(k,f)=>{try{R[k]=f()}catch(e){R[k]={error:String(e&&e.stack||e).slice(0,500)}}};
T('story',()=>{const q=__TC_STORY.qa();return{ok:q.ok,why:q.why,steps:q.steps,done:q.done,built:q.built,chapter:q.chapter,ms:q.ms,error:q.error,voiceMissing:q.voiceMissing,money:q.money,log:(q.log||[]).slice(-12).join(' ')}});
T('s56',()=>__TC_S56.qa());
T('cuts',()=>{const q=TCCUT.qa();return{ok:q.ok,why:q.why,scenes:q.scenes,chapters:q.chapters,warn:q.warn,error:q.error}});
T('locks',()=>{const q=__TC_STORY.qaLocks();return{ok:q.ok,why:q.why,error:q.error}});
T('lockphys',()=>{const q=TCLOCK.qa();return{ok:q.ok,why:q.why,nav:q.nav&&{steps:q.nav.steps,bad:q.nav.bad,wait:q.nav.wait,waits:q.nav.waits},error:q.error}});
T('vrec',()=>TCVREC_ST.audit());
T('engine',()=>__TC_STORY.stats());
T('s56st',()=>({err:__TC_S56.ST.err,errs:__TC_S56.ST.errs}));
T('wx',()=>({kinds:WEATHER.KINDS,ov:WEATHER.state.override}));
return JSON.stringify(R)})()
