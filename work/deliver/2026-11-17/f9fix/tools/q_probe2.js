return (async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));const out={};const errs=[];window.addEventListener('error',e=>errs.push(String(e.message)));const S9=window.__TC_S9STORY;
 out.s9=Object.keys(S9.ST).length;const byZ={};for(const [id,s] of Object.entries(S9.ST))(byZ[s.zone]=byZ[s.zone]||[]).push(id);out.s9byZone=Object.fromEntries(Object.entries(byZ).map(([z,L])=>[z,L.length]));
 out.liveStories=tcF9StoryList().length;const Z=tcF9ZoneList().map(o=>o.z);out.f9Zones=Z.length;out.zonesNoStory=Z.filter(z=>!byZ[z]&&!tcF9StoryList().some(s=>s.zone===z));out.s9ZonesNotInF9=Object.keys(byZ).filter(z=>!Z.includes(z));
 out.f9zst=Array.isArray(window.__TC_F9ZST)?window.__TC_F9ZST.length:typeof window.__TC_F9ZST;
 if(!PERF.hud)perfHudToggle();tcF9Show('zones');await w(300);const pz=tcF9P('zones');out.summaries=[...pz.querySelectorAll('summary')].slice(0,6).map(s=>s.textContent.replace(/\s+/g,' ').slice(0,140));
 out.summNone=[...pz.querySelectorAll('summary')].filter(s=>/אין סיפורים/.test(s.textContent)).map(s=>s.parentNode.dataset.zone);
 const d=pz.querySelector('details[data-zone="E4"]')||pz.querySelector('details');d.open=true;await w(300);out.e4rows=d.querySelectorAll('[data-q]').length;out.e4text=(d.querySelector('[data-q]')||{}).textContent;
 const qa=d.querySelector('[data-qqa]');if(qa){const m0=PlayerProfile.money,s0=JSON.stringify(PlayerProfile.story);qa.click();await w(100);out.qaOut=(d.querySelector('[data-qout]')||{}).textContent;out.qaSame=PlayerProfile.money===m0&&JSON.stringify(PlayerProfile.story)===s0}
 const t0=performance.now();const R=tcF9CK.quest();out.quest={ok:R.ok,sum:R.sum,ms:Math.round(performance.now()-t0),bad:R.text.split('\n').filter(l=>/✗/.test(l)).slice(0,12)};
 const go=d.querySelector('[data-qgo]');if(go){go.click();await w(200);out.goState=(d.querySelector('[data-qst]')||{}).textContent;out.goCam=[Math.round(Camera.x),Math.round(Camera.y)];out.goNav=State.navigation&&State.navigation.targetId}
 try{const a=f9PanelAudit();out.audit={ok:a.ok,why:a.why.slice(0,4),ms:a.ms}}catch(e){out.audit=String(e)}
 try{const r=clGo('leave');out.leave=r;await w(1500);out.leaveBoard=clBoardText()}catch(e){out.leave=String(e)}
 try{const R=tcF9CK.story();out.story={ok:R.ok,sum:R.sum,bad:R.text.split("\n").filter(l=>/✗/.test(l))}}catch(e){out.story=String(e)}
 out.errs=errs;return out})()
