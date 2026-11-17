// geometry check of the new poses (no canvas): P34 library + the hook from 074zu (sapPose), hands / pelvis per pose
const fs=require('fs');const [a,b,part]=process.argv.slice(2);
const G={document:{createElement:()=>({getContext:()=>new Proxy({},{get:()=>()=>{}}),width:0,height:0})},devicePixelRatio:1,performance:{now:()=>Date.now()},setInterval:()=>0};
const src=fs.readFileSync(a,'utf8')+'\n'+fs.readFileSync(b,'utf8');
new Function('window','globalThis','document','devicePixelRatio','setInterval',src)(G,G,G.document,1,()=>0);
const P34=G.P34;if(!P34){console.log('no P34');process.exit(1)}
// take the pose code from the part
const p=fs.readFileSync(part,'utf8');const i=p.indexOf(' const SAP_KEY='),j=p.indexOf(' function sapInstall()');const code=p.slice(i,j);
const TAU=6.2832;const fns=new Function('TAU','err',code+';return{SAP_ACT,sapPose,sapF}')(TAU,(w,e)=>console.log('ERR',w,e));
G.P34X={pose:(S,L,act,fr,X)=>{if(fns.SAP_ACT[act.k])fns.sapPose(S,L,act,fr,X)}};for(const k in fns.SAP_ACT)P34.FR[k]=fns.sapF(k);
const look={h:1.76,top:{t:'tee',c:'#3d7fc4'},legs:{t:'trousers',c:'#333'},shoes:{t:'sneaker',c:'#eee'},hair:{t:'short',c:'#333'},skin:'#d9a57f'};
// a pose: the 3D hands (via pose through parts? we need S) — use P34.parts and the extreme points
const out={};for(const k of ['stand',...Object.keys(fns.SAP_ACT)]){const F=fns.sapF(k)||1;const r=[];for(const fr of [0,Math.floor(F/2),F-1]){let pts;try{pts=P34.parts(look,{k},2,fr).parts}catch(e){r.push('ERR '+e.message);continue}
  let y0=1e9,y1=-1e9,x0=1e9,x1=-1e9,nan=0;for(const q of pts)for(const v of q.pts){if(!Number.isFinite(v[0])||!Number.isFinite(v[1]))nan++;y0=Math.min(y0,v[1]);y1=Math.max(y1,v[1]);x0=Math.min(x0,v[0]);x1=Math.max(x1,v[0])}
  r.push({fr,n:pts.length,nan,h:+(y1-y0).toFixed(3),w:+(x1-x0).toFixed(3)})}out[k]=r}
console.log(JSON.stringify(out));
