return (async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));const out={};const errs=[];window.addEventListener('error',e=>errs.push(String(e.message)));
 if(!PERF.hud)perfHudToggle();tcF9Show('checks');await w(200);
 for(const k of ['live','story']){const t0=performance.now();let r;try{r=tcF9CK[k]()}catch(e){r={ok:false,sum:'שגיאה: '+e.message}}out[k]={ok:r.ok,sum:r.sum,ms:Math.round(performance.now()-t0),bad:(r.text||'').split('\n').filter(l=>/✗/.test(l)).slice(0,8)}}
 out.zst=tcF9StoryList().length;out.zstIds=tcF9StoryList().map(s=>s.zone+':'+s.id);out.engine=typeof window.__TC_STORY==='object'&&!Array.isArray(window.__TC_STORY)&&typeof window.__TC_STORY.state==='function';
 try{out.textAudit=s266TextAudit().issues}catch(e){out.textAudit=String(e)}out.build=BUILD;
 out.errs=errs;return out})()
