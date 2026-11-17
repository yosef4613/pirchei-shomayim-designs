return (async()=>{await new Promise(r=>setTimeout(r,6000));const o={};
 o.kiss=F2_KISS_SPACES.length;o.removed=S16X.removed;o.ready=APT_OPS.ready;o.clk=APT_OPS.clk;
 try{o.aoN=AO.flights.length;o.aoStands=[...new Set(AO.flights.map(f=>f.stand))].slice(0,30);o.aoInb=AO.flights.filter(f=>f.states&&f.states[0]&&f.states[0][1]==='INBOUND').length}catch(e){o.aoErr=String(e)}
 try{o.next=f2NextArrival()}catch(e){o.nextErr=String(e)}
 o.poi=APT_INTERACTIONS['APT-KISS-PICK'];o.poiKiss=APT_INTERACTIONS['APT-KISS'];
 try{const L=lane2('AIR-FRONT',1,0);o.lane0={ax:L.ax,ay:L.ay,bx:L.bx,by:L.by,w:L.w||L.hw};const L1=lane2('AIR-FRONT',1,1);o.lane1={ax:L1.ax,ay:L1.ay,bx:L1.bx,by:L1.by}}catch(e){o.laneErr=String(e)}
 try{o.s15n=S15SIM.flights.length;o.s15T=S15SIM.T;o.s15homes=S15SIM.flights.map(f=>f.id+':'+f.home+':'+f.kind).slice(0,40)}catch(e){o.s15Err=String(e)}
 try{const P=s15jPlan();o.planFlights=P?P.flights.length:null;o.planSample=P&&P.flights.slice(0,3).map(f=>JSON.stringify(f).slice(0,300))}catch(e){o.planErr=String(e)}
 try{o.doors=S15J_L.doors}catch(e){}
 try{o.car={L:PlayerCar.length||PlayerCar.L,W:PlayerCar.width||PlayerCar.W,asset:PlayerCar.asset,keys:Object.keys(PlayerCar).slice(0,60)}}catch(e){}
 o.mode=PlayerProfile.mode;o.mpp=WORLD_METERS_PER_PX;
 return o})()
