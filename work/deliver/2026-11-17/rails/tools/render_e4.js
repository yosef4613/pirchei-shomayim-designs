// rails 17.11 — ציור E4 / E3 לבדיקה: רקע קרקע, המסילות הראשיות כמו s9TrackStraight, השאר rlTrack, ואז האזור JX-E4 (אחרי) — node render_e4.js <wt> <net> <out> <x0,y0,x1,y1> <width> [after]
const {load,SvgCtx}=require('./render_lib.js');const fs=require('fs');
const [wt,netf,out,bx,wd,after]=process.argv.slice(2);const net=JSON.parse(fs.readFileSync(netf,'utf8'));const box=bx.split(',').map(Number);
const L=load(wt,net,after==='1');const G=L.G,c=new SvgCtx();G.ctx=c;
c.fillStyle='#cfc8b4';c.fillRect(box[0]-100,box[1]-100,box[2]-box[0]+200,box[3]-box[1]+200);
for(const x of[5800,5900]){c.fillStyle='#666b6d';c.fillRect(x-24,box[1]-50,48,box[3]-box[1]+100);c.fillStyle='#413d37';for(let y=2558;y<box[3]+50;y+=16)if(y>box[1]-60)c.fillRect(x-20,y,40,5);c.strokeStyle='#c6cbd0';c.lineWidth=3;for(const dx of[-13,13]){c.beginPath();c.moveTo(x+dx,box[1]-50);c.lineTo(x+dx,box[3]+50);c.stroke()}}
for(const g of net.segs){if(/^(A-|B-|T1|T2)/.test(g.id)&&g.pts.length===2)continue;if(!g.pts.some(p=>p[0]>box[0]-80&&p[0]<box[2]+80&&p[1]>box[1]-80&&p[1]<box[3]+80))continue;c.save();G.rlTrack({...g});c.restore()}
for(const J of G.TCT_J){try{J._p=null;G.tctDraw(c,J)}catch(e){}}
if(after==='1'&&G.RJX){for(const Z of G.RJX.zones)G.rjxDraw(c,Z);console.log('rjx',JSON.stringify(G.RJX.err),JSON.stringify(G.rjxAudit()))}
if(/\.svg$/.test(out))fs.writeFileSync(out,c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],'100%',' class="sk"'));else fs.writeFileSync(out,JSON.stringify(c.dumpOps()));
module.exports={};
