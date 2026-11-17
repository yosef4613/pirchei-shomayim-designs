return (async()=>{const out={};const S9=window.__TC_S9STORY;out.s9=Object.keys(S9.ST).length;const byZ={};for(const [id,s] of Object.entries(S9.ST)){(byZ[s.zone]=byZ[s.zone]||[]).push(id)}out.s9byZone=byZ;
 out.f9ZST=tcF9StoryList().length;out.f9Zones=tcF9ZoneList().map(o=>o.z);
 out.noS9=out.f9Zones.filter(z=>!byZ[z]);out.noAny=out.f9Zones.filter(z=>!byZ[z]&&!tcF9StoryList().some(s=>s.zone===z));
 out.s9NotInF9=Object.keys(byZ).filter(z=>!out.f9Zones.includes(z));
 try{const T=window.__TC_STORY;out.tc=typeof T;out.tcKeys=T?Object.keys(T).slice(0,40):null}catch(e){out.tcErr=String(e)}
 try{out.tcD=typeof TC_STORY!=='undefined'?Object.keys(TC_STORY).slice(0,30):null;out.ch=(TC_STORY.chapters||[]).length}catch(e){}
 const one=Object.values(S9.ST)[5];out.sample={k:Object.keys(one),steps:one.steps.length,start:one.start,hours:one.hours};
 out.zst=typeof window.__TC_ZSTORY;return out})()
