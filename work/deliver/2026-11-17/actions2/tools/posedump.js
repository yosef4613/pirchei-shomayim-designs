const fs=require('fs');const [a,b,part,out]=process.argv.slice(2);
const G={document:{createElement:()=>({getContext:()=>new Proxy({},{get:()=>()=>{}}),width:0,height:0})},devicePixelRatio:1};
new Function('window','globalThis','document','devicePixelRatio','setInterval',fs.readFileSync(a,'utf8')+'\n'+fs.readFileSync(b,'utf8'))(G,G,G.document,1,()=>0);
const P34=G.P34;const p=fs.readFileSync(part,'utf8');const code=p.slice(p.indexOf(' const SAP_KEY='),p.indexOf(' function sapInstall()'));
const fns=new Function('TAU','err',code+';return{SAP_ACT,sapPose,sapF}')(6.2832,(w,e)=>console.log('ERR',w,e));
G.P34X={pose:(S,L,act,fr,X)=>{if(fns.SAP_ACT[act.k])fns.sapPose(S,L,act,fr,X)}};for(const k in fns.SAP_ACT)P34.FR[k]=fns.sapF(k);
const look={h:1.76,top:{t:'tee',c:'#3d7fc4'},legs:{t:'trousers',c:'#333'},shoes:{t:'sneaker',c:'#eee'},hair:{t:'short',c:'#333'},skin:'#d9a57f'};
const R=[];for(const k of ['stand','wait',...Object.keys(fns.SAP_ACT)])for(const dir of [1,3]){const F=fns.sapF(k)||1;const fr=k.startsWith('saUp')||k.startsWith('saDn')||k==='saGive'||k==='saHang'?F-1:Math.floor(F/2);
 const pts=P34.parts(look,{k},dir,fr).parts.slice().sort((x,y)=>x.d-y.d).map(q=>({c:q.col||q.c||q.fill||'#888',p:q.pts.map(v=>[+v[0].toFixed(4),+v[1].toFixed(4)])}));R.push({k,dir,pts})}
fs.writeFileSync(out,JSON.stringify(R));console.log(R.length, Object.keys(P34.parts(look,{k:'stand'},2,0).parts[0]))
