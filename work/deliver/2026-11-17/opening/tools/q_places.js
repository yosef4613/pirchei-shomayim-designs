return (()=>{const R=navPoiRegistry(),o={};const want=/HOME|APT|AIR|TERM|PORT|CRANE|ISL|IS-|MARINA|E3-ST|E3-TERM|C2-MALL|D3-GAR|F3|B5|ARR|G4|E9|F9|H8|D9/i;
for(const [k,v] of Object.entries(R)){if(want.test(k))o[k]=[Math.round(v.x),Math.round(v.y),v.chunk||'',v.label||'']}
let cs=null;try{cs=[typeof CHUNK_SIZE!=='undefined'?CHUNK_SIZE:null,typeof WORLD!=='undefined'?[WORLD.w,WORLD.h]:null]}catch(e){}
const a=playerActor();
return {n:Object.keys(R).length,cs,player:[Math.round(a.x),Math.round(a.y),currentChunkId(a.x,a.y)],c3:(()=>{const r=[];for(let x=0;x<12000;x+=500)for(let y=0;y<12000;y+=500){try{const id=currentChunkId(x,y);if(id==='C3'||id==='A1'||id==='H9'||id==='E9')r.push([id,x,y])}catch(e){}}return r.slice(0,40)})(),o}})()
