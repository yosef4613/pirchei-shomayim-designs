// הספירה של הטבלה SA_SPEC מול המלאי (stories_dump.json) — בלי דפדפן
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const m=src.match(/var SA_SPEC=(\{[\s\S]*?\]\}\});/);const SPEC=eval('('+m[1]+')');
let n=0;const k={};for(const id in SPEC)for(const s in SPEC[id]){n++;const t=SPEC[id][s][0];k[t]=(k[t]||0)+1}
const D=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
const A=new Set(['drive','fix','wait','act','enter','clock','job','startJob','fuel','fixed','buy']);
let bad=[],plain=0,left=[];for(const S of D)S.steps.forEach((st,i)=>{if(st.keys.some(q=>A.has(q)))return;plain++;if(!(SPEC[S.id]&&SPEC[S.id][i+1]))left.push(S.id+'#'+(i+1)+' '+(st.btn||'—'))});
for(const id in SPEC)for(const s in SPEC[id]){const S=D.find(q=>q.id===id);if(!S){bad.push(id+' missing');continue}const st=S.steps[+s-1];if(!st){bad.push(id+'#'+s+' nostep');continue}if(st.keys.some(q=>A.has(q)))bad.push(id+'#'+s+' has '+st.keys)}
console.log(JSON.stringify({converted:n,plain,left:left.length,kinds:k,bad},null,0));if(process.argv[4])console.log(left.join('\n'));
