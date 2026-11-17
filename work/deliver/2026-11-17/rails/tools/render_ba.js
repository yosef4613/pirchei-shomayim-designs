// rails 17.11 — לפני / אחרי לאזור: node render_ba.js <worktree> <net.json> <outdir> <name> <x0,y0,x1,y1> [width]
const {load,drawBefore,SvgCtx}=require('./render_lib.js');const fs=require('fs'),path=require('path');
const [wt,netf,outd,name,bx,wd]=process.argv.slice(2);const net=JSON.parse(fs.readFileSync(netf,'utf8'));const box=bx.split(',').map(Number);const W=+(wd||900);
for(const [tag,withPart] of[['before',false],['after',true]]){const L=load(wt,JSON.parse(JSON.stringify(net)),withPart);const c=new SvgCtx();drawBefore(L,c,box);
 if(withPart&&L.G.RJX&&L.G.RJX.err)console.log('RJX.err',L.G.RJX.err);
 fs.writeFileSync(path.join(outd,name+'_'+tag+'.svg'),c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],W));fs.writeFileSync(path.join(outd,name+'_'+tag+'.ops.json'),JSON.stringify(c.dumpOps()));
 if(withPart&&L.G.rjxAudit)console.log('audit',JSON.stringify(L.G.rjxAudit()));console.log(tag,c.out.length)}
