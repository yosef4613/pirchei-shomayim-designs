// הטבלה "כמה שלבים הוסבו מתוך כמה" — מהנתונים (SA_SPEC) ומהמלאי (stories_dump.json): טקסט להחזרה, ו-HTML לדף הציור
const fs=require('fs');const [src,dump,outTxt,page]=process.argv.slice(2);
const s=fs.readFileSync(src,'utf8');const SPEC=eval('('+s.match(/var SA_SPEC=(\{[\s\S]*?\]\}\});/)[1]+')');
const D=JSON.parse(fs.readFileSync(dump,'utf8'));const A=new Set(['drive','fix','wait','act','enter','clock','job','startJob','fuel','fixed','buy']);
const KN={take:'הרמה',give:'מסירה',pick:'קטיף',work:'עבודה',check:'בדיקה',photo:'צילום',look:'תצפית',wear:'לבישה',sort:'מיון',hang:'תלייה',plant:'שתילה',via:'נשיאה בדרך'};
const fam=id=>id.startsWith('ZS-')?'17 האזורים (ZS)':id.split('-')[0];
const F={};let T={all:0,had:0,plain:0,conv:0,look:0,none0:0,none1:0};const kinds={};
for(const S of D){const f=fam(S.id),r=F[f]||(F[f]={st:0,all:0,had:0,plain:0,conv:0,look:0,none0:0,none1:0});r.st++;let had=false,has=false;
 S.steps.forEach((st,i)=>{r.all++;T.all++;if(st.keys.some(q=>A.has(q))){r.had++;T.had++;had=has=true;return}r.plain++;T.plain++;const a=SPEC[S.id]&&SPEC[S.id][i+1];if(a){kinds[a[0]]=(kinds[a[0]]||0)+1;if(a[0]==='look'){r.look++;T.look++}else{r.conv++;T.conv++;has=true}}});
 if(!had){r.none0++;T.none0++}if(!has){r.none1++;T.none1++}}
const rows=Object.entries(F).sort((a,b)=>b[1].plain-a[1].plain);
let txt='משפחה | סיפורים | שלבים | עם פעולה מקודם | רק "הגעה + לחיצה" | הוסבו לפעולה | תצפית | נשארו שיחה | סיפורים בלי פעולה: לפני → אחרי\n';
for(const [f,r] of rows)txt+=`${f} | ${r.st} | ${r.all} | ${r.had} | ${r.plain} | ${r.conv} | ${r.look} | ${r.plain-r.conv-r.look} | ${r.none0} → ${r.none1}\n`;
txt+=`סה״כ | ${D.length} | ${T.all} | ${T.had} | ${T.plain} | ${T.conv} | ${T.look} | ${T.plain-T.conv-T.look} | ${T.none0} → ${T.none1}\n`;
txt+='לפי סוג: '+Object.entries(kinds).sort((a,b)=>b[1]-a[1]).map(([k,n])=>KN[k]+' '+n).join(' · ')+'\n';
fs.writeFileSync(outTxt,txt);
if(page){let h='<table><tr><th>משפחה</th><th>סיפורים</th><th>שלבים</th><th>עם פעולה מקודם</th><th>רק "הגעה + לחיצה"</th><th>הוסבו לפעולה</th><th>תצפית</th><th>נשארו שיחה</th><th>סיפורים בלי פעולה: לפני ← אחרי</th></tr>';
 for(const [f,r] of rows)h+=`<tr><td>${f}</td><td>${r.st}</td><td>${r.all}</td><td>${r.had}</td><td>${r.plain}</td><td><b>${r.conv}</b></td><td>${r.look}</td><td>${r.plain-r.conv-r.look}</td><td>${r.none0} ← ${r.none1}</td></tr>`;
 h+=`<tr><th>סה״כ</th><th>${D.length}</th><th>${T.all}</th><th>${T.had}</th><th>${T.plain}</th><th>${T.conv}</th><th>${T.look}</th><th>${T.plain-T.conv-T.look}</th><th>${T.none0} ← ${T.none1}</th></tr></table><p>לפי סוג: ${Object.entries(kinds).sort((a,b)=>b[1]-a[1]).map(([k,n])=>KN[k]+' '+n).join(' · ')}</p><p>"נשארו שיחה" — שלבים שבהם מישהו מבקש או מספר (תדריך, תשלום בסוף); שניים מהם (הדיג בשונית, שלוש ההרמות במנוף) כבר פעולה במנגנון משלהם.</p>`;
 let P=fs.readFileSync(page,'utf8');P=P.replace(/<div id="tbl" class="c">[\s\S]*?<\/div>\n<\/main>/,'<div id="tbl" class="c">'+h+'</div>\n</main>');fs.writeFileSync(page,P)}
console.log(txt);
