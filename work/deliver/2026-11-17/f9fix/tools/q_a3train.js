return (async()=>{const out={};const q=tcF9StoryList().find(s=>s.id==='A3-TRAIN');if(!q)return{none:1};try{const c=gameClock();out.clock=c.hour+':'+c.minute}catch(e){}
 const [x0,y0,x1,y1]=q.box,W=x1-x0,H=y1-y0,cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');const c34=typeof c34Live==='function'?c34Live:null;if(c34)c34Live=()=>false;
 const img=(t,nt)=>{g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);g.setTransform(1,0,0,1,-x0,-y0);try{q.render(g,t*1000,nt)}catch(e){return null}return g.getImageData(0,0,W,H).data};
 const base=q.T*10+(q.t0||0),i0=q.on[1]+2,i1=q.T-1;const ref=img(base+i0,0);const bb=[1e9,1e9,-1,-1];let nd=0;const per=[];
 for(let k=0;k<12;k++){const t=base+i0+(i1-i0)*k/11,d=img(t,0);let n=0;for(let i=0;i<d.length;i+=4){if(d[i]!==ref[i]||d[i+1]!==ref[i+1]||d[i+2]!==ref[i+2]||d[i+3]!==ref[i+3]){n++;const p=i/4,x=p%W,y=(p/W)|0;bb[0]=Math.min(bb[0],x);bb[1]=Math.min(bb[1],y);bb[2]=Math.max(bb[2],x);bb[3]=Math.max(bb[3],y)}}per.push([Math.round(t-base),n]);nd+=n}
 if(c34)c34Live=c34;out.diffPixels=per;out.bbWorld=[bb[0]+x0,bb[1]+y0,bb[2]+x0,bb[3]+y0];
 let M=[];try{M=TC_LIVE.zones.A3.movers(tcF9Now(),true)}catch(e){}out.movers=M.map(m=>[m.id,m.when,m.box]);
 const B=out.bbWorld;out.overlap=M.filter(m=>m.box&&m.box[0]<B[2]&&m.box[2]>B[0]&&m.box[1]<B[3]&&m.box[3]>B[1]).map(m=>m.id);
 try{out.match=JSON.stringify(A34PLAY.matchNow())}catch(e){}try{out.next=JSON.stringify(A34PLAY.nextMatch())}catch(e){}
 return out})()
