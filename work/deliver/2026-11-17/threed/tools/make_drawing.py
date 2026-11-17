# הציור (כלל 13): B4 מלמעלה מתוך הנתונים, המצלמה של המשחק, וההפרדה בין נתוני העולם לציור. SVG בקוד בלבד, בלי תמונות.
import json, sys, html, math
D = json.load(open(sys.argv[1], encoding='utf-8')); OUT = sys.argv[2]
S = 5.2; PADX, PADY = 70, 60
wx0, wy0, wx1, wy1 = D['window']
X = lambda x: PADX + (x - wx0) * S
Y = lambda y: PADY + (y - wy0) * S
W = int(X(wx1) + PADX); H = int(Y(wy1) + PADY)
e = html.escape
o = []
o.append(f'<rect x="{X(wx0)}" y="{Y(wy0)}" width="{(wx1-wx0)*S}" height="{(wy1-wy0)*S}" fill="#6c9b51"/>')
zr = D['zone_rect']
o.append(f'<rect x="{X(zr[0])}" y="{Y(zr[1])}" width="{(zr[2]-zr[0])*S}" height="{(zr[3]-zr[1])*S}" fill="none" stroke="#fff6" stroke-width="2" stroke-dasharray="8 6"/>')
def clip(v, a, b): return max(a, min(b, v))
for r in D['roads']:
    (ax, ay), (bx, by) = r['pts']
    ax, bx = clip(ax, wx0, wx1), clip(bx, wx0, wx1); ay, by = clip(ay, wy0, wy1), clip(by, wy0, wy1)
    w = r['width'] + 2 * r['walk']
    o.append(f'<line x1="{X(ax)}" y1="{Y(ay)}" x2="{X(bx)}" y2="{Y(by)}" stroke="#c9c6bc" stroke-width="{w*S}" stroke-linecap="square"/>')
for r in D['roads']:
    (ax, ay), (bx, by) = r['pts']
    ax, bx = clip(ax, wx0, wx1), clip(bx, wx0, wx1); ay, by = clip(ay, wy0, wy1), clip(by, wy0, wy1)
    o.append(f'<line x1="{X(ax)}" y1="{Y(ay)}" x2="{X(bx)}" y2="{Y(by)}" stroke="#4a4f55" stroke-width="{r["width"]*S}" stroke-linecap="square"/>')
    col = '#e8c440'
    o.append(f'<line x1="{X(ax)}" y1="{Y(ay)}" x2="{X(bx)}" y2="{Y(by)}" stroke="{col}" stroke-width="1.6" stroke-dasharray="{"0" if r["median"] else "10 8"}"/>')
for n in D['nodes']:
    if n['kind'] == 'roundabout':
        o.append(f'<circle cx="{X(n["p"][0])}" cy="{Y(n["p"][1])}" r="{14*S}" fill="#4a4f55" stroke="#c9c6bc" stroke-width="{2*S}"/><circle cx="{X(n["p"][0])}" cy="{Y(n["p"][1])}" r="{6*S}" fill="#7fae5f" stroke="#fff" stroke-width="2"/>')
    if n['kind'] == 'signal':
        o.append(f'<circle cx="{X(n["p"][0])}" cy="{Y(n["p"][1])}" r="7" fill="#e04a3a" stroke="#fff" stroke-width="2"/>')
COL = {'building': '#d9cdb4', 'parking': '#7c8187', 'yard': '#b9b29f', 'park': '#7fae5f', 'court': '#c46a3c'}
for s in D['sites'] + [dict(l, kind='park') for l in D['lots']]:
    r = s['rect']; c = COL.get(s['kind'], '#aaa')
    o.append(f'<rect x="{X(r[0])}" y="{Y(r[1])}" width="{(r[2]-r[0])*S}" height="{(r[3]-r[1])*S}" fill="{c}" stroke="#2228" stroke-width="1"/>')
    if s['kind'] == 'building':
        h = (s['floors'] or 1) * 3.2 * 0.6 * S   # הגובה במבט 3/4 של המשחק (0.6)
        o.append(f'<polygon points="{X(r[0])},{Y(r[1])} {X(r[2])},{Y(r[1])} {X(r[2])},{Y(r[1])-h} {X(r[0])},{Y(r[1])-h}" fill="#efe6d2" stroke="#2228"/>')
        o.append(f'<text x="{(X(r[0])+X(r[2]))/2}" y="{(Y(r[1])+Y(r[3]))/2+4}" font-size="11" text-anchor="middle" fill="#2a2a2a">{e(s["id"])} · {s["floors"]} ק׳</text>')
for dw in D['driveways']:
    (ax, ay), (bx, by) = dw['pts']
    o.append(f'<line x1="{X(ax)}" y1="{Y(ay)}" x2="{X(bx)}" y2="{Y(by)}" stroke="#55595e" stroke-width="{dw["w"]*S}"/>')
names = {}
for r in D['roads']:
    names.setdefault(r['name'], r)
for nm, r in names.items():
    (ax, ay), (bx, by) = r['pts']; mx, my = clip((ax+bx)/2, wx0+6, wx1-6), clip((ay+by)/2, wy0+6, wy1-6)
    rot = -90 if ax == bx else 0
    o.append(f'<text x="{X(mx)}" y="{Y(my)}" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle" transform="rotate({rot} {X(mx)} {Y(my)})" style="paint-order:stroke" stroke="#0008" stroke-width="3">{e(nm)}</text>')
# הרכב של השחקן — נקודת ההתחלה
o.append(f'<rect x="{X(57.2)}" y="{Y(30)}" width="{1.84*S}" height="{4.6*S}" rx="3" fill="#d4af37" stroke="#1b2b45" stroke-width="2"/><text x="{X(57.2)-6}" y="{Y(33)}" font-size="12" text-anchor="end" fill="#fff" style="paint-order:stroke" stroke="#000a" stroke-width="3">הרכב של השחקן</text>')
plan = '\n'.join(o)
# המצלמה
cam = '''<svg viewBox="0 0 460 250" width="460" height="250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="המצלמה של המשחק">
<rect width="460" height="250" fill="#f6f2e6"/>
<line x1="30" y1="210" x2="430" y2="210" stroke="#6c9b51" stroke-width="6"/>
<rect x="250" y="150" width="60" height="60" fill="#d9cdb4" stroke="#333"/>
<line x1="120" y1="20" x2="250" y2="210" stroke="#1b2b45" stroke-width="2" stroke-dasharray="6 4"/>
<line x1="120" y1="20" x2="120" y2="210" stroke="#999" stroke-width="1"/>
<path d="M120 80 A60 60 0 0 1 151 69" fill="none" stroke="#d4af37" stroke-width="3"/>
<text x="160" y="70" font-size="14" fill="#1b2b45">31° מהאנך (atan 0.6)</text>
<circle cx="120" cy="20" r="9" fill="#d4af37"/><text x="135" y="25" font-size="13">מצלמה אורתוגרפית</text>
<text x="230" y="120" font-size="13" fill="#1b2b45">גובה z ← עולה במסך 0.6·z</text>
<text x="30" y="240" font-size="13" fill="#333">ומתיחה אנכית של התמונה ×1.166 (1/cos 31°) = בדיוק (x, y − 0.6·z) של המשחק</text>
</svg>'''
arch = '''<svg viewBox="0 0 900 230" width="900" height="230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="הפרדה בין הנתונים לציור">
<rect width="900" height="230" fill="#f6f2e6"/>
<g font-size="14" text-anchor="middle">
<rect x="680" y="30" width="200" height="80" rx="10" fill="#1b2b45"/><text x="780" y="62" fill="#d4af37" font-weight="bold">נתוני העולם</text><text x="780" y="86" fill="#fff">city_plan → b4_data.json</text>
<rect x="400" y="30" width="230" height="80" rx="10" fill="#28465e"/><text x="515" y="62" fill="#d4af37" font-weight="bold">הסימולציה (בלי ציור)</text><text x="515" y="86" fill="#fff">רכב, רמזורים, התנגשות, שעון</text>
<rect x="40" y="10" width="300" height="55" rx="10" fill="#3d6e4e"/><text x="190" y="44" fill="#fff">מצייר 2D של היום (קנבס 3/4)</text>
<rect x="40" y="80" width="300" height="55" rx="10" fill="#7a4e2a"/><text x="190" y="114" fill="#fff">מצייר תלת־ממד (Three.js) — האב־טיפוס</text>
<rect x="250" y="160" width="400" height="55" rx="10" fill="#d4af37"/><text x="450" y="185" fill="#1b2b45" font-weight="bold">World Manager — עיר / אזור נטען, מצייר לפי העיר</text><text x="450" y="205" fill="#1b2b45">השחקן, הכסף, המשימות, השמירה — משותפים לכל הערים</text>
</g>
<g stroke="#1b2b45" stroke-width="2.5" fill="none"><path d="M680 70 H630"/><path d="M400 60 L340 40"/><path d="M400 80 L340 105"/><path d="M515 110 V160"/></g>
</svg>'''
inv = [('B4 של הבעלים (Babylon.js)', 'turbo-city-b4 · 12MB · 7 מבנים מ-Kenney (CC0) · פריסה חופשית, לא המפה'),
       ('Downtown (Babylon.js)', 'turbo-city-downtown · ‏10.7MB בקבצים נפרדים · 14 דגמי glb'),
       ('כיכר קטנה (Three.js)', 'turbo-city-three-small · ‏0.56MB · הכול בקוד, בלי דגמים — הבסיס הכי קרוב לאב־טיפוס'),
       ('המשחק', 'C34 / P34 / A34 — ציירי 3/4 בקנבס (ממצא gfxlib); המצלמה x, y − 0.6·z'),
       ('נתוני B4', 'study/roads/city_plan.json — 11 דרכים, 7 מבנים, 4 חניונים, פארק, מגרש — במטרים')]
invh = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in inv)
page = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>הציור · ניסוי תלת־ממד B4</title>
<style>:root{{--bg:#efeadb;--ink:#1b2b45;--gold:#d4af37}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 Arial,sans-serif}}main{{max-width:1000px;margin:auto;padding:16px}}h1{{margin:.2em 0}}h2{{border-bottom:3px solid var(--gold);display:inline-block}}svg{{max-width:100%;height:auto;background:#fff;border-radius:10px}}table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #0002;padding:6px}}ul{{padding-inline-start:20px}}</style></head><body><main>
<h1>ניסוי תלת־ממד — הציור לפני הבנייה</h1>
<p>אזור אחד: <b>B4 — {e(D["purpose"])}</b>, לפי תוכנית הדרכים ({e(D["src"])}). רכב אחד: המכונית של השחקן. המראה: הצבעים והמצלמה של טורבו סיטי. הכול בקוד — בלי תמונות, בלי טקסטורות, בלי קובצי דגמים.</p>
<h2>B4 מלמעלה (מתוך הנתונים, במטרים)</h2>
<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="B4 מלמעלה">{plan}</svg>
<p>הקו המקווקו — גבולות B4 ({zr[2]-zr[0]:.0f} × {zr[3]-zr[1]:.0f} מ׳). המבנים מצוירים כמו במשחק: קיר דרומי שעולה 0.6 מהגובה. נקודה אדומה — רמזור. העיגול — כיכר הספורט.</p>
<h2>המצלמה</h2>
{cam}
<p>ממצא (gfxlib, ונבדק כאן): מצלמה אורתוגרפית מוטה 31° מהאנך + מתיחה אנכית ×1.166 נותנת בדיוק את ההיטל של המשחק. באב־טיפוס — שלושה מצבים: "מבט המשחק" (ההיטל המדויק), "מעקב" (מאחורי הרכב), "חופשי" (סיבוב וזום).</p>
<h2>ההפרדה בין נתוני המשחק לציור (World Manager)</h2>
{arch}
<h2>מה כבר קיים (כלל 16 / 19)</h2><table>{invh}</table>
<h2>מה ייבנה באב־טיפוס</h2><ul>
<li>הקרקע, הכבישים ברוחב האמיתי (עורק 22.6 מ׳ עם חציון, מאסף 11.8, מקומי 10.8), מדרכות, אבני שפה, קווי נתיבים, מעברי חצייה רק בצמתים (כלל 21), כיכר.</li>
<li>7 המבנים בגובה לפי הקומות, חלונות, גגות ומעקות; החניונים עם קווי חניה; הפארק עם עצים וספסלים; מגרש הכדורסל.</li>
<li>רמזורים שעובדים (מחזור), פנסי רחוב, יום / לילה עם אורות.</li>
<li>מכונית אחת בקוד (סדאן 4.6 × 1.84 מ׳) — נהיגה WASD, התנגשות במבנים, פנסים בלילה.</li>
<li>מונה FPS, קריאות ציור ומשולשים; מצב "איכות נמוכה" למחשב חלש.</li></ul>
</main></body></html>'''
assert 'data:image' not in page and '<img' not in page
open(OUT, 'w', encoding='utf-8').write(page); print(len(page))
