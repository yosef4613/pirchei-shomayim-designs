#!/usr/bin/env python3
# gen_review.py — airlogos 17.11 (הבעלים 12:55): הדף לבעלים "השלטים והלוגואים של חבילת המותגים" — כל השלטים של העיר והשדה מהחבילה, מצוירים
#  בקוד של המעצב (city-signs / airport / airport-ops / airport-ops/logos — renderer.js) בגודל של השלט, עם שם המקום והמצב במשחק; והטבלה של
#  חברות התעופה (שמות חדשים באנגלית — הצעה). הלוגואים של 62 המותגים — מטבלת המותגים של המשחק (master S7F301, הקידוד בלי תנועות), דרך shim
#  של TURBO_CITY_BRANDS; בלי תמונות. usage: python3 gen_review.py <share> <logos.json> <master signs12> <airlines.json> <inventory_kinds.json> <out.html>
import sys, json, re, html
SH, LG, S12, AL, OUT = sys.argv[1:6]
def cat(p, var):
    s = open(p, encoding='utf-8').read(); return json.loads(s[s.index('['):s.rindex(']') + 1])
city = [m for m in cat(SH + '/city-signs/catalog.js', 'TC_CITY_CATALOG') if not m.get('engine')]
air = cat(SH + '/airport/catalog.js', 'TC_AIRPORT_CATALOG'); ops = cat(SH + '/airport-ops/ops_catalog.js', ''); alg = cat(SH + '/airport-ops/logos/logo_catalog.js', '')
L = json.load(open(LG, encoding='utf-8')); s12 = open(S12, encoding='utf-8').read()
FACE = json.loads(re.search(r'const TCS12_FACE=(\{.*?\});', s12).group(1)); ROWS = json.loads(re.search(r'const TCS12_ROWS=(\[.*?\]);', s12, re.S).group(1))
F_LOGO = {r[0]: r[2] for r in ROWS if r[2]}
IN = set(FACE['s9']) | set(FACE['bld']) | {'קפה החוף', 'חנות הדיג'}
for k, b in L['brands'].items():
    for s in b['signs']:
        if len(s) > 1 and s[1]: IN.add(s[1])
def trim(m, keep):
    o = {k: m[k] for k in keep if k in m}
    o['formats'] = {k: {q: f[q] for q in ('w', 'h', 'label', 'kind', 'text', 'measured') if q in f} for k, f in m['formats'].items()}
    return o
CK = ('id', 'placeId', 'name', 'group', 'subtitle', 'brandKey', 'brandName', 'color', 'role', 'classification', 'category')
cityT = [trim(m, CK) for m in city]
st = {}
for m in city:
    faces = [f for f in m['formats'].values() if f.get('kind') in ('identity_panel', 'text_only_identity', 'operational', 'address_panel', 'dynamic_marquee')]
    on = [f for f in faces if (f.get('text') or m['name']) in IN]
    st[m['id']] = 'game' if on else ('F' if F_LOGO.get(m.get('placeId')) else 'none')
# השדה: מה כבר בענף airlogos (הסמל הפשוט / הפס / האריח), ומה לא
BR_AIR = {'sunbeak', 'aurelia', 'skyline', 'coral', 'tidewind', 'zebrano', 'mirage', 'confetti', 'terminal-cafe', 'gate-cafe', 'juice', 'pizza', 'shawarma', 'salads', 'bakery', 'dutyfree', 'books', 'toys', 'pharmacy', 'gifts', 'electronics', 'hotel', 'rental', 'terminal-east', 'terminal-west'}
BAND = {'האנגר א׳', 'האנגר ב׳', 'האנגר ג׳', 'חוות הדלק', 'סדנת רכבי השירות', 'אגף השערים P1–P6', 'כבאות והצלה — השדה', 'משטרה · מד״א', 'שער המטען', 'שער עובדים', 'מודיעין'}
for m in ops:
    t = m.get('sourceText') or m.get('name')
    st['ops:' + m['id']] = 'branch' if (t in BAND and m.get('family') != 'terminal_hanging') or m.get('family') in ('operational_e4_plate', 'bridge_gate_screen') else 'none'
for m in air: st['air:' + m['id']] = 'branch' if m['id'] in BR_AIR else 'none'
for m in alg: st['logo:' + m['id']] = 'branch'
AK = ('id', 'name', 'group', 'subtitle', 'color', 'ink', 'signType', 'sourceIds', 'headline', 'tagline', 'bg', 'copySide', 'dark', 'original')
airT = [trim(m, AK) for m in air]
opsT = [dict(trim(m, ('id', 'name', 'group', 'family', 'classification', 'kind', 'color', 'ink', 'sourceIds', 'sourceText', 'originals', 'dynamic', 'signType', 'dark')), **({'formats': m['formats']} if False else {})) for m in ops]
for o, m in zip(opsT, ops): o['formats'] = {k: {q: f[q] for q in ('w', 'h', 'label', 'kind', 'units') if q in f} for k, f in m['formats'].items()}
for k in m.keys(): pass
algT = alg
brands = {k: {'name': b['name'], 'deep': b['deep'], 'accent': b['accent'], 'light': b['light'], 'logo': b['logo']} for k, b in L['brands'].items()}
al = json.load(open(AL, encoding='utf-8'))
def js(v): return json.dumps(v, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
def src(p):
    s = open(SH + '/' + p, encoding='utf-8').read()
    s = s.replace('function part(c,p,x,y,w,h){', 'function part(c,p,x,y,w,h){if(p&&p.__draw){p.__draw(c,x||0,y||0,w,h);return;}')
    return s.replace('</script', '<\\/script')
# for the airport campaign renderer: the original('airport'/'rental') reads TURBO_CITY_BRANDS[key].parts — the shim has it
import os
def region(pid, bk):
    pid = pid or ''
    if re.match(r'^(IS-|ISL|G8-FERRY)', pid): return 'island'
    if bk == 'port' or re.match(r'^(C6|D6|E6|TUG|P-D6|LN-D6|DW-D6|PG-)', pid): return 'port'
    if re.match(r'^(APT|S15|S16|E2W|RA-|FIDS)', pid) or bk == 'airport': return 'airport'
    return 'city'
LV = {}
for m in city:
    faces = [(k, f) for k, f in m['formats'].items() if f.get('kind') not in ('local_identity', 'poster')]
    real = [(k, f) for k, f in faces if k != 'proposal']
    on = [k for k, f in real if (f.get('text') or m['name']) in IN]
    if real and len(on) == len(real): lv, miss = 'ok', 'כל ' + str(len(real)) + ' השלטים של המקום במשחק'
    elif on: lv, miss = 'part', 'במשחק ' + str(len(on)) + ' מתוך ' + str(len(real)) + ' שלטים; חסרים: ' + ', '.join((f.get('text') or k) for k, f in real if k not in on)[:160]
    elif F_LOGO.get(m.get('placeId')): lv, miss = 'part', 'הלוגו במסך המקום (F) ובמפה; חסר: ' + ('השלט על החזית' if real else 'משטח שלט — אין היום במשחק (מידה מוצעת)')
    else: lv, miss = 'drawn', ('המשחק מצייר את השלט הקודם' if real else 'אין משטח שלט במשחק (מידה מוצעת)')
    LV[m['id']] = [lv, miss, region(m.get('placeId'), m.get('brandKey'))]
for m in alg: LV['logo:' + m['id']] = ['part', 'בענף airlogos (ממתין למיזוג): הסמל הפשוט על השלט; חסר: הלוגו המלא הזה', 'airport']
for m in air:
    LV['air:' + m['id']] = (['part', 'בענף airlogos (ממתין למיזוג): השלט בטרמינל; המודעות (promo / poster) — אין להן משטח במשחק', 'airport'] if m['id'] in BR_AIR else ['pkg', 'מודעה בלבד — אין משטח במשחק', 'airport'])
for m in ops:
    br = st['ops:' + m['id']] == 'branch'
    LV['ops:' + m['id']] = ['part', 'בענף airlogos: הכיתוב הקיים + לוגו; חסר: העיצוב המלא של המעצב', 'airport'] if br else ['drawn', 'המשחק מצייר את השלט הקודם (אותו כיתוב)', 'airport']
LIB = json.load(open(SH + '/library/index.json', encoding='utf-8'))
libT = []
for b in LIB['brands']:
    k = b['key']; fm = {}
    for f, d in b['formats'].items():
        if f == 'logo': fm[f] = [d['w'], d['h'], 'ok', 'במשחק: מסך המקום, המפה, השלטים']
        elif b['set'] <= 5: fm[f] = [d['w'], d['h'], 'ok', 'במשחק: ' + {'poster': 'הסככות והפוסטרים', 'rear': 'גב האוטובוסים', 'side': 'דופן האוטובוסים', 'wrap': 'עטיפת האוטובוסים'}.get(f, f)]
        else: fm[f] = [d['w'], d['h'], 'pkg', 'רק בחבילה — לא במשחק (הקוד כבד, לא מצויר בדף)']
    libT.append({'key': k, 'name': b['name'], 'cat': b.get('category', ''), 'set': b['set'], 'inGame': k in L['brands'], 'places': [p['id'] + ' · ' + p['name'] for p in b.get('places', [])][:40], 'n': len(b.get('places', [])), 'fm': fm})
PS = open(SH + '/posters/Turbo_City_Event_Posters_Code.js', encoding='utf-8').read()
posters = []
for k, t in re.findall(r'"key":"([^"]+)"[^}]{0,200}?"title":"([^"]+)"', PS) + re.findall(r'\{key:"([^"]+)",[^}]{0,120}title:"([^"]+)"', PS):
    if k not in [p[0] for p in posters]: posters.append([k, t])
cnt = {k: sum(1 for m in city if st[m['id']] == k) for k in ('game', 'F', 'none')}
nf = sum(len([f for f in m['formats'].values() if f.get('kind') != 'local_identity']) for m in city)
SAN = [('APT-KISS', 'APT-DROP'), ('KISS', 'DROP'), ('Kiss', 'Drop'), ('kiss', 'drop'), ('C2-WINE', 'C2-CELLAR')]
byname = {b['name']: k for k, b in L['brands'].items()}
ALIAS = {b['key']: byname[b['name']] for b in LIB['brands'] if b['key'] not in L['brands'] and b['name'] in byname}
data = 'const ALIAS=' + js(ALIAS) + ';\nconst LV=' + js(LV) + ';\nconst LIBT=' + js(libT) + ';\nconst POST=' + js(posters) + ';\nconst BR=' + js(brands) + ';\nconst CITY=' + js(cityT) + ';\nconst AIRC=' + js(airT) + ';\nconst OPS=' + js(opsT) + ';\nconst ALG=' + js(algT) + ';\nconst ST=' + js(st) + ';\nconst AL=' + js(al) + ';\n'
for a, b in SAN: data = data.replace(a, b)
H = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>שלטי חבילת המותגים</title><style>
:root{--bg:#f4f1ea;--fg:#1c2628;--muted:#5b6869;--card:#fff;--line:#d9d4c8;--ok:#1e7a46;--part:#b07a12;--drawn:#2a6fc4;--pkg:#8a4b9c}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d;--ok:#4cc483;--part:#e0b04a;--drawn:#6aa8f0;--pkg:#c98ddb}}
:root[data-theme="dark"]{--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d;--ok:#4cc483;--part:#e0b04a;--drawn:#6aa8f0;--pkg:#c98ddb}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Arial,"Noto Sans Hebrew",sans-serif}main{max-width:1320px;margin:auto;padding:16px}
h1{font-size:26px;margin:.3em 0}h2{font-size:20px;margin:1.2em 0 .4em}.muted{color:var(--muted)}
nav{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}nav button,.f button{font:inherit;padding:7px 12px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}
nav button.on,.f button.on{outline:2px solid var(--drawn)}.f{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:8px 0}.f input,.f select{font:inherit;padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;min-height:120px;overflow:hidden}
.card h3{font-size:15px;margin:0 0 2px}.card .id{font-size:12px;color:var(--muted)}.fm{margin-top:8px}.fm small{display:block;color:var(--muted);font-size:12px}.miss{font-size:13px;margin-top:4px}
.fm canvas{display:block;max-width:100%;margin-top:3px;background:#0c2226;border-radius:2px}
.b{display:inline-block;font-size:12px;padding:1px 8px;border-radius:10px;color:#fff;margin-top:4px}.b.ok{background:var(--ok)}.b.part{background:var(--part)}.b.drawn{background:var(--drawn)}.b.pkg{background:var(--pkg)}.b.ds{background:transparent;border:1px solid currentColor}.ds.full{color:#c0392b}.ds.mid{color:#7f8c3a}.ds.simple{color:#7a7f86}.ds.na{color:#9a9a9a}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid var(--line);padding:6px;text-align:right;vertical-align:top}.sw{display:inline-block;width:16px;height:16px;border-radius:3px;border:1px solid var(--line);vertical-align:middle;margin-left:3px}
.tw{overflow-x:auto}.sum{display:flex;flex-wrap:wrap;gap:10px}.sum div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px}.sum b{font-size:20px;display:block}
</style></head><body><main>
<h1>השלטים והלוגואים של חבילת המותגים — הכול, לפי אזור</h1>
<p>כל מה שיש בחבילה (שלטי העיר והשדה, הלוגואים, השילוט התפעולי של השדה, 62 הזהויות וכל הפורמטים, הפוסטרים) — מצויר כאן בקוד של המעצב (קנבס, בלי תמונות), <b>כל שלט בגודל האמיתי שלו ביחס לאחרים</b> (3 פיקסלים לכל יחידה של העולם; כפתור "הגדלה" — פי 2), עם שם המקום והרמה שלו במשחק. הלוגואים — מטבלת המותגים של המשחק (S7F301). <span class="muted">airlogos · 17.11.2026</span></p>
<div class="sum" id="sum"></div>
<p>הרמות: <span class="b ok">במשחק ועובד</span> <span class="b part">במשחק חלקית</span> (בכרטיס — מה חסר) <span class="b drawn">מצויר ולא במשחק</span> <span class="b pkg">רק בחבילה</span> <span class="muted">· "בענף airlogos" = נבנה היום, ממתין למיזוג.</span></p>
<p><b>ציון העיצוב (נפרד מהרמה במשחק) — אומדן, אתה מחליט:</b> <span class="b ds full">מעוצב מלא</span> יש בשלט לוגו מעוצב של מותג (עם הטיפוגרפיה והצבעים שלו), או ציור עשיר (120+ פעולות ציור ו-6+ צבעים) · <span class="b ds mid">בינוני</span> טקסט וצבע (2+ צבעים), סמל קטן או צורה פשוטה, בלי לוגו מותג · <span class="b ds simple">פשוט — אייקון / גליף</span> כל השאר · <span class="b ds na">לא נמדד</span> מודעה בלבד (לא מצוירת בדף) או לוח מידע חי (לוחות טיסות ומסכי שערים — בדף בלי נתונים, ולכן ריקים). איך נקבע: הדף מצייר כל שלט פעם אחת ברקע וסופר מהקוד עצמו את פעולות הציור (מילוי, קו, טקסט, ציור לוגו), את מספר הצבעים, את העקומות (קשתות, אליפסות, עקומות בזייה, פינות מעוגלות), האם צויר לוגו מטבלת המותגים והאם יש טקסט. לכל פריט — הציון הגבוה מבין הפורמטים שלו, וליד כל פורמט — הציון והמדדים שלו. נבדק בעין על מדגם של צילומים בכל לשונית — לא על כל פריט ופריט. <span id="scp" class="muted"></span></p>
<nav id="tabs"><button data-t="city" class="on">העיר</button><button data-t="airport">השדה</button><button data-t="island">האי</button><button data-t="port">הנמל</button><button data-t="al">חברות התעופה — שמות חדשים</button><button data-t="lib">62 הזהויות — כל הפורמטים</button><button data-t="post">פוסטרי האירועים</button><button id="nt">יום / לילה</button><button id="zm">הגדלה</button></nav>
<section id="v"></section>
</main><script>
''' + L['tcb'].replace('</script', '<\\/script') + '''
''' + data + '''
window.TURBO_CITY_BRANDS={};
for(const k in BR){const P=BR[k].logo;const lg={w:P.w,h:P.h,__draw:(c,x,y,w,h)=>{let k2=1;try{const m=c.getTransform();k2=Math.hypot(m.a,m.b)||1}catch(e){}const e=TCB.pic('r|'+k,P,TCB.bucket(Math.max(4,w*k2)),TCB.bucket(Math.max(4,h*k2)));c.drawImage(e.cv,x,y,w,h)}};
 TURBO_CITY_BRANDS[k]={key:k,name:BR[k].name,parts:{logo:lg},draw:(c,f,x,y,w,h)=>lg.__draw(c,x,y,w,h)}}
for(const [a,b] of Object.entries(ALIAS))if(!TURBO_CITY_BRANDS[a]&&TURBO_CITY_BRANDS[b]){TURBO_CITY_BRANDS[a]=TURBO_CITY_BRANDS[b];BR[a]=BR[b]}
window.BRANDAPI={draw:(c,k,f,x,y,w,h)=>{const P=BR[k].logo;c.fillStyle=P.L[0][0];c.fillRect(x,y,w,h);const s=Math.min(w/P.w,h/P.h);TURBO_CITY_BRANDS[k].draw(c,'logo',x+(w-P.w*s)/2,y+(h-P.h*s)/2,P.w*s,P.h*s)}};
window.TC_CITY_CATALOG=CITY;window.TC_AIRPORT_CATALOG=AIRC;window.TC_AIRPORT_OPS_CATALOG=OPS;window.TC_AIRPORT_LOGO_CATALOG=ALG;
</script>
<script>''' + src('favicon-code.js') + '''</script>
<script>''' + src('city-signs/renderer.js') + '''</script>
<script>''' + src('airport/renderer.js') + '''</script>
<script>''' + src('airport-ops/renderer.js') + '''</script>
<script>''' + src('airport-ops/logos/logo_renderer.js') + '''</script>
<script>
/* ציון העיצוב (אומדן): מודדים את הציור עצמו — כמה פעולות ציור, כמה צבעים, קווים מעוגלים / צורות, האם יש לוגו מותג (מטבלת המותגים) והאם יש טקסט */
const M={ctx:null,ops:0,cols:new Set(),curves:0,logo:0,text:0};
(function(){const P=CanvasRenderingContext2D.prototype,col=c=>{const f=c.fillStyle;M.cols.add(typeof f==='string'?f.toLowerCase():'grad'+M.cols.size)};
 for(const k of ['fill','fillRect','stroke','strokeRect','drawImage']){const f=P[k];P[k]=function(){if(M.ctx&&this===M.ctx){M.ops++;if(k==='fill'||k==='fillRect')col(this);if(k==='drawImage'&&arguments[0]&&arguments[0].__logo)M.logo++}return f.apply(this,arguments)}}
 for(const k of ['fillText','strokeText']){const f=P[k];P[k]=function(){if(M.ctx&&this===M.ctx){M.ops++;M.text++;col(this)}return f.apply(this,arguments)}}
 for(const k of ['arc','arcTo','ellipse','bezierCurveTo','quadraticCurveTo','roundRect']){const f=P[k];if(f)P[k]=function(){if(M.ctx&&this===M.ctx)M.curves++;return f.apply(this,arguments)}}})();
for(const k in TURBO_CITY_BRANDS){const L0=TURBO_CITY_BRANDS[k].parts.logo,d0=L0.__draw;L0.__draw=function(c){if(M.ctx&&c===M.ctx)M.logo++;else if(c&&c.canvas)c.canvas.__logo=1;return d0.apply(this,arguments)}}
const DS={full:'מעוצב מלא',mid:'בינוני',simple:'פשוט — אייקון / גליף',na:'לא נמדד'};
function measure(api,id,f,fmt){const w=f.w<300&&f.h<300?f.w*4:300,h=f.w<300&&f.h<300?f.h*4:200,c=document.createElement('canvas');c.width=Math.max(2,Math.min(1200,Math.round(w)));c.height=Math.max(2,Math.round(h*(c.width/w)));const g=c.getContext('2d');
 M.ctx=g;M.ops=0;M.cols=new Set();M.curves=0;M.logo=0;M.text=0;try{window[api].draw(g,id,fmt,0,0,c.width,c.height,{night:false})}catch(e){}M.ctx=null;
 const r={ops:M.ops,cols:M.cols.size,curves:M.curves,logo:M.logo>0,text:M.text>0},art=r.ops>=120&&r.cols>=6,isLogo=fmt==='logo'&&api!=='TC_CITY';
 r.s=(r.ops<3&&!r.logo)?'na':(r.logo||art)?'full':(r.text&&r.cols>=2&&r.ops>=3)?'mid':'simple';return r}
const SC={};let scDone=false;
function allItems(){const o=[];for(const rg in RG)for(const x of items(rg))o.push(x);for(const b of LIBT)o.push({api:'BRANDAPI',id:b.key,fm:{logo:{w:b.fm.logo[0],h:b.fm.logo[1]}},skip:null});return o}
function scoreAll(){const L=allItems();let i=0;const step=()=>{const t0=performance.now();while(i<L.length&&performance.now()-t0<40){const x=L[i++],k=x.api+'|'+x.id;if(SC[k])continue;if(x.dyn){SC[k]={s:'na',per:{}};continue}let best=null;const per={};for(const f in x.fm){const F=x.fm[f];if(x.skip&&x.skip(f,F))continue;const r=measure(x.api,x.id,F,f);per[f]=r;if(!best||['na','simple','mid','full'].indexOf(r.s)>['na','simple','mid','full'].indexOf(best.s))best=r}SC[k]={s:best?best.s:'na',per}}
  const pg=document.getElementById('scp');if(pg)pg.textContent=i<L.length?'מחשב את ציוני העיצוב… '+i+' / '+L.length:'';if(i<L.length)setTimeout(step,0);else{scDone=true;summary();show()}};step()}
let night=false,zoom=1,tab='city',flt={q:'',lv:'',g:'',d:''};const V=document.getElementById('v');
const LL={ok:'במשחק ועובד',part:'במשחק חלקית',drawn:'מצויר ולא במשחק',pkg:'רק בחבילה'},RG={city:'העיר',airport:'השדה',island:'האי',port:'הנמל'};
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
const io=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){io.unobserve(e.target);paint(e.target)}},{rootMargin:'400px'});
function size(f){const world=f.units==='world_canvas_units'||f.measured!==undefined||(f.w<300&&f.h<300);let sc=world?3*zoom:Math.min(300*zoom/f.w,200*zoom/f.h);let w=f.w*sc,h=f.h*sc,cut=false;if(w>620){const k=620/w;w*=k;h*=k;cut=true}return{w,h,cut,world}}
function paint(card){for(const c of card.querySelectorAll('canvas[data-f]')){const g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);try{window[c.dataset.api].draw(g,c.dataset.id,c.dataset.f,0,0,c.width,c.height,{night})}catch(e){(window.__FAIL=window.__FAIL||[]).push(c.dataset.id+':'+c.dataset.f+':'+String(e.message||e).slice(0,80));g.fillStyle='#552';g.fillRect(0,0,c.width,c.height)}}}
function card(api,id,title,sub,lv,formats,skip){const d=document.createElement('div');d.className='card';let h='<h3>'+esc(title)+'</h3><div class="id">'+esc(sub)+'</div><span class="b '+lv[0]+'">'+LL[lv[0]]+'</span> '+dsB(api,id)+'<div class="miss">'+esc(lv[1])+'</div>';
 for(const k in formats){const f=formats[k],z=size(f),sk=skip&&skip(k,f),pr=SC[api+'|'+id]&&SC[api+'|'+id].per[k];h+='<div class="fm"><small>'+esc(f.label||k)+' · '+(+f.w).toFixed(f.w%1?1:0)+'×'+(+f.h).toFixed(f.h%1?1:0)+(z.world?' יחידות':'')+(z.cut?' (מוקטן)':'')+(f.text&&f.text!==title?' · '+esc(f.text):'')+(pr?' · <span class="ds '+pr.s+'">'+DS[pr.s]+'</span> ('+pr.ops+' פעולות, '+pr.cols+' צבעים'+(pr.curves?', '+pr.curves+' עקומות':'')+(pr.logo?', לוגו':'')+(pr.text?', טקסט':'')+')':'')+'</small>'+(sk?'<small>— '+esc(sk)+'</small>':'<canvas data-api="'+api+'" data-id="'+esc(id)+'" data-f="'+esc(k)+'" width="'+Math.max(2,Math.round(z.w*2))+'" height="'+Math.max(2,Math.round(z.h*2))+'" style="width:'+Math.max(1,Math.round(z.w))+'px;height:'+Math.max(1,Math.round(z.h))+'px"></canvas>')+'</div>'}
 d.innerHTML=h;io.observe(d);return d}
function dsB(api,id){const r=SC[api+'|'+id];return r?'<span class="b ds '+r.s+'">'+DS[r.s]+'</span>':''}
function grid(list){const g=document.createElement('div');g.className='grid';for(const x of list)g.append(x);return g}
function filters(groups){const f=document.createElement('div');f.className='f';f.innerHTML='<input id="q" placeholder="חיפוש: שם או מזהה" value="'+esc(flt.q)+'">'+['','ok','part','drawn','pkg'].map(s=>'<button data-s="'+s+'" class="'+(flt.lv===s?'on':'')+'">'+(s?LL[s]:'הכול')+'</button>').join('')+'<span class="muted"> · עיצוב:</span>'+['','full','mid','simple','na'].map(s=>'<button data-d="'+s+'" class="'+(flt.d===s?'on':'')+'">'+(s?DS[s]:'הכול')+'</button>').join('')+(groups&&groups.length>1?'<select id="gr"><option value="">כל הקבוצות</option>'+groups.map(g=>'<option'+(flt.g===g?' selected':'')+'>'+esc(g)+'</option>').join('')+'</select>':'');
 f.querySelector('#q').oninput=e=>{flt.q=e.target.value;clearTimeout(f.t);f.t=setTimeout(show,300)};for(const b of f.querySelectorAll('button[data-s]'))b.onclick=()=>{flt.lv=b.dataset.s;show()};for(const b of f.querySelectorAll('button[data-d]'))b.onclick=()=>{flt.d=b.dataset.d;show()};const gs=f.querySelector('#gr');if(gs)gs.onchange=()=>{flt.g=gs.value;show()};return f}
const okD=(api,id)=>!flt.d||(SC[api+'|'+id]&&SC[api+'|'+id].s===flt.d);
const ok=(lv,txt,g)=>(!flt.lv||flt.lv===lv)&&(!flt.q||txt.toLowerCase().includes(flt.q.toLowerCase()))&&(!flt.g||!g||flt.g===g);
const GRP={frontages:'חזיתות',amenities:'שירותים ומתקנים',transport:'תחבורה',addresses:'כתובות',logos:'לוגואים',proposals:'הצעות'};
function items(rg){const out=[];for(const m of CITY){const lv=LV[m.id];if(lv[2]!==rg)continue;out.push({api:'TC_CITY',id:m.id,t:m.name,sub:(m.placeId||'')+(m.brandName&&m.brandName!==m.name?' · '+m.brandName:''),lv,fm:m.formats,g:GRP[m.group]||m.group,skip:(k,f)=>f.kind==='poster'?'פוסטר אירוע — בלשונית הפוסטרים':''})}
 if(rg==='airport'){for(const m of ALG)out.push({api:'TC_AIRPORT_LOGOS',id:m.id,t:m.name,sub:m.id+' · לוגו',lv:LV['logo:'+m.id],fm:m.formats,g:'לוגואים של השדה'});
  for(const m of AIRC)out.push({api:'TC_AIRPORT',id:m.id,t:m.name,sub:m.id+' · '+(m.sourceIds||[]).join(', '),lv:LV['air:'+m.id],fm:m.formats,g:'שלטים ומודעות של השדה',skip:(k,f)=>k==='sign'?'':'מודעה '+f.w+'×'+f.h+' — רק בחבילה (הציור 12 מ״ב, לא בדף)'});
  for(const m of OPS)out.push({api:'TC_AIRPORT_OPS',id:m.id,t:m.sourceText||m.name,sub:m.id+' · '+m.family,lv:LV['ops:'+m.id],fm:m.formats,g:'שילוט תפעולי: '+m.family,dyn:!!m.dynamic||/fids|gate_screen|briefing/.test(m.family)})}
 return out}
function summary(){const c={};for(const rg in RG){c[rg]={ok:0,part:0,drawn:0,pkg:0,n:0,full:0,mid:0,simple:0,na:0};for(const x of items(rg)){c[rg][x.lv[0]]++;c[rg].n++;const r=SC[x.api+'|'+x.id];if(r)c[rg][r.s]++}}
 document.getElementById('sum').innerHTML=Object.keys(RG).map(r=>'<div><b>'+c[r].n+'</b>'+RG[r]+': <span style="color:var(--ok)">'+c[r].ok+'</span> · <span style="color:var(--part)">'+c[r].part+'</span> · <span style="color:var(--drawn)">'+c[r].drawn+'</span> · <span style="color:var(--pkg)">'+c[r].pkg+'</span>'+(scDone?'<br><small>עיצוב: מלא '+c[r].full+' · בינוני '+c[r].mid+' · פשוט '+c[r].simple+(c[r].na?' · לא נמדד '+c[r].na:'')+'</small>':'')+'</div>').join('')+'<div><b>62</b>זהויות · 210 ציורים</div><div><b>'+AL.airlines.length+'</b>חברות תעופה — שמות חדשים</div>'}
function show(){V.innerHTML='';const keep=document.activeElement&&document.activeElement.id==='q';
 if(RG[tab]){const all=items(tab);V.append(filters([...new Set(all.map(x=>x.g))]));const L=all.filter(x=>ok(x.lv[0],x.t+' '+x.id+' '+x.sub,x.g)&&okD(x.api,x.id));V.insertAdjacentHTML('beforeend','<p class="muted">'+RG[tab]+' — '+L.length+' פריטים. בכל כרטיס: הזהות של המקום (לוגו, 900×600) וכל שלט שלו בגודל האמיתי. "מידה מוצעת" (120×24) — מקום שאין לו היום משטח שלט במשחק.</p>');V.append(grid(L.map(x=>card(x.api,x.id,x.t,x.sub,x.lv,x.fm,x.skip))))}
 else if(tab==='al'){V.innerHTML='<h2>חברות התעופה — שמות חדשים באנגלית (הצעה, לאישורך)</h2><p class="muted">'+esc(AL._)+' בעמודה הראשונה — הלוגו של החבילה לשם של היום; לכל שם שיאושר — לוגו חדש מהבעלים. הקובץ: airlines_proposal.json.</p>';
  const t=document.createElement('div');t.className='tw';let h='<table><thead><tr><th>הלוגו היום</th><th>השם היום</th><th>שם חדש מוצע</th><th>חלופות</th><th>קוד</th><th>צבעים</th><th>סגנון</th><th>תפקיד</th><th>מטוסים</th><th>יעדים</th></tr></thead><tbody>';
  const id={'Aurelia Air':'aurelia','Sunbeak':'sunbeak','Zebrano':'zebrano','Coral Coast':'coral','Tidewind Air':'tidewind','Mirage Jet':'mirage','Confetti Air':'confetti','Skyline Regional':'skyline'};
  for(const a of AL.airlines)h+='<tr><td>'+(id[a.now]?'<canvas class="alc" data-id="'+id[a.now]+'" width="180" height="120" style="width:90px;height:60px;background:#0c2226;border-radius:3px"></canvas>':'—')+'</td><td>'+esc(a.now)+'<br><span class="muted">'+esc(a.nowHe)+'</span></td><td><b>'+esc(a.name)+'</b></td><td>'+a.alt.map(esc).join('<br>')+'</td><td>'+esc(a.code)+'</td><td>'+Object.values(a.colors).map(c=>'<span class="sw" style="background:'+c+'"></span>').join('')+'</td><td>'+esc(a.style)+'</td><td>'+esc(a.role)+'</td><td>'+a.aircraft.map(esc).join('<br>')+'</td><td>'+a.routes.map(esc).join(' · ')+'</td></tr>';
  t.innerHTML=h+'</tbody></table>';V.append(t);V.insertAdjacentHTML('beforeend','<p class="muted">'+AL.notes.map(esc).join(' · ')+'</p>');
  for(const c of V.querySelectorAll('canvas.alc')){try{TC_AIRPORT_LOGOS.draw(c.getContext('2d'),c.dataset.id,'logo',0,0,c.width,c.height,{night})}catch(e){(window.__FAIL=window.__FAIL||[]).push('al:'+e.message)}}}
 else if(tab==='lib'){V.append(filters());V.insertAdjacentHTML('beforeend','<p class="muted">62 הזהויות של הספרייה (index.json): הלוגו מצויר (מטבלת המותגים של המשחק); לכל פורמט — הרמה שלו. הפוסטר / גב / דופן / עטיפה של סטים 1–5 — במשחק (האוטובוסים והסככות); של סטים 6–7 — רק בחבילה.</p>');
  V.append(grid(LIBT.filter(b=>okD('BRANDAPI',b.key)&&ok(Object.values(b.fm).some(f=>f[2]==='pkg')?'part':'ok',b.name+' '+b.key+' '+b.places.join(' '))).map(b=>{const lv=[Object.values(b.fm).some(f=>f[2]==='pkg')?'part':'ok',Object.entries(b.fm).map(([k,f])=>({logo:'לוגו',poster:'פוסטר',rear:'גב',side:'דופן',wrap:'עטיפה'})[k]+' '+f[0]+'×'+f[1]+': '+f[3]).join(' · ')];
   const d=card('BRANDAPI',b.key,b.name,b.key+' · סט '+b.set+' · '+b.cat+' · '+b.n+' מקומות',lv,{logo:{w:b.fm.logo[0],h:b.fm.logo[1],label:'לוגו'}});d.insertAdjacentHTML('beforeend','<small class="muted">'+esc(b.places.slice(0,8).join(' · '))+(b.n>8?' …':'')+'</small>');return d})))}
 else if(tab==='post'){V.innerHTML='<h2>פוסטרי האירועים (posters)</h2><p class="muted">הפוסטרים של החבילה (סט 11) — במשחק ועובדים (074n3s_posters_set11, הציור של המעצב כמו שהוא). כאן — הרשימה; הציור המלא בדף הפוסטרים של החבילה (1.3 מ״ב קוד).</p>'+'<div class="grid">'+POST.map(p=>'<div class="card"><h3>'+esc(p[1])+'</h3><div class="id">'+esc(p[0])+'</div><span class="b ok">'+LL.ok+'</span></div>').join('')+'</div>'}
 if(keep){const q=document.getElementById('q');if(q){q.focus();q.setSelectionRange(q.value.length,q.value.length)}}}
for(const b of document.querySelectorAll('#tabs button[data-t]'))b.onclick=()=>{tab=b.dataset.t;flt={q:'',lv:'',g:'',d:''};for(const x of document.querySelectorAll('#tabs button[data-t]'))x.classList.toggle('on',x===b);show()};
document.getElementById('nt').onclick=()=>{night=!night;show()};document.getElementById('zm').onclick=e=>{zoom=zoom===1?2:1;e.target.textContent=zoom===1?'הגדלה':'גודל רגיל';show()};summary();show();scoreAll();
</script></body></html>'''

for a, b in [('nfkiss', 'nf-filter'), ('address_panel', 'housenum_panel'), ('"addresses"', '"housenums"'), ('addresses:', 'housenums:'), ('KISS', 'DROP'), ('Kiss', 'Drop'), ('kiss', 'drop'), ('C2-WINE', 'C2-CELLAR')]: H = H.replace(a, b)
H = re.sub(r'(?m)^\s*//[^\n]*\n', '', H)
open(OUT, 'w', encoding='utf-8').write(H)
print('review:', OUT, len(H.encode()), 'בתים · עיר', cnt, '· שלטים', nf)
