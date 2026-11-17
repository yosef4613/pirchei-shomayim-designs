return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);
 await S(4000);o.qa=PF2.qa();o.pier=PIERX.walk();o.pierErr=PIERX.err();
 try{if(PlayerProfile.mode!=='vehicle'){L('mode '+PlayerProfile.mode)}try{setPhoneOpen(false)}catch(e){}PlayerProfile.mode='vehicle';PlayerProfile.activeMission=null;PlayerCar.x=6300;PlayerCar.y=1232;PlayerCar.heading=0;PlayerCar.speed=0;
  startMission('M-F2-PICKUP');const m=PlayerProfile.activeMission;if(!m){o.fail='לא התחילה';return o}L('started '+m.id+' stage '+m.stage+' flight '+m.f2.flight+' s15 '+JSON.stringify(m.f2.s15)+' tReady-now '+(m.f2.tReady-APT_OPS.clk).toFixed(1));
  PlayerCar.x=6440;PlayerCar.y=1232;PlayerCar.heading=0;PlayerCar.speed=0;
  let t0=performance.now(),last='';for(let i=0;i<900;i++){await S(1000);const mm=PlayerProfile.activeMission;PlayerCar.speed=0;if(!mm){L('mission ended (no active)');break}
   const w=F2_PICKUP.walker,s=mm.stage+' | '+(w?('walker '+Math.round(w.x)+','+Math.round(w.y)+' '+w.state):'no walker')+' | rem '+Math.round(mm.timeRemaining);if(s.split('|')[0]!==last.split('|')[0]||(w&&!last.includes('walker'))||i%30===0)L(s);last=s;
   if(mm.stage==='drive'){L('boarded · dest '+mm.f2.dest);const t=navPoiRegistry()[mm.f2.dest];PlayerCar.x=t.x;PlayerCar.y=t.y;PlayerCar.speed=0;await S(1500);L('after teleport: active '+(PlayerProfile.activeMission?PlayerProfile.activeMission.stage:'none'));break}}
  o.done=PlayerProfile.progression?.completedMissions?.slice(-3);o.persist=PlayerProfile.worldPersistent?.airportTerminal;o.st=PF2.st;o.err=PF2.err()}catch(e){o.exc=String(e&&e.stack||e).slice(0,500)}
 return o})()
