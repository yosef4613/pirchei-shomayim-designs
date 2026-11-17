#!/usr/bin/env python3
# h8_page.py — דף הציור של בית השחקן (house8, 17.11): לכל רמה — הצילום מהמשחק (מצויר בקנבס מתוך נתוני הצבע, בלי קובץ תמונה),
# תוכנית SVG מהנתונים (C3LV / C3PH_B), ומה נוסף ברמה; ובסוף — מה מההצעה עוד לא בבנייה, והצעת התיקון.
# python3 h8_page.py <shots_dir> <out.html> [build_name]
import sys, os, json, base64, html
from PIL import Image
SH, OUT = sys.argv[1], sys.argv[2]; BUILD = sys.argv[3] if len(sys.argv) > 3 else 'S7F302'
R = json.load(open(os.path.join(SH, 'h8_shots.json'), encoding='utf-8')); D = R['data']; LV = D['lv']
E = html.escape
OWNER_PRICE = {2: 4200, 3: 9000, 4: 17000, 5: 28000, 6: 35000, 7: 55000, 8: 80000}   # D‑343 (שונה 2.11 10:26)

def enc(png, maxw=980, colors=96):
    im = Image.open(png).convert('RGB')
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:colors * 3]; px = q.load(); W, H = q.size; out = bytearray()
    for y in range(H):
        x = 0
        while x < W:
            c = px[x, y]; n = 1
            while x + n < W and px[x + n, y] == c and n < 256: n += 1
            out += bytes((c, n - 1)); x += n
    return {'w': W, 'h': H, 'p': ''.join('%02x%02x%02x' % tuple(pal[i:i + 3]) for i in range(0, len(pal), 3)), 'd': base64.b64encode(bytes(out)).decode()}

def money(v): return '₪' + format(v, ',') if v else 'חינם (ההתחלה)'
F = R['frame']; FX0, FY0, FX1, FY1 = F
def plan_svg(L, prev):
    # the lot from above, in world units (the frame of all the levels); what is new in this level — in colour
    pb = {o['id'][-2:] if False else o['type'] for o in (prev['b'] if prev else [])}
    s = ['<svg viewBox="%d %d %d %d" class="plan" role="img" aria-label="תוכנית רמה %d">' % (FX0, FY0, FX1 - FX0, FY1 - FY0, L['n'])]
    lot = D.get('lot')
    if lot and lot.get('parts'):
        for p in lot['parts']: s.append('<rect x="%s" y="%s" width="%s" height="%s" class="lot"/>' % (p[0], p[1], p[2] - p[0], p[3] - p[1]))
    if L.get('drive'):
        d = L['drive']; s.append('<rect x="%s" y="%s" width="%s" height="%s" class="drive"/>' % (d[0], d[1], d[2] - d[0], d[3] - d[1]))
    pst = {(q['x'], q['y']) for q in (prev['stalls'] if prev else [])}
    for q in L['stalls']:
        s.append('<rect x="%s" y="%s" width="%s" height="%s" class="stall%s"/>' % (q['x'], q['y'], q['w'], q['h'], '' if (q['x'], q['y']) in pst else ' new'))
    if L.get('pool'):
        p = L['pool']; new = not prev or prev.get('pool') != p
        s.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" class="pool%s"/>' % (p[0], p[1], p[2] - p[0], p[3] - p[1], ' new' if new else ''))
    if L.get('pad'):
        P = L['pad']; new = not prev or not prev.get('pad')
        s.append('<circle cx="%s" cy="%s" r="%s" class="safe"/><circle cx="%s" cy="%s" r="%s" class="pad%s"/><text x="%s" y="%s" class="padh">H</text>' % (P['c'][0], P['c'][1], P['safety'], P['c'][0], P['c'][1], P['r'], ' new' if new else '', P['c'][0], P['c'][1] + 12))
    for o in L['b']:
        new = o['type'] not in pb
        cls = 'bld hg' if o['type'] == 'HANGAR' else 'bld'
        s.append('<rect x="%s" y="%s" width="%s" height="%s" class="%s%s"/>' % (o['x'], o['y'], o['w'], o['h'], cls, ' new' if new else ''))
        s.append('<text x="%s" y="%s" class="bl">%s</text>' % (o['x'] + o['w'] / 2, o['y'] + o['h'] / 2 + 8, E(o['label'])))
    g = D['base'].get('gate')
    if g: s.append('<rect x="%s" y="%s" width="10" height="%s" class="gate"/>' % (g['x'], g['y'], g['h']))
    s.append('</svg>'); return ''.join(s)

def added(L, prev):
    a = []
    if not prev:
        a += ['הבית הקטן (PH1) — הדלת היא נקודת השמירה', 'חניה אחת על הקרקע, ליד השער', 'המלתחה (חדר ההלבשה) — במסך F של הבית']
        return a
    pt = {o['type'] for o in prev['b']}
    for o in L['b']:
        if o['type'] not in pt: a.append(('מבנה חדש: ' if o['type'] in ('STUDIO', 'HANGAR', 'PH7W', 'PH8W') else 'הבית מוחלף: ') + o['label'] + ' (' + o['type'] + ', ' + str(o['w']) + '×' + str(o['h']) + ')')
    gone = [o for o in prev['b'] if o['type'] not in {q['type'] for q in L['b']}]
    for o in gone:
        if o['type'] in ('STUDIO',): a.append('הסטודיו נכנס לתוך ' + L['b'][0]['label'] if False else 'הסטודיו לא נשאר כמבנה נפרד ברמה הזאת')
    dn = len(L['stalls']) - len(prev['stalls'])
    if dn: a.append('+%d חניות (סך הכול %d; מקומות במוסך: %d)' % (dn, len(L['stalls']), L['garage']))
    if L.get('pool') and not prev.get('pool'): a.append('בריכה בחצר')
    elif L.get('pool') and prev.get('pool') != L['pool']: a.append('הבריכה גדלה / זזה')
    if L.get('pad') and not prev.get('pad'): a.append('מנחת מסוקים בחצר (Ø %d, טבעת בטיחות %d)' % (L['pad']['r'] * 2, L['pad']['safety']))
    dt = L['trees'] - prev['trees']
    if dt > 0: a.append('+%d עצים בגינה' % dt)
    df = L['flowers'] - prev['flowers']
    if df > 0: a.append('+%d ערוגות' % df)
    return a

cards = []; shots = {}
for i, L in enumerate(LV):
    n = L['n']; prev = LV[i - 1] if i else None; f = os.path.join(SH, 'L%d.png' % n)
    if os.path.exists(f): shots[n] = enc(f)
    pr = L['price']; op = OWNER_PRICE.get(n)
    price = money(pr) + ('' if not op or op == pr else ' <span class="warn">— הבעלים קבע %s (D‑343)</span>' % money(op))
    lst = ''.join('<li>%s</li>' % E(x) for x in added(L, prev))
    hg = any(o['type'] == 'HANGAR' for o in L['b'])
    note = '<p class="warn">ברמה הזאת עדיין עומד "המבנה למסוק" — הבעלים החליט (2.11 10:26, D‑373): בלי מבנה למסוק, המסוק חונה על המנחת.</p>' if hg else ''
    if any(o['type'] == 'STUDIO' for o in L['b']): note += '<p class="warn">הסטודיו עומד, אבל אין בו F ואין מסך עיצוב — מבנה בלבד.</p>'
    cards.append('''<section class="card" id="L%d"><header><b class="lvn">%d</b><div><h2>%s</h2><p class="meta">מחיר: %s · חניות: %d · מקומות במוסך: %d · מבנים: %s</p></div></header>
<div class="two"><figure><canvas class="shot" data-n="%d" aria-label="הצילום מהמשחק, רמה %d"></canvas><figcaption>הצילום מהמשחק (%s, זום %s, יום) — מצויר בקנבס מתוך נתוני הצבע של הצילום, בלי קובץ תמונה</figcaption></figure>
<figure>%s<figcaption>התוכנית מלמעלה מהנתונים (C3LV) — בכתום: מה שנוסף ברמה הזאת</figcaption></figure></div>
<h3>מה נוסף ברמה %d</h3><ul>%s</ul>%s</section>''' % (n, n, E(L['he']), price, len(L['stalls']), L['garage'], E(' · '.join(o['label'] for o in L['b'])), n, n, BUILD, R['zoom'], plan_svg(L, prev), n, lst, note))

rows = ''.join('<tr><td>%d</td><td>%s</td><td>%s</td><td class="%s">%s</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
    L['n'], E(L['he']), money(L['price']), 'warn' if OWNER_PRICE.get(L['n'], L['price']) != L['price'] else '', money(OWNER_PRICE.get(L['n'], L['price'])), len(L['stalls']),
    'כן' if L.get('pool') else '—', 'כן' if L.get('pad') else '—', E(' · '.join(o['label'] for o in L['b']))) for L in LV)

GAPS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gaps.html'), encoding='utf-8').read()
page = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>בית השחקן — 8 הרמות</title>
<style>:root{--bg:#f3f2ee;--fg:#1d232b;--mut:#5b636b;--card:#ffffff;--line:#d9d6cc;--lot:#cfe0b8;--bld:#9aa3ab;--new:#e8862a;--pool:#5cb8e0;--pad:#7d8489;--warn:#a4430f;--drive:#d8cdb4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181c;--fg:#e8ebee;--mut:#9aa3ab;--card:#1e2328;--line:#343b42;--lot:#2f4429;--bld:#5d666e;--new:#f0a050;--pool:#2f7fa8;--pad:#4b5258;--warn:#f0a070;--drive:#4a4436}}
:root[data-theme="dark"]{--bg:#15181c;--fg:#e8ebee;--mut:#9aa3ab;--card:#1e2328;--line:#343b42;--lot:#2f4429;--bld:#5d666e;--new:#f0a050;--pool:#2f7fa8;--pad:#4b5258;--warn:#f0a070;--drive:#4a4436}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Segoe UI",Arial,sans-serif}main{max-width:1180px;margin:0 auto;padding:16px}
h1{font-size:24px;margin:8px 0}h2{font-size:18px;margin:0}h3{font-size:15px;margin:12px 0 4px}.meta{margin:2px 0;color:var(--mut);font-size:13px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:16px 0}.card header{display:flex;gap:12px;align-items:center}
.lvn{display:inline-flex;width:40px;height:40px;border-radius:50%;background:var(--new);color:#fff;align-items:center;justify-content:center;font-size:20px;flex:none}
.two{display:grid;grid-template-columns:1.25fr 1fr;gap:12px;margin-top:10px}@media (max-width:760px){.two{grid-template-columns:1fr}}
figure{margin:0}figcaption{font-size:12px;color:var(--mut)}canvas.shot{width:100%;height:auto;display:block;border-radius:6px;background:#888}
svg.plan{width:100%;height:auto;display:block;background:var(--bg);border-radius:6px;direction:ltr}
.lot{fill:var(--lot)}.drive{fill:var(--drive)}.stall{fill:none;stroke:var(--mut);stroke-width:2}.stall.new{stroke:var(--new);stroke-width:3}
.bld{fill:var(--bld);stroke:var(--fg);stroke-width:1.5}.bld.new{fill:var(--new)}.bld.hg{stroke-dasharray:8 5}.bl{font-size:22px;text-anchor:middle;fill:var(--fg);font-weight:700}
.pool{fill:var(--pool)}.pool.new{stroke:var(--new);stroke-width:4}.pad{fill:var(--pad)}.pad.new{stroke:var(--new);stroke-width:4}.safe{fill:none;stroke:var(--new);stroke-dasharray:6 6;stroke-width:2}.padh{font-size:34px;fill:#fff;text-anchor:middle;font-weight:700}
.gate{fill:var(--fg)}.warn{color:var(--warn)}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}
.scroll{overflow-x:auto}ul{margin:4px 0;padding-inline-start:20px}.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:16px 0}
.tag{display:inline-block;font-size:12px;border-radius:4px;padding:0 6px;border:1px solid var(--line)}.ok{color:#2e7d32}</style></head><body><main>
<h1>בית השחקן ב-C3 — 8 הרמות</h1>
<p>מה שיש היום ב-@BUILD@, רמה אחרי רמה: הצילום מהמשחק של המגרש C3-PH באותה רמה, התוכנית מלמעלה, ומה נוסף. בסוף — מה מההצעה המקורית (D‑150, ‏D‑261, ‏D‑338, ‏D‑343, ‏D‑373) עוד לא בבנייה, והצעת התיקון.</p>
<div class="box"><h3>איך עולים רמה (במשחק היום)</h3><ul>
<li>ברגל, ליד הדלת של הבית (עד 175 פיקס׳) — F פותח את מסך הבית: "רמה N / 8", הרכבים שלי, חדר הלבשה, שמירה, ו"שדרוג הבית" עם 8 השורות.</li>
<li>הכפתור "שדרג לרמה N+1 · מחיר" — פעיל רק ליד הדלת ורק כשיש מספיק כסף. אין תנאי אחר (לא פרק בסיפור ולא משימה).</li>
<li>מיד אחרי הקנייה: הרמה נשמרת (שמירה עם גיבוי), מקומות המוסך גדלים, והמגרש מתחלף — המבנים, החניות, הגינה, הבריכה והמנחת של הרמה החדשה.</li>
<li>שמירה ישנה עם רמה — נטענת לאותה רמה (homeLevel 1–8).</li></ul></div>
<div class="box scroll"><h3>8 הרמות בטבלה</h3><table><tr><th>רמה</th><th>מה</th><th>המחיר בבנייה</th><th>המחיר שהבעלים קבע</th><th>חניות</th><th>בריכה</th><th>מנחת</th><th>המבנים</th></tr>@ROWS@</table></div>
@CARDS@
@GAPS@
<p class="meta">נוצר מ-@BUILD@ עם tools/h8_shots.js ו-tools/h8_page.py (house8, 17.11). אין בדף קובץ תמונה: הצילומים מצוירים בקנבס מנתוני הצבע, והתוכניות — SVG בקוד.</p>
</main><script>const SH=@SH@;
for(const c of document.querySelectorAll('canvas.shot')){const s=SH[c.dataset.n];if(!s)continue;c.width=s.w;c.height=s.h;const g=c.getContext('2d'),im=g.createImageData(s.w,s.h),P=[];
for(let i=0;i<s.p.length;i+=6)P.push([parseInt(s.p.substr(i,2),16),parseInt(s.p.substr(i+2,2),16),parseInt(s.p.substr(i+4,2),16)]);
const b=atob(s.d),A=im.data;let o=0;for(let i=0;i<b.length;i+=2){const p=P[b.charCodeAt(i)],n=b.charCodeAt(i+1)+1;for(let k=0;k<n;k++){A[o]=p[0];A[o+1]=p[1];A[o+2]=p[2];A[o+3]=255;o+=4}}g.putImageData(im,0,0)}</script></body></html>'''
page = page.replace('@BUILD@', BUILD).replace('@ROWS@', rows).replace('@CARDS@', ''.join(cards)).replace('@GAPS@', GAPS.replace('%BUILD%', BUILD)).replace('@SH@', json.dumps(shots, separators=(',', ':')))
open(OUT, 'w', encoding='utf-8').write(page)
import re
print(OUT, len(page), 'images:', bool(re.search(r'data:image|<img|new Image|url\(', page)), {k: (v['w'], v['h'], len(v['d'])) for k, v in shots.items()})
