// q_accept.js — perf 17.11: קבלת משימה (startMission) — כמה זמן, ומה בתוכה (הממצא של missions: שיא 116 מ"ש). ‏probe_c2 / zoomcycle QX.
// עוטף לזמן המדידה בלבד: setNavigationTarget, ‏recalcNavigation, ‏navPoiRegistry, ‏renderPhone, ‏toast, ‏SaveManager.log / save, ‏updateHud, ‏Dbg.event;
// לכל משימה (עד 6 משימות עבודה שאפשר להתחיל) — startMission, ואחר כך מנקה (activeMission ו-navigation חוזרים למה שהיה).
return (async()=>{const o={};const acc={},cnt={};const W=[];
 const wrap=(name,get,set)=>{let f;try{f=get()}catch(e){return}if(typeof f!=='function')return;const w=function(){const t=performance.now();try{return f.apply(this,arguments)}finally{const d=performance.now()-t;acc[name]=(acc[name]||0)+d;cnt[name]=(cnt[name]||0)+1}};try{set(w);W.push(()=>set(f))}catch(e){(o.noWrap||(o.noWrap=[])).push(name)}};
 wrap('setNavigationTarget',()=>setNavigationTarget,f=>{setNavigationTarget=f});wrap('recalcNavigation',()=>recalcNavigation,f=>{recalcNavigation=f});wrap('navPoiRegistry',()=>navPoiRegistry,f=>{navPoiRegistry=f});
 wrap('renderPhone',()=>renderPhone,f=>{renderPhone=f});wrap('toast',()=>toast,f=>{toast=f});wrap('SaveManager.log',()=>SaveManager.log,f=>{SaveManager.log=f});wrap('SaveManager.save',()=>SaveManager.save,f=>{SaveManager.save=f});
 wrap('updateHud',()=>updateHud,f=>{updateHud=f});wrap('Dbg.event',()=>Dbg.event,f=>{Dbg.event=f});wrap('renderMissionPanel',()=>renderMissionPanel,f=>{renderMissionPanel=f});
 const am=PlayerProfile.activeMission,nav=State.navigation;
 try{const ids=Object.keys(MISSION_DEFS).filter(id=>!/^M-ST-/.test(id));o.defs=ids.length;o.calls=[];let k=0;
  for(const id of ids){if(k>=6)break;PlayerProfile.activeMission=null;State.navigation=null;for(const x in acc){acc[x]=0;cnt[x]=0}
   const t=performance.now();let r,er=null;try{r=startMission(id)}catch(e){er=String(e).slice(0,160)}const ms=performance.now()-t;
   if(!PlayerProfile.activeMission&&!er)continue;k++;
   o.calls.push({id,ms:+ms.toFixed(1),started:!!PlayerProfile.activeMission,er,in:Object.fromEntries(Object.entries(acc).filter(([x,v])=>v>0.05).map(([x,v])=>[x,+v.toFixed(1)+'×'+cnt[x]]))})}
 }catch(e){o.err=String(e&&e.stack||e).slice(0,500)}
 finally{for(const u of W.reverse())try{u()}catch(e){}PlayerProfile.activeMission=am;State.navigation=nav}
 return o})()
