const {load,drawBefore,SvgCtx}=require('./render_lib.js');const fs=require('fs');
const [wt,netf,out,bx]=process.argv.slice(2);const net=JSON.parse(fs.readFileSync(netf,'utf8'));
const box=(bx||'6291,5016,6619,5246').split(',').map(Number);const L=load(wt,net);const c=new SvgCtx();
drawBefore(L,c,box);fs.writeFileSync(out,c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],1100));fs.writeFileSync(out.replace(/\.svg$/,'.ops.json'),JSON.stringify(c.dumpOps()));console.log('ok',c.out.length,'elements');
