/* Turbo City B4 — independent, offline 3D asset experiment. Original integration code. */
(()=>{'use strict';
const $=id=>document.getElementById(id), B=BABYLON, V=(x=0,y=0,z=0)=>new B.Vector3(x,y,z);
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)), lerp=(a,b,t)=>a+(b-a)*t;
const ASSETS=JSON.parse($('asset-data').textContent), AUDIT={loaded:[],failures:[],trees:0,models:0,frames:0};
const key={}, colliders=[], worldLabels=[], lampBulbs=[], nightLights=[], roads=[];
let engine,scene,orbit,driveCam,streetCam,sun,hemi,shadow,player,playerHalo;
let mode='orbit',night=false,low=false,paused=false,started=false,speed=0,heading=Math.PI/2,elapsed=0;
let money=2500,job=0,jobDone=false,toastUntil=0;
const lamps=[],people=[],traffic=[],templates={};
const sites=[
 {id:'N1',name:'רחוב בית הספר 4',use:'מגורים',asset:'commercial',x:-43,z:26,w:13,ys:.84},
 {id:'N0',name:'שדרת המערב 12',use:'מגורים',asset:'houseK',x:-43,z:5,w:12,ys:.92},
 {id:'N2',name:'רחוב השכונה 6',use:'מגורים',asset:'commercial',x:31,z:26,w:12,ys:.84},
 {id:'N3',name:'רחוב השכונה 10',use:'מגורים',asset:'houseB',x:51,z:13,w:16,ys:1.2},
 {id:'S1',name:'שוק העיר',use:'סופר שכונתי',asset:'houseQ',x:-43,z:-29,w:18,ys:.72},
 {id:'S2',name:'מרפאת השכונה',use:'מרפאה',asset:'houseH',x:-12,z:-29,w:15,ys:.76},
 {id:'S3',name:'בית ספר השכונה',use:'בית ספר',asset:'houseB',x:37,z:-29,w:22,ys:.82}
];
const demo={version:'B4-DOWNTOWN-R3',ready:false,get state(){return {ready:started,mode,night,low,paused,speed,heading,money,job,jobDone,player:player?{x:player.position.x,y:player.position.y,z:player.position.z}:null,assets:AUDIT.loaded.length,failures:AUDIT.failures.slice(),trees:AUDIT.trees,instances:AUDIT.models,meshes:scene?.meshes.length,frames:AUDIT.frames}},setMode,reset,night:()=>setNight(!night),pause:()=>{paused=!paused;return paused},teleport:(x,z)=>{player.position.set(x,.25,z);speed=0},snapshot:()=>JSON.parse(JSON.stringify(demo.state))};
window.TurboB4=demo;

function material(name,hex,rough=1){const m=new B.StandardMaterial(name,scene);m.diffuseColor=B.Color3.FromHexString(hex);m.specularColor=new B.Color3(.035,.035,.035);m.roughness=rough;return m}
const mats={};
function box(name,x,y,z,w,h,d,m,collide=false){const o=B.MeshBuilder.CreateBox(name,{width:w,height:h,depth:d},scene);o.position.set(x,y,z);o.material=typeof m==='string'?mats[m]:m;o.receiveShadows=true;o.isPickable=false;if(collide)colliders.push({x,z,w:w/2,d:d/2});return o}
function cylinder(name,x,y,z,r,h,m,sides=12){const o=B.MeshBuilder.CreateCylinder(name,{diameter:r*2,height:h,tessellation:sides},scene);o.position.set(x,y,z);o.material=typeof m==='string'?mats[m]:m;o.isPickable=false;o.receiveShadows=true;return o}
function pathRect(x,z,w,d,m,y=.11){return box('surface',x,y,z,w,.08,d,m)}
function road(x,z,w,d){roads.push({x,z,w,d});pathRect(x,z,w+2.8,d+2.8,'curb',.04);pathRect(x,z,w,d,'asphalt',.12)}
function sign(text,x,y,z,w=10,color='#203b39',billboard=false){
 const cv=document.createElement('canvas');cv.width=512;cv.height=128;const c=cv.getContext('2d');
 c.fillStyle=color;c.fillRect(0,0,512,128);c.strokeStyle='#d9e6cb';c.lineWidth=5;c.strokeRect(6,6,500,116);
 c.fillStyle='#f8f7e9';c.font='bold 44px Arial';c.textAlign='center';c.textBaseline='middle';c.direction='rtl';c.fillText(text,256,65,470);
 const tex=new B.DynamicTexture('sign:'+text,cv,scene,false);tex.hasAlpha=false;
 const m=new B.StandardMaterial('signmat',scene);m.diffuseTexture=tex;m.emissiveColor=B.Color3.FromHexString('#abbeb3').scale(.38);m.specularColor=B.Color3.Black();m.backFaceCulling=false;
 const p=B.MeshBuilder.CreatePlane('label:'+text,{width:w,height:w/4,sideOrientation:B.Mesh.DOUBLESIDE},scene);p.material=m;p.position.set(x,y,z);p.isPickable=false;
 if(billboard){p.billboardMode=B.Mesh.BILLBOARDMODE_ALL;worldLabels.push(p)}else p.rotation.y=Math.PI;
 return p;
}

// Decode and verify the embedded GLB before handing any bytes to the loader.
async function checkedAssetBytes(asset) {
  const url = new URL(asset.url, location.href).href;
  const unavailable = () => new Error('לא ניתן לטעון את קובץ הדגם. אם מופיע דף סינון, יש להעביר את הכתובת לבדיקה: ' + url);
  let response;
  try { response = await fetch(url); } catch { throw unavailable(); }
  if (!response.ok || (response.headers.get('content-type') || '').includes('text/html')) {
    throw unavailable();
  }
  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.length !== asset.byteLength || bytes.length < 20) throw unavailable();
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  if (view.getUint32(0, true) !== 0x46546c67 || view.getUint32(4, true) !== 2 ||
      view.getUint32(8, true) !== bytes.length) throw unavailable();
  let hash = 2166136261;
  for (const value of bytes) hash = Math.imul(hash ^ value, 16777619) >>> 0;
  if (hash !== asset.checksum32) throw unavailable();
  let offset = 12;
  while (offset < bytes.length) {
    if (offset + 8 > bytes.length) throw unavailable();
    const length = view.getUint32(offset, true);
    if (length % 4 || offset + 8 + length > bytes.length) throw unavailable();
    offset += 8 + length;
  }
  if (globalThis.crypto && globalThis.crypto.subtle && asset.sha256) {
    const digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);
    const actual = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
    if (actual !== asset.sha256) throw unavailable();
  }
  return bytes;
}

async function loadAssets(){
 const entries=Object.entries(ASSETS);let n=0;
 for(const [id,a] of entries){
  $('loadText').textContent='טוען דגמים מהקובץ · '+(++n)+' / '+entries.length;
  $('loadBar').style.width=Math.round(n/entries.length*82)+'%';
  try{
   const bytes=await checkedAssetBytes(a);
   const con=await B.SceneLoader.LoadAssetContainerAsync('',bytes,scene,undefined,'.glb');
   for(const m of con.meshes){m.isPickable=false;m.receiveShadows=true}
   for(const m of con.materials){m.backFaceCulling=false;if(m.maxSimultaneousLights!==undefined)m.maxSimultaneousLights=4}
   templates[id]={con,bounds:a.bounds};AUDIT.loaded.push(id);
  }catch(e){AUDIT.failures.push(id+': '+e.message);throw new Error('טעינת הדגם '+id+' נכשלה: '+e.message)}
 }
}

function model(id,name,x,z,size,rot=0,axis='x',y=.2,ys=1){
 const t=templates[id];if(!t)throw new Error('missing '+id);
 const b=t.bounds,dim=b.dimensions,idx=axis==='y'?1:axis==='z'?2:0,s=size/dim[idx];
 const root=new B.TransformNode(name,scene),pivot=new B.TransformNode(name+':pivot',scene);pivot.parent=root;
 pivot.scaling.set(s,s*ys,s);pivot.position.set(-(b.min[0]+b.max[0])/2*s,-b.min[1]*s*ys,-(b.min[2]+b.max[2])/2*s);
 const inst=t.con.instantiateModelsToScene(n=>name+':'+n,false,{doNotInstantiate:false});
 inst.rootNodes.forEach(n=>{n.parent=pivot});
 root.position.set(x,y,z);root.rotation.y=rot;
 for(const m of root.getChildMeshes()){m.isPickable=false;m.receiveShadows=true;if(shadow)shadow.addShadowCaster(m)}
 root.metadata={asset:id,width:dim[0]*s,depth:dim[2]*s,height:dim[1]*s*ys};AUDIT.models++;return root;
}

function streetLamp(x,z,rot=0){
 const p=cylinder('lamp-post',x,2.6,z,.075,5.2,'metal',8);
 const arm=box('lamp-arm',x+Math.sin(rot)*.65,5.18,z+Math.cos(rot)*.65,.12,.12,1.4,'metal');arm.rotation.y=rot;
 const light=box('lamp-light',x+Math.sin(rot)*1.2,5.08,z+Math.cos(rot)*1.2,.55,.1,.85,'lamp');light.rotation.y=rot;lampBulbs.push(light);
 lamps.push([x,z]);return p;
}
function bench(x,z,rot=0){const root=new B.TransformNode('park-bench',scene);for(const [a,b,c,w,h,d,m] of [[0,.62,0,2,.12,.6,'wood'],[0,1,-.26,2,.5,.1,'wood'],[-.75,.3,0,.1,.6,.5,'metal'],[.75,.3,0,.1,.6,.5,'metal']]){const o=box('bench',a,b,c,w,h,d,m);o.parent=root}root.position.set(x,.16,z);root.rotation.y=rot}
function tree(id,x,z,h,angle=0){const o=model(id,'tree',x,z,h,angle,'y');AUDIT.trees++;return o}

function buildGround(){
 box('island-base',0,-1.25,0,158,2.5,126,'base');pathRect(0,0,157,125,'grass',.025);
 // A single district, with connected outer streets and two neighborhood streets.
 road(0,51,140,10);road(0,-51,140,10);road(-65,0,10,112);road(65,0,10,112);
 road(0,-8,130,9);road(12,0,9,102);
 for(let x=-57;x<=57;x+=7){pathRect(x,51,3,.15,'paint',.18);pathRect(x,-51,3,.15,'paint',.18)}
 for(let z=-42;z<=42;z+=7){pathRect(-65,z,.15,3,'paint',.18);pathRect(65,z,.15,3,'paint',.18);if(Math.abs(z+8)>7)pathRect(12,z,.15,3,'paint',.18)}
 for(let x=-55;x<58;x+=7)if(Math.abs(x-12)>8)pathRect(x,-8,3,.12,'paint',.18);
 // Zebra crossings are real horizontal geometry.
 for(const z of [-15,-1])for(let x=7;x<=17;x+=1.5)pathRect(x,z,.85,3.3,'white',.2);
 for(const x of [5,19])for(let z=-12;z<=-4;z+=1.5)pathRect(x,z,3.2,.85,'white',.2);
 for(const x of [-55,55])for(let z=47;z<=55;z+=1.5)pathRect(x,z,3.2,.85,'white',.2);
 // Distinct, usable parcels around the free models.
 for(const s of sites){const nw=s.id==='S3'?27:s.id==='S1'?25:22,nd=s.id[0]==='N'?21:23;
  pathRect(s.x,s.z,nw,nd,'paving',.09);pathRect(s.x,s.z-nd/2-1,4,4,'paving',.11);
 }
 pathRect(-16,25,23,29,'park',.12);
 pathRect(-16,25,3,29,'sand',.17);pathRect(-16,27,23,2,'sand',.17);
 // Courtyard fountain and a small playground.
 cylinder('fountain-rim',-16,.38,27,3.4,.5,'stone',32);cylinder('water',-16,.66,27,2.9,.09,'water',32);
 cylinder('fountain-column',-16,1.05,27,.34,.9,'stone');cylinder('upper-bowl',-16,1.6,27,1.2,.15,'stone',24);
 const jet=B.MeshBuilder.CreateCylinder('water-jet',{diameter:.1,height:1.7,tessellation:8},scene);jet.position.set(-16,2.3,27);jet.material=mats.water;jet.isPickable=false;
 bench(-22,23,Math.PI/2);bench(-10,23,-Math.PI/2);bench(-22,32,Math.PI/2);bench(-10,32,-Math.PI/2);
 pathRect(-16,14,11,6,'sand',.17);
 for(const x of [-19,-14]){cylinder('swing-pole',x,1.8,14,.09,3.4,'teal',8);cylinder('swing-pole',x,1.8,16,.09,3.4,'teal',8)}
 box('swing-beam',-16.5,3.45,15,5.8,.15,.15,'teal');
 for(const x of [-18,-15]){box('swing-rope',x,2.3,15,.035,2.1,.035,'metal');box('swing-seat',x,1.2,15,.8,.1,.5,'wood')}
 // Parking: 18 marked bays south of the shops, 8 on the east side.
 pathRect(-30,-42,52,7.5,'asphalt',.13);
 for(let i=0;i<18;i++){const x=-54+i*2.9;pathRect(x,-42,.08,5.8,'white',.2)}
 pathRect(55,-30,8,25,'asphalt',.13);for(let i=0;i<8;i++)pathRect(55,-41+i*3,6.6,.08,'white',.2);
 // A neighboring skyline makes depth and camera parallax visible.
 for(let i=0;i<15;i++){const x=-98+i*14,h=8+(i*7%13);box('distant-building',x,h/2,91,8,h,9,'distant')}
 sign('רחוב השכונה',45,.24,50,12,'#35524d').rotation.x=Math.PI/2;
}

function buildNeighborhood(){
 for(const s of sites){
  const o=model(s.asset,s.id,s.x,s.z,s.w,Math.PI,'x',.2,s.ys),m=o.metadata;
  colliders.push({x:s.x,z:s.z,w:m.width*.47,d:m.depth*.46});
  sign(s.name,s.x,m.height+2.2,s.z,Math.max(9,s.w*.75),'#26443f',true);
  if(s.id==='S1')sign('שוק העיר',s.x,3.5,s.z-m.depth/2-.1,10,'#b16837');
  if(s.id==='S2'){box('clinic-cross',s.x,3.2,s.z-m.depth/2-.12,2,.55,.08,'white');box('clinic-cross',s.x,3.2,s.z-m.depth/2-.13,.55,2,.08,'white')}
 }
 // Extra cottages show a different free asset family, outside the seven landmarks.
 for(const [x,z,r] of [[-1,38,0],[48,36,Math.PI]]){
  const o=model('houseA','garden-house',x,z,8,r);colliders.push({x,z,w:4,d:3.4});
 }
 let n=0;for(let x=-56;x<=56;x+=10)for(const z of [-43,43])if(Math.abs(x-12)>8){tree(n++%3?'tree':'oak',x,z,4.6+(n%3)*.65,n);}
 for(let z=-36;z<42;z+=10)for(const x of [-57,57])tree(n++%3?'tree':'oak',x,z,5+(n%3)*.4,n);
 for(const [x,z] of [[-25,37],[-8,38],[-25,17],[-8,17],[-25,24],[-8,31],[-29,-23],[1,-22],[25,6],[45,-16],[5,18],[5,30]])tree('oak',x,z,5+(++n%3)*.6,n);
 for(let x=-55;x<=55;x+=22){streetLamp(x,44,0);streetLamp(x,-44,Math.PI)}
 for(let z=-30;z<=30;z+=20){streetLamp(-58,z,-Math.PI/2);streetLamp(58,z,Math.PI/2)}
 for(const [x,z,rot] of [[5,-16,0],[20,0,Math.PI],[5,0,-Math.PI/2],[20,-16,Math.PI/2]])model('signal','traffic-light',x,z,3.7,rot,'y');
 for(const [x,z,rot] of [[-57,-45,0],[57,45,Math.PI]])model('stop','stop-sign',x,z,2.4,rot,'y');
 const placed=[[-51,-42,'sedan'],[-42,-42,'taxi'],[-33,-42,'sedan'],[-21,-42,'van'],[-9,-42,'sedan'],[55,-35,'police'],[55,-23,'sedan'],[55,-29,'taxi']];
 for(const [x,z,id] of placed)model(id,'parked-car',x,z,4.2,Math.PI,'z');
 for(const [x,z] of lamps.filter((_,i)=>i%4===0).slice(0,5)){
  const l=new B.PointLight('warm street light',V(x,4.7,z),scene);l.diffuse=B.Color3.FromHexString('#ffbb6a');l.range=17;l.intensity=0;nightLights.push(l);
 }
 sign('B4 · השכונה',-5,6,-60,22,'#213e3c',false);
}

function makePerson(x,z,color,phase){
 const root=new B.TransformNode('pedestrian',scene);root.position.set(x,.2,z);
 const shirt=material('shirt'+phase,color),skin=mats.skin,parts=[];
 const body=B.MeshBuilder.CreateCapsule('person-body',{height:.9,radius:.22,tessellation:6,subdivisions:1},scene);body.position.y=1.15;body.material=shirt;body.parent=root;
 const head=B.MeshBuilder.CreateSphere('person-head',{diameter:.38,segments:6},scene);head.position.y=1.87;head.material=skin;head.parent=root;
 for(const side of [-1,1]){const leg=box('person-leg',side*.13,.48,0,.18,.8,.2,'trousers');leg.parent=root;parts.push(leg);const arm=box('person-arm',side*.32,1.2,0,.15,.7,.16,shirt);arm.parent=root;parts.push(arm)}
 for(const m of root.getChildMeshes())m.isPickable=false;
 const p={root,x,z,phase,parts};people.push(p);return p;
}

function buildPeople(){for(let i=0;i<12;i++)makePerson(-52+i*8.6,i%2?44:-44,['#cf714e','#508f8b','#e1b75c','#5e718c'][i%4],i*1.9);}

const ROUTE=[[-64,-50],[-49,-50],[49,-50],[64,-50],[65,-35],[65,35],[64,50],[49,51],[-49,51],[-64,50],[-65,35],[-65,-35]].map(p=>V(p[0],.24,p[1]));
let route,routeLen;
function buildCars(){
 player=model('sedan','player-car',-43,-51,4.5,heading,'z',.24);
 playerHalo=B.MeshBuilder.CreateTorus('player-marker',{diameter:5.8,thickness:.1,tessellation:40},scene);playerHalo.position.copyFrom(player.position);playerHalo.position.y=.28;playerHalo.material=mats.halo;playerHalo.isPickable=false;
 route=B.Curve3.CreateCatmullRomSpline(ROUTE,12,true).getPoints();routeLen=route.length-1;
 for(let i=0;i<5;i++){const root=model(['taxi','sedan','van','police','sedan'][i],'traffic-car',0,0,4.25,0,'z',.24);traffic.push({root,u:(.13+i/5)%1,rate:.009+i*.0006})}
}

function setMode(next){
 if(!scene)return;mode=next;
 orbit.detachControl();driveCam.detachControl();streetCam.detachControl();
 if(next==='orbit'){scene.activeCamera=orbit;orbit.attachControl($('view'),true);orbit.inputs.attached.keyboard?.detachControl();}
 else if(next==='drive'){scene.activeCamera=driveCam;driveCam.position.copyFrom(player.position.add(V(-Math.sin(heading)*10,5,-Math.cos(heading)*10)));driveCam.setTarget(player.position.add(V(0,1.3,0)));}
 else {scene.activeCamera=streetCam;streetCam.position.set(-23,1.8,-1);streetCam.setTarget(V(-17,3,27));streetCam.attachControl($('view'),true);streetCam.inputs.attached.keyboard?.detachControl();}
 document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
 $('modeLabel').textContent={orbit:'מבט על השכונה',drive:'נהיגה · מצלמה עוקבת',street:'סיור בגובה הרחוב'}[mode];
 $('hint').textContent=mode==='street'?'WASD / חצים להליכה · גרירה בעכבר למבט סביב':mode==='drive'?'W / ↑ גז · S / ↓ רוורס · A D / ← → היגוי · רווח בלם':'גרירה לסיבוב · גלגלת לזום · לחצו ״נהיגה״ כדי לצאת לדרך';
 $('driveHUD').hidden=mode!=='drive';
}

function reset(){if(!player)return;player.position.set(-43,.24,-51);heading=Math.PI/2;player.rotation.y=heading;speed=0;orbit.setTarget(V(0,1,0));orbit.alpha=-Math.PI*.63;orbit.beta=.91;orbit.radius=147;setMode(mode);toast('חזרנו לנקודת ההתחלה')}
function setNight(on){night=on;if(!scene)return;
 sun.intensity=on?.16:1.2;hemi.intensity=on?.42:.65;sun.diffuse=B.Color3.FromHexString(on?'#8297df':'#fff0d5');
 scene.clearColor=B.Color4.FromHexString(on?'#172b42ff':'#bed2d4ff');scene.fogColor=B.Color3.FromHexString(on?'#1d344a':'#bed2d4');
 mats.lamp.emissiveColor=B.Color3.FromHexString(on?'#ffc76a':'#d4d5bd').scale(on?1.5:.12);
 mats.water.diffuseColor=B.Color3.FromHexString(on?'#356a8a':'#59bcc0');
 for(const l of nightLights)l.intensity=on?1.1:0;
 $('nightBtn').textContent=on?'☀ יום':'☾ ערב';$('timeLabel').textContent=on?'19:40':'16:20';
}
function quality(){low=!low;scene.shadowsEnabled=!low;shadow.getShadowMap().refreshRate=low?0:2;shadow.setDarkness(low?.45:.32);engine.setHardwareScalingLevel(low?Math.max(1.4,window.devicePixelRatio):Math.max(1,window.devicePixelRatio/1.35));$('qualityBtn').textContent=low?'איכות: חסכונית':'איכות: מלאה';}
function blocked(x,z,r=1){return Math.abs(x)>74||Math.abs(z)>59||colliders.some(c=>Math.abs(x-c.x)<c.w+r&&Math.abs(z-c.z)<c.d+r)}
function onRoad(x,z){return roads.some(r=>Math.abs(x-r.x)<r.w/2&&Math.abs(z-r.z)<r.d/2)}
function toast(text){$('toast').textContent=text;$('toast').classList.add('show');toastUntil=performance.now()+2800;}

function tick(dt){
 const forward=!!(key.KeyW||key.ArrowUp),back=!!(key.KeyS||key.ArrowDown),left=!!(key.KeyA||key.ArrowLeft),right=!!(key.KeyD||key.ArrowRight);
 if(mode==='drive'){
  const old=speed,grip=onRoad(player.position.x,player.position.z)?1:.5;
  speed+=(forward?11:back?-9:0)*dt;speed*=Math.exp(-(key.Space?7:((forward||back) ? .15 : .75))*dt);speed=clamp(speed,-6,19*grip);
  if(Math.abs(speed)>.1)heading+=(right-left)*dt*1.65*clamp(speed/6,-1,1);
  const nx=player.position.x+Math.sin(heading)*speed*dt,nz=player.position.z+Math.cos(heading)*speed*dt;
  if(blocked(nx,nz,1.1)){speed=-old*.12;}else{player.position.x=nx;player.position.z=nz;}
  player.rotation.y=heading;
  const want=player.position.add(V(-Math.sin(heading)*10,4.7,-Math.cos(heading)*10));driveCam.position=B.Vector3.Lerp(driveCam.position,want,1-Math.exp(-dt*6));driveCam.setTarget(player.position.add(V(0,1.2,0)));
 }else if(mode==='street'){
  const f=streetCam.getForwardRay().direction;f.y=0;f.normalize();const r=V(f.z,0,-f.x),mv=f.scale(+forward-+back).add(r.scale(+right-+left));
  if(mv.lengthSquared()>.01){mv.normalize().scaleInPlace((key.ShiftLeft?8:4)*dt);const nx=streetCam.position.x+mv.x,nz=streetCam.position.z+mv.z;if(!blocked(nx,nz,.3)){streetCam.position.x=nx;streetCam.position.z=nz}}streetCam.position.y=1.8;
 }
 for(const t of traffic){t.u=(t.u+t.rate*dt)%1;const idx=t.u*routeLen,i=Math.floor(idx),f=idx-i,a=route[i],b=route[(i+1)%routeLen];t.root.position.copyFrom(B.Vector3.Lerp(a,b,f));t.root.rotation.y=Math.atan2(b.x-a.x,b.z-a.z)}
 for(const p of people){const u=elapsed*.17+p.phase;p.root.position.x=p.x+Math.sin(u)*4;p.root.rotation.y=Math.cos(u)>0?Math.PI/2:-Math.PI/2;p.parts.forEach((m,i)=>m.rotation.x=Math.sin(elapsed*6+p.phase+(i%2?Math.PI:0))*.32);}
 playerHalo.position.x=player.position.x;playerHalo.position.z=player.position.z;playerHalo.isVisible=mode==='orbit';
 for(const l of worldLabels)l.isVisible=mode==='orbit'&&orbit.radius>75;
 $('speed').textContent=Math.round(Math.abs(speed)*3.6);$('money').textContent=money.toLocaleString('en-US');
 if(toastUntil&&performance.now()>toastUntil){$('toast').classList.remove('show');toastUntil=0}
 updateMission();
}

const deliveryStops=[{x:-43,z:-40,name:'שוק העיר'},{x:-12,z:-40,name:'מרפאת השכונה'},{x:37,z:-40,name:'בית הספר'}];
function updateMission(){if(!job||jobDone||mode!=='drive')return;const p=deliveryStops[job-1],dist=Math.hypot(player.position.x-p.x,player.position.z-p.z);$('jobHint').hidden=dist>8;$('jobHint').textContent='E · '+(job===1?'איסוף ארגז':'מסירת הארגז')+' · '+p.name;}
function missionAction(){if(!job||jobDone)return;const p=deliveryStops[job-1];if(Math.hypot(player.position.x-p.x,player.position.z-p.z)>8||Math.abs(speed)>2){toast('עוצרים ליד נקודת השליחות ואז לוחצים E');return}if(job===3){jobDone=true;money+=300;$('missionText').textContent='השליחות הושלמה · קיבלת 300 מטבעות';$('jobHint').hidden=true;toast('כל הכבוד! שליחות השכונה הושלמה')}else{job++;$('missionText').textContent='היעד הבא: '+deliveryStops[job-1].name;toast(job===2?'אספת ארגז. ממשיכים למרפאה':'נמסר למרפאה. ממשיכים לבית הספר')}}

function miniMap(){const cv=$('mini'),c=cv.getContext('2d'),w=cv.width,h=cv.height,X=x=>(x+80)/160*w,Z=z=>(64-z)/128*h;
 c.fillStyle='#d5dec9';c.fillRect(0,0,w,h);
 for(const r of roads){c.fillStyle='#818b88';c.fillRect(X(r.x-r.w/2),Z(r.z+r.d/2),r.w/160*w,r.d/128*h)}
 c.fillStyle='#86a878';c.fillRect(X(-28),Z(40),23/160*w,29/128*h);
 for(const s of sites){c.fillStyle=s.id[0]==='N'?'#b7aa91':'#6eaaa7';c.fillRect(X(s.x-7),Z(s.z+6),14/160*w,12/128*h)}
 if(job&&!jobDone){const p=deliveryStops[job-1];c.fillStyle='#e7a440';c.beginPath();c.arc(X(p.x),Z(p.z),6,0,Math.PI*2);c.fill()}
 const p=mode==='street'?streetCam.position:player.position;c.save();c.translate(X(p.x),Z(p.z));c.rotate(heading);c.fillStyle='#0a6e63';c.strokeStyle='#fff';c.lineWidth=2;c.beginPath();c.moveTo(0,-7);c.lineTo(5,5);c.lineTo(0,2);c.lineTo(-5,5);c.closePath();c.fill();c.stroke();c.restore();
}

function events(){
 document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));
 $('nightBtn').onclick=()=>setNight(!night);$('qualityBtn').onclick=quality;$('resetBtn').onclick=reset;
 $('sourcesBtn').onclick=()=>{$('sources').showModal();for(const k in key)delete key[k]};
 $('closeSources').onclick=()=>$('sources').close();
 $('sources').onclick=e=>{if(e.target===$('sources')){const r=$('sources').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)$('sources').close()}};
 $('fullBtn').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{toast('אפשר גם להגדיל את חלון הדפדפן')}};
 $('jobBtn').onclick=()=>{job=1;jobDone=false;setMode('drive');$('jobBtn').hidden=true;$('missionText').textContent='אוספים ארגז משוק העיר';toast('סעו אל הנקודה הכתומה במפה · עוצרים ולוחצים E')};
 window.addEventListener('keydown',e=>{
  if($('sources').open)return;
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();key[e.code]=true;
  if(e.repeat)return;
  if(e.code==='Digit1')setMode('orbit');if(e.code==='Digit2')setMode('drive');if(e.code==='Digit3')setMode('street');
  if(e.code==='KeyN')setNight(!night);if(e.code==='KeyR')reset();if(e.code==='KeyE')missionAction();
  if(e.code==='KeyP'){paused=!paused;toast(paused?'המשחק מושהה · P להמשך':'ממשיכים')}
 });
 window.addEventListener('keyup',e=>delete key[e.code]);
 window.addEventListener('blur',()=>{for(const k in key)delete key[k]});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)for(const k in key)delete key[k]});
 document.querySelectorAll('[data-key]').forEach(b=>{
  b.onpointerdown=e=>{e.preventDefault();b.setPointerCapture(e.pointerId);key[b.dataset.key]=true};
  b.onpointerup=b.onpointercancel=b.onlostpointercapture=()=>delete key[b.dataset.key];
 });
 window.addEventListener('resize',()=>engine.resize());
}

async function start(){
 try{
  if(!B.Engine.isSupported())throw new Error('נדרשת האצת גרפיקה WebGL בדפדפן. נסו Chrome או Edge והפעילו האצת חומרה.');
  B.SceneLoader.ShowLoadingScreen=false;
  engine=new B.Engine($('view'),true,{preserveDrawingBuffer:true,stencil:true,powerPreference:'high-performance',disableWebGL2Support:false});
  engine.setHardwareScalingLevel(Math.max(1,window.devicePixelRatio/1.35));
  scene=new B.Scene(engine);scene.clearColor=B.Color4.FromHexString('#bed2d4ff');scene.ambientColor=new B.Color3(.2,.22,.2);
  scene.fogMode=B.Scene.FOGMODE_EXP2;scene.fogDensity=.0018;scene.fogColor=B.Color3.FromHexString('#bed2d4');scene.skipPointerMovePicking=true;
  scene.imageProcessingConfiguration.toneMappingEnabled=true;scene.imageProcessingConfiguration.toneMappingType=B.ImageProcessingConfiguration.TONEMAPPING_ACES;scene.imageProcessingConfiguration.exposure=1.15;scene.imageProcessingConfiguration.contrast=1.12;
  hemi=new B.HemisphericLight('sky',V(0,1,0),scene);hemi.intensity=.8;hemi.groundColor=B.Color3.FromHexString('#8a9b83');
  sun=new B.DirectionalLight('sun',V(-.8,-1,.45),scene);sun.position=V(80,110,-55);sun.intensity=2;sun.diffuse=B.Color3.FromHexString('#fff0d5');sun.autoCalcShadowZBounds=true;
  shadow=new B.ShadowGenerator(1024,sun);shadow.usePercentageCloserFiltering=false;shadow.filteringQuality=B.ShadowGenerator.QUALITY_LOW;shadow.bias=.0008;shadow.normalBias=.03;shadow.setDarkness(.32);
  orbit=new B.ArcRotateCamera('orbit',-Math.PI*.63,.91,147,V(0,1,0),scene);orbit.lowerRadiusLimit=24;orbit.upperRadiusLimit=235;orbit.lowerBetaLimit=.18;orbit.upperBetaLimit=1.47;orbit.wheelPrecision=13;orbit.panningSensibility=65;orbit.minZ=.2;orbit.maxZ=800;orbit.fov=.78;
  driveCam=new B.FreeCamera('follow',V(-55,5,-51),scene);driveCam.minZ=.1;driveCam.maxZ=700;driveCam.fov=.9;
  streetCam=new B.UniversalCamera('street',V(-23,1.8,-1),scene);streetCam.minZ=.08;streetCam.maxZ=700;streetCam.fov=1.05;streetCam.angularSensibility=2500;
  scene.activeCamera=orbit;
  for(const [id,col] of Object.entries({base:'#2b4545',grass:'#a6be87',park:'#8aaa72',paving:'#d7d4bf',curb:'#d9d9ca',asphalt:'#515c5e',paint:'#e5d6aa',white:'#f5f3da',sand:'#d6c6a1',stone:'#e1dfc9',water:'#59bcc0',metal:'#405354',wood:'#b17a4b',teal:'#499b95',lamp:'#eeeece',distant:'#a8b5b1',skin:'#d6a581',trousers:'#374b5d',halo:'#23c7a2'}))mats[id]=material(id,col);
  mats.water.alpha=.88;mats.water.specularColor=new B.Color3(.4,.5,.5);mats.halo.emissiveColor=B.Color3.FromHexString('#4af2c6');
  await loadAssets();$('loadText').textContent='מרכיב את השכונה…';
  buildGround();buildNeighborhood();buildCars();buildPeople();events();setMode('orbit');setNight(false);
  $('assetCount').textContent=AUDIT.loaded.length;$('treeCount').textContent=AUDIT.trees;$('loadBar').style.width='100%';
  $('loading').classList.add('done');setTimeout(()=>$('loading').hidden=true,550);started=true;demo.ready=true;
  let last=performance.now(),hudAt=0;
  engine.runRenderLoop(()=>{const now=performance.now(),dt=Math.min((now-last)/1000,.25);last=now;if(!document.hidden&&!paused){for(let left=dt;left>0;){const h=Math.min(left,1/60);elapsed+=h;tick(h);left-=h}}scene.render();AUDIT.frames++;if(now-hudAt>250){$('fps').textContent=Math.round(engine.getFps());miniMap();hudAt=now}});
  toast('השכונה מוכנה · גררו בעכבר כדי להסתובב סביבה');
 }catch(e){AUDIT.failures.push(String(e));$('loadTitle').textContent='לא הצלחנו לפתוח את התלת־ממד';$('loadText').textContent=e.message;$('loadText').style.maxWidth='560px';$('loadBar').style.background='#dd8c71';console.error(e)}
}
start();
})();
