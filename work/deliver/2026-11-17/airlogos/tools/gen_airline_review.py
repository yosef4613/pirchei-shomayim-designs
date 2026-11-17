#!/usr/bin/env python3
# gen_airline_review.py — airlogos 17.11 (הבעלים 17:25: "היה חסר בדף הזה את הלוגואים של חברות התעופה"): דף נפרד לחברות התעופה —
#  (1) 12 החברות של המשחק: השם, הקוד, הצבעים (LIV של 013, שני הווריאנטים), והסמל כמו שהוא מצויר במשחק — על הזנב מלמעלה וב-3/4,
#  בלוח הצ׳ק-אין, מעל מסך השער ובלוח הטיסות; והלוגו של המעצב (900×600); (2) 12 השמות החדשים (airlines_proposal.json); (3) "טוב — לשמור" /
#  "צריך מחדש" + הערה לכל חברה ופורמט, ב-localStorage, וכפתור "העתק רשימה" בפורמט של owner_marks_1117.json. קוד בלבד, בלי תמונות.
# usage: python3 gen_airline_review.py <src_game parts> <share> <airlines_proposal.json> <out.html>
import sys, json, re
PARTS, SH, AL, OUT = sys.argv[1:5]
c13 = open(PARTS + '/013_C3.js', encoding='utf-8').read()
i = c13.index('const AL=(n,w,k,v)=>'); j = c13.index('window.__A34LIV=', i); LIVSRC = c13[i:j]
MKHE = re.search(r'const MK_HE=(\{[^}]*\});', c13).group(1)
k74 = open(PARTS + '/074k_S15c_ground.js', encoding='utf-8').read(); GRAL = re.search(r'const S15GR_AL=(\{[^;]*\});', k74).group(1)
part = open(PARTS + '/074v_airlogos.js', encoding='utf-8').read()
ROWS = part[part.index('const TCAL_ROWS=') + 16: part.index(';\nconst TCAL_BY')]
DRAW = part[part.index('const TCAL_D=(function(){const logo=tcalLogo;') + 45: part.index('return{sign,emblem}})();')]
LR = open(SH + '/airport-ops/logos/logo_renderer.js', encoding='utf-8').read().replace('</script', '<\\/script')
s = open(SH + '/airport-ops/logos/logo_catalog.js', encoding='utf-8').read(); LC = json.loads(s[s.index('['):s.rindex(']') + 1])
LC = [m for m in LC if m.get('group') == 'airlines']
AP = json.load(open(AL, encoding='utf-8'))
def js(v): return json.dumps(v, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
H = r'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>לוגואי חברות התעופה</title><style>
:root{--bg:#f4f1ea;--fg:#1c2628;--muted:#5b6869;--card:#fff;--line:#d9d4c8;--keep:#1e7a46;--redo:#b3402e;--acc:#2a6fc4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d;--keep:#4cc483;--redo:#f07a68;--acc:#6aa8f0}}
:root[data-theme="dark"]{--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d;--keep:#4cc483;--redo:#f07a68;--acc:#6aa8f0}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Arial,"Noto Sans Hebrew",sans-serif}main{max-width:1280px;margin:auto;padding:16px}
h1{font-size:26px;margin:.3em 0}h2{font-size:21px;margin:1.4em 0 .5em}h3{font-size:18px;margin:0}.muted{color:var(--muted)}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}button{font:inherit;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}
.co{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;margin:12px 0}.hd{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline}.hd .code{font-weight:700;color:var(--acc)}
.sw{display:inline-block;width:18px;height:18px;border-radius:4px;border:1px solid var(--line);vertical-align:middle;margin-left:3px}
.fs{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}.f{border:1px solid var(--line);border-radius:10px;padding:8px;min-width:200px;max-width:100%}
.f small{display:block;color:var(--muted);font-size:12px;max-width:360px}.f canvas{display:block;max-width:100%;margin:6px 0;border-radius:3px}
.mk{display:flex;gap:6px}.mk button{font-size:14px;padding:3px 10px}.mk button.on.keep{background:var(--keep);color:#fff;border-color:var(--keep)}.mk button.on.redo{background:var(--redo);color:#fff;border-color:var(--redo)}
textarea{font:inherit;width:100%;box-sizing:border-box;min-height:44px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--fg);padding:6px;margin-top:8px}
#out{min-height:140px;font:13px/1.4 monospace;direction:ltr;text-align:left}
</style></head><body><main>
<h1>לוגואי חברות התעופה — מה יש היום במשחק, ומה מוצע</h1>
<p>כל חברות התעופה של המשחק, והסמל של כל אחת בכל מקום שבו הוא מופיע במשחק: על הזנב מלמעלה וב-3/4, בלוח הצ׳ק-אין, מעל מסך השער ובלוח הטיסות. בנוסף — הלוגו המלא של המעצב (900×600), ו-12 השמות החדשים באנגלית שהוצעו. הכול מצויר בקוד, בלי תמונות. <b>הגודל אמיתי, ביחס לשאר המשחק</b>: 3 פיקסלים לכל יחידת עולם. הלוגו של המעצב מוצג מוקטן.</p>
<p class="muted">הצ׳ק-אין ומסך השער מצוירים באותו קוד ציור של המשחק (074v_airlogos). בזנב — אותו סמל, באותם צבעים ובאותו גודל כמו במשחק (יחידת עולם = 10 ס״מ), אבל צורת המטוס מפושטת: רואים רק את החלק האחורי. ב-3/4 מופיע גם הכיתוב העברי שעל גוף המטוס. בלוח הטיסות — רק הקוד, בלי סמל, כמו במשחק. ליד כל פורמט: "טוב — לשמור" / "צריך מחדש", ולכל חברה — הערה. הסימונים נשמרים בדפדפן. בתחתית — "העתק רשימה".</p>
<div class="bar"><button id="zm">הגדלה פי 2</button><button id="nt">יום / לילה</button><span class="muted" id="cnt"></span></div>
<h2>(1) חברות התעופה שיש היום במשחק</h2><section id="now"></section>
<h2>(2) שמות חדשים באנגלית — הצעה (לאישורך)</h2><p class="muted">לכל שם: קוד, צבעים מוצעים ותפקיד. הסמל בשלט הוא הסמל הנוכחי של אותה חברה, רק עם השם החדש — זמני, עד שתעצב לוגו חדש. שום דבר מזה לא נכנס למשחק לפני אישור.</p><section id="new"></section>
<h2>(3) הרשימה</h2><p class="muted">אותו פורמט כמו owner_marks_1117.json (version / source / updatedAt / reviews). המפתחות: airline:&lt;מזהה&gt; לחברות של היום, airline-new:&lt;קוד&gt; לשמות החדשים.</p>
<div class="bar"><button id="cp">העתק רשימה</button><button id="clr">ניקוי הסימונים</button><span id="cpm" class="muted"></span></div><textarea id="out" readonly></textarea>
</main>
<script>
const TCAL_ROWS=''' + ROWS + ''';
const MK_HE=''' + MKHE + ''';
const S15GR_AL=''' + GRAL + ''';
const AP=''' + js(AP) + ''';
''' + LIVSRC + '''
window.TC_AIRPORT_LOGO_CATALOG=''' + js(LC) + ''';
/* הסמל של נמל התעופה / ההשכרה — לא נדרש בדף הזה (רק חברות תעופה) */
function tcalLogo(){return false}
const TCAL_D=(function(){const logo=tcalLogo;
''' + DRAW + '''
return{sign,emblem}})();
</script>
<script>''' + LR + '''</script>
<script>
const ID={'Aurelia Air':'aurelia','Sunbeak':'sunbeak','Zebrano':'zebrano','Coral Coast':'coral','Tidewind Air':'tidewind','Mirage Jet':'mirage','Confetti Air':'confetti','Skyline Regional':'skyline','Crateway Cargo':'crateway','Boxline Cargo':'boxline','Swiftpak':'swiftpak','Pelicarga':'pelicarga'};
const ROW={};for(const r of TCAL_ROWS)ROW[r[0]]={id:r[0],name:r[1],group:r[2],color:r[3],ink:r[4],signType:r[5],w:r[6],h:r[7]};
const CUR=[];for(const g of ['pax','cargo']){const seen=new Set();for(const q of LIV[g]){if(seen.has(q.n))continue;seen.add(q.n);CUR.push({n:q.n,g,vars:LIV[g].filter(v=>v.n===q.n)})}}
let zoom=1,night=false;const K='tc_airline_marks_1117';let ST={};try{ST=JSON.parse(localStorage.getItem(K)||'{}')||{}}catch(e){ST={}}
function save(){try{localStorage.setItem(K,JSON.stringify(ST))}catch(e){}out()}
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
function cv(w,h){const c=document.createElement('canvas'),d=2;c.width=Math.round(w*3*zoom*d);c.height=Math.round(h*3*zoom*d);c.style.width=Math.round(w*3*zoom)+'px';const g=c.getContext('2d');g.scale(3*zoom*d,3*zoom*d);return[c,g]}
/* מלמעלה: החלק האחורי של מטוס צר-גוף (AC-NB-01: אורך 37.6 מ׳, רוחב הגוף 4 מ׳), בצבעי LIV; הסמל — 013:logo(c,lv,-L*.42,0,hw*.75) = 15 יחידות */
function tailTop(lv,emb){const W=150,H=70,[c,g]=cv(W,H),hw=20,L=376,xs=-L*.25;g.translate(8,H/2);g.fillStyle=night?'#2b3438':'#8a949a';g.fillRect(-8,-H/2,W,H);
 const X=x=>x-(-L*.5)*1;g.fillStyle=lv.b;g.beginPath();g.moveTo(X(-L*.5),0);g.quadraticCurveTo(X(-L*.5)+10,-hw,X(-L*.5)+40,-hw);g.lineTo(W,-hw);g.lineTo(W,hw);g.lineTo(X(-L*.5)+40,hw);g.quadraticCurveTo(X(-L*.5)+10,hw,X(-L*.5),0);g.fill();
 g.fillStyle=lv.t;g.beginPath();g.moveTo(X(-L*.5),0);g.quadraticCurveTo(X(-L*.5)+10,-hw,X(-L*.5)+40,-hw);g.lineTo(X(-L*.5)+64,-hw);g.lineTo(X(-L*.5)+64,hw);g.lineTo(X(-L*.5)+40,hw);g.quadraticCurveTo(X(-L*.5)+10,hw,X(-L*.5),0);g.fill();
 g.fillStyle=lv.t;g.beginPath();g.moveTo(X(-L*.5)+6,-hw*.6);g.lineTo(X(-L*.5)+4,-hw*2.6);g.lineTo(X(-L*.5)+20,-hw*2.6);g.lineTo(X(-L*.5)+36,-hw*.8);g.closePath();g.moveTo(X(-L*.5)+6,hw*.6);g.lineTo(X(-L*.5)+4,hw*2.6);g.lineTo(X(-L*.5)+20,hw*2.6);g.lineTo(X(-L*.5)+36,hw*.8);g.closePath();g.fill();
 if(lv.s){g.fillStyle=lv.s;g.fillRect(X(-L*.5)+64,hw*.5,W,hw*.24);g.fillRect(X(-L*.5)+64,-hw*.74,W,hw*.24)}
 const x=X(-L*.42),s=hw*.75;emb(g,x,0,s);return c}
/* 3/4: הזנב האנכי + גב הגוף; הסמל (068: decor.mark, size R*.75 = 15 יחידות) על חלק הזנב, והכיתוב העברי על הגוף */
function tail34(lv,emb,he){const W=150,H=80,[c,g]=cv(W,H);g.fillStyle=night?'#2b3438':'#8a949a';g.fillRect(0,0,W,H);const y0=56;
 g.fillStyle=lv.u||lv.b;g.fillRect(0,y0,W,16);g.fillStyle=lv.b;g.beginPath();g.ellipse(W*.55,y0,W*.55,10,0,Math.PI,0);g.fill();g.fillRect(0,y0-2,W,6);
 g.fillStyle=lv.t;g.beginPath();g.moveTo(14,y0-6);g.lineTo(2,6);g.lineTo(22,6);g.lineTo(54,y0-8);g.closePath();g.fill();g.fillRect(0,y0-10,48,12);
 if(lv.s){g.fillStyle=lv.s;g.fillRect(48,y0+4,W,3)}emb(g,26,y0-6,15);
 if(he){g.save();g.font='800 6.6px Arial,"Noto Sans Hebrew",sans-serif';g.textAlign='center';g.textBaseline='middle';g.direction='rtl';g.fillStyle=lv.s||'#1d2730';g.fillText(he,W*.68,y0-4);g.restore()}return c}
function embFn(id,col){return(g,x,y,s)=>{if(!id)return;const z=s*1.12;TCAL_D.emblem(g,'airline',x-z/2,y-z/2,z,col,{id})}}
function oldMark(lv){return(g,x,y,s)=>{g.save();g.translate(x,y);g.fillStyle=lv.m;g.beginPath();g.arc(0,0,s*.32,0,7);g.fill();g.restore()}}
function signC(id,name,col,ink){const r=ROW[id]||{id,name,group:'airlines',color:col,ink:ink||'#fff',signType:'airline'};const m=Object.assign({},r,{signText:name});if(col)m.color=col;if(ink)m.ink=ink;const [c,g]=cv(28,6);TCAL_D.sign(g,m,28,6,night);return c}
function gateC(id,name,code){const [c,g]=cv(48,24);g.fillStyle=night?'#2b3438':'#c9cdd0';g.fillRect(0,0,48,24);if(id&&ROW[id]){g.save();g.translate(10,1);const m=Object.assign({},ROW[id],{signText:name});TCAL_D.sign(g,m,28,6,night);g.restore()}
 g.fillStyle='#10161e';g.strokeStyle='#5e6b78';g.lineWidth=1;g.fillRect(2,7.6,44,14);g.strokeRect(2,7.6,44,14);g.textAlign='center';g.textBaseline='middle';g.fillStyle='#ffd25a';g.font='bold 4.6px sans-serif';g.fillText('שער P2 · '+code+' 213',24,11.6);g.fillStyle='#f2f4f7';g.font='4.2px sans-serif';g.fillText('פריז 08:30',24,16.2);g.fillStyle='#4cc483';g.fillText('בזמן',24,20.2);return c}
function fidsC(code){const [c,g]=cv(100,12);g.fillStyle='#10161e';g.fillRect(0,0,100,12);g.textBaseline='middle';g.font='bold 6px sans-serif';g.textAlign='right';g.fillStyle='#f2f4f7';g.fillText('08:30',97,6);g.fillText(code+' 213',80,6);g.font='6px sans-serif';g.fillStyle='#cfd6de';g.fillText('פריז',57,6);g.textAlign='center';g.fillStyle='#f2f4f7';g.fillText('P2',38,6);g.textAlign='left';g.fillStyle='#4cc483';g.font='bold 5px sans-serif';g.fillText('בזמן',3,6);return c}
function logoC(id){const c=document.createElement('canvas');c.width=360;c.height=240;c.style.width=180*zoom+'px';try{TC_AIRPORT_LOGOS.draw(c.getContext('2d'),id,'logo',0,0,360,240,{night})}catch(e){}return c}
function mk(key,part){const r=ST[key]&&ST[key].parts&&ST[key].parts[part];const d=document.createElement('div');d.className='mk';for(const [v,t] of [['keep','טוב — לשמור'],['redo','צריך מחדש']]){const b=document.createElement('button');b.className=v+(r===v?' on':'');b.textContent=t;b.onclick=()=>{ST[key]=ST[key]||{parts:{},note:''};if(ST[key].parts[part]===v)delete ST[key].parts[part];else ST[key].parts[part]=v;save();render()};d.append(b)}return d}
function fmt(key,part,title,canvas,note){const f=document.createElement('div');f.className='f';f.innerHTML='<small><b>'+esc(title)+'</b></small>';if(canvas)f.append(canvas);if(note)f.insertAdjacentHTML('beforeend','<small>'+esc(note)+'</small>');f.append(mk(key,part));return f}
function noteBox(key){const t=document.createElement('textarea');t.placeholder='הערה לחברה הזאת';t.value=(ST[key]&&ST[key].note)||'';t.oninput=()=>{ST[key]=ST[key]||{parts:{},note:''};ST[key].note=t.value;save()};return t}
function render(){const N=document.getElementById('now');N.innerHTML='';
 for(const a of CUR){const id=ID[a.n],key='airline:'+id,lv=a.vars[0],he=MK_HE[a.n]||'',code=(S15GR_AL[a.n]||[])[1]||'—',has=!!ROW[id];const co=document.createElement('div');co.className='co';
  co.innerHTML='<div class="hd"><h3>'+esc(a.n)+'</h3><span class="muted">'+esc(he)+'</span><span class="code">'+esc(code)+'</span><span class="muted">'+(a.g==='cargo'?'מטען':'נוסעים')+' · סגנון '+esc(lv.w)+' · '+a.vars.length+' וריאנטים: </span>'+a.vars.map(v=>[v.b,v.s,v.t,v.m].map(c=>'<span class="sw" style="background:'+c+'" title="'+c+'"></span>').join('')).join(' &nbsp;·&nbsp; ')+'</div>';
  const fs=document.createElement('div');fs.className='fs';const emb=has?embFn(id,lv.m):oldMark(lv);
  fs.append(fmt(key,'tail-top','על הזנב — מלמעלה',tailTop(lv,emb),has?'הסמל של החבילה, בצבע הסמל של החברה (15 יחידות)':'אין סמל בחבילה — הסימן הישן'));
  fs.append(fmt(key,'tail-34','על הזנב — 3/4',tail34(lv,emb,he),'עם הכיתוב העברי שעל הגוף, כמו במשחק'));
  if(has){fs.append(fmt(key,'checkin','לוח הצ׳ק-אין (28×6)',signC(id,a.n),'airlogos — בענף'));fs.append(fmt(key,'gate','מעל מסך השער (28×6 מעל 44×14)',gateC(id,a.n,code)))}
  fs.append(fmt(key,'fids','לוח הטיסות — שורה',fidsC(code==='—'?'XX':code),'רק הקוד — בלי סמל'));
  if(TC_AIRPORT_LOGO_CATALOG.some(m=>m.id===id))fs.append(fmt(key,'logo','הלוגו של המעצב (900×600, מוקטן)',logoC(id),'airport-ops/logos — לא במשחק'));
  co.append(fs,noteBox(key));N.append(co)}
 const W=document.getElementById('new');W.innerHTML='';
 for(const a of AP.airlines){const key='airline-new:'+a.code,cur=CUR.find(x=>x.n===a.now),id=ID[a.now],lv=Object.assign({},cur?cur.vars[0]:{},{b:a.colors.base,s:a.colors.main,t:a.colors.main,m:a.colors.accent});const co=document.createElement('div');co.className='co';
  co.innerHTML='<div class="hd"><h3>'+esc(a.name)+'</h3><span class="code">'+esc(a.code)+'</span><span class="muted">במקום '+esc(a.now)+' · חלופות: '+a.alt.map(esc).join(' / ')+'</span>'+Object.values(a.colors).map(c=>'<span class="sw" style="background:'+c+'"></span>').join('')+'</div><p class="muted" style="margin:.3em 0">'+esc(a.role)+' · '+esc(a.style)+' · '+a.aircraft.map(esc).join(', ')+' · '+a.routes.map(esc).join(' · ')+'</p>';
  const fs=document.createElement('div');fs.className='fs';const emb=ROW[id]?embFn(id,a.colors.accent):oldMark(lv);
  fs.append(fmt(key,'name','השם והקוד',null,a.name+' · '+a.code));
  fs.append(fmt(key,'colors','הצבעים על הזנב — מלמעלה',tailTop(lv,emb),'סמל זמני'));
  fs.append(fmt(key,'emblem','השלט עם השם החדש (28×6)',signC(id&&ROW[id]?id:'aurelia',a.name,a.colors.main,'#fff6e6'),'סמל זמני — הלוגו יעוצב'));
  co.append(fs,noteBox(key));W.append(co)}
 out()}
function payload(){const r={};for(const k in ST){const v=ST[k];if(v&&(Object.keys(v.parts||{}).length||v.note))r[k]={parts:v.parts||{},note:v.note||''}}return{version:1,source:'Airline logos review · airlogos · S7F302',updatedAt:Date.now(),reviews:r}}
function out(){const p=payload(),o=document.getElementById('out');o.value=JSON.stringify(p,null,1);let k=0,r=0;for(const x of Object.values(p.reviews))for(const v of Object.values(x.parts))v==='keep'?k++:r++;document.getElementById('cnt').textContent='מסומנים: '+k+' לשמור · '+r+' מחדש'}
document.getElementById('cp').onclick=()=>{const o=document.getElementById('out'),m=document.getElementById('cpm');out();const t=o.value;
 const fb=()=>{try{o.focus();o.select();o.setSelectionRange(0,t.length);const ok=document.execCommand&&document.execCommand('copy');m.textContent=ok?'הועתק':'הטקסט מסומן — העתק ידנית (Ctrl+C)'}catch(e){m.textContent='הטקסט מסומן — העתק ידנית (Ctrl+C)'}};
 try{if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(()=>{m.textContent='הועתק'},fb);else fb()}catch(e){fb()}};
document.getElementById('clr').onclick=()=>{ST={};save();render()};
document.getElementById('zm').onclick=e=>{zoom=zoom===1?2:1;e.target.textContent=zoom===1?'הגדלה פי 2':'גודל אמיתי';render()};
document.getElementById('nt').onclick=()=>{night=!night;render()};render();
</script></body></html>'''
open(OUT, 'w', encoding='utf-8').write(H)
print('airline review:', OUT, len(H.encode()), 'בתים ·', len(LC), 'לוגואים של המעצב')
