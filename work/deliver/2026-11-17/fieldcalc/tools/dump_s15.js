// הוצאת S15D ו-S15SIM מקובץ הנתונים (קריאה בלבד)
const fs=require('fs');
const src=fs.readFileSync(process.argv[2],'utf8').split('\n');
const out={};
for(const ln of src){const m=ln.match(/^var (S15D|S15SIM)=(.*);?\s*$/); if(m){let t=m[2].replace(/;\s*$/,''); out[m[1]]=JSON.parse(t);} }
fs.writeFileSync(process.argv[3],JSON.stringify(out));
const D=out.S15D,S=out.S15SIM;
console.log('S15D keys',Object.keys(D).join(' '));
console.log('S15SIM keys',Object.keys(S).join(' '), 'T',S.T);
