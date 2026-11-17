return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(s),OLD='-K'+'ISS';
 await S(3000);
 try{
  const reg=navPoiRegistry();o.poi={drop:!!reg['APT-DROP'],pick:!!reg['APT-DROP-PICK'],oldDrop:!!reg['APT'+OLD],oldPick:!!reg['APT'+OLD+'-PICK']};
  o.def={pickup:MISSION_DEFS['M-F2-PICKUP']&&MISSION_DEFS['M-F2-PICKUP'].pickup};
  o.spaces=typeof F2_DROP_SPACES!=='undefined'?F2_DROP_SPACES.map(s=>s.id):'missing';
  // 1. start M-F2-PICKUP (as the pier test does), navigate to the pick-up point
  try{setPhoneOpen(false)}catch(e){}PlayerProfile.mode='vehicle';PlayerProfile.activeMission=null;PlayerCar.x=6300;PlayerCar.y=1232;PlayerCar.heading=0;PlayerCar.speed=0;
  startMission('M-F2-PICKUP');const m=PlayerProfile.activeMission;o.started=m?{id:m.id,stage:m.stage,pickup:m.pickup||m.def?.pickup||null}:null;
  try{setNavigationTarget('APT-DROP-PICK',{mission:true,silent:true})}catch(e){L('nav '+e)}
  // 2. build an "old" save: the same state, with the ids as before S7F301
  const cur=collectSaveState();const js=JSON.stringify(cur);o.curHasNew=(js.match(/(APT|F2|PAX)-DROP/g)||[]).length;
  let oldJs=js.replace(/\b(APT|F2|PAX)-DROP\b/g,(mm,p)=>p+OLD);
  const old=JSON.parse(oldJs);old.progression=old.progression||{};old.progression.discoveredPois=(old.progression.discoveredPois||[]).concat(['APT'+OLD,'APT'+OLD+'-PICK']);
  old.__oldNav={target:'APT'+OLD+'-PICK',poi:'F2'+OLD+'-LANE',pax:'F2-PAX'+OLD+'-1'};
  o.oldHas=(JSON.stringify(old).match(new RegExp('(APT|F2|PAX)'+OLD,'g'))||[]).length;
  PlayerProfile.activeMission=null;
  const before=SAVE_IDMAP.n;let r;try{r=TurboCitySave.importData(old)}catch(e){r={exc:String(e)}}
  await S(1500);
  o.import=r;o.mapped=SAVE_IDMAP.n-before;
  const after=JSON.stringify(collectSaveState());o.afterOld=(after.match(new RegExp('(APT|F2|PAX)'+OLD,'g'))||[]).length;o.afterNew=(after.match(/(APT|F2|PAX)-DROP/g)||[]).length;
  const am=PlayerProfile.activeMission;o.resumed=am?{id:am.id,stage:am.stage}:null;o.disc=(PlayerProfile.progression.discoveredPois||[]).filter(x=>/APT-(DROP|K)/.test(x));
  o.nav=State.navigation?{target:State.navigation.target||State.navigation.id||null}:null;
  o.ok=!!(o.poi.drop&&o.poi.pick&&!o.poi.oldPick&&o.def.pickup==='APT-DROP-PICK'&&r&&r.ok&&o.mapped>0&&o.afterOld===0&&o.resumed&&o.resumed.id==='M-F2-PICKUP');
 }catch(e){o.exc=String(e&&e.stack||e).slice(0,600)}
 try{o.err=(window.__TC_DEV&&__TC_DEV.errors)?__TC_DEV.errors().length:null}catch(e){}
 return o})()
