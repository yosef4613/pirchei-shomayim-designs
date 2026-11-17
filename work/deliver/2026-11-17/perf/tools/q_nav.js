// q_nav.js — perf 17.11: מה עולה הניווט בקבלת משימה (הממצא של missions: שיא 116 מ"ש ב-setNavigationTarget). ‏node qa_tools/probe_c2.js <build> q_nav.js <out.json>
// בתוך המשחק: עוטף לזמן המדידה בלבד (ומחזיר בסוף) את navPoiRegistry, ‏recalcNavigation, ‏shortestNodePath, ‏nearestRoadNode, ‏renderPhone, ‏toast, ‏SaveManager.log,
// וקורא ל-setNavigationTarget ליעדים רחוקים — הפעם הראשונה (קר) והפעמים הבאות; לכל קריאה — הזמן הכולל ומה בתוכו.
return (async()=>{const o={nodes:NODES.length,edges:EDGES.length};const acc={},cnt={};const W=[];
 const wrap=(name,get,set)=>{const f=get();if(typeof f!=='function')return;const w=function(){const t=performance.now();try{return f.apply(this,arguments)}finally{const d=performance.now()-t;acc[name]=(acc[name]||0)+d;cnt[name]=(cnt[name]||0)+1}};try{set(w);W.push(()=>set(f))}catch(e){(o.noWrap||(o.noWrap=[])).push(name)}};
 wrap('navPoiRegistry',()=>navPoiRegistry,f=>{navPoiRegistry=f});wrap('recalcNavigation',()=>recalcNavigation,f=>{recalcNavigation=f});
 wrap('shortestNodePath',()=>shortestNodePath,f=>{shortestNodePath=f});wrap('nearestRoadNode',()=>nearestRoadNode,f=>{nearestRoadNode=f});
 wrap('renderPhone',()=>renderPhone,f=>{renderPhone=f});wrap('toast',()=>toast,f=>{toast=f});wrap('SaveManager.log',()=>SaveManager.log,f=>{SaveManager.log=f});
 wrap('b5PedRoute',()=>b5PedRoute,f=>{b5PedRoute=f});
 const sv=State.navigation?JSON.parse(JSON.stringify(State.navigation)):null,am=PlayerProfile.activeMission;
 try{
  const R=navPoiRegistry();o.pois=Object.keys(R).length;const a=playerActor();o.player=[Math.round(a.x),Math.round(a.y),PlayerProfile.mode];
  const ids=Object.keys(R).filter(k=>!R[k].hidden&&!/^(D5-FK-|ACT-)/.test(k));ids.sort((x,y)=>Math.hypot(R[y].x-a.x,R[y].y-a.y)-Math.hypot(R[x].x-a.x,R[x].y-a.y));
  const pick=[ids[0],ids[1],ids[Math.floor(ids.length*.3)],ids[Math.floor(ids.length*.6)],ids[ids.length-1]].filter(Boolean);
  PlayerProfile.activeMission=null;o.calls=[];
  const SE=(typeof TCSTORY!=='undefined'&&TCSTORY.E)||null,mo=SE?SE.modeOv:null;o.storyHandle=!!SE;
  for(const md of ['open','story'])for(const rep of [0,1,2])for(const id of pick){if(SE)SE.modeOv=md==='story'?'story':mo;for(const k in acc){acc[k]=0;cnt[k]=0}const t=performance.now();let r;try{r=setNavigationTarget(id,{mission:true})}catch(e){r='err '+e}const ms=performance.now()-t;
   o.calls.push({md,rep,id,ms:+ms.toFixed(1),ok:r===true,pts:State.navigation&&State.navigation.points&&State.navigation.points.length,in:Object.fromEntries(Object.entries(acc).filter(([k,v])=>v>0.05).map(([k,v])=>[k,+v.toFixed(1)+'×'+cnt[k]]))})}
  if(SE)SE.modeOv=mo;
  // the registry alone, and with the phone open
  {const r=[];for(let i=0;i<5;i++){const t=performance.now();navPoiRegistry();r.push(performance.now()-t)}r.sort((x,y)=>x-y);o.registryMs=+r[2].toFixed(2)}
  try{const op=State.phoneOpen;if(!op&&typeof setPhoneOpen==='function')setPhoneOpen(true);for(const k in acc){acc[k]=0;cnt[k]=0}const t=performance.now();setNavigationTarget(pick[2],{mission:true});o.withPhone={ms:+(performance.now()-t).toFixed(1),in:Object.fromEntries(Object.entries(acc).filter(([k,v])=>v>0.05).map(([k,v])=>[k,+v.toFixed(1)+'×'+cnt[k]]))};if(!op&&typeof setPhoneOpen==='function')setPhoneOpen(false)}catch(e){o.phoneErr=String(e).slice(0,200)}
  if(typeof PERF17!=='undefined')o.perf17=PERF17.stats;
 }catch(e){o.err=String(e&&e.stack||e).slice(0,600)}
 finally{try{if(typeof TCSTORY!=='undefined'&&TCSTORY.E&&o.storyHandle)TCSTORY.E.modeOv=null}catch(e){}for(const u of W.reverse())try{u()}catch(e){}PlayerProfile.activeMission=am;State.navigation=sv}
 return o})()
