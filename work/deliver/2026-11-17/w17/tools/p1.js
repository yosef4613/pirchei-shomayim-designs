(()=>{const o={};const T=(k,f)=>{try{o[k]=f()}catch(e){o[k]='ERR '+String(e&&e.message||e).slice(0,160)}};
T('cat',()=>Object.keys(VEHICLE_CATALOG));
T('refs',()=>Object.keys(fleetTypes()));
T('tcref',()=>Object.keys(TurboCity.ref||{}));
T('scale',()=>['W17-SC','W17-JP','W17-BK','VH-SP-05','VH-SP-02','VH-SP-01','VH-SD-04','VH-PK-02'].map(a=>[a,roadVehicleScaleFor(a,a.startsWith('W17')?a:'Sedan'),roadVehicleScaleFor(a,'Sports'),roadVehicleScaleFor(a,'Pickup')]));
T('info',()=>['W17-JP','W17-SC','W17-BK'].map(a=>{const i=TurboCity.info(a,{scale:1});return[a,i.w,i.h,i.fp]}));
T('c34id',()=>['VH-SP-01','VH-SP-02','VH-SD-04','VH-PK-02','VH-SP-05','W17-SC'].map(a=>{const [L,W]=c34Dims(a,roadVehicleScaleFor(a,'Sedan'));return[a,c34Id(a,L,W)]}));
T('vis',()=>['VH-SP-01','VH-SP-02','VH-SD-04','VH-PK-02','VH-SP-05'].map(a=>[a,!!TurboCity.get(a),(TurboCity.get(a)||{}).pal,((TurboCity.get(a)||{}).rims||[]).join('')]));
T('pl',()=>{const L=p672Pl();return Object.keys(L)});
T('w17look',()=>Object.keys(W17K.look('SC',0)));
T('spr',()=>{const L=JSON.parse(JSON.stringify(p672Pl(),(k,v)=>k.slice(0,2)==='__'?undefined:v));L.hat=W17K.look('SC',0).hat;const e=W17K.sprite('SC',{N:32,k:4,res:1,col:'#c8262b',rider:L,crank:0});return[e.cv.width,e.cv.height,e.riderN]});
T('w17',()=>__TC_W17.list().map(r=>[r.id,r.role,r.ph,r.x,r.y]));
T('extraW17',()=>VehicleWorld.extra.filter(q=>/^W17-/.test(q.asset)).map(q=>[q.id,q.asset,Math.round(q.x),Math.round(q.y),q.cl]));
T('kmh',()=>WORLD_METERS_PER_PX);
T('saveBorrow',()=>{const s=collectSaveState();return Object.keys(s).join(',')+' | wp:'+Object.keys(s.worldPersistent||{}).join(',')});
T('money',()=>[PlayerProfile.money,PlayerProfile.home.garageCapacity,ensureGarageSchema().vehicles.length]);
T('dealerPos',()=>{const s=(typeof D3_SERVICES!=='undefined'?D3_SERVICES:[]);return s.map(q=>[q.id,q.x,q.y])});
T('g7',()=>Object.keys(G7_VEH_HE));
return o})()
