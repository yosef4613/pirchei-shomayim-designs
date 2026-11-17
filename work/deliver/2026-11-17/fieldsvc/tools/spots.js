const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const {S15D,S15SIM}=new Function(src+';return {S15D,S15SIM}')();
const sp=S15D.spots;console.log('spots',Object.keys(sp).length);
const by={};for(const [id,o] of Object.entries(sp)){const t=o.t||id.split('-')[0];(by[t]=by[t]||[]).push(id+'@'+(o.home||'')+(o.serves?'>'+o.serves:''))}
for(const t in by)console.log(t,by[t].length,by[t].join(' '));
console.log('stands',Object.entries(S15D.stands).map(([k,s])=>k+':'+s.type+':'+s.cx+','+s.nose+':'+(s.bridge?'B':'')).join(' '));
console.log('parked',JSON.stringify(S15D.parked));
console.log('pockets',Object.keys(S15D.pockets||{}).join(' '));
console.log('sched',JSON.stringify(S15SIM.sched).slice(0,800));
