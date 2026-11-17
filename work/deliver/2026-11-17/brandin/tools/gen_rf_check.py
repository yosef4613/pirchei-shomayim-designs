#!/usr/bin/env python3
# gen_rf_check.py — brandin: דף בדיקה "לפני / אחרי" לששת המזנונים — לפני: הקוד של המעצב כמו שהוא (refined_1825/refined/brands/*.js);
#  אחרי: הנתונים המוקטנים של המשחק (refined_data.json) באותו מפענח של 074v_brandin. כל שלט בגודל שלו במשחק (פי 6 ופי 2), ביום ובלילה,
#  וההבדל הממוצע בין שניהם (נמדד בדף). usage: python3 gen_rf_check.py <out.html>
import sys, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); D = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/set7_watch/refined_1825/refined/'
RF = json.load(open(HERE + '/refined_data.json', encoding='utf-8'))
tpl = open(HERE + '/brandin_tpl.js', encoding='utf-8').read()
a = tpl.index('const TCBI_RF_IX'); b = tpl.index('function tcbiRfSpr')
dec = tpl[a:b]
cat = open(D + 'catalog.js', encoding='utf-8').read()
br = ''.join('<script>' + open(D + 'brands/' + i + '.js', encoding='utf-8').read().replace('</script', '<\\/script') + '</script>\n' for i in RF['brands'])
H = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מזנוני השדה — לפני ואחרי</title>
<style>:root{--bg:#f4f1ea;--fg:#1c2628;--muted:#5b6869;--card:#fff;--line:#d9d4c8}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d}}
:root[data-theme="dark"]{--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Arial,sans-serif}main{max-width:1100px;margin:auto;padding:16px}.row{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;margin:10px 0;overflow-x:auto}
.pair{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-start}.pair div{display:flex;flex-direction:column;gap:4px}small{color:var(--muted)}canvas{background:#0c2226;border-radius:2px;max-width:100%}button{font:inherit;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg)}</style></head>
<body><main><h1>מזנוני השדה — הקוד של המעצב מול המשחק</h1><p>לכל מזנון: השלט בגודל שלו במשחק (יחידות עולם × 6, ומתחת — × 2, כמעט כמו במשחק בזום רגיל) והלוגו (5:4). מימין — הקוד של המעצב כמו שהוא; משמאל — הנתונים המוקטנים שנכנסו למשחק (48 צבעים, 8 נקודות ליחידת עולם). "הבדל" — ההפרש הממוצע בין שני הציורים באותו גודל (0–255 לכל ערוץ).</p>
<p><button id="nt">יום / לילה</button> <span id="sum"></span></p><section id="v"></section></main>
<script>''' + cat + '</script>\n' + br + '''<script>
const TCBI_RF=''' + json.dumps(RF, ensure_ascii=False, separators=(',', ':')) + ''';\n''' + dec + '''
let night=false;const V=document.getElementById('v');
function before(c,id,f,w,h){TC_REFINED_BRANDS[id].draw(c,f,0,0,w,h,{night})}
function diff(id,f,w,h){const a=document.createElement('canvas'),b=document.createElement('canvas');a.width=b.width=w;a.height=b.height=h;before(a.getContext('2d'),id,f,w,h);tcbiRfDraw(b.getContext('2d'),id,f,0,0,w,h,night);
 const A=a.getContext('2d').getImageData(0,0,w,h).data,B=b.getContext('2d').getImageData(0,0,w,h).data;let s=0;for(let i=0;i<A.length;i+=4)s+=Math.abs(A[i]-B[i])+Math.abs(A[i+1]-B[i+1])+Math.abs(A[i+2]-B[i+2]);return s/(A.length/4*3)}
function show(){V.innerHTML='';const R=[];for(const m of TC_REFINED_CATALOG){const d=document.createElement('div');d.className='row';d.innerHTML='<h3>'+m.name+' · '+m.id+' · שלט '+m.face.w+'×'+m.face.h+'</h3>';
 for(const [f,W,H] of [['sign',m.face.w*6,m.face.h*6],['sign',m.face.w*2,m.face.h*2],['logo',150,120]]){const p=document.createElement('div');p.className='pair';const df=diff(m.id,f,W,H);R.push(df);
  for(const [lab,fn] of [['לפני — הקוד של המעצב',(c)=>before(c,m.id,f,W,H)],['אחרי — במשחק',(c)=>tcbiRfDraw(c,m.id,f,0,0,W,H,night)]]){const q=document.createElement('div'),c=document.createElement('canvas');c.width=W;c.height=H;c.style.width=W+'px';fn(c.getContext('2d'));q.append(c);q.insertAdjacentHTML('beforeend','<small>'+lab+'</small>');p.append(q)}
  p.insertAdjacentHTML('beforeend','<small>'+(f==='sign'?'שלט':'לוגו')+' '+W+'×'+H+' · הבדל '+df.toFixed(1)+'</small>');d.append(p)}V.append(d)}
 document.getElementById('sum').textContent='הבדל ממוצע: '+(R.reduce((a,b)=>a+b,0)/R.length).toFixed(1)+' · הכי גדול: '+Math.max(...R).toFixed(1);window.__RF=R}
document.getElementById('nt').onclick=()=>{night=!night;show()};show();
</script></body></html>'''
open(sys.argv[1], 'w', encoding='utf-8').write(H); print(sys.argv[1], os.path.getsize(sys.argv[1]))
