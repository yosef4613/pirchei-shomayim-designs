return (async()=>{const out={};const errs=[];const oe=window.onerror;window.addEventListener('error',e=>errs.push(String(e.message)));
 out.storyType=Array.isArray(window.__TC_STORY)?'array':typeof window.__TC_STORY;out.tcStoryType=Array.isArray(TC_STORY)?'array':typeof TC_STORY;
 if(!PERF.hud)perfHudToggle();
 tcF9Show('events');await new Promise(r=>setTimeout(r,300));const pe=tcF9P('events');out.eventsBad=[...pe.querySelectorAll('.tcF9Bad')].map(x=>x.textContent);out.eventsButtons=pe.querySelectorAll('button').length;
 tcF9Show('zones');await new Promise(r=>setTimeout(r,300));const pz=tcF9P('zones');out.zones=pz.querySelectorAll('details').length;out.zonesBad=[...pz.querySelectorAll('.tcF9Bad')].map(x=>x.textContent).slice(0,5);
 const d=pz.querySelector('details');if(d){d.open=true;await new Promise(r=>setTimeout(r,400));out.firstZone=d.dataset.zone;out.firstBodyLen=d.lastElementChild.innerHTML.length}
 tcF9Show('events');await new Promise(r=>setTimeout(r,300));out.eventsButtons2=pe.querySelectorAll('button').length;
 out.errs=errs;return out})()
