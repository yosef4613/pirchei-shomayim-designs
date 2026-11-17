// where_words.js — לכל מילה: כמה מופעים במזהים (שמות פנימיים) וכמה במחרוזות / תבניות (טקסט — אולי לשחקן), עם דוגמאות. node where_words.js <build.html>
const fs=require('fs'),path=require('path'),acorn=require(path.join(__dirname,'node','node_modules','acorn'));
const html=fs.readFileSync(process.argv[2],'utf8');const W=(process.argv[3]||'slot,body,model,pool,bar,strip,club,beach,swim,party,wine,disco,female,cheat,girl,escort,hot,spa,lover,love,sex,bed,dance,dress,pub,מועדון,חוף,בריכה,יין,בירה,נשים,רחצה,חתונה,שינה,מסיבה,בגד ים').split(',');
const res={};for(const w of W)res[w]={id:0,str:0,ex:{}};
const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m;
while((m=re.exec(html))){let toks;try{toks=[...acorn.tokenizer(m[1],{ecmaVersion:'latest',allowHashBang:true,allowReturnOutsideFunction:true})]}catch(e){continue}
 for(const t of toks){const lab=t.type.label;let kind=null,val='';if(lab==='name'){kind='id';val=String(t.value)}else if(lab==='string'||lab==='template'){kind='str';val=String(t.value)}else continue;
  const low=val.toLowerCase();for(const w of W){const hit=/[א-ת]/.test(w)?new RegExp('(^|[^א-ת])[ובלהמשכ]{0,2}'+w+'($|[^א-ת])').test(val):low.includes(w);if(hit){res[w][kind]++;const k=kind==='id'?val:val.slice(0,40);res[w].ex[k]=(res[w].ex[k]||0)+1}}}}
for(const w of W){const r=res[w];const ex=Object.entries(r.ex).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([k,n])=>k+'×'+n).join(' | ');console.log(w.padEnd(8),'מזהים',String(r.id).padStart(4),'מחרוזות',String(r.str).padStart(4),' ',ex)}
