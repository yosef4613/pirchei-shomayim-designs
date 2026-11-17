// שאילתה: הגאומטריה של דרכי האי ליד מסוף המשא וחנות האי (לתכנון משאית הפיזור — LOGI): הנתיבים, הצמתים, ומפה של מה תפוס (10 פיקס׳)
return (()=>{const R={nodes:{},lanes:{},grids:{}};
 for(const id of ['IL','ISE-0','ISE-1','ISE-2','ISE-3','ISEL-0','ISEL-1','ISEL-4','ISW-1','ISW-2','ISW-3','ISW-4','ISW-5','ISW-6','E69_73'])try{const n=byNode[id];if(n)R.nodes[id]=[Math.round(n.x),Math.round(n.y),n.type]}catch(e){}
 const IS=EDGES.filter(e=>/^IS-/.test(e.id));R.edges=IS.map(e=>[e.id,e.a,e.b,e.cls,e.oneway||0,e.serviceOnly?1:0]);
 const LN=[];for(const e of IS)for(const d of [1,-1])for(let k=0;k<3;k++){const L=lane2(e.id,d,k);if(!L)continue;LN.push(L);R.lanes[e.id+'/'+d+'/'+k]={a:[+L.ax.toFixed(1),+L.ay.toFixed(1)],u:[+L.ux.toFixed(3),+L.uy.toFixed(3)],len:+L.len.toFixed(1),cnt:L.cnt,w:L.w||L.width||null,moves:(L.moves||[]).map(m=>m.kind+'>'+(m.to&&m.to.edge)+'/'+(m.to&&m.to.dir))}}
 R.laneKeys=LN.length?Object.keys(LN[0]).join(','):'';
 const dl=(x,y)=>{let b=1e9;for(const L of LN){const px=x-L.ax,py=y-L.ay,s=Math.max(0,Math.min(L.len,px*L.ux+py*L.uy)),qx=L.ax+L.ux*s,qy=L.ay+L.uy*s;b=Math.min(b,Math.hypot(x-qx,y-qy))}return b};
 const grid=(x0,y0,x1,y1)=>{const rows=[];for(let y=y0;y<=y1;y+=10){let s='';for(let x=x0;x<=x1;x+=10){const d=dl(x,y);let c='.';if(d<6)c='=';else if(d<13)c='-';else{let b=null;try{b=blockedAt(x,y,3)}catch(e){b='?'}if(b)c=b==='WATER'?'~':b==='WORLD'?'W':'#'}s+=c}rows.push(y+' '+s)}return rows};
 R.grids.freight=grid(8800,7280,9420,7740);R.grids.shop=grid(8420,7180,8760,7500);
 R.blockNames={};for(const [x,y] of [[8930,7590],[9015,7600],[9100,7500],[9200,7400],[8610,7325],[8600,7380],[8700,7300],[8560,7420]])try{R.blockNames[x+','+y]=blockedAt(x,y,3)}catch(e){}
 try{R.trucks=LOGI.veh.map(v=>[v.id,v.asset,Math.round(v.x),Math.round(v.y),v.c5.mode]);R.vehLen=(()=>{try{const i=vehicleQaInfo({id:'x',asset:'VH-TR-01'});return i&&i.info&&i.info.fp}catch(e){return null}})()}catch(e){}
 return R})()
