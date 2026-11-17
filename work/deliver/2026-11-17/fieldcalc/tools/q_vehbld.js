// q_vehbld.js — fieldcalc: K‑104 של הישן (045: "the vehicle bodies × the fences and the buildings, every 0.2 s") על S15 — מדידה בלבד:
// כל רכב של S15SIM.veh כל 0.5 ש׳ במחזור — מעטפת (s15grDims / v.L × v.W) מול המבנים (S15J_L.bld, ‏S15D.base) ומול הגדר (S15D.fence) — בלי האזורים שמותר להיות בהם
return (()=>{const out={byBld:{},samples:0,fence:[],err:null};try{const T=S15SIM.T,dt=.5,bld=[];
 for(const [k,b] of Object.entries(S15J_L.bld||{}))bld.push(['T-'+k,b.r]);for(const b of S15D.base||[])bld.push([b.id,b.rect]);
 const ok=[];for(const r of Object.values(S15J_L.bagHalls||{}))ok.push([r[0]-30,880,r[2]+30,r[3]+4]);ok.push([7865,880,7953,1215]);   // עמדות הכבודה + הדלתות; AIR-PASS
 const inR=(x,y,r)=>x>=r[0]&&x<=r[2]&&y>=r[1]&&y<=r[3];
 const F=S15D.fence;const inPoly=(x,y)=>{let c=false;for(let i=0,j=F.length-1;i<F.length;j=i++){const a=F[i],b=F[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])c=!c}return c};
 for(const v of S15SIM.veh){let t=0;const D=(()=>{try{const ty=s15grType(v);return ty?s15grDims(ty):[v.L||40,v.W||22]}catch(e){return[v.L||40,v.W||22]}})();
  for(t=0;t<T;t+=dt){const q=s15PoseAt(v,t);if(!q)continue;out.samples++;const c=Math.cos(q[2]),s=Math.sin(q[2]),hl=D[0]/2,hw=D[1]/2;
   const P=[[q[0]+c*hl-s*hw,q[1]+s*hl+c*hw],[q[0]+c*hl+s*hw,q[1]+s*hl-c*hw],[q[0]-c*hl+s*hw,q[1]-s*hl-c*hw],[q[0]-c*hl-s*hw,q[1]-s*hl+c*hw]];
   for(const [id,r] of bld){const inn=P.filter(p=>inR(p[0],p[1],r)&&!ok.some(o=>inR(p[0],p[1],o)));if(inn.length){const k=id+'|'+v.id;const e=out.byBld[k]||(out.byBld[k]={n:0,t0:t,x:Math.round(q[0]),y:Math.round(q[1]),f:q[4]});e.n++}}
   if(P.some(p=>!inPoly(p[0],p[1]))&&out.fence.length<30)out.fence.push(v.id+' '+t+' ('+Math.round(q[0])+','+Math.round(q[1])+')')}}
 out.byBld=Object.entries(out.byBld).map(([k,e])=>k+' ×'+e.n+' מ-'+e.t0+' ('+e.x+','+e.y+') f'+e.f).sort();
 }catch(e){out.err=String(e&&e.stack||e).slice(0,300)}return out})()
