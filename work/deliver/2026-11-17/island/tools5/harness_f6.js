// island5: הרצה של הציור של מעבר השיט (021v) מחוץ לדפדפן — על SvgCtx של rails; פלט: ops.json (לרסטר שלי) ו-svg (לדף התוכנית)
// node harness_f6.js <worktree> <out-prefix> [night=0|1] [box x0,y0,x1,y1]
const fs=require('fs'),path=require('path'),vm=require('vm');
const RT='/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/rails/tools/';
const {SvgCtx}=require(RT+'svgctx.js');const {fnsrc,stmt}=require(RT+'fnsrc.js');
const [wt,outp,night,bx]=process.argv.slice(2);const P=f=>path.join(wt,'parts',f);
const box=(bx||'6600,4780,7400,5420').split(',').map(Number);
const src=fs.readFileSync(P('021v_F6_s10b_bridge.js'),'utf8');
const s020=fs.readFileSync(P('020_E5_E6_E4_p681.js'),'utf8'),s020a=fs.readFileSync(P('020a_S13_east2.js'),'utf8');
const ptsOf=(s,id)=>JSON.parse(s.match(new RegExp("id:'"+id+"'[^\\n]*?pts:(\\[\\[[^\\n]*?\\]\\])"))[1]);
const segs={'EAST-N1':ptsOf(s020a,'EAST-N1'),'EAST-B4':[[6460,5120],[7250,5120]],'EAST-C':[[7250,5120],[14400,5120]],'EAST-S2':[[6373,5158],[9600,5158],[14400,5158]],'ISL-A1':ptsOf(s020,'ISL-A1')};
const ctxBox={ctx:null};
const sb={Math,String,Number,Array,Object,JSON,console,performance:{now:()=>0},window:{},
 S9K:.6,S9HM:10,S9_SUN:{dx:.27,dy:.36},Camera:{zoom:1},e3InView:()=>true,g77Heb:t=>t,
 S9_HOOKS:{rail:[],over:[],water:[]},f56Rail:function(){},F56_SIDING:{id:'SIDING-F6',pts:[[6460,5120],[7200,5050]]},
 RAIL_SEG_BY_ID:{},w3IsSea:(x,y)=>x>6232,PORT_BERTHS:[],FISH3:{HOOK:{}},F56LIVE:{pilotPose:()=>({stop:'berth',x:0,y:0,h:0}),pilotDraw(){}},
 BOAT34:{buoy(c,x,y,col){c.fillStyle=col==='red'?'#d23a2c':'#2f9a4a';c.beginPath();c.arc(x,y,6,0,6.283);c.fill()},T:{}},
 S10U:{err:()=>null},roadAudit:function(){return{ok:true,checks:[]}},F56_BUOYS:[],RL_DECK_W:66,RL_COAST_X:6000};
for(const [id,pts] of Object.entries(segs)){const g={id,pts};sb.RAIL_SEG_BY_ID[id]=g}
sb.RL_BRIDGES=Object.keys(segs);
vm.createContext(sb);
const pre=['let ctx=null;',fnsrc(P('019b_E4E5_s9_draw.js'),'s9Hex'),fnsrc(P('019b_E4E5_s9_draw.js'),'s9Txt'),fnsrc(P('020_E5_E6_E4_p681.js'),'e5Walk'),fnsrc(P('020_E5_E6_E4_p681.js'),'e5OffsetPts'),
 fnsrc(P('040_C6_E6_D4_p520a.js'),'rlPiers'),fnsrc(P('040_C6_E6_D4_p520a.js'),'rlBBox'),stmt(P('040_C6_E6_D4_p520a.js'),'const rlPath='),fnsrc(P('040_C6_E6_D4_p520a.js'),'rlRails'),
 fnsrc(P('040_C6_E6_D4_p520a.js'),'rlTrackLayer'),fnsrc(P('040_C6_E6_D4_p520a.js'),'rlTrack'),fnsrc(P('040_C6_E6_D4_p520a.js'),'rlDeck')].join('\n');
const code=pre+'\n'+src.replace(/try\{window\.roadAudit=roadAudit\}catch\(e\)\{\}/,'')+'\n;this.__S10V=S10V;this.__setCtx=c=>{ctx=c};';
vm.runInContext(code,sb,{filename:'021v'});
const S=sb.__S10V;const c=new SvgCtx();sb.__setCtx(c);const N=night==='1';
// מים
c.fillStyle=N?'#0f2a44':'#4f93c4';c.fillRect(box[0]-50,box[1]-50,box[2]-box[0]+100,box[3]-box[1]+100);
c.fillStyle=N?'#3b3a33':'#d9d2bd';c.fillRect(box[0]-50,box[1]-50,Math.max(0,6230-box[0]+50),box[3]-box[1]+100);
for(const f of sb.S9_HOOKS.rail)f(c,0,N);
const L=Object.values(sb.RAIL_SEG_BY_ID);for(const g of L)vm.runInContext('rlDeck(RAIL_SEG_BY_ID["'+g.id+'"])',sb);for(const k of[0,1,2])for(const g of L)vm.runInContext('rlTrackLayer(RAIL_SEG_BY_ID["'+g.id+'"],'+k+')',sb);
for(const f of sb.S9_HOOKS.water)f(c,0,N);
// רכבת על B4 — מלבן של קרונות, כדי לראות את הקשת מעליה
c.fillStyle='#a5532e';c.fillRect(6860,5106,150,28);c.fillStyle='#2f6a8f';c.fillRect(7016,5106,150,28);
for(const f of sb.S9_HOOKS.over)f(c,0,N);
fs.writeFileSync(outp+'.ops.json',JSON.stringify(c.dumpOps()));
fs.writeFileSync(outp+'.svg',c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],1200));
const a=S.audit();console.log('ops',c.out.length,'audit',a.ok,JSON.stringify(a.checks.filter(x=>!x.ok).map(x=>x.name+': '+x.detail)).slice(0,1500));
