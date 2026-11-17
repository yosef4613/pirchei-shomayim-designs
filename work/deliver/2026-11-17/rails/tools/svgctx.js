// rails 17.11 — הקשר ציור (Canvas 2D) שכותב SVG: מריצים את פונקציות הציור של המשחק כמו שהן ומקבלים ציור SVG נקי (כלל 13 / 17)
class SvgCtx{
 constructor(){this.ops=[];this.clips={};this.out=[];this.defs=[];this.id=0;this.S={m:[1,0,0,1,0,0],fillStyle:'#000',strokeStyle:'#000',lineWidth:1,lineCap:'butt',lineJoin:'miter',globalAlpha:1,dash:[],clip:null,font:'10px sans-serif',textAlign:'start',textBaseline:'alphabetic'};this.stack=[];this.path=[];this.filter='none';this.globalCompositeOperation='source-over';this.imageSmoothingEnabled=true}
 get fillStyle(){return this.S.fillStyle}set fillStyle(v){this.S.fillStyle=v}
 get strokeStyle(){return this.S.strokeStyle}set strokeStyle(v){this.S.strokeStyle=v}
 get lineWidth(){return this.S.lineWidth}set lineWidth(v){this.S.lineWidth=v}
 get lineCap(){return this.S.lineCap}set lineCap(v){this.S.lineCap=v}
 get lineJoin(){return this.S.lineJoin}set lineJoin(v){this.S.lineJoin=v}
 get globalAlpha(){return this.S.globalAlpha}set globalAlpha(v){this.S.globalAlpha=v}
 get font(){return this.S.font}set font(v){this.S.font=v}
 get textAlign(){return this.S.textAlign}set textAlign(v){this.S.textAlign=v}
 get textBaseline(){return this.S.textBaseline}set textBaseline(v){this.S.textBaseline=v}
 save(){this.stack.push({...this.S,m:this.S.m.slice(),dash:this.S.dash.slice()})}
 restore(){if(this.stack.length)this.S=this.stack.pop()}
 setLineDash(d){this.S.dash=(d||[]).slice()}getLineDash(){return this.S.dash.slice()}
 _mul(a,b){return[a[0]*b[0]+a[2]*b[1],a[1]*b[0]+a[3]*b[1],a[0]*b[2]+a[2]*b[3],a[1]*b[2]+a[3]*b[3],a[0]*b[4]+a[2]*b[5]+a[4],a[1]*b[4]+a[3]*b[5]+a[5]]}
 translate(x,y){this.S.m=this._mul(this.S.m,[1,0,0,1,x,y])}rotate(a){const c=Math.cos(a),s=Math.sin(a);this.S.m=this._mul(this.S.m,[c,s,-s,c,0,0])}scale(x,y){this.S.m=this._mul(this.S.m,[x,0,0,y,0,0])}
 setTransform(a,b,c,d,e,f){this.S.m=[a,b,c,d,e,f]}resetTransform(){this.S.m=[1,0,0,1,0,0]}transform(a,b,c,d,e,f){this.S.m=this._mul(this.S.m,[a,b,c,d,e,f])}
 _p(x,y){const m=this.S.m;return[m[0]*x+m[2]*y+m[4],m[1]*x+m[3]*y+m[5]]}
 _sc(){const m=this.S.m;return Math.sqrt(Math.abs(m[0]*m[3]-m[1]*m[2]))}
 beginPath(){this.path=[]}
 moveTo(x,y){const p=this._p(x,y);this.path.push('M'+p[0].toFixed(1)+' '+p[1].toFixed(1))}
 lineTo(x,y){const p=this._p(x,y);if(!this.path.length)this.path.push('M');this.path.push('L'+p[0].toFixed(1)+' '+p[1].toFixed(1))}
 closePath(){this.path.push('Z')}
 rect(x,y,w,h){this.moveTo(x,y);this.lineTo(x+w,y);this.lineTo(x+w,y+h);this.lineTo(x,y+h);this.closePath()}
 bezierCurveTo(a,b,c,d,e,f){const p1=this._p(a,b),p2=this._p(c,d),p3=this._p(e,f);this.path.push('C'+[p1,p2,p3].map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' '))}
 quadraticCurveTo(a,b,c,d){const p1=this._p(a,b),p2=this._p(c,d);this.path.push('Q'+[p1,p2].map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' '))}
 arc(cx,cy,r,a0,a1,ccw){this.ellipse(cx,cy,r,r,0,a0,a1,ccw)}
 ellipse(cx,cy,rx,ry,rot,a0,a1,ccw){let span=a1-a0;if(ccw){span=-(((a0-a1)%(2*Math.PI))+2*Math.PI)%(2*Math.PI);if(Math.abs(a0-a1)>=2*Math.PI-1e-6)span=-2*Math.PI}else{if(span>=2*Math.PI)span=2*Math.PI}const n=Math.max(8,Math.ceil(Math.abs(span)/(Math.PI/16)));const cr=Math.cos(rot),sr=Math.sin(rot);for(let i=0;i<=n;i++){const t=a0+span*i/n,x=cx+rx*Math.cos(t)*cr-ry*Math.sin(t)*sr,y=cy+rx*Math.cos(t)*sr+ry*Math.sin(t)*cr;if(i===0&&!this.path.length)this.moveTo(x,y);else this.lineTo(x,y)}}
 _col(v){if(v&&typeof v==='object')return v._c||'#888';return v==null?'none':String(v)}
 _cl(){return this.S.clip?` clip-path="url(#${this.S.clip})"`:''}
 _op(){return this.S.globalAlpha<1?` opacity="${this.S.globalAlpha.toFixed(3)}"`:''}
 _d(p){return(p&&p._d?p._d(this):this.path).join('')}
 stroke(p){const d=this._d(p);if(!d)return;this.ops.push({t:'s',d,w:this.S.lineWidth*this._sc(),c:this._col(this.S.strokeStyle),cap:this.S.lineCap,dash:this.S.dash.map(v=>v*this._sc()),a:this.S.globalAlpha,clip:this.S.clip});const w=this.S.lineWidth*this._sc();const da=this.S.dash.length?` stroke-dasharray="${this.S.dash.map(v=>(v*this._sc()).toFixed(1)).join(' ')}"`:'';this.out.push(`<path d="${d}" fill="none" stroke="${this._col(this.S.strokeStyle)}" stroke-width="${w.toFixed(1)}" stroke-linecap="${this.S.lineCap}" stroke-linejoin="${this.S.lineJoin}"${da}${this._op()}${this._cl()}/>`)}
 fill(p,rule){if(typeof p==='string'){rule=p;p=null}const d=this._d(p);if(!d)return;this.ops.push({t:'f',d,c:this._col(this.S.fillStyle),a:this.S.globalAlpha,clip:this.S.clip,rule});this.out.push(`<path d="${d}" fill="${this._col(this.S.fillStyle)}"${rule==='evenodd'?' fill-rule="evenodd"':''}${this._op()}${this._cl()}/>`)}
 fillRect(x,y,w,h){const sv=this.path;this.path=[];this.rect(x,y,w,h);this.fill();this.path=sv}
 strokeRect(x,y,w,h){const sv=this.path;this.path=[];this.rect(x,y,w,h);this.stroke();this.path=sv}
 clearRect(){}
 clip(p,rule){if(typeof p==='string'){rule=p;p=null}const d=this._d(p);const id='c'+(++this.id);this.clips[id]={d,parent:this.S.clip,rule};this.defs.push(`<clipPath id="${id}"${this.S.clip?` clip-path="url(#${this.S.clip})"`:''}><path d="${d}"${rule==='evenodd'?' clip-rule="evenodd"':''}/></clipPath>`);this.S.clip=id}
 createLinearGradient(){return{_c:'#888',addColorStop(o,c){if(o<=.5)this._c=c}}}
 createRadialGradient(){return{_c:'rgba(0,0,0,0)',addColorStop(o,c){if(o===0)this._c=c}}}
 fillText(t,x,y){const p=this._p(x,y);const fs=(parseFloat((this.S.font.match(/([\d.]+)px/)||[0,10])[1])*this._sc()).toFixed(1);const an=this.S.textAlign==='center'?'middle':this.S.textAlign==='right'||this.S.textAlign==='end'?'end':'start';this.out.push(`<text x="${p[0].toFixed(1)}" y="${p[1].toFixed(1)}" font-size="${fs}" text-anchor="${an}" fill="${this._col(this.S.fillStyle)}"${this._cl()}>${String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')}</text>`)}
 strokeText(){}measureText(t){return{width:String(t).length*5}}drawImage(){}
 dumpOps(){return{ops:this.ops,clips:this.clips}}
 svg(vb,w,extra=''){const m=60,X0=vb[0]-m,Y0=vb[1]-m,X1=vb[0]+vb[2]+m,Y1=vb[1]+vb[3]+m;
  const clipLine=d=>{/* keep only the runs of a polyline near the view (stroke widths here are < 2*m) */const out=[];let cur=[];const pts=[];const re=/([MLZ])([^MLZ]*)/g;let q;while((q=re.exec(d))){const k=q[1],a=q[2].trim().split(/\s+/).map(Number);if(k==='Z'){pts.push(['Z']);continue}pts.push([k,a[0],a[1]])}
   if(pts.some(p=>p[0]==='Z'))return d;const inb=p=>p[1]>=X0&&p[1]<=X1&&p[2]>=Y0&&p[2]<=Y1;let prevIn=false,prev=null;
   for(const p of pts){const i=inb(p);if(p[0]==='M'){if(cur.length>1)out.push(cur);cur=i?[p]:[];prev=p;prevIn=i;continue}
    if(i||prevIn){if(!cur.length&&prev)cur.push(['M',prev[1],prev[2]]);cur.push(p)}else{if(cur.length>1)out.push(cur);cur=[]}prev=p;prevIn=i}
   if(cur.length>1)out.push(cur);return out};
  const runD=r=>r.map((p,j)=>(j?'L':'M')+p[1].toFixed(1)+' '+p[2].toFixed(1)).join('');
  const keep=e=>{const md=e.match(/ d="([^"]+)"/);if(!md)return e;if(md[1].length<200)return e;const runs=clipLine(md[1]);if(typeof runs==='string')return e;if(!runs.length)return'';
   if(!/stroke-dasharray/.test(e))return e.replace(md[1],runs.map(runD).join(''));
   /* a dashed line: each run keeps the phase of the whole line (stroke-dashoffset = the length before it) */
   const all=[];{const re=/([ML])([^MLZ]*)/g;let q;while((q=re.exec(md[1]))){const a=q[2].trim().split(/\s+/).map(Number);all.push([q[1],a[0],a[1]])}}
   const cum=[0];for(let i=1;i<all.length;i++)cum.push(cum[i-1]+(all[i][0]==='M'?0:Math.hypot(all[i][1]-all[i-1][1],all[i][2]-all[i-1][2])));
   const idx=p=>{for(let i=0;i<all.length;i++)if(Math.abs(all[i][1]-p[1])<.05&&Math.abs(all[i][2]-p[2])<.05)return i;return 0};
   return runs.map(r=>e.replace(md[1],runD(r)).replace('/>',` stroke-dashoffset="${(cum[idx(r[0])]).toFixed(1)}"/>`)).join('')};
  return`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.join(' ')}" width="${w}" style="max-width:100%;height:auto"${extra}><defs>${this.defs.join('')}</defs>${this.out.map(keep).join('')}</svg>`}
}
class Path2DShim{constructor(){this.cmds=[]}moveTo(x,y){this.cmds.push(['moveTo',x,y])}lineTo(x,y){this.cmds.push(['lineTo',x,y])}closePath(){this.cmds.push(['closePath'])}rect(...a){this.cmds.push(['rect',...a])}arc(...a){this.cmds.push(['arc',...a])}ellipse(...a){this.cmds.push(['ellipse',...a])}
 _d(c){const sv=c.path;c.path=[];for(const [k,...a] of this.cmds)c[k](...a);const r=c.path;c.path=sv;return r}}
module.exports={SvgCtx,Path2DShim};
