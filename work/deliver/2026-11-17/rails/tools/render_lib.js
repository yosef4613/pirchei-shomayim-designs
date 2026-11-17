// rails 17.11 — טוען את פונקציות הציור של המסילות מהמקור (כמו שהן) ומריץ אותן על SvgCtx: "לפני" = הסדר של המשחק
const path=require('path'),fs=require('fs');const {fnsrc,stmt}=require('./fnsrc.js');const {SvgCtx,Path2DShim}=require('./svgctx.js');
function load(wt,net,withPart=false){const extraSrc=withPart?('let drawLineRail=function(){};\n'+fs.readFileSync(path.join(wt,'parts','038d2_rails_jx.js'),'utf8')+'\n;drawLineRail=drawLineRail;'):'';
 const P=f=>path.join(wt,'parts',f);
 const p040=P('040_C6_E6_D4_p520a.js'),p020=P('020_E5_E6_E4_p681.js'),p038=P('038d_rail_turnouts.js');
 const src=[
  'let ctx=null;const RL_DECK_W=66,RL_COAST_X=6000;const e3InView=()=>true;const E3_BYPASS={pts:[[5978,2552]].concat((RAIL_SEG_BY_ID["BYP-NC"]||{pts:[]}).pts.map(p=>p.slice()))};',
  fnsrc(p020,'e5Walk'),fnsrc(p020,'e5OffsetPts'),fnsrc(p020,'e5SwitchStand'),fnsrc(p020,'e5Buffer'),
  'let '+fnsrc(p040,'rlPiers').replace(/^function rlPiers/,'rlPiers=function'),
  fnsrc(p040,'rlBBox'),stmt(p040,'const rlVisible='),stmt(p040,'const rlPath='),fnsrc(p040,'rlRails'),fnsrc(p040,'rlTrackLayer'),fnsrc(p040,'rlTrack'),fnsrc(p040,'rlDeck'),
  stmt(p040,'const RL_BRIDGES='),
  fs.readFileSync(p038,'utf8').slice(fs.readFileSync(p038,'utf8').indexOf('const TCT_J='),fs.readFileSync(p038,'utf8').indexOf('/* the check (D‑533)')),
  extraSrc,
  'return {RJX:(typeof RJX!=="undefined"?RJX:null),rjxDraw:(typeof rjxDraw!=="undefined"?rjxDraw:null),rjxPrep:(typeof rjxPrep!=="undefined"?rjxPrep:null),rjxAudit:(typeof rjxAudit!=="undefined"?rjxAudit:null),set ctx(c){ctx=c},get ctx(){return ctx},rlPiers:(...a)=>rlPiers(...a),wrapPiers:(f)=>{const o=rlPiers;rlPiers=function(g){return f(o,g)}},rlTrack,rlTrackLayer,rlDeck,rlPath,rlRails,rlBBox,RL_BRIDGES,TCT_J,get tctDraw(){return tctDraw},tctPrep,e5OffsetPts,e5Walk,e5SwitchStand,api:(typeof RAILS_JX!=="undefined"?RAILS_JX:null)}'
 ].join('\n');
 const RAIL_SEG_BY_ID={},RAIL_NODE_BY_ID={};for(const g of net.segs){RAIL_SEG_BY_ID[g.id]=g}for(const n of net.nodes)RAIL_NODE_BY_ID[n.id]=n;
 const F56_SIDING={id:'SIDING-F6',pts:net.f56};
 const f=new Function('RAIL_SEG_BY_ID','RAIL_NODE_BY_ID','F56_SIDING','RAIL_SEGS','RAIL_NODES','Path2D','window',src);
 const G=f(RAIL_SEG_BY_ID,RAIL_NODE_BY_ID,F56_SIDING,net.segs,net.nodes,Path2DShim,{});
 // S10V: העמודים — בלי עמוד במפתח השיט (021v)
 const SPAN={x0:6585,x1:6965};const inSpan=x=>x>SPAN.x0+4&&x<SPAN.x1-4;
 G.wrapPiers((o,g)=>{const had=!!(g&&g._piers);const out=o(g);if(had&&g._s10v)return out;if(g&&g.id==='EAST-B'){g._piers=out.filter(q=>!inSpan(q.x)&&Math.abs(q.x-SPAN.x0)>14&&Math.abs(q.x-SPAN.x1)>14);g._s10v=1;return g._piers}if(g&&g.id==='SIDING-F6'){g._piers=out.filter(q=>!(q.x>SPAN.x0-14&&q.x<SPAN.x1+14));g._s10v=1;return g._piers}return out});
 return {G,RAIL_SEG_BY_ID,F56_SIDING};
}
// הסדר של המשחק באזור המסילות של הים (E4 hook → drawLineRail → tcTurnouts)
function drawBefore(L,c,box,opt={}){const {G,RAIL_SEG_BY_ID,F56_SIDING}=L;G.ctx=c;
 c.fillStyle=opt.sea||'#1f5f8f';c.fillRect(box[0]-200,box[1]-200,box[2]-box[0]+400,box[3]-box[1]+400);
 const v={x0:box[0],y0:box[1],x1:box[2],y1:box[3]};const vis=g=>{const b=G.rlBBox(g);return b.x1+60>v.x0&&b.x0-60<v.x1&&b.y1+60>v.y0&&b.y0-60<v.y1};
 // 1. drawE4Rail → S9_HOOKS.rail → sidingRail (021v): rlDeck + rlTrack של מסילת ההיפוך
 if(F56_SIDING.pts.length){c.save();G.rlDeck(F56_SIDING);G.rlTrack(F56_SIDING);c.restore()}
 // 2. drawLineRail: הסיפונים, ואז המצעים / האדנים / הפסים בשכבות
 const Ls=G.RL_BRIDGES.map(id=>RAIL_SEG_BY_ID[id]).filter(g=>g&&vis(g));
 for(const g of Ls){c.save();if(g.id==='B-LINK'){c.beginPath();c.rect(5996,4700,440,470);c.clip()}else if(/^ISL-/.test(g.id)){c.beginPath();c.rect(6000,5100,720,868);c.clip()}if(g.kind!=='siding')G.rlDeck(g);c.restore()}
 for(const k of[0,1,2])for(const g of Ls){c.save();G.rlTrackLayer(g,k);c.restore()}
 // 3. tcTurnouts (038d) — אחרי drawLineRail
 if(!opt.noTct)for(const J of G.TCT_J){try{G.tctDraw(c,J)}catch(e){}}
 if(G.RJX&&!opt.noJx){for(const Z of G.RJX.zones)G.rjxDraw(c,Z)}
 if(opt.after)opt.after(c,G);
}
module.exports={load,drawBefore,SvgCtx};
