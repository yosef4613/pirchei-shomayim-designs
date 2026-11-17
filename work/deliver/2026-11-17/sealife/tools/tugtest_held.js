// tugtest_held.js — כמו tugtest.js, אבל המעבורת מוחזקת ב-G8 כל הזמן (ferryNear אמת לכל מבט של 34 שנ׳ ומעלה)
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const pre=`var window={};var MIN=290,DAY=0;function lgMinOfDay(){return MIN%1440}function gameClock(){return{day:DAY}}
var G84_CLOCK={rate:.5};var WORLD={maxY:7750};var S9_HOOKS={live:[]};function wtcPropsLive(){};var Camera={zoom:1};
var S14={D:{tugs:[{id:'TUG-1',x:3648,y:5352,h:-Math.PI/2,L:281.2,B:95.6},{id:'TUG-2',x:3784,y:5352,h:-Math.PI/2,L:281.2,B:95.6},{id:'TUG-3',x:3883.625,y:5352,h:-Math.PI/2,L:281.2,B:95.6}]},TPX:{f:null},
 dayT(m){return[0,m]},gmin(){return MIN},poseOf(){return{x:3648,y:5352,h:-Math.PI/2}},ferryNear(x0,y0,x1,y1,R,secs){return FH.held&&secs>=34},scripts(){return{tug:[]}}};
var FH={held:true,c:0};function a6FerryPersistent(){return FH.cl||(FH.cl={clock:100})}function a6FerryPose(){return{phase:'G8',remaining:.5}}
var SHIPO={id:'BRT-D6',x:4487,y:5271,h:0,L:450,B:110};var S10KIT={c6d6:{shipOf(){return SHIPO}}};
var S10CI={ship:{ph:'sea',t:0,a:0,hold:Array(12).fill(1),x:4487,y:8170,h:-Math.PI/2,departDay:-1},pool:[1]};
const PI=Math.PI,DOCK={x:4487,y:5271,h:0},OFF={x:4487,y:5441},SEA={x:4487,y:8170},PULL=30,ROT=24,SAIL=45;
function shipTick(dt){const sh=S10CI.ship;sh.t+=dt;const go=p=>{sh.ph=p;sh.t=0;LOG.push([T|0,p])};const set=(x,y,h)=>{sh.x=x;sh.y=y;sh.h=h;SHIPO.x=x;SHIPO.y=y;SHIPO.h=h};
 if(sh.ph==='docked'){if(sh.hold.length)go('rdown');return}if(sh.ph==='rdown'){if(sh.t>=16)go('unload');return}
 if(sh.ph==='unload'){if(sh.hold.length){if(sh.t>20){sh.hold.shift();sh.t=0}}else go('rup');return}if(sh.ph==='rup'){if(sh.t>=16)go('out1');return}
 if(sh.ph==='out1'){const u=Math.min(1,sh.t/PULL),e=(1-Math.cos(PI*u))/2;set(DOCK.x,DOCK.y+170*e,0);if(u>=1)go('out2');return}
 if(sh.ph==='out2'){const u=Math.min(1,sh.t/ROT),e=(1-Math.cos(PI*u))/2;set(OFF.x,OFF.y,e*PI/2);if(u>=1)go('out3');return}
 if(sh.ph==='out3'){set(OFF.x,Math.min(SEA.y,sh.y+SAIL*dt),PI/2);if(sh.y>=SEA.y){go('sea');sh.departDay=DAY}return}
 if(sh.ph==='sea'){if(DAY!==sh.departDay&&MIN%1440>=330){sh.hold=Array(12).fill(1);set(SEA.x,SEA.y,-PI/2);go('in1')}return}
 if(sh.ph==='in1'){set(OFF.x,Math.max(OFF.y,sh.y-SAIL*dt),-PI/2);if(sh.y<=OFF.y)go('in2');return}
 if(sh.ph==='in2'){const u=Math.min(1,sh.t/ROT),e=(1-Math.cos(PI*u))/2;set(OFF.x,OFF.y,-PI/2+e*PI/2);if(u>=1)go('in3');return}
 if(sh.ph==='in3'){const u=Math.min(1,sh.t/PULL),e=(1-Math.cos(PI*u))/2;set(DOCK.x,OFF.y+(DOCK.y-OFF.y)*e,0);if(u>=1)go('docked');return}}
var T=0,LOG=[];function simStep(dt){shipTick(dt);a6FerryPersistent().clock+=dt}`;
const f=new Function(pre+src+`;return{X:TUGX,step:(dt)=>{simStep(dt);T+=dt;MIN+=dt*.5;if(MIN>=1440*(DAY+1))DAY++},LOG,SHIPO,ST:S10CI};`);
const E=f();const FHC=()=>E.X?0:0;const ob=(x,y,h,L,B)=>({x,y,c:Math.cos(h),s:Math.sin(h),L,B});
const pts=o=>{const R=[];for(const [lx,ly] of[[o.L/2,0],[o.L*.3,o.B/2],[o.L*.3,-o.B/2],[-o.L/2,o.B/2],[-o.L/2,-o.B/2],[0,o.B/2],[0,-o.B/2],[0,0]])R.push([o.x+lx*o.c-ly*o.s,o.y+lx*o.s+ly*o.c]);return R};
const inside=(P,q,m)=>{const x=P[0]-q.x,y=P[1]-q.y,u=x*q.c+y*q.s,v=-x*q.s+y*q.c;return Math.abs(u)<q.L/2-m&&Math.abs(v)<q.B/2-m};
const hit=(a,b,m)=>pts(a).some(P=>inside(P,b,m))||pts(b).some(P=>inside(P,a,m));
const bad={};let jumps=0;const prev={};
for(let i=0;i<40000;i++){E.step(.1);const s=E.X.state(),S=E.SHIPO,sh=ob(S.x,S.y,S.h,S.L,S.B),T1=ob(3648,5352,-Math.PI/2,281.2,95.6);const O=[];
 for(const t of s.tugs){const p=prev[t.id];if(p&&Math.hypot(t.x-p[0],t.y-p[1])>8)jumps++;prev[t.id]=[t.x,t.y];if(t.home)continue;const o=ob(t.x,t.y,t.h,281.2,95.6);O.push(o);
  if(hit(o,sh,6))bad[t.id+'×ship '+t.mode+' '+s.ship.ph]=(bad[t.id+'×ship '+t.mode+' '+s.ship.ph]||0)+1;if(hit(o,T1,2))bad[t.id+'×T1 '+t.mode]=(bad[t.id+'×T1 '+t.mode]||0)+1;if(o.y-140<5200&&Math.abs(o.x-3716)<70)bad[t.id+' pier '+t.mode]=1}
 if(O.length===2&&hit(O[0],O[1],2))bad['tug×tug '+s.tugs.map(t=>t.mode).join('/')]=(bad['tug×tug '+s.tugs.map(t=>t.mode).join('/')]||0)+1;
 if(E.X.stats().dep>=1&&E.X.stats().arr>=2&&!s.job)break}
console.log('ferryClock',FHC(),JSON.stringify(E.X.stats()),'\njumps',jumps,'\nbad',JSON.stringify(bad),'\nlog',JSON.stringify(E.LOG.slice(0,40)));
