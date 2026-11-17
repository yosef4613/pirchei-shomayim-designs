/* old_libs.js — נוצר אוטומטית ע"י extract_old.py מתוך /home/user/tc_root/tc/pkg/work/src_game_t17_gfxlib (הענף abb6df5). הקוד הישן של המשחק מילה במילה. גדלים: {"C34": 274799, "P34": 106432, "A34": 99734} */
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
const x0=X+cab[0]*L,x1=X+cab[1]*L,cw=W*.78,lng=['suv','mv','van'].includes(ty),r0=m.rf?X+m.rf[0]*L:lng?X+L*.07:x0+(x1-x0)*.22,r1=m.rf?X+m.rf[1]*L:x1-(x1-x0)*(ty=='sport'?.4:.3),xm=(x0+x1)/2,sb=D.sb*W,
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
const roofH=x=>boxT?Math.max(1,G.hw(x)-sb-.8):Math.max(1,gH(x)-W*.07),rf0=boxT?(ty=='van'&&!m.rf?X+L*.05:r0):r0,roofB=(t,d=0)=>{const n=20,xc=(rf0+r1)/2,hx=(r1-rf0)/2;for(let i=0;i<=n;i++){const x=rf0+(r1-rf0)*i/n,y=(roofH(x)-d)*q5((x-xc)/hx,boxT?16:4);i?t.lineTo(x,y):t.moveTo(x,y)}for(let i=n;i>=0;i--){const x=rf0+(r1-rf0)*i/n;t.lineTo(x,-(roofH(x)-d)*q5((x-xc)/hx,boxT?16:4))}t.closePath()},roofPath=(d=0)=>{c.beginPath();roofB(c,d)};
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
  const r0 = m.rf ? X + m.rf[0] * L : lng ? X + L * .07 : x0 + (x1 - x0) * .22, r1 = m.rf ? X + m.rf[1] * L : x1 - (x1 - x0) * (ty == 'sport' ? .4 : .3), xm = (x0 + x1) / 2, sb = D.sb * W, boxT = ty == 'van' || ty == 'truck';   // R‑70 (cars70, 11.11): the roof from the proportions table (m.rf — 063a), else today's formula (48% of the cabin, 38% in a sports car)
  const gH = x => Math.max(1, Math.min(cw / 2, Gg.hw(x) - sb - .5)), q5 = (u, p) => Math.pow(Math.max(0, 1 - Math.pow(Math.abs(u), p)), 1 / p);
  const gx0 = boxT ? x0 + .5 : x0, gx1 = x1, bF = Math.min(1.6, (x1 - r1) * .12), bR = boxT ? 0 : Math.min(1.2, Math.max(0, (r0 - x0) * .25));
  const yg = x => gH(x) * (.84 + .16 * Math.min(1, (x - gx0) / 2.6, (gx1 - x) / 2.6));
  const roofH = x => boxT ? Math.max(1, Gg.hw(x) - sb - .8) : Math.max(1, gH(x) - W * .07), rf0 = boxT ? (ty == 'van' && !m.rf ? X + L * .05 : r0) : r0;
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
  if (M.m.rf && typeof r70Prep === 'function') r70Prep(M);   // R‑70 · cars70: the door lines from the model's doors, the limousine's pillars (063a)
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
      drawRim(g, opt.rim != null && opt.rim >= 0 ? opt.rim : M.rim, M.m.rimR || .64);   // sp01: a big rim in a low-profile tyre (m.rimR — 063a)
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
    if (M.m.limo && typeof r70LimoInside === 'function') r70LimoInside(g, M, Pj, U);   // R‑70 · cars70: the seats and the driver under the see-through roof
    if (!M.open) { const pr = [M.xc, 0, M.zR], T = aff(pr, [pr[0] + 1, 0, M.zR], [pr[0], 1, M.zR], Pj(pr), Pj([pr[0] + 1, 0, M.zR]), Pj([pr[0], 1, M.zR]));
    g.save(); g.setTransform(T[0], T[1], T[2], T[3], T[4], T[5]); g.beginPath(); const rl = M.FR.map(f => f.r); g.moveTo(rl[0][0], rl[0][1]); for (const q of rl) g.lineTo(q[0], q[1]); g.closePath();
    g.clip(); if (M.m.limo) g.globalAlpha = .32; else if (M.m.glassRoof) g.globalAlpha = M.m.glassRoof; g.drawImage(tex.cv, tex.u0, tex.v0, tex.wu, tex.hv); g.restore();
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
  if (s === 5 && typeof W17RIM === 'function') { W17RIM(g, 0, 0, rr); return }   // W17 · פריט 22 (11.11): ה"כוכב" — חמישה חישורים כפולים, לא כמו "5 חישורים" (074zd W17RIM)
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
      if (ty == 'sport' && !M.m.coupe) for (const sg of [1, -1]) quad(false, sg * W * .16, sg * W * .27, .08, .26, '#0e1012', 'rgba(200,205,210,.7)') }
  }
  if (M.m.coupe && typeof r70CoupeEnds === 'function') r70CoupeEnds(g, M, quad, frontV, rearV, U);   // sp01: the luxury coupe's front and rear (063a)
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
    if (M.m.limo && typeof r70LimoSide === 'function') r70LimoSide(g, M, Pj, s, sideAt, pc, U);   // R‑70 · cars70: the limousine's pillars, the chrome
    else if (!M.boxT && M.D.doors > 2 && M.ty != 'sport') { const xb = M.xm; const P = [sideAt(xb - .9, 0), sideAt(xb + .9, 0), sideAt(xb + .7, 1), sideAt(xb - .7, 1)].map(Pj); g.fillStyle = pc(s, 'side'); g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = .5; poly(g, P); g.fill(); g.stroke() }
    if (M.m.coupe && typeof r70CoupeSide === 'function') r70CoupeSide(g, M, Pj, s, sideAt, pc, U);   // sp01: the side vent, the handle, the chrome (063a)
    if (M.boxT) { const xb = M.x0 + .8; const P = [sideAt(xb, 0), sideAt(xb + 1.2, 0), sideAt(xb + 1.2, gTop), sideAt(xb, gTop)].map(Pj); g.fillStyle = litC(litBase(col), lb([0, s, 0])); poly(g, P); g.fill();
      g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.5, .4 * U); for (const xd of M.dl) if (xd < M.x0) { const p0 = Pj(sideAt(xd, 0)), p1 = Pj(sideAt(xd, .9)); g.beginPath(); g.moveTo(p0[0], p0[1]); g.lineTo(p1[0], p1[1]); g.stroke() }
      // the van's A pillar
      const iA2 = s === 1 ? M.iSideP[1] : M.iSideN[0], a = Pj(FR[iA2].b), b = Pj(lerp3(FR[iA2].b, FR[iA2].r, gTop)); g.strokeStyle = pc(s, 'front'); g.lineWidth = Math.max(.8, 1.4 * U); g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
      // the line of the top of the windows
      g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = Math.max(.5, .4 * U); const c0 = Pj(sideAt(M.x0 + .8, gTop)), c1 = Pj(lerp3(FR[iA2].b, FR[iA2].r, gTop)); g.beginPath(); g.moveTo(c0[0], c0[1]); g.lineTo(c1[0], c1[1]); g.stroke() }
    // the belt trim
    const I = s === 1 ? M.iSideP : M.iSideN; g.strokeStyle = M.m.limo ? '#dfe5ea' : 'rgba(16,19,23,.75)'; g.lineWidth = Math.max(.6, .55 * U); g.beginPath();
    let first = true; for (let i = Math.min(I[0], I[1]); i <= Math.max(I[0], I[1]); i++) { const p = FR[i % n].b; if (M.boxT && p[0] < M.x0 + .8) continue; const q = Pj(p); if (first) { g.moveTo(q[0], q[1]); first = false } else g.lineTo(q[0], q[1]) } g.stroke();
  }
}


// ---------- R‑70 · cars70 (11.11.2026): טבלת הפרופורציות — הגוף ב-3/4 נבנה מהטבלה, לא מהציור הישן מלמעלה (D‑389, ‏D‑390, ‏D‑391) ----------
// הבעיה (הבעלים / הביקורת 2.11 13:13): התא והגג נגזרים מהציור הישן (cab של השורה ב-VM, והגג = 48% מהתא, 38% בספורט) — סדאן: מכסה מנוע 37%,
// תא 37%, גג 16%, תא מטען 27% (במכונית אמיתית ~30 / 50 / 35 / 20). כאן: שורה לכל דגם, במטרים של מכונית אמיתית מאותו סוג (×1; המשחק מצייר
// ×1.125 — FLEET_GAME): האורך והרוחב (המעטפת של המחלקה, FLEET_REAL — לא משתנה: החניות, הנתיבים והתנועה בלי שינוי), הגובה, המרחק בין
// הסרנים והבליטות, והאורכים מהחרטום אחורה: מכסה המנוע (עד בסיס השמשה), השמשה הקדמית, הגג, השמשה האחורית ותא המטען; הגבהים: קצה מכסה המנוע,
// קו החלונות, הגג, הזנב, המרווח מהקרקע. מהשורה נבנים cab / wb / rf של הדגם ו-HT_M שלו — אותו צייר (הצבעים, הפנסים, הגריל, הפרטים — הזהות
// של הדגם נשמרת), רק הגוף מהטבלה. הבדיקה האוטומטית (C34.r70check): כל חלק נמדד ב-geo עצמו מול הטבלה — סטייה מותרת 0.2 מ׳ (D‑390).
// הסדר (D‑391 / D‑392): קודם 6 דגמי האב (mode 'proto' — ברירת המחדל במשחק), אחרי האישור — הקיימים (mode 'all' — בדף "מה צריך"). אין שינוי גורף:
// דגם בלי שורה פעילה מצויר בדיוק כמו היום (בלי m.rf — הנוסחה של 063).
const R70 = { mode: null, TOL: .2, bak: new Map(), ver: 'r70-1',
  // דגמי האב (D‑391; המפרט של הבעלים 11.11 10:50 — owner_2026-11-11_1050_cars40.txt): מקבוצות העיצוב מחדש / החלקי, והנפוץ בעיר בכל משפחה —
  // מיני HB-03 · סדאן SD-04 (SD-02 — "ליטוש בלבד") · רכב שטח SU-02 · מיניוואן MV-02 · טנדר PK-02 (דאבל קבינה, יש בעיר) · מכונית־על SP-02
  PROTO: ['VH-HB-03', 'VH-SD-04', 'VH-SU-02', 'VH-MV-02', 'VH-PK-02', 'VH-SP-02'],
  // רמת הטיפול של כל אחד מ-26 הקיימים (המפרט של הבעלים): polish — ליטוש בלבד · part — עיצוב חלקי וגאומטריה מותאמת · body — הגוף והצללית מחדש
  LEVEL: { 'VH-HB-01': 'polish', 'VH-SD-01': 'polish', 'VH-SD-02': 'polish', 'VH-PR-01': 'polish',
    'VH-HB-02': 'part', 'VH-SD-03': 'part', 'VH-SU-01': 'part', 'VH-SU-03': 'part', 'VH-PK-02': 'part', 'VH-PR-02': 'part', 'VH-SP-04': 'part',
    'VH-HB-03': 'body', 'VH-SD-04': 'body', 'VH-SU-02': 'body', 'VH-SU-04': 'body', 'VH-SU-05': 'body', 'VH-MV-01': 'body', 'VH-MV-02': 'body', 'VH-MV-03': 'body',
    'VH-PK-01': 'body', 'VH-PK-03': 'body', 'VH-PR-03': 'body', 'VH-PR-04': 'body', 'VH-SP-02': 'body', 'VH-SP-03': 'body',
    'VH-SP-01': 'body' },   // sp01 (הבעלים 11.11 20:20 — "והרכב על [במת הסיבוב] צריך עיצוב מחדש"): מ-'part' ל-'body' — עיצוב מחדש מלא, ברמה של SP-02
  // רכב אמיתי אחד כייחוס לכל דגם (המידות: אורך × רוחב × גובה, בין הסרנים — מ׳, ×1); הצורה מקורית והשם בדיוני במשחק (D‑389)
  REF: { 'VH-HB-01': ['Volkswagen Polo', 4.07, 1.75, 1.46, 2.56], 'VH-HB-02': ['Volkswagen Golf GTI', 4.29, 1.79, 1.46, 2.63], 'VH-HB-03': ['MINI Cooper 5 דלתות', 4.01, 1.73, 1.43, 2.57],
    'VH-SD-01': ['Toyota Corolla סדאן', 4.63, 1.78, 1.43, 2.70], 'VH-SD-02': ['Toyota Camry', 4.88, 1.84, 1.45, 2.83], 'VH-SD-03': ['Škoda Octavia ליפטבק', 4.69, 1.83, 1.47, 2.69],
    'VH-SD-04': ['Mazda3 סדאן', 4.66, 1.80, 1.44, 2.73], 'VH-SU-01': ['Hyundai Tucson', 4.50, 1.87, 1.65, 2.68], 'VH-SU-02': ['Kia Sorento', 4.81, 1.90, 1.70, 2.82],
    'VH-SU-03': ['Toyota RAV4', 4.60, 1.86, 1.69, 2.69], 'VH-SU-04': ['Toyota Land Cruiser Prado', 4.84, 1.89, 1.85, 2.79], 'VH-SU-05': ['BMW X4', 4.75, 1.92, 1.62, 2.86],
    'VH-MV-01': ['Toyota Sienna', 5.17, 1.99, 1.77, 3.06], 'VH-MV-02': ['Volkswagen Touran', 4.53, 1.83, 1.66, 2.79], 'VH-MV-03': ['Kia Carnival', 5.16, 2.00, 1.78, 3.09],
    'VH-PK-01': ['Toyota Hilux קבינה בודדת', 5.27, 1.80, 1.70, 3.09], 'VH-PK-02': ['Toyota Hilux דאבל קבינה', 5.33, 1.86, 1.82, 3.09], 'VH-PK-03': ['Ford Maverick', 5.07, 1.84, 1.75, 3.08],
    'VH-PR-01': ['BMW סדרה 5', 4.94, 1.87, 1.48, 2.98], 'VH-PR-02': ['Mercedes-Benz S-Class', 5.18, 1.95, 1.50, 3.11], 'VH-PR-03': ['BMW סדרה 8 קופה', 4.85, 1.90, 1.34, 2.82],
    'VH-PR-04': ['Porsche Cayenne', 4.93, 1.98, 1.70, 2.90], 'VH-SP-01': ['Aston Martin Vantage (2018–)', 4.47, 1.94, 1.27, 2.70], 'VH-SP-02': ['McLaren 720S', 4.54, 1.93, 1.20, 2.67],
    'VH-SP-03': ['Mazda MX-5', 3.92, 1.74, 1.23, 2.31], 'VH-SP-04': ['Ford Mustang', 4.79, 1.92, 1.38, 2.72] } };
// t(L, W, H, wb, of, [hood, ws, roof, rw] → trunk = the rest, [nose, belt, tail, gc], o): one row (real m)
const r70t = (L, W, H, wb, of, P, Z, o) => { const [hood, ws, roof, rw] = P, trunk = +(L - hood - ws - roof - rw).toFixed(3), [nose, belt, tail, gc] = Z;
  return Object.assign({ L, W, H, wb, of, or: +(L - wb - of).toFixed(3), hood, ws, roof, rw, trunk, nose, belt, tail, gc }, o || {}) };
R70.T = {
  // ---- האצ׳בקים (מחלקה Compact 4.0 × 1.75) ----
  'VH-HB-01': r70t(4.0, 1.75, 1.48, 2.55, .80, [1.00, .70, 1.62, .36], [.72, .97, .95, .15], { ref: 'האצ׳בק עירונית 5 דלתות', real: [4.0, 1.75, 1.48] }),
  'VH-HB-02': r70t(4.0, 1.75, 1.44, 2.58, .80, [1.05, .74, 1.50, .40], [.70, .95, .93, .14], { ref: 'האצ׳בק ספורטיבית 3 דלתות', real: [4.05, 1.78, 1.44] }),
  'VH-HB-03': r70t(4.0, 1.75, 1.43, 2.57, .78, [.95, .72, 1.70, .33], [.72, .98, .95, .14], { ref: 'מיני 5 דלתות — גג ארוך ושטוח, חרטום קצר', real: [4.0, 1.73, 1.43] }),
  // ---- הסדאנים (Sedan 4.8 × 1.85) ----
  'VH-SD-01': r70t(4.8, 1.85, 1.45, 2.75, .93, [1.38, .62, 1.50, .45], [.72, .97, .98, .15], { ref: 'סדאן קומפקטית', real: [4.55, 1.78, 1.45] }),
  'VH-SD-02': r70t(4.8, 1.85, 1.45, 2.80, .95, [1.42, .62, 1.52, .42], [.72, .97, 1.00, .15], { ref: 'סדאן משפחתית (D) — הנמדדת ב-R‑70', real: [4.8, 1.85, 1.45] }),
  'VH-SD-03': r70t(4.8, 1.85, 1.43, 2.80, .95, [1.38, .70, 1.35, .80], [.72, .96, .98, .15], { ref: 'ליפטבק — שמשה אחורית ארוכה ומשופעת', real: [4.75, 1.83, 1.43] }),
  'VH-SD-04': r70t(4.8, 1.85, 1.44, 2.81, .92, [1.40, .62, 1.42, .50], [.70, .96, .98, .14], { ref: 'סדאן קומפקטית ארוכת חרטום (דגם האב של הסדאן) — לפי הייחוס, במעטפת של 4.8 מ׳', real: [4.66, 1.80, 1.44] }),
  // ---- רכבי השטח (SUV 4.8 × 1.95) ----
  'VH-SU-01': r70t(4.8, 1.95, 1.62, 2.80, .92, [1.20, .72, 2.10, .40], [.88, 1.06, 1.05, .19], { ref: 'קרוסאובר', real: [4.6, 1.86, 1.62] }),
  'VH-SU-02': r70t(4.8, 1.95, 1.72, 2.82, .92, [1.20, .65, 2.42, .23], [.94, 1.10, 1.08, .20], { ref: 'רכב שטח גדול — גג גבוה עד הזנב (דגם האב של רכב השטח)', real: [4.81, 1.90, 1.70] }),
  'VH-SU-03': r70t(4.8, 1.95, 1.68, 2.82, .92, [1.18, .70, 2.30, .27], [.92, 1.10, 1.08, .20], { ref: 'רכב שטח בינוני (המעטפת של היום 4.8 מ׳)', real: [4.45, 1.85, 1.66] }),
  'VH-SU-04': r70t(4.8, 1.95, 1.88, 2.75, .85, [1.15, .48, 2.50, .12], [1.00, 1.18, 1.15, .28], { ref: 'רכב שטח קלאסי — שמשה זקופה, גלגל רזרבי מאחור', real: [4.7, 1.9, 1.88] }),
  'VH-SU-05': r70t(4.8, 1.95, 1.62, 2.80, .92, [1.22, .72, 1.55, .78], [.88, 1.06, 1.02, .19], { ref: 'קרוסאובר קופה — גג יורד לאחור', real: [4.75, 1.9, 1.62] }),
  // ---- המיניוואנים (Minivan 5.1 × 1.95) ----
  'VH-MV-01': r70t(5.1, 1.95, 1.76, 3.05, .98, [.90, 1.00, 2.70, .20], [.88, 1.04, 1.02, .16], { ref: 'מיניוואן', real: [5.1, 1.95, 1.76] }),
  'VH-MV-02': r70t(5.1, 1.95, 1.68, 3.10, .98, [.95, 1.02, 2.60, .22], [.86, 1.02, 1.00, .15], { ref: 'מיניוואן קומפקטית בהגדלה של המעטפת (5.1 מ׳) — חרטום קצר, שמשה ארוכה, גג עד הזנב (דגם האב)', real: [4.53, 1.83, 1.66] }),
  'VH-MV-03': r70t(5.1, 1.95, 1.80, 3.08, .98, [.95, .95, 2.75, .18], [.90, 1.06, 1.04, .17], { ref: 'מיניוואן משפחתית גדולה', real: [5.15, 1.99, 1.8] }),
  // ---- הטנדרים (Pickup 5.4 × 2.0); "תא המטען" = הארגז ----
  'VH-PK-01': r70t(5.4, 2.0, 1.82, 3.25, .93, [1.42, .55, .85, .10], [1.02, 1.22, 1.18, .23], { ref: 'טנדר — קבינה רגילה וארגז ארוך', real: [5.3, 1.95, 1.8], floor: .88 }),
  'VH-PK-02': r70t(5.4, 2.0, 1.82, 3.12, .93, [1.42, .55, 1.55, .10], [1.02, 1.22, 1.18, .23], { ref: 'טנדר דאבל קבינה — 4 דלתות, ארגז קצר יותר (דגם האב)', real: [5.33, 1.86, 1.82], floor: .88 }),
  'VH-PK-03': r70t(5.4, 2.0, 1.75, 3.15, .92, [1.35, .55, 1.15, .10], [.98, 1.18, 1.14, .22], { ref: 'טנדר קומפקטי — קבינה וחצי', real: [5.0, 1.85, 1.75], floor: .84 }),
  // ---- היוקרה (Premium 5.1 × 1.9) ----
  'VH-PR-01': r70t(5.1, 1.9, 1.47, 3.00, .95, [1.55, .66, 1.55, .48], [.72, .98, 1.02, .14], { ref: 'סדאן פרימיום', real: [5.0, 1.88, 1.47] }),
  'VH-PR-02': r70t(5.1, 1.9, 1.48, 3.10, .95, [1.55, .66, 1.65, .45], [.73, .99, 1.03, .14], { ref: 'סלון יוקרה ארוך', real: [5.15, 1.92, 1.48] }),
  'VH-PR-03': r70t(5.1, 1.9, 1.32, 2.85, .98, [1.75, .72, 1.05, .70], [.66, .90, .95, .12], { ref: 'קופה יוקרה / גרנד טורר (D‑388) — מכסה מנוע ארוך, תא לאחור', real: [4.95, 1.95, 1.32] }),
  'VH-PR-04': r70t(5.1, 1.9, 1.70, 3.00, .95, [1.28, .72, 2.30, .40], [.92, 1.10, 1.08, .21], { ref: 'רכב שטח ספורטיבי יוקרתי (D‑388)', real: [5.0, 2.0, 1.7] }),
  // ---- הספורט (Sports 4.5 × 1.9) ----
  // sp01 (11.11): קופה ספורט יוקרתית מודרנית — המנוע מלפנים, מאחורי הסרן הקדמי (front-mid): מכסה מנוע ארוך (1.70), התא לאחור, שמשה משופעת,
  // גג קצר שיורד בקו פאסטבק אל שמשה אחורית ארוכה (0.80) וזנב קצר וגבוה (ברווזי, 0.60); גלגל גדול (0.70, ‏20″ בפרופיל נמוך — החישוק 74% מהצמיג) בתוך הקשת;
  // גריל גדול, פס LED מתחת לפנסים ופס LED אחורי לכל הרוחב, פתח אוורור בצד (המנוע מלפנים), קווי כיפה במכסה; שתי דלתות ארוכות ודלת אחורית (האצ׳) עם השמשה.
  // (try5100 — גג שחור ושמשה אחורית 0.94: מלמעלה כל התא נקרא ככתם כהה אחד — הוחלף בגג בצבע הגוף)
  // הקודם ('part', ‏try4753): מכסה 1.45 · גג 0.95 · תא מטען 0.76 — "סדאן נמוכה" עם פסי מרוץ וכנף; הגלגל בולט מהגוף (pt 0.45).
  'VH-SP-01': r70t(4.5, 1.9, 1.28, 2.70, .86, [1.70, .80, .60, .80], [.64, .92, .95, .11], { ref: 'קופה ספורט יוקרתית מודרנית — מנוע מלפנים מאחורי הסרן (front-mid), מכסה ארוך, התא לאחור, גג פאסטבק, זנב קצר', real: [4.47, 1.94, 1.27],
    pt: .05, wd: .70, rimR: .74, coupe: 1, vd: { hl: 'slim', gr: 'big', hood: 'long', tl: 'bar', zf: .19, pf: 2.5, feat: ['lip'] },
    door: [{ side: 'L', x0: 1.45, x1: 2.75, hinge: 'front', type: 'hinged', z0: .26, z1: 1.22, angle: 65, role: 'driver' }, { side: 'R', x0: 1.45, x1: 2.75, hinge: 'front', type: 'hinged', z0: .26, z1: 1.22, angle: 65, role: 'front' },
      { side: 'rear', x0: 0, x1: 1.40, hinge: 'top', type: 'lift', z0: .72, z1: 1.22, angle: 75, role: 'tailgate', bags: 2 }] }),
  'VH-SP-02': r70t(4.5, 1.9, 1.18, 2.67, 1.0, [1.00, .98, .72, .92], [.48, .78, .95, .10], { ref: 'מכונית־על מודרנית — מנוע מאחורי התא, התא קדימה, מכסה קדמי קצר, נמוכה (דגם האב; ‏D‑388: המעוגלת)', real: [4.54, 1.93, 1.20], pt: .05, glassRoof: .5 }),
  'VH-SP-03': r70t(4.5, 1.9, 1.18, 2.50, .92, [1.50, .55, .90, .30], [.62, .86, .90, .12], { ref: 'רודסטר — גג פתוח, תא קצר', real: [4.2, 1.8, 1.25] }),
  'VH-SP-04': r70t(4.5, 1.9, 1.36, 2.72, .95, [1.60, .68, 1.00, .55], [.70, .92, .96, .13], { ref: 'קופה שרירים — מכסה מנוע ארוך', real: [4.8, 1.92, 1.36] }),
  // ---- הוואנים (Van 5.5 × 2.0): הגג עד הזנב, "תא המטען" = מה שמאחורי הגג ----
  'VH-VN-01': r70t(5.5, 2.0, 2.35, 3.40, .95, [.78, .72, 3.82, 0], [.98, 1.12, 1.10, .19], { ref: 'ואן מטען', real: [5.5, 2.0, 2.35], cab: 1.25 }),
  'VH-VN-02': r70t(5.5, 2.0, 2.45, 3.50, .92, [.72, .75, 3.85, 0], [.98, 1.12, 1.10, .19], { ref: 'ואן מטען ארוך', real: [6.0, 2.05, 2.5], cab: 1.25 }),
  'VH-VN-03': r70t(5.5, 2.0, 2.20, 3.30, .98, [.82, .70, 3.78, 0], [.96, 1.10, 1.08, .18], { ref: 'ואן חלוקה קצר', real: [4.9, 1.9, 2.0], cab: 1.2 }),
  // ---- המשאית הקלה (Truck 9.0 × 2.5): קבינה מעל המנוע, ארגז מאחור; "הגג" = גג הקבינה ----
  'VH-TR-01': r70t(9.0, 2.5, 3.10, 5.10, 1.35, [.18, .32, 1.62, .02], [1.30, 1.45, 1.30, .26], { ref: 'משאית קלה — קבינה מעל המנוע', real: [9.0, 2.5, 3.2], box: 3.1 }),
  // ---- השירותים (VS-*) — על אותם גופים ----
  'VS-TX-01': r70t(4.8, 1.85, 1.45, 2.80, .95, [1.42, .62, 1.52, .42], [.72, .97, 1.00, .15], { ref: 'מונית — על הסדאן המשפחתית', real: [4.8, 1.85, 1.45] }),
  'VS-TX-02': r70t(4.8, 1.85, 1.72, 2.90, .95, [.92, .95, 2.45, .20], [.88, 1.04, 1.02, .16], { ref: 'מונית מיניוואן (המעטפת של המונית 4.8 מ׳)', real: [4.8, 1.85, 1.72] }),
  'VS-PL-01': r70t(4.9, 1.9, 1.47, 2.85, .96, [1.45, .63, 1.55, .43], [.73, .98, 1.00, .15], { ref: 'ניידת — על סדאן', real: [4.9, 1.86, 1.47] }),
  'VS-PL-02': r70t(4.9, 1.9, 1.75, 2.88, .94, [1.22, .66, 2.42, .25], [.94, 1.11, 1.09, .21], { ref: 'ניידת רכב שטח', real: [4.9, 1.95, 1.75] }),
  'VS-AM-01': r70t(6.5, 2.3, 2.75, 3.65, .95, [.80, .74, 4.85, 0], [1.00, 1.15, 1.12, .20], { ref: 'אמבולנס ואן', real: [6.4, 2.25, 2.75], cab: 1.3 }),
  'VS-AM-02': r70t(6.5, 2.3, 3.00, 3.80, .95, [.95, .45, 1.40, .03], [1.10, 1.30, 1.20, .24], { ref: 'אמבולנס עם תיבה', real: [7.0, 2.4, 3.0], box: 3.0 }),
  'VS-FR-01': r70t(9.5, 2.5, 3.30, 4.80, 1.40, [.30, .35, 2.30, .02], [1.40, 1.55, 1.40, .28], { ref: 'כבאית סולם — קבינת צוות', real: [9.5, 2.5, 3.3], box: 3.3 }),
  'VS-FR-02': r70t(9.5, 2.5, 3.20, 4.60, 1.40, [.30, .35, 2.25, .02], [1.40, 1.55, 1.40, .28], { ref: 'כבאית מים — קבינת צוות', real: [8.6, 2.5, 3.2], box: 3.2 }),
  'VS-TW-01': r70t(9.0, 2.5, 2.70, 5.00, 1.30, [.90, .45, 1.10, .03], [1.20, 1.38, 1.10, .25], { ref: 'גרר קל — קבינה ומשטח (המעטפת של היום: משאית 9 מ׳)', real: [6.8, 2.3, 2.6] }),
  'VS-TW-02': r70t(9.0, 2.5, 3.00, 5.10, 1.35, [.30, .35, 1.70, .02], [1.35, 1.50, 1.20, .28], { ref: 'גרר כבד — קבינה מעל המנוע', real: [9.5, 2.55, 3.1] }),
  'VS-DL-01': r70t(5.5, 2.0, 2.40, 3.40, .95, [.78, .72, 3.82, 0], [.98, 1.12, 1.10, .19], { ref: 'ואן משלוחים', real: [5.5, 2.0, 2.4], cab: 1.25 }),
  'VS-DL-02': r70t(9.0, 2.5, 3.20, 5.10, 1.30, [.20, .32, 1.60, .02], [1.30, 1.45, 1.30, .26], { ref: 'משאית תיבה למשלוחים', real: [8.0, 2.5, 3.4], box: 3.2 }),
  'VS-MN-01': r70t(5.4, 2.0, 1.95, 3.25, .93, [1.42, .55, 1.55, .10], [1.02, 1.22, 1.18, .23], { ref: 'טנדר תחזוקה עירוני — דאבל קבינה, גגון אורות', real: [5.35, 1.9, 1.95], floor: .88 }),
  'VS-GS-01': r70t(5.5, 2.0, 2.30, 3.40, .95, [.80, .72, 3.78, 0], [.98, 1.12, 1.10, .19], { ref: 'ואן שירות', real: [5.0, 1.95, 2.2], cab: 1.25 })
};
// the wheel (the tyre's outer diameter, real m) of a real car of each type: 195/55 R16 · 215/55 R17 · 235/60 R18 · 265/65 R17 · 275/35 R19 …
const R70WD = { hatch: .63, sedan: .67, prem: .70, suv: .74, mv: .68, sport: .68, van: .70, pk: .78, truck: .95 };
// the rows of a model: its first VM row (the frozen twin '~F' of the field stays as it was — p440c)
const r70Row = id => VM.find(r => r[0] === id), M0ty = id => { const m = r70Row(id); return m ? m[2] : '' };
// one model from the table → its row (cab, wb, rf) and its heights (HT_M); the backup restores today's
function r70Apply(id, on) {
  const m = r70Row(id), t = R70.T[id]; if (!m || !t) return false;
  if (!R70.bak.has(id)) R70.bak.set(id, { cab: m[5].slice(), wb: m[8].slice(), rf: m.rf, ht: Object.prototype.hasOwnProperty.call(HT_M, id) ? Object.assign({}, HT_M[id]) : null });
  const B = R70.bak.get(id);
  if (!B.vd) B.vd = { pt: (VD_M[id] || {}).pt };
  if (!('vd0' in B)) B.vd0 = VD_M[id] ? JSON.parse(JSON.stringify(VD_M[id])) : null;   // sp01: the whole VD_M row (t.vd — the model's look from the table)
  if (!on) { delete m.limo; delete m.glassRoof; delete m.coupe; delete m.rimR; if (t.vd) { if (B.vd0) VD_M[id] = JSON.parse(JSON.stringify(B.vd0)); else delete VD_M[id] } if (VD_M[id]) { if (B.vd.pt == null) delete VD_M[id].pt; else VD_M[id].pt = B.vd.pt } m[5] = B.cab.slice(); m[8] = B.wb.slice(); if (B.rf) m.rf = B.rf; else delete m.rf; if (B.ht) HT_M[id] = Object.assign({}, B.ht); else delete HT_M[id]; return true }
  const ty = m[2], L = m[3], X = -L / 2, f = L / t.L, boxT = ty == 'van' || ty == 'truck';
  // the lengths from the nose back (asset units): the cowl (the windshield's base), the roof's front and rear tips, the rear glass base
  const uCowl = L / 2 - t.hood * f, r1 = uCowl - t.ws * f, rf0 = r1 - t.roof * f, uRG = rf0 - t.rw * f;
  const bF = Math.min(1.6, .12 * t.ws * f / 1.12), x1 = uCowl - bF;   // geo(): uCowl = x1 + bF, bF = min(1.6, (x1 − r1) · .12)
  let x0;
  if (ty == 'truck') x0 = rf0 - t.rw * f;                             // a truck: the cab's back wall (the box behind it) — the cab = hood + windshield + roof + rear
  else if (ty == 'van') x0 = x1 - (t.cab || 1.25) * f;                 // the van: the B pillar (the front doors), the box to the tail
  else { const bR = Math.min(1.2, .2 * t.rw * f); x0 = uRG + bR }      // geo(): uRG = x0 − bR, bR = min(1.2, (r0 − x0) · .25)
  if (t.vd) VD_M[id] = Object.assign(JSON.parse(JSON.stringify(B.vd0 || {})), t.vd); if (t.coupe) m.coupe = 1; if (t.rimR) m.rimR = t.rimR;
  if (ty == 'limo') m.limo = 1; if (t.glassRoof) m.glassRoof = t.glassRoof; if (t.pt != null) { VD_M[id] = VD_M[id] || {}; VD_M[id].pt = t.pt }
  m[5] = [+((x0 - X) / L).toFixed(4), +((x1 - X) / L).toFixed(4)];
  m.rf = [+((rf0 - X) / L).toFixed(4), +((r1 - X) / L).toFixed(4)];
  // the wheels: the rear axle at the rear overhang, the front at the front overhang; a third axle keeps its distance from the rear
  const wr = t.or / t.L, wf = 1 - t.of / t.L;
  m[8] = B.wb.length > 2 ? [wr, wr + (B.wb[1] - B.wb[0]), wf].map(v => +v.toFixed(4)) : [+wr.toFixed(4), +wf.toFixed(4)];
  // the heights (real m × 10 — geo() multiplies them by FLEET_GAME); the box of a truck, the bed floor of a pickup
  const h = Object.assign({}, B.ht || {}, { roof: t.H * 10, belt: t.belt * 10, hood: t.nose * 10, tail: t.tail * 10, gc: t.gc * 10 });
  if (t.floor) h.floor = t.floor * 10; if (t.box) h.box = t.box * 10;
  t.wd = t.wd || R70WD[ty] || .67; h.wr = t.wd / 2 * 10 * (G.FLEET_GAME || 1.125);   // geo() takes wr as is (world px)
  HT_M[id] = h; return true;
}
// the caches of the library that hold a model's shape (the outline, the geometry, the texture, the pictures, the wheels, the lamps)
function r70Flush() {
  VDG.clear(); GEO.clear(); TEX.clear();
  try { C34.clear() } catch (e) { }
  try { WHL.clear(); LAMPS.clear(); LAMPP.clear(); LOV.clear(); LOVB = 0 } catch (e) { }   // (defined further on in the library; at run time they exist)
}
// the mode: 'off' — today's (the old formula) · 'proto' — the 6 prototypes from the table (the game's default) · 'stage2' — the next step after the
// owner's approval: the prototypes + every one of the 26 marked "partial" or "body" (the 4 "polish only", the vans, the truck and the service
// vehicles stay as today — no sweeping change, the owner 11.11 10:50) · 'all' — every model in the table (the "what's needed" page only)
C34.r70 = function (mode) {
  if (mode == null) return R70.mode; mode = mode === 'all' || mode === 'off' || mode === 'stage2' ? mode : 'proto';
  const on = id => mode === 'all' || (R70.PROTO.includes(id) || (R70.ALWAYS || []).includes(id)) && mode !== 'off' || mode === 'stage2' && (R70.LEVEL[id] === 'part' || R70.LEVEL[id] === 'body');
  for (const id of Object.keys(R70.T)) r70Apply(id, on(id));
  R70.mode = mode; r70Flush(); return mode;
};
C34.r70T = R70.T; C34.r70Proto = R70.PROTO.slice(); C34.r70Tol = R70.TOL; C34.r70Level = R70.LEVEL; C34.r70Ref = R70.REF;
// the measurement (real m: world px / 10 / 1.125) of a model's geometry — the same quantities as the table
C34.r70measure = function (id) {
  const M = geo(id), s = M.sc / (10 * (G.FLEET_GAME || 1.125)), ty = M.ty, L = M.L, X = M.X, boxT = M.boxT, wb = M.m[8];
  const rf0 = M.rf0, r1 = M.r1, uCowl = M.uCowl, uRG = boxT ? (ty == 'truck' ? M.x0 : rf0) : M.uRG, q = v => +(v * s).toFixed(3);
  const o = { L: q(L), W: q(M.W), H: q(M.zR), wb: q((wb[wb.length - 1] - wb[0]) * L), of: q((1 - wb[wb.length - 1]) * L), or: q(wb[0] * L),
    hood: q(L / 2 - uCowl), ws: q(uCowl - r1), roof: q(r1 - rf0), rw: q(ty == 'truck' ? rf0 - M.x0 : rf0 - uRG), trunk: q(uRG - X),
    nose: q(M.zHood), belt: q(M.zBelt), tail: q(M.zTail), gc: q(M.gc), wr: q(M.wr), lw: +(L / M.W).toFixed(2) };
  if (ty == 'van') o.cab = q(M.x1 - M.x0);
  // the footprint of the drawn body (the rings, the wheels): it must stay inside the model's envelope — the stalls and the lanes
  let u0 = 1e9, u1 = -1e9, v1 = 0; for (const R of [M.RA, M.RB, M.RC]) for (const p of R) { if (p[0] < u0) u0 = p[0]; if (p[0] > u1) u1 = p[0]; if (Math.abs(p[1]) > v1) v1 = Math.abs(p[1]) }
  for (const w of M.wheels) { if (Math.abs(w.vo) > v1) v1 = Math.abs(w.vo); if (w.u - w.ra < u0) u0 = w.u - w.ra; if (w.u + w.ra > u1) u1 = w.u + w.ra }
  o.fp = { len: q(u1 - u0), wid: q(2 * v1), u0: q(u0), u1: q(u1) };
  // the percentages the review measured (of the length): the hood, the cabin (the glass house's base), the roof, the trunk
  o.pct = { hood: Math.round((L / 2 - uCowl) / L * 100), cabin: Math.round((uCowl - uRG) / L * 100), roof: Math.round((r1 - rf0) / L * 100), trunk: Math.round((uRG - X) / L * 100) };
  return o;
};
// the automatic check (D‑390): every part against the table, the deviation allowed — 0.2 m
C34.r70check = function (id) {
  const t = R70.T[id]; if (!t) return { id, ok: null, why: 'אין שורה בטבלה' }; const m = C34.r70measure(id), keys = ['L', 'W', 'H', 'wb', 'of', 'or', 'hood', 'ws', 'roof', 'rw', 'trunk', 'nose', 'belt', 'tail', 'gc'];
  if (t.cab && M0ty(id) == 'van') keys.push('cab'); if (t.wd) { t.wr = +(t.wd / 2).toFixed(3); keys.push('wr') } const d = {}; let worst = 0, wk = '';
  for (const k of keys) { if (t[k] == null || m[k] == null) continue; const e = +Math.abs(m[k] - t[k]).toFixed(3); d[k] = e; if (e > worst) { worst = e; wk = k } }
  return { id, ok: worst <= R70.TOL + 1e-9, worst, worstKey: wk, dev: d, m };
};
// ---------- the stretch limousine (model 49, the owner 11.11 13:15: "perfect and exact like the real one, and luxurious") ----------
// The reference: a classic stretch limousine — Lincoln Town Car 120″: 8.53 × 1.99 × 1.48 m, wheelbase 6.17 m (3.12 + 3.05), the wheel 0.70 m;
// four side windows (the front door, two in the stretch, the long rear door), a thick B pillar and the stretch pillars, the C pillar at the
// rear window, chrome (the grille, the belt, a strip along the body), dark glass. ONE long body from the table — not a car cut and lengthened.
// Its row's own cab / wheels are the old formula's (a sedan stretched — "was"); the table makes the body ("need").
VD_M['VH-LM-01'] = { hl: 'slim', gr: 'big', hood: 'long', tl: 'bar', zf: .07, pf: 3.2, zr: .06, pr: 3.4, fl: .6, doors: 4 };
if (!VM.some(r => r[0] === 'VH-LM-01')) VM.push(Object.assign(['VH-LM-01', 'Stretch Limousine', 'limo', 170, 39.7, [.28, .62], .14, .06, [.15, .85], [7, 0, 3]], { ex: 'lux' }));
ID_REF['VH-LM-01'] = 'Limousine'; REFS.Limousine = [8.53 * 11.25 / .8, 1.99 * 11.25 / .8];   // geo(): sc = REFS × 0.8 / L → 8.53 m × 1.125
R70.T['VH-LM-01'] = r70t(8.53, 1.99, 1.48, 6.17, 1.07, [1.55, .70, 4.60, .55], [.73, .98, 1.00, .15], { ref: 'לימוזינת מתיחה קלאסית — גוף ארוך אחד, 4 חלונות בצד', real: [8.53, 1.99, 1.48], wd: .70,
  // from the rear (m): the rear quarter window 1.85–3.35, the long passenger door in the middle 3.40–4.90, the stretch window 4.95–5.85, the front door 5.95–7.00
  // (pillars at 3.375, 4.925 and the B pillar at 5.90); four doors — the driver's and the front passenger's, and the long middle door on each side
  pillars: [3.375, 4.925, 5.90], doors: [3.40, 4.90, 5.95, 7.00],
  door: [{ side: 'L', x0: 5.95, x1: 7.00, hinge: 'front', type: 'hinged', z0: .30, z1: 1.40, angle: 65, role: 'driver' }, { side: 'R', x0: 5.95, x1: 7.00, hinge: 'front', type: 'hinged', z0: .30, z1: 1.40, angle: 65, role: 'front' },
    { side: 'L', x0: 3.40, x1: 4.90, hinge: 'front', type: 'hinged', z0: .30, z1: 1.42, angle: 70, role: 'passengers' }, { side: 'R', x0: 3.40, x1: 4.90, hinge: 'front', type: 'hinged', z0: .30, z1: 1.42, angle: 70, role: 'passengers' },
    { side: 'rear', x0: 0, x1: 1.13, hinge: 'front', type: 'lift', z0: .75, z1: 1.0, angle: 80, role: 'trunk', bags: 3 }] });
R70.REF['VH-LM-01'] = ['Lincoln Town Car 120″ (לימוזינת מתיחה)', 8.53, 1.99, 1.48, 6.17];
R70.ALWAYS = ['VH-LM-01'];   // on in every mode but 'off'
// ---------- sp01 (11.11): קופת הספורט היוקרתית — הפרטים שהגוף מהטבלה לא נותן לבד (רק לדגם עם coupe בשורה; בלי שינוי לאף דגם אחר) ----------
// החזית והזנב (על הרצועה התחתונה, כמו הגריל של lowerDetails): פס LED מתחת לפנסים, פתחי אוויר בצדדים, שפת פיצול; מאחור — פס LED לכל הרוחב,
// מפזר שחור עם צלעות, שתי יציאות פליטה כפולות. quad(front, v0, v1, t0, t1, fill, stroke) — מ-lowerDetails (t: 0 — הסף, 1 — הקו הרחב).
function r70CoupeEnds(g, M, quad, frontV, rearV, U) {
  const W = M.W;
  if (frontV) {
    for (const sg of [1, -1]) {
      quad(true, sg * W * .27, sg * W * .41, .08, .46, '#0d0f12', 'rgba(255,255,255,.10)');   // the side air intakes
      quad(true, sg * W * .29, sg * W * .39, .16, .38, 'rgba(60,66,74,.55)');                 // their mesh
      quad(true, sg * W * .25, sg * W * .44, .86, .97, '#eaf6ff', 'rgba(150,200,255,.55)');     // the LED strip (daytime running light) under the headlamp
      quad(true, sg * W * .28, sg * W * .42, .895, .935, '#ffffff') }
    quad(true, -W * .44, W * .44, 0, .06, '#1a1d21');                                       // the splitter lip
  }
  if (rearV) {
    quad(false, -W * .43, W * .43, .86, .99, '#7a0d12', 'rgba(0,0,0,.4)');                   // the full-width LED bar
    quad(false, -W * .41, W * .41, .9, .95, '#ff3a2e');
    quad(false, -W * .3, W * .3, 0, .3, '#121417');                                         // the diffuser
    for (const v of [-.18, -.06, .06, .18]) quad(false, W * v - W * .006, W * v + W * .006, 0, .28, '#2c3036');
    for (const sg of [1, -1]) for (const v of [.2, .27]) quad(false, sg * W * (v - .028), sg * W * (v + .028), .07, .2, '#2a2d31', 'rgba(210,215,220,.85)')   // the twin exhaust tips
  }
}
// הצד: פתח האוורור מאחורי הגלגל הקדמי (המנוע מלפנים), ידית דלת שקועה, וקו כרום דק מתחת לחלונות
function r70CoupeSide(g, M, Pj, s, sideAt, pc, U) {
  const fw = M.wheels.filter(w => w.s === s).sort((a, b) => b.u - a.u)[0]; if (!fw) return;
  const zB = x => M.zB(x), at = (x, t) => { const z = M.gc + (zB(x) - M.gc) * t; return Pj([x, s * (M.Gg.hw(x) + .02), z]) };
  const xa = fw.u - fw.ra - M.A(.06), xb = xa - M.A(.42);
  g.save(); g.fillStyle = '#0e1013'; g.strokeStyle = 'rgba(255,255,255,.14)'; g.lineWidth = Math.max(.4, .3 * U);
  const P = [at(xa, .62), at(xa, .98), at(xb, .9), at(xb + M.A(.08), .66)]; poly(g, P); g.fill(); g.stroke();
  // the flush handle near the rear of the door
  const dr = (M.dl && M.dl.length ? Math.min(...M.dl) : M.x0) + M.A(.22), h0 = Pj([dr, s * (M.Gg.hw(dr) + .02), M.zB(dr) * .985]), h1 = Pj([dr + M.A(.2), s * (M.Gg.hw(dr + M.A(.2)) + .02), M.zB(dr + M.A(.2)) * .985]);
  g.strokeStyle = 'rgba(15,17,20,.55)'; g.lineWidth = Math.max(.5, .45 * U); g.beginPath(); g.moveTo(h0[0], h0[1]); g.lineTo(h1[0], h1[1]); g.stroke();
  // the thin chrome under the side glass
  g.strokeStyle = 'rgba(225,230,235,.75)'; g.lineWidth = Math.max(.4, .28 * U); g.beginPath();
  for (let i = 0; i <= 16; i++) { const p = Pj(sideAt(lerp(M.bx0 + M.A(.1), M.bx1 - M.A(.05), i / 16), .02)); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]) } g.stroke();
  g.restore();
}
// ---------- the doors — part of the model (the owner 11.11 13:40: "the doors part of the model itself, also in the new ones — not to work twice") ----------
// one list per model, real m from the rear: {side 'L' | 'R' | 'rear', x0, x1, hinge 'front' | 'rear' | 'top' | 'side' | 'bottom', type 'hinged' | 'sliding' | 'lift' | 'drop' | 'double',
// z0, z1 (the opening's bottom and top), angle (the open angle, deg; sliding — 0), role}. The default here (D‑671) until the doors agent's schema
// (deliver/2026-11-11/cars70/from_doors.txt); the state 0 … 1 of each door — the doors agent's; the closed shut lines are drawn from this list.
function r70DoorsOf(id) {
  const t = R70.T[id]; if (!t) return []; if (t.door) return t.door; const m = r70Row(id), ty = m ? m[2] : 'sedan', D = (VD_M[id] || {}).doors || (VD_T[ty] || {}).doors || 4;
  const L = t.L, cowl = L - t.hood, glassR = t.trunk, z0 = +(t.gc + .15).toFixed(2), z1 = +Math.max(t.belt + .1, t.H - .05).toFixed(2), out = [], both = d => { out.push(Object.assign({ side: 'L' }, d), Object.assign({ side: 'R' }, d)) };
  if (ty == 'truck') { both({ x0: +(cowl - (t.roof + t.ws) + .1).toFixed(2), x1: +(cowl - .05).toFixed(2), hinge: 'front', type: 'hinged', z0: t.gc + .4, z1: t.H - .15, angle: 70, role: 'cab' }); return out }
  const dF1 = cowl - .05, dF0 = Math.max(glassR + .3, dF1 - (D > 2 && ty != 'sport' ? 1.1 : 1.3));
  both({ x0: +dF0.toFixed(2), x1: +dF1.toFixed(2), hinge: 'front', type: 'hinged', z0, z1, angle: 65, role: 'front' });
  if (ty == 'van') { both({ x0: +(dF0 - 1.25).toFixed(2), x1: +(dF0 - .05).toFixed(2), hinge: 'rear', type: 'sliding', z0, z1: t.H - .15, angle: 0, role: 'side' }); out.push({ side: 'rear', x0: 0, x1: .1, hinge: 'side', type: 'double', z0: t.gc + .2, z1: t.H - .1, angle: 90, role: 'rear' }) }
  else if (D > 2 && ty != 'sport') { const r1 = dF0 - .04, r0 = Math.max(glassR + .15, r1 - 1.0); both({ x0: +r0.toFixed(2), x1: +r1.toFixed(2), hinge: ty == 'mv' ? 'rear' : 'front', type: ty == 'mv' ? 'sliding' : 'hinged', z0, z1, angle: ty == 'mv' ? 0 : 70, role: 'rear' }) }
  if (ty == 'pk') out.push({ side: 'rear', x0: 0, x1: .08, hinge: 'bottom', type: 'drop', z0: t.floor || .85, z1: t.tail, angle: 90, role: 'tailgate' });
  else if (ty == 'sedan' || ty == 'prem' || ty == 'sport') out.push({ side: 'rear', x0: 0, x1: +(t.trunk).toFixed(2), hinge: 'front', type: 'lift', z0: t.tail - .25, z1: t.tail, angle: 75, role: 'trunk' });
  else if (ty != 'van') out.push({ side: 'rear', x0: 0, x1: +(t.trunk + t.rw).toFixed(2), hinge: 'top', type: 'lift', z0: +(t.belt - .3).toFixed(2), z1: +(t.H - .05).toFixed(2), angle: 80, role: 'tailgate' });
  return out;
}
// the trunk / the bed / the cargo doors: how many medium suitcases (55 × 40 × 24 cm, the hall's S15GR_BAGC) — the doors agent's defaults (13:55), a row may say its own
const R70BAGS = { hatch: 2, sedan: 3, prem: 3, sport: 1, suv: 4, mv: 4, pk: 6, van: 10, truck: 0, limo: 3 };
C34.r70Doors = id => { const m = r70Row(id), ty = m ? m[2] : 'sedan'; return r70DoorsOf(id).map(d => { const o = Object.assign({}, d); if (o.side === 'rear' && o.bags == null) o.bags = R70BAGS[ty] != null ? R70BAGS[ty] : 2; return o }) };
// the door lines from the doors (once per geometry) — every model whose body is from the table
function r70Prep(M) { if (M._r70) return; M._r70 = 1; const t = R70.T[M.id], f = M.L / (t ? t.L : M.L); if (!t) return;
  const side = r70DoorsOf(M.id).filter(d => d.side === 'L'), xs = []; for (const d of side) xs.push(M.X + d.x0 * f, M.X + d.x1 * f); if (xs.length) M.dl = xs;
  if (t.pillars) M.limoP = t.pillars.map(x => M.X + x * f) }
// the door lines and the pillars of the limousine, in the units of its geometry (once per geometry)
function r70LimoPrep(M) { r70Prep(M) }
// the side: the pillars (B and the stretch), the long rear door's window frame, the chrome strip along the body, the gloss
function r70LimoSide(g, M, Pj, s, sideAt, pc, U) {
  const w = M.A(.075);
  for (const xb of M.limoP || []) { const P = [sideAt(xb - w, 0), sideAt(xb + w, 0), sideAt(xb + w * .8, 1), sideAt(xb - w * .8, 1)].map(Pj); g.fillStyle = pc(s, 'side'); g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = .5; poly(g, P); g.fill(); g.stroke() }
  // the chrome: a strip along the body at the door handles' height, and the window frame top (the drip rail)
  const zc = x => M.gc + (M.zcap(x) - M.gc) * .62, x0 = M.X + M.dT + M.A(.25), x1 = M.L / 2 - M.hi - M.A(.25), N = 28;
  g.save(); g.lineCap = 'round';
  for (const [st, lw, dz] of [['rgba(20,24,30,.35)', .9, -M.A(.02)], ['#e9eef2', .55, 0]]) { g.strokeStyle = st; g.lineWidth = Math.max(.5, lw * U); g.beginPath();
    for (let i = 0; i <= N; i++) { const x = lerp(x0, x1, i / N), hw = M.Gg.hw(x), p = Pj([x, s * (hw + .05), zc(x) + dz]); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]) } g.stroke() }
  g.strokeStyle = '#dfe5ea'; g.lineWidth = Math.max(.5, .45 * U); g.beginPath(); for (let i = 0; i <= N; i++) { const t = i / N, p = Pj(sideAt(lerp(M.bx0, M.bx1, t), .985)); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]) } g.stroke();
  // the gloss: a soft long reflection on the upper side (black and pearl white are both glossy)
  g.strokeStyle = 'rgba(255,255,255,.22)'; g.lineWidth = Math.max(.6, .8 * U); g.beginPath();
  for (let i = 0; i <= N; i++) { const x = lerp(x0 + M.A(.4), x1 - M.A(.6), i / N), hw = M.Gg.hw(x), p = Pj([x, s * (hw - .2), M.zcap(x) - M.A(.06)]); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]) } g.stroke();
  g.restore();
}
// the inside under the see-through roof (rule 15): the carpet, the partition, the driver (a suit and a peaked cap), the rear bench and the
// side bench in cream leather, the bar — clipped to the roof's outline, so that it is seen only through the roof
function r70LimoInside(g, M, Pj, U) {
  const f = M.L / 8.53, X = M.X, at = (xm, vm, zm) => Pj([X + xm * f, vm * f, zm * f]), hwR = M.roofH(M.xc) / f;
  g.save(); g.beginPath(); const rl = M.FR.map(q => Pj([q.r[0], q.r[1], M.zR])); g.moveTo(rl[0][0], rl[0][1]); for (const q of rl) g.lineTo(q[0], q[1]); g.closePath(); g.clip();
  const quad = (P, c) => { g.fillStyle = c; g.beginPath(); P.forEach((q, i) => i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.closePath(); g.fill() };
  const box = (xa, xb, va, vb, za, zb, top, side) => { quad([at(xa, va, zb), at(xb, va, zb), at(xb, vb, zb), at(xa, vb, zb)], top);
    quad([at(xa, vb, za), at(xb, vb, za), at(xb, vb, zb), at(xa, vb, zb)], side) };
  const v = Math.min(.78, hwR * .95);
  quad([at(1.45, -v, .62), at(7.05, -v, .62), at(7.05, v, .62), at(1.45, v, .62)], '#2b2522');                       // the carpet
  box(5.72, 5.82, -v, v, .62, 1.18, '#1d1f23', '#16181b');                                                           // the partition behind the driver
  box(5.95, 6.55, -.62, -.12, .62, .98, '#2a2c31', '#202227'); box(5.95, 6.55, .12, .62, .62, .98, '#2a2c31', '#202227');   // the front seats
  box(5.9, 6.05, -.62, -.12, .98, 1.36, '#33353a', '#26282c'); box(5.9, 6.05, .12, .62, .98, 1.36, '#33353a', '#26282c');
  // the driver: the suit, the white collar, the head, the peaked cap with its visor (on the left — the city drives on the right)
  const dv = -.37; box(6.0, 6.42, dv - .2, dv + .2, .98, 1.32, '#15171b', '#101215');
  quad([at(6.33, dv - .07, 1.33), at(6.42, dv - .07, 1.33), at(6.42, dv + .07, 1.33), at(6.33, dv + .07, 1.33)], '#f2f2f0');
  const hc = at(6.22, dv, 1.42), hr = Math.max(1.2, .1 * f * U); g.fillStyle = '#d8a882'; g.beginPath(); g.arc(hc[0], hc[1], hr, 0, 7); g.fill();
  const cc = at(6.2, dv, 1.5); g.fillStyle = '#121418'; g.beginPath(); g.ellipse(cc[0], cc[1], hr * 1.15, hr * .85, 0, 0, 7); g.fill();
  const vz = at(6.34, dv, 1.47); g.fillStyle = '#050607'; g.beginPath(); g.ellipse(vz[0], vz[1], hr * .7, hr * .35, 0, 0, 7); g.fill();
  g.fillStyle = '#c9a13a'; g.fillRect(cc[0] - hr * .35, cc[1] - hr * .1, hr * .7, Math.max(.6, hr * .2));          // the cap's badge
  // the rear compartment: the rear bench across, the side bench along the right (a "J"), the bar along the left with glasses
  const cream = '#e8dcc4', creamS = '#cdbd9e';
  box(1.55, 2.05, -v + .06, v - .06, .62, .95, cream, creamS); box(1.5, 1.66, -v + .06, v - .06, .95, 1.35, '#efe5d1', creamS);
  box(2.05, 5.0, v - .52, v - .06, .62, .95, cream, creamS); box(2.05, 5.0, v - .16, v - .06, .95, 1.3, '#efe5d1', creamS);
  for (const x of [2.8, 3.6, 4.4]) quad([at(x, v - .5, .955), at(x + .02, v - .5, .955), at(x + .02, v - .08, .955), at(x, v - .08, .955)], 'rgba(120,100,70,.35)');   // the seams
  box(2.6, 4.7, -v + .06, -v + .42, .62, 1.0, '#4a2e1c', '#3a2416');                                                // the bar (dark wood)
  quad([at(2.65, -v + .1, 1.005), at(4.65, -v + .1, 1.005), at(4.65, -v + .38, 1.005), at(2.65, -v + .38, 1.005)], 'rgba(170,200,220,.35)');
  for (const x of [3.0, 3.35, 3.7]) { const q = at(x, -v + .24, 1.06); g.fillStyle = 'rgba(230,240,248,.8)'; g.beginPath(); g.arc(q[0], q[1], Math.max(.6, .035 * f * U), 0, 7); g.fill() }
  const lt = [at(2.2, 0, 1.44), at(5.5, 0, 1.44)]; g.strokeStyle = 'rgba(120,170,255,.55)'; g.lineWidth = Math.max(.6, .5 * U); g.beginPath(); g.moveTo(lt[0][0], lt[0][1]); g.lineTo(lt[1][0], lt[1][1]); g.stroke();   // the ceiling's light strip
  g.restore();
  // the see-through roof's frame: the roof is drawn at a low alpha after this (063); its edge in the body's paint
}
C34.r70mode0 = (G.__R70_MODE || 'stage2');
C34.r70(C34.r70mode0);
// ---------- sp05 (11.11.2026): VH-SP-05 — מכונית־העל "טריז", בתוך הספרייה C34 (אחרי 063a / 063b): שורה משלו בטבלה של R‑70, באותו צייר ----------
// הנתונים — 012c (G.TC_SP05). כאן: השורה ב-VM (והתאום הקפוא ~F), העיצוב (VD_M), האורך שלו (4.78 מ׳ — כמו הלימוזינה: ID_REF / REFS), השורה בטבלה,
// והפרטים שאין לאף דגם אחר — כולם בעטיפות של הצייר, רק לדגם הזה (שום דגם אחר לא משתנה):
//   veh (הציור מלמעלה = הטקסטורה של 3/4): קפלים ומשטחים משושים במכסה הקדמי, פנסי Y, צלעות "Y" בגג, מכסה מנוע משושה עם תריסים, פתחי אוויר בכתפיים, רשת הפליטה;
//   lowerDetails: פתח האוויר הגדול בצד, הקפל האלכסוני, הסף השחור; פתחי האוויר המשושים בחזית והשפה; המפזר עם הצלעות וארבעת פתחי הפליטה במרכז;
//   drawGlassHouse (לפני הזכוכית): פנסי Y מלפנים ומאחור, הרשת שבין הפנסים האחוריים; buildExtras: הכנף על שני עמודים עם לוחות הקצה;
//   drawRim: חישוק גדול (78% מהגלגל) עם 5 חישורי Y ומלחציים צבעוניים; carLamps: האורות בלילה במקום פנסי ה-Y; render: אחד משלושת הצבעים הבולטים,
//   ודלתות המספריים פתוחות (C34.sp05Open, או opt.cargo.key 'sp5d' — המכונית באולם התצוגה).
(function () {
  const X5 = G.TC_SP05; if (!X5) return;
  const ID = X5.id, T = X5.T, mine = id => id === ID || id === ID + '~F', SP5RIM = 9;
  // the painter's width of its own (the sports class would make it 4.5 m long): no class — its own length, as the limousine
  if (typeof G.fleetClassOf === 'function' && !G.fleetClassOf.__sp05) { const f0 = G.fleetClassOf; G.fleetClassOf = function (id, ty) { return mine(id) ? null : f0(id, ty) }; G.fleetClassOf.__sp05 = 1 }
  if (!VM.some(r => r[0] === ID)) {
    const m = X5.row.slice(); let a = null; try { a = TurboCity.get(ID) } catch (e) { a = null } if (a && a.fp && a.fp[3] > 0) m[4] = a.fp[3]; m.w0 = m[4];
    VM.push(m); const f = Object.assign(m.slice(), m); f[0] = ID + '~F'; f.frozen = 1; VM.push(f);   // the frozen twin (p440)
  }
  VD_M[ID] = JSON.parse(JSON.stringify(X5.vd));
  ID_REF[ID] = 'Hyper'; REFS.Hyper = [X5.own[0] * 11.25 / .8, X5.own[1] * 11.25 / .8];   // geo(): sc = REFS × 0.8 / L → 4.78 m × 1.125
  RIMS[ID] = SP5RIM;
  R70.T[ID] = r70t(T[0], T[1], T[2], T[3], T[4], T[5], T[6], { ref: X5.he + ' — ' + X5.why, real: X5.real.slice(), wd: X5.wd, pt: .05, door: X5.door.map(d => Object.assign({}, d)), sp05: 1 });
  R70.REF[ID] = X5.ref.slice(); R70.LEVEL[ID] = 'new';
  if (!(R70.ALWAYS || (R70.ALWAYS = [])).includes(ID)) R70.ALWAYS.push(ID);
  const SP5 = C34.sp05 = { id: ID, ver: X5.ver, open: 0, cur: false, err: null, made: 0 };
  // ---- helpers: metres → the asset's units; the surface of the body (the rings of geo) ----
  const MU = M => M.L / T[0], xd = (M, d) => M.L / 2 - d * MU(M), zh = (M, h) => h * MU(M);
  const fillP = (g, P, st) => { poly(g, P); g.fillStyle = st; g.fill() }, lineP = (g, P, st, lw, close) => { g.beginPath(); g.moveTo(P[0][0], P[0][1]); for (let i = 1; i < P.length; i++) g.lineTo(P[i][0], P[i][1]); if (close) g.closePath(); g.strokeStyle = st; g.lineWidth = lw; g.stroke() };
  // a point of the side (d from the nose, h above the ground, m): between the sill ring and the widest ring, then up to the edge of the top
  const sideP = (M, d, h, s) => { const x = xd(M, d), z = zh(M, h), hw = M.Gg.hw(x), zb = M.zB(x), zc = M.zcap(x); let v;
    if (z <= zb) v = hw - M.dA * (1 - Math.max(0, Math.min(1, (z - M.gc) / Math.max(.01, zb - M.gc)))); else v = hw - M.dC(x) * Math.max(0, Math.min(1, (z - zb) / Math.max(.01, zc - zb)));
    return [x, s * (v + .06), Math.min(z, zc)] };
  // a point of the nose / the tail at |y| = v m (beyond the corner — the corner): t 0 — the sill ring, 1 — the widest ring, 2 — the edge of the top
  const ringAt = (R, front, v) => { const n = R.length, I = []; if (front) for (let j = n - 1; j >= Math.max(0, n - 17); j--) I.push(j); else for (let j = 0; j < Math.min(n, 17); j++) I.push(j);   // the cap only (geo: 16 dense points at each end) — a lamp never slides onto the side
    for (let q = 0; q < I.length - 1; q++) { const a = R[I[q]], b = R[I[q + 1]]; if ((a[1] - v) * (b[1] - v) <= 0 && a[1] !== b[1]) return lerp3(a, b, (v - a[1]) / (b[1] - a[1])) } return R[I[I.length - 1]] };
  const endP = (M, front, vm, t, sg) => { const v = vm * MU(M), a = ringAt(M.RA, front, v), b = ringAt(M.RB, front, v), c = ringAt(M.RC, front, v), p = t <= 1 ? lerp3(a, b, t) : lerp3(b, c, Math.min(1, t - 1));
    return [p[0] + (front ? .05 : -.05), sg * p[1], p[2]] };
  // ---- the paint: one of the three bright ones ----
  const render0 = render;
  render = function (id, col, k, N, res, opt) {
    if (!mine(id)) return render0(id, col, k, N, res, opt);
    sp5Late(); col = X5.paintOf(col); SP5.cur = true; let r;
    try { r = render0(id, col, k, N, res, opt) } finally { SP5.cur = false }
    const open = Math.max(SP5.open || 0, opt && opt.cargo && /^sp5d/.test(opt.cargo.key || '') ? 1 : 0); SP5.made++;
    if (open > .01) { try { return sp5Doors(r, id, col, k, N, res, open) } catch (e) { SP5.err = 'doors: ' + (e && e.message || e) } }
    return r;
  };
  C34.render = render;
  // the wrappers that must wait for 064 (the turning wheels): once, at the first picture
  function sp5Late() { if (SP5.late) return; SP5.late = 1;
    const w0 = C34.wheels; if (typeof w0 === 'function') C34.wheels = function (ctx, id, x, y, k, N, dist, rim, q) { return w0(ctx, id, x, y, k, N, dist, mine(id) ? SP5RIM : rim, q) } }
  // ---- the picture from above (the texture of the 3/4 top): the facets, the Y lamps, the hexagons ----
  const veh0 = veh;
  veh = function (c, m, S, t) {
    if (!m || !mine(m[0])) return veh0(c, m, S, t);
    c.save(); try { veh0(c, m, S, t) } finally { c.restore() }
    c.save(); try { c.translate(m[3] / 2 + 10, m[4] / 2 + 10); sp5Top(c, m, S) } catch (e) { SP5.err = 'top: ' + (e && e.message || e) } finally { c.restore() }
  };
  function sp5Top(c, m, S) {
    const M = geo(m[0]), u = MU(M), col = m.fix || PAL[S.c][1], X = M.X, x = d => xd(M, d), hw = q => M.Gg.hw(q), dk = '#121519';
    c.lineJoin = 'miter'; c.lineCap = 'butt';
    for (const s of [1, -1]) {
      // the front lid: a sharp crease from the windshield to the nose, the outer facet darker, the inner one lighter — flat planes, not a dome
      const A = [x(1.08), s * .30 * u], B = [x(.14), s * .50 * u];
      fillP(c, [A, [x(1.08), s * (hw(x(1.08)) - .03 * u)], [x(.62), s * (hw(x(.62)) - .03 * u)], [x(.22), s * (hw(x(.22)) - .03 * u)], B], 'rgba(10,14,20,.13)');
      fillP(c, [A, B, [x(.14), 0], [x(1.08), 0]], 'rgba(255,255,255,.07)');
      lineP(c, [A, B], 'rgba(0,0,0,.32)', .55); lineP(c, [[A[0], A[1] - s * .035 * u], [B[0], B[1] - s * .035 * u]], 'rgba(255,255,255,.30)', .4);
      // two small hexagonal vents by the windshield
      fillP(c, [[x(1.06), s * .36 * u], [x(.98), s * .33 * u], [x(.94), s * .40 * u], [x(.98), s * .50 * u], [x(1.06), s * .52 * u]], dk);
      // the headlamp from above: a slim angular strip on the corner, the Y of light in it
      const st = [.16, .28, .42, .56], o = st.map(d => [x(d), s * (hw(x(d)) - .025 * u)]), iN = st.map((d, i) => [x(d), s * (hw(x(d)) - (.10 - i * .017) * u)]);
      fillP(c, o.concat(iN.reverse()), '#181c21');
      const ym = d => s * (hw(x(d)) - .055 * u); lineP(c, [[x(.18), ym(.18)], [x(.40), ym(.40)]], '#eef6ff', .5);
      lineP(c, [[x(.40), ym(.40)], [x(.54), s * (hw(x(.54)) - .03 * u)]], '#eef6ff', .42); lineP(c, [[x(.40), ym(.40)], [x(.53), s * (hw(x(.53)) - .085 * u)]], '#eef6ff', .42);
      // the shoulder intakes over the rear haunches (ahead of the rear wheels)
      const sh0 = [2.86, 3.02, 3.20, 3.36], top = sh0.map(d => [x(d), s * (M.yg(x(d)) + .07 * u)]), out = sh0.map(d => [x(d), s * (hw(x(d)) - .13 * u)]);
      fillP(c, top.concat(out.reverse()), '#0e1013');
      for (const f of [.3, .55, .8]) { const xx = x(2.86 + .5 * f); lineP(c, [[xx, s * (M.yg(xx) + .08 * u)], [xx, s * (hw(xx) - .14 * u)]], 'rgba(255,255,255,.08)', .3) }
      // the tail lamps from above: a thin red Y at the tail's corners
      const xt = X + .05 * u, yT = hw(xt);
      lineP(c, [[xt, s * .46 * u], [xt, s * (yT - .2 * u)]], '#d8191b', .55); lineP(c, [[xt, s * (yT - .2 * u)], [xt + .1 * u, s * (yT - .05 * u)]], '#d8191b', .45); lineP(c, [[xt, s * (yT - .2 * u)], [xt - .01 * u, s * (yT - .04 * u)]], '#d8191b', .45);
    }
    // the hexagon on the middle of the front lid
    const Hx = [[x(.24), 0], [x(.40), .24 * u], [x(.90), .24 * u], [x(1.04), 0], [x(.90), -.24 * u], [x(.40), -.24 * u]];
    fillP(c, Hx, 'rgba(255,255,255,.05)'); lineP(c, Hx, 'rgba(0,0,0,.26)', .45, true);
    // the roof: flat planes, not a bubble — the body's paint over today's rounded gloss, the outer facets darker, two ridges in a Y converging to the back
    { const ra = M.rf0, rb = M.r1, K = 12, E = []; for (let i = 0; i <= K; i++) { const q = lerp(ra, rb, i / K); E.push([q, M.roofY(q) + .25]) }
      fillP(c, E.concat(E.slice().reverse().map(p => [p[0], -p[1]])), sh(col, -.03));
      for (const s of [1, -1]) fillP(c, E.map(p => [p[0], s * p[1]]).concat([[ra + .04 * u, s * .09 * u], [(ra + rb) / 2, s * .16 * u], [rb - .05 * u, s * .30 * u]].reverse()), 'rgba(10,14,20,.16)') }
    for (const s of [1, -1]) { const P = [[M.r1 - .05 * u, s * .30 * u], [(M.r1 + M.rf0) / 2, s * .16 * u], [M.rf0 + .04 * u, s * .09 * u]]; lineP(c, P, 'rgba(0,0,0,.26)', .5); lineP(c, P.map(q => [q[0], q[1] - s * .03 * u]), 'rgba(255,255,255,.22)', .35) }
    // the engine cover (behind the cabin, where the rear window would be): a dark frame, a spine in the body's paint, three hexagonal louvred panes a side
    const ea = M.uRG + .04 * u, eb = M.rf0 - .03 * u, N = 10, edge = s => { const P = []; for (let i = 0; i <= N; i++) { const q = lerp(ea, eb, i / N); P.push([q, s * Math.max(1, M.yg(q) - .02 * u)]) } return P };
    fillP(c, edge(1).concat(edge(-1).reverse()), '#16191d');
    fillP(c, [[ea, -.06 * u], [eb, -.05 * u], [eb, .05 * u], [ea, .06 * u]], col);
    for (const s of [1, -1]) for (let i = 0; i < 3; i++) {
      const c0 = lerp(ea, eb, .19 + i * .31), hl = (eb - ea) * .13, cy = (M.yg(c0) * .55 + .03 * u) * s, hwp = Math.max(.6, M.yg(c0) * .34);
      const P = [[c0 - hl, cy], [c0 - hl * .55, cy + hwp], [c0 + hl * .55, cy + hwp], [c0 + hl, cy], [c0 + hl * .55, cy - hwp], [c0 - hl * .55, cy - hwp]];
      fillP(c, P, '#2a3038'); lineP(c, P, sh(col, -.08), .5, true);
      for (let j = 1; j < 4; j++) { const xx = c0 - hl + 2 * hl * j / 4; lineP(c, [[xx, cy - hwp * .8], [xx, cy + hwp * .8]], 'rgba(0,0,0,.55)', .3) }
    }
    // the tail deck: the engine's outlet — a hexagon mesh between the haunches
    const ta = x(4.56), tb = x(4.16), mw = .52 * u; fillP(c, [[ta, -mw], [tb, -mw * .9], [tb, mw * .9], [ta, mw]], '#121418');
    c.strokeStyle = 'rgba(255,255,255,.09)'; c.lineWidth = .25; c.beginPath(); const hs = .07 * u;
    for (let gx = ta + hs, r = 0; gx < tb - hs * .5; gx += hs * 1.5, r++) for (let gy = -mw + hs * (r % 2 ? 1.4 : .6); gy < mw - hs * .4; gy += hs * 1.73) { for (let a = 0; a <= 6; a++) { const an = a / 6 * Math.PI * 2, px = gx + Math.cos(an) * hs * .5, py = gy + Math.sin(an) * hs * .5; a ? c.lineTo(px, py) : c.moveTo(px, py) } }
    c.stroke();
  }
  // ---- the side, the lower front and the lower rear ----
  const lower0 = lowerDetails;
  lowerDetails = function (g, M, Pj, Pu, vis, lb, nearS, clipArches, U, base, faces) {
    if (!mine(M.id)) return lower0(g, M, Pj, Pu, vis, lb, nearS, clipArches, U, base, faces);
    const vis2 = n => n[1] === 0 && n[2] === 0 && Math.abs(n[0]) === 1 ? 0 : vis(n);   // the sill, the door lines and the arch lips as every car; the ends — ours
    lower0(g, M, Pj, Pu, vis2, lb, nearS, clipArches, U, base, faces);
    try { sp5Lower(g, M, Pj, vis, nearS, clipArches, U, base) } catch (e) { SP5.err = 'lower: ' + (e && e.message || e) }
  };
  function sp5Lower(g, M, Pj, vis, nearS, clipArches, U, base) {
    const lw = w => Math.max(.5, w * U), J = P => P.map(Pj);
    if (nearS) { const s = nearS, S = (d, h) => sideP(M, d, h, s), arch = clipArches();
      // the side skirt (carbon), from arch to arch
      fillP(g, J([S(1.50, .12), S(2.4, .12), S(3.36, .13), S(3.36, .22), S(2.4, .19), S(1.50, .17)]), '#17191c');
      lineP(g, J([S(1.50, .175), S(3.36, .225)]), 'rgba(255,255,255,.18)', lw(.3));
      // the sharp diagonal crease from the front arch to the big intake: a dark line, the light above it (two planes meeting)
      lineP(g, J([S(1.46, .50), S(2.10, .60), S(2.78, .71)]), 'rgba(0,0,0,.36)', lw(.5)); lineP(g, J([S(1.46, .53), S(2.10, .63), S(2.78, .74)]), 'rgba(255,255,255,.24)', lw(.35));
      // the big side intake ahead of the rear wheel — a hexagon, with the vanes in it
      const IN = [S(2.80, .27), S(3.34, .23), S(3.40, .56), S(3.12, .76), S(2.84, .71), S(2.70, .47)];
      fillP(g, J(IN), '#0b0d10'); lineP(g, J([IN[5], IN[4], IN[3], IN[2]]), 'rgba(255,255,255,.22)', lw(.35));
      for (const h of [.36, .46, .56]) lineP(g, J([S(2.80, h), S(3.33, h - .03)]), 'rgba(150,160,170,.18)', lw(.3));
      // the upper intake on the shoulder, behind the side window
      fillP(g, J([S(2.98, .79), S(3.40, .83), S(3.38, .92), S(3.04, .88)]), '#101215');
      if (arch) g.restore();
    }
    const W = (vm, t, sg, front) => Pj(endP(M, front, vm, t, sg));
    if (vis([1, 0, 0]) > .02) {   // the front: two big hexagonal intakes, the slot between them, the splitter
      for (const sg of [1, -1]) { const Q = [W(.34, .16, sg, 1), W(.76, .10, sg, 1), W(.93, .55, sg, 1), W(.84, 1.18, sg, 1), W(.42, 1.10, sg, 1), W(.30, .62, sg, 1)];
        fillP(g, Q, '#0c0e11'); lineP(g, [Q[4], Q[3], Q[2]], 'rgba(255,255,255,.16)', lw(.3));
        lineP(g, [W(.40, .98, sg, 1), W(.86, .38, sg, 1)], base, lw(1.0)); lineP(g, [W(.40, 1.0, sg, 1), W(.86, .40, sg, 1)], 'rgba(255,255,255,.25)', lw(.3)) }   // the blade across each intake
      fillP(g, [W(-.24, .30, 1, 1), W(.24, .30, 1, 1), W(.24, .78, 1, 1), W(-.24, .78, 1, 1)], '#0f1114');
      fillP(g, [W(-.96, 0, 1, 1), W(.96, 0, 1, 1), W(.96, .12, 1, 1), W(-.96, .12, 1, 1)], '#141619'); lineP(g, [W(-.95, .12, 1, 1), W(.95, .12, 1, 1)], 'rgba(255,255,255,.2)', lw(.3));
    }
    if (vis([-1, 0, 0]) > .02) {   // the rear: the diffuser with its fins, the hexagonal housing with the four pipes in the middle
      fillP(g, [W(-.88, 0, 1, 0), W(.88, 0, 1, 0), W(.88, .56, 1, 0), W(-.88, .56, 1, 0)], '#101215');
      for (const v of [-.68, -.42, -.15, .15, .42, .68]) lineP(g, [W(v, .02, 1, 0), W(v, .5, 1, 0)], 'rgba(130,138,146,.45)', lw(.35));
    }
  }
  // the four pipes in the middle of the tail, high (as the real one), in a hexagonal housing — on the band the 3/4 view sees
  function sp5Pipes(g, M, Pj, U) {
    const W = (vm, t) => Pj(endP(M, false, vm, t, 1)), HX = [W(-.40, 1.30), W(-.30, 1.02), W(.30, 1.02), W(.40, 1.30), W(.30, 1.58), W(-.30, 1.58)];
    fillP(g, HX, '#15171a'); lineP(g, HX, '#5a6168', Math.max(.5, .35 * U), true);
    for (const v of [-.22, -.075, .075, .22]) { const c0 = W(v, 1.30), e = W(v + .06, 1.30), r = Math.max(1, Math.hypot(e[0] - c0[0], e[1] - c0[1])), ry = Math.max(.9, Math.abs(W(v, 1.46)[1] - c0[1]));
      g.beginPath(); for (let a = 0; a <= 6; a++) { const an = a / 6 * Math.PI * 2 + Math.PI / 6, px = c0[0] + Math.cos(an) * r, py = c0[1] + Math.sin(an) * ry; a ? g.lineTo(px, py) : g.moveTo(px, py) }
      g.fillStyle = '#040508'; g.fill(); g.strokeStyle = '#b8bfc6'; g.lineWidth = Math.max(.5, r * .3); g.stroke() }
  }
  // ---- before the glass: the Y lamps (front and back), the mesh between the tail lamps ----
  const glass0 = drawGlassHouse;
  drawGlassHouse = function (g, M, Pj, vis, lb, tex, U, col, nearS) {
    if (mine(M.id)) try { sp5Upper(g, M, Pj, vis, U) } catch (e) { SP5.err = 'upper: ' + (e && e.message || e) }
    return glass0(g, M, Pj, vis, lb, tex, U, col, nearS);
  };
  function sp5Upper(g, M, Pj, vis, U) {
    const lw = w => Math.max(.5, w * U), W = (vm, t, sg, front) => Pj(endP(M, front, vm, t, sg));
    for (const sg of [1, -1]) {
      if (vis([.8, sg * .55, .3]) > .02) {   // the headlamp: a slim dark housing rising to the corner, the Y of white light in it
        fillP(g, [W(.44, 1.22, sg, 1), W(.90, 1.38, sg, 1), W(.96, 1.86, sg, 1), W(.48, 1.62, sg, 1)], '#15181c');
        const a = W(.50, 1.44, sg, 1), b = W(.76, 1.56, sg, 1); lineP(g, [a, b], '#f2f8ff', lw(.5)); lineP(g, [b, W(.93, 1.80, sg, 1)], '#f2f8ff', lw(.42)); lineP(g, [b, W(.92, 1.34, sg, 1)], '#f2f8ff', lw(.42));
        lineP(g, [W(.47, 1.63, sg, 1), W(.95, 1.87, sg, 1)], 'rgba(255,255,255,.3)', lw(.25));
      }
      if (vis([-.8, sg * .55, .3]) > .02) {   // the tail lamp: the red Y in a dark housing
        fillP(g, [W(.46, 1.18, sg, 0), W(.92, 1.10, sg, 0), W(.96, 1.90, sg, 0), W(.50, 1.80, sg, 0)], '#1a0c0e');
        const a = W(.50, 1.50, sg, 0), b = W(.74, 1.50, sg, 0); lineP(g, [a, b], '#ff2a1c', lw(.55)); lineP(g, [b, W(.92, 1.84, sg, 0)], '#ff2a1c', lw(.48)); lineP(g, [b, W(.91, 1.18, sg, 0)], '#ff2a1c', lw(.48));
        lineP(g, [a, b], 'rgba(255,190,170,.65)', lw(.18));
      }
    }
    if (vis([-1, 0, 0]) > .02) {   // between the tail lamps: the dark engine mesh (hexagons) over the pipes
      const P = [W(-.40, 1.60, 1, 0), W(.40, 1.60, 1, 0), W(.42, 1.90, 1, 0), W(-.42, 1.90, 1, 0)]; fillP(g, P, '#0e1013');
      g.save(); poly(g, P); g.clip(); g.strokeStyle = 'rgba(255,255,255,.12)'; g.lineWidth = lw(.2); g.beginPath();
      for (let v = -.40; v <= .40; v += .08) for (let t = 1.64; t <= 1.88; t += .12) { const q = W(v + (Math.round((t - 1.64) / .12) % 2 ? .04 : 0), t, 1, 0), r = Math.max(.8, .028 * MU(M) * U); for (let a = 0; a <= 6; a++) { const an = a / 6 * Math.PI * 2, px = q[0] + Math.cos(an) * r, py = q[1] + Math.sin(an) * r * .7; a ? g.lineTo(px, py) : g.moveTo(px, py) } }
      g.stroke(); g.restore(); sp5Pipes(g, M, Pj, U);
    }
  }
  // ---- the wing: a wide plane on two pylons, with end plates (carbon), over the tail deck ----
  const extras0 = buildExtras;
  buildExtras = function (M, col, opt) {
    const E = extras0(M, col, opt); if (!mine(M.id)) return E;
    const u = MU(M), X = M.X, xa = X + .05 * u, xb = X + .50 * u, y = .86 * u, z0 = zh(M, 1.07), z1 = zh(M, 1.12), cf = '#191c20', ct = '#2b3036';
    E.push({ base: [[xa, -y], [xb, -y], [xb, y], [xa, y]], topBase: [[xa, -y], [xb, -y + .02 * u], [xb, y - .02 * u], [xa, y]], z0, z1, col: cf, top: ct, c: [(xa + xb) / 2, 0, z1],
      deco: (g, f, at) => { if (f.n[0] < -.5) { g.fillStyle = 'rgba(255,40,28,.85)'; poly(g, [at(.47, .35), at(.53, .35), at(.53, .7), at(.47, .7)]); g.fill() } } });   // the third brake lamp in the middle of the wing's edge
    for (const sg of [-1, 1]) {
      E.push({ base: [[X + .02 * u, sg * .84 * u], [X + .56 * u, sg * .84 * u], [X + .56 * u, sg * .90 * u], [X + .02 * u, sg * .90 * u]], z0: zh(M, .93), z1: zh(M, 1.17), col: cf, top: ct, c: [X + .29 * u, sg * .87 * u, zh(M, 1.05)] });
      E.push({ base: [[X + .18 * u, sg * .27 * u], [X + .36 * u, sg * .27 * u], [X + .36 * u, sg * .33 * u], [X + .18 * u, sg * .33 * u]], z0: M.zcap(X + .27 * u) - .2, z1: z0, col: cf, top: cf, c: [X + .27 * u, sg * .3 * u, (M.zcap(X + .27 * u) + z0) / 2] });
    }
    return E;
  };
  // ---- the rims: large (78% of the wheel), five Y spokes, the brake disc and a coloured caliper behind them ----
  const rim0 = drawRim;
  drawRim = function (g, s, rr) {
    if (s !== SP5RIM && !SP5.cur) return rim0(g, s, rr);
    const R = .78, ring = (r, f) => { g.fillStyle = f; g.beginPath(); g.arc(0, 0, r, 0, 7); g.fill() };
    ring(R, '#0f1114'); ring(R * .82, '#565d64'); ring(R * .74, '#3b4147');
    g.fillStyle = '#ffb20a'; g.beginPath(); g.arc(0, 0, R * .8, -2.55, -1.35); g.arc(0, 0, R * .52, -1.35, -2.55, true); g.closePath(); g.fill();   // the caliper (upper rear)
    const gr = g.createLinearGradient(-R, -R, R, R); gr.addColorStop(0, '#8a939b'); gr.addColorStop(.5, '#2f353b'); gr.addColorStop(1, '#6d757d');
    g.strokeStyle = gr; g.lineCap = 'round';
    for (let i = 0; i < 5; i++) { const a = i / 5 * Math.PI * 2, P = (ang, r) => [Math.cos(ang) * r, Math.sin(ang) * r], m0 = P(a, R * .2), m1 = P(a, R * .52);
      g.lineWidth = R * .13; g.beginPath(); g.moveTo(m0[0], m0[1]); g.lineTo(m1[0], m1[1]); g.stroke();
      g.lineWidth = R * .085; for (const da of [-.24, .24]) { const e = P(a + da, R * .94); g.beginPath(); g.moveTo(m1[0], m1[1]); g.lineTo(e[0], e[1]); g.stroke() } }
    g.lineWidth = R * .06; g.strokeStyle = '#9aa2aa'; g.beginPath(); g.arc(0, 0, R * .97, 0, 7); g.stroke();
    g.fillStyle = '#cfd4d9'; g.beginPath(); for (let a = 0; a <= 6; a++) { const an = a / 6 * Math.PI * 2; a ? g.lineTo(Math.cos(an) * R * .15, Math.sin(an) * R * .15) : g.moveTo(Math.cos(an) * R * .15, Math.sin(an) * R * .15) } g.fill();
    ring(R * .07, '#1b1e22');
  };
  // ---- the lamps at night: at the Y lamps (two points a side in front, two at the back) ----
  const lamps0 = carLamps;
  carLamps = function (M) {
    const d = lamps0(M); if (!mine(M.id)) return d;
    const L = d.list.filter(l => l.t !== 'H' && l.t !== 'T');
    for (const s of [1, -1]) {
      for (const [v, t] of [[.62, 1.5], [.90, 1.62]]) { const p = endP(M, true, v, t, s); L.push({ t: 'H', u: p[0], v: p[1], z: p[2], n: [1, s * .35, .2], s }) }
      for (const [v, t] of [[.60, 1.5], [.90, 1.55]]) { const p = endP(M, false, v, t, s); L.push({ t: 'T', u: p[0], v: p[1], z: p[2], n: [-1, s * .35, .25], s }) }
    }
    d.list = L; return d;
  };
  // ---- the scissor doors, open: the far door before the body, the near one (and the opening it leaves) after ----
  // the door's outline (d from the nose, h, m): from the front arch to the intake, up to the roof; the window above the belt; the hinge at the front, at the belt
  const DOOR = { out: [[1.52, .18], [2.80, .20], [2.82, .80], [2.72, 1.06], [2.12, 1.10], [1.42, .82], [1.46, .50]], win: [[1.62, .83], [2.68, .83], [2.64, 1.03], [2.14, 1.06]], hinge: [1.46, .84] };
  function sp5Doors(r, id, col, k, N, res, open) {
    const M = geo(id), th = k / N * Math.PI * 2, cs = Math.cos(th), sn = Math.sin(th), sc = M.sc, K = K34, u = MU(M);
    const rel = p => [res * sc * (p[0] * cs - p[1] * sn), res * sc * (p[0] * sn + p[1] * cs - K * p[2])];
    const wn = n => [n[0] * cs - n[1] * sn, n[0] * sn + n[1] * cs, n[2]], vis = n => { const w = wn(n); return w[1] * K + w[2] }, lb = n => litK(norm3(wn(n)));
    const nearS = vis([0, 1, 0]) > .02 ? 1 : vis([0, -1, 0]) > .02 ? -1 : 0, D0 = X5.door[0];
    const ang = (D0.angle || 80) * Math.PI / 180 * open, tilt = (D0.tilt || 8) * Math.PI / 180 * open;
    const xh = xd(M, DOOR.hinge[0]), zhh = zh(M, DOOR.hinge[1]), vD = M.Gg.hw(xd(M, 2.1)) + .12;
    const rot = (q, s) => { const dx = xd(M, q[0]) - xh, dz = zh(M, q[1]) - zhh, x = xh + dx * Math.cos(ang) + dz * Math.sin(ang), z = zhh - dx * Math.sin(ang) + dz * Math.cos(ang);
      return [x, s * (vD + Math.max(0, z - zhh) * Math.tan(tilt) + .06), z] };
    let x0 = -r.ox, y0 = -r.oy, x1 = r.cv.width - r.ox, y1 = r.cv.height - r.oy;
    for (const s of [1, -1]) for (const q of DOOR.out) { const p = rel(rot(q, s)); x0 = Math.min(x0, p[0] - 3); y0 = Math.min(y0, p[1] - 3); x1 = Math.max(x1, p[0] + 3); y1 = Math.max(y1, p[1] + 3) }
    const ox = Math.ceil(-x0), oy = Math.ceil(-y0), cv = document.createElement('canvas'); cv.width = Math.ceil(x1 - x0) + 2; cv.height = Math.ceil(y1 - y0) + 2;
    const g = cv.getContext('2d'); g.lineJoin = 'round'; const P = p => { const q = rel(p); return [ox + q[0], oy + q[1]] }, U = res * sc;
    const door = (s, inner) => { const O = DOOR.out.map(q => P(rot(q, s))), Wn = DOOR.win.map(q => P(rot(q, s)));
      const n = [0, s * Math.cos(tilt), Math.sin(tilt)], skin = inner ? litC('#2a2d33', lb([0, -s, .2])) : litC(litBase(col), lb(n));
      if (!inner) { const Ii = DOOR.out.map(q => { const p = rot(q, s); p[1] -= s * .16 * u; return P(p) }); fillP(g, [O[0], O[1], Ii[1], Ii[0]], '#1c1f24'); fillP(g, [O[6], O[0], Ii[0], Ii[6]], '#24282d') }   // the door's thickness: its sill edge and its front edge
      fillP(g, O, skin); lineP(g, O, 'rgba(0,0,0,.6)', Math.max(.9, .6 * U), true);
      if (!inner) lineP(g, [O[3], O[4], O[5]], 'rgba(255,255,255,.35)', Math.max(.6, .35 * U));   // the light on its top edge
      fillP(g, Wn, inner ? 'rgba(52,66,78,.9)' : 'rgba(40,54,66,.88)'); lineP(g, [Wn[0], Wn[2]], 'rgba(255,255,255,.14)', Math.max(.6, .5 * U));
      if (!inner) { const a = P(rot([1.50, .52], s)), b = P(rot([2.78, .72], s)); lineP(g, [a, b], 'rgba(0,0,0,.3)', Math.max(.5, .45 * U)) }   // the crease goes up with the door
      else { const a = P(rot([1.70, .55], s)), b = P(rot([2.60, .60], s)); lineP(g, [a, b], '#d9a21b', Math.max(.6, .5 * U)) } };   // the trim's stitching
    for (const s of nearS ? [-nearS] : [1, -1]) door(s, true);
    g.drawImage(r.cv, ox - r.ox, oy - r.oy);
    if (nearS) { const s = nearS, Ap = DOOR.out.map(q => { const x = xd(M, q[0]); return P([x, s * (M.Gg.hw(x) + .05), zh(M, q[1])]) });
      fillP(g, Ap, '#121417');
      const seat = [[2.20, .30], [2.52, .32], [2.62, .96], [2.40, 1.02]].map(q => { const x = xd(M, q[0]); return P([x, s * (M.Gg.hw(x) * .55), zh(M, q[1])]) }); fillP(g, seat, '#2c2f35');
      lineP(g, seat.slice(0, 2), '#d9a21b', Math.max(.5, .35 * U));
      door(s, false) }
    return { cv, ox, oy, k: r.k, N: r.N, res: r.res, open };
  }
  // the scissor doors in the world, for the one door mechanism of the city (074zf, VDR — the state 0 … 1 of each door, the player's E, the live city):
  // VDR.paint(c, P, x, y, h, open, col, which) — the same frame (u forward, v to the right, z up, world px; P.pxM px per m); 'pre' — the far door, 'post' — the opening and the near door
  C34.sp05DoorPaint = function (c, P, x, y, h, open, col, which) {
    const ch = Math.cos(h), sn = Math.sin(h), K = K34, pm = P.pxM || 11.25, Lm = T[0], base = X5.paintOf(col); let n = 0;
    const pj = (u, v, z) => [x + u * ch - v * sn, y + u * sn + v * ch - K * z], wn = q => [q[0] * ch - q[1] * sn, q[0] * sn + q[1] * ch, q[2]], lb = q => litK(norm3(wn(q)));
    const U = dn => (Lm / 2 - dn) * pm, Z = hm => hm * pm, poly2 = (A, st) => { c.beginPath(); c.moveTo(A[0][0], A[0][1]); for (const q of A) c.lineTo(q[0], q[1]); c.closePath(); c.fillStyle = st; c.fill() };
    for (let i = 0; i < P.length; i++) {
      const d = P[i], a = Math.max(0, Math.min(1, +(open && open[i]) || 0)); if (!d || !d.scissor || a < .004) continue;
      const s = d.s, near = s * ch >= -1e-3; if ((which === 'post') !== near) continue;
      const D0 = X5.door[0], ang = (D0.angle || 80) * Math.PI / 180 * a, tilt = (D0.tilt || 8) * Math.PI / 180 * a, uh = U(DOOR.hinge[0]), zh0 = Z(DOOR.hinge[1]), vD = (d.v || P.hw || 11) + .08 * pm;
      const rot = q => { const du = U(q[0]) - uh, dz = Z(q[1]) - zh0, u = uh + du * Math.cos(ang) + dz * Math.sin(ang), z = zh0 - du * Math.sin(ang) + dz * Math.cos(ang); return pj(u, s * (vD + Math.max(0, z - zh0) * Math.tan(tilt)), z) };
      if (near) { c.save(); c.globalAlpha *= Math.min(1, a * 2.6); poly2(DOOR.out.map(q => pj(U(q[0]), s * (vD - .04 * pm), Z(q[1]))), '#121417');
        poly2([[2.20, .30], [2.52, .32], [2.62, .96], [2.40, 1.02]].map(q => pj(U(q[0]), s * vD * .55, Z(q[1]))), '#2c2f35'); c.restore() }
      const O = DOOR.out.map(rot), Wn = DOOR.win.map(rot), skin = near ? litC(litBase(base), lb([0, s * Math.cos(tilt), Math.sin(tilt)])) : litC('#2a2d33', lb([0, -s, .2]));
      if (near) { const I = DOOR.out.map(q => { const p = rot(q); return [p[0] + s * sn * .16 * pm, p[1] - s * ch * .16 * pm] }); poly2([O[0], O[1], I[1], I[0]], '#1c1f24') }
      poly2(O, skin); c.beginPath(); c.moveTo(O[0][0], O[0][1]); for (const q of O) c.lineTo(q[0], q[1]); c.closePath(); c.strokeStyle = 'rgba(0,0,0,.6)'; c.lineWidth = .5; c.stroke();
      poly2(Wn, near ? 'rgba(40,54,66,.88)' : 'rgba(52,66,78,.9)');
      if (near) { c.strokeStyle = 'rgba(255,255,255,.35)'; c.lineWidth = .35; c.beginPath(); c.moveTo(O[3][0], O[3][1]); c.lineTo(O[4][0], O[4][1]); c.lineTo(O[5][0], O[5][1]); c.stroke() }
      else { const p = rot([1.70, .55]), q = rot([2.60, .60]); c.strokeStyle = '#d9a21b'; c.lineWidth = .4; c.beginPath(); c.moveTo(p[0], p[1]); c.lineTo(q[0], q[1]); c.stroke() }
      n++;
    }
    return n;
  };
  // the doors open / closed for every SP-05 picture (the live page's button), and the pictures of this model only are dropped
  C34.sp05Open = function (v) { SP5.open = Math.max(0, Math.min(1, +v || 0)); C34.sp05Flush(); return SP5.open };
  C34.sp05Flush = function () { let n = 0; for (const key of Array.from(CACHE.keys())) if (key.startsWith(ID + '|') || key.startsWith(ID + '~F|')) { const e = CACHE.get(key); CBYTES -= e.cv.width * e.cv.height * 4; CACHE.delete(key); n++ } return n };
  // the check of this model: the table (C34.r70check), the doors, the body inside its own envelope (4.78 × 2.00 m)
  C34.sp05Check = function () { const c = C34.r70check(ID), m = c.m || C34.r70measure(ID); return { id: ID, mode: R70.mode, on: !!(r70Row(ID) && r70Row(ID).rf), check: { ok: c.ok, worst: c.worst, worstKey: c.worstKey }, L: m.L, W: m.W, H: m.H, fp: m.fp, pct: m.pct, doors: C34.r70Doors(ID), err: SP5.err } };
  C34.r70(R70.mode || C34.r70mode0 || 'proto');   // re-applied with this row (on in every mode but 'off')
})();
// ---------- cars14 (11.11.2026): ליטוש 4 הדגמים ו-12 התוספות — בתוך הטבלה של R‑70 (063a), באותו צייר ----------
// (1) ליטוש בלבד (HB-01 · SD-01 · SD-02 · PR-01 — המפרט של הבעלים 10:50; D‑686): במצב stage2 הגוף שלהם מהטבלה (השורות כבר בטבלה של cars70 — הגג, מכסה
//     המנוע ותא המטען של מכונית אמיתית) והגלגל בתוך הקשת; הצבעים, הפנסים, הגריל והפרטים — כמו היום. המעטפת בלי שינוי.
// (2) 12 התוספות (012b — TC_CARS14): שורה בטבלה לכל אחת (במטרים של הייחוס, במעטפת של המחלקה; המיקרו — באורך שלו), שורה ב-VM ובעיצוב (VD_M),
//     הדלתות ותא המטען בתוך השורה (door — C34.r70Doors), ותמיד פעילות (חוץ מ-'off'). הבדיקה — C34.r70check, כמו כל דגם.
(function () {
  const X14 = G.TC_CARS14; if (!X14) return;
  for (const q of X14.models) {
    const id = q.id, t = q.T;
    if (!VM.some(r => r[0] === id)) {
      const m = Object.assign(q.row.slice(), q.rowEx ? { ex: q.rowEx } : {});
      let a = null; try { a = TurboCity.get(id) } catch (e) { a = null } if (a && a.fp && a.fp[3] > 0) m[4] = a.fp[3]; m.w0 = m[4];   // the painter's width (as the loop of 063)
      VM.push(m); const f = Object.assign(m.slice(), m); f[0] = id + '~F'; f[4] = m.w0; f.frozen = 1; VM.push(f);                   // the frozen twin (p440)
    }
    VD_M[id] = JSON.parse(JSON.stringify(q.vd));
    if (q.own) { ID_REF[id] = 'Own' + id; REFS['Own' + id] = [q.own[0] * 11.25 / .8, q.own[1] * 11.25 / .8] }   // its own length (geo: sc = REFS × 0.8 / L), as the limousine
    R70.T[id] = r70t(t[0], t[1], t[2], t[3], t[4], t[5], t[6], Object.assign({ ref: q.he + ' — ' + q.why, real: q.ref.slice(1, 4), cars14: 1 }, t[7]));
    R70.REF[id] = q.ref.slice(); R70.LEVEL[id] = 'new';
    if (!(R70.ALWAYS || (R70.ALWAYS = [])).includes(id)) R70.ALWAYS.push(id);
  }
  for (const id of X14.polish) { const t = R70.T[id]; if (t && X14.polishPt[id] != null) t.pt = X14.polishPt[id] }
  R70.POLISH = X14.polish.slice(); R70.NEW = X14.ids.slice();
  // the mode — as 063a, and the 4 "polish only" join stage2 (the owner: "polish only"; D‑686 — every model that passed its checks goes in)
  C34.r70 = function (mode) {
    if (mode == null) return R70.mode; mode = mode === 'all' || mode === 'off' || mode === 'stage2' ? mode : 'proto';
    const lv = id => R70.LEVEL[id], on = id => mode === 'all' || mode !== 'off' && (R70.PROTO.includes(id) || R70.ALWAYS.includes(id)) ||
      mode === 'stage2' && (lv(id) === 'part' || lv(id) === 'body' || lv(id) === 'polish');
    for (const id of Object.keys(R70.T)) r70Apply(id, on(id));
    R70.mode = mode; r70Flush(); return mode;
  };
  C34.r70New = R70.NEW.slice(); C34.r70Polish = R70.POLISH.slice(); C34.r70Names = Object.fromEntries(X14.models.map(q => [q.id, q.he]));
  // every model the mode draws from the table (for the checks): on, and its check
  C34.r70On = () => Object.keys(R70.T).filter(id => { const m = r70Row(id); return !!(m && m.rf) });
})();
C34.r70mode0 = (G.__R70_MODE || 'stage2');   // D‑685 / D‑686: ברירת המחדל במשחק — stage2 (22 הדגמים + ליטוש 4 + 12 התוספות + הלימוזינה); 'proto' — כפתור
C34.r70(C34.r70mode0);
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
function p34LibInit(){if(window.P34)return true;
/* p34v3.js — Turbo City · people in the 3/4 view, the second sample (D‑263; the owner's notes of 29.10.2026 01:00, part ג).
   The projection and the sun of the cars (C34): screen = (x, y − K·z) with K = 0.6 (the same angle as the cars — the first sample
   used 0.86), the sun up-left (LD), ambient .62 + diffuse .38, the same colour ramp.  People are drawn ×1.45 real (replaces D‑73).
   A person is a small 3D model in metres: legs on a planted-foot gait (two-bone IK — the foot in contact does not slide when the
   walk phase advances by distance / cycle()), arms, a torso of cross-sections, neck, head (an ellipsoid) with hair / hat / beard
   cut from it by planes, clothes and things people carry.  Every part is shaded from its surface normals (cylinders across their
   width, ellipsoids radially) with the materials' highlights; a thin dark rim is baked around each picture; a clear contact shadow
   under the feet is drawn first.
   Pictures: one per (layer × look of that layer × activity × direction (8) × frame × density), cached with a byte cap (least
   recently used goes first).  Layers: body (skin, legs, shoes), top (shirt / jacket / coat / vest), hair (hair, beard, hat), item
   (bags, suitcase, tools, wands, the table set).  The parts of an earlier layer erase a later layer where they are in front of it,
   so the layers stack back to front without a seam.  'flat' — one picture per whole person (for comparison and for close-ups).
   API (world px, 10 px = 1 m, like the cars):  P34.draw(ctx, x, y, look, act, heading, phase, res[, mode]) — (x, y) the ground point,
   heading 0 = east, clockwise; phase 0…1 of the activity; res = device px per world px.  P34.cycle(look, act) — world metres per
   walk cycle (two steps).  P34.stats(), P34.clear(), P34.budgetMB. */
(function (G) {
'use strict';
const K = 0.6, SCALE = 1.125, PXM = 10;   // p440b: × 1.125 real, the game size of everything that moves (was × 1.45)
// p670 (people v2): the people's own camera — the depth of the body drawn at KYC (about 34° from above instead of the cars' 59°), the
// height the same (K): the face and the front read.  The feet keep the world depth (KW: standing and walking — the planted foot does
// not slide); who sits (bench, table) is all in the people's camera.
const KYC = .4; let KW = false, LOD = 0, RIDE = false;   // W17: RIDE — a rider on a vehicle: the cars' camera (the depth 1:1), so the hands meet the bars and the feet the pegs
const ky = z => { if (RIDE) return 1; if (!KW || z >= .55) return KYC; if (z <= .1) return 1; const t = (z - .1) / .45; return 1 + (KYC - 1) * t * t * (3 - 2 * t) };
const FR = { walk: 12, drag: 12, carry: 12, stand: 1, wait: 8, eat: 8, marshal: 8, stop: 1, bench: 1, f1: 8, f2: 8, f3: 8, f4: 8, f5: 8 };   // p641: the fishing activities, one per rod   // p581: bench — sitting on a bench
// ---- vectors ----
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]], sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k], dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const crs = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const nrm = v => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n] };
const lrp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const comb = (o, f, a, l, s, z) => [o[0] + f[0] * a + l[0] * s, o[1] + f[1] * a + l[1] * s, o[2] + z];
const Z = [0, 0, 1];
// ---- light (the cars' sun) ----
const LD = nrm([-0.42, -0.55, 0.72]), VW = nrm([0, K, KYC]), HV = nrm(add(LD, VW));   // p670: VW — the people's camera
const AMB = .62, DIF = .38, TOPB = AMB + DIF * LD[2];
const MAT = { cloth: { s: .05, p: 4 }, denim: { s: .06, p: 5 }, wool: { s: .03, p: 3 }, skin: { s: .13, p: 9, glow: .2 }, hair: { s: .3, p: 12 },
  leather: { s: .55, p: 20 }, sole: { s: .05, p: 4 }, plastic: { s: .42, p: 16 }, hivis: { s: .08, p: 5, glow: .2 }, refl: { s: .7, p: 6, glow: .35 },
  metal: { s: .7, p: 24 }, paper: { s: .04, p: 4 }, wood: { s: .12, p: 8 }, glow: { s: 0, p: 1, glow: .85 } };
let LIFT = 0;   // 29.10 02:25: the small pictures (under ~30 px) — the shadows lifted toward the lit tone, so the clothes read
function bri(n, m, occ) {
  let b = (AMB + DIF * Math.max(0, dot(n, LD))) / TOPB; if (n[2] < 0) b *= 1 + .3 * n[2]; if (LIFT && b < 1.04) b += (1.04 - b) * .45;
  if (m) { if (m.s) b += m.s * Math.pow(Math.max(0, dot(n, HV)), m.p); if (m.glow) b = b * (1 - m.glow) + 1.12 * m.glow }
  return b * (occ || 1);
}
const hexC = h => { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255] };
const HEXM = new Map();
function col(h, b) {   // the cars' ramp: darker toward a cool dark, lighter toward white
  let c = HEXM.get(h); if (!c) { c = hexC(h); HEXM.set(h, c) }
  if (b <= 1) return `rgb(${c[0] * b + 14 * (1 - b) | 0},${c[1] * b + 17 * (1 - b) | 0},${c[2] * b + 22 * (1 - b) | 0})`;
  const k = Math.min(1, (b - 1) * .6); return `rgb(${c[0] + (255 - c[0]) * k | 0},${c[1] + (255 - c[1]) * k | 0},${c[2] + (255 - c[2]) * k | 0})`;
}
// ---- projection: world metres (around the ground point) → screen metres (× SCALE) ----
const P = p => [p[0] * SCALE, (p[1] * ky(p[2]) - K * p[2]) * SCALE];
const PD = n => [n[0], n[1] * KYC - K * n[2]];
const PV = v => [v[0] * SCALE, (v[1] * KYC - K * v[2]) * SCALE];   // p670: a direction on the body → the screen
function hull(p) {
  if (p.length < 3) return p.slice();
  p = p.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]); const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo = [], up = []; for (const q of p) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q) }
  for (let i = p.length - 1; i >= 0; i--) { const q = p[i]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q) }
  return lo.slice(0, -1).concat(up.slice(0, -1));
}
const polyPath = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath() };
const circ2 = (c, r, n) => { const o = []; for (let i = 0; i < n; i++) { const t = i / n * Math.PI * 2; o.push([c[0] + Math.cos(t) * r, c[1] + Math.sin(t) * r]) } return o };

// ---- shapes → parts.  A part: { L layer, d depth (world y toward the camera), pts (screen), path(c), paint(c) } ----
function limbPart(L, d, A, B, ra, rb, hex, mat, occ) {
  const pts = hull(circ2(P(A), ra * SCALE, 14).concat(circ2(P(B), rb * SCALE, 14))), path = polyPath(pts);
  return { L, d, pts, path, ol: 'side', oc: hex, sA: P(A), sB: P(B), ra: ra * SCALE, rb: rb * SCALE, paint: c => {
    const a = nrm(sub(B, A)), t = Math.abs(a[2]) < .9 ? Z : [1, 0, 0], e1 = nrm(crs(a, t)), e2 = crs(a, e1);
    const ax = PD(a); let q = [-ax[1], ax[0]]; const ql = Math.hypot(q[0], q[1]); q = ql < 1e-6 ? [1, 0] : [q[0] / ql, q[1] / ql];
    const st = []; for (let i = 0; i < 24; i++) { const th = i / 24 * Math.PI * 2, n = add(mul(e1, Math.cos(th)), mul(e2, Math.sin(th))); if (dot(n, VW) <= 0) continue; const pd = PD(n); st.push([pd[0] * q[0] + pd[1] * q[1], bri(n, mat, occ)]) }
    c.beginPath(); path(c);
    if (st.length < 2) { c.fillStyle = col(hex, .8 * (occ || 1)); c.fill(); return }
    st.sort((u, v) => u[0] - v[0]); const o0 = st[0][0], o1 = st[st.length - 1][0], r = (ra + rb) / 2 * SCALE, m = P(lrp(A, B, .5));
    const g = c.createLinearGradient(m[0] + q[0] * r * o0, m[1] + q[1] * r * o0, m[0] + q[0] * r * o1, m[1] + q[1] * r * o1);
    for (const [o, b] of st) g.addColorStop(Math.min(1, Math.max(0, (o - o0) / ((o1 - o0) || 1))), col(hex, b));
    c.fillStyle = g; c.fill();
  } };
}
// an ellipsoid (centre, unit axes, radii), optionally cut by half-spaces {n, d}: n·(p − c) ≥ d is kept.  Samples on the unit sphere,
// plus the exact cut circles; the picture is the convex hull of the projected points, shaded radially from the brightest visible point.
function ellipSamples(cen, ax, rad, cuts, nLat, nLon) {
  const cs = (cuts || []).map(k => { const m = [rad[0] * dot(ax[0], k.n), rad[1] * dot(ax[1], k.n), rad[2] * dot(ax[2], k.n)], mm = Math.hypot(m[0], m[1], m[2]) || 1; return { m: [m[0] / mm, m[1] / mm, m[2] / mm], dl: k.d / mm } });
  const ok = s => { for (const k of cs) if (k.m[0] * s[0] + k.m[1] * s[1] + k.m[2] * s[2] < k.dl - 1e-7) return false; return true };
  const out = [], put = s => out.push({ p: [cen[0] + ax[0][0] * rad[0] * s[0] + ax[1][0] * rad[1] * s[1] + ax[2][0] * rad[2] * s[2], cen[1] + ax[0][1] * rad[0] * s[0] + ax[1][1] * rad[1] * s[1] + ax[2][1] * rad[2] * s[2], cen[2] + ax[0][2] * rad[0] * s[0] + ax[1][2] * rad[1] * s[1] + ax[2][2] * rad[2] * s[2]],
    n: nrm([ax[0][0] * s[0] / rad[0] + ax[1][0] * s[1] / rad[1] + ax[2][0] * s[2] / rad[2], ax[0][1] * s[0] / rad[0] + ax[1][1] * s[1] / rad[1] + ax[2][1] * s[2] / rad[2], ax[0][2] * s[0] / rad[0] + ax[1][2] * s[1] / rad[1] + ax[2][2] * s[2] / rad[2]]) });
  for (let i = 0; i <= nLat; i++) { const ph = -Math.PI / 2 + Math.PI * i / nLat, cp = Math.cos(ph), sp = Math.sin(ph); const nl = i === 0 || i === nLat ? 1 : nLon;
    for (let j = 0; j < nl; j++) { const th = j / nl * Math.PI * 2, s = [cp * Math.cos(th), cp * Math.sin(th), sp]; if (ok(s)) put(s) } }
  for (const k of cs) { if (Math.abs(k.dl) >= 1) continue; const r = Math.sqrt(1 - k.dl * k.dl), u = nrm(crs(k.m, Math.abs(k.m[2]) < .9 ? Z : [1, 0, 0])), v = crs(k.m, u);
    for (let j = 0; j < 28; j++) { const t = j / 28 * Math.PI * 2, s = [k.m[0] * k.dl + r * (u[0] * Math.cos(t) + v[0] * Math.sin(t)), k.m[1] * k.dl + r * (u[1] * Math.cos(t) + v[1] * Math.sin(t)), k.m[2] * k.dl + r * (u[2] * Math.cos(t) + v[2] * Math.sin(t))]; if (ok(s)) put(s) } }
  return out;
}
function ellipPart(L, d, cen, ax, rad, cuts, hex, mat, occ, extra) {
  const sm = ellipSamples(cen, ax, rad, cuts, 9, 18); if (sm.length < 3) return null;
  const pts = hull(sm.map(q => P(q.p))), path = polyPath(pts);
  return { L, d, pts, path, sm, ol: 'full', oc: hex, paint: c => {
    c.beginPath(); path(c);
    const vis = sm.filter(q => dot(q.n, VW) > .02);
    if (!vis.length) { c.fillStyle = col(hex, .75 * (occ || 1)); c.fill(); if (extra) extra(c); return }
    let best = vis[0], bb = -1; for (const q of vis) { q.b = bri(q.n, mat, occ); if (q.b > bb) { bb = q.b; best = q } }
    const p0 = P(best.p); let R = 1e-4; for (const p of pts) R = Math.max(R, Math.hypot(p[0] - p0[0], p[1] - p0[1]));
    const bin = [0, 0, 0, 0], cnt = [0, 0, 0, 0]; for (const q of vis) { const pp = P(q.p), t = Math.min(.999, Math.hypot(pp[0] - p0[0], pp[1] - p0[1]) / R); const k = t * 4 | 0; bin[k] += q.b; cnt[k]++ }
    const g = c.createRadialGradient(p0[0], p0[1], 0, p0[0], p0[1], R); g.addColorStop(0, col(hex, bb));
    let last = bb; for (let k = 0; k < 4; k++) { if (cnt[k]) last = bin[k] / cnt[k]; g.addColorStop((k + .6) / 4, col(hex, last)) }
    c.fillStyle = g; c.fill(); if (extra) extra(c);
  } };
}
// a box (centre, unit axes, half sizes): the visible faces, each flat-lit, with a darker edge
function boxPart(L, d, cen, ax, hs, hex, mat, opt) {
  const cr = []; for (const a of [-1, 1]) for (const b of [-1, 1]) for (const e of [-1, 1]) cr.push(add(cen, add(mul(ax[0], a * hs[0]), add(mul(ax[1], b * hs[1]), mul(ax[2], e * hs[2])))));
  const pts = hull(cr.map(P)), path = polyPath(pts);
  const faces = []; for (let i = 0; i < 3; i++) for (const s of [-1, 1]) { const n = mul(ax[i], s); if (dot(n, VW) <= .01) continue;
    const j = (i + 1) % 3, k = (i + 2) % 3, fc = add(cen, mul(ax[i], s * hs[i]));
    faces.push({ n, i, s, q: [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([u, v]) => P(add(fc, add(mul(ax[j], u * hs[j]), mul(ax[k], v * hs[k]))))) }) }
  return { L, d, pts, path, paint: c => {
    for (const f of faces) { c.beginPath(); polyPath(f.q)(c); c.fillStyle = col(hex, bri(f.n, mat) * (opt && opt.face ? opt.face(f) : 1)); c.fill() }
    if (opt && opt.deco) opt.deco(c, faces);
    c.beginPath(); path(c); c.strokeStyle = col(hex, .45); c.lineWidth = .012 * SCALE; c.stroke();
  } };
}
function linePart(L, d, list, hex, w, mat, cap) {   // a polyline of world points (straps, handles, cane, fork)
  const pts2 = list.map(P), half = w * SCALE / 2;
  const pts = []; for (const p of pts2) pts.push([p[0] - half, p[1] - half], [p[0] + half, p[1] + half]);
  return { L, d, pts: hull(pts), path: c => { c.moveTo(pts2[0][0], pts2[0][1]); for (let i = 1; i < pts2.length; i++) c.lineTo(pts2[i][0], pts2[i][1]) }, stroke: true, w: w * SCALE,
    paint: c => { c.beginPath(); c.moveTo(pts2[0][0], pts2[0][1]); for (let i = 1; i < pts2.length; i++) c.lineTo(pts2[i][0], pts2[i][1]); c.lineCap = cap || 'round'; c.lineJoin = 'round'; c.strokeStyle = col(hex, mat ? bri(Z, mat) : 1); c.lineWidth = w * SCALE; c.stroke() } };
}
function discPart(L, d, cen, r, th, hexTop, hexSide, mat) {   // a horizontal disc (table top, plate): side band, then the top
  const a = P(cen), b = P([cen[0], cen[1], cen[2] - th]), R = r * SCALE, Ry = R * ky(cen[2]);   // p670: a flat disc is an ellipse in the people's camera
  const el = (c0, n) => { const o = []; for (let i = 0; i < n; i++) { const t = i / n * Math.PI * 2; o.push([c0[0] + Math.cos(t) * R, c0[1] + Math.sin(t) * Ry]) } return o };
  const pts = hull(el(a, 24).concat(el(b, 24)));
  return { L, d, pts, path: polyPath(pts), ol: 'full', oc: hexSide, paint: c => {
    c.beginPath(); polyPath(pts)(c); c.fillStyle = col(hexSide, .78); c.fill();
    const g = c.createRadialGradient(a[0] - R * .35, a[1] - Ry * .45, R * .05, a[0], a[1], R * 1.05); g.addColorStop(0, col(hexTop, bri(Z, mat) * 1.06)); g.addColorStop(1, col(hexTop, bri(Z, mat) * .9));
    c.beginPath(); c.ellipse(a[0], a[1], R, Ry, 0, 0, Math.PI * 2); c.fillStyle = g; c.fill();
  } };
}

// ---- the body ----
function dims(L) {
  const h = L.h || 1.76, hs = h / 1.76, w = L.w || 1, bel = L.belly || 1, kid = h < 1.5, hk = kid ? Math.pow(hs, .45) : hs;
  return { h, hs, w, bel, kid, hk,
    hipZ: .53 * h, hipS: .08 * w * hs, thigh: .245 * h, shin: .243 * h, ankZ: .045 * h,
    armS: .166 * w * hs, shZ: .79 * h, uarm: .168 * h, farm: .146 * h,   // p670: the shoulders
    rT: .068 * hs * (.88 + .12 * w), rK: .05 * hs, rA: .036 * hs, rU: .044 * hs * (.9 + .1 * w), rE: .036 * hs, rW: .029 * hs, rHd: .045 * hs,
    neck0: .812 * h, neck1: .875 * h, rN: .051 * hs, headZ: .93 * h, head: [.077 * hk, .094 * hk, .114 * hk] };   // p670: the head of a man (15 × 19 × 23 cm), the neck, the hand
}
// the torso cross-sections (z, half width, half depth) by the kind of top; the hem decides how low the cloth goes
function torsoRings(D, top) {
  const h = D.h, w = D.w * D.hs, dd = D.hs, b = D.bel;
  const R = [[.6 * h, .136 * w * (1 + (b - 1) * .6), .093 * dd * (1 + (b - 1) * 1.6)], [.7 * h, .156 * w, .104 * dd * (1 + (b - 1) * .5)], [.76 * h, .165 * w * (top === 'suit' ? 1.04 : 1), .098 * dd],
    [.795 * h, .168 * w * (top === 'suit' ? 1.05 : 1), .088 * dd], [.82 * h, .118 * w, .066 * dd]];   // p670: the chest, the shoulder line, the trapezius (the neck shows)
  const hem = { tee: [.49 * h, .146 * w * (1 + (b - 1) * .5), .098 * dd * (1 + (b - 1) * 1.2)], shirt: [.525 * h, .14 * w * (1 + (b - 1) * .5), .095 * dd * (1 + (b - 1) * 1.3)],
    suit: [.43 * h, .162 * w * (1 + (b - 1) * .4), .104 * dd * (1 + (b - 1) * 1.1)], coat: [.3 * h, .2 * w, .135 * dd], labcoat: [.33 * h, .19 * w, .128 * dd], kid: [.5 * h, .148 * w, .1 * dd] }[top] || [.5 * h, .145 * w, .098 * dd];
  const out = [hem]; if (top === 'coat' || top === 'labcoat') out.push([.45 * h, .17 * w, .112 * dd]); return out.concat(R);
}
function gaitFoot(u, side, step, h) {   // the planted-foot gait: stance 60 % (the foot moves back linearly — no slide), swing 40 %
  const q = ((u + (side > 0 ? .5 : 0)) % 1 + 1) % 1;
  if (q < .6) return { a: step * (.6 - 2 * q), lift: 0, heel: q > .44 ? (q - .44) / .16 : 0, q };
  const t = (q - .6) / .4, sm = t * t * (3 - 2 * t); return { a: step * (-.6 + 1.2 * sm), lift: .04 * h * Math.sin(Math.PI * t), heel: Math.max(0, 1 - t * 2.5), q };
}
function ik(H, A, L1, L2, bend) {
  let dv = sub(A, H), d = Math.hypot(dv[0], dv[1], dv[2]); const mx = (L1 + L2) * .9995;
  if (d > mx) { dv = mul(dv, mx / d); A = add(H, dv); d = mx }
  const u = mul(dv, 1 / d), a = (L1 * L1 - L2 * L2 + d * d) / (2 * d), hh = Math.sqrt(Math.max(0, L1 * L1 - a * a));
  const n = nrm(sub(bend, mul(u, dot(bend, u))));
  return { knee: add(add(H, mul(u, a)), mul(n, hh)), ank: A };
}
const STEP = (D, item) => .216 * D.h * (item === 'shopping' || item === 'toolbox' ? .9 : 1);   // 29.10 02:25 — 28 % shorter than the first sample (.3 h): the body is drawn at 0.6, the ground is not

const PX34 = { comb, ik, add, sub, mul, nrm, dot, crs, lrp, Z, gaitFoot };   // W17: the helpers for the riders' pose (074zd_w17_kit.js — G.P34X.pose)
function pose(look, act, dir, fr) {
  const L = look, D = dims(look), k = act.k, F = FR[k] || 1, u = F > 1 ? fr / F : 0, item = (look.item && look.item.k) || '';
  const hd = dir * Math.PI / 4, f = [Math.cos(hd), Math.sin(hd), 0], l = [Math.sin(hd), -Math.cos(hd), 0];
  const walking = k === 'walk' || k === 'drag' || k === 'carry';
  // the upper body turns a little toward the camera in the side views (E / W) so that both arms read; the hips half of that
  const tw = .3 * Math.cos(hd), rot = (v, a) => [v[0] * Math.cos(a) - v[1] * Math.sin(a), v[0] * Math.sin(a) + v[1] * Math.cos(a), 0];
  const swing = walking ? Math.sin(u * Math.PI * 2) : 0;
  const fU = rot(f, tw - .06 * swing), lU = rot(l, tw - .06 * swing), fH = rot(f, tw * .5 + .07 * swing), lH = rot(l, tw * .5 + .07 * swing);
  const O = [0, 0, 0], step = STEP(D, item);
  const S = { D, f, l, fU, lU, k, item, sit: k === 'eat' || k === 'bench', table: k === 'eat', u, dir, props: [] };
  // ---- legs and pelvis ----
  let pelZ = D.hipZ, shift = 0, lean = 0, pitch = 0;
  if (walking) pelZ -= .02 * D.h * (1 + Math.cos(u * Math.PI * 4)) / 2;
  if (k === 'wait') shift = .022 * Math.sin(u * Math.PI * 2);
  if (k === 'eat') { pelZ = .5 * D.h * .52 + .08 * D.hs; lean = .12 }
  else if (k === 'bench') { pelZ = .46 + .08 * D.hs; lean = -.04 }   // p581: the bench seat at 0.46 for everyone
  const pel = comb(O, l, 0, l, shift, pelZ);
  S.pel = pel; S.legs = [];
  for (const side of [1, -1]) {   // +1 left, −1 right
    const hip = comb(pel, fH, 0, lH, side * D.hipS, 0);
    let ank, bend = f, heelZ = 0, toeA = (L.shoes && L.shoes.t === 'leather' ? .082 : .072) * D.hs;
    if (S.sit) { ank = comb(O, f, S.table ? D.thigh * .93 + .09 * D.hs : D.thigh * .6 + .04 * D.hs, l, side * D.hipS * 1.15, D.ankZ); bend = nrm(add(f, mul(Z, 2.2))) }
    else if (walking) { const g = gaitFoot(u, side, step, D.h); ank = comb(O, f, g.a, l, side * D.hipS * .9, D.ankZ + g.lift + g.heel * .05 * D.hs); heelZ = g.heel * .05 * D.hs }
    else { ank = comb(O, f, side > 0 ? .02 : -.01, l, side * (D.hipS + .02) - shift * .2, D.ankZ) }
    const j = ik(hip, ank, D.thigh, D.shin, bend);
    const toe = add(j.ank, add(mul(f, toeA), [0, 0, -D.ankZ + .028 - heelZ * .6])), heel = add(j.ank, add(mul(f, -.028 * D.hs), [0, 0, -D.ankZ + .03]));
    toe[2] = Math.max(.025, toe[2]); heel[2] = Math.max(.028, heel[2]);
    S.legs.push({ side, hip, knee: j.knee, ank: j.ank, toe, heel, y: dot(lH, [0, 1, 0]) * side });
  }
  // ---- torso, neck, head ----
  const tc = comb(O, fU, lean * .25, lU, shift * .6, 0);   // the torso's ground centre
  S.torsoAt = z => comb(tc, fU, lean * (z - pelZ), lU, 0, 0);
  S.pelZ = pelZ; S.lean = lean;
  const bob = walking ? pelZ - D.hipZ : (S.sit ? pelZ - D.hipZ : 0);
  S.dz = bob;   // the torso rides on the pelvis
  if (k === 'wait') pitch = u > .45 && u < .8 ? .45 : .05;
  if (k === 'eat') pitch = .25 + .12 * Math.sin(u * Math.PI * 2);
  if (k === 'bench') pitch = .08;
  const nb = add(S.torsoAt(D.neck0 + bob), [0, 0, D.neck0 + bob]), nt = add(S.torsoAt(D.neck1 + bob), [fU[0] * .012, fU[1] * .012, D.neck1 + bob]);
  S.neck = [nb, nt];
  const ef = nrm(add(mul(fU, Math.cos(pitch)), mul(Z, -Math.sin(pitch)))), ez = nrm(add(mul(Z, Math.cos(pitch)), mul(fU, Math.sin(pitch))));
  S.head = { c: add(add(S.torsoAt(D.headZ + bob), [0, 0, D.headZ + bob]), add(mul(fU, .016 * D.hs), mul(ef, .01 * D.hs))), ax: [lU, ef, ez], r: D.head };
  // ---- arms: the upper arm and forearm directions in the upper-body frame (a forward, s outward, z up) ----
  S.arms = [];
  const amp = .34, fwdOf = side => { if (!walking) return 0; const g = gaitFoot(u, -side, step, D.h); return g.a / (.6 * step) };
  for (const side of [1, -1]) {
    let d1, d2, hold = null;
    const right = side < 0;
    if (walking) {
      const s = fwdOf(side); let A = amp * s, out = .06, flex = .18 + .26 * Math.max(0, s);
      if (k === 'drag' && right) { A = -.34; out = .13; flex = .06 }
      else if (k === 'carry' || ((item === 'briefcase' || item === 'toolbox') && right) || item === 'shopping') { A = .13 * s; out = item === 'shopping' ? .2 : .14; flex = .04 }
      d1 = [Math.sin(A), out, -Math.cos(A)]; d2 = [Math.sin(A + flex), out * .6, -Math.cos(A + flex)];
    } else if (k === 'marshal') {
      const w = Math.sin(u * Math.PI * 2);   // "come ahead": the wands beat from overhead toward the face
      d1 = [.3, .6, .74]; d2 = [.18 + .3 * (w * .5 + .5), .26 - .7 * (w * .5 + .5), .95 - .4 * (w * .5 + .5)];
    } else if (k === 'stop') { d1 = [.22, .52, .82]; d2 = [.22, -.8, .55] }
    else if (k === 'bench') { d1 = [.3, .16, -.94]; d2 = [.96, -.1, -.26] }   // p581: the hands rest on the thighs
    else if (k === 'eat') {
      if (right) { const t = .5 - .5 * Math.cos(u * Math.PI * 2);   // the fork: from the plate up to the mouth and back
        d1 = [.55 - .1 * t, .22, -.8 + .55 * t]; d2 = [.95 - .55 * t, -.05 - .2 * t, .05 + .85 * t] }
      else { d1 = [.5, .25, -.82]; d2 = [.97, -.18, .05] }
    } else if (k === 'wait') {
      if (!right && u > .4 && u < .85) { d1 = [.22, .2, -.95]; d2 = [.55, -.82, .25] }   // looks at the watch
      else if (right && item === 'cane') { d1 = [.28, .16, -.95]; d2 = [.5, .05, -.86] }
      else { d1 = [.04, .08, -1]; d2 = [.12, .04, -1] }
    } else if (k.length === 2 && k[0] === 'f' && G.FISHX) { const q = G.FISHX.armsFor(k, fr, right); d1 = q[0]; d2 = q[1] }   // p641
    else { d1 = [.03, .07, -1]; d2 = [.1, .03, -1] }
    const W = v => nrm(add(add(mul(fU, v[0]), mul(lU, v[1] * side)), mul(Z, v[2])));
    const sh = add(add(S.torsoAt(D.shZ + bob), [0, 0, D.shZ + bob]), add(mul(lU, side * D.armS), mul(fU, -.008)));
    const el = add(sh, mul(W(d1), D.uarm)), wd = W(d2), wr = add(el, mul(wd, D.farm)), hand = add(wr, mul(wd, .052 * D.hs));   // p670: the hand of a man
    S.arms.push({ side, sh, el, wr, hand, wd });
  }
  if (G.P34X && G.P34X.pose) try { G.P34X.pose(S, L, act, fr, PX34) } catch (e) { G.P34X.err = String(e && e.message || e) }   // W17: the riders (k 'ride')
  return S;
}

// ---- the looks: colours and kinds ----
const DEF = { h: 1.76, w: 1, belly: 1, skin: '#d9a57f', hair: { t: 'short', c: '#3b2a1f' }, top: { t: 'tee', c: '#3d7fc4' }, legs: { t: 'trousers', c: '#2d3a4f' }, shoes: { t: 'sneaker', c: '#e9ecef' } };

// ---- the parts of one person in one pose ----
function parts(look, act, dir, fr, small, lod) {
  KW = act.k !== 'bench' && act.k !== 'eat'; LOD = lod || 0; RIDE = !!(G.P34X && G.P34X.cam && G.P34X.cam(act));   // W17
  try { return parts0(look, act, dir, fr, small, LOD) } finally { KW = false; LOD = 0; RIDE = false }
}
function parts0(look, act, dir, fr, small, lod) {
  const L = small ? smallLook(Object.assign({}, DEF, look)) : Object.assign({}, DEF, look), S = pose(L, act, dir, fr), D = S.D, out = [], F = S.f, fU = S.fU, lU = S.lU;
  const yv = p => p[1];   // the depth key: the world y (south = toward the camera)
  const torsoY = S.torsoAt(1)[1], headD = Math.max(S.head.c[1], torsoY + .02);
  const top = L.top || {}, legs = L.legs || {}, shoes = L.shoes || {}, item = L.item || {};
  const legMat = legs.t === 'jeans' ? MAT.denim : (legs.t === 'suit' ? MAT.wool : MAT.cloth);
  const legBias = S.sit ? -.02 - .3 : -.15;
  // legs: thigh, shin, the shoe (sole and upper)
  for (const g of S.legs) {
    const far = g.y < -.02 ? .86 : 1, base = (g.hip[1] + g.ank[1]) / 2 + legBias + g.y * .01;
    /* D‑593: the cuts of the wardrobe (legs.cut, shoes.cut, shoes.shaft) — a look without them is drawn exactly as before */
    const shortLeg = legs.t === 'shorts', kneeCut = lrp(g.hip, g.knee, 1.08), lcut = legs.cut || '', sportS = shortLeg && lcut === 'sport', cargo = !shortLeg && lcut === 'cargo', jogger = !shortLeg && lcut === 'jogger', sandal = shoes.t === 'sandal', scut = shoes.cut || '';
    if (sportS) { out.push(limbPart('body', base - .0004, lrp(g.hip, g.knee, .42), g.knee, D.rT * .9, D.rK * .93, L.skin, MAT.skin, far)); out.push(limbPart('body', base, g.hip, lrp(g.hip, g.knee, .6), D.rT * 1.03, D.rT * 1.02, legs.c, legMat, far)) }   // short sport shorts: the cloth to the middle of the thigh
    else out.push(limbPart('body', base, g.hip, g.knee, cargo ? D.rT * 1.05 : D.rT, cargo ? D.rK * 1.12 : D.rK, legs.c, legMat, far));
    if (shortLeg) { out.push(limbPart('body', base + .001, sportS ? g.knee : kneeCut, g.ank, D.rK * .86, D.rA, L.skin, MAT.skin, far)); if (!sandal) out.push(limbPart('body', base + .002, lrp(kneeCut, g.ank, sportS ? .9 : .8), g.ank, D.rA * 1.12, D.rA * 1.1, L.socks || '#f1f2f4', MAT.cloth, far)) }
    const st_ = shoes.t || 'sneaker', boot = st_ === 'boot' && (!shortLeg || !!shoes.shaft);
    // a boot: the trouser leg ends at the top of the shaft and is drawn over it (the leg goes into the boot)
    if (lod >= 2 && !shortLeg && !lcut && legs.t !== 'jeans' && dot(F, VW) > -.15) { const cp = linePart('body', base + (boot ? .0063 : .0013), [add(lrp(g.hip, g.knee, .2), mul(F, D.rT * .9)), add(g.knee, mul(F, D.rK * .97)), add(lrp(g.knee, g.ank, boot ? .62 : .86), mul(F, D.rA * 1.12))], col2hex(legs.c, 1.2), .0042 * D.hs, null), c0 = cp.paint; cp.paint = c => { c.globalAlpha = .5; c0(c); c.globalAlpha = 1 }; out.push(cp) }   // p670: the crease
    if (!shortLeg) out.push(limbPart('body', base + (boot ? .006 : .001), g.knee, boot ? add(g.ank, [0, 0, .095 * D.hs]) : g.ank, cargo ? D.rK * 1.12 : D.rK, D.rA * (cargo ? 1.36 : 1.12), legs.c, legMat, far));
    if (cargo) { const sd = mul(lU, g.side); if (sd[1] > -.2) { const pc = add(lrp(g.hip, g.knee, .66), mul(sd, D.rT * .74));   // D‑593: the side pocket of cargo trousers, its flap
        out.push(linePart('body', base + .0066, [add(pc, [0, 0, .042 * D.hs]), add(pc, [0, 0, -.042 * D.hs])], col2hex(legs.c, .84), .056 * D.hs, null, 'butt'));
        out.push(linePart('body', base + .0067, [add(pc, [0, 0, .044 * D.hs]), add(pc, [0, 0, .02 * D.hs])], col2hex(legs.c, .68), .06 * D.hs, null, 'butt')) } }
    if (jogger) { out.push(limbPart('body', base + (boot ? .0061 : .0012), lrp(g.knee, g.ank, boot ? .5 : .85), lrp(g.knee, g.ank, boot ? .6 : .98), D.rA * 1.22, D.rA * 1.17, col2hex(legs.c, .68), legMat, far));   // D‑593: joggers — the ribbed cuff, the stripe down the side
      if (D.hs * SCALE > .9) { const sd = mul(lU, g.side * .9); out.push(linePart('body', base + .0065, [add(lrp(g.hip, g.knee, .12), mul(sd, D.rT * .97)), add(g.knee, mul(sd, D.rK * .97)), add(lrp(g.knee, g.ank, boot ? .52 : .83), mul(sd, D.rA * 1.08))], legs.c2 || '#f1f1ee', .012 * D.hs, null)) } }
    if (sportS && D.hs * SCALE > .9) { const sd = mul(lU, g.side * .9); out.push(linePart('body', base + .0065, [add(lrp(g.hip, g.knee, .08), mul(sd, D.rT * 1.0)), add(lrp(g.hip, g.knee, .57), mul(sd, D.rT * 1.0))], legs.c2 || '#f1f1ee', .012 * D.hs, null)) }
    if (legs.t === 'jeans' && D.hs * SCALE > .9) { const sd = mul(lU, g.side * .9); out.push(linePart('body', base + .0065, [add(lrp(g.hip, g.knee, .15), mul(sd, D.rT * .95)), add(g.knee, mul(sd, D.rK * .95)), add(lrp(g.knee, g.ank, .9), mul(sd, D.rA * 1.05))], '#7f9cc4', .006, null)) }
    // the shoe (29.10 02:25): 0.6 of a real shoe like the body (~16 cm); a thin sole rim; a toe box (low) and a heel counter (higher),
    // so it reads as a shoe and not a capsule; a shape per kind; a main colour (c) and a second one (c2)
    const c1 = shoes.c || '#e9ecef', c2 = shoes.c2 || (st_ === 'sneaker' ? '#c0392b' : st_ === 'leather' ? '#2a1a10' : '#26211c'), hs_ = D.hs;
    const f3 = nrm(sub(g.toe, g.heel)), lat = nrm(crs(Z, f3)), up3 = nrm(crs(f3, lat)), outer = mul(lat, -g.side);   // lat points to the foot's right; the outer side of the left foot (+1) is its left
    const ax3 = [lat, f3, up3], at3 = (p, a, u) => add(add(p, mul(f3, a)), mul(up3, u));
    const solC = st_ === 'sneaker' ? '#eef0f2' : c2, upMat = st_ === 'sneaker' ? MAT.plastic : (st_ === 'boot' ? { s: .3, p: 14 } : MAT.leather);
    const lea = st_ === 'leather', mid = lrp(g.heel, g.toe, .5);
    const sole = sandal ? ellipPart('body', base + .003, at3(mid, .004 * hs_, .001), ax3, [.034 * hs_, .088 * hs_, .0075 * hs_], null, c2, MAT.sole, far)   // D‑593: a sandal — the foot in skin on a flat sole
      : ellipPart('body', base + .003, at3(mid, .002 * hs_, .002), ax3, [(lea ? .029 : .033) * hs_, .082 * hs_, (boot ? .011 : .008) * hs_], null, solC, MAT.sole, far);
    const toeBox = sandal ? ellipPart('body', base + .004, at3(g.toe, -.027 * hs_, .017 * hs_), ax3, [.0265 * hs_, .056 * hs_, .0155 * hs_], null, L.skin, MAT.skin, far)
      : ellipPart('body', base + .004, at3(g.toe, -.022 * hs_, .016 * hs_), ax3, [(lea ? .024 : .029) * hs_, (lea ? .062 : .054) * hs_, (lea ? .016 : .02) * hs_], null, c1, upMat, far);
    const heelC = boot ? null : sandal ? ellipPart('body', base + .004 + (dot(f3, [0, 1, 0]) < 0 ? .0002 : -.0002), at3(g.heel, .012 * hs_, .024 * hs_), ax3, [.026 * hs_, .036 * hs_, .026 * hs_], null, L.skin, MAT.skin, far)
      : ellipPart('body', base + .004 + (dot(f3, [0, 1, 0]) < 0 ? .0002 : -.0002), at3(g.heel, .012 * hs_, .028 * hs_), ax3, [.03 * hs_, .042 * hs_, .032 * hs_], null, c1, upMat, far);
    for (const p_ of [sole, toeBox, heelC]) if (p_) out.push(p_);
    const outerVis = outer[1] > -.3;
    if (sandal) {   // D‑593: two straps across the foot, one behind the heel
      for (const [t, hg] of [[.4, .047], [.7, .035]]) { const b0 = lrp(g.heel, g.toe, t), m = add(b0, mul(up3, hg * hs_));
        out.push(linePart('body', base + .0046, [add(add(b0, mul(lat, .031 * hs_)), mul(up3, .009 * hs_)), add(m, mul(lat, .017 * hs_)), add(m, mul(lat, -.017 * hs_)), add(add(b0, mul(lat, -.031 * hs_)), mul(up3, .009 * hs_))], c1, .014 * hs_, MAT.leather, 'butt')) }
      out.push(linePart('body', base + .004 + (dot(f3, [0, 1, 0]) < 0 ? .0007 : -.0007), [add(at3(g.heel, .014 * hs_, .03 * hs_), mul(lat, .027 * hs_)), at3(g.heel, -.024 * hs_, .037 * hs_), add(at3(g.heel, .014 * hs_, .03 * hs_), mul(lat, -.027 * hs_))], c1, .011 * hs_, MAT.leather, 'round'));
    } else if (st_ === 'sneaker' && scut === 'hightop') {   // D‑593: a canvas high-top — the collar round the ankle (under a long trouser leg), the white rubber toe cap, three lace bars, the round patch
      const cd = shortLeg ? .005 : .0008;
      out.push(limbPart('body', base + cd, add(g.ank, [0, 0, -.014]), add(g.ank, [0, 0, .066 * hs_]), .04 * hs_, .0385 * hs_, c1, MAT.cloth, far));
      out.push(limbPart('body', base + cd + .0002, add(g.ank, [0, 0, .052 * hs_]), add(g.ank, [0, 0, .066 * hs_]), .0395 * hs_, .039 * hs_, c2, MAT.cloth, far));
      { const cap = ellipPart('body', base + .0043, at3(g.toe, -.008 * hs_, .013 * hs_), ax3, [.0275 * hs_, .027 * hs_, .0165 * hs_], null, '#f1f1ee', MAT.plastic, far); if (cap) out.push(cap) }
      for (const t of [.5, .63, .76]) { const m = add(lrp(g.heel, g.toe, t), mul(up3, .037 * hs_)); out.push(linePart('body', base + .0046, [add(m, mul(lat, .012 * hs_)), add(m, mul(lat, -.012 * hs_))], '#f7f7f5', .005 * hs_, { s: 0, p: 1 }, 'butt')) }
      if (outerVis && shortLeg && lod >= 1) { const e = ellipPart('body', base + .0054, add(add(g.ank, [0, 0, .03 * hs_]), mul(outer, .037 * hs_)), ax3, [.008 * hs_, .013 * hs_, .013 * hs_], null, '#f4f4f2', MAT.plastic, far); if (e) out.push(e) }
    } else if (st_ === 'sneaker' && scut === 'runner') {   // D‑593: a running shoe — the thick wedge under the heel in the second colour, a curved stripe, a heel tab, three lace bars
      { const wedge = ellipPart('body', base + .0032, at3(g.heel, .024 * hs_, .008 * hs_), ax3, [.0345 * hs_, .052 * hs_, .018 * hs_], null, c2, MAT.plastic, far); if (wedge) out.push(wedge) }
      if (outerVis) out.push(linePart('body', base + .0045, [add(at3(g.heel, 0, .02 * hs_), mul(outer, .03 * hs_)), add(at3(mid, -.004 * hs_, .041 * hs_), mul(outer, .026 * hs_)), add(at3(mid, .036 * hs_, .015 * hs_), mul(outer, .029 * hs_))], c2, .0105 * hs_, { s: 0, p: 1 }, 'round'));
      for (const t of [.52, .64, .76]) { const m = add(lrp(g.heel, g.toe, t), mul(up3, .036 * hs_)); out.push(linePart('body', base + .0046, [add(m, mul(lat, .012 * hs_)), add(m, mul(lat, -.012 * hs_))], c2, .005 * hs_, { s: 0, p: 1 }, 'butt')) }
      out.push(linePart('body', base + .004 + (dot(f3, [0, 1, 0]) < 0 ? .0007 : -.0007), [at3(g.heel, -.02 * hs_, .03 * hs_), at3(g.heel, -.024 * hs_, .06 * hs_)], c2, .012 * hs_, { s: 0, p: 1 }, 'round'));
    } else if (st_ === 'sneaker') {
      if (outerVis) out.push(linePart('body', base + .0045, [add(at3(g.heel, -.004 * hs_, .03 * hs_), mul(outer, .029 * hs_)), add(at3(mid, .028 * hs_, .02 * hs_), mul(outer, .028 * hs_))], c2, .009 * hs_, { s: 0, p: 1 }, 'round'));
      for (const t of [.55, .72]) { const m = add(lrp(g.heel, g.toe, t), mul(up3, .036 * hs_)); out.push(linePart('body', base + .0046, [add(m, mul(lat, .012 * hs_)), add(m, mul(lat, -.012 * hs_))], '#f7f7f5', .0055 * hs_, { s: 0, p: 1 }, 'butt')) }
    } else if (boot) {
      out.push(limbPart('body', base + .005, add(g.ank, [0, 0, -.012]), add(g.ank, [0, 0, .11 * hs_]), .041 * hs_, .04 * hs_, c1, upMat, far));
      out.push(limbPart('body', base + .0052, add(g.ank, [0, 0, .07 * hs_]), add(g.ank, [0, 0, .088 * hs_]), .0418 * hs_, .0415 * hs_, c2, MAT.leather, far));
    }
  }
  if (lod >= 2 && legs.t === 'jeans' && dot(S.f, VW) < -.3) for (const s of [1, -1]) {   // p670: the back pockets of jeans, orange stitches
    const q = (u, dz) => add(S.pel, add(add(mul(S.f, -.093 * D.hs), mul(S.l, s * u * D.hs)), [0, 0, dz * D.hs])), o = [q(.03, .035), q(.115, .035), q(.11, -.055), q(.072, -.075), q(.035, -.055), q(.03, .035)];
    const sp = linePart('body', torsoY - .02, o, '#c99a52', .0042 * D.hs, null), s0 = sp.paint; sp.paint = c => { c.globalAlpha = .85; s0(c); c.globalAlpha = 1 }; out.push(sp) }
  // the pelvis (the trousers between the legs and the shirt)
  { const pc = S.pel, a = [], hw = (D.hipS + D.rT * .95), hd = .09 * D.hs * (1 + (D.bel - 1) * .8);
    for (const dz of [-.07 * D.hs, .06 * D.hs]) for (let i = 0; i < 16; i++) { const t = i / 16 * Math.PI * 2; a.push(P(add(pc, add(add(mul(S.f, Math.cos(t) * hd), mul(S.l, Math.sin(t) * hw)), [0, 0, dz])))) }
    const pts = hull(a); out.push({ L: 'body', d: torsoY - .05, pts, path: polyPath(pts), paint: c => { c.beginPath(); polyPath(pts)(c); const g = c.createLinearGradient(pts.reduce((m, p) => Math.min(m, p[0]), 9), 0, pts.reduce((m, p) => Math.max(m, p[0]), -9), 0); g.addColorStop(0, col(legs.c, .84)); g.addColorStop(.5, col(legs.c, .74)); g.addColorStop(1, col(legs.c, .64)); c.fillStyle = g; c.fill() } }) }
  // arms (skin) and hands; sleeves are in the top layer
  const longSl = top.t === 'suit' || top.t === 'coat' || top.t === 'labcoat' || top.long;
  for (const a of S.arms) {
    const d = (a.el[1] + a.wr[1]) / 2, dU = (a.sh[1] + a.el[1]) / 2, far = (a.el[1] - torsoY) < -.04 && a.side * dot(lU, [0, 1, 0]) < -.2 ? .85 : 1;
    const dd = Math.max(d, dU);
    a.dd = dd + .01; a.far = far;
    { const up = limbPart('body', dU + .008, a.sh, a.el, D.rU, D.rE, L.skin, MAT.skin, far); up.olFrom = .35; out.push(up) }
    const fa = limbPart('body', dd + .009, a.el, a.wr, D.rE, D.rW, L.skin, MAT.skin, far); fa.arm = 'fore'; out.push(fa);
    const hp_ = ellipPart('body', Math.max(dd, a.hand[1]) + .012, a.hand, [lU, a.wd, nrm(crs(lU, a.wd))], [D.rHd * .52, D.rHd * 1.25, D.rHd * .9], null, L.gloves || L.skin, L.gloves ? MAT.cloth : MAT.skin, far); if (hp_) { hp_.arm = 'fore'; out.push(hp_) }
    if (lod >= 1) { const fw = nrm(sub(fU, mul(a.wd, dot(fU, a.wd)))), tp = ellipPart('body', Math.max(dd, a.hand[1]) + .0125, add(add(a.hand, mul(fw, D.rHd * .72)), mul(a.wd, -D.rHd * .3)), [lU, a.wd, fw], [D.rHd * .34, D.rHd * .66, D.rHd * .32], null, L.gloves || L.skin, L.gloves ? MAT.cloth : MAT.skin, far); if (tp) { tp.arm = 'fore'; out.push(tp) } }   // p670: the thumb
    if (L.gloves) { const gc = limbPart('body', dd + .0095, lrp(a.el, a.wr, .84), lrp(a.el, a.wr, 1.03), D.rW * 1.36, D.rW * 1.3, col2hex(L.gloves, .76), MAT.cloth, far); gc.arm = 'fore'; out.push(gc) }   // D‑593: work gloves — the hand and a cuff
    if (L.watch && a.side > 0) { const w0 = longSl ? .975 : .88, wb = limbPart('top', dd + .0104, lrp(a.el, a.wr, w0), lrp(a.el, a.wr, w0 + .1), D.rW * 1.2, D.rW * 1.2, L.watch.b || '#1d1f22', MAT.leather, far),   // D‑593: a watch on the left wrist — the strap and the case
        wf = limbPart('top', dd + .0105, lrp(a.el, a.wr, w0 + .028), lrp(a.el, a.wr, w0 + .072), D.rW * 1.44, D.rW * 1.44, L.watch.c || '#c9ced3', MAT.metal, far); wb.arm = wf.arm = 'fore'; out.push(wb, wf) }
  }
  // neck and head (skin); p670: the face is painted on the head (lod 1: the eyes and the brows; lod 2: the nose, the mouth, the glasses)
  out.push(limbPart('body', headD - .004, S.neck[0], S.neck[1], D.rN, D.rN * .92, L.skin, MAT.skin, .9));
  const capT = (L.hair && L.hair.t) || 'short', cap = capT !== 'none' && capT !== 'bald';   // with hair: the face is the head below the hairline, over the hair
  const H = S.head, headP = ellipPart('body', headD, H.c, H.ax, H.r, null, L.skin, MAT.skin, 1, lod >= 1 && !cap ? faceOf(H, L, lod) : null);
  out.push(headP);
  if (lod >= 1 && dot(H.ax[1], VW) > -.3) { const np = ellipPart(cap ? 'hair' : 'body', cap ? headD + .0106 : headD + .0004, add(H.c, add(mul(H.ax[1], H.r[1] * .93), mul(H.ax[2], -H.r[2] * .1))), H.ax, [.012 * D.hk, .017 * D.hk, .024 * D.hk], null, L.skin, MAT.skin, 1);
    if (np) { np.ol = lod >= 2 && Math.abs(H.ax[1][0]) > .55 ? 'full' : null; out.push(np) } }   // p670: the nose (its line only in profile)
  // ears (when the side of the head shows)
  for (const s of [1, -1]) { const ep = add(H.c, add(mul(H.ax[0], s * H.r[0] * .97), mul(H.ax[2], -.012))); if (dot(mul(H.ax[0], s), VW) > -.15) out.push(ellipPart('body', headD + .001 * (s * dot(H.ax[0], [0, 1, 0]) > 0 ? 1 : -1), ep, H.ax, [.012 * D.hk, .02 * D.hk, .028 * D.hk], null, L.skin, MAT.skin, .95)) }

  // ---- the top layer: the torso by bands, sleeves, collar, belt, placket, lapels, tie, the vest ----
  /* D‑593: the cuts of the wardrobe (top.cut): polo — untucked, a short placket of two buttons; tank — no sleeves; sweater, hoodie — a little wider, knitted bands */
  const tcut = top.cut || '', polo = tcut === 'polo', knit = tcut === 'sweater' || tcut === 'hoodie';
  const tKind = top.t === 'polo' || top.t === 'shirt' ? 'shirt' : (top.t || 'tee'), rings = (rg => knit ? rg.map((r, i) => i < rg.length - 1 ? [r[0], r[1] * 1.045, r[2] * 1.075] : r) : rg)(torsoRings(D, D.kid ? 'kid' : polo ? 'tee' : tKind));
  const ringPts = (rg, n) => { const [z, hw, hd] = rg, cc = add(S.torsoAt(z + S.dz), [0, 0, z + S.dz]), o = []; for (let i = 0; i < n; i++) { const t = i / n * Math.PI * 2; o.push(add(cc, add(mul(fU, Math.cos(t) * hd), mul(lU, Math.sin(t) * hw)))) } return o };
  const tMat = tKind === 'suit' ? MAT.wool : (tKind === 'coat' ? MAT.wool : MAT.cloth), tc = top.c || '#3d7fc4', hs = D.hs;
  const bandParts = (rgs, hex, mat, Lr, d0) => { for (let i = 0; i < rgs.length - 1; i++) {
    const r0 = rgs[i], r1 = rgs[i + 1], pts = hull(ringPts(r0, 20).concat(ringPts(r1, 20)).map(P)), path = polyPath(pts);
    out.push({ L: Lr, d: d0 + i * .0005, pts, path, paint: c => {
      const st = [], dz = (r1[0] - r0[0]) || 1;
      for (let j = 0; j < 28; j++) { const t = j / 28 * Math.PI * 2, hw = (r0[1] + r1[1]) / 2, hd = (r0[2] + r1[2]) / 2;
        const nh = nrm(add(mul(fU, Math.cos(t) / hd), mul(lU, Math.sin(t) / hw))), rr0 = Math.hypot(r0[2] * Math.cos(t), r0[1] * Math.sin(t)), rr1 = Math.hypot(r1[2] * Math.cos(t), r1[1] * Math.sin(t));
        const n = nrm(add(nh, [0, 0, -(rr1 - rr0) / dz])); if (dot(n, VW) <= 0) continue;
        const px = (fU[0] * Math.cos(t) * hd + lU[0] * Math.sin(t) * hw) * SCALE; st.push([px, bri(n, mat)]) }
      c.beginPath(); path(c); if (st.length < 2) { c.fillStyle = col(hex, .8); c.fill(); return }
      st.sort((a, b) => a[0] - b[0]); const cx = P(add(S.torsoAt((r0[0] + r1[0]) / 2), [0, 0, (r0[0] + r1[0]) / 2 + S.dz])), x0 = cx[0] + st[0][0], x1 = cx[0] + st[st.length - 1][0];
      const g = c.createLinearGradient(x0, cx[1], x1, cx[1]); for (const [px, b] of st) g.addColorStop(Math.min(1, Math.max(0, (cx[0] + px - x0) / ((x1 - x0) || 1))), col(hex, b));
      c.fillStyle = g; c.fill();
    } });
  } };
  { const bp = []; for (let i = 0; i < rings.length - 1; i++) bp.push(hull(ringPts(rings[i], 20).concat(ringPts(rings[i + 1], 20)).map(P)));   // p670: the line of the torso — under its bands
    out.push({ L: 'top', d: torsoY - .0002, pts: hull(bp.flat()), path: c => { for (const q of bp) polyPath(q)(c) }, paint: c => { if (!OWM) return; c.beginPath(); for (const q of bp) polyPath(q)(c); c.lineWidth = OWM * 2; c.strokeStyle = col(tc, .34); c.globalAlpha = .85; c.stroke(); c.globalAlpha = 1 } }) }
  bandParts(rings, tc, tMat, 'top', torsoY);
  // the top of the shoulders, lit (the cap of the highest ring)
  { const rt = rings[rings.length - 1], pts = hull(ringPts(rt, 20).map(P)); out.push({ L: 'top', d: torsoY + .003, pts, path: polyPath(pts), paint: c => { c.beginPath(); polyPath(pts)(c); c.fillStyle = col(tc, bri(Z, tMat) * 1.02); c.fill() } }) }
  const front = dot(fU, [0, 1, 0]), fz = z => add(S.torsoAt(z + S.dz), [0, 0, z + S.dz]);
  const onFront = (z, s, out_) => { const rr = rings.reduce((b, r) => Math.abs(r[0] - z) < Math.abs(b[0] - z) ? r : b, rings[0]); return add(fz(z), add(mul(fU, rr[2] * (out_ || 1.0) * Math.sqrt(Math.max(0, 1 - (s / rr[1]) ** 2))), mul(lU, s))) };
  const frontD = torsoY + front * .1, backD = torsoY - front * .1;
  // the collar: a ring around the neck base; its front half and back half sit at their own depths
  { const z = D.neck0 + S.dz - .004, cc = fz(D.neck0 - .004), rN = D.rN * 1.35, half = sgn => { const o = []; for (let i = 0; i <= 10; i++) { const t = (i / 10 - .5) * Math.PI; const v = add(mul(fU, sgn * Math.cos(t) * rN), mul(lU, Math.sin(t) * rN * 1.1)); o.push(add([cc[0], cc[1], z], v)) } return o };
    void cc;
    const plain = tKind === 'tee' || D.kid;
    const cFront = plain ? col2hex(tc, .74) : tKind === 'suit' ? (top.c2 || '#f3f4f6') : tKind === 'coat' || tKind === 'labcoat' ? col2hex(tc, .86) : (top.c2 || col2hex(tc, 1.12));
    const cBack = plain ? col2hex(tc, .74) : tKind === 'suit' || tKind === 'coat' ? col2hex(tc, .82) : (top.c2 || col2hex(tc, 1.12));
    if (tcut !== 'tank') for (const sg of [1, -1]) { const hp = half(sg), dd = dot(mul(fU, sg), [0, 1, 0]) > 0 ? headD + .002 : headD - .02;
      out.push(linePart('top', dd, hp, sg > 0 ? cFront : cBack, plain ? (knit ? (tcut === 'hoodie' ? .046 : .03) : .018) * D.hs : (tKind === 'coat' ? .04 : .03) * D.hs, plain ? { s: 0, p: 1 } : MAT.cloth)) }
  }
  if (L.scarf) {   // D‑593: a scarf — a thick ring round the neck, its end hanging in front
    const zs = D.neck0 + S.dz + .014 * D.hs, rS = D.rN * 1.5, c0 = fz(D.neck0), sc = L.scarf;
    for (const sg of [1, -1]) { const o = []; for (let i = 0; i <= 10; i++) { const t = (i / 10 - .5) * Math.PI; o.push(add([c0[0], c0[1], zs], add(mul(fU, sg * Math.cos(t) * rS), mul(lU, Math.sin(t) * rS * 1.08)))) }
      out.push(linePart('top', dot(mul(fU, sg), [0, 1, 0]) > 0 ? headD + .0025 : headD - .019, o, sc, .052 * D.hs, MAT.wool)) }
    if (front > -.25) { out.push(linePart('top', frontD + .0085, [onFront(D.neck0 - .012, .034 * D.hs, 1.14), onFront(.7 * D.h, .05 * D.hs, 1.1)], sc, .05 * D.hs, MAT.wool, 'butt'));
      out.push(linePart('top', frontD + .0086, [onFront(.712 * D.h, .05 * D.hs, 1.1), onFront(.7 * D.h, .05 * D.hs, 1.1)], col2hex(sc, .68), .05 * D.hs, MAT.wool, 'butt')) }
  }
  // shirt / polo: placket and buttons, tucked in with a belt
  if (tKind === 'shirt' && front > -.2) { const pl = [onFront(D.neck0 - .03 * D.hs, 0, 1.02), onFront((polo ? .712 : .6) * D.h, 0, 1.02)]; out.push(linePart('top', frontD + .003, pl, polo ? col2hex(tc, .8) : tc, (polo ? .022 : .012) * D.hs, { s: 0, p: 1 }, polo ? 'butt' : undefined));
    const bz = i => (polo ? .782 - i * .038 : .78 - i * .07) * D.h;
    for (let i = 0; i < (polo ? 2 : 3); i++) out.push(linePart('top', frontD + .004, [onFront(bz(i), 0, 1.04), onFront(bz(i) - .002, 0, 1.04)], '#f4f4f2', .012 * D.hs, MAT.plastic)) }
  if (((tKind === 'shirt' && !polo) || top.belt) && !D.kid) {   // the belt: a band all round at the hem, the buckle in front
    const z = rings[0][0] + .012 * D.hs, hw = rings[0][1] * 1.03, hd = rings[0][2] * 1.05, cc = fz(z);
    for (const sg of [1, -1]) { const o = []; for (let i = 0; i <= 12; i++) { const t = (i / 12 - .5) * Math.PI; o.push(add(cc, add(mul(fU, sg * Math.cos(t) * hd), mul(lU, Math.sin(t) * hw)))) }
      out.push(linePart('top', torsoY + sg * front * .1 + .003, o, L.belt || '#2a211b', .024 * D.hs, MAT.leather)) }
    if (front > -.1) out.push(boxPart('top', frontD + .006, onFront(z, 0, 1.08), [fU, lU, Z], [.006, .02 * D.hs, .014 * D.hs], '#c9b27a', MAT.metal));
  }
  // the suit: the V of the shirt and the tie in front, lapels
  if (tKind === 'suit' && front > -.25) { const zt = D.neck0 - .01, zb = .66 * D.h;
    const vL = onFront(zt, .055 * D.hs, 1.02), vR = onFront(zt, -.055 * D.hs, 1.02), vB = onFront(zb, 0, 1.03), pts = [vL, vR, vB].map(P);
    out.push({ L: 'top', d: frontD + .004, pts: hull(pts), path: polyPath(pts), paint: c => { c.beginPath(); polyPath(pts)(c); c.fillStyle = col(top.c2 || '#f3f4f6', .9); c.fill() } });
    if (!top.noTie) out.push(linePart('top', frontD + .005, [onFront(zt - .02, 0, 1.04), onFront(zb + .01, 0, 1.06)], top.tie || '#8c1d2a', .026 * D.hs, MAT.cloth));   /* D‑593: a suit without a tie — the open collar */
    for (const s of [1, -1]) out.push(linePart('top', frontD + .0055, [onFront(zt, s * .06 * D.hs, 1.03), onFront(zb + .012, s * .012, 1.05)], tc, .016 * D.hs, { s: .1, p: 6 }));
  }
  // p670: the details of the clothes, the apron, the stethoscope
  clothes(out, { L, D, S, top, tKind, tc, hs, rings, fz, onFront, frontD, backD, front, torsoY, fU, lU, lod });
  // the coat: two rows of buttons
  if (tKind === 'coat' && front > -.2) for (const s of [1, -1]) for (let i = 0; i < 3; i++) { const z = (.72 - i * .09) * D.h; out.push(linePart('top', frontD + .004, [onFront(z, s * .05 * D.hs, 1.04), onFront(z - .002, s * .05 * D.hs, 1.04)], '#1d1a17', .016 * D.hs, MAT.plastic)) }
  // a hi-vis vest over the top: its own torso from the waist to the shoulders, two silver bands round, braces over the shoulders
  if (L.vest) { const vr = torsoRings(D, 'tee').slice(0, 4).map((r, i) => [i === 0 ? .56 * D.h : r[0], r[1] * 1.07, r[2] * 1.1]);
    bandParts(vr, L.vest, L.vestK === 'fish' ? MAT.cloth : MAT.hivis, 'top', torsoY + .0065);
    if (L.vestK === 'fish') { if (front > -.3) for (const s of [1, -1]) for (const zz of [.7, .615]) { const z = zz * D.h;   // p641: the fishing vest — four pockets with flaps
      out.push(linePart('top', frontD + .012, [onFront(z, s * .062 * D.hs, 1.16), onFront(z - .05 * D.h, s * .062 * D.hs, 1.16)], col2hex(L.vest, .72), .058 * D.hs, MAT.cloth));
      out.push(linePart('top', frontD + .013, [onFront(z + .004 * D.h, s * .062 * D.hs, 1.17), onFront(z - .012 * D.h, s * .062 * D.hs, 1.17)], col2hex(L.vest, .55), .062 * D.hs, MAT.cloth)) } }
    else for (const zz of [.62, .69]) { const z = zz * D.h, hw = vr[1][1] * 1.02, hd = vr[1][2] * 1.03, cc = fz(z);
      for (const sg of [1, -1]) { const o = []; for (let i = 0; i <= 12; i++) { const t = (i / 12 - .5) * Math.PI; o.push(add(cc, add(mul(fU, sg * Math.cos(t) * hd), mul(lU, Math.sin(t) * hw)))) }
        out.push(linePart('top', torsoY + sg * front * .1 + .008, o, '#d8dde2', .03 * D.hs, MAT.refl)) } }
    if (L.vestK !== 'fish') for (const s of [1, -1]) for (const sg of [1, -1]) { const o = [fz(.6 * D.h), fz(.77 * D.h), fz(.805 * D.h)].map((p, i) => add(p, add(mul(fU, sg * (i === 2 ? .03 : .1) * D.hs), mul(lU, s * .085 * D.hs))));
      out.push(linePart('top', torsoY + sg * front * .1 + .009, o, '#d8dde2', .026 * D.hs, MAT.refl)) }
  }
  // sleeves
  for (const a of S.arms) {
    if (tcut === 'tank') { const sk_ = ellipPart('top', a.dd - .001, add(a.sh, [0, 0, -.008]), [lU, fU, Z], [D.rU * 1.2, D.rU * 1.24, D.rU * 1.3], null, L.skin, MAT.skin, a.far); if (sk_) out.push(sk_); continue }   // D‑593: sleeveless — the bare shoulder over the cloth
    const sl = longSl ? 1 : (top.sleeve != null ? top.sleeve : .5), end = lrp(a.sh, a.el, Math.min(1, sl * 1.0));
    const r0 = D.rU * 1.25, r1 = D.rE * 1.22, rm = r0 + (r1 - r0) * Math.min(1, sl);
    { const sp = limbPart('top', a.dd - .001, add(a.sh, [0, 0, -.006]), end, r0 * .9, rm, tc, tMat, a.far); sp.olFrom = .35; out.push(sp) }   // p670: the sleeve from the shoulder; its line below the cap
    if (longSl) { const s1 = limbPart('top', a.dd + .0001, a.el, lrp(a.el, a.wr, .92), r1, D.rW * 1.32, tc, tMat, a.far), s2 = limbPart('top', a.dd + .0002, lrp(a.el, a.wr, .86), lrp(a.el, a.wr, .97), D.rW * 1.36, D.rW * 1.32, col2hex(tc, .78), tMat, a.far); s1.arm = s2.arm = 'fore'; out.push(s1, s2) }
    else out.push(limbPart('top', a.dd - .0005, lrp(a.sh, a.el, sl * .88), end, rm * 1.02, rm * 1.03, col2hex(tc, .82), tMat, a.far));
  }
  // ---- the hair layer: hair, beard, hat, ear defenders ----
  const hair = L.hair && /^(long|curly|side)$/.test(L.hair.t) ? Object.assign({}, L.hair, { t: 'short' }) : (L.hair || {}), hat = L.hat || null, beard = L.beard || null;   // p583: short hair for everyone
  const ef = H.ax[1], ez = H.ax[2], el = H.ax[0];
  const hr = (k) => H.r.map(v => v * k);
  if (beard) {   // the beard: the ellipsoid below the cheekbones in front; what the rest of the head hides is erased in the same layer
    const nb = nrm(add(mul(ef, .62), mul(ez, -.78))), cut = { n: nb, d: .012 * D.hk };
    const bp = ellipPart('hair', headD + (dot(nb, VW) < 0 ? .006 : .0108), H.c, H.ax, hr(1.07), [cut], beard.c || hair.c || '#3b2a1f', MAT.hair, .92); if (bp) out.push(bp);
    const rest = ellipSamples(H.c, H.ax, H.r, [{ n: mul(nb, -1), d: -cut.d }], 8, 16).map(q => P(q.p));
    if (rest.length > 2 && dot(nb, VW) < 0) { const pts = hull(rest); out.push({ L: 'hair', d: headD + .0065, pts, path: polyPath(pts), erase: true, paint: c => { c.globalCompositeOperation = 'destination-out'; c.beginPath(); polyPath(pts)(c); c.fill(); c.globalCompositeOperation = 'source-over' } }) }
  }
  if (hair.t && hair.t !== 'none' && hair.t !== 'bald') {
    const style = ({ short: [1.05, -.74, .67, -.004], crop: [1.03, -.74, .67, .004], curly: [1.12, -.66, .75, -.02], side: [1.07, -.72, .69, -.01], long: [1.1, -.5, .87, -.05] }[hair.t] || [1.05, -.74, .67, -.004]).slice();   // p670: the hairline higher — the forehead shows
    if (small) { style[0] = 1 + (style[0] - 1) * .4; style[3] += .022 }   // less hair seen from above in the small pictures
    const nh = nrm(add(mul(ef, style[1]), mul(ez, style[2]))), hp = ellipPart('hair', headD + .01, H.c, H.ax, hr(style[0]), [{ n: nh, d: style[3] * D.hk }], hair.c, MAT.hair, 1,
      hair.t === 'curly' ? c => { c.save(); c.clip(); c.fillStyle = 'rgba(255,255,255,.07)'; const p0 = P(H.c); for (let i = 0; i < 7; i++) { const a = i * 2.4; c.beginPath(); c.arc(p0[0] + Math.cos(a) * .05 * SCALE * D.hk, p0[1] + Math.sin(a) * .05 * SCALE * D.hk - .04 * SCALE, .022 * SCALE * D.hk, 0, Math.PI * 2); c.fill() } c.restore() } : (lod >= 2 ? strands(H, hair.c, style[0]) : null));
    if (hp) { if (hair.t === 'curly') { const p0 = hp.pts; hp.pts = hull(p0.flatMap(p => circ2(p, .012 * SCALE * D.hk, 6))); hp.path = polyPath(hp.pts) } out.push(hp) }
    // p670: the face — the head below the hairline, over the hair where it faces the camera (the cap of hair is convex: its edge would cross the forehead)
    const fb = ellipPart('hair', dot(ef, VW) > -.05 ? headD + .0105 : headD + .0095, H.c, H.ax, H.r, [{ n: mul(nh, -1), d: -style[3] * D.hk }, { n: ef, d: -.15 * H.r[1] }], L.skin, MAT.skin, 1, lod >= 1 ? faceOf(H, L, lod) : null); if (fb) out.push(fb);
  } else if (hair.t === 'bald' && !hat) {   // the fringe above the ears and round the back
    for (const s of [1, -1]) { const ctr = add(H.c, add(add(mul(el, s * H.r[0] * .93), mul(ef, -H.r[1] * .25)), mul(ez, .01))); if (dot(mul(el, s), VW) > -.3) out.push(ellipPart('hair', headD + .01 + (s * dot(el, [0, 1, 0]) > 0 ? .002 : -.03), ctr, H.ax, [.022 * D.hk, .06 * D.hk, .035 * D.hk], null, hair.c || '#bdbdbd', MAT.hair, .95)) }
    if (dot(mul(ef, -1), VW) > -.2) out.push(ellipPart('hair', headD + .009, add(H.c, add(mul(ef, -H.r[1] * .9), mul(ez, -.005))), H.ax, [.06 * D.hk, .02 * D.hk, .035 * D.hk], null, hair.c || '#bdbdbd', MAT.hair, .95));
  }
  if (hat && G.P34X && G.P34X.hat && G.P34X.hat[hat.t]) try { G.P34X.hat[hat.t](out, { H, ef, ez, el, headD, D, hat, lod, L, ellipPart, discPart, linePart, P, MAT, col, hull, polyPath, add, sub, mul, nrm, dot, SCALE, VW }) } catch (e) { G.P34X.err = String(e && e.message || e) }   // W17: the riders' helmets
  else if (hat) {
    if (hat.t === 'hat') {   // a brimmed hat: the brim (a disc), then the crown with its band
      const sun = hat.cut === 'sun', bz = H.c[2] + H.r[2] * (sun ? .6 : .52), bc = [H.c[0], H.c[1], bz], hc = hat.c || '#16181b';   /* D‑593: the wide sun hat — a wider brim, a low round crown, a ribbon (hat.b) */
      out.push(discPart('hair', headD + .02, bc, (sun ? .17 : .148) * D.hk, .008, hc, hc, MAT.wool));
      const cr = (sun ? [[0, .088, .1], [.05, .084, .096], [.088, .06, .07]] : [[0, .088, .1], [.07, .085, .098], [.12, .07, .082]]).map(([dz, a, b]) => { const o = []; for (let i = 0; i < 20; i++) { const t = i / 20 * Math.PI * 2; o.push(P([bc[0] + (ef[0] * Math.cos(t) * b + el[0] * Math.sin(t) * a) * D.hk, bc[1] + (ef[1] * Math.cos(t) * b + el[1] * Math.sin(t) * a) * D.hk, bz + dz * D.hk])) } return o });
      const pts = hull(cr.flat()); out.push({ L: 'hair', d: headD + .021, pts, path: polyPath(pts), paint: c => { c.beginPath(); polyPath(pts)(c); const x0 = Math.min(...pts.map(p => p[0])), x1 = Math.max(...pts.map(p => p[0]));
        const g = c.createLinearGradient(x0, 0, x1, 0); g.addColorStop(0, col(hc, 1.05)); g.addColorStop(.5, col(hc, .86)); g.addColorStop(1, col(hc, .7)); c.fillStyle = g; c.fill();
        c.beginPath(); polyPath(hull(cr[2]))(c); c.fillStyle = col(hc, 1.12); c.fill();
        c.beginPath(); polyPath(hull(cr[0].concat(cr[0].map(p => [p[0], p[1] - .022 * SCALE * D.hk]))))(c); c.save(); c.clip(); c.beginPath(); polyPath(pts)(c); c.fillStyle = 'rgba(0,0,0,.35)'; if (!hat.b) c.fill(); c.restore();
        if (hat.b) { const lift = cr[0].map(p => [p[0], p[1] - .02 * SCALE * D.hk]);   // D‑593: a ribbon in its own colour — a band at the foot of the crown, the crown above it drawn again
          c.beginPath(); polyPath(hull(cr[0].concat(lift)))(c); c.fillStyle = col(hat.b, .95); c.fill();
          c.beginPath(); polyPath(hull(lift.concat(cr[1], cr[2])))(c); c.fillStyle = g; c.fill(); c.beginPath(); polyPath(hull(cr[2]))(c); c.fillStyle = col(hc, 1.12); c.fill() } } });
    } else if (hat.t === 'bucket') {   // D‑593: a bucket hat — a soft crown with a flat top and a short brim that slopes down
      const bz = H.c[2] + H.r[2] * .54, bc = [H.c[0], H.c[1], bz], hc = hat.c || '#a89a6a';
      const ring = (dz, a, b) => { const o = []; for (let i = 0; i < 20; i++) { const t = i / 20 * Math.PI * 2; o.push(P([bc[0] + (ef[0] * Math.cos(t) * b + el[0] * Math.sin(t) * a) * D.hk, bc[1] + (ef[1] * Math.cos(t) * b + el[1] * Math.sin(t) * a) * D.hk, bz + dz * D.hk])) } return o };
      const sets = [[ring(-.016, .118, .127), ring(.014, .09, .101)], [ring(.014, .088, .099), ring(.088, .08, .09)]];
      sets.forEach((rr, k) => { const pts = hull(rr.flat()); out.push({ L: 'hair', d: headD + .02 + k * .001, pts, path: polyPath(pts), ol: 'full', oc: hc, paint: c => { c.beginPath(); polyPath(pts)(c);
        const x0 = Math.min(...pts.map(p => p[0])), x1 = Math.max(...pts.map(p => p[0])), g = c.createLinearGradient(x0, 0, x1, 0); g.addColorStop(0, col(hc, k ? 1.08 : .97)); g.addColorStop(.55, col(hc, k ? .9 : .8)); g.addColorStop(1, col(hc, k ? .74 : .66)); c.fillStyle = g; c.fill();
        if (k) { c.beginPath(); polyPath(hull(rr[1]))(c); c.fillStyle = col(hc, 1.14); c.fill() } } }) });
    } else if (hat.t === 'beanie') {   // D‑593: a knitted cap — the dome, the turned-up band, a pompom
      const hc = hat.c || '#7a7f87', nb = nrm(add(mul(ef, -.2), mul(ez, .98)));
      { const dome = ellipPart('hair', headD + .021, H.c, H.ax, [H.r[0] * 1.1, H.r[1] * 1.1, H.r[2] * 1.17], [{ n: nb, d: .2 * H.r[2] }], hc, MAT.wool, 1); if (dome) out.push(dome) }
      { const band = ellipPart('hair', headD + .0215, H.c, H.ax, hr(1.14), [{ n: nb, d: .13 * H.r[2] }, { n: mul(nb, -1), d: -.43 * H.r[2] }], col2hex(hc, .78), MAT.wool, 1); if (band) out.push(band) }
      { const pom = ellipPart('hair', headD + .022, add(H.c, mul(ez, H.r[2] * 1.22)), H.ax, [.03 * D.hk, .03 * D.hk, .028 * D.hk], null, hat.b || col2hex(hc, 1.3), MAT.wool, 1); if (pom) out.push(pom) }
    } else if (hat.t === 'chef') {   // p670: the chef's hat — a band and the puff
      const hc = hat.c || '#f6f6f2'; out.push(limbPart('hair', headD + .02, add(H.c, mul(H.ax[2], H.r[2] * .45)), add(H.c, mul(H.ax[2], H.r[2] * 1.3)), .084 * D.hk, .088 * D.hk, hc, MAT.cloth, 1));
      const pf = ellipPart('hair', headD + .021, add(H.c, mul(H.ax[2], H.r[2] * 1.55)), H.ax, [.108 * D.hk, .104 * D.hk, .068 * D.hk], null, hc, MAT.cloth, 1, lod >= 2 ? c => { c.save(); c.clip(); c.strokeStyle = col(hc, .78); c.lineWidth = .004 * SCALE; for (const u of [-.6, -.2, .2, .6]) { const a = P(add(H.c, add(mul(H.ax[0], u * .1 * D.hk), mul(H.ax[2], H.r[2] * 1.3)))), b = P(add(H.c, add(mul(H.ax[0], u * .11 * D.hk), mul(H.ax[2], H.r[2] * 1.75)))); c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke() } c.restore() } : null); if (pf) out.push(pf);
    } else if (hat.t === 'peak') {   // p670: the peaked cap of a uniform — the band, the crown (wider than the head), the black visor, the badge
      const hc = hat.c || '#1b2b45', bc = hat.b || col2hex(hc, .55), fr = dot(ef, [0, 1, 0]) > -.3;
      out.push(discPart('hair', headD + .02, add(H.c, mul(ez, H.r[2] * .84)), .086 * D.hk, H.r[2] * .4, bc, bc, MAT.cloth));
      out.push(discPart('hair', headD + .0205, add(H.c, add(mul(ez, H.r[2] * .84 + .022 * D.hk), mul(ef, H.r[1] * .1))), .106 * D.hk, .022 * D.hk, hc, col2hex(hc, .78), MAT.wool));
      { const vc = add(H.c, add(mul(ef, H.r[1] * .9), mul(ez, H.r[2] * .5))), o = []; for (let i = 0; i <= 12; i++) { const t = (i / 12 - .5) * Math.PI; o.push(P(add(vc, add(mul(ef, Math.cos(t) * .036 * D.hk), add(mul(el, Math.sin(t) * .062 * D.hk), mul(ez, -Math.cos(t) * .006 * D.hk)))))) }
        const pts = hull(o); out.push({ L: 'hair', d: headD + (fr ? .0215 : -.05), pts, path: polyPath(pts), ol: 'full', oc: '#0e1012', paint: c => { c.beginPath(); polyPath(pts)(c); c.fillStyle = col('#16181b', fr ? 1.25 : .9); c.fill() } }) }
      if (lod >= 1 && dot(ef, [0, 1, 0]) > -.15) out.push(ellipPart('hair', headD + .0222, add(H.c, add(mul(ef, H.r[1] * .99), mul(ez, H.r[2] * .66))), H.ax, [.016 * D.hk, .006 * D.hk, .015 * D.hk], null, hat.e || '#d4af37', MAT.metal, 1));
    } else if (hat.t === 'garrison') {   // p670: the side cap of a steward — long, folded, tilted to one side, the company's pin
      const hc = hat.c || '#1b2b45';
      out.push(ellipPart('hair', headD + .021, add(H.c, add(mul(ez, H.r[2] * .9), mul(el, H.r[0] * .16))), H.ax, [.042 * D.hk, .102 * D.hk, .036 * D.hk], [{ n: ez, d: -.011 * D.hk }], hc, MAT.wool, 1));
      if (lod >= 1 && Math.abs(dot(el, [0, 1, 0])) < .95) out.push(ellipPart('hair', headD + .0215, add(H.c, add(add(mul(ez, H.r[2] * .9), mul(el, H.r[0] * (dot(el, [0, 1, 0]) > 0 ? .5 : -.2))), mul(ef, H.r[1] * .45))), H.ax, [.008 * D.hk, .012 * D.hk, .01 * D.hk], null, hat.e || '#d4af37', MAT.metal, 1));
    } else if (hat.t === 'helmet' || hat.t === 'cap') {
      const isH = hat.t === 'helmet', hc = hat.c || '#f2c418';
      if (isH) out.push(discPart('hair', headD + .02, add(H.c, mul(ez, H.r[2] * .36)), .108 * D.hk, .006, hc, hc, MAT.plastic));   // p670: the hat sits on the head, the eyes show under it
      const dome = ellipPart('hair', headD + .021, H.c, H.ax, hr(isH ? 1.13 : 1.08), [{ n: nrm(add(mul(ef, isH ? -.05 : -.35), mul(ez, .95))), d: (isH ? .3 : .06) * H.r[2] }], hc, isH ? MAT.plastic : MAT.cloth, 1,
        isH && lod >= 2 ? c => { c.beginPath(); for (let i = 0; i <= 10; i++) { const a = -1.15 + i * .21, q = P(add(H.c, add(mul(ef, H.r[1] * 1.14 * Math.sin(a)), mul(ez, H.r[2] * 1.14 * Math.cos(a))))); i ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1]) } c.lineWidth = .014 * SCALE * D.hk; c.strokeStyle = col(hc, 1.18); c.stroke(); c.lineWidth = .004 * SCALE; c.strokeStyle = col(hc, .7); c.stroke() } : null); if (dome) out.push(dome);
      if (!isH) { const vc = add(H.c, add(mul(ef, H.r[1] * 1.0), mul(ez, H.r[2] * .52))), o = []; for (let i = 0; i <= 12; i++) { const t = (i / 12 - .5) * Math.PI; o.push(P(add(vc, add(mul(ef, Math.cos(t) * .052 * D.hk), mul(el, Math.sin(t) * .066 * D.hk))))) }
        const pts = hull(o); out.push({ L: 'hair', d: headD + (dot(ef, [0, 1, 0]) > -.3 ? .022 : -.05), pts, path: polyPath(pts), paint: c => { c.beginPath(); polyPath(pts)(c); c.fillStyle = col(hc, .92); c.fill() } }) }
    }
  }
  if (L.earmuff) {   // the ear defenders of the ramp: two cups and the band over the head
    for (const s of [1, -1]) { const ctr = add(H.c, add(mul(el, s * H.r[0] * 1.15), mul(ez, -.008))); out.push(ellipPart('hair', headD + .015 + s * dot(el, [0, 1, 0]) * .05, ctr, H.ax, [.022 * D.hk, .04 * D.hk, .045 * D.hk], null, L.earmuff, MAT.plastic, 1)) }
    const arc = []; for (let i = 0; i <= 10; i++) { const t = (i / 10) * Math.PI; arc.push(add(H.c, add(mul(el, Math.cos(t) * H.r[0] * 1.18), mul(ez, Math.sin(t) * H.r[2] * 1.12 - .008)))) }
    out.push(linePart('hair', headD + .016, arc, '#2a2d31', .018 * D.hk, MAT.plastic));
  }
  // ---- items ----
  const R = S.arms.find(a => a.side < 0), Lf = S.arms.find(a => a.side > 0);
  const hang = (a, hs, hex, mat, deco) => { const top = add(a.hand, [0, 0, -.05 * D.hs - hs[2]]); return boxPart('item', a.hand[1] + .015 + (a.side * dot(lU, [0, 1, 0]) > 0 ? .02 : -.02), top, [fU, lU, Z], hs, hex, mat, deco) };
  const handle = (a, b, w, hex) => linePart('item', (a[1] + b[1]) / 2 + .02, [a, b], hex, w, MAT.plastic);
  const it = item.k;
  if (it === 'suitcase') {   // dragged on its wheels, tilted toward the hand
    const grip = R.hand, back = mul(S.f, -1), Wg = add(add(grip, mul(back, .3 * D.hs)), [0, 0, 0]); Wg[2] = .035;   // 29.10 02:25: a cabin case, close behind the hand
    const axis = nrm(sub(grip, Wg)), cl = .5 * D.hs, side = nrm(crs(axis, S.l)), cen = add(Wg, mul(axis, cl / 2));
    const hs = [.085 * D.hs, .15 * D.hs, cl / 2], ax = [nrm(crs(S.l, axis)), S.l, axis];
    const dep = cen[1]; void side;
    out.push(boxPart('item', dep, cen, ax, hs, item.c || '#24406b', MAT.plastic, { deco: (c, faces) => { for (const f of faces) if (f.i === 0) { const q = f.q; c.strokeStyle = 'rgba(255,255,255,.18)'; c.lineWidth = .008 * SCALE; c.beginPath(); for (let j = 1; j < 4; j++) { const t = j / 4; c.moveTo(q[0][0] + (q[1][0] - q[0][0]) * t, q[0][1] + (q[1][1] - q[0][1]) * t); c.lineTo(q[3][0] + (q[2][0] - q[3][0]) * t, q[3][1] + (q[2][1] - q[3][1]) * t) } c.stroke() } } }));
    const topC = add(cen, mul(axis, cl / 2)); for (const s of [1, -1]) out.push(linePart('item', (topC[1] + grip[1]) / 2 + .001, [add(topC, mul(S.l, s * .06 * D.hs)), add(grip, mul(S.l, s * .05 * D.hs))], '#9aa3ad', .012 * D.hs, MAT.metal));
    { const gc = P(add(Wg, mul(axis, .0))), gt = P([cen[0], cen[1], 0]), rr = .17 * SCALE * D.hs, pts = hull(circ2(gc, rr, 10).concat(circ2(gt, rr, 10)));
      out.push({ L: 'item', d: -9, pts, path: polyPath(pts), under: true, paint: c => { const m = [(gc[0] + gt[0]) / 2 + .05 * SCALE, (gc[1] + gt[1]) / 2 + .04 * SCALE], g = c.createRadialGradient(m[0], m[1], 0, m[0], m[1], rr * 1.5); g.addColorStop(0, 'rgba(10,13,18,.36)'); g.addColorStop(1, 'rgba(10,13,18,0)'); c.fillStyle = g; c.beginPath(); c.arc(m[0], m[1], rr * 1.5, 0, Math.PI * 2); c.fill() } }) }
    for (const s of [1, -1]) out.push(ellipPart('item', Wg[1] - .01, add(Wg, mul(S.l, s * .12 * D.hs)), [S.f, S.l, Z], [.033 * D.hs, .016 * D.hs, .033 * D.hs], null, '#1d2024', MAT.plastic, 1));
  }
  if (it === 'backpack') {
    const cen = add(fz(.66 * D.h), mul(fU, -(.11 * D.hs + .08 * D.hs))), hs = [.075 * D.hs, .135 * D.hs, .17 * D.hs];
    out.push(boxPart('item', torsoY - front * .2, cen, [fU, lU, Z], hs, item.c || '#e0662a', MAT.cloth, { deco: (c, faces) => { const f = faces.find(q => q.i === 0 && q.s < 0); if (!f) return; const q = f.q; c.strokeStyle = 'rgba(0,0,0,.25)'; c.lineWidth = .01 * SCALE; c.beginPath(); c.moveTo((q[0][0] + q[3][0]) / 2, (q[0][1] + q[3][1]) / 2); c.lineTo((q[1][0] + q[2][0]) / 2, (q[1][1] + q[2][1]) / 2); c.stroke() } }));
    for (const s of [1, -1]) { const o = [onFront(.6 * D.h, s * .085 * D.hs, 1.06), onFront(.74 * D.h, s * .09 * D.hs, 1.07), add(fz(.81 * D.h), mul(lU, s * .08 * D.hs)), add(fz(.79 * D.h), add(mul(fU, -.1 * D.hs), mul(lU, s * .08 * D.hs)))];
      out.push(linePart('item', frontD + .01, o.slice(0, 3), col2hex(item.c || '#e0662a', .7), .024 * D.hs, MAT.cloth)) }
  }
  if (it === 'shoulderbag') {
    const cen = add(fz(.5 * D.h), add(mul(lU, .2 * D.hs), mul(fU, .02))), side = dot(lU, [0, 1, 0]);
    out.push(boxPart('item', torsoY + side * .2, cen, [fU, lU, Z], [.12 * D.hs, .035 * D.hs, .1 * D.hs], item.c || '#5a3b26', MAT.leather));
    out.push(linePart('item', frontD + .011, [add(cen, [0, 0, .1 * D.hs]), onFront(.72 * D.h, .02, 1.06), add(fz(.815 * D.h), mul(lU, -.09 * D.hs))], col2hex(item.c || '#5a3b26', .7), .018 * D.hs, MAT.leather));
  }
  if (it === 'briefcase') { out.push(hang(R, [.19 * D.hs, .045 * D.hs, .14 * D.hs], item.c || '#3a2618', MAT.leather)); out.push(handle(add(R.hand, mul(fU, -.05)), add(R.hand, mul(fU, .05)), .014 * D.hs, '#1c140e')) }
  if (it === 'toolbox') { out.push(hang(R, [.17 * D.hs, .075 * D.hs, .075 * D.hs], item.c || '#c43a2a', MAT.plastic, { deco: (c, faces) => { for (const f of faces) if (f.i === 2 && f.s > 0) { c.strokeStyle = 'rgba(0,0,0,.35)'; c.lineWidth = .008 * SCALE; c.beginPath(); c.moveTo((f.q[0][0] + f.q[1][0]) / 2, (f.q[0][1] + f.q[1][1]) / 2); c.lineTo((f.q[2][0] + f.q[3][0]) / 2, (f.q[2][1] + f.q[3][1]) / 2); c.stroke() } } }));
    out.push(handle(add(R.hand, mul(fU, -.06)), add(R.hand, mul(fU, .06)), .016 * D.hs, '#222')) }
  if (it === 'shopping') { const cs = item.c || ['#d84a3a', '#c9a46a']; for (const [i, a] of [R, Lf].entries()) { out.push(hang(a, [.12 * D.hs, .055 * D.hs, .15 * D.hs], cs[i % cs.length], MAT.paper)); for (const s of [1, -1]) out.push(handle(a.hand, add(a.hand, add(mul(fU, s * .07 * D.hs), [0, 0, -.06 * D.hs])), .008 * D.hs, '#2b2b2b')) } }
  if (it === 'cane') { const top = R.hand, foot = add(comb([0, 0, 0], fU, .26 * D.hs, lU, -.22 * D.hs, 0), [0, 0, .01]); out.push(linePart('item', top[1] + .02, [add(top, mul(fU, -.04)), add(top, [0, 0, .02]), foot], '#3b2a1f', .02 * D.hs, MAT.wood)) }
  if (it === 'wands') { for (const a of S.arms) { const tip = add(a.hand, mul(a.wd, .36 * D.hs)); const glow = P(lrp(a.hand, tip, .6)), gr = .16 * SCALE * D.hs;
      out.push({ L: 'item', d: a.hand[1] + .02, pts: hull(circ2(glow, gr, 10)), path: polyPath(hull(circ2(glow, gr, 10))), noRim: true, paint: c => { const g = c.createRadialGradient(glow[0], glow[1], 0, glow[0], glow[1], gr); g.addColorStop(0, 'rgba(255,170,60,.42)'); g.addColorStop(1, 'rgba(255,140,40,0)'); c.fillStyle = g; c.beginPath(); c.arc(glow[0], glow[1], gr, 0, Math.PI * 2); c.fill() } });
      out.push(limbPart('item', a.hand[1] + .021, add(a.hand, mul(a.wd, .02)), tip, .018 * D.hs, .015 * D.hs, '#ff7a1a', MAT.glow, 1)); out.push(limbPart('item', a.hand[1] + .022, add(a.hand, mul(a.wd, -.03)), add(a.hand, mul(a.wd, .05)), .02 * D.hs, .02 * D.hs, '#222', MAT.plastic, 1)) } }
  if (S.table) {   // the table set: chair, table, plate, glass, the fork in the right hand.  The table top goes over the legs and the
    // lower torso; what rests on it or above it (the forearms, the hands, the plate) goes over the table.
    const ch = comb([0, 0, 0], S.f, -.06, S.l, 0, 0), sz = .46 * D.hs, legMax = Math.max(...out.filter(p => p.L === 'body' && p.d < torsoY - .1).map(p => p.d), torsoY - .2);
    const td = Math.max(torsoY, legMax) + .03;
    out.push(boxPart('item', ch[1] - .3, add(ch, [0, 0, sz]), [S.f, S.l, Z], [.2 * D.hs, .21 * D.hs, .015], '#6b6f75', MAT.metal));
    const bk = add(add(ch, mul(S.f, -.22 * D.hs)), [0, 0, sz + .2 * D.hs]);
    out.push(boxPart('item', bk[1] > torsoY ? torsoY + .04 : bk[1] - .2, bk, [S.f, S.l, Z], [.015, .2 * D.hs, .19 * D.hs], '#6b6f75', MAT.metal));
    for (const [a, s] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) { const b = add(ch, add(mul(S.f, a * .18 * D.hs), mul(S.l, s * .19 * D.hs))); out.push(linePart('item', b[1] - .45, [b, add(b, [0, 0, sz])], '#4d5157', .02 * D.hs, MAT.metal)) }
    const tcn = comb([0, 0, 0], S.f, .56 * D.hs, S.l, 0, .75 * D.hs), tdd = tcn[1] < torsoY - .2 ? tcn[1] - .5 : td;
    out.push(linePart('item', tdd - .002, [add(tcn, [0, 0, -.73 * D.hs]), tcn], '#3a3d42', .05 * D.hs, MAT.metal));
    out.push(discPart('item', tdd, tcn, .36 * D.hs, .03, '#e8e2d6', '#b5ab98', MAT.wood));
    const pl = comb([0, 0, 0], S.f, .33 * D.hs, S.l, -.03, .755 * D.hs);
    out.push(discPart('item', tdd + .004, pl, .11 * D.hs, .012, '#fbfbf8', '#d6d6d2', MAT.plastic));
    out.push(ellipPart('item', tdd + .005, add(pl, [0, 0, .012]), [S.f, S.l, Z], [.05 * D.hs, .06 * D.hs, .018], null, '#c9773a', MAT.cloth, 1));
    const gl = comb([0, 0, 0], S.f, .45 * D.hs, S.l, .18 * D.hs, .755 * D.hs); out.push(limbPart('item', tdd + .006, gl, add(gl, [0, 0, .12 * D.hs]), .03 * D.hs, .034 * D.hs, '#b8d6e6', MAT.metal, 1));
    // the forearms and hands rest on the table or above it — they go over it (when the table is not behind the person)
    if (tdd === td) for (const p of out) if ((p.L === 'body' || p.L === 'top') && p.arm === 'fore' && p.d < td + .01) p.d = td + .01 + (p.d - torsoY) * .001 + (p.L === 'top' ? .0005 : 0);
    out.push(linePart('item', Math.max(R.hand[1] + .03, tdd + .02), [R.hand, add(R.hand, mul(R.wd, .12 * D.hs))], '#c8cdd2', .008 * D.hs, MAT.metal));
  }
  return { parts: out.filter(Boolean), S };
}
// the small pictures: stronger, lighter clothes and lighter hair (the owner, 29.10 02:25: "at the game zoom the people read as dark spots")
function hsl(hex) { const c = hexC(hex).map(v => v / 255), mx = Math.max(...c), mn = Math.min(...c), l = (mx + mn) / 2; let h = 0, s = 0;
  if (mx !== mn) { const d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === c[0] ? (c[1] - c[2]) / d + (c[1] < c[2] ? 6 : 0) : mx === c[1] ? (c[2] - c[0]) / d + 2 : (c[0] - c[1]) / d + 4; h /= 6 } return [h, s, l] }
function hex3(h, s, l) { const f = n => { const k = (n + h * 12) % 12, a = s * Math.min(l, 1 - l), v = l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)); return Math.round(v * 255).toString(16).padStart(2, '0') }; return '#' + f(0) + f(8) + f(4) }
function vivid(hex, k) { if (!hex || hex[0] !== '#') return hex; const [h, s, l] = hsl(hex); return hex3(h, Math.min(1, s * 1.3 + .05), l + (.6 - l) * (k || .32)) }
function smallLook(L) { const o = Object.assign({}, L);
  o.top = Object.assign({}, L.top, { c: vivid(L.top.c), c2: L.top.c2 }); o.legs = Object.assign({}, L.legs, { c: vivid(L.legs.c, .22) }); o.shoes = Object.assign({}, L.shoes, { c: vivid(L.shoes.c, .2) });
  if (L.vest) o.vest = vivid(L.vest, .15);
  if (L.hair) o.hair = Object.assign({}, L.hair, { c: vivid(L.hair.c, .3) });
  if (L.hat) o.hat = Object.assign({}, L.hat, { c: vivid(L.hat.c, .28) });
  if (L.item && L.item.c) o.item = Object.assign({}, L.item, { c: Array.isArray(L.item.c) ? L.item.c.map(c => vivid(c, .2)) : vivid(L.item.c, .2) });
  return o }
// ---- p670: the face — on the head ellipsoid, where it faces the camera: the eyes (white, iris, pupil, the upper lid), the brows (the
// colour of the hair), the nostrils, the mouth, a little warmth on the cheeks, glasses.  lod 1 — the eyes as dark dots and the brows.
function faceOf(H, L, lod) { return c => {
  const at = (u, f, v) => { const s = nrm([u, f, v]), p = add(H.c, add(add(mul(H.ax[0], H.r[0] * s[0]), mul(H.ax[1], H.r[1] * s[1])), mul(H.ax[2], H.r[2] * s[2])));
    const n = nrm(add(add(mul(H.ax[0], s[0] / H.r[0]), mul(H.ax[1], s[1] / H.r[1])), mul(H.ax[2], s[2] / H.r[2]))); return { p, n, v: dot(n, VW) } };
  const ell = (q, ru, rv, fill, a, stroke) => { const tu = nrm(sub(H.ax[0], mul(q.n, dot(H.ax[0], q.n)))), tv = nrm(sub(H.ax[2], mul(q.n, dot(H.ax[2], q.n)))), A = PV(tu), B = PV(tv), o = P(q.p);
    c.save(); c.transform(A[0] * ru, A[1] * ru, B[0] * rv, B[1] * rv, o[0], o[1]); c.beginPath(); c.arc(0, 0, 1, 0, Math.PI * 2); c.restore();
    c.globalAlpha = a == null ? 1 : a; if (stroke) { c.lineWidth = stroke; c.strokeStyle = fill; c.stroke() } else { c.fillStyle = fill; c.fill() } c.globalAlpha = 1 };
  const k = H.r[2] / .114, sk = L.skin || '#d9a57f', hairC = (L.hair && L.hair.c) || '#3b2a1f', brow = mixHex(hairC, '#000000', .15), fine = lod >= 2;
  if (fine) for (const s of [1, -1]) { const q = at(s * .5, .74, -.22); if (q.v > .2) ell(q, .02 * k, .013 * k, '#d0604a', .1) }
  for (const s of [1, -1]) { const q = at(s * .37, .87, .08); if (q.v < .1) continue;
    if (fine) { ell(q, .016 * k, .0086 * k, '#f1ebe3'); ell(at(s * .35, .9, .08), .0079 * k, .0083 * k, L.eyes || '#3d2b1d'); ell(at(s * .35, .91, .085), .0036 * k, .0038 * k, '#0e0a08');
      ell(at(s * .37, .86, .155), .017 * k, .0038 * k, mixHex(sk, '#1a0f0a', .62)) }
    else ell(q, .0105 * k, .0085 * k, '#2a1d15', .92);
    const b = at(s * .38, .81, .33); if (b.v > .05) ell(b, .021 * k, (fine ? .0056 : .0062) * k, brow, .95) }
  if (fine) { const n = at(0, .97, -.25); if (n.v > .1) ell(n, .0115 * k, .0042 * k, mixHex(sk, '#2a140c', .45), .85);
    const m = at(0, .9, -.47); if (m.v > .1) { ell(m, .019 * k, .0043 * k, mixHex(sk, '#6a2a22', .62), .95); ell(at(0, .89, -.54), .012 * k, .003 * k, mixHex(sk, '#ffffff', .18), .6) } }
  if (L.glasses) { let e = []; for (const s of [1, -1]) { const q = at(s * .37, .9, .08); if (q.v > .12) { if (L.shades) { ell(q, .0225 * k, .0165 * k, '#14171b', .94); if (fine) ell(at(s * .33, .9, .12), .007 * k, .0035 * k, '#ffffff', .28) }   /* D‑593: sunglasses — dark lenses */ ell(q, .022 * k, .016 * k, L.glasses, .95, .0045 * SCALE * k); e.push(q) } }
    if (e.length === 2) { const a = P(e[0].p), b = P(e[1].p); c.beginPath(); c.moveTo(a[0] + (b[0] - a[0]) * .3, a[1]); c.lineTo(a[0] + (b[0] - a[0]) * .7, b[1]); c.lineWidth = .004 * SCALE * k; c.strokeStyle = L.glasses; c.stroke() } }
} }
// ---- p670: the hair — strands from the crown toward the forehead and the sides, lighter and darker, inside the hair
function strands(H, hc, m) { return c => { c.save(); c.clip(); const at = (u, f, v) => { const s = nrm([u, f, v]); return P(add(H.c, add(add(mul(H.ax[0], H.r[0] * m * s[0]), mul(H.ax[1], H.r[1] * m * s[1])), mul(H.ax[2], H.r[2] * m * s[2])))) };
  c.lineCap = 'round'; c.lineWidth = .0042 * SCALE * H.r[2] / .114;
  for (let i = -3; i <= 3; i++) { const u = i * .26; c.strokeStyle = i % 2 ? col(hc, 1.3) : col(hc, .72); c.globalAlpha = .3; c.beginPath();
    const p = [at(u * .25, -.75, .7), at(u * .55, -.25, 1), at(u * .85, .35, .9), at(u * 1.1, .8, .5)]; c.moveTo(p[0][0], p[0][1]); for (let j = 1; j < 4; j++) c.lineTo(p[j][0], p[j][1]); c.stroke() }
  c.globalAlpha = 1; c.restore() } }
// ---- p670: the details of the clothes — the collar points, the breast pocket, the folds over the belt, the back yoke (shirt); the zipper, the
// pockets and the hem band (jacket); the pockets (coat); the lab coat (the V of the scrubs, the lapels, the buttons, the pocket with pens); the
// V-neck; the stethoscope; the apron (front panel, neck strap, ties).  lod 1 — the zipper, the collar points, the apron; lod 2 — all.
function clothes(out, o) {
  const { L, D, top, tKind, tc, hs, rings, fz, onFront, frontD, backD, front, torsoY, fU, lU, lod } = o, h = D.h;
  if (D.kid && !L.apron) return;
  const onBack = (z, s) => { const rr = rings.reduce((b, r) => Math.abs(r[0] - z) < Math.abs(b[0] - z) ? r : b, rings[0]); return add(fz(z), add(mul(fU, -rr[2] * 1.03 * Math.sqrt(Math.max(0, 1 - (s / rr[1]) ** 2))), mul(lU, s))) };
  const seam = (list, hex, w, d, a, mat) => { const p = linePart('top', d, list, hex, w, mat || null); if (a != null && a < 1) { const p0 = p.paint; p.paint = c => { c.globalAlpha = a; p0(c); c.globalAlpha = 1 } } out.push(p); return p };
  const poly = (list, d, hex, b, ol) => { const pts = list.map(P); out.push({ L: 'top', d, pts: hull(pts), path: polyPath(pts), ol: ol ? 'full' : null, oc: hex, paint: c => { c.beginPath(); polyPath(pts)(c); c.fillStyle = col(hex, b); c.fill() } }) };
  const dk = k => col2hex(tc, k), F = front > -.2, B = front < -.25, fine = lod >= 2, hem = rings[0][0];
  if (lod < 1 && !L.apron) return;
  if (tKind === 'shirt' && F) {
    if (front > .4) for (const s of [1, -1]) poly([onFront(D.neck0 + .004, s * .052 * hs, 1.05), onFront(D.neck0 - .052 * hs, s * .03 * hs, 1.07), onFront(D.neck0 - .014, s * .005, 1.07)], frontD + .0062, top.c2 || col2hex(tc, 1.06), 1.08, fine);
    if (fine && top.cut !== 'polo') { const pk = [[.735, .035], [.735, .095], [.668, .095], [.66, .065], [.668, .035], [.735, .035]].map(([z, s]) => onFront(z * h, s * hs, 1.04));
      seam(pk, dk(.6), .0042 * hs, frontD + .0045, .9); seam([onFront(.72 * h, .035 * hs, 1.045), onFront(.72 * h, .095 * hs, 1.045)], dk(.6), .0038 * hs, frontD + .0046, .8);
      if (top.long || L.belt) for (const s of [1, -1]) for (const [z0, z1, s0, s1] of [[.538, .6, .125, .085], [.54, .62, .07, .045]]) seam([onFront(z0 * h, s * s0 * hs, 1.03), onFront(z1 * h, s * s1 * hs, 1.03)], dk(.66), .0048 * hs, frontD + .0042, .6) }
  }
  // D‑593: the cuts of the wardrobe — a tie on a buttoned shirt; the knitted hem of a sweater and of a hoodie; the hood, the pocket and the strings of a hoodie; the neckline of a sleeveless top
  { const cut = top.cut || '';
    if (tKind === 'shirt' && cut !== 'polo' && top.tie && F) { seam([onFront(D.neck0 - .016, 0, 1.08), onFront(.61 * h, 0, 1.09)], top.tie, .024 * hs, frontD + .0052, 1, MAT.cloth);
      out.push(boxPart('top', frontD + .0054, onFront(D.neck0 - .02 * hs, 0, 1.1), [fU, lU, Z], [.005, .013 * hs, .012 * hs], top.tie, MAT.cloth)) }
    if (cut === 'sweater' || cut === 'hoodie') { const hb = dk(.74), hw = rings[0][1] * .98;
      if (front > -.3) { const o = []; for (let i = -6; i <= 6; i++) o.push(onFront(hem + .016 * hs, i / 6 * hw, 1.02)); seam(o, hb, .03 * hs, frontD + .0043, 1, MAT.cloth) }
      if (front < .3) { const o = []; for (let i = -6; i <= 6; i++) o.push(onBack(hem + .016 * hs, i / 6 * hw)); seam(o, hb, .03 * hs, backD + .0043, 1, MAT.cloth) } }
    if (cut === 'hoodie') { const hd = ellipPart('top', B ? backD + .0066 : backD - .0012, add(fz(D.neck0 + .008 * hs), mul(fU, -.072 * hs)), [lU, fU, Z], [.098 * hs, .062 * hs, .072 * hs], null, tc, MAT.cloth, B ? 1 : .9); if (hd) out.push(hd);
      if (B) { const ho = ellipPart('top', backD + .0068, add(fz(D.neck0 + .03 * hs), mul(fU, -.066 * hs)), [lU, fU, Z], [.066 * hs, .036 * hs, .026 * hs], null, col2hex(tc, .66), MAT.cloth, 1); if (ho) { ho.ol = null; out.push(ho) } }   // the opening of the hood, darker
      if (F) { const pk = [[.612, -.085], [.635, -.045], [.635, .045], [.612, .085], [.548, .1], [.548, -.1], [.612, -.085]].map(([z, s]) => onFront(z * h, s * hs, 1.045)); poly(pk, frontD + .0041, tc, .9, false); seam(pk, dk(.6), .0045 * hs, frontD + .0045, .9);
        for (const s of [1, -1]) seam([onFront(D.neck0 - .01, s * .03 * hs, 1.08), onFront(.715 * h, s * .036 * hs, 1.08)], '#eef0ee', .0075 * hs, frontD + .0056, 1, MAT.cloth) } }
    if (cut === 'tank') { const sk = L.skin || '#d9a57f';
      if (front > -.2) poly([onFront(D.neck0, .078 * hs, 1.03), onFront(D.neck0, -.078 * hs, 1.03), onFront(.765 * h, -.062 * hs, 1.04), onFront(.742 * h, -.03 * hs, 1.045), onFront(.742 * h, .03 * hs, 1.045), onFront(.765 * h, .062 * hs, 1.04)], frontD + .0042, sk, .97, false);
      if (front < .2) poly([onBack(D.neck0, .075 * hs), onBack(D.neck0, -.075 * hs), onBack(.775 * h, -.055 * hs), onBack(.762 * h, 0), onBack(.775 * h, .055 * hs)], backD + .0042, sk, .9, false) } }
  if (tKind === 'jacket' && F) {
    seam([onFront(D.neck0 - .006, 0, 1.07), onFront(hem + .012, 0, 1.07)], '#c3c9cf', .0062 * hs, frontD + .0062, 1, MAT.metal);
    out.push(boxPart('top', frontD + .0064, onFront(D.neck0 - .03 * hs, 0, 1.1), [fU, lU, Z], [.004, .006 * hs, .013 * hs], '#d5dade', MAT.metal));
    if (fine) { for (const s of [1, -1]) seam([onFront(.6 * h, s * .07 * hs, 1.04), onFront(.535 * h, s * .118 * hs, 1.03)], dk(.5), .0068 * hs, frontD + .0045, .9);
      const band = []; for (let i = -6; i <= 6; i++) band.push(onFront(hem + .014 * hs, i / 6 * .142 * hs, 1.03)); seam(band, dk(.72), .02 * hs, frontD + .0043, 1, MAT.cloth) }
  }
  if (tKind === 'coat' && F && fine) for (const s of [1, -1]) seam([onFront(.47 * h, s * .07 * hs, 1.03), onFront(.47 * h, s * .15 * hs, 1.02)], dk(.55), .01 * hs, frontD + .0045, .9);
  if (tKind === 'labcoat' && F) { const zt = D.neck0 - .006, zb = .655 * h, sc = top.c2 || '#3aa39a';
    poly([onFront(zt, .056 * hs, 1.02), onFront(zt, -.056 * hs, 1.02), onFront(zb, 0, 1.03)], frontD + .004, sc, .92, false);
    for (const s of [1, -1]) seam([onFront(zt, s * .062 * hs, 1.03), onFront(zb + .012, s * .012, 1.05)], dk(.82), .016 * hs, frontD + .0055, 1, MAT.cloth);
    seam([onFront(zb, 0, 1.05), onFront(rings[0][0] + .01, 0, 1.06)], dk(.62), .0045 * hs, frontD + .005, .9);
    for (let i = 0; i < 3; i++) out.push(linePart('top', frontD + .0057, [onFront((.61 - i * .07) * h, -.012, 1.06), onFront((.61 - i * .07) * h - .002, -.012, 1.06)], '#dcdfe2', .012 * hs, MAT.plastic));
    if (fine) { const pk = [[.735, .045], [.735, .11], [.67, .11], [.67, .045], [.735, .045]].map(([z, s]) => onFront(z * h, s * hs, 1.04)); seam(pk, dk(.66), .0042 * hs, frontD + .0045, .9);
      for (const [s, c_] of [[.06, '#2a5bd7'], [.075, '#c0392b']]) seam([onFront(.745 * h, s * hs, 1.05), onFront(.71 * h, s * hs, 1.05)], c_, .006 * hs, frontD + .0047, 1, MAT.plastic);
      for (const s of [1, -1]) { const q = [[.46, .05], [.46, .13], [.39, .13], [.39, .05], [.46, .05]].map(([z, u]) => add(fz(z * h), add(mul(fU, .13 * hs), mul(lU, s * u * hs)))); seam(q, dk(.66), .0042 * hs, frontD + .0045, .9) } }
  }
  if (top.vneck && F) { const zt = D.neck0 - .004, zb = .735 * h; poly([onFront(zt, .05 * hs, 1.03), onFront(zt, -.05 * hs, 1.03), onFront(zb, 0, 1.04)], frontD + .0042, L.skin || '#d9a57f', .95, false);
    for (const s of [1, -1]) seam([onFront(zt, s * .052 * hs, 1.04), onFront(zb, 0, 1.05)], dk(.7), .009 * hs, frontD + .0046, 1, MAT.cloth) }
  if (B && fine && tKind !== 'coat' && tKind !== 'labcoat' && tKind !== 'suit') { seam([-.15, -.08, 0, .08, .15].map(s => onBack(.77 * h, s * hs)), dk(.66), .0045 * hs, backD + .004, .75);
    if (tKind === 'shirt') seam([onBack(.765 * h, 0), onBack(.62 * h, 0)], dk(.7), .004 * hs, backD + .004, .55) }
  if (B && fine && tKind === 'labcoat') seam([onBack(.5 * h, 0), onBack(rings[0][0] + .01, 0)], dk(.62), .0045 * hs, backD + .004, .9);
  if (L.steth) { const sc = '#2a2c30';
    if (F) { const nk = s => add(fz(D.neck0 - .01), add(mul(lU, s * .062 * hs), mul(fU, .03 * hs)));
      seam([nk(1), onFront(.775 * h, .062 * hs, 1.1), onFront(.71 * h, .045 * hs, 1.12)], sc, .0085 * hs, frontD + .0075, 1, MAT.plastic);
      seam([nk(-1), onFront(.775 * h, -.062 * hs, 1.1), onFront(.7 * h, -.055 * hs, 1.13)], sc, .0085 * hs, frontD + .0075, 1, MAT.plastic);
      out.push(ellipPart('top', frontD + .0078, onFront(.69 * h, -.055 * hs, 1.16), [lU, fU, Z], [.016 * hs, .008 * hs, .016 * hs], null, '#c9ced3', MAT.metal, 1)) }
    else { const o = []; for (let i = 0; i <= 10; i++) { const t = (i / 10 - .5) * Math.PI; o.push(add(fz(D.neck0 - .005), add(mul(fU, -Math.cos(t) * .065 * hs), mul(lU, Math.sin(t) * .07 * hs)))) } seam(o, sc, .0085 * hs, backD + .006, 1, MAT.plastic) } }
  // p670: the uniforms — the badge on the left of the chest (wings of a pilot, the company's pin, the star of the police, a name tag),
  // the reflective stripes round the body (fire, refinery, road), the shoulder boards with their bars (pilots)
  if (L.badge && F && front > .05) { const b = L.badge, z = (b.z || .735) * h, s0 = -.078 * hs, bc = b.c || '#d4af37';
    if (b.k === 'wings') { seam([onFront(z + .006 * h, s0 - .046 * hs, 1.07), onFront(z, s0 - .012 * hs, 1.08), onFront(z, s0 + .012 * hs, 1.08), onFront(z + .006 * h, s0 + .046 * hs, 1.07)], bc, .011 * hs, frontD + .0066, 1, MAT.metal);
      out.push(ellipPart('top', frontD + .0068, onFront(z, s0, 1.1), [lU, fU, Z], [.012 * hs, .006 * hs, .012 * hs], null, b.c2 || bc, MAT.metal, 1)) }
    else if (b.k === 'tag') { const a = onFront(z, s0 - .03 * hs, 1.07), c_ = onFront(z, s0 + .03 * hs, 1.07); seam([a, c_], '#f4f5f2', .026 * hs, frontD + .0064, 1, MAT.plastic); seam([onFront(z + .009 * h, s0 - .03 * hs, 1.08), onFront(z + .009 * h, s0 + .03 * hs, 1.08)], bc, .008 * hs, frontD + .0066, 1, MAT.plastic) }
    else out.push(ellipPart('top', frontD + .0066, onFront(z, s0, 1.09), [lU, fU, Z], [(b.k === 'star' ? .017 : .013) * hs, .006 * hs, (b.k === 'star' ? .019 : .013) * hs], null, bc, MAT.metal, 1, b.c2 ? c => { c.save(); c.clip(); const p = P(onFront(z, s0, 1.1)); c.beginPath(); c.arc(p[0], p[1], .006 * SCALE * hs, 0, Math.PI * 2); c.fillStyle = b.c2; c.fill(); c.restore() } : null)) }
  if (L.stripe) { const sc = L.stripe; for (const zz of (L.stripeZ || [.52, .62])) { const z = zz * h; if (z < hem + .01) continue;
    if (front > -.3) { const o = []; for (let i = -6; i <= 6; i++) o.push(onFront(z, i / 6 * .15 * hs, 1.03)); seam(o, sc, .022 * hs, frontD + .0052, 1, MAT.refl) }
    if (front < .3) { const o = []; for (let i = -6; i <= 6; i++) o.push(onBack(z, i / 6 * .15 * hs)); seam(o, sc, .022 * hs, backD + .0052, 1, MAT.refl) } } }
  if (L.epau && fine) { const e = L.epau; for (const s of [1, -1]) { const a = add(fz(D.shZ + .004), mul(lU, s * .06 * hs)), b = add(fz(D.shZ + .002), mul(lU, s * .13 * hs));
    seam([a, b], e.b || '#14181f', .026 * hs, torsoY + .0035, 1, MAT.wool); for (let k = 0; k < (e.n || 0); k++) { const u = .45 + k * .14, q = add(a, mul(sub(b, a), u)); seam([add(q, mul(fU, -.012 * hs)), add(q, mul(fU, .012 * hs))], e.c || '#d4af37', .006 * hs, torsoY + .0037, 1, MAT.metal) } } }
  if (L.apron) { const ac = L.apron.c || '#f2f2ee', zt = .745 * h, zw = .6 * h, zb = (L.apron.low || .33) * h, wt = .085 * hs, ww = .15 * hs, wb = .17 * hs;
    const pt = (z, s) => z >= .55 * h ? onFront(z, s, 1.06) : add(fz(z), add(mul(fU, .128 * hs), mul(lU, s)));
    if (front > -.3) { const pl = [pt(zt, -wt), pt(zt, wt), pt(zw, ww), pt(.53 * h, ww * 1.06), pt(zb, wb), pt(zb, -wb), pt(.53 * h, -ww * 1.06), pt(zw, -ww)], pts = pl.map(P);
      const x0 = Math.min(...pts.map(p => p[0])), x1 = Math.max(...pts.map(p => p[0]));
      out.push({ L: 'top', d: frontD + .007, pts: hull(pts), path: polyPath(pts), ol: 'full', oc: ac, paint: c => { c.beginPath(); polyPath(pts)(c); const g = c.createLinearGradient(x0, 0, x1, 0);
        g.addColorStop(0, col(ac, bri(mul(fU, 1), MAT.cloth) * 1.06)); g.addColorStop(1, col(ac, bri(mul(fU, 1), MAT.cloth) * .86)); c.fillStyle = g; c.fill();
        if (lod >= 2) { const a = P(pt(.5 * h, -.09 * hs)), b = P(pt(.5 * h, .09 * hs)); c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.lineWidth = .0045 * SCALE; c.strokeStyle = col(ac, .6); c.stroke() } } });
      for (const s of [1, -1]) { seam([pt(zt, s * wt * .9), add(fz(D.neck0 + .01), add(mul(lU, s * .055 * hs), mul(fU, .01)))], col2hex(ac, .85), .012 * hs, frontD + .0072, 1, MAT.cloth);
        seam([pt(zw, s * ww), onFront(zw, s * .145 * hs, 1.02), add(fz(zw), add(mul(lU, s * .13 * hs), mul(fU, -.06 * hs)))], col2hex(ac, .85), .012 * hs, frontD + .0071, 1, MAT.cloth) } }
    else { const c0 = onBack(zw, 0); for (const s of [1, -1]) { out.push(ellipPart('top', backD + .006, add(c0, mul(lU, s * .03 * hs)), [lU, fU, Z], [.028 * hs, .012 * hs, .018 * hs], null, col2hex(ac, .9), MAT.cloth, 1));
        seam([add(c0, mul(lU, s * .01)), add(c0, add(mul(lU, s * .04 * hs), [0, 0, -.09 * hs]))], col2hex(ac, .85), .012 * hs, backD + .0062, 1, MAT.cloth) }
      seam([onBack(zw, -.14 * hs), onBack(zw, .14 * hs)], col2hex(ac, .85), .012 * hs, backD + .0058, 1, MAT.cloth) } }
}
function mixHex(a, b, t) { const x = hexC(a), y = hexC(b); return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, '0')).join('') }
function col2hex(h, b) { const c = hexC(h); const f = v => Math.max(0, Math.min(255, Math.round(v * b))).toString(16).padStart(2, '0'); return '#' + f(c[0]) + f(c[1]) + f(c[2]) }

// ---- rendering: a list of parts (and erasers) into a canvas at pxm device px per screen metre, with the thin dark rim ----
const LAYERS = ['body', 'top', 'hair', 'item'];
const mk = (w, h) => { if (typeof OffscreenCanvas !== 'undefined') return new OffscreenCanvas(w, h); const c = document.createElement('canvas'); c.width = w; c.height = h; return c };
// p670: the line of the parts — stroked over the fill ('side': the two long sides of a limb; 'full': the outline), in the part's darker
// colour, from lod 1; OWM — its width in screen metres while a picture is made
let OWM = 0;
function olStroke(c, p) { c.lineWidth = OWM; c.strokeStyle = col(p.oc, .36); c.globalAlpha = .82; c.beginPath();
  if (p.ol === 'side') { const dx = p.sB[0] - p.sA[0], dy = p.sB[1] - p.sA[1], l = Math.hypot(dx, dy); if (l < 1e-6) { c.globalAlpha = 1; return } const nx = -dy / l, ny = dx / l, t = p.olFrom || 0;
    const ax = p.sA[0] + dx * t, ay = p.sA[1] + dy * t, ra = p.ra + (p.rb - p.ra) * t;
    for (const s of [1, -1]) { c.moveTo(ax + nx * ra * s, ay + ny * ra * s); c.lineTo(p.sB[0] + nx * p.rb * s, p.sB[1] + ny * p.rb * s) } }
  else p.path(c);
  c.stroke(); c.globalAlpha = 1 }
function render(seq, pxm, rim, small, lod, owm) {   /* D‑593: owm — the width of the line in screen metres, for a big picture (the dressing room) */
  LIFT = small ? 1 : 0; OWM = owm > 0 ? owm : (lod >= 1 ? Math.min(1.6, .35 + pxm * .0085) / pxm : 0);
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const e of seq) if (!e.er) for (const p of e.p.pts) { if (p[0] < x0) x0 = p[0]; if (p[0] > x1) x1 = p[0]; if (p[1] < y0) y0 = p[1]; if (p[1] > y1) y1 = p[1] }
  if (!isFinite(x0)) return null;
  const pad = 3, ox = Math.ceil(-x0 * pxm) + pad, oy = Math.ceil(-y0 * pxm) + pad, W = Math.max(1, ox + Math.ceil(x1 * pxm) + pad), Hh = Math.max(1, oy + Math.ceil(y1 * pxm) + pad);   // p670: the origin on a whole pixel
  const cv = mk(W, Hh), c = cv.getContext('2d'); c.setTransform(pxm, 0, 0, pxm, ox, oy); c.lineJoin = 'round'; c.lineCap = 'round';
  const glow = [], under = [];
  for (const e of seq) {
    if (e.er) { c.globalCompositeOperation = 'destination-out'; c.beginPath(); e.p.path(c); if (e.p.stroke) { c.lineWidth = e.p.w; c.stroke() } else c.fill(); c.globalCompositeOperation = 'source-over'; continue }
    if (e.p.noRim) { glow.push(e.p); continue }
    if (e.p.under) { under.push(e.p); continue }
    e.p.paint(c); if (OWM && e.p.ol) olStroke(c, e.p);
  }
  let out = cv;
  if (rim && !small) {   // the rim: the picture's alpha, spread by w device px, filled dark, under the picture
    const w = Math.max(1, Math.round(pxm * .0085)), q = Math.max(1, Math.round(w * .7)), t = mk(W, Hh), g = t.getContext('2d');   // p670: whole pixels, darker
    for (const [dx, dy] of [[w, 0], [-w, 0], [0, w], [0, -w], [q, q], [-q, q], [q, -q], [-q, -q]]) g.drawImage(cv, dx, dy);
    g.globalCompositeOperation = 'source-in'; g.fillStyle = pxm < 40 ? 'rgba(16,20,26,.68)' : 'rgba(16,20,26,.84)'; g.fillRect(0, 0, W, Hh);
    g.globalCompositeOperation = 'source-over'; g.drawImage(cv, 0, 0); out = t;
  }
  if (under.length) { const g = out.getContext('2d'); g.setTransform(pxm, 0, 0, pxm, ox, oy); g.globalCompositeOperation = 'destination-over'; for (const p of under) p.paint(g); g.globalCompositeOperation = 'source-over' }
  if (glow.length) { const g = out.getContext('2d'); g.setTransform(pxm, 0, 0, pxm, ox, oy); g.globalCompositeOperation = 'lighter'; for (const p of glow) p.paint(g); g.globalCompositeOperation = 'source-over' }
  LIFT = 0; OWM = 0;
  return { cv: out, ox, oy, bytes: W * Hh * 4 };
}
// the sequence of one layer: its parts by depth, with the parts of the earlier layers that stand in front of them as erasers
function layerSeq(all, li) {
  const own = all.filter(p => p.L === LAYERS[li]).sort((a, b) => a.d - b.d); if (!own.length) return null;
  const dmin = own[0].d, ers = all.filter(p => LAYERS.indexOf(p.L) < li && p.d > dmin && !p.noRim && !p.under);
  const seq = own.map(p => ({ p, d: p.d, er: false })).concat(ers.map(p => ({ p, d: p.d, er: true })));
  seq.sort((a, b) => a.d - b.d || (a.er ? -1 : 1));
  return seq;
}
// ---- the cache ----
const CACHE = new Map(); let BYTES = 0, MADE = 0, MADE_MS = 0, HITS = 0, EVICT = 0;
const P34 = G.P34 = { K, SCALE, FR, KYC, lodPx: [30, 80], budgetMB: 24, rim: true, smallPx: 30, partsKeepMs: 600, dpr: typeof devicePixelRatio !== 'undefined' ? Math.min(2, devicePixelRatio || 1) : 1 };
const lk0 = L => { const o = Object.assign({}, DEF, L); return { body: [o.h, o.w, o.belly, o.skin, o.legs.t, o.legs.c, o.shoes.t, o.shoes.c, o.socks || '', o.glasses || '', o.eyes || '', o.hair.c].join(','),
  top: [o.h, o.w, o.belly, o.top.t, o.top.c, o.top.c2 || '', o.top.tie || '', o.top.sleeve, o.top.long ? 1 : 0, (o.vest || '') + (o.vestK || ''), o.belt || '', o.apron ? o.apron.c + (o.apron.low || '') : '', o.steth ? 1 : 0, o.top.vneck ? 1 : 0, o.skin, o.badge ? o.badge.k + o.badge.c + (o.badge.c2 || '') + (o.badge.z || '') : '', (o.stripe || '') + (o.stripeZ || ''), o.epau ? o.epau.n + o.epau.c + o.epau.b : ''].join(','),   /* p670: the uniforms */
  hair: [o.h, o.hair.t, o.hair.c, o.hat ? o.hat.t + o.hat.c + (o.hat.b || '') + (o.hat.e || '') : '', o.beard ? o.beard.c : '', o.earmuff || '', o.skin, o.glasses || ''].join(','),   /* p670: the band and the badge of the cap */
  item: [o.h, o.w, o.item ? o.item.k + (o.item.c || '') : ''].join(',') } };
/* D‑593: the fields of the wardrobe (the cuts of the top, the legs, the shoes and the hat; gloves, a watch, a scarf, dark lenses) are part of the key — only when a look has them */
const lk = L => { const k = lk0(L), t = L.top || {}, g = L.legs || {}, s = L.shoes || {}, h = L.hat || {};
  const b = [g.cut || '', g.c2 || '', s.cut || '', s.shaft ? 1 : '', L.gloves || '', L.shades ? 1 : ''].join('~'), tt = [t.cut || '', t.noTie ? 1 : '', L.scarf || '', L.watch ? (L.watch.c || '') + (L.watch.b || '') : ''].join('~'), hh = [h.cut || '', L.shades ? 1 : ''].join('~');
  if (b !== '~~~~~') k.body += '|' + b; if (tt !== '~~~') k.top += '|' + tt; if (hh !== '~') k.hair += '|' + hh; return k };
const PCACHE = new Map();
/* mem (R-89): הגאומטריה של תנוחה (כ-300 ק״ב לכל אחת, עד 64) נדרשת רק כשנוצרות תמונות חדשות של אותה תנוחה — בשכבה אחרת באותה קריאה,
   או בזום אחר (בזמן תנועת זום — פריים אחרי פריים). התמונות עצמן נשארות במטמון שלהן; תנוחה שלא נגעו בה P34.partsKeepMs (‏0.6 שנייה) —
   יוצאת, ונבנית מחדש אם תידרש (אותו חישוב, אותו ציור). בהליכה רגילה כל תמונה חדשה היא תנוחה חדשה, כך שהמטמון כמעט לא נקרא שוב. */
let PC_CALLS = 0, PC_SWEPT = 0, PC_FREED = 0;
function partsOf(look, act, dir, fr, key, small, lod) { const now = performance.now(); let e = PCACHE.get(key); if (e) { e.t = now; return e.p }
  pcSweep(); const p = parts(look, act, dir, fr, small, lod).parts; PCACHE.set(key, { p, t: now }); if (PCACHE.size > 64) PCACHE.delete(PCACHE.keys().next().value); return p }
function pcSweep() { const now = performance.now(); if (now - PC_SWEPT < 250) return; PC_SWEPT = now; const keep = P34.partsKeepMs; if (!(keep > 0) || !PCACHE.size) return;
  for (const [k, e] of PCACHE) if (now - e.t > keep) { PCACHE.delete(k); PC_FREED++ } }
if (typeof setInterval === 'function') setInterval(() => { try { pcSweep() } catch (e) { } }, 500);
function put(key, e) { CACHE.set(key, e); BYTES += e ? e.bytes : 0; if (P34.budgetMB > 0) while (BYTES > P34.budgetMB * 1048576 && CACHE.size > 1) { const [k0, e0] = CACHE.entries().next().value; if (k0 === key) break; CACHE.delete(k0); BYTES -= e0 ? e0.bytes : 0; EVICT++ } }
function get(key) { const e = CACHE.get(key); if (e !== undefined) { if (++HITS % 8 === 0) { CACHE.delete(key); CACHE.set(key, e) } return e } return undefined }
const dirOf = h => ((Math.round(h / (Math.PI / 4)) % 8) + 8) % 8;
const frOf = (k, ph) => { const F = FR[k] || 1; return F > 1 ? ((Math.floor(ph * F) % F) + F) % F : 0 };
// the height of a look standing, in screen metres (once per look) → is its picture small (under P34.smallPx css px)?
function hmOf(look) { if (look.__hm == null) { let y0 = Infinity, y1 = -Infinity; for (const p of parts(look, { k: 'stand' }, 2, 0).parts) for (const q of p.pts) { y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]) } look.__hm = y1 - y0 } return look.__hm }
P34.sprites = function (look, act, heading, phase, res, mode) {
  if ((++PC_CALLS & 255) === 0) pcSweep();
  const small = hmOf(look) * PXM * res / P34.dpr < P34.smallPx;
  const hd = hmOf(look) * PXM * res, lod = small || hd < P34.lodPx[0] ? 0 : hd < P34.lodPx[1] ? 1 : 2;   // p670: the detail by the height in device px
  const d = dirOf(heading), fr = frOf(act.k, phase), keys = look.__k || (look.__k = lk(look)), pk = act.k + '/' + d + '/' + fr + '/' + (look.item ? look.item.k : '') + (small ? '/s' : '') + '/l' + lod;
  const pxm = PXM * res, all = () => partsOf(look, act, d, fr, JSON.stringify(keys) + pk, small, lod);
  if (mode === 'flat') { const key = 'F|' + keys.body + '|' + keys.top + '|' + keys.hair + '|' + keys.item + '|' + pk + '|' + res; let e = get(key);
    if (e === undefined) { const t0 = performance.now(); const A = all().slice().sort((a, b) => a.d - b.d); e = render(A.map(p => ({ p, d: p.d, er: false })), pxm, P34.rim, small, lod); MADE_MS += performance.now() - t0; MADE++; put(key, e) } return e ? [e] : [] }
  const out = [];
  for (let li = 0; li < 4; li++) { const key = LAYERS[li] + '|' + keys[LAYERS[li]] + '|' + pk + '|' + res; let e = get(key);
    if (e === undefined) { const t0 = performance.now(); const seq = layerSeq(all(), li); e = seq ? render(seq, pxm, P34.rim, small, lod) : null; MADE_MS += performance.now() - t0; MADE++; put(key, e) }
    if (e) out.push(e) }
  return out;
};
// the contact shadow: a dark core under the feet and a soft short cast toward the lower right (the sun up-left); one picture per density
const SH = new Map();
function shadow(res, kind) { const key = kind + '|' + res; let e = SH.get(key); if (e) return e;
  const pxm = PXM * res, R = (kind === 'sit' ? .5 : .34) * SCALE, W = Math.ceil(R * 3.2 * pxm), Hh = Math.ceil(R * 2 * pxm), cv = mk(W, Hh), c = cv.getContext('2d'), ox = W * .3, oy = Hh * .42;
  c.setTransform(pxm, 0, 0, pxm, ox, oy);
  c.save(); c.translate(.32 * SCALE, .16 * SCALE); c.rotate(.6); c.scale(1, .42); let g = c.createRadialGradient(0, 0, 0, 0, 0, R * 1.25); g.addColorStop(0, 'rgba(12,16,22,.24)'); g.addColorStop(.6, 'rgba(12,16,22,.12)'); g.addColorStop(1, 'rgba(12,16,22,0)'); c.fillStyle = g; c.beginPath(); c.arc(0, 0, R * 1.25, 0, Math.PI * 2); c.fill(); c.restore();
  c.save(); c.scale(1, .5); g = c.createRadialGradient(0, 0, 0, 0, 0, R * .78); g.addColorStop(0, 'rgba(10,13,18,.55)'); g.addColorStop(.55, 'rgba(10,13,18,.34)'); g.addColorStop(1, 'rgba(10,13,18,0)'); c.fillStyle = g; c.beginPath(); c.arc(0, 0, R * .78, 0, Math.PI * 2); c.fill(); c.restore();
  e = { cv, ox, oy }; SH.set(key, e); return e }
P34.draw = function (ctx, x, y, look, act, heading, phase, res, mode) {
  const sh = shadow(res, act.k === 'eat' || act.k === 'bench' ? 'sit' : 'stand'); ctx.drawImage(sh.cv, x - sh.ox / res, y - sh.oy / res, sh.cv.width / res, sh.cv.height / res);
  let X = x, Y = y;   // p670: on a canvas at the picture's own density — the anchor on a whole device pixel (no resampling, no blur)
  try { const T = ctx.getTransform(); if (Math.abs(T.b) < 1e-9 && Math.abs(T.c) < 1e-9 && Math.abs(T.a - res) < res * 1e-3 && Math.abs(T.d - res) < res * 1e-3) { const u = T.a * x + T.e, v = T.d * y + T.f; X = x + (Math.round(u) - u) / T.a; Y = y + (Math.round(v) - v) / T.d } } catch (e) { }
  for (const s of P34.sprites(look, act, heading, phase, res, mode)) ctx.drawImage(s.cv, X - s.ox / res, Y - s.oy / res, s.cv.width / res, s.cv.height / res);
};
P34.cycle = (look) => { const D = dims(Object.assign({}, DEF, look)); return 2 * SCALE * STEP(D, look.item && look.item.k) };
P34.stats = () => ({ sprites: CACHE.size, MB: +(BYTES / 1048576).toFixed(2), poses: PCACHE.size, posesFreed: PC_FREED, made: MADE, makeMs: +MADE_MS.toFixed(1), makeAvg: MADE ? +(MADE_MS / MADE).toFixed(2) : 0, evicted: EVICT, budgetMB: P34.budgetMB });
P34.clear = () => { CACHE.clear(); PCACHE.clear(); BYTES = 0; MADE = 0; MADE_MS = 0; HITS = 0; EVICT = 0 };
// the height on the screen (px) of a look standing, at a zoom (world px per metre = 10 × zoom)
P34.heightPx = (look, zoom) => { const A = parts(look, { k: 'stand' }, 2, 0).parts; let y0 = Infinity, y1 = -Infinity; for (const p of A) for (const q of p.pts) { y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]) } return { top: y0 * PXM * zoom, bottom: y1 * PXM * zoom, px: (y1 - y0) * PXM * zoom } };
P34.parts = parts; P34.DEF = DEF; P34.lk = lk;   /* p670: the game's cache key from the generator's own */
// p670: the pose for the layers outside (FISHX: the rod from the hand) — the hands where they are drawn (their depth in the people's camera)
P34.pose = function (look, act, dir, fr) { const S = pose(look, act, dir, fr); KW = !!act && act.k !== 'bench' && act.k !== 'eat';
  for (const a of S.arms) a.hand = [a.hand[0], a.hand[1] * ky(a.hand[2]), a.hand[2]]; KW = false; return S };
// D‑593: one whole person at any heading and any phase (a continuous turn, a continuous step) — the same parts and the same rendering as the game's
// pictures, not cached (the turntable of the dressing room, the pictures of the shop).  owm — the line's width in screen metres (a big picture).
P34.spriteAt = function (look, act, heading, phase, res, owm) { const k = (act && act.k) || 'stand', F = FR[k] || 1, u = ((phase % 1) + 1) % 1, fr = F > 1 ? (k.length === 2 && k[0] === 'f' ? Math.floor(u * F) % F : u * F) : 0;
  const A = parts(look, { k }, heading / (Math.PI / 4), fr, false, 2).parts.slice().sort((a, b) => a.d - b.d); return render(A.map(p => ({ p, d: p.d, er: false })), PXM * res, P34.rim, false, 2, owm) };
})(typeof window !== 'undefined' ? window : globalThis);
/* p540 (הבעלים 10:36 — "מקסחי הדשה זזים בלי ללכת"): the library takes the act as {k:…}; a string ('walk') gave no steps — take both */
(function(){try{const d0=window.P34&&P34.draw;if(d0&&!d0.__p540){const f=function(ctx,x,y,look,act,h,ph,res,mode){return d0.call(this,ctx,x,y,look,typeof act==='string'?{k:act}:(act||{k:'stand'}),h,ph,res,mode)};f.__p540=1;P34.draw=f}}catch(e){}})();
/* p558: the people of the live layers (P34.draw directly) — the density of the picture rounded up to a step of 2^(1/8) (≈ 9 %), so a zoom
   that moves does not make a new picture every frame; the size on the screen is the same (the library draws it at res), and the "small"
   choice of the library stays as it was (if the step would change it — the exact density). The game's people (mode 'flat') — untouched. */
(function(){try{const d0=window.P34&&P34.draw;if(d0&&!d0.__p558){const LV=[1,1.25,1.5,2,2.5,3,4],ST=window.__P558RES={snapped:0,kept:0};
  const q=r=>{if(!(r>0))return r;for(const v of LV)if(Math.abs(v-r)<1e-6)return r;return Math.pow(2,Math.ceil(Math.log2(r)*8-1e-6)/8)};
  const f=function(ctx,x,y,look,act,h,ph,res,mode){if(mode==='flat')return d0.call(this,ctx,x,y,look,act,h,ph,res,mode);let r=q(res);
   if(r!==res&&look&&look.__hm!=null){const s0=look.__hm*10*res/P34.dpr<P34.smallPx,s1=look.__hm*10*r/P34.dpr<P34.smallPx;if(s0!==s1)r=res}
   if(r!==res)ST.snapped++;else ST.kept++;return d0.call(this,ctx,x,y,look,act,h,ph,r,mode)};f.__p558=1;f.__p540=d0.__p540;P34.draw=f}}catch(e){}})();




/* p636: the density of every person is P34's own — from the scale of the canvas it is drawn on (zoom × screen density), at every call */
(function(){try{const d0=window.P34&&P34.draw;if(d0&&!d0.__p636){const ST=window.__P636={calls:0,raised:0,max:0};
  const f=function(ctx,x,y,look,act,heading,phase,res,mode){ST.calls++;
   try{if(typeof Camera!=='undefined'&&Camera.zoom>=((window.P599&&P599.zoom)||2)&&ctx&&ctx.getTransform){const T=ctx.getTransform(),k=Math.hypot(T.a,T.b);
    if(k>0&&!(res>=k-1e-6)){const L=(typeof P34G!=='undefined'&&P34G.R)||[1,1.25,1.5,2,2.5,3,4,5.5,8,11];let r=L[L.length-1];for(const v of L)if(v>=k-1e-6){r=v;break}
     if(!(res>=r)){res=r;ST.raised++;if(r>ST.max)ST.max=r}}}}catch(e){}
   return d0.call(this,ctx,x,y,look,act,heading,phase,res,mode)};
  f.__p636=1;f.__p558=d0.__p558;P34.draw=f}}catch(e){}})();
return true}
function a34LibInit(){if(window.A34)return true;
/* a34.js — Turbo City · D‑268 · the aircraft in the 3/4 view (oblique, K = 0.6): the sample before the whole fleet (step 4).
   Plain script, defines window.A34.  No dependence on the game's globals.
   World: x east, y south, z up, in METRES; the page turns metres into its field scale s (7.47 px/m today, 10 px/m in the new field):
   screen = ((x)·s, (y − K·z)·s).  The ground plan is not foreshortened; a surface at height z moves up (north on the screen) by K·z.
   The sun, the ambient and the colour ramp are the vehicles' (c34m.js: LD, AMB .62, DIF .38, litC), the materials' gloss the people's.
   The geometry follows the game's aircraft table (AC: length, span, fuselage width, wing chords, sweep, engines) and the details of
   air_({...}) (nose / tail-cone lengths, doors, windows, engines, tailplane span, the tri-jet's third engine, the upper deck); the
   heights are the class's real ones (A34.TYPES[id].src says which).
   An aircraft is a set of PIECES — the body (fuselage, fin, upper tail, tail engine), each wing, each engine, each low tailplane, the
   gear legs — and every piece carries the sort key of the scene: y of its south edge + (height of its lowest point) / K. */
(function (G) {
'use strict';
const K = 0.6, TAU = Math.PI * 2, D2R = Math.PI / 180;
const nrm = v => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n] };
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const crs = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const lerp = (a, b, t) => a + (b - a) * t, cl = (v, a, b) => Math.max(a, Math.min(b, v));
const sm = x => { x = cl(x, 0, 1); return x * x * (3 - 2 * x) };
// ---- the sun (c34m.js) and the view ----
const LD = nrm([-0.42, -0.55, 0.72]), VW = nrm([0, K, 1]), HV = nrm([LD[0] + VW[0], LD[1] + VW[1], LD[2] + VW[2]]);
const AMB = .62, DIF = .38, TOPB = AMB + DIF * LD[2];
const MAT = { paint: [.2, 9], metal: [.34, 14], glass: [.75, 30], rubber: [.03, 6], matte: [0, 1] };
function lit(n, mat) { let b = (AMB + DIF * Math.max(0, dot(n, LD))) / TOPB; if (n[2] < 0) b *= 1 + .3 * n[2]; const m = MAT[mat] || MAT.paint; if (m[0]) b += m[0] * Math.pow(Math.max(0, dot(n, HV)), m[1]); return b }
const hexRGB = h => { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255] };
const litC = (hex, b) => { const c = hexRGB(hex); if (b <= 1) return `rgb(${c[0] * b + 14 * (1 - b) | 0},${c[1] * b + 17 * (1 - b) | 0},${c[2] * b + 22 * (1 - b) | 0})`; const k = Math.min(1, (b - 1) * .6); return `rgb(${c[0] + (255 - c[0]) * k | 0},${c[1] + (255 - c[1]) * k | 0},${c[2] + (255 - c[2]) * k | 0})` };
const mixC = (a, b, f) => { const p = hexRGB(a), q = hexRGB(b); return '#' + p.map((v, i) => Math.round(v + (q[i] - v) * f).toString(16).padStart(2, '0')).join('') };
const sh = (h, f) => { const c = hexRGB(h), m = f < 0 ? 0 : 255, k = Math.abs(f); return '#' + c.map(v => Math.round(v + (m - v) * k).toString(16).padStart(2, '0')).join('') };   // the game's sh()
const lum = h => { const c = hexRGB(h); return (c[0] * .299 + c[1] * .587 + c[2] * .114) / 255 };
// the shadow on the ground (D‑277, one sun for the whole game): a point at height z falls z·(C34.SUN.x, C34.SUN.y) = z·(0.25, 0.32) to the
// south-east — 0.41 of its height, as every vehicle's (it was z·(0.583, 0.764), its own sun)
const SUN0 = { x: .25, y: .32 }, SUN = () => (G.C34 && G.C34.SUN) || SUN0;

// ---- the liveries (the game's LIV, the 4 airlines of the sample) and the Hebrew titles (MK_HE) ----
const LIV = {
  aurelia: { n: 'אורליה', w: 'classic', k: 'arc', b: '#f4f6f8', u: '#d9dde2', s: '#1f5aa6', t: '#1f5aa6', m: '#f2c230' },
  sunbeak: { n: 'מקור השמש', w: 'allover', k: 'bird', b: '#f6c518', u: '#d9a60c', s: '#1d1d1f', t: '#1d1d1f', m: '#f6c518', eng: '#1d1d1f' },
  mirage: { n: 'מיראז׳', w: 'nose', k: 'chev', b: '#ffffff', u: '#e3e3ea', s: '#e0218a', t: '#e0218a', m: '#ffd400', eng: '#e0218a' },
  skyline: { n: 'קו הרקיע', w: 'spine', k: 'diamond', b: '#eef2f6', u: '#9fb2c6', s: '#3a3f8f', t: '#3a3f8f', m: '#f2c230', eng: '#3a3f8f' }
};

// ---- the types (metres).  From the game's AC table: L, WS, fw, wc (root chord), tc (tip chord), sw (tip LE sweep offset), the
// engines (spanwise fraction of the half span), ts; from air_({...}): nl, tl, doors, windows, en (nacelle length × fw), hs, extras.
// The heights (zb fuselage bottom, H fin top, wz wing root, dihedral, nacelle diameter) — the real class (src). ----
// R‑14 (4) · the nose of each type from the real aircraft's proportions (side and plan views of the class): x metres aft of the tip →
// the crown and the chin (metres from the fuselage's centre line) and the half width; the cockpit's panes on the east side (mirrored):
// [front-bottom, back-bottom, back-top, front-top] as [a metres aft of the tip, θ degrees round the axis — 90 the crown]
const NOSE = {
  'AC-NB-01': { src: 'A320', x: [0, .3, .7, 1.2, 2.0, 2.3, 2.65, 3.4, 4.4, 5.6, 7.2], top: [-.3, .35, .72, .95, 1.18, 1.7, 1.88, 1.95, 1.99, 2.0, 2.0], bot: [-.3, -.85, -1.2, -1.5, -1.75, -1.8, -1.86, -1.94, -1.99, -2.0, -2.0], hw: [0, .62, .95, 1.25, 1.58, 1.66, 1.76, 1.89, 1.97, 2.0, 2.0],
    cab: { zs: 1.24, h: .36, vd: .2, lean: .15, ls: .32, lr: .21, q: .42, sb: .4 },
    door: 4.4 },
  'AC-MW-01': { src: '787-9', x: [0, .4, 1, 2, 2.9, 3.3, 3.75, 4.7, 5.7, 7.2, 9.2], top: [-.3, .55, 1.12, 1.62, 1.85, 2.42, 2.68, 2.86, 2.94, 2.98, 2.985], bot: [-.3, -1.02, -1.6, -2.2, -2.5, -2.6, -2.68, -2.8, -2.9, -2.97, -2.985], hw: [0, .86, 1.38, 1.98, 2.32, 2.42, 2.52, 2.68, 2.8, 2.87, 2.885],
    cab: { zs: 1.86, h: .55, vd: .3, lean: .2, ls: .46, lr: .31, q: .42, sb: .4 },
    door: 6.9 },
  'AC-LG-01': { src: '747', x: [0, .4, 1, 2, 3, 4.5, 6, 7.5, 9.6], top: [-.3, .5, 1.1, 1.8, 2.3, 2.75, 2.95, 2.98, 2.98], bot: [-.3, -1.1, -1.7, -2.3, -2.65, -2.9, -2.97, -2.98, -2.98], hw: [0, .85, 1.4, 2.0, 2.4, 2.75, 2.92, 2.98, 2.98],
    cab: { zs: 4.25, h: .37, vd: .15, lean: .15, ls: .34, lr: .22, q: .55, sb: .3 }, door: 8.6 },
  'AC-RJ-01': { src: 'E175', x: [0, .25, .55, .95, 1.6, 1.85, 2.15, 2.8, 3.6, 4.5, 5.6], top: [-.4, .15, .48, .7, .9, 1.27, 1.45, 1.57, 1.63, 1.67, 1.675], bot: [-.4, -.75, -1.02, -1.24, -1.44, -1.5, -1.55, -1.62, -1.66, -1.675, -1.675], hw: [0, .45, .72, .95, 1.2, 1.26, 1.33, 1.42, 1.48, 1.5, 1.505],
    cab: { zs: 1.03, h: .29, vd: .16, lean: .12, ls: .26, lr: .17, q: .42, sb: .4 },
    door: 3.5 },
  'AC-TP-01': { src: 'ATR 72', x: [0, .3, .7, 1.2, 1.8, 2.05, 2.35, 3.3, 4.2, 5.0, 6.3], top: [-.45, -.05, .3, .6, .82, 1.1, 1.24, 1.33, 1.38, 1.4, 1.4], bot: [-.45, -.75, -.95, -1.12, -1.25, -1.28, -1.31, -1.38, -1.4, -1.4, -1.4], hw: [0, .38, .62, .85, 1.05, 1.11, 1.18, 1.33, 1.39, 1.4, 1.4],
    cab: { zs: .87, h: .25, vd: .14, lean: .1, ls: .24, lr: .15, q: .45, sb: .4 },
    door: 3.4 },
  // the small types (the owner's photos 15:49–16:17, D‑282: the real type's measures): the cowling and the cabin, the cabin's glazing
  'AC-PR-01': { src: 'Cessna 172S', x: [0, .12, .28, .6, 1.1, 1.45, 2.15, 3.3, 3.9], top: [0, .1, .2, .28, .34, .38, .72, .72, .56], bot: [0, -.1, -.36, -.46, -.52, -.56, -.56, -.56, -.56], hw: [0, .1, .3, .45, .52, .56, .56, .56, .56],
    cab: { zs: .40, h: .28, vd: .45, lean: .04, ls: .9, lr: .75, sb: -.8, pil: .09 }, door: 2.4 },
  'AC-LT-01': { src: 'Beechcraft Baron 58', x: [0, .25, .7, 1.4, 2.0, 2.6, 5.0, 5.8, 6.3], top: [-.15, .05, .2, .3, .34, .7, .7, .62, .61], bot: [-.15, -.38, -.5, -.58, -.6, -.6, -.6, -.6, -.61], hw: [0, .2, .38, .52, .6, .61, .61, .61, .61],
    cab: { zs: .36, h: .25, vd: .4, lean: .1, ls: .8, lr: .62, n: 4, sb: -.6, pil: .11 }, door: 4.4 },
  'AC-BJ-01': { src: 'Citation Mustang', x: [0, .3, .8, 1.5, 2.1, 2.7, 3.4], top: [-.15, .05, .2, .32, .38, .74, .78], bot: [-.15, -.35, -.5, -.62, -.7, -.76, -.78], hw: [0, .22, .42, .6, .7, .77, .78],
    cab: { zs: .40, h: .28, vd: .25, lean: .15, ls: .5, lr: .35, sb: .2, pil: .08 }, door: 3.0 },
  'AC-CN-01': { src: 'Piaggio P.180', x: [0, .5, 1.2, 2.0, 2.6, 3.3, 4.2], top: [-.2, .1, .35, .48, .55, .9, .975], bot: [-.2, -.45, -.62, -.75, -.82, -.9, -.975], hw: [0, .3, .55, .74, .82, .92, .975],
    cab: { zs: .55, h: .3, vd: .3, lean: .18, ls: .55, lr: .4, sb: .25, pil: .08 }, door: 3.8 },
  'AC-AM-01': { src: 'ICON A5', x: [0, .4, 1.0, 1.5, 2.3, 3.0, 3.6, 4.3, 5.2, 6.1, 6.93], top: [-.25, -.02, .12, .18, .6, .62, .56, .42, .4, .44, .5], bot: [-.25, -.48, -.6, -.62, -.65, -.65, -.6, -.3, -.05, .12, .3], hw: [0, .3, .55, .63, .65, .65, .6, .32, .22, .16, .06],
    cab: { zs: .16, h: .42, vd: .3, lean: .12, ls: .7, n: 1, sb: -.1, pil: .06 }, door: 2.0 },
  'AC-TB-01': { src: 'Cessna 408 SkyCourier', x: [0, .4, 1.0, 1.6, 2.4, 3.0], top: [-.3, .1, .4, .55, 1.0, 1.05], bot: [-.3, -.6, -.85, -.98, -1.05, -1.05], hw: [0, .45, .8, .98, 1.05, 1.05],
    cab: { zs: .55, h: .38, vd: .45, lean: .2, ls: .7, lr: .5, sb: -.2, pil: .1 }, door: 3.4 }
};
// a smooth curve through a table (Catmull-Rom on the samples; flat outside them)
function tab(X, Y, x) { const n = X.length; if (x <= X[0]) return Y[0]; if (x >= X[n - 1]) return Y[n - 1]; let i = 0; while (x > X[i + 1]) i++;
  const t = (x - X[i]) / (X[i + 1] - X[i]), y0 = Y[Math.max(0, i - 1)], y1 = Y[i], y2 = Y[i + 1], y3 = Y[Math.min(n - 1, i + 2)], m1 = (y2 - y0) / 2, m2 = (y3 - y1) / 2;
  return (2 * t * t * t - 3 * t * t + 1) * y1 + (t * t * t - 2 * t * t + t) * m1 + (-2 * t * t * t + 3 * t * t) * y2 + (t * t * t - t * t) * m2 }
const TYPES = {
  'AC-MW-01': { he: 'רחב-גוף דו-מנועי', model: 'TD-789', fit: [1, 1], L: 62.81, WS: 60.12, fw: 5.77, fh: 5.97, wc: 9.6, tc: 1.9, sw: 14.5, nl: .085, tl: .22, zb: 1.95, H: 17.02, wz: 2.6, dih: 6, wt: [1.35, .28], kink: .34,
    winglet: 0, eng: [.32], ed: 3.3, elen: 1.3, hs: .33, gear: { main: [[4.9, 2]], tire: [.68, .45] }, doors: [.109, .40, .64, .86], win: [.13, .88, 48, [[.37, .42], [.62, .66]]], liv: 'sunbeak',
    src: 'Boeing 787-9 במקום התלת-מנועי (הבעלים 16:46, סעיף 3 — ברירת מחדל שממתינה לאישור; אותו תפקיד, בלי מטוס נוסף): אורך 62.81 מ׳, מוטה 60.12, גובה 17.02, גוף 5.77 × 5.97; כנף משוכה 32° עם קצה כנף נטוי (בלי כנפון), שני מנועים גדולים מתחת לכנף, זנב רגיל, 4 דלתות לצד, חלונות גדולים. לא בטוח: מוטת המייצב (≈19.8), קוטר המעטפת של המנוע (3.3)' },
  'AC-LG-01': { he: 'מטוס נוסעים גדול', model: 'TW-350', fit: [1, 0.9839], L: 70.66, WS: 64.44, fw: 5.96, wc: 10, tc: 2, sw: 16, nl: .075, tl: .2, zb: 2.6, H: 19.41, wz: 3.2, dih: 7, wt: [1.5, .32], kink: .34,
    winglet: 1.8, eng: [.27, .5], ed: 2.9, elen: 1.1, hump: 1.95, hr: [.85, .7], hs: .33, gear: { main: [[5.6, 2], [1.9, 2]], tire: [.62, .42] }, doors: [.121, .40, .62, .86], win: [.095, .9, 56, [[.38, .42], [.6, .64]]], liv: 'mirage',
    src: 'Boeing 747-400: אורך 70.66 מ׳, מוטה 64.44 מ׳, גובה 19.41 מ׳ (הבעלים 16:46: היה 66.8); קומה עליונה בחלק הקדמי; 4 מנועים מתחת לכנף, winglets נטויים 1.8 מ׳, זנב רגיל' },
  'AC-NB-01': { he: 'צר-גוף', model: 'TN-320', fit: [0.9911, 0.9666], L: 37.57, WS: 35.8, fw: 4, wc: 6.4, tc: 1.5, sw: 9, nl: .1, tl: .22, zb: 1.65, H: 11.76, wz: 2.1, dih: 6, wt: [.95, .22], kink: .34,
    winglet: 2.2, eng: [.34], ed: 2.2, elen: 1.15, hs: .36, gear: { main: [[3.8, 1]], tire: [.58, .38] }, doors: [.116, .88], win: [.17, .84, 28, [[.4, .46]]], liv: 'aurelia',
    src: 'Airbus A320ceo עם sharklets: אורך 37.57 מ׳, מוטה 35.80 מ׳, גובה 11.76 מ׳' },
  'AC-TP-01': { he: 'טורבו-פרופ אזורי', model: 'TP-72', fit: [0.9854, 1], L: 27.17, WS: 27.05, fw: 2.8, wc: 2.6, tc: 1.7, sw: .5, nl: .12, tl: .26, zb: .95, H: 7.65, high: true, dih: 1.2, wt: [.5, .25], kink: 0,
    winglet: 0, prop: [.27], ttail: true, hs: .3, gear: { main: [[2.05, 1]], tire: [.45, .3], sponson: true }, doors: [.123, .86], win: [.22, .8, 18, []], liv: 'skyline',
    src: 'ATR 72-600: אורך 27.17 מ׳, מוטה 27.05 מ׳, גובה 7.65 מ׳; כנף עליונה, זנב T ומדחפים' },
  // p390 · the rest of the game's fleet (the AC table: L, WS, fw, wc, tc, sw, the engines; the heights of the real class)
  'AC-RJ-01': { he: 'סילון אזורי', model: 'TR-75', fit: [0.9848, 0.9706], L: 31.68, WS: 26.0, fw: 3.01, fh: 3.35, wc: 4.7, tc: 1.25, sw: 5.6, nl: .1, tl: .24, zb: 1.15, H: 9.86, wz: 1.55, dih: 5, wt: [.6, .16], kink: .32,
    winglet: 1.3, eng: [.34], ed: 1.5, elen: 1.05, hs: .38, gear: { main: [[2.6, 1]], tire: [.5, .3] }, doors: [.109, .87], win: [.2, .83, 21, [[.43, .47]]], liv: 'aurelia',
    src: 'Embraer E175 (הבעלים 16:46, סעיף 2 — דגם אחד, כל הצורה ממנו): אורך 31.68 מ׳, מוטה 26.00 (כנף STD), גובה 9.86, גוף 3.01 × 3.35 (בועה כפולה); כנף נמוכה משוכה 23.5° עם כנפונים, שני CF34-8E מתחת לכנף, זנב רגיל עם מייצב על הגוף, 21 חלונות. לא בטוח: מפשק הגלגלים (5.2), מוטת המייצב (≈9.9)' },
  'AC-QJ-01': { he: 'ארבע-מנועי אזורי', model: 'TQ-410', fit: [0.9946, 1], L: 31.0, WS: 26.21, fw: 3.56, wc: 5.4, tc: 1.6, sw: 4, nl: .1, tl: .22, zb: 1.0, H: 8.59, high: true, dih: -3, wt: [.6, .2], kink: 0,
    winglet: 0, eng: [.22, .4], ed: 1.25, elen: 1.1, ttail: true, hs: .4, gear: { main: [[2.4, 1]], tire: [.5, .3], sponson: true }, doors: [.22, .86], win: [.17, .84, 26, [[.4, .46]]], liv: 'aurelia', src: 'BAe 146-300 / Avro RJ100: אורך 31.0 מ׳, מוטה 26.21 מ׳, גובה 8.59 מ׳, גוף 3.56 מ׳ (הבעלים 16:46: היה 35 × 31); כנף עליונה, 4 מנועים, זנב T' },
  'AC-CG-01': { he: 'מטוס מטען', model: 'TF-76F', fit: [0.9876, 1], L: 54.94, WS: 47.57, fw: 5.03, wc: 8.6, tc: 2.0, sw: 12, nl: .09, tl: .22, zb: 1.6, H: 15.85, wz: 2.4, dih: 6, wt: [1.15, .28], kink: .34,
    winglet: 0, eng: [.34], ed: 2.9, elen: 1.25, hs: .39, cargo: true, gear: { main: [[4.65, 2]], tire: [.62, .42] }, doors: [.12], liv: 'aurelia', src: 'Boeing 767-300F: אורך 54.94 מ׳, מוטה 47.57 מ׳, גובה 15.85 מ׳; כנף נמוכה משוכה 31.5°, שני מנועים מתחת לכנף, זנב רגיל, בלי חלונות נוסעים (הבעלים 18:21: לא כנף עליונה וזנב T)' },
  'AC-HC-01': { he: 'מטוס מטען כבד', model: 'TH-40F', fit: [0.9715, 1], L: 69.1, WS: 73.3, fw: 6.4, wc: 10, tc: 3, sw: 10, nl: .07, tl: .2, zb: 1.6, H: 21.08, high: true, dih: -3, wt: [1.5, .4], kink: 0,
    winglet: 0, eng: [.22, .46], ed: 2.8, elen: 1.1, hs: .36, cargo: true, gear: { main: [[3.4, 5]], tire: [.62, .42], sponson: true }, doors: [.1], liv: 'aurelia', src: 'Antonov An-124-100: אורך 69.1 מ׳, מוטה 73.3 מ׳, גובה 21.08 מ׳; כנף עליונה עם שיפוע כלפי מטה, 4 מנועים מתחת לכנף, זנב רגיל (הבעלים 18:21: לא T)' },
  'AC-BJ-01': { he: 'סילון עסקים', model: 'TJ-60', fit: [0.9642, 1], L: 12.37, WS: 13.16, fw: 1.55, wc: 2.4, tc: 1.0, sw: .5, nl: .14, tl: .28, zb: .45, H: 4.09, wz: .55, dih: 4, wt: [.32, .11], kink: .25, wingU: .096,
    winglet: 0, reng: { at: .72, ed: .58, elen: 1.75 }, ttail: true, hs: .36, gear: { main: [[1.6, 1]], tire: [.3, .17] }, doors: [.2], win: [.31, .5, 4, []], liv: 'aurelia',
    src: 'Cessna Citation Mustang 510 (Textron Aviation): אורך 12.37 מ׳, מוטה 13.16 מ׳, גובה 4.09 מ׳, רוחב התא 1.40 מ׳ מבפנים; שני מנועים על הגוף מאחור' },
  'AC-PR-01': { he: 'מטוס קל חד-מנועי', model: 'TA-12', fit: [1, 1], L: 8.28, WS: 11.0, fw: 1.12, wc: 1.63, tc: 1.12, sw: 0, nl: .16, tl: .32, zb: .62, H: 2.72, high: true, dih: 1.7, wt: [.2, .13], kink: .5, wingU: .24,
    winglet: 0, nprop: { r: .965 }, strut: true, hs: .31, gear: { main: [[1.27, 1]], tire: [.24, .14] }, doors: [], win: null, liv: 'aurelia',
    src: 'Cessna 172S (Textron Aviation): אורך 8.28 מ׳, מוטה 11.00 מ׳, גובה 2.72 מ׳, רוחב התא 1.0 מ׳ מבפנים, מדחף 1.93 מ׳; כנף גבוהה עם תומכות' },
  'AC-LT-01': { he: 'דו-מנועי קל', model: 'TB-58', fit: [0.9934, 1], L: 9.09, WS: 11.53, fw: 1.22, wc: 2.13, tc: .95, sw: .45, nl: .2, tl: .32, zb: .55, H: 2.97, wz: .62, dih: 6, wt: [.28, .12], kink: 0, wingU: .148,
    winglet: 0, prop: [.28], pr: .99, pn: .34, hs: .42, gear: { main: [[1.46, 1]], tire: [.3, .17] }, doors: [], win: null, liv: 'aurelia',
    src: 'Beechcraft Baron 58 (Textron Aviation): אורך 9.09 מ׳, מוטה 11.53 מ׳, גובה 2.97 מ׳, מדחפים 1.98 מ׳, רוחב מסלול 2.92 מ׳; כנף נמוכה, שני מנועים בכנף' },
  'AC-CN-01': { he: 'מטוס קנרד עם מדחפים דוחפים', model: 'TV-180', fit: [1, 1], L: 14.41, WS: 14.03, fw: 1.95, wc: 1.65, tc: .7, sw: .35, nl: .16, tl: .3, zb: .6, H: 3.97, wz: 1.2, dih: 2, wt: [.22, .1], kink: 0, wingU: -.069,
    winglet: 0, prop: [.27], pusher: true, pr: 1.08, pn: .34, canard: { u: .36, span: 1.9, chord: .65 }, ttail: true, hs: .3, gear: { main: [[1.4, 1]], tire: [.3, .18] }, doors: [.22], win: [.33, .55, 6, []], liv: 'aurelia',
    src: 'Piaggio P.180 Avanti II (Piaggio Aerospace): אורך 14.41 מ׳, מוטה 14.03 מ׳, גובה 3.97 מ׳, מדחפים דוחפים 2.16 מ׳; כנף קדמית קטנה (canard), כנף ראשית מאחור וזנב T' },
  'AC-AM-01': { he: 'מטוס אמפיבי', model: 'TS-12', fit: [0.9714, 1], L: 7.01, WS: 10.61, fw: 1.3, wc: 1.5, tc: 1.05, sw: .1, nl: .2, tl: .35, zb: .42, H: 2.47, high: true, dih: 1, wt: [.2, .12], kink: 0, wingU: .154,
    winglet: 0, cpush: { r: .84, at: .64, z: .6 }, seawing: { at: .3, span: .85, chord: 1.4, z: -.32 }, hull: true, ttail: true, hs: .31, gear: { main: [[.95, 1]], tire: [.22, .13] }, doors: [], win: null, liv: 'aurelia',
    src: 'ICON A5 (ICON Aircraft, iconaircraft.com/a5): אורך 7.01 מ׳, מוטה 10.61 מ׳, גובה 2.47 מ׳ (הבעלים 18:21); גוף סירה, כנף גבוהה, מדחף דוחף אחד מאחורי תא הטייס, "כנפי ים" בצדי הגוף וזנב T' },
  'AC-TB-01': { he: 'מטען קטן דו-מנועי', model: 'TK-20F', fit: [0.952, 1], L: 16.8, WS: 22.02, fw: 2.1, wc: 2.0, tc: 1.3, sw: .2, nl: .1, tl: .3, zb: .9, H: 6.3, high: true, dih: 2, wt: [.3, .18], kink: .4, wingU: .105, box: 4.5,
    winglet: 0, prop: [.32], pr: 1.4, pn: .45, strut: true, cargo: true, cargoAt: .6, ttail: true, hs: .3, gear: { main: [[1.7, 1]], tire: [.42, .25], sponson: true }, doors: [], win: null, liv: 'aurelia',
    src: 'Cessna 408 SkyCourier (Textron Aviation) במקום Skyvan (ברירת מחדל של המתאם 16:15, לאישור הבעלים): אורך 16.80 מ׳, מוטה 22.02 מ׳, גובה 6.30 מ׳ (Wikipedia); גוף קופסתי, כנף גבוהה עם תומכות, שני טורבו-פרופ, כן נסע קבוע, זנב אחד עם מייצב בראשו (התמונות של הבעלים 16:36); 3 מכולות LD3. לא בטוח: רוחב הגוף (2.1)' }
};

// ======================================================================================================================================
// the fuselage: rings along a (metres aft of the nose tip).  ring(a) → {zm, rv, rs, hump}; the point at angle θ (0 = east side,
// 90° = crown): (rs·cos θ, yN − a, zm + rv·sin θ + hump·g(sin θ))
function fusShape(t) {
  const L = t.L, R = t.fw / 2, Rz = (t.fh || t.fw) / 2, zc = t.zb + Rz, nl = t.nl * L, tlv = t.tl * L * 1.3, zTip = zc - .12 * Rz, NR = NOSE[t.id],   // Rz: the half height (t.fh, the E175's 3.35 on 3.01)
  xN = NR ? NR.x[NR.x.length - 1] : 0;
  // D‑278 (the owner 09:21, "the front must be real"): an ogive — the plan narrows over 1.6 nose lengths to a rounder point, the crown
  // rises over 1.9 (the cockpit's slope), the chin over 1.0
  const At = 1.9 * nl, Ab = 1.0 * nl, As = 1.6 * nl, aT = L - tlv, ze = zc + .4 * Rz, re = .15 * R;
  const sq = (x, A, e) => x >= A ? 1 : Math.pow(Math.max(0, 1 - Math.pow(1 - x / A, e || 2.3)), .5);
  const hr = t.hr || [.2, 2.2], hump = a => !t.hump ? 0 : t.hump * sm((a - hr[0] * nl) / (hr[1] * nl)) * (1 - sm((a - .3 * L) / (.1 * L)));
  const f = a => {
    let top, bot, rs;
    if (NR && a < xN) { top = zc + tab(NR.x, NR.top, a); bot = zc + tab(NR.x, NR.bot, a); rs = tab(NR.x, NR.hw, a); if (a < .02) { rs = Math.max(rs, .0) } }   // R‑14: the real nose
    else if (a < aT) { top = zTip + (zc + Rz - zTip) * sq(a, At, 2.1); bot = zTip - (zTip - (zc - Rz)) * sq(a, Ab, 2.4); rs = R * sq(a, As, 1.75) }
    else { const s = (a - aT) / (L - aT); top = zc + Rz + (ze + re - (zc + Rz)) * Math.pow(s, 1.8); bot = zc - Rz + (ze - re - (zc - Rz)) * Math.pow(s, .8); rs = R + (re - R) * Math.pow(s, 1.3) }
    return { zm: (top + bot) / 2, rv: (top - bot) / 2, rs, hump: hump(a) };
  };
  // D‑281 (option 1): round the cockpit the upper half of the section is broader (a superellipse, q < 1), so the sill runs across the
  // nose in a very shallow V — the crown itself (q⁰ = 1) unchanged; ahead and aft of the cockpit as approved
  if (t.hump && NR && NR.cab) f.hgW = 1;
  if (NR && NR.cab && NR.cab.q) { const zs = zc + NR.cab.zs; let aC = 0; while (aC < L * .5) { const r = f(aC); if (r.zm + r.rv + r.hump >= zs) break; aC += .02 }
    const q0 = NR.cab.q; f.q = a => lerp(1, lerp(q0, 1, sm((a - aC - 2.2) / 2)), sm((a - aC + 1.1) / .9)) }
  if (t.box) { const n = t.box, nl2 = nl * 1.6; f.box = a => a < nl2 ? 2 + (n - 2) * sm(a / nl2) : a > L - tlv * .7 ? 2 + (n - 2) * (1 - sm((a - (L - tlv * .7)) / (tlv * .7))) : n }   // round at the nose and the tail's end
  f.R = R; f.Rz = Rz; f.zc = zc; f.nl = nl; f.At = At; f.As = As; f.aT = aT; f.aC = Math.max(At, Ab, As, xN, t.hump ? .42 * L : 0); f.L = L; f.NR = NR;
  return f;
}
const hg = s => sm((s - .4) / .6);   // the upper deck: a ridge on the crown
const hgW = s => sm((s - .12) / .7);   // D‑281: the 747's upper deck as broad as the real one (its cockpit ~3.5 m wide)
function fusP(F, yN, a, th) { const r = F(a), q = F.q ? F.q(a) : 1; let s = Math.sin(th), c = Math.cos(th);
  if (F.box) { const e = 2 / F.box(a); c = Math.sign(c) * Math.pow(Math.abs(c), e); s = Math.sign(s) * Math.pow(Math.abs(s), e) }   // a box-like section (t.box): a superellipse
  return [r.rs * c, yN - a, r.zm + r.rv * (s > 0 && q !== 1 ? Math.pow(s, q) : s) + (s > 0 ? r.hump * (F.hgW ? hgW(s) : hg(s)) : 0)] }
function fusN(F, yN, a, th) {   // the outward normal
  const e = .004, p = fusP(F, yN, a, th), pa = fusP(F, yN, a + .05, th), pt = fusP(F, yN, a, th + e);
  let n = nrm(crs(sub(pt, p), sub(pa, p))); const r = F(a); if (dot(n, [p[0], 0, p[2] - r.zm]) < 0) n = [-n[0], -n[1], -n[2]]; return n;
}
// D‑278: the point of the nose at height z in the direction phi (degrees; 0 ahead, 90 abeam) seen from the axis at the full-width
// station a = F.As, on the side sd (+1 east) → { p, a, th } (null when the nose does not reach that height there)
function nosePt(F, yN, phi, z, sd) {
  const at = a => { const r = F(a); let s = (z - r.zm) / (r.rv || 1e-6); if (s > 1 || s < -1) return null; const th = Math.asin(s), x = r.rs * Math.cos(th); return { a, th, ph: Math.atan2(x, F.As - a) / D2R } };
  const A1 = F.As * 1.8; let best = null, prev = null;
  for (let i = 0; i <= 240; i++) { const a = A1 * i / 240, q = at(a); if (!q) { prev = null; continue }
    if (prev && (prev.ph - phi) * (q.ph - phi) <= 0) { let lo = prev, hi = q; for (let k = 0; k < 24; k++) { const m = at((lo.a + hi.a) / 2); if (!m) break; if ((lo.ph - phi) * (m.ph - phi) <= 0) hi = m; else lo = m } best = lo; break }
    prev = q }
  if (!best) return null;
  const th = sd > 0 ? best.th : Math.PI - best.th;
  return { p: fusP(F, yN, best.a, th), a: best.a, th };
}
// the livery on the body: colour at (a, θ) and the breaks along a for the strip at θ (so a boundary is a smooth curve)
function liveryFns(t, lv, F) {
  const L = t.L, nl = F.nl, tl = t.tl * L, tail0 = L - 1.35 * tl;
  const tailAt = th => tail0 + .14 * tl * Math.max(0, Math.sin(th));   // the tail section's front edge bulges aft on the crown (the game's curve)
  const w = lv.w, bA0 = 1.1 * nl, bP = (tail0 - bA0) / 8, beak = w === 'allover' ? mixC(lv.s, lv.b, .42) : lv.s;
  const col = (a, th) => {
    const s = Math.sin(th), c = Math.abs(Math.cos(th)), deg = Math.asin(cl(s, -1, 1)) / D2R;
    if (a > tailAt(th)) return lv.t;
    if (w === 'allover') { if (a < .09 * nl) return beak;   // the beak: a small soft tip (the owner 14:39 (4): smaller, softer; it was .16 · nl, black)
      if (deg > 4 && deg < 8) return lv.s; if (s < -.45) return lv.u; return lv.b }
    if (w === 'nose') { const nb = 1.15 * nl - .12 * nl * Math.max(0, s); if (a < nb) return lv.s; if (deg > 5 && deg < 8) return lv.s; if (s < -.5) return lv.u; return lv.b }
    if (w === 'spine') { if (a > .8 * nl && c < .36 && s > 0) return lv.s; if (deg > 5 && deg < 9) return lv.s; if (s < -.45) return lv.u; return lv.b }
    // p390 · the game's other styles: bands (two stripes along the side), split (the lower half in the second colour), swoosh (a band
    // that rises from the belly at the nose to the crown at the tail), dots (as classic; the confetti is left out)
    if (w === 'bands') { const u = a - bA0 - .9 * Math.cos(th) * t.fw / 2; if (a > bA0 && a < tail0 - .2 * bP && u > 0 && (u % bP) < .42 * bP) return lv.s; if (s < -.5) return lv.u; return lv.b }   // the game's: slanted stripes across the body
    if (w === 'split') { if (a > .9 * nl && s < -.08) return lv.s; return lv.b }
    if (w === 'swoosh') { const q = a / L, d0 = -35 + 85 * q; if (a > nl && deg > d0 && deg < d0 + 10) return lv.s; if (s < -.5) return lv.u; return lv.b }
    // classic: the cheat line under the windows, a thin one above
    if (a > 1.3 * nl && deg > 5 && deg < 13) return lv.s; if (a > 1.6 * nl && deg > 29 && deg < 31.5) return lv.s; if (s < -.5) return lv.u; return lv.b;
  };
  const breaks = th => { const s = Math.sin(th), B = [tailAt(th)];
    if (w === 'allover') B.push(.09 * nl); if (w === 'nose') B.push(1.15 * nl - .12 * nl * Math.max(0, s)); if (w === 'spine') B.push(.8 * nl); if (w === 'classic') B.push(1.3 * nl, 1.6 * nl);
    if (w === 'bands') { const o = .9 * Math.cos(th) * t.fw / 2; for (let k = 0; k < 9; k++) B.push(bA0 + o + k * bP, bA0 + o + (k + .42) * bP) }
    return B };
  return { col, breaks, tailAt };
}

// ======================================================================================================================================
// a face: { P: [[x,y,z] …], c: hex, m: material, n?: normal, g?: [nA, nB] (a gradient across the face from edge 0–3 to edge 1–2),
//           both?: no back-face test, a?: alpha, line?: stroke only (w metres) }
function face(P, c, m, o) { return Object.assign({ P, c, m: m || 'paint' }, o || {}) }
const orient = (f, d) => { if (dot(faceN(f.P), d) < 0) f.P.reverse(); return f };
const faceN = P => { let n = [0, 0, 0]; for (let i = 0; i < P.length; i++) { const p = P[i], q = P[(i + 1) % P.length]; n[0] += (p[1] - q[1]) * (p[2] + q[2]); n[1] += (p[2] - q[2]) * (p[0] + q[0]); n[2] += (p[0] - q[0]) * (p[1] + q[1]) } return nrm(n) };

// the fuselage as strips: per θ facet, along a; merged where the section is constant and the colour does not change
function buildFuselage(t, lv, yN, F, LF, opt) {
  const faces = [], N = opt && opt.lod ? 40 : 72, L = t.L, base = [];
  const nA = 18, step = a => a < F.aC ? Math.max(.12, F.nl / 12) : a > F.aT ? Math.max(.15, (L - F.aT) / 16) : 1.2;
  for (let a = 0; a < L - 1e-6;) { base.push(a); a = Math.min(L, a + step(a)) } base.push(L);
  for (let k = 0; k < N; k++) {
    const t0 = -Math.PI / 2 + k * TAU / N, t1 = t0 + TAU / N, tm = (t0 + t1) / 2;
    const A = base.concat(LF.breaks(tm).filter(x => x > 0 && x < L)).sort((p, q) => p - q);
    let run = null;
    const flush = () => { if (!run) return; const P = [fusP(F, yN, run.a0, t0), fusP(F, yN, run.a0, t1), fusP(F, yN, run.a1, t1), fusP(F, yN, run.a1, t0)], am = (run.a0 + run.a1) / 2;
      faces.push(face(P, run.c, 'paint', { g: [fusN(F, yN, am, t0), fusN(F, yN, am, t1)], g4: [fusN(F, yN, run.a0, t0), fusN(F, yN, run.a0, t1), fusN(F, yN, run.a1, t1), fusN(F, yN, run.a1, t0)], fus: 1 })); run = null };   // g4: the corners' normals (the owner 14:39 (1): the light smooth along the body too)
    for (let i = 0; i + 1 < A.length; i++) {
      const a0 = A[i], a1 = A[i + 1]; if (a1 - a0 < 1e-4) continue;
      const c = LF.col((a0 + a1) / 2, tm), flat = a0 >= F.aC - 1e-6 && a1 <= F.aT + 1e-6;
      if (run && run.flat && flat && run.c === c && Math.abs(run.a1 - a0) < 1e-6) { run.a1 = a1; continue }
      flush(); run = { a0, a1, c, flat };
    }
    flush();
  }
  return faces;
}

// a body of revolution along y (a nacelle): rings (y, ρ) around the axis (x0, ·, z0); strips with gradients
function buildRevolve(x0, z0, rings, col, mat, N) {
  const faces = []; N = N || 40;
  for (let k = 0; k < N; k++) {
    const t0 = k * TAU / N, t1 = t0 + TAU / N;
    for (let i = 0; i + 1 < rings.length; i++) {
      const [ya, ra, ca] = rings[i], [yb, rb] = rings[i + 1];
      const P = [[x0 + ra * Math.cos(t0), ya, z0 + ra * Math.sin(t0)], [x0 + ra * Math.cos(t1), ya, z0 + ra * Math.sin(t1)], [x0 + rb * Math.cos(t1), yb, z0 + rb * Math.sin(t1)], [x0 + rb * Math.cos(t0), yb, z0 + rb * Math.sin(t0)]];
      const rp = (rb - ra) / ((yb - ya) || 1e-6), nn = th => nrm([Math.cos(th), -rp, Math.sin(th)]);
      faces.push(face(P, ca || col, mat, { g: [nn(t0), nn(t1)] }));
    }
  }
  return faces;
}
// a disc facing +y (south) at y, centre (x0, z0): ellipse on the screen
function disc(x0, y, z0, r, col, mat, o) { const P = []; for (let i = 0; i < 28; i++) { const t = i / 28 * TAU; P.push([x0 + r * Math.cos(t), y, z0 + r * Math.sin(t)]) } return face(P, col, mat, Object.assign({ n: [0, 1, 0] }, o || {})) }

// a lofted plate along a span (wing, tailplane, winglet): stations [{x, yLE, yTE, z, t}] (x = |span position| × side), chord profile
const CH = [0, .03, .12, .3, .55, .8, 1], TOP = [0, .3, .44, .5, .42, .27, .05], BOT = [0, .26, .36, .38, .3, .17, .03];
function buildPlate(st, col, o) {
  o = o || {}; const faces = [];
  const pt = (s, i, up) => { const y = lerp(s.yLE, s.yTE, CH[i]); return [s.x, y, s.z + (up ? TOP[i] : -BOT[i]) * s.t] };
  for (let j = 0; j + 1 < st.length; j++) {
    const A = st[j], B = st[j + 1];
    for (let i = 0; i + 1 < CH.length; i++) {
      faces.push(orient(face([pt(A, i, 1), pt(B, i, 1), pt(B, i + 1, 1), pt(A, i + 1, 1)], col, o.mat || 'paint'), [0, i === 0 ? .5 : 0, 1]));
      faces.push(orient(face([pt(A, i + 1, 0), pt(B, i + 1, 0), pt(B, i, 0), pt(A, i, 0)], sh(col, -.12), o.mat || 'paint'), [0, i === 0 ? .5 : 0, -1]));
    }
  }
  // the ends (the root is inside the fuselage; the tip cap)
  const cap = s => { const U = [], D = []; for (let i = 0; i < CH.length; i++) { U.push(pt(s, i, 1)); D.push(pt(s, i, 0)) } return U.concat(D.reverse()) };
  faces.push(face(cap(st[st.length - 1]), sh(col, -.06), 'paint', { both: false }));
  return faces;
}
// the same plate standing up (fin): stations [{z, yLE, yTE, t}] at x = 0
function buildFin(st, col) {
  const faces = [];
  const pt = (s, i, side) => [side * (side > 0 ? TOP[i] : BOT[i]) * s.t * (BOT[i] > 0 || TOP[i] > 0 ? 1 : 1), lerp(s.yLE, s.yTE, CH[i]), s.z];
  const half = (s, i, side) => [side * .5 * s.t * (i === 0 ? 0 : [0, .55, .82, .97, 1, .82, .2][i]), lerp(s.yLE, s.yTE, CH[i]), s.z];
  for (let j = 0; j + 1 < st.length; j++) {
    const A = st[j], B = st[j + 1];
    for (let i = 0; i + 1 < CH.length; i++) for (const sd of [1, -1]) {
      faces.push(orient(face([half(A, i, sd), half(A, i + 1, sd), half(B, i + 1, sd), half(B, i, sd)], col, 'paint'), [sd, i === 0 ? .3 : 0, 0]));
    }
  }
  const T = st[st.length - 1], U = [], D = []; for (let i = 0; i < CH.length; i++) { U.push(half(T, i, 1)); D.push(half(T, i, -1)) }
  faces.push(orient(face(U.concat(D.reverse()), sh(col, .06), 'paint'), [0, 0, 1]));
  void pt; return faces;
}
// an oriented box: the plan polygon (4 corners, any order around), z bottom / top per corner
function boxFaces(plan, zb, zt, cols, o) {
  o = o || {}; const faces = [], n = plan.length, Zb = i => Array.isArray(zb) ? zb[i] : zb, Zt = i => Array.isArray(zt) ? zt[i] : zt;
  // orientation: make the plan counter-clockwise in (x, y) with y south → use the signed area
  let ar = 0; for (let i = 0; i < n; i++) { const p = plan[i], q = plan[(i + 1) % n]; ar += p[0] * q[1] - q[0] * p[1] }
  const pl = ar > 0 ? plan : plan.slice().reverse(), zbb = ar > 0 ? i => Zb(i) : i => Zb(n - 1 - i), ztt = ar > 0 ? i => Zt(i) : i => Zt(n - 1 - i);
  for (let i = 0; i < n; i++) { const j = (i + 1) % n, p = pl[i], q = pl[j];
    faces.push(face([[p[0], p[1], zbb(i)], [q[0], q[1], zbb(j)], [q[0], q[1], ztt(j)], [p[0], p[1], ztt(i)]], cols.side || cols.top, o.mat || 'matte', { side: i })) }
  faces.push(face(pl.map((p, i) => [p[0], p[1], ztt(i)]), cols.top, o.mat || 'matte', { top: 1 }));
  return faces;
}
// a vertical cylinder: centre, radius, z0..z1 (the drum of the bridge, a column)
function vcyl(cx, cy, r, z0, z1, col, mat, N) {
  const faces = []; N = N || 24;
  for (let i = 0; i < N; i++) { const a = i / N * TAU, b = (i + 1) / N * TAU;
    faces.push(face([[cx + r * Math.cos(a), cy + r * Math.sin(a), z0], [cx + r * Math.cos(b), cy + r * Math.sin(b), z0], [cx + r * Math.cos(b), cy + r * Math.sin(b), z1], [cx + r * Math.cos(a), cy + r * Math.sin(a), z1]], col, mat, { g: [[Math.cos(a), Math.sin(a), 0], [Math.cos(b), Math.sin(b), 0]] })) }
  const T = []; for (let i = 0; i < N; i++) { const a = i / N * TAU; T.push([cx + r * Math.cos(a), cy + r * Math.sin(a), z1]) }
  faces.push(face(T, sh(col, .05), mat, { n: [0, 0, 1] }));
  return faces;
}

// ======================================================================================================================================
// the aircraft: pieces in local metres (origin at the nose gear on the ground, nose to the south = +y)
// ======================================================================================================================================
// D‑281 (the owner 13:50, a standing rule: every detail where the 3D body and the real type's proportions put it, every direction
// from the one model in the one projection, no fix for one direction): the cockpit's windows as one fixed shape on the nose's surface — every view comes from the one body in the one projection (x, y − K·z), only what faces the camera drawn.
//  * the sill: one straight line along the cockpit at the height zs over the axis (a small fall aft, sl, allowed);
//  * the stations along the body (metres from the nose tip): the windscreen from the centre post (where the crown reaches the sill)
//    up to aw on the crown; the pillars [bottom, top] between the windscreen and the opening window, between it and the rear one,
//    and the rear one's end — every pillar leans aft;
//  * the upper edge of every side window just under the roof line of its station (m below the crown in the profile; the rear one
//    m3); the windscreen's from the crown at aw down to the first pillar's top;
//  * per type (NOSE[id].cab) or, for the other types, in fuselage radii from the crown's crossing of the sill.
function cabOf(t, NR, F) {
  // the owner 14:39 (3): the row lower (h ×0.8) and its wrap to the sides shorter (ls ×0.75, lr ×0.7) — the NOSE tables.
  // D‑281 (option 1, the coordinator 14:15 for the owner; agent 3 14:10): one low row (~11 % of the nose's width) on the surface — no
  // cut, the outline smooth: the sill zs one height for the windscreen and the side windows; the windscreen's two panes from the centre
  // post to a corner only vd aft of it (a very shallow V), up to zs + h on the steep part of the crown; then on each side a short
  // opening window and a shorter rear one (ls, lr), their pillars leaning aft (lean); the rear one lower (80 %)
  const R = F.R, C = NR && NR.cab ? NR.cab : {};
  return { zs: C.zs != null ? C.zs : .62 * R, h: C.h != null ? C.h : .22 * R, vd: C.vd != null ? C.vd : .075 * R, lean: C.lean != null ? C.lean : .1 * R, ls: C.ls != null ? C.ls : .28 * R, lr: C.lr != null ? C.lr : .2 * R, sb: C.sb != null ? C.sb : .4, n: C.n || 2, pil: C.pil };
}
function cockpit3D(F, yN, t, NR, decor) {
  const R = F.R, zc = F.zc, C = cabOf(t, NR, F), sc = NR && NR.cab ? 1 : R / 2, post = .022 * sc, pil = C.pil || .028 * sc, pad = .02 * sc;   // the owner 14:39 (2): thin frame and posts (a light aircraft's pillars: cab.pil)
  const crown = a => { const r = F(a); return r.zm + r.rv + r.hump - zc };
  const cross = z => { let a = 0; while (a < F.L * .5 && crown(a) < z) a += .05; let lo = Math.max(0, a - .05), hi = a; for (let k = 0; k < 20; k++) { const m = (lo + hi) / 2; if (crown(m) < z) lo = m; else hi = m } return hi };
  const aC = cross(C.zs), aT = cross(C.zs + C.h), zS = C.zs, zH = C.zs + C.h;
  // the stations: the windscreen's corner, then n side windows (the first ls long, the others lr) — the airliners 2, a light aircraft's cabin more
  const PB = []; { let b = aC + C.vd; PB.push([b, b + C.lean]); for (let k = 1; k <= C.n; k++) { b += k === 1 ? C.ls : C.lr; PB.push([b, b + C.lean * (1 + .15 * k)]) } }
  const b1 = PB[0][0], b2 = PB[1][0], b3 = PB[PB.length - 1][0], aw = aT;
  const zSill = () => zS;
  const thAt = (a, z) => { const r = F(a), Z = zc + z, zt = r.zm + r.rv + r.hump; if (Z >= zt) return Math.PI / 2; if (Z <= r.zm - r.rv) return -Math.PI / 2;
    const q = F.q ? F.q(a) : 1; let lo = -1, hi = 1; for (let k = 0; k < 22; k++) { const m = (lo + hi) / 2, zz = r.zm + r.rv * (m > 0 && q !== 1 ? Math.pow(m, q) : m) + (m > 0 ? r.hump * (F.hgW ? hgW(m) : hg(m)) : 0); if (zz < Z) lo = m; else hi = m } return Math.asin((lo + hi) / 2) };
  const pt = (a, z, sd, xMin) => { let th = thAt(a, z); if (xMin) { const r = F(a), tm = Math.acos(Math.min(1, xMin / Math.max(1e-3, r.rs))); th = Math.min(th, tm) } const T = sd > 0 ? th : Math.PI - th; return { p: fusP(F, yN, a, T), n: fusN(F, yN, a, T) } };
  // the side windows' lower edge: one horizontal line sb·h above the windscreen's (agent 3 14:30: cut level, on aft, not down); the rear one's top a little lower
  const pane = k => { const [p0, q0] = k === 0 ? [aC, aT] : PB[k - 1], [p1, q1] = PB[k], zb = k === 0 ? zS : zS + C.sb * C.h, zt = k === C.n ? zH - .12 * C.h : zH;
    return { B: u => [lerp(p0, p1, u), zb], T: u => [lerp(q0, q1, u), zt], k } };
  const GL = ['#2a4256', '#57748c', '#c4d9e8'], info = { panes: [], aRef: aC, bend: 0, cab: { aC, aw, PB, zs: C.zs, sl: 0, h: C.h } };
  for (const sd of [1, -1]) {
    const frame = [], glass = [], extra = [];
    for (let k = 0; k <= C.n; k++) {
      const P = pane(k), len = Math.hypot(P.B(1)[0] - P.B(0)[0], .5 * (P.T(1)[0] - P.T(0)[0])) || 1, n = k === 0 ? 8 : 5;
      for (const grow of [true, false]) {
        const du0 = grow ? 0 : (k === 0 ? 0 : pil / len), du1 = grow ? -.01 : pil / len, dwb = grow ? -pad : pil * .8, dwt = grow ? 0 : pil * .8 + pad, xMin = k === 0 && !grow ? post : 0;
        const at = (u, w) => { const B = P.B(u), T = P.T(u), hb = (T[1] - B[1]) || 1, wb = dwb / hb, wt = 1 - dwt / hb, W = lerp(wb, wt, w), a = lerp(B[0], T[0], W);
          if (grow && k === 0 && u <= 1e-9) { const p = fusP(F, yN, a, Math.PI / 2); return { p, n: fusN(F, yN, a, Math.PI / 2) } }   // the frame closes on the centre post
          return pt(a, lerp(B[1], T[1], W), sd, xMin) };
        const U = i => lerp(du0, 1 - du1, i / n), outl = [];
        const nm = at(.5, .5).n;
        for (let i = 0; i < n; i++) { const u0 = U(i), u1 = U(i + 1), um = (u0 + u1) / 2, Q = [at(u0, 0), at(um, 0), at(u1, 0), at(u1, 1), at(um, 1), at(u0, 1)], c = at(um, .5);
          let PP = Q.map(q => q.p); if (dot(faceN(PP), c.n) < 0) PP = PP.reverse();
          if (grow) frame.push(face(PP, '#28323b', 'matte', { n: c.n, noSeam: 1 }));
          else glass.push(face(PP, GL[1], 'glass', { g: [nm, nm], grad: GL, gax: [at(um, 0).p, at(um, 1).p], noSeam: 1 })) }
        if (!grow) { for (let i = 0; i <= n; i++) outl.push(at(U(i), 0)); for (let j = 1; j <= 4; j++) outl.push(at(U(n), j / 4)); for (let i = n; i >= 0; i--) outl.push(at(U(i), 1)); for (let j = 3; j >= 1; j--) outl.push(at(U(0), j / 4));
          info.panes.push({ sd, k, far: false, P: outl.map(q => q.p), N: outl.map(q => q.n), AZ: [P.B(0), P.B(1), P.T(1), P.T(0)] }) }
        if (!grow && k === 0) for (const f of [.3, .72]) { const A = at(f, .02), Bq = at(f - .08, .25); extra.push({ line: 1, P: [A.p, Bq.p], c: '#1b2229', w: .022 * sc, n: A.n }) }
        // the sky in the glass: a soft slanted streak across the pane (on its surface)
        if (!grow) { const S = [at(.16, .08), at(.34, .08), at(.56, .94), at(.38, .94)]; let SP = S.map(q => q.p.map((v, i) => v + q.n[i] * .004)); const cn = at(.36, .5).n; if (dot(faceN(SP), cn) < 0) SP = SP.reverse();
          extra.push(face(SP, '#ffffff', 'matte', { n: cn, a: .2, noSeam: 1 })) }
      }
    }
    decor.push(...frame, ...glass, ...extra);
  }
  return info;
}
function bandFor(m, h) {
  const I = m.info, dec = [], BD = cockpit3D(I.F, I.yN, I.t, NOSE[I.id], dec), body = m.pieces.find(p => p.kind === 'body');
  const pieces = m.pieces.map(p => p !== body ? p : Object.assign({}, p, { decor: p.decor.slice(0, I.bandAt).concat(dec, p.decor.slice(I.bandAt)) }));
  return { pieces, info: Object.assign({}, I, { band: BD }) };
}
// the owner 16:46 (1): the model as drawn takes exactly the real length and span — the fin's and the T-tail's trailing edge past the tail
// cone and the winglets' cant outward used to add up to 3.6% (HC-01 2.5 m, NB-01 1.2 m of span); the first build of a type measures its plan
// box and the type is built from then on with L and WS scaled so that the box is L × WS (one factor per type: the row's fit [kL, kW], measured
// offline so that the game pays nothing; a row without it is measured on its first build and kept in FIT)
const FIT = {};
function fitOf(id, livKey, opt, t0) { const m = buildRaw(id, livKey, Object.assign({}, opt, { lod: 1 }), t0); let xa = 1e9, xb = -1e9, ya = 1e9, yb = -1e9;
  for (const p of m.pieces) { for (const f of p.faces || []) for (const q of f.P) { xa = Math.min(xa, q[0]); xb = Math.max(xb, q[0]); ya = Math.min(ya, q[1]); yb = Math.max(yb, q[1]) } }
  const kL = t0.L / Math.max(.1, yb - ya), kW = t0.WS / Math.max(.1, xb - xa);
  return FIT[id] = { kL: Math.abs(kL - 1) < .002 ? 1 : Math.min(1.05, kL), kW: Math.abs(kW - 1) < .002 ? 1 : Math.min(1.05, kW) } }
function build(id, livKey, opt) {
  opt = opt || {}; const t0 = TYPES[id]; if (!t0) throw new Error('A34: unknown type ' + id); t0.id = id;
  const f = opt.raw ? { kL: 1, kW: 1 } : t0.fit ? { kL: t0.fit[0], kW: t0.fit[1] } : FIT[id] || fitOf(id, livKey, opt, t0);   // t0.fit: measured once (dev/fleet_dims.js checks it)
  return buildRaw(id, livKey, opt, f.kL === 1 && f.kW === 1 ? t0 : Object.assign({}, t0, { L: t0.L * f.kL, WS: t0.WS * f.kW, Lr: t0.L, WSr: t0.WS })) }
function buildRaw(id, livKey, opt, t) {
  opt = opt || {};
  const lv = livKey && typeof livKey === 'object' ? livKey : LIV[livKey || t.liv], L = t.L, R = t.fw / 2, HS = t.WS / 2, yN = .17 * L, yC = -.33 * L, x0 = .06 * L, TF = t.boom ? Object.assign({}, t, { L: t.L * t.boom.pod }) : t, F = fusShape(TF), LF = liveryFns(TF, lv, F), NRV = opt.lod ? 24 : 44;
  const ofU = u => yC + u * L;   // game frame u (fraction of L from the centre, + forward) → local y
  const pieces = [];
  const piece = (kind, faces, extra) => { const p = Object.assign({ kind, faces, decor: [] }, extra || {}); pieces.push(p); return p };
  const topAt = a => { const r = F(a); return r.zm + r.rv + r.hump };
  // ---- the body ----
  const body = buildFuselage(TF, lv, yN, F, LF, opt);
  const decor = [];
  // the cockpit's windows (D‑281): one low row fixed on the nose — cockpit3D() below
  const bandAt = decor.length, BD = opt.noBand ? null : cockpit3D(F, yN, t, NOSE[id], decor);   // p390: noBand — the game adds the band of each direction (bandFor)
  // the nose's gloss (R‑14 (2)): a soft highlight along the upper curve of the nose
  { const nl = F.nl, a0 = .12 * nl, a1 = Math.min(F.aC * .55, 1.1 * nl), P = [];
    for (let i = 0; i <= 8; i++) P.push(fusP(F, yN, lerp(a0, a1, i / 8), 101 * D2R)); for (let i = 8; i >= 0; i--) P.push(fusP(F, yN, lerp(a0, a1, i / 8), 118 * D2R));
    decor.push(face(P.map(p => [p[0], p[1], p[2] + .01]), '#ffffff', 'matte', { n: [0, 0, 1], a: .16, noSeam: 1 })) }
  // the front door, the bridge's (R‑14 (3)): the port side's first door — a panel, its outline, its window
  { const NR = NOSE[id], a = NR ? NR.door : (t.doors && t.doors[0] || .2) * L, P = [], W = [];
    for (const d of [4, 14, 24, 34]) P.push(fusP(F, yN, a - .5, d * D2R)); for (const d of [34, 24, 14, 4]) P.push(fusP(F, yN, a + .5, d * D2R));
    decor.push(face(P.map(p => [p[0], p[1], p[2] + .01]), '#000000', 'matte', { n: fusN(F, yN, a, 19 * D2R), a: .07, noSeam: 1 }));
    decor.push({ line: 1, P: P.concat([P[0]]).map(p => [p[0], p[1], p[2] + .015]), c: 'rgba(20,30,40,.75)', w: .07 });
    for (const [d, da] of [[24, -.18], [24, .18], [30, .18], [30, -.18]]) W.push(fusP(F, yN, a + da, d * D2R));
    decor.push(face(W.map(p => [p[0], p[1], p[2] + .02]), '#22384e', 'glass', { n: fusN(F, yN, a, 27 * D2R) })) }
  // the radome's seam (D‑278): a thin line round the nose cone, ahead of the windscreen
  { const P = []; for (let d = 8; d <= 172; d += 8) P.push(fusP(F, yN, .40 * F.nl - .05 * F.nl * Math.abs(Math.cos(d * D2R)), d * D2R).map((v, i) => i === 2 ? v + .015 : v)); decor.push({ line: 1, P, c: 'rgba(40,52,64,.24)', w: .03 }) }
  // the passenger windows (both sides, just above the widest line) and the doors (outlines)
  if (t.cargo) { const a = (t.cargoAt || .16) * L, P = []; for (const d of [8, 40, 62]) P.push(fusP(F, yN, a - 1.8, d * D2R)); for (const d of [62, 40, 8]) P.push(fusP(F, yN, a + 1.8, d * D2R)); decor.push({ line: 1, P: P.concat([P[0]]), c: 'rgba(28,38,50,.65)', w: .08 }) }   // p390: the cargo door
  if (t.win) { const [w0, w1, n, skip] = t.win, ww = Math.min(.3, (w1 - w0) * L / n * .5);
    for (let i = 0; i < n; i++) { const u = w0 + (w1 - w0) * i / (n - 1); if (skip.some(([p, q]) => u > p && u < q)) continue; const a = u * L;
      for (const [d0, d1] of [[17, 26], [154, 163]]) decor.push(face([fusP(F, yN, a - ww / 2, d0 * D2R), fusP(F, yN, a + ww / 2, d0 * D2R), fusP(F, yN, a + ww / 2, d1 * D2R), fusP(F, yN, a - ww / 2, d1 * D2R)], '#22384e', 'glass', { n: fusN(F, yN, a, (d0 + d1) / 2 * D2R) })) } }
  // the owner 14:46 (1): the upper deck's windows (the 747) — a row on both sides along the hump, the passenger windows' size and pitch,
  // from a little aft of the cockpit's side windows to before the hump falls; each on the hump's side wall, its centre 1.1 m under the
  // hump's top (the upper cabin), found on the section of its station — the model's own surface (D‑281)
  if (t.hump && t.win && BD) { const [w0, w1, n] = t.win, pitch = (w1 - w0) * L / (n - 1), ww = Math.min(.3, pitch * .5), hh = .47;
    let aE = BD.cab.PB[2][0]; while (aE < L * .5 && F(aE).hump < .97 * t.hump) aE += .05; while (aE < L * .5 && F(aE).hump >= .97 * t.hump) aE += .05;   // where the hump begins to fall
    const a0 = BD.cab.PB[2][0] + 1.0, a1 = aE - .7, nU = Math.max(0, Math.floor((a1 - a0) / pitch) + 1);
    const thAt = (a, z) => { let lo = 0, hi = Math.PI / 2; for (let k = 0; k < 30; k++) { const m = (lo + hi) / 2; if (fusP(F, yN, a, m)[2] < z) lo = m; else hi = m } return (lo + hi) / 2 };
    for (let i = 0; i < nU; i++) { const a = a0 + i * pitch, zt = topAt(a), tc = thAt(a, zt - 1.1), d = Math.hypot(...sub(fusP(F, yN, a, tc + .01), fusP(F, yN, a, tc))) / .01, dt = hh / 2 / Math.max(.2, d);
      for (const sd of [1, -1]) { const th = v => sd > 0 ? v : Math.PI - v, Q = [fusP(F, yN, a - ww / 2, th(tc - dt)), fusP(F, yN, a + ww / 2, th(tc - dt)), fusP(F, yN, a + ww / 2, th(tc + dt)), fusP(F, yN, a - ww / 2, th(tc + dt))];
        const nn = fusN(F, yN, a, th(tc)); let PP = Q.map(p => p.map((v, k) => v + nn[k] * .01)); if (dot(faceN(PP), nn) < 0) PP = PP.reverse();
        decor.push(face(PP, '#22384e', 'glass', { n: nn, noSeam: 1 })) } } }
  for (const [di, u] of (t.doors || []).entries()) { const a = u * L; for (const sd of [1, -1]) { if (di === 0 && sd > 0) continue; const P = [], th = d => (sd > 0 ? d : 180 - d) * D2R;
    for (const d of [3, 12, 22, 33]) P.push(fusP(F, yN, a - .55, th(d))); for (const d of [33, 22, 12, 3]) P.push(fusP(F, yN, a + .55, th(d)));
    decor.push({ line: 1, P, c: 'rgba(28,38,50,.7)', w: .07 }) } }
  // the titles on the crown and the model behind the cockpit (the game's mkBody), the airline's mark on the tail section
  const dark = lum(lv.b) < .45, nameCol = Math.abs(lum(lv.s) - lum(lv.b)) > .3 ? lv.s : Math.abs(lum(lv.t) - lum(lv.b)) > .3 ? lv.t : (dark ? '#f4f6f8' : '#1d2730');
  const aT = .37 * L, zT = topAt(aT);
  decor.push({ text: lv.n, at: [0, yN - aT, zT], size: R * .82, maxW: .34 * L, col: nameCol, halo: dark ? 'rgba(0,0,0,.35)' : 'rgba(255,255,255,.55)' });
  decor.push({ text: t.model, at: [-R * .55, yN - F.nl * 1.9, topAt(F.nl * 1.9) - .3], size: R * .3, maxW: F.nl * 1.4, col: dark ? '#f4f6f8' : '#1d2730', light: 1 });
  decor.push({ mark: lv.k, at: [0, yN - (L - 1.35 * t.tl * L + .5 * t.tl * L), topAt(L - .8 * t.tl * L)], size: R * .75, col: lv.m });
  // the tri-jet's third engine at the fin root (the game: fan(-L*.35, 0, L*.17, hw*1.05))
  const extra = [];
  let finZ0 = topAt(.8 * L) - .25;
  if (t.tailEng) {
    const ec = ofU(-.35), n = .17 * L, r = t.fw * .26, z0 = topAt(.85 * L) + r * .55;
    const rings = [[ec + n / 2, r * .9], [ec + n / 2 - .25, r], [ec + n * .1, r * 1.04], [ec - n * .3, r * .95], [ec - n / 2, r * .7]];
    extra.push(...buildRevolve(0, z0, rings, lv.eng || lv.t, 'metal', 40));
    extra.push(disc(0, ec + n / 2 + .02, z0, r * .9, '#c9ced3', 'metal'), disc(0, ec + n / 2 + .04, z0, r * .74, '#16191c', 'matte'), disc(0, ec + n / 2 + .3, z0, r * .17, '#6f7880', 'metal'));
    finZ0 = z0 + r * .7;
  }
  // the fin (from u −.30 to −.50, the class height, swept ~35°); fin thickness × opt.finThick (the readability option)
  if (!t.boom) { const ttail = t.ttail, y0 = ofU(-.30), y1 = ofU(-.50), c0 = y0 - y1, span = t.H - finZ0, swp = Math.tan((ttail ? 30 : 36) * D2R), ct = c0 * (ttail ? .62 : .42), th = (opt.finThick || 1) * .115;
    const st = [0, .5, 1].map(f => { const z = finZ0 + span * f, yLE = y0 - span * f * swp, c = lerp(c0, ct, f); return { z, yLE, yTE: yLE - c, t: c * th } });
    extra.push(...buildFin(st, lv.t));
    const T = st[2]; decor.push({ line: 1, P: [[0, lerp(st[0].yLE, st[0].yTE, .68), st[0].z + .3], [0, lerp(T.yLE, T.yTE, .68), T.z - .1]], c: 'rgba(0,0,0,.3)', w: .08, late: 1 });
    // the T-tail (the turboprop): the tailplane on top of the fin
    if (ttail) { const zt = t.H - .15, rc = .07 * L, tcc = .04 * L, sw = .05 * L, hs = HS * t.hs, yl = T.yLE + .4;
      for (const sd of [1, -1]) extra.push(...buildPlate([{ x: sd * .1, yLE: yl, yTE: yl - rc, z: zt, t: .16 }, { x: sd * hs, yLE: yl - sw, yTE: yl - sw - tcc, z: zt + .1, t: .08 }], lv.t)) }
  }
  // the high wing's centre box (over the fuselage) belongs to the body
  let wingSt = null;
  const yRLE = ofU(t.wingU != null ? t.wingU : .06), yRTE = yRLE - t.wc, yTLE = yRLE - t.sw, yTTE = yTLE - t.tc, yr = .41 * t.fw;
  const wingLE = x => lerp(yRLE, yTLE, (x - yr) / (HS - yr)), wingTE = x => x <= yr + (HS - yr) * t.kink ? yRTE : lerp(yRTE, yTTE, ((x - yr) / (HS - yr) - t.kink) / (1 - t.kink));
  const wingZ = x => (t.high ? t.zb + t.fw + .25 : t.wz) + Math.max(0, x - R) * Math.tan(t.dih * D2R);
  const wingT = x => lerp(t.wt[0], t.wt[1], cl((x - R) / (HS - R), 0, 1));
  const wingCol = lv.w === 'allover' ? sh(lv.b, -.04) : '#dfe3e7';
  // (the small types: drawn after the cabin's windows — the wing lies on the roof, over the windows' upper edge)
  if (t.high) { const s0 = { x: -R, yLE: wingLE(R), yTE: wingTE(R), z: wingZ(R), t: wingT(R) }, s1 = Object.assign({}, s0, { x: R }), B = buildPlate([s0, s1], wingCol);
    if (NOSE[id] && NOSE[id].cab && t.L < 20) decor.push(...B.map(f => Object.assign(f, { late: 1 }))); else extra.push(...B) }
  piece('body', body.concat(extra), { decor });
  // ---- the wings (each side a piece), with the trailing-edge kink, the dihedral and the winglet ----
  for (const sd of [1, -1]) {
    const xs = (t.high ? [R, R + (HS - R) * .5, HS] : [R * .72, yr + (HS - yr) * t.kink, HS]).map(x => Math.max(x, 0));
    const st = xs.map(x => ({ x: sd * x, yLE: wingLE(x), yTE: wingTE(x), z: wingZ(x), t: wingT(x) }));
    const f = buildPlate(st, wingCol), dec = [];
    // the flaps, the aileron, the slats (lines on the upper surface)
    const onTop = (x, c) => { const y = lerp(wingLE(x), wingTE(x), c), i = c < .3 ? 2 : c < .55 ? 3 : c < .8 ? 4 : 5; return [sd * x, y, wingZ(x) + TOP[i] * wingT(x) + .02] };
    const xa = xs[0] + .3, xk = xs[1], xt = HS - .4;
    dec.push({ line: 1, P: [onTop(xa, .74), onTop(xk, .72), onTop(xt, .7)], c: 'rgba(30,40,50,.38)', w: .06 });
    for (const x of [xa + (xk - xa) * .5, xk, xk + (xt - xk) * .45, xk + (xt - xk) * .72]) dec.push({ line: 1, P: [onTop(x, .72), onTop(x, .98)], c: 'rgba(30,40,50,.3)', w: .05 });
    if (!t.high) dec.push({ line: 1, P: [onTop(xa + 1, .12), onTop(xt - .5, .12)], c: 'rgba(30,40,50,.26)', w: .05, dash: [.9, .6] });
    if (t.winglet) { const xT = HS, yl = wingLE(HS) - t.tc * .1, zt = wingZ(HS), h = t.winglet, cant = Math.tan(14 * D2R), c0 = t.tc * .85, c1 = t.tc * .38, swp = h * .7;
      const P0 = [sd * xT, yl, zt], P1 = [sd * (xT + h * cant), yl - swp, zt + h], P2 = [sd * (xT + h * cant), yl - swp - c1, zt + h], P3 = [sd * xT, yl - c0, zt];
      const off = v => [v[0] - sd * .07, v[1], v[2]], off2 = v => [v[0] + sd * .07, v[1], v[2]];
      f.push(orient(face([P0, P1, P2, P3].map(off), lv.t, 'paint'), [-sd, 0, .25]), orient(face([P0, P1, P2, P3].map(off2), sh(lv.t, -.1), 'paint'), [sd, 0, -.25]));
      f.push(orient(face([off(P0), off2(P0), off2(P1), off(P1)], sh(lv.t, .1), 'paint'), [0, 1, .3])) }
    if (t.strut) { const xs2 = HS * .52; dec.push({ line: 1, P: [[sd * R * .95, wingLE(R) - t.wc * .5, t.zb + .35], [sd * xs2, lerp(wingLE(xs2), wingTE(xs2), .3), wingZ(xs2) - wingT(xs2) * .4]], c: '#8a9198', w: .07 }) }   // p390
    wingSt = st;
    piece('wing', f, { decor: dec, side: sd });
  }
  // ---- the engines: turbofans under the wing (pylons), or turboprop nacelles with the propeller ----
  if (t.eng) for (const f0 of t.eng) for (const sd of [1, -1]) {
    const x = f0 * HS, n = t.fw * t.elen, r = t.ed / 2, yc = (x0 - t.sw * f0 + t.fw * .45) + yC, zw = wingZ(x) - wingT(x) * .3, z0 = zw - r * .62;
    const rings = [[yc + n / 2, r * .86, '#d4d8dc'], [yc + n / 2 - .12, r * .97], [yc + n / 2 - .45, r], [yc + n * .05, r * .99], [yc - n * .32, r * .88], [yc - n * .44, r * .74, '#8a9198'], [yc - n / 2, r * .66, '#8a9198']];
    const fc = buildRevolve(sd * x, z0, rings, lv.eng || sh(lv.b, -.03), 'metal', NRV);
    // the pylon (a thin wall to the wing) and the core cone behind
    fc.unshift(...boxFaces([[sd * x - .18, yc + n * .1], [sd * x + .18, yc + n * .1], [sd * x + .18, yc - n * .75], [sd * x - .18, yc - n * .75]], z0 + r * .6, zw + .05, { top: sh(lv.eng || lv.b, -.15), side: sh(lv.eng || lv.b, -.2) }, { mat: 'paint' }));
    fc.unshift(...buildRevolve(sd * x, z0, [[yc - n / 2 + .05, r * .5, '#5c636a'], [yc - n / 2 - n * .2, r * .12]], '#5c636a', 'metal', 24));
    fc.push(disc(sd * x, yc + n / 2 + .01, z0, r * .86, '#c9ced3', 'metal'), disc(sd * x, yc + n / 2 + .03, z0, r * .72, '#16191c', 'matte'), disc(sd * x, yc + n / 2 + .25, z0, r * .16, '#7a838b', 'metal', { spin: 1 }));
    piece('engine', fc, { side: sd });
  }
  if (t.prop) for (const f0 of t.prop) for (const sd of [1, -1]) {
    const x = f0 * HS, zw = wingZ(x), r = t.pn || .62, z0 = zw - (t.pn ? t.pn * .4 : .3), sc = (t.pn || .62) / .62, yF = t.pusher ? wingLE(x) + .3 * sc : wingLE(x) + 2.3 * sc, yB = t.pusher ? wingTE(x) - 1.4 * sc : wingTE(x) - 1.6 * sc;
    const rings = [[yF, r * .55], [yF - .4, r * .9], [yF - 1.2, r], [yB + 1.2, r * .95], [yB, r * .45]];
    const fc = buildRevolve(sd * x, z0, rings, lv.b, 'paint', 32);
    // the propeller: six blades in the disc (parked), the spinner
    const pr = t.pr || 1.96, yP = t.pusher ? yB - .3 * sc : yF + .35 * sc, dn = t.pusher ? -1 : 1;
    for (let i = 0; i < 6; i++) { const a = (i / 6) * TAU + .3, b = a + .1, c0 = .3;
      fc.push(face([[sd * x + c0 * Math.cos(a - .25), yP, z0 + c0 * Math.sin(a - .25)], [sd * x + pr * Math.cos(a), yP, z0 + pr * Math.sin(a)], [sd * x + pr * Math.cos(b), yP, z0 + pr * Math.sin(b)], [sd * x + c0 * Math.cos(b + .25), yP, z0 + c0 * Math.sin(b + .25)]], '#2a2e33', 'metal', { n: [0, 1, 0], both: true })) }
    fc.push(...buildRevolve(sd * x, z0, [[yP + dn * .7 * sc, .02], [yP + dn * .45 * sc, .2 * sc], [yP, .32 * sc]], lv.b, 'paint', 20));
    piece('engine', fc, { side: sd });
  }
  // ---- p390 · the odd ones: rear-mounted jets, the nose propeller, the tandem push-pull pair, the canard, wing floats, the strut, the
  // twin booms (their fins and the tailplane between them) ----
  const zcB = t.zb + R;
  if (t.reng) for (const sd of [1, -1]) { const e = t.reng, r = e.ed / 2, n = e.elen, yc = yN - e.at * L, x = sd * (R + r + .18), z0 = zcB + .25 * R;
    const fc = buildRevolve(x, z0, [[yc + n / 2, r * .86, '#d4d8dc'], [yc + n / 2 - .12, r * .98], [yc + n * .1, r], [yc - n * .3, r * .9], [yc - n / 2, r * .7, '#8a9198']], lv.eng || sh(lv.b, -.03), 'metal', NRV);
    fc.unshift(...boxFaces([[sd * R * .7, yc + .3], [x, yc + .3], [x, yc - .6], [sd * R * .7, yc - .6]], z0 - .12, z0 + .12, { top: sh(lv.b, -.08), side: sh(lv.b, -.16) }, { mat: 'paint' }));
    fc.push(disc(x, yc + n / 2 + .01, z0, r * .86, '#c9ced3', 'metal'), disc(x, yc + n / 2 + .03, z0, r * .7, '#16191c', 'matte'));
    piece('engine', fc, { side: sd }) }
  if (t.nprop) { const r0 = F(0.02), z0 = r0.zm, yP = yN + .12, pr = t.nprop.r, fc = [];
    fc.push(...buildRevolve(0, z0, [[yP + .42, .02], [yP + .22, .15], [yP, .22]], '#d8dce0', 'metal', 20));
    for (const a of [.4, .4 + Math.PI]) fc.push(face([[.06 * Math.cos(a - 1.4), yP + .05, z0 + .06 * Math.sin(a - 1.4)], [pr * Math.cos(a), yP + .05, z0 + pr * Math.sin(a)], [pr * Math.cos(a + .12), yP + .05, z0 + pr * Math.sin(a + .12)], [.06 * Math.cos(a + 1.6), yP + .05, z0 + .06 * Math.sin(a + 1.6)]], '#2a2e33', 'metal', { n: [0, 1, 0], both: true }));
    extra.push(...fc) }
  if (t.tandem) { const yl = wingLE(R), yt = wingTE(R), zw = wingZ(0) + wingT(0) * .5, z0 = zw + 1.0, r = .42, pr = t.tandem.r, yF = yl + .9, yB = yt - .9, fc = [];
    fc.push(...boxFaces([[-.12, yl - .4], [.12, yl - .4], [.12, yt + .4], [-.12, yt + .4]], zw, z0 - r * .6, { top: sh(lv.b, -.1), side: sh(lv.b, -.2) }, { mat: 'paint' }));
    fc.push(...buildRevolve(0, z0, [[yF, r * .5], [yF - .3, r * .9], [(yF + yB) / 2, r], [yB + .3, r * .9], [yB, r * .5]], lv.b, 'paint', 24));
    for (const [yP, dn] of [[yF + .1, 1], [yB - .1, -1]]) { for (const a of [0, 2.09, 4.19]) fc.push(face([[.05 * Math.cos(a - 1.4), yP, z0 + .05 * Math.sin(a - 1.4)], [pr * Math.cos(a), yP, z0 + pr * Math.sin(a)], [pr * Math.cos(a + .12), yP, z0 + pr * Math.sin(a + .12)], [.05 * Math.cos(a + 1.6), yP, z0 + .05 * Math.sin(a + 1.6)]], '#2a2e33', 'metal', { n: [0, dn, 0], both: true }));
      fc.push(...buildRevolve(0, z0, [[yP + dn * .4, .02], [yP + dn * .2, .14], [yP, .2]], lv.b, 'paint', 16)) }
    piece('engine', fc, { side: 0 }) }
  if (t.cpush) { const c = t.cpush, yP = yN - c.at * L, z0 = F.zc + c.z, pr = c.r, fc = [];
    fc.push(...buildRevolve(0, z0, [[yP + 1.25, .06], [yP + 1.0, .3], [yP + .45, .33], [yP + .12, .2], [yP + .02, .09]], lv.b, 'paint', 20));
    for (const a of [0, 2.09, 4.19]) fc.push(face([[.05 * Math.cos(a - 1.4), yP, z0 + .05 * Math.sin(a - 1.4)], [pr * Math.cos(a), yP, z0 + pr * Math.sin(a)], [pr * Math.cos(a + .1), yP, z0 + pr * Math.sin(a + .1)], [.05 * Math.cos(a + 1.6), yP, z0 + .05 * Math.sin(a + 1.6)]], '#2a2e33', 'metal', { n: [0, -1, 0], both: true }));
    piece('engine', fc, { side: 0 }) }
  if (t.seawing) { const c = t.seawing, yl = yN - c.at * L, z = F.zc + c.z; for (const sd of [1, -1])
    piece('stab', buildPlate([{ x: sd * R * .85, yLE: yl, yTE: yl - c.chord, z, t: .22 }, { x: sd * (R + c.span), yLE: yl - .35, yTE: yl - c.chord * .8, z: z + .12, t: .1 }], lv.w === 'allover' ? sh(lv.b, -.06) : sh(lv.b, -.03)), { side: sd }) }
  if (t.canard) { const c = t.canard, yl = ofU(c.u), z = zcB - .15 * R; for (const sd of [1, -1])
    piece('stab', buildPlate([{ x: sd * R * .8, yLE: yl, yTE: yl - c.chord, z, t: c.chord * .1 }, { x: sd * (R + c.span), yLE: yl - .25, yTE: yl - .25 - c.chord * .6, z: z + .05, t: c.chord * .07 }], lv.w === 'allover' ? sh(lv.b, -.06) : '#e3e6e9'), { side: sd }) }
  if (t.floats) for (const sd of [1, -1]) { const x = sd * HS * .82, zw = wingZ(Math.abs(x)) - wingT(Math.abs(x)) * .3, z0 = zw - .95, yc = (wingLE(Math.abs(x)) + wingTE(Math.abs(x))) / 2;
    const fc = buildRevolve(x, z0, [[yc + .8, .05], [yc + .55, .2], [yc, .24], [yc - .7, .12]], sh(lv.b, -.04), 'paint', 16);
    fc.unshift(...boxFaces([[x - .04, yc + .2], [x + .04, yc + .2], [x + .04, yc - .2], [x - .04, yc - .2]], z0 + .15, zw, { top: '#6c737a', side: '#5a6067' }, { mat: 'metal' }));
    piece('engine', fc, { side: sd }) }
  if (t.boom) { const xb = t.boom.x * HS, yW = wingTE(xb), yT = yN - L, r0 = .32, z0 = wingZ(xb) - .25, hs = xb + .6;
    for (const sd of [1, -1]) { const fc = buildRevolve(sd * xb, z0, [[yW + 1.2, r0 * .9], [yW, r0], [yT + 2.2, r0 * .75], [yT, r0 * .5]], lv.b, 'paint', 16);
      const y0 = yT + 2.2, y1 = yT + .2, st = [0, 1].map(f => { const z = z0 + r0 + (t.H - z0 - r0) * f, yLE = y0 - f * 1.0, c = lerp(y0 - y1, (y0 - y1) * .6, f); return { z, yLE, yTE: yLE - c, t: c * .12 } });
      fc.push(...buildFin(st, lv.t).map(f => Object.assign(f, { P: f.P.map(q => [q[0] + sd * xb, q[1], q[2]]) })));
      piece('body2', fc, { side: sd }) }
    const zt = t.H - .2, yl = yT + 1.9; piece('stab', buildPlate([{ x: -hs, yLE: yl, yTE: yl - 1.3, z: zt, t: .12 }, { x: hs, yLE: yl, yTE: yl - 1.3, z: zt, t: .12 }], lv.t), { side: 0 }) }
  // ---- the low tailplanes ----
  if (!t.ttail && !t.boom) for (const sd of [1, -1]) {
    const yl = ofU(-.36), rc = .1 * L, tcc = .045 * L, sw = .07 * L, hs = HS * t.hs, a = yN - yl, r = F(a), z = r.zm + r.rv * .15, x0s = Math.max(.2, r.rs * .55);
    const st = [{ x: sd * x0s, yLE: yl, yTE: yl - rc, z, t: rc * .11 }, { x: sd * hs, yLE: yl - sw, yTE: yl - sw - tcc, z: z + (hs - x0s) * Math.tan(6 * D2R), t: tcc * .09 }];
    piece('stab', buildPlate(st, lv.w === 'allover' ? sh(lv.b, -.06) : '#e3e6e9'), { side: sd });
  }
  // ---- the gear: tyres (dark discs seen edge-on), legs, bogies ----
  const tyre = (x, y, r, w) => ({ tyre: 1, x, y, r, w });
  const gearPiece = (list, legs) => piece('gear', [], { tyres: list, legs });
  { const [tr, tw] = t.gear.tire, ymg = yC + x0 - t.wc * .55;
    for (const [gx, nAx] of t.gear.main) for (const sd of [1, -1]) {
      const T = [], X = sd * gx; for (let i = 0; i < nAx; i++) { const y = ymg + (nAx > 1 ? (i - (nAx - 1) / 2) * tr * 2.3 : 0); for (const dx of [-.42, .42]) T.push(tyre(X + dx * (tr * 1.25), y, tr, tw)) }
      const top = t.high ? t.zb + .6 : Math.min(wingZ(gx) - .2, t.zb + 1.4);
      gearPiece(T, [{ x: X, y: ymg, z0: tr * .9, z1: top, r: .17 }]);
    }
    if (t.gear.centre) { const T = [], y0 = ymg - 1.2; for (let i = 0; i < t.gear.centre; i++) for (const dx of [-.5, .5]) T.push(tyre(dx, y0 + (i - .5) * tr * 2.3, tr, tw)); gearPiece(T, [{ x: 0, y: y0, z0: tr, z1: t.zb + .3, r: .16 }]) }
    const nr = tr * .72; gearPiece([tyre(-.32, 0, nr, tw * .9), tyre(.32, 0, nr, tw * .9)], [{ x: 0, y: 0, z0: nr, z1: t.zb + .2, r: .1 }]);
    if (t.gear.sponson) for (const sd of [1, -1]) { const f = boxFaces([[sd * R * .7, ymg + 1.8], [sd * (R + .55), ymg + 1.5], [sd * (R + .55), ymg - 1.9], [sd * R * .7, ymg - 2.2]], t.zb + .1, t.zb + 1.2, { top: sh(lv.b, -.06), side: sh(lv.b, -.12) }, { mat: 'paint' }); piece('body2', f) }
  }
  // the piece's bounding values (local metres): yMax (the south edge), zMin (the lowest point), x range; the sort key comes from them
  for (const p of pieces) bounds(p);
  const info = { id, t, lv, L, R, HS, yN, yC, yTail: yN - L, wingLE, wingTE, wingZ, wingT, finTop: t.H, F, x0, band: BD, bandAt };
  return { pieces, info };
}

// ======================================================================================================================================
// p390 · the helicopters (the game's AC-HL table: L, the rotor's diameter, the main and accent colours, the style k, the blades; HSP:
// the body's length / width as fractions of L, its shape, the glass, skids or wheels, a tail rotor, a ducted fan or a four-blade rotor)
const HELI = {
  // the real types (the owner's photos 15:49–16:15, D‑282): L the fuselage with its boom (m), D the main rotor (m), nb its blades
  'AC-HL-01': { he: 'מסוק קל', L: 9.07, D: 10.06, H: 3.28, tr: 1.47, hub: .33, main: '#d9dce0', acc: '#2a6ab0', k: 0, nb: 2, src: 'Robinson R44: רוטור 10.06 מ׳, אורך כולל 11.66 מ׳, 2 להבים, מגלשיים' },
  'AC-HL-02': { he: 'מסוק משטרה וחילוץ', L: 13.77, D: 13.8, H: 4.98, tr: 2.7, hub: .375, main: '#1c2430', acc: '#e8e8ea', k: 4, nb: 5, src: 'Leonardo AW139: רוטור 13.8 מ׳, אורך כולל 16.66 מ׳, 5 להבים, גלגלים' },
  'AC-HL-03': { he: 'מסוק תובלה', L: 15.6, Lo: 30.14, D: 18.29, H: 5.68, main: '#4a5a3a', acc: '#d8d8d0', k: 6, nb: 3, src: 'Boeing CH-47F Chinook: שני רוטורים של 18.29 מ׳ (3 להבים), גוף 15.6 מ׳ לציור (הבעלים 18:21), 30.14 מ׳ עם הרוטורים למעטפת ולרחבה, גובה 5.68 מ׳ (RSAF CH-47F fact sheet), 4 גלגלים, בלי רוטור זנב' },
  'AC-HL-04': { he: 'מסוק רפואי', L: 13.77, D: 13.8, H: 4.98, tr: 2.7, hub: .375, main: '#f4d21f', acc: '#1f8a4c', k: 4, nb: 5, ems: 1, src: 'Leonardo AW139 (רפואי)' },
  'AC-HL-05': { he: 'מסוק עסקים', L: 13.77, D: 13.8, H: 4.98, tr: 2.7, hub: .375, main: '#1d2b44', acc: '#c9a24a', k: 4, nb: 5, src: 'Leonardo AW139 (עסקים)' },
  'AC-HL-06': { he: 'מסוק תיירות', L: 10.68, D: 10.69, H: 3.34, hub: .326, main: '#f2f4f6', acc: '#e8682b', k: 5, nb: 3, src: 'Airbus H130 (EC130): רוטור 10.69 מ׳, גוף 10.68 מ׳, 3 להבים, Fenestron, תא זכוכית רחב, מגלשיים' },
  // the owner 16:46 (4), D‑149: the fire helicopter — the drawing only (its base at the fire station, the call out and the refills come
  // with the emergency stage): an AW139 in the fire service's red with a white band, a Bambi bucket on its long line — hanging under it
  // in the air, on the ground beside it when it stands
  'AC-HL-07': { he: 'מסוק כיבוי', L: 13.77, D: 13.8, H: 4.98, tr: 2.7, hub: .375, main: '#c8261e', acc: '#f4f4f0', k: 4, nb: 5, fire: 1, src: 'Leonardo AW139 בגרסת כיבוי (D‑149): דלי Bambi ‏(≈2 מ׳ קוטר, 1.6 מ׳ גובה) על כבל; ציור בלבד — ההתנהגות בשלב החירום' }
};
const HSP = [{ bw: .13, b: .36, body: 'tear', glass: 'bubble', gear: 'skid', tail: 'rotor' }, { bw: .15, b: .38, body: 'tear', glass: 'std', gear: 'skid', tail: 'rotor' },
  { bw: .17, b: .46, body: 'box', glass: 'std', gear: 'wheels', tail: 'rotor' }, { bw: .16, b: .40, body: 'round', glass: 'std', gear: 'skid', tail: 'fen' },
  { bw: .16, b: .52, body: 'sleek', glass: 'wide', gear: 'wheels', tail: 'rotor4', boom: [[.62, .8], [.42, .55], [.28, .36], [.22, .3]] }, { bw: .19, b: .42, body: 'round', glass: 'pano', gear: 'skid', tail: 'fen', hzk: .5, front: 'blunt', boom: [[.5, .62], [.34, .44], [.24, .32], [.2, .27]] },
  { bw: .24, b: 1, body: 'tandem', glass: 'std', gear: 'wheels4', tail: 'none' }];   // 4 AW139 · 5 H130 · 6 CH-47
// a body of revolution with elliptic sections: rings [y, rx, rz, colour?] round the axis (x0, ·, z0)
function revolveE(x0, z0, rings, col, mat, N) {
  const faces = []; N = N || 24;
  for (let k = 0; k < N; k++) { const t0 = k * TAU / N, t1 = t0 + TAU / N;
    for (let i = 0; i + 1 < rings.length; i++) { const [ya, xa, za, ca] = rings[i], [yb, xb, zb] = rings[i + 1];
      const P = [[x0 + xa * Math.cos(t0), ya, z0 + za * Math.sin(t0)], [x0 + xa * Math.cos(t1), ya, z0 + za * Math.sin(t1)], [x0 + xb * Math.cos(t1), yb, z0 + zb * Math.sin(t1)], [x0 + xb * Math.cos(t0), yb, z0 + zb * Math.sin(t0)]];
      const nn = th => nrm([Math.cos(th) / Math.max(.05, (xa + xb) / 2), -((xb - xa) / ((yb - ya) || 1e-6)) * 0, Math.sin(th) / Math.max(.05, (za + zb) / 2)]);
      faces.push(face(P, ca || col, mat, { g: [nn(t0), nn(t1)] })) } }
  return faces;
}
// heli(id, { spin }) → { pieces, info } — local metres, the origin at the mast's foot on the ground, the nose to the south (+y)
// the tandem-rotor transport (CH-47F): a long rounded box, the fuel pods along its lower sides, the low front pylon over the cockpit and
// the tall rear one with the two engines beside it, two rotors of 3 blades that overlap, four wheels, a blunt end with the ramp
function buildTandem(id, T, opt) {
  const L = T.L, pieces = [], piece = (kind, faces, extra) => { const p = Object.assign({ kind, faces, decor: [] }, extra || {}); pieces.push(p); return p };
  const zs = .55, hw = 1.3, hz = 1.35, zc = zs + hz, nx = L / 2, y1 = -L / 2, N = opt.lod ? 20 : 28, decor = [];
  const body = revolveE(0, zc, [[nx, .25, .3], [nx - .45, .95, 1.0], [nx - 1.5, 1.24, 1.3], [nx - 3, hw, hz], [y1 + 1.6, hw, hz], [y1 + .35, hw * .96, hz * .9], [y1, hw * .9, hz * .78]], T.main, 'paint', N);
  for (const sd of [1, -1]) body.push(...revolveE(sd * (hw + .18), zs + .55, [[nx - 4.2, .08, .1], [nx - 4.8, .32, .42], [y1 + 3.2, .34, .44], [y1 + 2.4, .1, .12]], sh(T.main, -.05), 'paint', 14));
  // the pylons: low in front, tall behind (its fin-like fairing), the engines either side of it
  body.push(...revolveE(0, zc + hz * .82, [[nx - 1.2, .1, .1], [nx - 1.7, .55, .45], [nx - 2.6, .5, .42], [nx - 3.4, .1, .1]], T.main, 'paint', 14));
  body.push(...buildFin([{ z: zc + hz * .6, yLE: y1 + 4.4, yTE: y1 + .2, t: 1.4 }, { z: zc + hz + 1.75, yLE: y1 + 2.4, yTE: y1 + .7, t: .8 }], T.main));
  for (const sd of [1, -1]) body.push(...revolveE(sd * 1.05, zc + hz + .35, [[y1 + 4.6, .1, .1], [y1 + 4.3, .38, .38], [y1 + 2.3, .4, .4], [y1 + 1.9, .22, .22]], sh(T.main, -.08), 'metal', 14));
  // the cockpit's glass: the windscreen and the side windows on the nose
  for (const sd of [1, -1]) { const P = [[sd * .1, nx - .55, zc + .55], [sd * .95, nx - 1.0, zc + .45], [sd * 1.2, nx - 1.75, zc + .4], [sd * 1.2, nx - 1.75, zc - .15], [sd * .95, nx - .95, zc - .1], [sd * .1, nx - .45, zc - .05]];
    decor.push(face(sd > 0 ? P : P.slice().reverse(), '#1d3346', 'glass', { n: [sd * .6, .5, .6], grad: ['#1a2c3d', '#57748c', '#c4d9e8'] })) }
  piece('body', body, { decor });
  { const r = .45, T4 = []; for (const y of [nx - 3.2, y1 + 3.6]) for (const sd of [1, -1]) T4.push({ tyre: 1, x: sd * 1.45, y, r, w: .3 }); piece('gear', [], { tyres: T4, legs: [] }) }
  // the rotors: the front hub over the cockpit, the rear one high on its pylon; parked blades or the discs
  const f = [], R2 = T.D / 2;
  for (const [yH, zt, a0] of [[nx - 2.2, zc + hz + .9, .3], [y1 + 1.6, zc + hz + 2.25, .9]]) {
    f.push(...vcyl(0, yH, .14, zt - .6, zt, '#3a3f45', 'metal', 10), ...vcyl(0, yH, .38, zt - .05, zt + .14, '#2a2e33', 'metal', 14));
    if (opt.spin) { const P = []; for (let i = 0; i < 36; i++) { const a = i / 36 * TAU; P.push([R2 * Math.cos(a), yH + R2 * Math.sin(a), zt + .06]) } f.push(face(P, '#d2dceb', 'glass', { n: [0, 0, 1], a: .18, ns: 1 })) }
    else for (let i = 0; i < 3; i++) { const a = a0 + i * TAU / 3, c = Math.cos(a), sn = Math.sin(a), w = .3; f.push(face([[-sn * w, yH + c * w, zt + .06], [R2 * c - sn * w, yH + R2 * sn + c * w, zt + .02], [R2 * c + sn * w, yH + R2 * sn - c * w, zt + .02], [sn * w, yH - c * w, zt + .06]], '#2c3036', 'metal', { n: [0, 0, 1], both: true })) } }
  piece('rotor', f);
  for (const p of pieces) bounds(p);
  return { pieces, info: { id, heli: true, t: Object.assign({ he: T.he, H: zc + hz + 2.4, zb: zs, fw: 2 * hw }, T), L, R: hw, yN: nx, HS: T.D / 2 + 6 } };
}
function buildHeli(id, opt) {
  opt = opt || {}; const T = HELI[id]; if (!T) throw new Error('A34: unknown helicopter ' + id);
  if ((HSP[T.k] || {}).body === 'tandem') return buildTandem(id, T, opt);
  const H = HSP[T.k] || HSP[0], L = T.L, b = L * H.b, bw = L * H.bw, hw = bw / 2, hz = bw * (H.hzk || .62), nx = H.body === 'sleek' ? b * .74 : b * .62, zs = H.gear === 'wheels' ? .7 : .55, zc = zs + hz;
  const yH = T.hub != null ? nx - T.hub * L : .05 * b;   // the rotor's hub: T.hub × L behind the nose (from the real overall length)
  const pieces = [], piece = (kind, faces, extra) => { const p = Object.assign({ kind, faces, decor: [] }, extra || {}); pieces.push(p); return p };
  const fb = H.body === 'box' ? [1, 1] : H.body === 'round' ? [1.06, 1] : [1, 1];
  // D‑281/D‑282 (the coordinator 18:2x): the H130's cabin is broad and glazed to the front (a blunt nose), the others come to a point
  const rings = H.front === 'blunt' ? [[nx, .36 * hw, .42 * hz], [nx - .04 * b, .8 * hw, .82 * hz], [nx - .15 * b, .97 * hw * fb[0], .98 * hz], [.05 * b, hw * fb[0], hz], [-.25 * b, .92 * hw, .9 * hz], [-.45 * b, .48 * hw, .58 * hz]]
    : [[nx, .06 * hw, .06 * hz], [nx - .07 * b, .5 * hw, .55 * hz], [nx - .22 * b, .88 * hw * fb[0], .93 * hz], [.05 * b, hw * fb[0], hz], [-.25 * b, .9 * hw, .88 * hz], [-.45 * b, .42 * hw, .5 * hz]];
  if (H.body === 'box') rings.splice(1, 1, [nx - .05 * b, .7 * hw, .7 * hz]);
  const body = revolveE(0, zc, rings, T.main, 'paint', opt.lod ? 20 : 28), decor = [];
  // the boom (its stripe in the accent), the fin with the tail rotor or the ducted fan, the tailplane
  const yB0 = -.3 * b, yB1 = nx - L, zb = zc + .25 * hz;   // the owner 16:46 (1): nose to tail = the real fuselage length L
  body.push(...revolveE(0, zb, (BM => [[yB0, BM[0][0] * hw, BM[0][1] * hw], [yB0 + (yB1 - yB0) * .45, BM[1][0] * hw, BM[1][1] * hw], [yB1 + .4, BM[2][0] * hw, BM[2][1] * hw], [yB1, BM[3][0] * hw, BM[3][1] * hw]])(H.boom || [[.42, .42], [.24, .24], [.14, .14], [.1, .1]]), T.main, 'paint', 12));
  const fin = [{ z: zb, yLE: yB1 + 1.1, yTE: yB1 - .1, t: .12 }, { z: zb + hz * 1.3, yLE: yB1 + .35, yTE: yB1 - .35, t: .08 }];
  body.push(...buildFin(fin.map(q => ({ z: q.z, yLE: q.yLE, yTE: q.yTE, t: H.tail === 'fen' ? .35 : q.t })), T.acc));
  const yS = yB1 + 1.4, sp = hw * 1.45; body.push(...buildPlate([{ x: -sp, yLE: yS, yTE: yS - .5, z: zb, t: .06 }, { x: sp, yLE: yS, yTE: yS - .5, z: zb, t: .06 }], T.acc));
  if (H.tail === 'fen') body.push(disc(-.19, yB1 + .3, zb + hz * .45, .32, '#1b1f24', 'matte', { n: [-1, 0, 0], both: true }));
  else { const tr = T.tr ? T.tr / 2 : L * .075, tx = -.18, tz = zb + hz * .5, n = H.tail === 'rotor4' ? 4 : 2;
    if (opt.spin) { const P = []; for (let i = 0; i < 20; i++) { const a = i / 20 * TAU; P.push([tx, yB1 + .2 + tr * Math.cos(a), tz + tr * Math.sin(a)]) } body.push(face(P, '#cfd8e2', 'glass', { n: [-1, 0, 0], both: true, a: .25, ns: 1 })) }
    else for (let i = 0; i < n; i++) { const a = .5 + i * TAU / n; body.push(face([[tx, yB1 + .2, tz], [tx, yB1 + .2 + tr * Math.cos(a), tz + tr * Math.sin(a)], [tx, yB1 + .2 + tr * Math.cos(a + .14), tz + tr * Math.sin(a + .14)]], '#22262b', 'metal', { n: [-1, 0, 0], both: true })) } }
  // the glass: the canopy over the front, a streak of sky
  { const gl = H.glass, y0 = nx - .02 * b, y1 = nx - (gl === 'bubble' ? .42 : gl === 'pano' ? .52 : .3) * b, th0 = gl === 'bubble' ? -25 : gl === 'pano' ? -38 : 5;
    const ell = (y, th) => { const u = (y - rings[0][0]) / (rings[rings.length - 1][0] - rings[0][0]); let i = 0; while (i + 1 < rings.length - 1 && y < rings[i + 1][0]) i++;
      const A = rings[i], B = rings[i + 1], f = (y - A[0]) / ((B[0] - A[0]) || 1e-6), rx = lerp(A[1], B[1], f), rz = lerp(A[2], B[2], f); void u; return [rx * Math.cos(th) * 1.01, y, zc + rz * Math.sin(th) * 1.01] };
    for (const [d0, d1] of [[th0, 88], [92, 180 - th0]]) { const P = []; for (let i = 0; i <= 6; i++) P.push(ell(lerp(y0, y1, i / 6), d0 * D2R)); for (let i = 6; i >= 0; i--) P.push(ell(lerp(y0, y1, i / 6), d1 * D2R));
      decor.push(face(P, '#1d3346', 'glass', { n: [0, .4, .9], grad: ['#1a2c3d', '#7fa3c1'] })) }
    // the cabin's side windows (the coordinator 18:2x, D‑282: as the real one): the AW139's five large ones a side, the H130's two panoramic
    if (gl === 'wide' || gl === 'pano') { const nW = gl === 'wide' ? 5 : 2, ya = y1 - .03 * b, yb = gl === 'wide' ? -.3 * b : -.34 * b, st = (ya - yb) / nW, t0 = (gl === 'wide' ? 8 : 0) * D2R, t1 = (gl === 'wide' ? 42 : 64) * D2R;
      for (let i = 0; i < nW; i++) { const a0 = ya - i * st - st * .1, a1 = ya - (i + 1) * st + st * .1;
        for (const sd of [1, -1]) { const th = t => sd > 0 ? t : Math.PI - t, P = [ell(a0, th(t0)), ell(a1, th(t0)), ell(a1, th(t1)), ell(a0, th(t1))];
          decor.push(face(P, '#22384e', 'glass', { n: [sd, 0, .35], grad: ['#1a2c3d', '#6f93b1'] })) } } } }
  // the role markings: the EMS checker band, the corporate pin stripe, a light band along the top
  if (T.ems) for (let i = 0; i < 8; i++) { const y = .3 * b - i * .1 * b; for (const sd of [1, -1]) { const P = [[sd * hw * .97, y, zc - .1 * hz], [sd * hw * .97, y - .1 * b, zc - .1 * hz], [sd * hw * .97, y - .1 * b, zc + .2 * hz], [sd * hw * .97, y, zc + .2 * hz]]; if (i % 2) decor.push(face(P, T.acc, 'paint', { n: [sd, 0, 0] })) } }
  else decor.push({ line: 1, P: [[hw * .98, .35 * b, zc + .05 * hz], [hw * .98, -.42 * b, zc + .05 * hz]], c: T.acc, w: .12 }, { line: 1, P: [[-hw * .98, .35 * b, zc + .05 * hz], [-hw * .98, -.42 * b, zc + .05 * hz]], c: T.acc, w: .12 });
  if (T.fire) for (const sd of [1, -1]) decor.push(face([[sd * hw * .975, .38 * b, zc - .42 * hz], [sd * hw * .975, -.45 * b, zc - .42 * hz], [sd * hw * .975, -.45 * b, zc - .08 * hz], [sd * hw * .975, .38 * b, zc - .08 * hz]], T.acc, 'paint', { n: [sd, 0, 0] }));   // D‑149: the fire service's white band
  piece('body', body, { decor });
  // the gear: skids with their cross tubes, or wheels
  if (H.gear === 'skid') { const f = [], xs = bw * .68;
    for (const sd of [1, -1]) { f.push(...boxFaces([[sd * xs - .05, .5 * b], [sd * xs + .05, .5 * b], [sd * xs + .05, -.42 * b], [sd * xs - .05, -.42 * b]], 0, .1, { top: '#2a2e33', side: '#1b1e22' }, { mat: 'metal' }));
      for (const y of [.3 * b, -.2 * b]) f.push(...boxFaces([[sd * xs - .04, y - .04], [sd * hw * .5 + .04 * sd, y - .04], [sd * hw * .5 + .04 * sd, y + .04], [sd * xs - .04, y + .04]], .1, zs + .1, { top: '#3a3f45', side: '#2a2e33' }, { mat: 'metal' })) }
    piece('gear', f) }
  else { const r = .32; piece('gear', [], { tyres: [{ tyre: 1, x: -hw * .9, y: -.1 * b, r, w: .22 }, { tyre: 1, x: hw * .9, y: -.1 * b, r, w: .22 }, { tyre: 1, x: 0, y: .45 * b, r: r * .8, w: .18 }], legs: [{ x: 0, y: .45 * b, z0: r * .8, z1: zs, r: .08 }] }) }
  // the main rotor: the mast, the hub, the blades (parked) or the disc (turning) — a piece of its own, high up
  { const zt = T.H ? Math.max(zc + hz + .25, T.H - .12) : zc + hz + .45, R2 = T.D / 2, f = [];
    f.push(...vcyl(0, yH, .12, zc + hz * .8, zt, '#3a3f45', 'metal', 10), ...vcyl(0, yH, .32, zt - .05, zt + .12, '#2a2e33', 'metal', 14));
    if (opt.spin) { const P = []; for (let i = 0; i < 36; i++) { const a = i / 36 * TAU; P.push([R2 * Math.cos(a), yH + R2 * Math.sin(a), zt + .06]) } f.push(face(P, '#d2dceb', 'glass', { n: [0, 0, 1], a: .2, ns: 1 })) }
    else for (let i = 0; i < T.nb; i++) { const a = .6 + i * TAU / T.nb, c = Math.cos(a), sn = Math.sin(a), w = .16; f.push(face([[-sn * w, yH + c * w, zt + .06], [R2 * c - sn * w, yH + R2 * sn + c * w, zt + .02], [R2 * c + sn * w, yH + R2 * sn - c * w, zt + .02], [sn * w, yH - c * w, zt + .06]], '#2c3036', 'metal', { n: [0, 0, 1], both: true })) }
    piece('rotor', f) }
  // D‑149 · the fire bucket (a Bambi bucket: a red-orange drum, a dark rim, open at the top) on its line from the belly hook: in the air
  // 9 m under the hook; standing, on the ground beside the right door with the line laid to it
  if (T.fire) { const f = [], d = [], hook = [0, yH, zs + .15], air = !!opt.spin, bx = air ? 0 : hw + 2.6, by = air ? yH : yH - 1.2, bz = air ? -9 : 0, r0 = .95, r1 = .8, hB = 1.6;
    f.push(...vcyl(bx, by, r1, bz, bz + hB * .45, '#d9441c', 'paint', 16), ...vcyl(bx, by, r0, bz + hB * .45, bz + hB, '#e2531f', 'paint', 16), ...vcyl(bx, by, r0 + .05, bz + hB - .12, bz + hB + .02, '#22201e', 'metal', 16));
    { const P = []; for (let i = 0; i < 16; i++) { const a = i / 16 * TAU; P.push([bx + r0 * Math.cos(a), by + r0 * Math.sin(a), bz + hB]) } f.push(face(P, '#3a1c12', 'matte', { n: [0, 0, 1] })) }
    const top = [bx, by, bz + hB + .9];
    for (const a of [0, 2.1, 4.2]) d.push({ line: 1, P: [[bx + r0 * Math.cos(a), by + r0 * Math.sin(a), bz + hB], top], c: 'rgba(30,30,30,.85)', w: .05 });   // the bucket's own rigging
    d.push({ line: 1, P: air ? [hook, top] : [hook, [hook[0], hook[1], .05], [bx * .5, (hook[1] + by) / 2 + .6, .05], [bx, by - 1.4, .05], top], c: 'rgba(25,25,25,.9)', w: .06 });
    piece('bucket', f, { decor: d }) }
  shiftY(pieces, -yH); for (const p of pieces) bounds(p);   // the hub at the origin: the pose (the pad's centre) under the rotor
  return { pieces, info: { id, heli: true, t: Object.assign({ he: T.he, H: T.H || zc + hz + .6, zb: zs, fw: bw }, T), L, R: hw, yN: nx - yH, HS: T.D / 2 } };
}
function shiftY(pieces, dy) { if (!dy) return; const mv = P => P.map(q => [q[0], q[1] + dy, q[2]]);
  for (const p of pieces) { for (const f of p.faces || []) f.P = mv(f.P); for (const d of p.decor || []) if (d.P) d.P = mv(d.P); for (const r of p.tyres || []) r.y += dy; for (const l of p.legs || []) l.y += dy }
}
function bounds(p) { let yM = -1e9, zm = 1e9, xa = 1e9, xb = -1e9;
  const acc = q => { yM = Math.max(yM, q[1]); zm = Math.min(zm, q[2]); xa = Math.min(xa, q[0]); xb = Math.max(xb, q[0]) };
  for (const f of p.faces || []) for (const q of f.P) acc(q);
  if (p.tyres) for (const r of p.tyres) { acc([r.x - r.w / 2, r.y + r.r, 0]); acc([r.x + r.w / 2, r.y - r.r, 0]) }
  p.yMax = yM; p.zMin = Math.max(0, zm); p.x0 = xa; p.x1 = xb; return p }
// ======================================================================================================================================
// drawing.  M = { X, Y, s } : local metres → world px of the field: (X + x·s, Y + y·s − K·z·s); seam = the stroke width (world px)
function P2(M, p) { return [M.X + p[0] * M.s, M.Y + (p[1] - K * p[2]) * M.s] }
// the owner 14:39 (1): no grid of seams on the skin — a face's outline pushed out by d px (a mitre at each corner) and filled once, so
// that neighbours overlap a little and no background shows between them; no stroke (it drew the grid, and cost a second raster)
function growS(S, d) {
  const n = S.length, E = []; let ar = 0;
  for (let i = 0; i < n; i++) { const p = S[i], q = S[(i + 1) % n]; ar += p[0] * q[1] - q[0] * p[1] }
  const sg = ar >= 0 ? 1 : -1;
  for (let i = 0; i < n; i++) { const p = S[i], q = S[(i + 1) % n], ex = q[0] - p[0], ey = q[1] - p[1], l = Math.hypot(ex, ey); E.push(l > 1e-6 ? [sg * ey / l, -sg * ex / l] : null) }
  for (let i = 0; i < n; i++) if (!E[i]) { let j = i; do { j = (j + n - 1) % n } while (!E[j] && j !== i); E[i] = E[j] || [0, 0] }
  return S.map((v, i) => { const a = E[(i + n - 1) % n], b = E[i], k = Math.max(.3, 1 + a[0] * b[0] + a[1] * b[1]); return [v[0] + d * (a[0] + b[0]) / k, v[1] + d * (a[1] + b[1]) / k] });
}
function drawFaces(c, faces, M, seam, o) {
  o = o || {};
  for (const f of faces) {
    if (f.line || f.text != null || f.mark) continue;
    const n = f.n || (f.g ? nrm([(f.g[0][0] + f.g[1][0]) / 2, (f.g[0][1] + f.g[1][1]) / 2, (f.g[0][2] + f.g[1][2]) / 2]) : faceN(f.P));
    if (!f.both) { const vis = f.g ? dot(faceN(f.P), VW) : dot(n, VW); if (vis <= 1e-3) continue }
    const S = f.P.map(p => P2(M, p)), gw = !f.noSeam && f.a == null && o.grow !== 0, G = gw ? growS(S, o.grow || .5) : S;
    c.beginPath(); c.moveTo(G[0][0], G[0][1]); for (let i = 1; i < G.length; i++) c.lineTo(G[i][0], G[i][1]); c.closePath();
    let fill;
    if (o.solid) fill = o.solid;
    else if (f.grad) { const h = S.length / 2 | 0, mid = (i0, i1) => { let x = 0, y = 0; for (let i = i0; i < i1; i++) { x += S[i][0]; y += S[i][1] } return [x / (i1 - i0), y / (i1 - i0)] }, A0 = f.gax ? P2(M, f.gax[0]) : mid(0, h), B0 = f.gax ? P2(M, f.gax[1]) : mid(h, S.length);
      const gr = c.createLinearGradient(A0[0], A0[1], B0[0], B0[1]), b = lit(n, f.m), gn = f.grad.length; f.grad.forEach((q, i) => gr.addColorStop(gn === 3 ? [0, .55, 1][i] : i / (gn - 1), litC(q, b))); fill = gr }
    else if (f.g4 && S.length === 4) {
      // the skin (the owner 14:39 (1)): the light at the four corners, a plane fitted to it on the screen, one gradient along that plane's
      // slope — the light continues from face to face both ways (no steps along the body); the same one fill
      const B = f.g4.map(q => lit(q, f.m)); let xc = 0, yc = 0, bc = 0; for (let i = 0; i < 4; i++) { xc += S[i][0] / 4; yc += S[i][1] / 4; bc += B[i] / 4 }
      let xx = 0, xy = 0, yy = 0, xb = 0, yb = 0; for (let i = 0; i < 4; i++) { const dx = S[i][0] - xc, dy = S[i][1] - yc, db = B[i] - bc; xx += dx * dx; xy += dx * dy; yy += dy * dy; xb += dx * db; yb += dy * db }
      const det = xx * yy - xy * xy; let be = 0, ga = 0; if (det > 1e-9) { be = (xb * yy - yb * xy) / det; ga = (yb * xx - xb * xy) / det }
      let s0 = 0, s1 = 0; for (let i = 0; i < 4; i++) { const v = (S[i][0] - xc) * be + (S[i][1] - yc) * ga; if (v < s0) s0 = v; if (v > s1) s1 = v }
      const dd = be * be + ga * ga;
      if (s1 - s0 < .004 || dd < 1e-12) fill = litC(f.c, bc);
      else { const gr = c.createLinearGradient(xc + be * s0 / dd, yc + ga * s0 / dd, xc + be * s1 / dd, yc + ga * s1 / dd); gr.addColorStop(0, litC(f.c, bc + s0)); gr.addColorStop(.5, litC(f.c, bc + (s0 + s1) / 2)); gr.addColorStop(1, litC(f.c, bc + s1)); fill = gr }
    }
    else if (f.g && S.length === 4) {
      // the gradient across the strip: from the middle of edge 0–3 to the middle of edge 1–2, perpendicular to the strip
      const A = [(S[0][0] + S[3][0]) / 2, (S[0][1] + S[3][1]) / 2], B = [(S[1][0] + S[2][0]) / 2, (S[1][1] + S[2][1]) / 2];
      let dx = S[3][0] - S[0][0], dy = S[3][1] - S[0][1]; const dl = Math.hypot(dx, dy);
      let bx = B[0] - A[0], by = B[1] - A[1];
      if (dl > 1e-6) { dx /= dl; dy /= dl; const pr = bx * dx + by * dy; bx -= pr * dx; by -= pr * dy }
      if (Math.hypot(bx, by) < 1e-4) fill = litC(f.c, lit(n, f.m));
      else { const gr = c.createLinearGradient(A[0], A[1], A[0] + bx, A[1] + by); gr.addColorStop(0, litC(f.c, lit(f.g[0], f.m))); gr.addColorStop(1, litC(f.c, lit(f.g[1], f.m))); fill = gr }
    } else fill = litC(f.c, lit(n, f.m));
    c.globalAlpha = f.a != null ? f.a : 1;
    c.fillStyle = fill; c.fill(); if (seam && !f.noSeam && !gw) { c.strokeStyle = fill; c.lineWidth = seam; c.lineJoin = 'round'; c.stroke() }
    c.globalAlpha = 1;
  }
}
function drawDecor(c, list, M, o) {
  o = o || {}; const oD = Object.assign({}, o, { grow: 0 });   // the decor keeps its exact outline (windows, panels)
  for (const d of list) {
    if (o.solid) { if (d.line || d.text || d.mark) continue; drawFaces(c, [d], M, 0, oD); continue }
    if (d.line) { if (d.n && dot(d.n, VW) <= 1e-3) continue; const S = d.P.map(p => P2(M, p)); c.strokeStyle = d.c; c.lineWidth = Math.max(.5 / (o.zoom || 1), d.w * M.s); c.lineCap = 'round'; if (d.dash) c.setLineDash(d.dash.map(v => v * M.s)); c.beginPath(); c.moveTo(S[0][0], S[0][1]); for (let i = 1; i < S.length; i++) c.lineTo(S[i][0], S[i][1]); c.stroke(); c.setLineDash([]); continue }
    if (d.text != null) { if (!d.text) continue; const p = P2(M, d.at), sz = d.size * M.s; if (sz * (o.zoom || 1) < 2.2) continue; c.save(); c.translate(p[0], p[1]); if (!d.flat) c.rotate(Math.PI / 2);
      c.font = (d.light ? '600 ' : '800 ') + sz + 'px Arial,"Noto Sans Hebrew",sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.direction = 'rtl';
      const w = c.measureText(d.text).width, mw = d.maxW * M.s; if (w > mw) c.font = (d.light ? '600 ' : '800 ') + (sz * mw / w) + 'px Arial,"Noto Sans Hebrew",sans-serif';
      if (d.halo) { c.lineJoin = 'round'; c.strokeStyle = d.halo; c.lineWidth = sz * .22; c.strokeText(d.text, 0, 0) } c.fillStyle = d.col; c.fillText(d.text, 0, 0); c.restore(); continue }
    if (d.mark) { const p = P2(M, d.at), s = d.size * M.s; c.save(); c.translate(p[0], p[1]); c.fillStyle = d.col; c.strokeStyle = d.col; c.lineWidth = s * .16;
      if (d.mark === 'bird') { c.beginPath(); c.moveTo(0, s * .5); c.lineTo(-s * .4, -s * .4); c.lineTo(0, -s * .15); c.lineTo(s * .4, -s * .4); c.closePath(); c.fill() }
      else if (d.mark === 'arc') { c.beginPath(); c.arc(0, 0, s * .45, -.4 + Math.PI / 2, 3.5 + Math.PI / 2); c.stroke() }
      else if (d.mark === 'chev') { c.beginPath(); c.moveTo(0, s * .5); c.lineTo(-s * .45, 0); c.lineTo(-s * .45, -s * .2); c.lineTo(0, s * .3); c.lineTo(s * .45, -s * .2); c.lineTo(s * .45, 0); c.closePath(); c.fill() }
      else if (d.mark === 'stripes') { for (const k of [-1, 0, 1]) c.fillRect(-s * .45, k * s * .28 - s * .07, s * .9, s * .14) }
      else if (d.mark === 'sun') { c.beginPath(); c.arc(0, 0, s * .26, 0, TAU); c.fill(); c.beginPath(); for (let i = 0; i < 8; i++) { const a = i / 8 * TAU; c.moveTo(Math.cos(a) * s * .34, Math.sin(a) * s * .34); c.lineTo(Math.cos(a) * s * .5, Math.sin(a) * s * .5) } c.stroke() }
      else if (d.mark === 'star') { c.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? s * .2 : s * .5; c.lineTo(Math.cos(a) * r, Math.sin(a) * r) } c.closePath(); c.fill() }
      else if (d.mark === 'ring') { c.beginPath(); c.arc(0, 0, s * .38, 0, TAU); c.stroke() }
      else if (d.mark === 'leaf') { c.beginPath(); c.ellipse(0, 0, s * .2, s * .48, 0, 0, TAU); c.fill() }
      else { c.beginPath(); c.moveTo(0, s * .5); c.lineTo(s * .32, 0); c.lineTo(0, -s * .5); c.lineTo(-s * .32, 0); c.closePath(); c.fill() }
      c.restore(); continue }
    drawFaces(c, [d], M, 0, oD);
  }
}
function drawGear(c, p, M, o) {
  o = o || {};
  const T = p.tyres.slice().sort((a, b) => a.y - b.y);
  const tyre = r => { const x = M.X + r.x * M.s, yc = M.Y + (r.y - K * r.r) * M.s, hh = r.r * Math.sqrt(1 + K * K) * M.s, hw = r.w / 2 * M.s;
    c.beginPath(); c.roundRect(x - hw, yc - hh, hw * 2, hh * 2, Math.min(hw, hh) * .7);
    if (o.solid) { c.fillStyle = o.solid; c.fill(); return }
    const g = c.createLinearGradient(x - hw, 0, x + hw, 0); g.addColorStop(0, '#2c3136'); g.addColorStop(.45, '#1d2125'); g.addColorStop(1, '#121417'); c.fillStyle = g; c.fill();
    c.fillStyle = 'rgba(255,255,255,.07)'; c.fillRect(x - hw * .7, yc - hh * .9, hw * 1.4, hh * .35) };
  const leg = l => { const x = M.X + l.x * M.s, y0 = M.Y + (l.y - K * l.z0) * M.s, y1 = M.Y + (l.y - K * l.z1) * M.s, w = l.r * M.s;
    if (o.solid) { c.fillStyle = o.solid; c.fillRect(x - w, y1, w * 2, y0 - y1); return }
    const g = c.createLinearGradient(x - w, 0, x + w, 0); g.addColorStop(0, '#c9ced2'); g.addColorStop(.5, '#9aa1a8'); g.addColorStop(1, '#5d646b'); c.fillStyle = g; c.fillRect(x - w, y1, w * 2, y0 - y1) };
  if (!o.solid) for (const r of T) { const x = M.X + r.x * M.s, y = M.Y + r.y * M.s; c.fillStyle = 'rgba(8,12,16,.38)'; c.beginPath(); c.ellipse(x + r.w * .15 * M.s, y + r.r * .15 * M.s, (r.w * .75 + .1) * M.s, r.r * .55 * M.s, 0, 0, TAU); c.fill() }   // R‑14 (3): the contact shadow
  const legs = p.legs || [], back = T.filter(r => r.y < (legs[0] ? legs[0].y : 1e9) - .01), front = T.filter(r => !back.includes(r));
  back.forEach(tyre); legs.forEach(leg); front.forEach(tyre);
}
// a piece of an aircraft (or any piece with faces + decor + tyres)
function drawPiece(c, p, M, seam, o) {
  o = o || {};
  if (p.tyres) drawGear(c, p, M, o); if (!p.faces.length) return;
  drawFaces(c, p.faces, M, seam, o);
  if (p.decor && p.decor.length) drawDecor(c, p.decor.filter(d => !d.late), M, o);
  if (p.decor) drawDecor(c, p.decor.filter(d => d.late), M, o);
}
// the shadow of a piece on the ground (opaque; the page lays the shadow layer down with its alpha)
function shadowPiece(c, p, M) {
  c.beginPath();
  const U = SUN(), SHX = U.x, SHY = U.y, S = q => [M.X + (q[0] + q[2] * SHX) * M.s, M.Y + (q[1] + q[2] * SHY) * M.s];
  if (p.tyres && !p.faces.length) { for (const r of p.tyres) { const a = S([r.x - r.w / 2, r.y - r.r, r.r]), w = r.w * M.s, h = r.r * 2 * M.s; c.rect(a[0], a[1] - h * .2, w + r.r * SHX * M.s, h) } for (const l of p.legs || []) { const a = S([l.x, l.y, l.z0]), b = S([l.x, l.y, l.z1]); c.moveTo(a[0] - l.r * M.s, a[1]); c.lineTo(b[0] - l.r * M.s, b[1]); c.lineTo(b[0] + l.r * M.s, b[1]); c.lineTo(a[0] + l.r * M.s, a[1]); c.closePath() } c.fill(); return }
  for (const f of p.faces) { if (f.line || f.ns) continue; let Q = f.P.map(S), ar = 0; for (let i = 0; i < Q.length; i++) { const a = Q[i], b = Q[(i + 1) % Q.length]; ar += a[0] * b[1] - b[0] * a[1] } if (Math.abs(ar) < 1e-6) continue; if (ar < 0) Q = Q.reverse();
    c.moveTo(Q[0][0], Q[0][1]); for (let i = 1; i < Q.length; i++) c.lineTo(Q[i][0], Q[i][1]); c.closePath() }
  c.fill('nonzero');
}
// the screen bounding box of a piece (world px)
function bboxPiece(p, M) {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const acc = s => { x0 = Math.min(x0, s[0]); x1 = Math.max(x1, s[0]); y0 = Math.min(y0, s[1]); y1 = Math.max(y1, s[1]) };
  for (const f of p.faces) for (const q of f.P) acc(P2(M, q));
  if (p.tyres) for (const r of p.tyres) { acc(P2(M, [r.x - r.w / 2, r.y, r.r * 2.2])); acc(P2(M, [r.x + r.w / 2, r.y + r.r, 0])) }
  if (p.legs) for (const l of p.legs) acc(P2(M, [l.x, l.y, l.z1]));
  return [x0 - 1, y0 - 1, x1 + 1, y1 + 1];
}
// the sort key of a piece, world px: y of its south edge + its lowest point's height / K
const keyOf = (p, M) => M.Y + p.yMax * M.s + p.zMin / K * M.s;

// ======================================================================================================================================
// ground service vehicles of the sample (boxes, the same sun) — a belt loader, a catering truck, a baggage tug with carts, cones
function gseBelt(x, y, dir, zTip, col) {   // dir: +1 = the belt rises toward east, −1 toward west; x, y = the rear end (metres)
  const L = 7.4, W = 2.1, f = [], d = dir, X = u => x + d * u;
  const P = (u0, u1, v0, v1) => [[X(u0), y + v0], [X(u1), y + v0], [X(u1), y + v1], [X(u0), y + v1]];
  f.push(...boxFaces(P(0, L * .82, -W / 2, W / 2), .45, 1.15, { top: sh(col, -.05), side: sh(col, -.2) }, { mat: 'paint' }));
  f.push(...boxFaces(P(.2, 1.9, -W / 2 + .1, -.05), 1.15, 2.35, { top: '#2b3036', side: sh(col, -.1) }, { mat: 'paint' }));   // the driver's cab at the rear left
  const z0 = 1.25, z1 = zTip, u0 = .9, u1 = L + .4, bw = .62;
  f.push(...boxFaces(P(u0, u1, -bw, bw), [z0 - .25, z1 - .25, z1 - .25, z0 - .25], [z0, z1, z1, z0], { top: '#30353b', side: '#4a5057' }, { mat: 'matte' }));
  for (const v of [-bw - .05, bw - .05]) f.push(...boxFaces(P(u0, u1, v, v + .1), [z0, z1, z1, z0], [z0 + .35, z1 + .35, z1 + .35, z0 + .35], { top: '#d6d9dc', side: '#9ba2a8' }, { mat: 'metal' }));
  const wh = []; for (const u of [1.1, L * .7]) for (const v of [-W / 2 + .1, W / 2 - .1]) wh.push({ x: X(u), y: y + v, r: .38, w: .3 });
  return { faces: f, tyres: wh };
}
function gseCatering(x, y, dir, zBox, col, band) {   // (x, y) = the platform's tip at the door; the truck extends from the aircraft along dir (±1 in x)
  const f = [], d = dir, X = u => x + d * u, W = 2.5;
  const P = (u0, u1, v0, v1) => { const a = X(u0), b = X(u1); return [[Math.min(a, b), y + v0], [Math.max(a, b), y + v0], [Math.max(a, b), y + v1], [Math.min(a, b), y + v1]] };
  f.push(...boxFaces(P(1.0, 10.4, -W / 2 + .15, W / 2 - .15), .5, 1.2, { top: '#2b3036', side: '#22262b' }));
  f.push(...boxFaces(P(8.2, 10.6, -W / 2, W / 2), 1.1, 3.0, { top: sh(col, -.04), side: sh(col, -.15) }, { mat: 'paint' }));
  f.push(...boxFaces(P(8.35, 8.9, -W / 2 + .2, W / 2 - .2), 2.1, 2.85, { top: '#1d3143', side: '#33434f' }, { mat: 'glass' }));
  f.push(...boxFaces(P(1.1, 7.4, -W / 2, W / 2), zBox, zBox + 2.6, { top: sh(col, .02), side: col }, { mat: 'paint' }));
  if (band) f.push(...boxFaces(P(1.1, 7.4, W / 2 - .01, W / 2), zBox + .9, zBox + 1.3, { top: band, side: band }, { mat: 'paint' }));
  f.push(...boxFaces(P(0, 1.1, -.9, .9), zBox - .05, zBox + .12, { top: '#9aa1a8', side: '#6c737a' }, { mat: 'metal' }));
  const dec = [];
  for (const v of [-W / 2 + .3, W / 2 - .3]) { dec.push({ line: 1, P: [[X(1.6), y + v, 1.2], [X(6.6), y + v, zBox]], c: '#5b636b', w: .12 }); dec.push({ line: 1, P: [[X(6.6), y + v, 1.2], [X(1.6), y + v, zBox]], c: '#5b636b', w: .12 }) }
  const wh = []; for (const u of [2.2, 9.4]) for (const v of [-W / 2 + .15, W / 2 - .15]) wh.push({ x: X(u), y: y + v, r: .45, w: .35 });
  return { faces: f, decor: dec, tyres: wh };
}
function gseTug(x, y, heading, col) {   // heading: 'n' | 's'; x, y = the centre
  const f = [], L = 2.9, W = 1.5, s = heading === 's' ? 1 : -1;
  f.push(...boxFaces([[x - W / 2, y - L / 2], [x + W / 2, y - L / 2], [x + W / 2, y + L / 2], [x - W / 2, y + L / 2]], .3, 1.0, { top: sh(col, -.05), side: sh(col, -.2) }, { mat: 'paint' }));
  const yc = y - s * .4; f.push(...boxFaces([[x - .6, yc - .55], [x + .6, yc - .55], [x + .6, yc + .55], [x - .6, yc + .55]], 1.0, 1.9, { top: '#2b3036', side: '#3a4047' }));
  const wh = []; for (const u of [-.95, .95]) for (const v of [-.62, .62]) wh.push({ x: x + v, y: y + u, r: .3, w: .26 });
  return { faces: f, tyres: wh };
}
function gseCart(x, y, col) {   // a covered baggage cart, along y, centre (x, y)
  const f = [], L = 2.7, W = 1.55;
  f.push(...boxFaces([[x - W / 2, y - L / 2], [x + W / 2, y - L / 2], [x + W / 2, y + L / 2], [x - W / 2, y + L / 2]], .35, .6, { top: '#4a5057', side: '#3a4047' }));
  f.push(...boxFaces([[x - W / 2 + .05, y - L / 2 + .1], [x + W / 2 - .05, y - L / 2 + .1], [x + W / 2 - .05, y + L / 2 - .1], [x - W / 2 + .05, y + L / 2 - .1]], .6, 1.85, { top: sh(col, .05), side: col }, { mat: 'matte' }));
  const wh = []; for (const u of [-.95, .95]) for (const v of [-.62, .62]) wh.push({ x: x + v, y: y + u, r: .2, w: .18 });
  return { faces: f, tyres: wh };
}
function cone(x, y) { const f = []; const r = .22, h = .75, N = 10; for (let i = 0; i < N; i++) { const a = i / N * TAU, b = (i + 1) / N * TAU; f.push(face([[x + r * Math.cos(a), y + r * Math.sin(a), .05], [x + r * Math.cos(b), y + r * Math.sin(b), .05], [x, y, h]], '#f07a22', 'paint')) } f.push(face([[x + .02, y + .23, .3], [x - .02, y + .23, .3], [x, y + .16, .45]], '#f4f4f4', 'paint', { both: true })); return { faces: f } }

G.A34 = { NOSE, tab, HELI, buildHeli, fusP, fusN, cockpit3D, cabOf, bandFor, K, LD, VW, get SHX() { return SUN().x }, get SHY() { return SUN().y }, TYPES, LIV, lit, litC, sh, build, bounds, drawPiece, drawFaces, drawDecor, shadowPiece, bboxPiece, keyOf, P2, boxFaces, vcyl, face, gseBelt, gseCatering, gseTug, gseCart, cone, fusShape };
})(typeof window !== 'undefined' ? window : globalThis);

return !!window.A34}
window.__OLD_SIZES={"C34": 274799, "P34": 106432, "A34": 99734};
