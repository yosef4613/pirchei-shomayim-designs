// rails 17.11 — שליפת רשת המסילות מקבצי המקור בלי דפדפן (Node): 020 + 020a + 020b + E3_BYPASS + S9DG (המסילה של F6) + TCT_J
// שימוש: node rail_extract.js <worktree> <out.json>
const fs=require('fs'),path=require('path');const [wt,out]=process.argv.slice(2);
const P=f=>fs.readFileSync(path.join(wt,'parts',f),'utf8');
const lines=(s,a,b)=>s.split('\n').slice(a-1,b).join('\n');
const p019=P('019_E3_E4_D2_p660.js').split('\n');const byp=p019.find(l=>l.startsWith('const E3_BYPASS='));
const p020=P('020_E5_E6_E4_p681.js').split('\n');
const i0=p020.findIndex(l=>l.startsWith('function e5SCurve'));const i1=p020.findIndex(l=>l.startsWith('function railRoute'));
const s9dg=P('019d_F5F6_s9.js').split('\n').find(l=>l.startsWith('const S9DG='));
const tct=P('038d_rail_turnouts.js');const tj=tct.slice(tct.indexOf('const TCT_J='),tct.indexOf('function tctDivPts'));
const RAIL_STOCK_DEF=p020.slice(p020.findIndex(l=>l.startsWith('const RAIL_STOCK=')),p020.findIndex(l=>l.startsWith('const RAIL_SIGNALS='))).join('\n');
const src=[byp,p020.slice(i0,i1).join('\n'),RAIL_STOCK_DEF,P('020a_S13_east2.js'),P('020b_S16c_east_s.js'),s9dg,
 "const F56_SIDING=(()=>{const R=S9DG.rails.find(r=>r.id==='SIDING');const p=R?R.pts.slice():[];if(p.length&&p[p.length-1][0]<7200)p.push([7200,5050]);return{id:'SIDING-F6',pts:p}})();",
 tj,
 (fs.existsSync(path.join(wt,'parts','038d2_rails_jx.js'))&&process.env.WITH_RJX?('let drawLineRail=function(){},tctDraw=function(){};\n'+P('038d2_rails_jx.js')):''),
 "module.exports={RAIL_NODES,RAIL_SEGS,TCT_J,F56_SIDING,S16C_EAST,PORT_TRACKS,S9DG_RAILS:S9DG.rails,ERR:(typeof window!=='undefined'?window:{}),GEO:(typeof RJX_GEO!=='undefined'?RJX_GEO:null)};"].join('\n');
const tmp=path.join(path.dirname(out),'_rail_src.js');
fs.writeFileSync(tmp,"'use strict';const window={};\n"+src);
const M=require(path.resolve(tmp));
const r1=v=>Math.round(v*100)/100;
const R={nodes:M.RAIL_NODES.map(n=>({...n})),segs:M.RAIL_SEGS.map(g=>{const o={};for(const k in g){if(k[0]==='_'||k==='cum'||k==='ptsWas')continue;o[k]=k==='pts'?g.pts.map(p=>[r1(p[0]),r1(p[1])]):g[k]}return o}),
 tct:M.TCT_J.map(J=>({id:J.id,main:J.main,half:J.half||0,deck:!!J.deck,div:J.div.map(d=>d.seg?{seg:d.seg,rev:!!d.rev}:{pts:'F56_SIDING'})})),
 f56:M.F56_SIDING.pts,s16c:M.S16C_EAST,s9dgRails:M.S9DG_RAILS.map(r=>({id:r.id,n:(r.pts||[]).length,pts:r.pts})),err:M.ERR};
fs.writeFileSync(out,JSON.stringify(R));
console.log('geo',JSON.stringify(M.GEO));console.log('nodes',R.nodes.length,'segs',R.segs.length,'tct',R.tct.length,'f56',R.f56.length,'s16c.err',M.S16C_EAST.err,'win',JSON.stringify(M.ERR));
