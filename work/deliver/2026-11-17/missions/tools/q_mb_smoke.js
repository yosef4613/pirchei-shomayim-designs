return (()=>{const R={};const T=(k,f)=>{try{R[k]=f()}catch(e){R[k]={error:String(e&&e.stack||e).slice(0,500)}}};
T('mb',()=>__TC_MB.qa());
T('story',()=>{const q=__TC_STORY.qa();return{ok:q.ok,why:q.why,steps:q.steps,done:q.done,built:q.built,chapter:q.chapter,ms:q.ms,error:q.error,log:(q.log||[]).join(' ')}});
T('locks',()=>__TC_STORY.qaLocks());
T('zs',()=>{const z=__TC_ZSTORY.check();return{ok:z.ok,n:z.n,bad:z.bad.slice(0,6)}});
T('zsfix',()=>__TC_ZSFIX.check());
T('mmis',()=>__TC_MMIS?{err:__TC_MMIS.S.err,n:__TC_MMIS.S.list.length}:null);
T('state',()=>__TC_MB.state());
T('storyErr',()=>__TC_STORY.state());
return JSON.stringify(R)})()
