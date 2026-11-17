(async()=>{const sl=ms=>new Promise(r=>setTimeout(r,ms)),o={},T=async(k,f)=>{try{o[k]=await f()}catch(e){o[k]='ERR '+String(e&&e.stack||e).slice(0,300)}};
await T('stats0',()=>__TC_W17R.stats());
await T('cat',()=>Object.entries(VEHICLE_CATALOG).map(([k,c])=>k+':'+c.cls+':'+c.price+':'+c.ref));
await T('qa',()=>__TC_W17R.qa());
await T('mode0',()=>PlayerProfile.mode+' '+PlayerCar.asset);
const settle=async()=>{for(let i=0;i<30&&DOORS.seq;i++)await sl(200);if(DOORS.seq)drSeqEnd()};
await T('out0',async()=>{if(PlayerProfile.mode==='vehicle'){PlayerCar.speed=0;exitVehicle();await sl(500);await settle()}return PlayerProfile.mode});
await T('sc',async()=>{const p=VehicleWorld.extra.find(q=>q.asset==='W17-SC'&&!w17rWhyNot(q,false));if(!p)return 'no scooter';PlayerPed.x=p.x+Math.cos((p.heading||0)+Math.PI/2)*16;PlayerPed.y=p.y+Math.sin((p.heading||0)+Math.PI/2)*16;
 await settle();const n=nearestDriveableVehicle(),r=enterVehicle();await sl(1500);await settle();Camera.x=PlayerCar.x;Camera.y=PlayerCar.y;Camera.zoom=4;const d0=W17R.n.drawn;await sl(1500);
 const a={id:p.id,near:n&&n.id,r,mode:PlayerProfile.mode,asset:PlayerCar.asset,col:PlayerCar.state&&PlayerCar.state.w17col,seq:!!DOORS.seq,drawnPerSec:(W17R.n.drawn-d0)/1.5,flat:W17R.n.flat,loan:w17rOnLoan(p.id),usableGuard:W17R.n.loanGuard};
 PlayerCar.speed=900;await sl(400);a.kmh=+carKmh().toFixed(1);PlayerCar.speed=0;await sl(300);a.exit=exitVehicle();await sl(500);await settle();a.mode2=PlayerProfile.mode;a.loanAfterExit=w17rOnLoan(p.id);return a});
await T('pm',async()=>{const p=TRAFFIC_CARS.find(v=>v.w17s&&v.w17s.type==='PM');const q=VehicleWorld.extra.find(v=>v.asset==='W17-CR');const z=q||p;if(!z)return 'none';PlayerPed.x=z.x+12;PlayerPed.y=z.y+4;const n=nearestDriveableVehicle();return{z:z.id,near:n&&n.id,blocked:W17R.blocked}});
await T('jp',async()=>{let c=null;for(let i=0;i<40&&!c;i++){c=w17rOffCands().find(q=>q.id==='W17-JP-1')||w17rOffCands()[0];if(!c)await sl(1000)}if(!c)return 'no cand';
 {let bs=null,bd=-1;for(const a of [Math.PI/2,-Math.PI/2,Math.PI]){const x=c.x+Math.cos(c.heading+a)*20,y=c.y+Math.sin(c.heading+a)*20;let m=1e9;for(const o of allParkedCars())m=Math.min(m,Math.hypot(o.x-x,o.y-y));if(m>bd){bd=m;bs={x,y}}}PlayerPed.x=bs.x;PlayerPed.y=bs.y}await settle();const n=nearestDriveableVehicle(),r=enterVehicle();await sl(1500);await settle();
 return{c:c.id,near:n&&n.id,r,mode:PlayerProfile.mode,asset:PlayerCar.asset,loan:w17rOnLoan(c.id),origin:State.borrowedVehicleOrigin,cands:w17rOffCands().map(q=>q.id)}});
await T('buy',async()=>{PlayerCar.speed=0;if(PlayerProfile.mode==='vehicle'){exitVehicle();await sl(500);await settle()}const D=(typeof D3_SERVICES!=='undefined'?D3_SERVICES:[]).find(s=>s.id==='D3-DEALER');
 const sv=nearbyD3Service;PlayerProfile.money=300000;PlayerProfile.home.garageCapacity=8;const n0=ensureGarageSchema().vehicles.length;
 nearbyD3Service=()=>({id:'D3-DEALER'});try{buyDealerVehicle('VH-SP-05');buyDealerVehicle('W17-SC');buyDealerVehicle('W17-JP');if(VEHICLE_CATALOG['VH-SP-06'])buyDealerVehicle('VH-SP-06')}finally{nearbyD3Service=sv}
 return{n0,n1:ensureGarageSchema().vehicles.length,v:ensureGarageSchema().vehicles.map(v=>v.vehicleId),money:PlayerProfile.money}});
await T('stats1',()=>__TC_W17R.stats());
await T('w17err',()=>[W17.err,W17.errN]);
return o})()
