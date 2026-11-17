/* Turbo City S7F282 · C34 original bus reference.
 * c34LibInit below is extracted verbatim from the uploaded game's script_4.js.
 * No simulation, advertising, LN decorations, DOM UI or source-game modification.
 * The tiny API after it renders the current C34 bus kit in a shared world viewBox.
 */
(function(){
'use strict';
window.FLEET_GAME=1.125;
function c34LibInit(){if(window.C34)return true;
/* c34m.js — Turbo City · p378 (S7F133) · every road vehicle in the 3/4 view (oblique, K = 0.6), with the lamps.  Plain script, defines window.C34.
   Built by build_c34m.py from the game file Turbo_City_v1_96_GATE77_S7F132.html: the car painter veh() with its tables (PAL, VM, VD_T, VD_M, vdGeo …)
   and eqp() are copied verbatim (the patches marked T34), then src/c34m_core.js.  No dependence on the game's globals. */
(function (G) {
// ---- the game's helpers (verbatim) ----
const __shM=new Map(),__sh0=(h,f)=>{const n=parseInt(h.slice(1),16),m=f<0?0:255,k=Math.abs(f);return'#'+[n>>16,n>>8&255,n&255].map(v=>Math.round(v+(m-v)*k).toString(16).padStart(2,'0')).join('')},sh=(h,f)=>{if(typeof h!=='string'||typeof f!=='number')return __sh0(h,f);let M=__shM.get(h);if(M===undefined){if(__shM.size>4096)__shM.clear();M=new Map();__shM.set(h,M)}let r=M.get(f);if(r===undefined){r=__sh0(h,f);M.set(f,r)}return r};
const lg=(c,a,b,d,e,s)=>{const g=c.createLinearGradient(a,b,d,e);s.forEach((v,i)=>g.addColorStop(i/(s.length-1),v));return g};
const rr=(c,x,y,w,h,r)=>{c.beginPath();c.roundRect(x,y,w,h,r)};
const ci=(c,x,y,r,f)=>{c.beginPath();c.arc(x,y,r,0,6.2832);if(f){c.fillStyle=f;c.fill()}};
const fr=(c,f,x,y,w,h,r=0)=>{c.fillStyle=f;if(r){rr(c,x,y,w,h,r);c.fill()}else c.fillRect(x,y,w,h)};

let FX=false;            // no animated beams in the pictures
let T34=false;           // true while today's picture is painted as the texture of the 3/4 body
const ANIM=false;
// ---- the game's car painter (verbatim + T34 patches) ----
const PAL=[['White','#f4f6f8'],['Black','#22262b'],['Gray','#7d858e'],['Silver','#c3c9cf'],['Blue','#2f6fd0'],['Red','#d23a3a'],['Green','#2f9e5f'],['Brown','#7a4f31'],['Yellow','#f3c623'],['Orange','#ee7d2d'],['Teal','#1f9aa6'],['Purple','#7a4ccf']];
const RIMN=['5-Spoke','Mesh','Split 10','Turbine','Steel','Star','Multi 7','Chrome Disc'];
function rim(c,x,y,r,s){const n=[5,0,10,8,0,5,7,0][s];ci(c,x,y,r,'#0d0f12');ci(c,x,y,r*.82,lg(c,x-r,y-r,x+r,y+r,['#f1f4f7','#8c949c','#d7dce0']));c.strokeStyle='#2a2f35';c.lineWidth=Math.max(.5,r*.14);
if(n)for(let i=0;i<n;i++){const a=i/n*6.283+(s==3?.5:0);c.beginPath();c.moveTo(x,y);c.lineTo(x+Math.cos(a)*r*.8,y+Math.sin(a)*r*.8);c.stroke()}
else if(s==1){c.lineWidth=.4;for(let k=-1;k<=1;k+=.5){c.beginPath();c.moveTo(x-r*.8,y+k*r*.6);c.lineTo(x+r*.8,y+k*r*.6);c.moveTo(x+k*r*.6,y-r*.8);c.lineTo(x+k*r*.6,y+r*.8);c.stroke()}}
ci(c,x,y,r*.28,s==7?'#cfd5da':'#2a2f35')}
const VM=[['VH-HB-01','City Hatch','hatch',72,34,[.12,.62],.16,.1,[.2,.78],[0,1,2,3,4,5,6,7]],['VH-HB-02','Sport Hatch','hatch',78,36,[.14,.58],.2,.08,[.2,.78],[0,1,2,3,4,5,6,7]],['VH-SD-01','Compact Sedan','sedan',84,35,[.3,.64],.14,.08,[.18,.78],[0,1,2,3,4,5,6,7]],['VH-SD-02','Family Sedan','sedan',94,38,[.28,.62],.14,.08,[.17,.8],[0,1,2,3,4,5,6,7]],
['VH-SU-01','Crossover','suv',88,40,[.08,.66],.12,.05,[.18,.8],[0,2,4,6]],['VH-SU-02','Large SUV','suv',102,44,[.06,.7],.08,.04,[.16,.82],[0,2,4,7]],['VH-MV-01','Minivan','mv',98,40,[.06,.7],.14,.05,[.17,.8],[0,1,4,5,6,7]],['VH-PK-01','Pickup','pk',108,43,[.5,.72],.1,.03,[.16,.82],[0,2,4,7]],
['VH-PR-01','Premium Sedan','prem',106,40,[.3,.6],.2,.05,[.16,.82],[0,1,2,3,5,7]],['VH-SP-01','Sports Coupe','sport',92,43,[.38,.6],.28,.07,[.2,.8],[0,1,2,3,5,6,7]],['VH-VN-01','Cargo Van','van',110,45,[.74,.95],.08,.03,[.17,.82],[0,4,7]],['VH-TR-01','Light Truck','truck',130,46,[.74,.96],.07,.02,[.16,.28,.84],[0,4,7]]];
/* ===== D-225 (ב) · p313: the car design, rebuilt (the owner 25.10 00:02: "from the front they all look the same and the wheels are
   distorted … at least the precision of the aircraft").  Every model by its own design sheet: the outline seen from above (the nose, the
   tail, the fender flares), the face (the headlamps, the grille, the bumper), the hood, the glass house (windshield, roof, side and rear
   windows, pillars), the tail lamps, the tyres under the body (from above a wheel shows only the edge of its tread — no rim faces).
   The same length, width and cabin of every model (D-135; the anchors of the people and of the brake lamps stay where they were). ===== */
const VD_T={
 hatch:{zf:.13,pf:2.9,zr:.07,pr:4.2,tf:.07,tr:.04,fl:.9,pt:.35,hood:'flat',hl:'slim',gr:'wide',tl:'L',sb:.065,doors:4},
 sedan:{zf:.13,pf:3.1,zr:.09,pr:3.6,tf:.07,tr:.05,fl:.7,pt:.3,hood:'twin',hl:'slim',gr:'wide',tl:'bar',sb:.06,doors:4},
 suv:{zf:.09,pf:4.6,zr:.05,pr:5.5,tf:.05,tr:.03,fl:1.5,pt:.9,hood:'dome',hl:'rect',gr:'big',tl:'vert',sb:.07,doors:4},
 mv:{zf:.1,pf:3.4,zr:.04,pr:6,tf:.06,tr:.02,fl:.6,pt:.3,hood:'short',hl:'wrap',gr:'slot',tl:'vert',sb:.065,doors:4},
 pk:{zf:.08,pf:5,zr:.03,pr:8,tf:.04,tr:0,fl:1.7,pt:1.1,hood:'twin',hl:'rect',gr:'bars',tl:'vert',sb:.07,doors:4},
 prem:{zf:.14,pf:3,zr:.1,pr:3.4,tf:.07,tr:.05,fl:.8,pt:.3,hood:'long',hl:'split',gr:'big',tl:'bar',sb:.06,doors:4},
 sport:{zf:.2,pf:2.3,zr:.12,pr:2.9,tf:.12,tr:.07,fl:1.9,pt:.45,hood:'vents',hl:'slim',gr:'intakes',tl:'bar',sb:.07,doors:2},
 van:{zf:.06,pf:5.5,zr:.03,pr:9,tf:.04,tr:0,fl:.5,pt:.35,hood:'short',hl:'rect',gr:'slot',tl:'vert',sb:.06,doors:2},
 truck:{zf:.05,pf:6.5,zr:.02,pr:10,tf:.03,tr:0,fl:.4,pt:.7,hood:'cab',hl:'rect',gr:'bars',tl:'vert',sb:.05,doors:2}};
const VD_M={
 'VH-HB-01':{hl:'round',gr:'slot',hood:'flat'},
 'VH-HB-02':{hl:'slim',gr:'wide',hood:'twin',feat:['roofBlack','roofSpoiler'],doors:2},
 'VH-HB-03':{hl:'round',gr:'oval',hood:'dome',zf:.11,pf:2.6,feat:['roofContrast'],doors:2},
 'VH-SD-01':{hl:'rect',gr:'slot',hood:'flat',tl:'L'},
 'VH-SD-02':{hl:'slim',gr:'wide',hood:'twin',feat:['fin']},
 'VH-SD-03':{hl:'bar',gr:'none',hood:'flat',zr:.11,pr:2.8,feat:['hatchline']},
 'VH-SD-04':{hl:'quad',gr:'bars',hood:'long',tl:'round',feat:['lip']},
 'VH-SU-01':{hl:'split',gr:'wide',feat:['railsBlack']},
 'VH-SU-02':{hl:'rect',gr:'big',feat:['sun','rails']},
 'VH-SU-03':{hl:'slim',gr:'slot',hood:'twin',feat:['bars']},
 'VH-SU-04':{hl:'round',gr:'vslots',hood:'flat',pf:7,zf:.06,fl:1.9,pt:1.4,feat:['basket']},
 'VH-SU-05':{hl:'slim',gr:'wide',hood:'twin',tl:'bar',zr:.09,pr:3.4,feat:['roofBlack']},
 'VH-MV-01':{hl:'wrap',gr:'slot',feat:['slidetrack']},
 'VH-MV-02':{hl:'wrap',gr:'wide',feat:['pano']},
 'VH-MV-03':{hl:'split',gr:'big',feat:['rails','slidetrack']},
 'VH-PK-01':{hl:'rect',gr:'bars',feat:['toolbox'],doors:2},
 'VH-PK-02':{hl:'rect',gr:'big',feat:['tonneau']},
 'VH-PK-03':{hl:'round',gr:'slot',feat:['rollbar'],doors:2},
 'VH-PR-01':{hl:'split',gr:'big',feat:['sun']},
 'VH-PR-02':{hl:'slim',gr:'big',hood:'long',feat:['pano']},
 'VH-PR-03':{hl:'slim',gr:'wide',hood:'long',zf:.18,pf:2.6,feat:['hoodvents'],doors:2},
 'VH-PR-04':{hl:'bar',gr:'big',feat:['sun','rails']},
 'VH-SP-01':{hl:'slim',gr:'intakes',hood:'twin',feat:['stripes','spoiler']},
 'VH-SP-02':{hl:'slim',gr:'intakes',hood:'vents',zf:.24,pf:2,feat:['enginevents']},
 'VH-SP-03':{hl:'round',gr:'oval',hood:'long',zf:.2,pf:2.4},
 'VH-SP-04':{hl:'quad',gr:'bars',hood:'flat',zf:.12,pf:3.4},
 'VH-VN-01':{hl:'rect',gr:'slot',feat:['roofvents']},
 'VH-VN-02':{hl:'wrap',gr:'wide',feat:['ladder']},
 'VH-VN-03':{hl:'round',gr:'slot',feat:['deflector']},
 'VH-TR-01':{hl:'rect',gr:'bars'},
 'VS-TX-01':{hl:'rect',gr:'slot'},'VS-TX-02':{hl:'wrap',gr:'slot'},
 'VS-PL-01':{hl:'slim',gr:'wide',feat:['pushbar']},'VS-PL-02':{hl:'split',gr:'big',feat:['pushbar']},
 'VS-AM-01':{hl:'rect',gr:'slot'},'VS-AM-02':{hl:'rect',gr:'bars'},
 'VS-FR-01':{hl:'quad',gr:'bars'},'VS-FR-02':{hl:'quad',gr:'bars'},
 'VS-TW-01':{hl:'rect',gr:'bars'},'VS-TW-02':{hl:'round',gr:'bars'},
 'VS-DL-01':{hl:'wrap',gr:'wide'},'VS-DL-02':{hl:'rect',gr:'slot'},
 'VS-MN-01':{hl:'rect',gr:'bars'},'VS-GS-01':{hl:'round',gr:'slot'}};
const VDG=new Map();
// the geometry of a model: the outline (the half seen on +y, rear → front, dense at the ends), its outward normals, the insets on demand
function vdGeo(m){const id=m[0];let G=VDG.get(id);if(G)return G;
 const[,,ty,L,W,cab,,,wb]=m,D=Object.assign({feat:[]},VD_T[ty]||VD_T.sedan,VD_M[id]||VD_M[String(id).replace(/~F$/,'')]||{}),X=-L/2,H=W/2,N=76,zf=D.zf*L,zr=D.zr*L,xf=L/2-zf,xr=X+zr;
 const tyL=Math.min(.17*L,W*.42),arch=tyL*.78;
 const hb=x=>{let h=H-D.fl;for(const f of wb){const u=(x-(X+f*L))/arch;if(Math.abs(u)<1)h+=D.fl*Math.cos(u*Math.PI/2)**2}
  const tF=Math.max(0,(x-(L/2-zf*1.8))/(zf*1.8)),tR=Math.max(0,((X+zr*1.8)-x)/(zr*1.8));return h*(1-D.tf*tF*tF-D.tr*tR*tR)};
 const hw=x=>{let h=hb(x);if(x>xf){const u=Math.min(1,(x-xf)/zf);h*=Math.pow(Math.max(0,1-Math.pow(u,D.pf)),1/D.pf)}
  if(x<xr){const u=Math.min(1,(xr-x)/zr);h*=Math.pow(Math.max(0,1-Math.pow(u,D.pr)),1/D.pr)}return h};
 // the points along the curve itself: the tail and the nose as superellipse arcs by angle (the flat fronts get points along their edge too), the side between
 const P=[],K=16,NS=N-2*K;for(let k=K;k>=1;k--){const th=Math.PI/2*k/K,u=Math.pow(Math.sin(th),2/D.pr),x=xr-zr*u;P.push([x,hb(x)*Math.pow(Math.cos(th),2/D.pr)])}
 for(let i=0;i<=NS;i++){const x=xr+(xf-xr)*i/NS;P.push([x,hb(x)])}
 for(let k=1;k<=K;k++){const th=Math.PI/2*k/K,u=Math.pow(Math.sin(th),2/D.pf),x=xf+zf*u;P.push([x,hb(x)*Math.pow(Math.cos(th),2/D.pf)])}
 P[0][1]=0;P[N][1]=0;
 const Nm=P.map((p,i)=>{const a=P[Math.max(0,i-1)],b=P[Math.min(N,i+1)],dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1;return[-dy/l,dx/l]});
 const ins=new Map(),inset=d=>{let q=ins.get(d);if(!q){q=P.map((p,i)=>[p[0]-d*Nm[i][0],Math.max(0,p[1]-d*Nm[i][1])]);ins.set(d,q)}return q};
 // the whole outline as a path (d > 0 — inside, d < 0 — outside)
 const loopB=(t,d)=>{const q=d?inset(d):P;t.moveTo(q[0][0],q[0][1]);for(let i=1;i<=N;i++)t.lineTo(q[i][0],q[i][1]);for(let i=N;i>=0;i--)t.lineTo(q[i][0],-q[i][1]);t.closePath()},loop=(c,d)=>{c.beginPath();loopB(c,d)};
 // the paths that are the same in every picture of the model — kept once (Path2D) for the real canvases
 const pc=new Map(),path2=(k,b)=>{let p=pc.get(k);if(!p){p=new Path2D();b(p);pc.set(k,p)}return p};
 // the indices of a stretch of the outline: from x ≥ a, and (near the ends) while |y| ≥ yb
 const fromX=a=>{let i=0;while(i<N&&P[i][0]<a)i++;return i},lastY=(i0,yb)=>{let j=i0;while(j<N&&P[j+1][1]>=yb)j++;return j},firstY=(i1,yb)=>{let j=i1;while(j>0&&P[j-1][1]>=yb)j--;return j};
 // a band along the outline (d0 → d1 inside) on side s, between the indices i0 … i1 (as a closed path)
 const band=(c,s,i0,i1,d0,d1)=>{const a=inset(d0),b=inset(d1);c.beginPath();c.moveTo(a[i0][0],s*a[i0][1]);for(let i=i0+1;i<=i1;i++)c.lineTo(a[i][0],s*a[i][1]);for(let i=i1;i>=i0;i--)c.lineTo(b[i][0],s*b[i][1]);c.closePath()};
 const line=(c,s,i0,i1,d)=>{const a=inset(d);c.moveTo(a[i0][0],s*a[i0][1]);for(let i=i0+1;i<=i1;i++)c.lineTo(a[i][0],s*a[i][1])};
 // the front band across the nose (both sides through the middle), for |y| ≤ yb
 const nose=(c,yb,d0,d1)=>{const j=lastY(fromX(L/2-zf),yb)+1,a=inset(d0),b=inset(d1);c.beginPath();c.moveTo(a[j][0],a[j][1]);for(let i=j+1;i<=N;i++)c.lineTo(a[i][0],a[i][1]);for(let i=N;i>=j;i--)c.lineTo(a[i][0],-a[i][1]);
  for(let i=j;i<=N;i++)c.lineTo(b[i][0],-b[i][1]);for(let i=N;i>=j;i--)c.lineTo(b[i][0],b[i][1]);c.closePath()};
 const tail=(c,yb,d0,d1)=>{const j=firstY(fromX(X+zr),yb)-1,a=inset(d0),b=inset(d1);c.beginPath();c.moveTo(a[j][0],a[j][1]);for(let i=j-1;i>=0;i--)c.lineTo(a[i][0],a[i][1]);for(let i=0;i<=j;i++)c.lineTo(a[i][0],-a[i][1]);
  for(let i=j;i>=0;i--)c.lineTo(b[i][0],-b[i][1]);for(let i=0;i<=j;i++)c.lineTo(b[i][0],b[i][1]);c.closePath()};
 G={D,P,N,hw,inset,loop,loopB,path2,band,line,nose,tail,fromX,lastY,firstY,tyL,arch,zf,zr};VDG.set(id,G);return G}
// a lamp along the outline at a corner (s = side): f — the front, else the rear; the stretch from x (inside) to |y| = yb at the end
function vdLamp(c,G,s,front,xa,yb,d0,d1,housing,lens,glow){const i0=front?G.fromX(xa):0,i1=front?G.lastY(i0,yb):G.fromX(xa),j0=front?i0:G.firstY(i1,yb);
 if(front){G.band(c,s,i0,i1,d0-.25,d1+.3);c.fillStyle=housing;c.fill();G.band(c,s,i0,i1,d0,d1);c.fillStyle=lens;c.fill();if(glow){c.strokeStyle=glow;c.lineWidth=.45;c.beginPath();G.line(c,s,i0,i1,d0+.3);c.stroke()}}
 else{G.band(c,s,j0,i1,d0-.25,d1+.3);c.fillStyle=housing;c.fill();G.band(c,s,j0,i1,d0,d1);c.fillStyle=lens;c.fill();if(glow){c.strokeStyle=glow;c.lineWidth=.45;c.beginPath();G.line(c,s,j0,i1,d0+.3);c.stroke()}}}
// a point on the outline at the front side where |y| ≈ yv, moved inside by d (for round lamps)
function vdAt(G,front,yv,d){const P=G.P,N=G.N;let i=front?N:0;if(front){while(i>0&&P[i][1]<yv)i--}else{while(i<N&&P[i][1]<yv)i++}const q=G.inset(d)[i];return[q[0],q[1]]}
function veh(c,m,S,t){const[id,,ty,L,W,cab,nf,nr,wb]=m,col=m.fix||PAL[S.c][1],X=-L/2,Y=-W/2,H=W/2,on=k=>S.L[k]!==false,G=vdGeo(m),D=G.D,F=k=>D.feat.includes(k)&&!(T34&&(k=='spoiler'||k=='roofSpoiler'||(k=='enginevents'&&m[0]=='VH-SP-02')));
c.translate(L/2+10,W/2+10);
const x0=X+cab[0]*L,x1=X+cab[1]*L,cw=W*.78,lng=['suv','mv','van'].includes(ty),r0=lng?X+L*.07:x0+(x1-x0)*.22,r1=x1-(x1-x0)*(ty=='sport'?.4:.3),xm=(x0+x1)/2,sb=D.sb*W,
 bx=ty=='truck'&&!m.fix?'#e9edf1':col,dk='#1c2026',sv='#c9ced4',lux=m.ex=='lux',boxT=ty=='van'||ty=='truck';
const lt=(()=>{try{const v=parseInt(String(col).slice(1),16);return((v>>16&255)*.3+(v>>8&255)*.59+(v&255)*.11)>150}catch(e){return false}})();
const bodyG=(a,b)=>lg(c,0,-H,0,H,[sh(col,a),sh(col,b),col,sh(col,b),sh(col,a)]);
// the detail by the size on the screen (like the aircraft): full from 48 px of length, the shape, the glass and the face from 24 px, below that the body,
// the glass, the roof and the lamps — a far car or a car in a zoom costs a few drawing calls
const real=(typeof CanvasRenderingContext2D!=='undefined'&&c instanceof CanvasRenderingContext2D)||(typeof OffscreenCanvasRenderingContext2D!=='undefined'&&c instanceof OffscreenCanvasRenderingContext2D);
const tfm=c.getTransform(),lod=(()=>{const px=L*Math.hypot(tfm.a,tfm.b);return px<24?2:px<48?1:0})(),GL=v=>lod?null:v;
const PF=(k,b,st)=>{c.fillStyle=st;if(real)c.fill(G.path2(k,b));else{c.beginPath();b(c);c.fill()}},PS=(k,b,st,lw)=>{c.strokeStyle=st;c.lineWidth=lw;if(real)c.stroke(G.path2(k,b));else{c.beginPath();b(c);c.stroke()}};
// the shadow — the outline itself, outside and soft
if(on('shadow')){c.save();c.translate(2.4,3.1);if(lod<2)PF('sh',t=>G.loopB(t,-1.2),'rgba(0,0,0,.11)');PF('b0',t=>G.loopB(t,0),lod<2?'rgba(0,0,0,.17)':'rgba(0,0,0,.24)');c.restore()}
// the tyres: under the body; from above only the edge of the tread shows (a little more on the off-road and the work cars)
if(on('wheels')&&lod==0){const tl=G.tyL,tw=Math.max(3.4,W*.15);c.strokeStyle='#2d3238';c.lineWidth=.5;
 wb.forEach(f=>{const x=X+f*L,h=G.hw(x);[-1,1].forEach(d=>{const yc=d*(h-tw/2+D.pt);fr(c,'#15181c',x-tl/2,yc-tw/2,tl,tw,Math.min(2.2,tw*.45));c.beginPath();for(let k=-2;k<=2;k++){const xx=x+k*tl*.17;c.moveTo(xx,yc-tw/2+.4);c.lineTo(xx,yc+tw/2-.4)}c.stroke();
  fr(c,'rgba(255,255,255,.07)',x-tl/2+1,d<0?yc-tw/2+.3:yc+tw/2-1.1,tl-2,.8,.4)})})}
if(on('paint')){
 // the body: the sides seen from above (darker), the upper surfaces, the outline
 PF('b0',t=>G.loopB(t,0),T34?lg(c,0,-H,0,H,[sh(col,-.1),sh(col,-.03),col,sh(col,-.03),sh(col,-.1)]):bodyG(-.45,-.16));
 if(lod<2)PF('b1',t=>G.loopB(t,sb),lg(c,0,-H,0,H,[sh(col,-.08),sh(col,.12),sh(col,.18),sh(col,.12),sh(col,-.08)]));
 if(lod==0){ // a soft lengthwise light over the upper surfaces and the shoulder lines
 c.save();G.loop(c,sb);c.clip();fr(c,lg(c,X,0,L/2,0,['rgba(0,0,0,.08)','rgba(255,255,255,.07)','rgba(255,255,255,.02)','rgba(0,0,0,.06)']),X,-H,L,W);c.restore();
 c.strokeStyle='rgba(255,255,255,.22)';c.lineWidth=.55;c.beginPath();{const i0=G.fromX(X+L*.16),i1=G.fromX(L/2-L*.14);G.line(c,1,i0,i1,sb+.5);G.line(c,-1,i0,i1,sb+.5)}c.stroke();
 // the fender arches (the edge of every flare) and the sills between them
 c.strokeStyle='rgba(0,0,0,.28)';c.lineWidth=.6;c.beginPath();wb.forEach(f=>{const x=X+f*L,i0=G.fromX(x-G.arch*1.05),i1=G.fromX(x+G.arch*1.05);G.line(c,1,i0,i1,.45);G.line(c,-1,i0,i1,.45)});c.stroke()}
 if(ty=='pk'&&lod==2)fr(c,'#262b31',X+L*.045,-H+2.6,x0-2.2-X-L*.045,W-5.2,1.6);
 if(ty=='pk'&&lod<2){const a=X+L*.045,b=x0-2.2,hh=H-2.6;fr(c,sh(col,-.25),a-.8,-hh-.8,b-a+1.6,2*hh+1.6,2.2);fr(c,lg(c,a,0,b,0,['#20252b','#2c3239']),a,-hh,b-a,2*hh,1.6);c.strokeStyle='#3b424a';c.lineWidth=.8;c.beginPath();for(let x=a+3;x<b-1;x+=4.2){c.moveTo(x,-hh+.6);c.lineTo(x,hh-.6)}c.stroke();
  fr(c,'rgba(255,255,255,.18)',a-.8,-hh,1,2*hh,.4)}
 if(ty=='truck'&&lod==2)fr(c,sh(bx,-.04),X+L*.02,Y+1,x0-3-X-L*.02,W-2.2,3);
 if(ty=='truck'&&lod<2){const a=X+L*.02,b=x0-3;fr(c,'rgba(0,0,0,.25)',a+.6,Y+1.6,b-a,W-2.4,3);fr(c,lg(c,0,Y,0,H,[sh(bx,-.12),sh(bx,.06),sh(bx,-.12)]),a,Y+1,b-a,W-2.2,3);c.strokeStyle=sh(bx,-.18);c.lineWidth=.8;c.beginPath();for(let x=a+L*.06;x<b-4;x+=9){c.moveTo(x,Y+2);c.lineTo(x,H-2.4)}c.stroke();
  c.strokeStyle='rgba(0,0,0,.35)';c.lineWidth=.6;c.strokeRect(a,Y+1,b-a,W-2.2)}
 if(lod<2)PS('b0',t=>G.loopB(t,0),T34?'rgba(8,10,13,.22)':'rgba(8,10,13,.6)',lod?.8:.6)}
// the glass house: the windshield, the side windows, the rear window — the inside through the glass (p305), the tint, the reflections
const gH=x=>Math.max(1,Math.min(cw/2,G.hw(x)-sb-.5)),q5=(u,p)=>Math.pow(Math.max(0,1-Math.pow(Math.abs(u),p)),1/p);
const gx0=boxT?x0+.5:x0,gx1=x1,bF=Math.min(1.6,(x1-r1)*.12),bR=boxT?0:Math.min(1.2,Math.max(0,(r0-x0)*.25)),yg=x=>gH(x)*(.84+.16*Math.min(1,(x-gx0)/2.6,(gx1-x)/2.6)),glassB=(t,d)=>{const n=22,y0=yg(gx0)-d,y1=yg(gx1)-d;for(let k=0;k<=6;k++){const f=k/6;t.lineTo(gx0-bR*(1-f*f)+d,y0*f)}for(let i=1;i<n;i++){const x=gx0+(gx1-gx0)*i/n;t.lineTo(x,yg(x)-d)}for(let k=6;k>=0;k--){const f=k/6;t.lineTo(gx1+bF*(1-f*f)-d,y1*f)}for(let k=1;k<=6;k++){const f=k/6;t.lineTo(gx1+bF*(1-f*f)-d,-y1*f)}for(let i=n-1;i>0;i--){const x=gx0+(gx1-gx0)*i/n;t.lineTo(x,-(yg(x)-d))}for(let k=6;k>=1;k--){const f=k/6;t.lineTo(gx0-bR*(1-f*f)+d,-y0*f)}t.closePath()},glassPath=(d)=>{c.beginPath();glassB(c,d)};
const roofH=x=>boxT?Math.max(1,G.hw(x)-sb-.8):Math.max(1,gH(x)-W*.07),rf0=boxT?(ty=='van'?X+L*.05:r0):r0,roofB=(t,d=0)=>{const n=20,xc=(rf0+r1)/2,hx=(r1-rf0)/2;for(let i=0;i<=n;i++){const x=rf0+(r1-rf0)*i/n,y=(roofH(x)-d)*q5((x-xc)/hx,boxT?16:4);i?t.lineTo(x,y):t.moveTo(x,y)}for(let i=n;i>=0;i--){const x=rf0+(r1-rf0)*i/n;t.lineTo(x,-(roofH(x)-d)*q5((x-xc)/hx,boxT?16:4))}t.closePath()},roofPath=(d=0)=>{c.beginPath();roofB(c,d)};
if(on('glass')){const ws=x1-r1,dw=Math.max(2.5,ws*.3);
 PF('gl',t=>glassB(t,0),lod==2?'#2a333d':'#1b2027');
 if(lod==0){c.save();glassPath(0);c.clip();
 [-1,1].forEach(d=>{fr(c,'#3a4149',r1-1.2,d*cw*.25-cw*.15,Math.min(ws*.5,5),cw*.3,1.6);fr(c,'#4a525b',r1-1.2,d*cw*.25-cw*.15,1.5,cw*.3,.8)});fr(c,'#23282e',r1+.4,-cw*.07,Math.min(ws*.48,4),cw*.14,1);
 fr(c,'#121519',x1-dw,-cw/2,dw+1,cw,1.2);c.strokeStyle='#0b0d10';c.lineWidth=1.1;c.beginPath();c.arc(x1-dw-1.2,-cw*.25,2.2,0,6.283);c.stroke();
 if(r0-x0>2.5)fr(c,'#3a4149',x0+.6,-cw*.4,Math.min(r0-x0-1.2,3.4),cw*.8,1.4);c.restore()}
 if(lod<2)PF('gl',t=>glassB(t,0),lg(c,x0,-cw/2,x1,cw/2,['rgba(36,54,70,.66)','rgba(88,118,140,.42)','rgba(36,54,70,.6)']));
 if(lod==0){fr(c,'rgba(79,209,255,.85)',x1-Math.max(2,ws*.26),-1.5,1.3,3,.5);
 // the reflections: a sweep across the windshield, a line along each side window
 c.save();glassPath(0);c.clip();c.fillStyle='rgba(255,255,255,.13)';c.beginPath();c.moveTo(x1-ws*.85,-cw*.5);c.lineTo(x1-ws*.55,-cw*.5);c.lineTo(x1-ws*.05,cw*.1);c.lineTo(x1-ws*.35,cw*.1);c.closePath();c.fill();c.restore();
 c.strokeStyle='rgba(255,255,255,.14)';c.lineWidth=.5;glassPath(1.1);c.stroke();
 // the wipers
 c.strokeStyle='rgba(10,12,14,.55)';c.lineWidth=.4;c.beginPath();c.moveTo(x1-1.3,-cw*.36);c.lineTo(x1-2.4,-cw*.03);c.moveTo(x1-1.3,cw*.0);c.lineTo(x1-2.4,cw*.33);c.stroke();
 PS('gl',t=>glassB(t,0),'rgba(8,10,13,.55)',.5)}}
if(on('paint')){
 // the roof and the pillars
 const rC=F('roofBlack')?['#2b2f34','#16191d']:F('roofContrast')?(lt?['#2b2f34','#16191d']:['#f6f7f4','#d6d9dc']):[sh(col,.22),sh(col,-.12)];
 PF('rf',t=>roofB(t,0),lg(c,0,-cw/2,0,cw/2,[rC[1],rC[0],rC[1]]));if(!T34&&lod==1&&on('roof')&&S.v==1){const a=rf0+(r1-rf0)*.08,b=r1-(r1-rf0)*.08,yy=roofH((a+b)/2)-1.1;[-1,1].forEach(d=>{fr(c,'rgba(0,0,0,.34)',a,d*yy-.9+d*.6,b-a,1.8,.8);fr(c,sv,a,d*yy-.9,b-a,1.8,.8)})}   /* p348 */if(lod==0){PS('rf',t=>roofB(t,0),'rgba(0,0,0,.28)',.5);
 c.save();roofPath();c.clip();fr(c,'rgba(255,255,255,.16)',rf0+2,-roofH(r1-2)*.75,r1-rf0-4,1.6,.8);c.restore();
 if(!boxT){const gy=yg,pa=x1-(x1-r1)*.22,pc=x0+(r0-x0)*.3;c.strokeStyle=sh(col,-.04);c.lineWidth=1.1;c.lineCap='round';c.beginPath();[-1,1].forEach(d=>{c.moveTo(r1-.3,d*(roofH(r1)-.3));c.lineTo(pa,d*(gy(pa)-.45));if(r0-x0>1.5){c.moveTo(r0+.3,d*(roofH(r0)-.3));c.lineTo(pc,d*(gy(pc)-.45))}});c.stroke();c.lineCap='butt';
  if(D.doors>2&&ty!='sport')[-1,1].forEach(d=>{const y0=d*roofH(xm),y1=d*gH(xm);fr(c,sh(col,-.1),xm-.8,Math.min(y0,y1),1.6,Math.abs(y1-y0),.3)})}
 else if(ty=='van'){c.strokeStyle=sh(col,-.05);c.lineWidth=1.2;c.beginPath();[-1,1].forEach(d=>{c.moveTo(r1-.4,d*(roofH(r1)-.4));c.lineTo(x1-1.4,d*(gH(x1-1.4)-.3))});c.stroke();c.strokeStyle='rgba(0,0,0,.18)';c.lineWidth=.5;c.beginPath();for(let x=rf0+L*.1;x<x0-2;x+=L*.12){c.moveTo(x,-roofH(x)+1);c.lineTo(x,roofH(x)-1)}c.stroke()}
 // the roof marks of the models
 const ra=rf0,rb=r1,rw=x=>roofH(x);
 if(F('sun')||F('pano')){const s0=F('pano')?ra+(rb-ra)*.08:ra+(rb-ra)*.48,s1=rb-(rb-ra)*.08,hw2=F('pano')?rw((s0+s1)/2)*.8:rw((s0+s1)/2)*.62;fr(c,'#2a3138',s0-.6,-hw2-.6,s1-s0+1.2,2*hw2+1.2,2);fr(c,lg(c,s0,0,s1,0,['rgba(24,36,48,.96)','rgba(62,88,108,.92)']),s0,-hw2,s1-s0,2*hw2,1.6);fr(c,'rgba(255,255,255,.2)',s0+(s1-s0)*.12,-hw2*.8,(s1-s0)*.22,hw2*.6,1)}
 if(F('rails')||F('railsBlack'))[-1,1].forEach(d=>{const yy=d*(rw((ra+rb)/2)-1.1);fr(c,'rgba(0,0,0,.3)',ra+2,yy-.5+d*.5,rb-ra-4,1.3,.6);fr(c,F('rails')?sv:'#2a2e33',ra+2,yy-.65,rb-ra-4,1.3,.6)});
 if(F('bars'))[.3,.7].forEach(f=>{const xx=ra+(rb-ra)*f,h2=rw(xx)-.6;fr(c,'rgba(0,0,0,.3)',xx+.5,-h2+.6,1.4,2*h2-.6,.5);fr(c,sv,xx,-h2,1.3,2*h2,.5)});
 if(F('basket')){const h2=rw((ra+rb)/2)-1.4;c.strokeStyle='#22262b';c.lineWidth=1;c.strokeRect(ra+2.5,-h2,rb-ra-5,2*h2);c.beginPath();for(let i=1;i<4;i++){const xx=ra+2.5+(rb-ra-5)*i/4;c.moveTo(xx,-h2);c.lineTo(xx,h2)}c.stroke()}
 if(F('fin')){c.fillStyle=dk;c.beginPath();c.moveTo(ra+1.2,-1.2);c.lineTo(ra+5.2,0);c.lineTo(ra+1.2,1.2);c.closePath();c.fill()}
 if(F('roofSpoiler'))fr(c,'#1d2125',ra-1.6,-rw(ra+1)*.92,2,rw(ra+1)*1.84,.8);
 if(F('roofvents'))[.3,.55].forEach(f=>fr(c,sh(col,-.22),X+L*f,-3,5,6,1));
 if(F('ladder')){const a=X+L*.12,b=X+L*.62,yy=rw((a+b)/2)-2.2;[-1,1].forEach(d=>fr(c,sv,a,d*yy-.6,b-a,1.2,.5));for(let xx=a+2;xx<b-1;xx+=6)fr(c,sv,xx,-yy,1,2*yy,.3)}
 if(F('deflector'))fr(c,sh(col,-.22),x0-1.5,-rw(x0)+.5,4,2*rw(x0)-1,2);
 // the roof accessory of the garage (state v = 1)
 if(!T34&&on('roof')&&S.v==1){const a=ra+(rb-ra)*.08,b=rb-(rb-ra)*.08,yy=rw((a+b)/2)-1.1;   /* p348: on the roof itself — silver rails, a dark edge, two bars */[.3,.66].forEach(f=>{const xx=a+(b-a)*f;fr(c,'rgba(0,0,0,.32)',xx+.6,-yy+.5,1.4,2*yy,.6);fr(c,'#9aa2aa',xx,-yy,1.3,2*yy,.6)});[-1,1].forEach(d=>{fr(c,'rgba(0,0,0,.34)',a,d*yy-.75+d*.6,b-a,1.5,.7);fr(c,sv,a,d*yy-.75,b-a,1.5,.7)})}}}
if(on('trim')&&lod==1&&D.gr!='none'){const z=G.zf,hz=Math.min(4.6,Math.max(2.2,z*.45));G.nose(c,W*(D.gr=='oval'?.12:D.gr=='bars'?.27:.2),.5,Math.max(1.6,hz-.45));c.fillStyle=D.gr=='big'||D.gr=='bars'?'#9aa2aa':'#15181b';c.fill()}
if(on('trim')&&lod==0){
 // the hood: its front edge (the line between the hood and the face), and its character by model
 const zf=G.zf,hi=Math.min(4.6,Math.max(2.2,zf*.45)),i0=G.fromX(L/2-zf*1.25);
 c.strokeStyle='rgba(0,0,0,.3)';c.lineWidth=.6;c.beginPath();{const j=G.N;G.line(c,1,i0,j,hi);const q=G.inset(hi);for(let i=j;i>=i0;i--)c.lineTo(q[i][0],-q[i][1])}c.stroke();
 const hx0=x1+1.5,hx1=L/2-hi-1;
 if(hx1-hx0>3){
  if(D.hood=='twin'||D.hood=='long'){c.lineWidth=.55;[[-1,'rgba(255,255,255,.2)',0],[1,'rgba(0,0,0,.22)',.6]].forEach(([q,cl,o])=>{c.strokeStyle=cl;c.beginPath();[-1,1].forEach(d=>{c.moveTo(hx0+1,d*(W*.19+o));c.quadraticCurveTo((hx0+hx1)/2,d*(W*.17+o),hx1,d*(W*.13+o))});c.stroke()})}
  if(D.hood=='long'){c.strokeStyle='rgba(255,255,255,.18)';c.lineWidth=.5;c.beginPath();c.moveTo(hx0+2,0);c.lineTo(hx1-1,0);c.stroke()}
  if(D.hood=='dome'){c.fillStyle=lg(c,0,-W*.22,0,W*.22,['rgba(255,255,255,0)','rgba(255,255,255,.12)','rgba(255,255,255,0)']);c.fillRect(hx0+1,-W*.22,hx1-hx0-1,W*.44);c.strokeStyle='rgba(0,0,0,.14)';c.lineWidth=.5;c.beginPath();[-1,1].forEach(d=>{c.moveTo(hx0+1.5,d*W*.17);c.lineTo(hx1-.5,d*W*.15)});c.stroke()}
  if(D.hood=='vents')[-1,1].forEach(d=>{if(T34){fr(c,'rgba(16,18,22,.32)',hx0+(hx1-hx0)*.38,d*W*.15-1.6,4.6,3.2,1.4);return}for(let k=0;k<3;k++)fr(c,'rgba(16,18,22,.75)',hx0+(hx1-hx0)*.35+k*1.7,d*W*.15-1.4,.9,2.8,.3)});
}
 if(F('hoodvents'))[-1,1].forEach(d=>[0,1.7].forEach(o=>fr(c,'#1a1d21',x1+4+o,d*W*.2-.5,1,2.2,.3)));
 // the doors (shut lines across the sides), the handles, the fuel flap
 c.strokeStyle='rgba(0,0,0,.32)';c.lineWidth=.5;c.beginPath();const dl=[x1-.8];if(boxT)dl.push(x0+.8);else if(D.doors>2&&ty!='sport')dl.push(xm-.6,x0-1);else dl.push(x0-2.5);
 dl.forEach(x=>[-1,1].forEach(d=>{const h=G.hw(x);c.moveTo(x,d*(h-.3));c.lineTo(x-.3,d*(h-sb-.2))}));c.stroke();
 const hc='rgba(232,237,242,.85)';[-1,1].forEach(d=>{const hy=d*(G.hw(xm)-sb*.5)-.3;fr(c,hc,xm+1.4,hy,2.2,.6,.3);if(D.doors>2&&!boxT&&ty!='sport')fr(c,hc,x0+.6,d*(G.hw(x0)-sb*.5)-.3,2.2,.6,.3)});
 if(!boxT){const fx=X+L*.2;c.strokeStyle='rgba(0,0,0,.3)';c.lineWidth=.45;c.beginPath();c.arc(fx,G.hw(fx)-sb*.55,.9,0,6.283);c.stroke()}
 // the mirrors (outside the body, at the bottom of the windshield) with their glass
 [-1,1].forEach(d=>{const x=x1-1.5,h=G.hw(x+1.2)-.4;c.fillStyle=sh(col,-.12);c.beginPath();c.moveTo(x+2.8,d*h);c.lineTo(x+2.2,d*(h+2.1));c.lineTo(x+.3,d*(h+2.3));c.lineTo(x,d*(h+.2));c.closePath();c.fill();c.strokeStyle='rgba(8,10,13,.55)';c.lineWidth=.4;c.stroke();fr(c,'rgba(150,185,210,.8)',x+.05,d>0?d*h+.4:d*h-2.3,.55,1.9,.2)});
 // the boot / the tailgate, the lip, the spoilers, the slide door track, the stripes
 if(ty=='sedan'||ty=='prem'){c.strokeStyle='rgba(0,0,0,.26)';c.lineWidth=.55;c.beginPath();const ti=G.fromX(X+G.zr*1.1);const q=G.inset(G.zr*.5+2);c.moveTo(q[0][0],0);for(let i=0;i<=ti;i++)c.lineTo(q[i][0],q[i][1]);c.moveTo(q[0][0],0);for(let i=0;i<=ti;i++)c.lineTo(q[i][0],-q[i][1]);c.stroke()}
 if(ty=='hatch'||ty=='mv'||ty=='suv'||F('hatchline')){c.strokeStyle='rgba(0,0,0,.28)';c.lineWidth=.55;c.beginPath();c.moveTo(x0-(F('hatchline')?3:1.2),-gH(x0)+1);c.lineTo(x0-(F('hatchline')?3:1.2),gH(x0)-1);c.stroke()}
 if(F('lip'))fr(c,sh(col,-.35),X+1.4,-W*.3,1.2,W*.6,.5);
 if(F('spoiler'))fr(c,sh(col,-.35),X+1.6,-W*.36,2.4,W*.72,1);
 if(F('slidetrack')){c.strokeStyle='rgba(0,0,0,.4)';c.lineWidth=.7;c.beginPath();c.moveTo(x0+(x1-x0)*.08,G.hw(xm)-.9);c.lineTo(x1-(x1-x0)*.28,G.hw(xm)-.9);c.stroke()}
 if(F('stripes')){const qa=x0+(x1-x0)*.22,qb=x1-(x1-x0)*.4;[-4,2].forEach(y=>[[X+L*.08,x0-.4],[qa+.4,qb-.4],[x1+.4,L/2-1.5]].forEach(([p,q])=>{if(q-p>.8)fr(c,'rgba(255,255,255,.6)',p,y,q-p,2)}))}
 if(F('enginevents'))for(let i=0;i<4;i++)fr(c,'rgba(20,22,26,.8)',x0-3-i*2.2,-W*.2,1,W*.4,.3);
 if(F('toolbox')){fr(c,'rgba(0,0,0,.3)',x0-7.2,Y+3.6,4.6,W-7.2,1);fr(c,'#b9c0c7',x0-7,Y+3,4.2,W-6,1);fr(c,'rgba(255,255,255,.35)',x0-6.6,Y+3.6,.8,W-7.2,.4)}
 if(F('tonneau')){fr(c,lg(c,0,Y,0,H,['#2b3036','#1a1d21','#2b3036']),X+L*.045,-H+2.6,x0-2.2-X-L*.045,W-5.2,1.6);fr(c,'rgba(255,255,255,.12)',X+L*.06,-.4,x0-X-L*.08-2,.8,.4)}
 if(F('rollbar'))[0,2].forEach(o=>fr(c,sv,x0-5+o,-H+3,1.1,W-6,.5));
 if(F('pushbar')){fr(c,'#16191d',L/2-.6,-W*.3,2.2,W*.6,.8);fr(c,'#2c3137',L/2+.2,-W*.26,.8,W*.52,.4)}
 if(lux){c.strokeStyle='rgba(225,230,235,.75)';c.lineWidth=.45;glassPath(-.35);c.stroke();fr(c,'rgba(225,230,235,.7)',X+L*.15,-H+sb*.45,L*.62,.6);fr(c,'rgba(225,230,235,.7)',X+L*.15,H-sb*.45-.6,L*.62,.6)}
 // the face: the fascia band (from the hood edge to the nose), the grille deep in it, the lower lip, the emblem
 G.nose(c,H*1.01,0,hi);c.fillStyle=lg(c,L/2-hi,0,L/2,0,[sh(col,-.04),sh(col,-.18)]);c.fill();
 c.strokeStyle='rgba(255,255,255,.18)';c.lineWidth=.45;c.beginPath();{const q=G.inset(hi+.55);for(let i=i0;i<=G.N;i++)i==i0?c.moveTo(q[i][0],q[i][1]):c.lineTo(q[i][0],q[i][1]);for(let i=G.N;i>=i0;i--)c.lineTo(q[i][0],-q[i][1])}c.stroke();
 const gr=D.gr,gd=Math.max(1.6,hi-.45),noseLine=(d,yb)=>{const q=G.inset(d),j=G.lastY(G.fromX(L/2-G.zf),yb)+1;c.moveTo(q[j][0],q[j][1]);for(let i=j;i<=G.N;i++)c.lineTo(q[i][0],q[i][1]);for(let i=G.N;i>=j;i--)c.lineTo(q[i][0],-q[i][1])};
 if(gr=='wide'){G.nose(c,W*.21,.5,gd);c.fillStyle='#121519';c.fill();c.save();c.clip();c.strokeStyle='rgba(150,158,166,.5)';c.lineWidth=.4;c.setLineDash([.55,.65]);c.beginPath();for(let d=1;d<gd;d+=.75)noseLine(d,W*.21);c.stroke();c.setLineDash([]);c.restore();G.nose(c,W*.21,.5,gd);c.strokeStyle=sv;c.lineWidth=.4;c.stroke()}
 if(gr=='slot'){G.nose(c,W*.19,.55,1.5);c.fillStyle='#15181c';c.fill();G.nose(c,W*.19,.55,.95);c.fillStyle=sh(sv,-.08);c.fill();G.nose(c,W*.24,2.1,gd);c.fillStyle='#16191d';c.fill();c.save();c.clip();c.strokeStyle='rgba(120,128,136,.45)';c.lineWidth=.35;c.beginPath();noseLine((2.1+gd)/2,W*.24);c.stroke();c.restore()}
 if(gr=='big'){G.nose(c,W*.18,.4,gd+.2);c.fillStyle='#181b1f';c.fill();c.save();c.clip();c.strokeStyle='#b9c0c7';c.lineWidth=gd-.6;c.setLineDash([.6,.7]);c.beginPath();noseLine((gd+.6)/2,W*.18);c.stroke();c.setLineDash([]);c.restore();G.nose(c,W*.18,.4,gd+.2);c.strokeStyle='#e3e7ea';c.lineWidth=.6;c.stroke()}
 if(gr=='bars'){G.nose(c,W*.27,.45,gd);c.fillStyle='#15171b';c.fill();c.strokeStyle='#c7cdd3';c.lineWidth=.55;c.beginPath();for(let d=1.1;d<gd-.2;d+=.95)noseLine(d,W*.27);c.stroke();G.nose(c,W*.27,.45,gd);c.strokeStyle='#dfe3e7';c.lineWidth=.45;c.stroke()}
 if(gr=='vslots'){G.nose(c,W*.23,.5,gd);c.fillStyle='#16191d';c.fill();c.save();c.clip();c.strokeStyle=sh(col,-.06);c.lineWidth=gd;c.setLineDash([1.7,1.3]);c.beginPath();noseLine((gd+.5)/2,W*.23);c.stroke();c.setLineDash([]);c.restore()}
 if(gr=='oval'){G.nose(c,W*.12,.55,gd);c.fillStyle='#14171b';c.fill();c.save();c.clip();c.strokeStyle='rgba(150,158,166,.5)';c.lineWidth=.35;c.beginPath();for(let d=1;d<gd;d+=.8)noseLine(d,W*.12);c.stroke();c.restore();G.nose(c,W*.12,.55,gd);c.strokeStyle=sv;c.lineWidth=.5;c.stroke()}
 if(gr=='intakes'){[-1,1].forEach(d=>{const i0=G.lastY(G.fromX(L/2-G.zf*.85),W*.36),i1=G.lastY(i0,W*.13);G.band(c,d,i0,i1,.45,gd+.3);c.fillStyle='#101215';c.fill();c.save();c.clip();c.strokeStyle='rgba(120,128,136,.4)';c.lineWidth=.35;c.beginPath();for(let k=1;k<gd;k+=.8)G.line(c,d,i0,i1,.45+k);c.stroke();c.restore()});G.nose(c,W*.09,.35,1.1);c.fillStyle='#1d2126';c.fill()}
 if(gr=='none'){G.nose(c,W*.3,.35,.95);c.fillStyle='rgba(16,18,22,.8)';c.fill()}
 if(ty!='truck'&&gr!='none'&&gr!='intakes'){const q=vdAt(G,true,0,gd+1.3);ci(c,q[0],0,.8,'#d8dde1');ci(c,q[0],0,.42,sh(col,-.2))}
 // the rear: the bumper band, the plate, the double rear door of the vans
 G.tail(c,W*.36,.25,1.1);c.fillStyle=sh(col,-.3);c.fill();
 {const q=vdAt(G,false,0,.4);fr(c,'#e9ecef',q[0],-W*.12,1.1,W*.24,.3);c.strokeStyle='rgba(0,0,0,.45)';c.lineWidth=.3;c.strokeRect(q[0],-W*.12,1.1,W*.24)}
 if(ty=='van'){c.strokeStyle='rgba(0,0,0,.35)';c.lineWidth=.5;c.beginPath();c.moveTo(X+.4,0);c.lineTo(X+L*.05,0);c.stroke()}}
if(on('lights')&&lod==2){[-1,1].forEach(d=>{const q=vdAt(G,true,W*.3,1.7);ci(c,q[0],d*q[1],Math.max(1.2,W*.08),'#eef3f6')});G.tail(c,W*.42,.3,1.5);c.fillStyle='#c62a22';c.fill()}
if(on('lights')&&lod<2){
 // the headlamps by model, in the corners of the fascia band: slim swept LED, round, rectangular, wrap-around, split (a light line over a
 // small lamp), a light bar, four round
 const hl=D.hl,HS='#181d23',LN=lg(c,L/2-7,0,L/2,0,['#c7d5df','#f8fbfd']),ZF=G.zf,HI=Math.min(4.6,Math.max(2.2,ZF*.45)),kz=Math.max(ZF,L*.07);
 [-1,1].forEach(d=>{
  if(hl=='slim')vdLamp(c,G,d,true,L/2-kz*1.05,W*.19,.35,HI*.62,HS,LN,GL('rgba(255,255,255,.95)'));
  if(hl=='rect')vdLamp(c,G,d,true,L/2-kz*.7,W*.23,.35,HI-.25,HS,LN,null);
  if(hl=='wrap')vdLamp(c,G,d,true,L/2-kz*1.3,W*.2,.35,HI-.15,HS,LN,GL('rgba(255,255,255,.85)'));
  if(hl=='split'){vdLamp(c,G,d,true,L/2-kz*1.15,W*.21,.3,1.3,HS,'#f4f8fb',GL('rgba(255,255,255,.95)'));vdLamp(c,G,d,true,L/2-kz*.6,W*.25,1.75,HI-.2,HS,LN,null)}
  if(hl=='bar')vdLamp(c,G,d,true,L/2-kz*.75,W*.32,.35,HI-.3,HS,LN,null);
  if(hl=='round'){const r=Math.min(W*.095,HI*.5+.6),q=vdAt(G,true,W*.31,r+.9);ci(c,q[0],d*q[1],r+.45,HS);ci(c,q[0],d*q[1],r,'#c9ced4');ci(c,q[0],d*q[1],r-.55,lg(c,q[0]-2,0,q[0]+2,0,['#d2dde5','#f8fbfd']));ci(c,q[0],d*q[1],r*.38,'rgba(150,165,178,.9)')}
  if(hl=='quad')[W*.355,W*.215].forEach(yv=>{const r=Math.min(W*.064,HI*.38+.4),q=vdAt(G,true,yv,r+.9);ci(c,q[0],d*q[1],r+.4,HS);ci(c,q[0],d*q[1],r,lg(c,q[0]-1.5,0,q[0]+1.5,0,['#d2dde5','#f8fbfd']));ci(c,q[0],d*q[1],r*.38,'rgba(150,165,178,.9)')});
  // the amber signal at the outer end
  if(lod==0){const sa=vdAt(G,true,W*.45,.9);fr(c,'#f5a524',sa[0]-1.8,d>0?sa[1]-1.2:-sa[1]+.1,1.8,1.1,.4)}});
 if(hl=='bar'){G.nose(c,W*.32,.4,1.25);c.fillStyle='#f4f8fb';c.fill()}
 if(lod==0&&(hl=='rect'||hl=='split'||hl=='bar'||hl=='wrap'))[-1,1].forEach(d=>{const q=vdAt(G,true,W*.34,HI*.55+.6);ci(c,q[0],d*q[1],Math.min(1,HI*.22),'rgba(118,138,154,.95)');if(hl!='bar'){const q2=vdAt(G,true,W*.26,HI*.55+.6);ci(c,q2[0],d*q2[1],Math.min(.8,HI*.18),'rgba(118,138,154,.9)')}});
 // the tail lamps by model: a bar across, L-shaped, vertical in the corners, round; amber inside, the reverse lamp outside
 const tl=D.tl,TH='#4e1010',TL=lg(c,X,0,X+5,0,['#ff5348','#b81c1c']);
 if(tl=='bar'){G.tail(c,W*.42,.3,1.35);c.fillStyle=TH;c.fill();G.tail(c,W*.42,.45,1.15);c.fillStyle=TL;c.fill()}
 [-1,1].forEach(d=>{
  if(tl=='bar'||tl=='L')vdLamp(c,G,d,false,X+Math.max(G.zr*.9,L*.06),W*.26,.3,tl=='L'?2.4:1.9,TH,TL,null);
  if(tl=='vert')vdLamp(c,G,d,false,X+Math.max(G.zr*1.2,L*.07),W*.36,.3,1.8,TH,TL,null);
  if(tl=='round')[W*.36,W*.24].forEach(yv=>{const q=vdAt(G,false,yv,1.7);ci(c,q[0],d*q[1],1.35,TH);ci(c,q[0],d*q[1],1.05,'#e8352c')});
  if(lod==0){const ia=vdAt(G,false,W*.27,.7),oa=vdAt(G,false,W*.41,.7);fr(c,'#f39a2b',ia[0],d>0?ia[1]-.9:-ia[1]-.1,1.3,1,.3);fr(c,'#e3e7ea',oa[0],d>0?oa[1]-.9:-oa[1]-.1,1.3,1,.3)}});
 // a soft beam only when the state asks for it (never in the prepared pictures of the traffic)
 if(S.L.beam&&FX){const g=c.createRadialGradient(L/2,0,1,L/2+12,0,16);g.addColorStop(0,'rgba(255,246,200,.3)');g.addColorStop(1,'rgba(255,246,200,0)');c.fillStyle=g;c.fillRect(L/2,-18,18,36)}}
if(m.ex=='off'){if(lod<2){ci(c,X-2.6,0,5.8,'#15181c');ci(c,X-2.6,0,3.8,'#2c3238');ci(c,X-2.6,0,1.5,'#8a929a')}if(lod==0){const yy=roofH(r1-2)*.72;fr(c,'#1b1f24',r1-3.4,-yy,1.9,2*yy,.6);for(let k=0;k<4;k++)ci(c,r1-2.45,-yy*.75+k*yy*.5,.55,'#f1f1e8')}}
if(m.eq||m.ex&&!lux&&m.ex!='off')eqp(c,m,S,t,X,Y,L,W,x0,x1,col,on)}


const nfx=m=>m[6];
function eqp(c,m,S,t,X,Y,L,W,x0,x1,col,on){const k=m.eq||m.ex,fl=FX?Math.sin(t*9)>0:1,cx=(x0+x1)/2;
const bar=(x,a,b,wd)=>{fr(c,'#1b1d20',x-2.5,-wd/2,5,wd,2);fr(c,fl?a:sh(a,-.6),x-1.6,-wd/2+1,3.2,wd/2-1,1);fr(c,fl?sh(b,-.6):b,x-1.6,0,3.2,wd/2-1,1);if(FX){const g=c.createRadialGradient(x,0,1,x,0,22);g.addColorStop(0,fl?'rgba(255,50,50,.5)':'rgba(50,100,255,.5)');g.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=g;c.fillRect(x-22,-22,44,44)}};
if(k=='wing'&&!T34){fr(c,'#1d2024',X-1,-W*.42,6,W*.84,2);fr(c,col,X,-W*.42,3,W*.84,1)}
if(k=='stripe'){const qa=x0+(x1-x0)*.22,qb=x1-(x1-x0)*.4;[-4.5,1.5].forEach(y=>[[X+L*.1,x0-.4],[qa+.4,qb-.4],[x1+.4,X+L*.7]].forEach(([p,q])=>{if(q-p>.8)fr(c,'rgba(255,255,255,.7)',p,y,q-p,3)}));fr(c,'#14171a',L/2-L*.2,-5,L*.08,10,2)}   /* p308: the stripes stop at the glass */
if(k=='off'){ci(c,X-3,0,6,'#15181b');ci(c,X-3,0,4,'#3a4048');[-1,1].forEach(d=>fr(c,'#f1f1e8',x1+3,d*W*.28-2,3,4,1))}
if(k=='lux'){fr(c,'#d9dde1',L/2-4,-W*.2,3,W*.4,1);fr(c,'rgba(255,255,255,.7)',X+L*.15,-W/2+1.5,L*.62,.8);fr(c,'rgba(255,255,255,.7)',X+L*.15,W/2-2.3,L*.62,.8);ci(c,L/2-nfx(m)*L-4,0,1.6,'#e6e9ec')}
if(k=='open'){fr(c,'#241e1a',x0,-W*.36,x1-x0,W*.72,5);[-1,1].forEach(d=>fr(c,'#6b4a35',x0+4,d*W*.17-4,(x1-x0)*.4,8,3));fr(c,'rgba(120,170,200,.6)',x1-2,-W*.38,2,W*.76,1)}
if(k=='taxi'){c.save();c.lineCap='butt';[-1,1].forEach(d=>{const y=d*(W/2-2.3),a=X+L*.2,b=x1-.8;c.setLineDash([]);c.lineWidth=2;c.strokeStyle='#14171a';c.beginPath();c.moveTo(a,y);c.lineTo(b,y);c.stroke();c.setLineDash([1,1]);c.lineWidth=.95;c.strokeStyle='#f6f4ea';[[-.5,0],[.5,1]].forEach(([o,f])=>{c.lineDashOffset=f;c.beginPath();c.moveTo(a,y+o);c.lineTo(b,y+o);c.stroke()})});c.restore();fr(c,'rgba(0,0,0,.3)',cx-6.4,-4.4,13,10,2.4);fr(c,'#f7f3dc',cx-6,-4.5,12,9,2);fr(c,'#14171a',cx-5,-1,10,2,.6);fr(c,'#f3c623',cx-5,-3.6,10,1.4,.5)}   /* D-225 (ב) · p308: the taxi — checkers on the sides, the roof sign */
if(k=='police'){fr(c,'#f1f3f5',X+L*.12,-W/2+1,L*.7,3.5,1);fr(c,'#f1f3f5',X+L*.12,W/2-4.5,L*.7,3.5,1);fr(c,'#f1f3f5',X+2,-W*.3,x0-X-4,W*.6,2);if(on('lights')&&!T34)bar(cx,'#ff3b30','#2f6bff',W*.7)}
if(k=='amb'){fr(c,'#d62d2d',X+L*.08,-W/2+1,L*.84,3,1);fr(c,'#d62d2d',X+L*.08,W/2-4,L*.84,3,1);fr(c,'#fff',cx-7,-7,14,14,2);fr(c,'#d62d2d',cx-5,-1.6,10,3.2);fr(c,'#d62d2d',cx-1.6,-5,3.2,10);if(on('lights')&&!T34)bar(x1-5,'#ff3b30','#2f6bff',W*.76)}
if(k=='fire'){fr(c,'#f1f3f5',X+L*.04,-W/2+1,L*.9,2.5);fr(c,'#f1f3f5',X+L*.04,W/2-3.5,L*.9,2.5);if(m.lad){fr(c,'#8d949b',X+L*.06,-8,x0-X-L*.1,5,1);fr(c,'#8d949b',X+L*.06,3,x0-X-L*.1,5,1);for(let q=X+L*.08;q<x0-4;q+=5)fr(c,'#6d747b',q,-8,1.5,16)}else{ci(c,X+L*.3,0,9,'#9aa1a8');ci(c,X+L*.3,0,6,'#c8ced4')}if(on('lights')&&!T34)bar(x1-4,'#ff3b30','#ffffff',W*.78)}
if(k=='tow'){if(T34){fr(c,'#8f979f',X+L*.03,-W*.42,x0-X-L*.03-4,W*.84,1);for(let q=X+L*.03+3.4;q<x0-5;q+=3.4)fr(c,'rgba(40,46,52,.45)',q,-W*.4,.5,W*.8);fr(c,'rgba(255,255,255,.18)',X+L*.03,-W*.42,x0-X-L*.03-4,1.2)}else{fr(c,'#2a2e33',X+L*.03,-W*.42,x0-X-L*.03-4,W*.84,2);for(let q=X+L*.08;q<x0-8;q+=7)fr(c,'#474d54',q,-W*.4,1.4,W*.8);fr(c,'#e0a81e',X+2,-W*.42,3,W*.84);ci(c,x1+1,0,3.2,fl?'#ffb000':'#7a5300')}}
if(k=='maint'){if(T34){fr(c,'#4a5058',X+L*.06,-W*.3,x0-X-L*.1,W*.6,1.5)}else{fr(c,'#3a4048',X+L*.06,-W*.35,x0-X-L*.1,W*.7,3);fr(c,'#f0c53a',X+2,-W*.4,4,W*.8);for(let q=-W*.4;q<W*.4;q+=7)fr(c,'#1b1d20',X+2,q,4,3.5);ci(c,cx,0,3.2,fl?'#ffb000':'#7a5300')}}
if(k=='deliv'&&!T34){fr(c,m.band||'#2f6fd0',X+L*.06,-W/2+1,L*.62,3.5);fr(c,m.band||'#2f6fd0',X+L*.06,W/2-4.5,L*.62,3.5);fr(c,m.band||'#2f6fd0',X+L*.25,-6,L*.28,12,2);fr(c,'#fff',X+L*.3,-3,L*.18,6,1)}
if(k=='svc'){fr(c,'#e8bf2a',X+L*.06,-W/2+1,L*.7,3);fr(c,'#e8bf2a',X+L*.06,W/2-4,L*.7,3);if(!T34)ci(c,cx,0,3,fl?'#ffb000':'#7a5300')}}

// ---- the other civilian / service models of the game (verbatim rows) ----
const vm=(a,e)=>Object.assign(a,e),R8=[0,1,2,3,4,5,6,7],R6=[0,1,2,3,5,7],R4=[0,2,4,7],R3=[0,4,7];
[vm(['VH-HB-03','Mini Hatch','hatch',62,32,[.1,.6],.15,.1,[.2,.78],R8]),
vm(['VH-SD-03','Liftback Sedan','sedan',90,37,[.2,.66],.15,.07,[.17,.8],R8]),vm(['VH-SD-04','Compact Saloon','sedan',80,34,[.3,.66],.13,.09,[.2,.78],R8]),
vm(['VH-SU-03','Compact SUV','suv',82,38,[.08,.66],.13,.06,[.19,.79],R4]),vm(['VH-SU-04','Off-Road SUV','suv',98,45,[.1,.68],.06,.03,[.16,.82],R4],{ex:'off'}),vm(['VH-SU-05','Coupe Crossover','suv',92,40,[.2,.62],.2,.1,[.18,.8],R4]),
vm(['VH-MV-02','Compact MPV','mv',86,38,[.08,.68],.14,.06,[.19,.8],R8]),vm(['VH-MV-03','Family MPV','mv',104,42,[.06,.72],.12,.04,[.16,.82],R6]),
vm(['VH-PK-02','Crew-Cab Pickup','pk',116,45,[.4,.72],.09,.03,[.15,.83],R4]),vm(['VH-PK-03','Compact Pickup','pk',96,38,[.46,.72],.12,.04,[.18,.82],R4]),
vm(['VH-PR-02','Luxury Saloon','prem',118,41,[.28,.62],.2,.05,[.14,.83],R6],{ex:'lux'}),vm(['VH-PR-03','Grand Tourer','prem',100,42,[.4,.64],.26,.06,[.17,.8],R6],{ex:'lux'}),vm(['VH-PR-04','Executive SUV','suv',106,45,[.1,.7],.1,.05,[.15,.83],R6],{ex:'lux'}),
vm(['VH-SP-02','Supercar','sport',94,47,[.45,.64],.34,.05,[.2,.78],R6],{ex:'wing'}),vm(['VH-SP-03','Roadster','sport',84,40,[.4,.64],.26,.08,[.2,.78],R6],{ex:'open'}),vm(['VH-SP-04','Muscle Coupe','sport',100,44,[.38,.64],.2,.05,[.17,.8],R6],{ex:'stripe'}),
vm(['VH-VN-02','Long Panel Van','van',126,46,[.78,.96],.07,.03,[.15,.84],R3]),vm(['VH-VN-03','Short Delivery Van','van',96,44,[.72,.95],.09,.04,[.18,.82],R3]),
vm(['VS-TX-01','Taxi Sedan','sedan',90,37,[.28,.62],.14,.07,[.17,.8],R4],{fix:'#f3c623',eq:'taxi'}),vm(['VS-TX-02','Taxi MPV','mv',98,40,[.06,.7],.14,.05,[.17,.8],R4],{fix:'#f3c623',eq:'taxi'}),
vm(['VS-PL-01','Police Sedan','sedan',92,38,[.28,.62],.14,.07,[.17,.8],R4],{fix:'#1c2026',eq:'police'}),vm(['VS-PL-02','Police SUV','suv',100,44,[.1,.68],.08,.04,[.16,.82],R4],{fix:'#1c2026',eq:'police'}),
vm(['VS-AM-01','Ambulance Van','van',116,46,[.76,.96],.08,.03,[.15,.84],R3],{fix:'#f4f6f8',eq:'amb'}),vm(['VS-AM-02','Ambulance Truck','truck',128,48,[.76,.96],.07,.02,[.15,.28,.84],R3],{fix:'#f4f6f8',eq:'amb'}),
vm(['VS-FR-01','Fire Engine (Ladder)','truck',152,48,[.76,.97],.06,.02,[.14,.3,.85],R3],{fix:'#c8262b',eq:'fire',lad:1}),vm(['VS-FR-02','Fire Pumper','truck',132,47,[.74,.97],.06,.02,[.15,.84],R3],{fix:'#c8262b',eq:'fire'}),
vm(['VS-TW-01','Tow Truck (Light)','truck',116,44,[.7,.96],.08,.02,[.17,.84],R3],{fix:'#e08a1e',eq:'tow'}),vm(['VS-TW-02','Tow Truck (Heavy)','truck',142,48,[.74,.97],.06,.02,[.14,.3,.86],R3],{fix:'#d9a21c',eq:'tow'}),
vm(['VS-DL-01','Delivery Van','van',104,44,[.74,.95],.08,.03,[.18,.82],R3],{fix:'#f4f6f8',ex:'deliv',band:'#2f6fd0'}),vm(['VS-DL-02','Delivery Box Truck','truck',124,45,[.74,.96],.07,.02,[.16,.84],R3],{fix:'#f3c623',ex:'deliv',band:'#7a4f31'}),
vm(['VS-MN-01','City Maintenance Truck','pk',110,43,[.46,.72],.1,.03,[.16,.83],R4],{fix:'#f08a1c',eq:'maint'}),vm(['VS-GS-01','General Service Vehicle','van',94,42,[.7,.94],.1,.04,[.18,.82],R3],{fix:'#2e7d5b',eq:'svc'})].forEach(m=>VM.push(m));
const W6ALL={'VS-AM-01':51.3,'VS-AM-02':56.6,'VH-HB-01':37.9,'VH-HB-02':41.0,'VH-HB-03':32.6,'VH-MV-01':46.8,'VH-MV-02':41.1,'VH-MV-03':49.7,'VH-PK-01':50.0,'VH-PK-02':53.7,'VH-PK-03':44.4,'VH-PR-01':49.4,'VH-PR-02':55.0,'VH-PR-03':46.6,'VH-PR-04':49.4,'VH-SD-01':41.9,'VH-SD-02':46.8,'VH-SD-03':44.9,'VH-SD-04':39.9,'VH-SP-01':48.8,'VH-SP-02':49.8,'VH-SP-03':44.5,'VH-SP-04':53.0,'VH-SU-01':44.7,'VH-SU-02':51.8,'VH-SU-03':41.6,'VH-SU-04':49.8,'VH-SU-05':46.7,'VH-VN-01':50.0,'VH-VN-02':57.3,'VH-VN-03':43.6,'VS-DL-01':47.3,'VS-GS-01':42.7,'VS-MN-01':50.9,'VS-PL-01':45.5,'VS-PL-02':49.5,'VS-TX-01':44.9,'VS-TX-02':48.8};
// ---- C34 ----
/* ===== C34 · the 3/4 vehicles (exp34 → main line p378, S7F133) =====
   The projection (shared with the buildings): world x east, y south, z up (game px, 10 px = 1 m); screen = (x, y − z·K), K = 0.6.
   The ground plan is not foreshortened, so the footprint of a car is exactly today's footprint; a horizontal surface at height z is
   today's top-down picture moved up by z·K.  The car is therefore built as a height field over today's top-down picture (the painter
   veh() above, copied from the game): every surface that is seen from above (the hood, the boot, the shoulders, the fascia band, the
   windshield, the roof) is drawn by mapping today's picture onto it, one affine piece per triangle; the faces that the top-down view never
   showed (the lower sides, the side glass, the lower front / rear, the wheels, the mirrors, the spoiler, the inside of the bed) are drawn
   in code.  One picture per model × paint × direction × density, cached. */
const K34 = 0.6;
const C34 = G.C34 = { K: K34, dirs: 16, SUN: { x: 0.25, y: 0.32 } };
const IDS = ['VH-HB-02', 'VH-SD-02', 'VH-SU-02', 'VH-SP-01', 'VH-VN-01', 'VH-PK-01'];
C34.models = IDS.slice();
C34.PAL = PAL.map(p => p.slice());
// PARAMETRIC: everything below is driven by the game's tables — the model row (VM: type, length, width, cabin, wheels), the design
// sheet (VD_T by type + VD_M by model: lamps, grille, hood, features, doors), the width table _w6 (W6ALL) — plus ONE small table of
// heights per body type.  A model needs a row of its own here only to differ from its type.
for (const m of VM) { const w0 = W6ALL[m[0]] || m[4]; let a = null; try { a = /^V[HS]-/.test(m[0]) ? TurboCity.get(m[0]) : null } catch (e) { a = null } if (a && a.fp && a.fp[3] > 0) m[4] = a.fp[3]; else if (W6ALL[m[0]]) m[4] = W6ALL[m[0]]; m.w0 = w0 }   // p440: the painter's width (the class's real width)
for (const m of VM.slice()) if (/^V[HS]-[A-Z]{2}-\d\d$/.test(m[0])) { const f = Object.assign(m.slice(), m); f[0] = m[0] + '~F'; f[4] = m.w0; f.frozen = 1; VM.push(f) }   // p440: the frozen twin of each road model (the field, p440c) — today's width
// the reference class (TurboCity.ref × ROAD_VEHICLE_SCALE_FACTOR .8, the width cap VEHICLE_WIDTH_MAX 38) → the game scale
const REFS = { Compact: [52, 28], Sedan: [58, 30], SUV: [60, 34], Minivan: [63.75, 34], Van: [68.75, 35], Pickup: [67.5, 33], Truck: [125, 38], Police: [60, 31], Ambulance: [90.3, 36], FireTruck: [128, 40], Sports: [56, 27], Premium: [63.75, 31], Taxi: [58, 30] };
const HEAVY = new Set(['Truck', 'Ambulance', 'FireTruck']);
const TYPE_REF = { hatch: 'Compact', sedan: 'Sedan', suv: 'SUV', mv: 'Minivan', pk: 'Pickup', prem: 'Premium', sport: 'Sports', van: 'Van', truck: 'Truck' };
const ID_REF = { 'VS-TX-01': 'Taxi', 'VS-TX-02': 'Taxi', 'VS-PL-01': 'Police', 'VS-PL-02': 'Police', 'VS-AM-01': 'Ambulance', 'VS-AM-02': 'Ambulance', 'VS-FR-01': 'FireTruck', 'VS-FR-02': 'FireTruck' };
// the heights by body type, world px (10 px = 1 m, real ×1.0): the roof, the belt line (bottom of the side glass), the front edge of the hood,
// the top of the tail, the ground clearance; fB — the widest line of the body between the sill and the belt; glassTop — the van's
// windshield / cab glass ends below the roof; floor — the pickup bed floor
const HT_T = {
  hatch: { roof: 14.5, belt: 9.3, hood: 7.9, tail: 9.0, gc: 1.6, fB: .5 },
  sedan: { roof: 14.5, belt: 9.0, hood: 7.4, tail: 8.4, gc: 1.6, fB: .5 },
  prem: { roof: 14.6, belt: 9.2, hood: 7.6, tail: 8.6, gc: 1.5, fB: .5 },
  suv: { roof: 17.5, belt: 11.0, hood: 9.6, tail: 10.6, gc: 2.3, fB: .5 },
  mv: { roof: 17.0, belt: 10.4, hood: 9.0, tail: 10.2, gc: 1.8, fB: .5 },
  sport: { roof: 12.5, belt: 8.0, hood: 5.9, tail: 7.7, gc: 1.2, fB: .5 },
  van: { roof: 22.0, belt: 11.0, hood: 9.4, tail: 11.0, gc: 1.9, fB: .5, glassTop: .62 },
  pk: { roof: 18.5, belt: 11.4, hood: 10.2, tail: 11.4, gc: 2.6, fB: .5, floor: 6.6 },
  truck: { roof: 25.0, belt: 12.5, hood: 11.5, tail: 12.5, gc: 2.4, fB: .5, glassTop: .62, box: 30.0 }
};
const HT_M = { 'VH-SU-04': { roof: 18.5, gc: 3.0 }, 'VH-HB-03': { roof: 14.8 }, 'VH-SU-05': { roof: 16.2 },
  'VH-SP-02': { roof: 11.4, belt: 7.3, hood: 5.2, tail: 7.6, gc: 1.1 },   // p378: the supercar — low and wide (it read as a white skeleton)
  'VS-MN-01': { roof: 19.5 }, 'VS-TW-01': { roof: 24.0 }, 'VS-TW-02': { roof: 25.5 } };
// the rim style (the game's RIMN index) by type, the first allowed rim of the model row otherwise
const RIM_T = { hatch: 0, sedan: 6, prem: 7, suv: 2, mv: 6, sport: 3, van: 4, pk: 5, truck: 4 };
const RIMS = {};
// the sun: upper left (shadows to the lower right); LD points toward the sun
const LD = (() => { const v = [-0.42, -0.55, 0.72], n = Math.hypot(...v); return v.map(a => a / n) })();
const AMB = .62, DIF = .38, TOPB = AMB + DIF * LD[2];
const litK = n => { const d = n[0] * LD[0] + n[1] * LD[1] + n[2] * LD[2]; let b = (AMB + DIF * Math.max(0, d)) / TOPB; if (n[2] < 0) b *= 1 + .3 * n[2]; return b };
const hexRGB = h => { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255] };
const rgbS = (c, a) => a == null ? `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})` : `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
// a colour lit by b (1 = like a flat top): darker toward a cool dark, lighter toward white
const litC = (hex, b) => { const c = hexRGB(hex); if (b <= 1) { const k = b; return rgbS([c[0] * k + 14 * (1 - k), c[1] * k + 17 * (1 - k), c[2] * k + 22 * (1 - k)]) } const k = Math.min(1, (b - 1) * .6); return rgbS([c[0] + (255 - c[0]) * k, c[1] + (255 - c[1]) * k, c[2] + (255 - c[2]) * k]) };
const overlay = b => b < 1 ? `rgba(14,17,22,${Math.min(.6, 1 - b).toFixed(3)})` : `rgba(255,255,255,${Math.min(.3, (b - 1) * .6).toFixed(3)})`;
const lerp = (a, b, t) => a + (b - a) * t;
const lerp3 = (p, q, t) => [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, p[2] + (q[2] - p[2]) * t];
const sub3 = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const cross3 = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm3 = v => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n] };
const pwl = (K, x) => { if (x <= K[0][0]) return K[0][1] + (x - K[0][0]) * (K[1][1] - K[0][1]) / (K[1][0] - K[0][0] || 1); for (let i = 1; i < K.length; i++) if (x <= K[i][0]) return lerp(K[i - 1][1], K[i][1], (x - K[i - 1][0]) / (K[i][0] - K[i - 1][0] || 1)); const a = K[K.length - 2], b = K[K.length - 1]; return b[1] + (x - b[0]) * (b[1] - a[1]) / (b[0] - a[0] || 1) };

// ---------- the geometry of a model (asset units, as veh() draws it; the game scale sc turns it into world px) ----------
const GEO = new Map();
function geo(id) {
  let M = GEO.get(id); if (M) return M;
  const m = VM.find(r => r[0] === id); if (!m) throw new Error('C34: unknown model ' + id);
  const [, , ty, L, W, cab, , , wb] = m, Gg = vdGeo(m), D = Gg.D, X = -L / 2, H = W / 2;
  const FZ = /~F$/.test(id), bid = FZ ? id.slice(0, -2) : id, rk = (typeof fleetClassOf === 'function' && fleetClassOf(bid, ty)) || ID_REF[bid] || TYPE_REF[ty] || 'Sedan', R = REFS[rk], f8 = .8 * (HEAVY.has(rk) ? .9 : 1), FT = !FZ && typeof vehicleReferenceTarget === 'function' ? vehicleReferenceTarget(rk) : null, sc = FT ? FT[0] / L : Math.min(R[0] * f8 / L, 38 / W), HK = FZ ? 1 : (G.FLEET_GAME || 1.125);   // p440: the game's length of the class; the frozen twin (~F) — today's rule
  const h = Object.assign({}, HT_T[ty] || HT_T.sedan, HT_M[bid] || {}), A = v => v / sc; for (const k of ['roof', 'belt', 'hood', 'tail', 'gc', 'floor', 'box']) if (h[k] != null) h[k] *= HK;   // p440: real × 1.125 (the frozen twin × 1)
  // the wheel: the radius from the tyre of today's picture (its length seen from above), within a real range
  h.wr = h.wr || Math.max(3.0 * HK, Math.min(4.0 * HK, Math.min(.17 * L, W * .42) * sc * .45));
  // the cabin, the glass and the roof exactly as veh() computes them
  const x0 = X + cab[0] * L, x1 = X + cab[1] * L, cw = W * .78, lng = ['suv', 'mv', 'van'].includes(ty);
  const r0 = lng ? X + L * .07 : x0 + (x1 - x0) * .22, r1 = x1 - (x1 - x0) * (ty == 'sport' ? .4 : .3), xm = (x0 + x1) / 2, sb = D.sb * W, boxT = ty == 'van' || ty == 'truck';
  const gH = x => Math.max(1, Math.min(cw / 2, Gg.hw(x) - sb - .5)), q5 = (u, p) => Math.pow(Math.max(0, 1 - Math.pow(Math.abs(u), p)), 1 / p);
  const gx0 = boxT ? x0 + .5 : x0, gx1 = x1, bF = Math.min(1.6, (x1 - r1) * .12), bR = boxT ? 0 : Math.min(1.2, Math.max(0, (r0 - x0) * .25));
  const yg = x => gH(x) * (.84 + .16 * Math.min(1, (x - gx0) / 2.6, (gx1 - x) / 2.6));
  const roofH = x => boxT ? Math.max(1, Gg.hw(x) - sb - .8) : Math.max(1, gH(x) - W * .07), rf0 = boxT ? (ty == 'van' ? X + L * .05 : r0) : r0;
  const pE = boxT ? 16 : 4, xc = (rf0 + r1) / 2, hx = (r1 - rf0) / 2, roofY = x => roofH(x) * q5((x - xc) / hx, pE);
  const hi = Math.min(4.6, Math.max(2.2, Gg.zf * .45)), dT = Math.max(sb, 2.6), dA = .9;
  // heights (asset units)
  const open = m.ex == 'open', zR = open ? A(h.belt + 3.2) : A(h.roof), zBelt = A(h.belt), zHood = A(h.hood), zTail = A(h.tail), gc = A(h.gc), wr = A(h.wr);
  const uCowl = gx1 + bF, uNose = L / 2 - hi, uRG = boxT ? X + dT + 1 : gx0 - bR;
  const capK = ty == 'pk' ? [[X, zTail], [x0 - 1, zBelt], [uCowl, zBelt], [uNose, zHood]] : [[X + dT, zTail], [Math.max(X + dT + .5, uRG), zBelt], [uCowl, zBelt], [uNose, zHood]];
  for (let i = 1; i < capK.length; i++) if (capK[i][0] < capK[i - 1][0] + .4) capK[i][0] = capK[i - 1][0] + .4;   // a cab-over (the cowl at the nose): keep the profile ordered
  const zcap = x => pwl(capK, Math.max(X - 1, Math.min(L / 2 + 1, x))), zB = x => gc + h.fB * (zcap(x) - gc);
  const dC = x => { let d = sb; const a = L / 2 - Gg.zf * 1.25, b = L / 2 - Gg.zf; if (x > a) d = sb + (hi - sb) * Math.min(1, (x - a) / Math.max(.01, b - a));
    const ta = X + Gg.zr * 1.3, tb = X + Gg.zr * .9; if (x < ta) d = Math.max(d, sb + (dT - sb) * Math.min(1, (ta - x) / Math.max(.01, ta - tb))); return d };
  // the outline samples (dense at the nose and the tail), its outward normals, the three rings of the body
  const P = Gg.P, N = Gg.N, KK = 16, idx = [];
  for (let i = 0; i <= KK; i++) idx.push(i);
  for (let i = KK + 3; i < N - KK - 1; i += 3) idx.push(i);
  for (let i = N - KK; i <= N; i++) idx.push(i);
  const nrm = i => { const p = P[Math.max(0, i - 1)], q = P[Math.min(N, i + 1)], dx = q[0] - p[0], dy = q[1] - p[1], l = Math.hypot(dx, dy) || 1; return [-dy / l, dx / l] };
  const RA = [], RB = [], RC = [], RN = [];
  for (const i of idx) {
    const p = P[i], n = nrm(i), d = dC(p[0]), cu = p[0] - d * n[0], cv = Math.max(0, p[1] - d * n[1]);
    RA.push([p[0] - dA * n[0], Math.max(0, p[1] - dA * n[1]), gc]); RB.push([p[0], p[1], zB(p[0])]); RC.push([cu, cv, zcap(cu)]); RN.push(n);
  }
  // keep ring C a simple curve (no swallowtail at the nose): x non-decreasing along the front, non-increasing along the tail
  for (let j = 1; j < RC.length; j++) if (RC[j][0] < RC[j - 1][0] && RC[j][1] <= RC[j - 1][1] && RC[j - 1][0] > 0) { RC[j][0] = RC[j - 1][0]; RC[j][2] = zcap(RC[j][0]) }
  for (let j = RC.length - 2; j >= 0; j--) if (RC[j][0] > RC[j + 1][0] && RC[j][1] <= RC[j + 1][1] && RC[j + 1][0] < 0) { RC[j][0] = RC[j + 1][0]; RC[j][2] = zcap(RC[j][0]) }
  // ---- the glass house: the base loop (the glass outline of veh(), on the cap) and the roof loop (roofB of veh()), point to point ----
  const tc = pE == 4 ? .86 : .97, xcf = xc + hx * tc, xcr = xc - hx * tc;
  const baseSideY = x => boxT ? Math.max(1, Gg.hw(x) - sb) : yg(x);
  const isTruck = ty == 'truck', bx0 = boxT && !isTruck ? X + dT + .6 : gx0, bx1 = gx1;   // a truck: the glass house is the cab only (its box is a prism)
  const nS = 12, nF = 7, FR = [];   // FR: {b:[u,v,z], r:[u,v,z], sec, s}
  const roofEnd = (front, f) => { // f: 1 at the corner → 0 at the tip
    const xk = front ? xcf : xcr, yk = roofY(xk), Yh = roofH(xk), y = yk * f, t = Math.pow(Math.max(0, 1 - Math.pow(Math.min(1, y / Yh), pE)), 1 / pE);
    const x = xc + (front ? 1 : -1) * hx * Math.max(tc, t); return [x, roofY(x) * (y > 0 ? 1 : 0) || y, zR] };
  const baseEnd = (front, f) => { if (front) { const y1 = baseSideY(bx1); return [bx1 + bF * (1 - f * f), y1 * f, 0] }
    if (boxT && !isTruck) { const y0 = baseSideY(bx0), xt = X + dT; return [bx0 - (bx0 - xt) * (1 - f * f), y0 * f, 0] }
    if (isTruck) return [bx0, baseSideY(bx0) * f, 0];
    const y0 = baseSideY(bx0); return [bx0 - bR * (1 - f * f), y0 * f, 0] };
  const zb = p => (p[2] = zcap(p[0]), p);
  const push = (b, r, sec, s) => FR.push({ b: zb([b[0], s * b[1], 0]), r: [r[0], s * r[1], zR], sec, s });
  // side +1 rear → front, front cap +1 → tip → −1, side −1 front → rear, rear cap −1 → tip → +1
  for (let k = 0; k <= nS; k++) { const t = k / nS, xr = lerp(xcr, xcf, t), xb = lerp(bx0, bx1, t); push([xb, baseSideY(xb)], [xr, roofY(xr)], 'side', 1) }
  for (let k = 1; k <= nF; k++) { const f = 1 - k / nF; push(baseEnd(true, f), roofEnd(true, f), 'front', 1) }
  for (let k = nF - 1; k >= 0; k--) { const f = 1 - k / nF; push(baseEnd(true, f), roofEnd(true, f), 'front', -1) }
  for (let k = nS - 1; k >= 0; k--) { const t = k / nS, xr = lerp(xcr, xcf, t), xb = lerp(bx0, bx1, t); push([xb, baseSideY(xb)], [xr, roofY(xr)], 'side', -1) }
  for (let k = 1; k <= nF; k++) { const f = 1 - k / nF; push(baseEnd(false, f), roofEnd(false, f), 'rear', -1) }
  for (let k = nF - 1; k >= 1; k--) { const f = 1 - k / nF; push(baseEnd(false, f), roofEnd(false, f), 'rear', 1) }
  // the sections of the loop (index ranges, inclusive of the shared corner points)
  const iSideP = [0, nS], iFront = [nS, nS + 2 * nF], iSideN = [nS + 2 * nF, 2 * nS + 2 * nF], iRear = [2 * nS + 2 * nF, FR.length];   // rear wraps to 0
  // the windshield / rear window: texture when the slope is gentle enough for today's picture to stretch onto it
  const rise = (zR - zBelt) * sc, wsTex = !boxT && (uCowl - r1) * sc >= .55 * rise, rwTex = !boxT && ((r0 - (gx0 - bR)) * sc >= .7 * rise);
  // the wheels
  const tw = Math.max(3.4, W * .15), wheels = [];
  for (const f of wb) for (const s of [1, -1]) { const u = X + f * L, hw = Gg.hw(u); wheels.push({ u, s, vo: s * (hw + D.pt), vi: s * (hw + D.pt - tw), r: wr, ra: wr + A(.75), hw }) }
  // the doors (veh(): the shut lines)
  const dl = [x1 - .8]; if (boxT) dl.push(x0 + .8); else if (D.doors > 2 && ty != 'sport') dl.push(xm - .6, x0 - 1); else dl.push(x0 - 2.5);
  if (ty == 'van') dl.push(x0 - (x0 - X) * .4);   // the sliding cargo door (a 3/4 detail: its rear seam)
  M = { id, m, ty, L, W, X, H, sc, h, Gg, D, open, dC, eq: m.eq || null, ex: m.ex || null, baseSideYF: baseSideY, rim: RIMS[id] != null ? RIMS[id] : ((m[9] || []).includes(RIM_T[ty]) ? RIM_T[ty] : (m[9] || [0])[0]), x0, x1, cw, r0, r1, xm, sb, boxT, gH, yg, roofH, roofY, rf0, xc, hx, xcf, xcr, hi, dT, dA, zR, zBelt, zHood, zTail, gc, wr,
    zcap, zB, capK, uCowl, uNose, uRG, RA, RB, RC, RN, FR, iSideP, iFront, iSideN, iRear, wsTex, rwTex, wheels, tw, dl, A, bx0, bx1, gx0, gx1, bF, bR,
    feat: k => D.feat.includes(k), bed: ty == 'pk' ? { u0: X + L * .045, u1: x0 - 2.2, hh: H - 2.6, zf: A(h.floor || 6.5) } : null };
  // the bounding radius (for the canvas size)
  M.rad = Math.hypot(L / 2, H + 3) * sc;
  GEO.set(id, M); return M;
}
C34.geo = geo;
C34.len = id => { const M = geo(id); return +(M.L * M.sc).toFixed(2) };       // the world length (game px)
C34.wid = id => { const M = geo(id); return +(M.W * M.sc).toFixed(2) };       // the world width (game px, the ×1.25 contract)
C34.all = () => VM.filter(m => /^V[HS]-[A-Z]{2}-\d\d$/.test(m[0])).map(m => m[0]);   // p440: not the frozen twins   // every road model of the game's table (civilian VH-*, service VS-*)

// ---------- today's picture as a texture (veh() with the 3/4 adjustments: no shadow, no tyres, a neutral side band) ----------
const TEX = new Map(); let SCR = null;   // SCR: the scratch layer of the shadows
function texture(id, col, res) {
  const M = geo(id), T = Math.max(2, Math.round(res * M.sc * 2.6 * 2) / 2), key = id + '|' + col + '|' + T;
  let t = TEX.get(key); if (t) { TEX.delete(key); TEX.set(key, t); return t }
  const cv = document.createElement('canvas'), L = M.L, W = M.W; cv.width = Math.ceil((L + 20) * T); cv.height = Math.ceil((W + 20) * T);
  const c = cv.getContext('2d'); c.scale(T, T);
  const mc = M.m.slice(); Object.assign(mc, M.m); const pi = PAL.findIndex(p => p[1].toLowerCase() === col); if (!M.m.fix && pi < 0) mc.fix = col;
  T34 = true; try { veh(c, mc, { v: 0, c: Math.max(0, pi), r: 0, d: 0, f: 0, L: { shadow: false, wheels: false } }, 0) } finally { T34 = false }
  t = { cv, T, u0: -L / 2 - 10, v0: -W / 2 - 10, wu: cv.width / T, hv: cv.height / T, bytes: cv.width * cv.height * 4 };
  TEX.set(key, t); while (TEX.size > C34.texMax) TEX.delete(TEX.keys().next().value); return t;
}
C34.texture = texture;
C34.texMax = 24;

// ---------- drawing helpers ----------
function aff(t0, t1, t2, p0, p1, p2) {
  const a1 = t1[0] - t0[0], b1 = t1[1] - t0[1], a2 = t2[0] - t0[0], b2 = t2[1] - t0[1], det = a1 * b2 - a2 * b1;
  if (Math.abs(det) < 1e-7) return null;
  const q1x = p1[0] - p0[0], q1y = p1[1] - p0[1], q2x = p2[0] - p0[0], q2y = p2[1] - p0[1];
  const i11 = b2 / det, i12 = -a2 / det, i21 = -b1 / det, i22 = a1 / det;
  const ma = q1x * i11 + q2x * i21, mc = q1x * i12 + q2x * i22, mb = q1y * i11 + q2y * i21, md = q1y * i12 + q2y * i22;
  return [ma, mb, mc, md, p0[0] - ma * t0[0] - mc * t0[1], p0[1] - mb * t0[0] - md * t0[1]];
}
const INF = .6;
// a triangle of the surface: 3D points (u, v, z) — the texture coordinates are (u, v), the place on the screen is the projection
function texTri(g, tex, Pj, a, b, c) {
  const p0 = Pj(a), p1 = Pj(b), p2 = Pj(c), A = aff(a, b, c, p0, p1, p2); if (!A) return;
  const area = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]); if (Math.abs(area) < .02) return;
  // the clip triangle grown by INF px on every edge (the edges moved out, the corners mitred, a sharp corner capped), so that the
  // neighbouring triangles overlap and no anti-aliased seam lets the ground through
  const P = area > 0 ? [p0, p1, p2] : [p0, p2, p1], E = [];
  for (let i = 0; i < 3; i++) { const a = P[i], b = P[(i + 1) % 3], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, nx = dy / l, ny = -dx / l; E.push([a[0] + nx * INF, a[1] + ny * INF, dx / l, dy / l, nx, ny]) }
  const Q = [];
  for (let i = 0; i < 3; i++) { const e0 = E[(i + 2) % 3], e1 = E[i], v = P[i], den = e0[2] * e1[3] - e0[3] * e1[2];
    let q; if (Math.abs(den) > 1e-6) { const t = ((e1[0] - e0[0]) * e1[3] - (e1[1] - e0[1]) * e1[2]) / den; q = [e0[0] + e0[2] * t, e0[1] + e0[3] * t] } else q = [v[0] + e1[4] * INF, v[1] + e1[5] * INF];
    const dx = q[0] - v[0], dy = q[1] - v[1], l = Math.hypot(dx, dy), cap = INF * 3; if (l > cap) { q = [v[0] + dx / l * cap, v[1] + dy / l * cap] } Q.push(q) }
  g.save(); g.beginPath(); g.moveTo(Q[0][0], Q[0][1]); g.lineTo(Q[1][0], Q[1][1]); g.lineTo(Q[2][0], Q[2][1]); g.closePath(); g.clip();
  g.setTransform(A[0], A[1], A[2], A[3], A[4], A[5]); g.drawImage(tex.cv, tex.u0, tex.v0, tex.wu, tex.hv); g.restore();
}
function poly(g, pts) { g.beginPath(); g.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]); g.closePath() }
function hull(pts) {
  const p = pts.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]), cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]), lo = [], up = [];
  for (const q of p) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q) }
  for (let i = p.length - 1; i >= 0; i--) { const q = p[i]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q) }
  return lo.slice(0, -1).concat(up.slice(0, -1));
}
const sarea = pts => { let a = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1] } return a / 2 };

// ---------- one picture ----------
function render(id, col, k, N, res, opt) {
  if (geo(id).m.fix) col = geo(id).m.fix.toLowerCase();   // a service vehicle keeps its own paint
  opt = opt || {};
  const M = geo(id), th = k / N * Math.PI * 2, cs = Math.cos(th), sn = Math.sin(th), sc = M.sc, K = K34, SUN = C34.SUN;
  const tex = texture(id, col, res), L = M.L, W = M.W, X = M.X, H = M.H;
  // world (relative to the ground centre of the car), then device
  const wx = (u, v) => sc * (u * cs - v * sn), wy = (u, v, z) => sc * (u * sn + v * cs - K * z);
  // the bounds: the body rings, the roof, the mirrors, the shadow
  let x0b = 1e9, x1b = -1e9, y0b = 1e9, y1b = -1e9;
  const grow = (x, y) => { if (x < x0b) x0b = x; if (x > x1b) x1b = x; if (y < y0b) y0b = y; if (y > y1b) y1b = y };
  // the bounds, tight: the body (ground ring, the top ring at its height), the roof, the mirrors, the spoilers, and their shadows
  const zTop = M.zR + M.A(.6), sxz = z => SUN.x * z * sc, syz = z => SUN.y * z * sc;
  const pt = (u, v, z, shz) => { grow(wx(u, v), wy(u, v, z)); grow(wx(u, v) + sxz(shz), wy(u, v, 0) + syz(shz)) };
  for (const p of M.RB) for (const s of [1, -1]) { const v = s * (p[1] + .6); pt(p[0], v, 0, M.zBelt); pt(p[0], v, M.zcap(p[0]) + M.A(.3), M.zBelt) }
  for (const f of M.FR) pt(f.r[0], f.r[1], zTop, M.zR);
  for (const s of [1, -1]) { const x = M.x1 - 1.5, h = M.Gg.hw(x + 1.2) + 2.6; pt(x, s * h, M.zBelt + M.A(1.2), M.zBelt); pt(x + 2.8, s * h, M.zBelt + M.A(1.2), M.zBelt) }
  if (M.feat('spoiler')) for (const s of [1, -1]) pt(X + 1.2, s * M.W * .37, M.zcap(X + 2.8) + M.A(1.9), M.zcap(X + 2.8) + M.A(1.9));
  if (M.feat('roofSpoiler')) for (const s of [1, -1]) pt(M.rf0 - 2.8, s * M.roofY(M.rf0 + 3), zTop, M.zR);
  const extras = buildExtras(M, col, opt);   // p378: the extras (the roof rack, the light bars, the tow deck …) count in the bounds
  for (const e of extras) for (const q of e.base) pt(q[0], q[1], e.z1, e.z1);
  const mg = 1.4 + 2 / res; x0b -= mg; y0b -= mg; x1b += mg; y1b += mg;
  const ox = Math.ceil(-x0b * res), oy = Math.ceil(-y0b * res), cw = Math.ceil((x1b - x0b) * res) + 1, ch = Math.ceil((y1b - y0b) * res) + 1;
  const cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
  const g = cv.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high'; g.lineJoin = 'round'; g.lineCap = 'round';
  const Pj = p => [ox + res * wx(p[0], p[1]), oy + res * wy(p[0], p[1], p[2])];
  const Pu = (u, v, z) => Pj([u, v, z]);
  const U = res * sc;                         // device px per asset unit
  const wn = n => [n[0] * cs - n[1] * sn, n[0] * sn + n[1] * cs, n[2]];       // a local direction in the world
  const vis = n => { const w = wn(n); return w[1] * K + w[2] };
  const depth = p => wy(p[0], p[1], 0) / sc * 0 + (sc * (p[0] * sn + p[1] * cs)) * K + sc * p[2];
  const lb = n => litK(norm3(wn(n)));
  const base = col;
  // ---- the shadow: drawn at half density on a scratch layer (one path per kind, so overlaps never double), then laid down soft ----
  {
    const hw2 = Math.ceil(cw / 2) + 2, hh2 = Math.ceil(ch / 2) + 2;
    if (!SCR) SCR = document.createElement('canvas');
    if (SCR.width < hw2 || SCR.height < hh2) { SCR.width = Math.max(SCR.width, hw2); SCR.height = Math.max(SCR.height, hh2) }
    const s = SCR.getContext('2d'); s.setTransform(1, 0, 0, 1, 0, 0); s.clearRect(0, 0, hw2 + 2, hh2 + 2); s.setTransform(.5, 0, 0, .5, 0, 0);
    const ring = (R, dx, dy) => { const pts = []; for (let j = 0; j < R.length; j++) pts.push([R[j][0], R[j][1]]); for (let j = R.length - 1; j >= 0; j--) pts.push([R[j][0], -R[j][1]]);
      return pts.map(q => [ox + res * (wx(q[0], q[1]) + dx), oy + res * (sc * (q[0] * sn + q[1] * cs) + dy)]) };
    const addPoly = P => { s.moveTo(P[0][0], P[0][1]); for (let i = 1; i < P.length; i++) s.lineTo(P[i][0], P[i][1]); s.closePath() };
    const zc = M.zBelt * sc, roofPts = M.FR.map(f => [f.r[0], f.r[1]]);
    // the drop shadow: the body swept from the ground to the belt, the glass house from the belt to the roof
    s.beginPath(); for (let t = 0; t <= 1.0001; t += .25) addPoly(ring(M.RB, SUN.x * zc * t, SUN.y * zc * t));
    for (let t = 0; t <= 1.0001; t += .34) { const z = lerp(M.zBelt, M.zR, t) * sc; addPoly(roofPts.map(q => [ox + res * (wx(q[0], q[1]) + SUN.x * z), oy + res * (sc * (q[0] * sn + q[1] * cs) + SUN.y * z)])) }
    s.fillStyle = 'rgba(0,0,0,.24)'; s.fill('nonzero');
    // the contact shadow: right under the body, a little wider than the footprint, darker under the tyres
    s.beginPath(); addPoly(ring(M.RB.map(p => [p[0], p[1] + .6, 0]), .3, .4)); s.fillStyle = 'rgba(0,0,0,.26)'; s.fill();
    s.beginPath(); for (const w of M.wheels) { const c0 = Pu(w.u, (w.vo + w.vi) / 2, 0); s.moveTo(c0[0] + w.r * U * 1.1, c0[1]); s.ellipse(c0[0], c0[1], w.r * U * 1.1, M.tw * U * .9, 0, 0, 7) } s.fillStyle = 'rgba(0,0,0,.25)'; s.fill();
    g.save(); try { g.filter = `blur(${(.75 * res).toFixed(2)}px)` } catch (e) { } g.drawImage(SCR, 0, 0, hw2, hh2, 0, 0, hw2 * 2, hh2 * 2); g.restore();
  }
  // ---- which side is turned to the viewer ----
  const sideV = s => vis([0, s, 0]), nearS = sideV(1) > .02 ? 1 : sideV(-1) > .02 ? -1 : 0;
  // the arch of a wheel in the plane of the body side (a circle around the hub), as a polygon on the screen
  const archPts = (w, rad, vv, zmin) => { const pts = []; for (let i = 0; i <= 32; i++) { const a = i / 32 * Math.PI * 2, z = w.r + Math.sin(a) * rad; pts.push([w.u + Math.cos(a) * rad, vv, zmin != null ? Math.max(zmin, z) : z]) } return pts.map(Pj) };
  // ---- the wheels: the wells, the tyres (far side first) ----
  const drawWheel = (w) => {
    const n = 22, Aa = [], Bb = [];
    for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, u = w.u + Math.cos(a) * w.r, z = w.r + Math.sin(a) * w.r; Aa.push(Pu(u, w.vo, z)); Bb.push(Pu(u, w.vi, z)) }
    g.fillStyle = '#16191d'; poly(g, hull(Aa.concat(Bb))); g.fill();
    // the tread lit from above: a lighter band along the top of the tyre
    const out = vis([0, w.s, 0]);
    if (out > .02) {
      const c0 = Pu(w.u, w.vo, w.r), cx = Pu(w.u + w.r, w.vo, w.r), cz = Pu(w.u, w.vo, 2 * w.r);
      g.save(); g.setTransform(cx[0] - c0[0], cx[1] - c0[1], cz[0] - c0[0], cz[1] - c0[1], c0[0], c0[1]);
      g.fillStyle = '#1d2025'; g.beginPath(); g.arc(0, 0, 1, 0, 7); g.fill();
      g.strokeStyle = 'rgba(255,255,255,.07)'; g.lineWidth = .06; g.beginPath(); g.arc(0, 0, .9, 0, 7); g.stroke();
      drawRim(g, opt.rim != null && opt.rim >= 0 ? opt.rim : M.rim, .64);
      // the fender shades the top of the wheel
      const gr = g.createLinearGradient(0, 1, 0, -.2); gr.addColorStop(0, 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
      g.fillStyle = gr; g.beginPath(); g.arc(0, 0, 1.01, 0, 7); g.fill();
      g.restore();
    }
  };
  const ws = M.wheels.slice().sort((a, b) => depth([a.u, a.vo, a.r]) - depth([b.u, b.vo, b.r]));
  if (nearS) for (const w of M.wheels) if (w.s === nearS) { g.fillStyle = '#0b0d10'; poly(g, archPts(w, w.ra * .98, w.s * (w.hw - 1), M.gc)); g.fill() }
  for (const w of ws) if (w.s !== nearS) drawWheel(w);
  for (const w of ws) if (w.s === nearS) drawWheel(w);
  // ---- the body: the lower band (sill → widest line) and the upper band (widest line → the edge of the top), both sides ----
  const faces = [];
  for (const s of [1, -1]) for (let j = 0; j < M.RB.length - 1; j++) {
    const n2 = [(M.RN[j][0] + M.RN[j + 1][0]) / 2, s * (M.RN[j][1] + M.RN[j + 1][1]) / 2];
    const f3 = (p) => [p[0], s * p[1], p[2]];
    const a0 = f3(M.RA[j]), a1 = f3(M.RA[j + 1]), b0 = f3(M.RB[j]), b1 = f3(M.RB[j + 1]), c0 = f3(M.RC[j]), c1 = f3(M.RC[j + 1]);
    for (const [lvl, p0, p1, p2, p3] of [[0, a0, a1, b1, b0], [1, b0, b1, c1, c0]]) {
      let n = norm3(cross3(sub3(p1, p0), sub3(p3, p0))); if (n[0] * n2[0] + n[1] * n2[1] < 0) n = [-n[0], -n[1], -n[2]];
      if (Math.abs(n[0]) + Math.abs(n[1]) + Math.abs(n[2]) < .1) continue;
      const vv = vis(n); if (vv <= .004) continue;
      faces.push({ lvl, s, p: [p0, p1, p2, p3], n, d: depth([(p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2, (p0[2] + p2[2]) / 2]) });
    }
  }
  faces.sort((a, b) => a.lvl - b.lvl || a.d - b.d);
  const clipArches = () => {   // the near side has holes at the wheels
    if (!nearS) return false; g.save(); g.beginPath(); g.rect(-5, -5, cw + 10, ch + 10);
    for (const w of M.wheels) if (w.s === nearS) { const a = archPts(w, w.ra, w.s * w.hw); let pts = a; if (sarea(pts) > 0) pts = pts.slice().reverse(); g.moveTo(pts[0][0], pts[0][1]); for (const q of pts) g.lineTo(q[0], q[1]); g.closePath() }
    g.clip('evenodd'); return true };
  const bodyB = litBase(base), q2 = b => Math.round(b * 100) / 100;
  // faces of one lit colour are filled as ONE path (adjacent quads then join without a seam)
  const fillGroups = (list, colorOf) => { const G2 = new Map(); for (const f of list) { const c = colorOf(f); let a = G2.get(c); if (!a) G2.set(c, a = []); a.push(f) }
    for (const [c, a] of G2) { g.fillStyle = c; g.beginPath(); for (const f of a) { const P = f.p.map(Pj); g.moveTo(P[0][0], P[0][1]); for (let i = 1; i < P.length; i++) g.lineTo(P[i][0], P[i][1]); g.closePath() } g.fill() } };
  // two passes so that the seams between faces of different light never let the ground show through: first the whole band in one
  // path (the darkest light), then each light group on top
  const drawBand = (list, clip) => {
    if (!list.length) return; const cl = clip && clipArches();
    const L0 = list.filter(f => f.lvl === 0), L1 = list.filter(f => f.lvl === 1);
    if (L0.length) { const bmin = Math.min(...L0.map(f => q2(lb(f.n)))); fillGroups(L0, () => litC(bodyB, bmin)); fillGroups(L0.filter(f => q2(lb(f.n)) > bmin), f => litC(bodyB, q2(lb(f.n)))) }
    for (const f of L1) { texTri(g, tex, Pj, f.p[0], f.p[1], f.p[2]); texTri(g, tex, Pj, f.p[0], f.p[2], f.p[3]) }
    if (L1.length) { // the light of the shoulder: a dark veil (alpha a) or a light one; the common part in one path, the rest per group
      const al = f => { const b = q2(lb(f.n) * .97); return b < 1 ? Math.min(.6, 1 - b) : -Math.min(.3, (b - 1) * .6) };
      const dk = L1.filter(f => al(f) > 0), li = L1.filter(f => al(f) < 0);
      if (dk.length) { const a0 = Math.min(...dk.map(al)); fillGroups(dk, () => `rgba(14,17,22,${a0.toFixed(3)})`);
        fillGroups(dk.filter(f => al(f) > a0 + .004), f => `rgba(14,17,22,${((al(f) - a0) / (1 - a0)).toFixed(3)})`) }
      if (li.length) { const a0 = Math.min(...li.map(f => -al(f))); fillGroups(li, () => `rgba(255,255,255,${a0.toFixed(3)})`);
        fillGroups(li.filter(f => -al(f) > a0 + .004), f => `rgba(255,255,255,${((-al(f) - a0) / (1 - a0)).toFixed(3)})`) } }
    if (cl) g.restore() };
  drawBand(faces.filter(f => f.s !== nearS), false);
  drawBand(faces.filter(f => f.s === nearS), true);
  // the details of the lower body: the sill, the door lines, the arch lips, the lower front and rear
  lowerDetails(g, M, Pj, Pu, vis, lb, nearS, clipArches, U, base, faces);
  // ---- the top of the body (hood, boot, the bed rails …): today's picture on a height field, piece by piece along the car ----
  {
    const loop = []; for (const p of M.RC) loop.push([p[0], p[1]]); for (let j = M.RC.length - 1; j >= 0; j--) loop.push([M.RC[j][0], -M.RC[j][1]]);
    const K2 = M.capK, xs = [-1e3].concat(K2.slice(1, -1).map(q => q[0]), [1e3]);
    for (let i = 0; i < xs.length - 1; i++) {
      const xa = Math.max(xs[i], X - 2), xb = Math.min(xs[i + 1], L / 2 + 2); if (xb <= xa) continue;
      const pa = [xa, 0, M.zcap(xa)], pb = [xb, 0, M.zcap(xb)], pc = [xa, 1, M.zcap(xa)];
      const T = aff(pa, pb, pc, Pj(pa), Pj(pb), Pj(pc)); if (!T) continue;
      g.save(); g.setTransform(T[0], T[1], T[2], T[3], T[4], T[5]);
      g.beginPath(); g.moveTo(loop[0][0], loop[0][1]); for (const q of loop) g.lineTo(q[0], q[1]); g.closePath();
      if (M.bed) { const b = M.bed; g.rect(b.u0, -b.hh, b.u1 - b.u0, 2 * b.hh) }
      g.clip('evenodd');
      const e = .5 / U; g.beginPath(); g.rect(xa - (i ? e : 0), -H - 4, xb - xa + e * 2, W + 8); g.clip();
      g.drawImage(tex.cv, tex.u0, tex.v0, tex.wu, tex.hv); g.restore();
    }
  }
  if (M.bed) drawBed(g, M, Pj, Pu, vis, lb, tex, U);
  // ---- the extras: the mirrors, the spoiler, the roof spoiler, the toolbox (behind the glass house first, the rest after) ----
  const glassD = depth([M.xc, 0, (M.zBelt + M.zR) / 2]);
  for (const e of extras) e.d = depth(e.c);
  extras.sort((a, b) => a.d - b.d);
  for (const e of extras) if (e.d < glassD && !e.roofX) drawPrism(g, e, Pj, vis, lb, tex, U);
  // ---- the glass house ----
  drawGlassHouse(g, M, Pj, vis, lb, tex, U, base, nearS);
  // ---- the roof: today's roof, lifted ----
  {
    if (!M.open) { const pr = [M.xc, 0, M.zR], T = aff(pr, [pr[0] + 1, 0, M.zR], [pr[0], 1, M.zR], Pj(pr), Pj([pr[0] + 1, 0, M.zR]), Pj([pr[0], 1, M.zR]));
    g.save(); g.setTransform(T[0], T[1], T[2], T[3], T[4], T[5]); g.beginPath(); const rl = M.FR.map(f => f.r); g.moveTo(rl[0][0], rl[0][1]); for (const q of rl) g.lineTo(q[0], q[1]); g.closePath();
    g.clip(); g.drawImage(tex.cv, tex.u0, tex.v0, tex.wu, tex.hv); g.restore();
    // the edge of the roof turned to the viewer: a crease under it (the tall box of a van), a little light on it
    const edgeLine = (dz, st, w) => { g.save(); g.strokeStyle = st; g.lineWidth = Math.max(.5, w * U); g.beginPath(); let on = false;
      for (let i = 0; i <= rl.length; i++) { const a = M.FR[i % rl.length], b = M.FR[(i + 1) % rl.length], n = [b.r[1] - a.r[1], -(b.r[0] - a.r[0]), 0];
        const outw = n[0] * (a.r[0] - M.xc) + n[1] * a.r[1] > 0 ? n : [-n[0], -n[1], 0], vvv = wn(norm3(outw))[1];
        if (vvv > .25) { const p = Pj([a.r[0], a.r[1], a.r[2] - dz]), q = Pj([b.r[0], b.r[1], b.r[2] - dz]); if (!on) { g.moveTo(p[0], p[1]); on = true } g.lineTo(q[0], q[1]) } else on = false }
      g.stroke(); g.restore() };
    if (M.boxT) edgeLine(M.A(.45), 'rgba(0,0,0,.16)', .7);
    edgeLine(0, 'rgba(255,255,255,.16)', .35); }
  }
  for (const e of extras) if (e.d >= glassD || e.roofX) drawPrism(g, e, Pj, vis, lb, tex, U);
  return { cv, ox, oy, k, N, res };
}
function litBase(col) { return sh(col, -.06) }
C34.render = render;

// ---------- the rims (in the plane of the wheel disc, unit = the tyre radius) ----------
function drawRim(g, s, rr) {
  const n = [5, 0, 10, 8, 0, 5, 7, 0][s] || 0;
  if (s === 4) { // steel
    g.fillStyle = '#3c4148'; g.beginPath(); g.arc(0, 0, rr, 0, 7); g.fill();
    g.strokeStyle = '#5b626a'; g.lineWidth = rr * .1; g.beginPath(); g.arc(0, 0, rr * .82, 0, 7); g.stroke();
    g.fillStyle = '#23272c'; for (let i = 0; i < 6; i++) { const a = i / 6 * 6.283; g.beginPath(); g.arc(Math.cos(a) * rr * .55, Math.sin(a) * rr * .55, rr * .1, 0, 7); g.fill() }
    g.fillStyle = '#9aa2aa'; g.beginPath(); g.arc(0, 0, rr * .24, 0, 7); g.fill(); return;
  }
  const gr = g.createLinearGradient(-rr, -rr, rr, rr); gr.addColorStop(0, '#f1f4f7'); gr.addColorStop(.5, '#8c949c'); gr.addColorStop(1, '#d7dce0');
  if (s === 7) { const g2 = g.createRadialGradient(-rr * .3, -rr * .3, 0, 0, 0, rr); g2.addColorStop(0, '#ffffff'); g2.addColorStop(1, '#9aa3ab'); g.fillStyle = g2; g.beginPath(); g.arc(0, 0, rr, 0, 7); g.fill(); g.fillStyle = '#5c646c'; g.beginPath(); g.arc(0, 0, rr * .2, 0, 7); g.fill(); return }
  // the dark inside of the rim, the spokes in metal over it, the lip
  g.fillStyle = '#262a30'; g.beginPath(); g.arc(0, 0, rr, 0, 7); g.fill();
  g.strokeStyle = gr; g.lineCap = 'round';
  if (n) { g.lineWidth = rr * (n >= 8 ? .13 : .22); for (let i = 0; i < n; i++) { const a = i / n * 6.283 + (s === 3 ? .5 : 0); g.beginPath(); g.moveTo(Math.cos(a) * rr * .2, Math.sin(a) * rr * .2);
      if (s === 3) g.quadraticCurveTo(Math.cos(a + .45) * rr * .6, Math.sin(a + .45) * rr * .6, Math.cos(a + .7) * rr * .92, Math.sin(a + .7) * rr * .92); else g.lineTo(Math.cos(a) * rr * .92, Math.sin(a) * rr * .92); g.stroke() } }
  else if (s === 1) { g.lineWidth = rr * .08; for (let i = 0; i < 10; i++) { const a = i / 10 * 6.283; g.beginPath(); g.moveTo(Math.cos(a) * rr * .2, Math.sin(a) * rr * .2); g.lineTo(Math.cos(a + .55) * rr * .92, Math.sin(a + .55) * rr * .92); g.moveTo(Math.cos(a) * rr * .2, Math.sin(a) * rr * .2); g.lineTo(Math.cos(a - .55) * rr * .92, Math.sin(a - .55) * rr * .92); g.stroke() } }
  g.lineWidth = rr * .1; g.beginPath(); g.arc(0, 0, rr * .95, 0, 7); g.stroke();
  g.fillStyle = gr; g.beginPath(); g.arc(0, 0, rr * .24, 0, 7); g.fill(); g.fillStyle = '#2a2f35'; g.beginPath(); g.arc(0, 0, rr * .1, 0, 7); g.fill();
}

// ---------- the lower body: sill, door lines, arch lips, the lower front (bumper, intake, plate) and the lower rear ----------
function lowerDetails(g, M, Pj, Pu, vis, lb, nearS, clipArches, U, base, faces) {
  const RA = M.RA, RB = M.RB, n = RB.length;
  // the point of a ring at a given x on side s (the side part of the outline)
  const atX = (R, x, s) => { for (let j = 0; j < n - 1; j++) { const a = R[j], b = R[j + 1]; if ((a[0] - x) * (b[0] - x) <= 0 && a[0] !== b[0]) { const t = (x - a[0]) / (b[0] - a[0]); const p = lerp3(a, b, t); return [p[0], s * p[1], p[2]] } } return null };
  if (nearS) {
    const s = nearS, arch = clipArches();
    // the sill: a dark strip along the bottom of the side
    const pts = [], top = []; for (let j = 0; j < n; j++) { const a = RA[j], b = RB[j]; if (Math.abs(M.RN[j][1]) < .55) continue; pts.push([a[0], s * a[1], a[2]]); top.push(lerp3([a[0], s * a[1], a[2]], [b[0], s * b[1], b[2]], .32)) }
    if (pts.length > 2) { g.fillStyle = 'rgba(10,12,15,.30)'; poly(g, pts.map(Pj).concat(top.reverse().map(Pj))); g.fill() }
    // the door shut lines (continuing those of today's picture on the shoulder)
    g.strokeStyle = 'rgba(0,0,0,.34)'; g.lineWidth = Math.max(.55, .5 * U);
    for (const x of M.dl) { const a = atX(RA, x, s), b = atX(RB, x - .3, s); if (!a || !b) continue; const p = Pj(lerp3(a, b, .3)), q = Pj(b); g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke() }
    if (M.ty == 'van') { // the sliding door track and a crease along the cargo side
      const a = atX(RB, M.x0 - 3, s), b = atX(RB, M.X + M.L * .1, s); if (a && b) { g.strokeStyle = 'rgba(0,0,0,.22)'; g.lineWidth = Math.max(.5, .45 * U); const p = Pj(a), q = Pj(b); g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke() } }
    if (arch) g.restore();
    // the lips of the arches
    for (const w of M.wheels) if (w.s === s) {
      const P = []; for (let i = 0; i <= 24; i++) { const a = Math.PI * (1 + i / 24), z = w.r + Math.sin(a) * w.ra; if (z < M.gc) continue; P.push(Pu(w.u + Math.cos(a) * w.ra, w.s * w.hw, z)) }
      // the arc over the wheel (the upper half: angles π..2π have sin < 0 → use the upper half instead)
      const Q = []; for (let i = 0; i <= 24; i++) { const a = Math.PI * i / 24, z = w.r + Math.sin(a) * w.ra; if (z < M.gc) continue; Q.push(Pu(w.u - Math.cos(a) * w.ra, w.s * w.hw, z)) }
      if (Q.length > 1) { g.strokeStyle = 'rgba(0,0,0,.42)'; g.lineWidth = Math.max(.6, .55 * U); g.beginPath(); g.moveTo(Q[0][0], Q[0][1]); for (const q of Q) g.lineTo(q[0], q[1]); g.stroke();
        g.strokeStyle = 'rgba(255,255,255,.10)'; g.lineWidth = Math.max(.4, .3 * U); const Q2 = Q.map((q, i) => { const a = Math.PI * i / 24; return Pu(w.u - Math.cos(a) * (w.ra + .7), w.s * w.hw, w.r + Math.sin(a) * (w.ra + .7)) }); g.beginPath(); g.moveTo(Q2[0][0], Q2[0][1]); for (const q of Q2) g.lineTo(q[0], q[1]); g.stroke() }
    }
  }
  // the lower front and the lower rear: a little drawing on the band between the sill ring and the widest ring
  const frontV = vis([1, 0, 0]) > .02, rearV = vis([-1, 0, 0]) > .02;
  const IDXF = [], IDXR = []; for (let j = n - 18; j < n; j++) IDXF.push(j); for (let j = 0; j < 18; j++) IDXR.push(j);
  const endPt = (front, v, t) => { // on the nose / the tail at |y| = |v|, t from the bottom ring (0) to the widest ring (1)
    const R = front ? IDXF : IDXR, av = Math.abs(v), sg = v < 0 ? -1 : 1;
    const find = Rr => { for (let q = 0; q < R.length - 1; q++) { const a = Rr[R[q]], b = Rr[R[q + 1]]; if ((a[1] - av) * (b[1] - av) <= 0 && a[1] !== b[1]) { const tt = (av - a[1]) / (b[1] - a[1]); return lerp3(a, b, tt) } } const e = Rr[front ? n - 18 : 17]; return e };
    const a = find(RA), b = find(RB), p = lerp3(a, b, t); return [p[0], sg * p[1], p[2]] };
  const quad = (front, v0, v1, t0, t1, fill, stroke) => { const pts = [], k = 6; for (let i = 0; i <= k; i++) pts.push(endPt(front, lerp(v0, v1, i / k), t0)); for (let i = k; i >= 0; i--) pts.push(endPt(front, lerp(v0, v1, i / k), t1));
    const P = pts.map(Pj); poly(g, P); if (fill) { g.fillStyle = fill; g.fill() } if (stroke) { g.strokeStyle = stroke; g.lineWidth = Math.max(.4, .3 * U); g.stroke() } };
  const W = M.W, gr = M.D.gr, ty = M.ty, lt = (() => { const v = parseInt(base.slice(1), 16); return ((v >> 16 & 255) * .3 + (v >> 8 & 255) * .59 + (v & 255) * .11) > 150 })();
  if (frontV) {
    const plate = () => { quad(true, -W * .12, W * .12, .3, .62, '#e9ecef', 'rgba(0,0,0,.5)'); quad(true, -W * .1, W * .1, .4, .52, 'rgba(40,46,54,.35)') };
    if (gr == 'intakes') { for (const sg of [1, -1]) quad(true, sg * W * .19, sg * W * .4, .22, .78, '#101215', 'rgba(255,255,255,.08)'); quad(true, -W * .42, W * .42, 0, .14, '#16191d'); quad(true, -W * .14, W * .14, .3, .7, '#121417'); plate() }
    else if (gr == 'big') { quad(true, -W * .3, W * .3, .32, .78, '#15181b', 'rgba(200,205,210,.35)'); quad(true, -W * .34, W * .34, .02, .2, '#9aa2aa'); for (const sg of [1, -1]) quad(true, sg * W * .34, sg * W * .41, .5, .64, '#eef3f6'); plate() }
    else if (gr == 'bars') { quad(true, -W * .45, W * .45, 0, .42, '#262a30'); quad(true, -W * .44, W * .44, .46, .74, '#c7cdd3', 'rgba(0,0,0,.35)'); quad(true, -W * .26, W * .26, .12, .36, '#15171b'); plate() }
    else if (gr == 'slot') { quad(true, -W * .46, W * .46, 0, .5, '#2a2e33'); quad(true, -W * .3, W * .3, .2, .42, '#16191d'); plate() }
    else { quad(true, -W * .3, W * .3, .2, .62, '#15181c', 'rgba(150,158,166,.35)'); quad(true, -W * .38, W * .38, 0, .12, 'rgba(10,12,14,.45)'); plate() }
  }
  if (rearV) {
    if (ty == 'van') { quad(false, -W * .47, W * .47, 0, .55, '#2a2e33'); quad(false, -W * .42, W * .42, .55, .62, 'rgba(0,0,0,.25)') }
    else if (ty == 'pk') { quad(false, -W * .46, W * .46, .38, .74, '#c7cdd3', 'rgba(0,0,0,.35)'); quad(false, -W * .44, W * .44, 0, .36, '#262a30'); quad(false, -W * .04, W * .04, .12, .3, '#111316') }
    else { quad(false, -W * .38, W * .38, 0, .3, '#1d2126'); for (const sg of [1, -1]) quad(false, sg * W * .33, sg * W * .41, .42, .5, '#8e1c1c');
      if (ty == 'sport') for (const sg of [1, -1]) quad(false, sg * W * .16, sg * W * .27, .08, .26, '#0e1012', 'rgba(200,205,210,.7)') }
  }
}

// ---------- the bed of the pickup: the floor (today's picture, lower) and the inner walls ----------
function drawBed(g, M, Pj, Pu, vis, lb, tex, U) {
  const b = M.bed, zt = M.zcap(b.u1), zf = b.zf, c = [[b.u0, -b.hh], [b.u1, -b.hh], [b.u1, b.hh], [b.u0, b.hh]];
  g.save(); poly(g, c.map(q => Pu(q[0], q[1], M.zcap(q[0])))); g.clip();
  const T = aff([0, 0, zf], [1, 0, zf], [0, 1, zf], Pu(0, 0, zf), Pu(1, 0, zf), Pu(0, 1, zf));
  g.save(); g.setTransform(T[0], T[1], T[2], T[3], T[4], T[5]); g.drawImage(tex.cv, tex.u0, tex.v0, tex.wu, tex.hv); g.restore();
  // the inner walls (their normals point into the bed)
  const walls = [[c[0], c[1], [0, 1, 0]], [c[1], c[2], [-1, 0, 0]], [c[2], c[3], [0, -1, 0]], [c[3], c[0], [1, 0, 0]]];
  for (const [p, q, n] of walls) { if (vis(n) <= .01) continue; const P = [Pu(p[0], p[1], zf), Pu(q[0], q[1], zf), Pu(q[0], q[1], M.zcap(q[0]) + .2), Pu(p[0], p[1], M.zcap(p[0]) + .2)];
    const cc = litC('#3a4048', lb(n)); g.fillStyle = cc; poly(g, P); g.fill();
    g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = Math.max(.4, .3 * U); g.beginPath(); for (let k = 1; k < 4; k++) { const t = k / 4, a = lerp3([p[0], p[1], zf], [q[0], q[1], zf], t), bb = lerp3([p[0], p[1], zf], [q[0], q[1], M.zcap(q[0])], t); const A = Pj(a), B = Pj([bb[0], bb[1], lerp(zf, M.zcap(bb[0]), .9)]); g.moveTo(A[0], A[1]); g.lineTo(B[0], B[1]) } g.stroke() }
  g.restore();
}

// ---------- small solids: prisms over a footprint polygon (local u, v), from z0 to z1 ----------
// p378: the roof light bar of a service car (its place from eqp(): the police — the middle of the cabin, the ambulance / the fire engine —
// the front of the roof) and the amber beacon of the work vehicles; the lenses are dim in the picture, the lamps overlay lights them
function barGeo(M) {
  if (M._bar !== undefined) return M._bar; const k = M.eq, A = M.A, cx = (M.x0 + M.x1) / 2; let b = null;
  if (k == 'police') b = { u: cx, hw: M.W * .35, a: '#ff3b30', b: '#2f6bff', kind: 'em' };
  else if (k == 'amb') b = { u: M.x1 - 5, hw: M.W * .38, a: '#ff3b30', b: '#2f6bff', kind: 'em' };
  else if (k == 'fire') b = { u: M.x1 - 4, hw: M.W * .39, a: '#ff3b30', b: '#ffffff', kind: 'em' };
  else if (k == 'tow' || k == 'maint' || k == 'svc') b = { u: M.boxT ? M.x0 + (M.x1 - M.x0) * .45 : cx, hw: M.W * .26, a: '#ffb000', b: '#ffb000', kind: 'amber' };
  if (b) { b.u = Math.max(M.rf0 + 3, Math.min(M.r1 - 2.6, b.u)); const yr = Math.max(1.5, M.roofY(b.u) - .8); b.hw = Math.min(b.hw, yr); b.z0 = M.zR - A(.05); b.z1 = M.zR + A(.38); b.z2 = M.zR + A(1.2) }
  return (M._bar = b);
}
function buildExtras(M, col, opt) {
  const E = [], D = M.D, X = M.X, H = M.H, W = M.W, A = M.A; opt = opt || {};
  // the mirrors (veh(): outside the body, at the bottom of the windshield)
  for (const d of [-1, 1]) { const x = M.x1 - 1.5, h = M.Gg.hw(x + 1.2) - .4, z0 = M.zBelt - A(.3), z1 = M.zBelt + A(1.1);
    E.push({ base: [[x + 2.8, d * h], [x + 2.2, d * (h + 2.1)], [x + .3, d * (h + 2.3)], [x, d * (h + .2)]], z0, z1, col: sh(col, -.12), top: sh(col, -.04), glassBack: true, c: [x + 1.4, d * (h + 1.2), (z0 + z1) / 2] }) }
  if (M.feat('spoiler')) { const zc = M.zcap(X + 2.8), z1 = zc + A(1.7), z0 = z1 - A(.55), y = W * .36;
    E.push({ base: [[X + 1.4, -y], [X + 4.1, -y], [X + 4.1, y], [X + 1.4, y]], z0, z1, col: sh(col, -.35), top: sh(col, -.28), c: [X + 2.8, 0, z1] });
    for (const sg of [-1, 1]) E.push({ base: [[X + 2.3, sg * W * .2 - .6], [X + 3.3, sg * W * .2 - .6], [X + 3.3, sg * W * .2 + .6], [X + 2.3, sg * W * .2 + .6]], z0: zc - .2, z1: z0, col: '#22262b', top: '#22262b', c: [X + 2.8, sg * W * .2, z0] }) }
  if (M.ex == 'wing') { // p378: the supercar's rear wing (was a picture on the tail)
    const zc = M.zcap(X + 3), z1 = zc + A(2.3), z0 = z1 - A(.5), y = W * .43;
    E.push({ base: [[X + .2, -y], [X + 5.4, -y], [X + 5.4, y], [X + .2, y]], z0, z1, col: '#1d2024', top: sh(col, -.08), c: [X + 2.8, 0, z1] });
    for (const sg of [-1, 1]) E.push({ base: [[X + 2.2, sg * W * .24 - .7], [X + 3.6, sg * W * .24 - .7], [X + 3.6, sg * W * .24 + .7], [X + 2.2, sg * W * .24 + .7]], z0: zc - .2, z1: z0, col: '#1d2024', top: '#1d2024', c: [X + 2.9, sg * W * .24, z0] }) }
  if (M.feat('roofSpoiler')) { const ra = M.rf0, yy = M.roofY(ra + 3) * .95, z1 = M.zR + A(.25), z0 = M.zR - A(.45);
    E.push({ base: [[ra - 2.6, -yy], [ra + 1.2, -yy], [ra + 1.2, yy], [ra - 2.6, yy]], z0, z1, col: '#1d2125', top: '#262a2f', c: [ra - 1, 0, z1] }) }
  if (M.ty == 'truck' && M.m.eq != 'tow') { const x0b = X + M.L * .02, x1b = M.x0 - 3, yy = H - 1.1, z0 = M.zBelt - A(2.5), z1 = A(M.h.box || 30), bc = M.m.fix || '#e9edf1';
    const band = M.ex == 'deliv' ? (M.m.band || '#2f6fd0') : M.eq == 'amb' ? '#d62d2d' : M.eq == 'fire' ? '#f1f3f5' : null;
    const deco = (g, f, at, U) => {
      if (Math.abs(f.n[1]) > .5) { // the sides: a band, the logo panel / the cross / the roll-up doors
        if (band) { g.fillStyle = band; poly(g, [at(.03, .2), at(.97, .2), at(.97, .3), at(.03, .3)]); g.fill() }
        if (M.ex == 'deliv') { g.fillStyle = band; poly(g, [at(.3, .44), at(.7, .44), at(.7, .8), at(.3, .8)]); g.fill(); g.fillStyle = '#fff'; poly(g, [at(.35, .52), at(.65, .52), at(.65, .72), at(.35, .72)]); g.fill() }
        if (M.eq == 'amb') { g.fillStyle = '#d62d2d'; poly(g, [at(.44, .42), at(.56, .42), at(.56, .78), at(.44, .78)]); g.fill(); poly(g, [at(.38, .54), at(.62, .54), at(.62, .66), at(.38, .66)]); g.fill() }
        if (M.eq == 'fire') { g.strokeStyle = 'rgba(0,0,0,.28)'; g.lineWidth = Math.max(.4, .3 * U); for (const s2 of [.08, .33, .58]) { poly(g, [at(s2, .36), at(s2 + .22, .36), at(s2 + .22, .92), at(s2, .92)]); g.stroke() } }
        g.strokeStyle = 'rgba(0,0,0,.12)'; g.lineWidth = Math.max(.35, .25 * U); g.beginPath(); for (let s2 = .1; s2 < .95; s2 += .1) { const a = at(s2, .03), b = at(s2, .97); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke() }
      else if (f.n[0] < -.5) { // the rear: the two doors, the handles
        g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = Math.max(.45, .35 * U); const a = at(.5, .04), b = at(.5, .97); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
        g.fillStyle = 'rgba(40,44,50,.55)'; for (const s2 of [.44, .56]) { poly(g, [at(s2 - .015, .35), at(s2 + .015, .35), at(s2 + .015, .6), at(s2 - .015, .6)]); g.fill() } } };
    E.push({ base: [[x0b, -yy], [x1b, -yy], [x1b, yy], [x0b, yy]], z0, z1, col: bc, topTex: true, deco, c: [(x0b + x1b) / 2, 0, (z0 + z1) / 2] }) }
  if (M.eq == 'tow') { // p378: a real flatbed — a steel deck with rails, the headboard behind the cab, the wheel-lift under the tail
    const u0 = X + M.L * .03, u1 = M.x0 - 4, yy = H - 1.2, z1 = M.zBelt + A(.6), z0 = M.zBelt - A(.9), rc = '#5d656e';
    E.push({ base: [[u0, -yy], [u1, -yy], [u1, yy], [u0, yy]], z0, z1, col: '#6b737b', topTex: true, c: [(u0 + u1) / 2, 0, z1], deco: (g, f, at, U) => { if (Math.abs(f.n[1]) > .5) { g.fillStyle = '#e0a81e'; poly(g, [at(0, .25), at(1, .25), at(1, .7), at(0, .7)]); g.fill() } } });
    for (const sg of [-1, 1]) E.push({ base: [[u0 + 1, sg * yy - .55], [u1 - .5, sg * yy - .55], [u1 - .5, sg * yy + .55], [u0 + 1, sg * yy + .55]], z0: z1, z1: z1 + A(.9), col: rc, top: '#8a929a', c: [(u0 + u1) / 2, sg * yy, z1 + A(.5)] });
    E.push({ base: [[u1 - .2, -yy + .3], [u1 + 1.3, -yy + .3], [u1 + 1.3, yy - .3], [u1 - .2, yy - .3]], z0: z1, z1: z1 + A(5.2), col: '#3a4048', top: '#4a525b', c: [u1 + .5, 0, z1 + A(2.6)],
      deco: (g, f, at, U) => { if (f.n[0] < -.5) { g.strokeStyle = 'rgba(200,206,212,.45)'; g.lineWidth = Math.max(.35, .25 * U); g.beginPath(); for (let t = .2; t < 1; t += .2) { const a = at(.06, t), b = at(.94, t); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } for (let s2 = .15; s2 < 1; s2 += .14) { const a = at(s2, .05), b = at(s2, .95); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke() } } });
    E.push({ base: [[X - 4.6, -1.3], [X + 1.5, -1.3], [X + 1.5, 1.3], [X - 4.6, 1.3]], z0: A(1.5), z1: A(2.5), col: '#2b3036', top: '#3a4048', c: [X - 1.5, 0, A(2)] });
    E.push({ base: [[X - 5.8, -W * .37], [X - 4.2, -W * .37], [X - 4.2, W * .37], [X - 5.8, W * .37]], z0: A(1.3), z1: A(2.4), col: '#e0a81e', top: '#f0bf3a', c: [X - 5, 0, A(1.9)] });
  }
  if (M.eq == 'maint' && M.bed) { // p378: the maintenance body — two tool compartments over the bed, the chevron board on the tail
    const b = M.bed, zt = M.zcap(b.u1) + A(3.0), cc = '#e9edf1';
    for (const sg of [-1, 1]) { const va = sg * (b.hh - 3.6), vb = sg * (b.hh + .4);
      E.push({ base: [[b.u0 + .6, Math.min(va, vb)], [b.u1 - .4, Math.min(va, vb)], [b.u1 - .4, Math.max(va, vb)], [b.u0 + .6, Math.max(va, vb)]], z0: b.zf, z1: zt, col: cc, top: '#cfd5db', c: [(b.u0 + b.u1) / 2, sg * (b.hh - 1.6), zt],
        deco: (g, f, at, U) => { if (Math.abs(f.n[1]) > .5) { g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.4, .3 * U); g.beginPath(); for (const s2 of [.34, .67]) { const a = at(s2, .08), q = at(s2, .95); g.moveTo(a[0], a[1]); g.lineTo(q[0], q[1]) } g.stroke(); g.fillStyle = '#7d858e'; for (const s2 of [.17, .5, .83]) { poly(g, [at(s2 - .03, .62), at(s2 + .03, .62), at(s2 + .03, .7), at(s2 - .03, .7)]); g.fill() } g.fillStyle = '#f08a1c'; poly(g, [at(0, .1), at(1, .1), at(1, .18), at(0, .18)]); g.fill() } } }) }
    E.push({ base: [[X + .1, -W * .44], [X + 1.3, -W * .44], [X + 1.3, W * .44], [X + .1, W * .44]], z0: M.zTail - A(1.2), z1: M.zTail + A(3.4), col: '#f0c53a', top: '#f3cf55', c: [X + .7, 0, M.zTail + A(1)],
      deco: (g, f, at, U) => { if (f.n[0] < -.5) { g.save(); poly(g, [at(0, 0), at(1, 0), at(1, 1), at(0, 1)]); g.clip(); g.fillStyle = '#1b1d20'; for (let s2 = -.6; s2 < 1; s2 += .2) { poly(g, [at(s2, 0), at(s2 + .1, 0), at(s2 + .4, 1), at(s2 + .3, 1)]); g.fill() } g.restore() } } });
  }
  if (M.feat('toolbox')) { const z0 = M.zBelt - A(.2), z1 = M.zBelt + A(.85), Y = -H;
    E.push({ base: [[M.x0 - 7, Y + 3], [M.x0 - 2.8, Y + 3], [M.x0 - 2.8, H - 3], [M.x0 - 7, H - 3]], z0, z1, col: '#b9c0c7', topTex: true, c: [M.x0 - 4.9, 0, z1] }) }
  // the taxi's roof sign (eqp(): on the middle of the roof) — a little box; it glows at night (the lamp 'S')
  if (M.eq == 'taxi') { const cx = (M.x0 + M.x1) / 2, yy = Math.min(4.5, Math.max(2, M.roofY(cx) - 1)); E.push({ base: [[cx - 5.5, -yy], [cx + 5.5, -yy], [cx + 5.5, yy], [cx - 5.5, yy]], z0: M.zR - A(.05), z1: M.zR + A(1.6), col: '#f3f0e0', top: '#f7f3dc', c: [cx, 0, M.zR + A(.8)], roofX: true,
    deco: (g, f, at) => { if (Math.abs(f.n[0]) > .5) { g.fillStyle = '#14171a'; poly(g, [at(.12, .3), at(.88, .3), at(.88, .7), at(.12, .7)]); g.fill(); g.fillStyle = '#f3c623'; poly(g, [at(.2, .4), at(.8, .4), at(.8, .6), at(.2, .6)]); g.fill() } } }) }
  // the light bar / the beacon (dim lenses; the lamps overlay makes them flash)
  const br = barGeo(M); if (br) {
    E.push({ base: [[br.u - 2.3, -br.hw], [br.u + 2.3, -br.hw], [br.u + 2.3, br.hw], [br.u - 2.3, br.hw]], z0: br.z0, z1: br.z1, col: '#1b1d20', top: '#26292d', c: [br.u, 0, br.z1], roofX: true });
    for (const sg of [-1, 1]) { const lc = sg < 0 ? br.a : br.b, v0 = sg < 0 ? -br.hw + .4 : .5, v1 = sg < 0 ? -.5 : br.hw - .4;
      E.push({ base: [[br.u - 1.7, v0], [br.u + 1.7, v0], [br.u + 1.7, v1], [br.u - 1.7, v1]], z0: br.z1, z1: br.z2, col: sh(lc, br.kind == 'amber' ? -.25 : -.42), top: sh(lc, br.kind == 'amber' ? -.1 : -.3), c: [br.u, sg * br.hw / 2, br.z2], roofX: true, noEdge: true }) } }
  // the roof rack of the garage (state v = 1): two silver rails on feet and two bars across
  if (opt.v == 1 && !M.open) { const ra = M.rf0, rb = M.r1, a = ra + (rb - ra) * .1, b2 = rb - (rb - ra) * .1, yy = Math.max(2, Math.min(M.roofY(a + 1), M.roofY(b2 - 1)) - 1.1), zr = M.zR;
    for (const sg of [-1, 1]) E.push({ base: [[a, sg * yy - .7], [b2, sg * yy - .7], [b2, sg * yy + .7], [a, sg * yy + .7]], z0: zr - A(.05), z1: zr + A(.75), col: '#aab2ba', top: '#d6dbe0', c: [(a + b2) / 2, sg * yy, zr + A(.4)], roofX: true });
    for (const f of [.3, .68]) { const xx = a + (b2 - a) * f; E.push({ base: [[xx, -yy - .6], [xx + 1.4, -yy - .6], [xx + 1.4, yy + .6], [xx, yy + .6]], z0: zr + A(.6), z1: zr + A(1.15), col: '#5b636b', top: '#8a929a', c: [xx + .7, 0, zr + A(.9)], roofX: true }) } }
  return E;
}
function drawPrism(g, e, Pj, vis, lb, tex, U) {
  const b = e.base, n = b.length, F = [];
  // the sides
  let ar = 0; for (let i = 0; i < n; i++) { const p = b[i], q = b[(i + 1) % n]; ar += p[0] * q[1] - q[0] * p[1] }
  // p378: a frustum when the top outline differs (topBase: the same vertices, set in — a sloped windshield, a rounded roof edge)
  const tb = e.topBase || b;
  for (let i = 0; i < n; i++) { const p = b[i], q = b[(i + 1) % n], pt = tb[i], qt = tb[(i + 1) % n]; let nn = [q[1] - p[1], -(q[0] - p[0]), 0]; if (ar < 0) nn = [-nn[0], -nn[1], 0];
    const P = [[p[0], p[1], e.z0], [q[0], q[1], e.z0], [qt[0], qt[1], e.z1], [pt[0], pt[1], e.z1]];
    if (tb !== b) { let m = norm3(cross3(sub3(P[1], P[0]), sub3(P[3], P[0]))); if (m[0] * nn[0] + m[1] * nn[1] < 0) m = [-m[0], -m[1], -m[2]]; nn = m } else nn = norm3(nn);
    if (vis(nn) <= .01) continue; F.push({ P, n: nn, i }) }
  for (const f of F) { const c = litC(e.col, lb(f.n)); g.fillStyle = c; g.strokeStyle = e.edge || 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.35, .22 * U); poly(g, f.P.map(Pj)); g.fill(); if (!e.noEdge) g.stroke();
    if (e.deco) { const P = f.P, at = (s2, t2) => Pj(lerp3(lerp3(P[0], P[1], s2), lerp3(P[3], P[2], s2), t2)); try { e.deco(g, f, at, U) } catch (err) { } }
    if (e.glassBack && f.n[0] < -.5) { const P = f.P, q = [lerp3(P[0], P[3], .2), lerp3(P[1], P[2], .2), lerp3(P[1], P[2], .85), lerp3(P[0], P[3], .85)].map(Pj); g.fillStyle = 'rgba(150,185,210,.85)'; poly(g, q); g.fill() } }
  const T = tb.map(p => [p[0], p[1], e.z1]);
  if (e.topTex && tex) { const A = aff(T[0], T[1], T[2], Pj(T[0]), Pj(T[1]), Pj(T[2])); if (!A) return; g.save(); poly(g, T.map(Pj)); g.clip(); g.setTransform(A[0], A[1], A[2], A[3], A[4], A[5]); g.drawImage(tex.cv, tex.u0, tex.v0, tex.wu, tex.hv); g.restore() }
  else if (e.topDraw) { const A = aff(T[0], T[1], T[2], Pj(T[0]), Pj(T[1]), Pj(T[2])); if (!A) return; g.save(); poly(g, T.map(Pj)); g.clip(); g.setTransform(A[0], A[1], A[2], A[3], A[4], A[5]); try { e.topDraw(g, U) } catch (err) { } g.restore() }
  else { g.fillStyle = e.top; poly(g, T.map(Pj)); g.fill() }
  g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = Math.max(.35, .25 * U); poly(g, T.map(Pj)); g.stroke();
}

// ---------- the glass house: the windshield and the rear window from today's picture (when they are gentle), the side glass, the pillars ----------
function drawGlassHouse(g, M, Pj, vis, lb, tex, U, col, nearS) {
  const FR = M.FR, n = FR.length, gTop = M.h.glassTop || 1, roofBlack = M.feat('roofBlack');
  const pillar = roofBlack ? '#22262b' : col;
  const faces = [];
  for (let i = 0; i < n; i++) {
    const a = FR[i], b = FR[(i + 1) % n]; let sec = a.sec === b.sec ? a.sec : (a.sec === 'side' ? b.sec : a.sec);
    if (i === n - 1) sec = 'rear';
    const p = [a.b, b.b, b.r, a.r]; let nn = norm3(cross3(sub3(p[1], p[0]), sub3(p[3], p[0])));
    const cx = (a.b[0] + b.b[0]) / 2 - M.xc, cy = (a.b[1] + b.b[1]) / 2; if (nn[0] * cx + nn[1] * cy < 0) nn = [-nn[0], -nn[1], -nn[2]];
    const vv = vis(nn); if (vv <= .004) continue; if (M.open && sec !== 'front') continue;
    faces.push({ i, p, n: nn, sec, s: a.s });
  }
  // the gradient of the glass on the screen (one for all the faces, so that they join without a seam)
  let y0 = 1e9, y1 = -1e9; for (const f of faces) for (const q of f.p) { const y = Pj(q)[1]; if (y < y0) y0 = y; if (y > y1) y1 = y }
  const glassG = g.createLinearGradient(0, y0, 0, y1); glassG.addColorStop(0, '#5d7486'); glassG.addColorStop(.45, '#33434f'); glassG.addColorStop(1, '#1a2129');
  const isGlass = (f) => { if (f.sec === 'side') return !(M.boxT && (f.p[0][0] + f.p[1][0]) / 2 < M.x0 + 1.2); if (f.sec === 'front') return true; return !M.boxT };
  const texF = f => (f.sec === 'front' && M.wsTex) || (f.sec === 'rear' && M.rwTex);
  const GP = [], PP = new Map(), addP = (c, q) => { let a = PP.get(c); if (!a) PP.set(c, a = []); a.push(q) };
  for (const f of faces) {
    const P = f.p, glass = isGlass(f);
    if (glass && gTop < 1) { // the van: glass up to gTop, painted above
      const m0 = lerp3(P[0], P[3], gTop), m1 = lerp3(P[1], P[2], gTop);
      GP.push([P[0], P[1], m1, m0]); addP(litC(litBase(col), Math.round(lb(f.n) * 100) / 100), [m0, m1, P[2], P[3]]); continue }
    if (texF(f)) { texTri(g, tex, Pj, P[0], P[1], P[2]); texTri(g, tex, Pj, P[0], P[2], P[3]); continue }
    if (glass) GP.push(P); else addP(litC(litBase(col), Math.round(lb(f.n) * 100) / 100), P);
  }
  const fillAll = (list, st) => { if (!list.length) return; g.fillStyle = st; g.beginPath(); for (const q of list) { const P = q.map(Pj); g.moveTo(P[0][0], P[0][1]); for (let i = 1; i < P.length; i++) g.lineTo(P[i][0], P[i][1]); g.closePath() } g.fill() };
  fillAll(GP, glassG); for (const [c, a] of PP) fillAll(a, c);
  const vf = new Set(faces.map(f => f.i)), visI = i => vf.has(((i % n) + n) % n);
  // the reflection on the side glass, the head rests behind it
  for (const s of [1, -1]) {
    const I = s === 1 ? M.iSideP : M.iSideN, list = faces.filter(f => f.sec === 'side' && f.s === s && isGlass(f)); if (!list.length) continue;
    g.save(); g.beginPath(); for (const f of list) { const P = (gTop < 1 ? [f.p[0], f.p[1], lerp3(f.p[1], f.p[2], gTop), lerp3(f.p[0], f.p[3], gTop)] : f.p).map(Pj); g.moveTo(P[0][0], P[0][1]); for (const q of P) g.lineTo(q[0], q[1]); g.closePath() } g.clip();
    // head rests (the front seat, the rear seat) seen through the glass
    const hr = (x) => { const yy = s * (M.roofY(x) * .55), z0 = M.zBelt + (M.zR - M.zBelt) * .15, z1 = M.zBelt + (M.zR - M.zBelt) * .62; const P = [[x - 2.4, yy, z0], [x + .2, yy, z0], [x + .6, yy, z1], [x - 1.6, yy, z1]].map(Pj); g.fillStyle = 'rgba(8,10,13,.45)'; poly(g, P); g.fill() };
    if (!M.boxT) { hr(M.r1 - (M.r1 - M.r0) * .18); if (M.D.doors > 2 && M.ty != 'sport') hr(M.r0 + (M.r1 - M.r0) * .22) } else hr(M.x0 + (M.x1 - M.x0) * .45);
    const a = Pj([M.xcr, 0, M.zR]), b = Pj([M.xcf, 0, M.zBelt]); g.strokeStyle = 'rgba(255,255,255,.13)'; g.lineWidth = Math.max(1, 2.2 * U);
    const L0 = Pj([M.xc - (M.xcf - M.xcr) * .1, s * M.roofY(M.xc), M.zR]), L1 = Pj([M.xc + (M.xcf - M.xcr) * .25, s * M.yg(M.xc) * 1.02, M.zBelt]);
    g.beginPath(); g.moveTo(L0[0], L0[1]); g.lineTo(L1[0], L1[1]); g.stroke(); g.restore();
  }
  // the procedural windshield / rear window (steep ones): a reflection, the wiper, the third brake lamp
  for (const sec of ['front', 'rear']) {
    const list = faces.filter(f => f.sec === sec && isGlass(f) && !texF(f)); if (!list.length) continue;
    g.save(); g.beginPath(); for (const f of list) { const P = (gTop < 1 ? [f.p[0], f.p[1], lerp3(f.p[1], f.p[2], gTop), lerp3(f.p[0], f.p[3], gTop)] : f.p).map(Pj); g.moveTo(P[0][0], P[0][1]); for (const q of P) g.lineTo(q[0], q[1]); g.closePath() } g.clip();
    const fx = sec === 'front' ? M.uCowl : M.bx0 - M.bR, rx = sec === 'front' ? M.r1 : M.rf0, zt = M.zBelt + (M.zR - M.zBelt) * gTop;
    const p0 = Pj([lerp(fx, rx, .1), -M.cw * .45, lerp(M.zBelt, zt, .1)]), p1 = Pj([lerp(fx, rx, .8), M.cw * .1, lerp(M.zBelt, zt, .8)]);
    g.strokeStyle = 'rgba(255,255,255,.12)'; g.lineWidth = Math.max(1, 3 * U); g.beginPath(); g.moveTo(p0[0], p0[1]); g.lineTo(p1[0], p1[1]); g.stroke();
    if (sec === 'front') { const d0 = Pj([fx - .3, -M.cw * .5, M.zBelt]), d1 = Pj([fx - .3, M.cw * .5, M.zBelt]), e0 = Pj([lerp(fx, rx, .2), -M.cw * .5, lerp(M.zBelt, zt, .2)]);
      g.strokeStyle = 'rgba(10,12,14,.75)'; g.lineWidth = Math.max(1, Math.abs(e0[1] - d0[1]) * .6); g.beginPath(); g.moveTo(d0[0], d0[1]); g.lineTo(d1[0], d1[1]); g.stroke() }
    else if (!M.boxT) { const w0 = Pj([fx, 0, M.zBelt + .3]), w1 = Pj([lerp(fx, rx, .55), -M.cw * .3, lerp(M.zBelt, M.zR, .55)]); g.strokeStyle = 'rgba(10,12,14,.7)'; g.lineWidth = Math.max(.6, .5 * U); g.beginPath(); g.moveTo(w0[0], w0[1]); g.lineTo(w1[0], w1[1]); g.stroke() }
    g.restore();
    if (sec === 'rear' && !M.boxT && M.ty != 'pk') { const q = [[rx + .3, -2.4, M.zR - M.A(.15)], [rx + .3, 2.4, M.zR - M.A(.15)], [rx + .9, 2.4, M.zR - M.A(.45)], [rx + .9, -2.4, M.zR - M.A(.45)]]; if (vis([-1, 0, .3]) > 0) { g.fillStyle = '#d0282a'; poly(g, q.map(Pj)); g.fill() } }
  }
  // the van's rear doors: the split, two small windows
  if (M.ty == 'van') {
    const list = faces.filter(f => f.sec === 'rear'); if (list.length) {
      const zr = M.zR, zb = M.zBelt, xa = M.bx0, xr = M.rf0, at = (v, t) => [lerp(M.X + M.dT, xr, t), v, lerp(zb, zr, t)];
      g.strokeStyle = 'rgba(0,0,0,.4)'; g.lineWidth = Math.max(.6, .45 * U); const a = Pj(at(0, 0)), b = Pj(at(0, .97)); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
      for (const sg of [1, -1]) { const P = [at(sg * 1.2, .55), at(sg * M.W * .36, .55), at(sg * M.W * .36, .86), at(sg * 1.2, .86)].map(Pj); g.fillStyle = glassG; poly(g, P); g.fill(); g.strokeStyle = 'rgba(0,0,0,.45)'; g.stroke() }
    }
  }
  // the pillars: A (windshield | side), C (side | rear), B (the middle of the side glass), the belt trim along the bottom of the glass
  const edge = (i) => [FR[i].b, FR[i].r];
  const strokeEdge = (i, w, c) => { const [p, q] = edge(i), a = Pj(p), b = Pj(q); g.strokeStyle = c; g.lineWidth = Math.max(.8, w * U); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke() };
  const pc = (s, sec) => litC(sh(pillar, -.06), lb([sec === 'front' ? .5 : -.5, s * .8, .3]));
  for (const s of [1, -1]) {
    const iA = s === 1 ? M.iSideP[1] : M.iSideN[0], iC = s === 1 ? M.iSideP[0] : M.iSideN[1] % n;
    const sideVis = vis([0, s, .3]) > .0;
    if (sideVis || visI(iA) || visI(iA - 1)) if (!M.boxT) strokeEdge(iA, 1.35, pc(s, 'front'));
    if (sideVis || visI(iC) || visI(iC - 1)) if (!M.boxT && !M.open) strokeEdge(iC, M.ty == 'sedan' || M.ty == 'sport' ? 2.2 : 1.6, pc(s, 'rear'));
    if (!sideVis) continue;
    const sideAt = (x, t) => { const T = (x - M.bx0) / (M.bx1 - M.bx0), xr = lerp(M.xcr, M.xcf, T); return lerp3([x, s * M.baseSideYF(x), M.zcap(x)], [xr, s * M.roofY(xr), M.zR], t) };
    if (!M.boxT && M.D.doors > 2 && M.ty != 'sport') { const xb = M.xm; const P = [sideAt(xb - .9, 0), sideAt(xb + .9, 0), sideAt(xb + .7, 1), sideAt(xb - .7, 1)].map(Pj); g.fillStyle = pc(s, 'side'); g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = .5; poly(g, P); g.fill(); g.stroke() }
    if (M.boxT) { const xb = M.x0 + .8; const P = [sideAt(xb, 0), sideAt(xb + 1.2, 0), sideAt(xb + 1.2, gTop), sideAt(xb, gTop)].map(Pj); g.fillStyle = litC(litBase(col), lb([0, s, 0])); poly(g, P); g.fill();
      g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.5, .4 * U); for (const xd of M.dl) if (xd < M.x0) { const p0 = Pj(sideAt(xd, 0)), p1 = Pj(sideAt(xd, .9)); g.beginPath(); g.moveTo(p0[0], p0[1]); g.lineTo(p1[0], p1[1]); g.stroke() }
      // the van's A pillar
      const iA2 = s === 1 ? M.iSideP[1] : M.iSideN[0], a = Pj(FR[iA2].b), b = Pj(lerp3(FR[iA2].b, FR[iA2].r, gTop)); g.strokeStyle = pc(s, 'front'); g.lineWidth = Math.max(.8, 1.4 * U); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
      // the line of the top of the windows
      g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.5, .4 * U); const c0 = Pj(sideAt(M.x0 + .8, gTop)), c1 = Pj(lerp3(FR[iA2].b, FR[iA2].r, gTop)); g.beginPath(); g.moveTo(c0[0], c0[1]); g.lineTo(c1[0], c1[1]); g.stroke() }
    // the belt trim
    const I = s === 1 ? M.iSideP : M.iSideN; g.strokeStyle = 'rgba(16,19,23,.75)'; g.lineWidth = Math.max(.6, .55 * U); g.beginPath();
    let first = true; for (let i = Math.min(I[0], I[1]); i <= Math.max(I[0], I[1]); i++) { const p = FR[i % n].b; if (M.boxT && p[0] < M.x0 + .8) continue; const q = Pj(p); if (first) { g.moveTo(q[0], q[1]); first = false } else g.lineTo(q[0], q[1]) } g.stroke();
  }
}

// ---------- the heavy vehicles kit (p378) ----------
// The buses, the tractor and its trailer (two pictures, each with its own heading), the container chassis with its boxes, the tanker and
// the forklift: the game paints them top-down from boxes (lv(): the body, the windows, the hatches, the wheels at fixed fractions), so in
// 3/4 they are built from boxes too — the same proportions and the same colours, with the faces the top view never showed (the window
// bands, the doors, the faces, the tails) drawn on the box faces.  World px (10 px = 1 m), the footprint of the game (length, width) given.
const KITS = new Map();
const FLIP = f => f.n[1] > .5 || f.n[0] < -.5;
const kq = (g, at, s0, s1, t0, t1, fill, stroke, lw) => { poly(g, [at(s0, t0), at(s1, t0), at(s1, t1), at(s0, t1)]); if (fill) { g.fillStyle = fill; g.fill() } if (stroke) { g.strokeStyle = stroke; g.lineWidth = lw || .5; g.stroke() } };
const box = (u0, u1, v0, v1, z0, z1, o) => { const e = Object.assign({ base: [[u0, v0], [u1, v0], [u1, v1], [u0, v1]], z0, z1, c: [(u0 + u1) / 2, (v0 + v1) / 2, (z0 + z1) / 2] }, o || {});
  if (e.ins) { const I = e.ins; e.topBase = [[u0 + (I.r || 0), v0 + (I.s || 0)], [u1 - (I.f || 0), v0 + (I.s || 0)], [u1 - (I.f || 0), v1 - (I.s || 0)], [u0 + (I.r || 0), v1 - (I.s || 0)]] } return e };   // ins: the top set in (front, rear, sides)
const glassGr = (g, at, t0, t1) => { const a = at(.5, t1), b = at(.5, t0), gr = g.createLinearGradient(a[0], a[1], b[0], b[1]); gr.addColorStop(0, '#5d7486'); gr.addColorStop(.5, '#33434f'); gr.addColorStop(1, '#1a2129'); return gr };
function kitLamp(t, u, v, z, n, s, o) { return Object.assign({ t, u, v, z, n, s }, o || {}) }
// kind: bus | coach | shuttle | tractor | trailer | chassis | tanker | fork
C34.kit = function (kind, L, W, o) {
  const id = 'K/' + kind + '/' + (+L).toFixed(1) + 'x' + (+W).toFixed(1) + (o && o.tag ? '/' + o.tag : ''); if (KITS.has(id)) return id;
  const k = KIT_DEF[kind]; if (!k) throw new Error('C34.kit: unknown kind ' + kind);
  const d = k(+L, +W, o || {}); d.kind = kind; d.lampDef = { list: d.lamps || [], sc: 1, nose: d.nose != null ? d.nose : L / 2, hw: d.hw != null ? d.hw : W / 2 }; KITS.set(id, d); return id;
};
C34.kitInfo = id => KITS.get(id) || null;
const KIT_DEF = {
  bus(L, W, o) { return busKit(L, W, o, 'bus') }, coach(L, W, o) { return busKit(L, W, o, 'coach') }, shuttle(L, W, o) { return busKit(L, W, o, 'shuttle') },
  tractor(L, W, o) { return tractorKit(L, W, o) }, trailer(L, W, o) { return trailerKit(L, W, o, false) }, chassis(L, W, o) { return trailerKit(L, W, o, true) },
  tanker(L, W, o) { return tankerKit(L, W, o) }, fork(L, W, o) { return forkKit(L, W, o) },
  cstack(L, W, o) { return cstackKit(L, W, o) }, reach(L, W, o) { return reachKit(L, W, o) }   // p386 (S7F139): the containers on the ground, the reach stacker
};
// the bus: one tall box — the window band, the doors on the right (the curb side), the face (the windshield, the destination sign), the
// engine tail; the roof of lv() (two hatches, the air conditioner)
function busKit(L, W0, o, ty) {
  // the game's own footprint (length, width — the bus is drawn at ~6.7 px/m), the height in the same metres (3.2 m city, 3.6 coach, 3.0 shuttle)
  const W = W0, Hb = W * (ty == 'coach' ? 1.41 : ty == 'shuttle' ? 1.07 : 1.25), gc = Math.max(1.4, W * .09), X = -L / 2, hw = W / 2, axR = X + L * .17, axF = X + L * .8, wr = Math.max(3, W * .2);
  const Hs = Hb - Hb * .09, lean = Math.max(1, L * .018), winT0 = ty == 'coach' ? .5 : ty == 'shuttle' ? .36 : .42, winT1 = .93, coach = ty == 'coach';
  const build = (col, opt) => {
    const band = col === '#f4f6f8' ? '#2f6fd0' : '#f4f6f8', B = [], roofC = coach ? '#eef1f3' : sh(col, .2), skirt = sh(col, -.32);
    // the body: the sides lean in a little, the face leans back (the windshield)
    B.push(box(X + .4, -X, -hw, hw, gc, Hs, { col, ins: { f: lean, r: .3, s: .25 }, topDraw: (g) => { g.fillStyle = roofC; g.fillRect(X, -hw, L, W) },
      deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.4, .3 * U);
        if (Math.abs(f.n[1]) > .5) { // the sides: the skirt, the livery under the windows, the glass band and its pillars, the doors (the curb side), the arches
          const right = f.n[1] > 0, gs = glassGr(g, at, winT0, winT1);
          kq(g, at, 0, 1, 0, .08, skirt); kq(g, at, 0, 1, winT0 - .1, winT0 - .045, band); kq(g, at, 0, 1, winT0 - .03, winT0 - .015, 'rgba(255,255,255,.25)');
          kq(g, at, .02, .98, winT0, winT1, gs); kq(g, at, .02, .98, winT1 - .012, winT1 + .01, '#14181d');
          const nw = coach ? 10 : 8; for (let i = 1; i < nw; i++) { const s2 = .02 + .96 * i / nw; kq(g, at, s2 - .005, s2 + .005, winT0, winT1, '#1a1f25') }
          g.fillStyle = 'rgba(255,255,255,.16)'; poly(g, [at(.1, winT1 - .04), at(.45, winT1 - .04), at(.38, winT0 + .05), at(.03, winT0 + .05)]); g.fill(); poly(g, [at(.55, winT1 - .04), at(.66, winT1 - .04), at(.6, winT0 + .05), at(.49, winT0 + .05)]); g.fill();
          if (right) { const doors = coach ? [[.86, .94]] : ty == 'shuttle' ? [[.76, .9], [.4, .54]] : [[.85, .95], [.46, .56]];
            for (const [a, b] of doors) { kq(g, at, a - .006, b + .006, .02, winT1 + .01, '#1b2128'); kq(g, at, a, (a + b) / 2 - .003, .06, winT1 - .02, gs); kq(g, at, (a + b) / 2 + .003, b, .06, winT1 - .02, gs); kq(g, at, a, b, .45, .47, 'rgba(255,255,255,.35)') } }
          else if (coach) { g.strokeStyle = 'rgba(0,0,0,.32)'; g.lineWidth = lw; for (const s2 of [.28, .46, .64]) { poly(g, [at(s2, .1), at(s2 + .15, .1), at(s2 + .15, winT0 - .14), at(s2, winT0 - .14)]); g.stroke() } }
          for (const ax of [axR, axF]) { const s2 = (ax - X) / L, ra = (wr + 1.3) / L, P = [at(s2 - ra, 0)]; for (let i = 0; i <= 16; i++) { const a = Math.PI * i / 16; P.push(at(s2 - Math.cos(a) * ra, Math.min(1, (wr + Math.sin(a) * (wr + 1.3) - gc) / (Hs - gc)))) } P.push(at(s2 + ra, 0)); g.fillStyle = '#121519'; poly(g, P); g.fill() } }
        else if (f.n[0] > .3) { // the face: two panes of the windshield, the destination sign, the lamps, the bumper
          const gs = glassGr(g, at, .34, .86); kq(g, at, .05, .495, .34, .86, gs); kq(g, at, .505, .95, .34, .86, gs); kq(g, at, .03, .97, .32, .34, '#1a1f25');
          g.fillStyle = 'rgba(255,255,255,.14)'; poly(g, [at(.1, .8), at(.3, .8), at(.2, .4), at(.08, .4)]); g.fill();
          g.strokeStyle = 'rgba(10,12,14,.8)'; g.lineWidth = lw; g.beginPath(); for (const s2 of [.28, .72]) { const a = at(s2, .36), b2 = at(s2 + .12, .52); g.moveTo(a[0], a[1]); g.lineTo(b2[0], b2[1]) } g.stroke();
          kq(g, at, .06, .94, .875, .97, '#15191d'); kq(g, at, .18, .82, .9, .945, '#ffb000');
          kq(g, at, 0, 1, 0, .11, '#2b3036'); for (const s2 of [.04, .8]) { kq(g, at, s2, s2 + .16, .14, .23, '#eef3f6', 'rgba(0,0,0,.4)', lw); kq(g, at, s2 + (s2 < .5 ? .17 : -.05), s2 + (s2 < .5 ? .21 : -.01), .14, .23, '#f5a524') }
          kq(g, at, .4, .6, .03, .08, '#e9ecef') }
        else if (f.n[0] < -.3) { // the tail: the rear window, the engine grille, the lamps, the plate
          kq(g, at, .14, .86, .62, .9, glassGr(g, at, .62, .9)); kq(g, at, .15, .85, .16, .44, '#262a30'); g.strokeStyle = 'rgba(160,168,176,.35)'; g.lineWidth = lw; g.beginPath(); for (let t = .2; t < .44; t += .045) { const a = at(.17, t), b2 = at(.83, t); g.moveTo(a[0], a[1]); g.lineTo(b2[0], b2[1]) } g.stroke();
          for (const s2 of [.02, .9]) { kq(g, at, s2, s2 + .08, .14, .5, '#8e1c1c'); kq(g, at, s2, s2 + .08, .5, .56, '#f39a2b') } kq(g, at, 0, 1, 0, .08, '#2b3036'); kq(g, at, .4, .6, .1, .14, '#e9ecef') } } }));
    // the roof: a rounded edge (a band set in), the hatches, the air conditioner
    B.push(box(X + .9, -X - lean - .2, -hw + .25, hw - .25, Hs, Hb - 1.1, { col: roofC, ins: { f: 1.4, r: 1, s: 1.1 }, noEdge: true, topDraw: (g) => { g.fillStyle = roofC; g.fillRect(X, -hw, L, W); g.fillStyle = 'rgba(0,0,0,.07)'; for (let x = X + L * .08; x < -X - 3; x += L * .1) g.fillRect(x, -hw + 1.5, .5, W - 3);
        for (const f of [.12, .72]) { g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(X + L * f - .3, -W * .17 - .3, L * .075 + .6, W * .34 + .6); g.fillStyle = sh(roofC, -.08); g.fillRect(X + L * f, -W * .17, L * .075, W * .34) } } }));
    B.push(box(X + L * .4, X + L * .62, -W * .27, W * .27, Hb - 1.3, Hb + .9, { col: '#6b737b', ins: { f: .6, r: .6, s: .6 }, topDraw: (g) => { g.fillStyle = '#8a929a'; g.fillRect(X + L * .4, -W * .3, L * .22, W * .6); g.fillStyle = 'rgba(30,34,38,.55)'; for (let x = X + L * .42; x < X + L * .6; x += 1.6) g.fillRect(x, -W * .2, .6, W * .4) } }));
    // the mirrors on their arms at the front corners
    for (const sg of [-1, 1]) B.push(box(-X - 1.4, -X + .6, sg > 0 ? hw - .2 : -hw - 1.3, sg > 0 ? hw + 1.3 : -hw + .2, Hs * .6, Hs * .78, { col: '#1b1f24', top: '#2b3036', noEdge: true }));
    return { boxes: B };
  };
  const lamps = [], zt = t => gc + t * (Hs - gc);
  for (const s of [-1, 1]) { lamps.push(kitLamp('H', -X - lean * .15, s * (hw - W * .12), zt(.185), [1, 0, .15], s), kitLamp('I', -X - lean * .15, s * (hw - W * .02), zt(.185), [.85, s * .5, .15], s, { f: 1 }), kitLamp('T', X + .4, s * (hw - W * .04), zt(.3), [-1, 0, .15], s),
    kitLamp('I', X + .4, s * (hw - W * .04), zt(.53), [-.85, s * .5, .15], s, { f: 0 }), kitLamp('R', X + .4, s * (hw - W * .04), zt(.17), [-1, 0, .15], s));
    for (const f of [.22, .5, .78]) lamps.push(kitLamp('W', X + L * f, s * hw, zt((winT0 + winT1) / 2), [0, s, .1], s)) }   // the lit cabin at night, through the side windows
  lamps.push(kitLamp('S', -X - lean * .8, 0, zt(.92), [1, 0, .3], 0));   // the destination sign glows at night
  return { L, W, top: Hb + .9, wheels: [axR, axF].map(u => ({ u, r: wr, tw: 3.6, hw: hw - .4 })), build, lamps, hw };
}
// the tractor unit: a cab-over on a dark chassis — the cab with a sloped windshield, the roof deflector, the mirrors, the steps, the
// exhaust stack; the fifth wheel, the fuel tanks between the axles, a front axle and two drive axles
function tractorKit(L, W, o) {
  const hf = Math.max(.62, Math.min(1, (o.full || L / .3) / 186)), X = -L / 2, Lc = L * .45, Hc = 29 * hf, hw = W / 2 * .97, wr = Math.max(3.6, 4.9 * Math.sqrt(hf)), zc0 = wr * 1.45;
  const cab0 = -X - Lc, axF = -X - Lc * .42, axD = [X + L * .18, X + L * .36], slope = Lc * .13;
  const build = (col) => {
    const B = [];
    B.push(box(X, cab0 + 1, -W * .3, W * .3, wr * .55, wr * 1.25, { col: '#2b3036', top: '#33393f' }));
    B.push(box(X + L * .08, X + L * .46, -W * .34, W * .34, wr * 1.25, wr * 1.25 + 1.3 * hf, { col: '#3a4048', top: '#4a5058', topDraw: (g) => { g.fillStyle = '#4a5058'; g.fillRect(X + L * .08, -W * .34, L * .38, W * .68); g.fillStyle = '#23272c'; g.beginPath(); g.arc(X + L * .27, 0, W * .14, 0, 7); g.fill(); g.fillRect(X + L * .08, -W * .05, L * .19, W * .1) } }));
    { const ta = axD[1] + wr + .6, tb = axF - wr - .6; if (tb - ta > 2) for (const sg of [-1, 1]) B.push(box(ta, tb, sg < 0 ? -hw + .4 : hw - 4.6, sg < 0 ? -hw + 4.6 : hw - .4, wr * .5, zc0 - .1, { col: '#aab2ba', top: '#d6dbe0', deco: (g, f, at) => { kq(g, at, .1, .14, .05, .95, 'rgba(0,0,0,.25)'); kq(g, at, .86, .9, .05, .95, 'rgba(0,0,0,.25)') } })) }
    B.push(box(-X - 1.6, -X + .2, -hw, hw, wr * .45, zc0 + .2, { col: '#2b3036', top: '#3a4048' }));
    // the exhaust stack behind the cab
    B.push(box(cab0 - 1.6, cab0 - .3, hw - 2.6, hw - 1.3, wr * .8, Hc + 2.5 * hf, { col: '#aab2ba', top: '#5b636b', noEdge: true }));
    B.push(box(cab0, -X, -hw, hw, zc0, Hc, { col, ins: { f: slope, r: 0, s: .5 }, topDraw: (g) => { g.fillStyle = sh(col, .1); g.fillRect(cab0, -hw, Lc, 2 * hw); g.fillStyle = 'rgba(0,0,0,.14)'; g.fillRect(cab0 + Lc * .1, -hw * .7, Lc * .45, hw * 1.4) },
      deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.4, .3 * U);
        if (f.n[0] > .3) { // the face: the windshield (two panes), the visor, the grille, the lamps, the bumper line, the badge
          const gs = glassGr(g, at, .5, .9); kq(g, at, .06, .495, .5, .9, gs); kq(g, at, .505, .94, .5, .9, gs); kq(g, at, .04, .96, .9, .96, sh(col, -.3));
          g.fillStyle = 'rgba(255,255,255,.14)'; poly(g, [at(.1, .86), at(.28, .86), at(.2, .54), at(.08, .54)]); g.fill();
          kq(g, at, .2, .8, .14, .44, '#15171b'); g.strokeStyle = '#c7cdd3'; g.lineWidth = lw; g.beginPath(); for (let t = .18; t < .44; t += .06) { const a = at(.22, t), b2 = at(.78, t); g.moveTo(a[0], a[1]); g.lineTo(b2[0], b2[1]) } g.stroke();
          kq(g, at, .44, .56, .46, .49, '#d8dde1'); for (const s2 of [.03, .83]) { kq(g, at, s2, s2 + .14, .12, .22, '#eef3f6', 'rgba(0,0,0,.4)', lw); kq(g, at, s2 + (s2 < .5 ? .15 : -.04), s2 + (s2 < .5 ? .18 : -.01), .12, .22, '#f5a524') } kq(g, at, 0, 1, 0, .09, '#2b3036') }
        else if (Math.abs(f.n[1]) > .5) { // the side: the door with its window, the step, a stripe
          kq(g, at, .5, .95, .52, .88, glassGr(g, at, .52, .88), 'rgba(0,0,0,.45)', lw); g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = lw; poly(g, [at(.42, .04), at(.98, .04), at(.98, .9), at(.42, .9)]); g.stroke();
          kq(g, at, .52, .6, .36, .4, '#c9ced4'); kq(g, at, 0, .4, .3, .36, sh(col, -.25)); kq(g, at, .02, .4, .52, .86, 'rgba(0,0,0,.08)') }
        else kq(g, at, .08, .92, .08, .92, 'rgba(0,0,0,.22)') } }));
    B.push(box(cab0 + .4, cab0 + Lc * .66, -hw * .9, hw * .9, Hc, Hc + 4.5 * hf, { col: sh(col, -.04), ins: { f: Lc * .3, r: 0, s: 1 }, top: sh(col, .14) }));
    // the steps under the doors, the mirrors
    for (const sg of [-1, 1]) { B.push(box(axF - wr - 2.6, axF - wr - .5, sg > 0 ? hw - .6 : -hw - .3, sg > 0 ? hw + .3 : -hw + .6, zc0 - 2.2 * hf, zc0 - .6 * hf, { col: '#3a4048', top: '#8a929a', noEdge: true }));
      B.push(box(-X - slope - 1.2, -X - slope + .4, sg > 0 ? hw - .2 : -hw - 1.5, sg > 0 ? hw + 1.5 : -hw + .2, Hc * .5, Hc * .74, { col: '#1b1f24', top: '#2b3036', noEdge: true })) }
    return { boxes: B };
  };
  const lamps = [];
  for (const s of [-1, 1]) lamps.push(kitLamp('H', -X, s * (hw - W * .13), zc0 + .17 * (Hc - zc0), [1, 0, .15], s), kitLamp('I', -X, s * (hw - .6), zc0 + .17 * (Hc - zc0), [.85, s * .5, .15], s, { f: 1 }));
  return { L, W, top: Hc + 4.5 * hf, wheels: [{ u: axF, r: wr, tw: 3.6, hw: hw - .3, zcl: zc0 }, ...axD.map(u => ({ u, r: wr, tw: 4.4, hw: hw - .3 }))], build, lamps, hw, nose: -X };
}
// the trailer: the box (a light tint of the paint, like lv(): sh(col, .58), the colour band of the company), the landing legs, the axles,
// the rear doors — or the container chassis: two rails and the boxes on them (cargo: the picture of the container on top, its colour)
function trailerKit(L, W, o, chassis) {
  const hf = Math.max(.62, Math.min(1, (o.full || L / .84) / 186)), X = -L / 2, hw = W / 2, zf = 11.5 * hf, Ht = 39 * hf, wr = Math.max(3.6, 4.9 * Math.sqrt(hf)), axl = [.13, .21, .29].map(f => X + L * f);
  const build = (col, opt) => {
    const B = [], panel = sh(col, .58);
    B.push(box(X + 1, -X - 1.2, -W * .28, W * .28, wr * 1.2, zf - (chassis ? 2.2 * hf : .2), { col: '#2b3036', top: '#33393f' }));
    B.push(box(X, X + 1.2, -hw + 1, hw - 1, 2.8 * hf, 4.8 * hf, { col: '#2b3036', top: '#3a4048' }));
    for (const sg of [-1, 1]) B.push(box(-X - L * .24, -X - L * .24 + 1.1, sg * W * .3 - .6, sg * W * .3 + .6, 0, zf - .5, { col: '#3a4048', top: '#3a4048' }));
    if (!chassis) {
      B.push(box(X, -X, -hw, hw, zf, Ht, { col: panel, topDraw: (g) => { g.fillStyle = sh(panel, .06); g.fillRect(X, -hw, L, W); g.fillStyle = 'rgba(0,0,0,.08)'; for (let x = X + 4; x < -X - 2; x += 4.6) g.fillRect(x, -hw + .6, .6, W - 1.2); g.fillStyle = col; g.fillRect(-X - L * .06, -W * .2, L * .06, W * .4) },
        deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U);
          if (Math.abs(f.n[1]) > .5) { kq(g, at, 0, 1, 0, .07, col); kq(g, at, 0, 1, .95, 1, col); kq(g, at, .72, .97, .22, .62, col); kq(g, at, .76, .93, .3, .54, 'rgba(255,255,255,.85)');
            for (let s2 = .01; s2 < .97; s2 += .04) kq(g, at, s2, s2 + .02, .075, .1, (Math.round(s2 * 25) % 2) ? '#d23a3a' : '#f4f6f8'); for (const s2 of [.04, .5, .95]) kq(g, at, s2 - .006, s2 + .006, .11, .15, '#f5a524');
            g.strokeStyle = 'rgba(0,0,0,.09)'; g.lineWidth = lw; g.beginPath(); for (let s2 = .02; s2 < 1; s2 += .022) { const a = at(s2, .08), b = at(s2, .94); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke() }
          else if (f.n[0] < -.5) { g.strokeStyle = 'rgba(0,0,0,.4)'; g.lineWidth = lw; poly(g, [at(.03, .03), at(.97, .03), at(.97, .97), at(.03, .97)]); g.stroke(); const a = at(.5, .03), b = at(.5, .97); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
            g.fillStyle = 'rgba(60,66,72,.8)'; for (const s2 of [.3, .42, .58, .7]) kq(g, at, s2 - .012, s2 + .012, .06, .94, 'rgba(70,76,82,.55)') } } }));
    } else {
      for (const sg of [-1, 1]) B.push(box(X, -X, sg * W * .3 - 1.4, sg * W * .3 + 1.4, zf - 2.2 * hf, zf, { col: '#23272c', top: '#2f353b' }));
      for (let i = 0; i < 6; i++) { const u = X + 3 + i * (L - 6) / 5; B.push(box(u - .7, u + .7, -hw + .8, hw - .8, zf - 1.6 * hf, zf - .4 * hf, { col: '#2b3036', top: '#3a4048' })) }
      const cg = opt && opt.cargo; if (cg) { const Hc = 25.5 * hf, list = cg.type === '40' ? [[X + .6, -X - .6]] : [[X + .4, -.6], [.6, -X - .4]];
        list.forEach(([u0, u1], j) => { const tex = cg.tex && cg.tex[j], cc = (cg.col && cg.col[j]) || '#9a6a3a';
          B.push(box(u0, u1, -hw + .3, hw - .3, zf, zf + Hc, { col: cc, topDraw: (g) => { if (tex && tex.cv && tex.sw) g.drawImage(tex.cv, tex.sx, tex.sy, tex.sw, tex.sh, u0, -hw + .3, u1 - u0, W - .6); else if (tex && tex.cv) g.drawImage(tex.cv, u0, -hw + .3, u1 - u0, W - .6); else { g.fillStyle = sh(cc, .1); g.fillRect(u0, -hw, u1 - u0, W) } },
            deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U);
              if (Math.abs(f.n[1]) > .5) { g.strokeStyle = 'rgba(0,0,0,.16)'; g.lineWidth = lw; g.beginPath(); for (let s2 = .02; s2 < 1; s2 += .03) { const a = at(s2, .04), b = at(s2, .96); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke(); kq(g, at, 0, 1, 0, .04, 'rgba(0,0,0,.25)'); kq(g, at, 0, 1, .96, 1, 'rgba(255,255,255,.15)') }
              else { g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = lw; g.beginPath(); for (const s2 of [.25, .5, .75]) { const a = at(s2, .04), b = at(s2, .96); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke(); poly(g, [at(.03, .03), at(.97, .03), at(.97, .97), at(.03, .97)]); g.stroke() } } })) }) }
    }
    return { boxes: B };
  };
  const lamps = [];
  for (const s of [-1, 1]) lamps.push(kitLamp('T', X, s * (hw - 2), (chassis ? zf - 1.4 : zf) * .62 + 1, [-1, 0, .1], s), kitLamp('I', X, s * (hw - .7), (chassis ? zf - 1.4 : zf) * .62 + 1, [-.85, s * .5, .1], s, { f: 0 }), kitLamp('R', X, s * (hw - 4.4), (chassis ? zf - 1.4 : zf) * .62 + 1, [-1, 0, .1], s));
  return { L, W, top: chassis ? zf + 25.5 * hf : Ht, wheels: axl.map(u => ({ u, r: wr, tw: 4.4, hw: hw - .3, zcl: chassis ? null : zf })), build, lamps, hw, nose: -X, cyl: null };
}
// the tanker (a rigid truck): the cab, the chassis, a round tank
function tankerKit(L, W, o) {
  const X = -L / 2, hw = W / 2, Lc = L * .22, Hc = 27, wr = 4.6, tr = W * .47, tz = 9 + tr;
  const build = (col) => {
    const B = []; B.push(box(X + 1, -X - Lc, -W * .3, W * .3, wr * .5, wr * 1.6, { col: '#2b3036', top: '#33393f' }));
    B.push(box(-X - Lc, -X, -hw, hw, wr * 1.5, Hc, { col, top: sh(col, .1), deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.4, .3 * U);
      if (f.n[0] > .5) { kq(g, at, .07, .93, .52, .88, glassGr(g, at, .52, .88), 'rgba(0,0,0,.5)', lw); kq(g, at, .2, .8, .14, .44, '#15171b'); for (const s2 of [.03, .83]) kq(g, at, s2, s2 + .14, .12, .22, '#eef3f6') }
      else if (Math.abs(f.n[1]) > .5) kq(g, at, .5, .95, .52, .86, glassGr(g, at, .52, .86), 'rgba(0,0,0,.45)', lw) } }));
    return { boxes: B, cyls: [{ u0: X + 1, u1: -X - Lc - 1.5, r: tr, z: tz, col: '#cfd6dc', bands: 4 }] };
  };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X, s * (hw - 2.2), 6, [1, 0, .15], s), kitLamp('I', -X, s * (hw - .6), 7, [.85, s * .5, .15], s, { f: 1 }), kitLamp('T', X, s * (hw - 1.5), 7, [-1, 0, .1], s), kitLamp('I', X, s * (hw - .6), 7, [-.85, s * .5, .1], s, { f: 0 }), kitLamp('R', X, s * (hw - 4), 7, [-1, 0, .1], s));
  return { L, W, top: tz + tr, wheels: [.14, .5, .58, .9].map(f => ({ u: X + f * L, r: wr, tw: 3.8, hw: hw - .3, zcl: f > .8 ? wr * 1.5 : null })), build, lamps, hw, nose: -X };
}
// the forklift: the counterweight, the seat under the overhead guard, the mast with the carriage and the forks in front
function forkKit(L, W, o) {
  const X = -L / 2, hw = W / 2, Hg = Math.max(18, L * .78), mast = -X - L * .29;
  const build = (col) => {
    const B = [], dk = '#2b3036', st = '#3a4048';
    B.push(box(X, X + L * .24, -hw, hw, 1.6, 10.5, { col: sh(col, -.12), top: sh(col, -.04) }));
    B.push(box(X + L * .24, mast - .4, -hw * .96, hw * .96, 1.6, 8, { col, top: sh(col, .08) }));
    B.push(box(X + L * .34, X + L * .52, -hw * .55, hw * .55, 8, 11.5, { col: '#1b1f24', top: '#262b31' }));
    for (const u of [X + L * .3, mast - 1.6]) for (const sg of [-1, 1]) B.push(box(u, u + .9, sg * (hw - .5) - .45, sg * (hw - .5) + .45, 8, Hg, { col: dk, top: dk, noEdge: true }));
    B.push(box(X + L * .28, mast - .4, -hw, hw, Hg, Hg + .9, { col: dk, top: dk, topDraw: (g) => { g.fillStyle = 'rgba(30,34,38,.85)'; g.fillRect(X + L * .28, -hw, mast - .4 - X - L * .28, W); g.fillStyle = 'rgba(160,168,176,.4)'; for (let u = X + L * .3; u < mast - 1; u += 1.6) g.fillRect(u, -hw + .4, .45, W - .8) } }));
    for (const sg of [-1, 1]) B.push(box(mast, mast + 1.2, sg * hw * .6 - .55, sg * hw * .6 + .55, 1, Hg + 2, { col: st, top: st }));
    B.push(box(mast, mast + 1.2, -hw * .6, hw * .6, Hg + 1, Hg + 2.2, { col: st, top: st }));
    B.push(box(mast + 1.2, mast + 2, -hw * .78, hw * .78, 1, 6.5, { col: '#4a5058', top: '#5b636b' }));
    for (const sg of [-1, 1]) B.push(box(mast + 2, -X, sg * hw * .45 - .55, sg * hw * .45 + .55, 1, 1.7, { col: '#9aa1a8', top: '#b9c0c7' }));
    return { boxes: B };
  };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', mast - 1.1, s * (hw - .5), Hg - 1.5, [1, 0, .1], s), kitLamp('T', X, s * (hw - 1), 8.5, [-1, 0, .1], s), kitLamp('R', X, s * (hw - 2.6), 8.5, [-1, 0, .1], s));
  lamps.push(kitLamp('Y', X + L * .32, -1.2, Hg + 1.6, [0, 0, 1], -1), kitLamp('Y', X + L * .32, 1.2, Hg + 1.6, [0, 0, 1], 1));
  return { L, W, top: Hg + 1, wheels: [{ u: mast - L * .1, r: 3.2, tw: 2.6, hw: hw - .2 }, { u: X + L * .2, r: 2.7, tw: 2.4, hw: hw - .2 }], build, lamps, hw, nose: -X };
}
// p386 (S7F139) · the containers standing on the ground — a stack of o.n boxes (1 … 3), each with the picture of its container on top (the
// game's own top view, as on the chassis of a port truck) and its corrugated sides in its colour: opt.cargo = { key, tex: [per tier],
// col: [per tier] } (tier 0 the lowest). The height of a box: the width × 1.0 (a container is 2.59 m tall, 2.44 m wide).
function cstackKit(L, W, o) {
  const n = Math.max(1, Math.min(4, (o && +o.n) || 1)), X = -L / 2, hw = W / 2, Hc = W * 1.0;
  const build = (col, opt) => {
    const B = [], cg = (opt && opt.cargo) || {};
    for (let j = 0; j < n; j++) { const tex = cg.tex && cg.tex[j], cc = (cg.col && cg.col[j]) || col || '#8a6a4a', top = j === n - 1, z0 = j * Hc, z1 = (j + 1) * Hc - (top ? 0 : .25);
      B.push(box(X + .2, -X - .2, -hw + .2, hw - .2, z0, z1, { col: cc, top: sh(cc, .08), topDraw: top ? (g) => { if (tex && tex.cv && tex.sw) g.drawImage(tex.cv, tex.sx, tex.sy, tex.sw, tex.sh, X + .2, -hw + .2, L - .4, W - .4); else if (tex && tex.cv) g.drawImage(tex.cv, X + .2, -hw + .2, L - .4, W - .4); else { g.fillStyle = sh(cc, .1); g.fillRect(X, -hw, L, W) } } : null,
        deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U);
          if (Math.abs(f.n[1]) > .5) { g.strokeStyle = 'rgba(0,0,0,.16)'; g.lineWidth = lw; g.beginPath(); for (let s2 = .02; s2 < 1; s2 += Math.max(.012, 2.2 / L)) { const a = at(s2, .04), b = at(s2, .96); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke(); kq(g, at, 0, 1, 0, .05, 'rgba(0,0,0,.28)'); kq(g, at, 0, 1, .95, 1, 'rgba(255,255,255,.16)');
            for (const s2 of [0, .985]) kq(g, at, s2, s2 + .015, 0, 1, 'rgba(40,44,48,.55)') }   // the corner posts
          else { g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = lw; g.beginPath(); for (const s2 of [.25, .5, .75]) { const a = at(s2, .04), b = at(s2, .96); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke(); poly(g, [at(.03, .03), at(.97, .03), at(.97, .97), at(.03, .97)]); g.stroke() } } }));
      if (!top) B[B.length - 1].topDraw = null }
    return { boxes: B };
  };
  return { L, W, top: n * Hc, wheels: [], build, lamps: [], hw, nose: -X };
}
// p386 (S7F139) · the reach stacker (LV-RS-01, ~9 × 3.2 m): the chassis on two axles (the big drive wheels in front), the counterweight
// at the back, the engine, the cab set to the left, the telescopic boom rising from behind the cab over the front axle and the spreader
// across its tip; the beacon on the cab, the head lamps on the cab front, the tail lamps at the back.
function reachKit(L, W, o) {
  const X = -L / 2, hw = W / 2, s = L / 67, zc = 3.2 * s, zd = 10 * s, cab0 = X + L * .44, cab1 = X + L * .66, Hcab = 25 * s, pv = X + L * .22, tip = -X + L * .03, zb0 = 17 * s, zb1 = 31 * s, bw = W * .17, sp = W * .95;
  const build = (col) => {
    const B = [], dk = '#2b3036', st = '#3a4048', c2 = sh(col, -.14);
    B.push(box(X, X + L * .2, -hw, hw, zc, 15.5 * s, { col: c2, top: sh(col, -.06) }));                                   // the counterweight
    B.push(box(X + L * .2, -X - L * .1, -hw * .94, hw * .94, zc, zd, { col, top: sh(col, .08) }));                        // the chassis
    B.push(box(X + L * .2, cab0 - .5, -hw * .7, hw * .55, zd, 14.5 * s, { col: c2, top: sh(col, .02), topDraw: (g) => { g.fillStyle = sh(col, .02); g.fillRect(X + L * .2, -hw * .7, cab0 - .5 - X - L * .2, hw * 1.25); g.fillStyle = 'rgba(20,24,28,.35)'; for (let u = X + L * .23; u < cab0 - 2; u += 2.2 * s) g.fillRect(u, -hw * .6, .8 * s, hw * 1.05) } }));   // the engine, its grille
    B.push(box(cab0, cab1, -hw, -hw + W * .46, zd, Hcab, { col: '#1b1f24', top: sh(col, .1), ins: { r: .4 * s, f: 1.2 * s, s: .3 * s },
      deco: (g, f, at) => { if (f.n[2] > .5) return; kq(g, at, .06, .94, .38, .9, 'rgba(150,185,210,.75)') } }));          // the cab, glass all round
    B.push({ base: [[pv, -bw], [pv + 6 * s, -bw], [pv + 6 * s, bw], [pv, bw]], topBase: [[tip - 7 * s, -bw], [tip, -bw], [tip, bw], [tip - 7 * s, bw]], z0: zb0, z1: zb1,
      col: sh(col, -.02), top: sh(col, .1), c: [(pv + tip) / 2, 0, (zb0 + zb1) / 2] });                                    // the boom, rising to the front
    for (const sg of [-1, 1]) B.push(box(pv - 1.2 * s, pv + 4 * s, sg * bw * 1.25 - .6 * s, sg * bw * 1.25 + .6 * s, zd, zb0 + 1.5 * s, { col: st, top: st }));   // its pivot
    B.push(box(tip - 2.4 * s, tip + 2.4 * s, -sp / 2, sp / 2, zb1 - 5.5 * s, zb1 - 2.5 * s, { col: dk, top: '#4a5058' }));   // the spreader
    for (const sg of [-1, 1]) B.push(box(tip - 2.6 * s, tip + 2.6 * s, sg < 0 ? -sp / 2 : sp / 2 - 2.2 * s, sg < 0 ? -sp / 2 + 2.2 * s : sp / 2, zb1 - 7 * s, zb1 - 2 * s, { col: '#e8b92b', top: '#f2c84b' }));   // its yellow ends
    return { boxes: B };
  };
  const lamps = []; for (const sg of [-1, 1]) lamps.push(kitLamp('H', cab1, -hw + W * .23 + sg * W * .15, Hcab - 3 * s, [1, 0, .1], sg), kitLamp('T', X, sg * (hw - 1.5 * s), 9 * s, [-1, 0, .1], sg), kitLamp('R', X, sg * (hw - 4 * s), 9 * s, [-1, 0, .1], sg));
  lamps.push(kitLamp('Y', (cab0 + cab1) / 2, -hw + W * .23, Hcab + .8 * s, [0, 0, 1], -1));
  return { L, W, top: zb1, wheels: [{ u: -X - L * .22, r: 5.2 * s, tw: 4.4 * s, hw: hw - .2 }, { u: X + L * .2, r: 4.4 * s, tw: 3.8 * s, hw: hw - .2 }], build, lamps, hw, nose: -X };
}
// ---------- p392 · the airport's ground vehicles and the farm's machines (D‑283: after entering an area no vehicle is seen from above) ----------
// The game paints them top-down (s6aDraw, g77DrawGse, f2DrawStairs, the farm's sprites); here each is a kit of boxes like the heavy
// vehicles: the game's footprint (L, W in world px) and the heights from the real vehicle (pm: px a metre = W ÷ its real width).
// A sloped solid (the belt, the stairs) is a box whose top rectangle stands further along u than its base (as the reach stacker's boom).
const GSE_Y = '#e8b92b', GSE_D = '#2b3036', GSE_M = '#3a4048', GSE_G = '#9aa3ab';
const slope = (u0, u1, d, v0, v1, z0, z1, o) => Object.assign({ base: [[u0, v0], [u0 + d, v0], [u0 + d, v1], [u0, v1]], topBase: [[u1 - d, v0], [u1, v0], [u1, v1], [u1 - d, v1]], z0, z1, c: [(u0 + u1) / 2, (v0 + v1) / 2, (z0 + z1) / 2] }, o || {});
// a small cab: the glass on the front, the sides and the back (the front +u)
function gseCab(u0, u1, v0, v1, z0, z1, col, o) {
  return box(u0, u1, v0, v1, z0, z1, Object.assign({ col, top: sh(col, .1), ins: { f: (u1 - u0) * .1, r: 0, s: .2 }, deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U);
    if (f.n[2] > .5) return; if (f.n[0] > .3) kq(g, at, .08, .92, .45, .92, glassGr(g, at, .45, .92), 'rgba(0,0,0,.45)', lw);
    else if (Math.abs(f.n[1]) > .5) kq(g, at, .1, .9, .45, .9, glassGr(g, at, .45, .9), 'rgba(0,0,0,.4)', lw);
    else kq(g, at, .15, .85, .5, .88, glassGr(g, at, .5, .88), 'rgba(0,0,0,.4)', lw) } }, o || {}));
}
const hazard = (g, at, t0, t1) => { for (let s2 = 0; s2 < 1; s2 += .125) kq(g, at, s2, s2 + .0625, t0, t1, GSE_Y); };
// the baggage tug (1.45 m wide): a low body, the seat under a canopy on four posts, the hitch at the back
function btugKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 1.45, z = m => m * pm, wr = z(.26);
  const build = (col) => { const B = [];
    B.push(box(X + z(.15), -X - z(.1), -hw, hw, wr * .7, z(.9), { col, top: sh(col, .08), deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) kq(g, at, 0, 1, .05, .22, GSE_Y); else if (f.n[0] > .5) { kq(g, at, .15, .85, .3, .7, '#15171b') } } }));
    B.push(box(-X - L * .36, -X - z(.1), -hw * .9, hw * .9, z(.9), z(1.05), { col: sh(col, -.06), top: sh(col, .04) }));   // the hood
    B.push(box(X + L * .18, X + L * .44, -hw * .6, hw * .6, z(.9), z(1.3), { col: GSE_D, top: '#3a4048' }));                 // the seat
    for (const u of [X + L * .1, -X - L * .38]) for (const sg of [-1, 1]) B.push(box(u, u + z(.06), sg * (hw - z(.08)) - z(.03), sg * (hw - z(.08)) + z(.03), z(.9), z(1.85), { col: GSE_M, top: GSE_M, noEdge: true }));
    B.push(box(X + L * .06, -X - L * .33, -hw, hw, z(1.85), z(1.93), { col: sh(col, -.04), top: sh(col, .12) }));            // the canopy
    B.push(box(X - z(.25), X + z(.05), -z(.08), z(.08), z(.3), z(.42), { col: GSE_D, top: GSE_D, noEdge: true }));           // the hitch
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X - z(.1), s * (hw - z(.2)), z(.75), [1, 0, .1], s), kitLamp('T', X + z(.15), s * (hw - z(.15)), z(.6), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', X + L * .25, 0, z(1.98), [0, 0, 1], -1));
  return { L, W, top: z(1.93), wheels: [{ u: -X - L * .2, r: wr, tw: z(.2), hw: hw - z(.08) }, { u: X + L * .24, r: wr, tw: z(.22), hw: hw - z(.08) }], build, lamps, hw, nose: -X };
}
// the pushback tug (towbar type, 2.7 m wide): a long low slab, the cab at the back, bumpers with hazard stripes, big wheels
function ptugKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 2.7, z = m => m * pm, wr = z(.5);
  const build = (col) => { const B = [], body = GSE_Y;
    B.push(box(X + z(.1), -X - z(.1), -hw, hw, z(.35), z(1.2), { col: body, top: sh(body, .08), deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[0]) > .5) { kq(g, at, 0, 1, 0, .3, GSE_D); hazard(g, at, .3, .5) } else kq(g, at, 0, 1, 0, .12, GSE_D) } }));
    B.push(gseCab(X + L * .08, X + L * .36, -hw * .78, hw * .78, z(1.2), z(2.05), col));
    B.push(box(-X - z(.1), -X + z(.12), -hw * .6, hw * .6, z(.45), z(.8), { col: GSE_D, top: GSE_M }));                     // the front bumper / tow pin
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X, s * (hw - z(.35)), z(1.0), [1, 0, .1], s), kitLamp('T', X + z(.1), s * (hw - z(.3)), z(.9), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', X + L * .22, 0, z(2.1), [0, 0, 1], -1));
  return { L, W, top: z(2.05), wheels: [{ u: -X - L * .2, r: wr, tw: z(.4), hw: hw - z(.1) }, { u: X + L * .22, r: wr, tw: z(.4), hw: hw - z(.1) }], build, lamps, hw, nose: -X };
}
// the belt loader (2 m wide): the chassis, the driver's seat on the left, the belt rising to the front (to the hold's door) with its rails
function beltKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 2.0, z = m => m * pm, wr = z(.3), bw = W * .2;
  const build = (col) => { const B = [];
    B.push(box(X + z(.2), -X - z(.4), -hw * .8, hw * .8, wr * .8, z(.85), { col, top: sh(col, .06), deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) kq(g, at, 0, 1, .06, .22, GSE_Y) } }));
    B.push(gseCab(X + L * .3, X + L * .5, -hw, -hw + W * .45, z(.85), z(1.95), col));
    B.push(slope(X + z(.1), -X, z(.5), -bw, bw, z(.9), z(3.0), { col: GSE_M, top: '#23272c' }));                             // the belt
    for (const sg of [-1, 1]) B.push(slope(X + z(.1), -X, z(.12), sg * (bw + z(.05)) - z(.04), sg * (bw + z(.05)) + z(.04), z(1.05), z(3.3), { col: GSE_G, top: '#c7cdd3', noEdge: true }));   // its rails
    for (const f of [.35, .75]) { const u = X + L * f; B.push(box(u - z(.08), u + z(.08), -bw * .7, bw * .7, z(.85), z(.9 + 2.1 * (f + .05)), { col: GSE_D, top: GSE_D, noEdge: true })) }   // the props
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X - z(.4), s * (hw * .8 - z(.2)), z(.7), [1, 0, .1], s), kitLamp('T', X + z(.2), s * (hw * .8 - z(.2)), z(.7), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', X + L * .4, -hw + W * .22, z(2.0), [0, 0, 1], -1));
  return { L, W, top: z(3.3), wheels: [{ u: -X - L * .28, r: wr, tw: z(.25), hw: hw * .8 }, { u: X + L * .22, r: wr, tw: z(.25), hw: hw * .8 }], build, lamps, hw, nose: -X };
}
// the catering truck (2.5 m wide): the cab in front, the body raised on its scissor (here at its lowest), the platform at the front of the body
function caterKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 2.5, z = m => m * pm, wr = z(.45), Lc = L * .23, band = '#2f6fd0';
  const build = (col) => { const B = [];
    B.push(box(X + z(.2), -X - z(.2), -hw * .9, hw * .9, wr * .9, z(1.05), { col: GSE_D, top: GSE_M, deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) { g.strokeStyle = GSE_G; g.lineWidth = Math.max(.4, .3 * U); const a = at(.05, .2), b = at(.6, .95), c2 = at(.05, .95), d = at(.6, .2); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.moveTo(c2[0], c2[1]); g.lineTo(d[0], d[1]); g.stroke() } } }));
    B.push(gseCab(-X - Lc, -X, -hw, hw, z(.55), z(2.6), col));
    B.push(box(X + z(.15), -X - Lc - z(.3), -hw, hw, z(1.15), z(3.75), { col, top: sh(col, .1), deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) { kq(g, at, 0, 1, .38, .5, band); kq(g, at, .02, .98, .02, .06, 'rgba(0,0,0,.2)') } else if (f.n[0] < -.5) { kq(g, at, .1, .9, .08, .9, sh(col, -.1)); kq(g, at, .48, .52, .08, .9, 'rgba(0,0,0,.3)') } } }));
    B.push(box(-X - Lc - z(.3), -X - Lc + z(.5), -hw * .9, hw * .9, z(3.55), z(3.75), { col: GSE_G, top: '#c7cdd3' }));      // the platform
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X, s * (hw - z(.35)), z(.9), [1, 0, .15], s), kitLamp('T', X + z(.15), s * (hw - z(.25)), z(1.3), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', -X - Lc * .5, 0, z(2.65), [0, 0, 1], -1));
  return { L, W, top: z(3.75), wheels: [{ u: -X - Lc * .5, r: wr, tw: z(.3), hw: hw - z(.1) }, { u: X + L * .24, r: wr, tw: z(.35), hw: hw - z(.1) }], build, lamps, hw, nose: -X };
}
// the ground power unit / the air cart (1.6 m wide): a box on four small wheels, the grille, the drawbar; tag 'ac' — the air cart's duct
function gpuKit(L, W, o) { const X = -L / 2, hw = W / 2, pm = W / 1.6, z = m => m * pm, wr = z(.22), ac = o && o.tag === 'ac';
  const build = (col) => { const B = [], c2 = ac ? '#d6dce1' : col;
    B.push(box(X + z(.1), -X - z(.35), -hw, hw, wr * 1.1, z(1.35), { col: c2, top: sh(c2, .08), deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) { g.fillStyle = 'rgba(0,0,0,.28)'; for (let s2 = .12; s2 < .5; s2 += .08) kq(g, at, s2, s2 + .04, .35, .8, 'rgba(0,0,0,.28)'); kq(g, at, .6, .9, .1, .3, GSE_Y) } } }));
    B.push(box(-X - z(.35), -X + z(.2), -z(.05), z(.05), z(.3), z(.4), { col: GSE_D, top: GSE_D, noEdge: true }));             // the drawbar
    if (ac) B.push(box(X - z(.1), X + z(.4), -hw * .5, hw * .5, z(1.0), z(1.5), { col: GSE_Y, top: sh(GSE_Y, .1) }));          // the duct's reel
    else B.push(box(X + z(.3), X + L * .45, -hw * .7, hw * .7, z(1.35), z(1.6), { col: GSE_D, top: '#3a4048' }));                // the cable reel
    return { boxes: B } };
  return { L, W, top: z(1.6), wheels: [{ u: -X - L * .3, r: wr, tw: z(.16), hw: hw - z(.06) }, { u: X + L * .22, r: wr, tw: z(.16), hw: hw - z(.06) }], build, lamps: [], hw, nose: -X };
}
// the main-deck loader (2.9 m wide): the low chassis, the long deck with its rollers, the bridge at the front, the operator's cab at the rear left
function hiloKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 2.9, z = m => m * pm, wr = z(.33);
  const build = (col) => { const B = [];
    B.push(box(X + z(.2), -X - z(.3), -hw * .85, hw * .85, wr * .9, z(.8), { col: GSE_D, top: GSE_M }));
    B.push(box(X + L * .2, -X - L * .1, -hw, hw, z(.8), z(1.0), { col, top: sh(col, .06), topDraw: (g) => { g.fillStyle = sh(col, .06); g.fillRect(X + L * .2, -hw, L * .7, W); g.fillStyle = 'rgba(40,46,52,.55)'; for (let u = X + L * .22; u < -X - L * .12; u += z(.35)) g.fillRect(u, -hw * .85, z(.12), W * .85) },
      deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) hazard(g, at, 0, 1) } }));
    for (const sg of [-1, 1]) B.push(box(X + L * .2, -X - L * .1, sg * (hw - z(.06)) - z(.04), sg * (hw - z(.06)) + z(.04), z(1.0), z(1.35), { col: GSE_G, top: '#c7cdd3', noEdge: true }));   // the rails
    B.push(box(-X - L * .1, -X, -hw * .7, hw * .7, z(.85), z(1.0), { col: GSE_G, top: '#c7cdd3' }));                          // the bridge
    B.push(gseCab(X + z(.1), X + L * .19, -hw, -hw + W * .38, z(.8), z(2.4), col));
    return { boxes: B } };
  const lamps = [kitLamp('Y', X + L * .1, -hw + W * .19, z(2.45), [0, 0, 1], -1)]; for (const s of [-1, 1]) lamps.push(kitLamp('T', X + z(.2), s * (hw * .85 - z(.2)), z(.6), [-1, 0, .1], s));
  return { L, W, top: z(2.4), wheels: [.16, .4, .64, .86].map(f => ({ u: X + L * f, r: wr, tw: z(.25), hw: hw * .82 })), build, lamps, hw, nose: -X };
}
// the passenger stairs truck (R-28, the owner 20:39; after a TLD ABS-580 / Mallaghan ST1000: 2.4 m wide, ~8.6 m long): the chassis and
// the low cab at the front; the flight rising from the rear (the bottom step 0.9 m) to the top platform, which stands over the cab on two
// pairs of columns from the chassis; the platform and the passage to the door are one deck (the passage slides out of the platform's front
// by o.ext px, its front edge with the black rubber bumper) at the door's sill — o.hpx px (the platform's top, absolute: the aircraft's
// door sill × the airport's px a metre), never lower than over the cab; side rails on the flight, the platform and the passage. Nothing hangs
// in the air: the flight on the chassis at the rear and an A-frame at its middle, the platform on its columns, the passage in the platform.
function stairsKit(L, W, o) { o = o || {}; const X = -L / 2, hw = W / 2, pm = W / 2.4, z = m => m * pm, wr = z(.42), Lc = L * .2, sw = z(.62);
  const H = Math.max(z(2.75), +o.hpx || z(3.4)), ext = Math.max(0, Math.min(z(2.6), +o.ext || 0)), th = z(.16), U1 = -X, U0 = U1 - Lc - z(1.4);
  const build = (col) => { const B = [];
    B.push(box(X + z(.2), U1 - z(.2), -hw * .85, hw * .85, wr * .9, z(1.0), { col: GSE_D, top: GSE_M }));                       // the chassis
    B.push(gseCab(U1 - Lc, U1, -hw, hw, z(.5), z(2.3), col));                                                                   // the cab
    // the platform's columns (behind the cab, both sides) and the A-frame under the flight's middle: from the chassis to what they carry
    for (const sg of [-1, 1]) { B.push(box(U0 + z(.1), U0 + z(.35), sg * sw - z(.12), sg * sw + z(.12), z(1.0), H - th, { col: GSE_M, top: GSE_M, noEdge: true }));
      B.push(box(U1 - Lc - z(.3), U1 - Lc - z(.08), sg * sw - z(.1), sg * sw + z(.1), z(1.0), H - th, { col: GSE_M, top: GSE_M, noEdge: true })) }
    const um = (X + z(.3) + U0) / 2, zm = z(1.0) + (H - z(1.0)) * .5;
    B.push(box(um - z(.2), um + z(.2), -sw * .7, sw * .7, z(1.0), zm - th, { col: GSE_M, top: GSE_M, noEdge: true }));
    // the flight: from the rear (on the chassis) up to the platform's back edge, its treads yellow-nosed
    B.push(slope(X + z(.3), U0 + z(.02), z(.9), -sw, sw, z(1.0), H, { col: GSE_G, top: '#d6dbe0', deco: (g, f, at0) => { if (f.n[2] > .3) return; kq(g, at0, 0, 1, 0, .25, GSE_Y) } }));
    for (const sg of [-1, 1]) B.push(slope(X + z(.3), U0 + z(.02), z(.1), sg * (sw + z(.05)) - z(.04), sg * (sw + z(.05)) + z(.04), z(1.9), H + z(1.0), { col: '#eef1f3', top: '#ffffff', noEdge: true }));
    // the deck: the platform over the cab and the passage out of its front — one piece, its top at H
    B.push(box(U0, U1 + ext, -sw - z(.1), sw + z(.1), H - th, H, { col: GSE_G, top: '#c7cdd3' }));
    B.push(box(U1 + ext - z(.12), U1 + ext, -sw - z(.1), sw + z(.1), H - th * 1.6, H + z(.05), { col: '#15181b', top: '#25292d', noEdge: true }));   // the bumper
    for (const sg of [-1, 1]) B.push(box(U0, U1 + ext - z(.15), sg * (sw + z(.05)) - z(.04), sg * (sw + z(.05)) + z(.04), H, H + z(1.0), { col: '#eef1f3', top: '#ffffff', noEdge: true }));   // its rails
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', U1, s * (hw - z(.35)), z(.9), [1, 0, .15], s), kitLamp('T', X + z(.2), s * (hw - z(.25)), z(.8), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', U1 - Lc * .5, 0, z(2.35), [0, 0, 1], -1));
  return { L, W, top: H + z(1.0), wheels: [{ u: U1 - Lc * .5, r: wr, tw: z(.3), hw: hw - z(.1) }, { u: X + L * .2, r: wr, tw: z(.3), hw: hw - z(.1) }], build, lamps, hw, nose: -X + ext, deck: { H, ext, u1: U1 + ext, sw } };
}
// a baggage cart / a cart of the train (1.5 m wide): the chassis, the bed with its low rails, the drawbar; the bags are the game's own on it
function bcartKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 1.5, z = m => m * pm, wr = z(.19);
  const build = (col) => { const B = [];
    B.push(box(X + z(.05), -X - z(.05), -hw, hw, wr * 1.1, z(.5), { col: '#4a5560', top: '#aab4bd' }));
    for (const sg of [-1, 1]) B.push(box(X + z(.05), -X - z(.05), sg * (hw - z(.04)) - z(.03), sg * (hw - z(.04)) + z(.03), z(.5), z(.78), { col: GSE_M, top: GSE_G, noEdge: true }));
    B.push(box(X + z(.05), X + z(.14), -hw, hw, z(.5), z(.85), { col: GSE_Y, top: sh(GSE_Y, .1) }));                         // the yellow tail edge
    B.push(box(-X - z(.05), -X + z(.5), -z(.04), z(.04), z(.28), z(.36), { col: GSE_D, top: GSE_D, noEdge: true }));           // the drawbar
    return { boxes: B } };
  return { L, W, top: z(.85), deck: z(.5), wheels: [{ u: -X - L * .2, r: wr, tw: z(.14), hw: hw - z(.06) }, { u: X + L * .2, r: wr, tw: z(.14), hw: hw - z(.06) }], build, lamps: [], hw, nose: -X };
}
// the farm tractor (2.4 m wide): the big rear wheels under their fenders, the small front ones, the hood, the cab glazed all round
function ftracKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 2.4, z = m => m * pm, wr = z(.8), wf = z(.47);
  const build = (col) => { const B = [], uR = X + L * .3;
    B.push(box(X + L * .12, -X - z(.15), -hw * .32, hw * .32, z(.5), z(1.45), { col, top: sh(col, .1), deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (f.n[0] > .5) kq(g, at, .15, .85, .2, .8, '#15171b') } }));   // the hood
    B.push(gseCab(uR - z(.75), uR + z(.75), -hw * .62, hw * .62, z(1.3), z(2.85), col, { top: sh(col, .14) }));
    for (const sg of [-1, 1]) B.push(box(uR - wr * 1.05, uR + wr * 1.05, sg * (hw - z(.25)) - z(.28), sg * (hw - z(.25)) + z(.28), wr * 1.6, wr * 1.75, { col: sh(col, -.1), top: sh(col, -.02), noEdge: true }));   // the fenders
    B.push(box(X - z(.1), X + z(.2), -z(.12), z(.12), z(.5), z(.7), { col: GSE_D, top: GSE_D, noEdge: true }));              // the hitch
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X - z(.15), s * hw * .25, z(1.2), [1, 0, .1], s), kitLamp('T', X + L * .2, s * (hw - z(.3)), z(1.5), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', X + L * .3, 0, z(2.9), [0, 0, 1], -1));
  return { L, W, top: z(2.85), wheels: [{ u: X + L * .3, r: wr, tw: z(.5), hw: hw - z(.25) }, { u: -X - L * .2, r: wf, tw: z(.3), hw: hw - z(.35) }], build, lamps, hw, nose: -X };
}
// the combine harvester (3.6 m wide): the body with the grain tank, the cab high in front, the header across the whole width, the auger
function combKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 3.6, z = m => m * pm, wr = z(.8), wb = z(.5), hd = -X - L * .14;
  const build = (col) => { const B = [];
    B.push(box(X + L * .04, hd - z(.6), -hw * .62, hw * .62, z(.7), z(3.0), { col, top: sh(col, .1), deco: (g, f, at0) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) { kq(g, at, .05, .95, .62, .66, GSE_Y); kq(g, at, .1, .35, .2, .5, 'rgba(0,0,0,.35)') } } }));
    B.push(box(X + L * .2, hd - z(1.6), -hw * .55, hw * .55, z(3.0), z(3.5), { col: sh(col, -.06), top: '#c2a24a' }));        // the grain tank's top (the grain)
    B.push(gseCab(hd - z(1.6), hd - z(.1), -hw * .5, hw * .3, z(2.4), z(3.85), col));
    B.push(box(hd, -X, -hw, hw, z(.25), z(1.05), { col: sh(col, -.18), top: sh(col, -.08), deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (f.n[0] > .5) { g.strokeStyle = 'rgba(20,20,20,.5)'; g.lineWidth = Math.max(.4, .3 * U); g.beginPath(); for (let s2 = .02; s2 < 1; s2 += .04) { const a = at(s2, .1), b = at(s2, .9); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke() } } }));   // the header
    B.push(box(hd - z(.6), hd, -hw * .35, hw * .35, z(.6), z(1.6), { col: sh(col, -.1), top: sh(col, -.02) }));                  // the feeder
    B.push(box(X + L * .15, hd - z(.4), hw * .62, hw * .62 + z(.3), z(3.2), z(3.5), { col: sh(col, -.05), top: sh(col, .08), noEdge: true }));   // the unloading auger, folded along the side
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', hd - z(.1), s * hw * .3, z(3.6), [1, 0, .1], s), kitLamp('T', X + L * .04, s * hw * .5, z(1.5), [-1, 0, .1], s));
  lamps.push(kitLamp('Y', hd - z(.9), 0, z(3.95), [0, 0, 1], -1));
  return { L, W, top: z(3.85), wheels: [{ u: hd - z(1.2), r: wr, tw: z(.6), hw: hw * .62 + z(.2) }, { u: X + L * .16, r: wb, tw: z(.4), hw: hw * .5 }], build, lamps, hw, nose: -X };
}
// the farm trailer (2.4 m wide): the bed with low sides, two axles, the drawbar to the tractor
function fwagKit(L, W) { const X = -L / 2, hw = W / 2, pm = W / 2.4, z = m => m * pm, wr = z(.45);
  const build = (col) => { const B = [], c2 = col || '#8a5a32';
    B.push(box(X + z(.1), -X - z(.5), -hw, hw, wr * 1.5, z(1.0), { col: GSE_D, top: '#6a4a2a' }));
    for (const sg of [-1, 1]) B.push(box(X + z(.1), -X - z(.5), sg * (hw - z(.05)) - z(.05), sg * (hw - z(.05)) + z(.05), z(1.0), z(1.6), { col: c2, top: sh(c2, .1), noEdge: true }));
    for (const u of [X + z(.1), -X - z(.6)]) B.push(box(u, u + z(.1), -hw, hw, z(1.0), z(1.6), { col: c2, top: sh(c2, .1), noEdge: true }));
    B.push(box(-X - z(.5), -X + z(.2), -z(.06), z(.06), z(.55), z(.68), { col: GSE_D, top: GSE_D, noEdge: true }));           // the drawbar
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('T', X + z(.1), s * (hw - z(.2)), z(.95), [-1, 0, .1], s));
  return { L, W, top: z(1.6), wheels: [{ u: X + L * .3, r: wr, tw: z(.3), hw: hw - z(.15) }, { u: X + L * .55, r: wr, tw: z(.3), hw: hw - z(.15) }], build, lamps, hw, nose: -X };
}
Object.assign(KIT_DEF, { btug: (L, W) => btugKit(L, W), ptug: (L, W) => ptugKit(L, W), belt: (L, W) => beltKit(L, W), cater: (L, W) => caterKit(L, W), gpu: (L, W, o) => gpuKit(L, W, o),
  hilo: (L, W) => hiloKit(L, W), stairs: (L, W, o) => stairsKit(L, W, o), bcart: (L, W) => bcartKit(L, W), ftrac: (L, W) => ftracKit(L, W), comb: (L, W) => combKit(L, W), fwag: (L, W) => fwagKit(L, W) });
// ---------- p398 · the rolling stock in 3/4 (the coordinator 18:2x: the trains and the ships at the real reference's size, D‑282) ----------
// Each car a kit of boxes from its reference (pm: px a metre = W ÷ the real width): the bogies and their wheels on the 1435 mm track,
// the body on them; the passenger cars with their window bands and doors, the locomotives with their cabs at both ends, the wagons
// with their loads (the containers of a Sgns as the game's own boxes, their pictures on top — opt.cargo, as the chassis of a port truck)
const RL_D = '#23272c', RL_M = '#3a4048', RL_G = '#8a929a';
function railWheels(X, L, hw, pm, bcs, ax, r) { const W = []; for (const c of bcs) for (const a of ax) W.push({ u: c + a, r, tw: .14 * pm, hw: .78 * pm }); return W }
function railBogies(B, bcs, len, hw, pm, z1) { for (const c of bcs) B.push(box(c - len / 2, c + len / 2, -.95 * pm, .95 * pm, .25 * pm, z1, { col: RL_D, top: RL_M })) }
// the passenger car: o.tag 'emu' (the commuter end car, its cab in front), 'dd' (the double-deck regional car), 'ic' / 'coach'; o.acc the band
function coachKit(L, W, o) {
  const X = -L / 2, hw = W / 2, ty = o.ty || o.tag || 'ic', acc = o.acc || '#1f7ac2', pm = W / (ty === 'dd' ? 2.8 : ty === 'emu' ? 2.82 : 2.83), z = m => m * pm, dd = ty === 'dd', cab = ty === 'emu';
  const zb = dd ? z(.75) : z(1.1), zt = dd ? z(4.6) : z(4.05), bc = L / 2 - z(dd ? 3.4 : 3.2), Ln = cab ? z(2.6) : 0;
  const build = (col) => { const B = [];
    railBogies(B, [-bc, bc], z(3.2), hw, pm, zb);
    B.push(box(X + z(.25), -X - z(.25) - Ln, -hw, hw, zb, zt, { col, top: sh(col, .06), ins: { f: 0, r: 0, s: z(.32) },
      deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U);
        if (Math.abs(f.n[1]) > .5) { // the sides: the skirt and the band, the windows (one row, two on the double-deck), the doors
          kq(g, at, 0, 1, 0, .09, sh(col, -.35)); kq(g, at, 0, 1, dd ? .5 : .4, dd ? .54 : .45, acc);
          const rows = dd ? [[.16, .4], [.6, .86]] : [[.52, .82]];
          for (const [t0, t1] of rows) { kq(g, at, .05, .95, t0, t1, glassGr(g, at, t0, t1), 'rgba(0,0,0,.4)', lw); g.fillStyle = sh(col, -.05); for (let s2 = .05 + .07; s2 < .94; s2 += .07) kq(g, at, s2 - .004, s2 + .004, t0, t1, sh(col, -.06)) }
          for (const s2 of dd ? [.27, .73] : [.035, .965]) { kq(g, at, s2 - .025, s2 + .025, .06, .92, sh(col, -.18), 'rgba(0,0,0,.45)', lw); kq(g, at, s2 - .018, s2 + .018, .55, .85, glassGr(g, at, .55, .85)) } }
        else if (Math.abs(f.n[0]) > .5) { kq(g, at, .3, .7, .05, .9, sh(col, -.25), 'rgba(0,0,0,.4)', lw) } } }));
    if (cab) { // the cab: the nose sloped back, the wide windscreen, the lamps
      B.push(box(-X - z(.25) - Ln, -X - z(.05), -hw, hw, zb, zt, { col, top: sh(col, .08), ins: { f: z(1.5), r: 0, s: z(.32) }, deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2);
        if (f.n[0] > .2) { kq(g, at, .08, .92, .5, .92, glassGr(g, at, .5, .92), 'rgba(0,0,0,.45)', Math.max(.35, .25 * U)); kq(g, at, 0, 1, .0, .14, acc); for (const s2 of [.06, .8]) kq(g, at, s2, s2 + .14, .24, .32, '#eef3f6') }
        else if (Math.abs(f.n[1]) > .5) { kq(g, at, 0, 1, dd ? .5 : .4, dd ? .54 : .45, acc); kq(g, at, .35, .85, .55, .82, glassGr(g, at, .55, .82)) } } }));
      for (const sg of [-1, 1]) B.push(box(-z(.7), z(.7), sg * z(.35) - z(.04), sg * z(.35) + z(.04), zt, zt + z(.55), { col: RL_D, top: RL_D, noEdge: true }));   // the pantograph
      B.push(box(-z(1.2), z(1.2), -z(.5), z(.5), zt + z(.55), zt + z(.62), { col: RL_G, top: '#b9c0c7', noEdge: true }) ) }
    else B.push(box(-L * .12, L * .12, -hw * .55, hw * .55, zt, zt + z(.28), { col: sh(col, -.08), top: sh(col, -.02) }));   // the air conditioner
    return { boxes: B } };
  const lamps = cab ? [-1, 1].map(s => kitLamp('H', -X, s * (hw - z(.5)), zb + z(.9), [1, 0, .1], s)) : [];
  return { L, W, top: zt + z(cab ? .62 : .28), wheels: railWheels(X, L, hw, pm, [-bc, bc], [-z(1.25), z(1.25)], z(.46)), build, lamps, hw, nose: -X };
}
// the locomotive: o.tag 'floco' (the diesel freight locomotive: the long hood, the cabs at both ends, the fans; three-axle bogies) or
// 'ploco' (the electric passenger locomotive: the sloped cabs, the pantographs; two-axle bogies); o.acc the stripe
function locoKit(L, W, o) {
  const X = -L / 2, hw = W / 2, fr = (o.ty || o.tag) === 'floco', acc = o.acc || '#2a2d30', pm = W / (fr ? 2.65 : 2.98), z = m => m * pm, zb = z(1.25), zt = z(fr ? 3.9 : 3.85), Lc = z(fr ? 2.2 : 2.4), bc = L / 2 - z(fr ? 4.3 : 3.6);
  const build = (col) => { const B = [];
    railBogies(B, [-bc, bc], z(fr ? 4.3 : 3.2), hw, pm, zb);
    B.push(box(X + z(.2) + Lc, -X - z(.2) - Lc, -hw, hw, zb, zt, { col, top: sh(col, .05), ins: { f: 0, r: 0, s: z(.25) }, topDraw: (g) => { g.fillStyle = sh(col, .05); g.fillRect(X + Lc, -hw, L - 2 * Lc, W); g.fillStyle = 'rgba(20,24,28,.55)'; if (fr) for (const f of [.3, .42, .54]) { g.beginPath(); g.arc(X + L * f, 0, z(.55), 0, 7); g.fill() } else for (const f of [.4, .6]) g.fillRect(X + L * f - z(.8), -z(.5), z(1.6), z(1)) },
      deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) { kq(g, at, 0, 1, 0, .14, acc); kq(g, at, 0, 1, .42, .48, acc); g.fillStyle = 'rgba(0,0,0,.28)'; for (let s2 = .1; s2 < .9; s2 += .1) kq(g, at, s2, s2 + .06, .6, .85, 'rgba(0,0,0,.22)') } } }));
    for (const sg of [-1, 1]) { const u0 = sg > 0 ? -X - z(.2) - Lc : X + z(.2), u1 = sg > 0 ? -X - z(.2) : X + z(.2) + Lc;   // the two cabs
      B.push(box(u0, u1, -hw, hw, zb, zt, { col, top: sh(col, .1), ins: sg > 0 ? { f: z(fr ? .5 : 1.1), r: 0, s: z(.25) } : { f: 0, r: z(fr ? .5 : 1.1), s: z(.25) },
        deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U);
          if (Math.abs(f.n[0]) > .2) { kq(g, at, 0, 1, 0, .22, acc); for (const s2 of [.06, .52]) kq(g, at, s2, s2 + .42, .56, .9, glassGr(g, at, .56, .9), 'rgba(0,0,0,.45)', lw); for (const s2 of [.08, .78]) kq(g, at, s2, s2 + .14, .3, .38, '#eef3f6') }
          else if (Math.abs(f.n[1]) > .5) { kq(g, at, 0, 1, 0, .14, acc); kq(g, at, .15, .75, .58, .88, glassGr(g, at, .58, .88), 'rgba(0,0,0,.4)', lw) } } })) }
    if (!fr) for (const u of [X + L * .28, -X - L * .28]) { for (const sg of [-1, 1]) B.push(box(u - z(.8), u + z(.8), sg * z(.3) - z(.04), sg * z(.3) + z(.04), zt, zt + z(.6), { col: RL_D, top: RL_D, noEdge: true })); B.push(box(u - z(1.1), u + z(1.1), -z(.55), z(.55), zt + z(.6), zt + z(.67), { col: RL_G, top: '#b9c0c7', noEdge: true })) }
    else B.push(box(X + L * .62, X + L * .66, -z(.25), z(.25), zt, zt + z(.45), { col: RL_D, top: '#15171b', noEdge: true }));   // the exhaust
    return { boxes: B } };
  const lamps = []; for (const s of [-1, 1]) lamps.push(kitLamp('H', -X, s * (hw - z(.45)), zb + z(.6), [1, 0, .1], s), kitLamp('T', X, s * (hw - z(.45)), zb + z(.6), [-1, 0, .1], s));
  return { L, W, top: zt + z(fr ? .45 : .67), wheels: railWheels(X, L, hw, pm, [-bc, bc], fr ? [-z(1.9), 0, z(1.9)] : [-z(1.3), z(1.3)], z(fr ? .53 : .625)), build, lamps, hw, nose: -X };
}
// the wagons: 'cw' the Sgns container flat (its containers: opt.cargo), 'box' the Hbbins covered wagon, 'tank' the tank wagon, 'flat' the
// Rgs flat wagon with its stanchions, 'hop' the Tadns hopper
function wagonKit(L, W, o) {
  const X = -L / 2, hw = W / 2, ty = o.ty || o.tag || 'box', acc = o.acc || '#d8b020', Wm = { cw: 2.6, box: 2.9, tank: 3.0, flat: 2.75, hop: 3.1 }[ty] || 2.9, pm = W / Wm, z = m => m * pm, bc = L / 2 - z(ty === 'hop' ? 2.4 : 2.7), zd = z(ty === 'flat' ? 1.3 : 1.2);
  const build = (col, opt) => { const B = [];
    railBogies(B, [-bc, bc], z(2.6), hw, pm, z(.95));
    for (const sg of [-1, 1]) B.push(box(X + z(.4), -X - z(.4), sg * (hw - z(.12)) - z(.12), sg * (hw - z(.12)) + z(.12), z(.85), zd, { col: ty === 'cw' || ty === 'flat' ? col : RL_D, top: RL_M }));   // the sills
    for (const u of [X + z(.2), -X - z(.6)]) B.push(box(u, u + z(.4), -hw, hw, z(.8), z(1.25), { col: RL_D, top: RL_M }));                                        // the headstocks, the buffers' beams
    if (ty === 'cw') { const cg = (opt && opt.cargo) || {}; for (const [j, c] of (cg.list || []).entries()) { const tex = c.tex, cc = c.col || '#8a6a4a', u0 = c.u0, u1 = c.u1, Hc = z(2.59);
        B.push(box(u0, u1, -z(1.22), z(1.22), zd, zd + Hc, { col: cc, topDraw: (g) => { if (tex && tex.cv && tex.sw) g.drawImage(tex.cv, tex.sx, tex.sy, tex.sw, tex.sh, u0, -z(1.22), u1 - u0, z(2.44)); else if (tex && tex.cv) g.drawImage(tex.cv, u0, -z(1.22), u1 - u0, z(2.44)); else { g.fillStyle = sh(cc, .1); g.fillRect(u0, -z(1.22), u1 - u0, z(2.44)) } },
          deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U); g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = lw; g.beginPath(); const st = Math.abs(f.n[1]) > .5 ? .03 : .2; for (let s2 = st; s2 < 1; s2 += st) { const a = at(s2, .04), b = at(s2, .96); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke(); kq(g, at, 0, 1, .96, 1, 'rgba(255,255,255,.15)') } })) } }
    else if (ty === 'box') B.push(box(X + z(.5), -X - z(.5), -hw, hw, zd, z(4.1), { col, top: sh(col, .06), ins: { f: 0, r: 0, s: z(.3) }, deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2), lw = Math.max(.35, .25 * U); if (Math.abs(f.n[1]) > .5) { g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = lw; g.beginPath(); for (let s2 = .25; s2 < 1; s2 += .25) { const a = at(s2, .02), b = at(s2, .98); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]) } g.stroke(); kq(g, at, .02, .98, .9, .95, sh(col, -.2)) } } }));
    else if (ty === 'tank') { B.push(box(X + z(.6), -X - z(.6), -z(.5), z(.5), z(1.4), z(1.65), { col: RL_D, top: RL_M })); B.push(box(-z(.5), z(.5), -z(.45), z(.45), z(4.0), z(4.35), { col: sh(col, -.05), top: sh(col, .1) })) }
    else if (ty === 'flat') { B.push(box(X + z(.3), -X - z(.3), -hw, hw, zd, zd + z(.12), { col: '#6a4a2a', top: '#7a5a3a', topDraw: (g) => { g.fillStyle = '#7a5a3a'; g.fillRect(X + z(.3), -hw, L - z(.6), W); g.fillStyle = 'rgba(0,0,0,.2)'; for (let u = X + z(.6); u < -X - z(.3); u += z(.6)) g.fillRect(u, -hw, z(.05), W) } }));
      for (let u = X + z(1.4); u < -X - z(1); u += z(2.6)) for (const sg of [-1, 1]) B.push(box(u - z(.06), u + z(.06), sg * (hw - z(.06)) - z(.05), sg * (hw - z(.06)) + z(.05), zd, zd + z(1.0), { col: RL_D, top: RL_D, noEdge: true })) }
    else if (ty === 'hop') { for (const f of [.2, .5, .8]) { const u = X + L * f; B.push(box(u - z(1.2), u + z(1.2), -hw * .6, hw * .6, z(.6), zd + z(.3), { col: RL_D, top: RL_M })) }
      B.push(box(X + z(.6), -X - z(.6), -hw, hw, zd, z(3.95), { col, top: sh(col, .06), ins: { f: z(.35), r: z(.35), s: z(.25) }, topDraw: (g) => { g.fillStyle = sh(col, .06); g.fillRect(X + z(.6), -hw, L - z(1.2), W); g.fillStyle = 'rgba(20,24,28,.55)'; g.fillRect(X + z(1.2), -z(.35), L - z(2.4), z(.7)) },
        deco: (g, f, at0, U) => { const fl = FLIP(f), at = (s2, t2) => at0(fl ? 1 - s2 : s2, t2); if (Math.abs(f.n[1]) > .5) { kq(g, at, .02, .98, .1, .14, sh(col, -.2)); for (let s2 = .1; s2 < .95; s2 += .12) kq(g, at, s2, s2 + .012, .05, .95, 'rgba(0,0,0,.2)') } } })) }
    return { boxes: B, cyls: ty === 'tank' ? [{ u0: X + z(.9), u1: -X - z(.9), r: z(1.45), z: z(2.65), col, bands: 3 }] : [] } };
  const top = ty === 'cw' ? zd + z(2.59) : ty === 'box' ? z(4.1) : ty === 'tank' ? z(4.35) : ty === 'hop' ? z(3.95) : zd + z(1.0);
  return { L, W, top, wheels: railWheels(X, L, hw, pm, [-bc, bc], [-z(.9), z(.9)], z(.46)), build, lamps: [], hw, nose: -X };
}
Object.assign(KIT_DEF, { coach: (L, W, o) => coachKit(L, W, o || {}), loco: (L, W, o) => locoKit(L, W, o || {}), wagon: (L, W, o) => wagonKit(L, W, o || {}) });
// the semi split into its two pictures: the tractor (the front 30 % of the footprint) and the trailer hung on the fifth wheel. uT — the
// tractor's centre, uK — the kingpin, both along the heading from the centre of the whole footprint; kR — the kingpin in the trailer's frame
const SEMIP = new Map();
C34.semiParts = function (L, W, chassis) {
  const mk = L.toFixed(2) + 'x' + W.toFixed(2) + (chassis ? 'c' : 't'); let S0 = SEMIP.get(mk); if (S0) return S0;
  const Lt = L * .3, uK = L / 2 - .73 * Lt, kf = Lt * .18, Ltr = uK + kf + L / 2;
  const S = { tractor: C34.kit('tractor', Lt, W, { full: L }), trailer: C34.kit(chassis ? 'chassis' : 'trailer', Ltr, W, { full: L }), uT: L / 2 - Lt / 2, uK, kR: Ltr / 2 - kf, Ltr, Lt };
  S.whole = C34.kit('semiw', L, W, { tag: chassis ? 'c' : 't', S });   // p380: the whole semi, straight — ONE picture (the parked ones, and on a straight road)
  SEMIP.set(mk, S); return S;
};
// a kit's solids moved along u by du (the top pictures drawn in the moved frame)
function shiftBox(e, du) { const o = Object.assign({}, e); o.base = e.base.map(q => [q[0] + du, q[1]]); if (e.topBase) o.topBase = e.topBase.map(q => [q[0] + du, q[1]]); o.c = [e.c[0] + du, e.c[1], e.c[2]];
  if (e.topDraw) { const f = e.topDraw; o.topDraw = (g, U) => { g.translate(du, 0); f(g, U) } } return o }
KIT_DEF.semiw = function (L, W, o) {
  const S = o.S, T = KITS.get(S.tractor), R = KITS.get(S.trailer), dT = S.uT, dR = S.uK - S.kR;
  const build = (col, opt) => { const a = T.build(col, {}), b = R.build(col, opt || {}); return { boxes: a.boxes.map(e => shiftBox(e, dT)).concat(b.boxes.map(e => shiftBox(e, dR))), cyls: [] } };
  const wheels = T.wheels.map(w => Object.assign({}, w, { u: w.u + dT })).concat(R.wheels.map(w => Object.assign({}, w, { u: w.u + dR })));
  const lamps = T.lamps.map(l => Object.assign({}, l, { u: l.u + dT })).concat(R.lamps.map(l => Object.assign({}, l, { u: l.u + dR })));
  return { L, W, top: Math.max(T.top, R.top), wheels, build, lamps, hw: W / 2, nose: L / 2 };
};
// one picture of a kit model (same projection, shadow and wheels as the cars; the boxes in depth order)
function renderKit(id, col, k, N, res, opt) {
  const KD = KITS.get(id); if (!KD) throw new Error('C34: unknown kit ' + id);
  const th = k / N * Math.PI * 2, cs = Math.cos(th), sn = Math.sin(th), K = K34, SUN = C34.SUN, built = KD.build(col, opt || {}), B = built.boxes, CY = built.cyls || [];
  const wx = (u, v) => u * cs - v * sn, wy = (u, v, z) => u * sn + v * cs - K * z;
  let x0b = 1e9, x1b = -1e9, y0b = 1e9, y1b = -1e9; const grow = (x, y) => { if (x < x0b) x0b = x; if (x > x1b) x1b = x; if (y < y0b) y0b = y; if (y > y1b) y1b = y };
  const pt = (u, v, z) => { grow(wx(u, v), wy(u, v, z)); grow(wx(u, v) + SUN.x * z, wy(u, v, 0) + SUN.y * z) };
  for (const b of B) for (const q of b.base) { pt(q[0], q[1], b.z1); pt(q[0], q[1], b.z0) }
  for (const c of CY) for (const u of [c.u0, c.u1]) for (const sg of [-1, 1]) { pt(u, sg * c.r, c.z + c.r); pt(u, sg * c.r, c.z - c.r) }
  for (const w of KD.wheels) for (const sg of [-1, 1]) { pt(w.u - w.r, sg * (w.hw + .5), 2 * w.r); pt(w.u + w.r, sg * (w.hw + .5), 0) }
  const mg = 1.4 + 2 / res; x0b -= mg; y0b -= mg; x1b += mg; y1b += mg;
  const ox = Math.ceil(-x0b * res), oy = Math.ceil(-y0b * res), cw = Math.ceil((x1b - x0b) * res) + 1, ch = Math.ceil((y1b - y0b) * res) + 1;
  const cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
  const g = cv.getContext('2d'); g.imageSmoothingEnabled = true; g.lineJoin = 'round'; g.lineCap = 'round';
  const Pj = p => [ox + res * wx(p[0], p[1]), oy + res * wy(p[0], p[1], p[2])], Pu = (u, v, z) => Pj([u, v, z]), U = res;
  const wn = n => [n[0] * cs - n[1] * sn, n[0] * sn + n[1] * cs, n[2]], vis = n => { const w = wn(n); return w[1] * K + w[2] }, lb = n => litK(norm3(wn(n)));
  const depth = p => (p[0] * sn + p[1] * cs) * K + p[2];
  // the shadow (half density, one path, soft)
  { const hw2 = Math.ceil(cw / 2) + 2, hh2 = Math.ceil(ch / 2) + 2; if (!SCR) SCR = document.createElement('canvas'); if (SCR.width < hw2 || SCR.height < hh2) { SCR.width = Math.max(SCR.width, hw2); SCR.height = Math.max(SCR.height, hh2) }
    const s = SCR.getContext('2d'); s.setTransform(1, 0, 0, 1, 0, 0); s.clearRect(0, 0, hw2 + 2, hh2 + 2); s.setTransform(.5, 0, 0, .5, 0, 0);
    const sp = (u, v, z) => [ox + res * (wx(u, v) + SUN.x * z), oy + res * (u * sn + v * cs + SUN.y * z)];
    s.beginPath(); const foot = []; for (const b of B) if (b.z1 - b.z0 > 1.5 || b.z1 > 6) foot.push(b); for (const c of CY) foot.push(box(c.u0, c.u1, -c.r, c.r, c.z - c.r, c.z + c.r));
    for (const b of foot) { const P = []; for (const q of b.base) { P.push(sp(q[0], q[1], 0)); P.push(sp(q[0], q[1], b.z1)) } const h = hull(P); s.moveTo(h[0][0], h[0][1]); for (const q of h) s.lineTo(q[0], q[1]); s.closePath() }
    s.fillStyle = 'rgba(0,0,0,.24)'; s.fill('nonzero');
    s.beginPath(); for (const w of KD.wheels) for (const sg of [-1, 1]) { const c0 = Pu(w.u, sg * (w.hw - w.tw / 2), 0); s.moveTo(c0[0] + w.r * U * 1.1, c0[1]); s.ellipse(c0[0], c0[1], w.r * U * 1.1, w.tw * U * .9, 0, 0, 7) } s.fillStyle = 'rgba(0,0,0,.25)'; s.fill();
    g.save(); try { g.filter = `blur(${(.75 * res).toFixed(2)}px)` } catch (e) { } g.drawImage(SCR, 0, 0, hw2, hh2, 0, 0, hw2 * 2, hh2 * 2); g.restore() }
  const sideV = sg => vis([0, sg, 0]), nearS = sideV(1) > .02 ? 1 : sideV(-1) > .02 ? -1 : 0;
  const wheel = (w, sg) => { const vo = sg * (w.hw + .3), vi = sg * (w.hw + .3 - w.tw), n = 22, Aa = [], Bb = [];
    const cl = sg === nearS && w.zcl != null && w.zcl < 2 * w.r - .2; if (cl) { const Q = []; for (const u of [w.u - w.r - 1, w.u + w.r + 1]) for (const v of [vo + sg, vi - sg]) for (const z of [-1, w.zcl]) Q.push(Pu(u, v, z)); g.save(); poly(g, hull(Q)); g.clip() }
    for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, u = w.u + Math.cos(a) * w.r, z = w.r + Math.sin(a) * w.r; Aa.push(Pu(u, vo, z)); Bb.push(Pu(u, vi, z)) }
    g.fillStyle = '#16191d'; poly(g, hull(Aa.concat(Bb))); g.fill();
    if (vis([0, sg, 0]) > .02) { const c0 = Pu(w.u, vo, w.r), cx = Pu(w.u + w.r, vo, w.r), cz = Pu(w.u, vo, 2 * w.r); g.save(); g.setTransform(cx[0] - c0[0], cx[1] - c0[1], cz[0] - c0[0], cz[1] - c0[1], c0[0], c0[1]);
      g.fillStyle = '#1d2025'; g.beginPath(); g.arc(0, 0, 1, 0, 7); g.fill(); drawRim(g, 4, .6); const gr = g.createLinearGradient(0, 1, 0, -.2); gr.addColorStop(0, 'rgba(0,0,0,.5)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.beginPath(); g.arc(0, 0, 1.01, 0, 7); g.fill(); g.restore() }
    if (cl) g.restore() };
  for (const w of KD.wheels) for (const sg of [1, -1]) if (sg !== nearS) wheel(w, sg);
  // the solids in depth order; the near wheels go in at the depth of their outer face
  const items = B.map(b => ({ d: depth(b.c), f: () => drawPrism(g, b, Pj, vis, lb, null, U) }));
  for (const c of CY) items.push({ d: depth([(c.u0 + c.u1) / 2, 0, c.z]), f: () => drawCyl(g, c, Pj, vis, lb, U, wx, wy, res) });
  items.sort((a, b) => a.d - b.d); for (const it of items) it.f();
  if (nearS) for (const w of KD.wheels) wheel(w, nearS);   // the near wheels in front of the body (in their arches), under a skirt clipped
  return { cv, ox, oy, k, N, res };
}
// a horizontal tank along u: the silhouette of the two end circles, shaded across, the end cap that faces the viewer, the bands
function drawCyl(g, c, Pj, vis, lb, U) {
  const ring = (u, n) => { const P = []; for (let i = 0; i < (n || 28); i++) { const a = i / (n || 28) * Math.PI * 2; P.push([u, Math.cos(a) * c.r, c.z + Math.sin(a) * c.r]) } return P };
  const A0 = ring(c.u0), A1 = ring(c.u1), S = hull(A0.concat(A1).map(Pj)); let y0 = 1e9, y1 = -1e9; for (const q of S) { y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]) }
  const top = Pj([(c.u0 + c.u1) / 2, 0, c.z + c.r]), bot = Pj([(c.u0 + c.u1) / 2, 0, c.z - c.r]), gr = g.createLinearGradient(top[0], top[1] - 2, bot[0], bot[1]);
  gr.addColorStop(0, sh(c.col, .25)); gr.addColorStop(.35, c.col); gr.addColorStop(1, sh(c.col, -.35)); g.fillStyle = gr; poly(g, S); g.fill(); g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.4, .3 * U); g.stroke();
  g.strokeStyle = 'rgba(0,0,0,.18)'; for (let i = 1; i < (c.bands || 0) + 1; i++) { const u = c.u0 + (c.u1 - c.u0) * i / ((c.bands || 0) + 1); g.beginPath(); let on = false; for (let k2 = 0; k2 <= 40; k2++) { const a = k2 / 40 * Math.PI * 2, n = [0, Math.cos(a), Math.sin(a)]; if (vis(n) > 0) { const q = Pj([u, n[1] * c.r, c.z + n[2] * c.r]); if (on) g.lineTo(q[0], q[1]); else { g.moveTo(q[0], q[1]); on = true } } else on = false } g.stroke() }
  for (const [u, n] of [[c.u0, [-1, 0, 0]], [c.u1, [1, 0, 0]]]) if (vis(n) > .02) { g.fillStyle = litC(c.col, lb(n) * .92); const R = ring(u).map(Pj); poly(g, R); g.fill(); g.stroke() }
  const T = Pj([c.u0 + (c.u1 - c.u0) * .3, 0, c.z + c.r]), T2 = Pj([c.u0 + (c.u1 - c.u0) * .7, 0, c.z + c.r]); g.fillStyle = '#8a9096'; for (const q of [T, T2]) { g.beginPath(); g.ellipse(q[0], q[1], 2.2 * U, 1.4 * U, 0, 0, 7); g.fill() }
}

// ---------- the cache and the API ----------
// p378: one picture per model × paint × rim × roof rack × cargo × direction × density.  Kit models (the heavy vehicles) are ids 'K/…'
// made by C34.kit(); `opt` = { rim, v, cargo: { key, tex, col } } (cargo — the container on a chassis).
const CACHE = new Map(); let CBYTES = 0, MADE = 0, MADE_MS = 0, HITS = 0, EVICT = 0;
const optKey = o => o ? ((o.rim != null ? o.rim : '') + '|' + (o.v ? 1 : 0) + '|' + (o.cargo ? o.cargo.key : '')) : '||';
const isKit = id => id.charCodeAt(0) === 75 && id.charCodeAt(1) === 47;   // 'K/'
function make(id, c, k, N, r, opt) { return isKit(id) ? renderKit(id, c, k, N, r, opt) : render(id, c, k, N, r, opt) }
// C34.sprite(id, colorHex, heading, res[, dirs[, opt]]) → {cv, ox, oy}: the picture turned to the nearest of `dirs` directions (heading in
// radians, 0 = east, clockwise on the screen — the game's ctx.rotate(heading)); (ox, oy) — the ground centre inside cv (device px).
// Draw it unrotated: ctx.drawImage(cv, x − ox/res, y − oy/res, cv.width/res, cv.height/res).
C34.sprite = function (id, col, heading, res, dirs, opt) {
  const N = dirs || C34.dirs, r = res || 1, k = ((Math.round(heading / (Math.PI * 2) * N) % N) + N) % N, c = (col || '#f4f6f8').toLowerCase();
  const key = id + '|' + c + '|' + optKey(opt) + '|' + N + '|' + k + '|' + r; let e = CACHE.get(key);
  if (e) { if (++HITS % 8 === 0) { CACHE.delete(key); CACHE.set(key, e) } return e }   // least recently used goes first (refreshed every 8th hit: cheap)
  const t0 = performance.now(); e = make(id, c, k, N, r, opt); MADE_MS += performance.now() - t0; MADE++;
  CACHE.set(key, e); CBYTES += e.cv.width * e.cv.height * 4; evict(key);
  return e;
};
// p380 · the owner 02:18 (4): when the cache is full, the pictures at a density other than the current one (C34.curRes — a zoom that
// is gone) go first, the least recently used of them; then the least recently used of all
function evict(keep) { if (!(C34.budgetMB > 0) || CBYTES <= C34.budgetMB * 1048576) return; const lim = C34.budgetMB * 1048576, cur = C34.curRes;
  if (cur != null) for (const [k0, e0] of CACHE) { if (CBYTES <= lim) break; if (k0 === keep || e0.res === cur) continue; CACHE.delete(k0); CBYTES -= e0.cv.width * e0.cv.height * 4; EVICT++; EVICT_OTHER++ }
  while (CBYTES > lim && CACHE.size > 1) { const [k0, e0] = CACHE.entries().next().value; if (k0 === keep) break; CACHE.delete(k0); CBYTES -= e0.cv.width * e0.cv.height * 4; EVICT++ } }
C34.curRes = null; let EVICT_OTHER = 0;
C34.budgetMB = 0;   // 0 = keep everything; e.g. 64 → the least recently used pictures are dropped above 64 MB
// for the game loop: peek() never draws — it returns the picture if it is made, else the nearest made direction of the same vehicle
// (or null) and queues the missing one; pump(ms) makes queued pictures until the time budget of this frame is spent
// p389: two queues — the pictures of the vehicles on the screen (QUEUE) and those of the ring around it (QPRE, made only with what is
// left); every request carries the game's frame (C34.frame) and is renewed while it is asked; one not renewed for C34.fresh frames
// (a vehicle no longer on the screen, the zone just left) is dropped — asked again if it comes back
const QUEUE = [], QPRE = [], QSET = new Map(), RESL = [1, 1.5, 2, 3];   // p380: four densities (were nine: a zoom made a whole new set)
C34.RESL = RESL; C34.frame = 0; C34.fresh = 0; C34.preFresh = 90; let STALE = 0, PRE_MADE = 0;
C34.peek = function (id, col, heading, res, dirs, opt, pre) {
  const N = dirs || C34.dirs, r = res || 1, c = (col || '#f4f6f8').toLowerCase(), k = ((Math.round(heading / (Math.PI * 2) * N) % N) + N) % N, base = id + '|' + c + '|' + optKey(opt) + '|' + N + '|';
  const key = base + k + '|' + r; let e = CACHE.get(key); if (e) { if (++HITS % 8 === 0) { CACHE.delete(key); CACHE.set(key, e) } return e }
  const q0 = QSET.get(key);
  if (!q0) { const q = [id, c, k, N, r, key, opt, C34.frame, !!pre]; QSET.set(key, q); (pre ? QPRE : QUEUE).push(q) }
  else { q0[7] = C34.frame; if (q0[8] && !pre) { q0[8] = false; QUEUE.push(q0) } }   // p389: renewed; a ring picture now on the screen — to the front queue
  if (pre) return null;
  for (const rr of RESL) if (rr !== r) { e = CACHE.get(base + k + '|' + rr); if (e) return e }   // the same direction at another density (a zoom just changed)
  for (let d = 1; d <= 3; d++) { e = CACHE.get(base + ((k + d) % N) + '|' + r) || CACHE.get(base + ((k - d + N) % N) + '|' + r); if (e) return e }   // a neighbour direction (up to 67.5°), else today's drawing
  return null;
};
function qTake(Q, fresh, pre) { while (Q.length) { const q = Q.shift(); if (pre && !q[8]) continue; if (QSET.get(q[5]) !== q) continue; QSET.delete(q[5]);
    if (CACHE.has(q[5])) continue; if (fresh > 0 && C34.frame - q[7] > fresh) { STALE++; continue } return q } return null }
function qMake(q) { try { C34.sprite(q[0], q[1], q[2] / q[3] * Math.PI * 2, q[4], q[3], q[6]) } catch (e) { C34.lastErr = q[0] + ': ' + (e && e.message || e) } }
// pump(ms [, preMs]): the front queue within ms (at least one picture when ms > 0), then — only if it is empty — the ring within preMs
C34.pump = function (ms, preMs) { const t0 = performance.now(); let n = 0, full = false;
  while (true) { if (performance.now() - t0 >= (ms == null ? 2 : ms)) { full = QUEUE.length > 0; break } const q = qTake(QUEUE, C34.fresh, false); if (!q) break; qMake(q); n++ }
  if (!full && preMs > 0) { const t1 = performance.now(); while (performance.now() - t1 < preMs) { const q = qTake(QPRE, C34.preFresh, true); if (!q) break; qMake(q); n++; PRE_MADE++ } }
  return n };
C34.queued = () => QUEUE.length;
C34.preQueued = () => QPRE.length;
C34.dirIndex = (heading, dirs) => { const N = dirs || C34.dirs; return ((Math.round(heading / (Math.PI * 2) * N) % N) + N) % N };
C34.stats = function () { let tb = 0; for (const t of TEX.values()) tb += t.bytes; return { sprites: CACHE.size, bytes: CBYTES, MB: +(CBYTES / 1048576).toFixed(2), textures: TEX.size, textureMB: +(tb / 1048576).toFixed(2), made: MADE, makeMs: +MADE_MS.toFixed(1), makeAvgMs: MADE ? +(MADE_MS / MADE).toFixed(2) : 0, evicted: EVICT, evictedOtherRes: EVICT_OTHER, queued: QUEUE.length, preQueued: QPRE.length, preMade: PRE_MADE, stale: STALE, budgetMB: C34.budgetMB, curRes: C34.curRes, lastErr: C34.lastErr || null } };
C34.clear = function () { CACHE.clear(); TEX.clear(); CBYTES = 0; MADE = 0; MADE_MS = 0; QUEUE.length = 0; QPRE.length = 0; QSET.clear() };
C34.dropTextures = function () { TEX.clear() };
let VMIX = null; const vmRow = id => { if (!VMIX) { VMIX = new Map(); for (const m of VM) if (!VMIX.has(m[0])) VMIX.set(m[0], m) } return VMIX.get(id) };
C34.rimFor = (id, r) => { if (isKit(id) || !(r >= 0)) return -1; const m = vmRow(id), L = m && m[9] || [0]; return L.includes(r) ? r : L[r % L.length] };
C34.has = id => isKit(id) ? KITS.has(id) : !!vmRow(id);
// the height of the top of a model (world px) — the line number disc of a bus, a pallet on a truck sit there
C34.top = function (id) { if (isKit(id)) { const k = KITS.get(id); return k ? k.top : 0 } const M = geo(id); return (M.ty == 'truck' && M.eq != 'tow' ? M.A(M.h.box || 30) : M.zR) * M.sc };

// ---------- the turning wheels (p378, the owner 28.10 23:12: "the wheels do not turn while driving") ----------
// The top-down painter never turned them (from above only the tread edge shows, the same stripes in every frame). In 3/4 the outer face of
// each near-side wheel is in the picture; per frame it is laid again over the picture, turned by the distance the vehicle went (the angle
// = −distance / radius: the top of the wheel moves forward): ONE drawImage of a small picture of that rim + one of the fender shade, in the
// plane of the wheel (the same affine frame the picture used). C34.wheelsAt — the frames of the near wheels, once per model × direction.
const WHL = new Map();
C34.wheelsAt = function (id, k, N) {
  N = N || C34.dirs; const key = id + '|' + N + '|' + k; let R = WHL.get(key); if (R) return R; R = [];
  const th = k / N * Math.PI * 2, cs = Math.cos(th), sn = Math.sin(th), K = K34;
  const add = (u, v, r, sc, s, zcl, kit) => { const c0 = [sc * (u * cs - v * sn), sc * (u * sn + v * cs - K * r)];
    R.push({ cx: c0[0], cy: c0[1], ax: sc * r * cs, ay: sc * r * sn, bx: 0, by: -K * sc * r, r: r * sc, s, zcl: zcl != null && zcl < 2 * r - .2 ? (zcl - r) / r : null, kit }) };
  if (isKit(id)) { const KD = KITS.get(id); if (KD) { const nearS = cs * K > .02 ? 1 : cs * K < -.02 ? -1 : 0; if (nearS) for (const w of KD.wheels) add(w.u, nearS * (w.hw + .3), w.r, 1, nearS, w.zcl, true) } }
  else { const M = geo(id); for (const w of M.wheels) if (w.s * cs * K > .02) add(w.u, w.vo, w.r, M.sc, w.s, null, false) }
  if (WHL.size > 6000) WHL.clear(); WHL.set(key, R); return R;
};
// p380 (the draw-call budget): the rim and the fender shade of each turn step are ONE small picture (24 steps of 15°, made on demand)
const WSTEPS = 24, RIMS_SP = {};
function rimSprite(style, kit, step) { const key = (kit ? 'k' : 'c') + style + '|' + step; let cv = RIMS_SP[key]; if (cv) return cv; cv = RIMS_SP[key] = document.createElement('canvas'); cv.width = cv.height = 64; const g = cv.getContext('2d');
  g.setTransform(30, 0, 0, 30, 32, 32); g.rotate(step / WSTEPS * Math.PI * 2); g.fillStyle = '#1d2025'; g.beginPath(); g.arc(0, 0, 1, 0, 7); g.fill();
  if (!kit) { g.strokeStyle = 'rgba(255,255,255,.07)'; g.lineWidth = .06; g.beginPath(); g.arc(0, 0, .9, 0, 7); g.stroke() }
  drawRim(g, style, kit ? .6 : .64);
  g.setTransform(30, 0, 0, 30, 32, 32); const gr = g.createLinearGradient(0, 1, 0, -.2); gr.addColorStop(0, kit ? 'rgba(0,0,0,.5)' : 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.beginPath(); g.arc(0, 0, 1.01, 0, 7); g.fill();
  return cv }
// dist — the distance the vehicle went (world px, forward +); rim — the rim style of the picture (the kits: steel); q — the picture's size factor.
// One drawImage per near wheel.
C34.wheels = function (ctx, id, x, y, k, N, dist, rim, q) {
  const R = C34.wheelsAt(id, k, N); if (!R.length) return 0; q = q || 1; let n = 0;
  for (const w of R) { const a = -dist / w.r, st = ((Math.round(a / (Math.PI * 2) * WSTEPS) % WSTEPS) + WSTEPS) % WSTEPS, sp = rimSprite(w.kit ? 4 : (rim != null && rim >= 0 ? rim : geo(id).rim), w.kit, st);
    ctx.save(); ctx.transform(w.ax * q, w.ay * q, w.bx * q, w.by * q, x + w.cx * q, y + w.cy * q);
    if (w.zcl != null) { ctx.beginPath(); ctx.rect(-1.2, -1.2, 2.4, 1.2 + w.zcl); ctx.clip() }
    ctx.drawImage(sp, -32 / 30, -32 / 30, 64 / 30, 64 / 30); ctx.restore(); n++ }
  return n;
};
// ---------- the lamps (p378) ----------
// Every model knows where its lamps are: the headlamps and the tail lamps of veh() (the same design sheet: hl / tl and the outline), the
// amber signals at the corners, the reverse lamps, the light bar on the roof.  They are points on the 3/4 body (u, v, z, the outward
// normal); for each of the 16 directions they are projected once (C34.lampsAt) and lit per frame over the cached picture (C34.lights):
// a few drawImage of a soft glow, nothing when every lamp is off.
const LAMPS = new Map(), LAMPP = new Map();
function surfZ(M, u, d) { const dc = M.dC ? M.dC(u) : 2; return lerp(M.zB(u), M.zcap(u), Math.max(0, Math.min(1, d / Math.max(.5, dc)))) }
function carLamps(M) {
  const G2 = M.Gg, W = M.W, D = M.D, A = M.A, L = [], HI = Math.min(4.6, Math.max(2.2, G2.zf * .45));
  const hy = { slim: .27, rect: .3, wrap: .3, split: .29, bar: .3, round: .31, quad: .29 }[D.hl] || .3, ty = { bar: .34, L: .35, vert: .39, round: .3 }[D.tl] || .35;
  const at = (front, yv, d) => { const q = vdAt(G2, front, yv, d); return [q[0], q[1], surfZ(M, q[0], d)] };
  const truckTail = M.ty == 'truck';
  for (const s of [-1, 1]) {
    const h = at(true, W * hy, HI * .42), t = at(false, W * ty, 1.3), fi = at(true, W * .44, 1.0), ri = at(false, W * .27, .9), rv = at(false, W * .41, .9);
    if (truckTail) for (const q of [t, ri, rv]) { q[0] = M.X + .5; q[2] = Math.min(q[2], M.zBelt - A(3.4)) }
    L.push({ t: 'H', u: h[0], v: s * h[1], z: h[2], n: [1, s * .3, .32], s });
    L.push({ t: 'T', u: t[0], v: s * t[1], z: t[2], n: [-1, s * .3, .3], s });
    L.push({ t: 'I', u: fi[0], v: s * fi[1], z: fi[2], n: [.8, s * .6, .3], s, f: 1 });
    L.push({ t: 'I', u: ri[0], v: s * ri[1], z: ri[2], n: [-.8, s * .6, .3], s, f: 0 });
    L.push({ t: 'R', u: rv[0], v: s * rv[1], z: rv[2], n: [-1, s * .3, .3], s });
  }
  if (M.eq == 'taxi') L.push({ t: 'S', u: (M.x0 + M.x1) / 2, v: 0, z: M.zR + A(1), n: [0, 0, 1], s: 0 });
  const b = barGeo(M); if (b) for (const s of [-1, 1]) L.push({ t: b.kind == 'amber' ? 'Y' : 'E', u: b.u, v: s * b.hw * .55, z: (b.z1 + b.z2) / 2, n: [0, 0, 1], s, col: s < 0 ? b.a : b.b });
  return { list: L, sc: M.sc, nose: M.L / 2, hw: M.H, lenW: M.L * M.sc };
}
function lampDef(id) { let d = LAMPS.get(id); if (d) return d; if (isKit(id)) { const k = KITS.get(id); d = k ? k.lampDef : { list: [], sc: 1, nose: 0, hw: 0 } } else d = carLamps(geo(id)); LAMPS.set(id, d); return d }
// the lamps of one direction: world offsets from the ground centre (x, y), the visibility (0 … 1) of each
C34.lampsAt = function (id, k, N) {
  N = N || C34.dirs; const key = id + '|' + N + '|' + k; let P = LAMPP.get(key); if (P) return P;
  const d = lampDef(id), th = k / N * Math.PI * 2, cs = Math.cos(th), sn = Math.sin(th), sc = d.sc;
  P = d.list.map(l => { const nw = [l.n[0] * cs - l.n[1] * sn, l.n[0] * sn + l.n[1] * cs, l.n[2]], nn = Math.hypot(nw[0], nw[1], nw[2]) || 1, vv = (nw[1] * K34 + nw[2]) / nn;
    return { t: l.t, s: l.s, f: l.f, col: l.col, x: sc * (l.u * cs - l.v * sn), y: sc * (l.u * sn + l.v * cs - K34 * l.z), vis: l.t == 'E' || l.t == 'Y' ? 1 : Math.max(0, Math.min(1, (vv + .12) / .42)) } });
  P.nose = d.nose * sc; P.hw = d.hw * sc; P.head = d.list.some(l => l.t === 'H'); if (LAMPP.size > 6000) LAMPP.clear(); LAMPP.set(key, P); return P;
};
// the glows: soft discs made once (a hot middle, a wide halo); the beam: a cone on the road ahead
const GLOW = {}; let BEAM = null;
// two kinds: hot (night — a white-hot middle, laid with 'lighter') and lit (day — the lens colour itself, laid normally)
function glow(c, day) { const key = c + (day ? 'd' : 'n'); let cv = GLOW[key]; if (cv) return cv; cv = GLOW[key] = document.createElement('canvas'); cv.width = cv.height = 64; const g = cv.getContext('2d'), rgb = hexRGB(c), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  if (day) { const hi = rgb.map(v => Math.min(255, v * .82 + 60)); gr.addColorStop(0, rgbS(hi, 1)); gr.addColorStop(.22, rgbS(rgb, 1)); gr.addColorStop(.36, rgbS(rgb, .5)); gr.addColorStop(.6, rgbS(rgb, .12)); gr.addColorStop(1, rgbS(rgb, 0)) }
  else { gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.12, rgbS(rgb.map(v => Math.min(255, v * .5 + 140)), 1)); gr.addColorStop(.32, rgbS(rgb, .55)); gr.addColorStop(.62, rgbS(rgb, .16)); gr.addColorStop(1, rgbS(rgb, 0)) }
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return cv }
function beam() { if (BEAM) return BEAM; const cv = BEAM = document.createElement('canvas'); cv.width = 160; cv.height = 96; const g = cv.getContext('2d');
  // a cone from the left middle, widening to the right; brightest near the lamps, fading with the distance and to the edges
  for (let i = 0; i < 40; i++) { const t = i / 39, w = 8 + t * 40, a = .5 * Math.pow(1 - t, 1.5) * (t < .08 ? t / .08 : 1); const gr = g.createLinearGradient(0, 48 - w, 0, 48 + w);
    gr.addColorStop(0, 'rgba(255,244,214,0)'); gr.addColorStop(.5, `rgba(255,244,214,${a.toFixed(3)})`); gr.addColorStop(1, 'rgba(255,244,214,0)'); g.fillStyle = gr; g.fillRect(t * 156, 48 - w, 4.2, 2 * w) }
  return cv }
const LC = { H: '#fff1cc', T: '#ff2a1f', B: '#ff1a10', I: '#ffa316', R: '#f4f6ff' };
// st: { head 0…1 (the headlamps and the tail lamps on — night / winter), beam 0…1, brake, rev, ind −1 left / 1 right / 2 both (hazard), on
// (the blink phase), bar (the roof lights flash), t (ms) }.  ctx in world coordinates; (x, y) the ground centre; k the direction of the picture.
// p380 (the draw-call budget): ALL the lamps of a vehicle are ONE drawImage — an overlay made once per (model, direction, lamp state, size,
// density) from the same glows, kept in a small LRU (C34.lightMB). A blink or a flash only changes the state (another overlay, one call).
const LOV = new Map(); let LOVB = 0, LOV_MADE = 0;
C34.lightMB = 8;
function lampMask(st) {
  const head = st.head || 0, hq = Math.round(Math.min(1, head) * 4), bq = st.beam > .02 && hq ? Math.round(Math.min(1, st.beam) * 4) : 0;
  const ind = st.ind && st.on ? (st.ind === 2 ? 3 : st.ind > 0 ? 1 : 2) : 0;
  let em = 0, am = 0; if (st.bar) { const e = Math.floor((st.t || 0) / 110) % 8; em = e === 0 || e === 2 ? 1 : e === 4 || e === 6 ? 2 : 0; am = Math.floor((st.t || 0) / 260) % 2 ? 2 : 1 }
  if (!hq && !st.brake && !st.rev && !ind && !em && !am) return null;
  return { hq, bq, b: st.brake ? 1 : 0, r: st.rev ? 1 : 0, ind, em, am, key: '' + hq + bq + (st.brake ? 1 : 0) + (st.rev ? 1 : 0) + ind + em + am };
}
function lightOverlay(id, k, N, q, res, M) {
  const key = id + '|' + N + '|' + k + '|' + q.toFixed(3) + '|' + res + '|' + M.key; let o = LOV.get(key);
  if (o) { LOV.delete(key); LOV.set(key, o); return o }
  const P = C34.lampsAt(id, k, N), head = M.hq / 4, beamA = M.bq / 4, day = head < .3, D = [];
  const dot = (l, c, r, a) => { if (a > .01) D.push([l.x * q, l.y * q, c, r * (day ? .62 : 1), Math.min(1, a)]) };
  for (const l of P) {
    if (l.t === 'H') { if (head > .02) dot(l, LC.H, 3.2 + 3.5 * head, (.35 + .65 * head) * l.vis) }
    else if (l.t === 'T') { if (M.b) dot(l, LC.B, 4.6, .95 * l.vis + .12); else if (head > .02) dot(l, LC.T, 2.6 + 1.6 * head, (.3 + .45 * head) * l.vis) }
    else if (l.t === 'R') { if (M.r) dot(l, LC.R, 3.4, .9 * l.vis + .1) }
    else if (l.t === 'I') { const si = M.ind === 3 ? 2 : M.ind === 1 ? 1 : M.ind === 2 ? -1 : 0; if (si && (si === 2 || si === l.s)) dot(l, LC.I, 3.6, .95 * Math.max(l.vis, .35)) }
    else if (l.t === 'E') { if (M.em && (l.s < 0 ? M.em === 1 : M.em === 2)) { dot(l, l.col, 5.2, 1); dot(l, l.col, 15, .32) } }
    else if (l.t === 'W') { if (head > .02) dot(l, '#ffe7b0', 8, .3 * head * l.vis) }
    else if (l.t === 'S') { if (head > .02) dot(l, '#ffe9a8', 5 + 2 * head, .55 * head) }
    else if (l.t === 'Y') { if (M.am && (M.am === 1) === (l.s < 0)) { dot(l, '#ffb000', 4.6, 1); dot(l, '#ffb000', 12, .25) } }
  }
  const th = k / N * Math.PI * 2, bm = beamA > .02 && head > .02 && P.head ? { a: Math.min(1, beamA) * .55, x: P.nose * q * .82, bl: Math.max(46, P.nose * 3.2), bw: Math.max(26, P.hw * 3.4) } : null;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const grow = (x, y) => { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y };
  for (const d of D) { grow(d[0] - d[3], d[1] - d[3]); grow(d[0] + d[3], d[1] + d[3]) }
  if (bm) { const cs = Math.cos(th), sn = Math.sin(th); for (const [u, v] of [[bm.x, -bm.bw / 2], [bm.x, bm.bw / 2], [bm.x + bm.bl, -bm.bw / 2], [bm.x + bm.bl, bm.bw / 2]]) grow(u * cs - v * sn, u * sn + v * cs) }
  if (x0 > x1) { o = { cv: null, x0: 0, y0: 0, w: 0, h: 0, add: !day, bytes: 0 } }
  else {
    x0 = Math.floor(x0 - 1); y0 = Math.floor(y0 - 1); const cw = Math.max(1, Math.ceil((x1 + 1 - x0) * res)), ch = Math.max(1, Math.ceil((y1 + 1 - y0) * res));
    const cv = document.createElement('canvas'); cv.width = cw; cv.height = ch; const g = cv.getContext('2d'); g.setTransform(res, 0, 0, res, -x0 * res, -y0 * res);
    g.globalCompositeOperation = day ? 'source-over' : 'lighter';
    if (bm) { g.save(); g.globalAlpha = bm.a; g.rotate(th); g.drawImage(beam(), bm.x, -bm.bw / 2, bm.bl, bm.bw); g.restore() }
    for (const d of D) { g.globalAlpha = d[4]; g.drawImage(glow(d[2], day), d[0] - d[3], d[1] - d[3], 2 * d[3], 2 * d[3]) }
    o = { cv, x0, y0, w: cw / res, h: ch / res, add: !day, bytes: cw * ch * 4 }; LOV_MADE++
  }
  LOV.set(key, o); LOVB += o.bytes;
  while (LOVB > C34.lightMB * 1048576 && LOV.size > 1) { const [k0, e0] = LOV.entries().next().value; LOV.delete(k0); LOVB -= e0.bytes }
  return o;
}
// draw: one drawImage (none when every lamp is off, or the overlay is off the view — vis(x0, y0, w, h) in world units, optional)
C34.lights = function (ctx, id, x, y, k, st, N, q, res, vis) {
  if (!st) return 0; const M = lampMask(st); if (!M) return 0;
  const o = lightOverlay(id, k, N || C34.dirs, q || 1, Math.min(2, res || 1), M); if (!o.cv) return 0;   // soft glows: at most 2 px per world px
  if (vis && !vis(x + o.x0, y + o.y0, o.w, o.h)) return 0;
  if (o.add) { const g0 = ctx.globalCompositeOperation; ctx.globalCompositeOperation = 'lighter'; ctx.drawImage(o.cv, x + o.x0, y + o.y0, o.w, o.h); ctx.globalCompositeOperation = g0 }
  else ctx.drawImage(o.cv, x + o.x0, y + o.y0, o.w, o.h);
  return 1;
};
C34.lightStats = () => ({ overlays: LOV.size, MB: +(LOVB / 1048576).toFixed(2), made: LOV_MADE });

// today's top-down look (the game's painter as is) — for the review page only
C34.topdown = function (ctx, id, col, x, y, heading) {
  const M = geo(id), mc = M.m.slice(); Object.assign(mc, M.m); const pi = PAL.findIndex(p => p[1].toLowerCase() === String(col).toLowerCase()); if (!M.m.fix && pi < 0) mc.fix = col;
  ctx.save(); ctx.translate(x, y); ctx.rotate(heading); ctx.scale(M.sc, M.sc); ctx.translate(-(M.L + 20) / 2, -(M.W + 20) / 2);
  veh(ctx, mc, { v: 0, c: Math.max(0, pi), r: 0, d: 0, f: 0, L: { beam: false } }, 0); ctx.restore();
};

})(window);

return true}

c34LibInit();
const C=window.C34,id=C.kit('bus',120,25.5),D=C.kitInfo(id);
const linePaint={1:4,2:6,3:9};
const lineColor=n=>C.PAL[linePaint[n]??linePaint[3]][1];
const safeClone=v=>JSON.parse(JSON.stringify(v));
const info={source:'Turbo City S7F282 · original c34LibInit, unchanged',id,
 len:D.L,width:D.W,top:D.top,projectionK:C.K,
 wheels:safeClone(D.wheels),lamps:safeClone(D.lamps),
 axlePositions:D.wheels.map(w=>w.u),wheelRadius:D.wheels[0].r,
 halfWidth:D.hw,viewBox:[-85,-90,170,170],directions:16,
 basePaintByLine:{1:lineColor(1),2:lineColor(2),3:lineColor(3)},
 nominalBody:{length:120,width:25.5,height:25.5*1.25,
  groundClearance:Math.max(1.4,25.5*.09),upperSideHeight:25.5*1.25*.91,
  wheelOutboardCenters:[-(25.5/2-.4+.3),25.5/2-.4+.3]},
 note:'Model includes original mirrors, roof equipment, glass, closed doors and lamps; no LN overlays or ads.'};
function draw(canvas,options){
 options=options||{};const angle=Number.isFinite(+options.angle)?+options.angle:0,
  line=[1,2,3].includes(+options.line)?+options.line:3,
  night=!!options.night,w=canvas.width,h=canvas.height,
  g=canvas.getContext('2d'),scale=Math.min(w/170,h/170),
  heading=angle*Math.PI/180,res=options.res===6?6:4,
  sp=C.sprite(id,lineColor(line),heading,res,16),k=sp.k;
 g.save();g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,w,h);
 g.imageSmoothingEnabled=true;if('imageSmoothingQuality' in g)g.imageSmoothingQuality='high';
 g.translate(w/2,h/2+5*scale);g.scale(scale,scale);
 g.drawImage(sp.cv,-sp.ox/sp.res,-sp.oy/sp.res,sp.cv.width/sp.res,sp.cv.height/sp.res);
 // Match the optional original night overlay. The intrinsic lens details are already in the sprite.
 if(night)C.lights(g,id,0,0,k,{head:1,beam:0,brake:false,rev:false,ind:0,on:false,bar:false,t:0},16,1,2);
 g.restore();
 return {angle:((k*360/16)%360+360)%360,line,night,scale,
  origin:[w/2,h/2+5*scale],sprite:{direction:k,res:sp.res,
   worldBounds:[-sp.ox/sp.res,-sp.oy/sp.res,sp.cv.width/sp.res,sp.cv.height/sp.res]},
  model:info.id};
}
window.OriginalBus={draw,info};
})();
