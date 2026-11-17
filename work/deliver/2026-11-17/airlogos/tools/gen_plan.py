#!/usr/bin/env python3
# gen_plan.py — airlogos 17.11: הציור (כלל 13) — דף נקי: מפה סכמטית ב-SVG של כל משטחי השילוט בשדה + גלריה של השלטים החדשים בקנבס,
#  באותו קוד ציור של החלק במשחק (parts/074v_airlogos.js). הלוגו של נמל התעופה / ההשכרה מצויר כאן כסימן פשוט (בדף אין את טבלת המותגים).
import sys, json, re, html
SH, PART, OUT = sys.argv[1:4]
inv = json.load(open(SH + '/airport/sign_inventory.json', encoding='utf-8'))
part = open(PART, encoding='utf-8').read()
rows = part[part.index('const TCAL_ROWS=') + 16: part.index(';\nconst TCAL_BY')]
draw = part[part.index('const TCAL_D=(function(){const logo=tcalLogo;') + 45: part.index('return{sign,emblem}})();')]
SHOP = {'קפה הטרמינל','קפה השער','מיצים','פיצה','שווארמה','סלטים','מאפה וקפה','דיוטי פרי','ספרים ועיתונים','צעצועים','בית מרקחת','מתנות','אלקטרוניקה'}
BAND = {'האנגר א׳','האנגר ב׳','האנגר ג׳','חוות הדלק','סדנת רכבי השירות','אגף השערים P1–P6','כבאות והצלה — השדה','משטרה · מד״א','שער המטען','שער עובדים','מודיעין'}
NEW = {'S15J-AIR','S15-PLATE-TERMINAL-E','S15-PLATE-TERMINAL-W','S16-HOTEL-SIGN','S16-RENT-KIOSK-SIGN'}
def kind(r):
    t = r.get('text') or ''
    if r['family'] == 'checkin_airline' or r['id'] in NEW or (r['family'] == 'terminal_hanging' and t in SHOP): return 'new'
    if t in BAND and r['family'] != 'terminal_hanging': return 'band'
    if r['family'] in ('operational_e4_plate', 'bridge_gate_screen'): return 'tile'
    return 'keep'
pts = []
for r in inv['instances']:
    a = r.get('anchor')
    if not a: continue
    pts.append({'id': r['id'], 't': r.get('text') or '', 'x': a[0], 'y': a[1], 'k': kind(r), 'f': r['family'], 'w': (r.get('face') or {}).get('w'), 'h': (r.get('face') or {}).get('h')})
pts.append({'id': 'APT-TOWER', 't': 'המגדל — לוח זהות חדש', 'x': 7980, 'y': 830, 'k': 'new', 'f': 'tower', 'w': 23, 'h': 22})
cnt = {k: sum(1 for p in pts if p['k'] == k) for k in ('new', 'band', 'tile', 'keep')}
X0, Y0, X1, Y1 = 4800, -560, 9700, 1800; SC = 0.2
def sx(x): return (x - X0) * SC
def sy(y): return (y - Y0) * SC
COL = {'new': '#d4572a', 'band': '#2a7fd4', 'tile': '#8a4fc0', 'keep': '#8a949a'}
svg = [f'<svg viewBox="0 0 {(X1-X0)*SC:.0f} {(Y1-Y0)*SC:.0f}" role="img" aria-label="מפת השילוט בשדה">']
svg.append(f'<rect x="0" y="0" width="{(X1-X0)*SC:.0f}" height="{(Y1-Y0)*SC:.0f}" fill="var(--ground)"/>')
for (x0, y0, x1, y1, lab) in [(4800, -520, 9600, -420, 'המסלול 09-27'), (6000, 1033, 7222, 1180, 'הזרוע המערבית'), (7222, 900, 8400, 1060, 'אגף השערים'), (8400, 1033, 9175, 1220, 'הטרמינל המזרחי'),
                              (8150, 1480, 9000, 1620, 'ההאנגרים'), (4950, 1000, 5300, 1120, 'מלון השדה'), (6150, 1250, 7400, 1700, 'החניונים (S16)')]:
    svg.append(f'<rect x="{sx(x0):.1f}" y="{sy(y0):.1f}" width="{(x1-x0)*SC:.1f}" height="{(y1-y0)*SC:.1f}" fill="var(--bld)" stroke="var(--line)" stroke-width=".6"/>')
    svg.append(f'<text x="{sx((x0+x1)/2):.1f}" y="{sy(y0)-3:.1f}" class="lab">{html.escape(lab)}</text>')
for p in sorted(pts, key=lambda p: ['keep', 'tile', 'band', 'new'].index(p['k'])):
    r = 4.2 if p['k'] != 'keep' else 2.6
    svg.append(f'<circle cx="{sx(p["x"]):.1f}" cy="{sy(p["y"]):.1f}" r="{r}" fill="{COL[p["k"]]}" stroke="var(--bg)" stroke-width=".8"><title>{html.escape(p["id"]+" · "+p["t"])}</title></circle>')
svg.append('</svg>')
trs = ''.join(f'<tr class="{p["k"]}"><td>{html.escape(p["id"])}</td><td>{html.escape(p["t"])}</td><td>{p["w"]}×{p["h"]}</td><td>{ {"new":"העיצוב של החבילה","band":"פס זהות + לוגו מאושר","tile":"הכיתוב בלי שינוי + לוגו (אריח בקצה הלוח / שלט חברת התעופה מעל מסך השער)","keep":"בלי שינוי (מידע תפעולי)"}[p["k"]]}</td></tr>' for p in sorted(pts, key=lambda p: (['new', 'band', 'tile', 'keep'].index(p['k']), p['id'])))
H = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>שילוט השדה</title><style>
:root{{--bg:#f6f3ec;--fg:#1d2a2c;--muted:#5d6a6c;--ground:#e4e9e0;--bld:#cfd6d8;--line:#7d8a8e;--card:#ffffff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#12191b;--fg:#e9eee9;--muted:#9aa6a6;--ground:#1d2a27;--bld:#2c3a3d;--line:#5c6c70;--card:#1a2426}}}}
:root[data-theme="dark"]{{--bg:#12191b;--fg:#e9eee9;--muted:#9aa6a6;--ground:#1d2a27;--bld:#2c3a3d;--line:#5c6c70;--card:#1a2426}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Arial,"Noto Sans Hebrew",sans-serif}}main{{max-width:1180px;margin:auto;padding:16px}}
h1{{font-size:26px;margin:.4em 0}}h2{{font-size:20px;margin:1.4em 0 .5em}}p,li{{color:var(--fg)}}.muted{{color:var(--muted)}}
svg{{width:100%;height:auto;display:block;border-radius:8px}}.lab{{font-size:7px;fill:var(--muted);text-anchor:middle}}
.leg span{{display:inline-block;width:12px;height:12px;border-radius:50%;margin:0 4px -1px 4px}}
.gal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}.card{{background:var(--card);border-radius:8px;padding:10px}}
.card canvas{{width:100%;height:auto;display:block;background:#0c2226;border-radius:4px}}.card b{{display:block;font-size:14px}}.card small{{color:var(--muted)}}
table{{border-collapse:collapse;width:100%;font-size:14px}}td{{border-bottom:1px solid var(--bld);padding:4px 6px}}tr.new td:first-child{{border-right:4px solid {COL["new"]}}}tr.band td:first-child{{border-right:4px solid {COL["band"]}}}tr.tile td:first-child{{border-right:4px solid {COL["tile"]}}}
.tw{{overflow-x:auto}}button{{font:inherit;padding:6px 12px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--fg)}}
</style></head><body><main>
<h1>השילוט והלוגואים של השדה — מחבילת המותגים</h1>
<p>כל משטח שילוט בשדה (המלאי של החבילה — {len(pts)} משטחים, ועוד המגדל). <b>{cnt["new"]}</b> מקבלים את העיצוב של החבילה (חברות התעופה, החנויות והמזנונים, חזיתות הטרמינל, מלון השדה, ההשכרה, המגדל),
<b>{cnt["band"]}</b> מקבלים פס זהות עם הלוגו המאושר (ההאנגרים, חוות הדלק, הסדנה, אגף השערים, הכבאות, המשטרה, שער המטען, שער העובדים, המודיעין),
<b>{cnt["tile"]}</b> שומרים על הכיתוב התפעולי ומקבלים לוגו לידו (11 הלוחות של השערים, החניונים, ההסעה ומסוף הרכבת–אוויר — אריח לוגו בקצה; 6 מסכי השערים — שלט חברת התעופה של הטיסה הבאה מעל המסך),
ו-{cnt["keep"]} נשארים כמו שהם — שלטי הכוונה, לוחות טיסות, מסכי שערים וסימוני מסלול (החבילה: "שומרים על המידע התפעולי").</p>
<p class="leg"><span style="background:{COL["new"]}"></span>העיצוב של החבילה <span style="background:{COL["band"]}"></span>פס זהות + לוגו <span style="background:{COL["tile"]}"></span>כיתוב תפעולי + לוגו <span style="background:{COL["keep"]}"></span>בלי שינוי</p>
{"".join(svg)}
<h2>המטוסים</h2>
<p>הסמל של כל אחת מ-8 חברות הנוסעים (הסמלים של החבילה, בגלריה למטה) — על הזנב של המטוס, מלמעלה וב-3/4, בצבעים של החברה (2 וריאנטים לכל חברה). חברות המטען והתעופה הכללית — הסימן הקיים.</p>
<h2>השלטים החדשים — באותו קוד ציור של המשחק</h2>
<p class="muted">המידות — של המשטח במשחק (יחידות העולם). בדף הזה הלוגו של נמל התעופה ושל ההשכרה מצויר כסימן פשוט; במשחק — הלוגו המאושר מטבלת המותגים. שמות חברות התעופה — באנגלית (הבעלים 17.11).</p>
<p><button id="nt">יום / לילה</button></p>
<div class="gal" id="gal"></div>
<h2>המלאי — משטח אחר משטח</h2>
<div class="tw"><table><tbody>{trs}</tbody></table></div>
<p class="muted">airlogos · 17.11.2026 · המקור: chatgpt.site של חבילת המותגים (catalog.js, renderer.js, sign_inventory.json) · החלק במשחק: parts/074v_airlogos.js</p>
</main><script>
const ROWS={rows};
const HEB={{}};
function logo(key,c,x,y,w,h){{const s=Math.min(w,h);c.save();c.translate(x+w/2,y+h/2);c.fillStyle=key==='rental'?'#1d2a16':'#03262d';c.fillRect(-s/2,-s/2,s,s);c.fillStyle=key==='rental'?'#ec881b':'#d4b376';
 c.beginPath();c.moveTo(-s*.36,s*.08);c.lineTo(s*.36,-s*.2);c.lineTo(s*.1,s*.22);c.lineTo(0,s*.04);c.closePath();c.fill();c.restore();return true}}
const D=(function(){{
{draw}
return{{sign}}}})();
let night=false;
function render(){{const g=document.getElementById('gal');g.innerHTML='';for(const r of ROWS){{const m={{id:r[0],name:r[1],group:r[2],color:r[3],ink:r[4],signType:r[5]}};if(m.group==='airlines')m.signText=HEB[m.id]||m.name;
 const w=r[6],h=r[7],sc=Math.max(4,Math.round(120/h)),cv=document.createElement('canvas');cv.width=Math.ceil(w*sc);cv.height=Math.ceil(h*sc);const c=cv.getContext('2d');c.scale(sc,sc);D.sign(c,m,w,h,night);
 const d=document.createElement('div');d.className='card';const b=document.createElement('b');b.textContent=m.signText||m.name;const s=document.createElement('small');s.textContent=w+'×'+h+' · '+(r[8].join(', ')||'שלט לאי צ׳ק-אין עתידי');d.append(cv,b,s);g.append(d)}}}}
document.getElementById('nt').onclick=()=>{{night=!night;render()}};render();
</script></body></html>'''
open(OUT, 'w', encoding='utf-8').write(H)
print('plan:', OUT, cnt, len(H))
