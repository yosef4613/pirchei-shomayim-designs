# -*- coding: utf-8 -*-
# gen_design.py — fieldfix: הציור (כלל 13) — SVG בקוד בלבד, בלי תמונות. python3 gen_design.py <out.html>
import sys, math, json
out = sys.argv[1]
# ---- המפה של צד הבסיס (קואורדינטות העולם, פיקסלים) ----
X0, Y0, X1, Y1 = 8050, 1250, 9650, 2560
S = 0.5
def P(x, y): return ((x - X0) * S, (y - Y0) * S)
def rect(r, fill, stroke='none', op=1, lbl=None, fs=11):
    x, y = P(r[0], r[1]); w, h = (r[2] - r[0]) * S, (r[3] - r[1]) * S
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" opacity="{op}"/>'
    if lbl: s += f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + 4:.1f}" font-size="{fs}" text-anchor="middle" fill="var(--ink)">{lbl}</text>'
    return s
def path(pts, col, w=3, dash=None):
    d = 'M' + ' L'.join(f'{P(*q)[0]:.1f},{P(*q)[1]:.1f}' for q in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""}/>'
def arc(cx, cy, r, a0, a1, n=6): return [[cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)] for i in range(n + 1)]
Y, BX, R3 = 1850, 9400, [9369, 2180]
g = []
g.append(rect([X0, Y0, X1, Y1], 'var(--grass)'))
g.append(rect([8050, 1775, 9475, 1925], 'var(--tw)', lbl='מסלול הסעה C'))
g.append(rect([9325, 1250, 9475, 1925], 'var(--tw)'))
g.append(f'<text x="{P(9400, 1350)[0]:.1f}" y="{P(9400, 1350)[1]:.1f}" font-size="11" text-anchor="middle" fill="var(--ink)" transform="rotate(90 {P(9400, 1350)[0]:.1f} {P(9400, 1350)[1]:.1f})">מסלול הסעה B</text>')
g.append(rect([7953, 1626, 9214, 1670], 'var(--road)', lbl='דרך הבסיס', fs=9))
g.append(rect([9088, 1250, 9176, 1626], 'var(--road)'))
g.append(rect([9170, 1670, 9214, 2034], 'var(--road)'))
g.append(rect([7909, 2034, 9214, 2078], 'var(--road)', lbl='דרך הזנבות', fs=9))
g.append(rect([9216, 2093, 9544, 2500], 'var(--stand)', 'var(--ink)', lbl=''))
g.append(rect([9236, 2140, 9524, 2480], 'none', '#e8742a'))
g.append(rect([9216, 2508, 9544, 2540], '#6b7680', lbl=''))
g.append(f'<text x="{P(9380, 2470)[0]:.1f}" y="{P(9380, 2470)[1]:.1f}" font-size="12" font-weight="700" text-anchor="middle" fill="var(--ink)">R3 — רחבת ההרצה</text>')
g.append(f'<text x="{P(9380, 2530)[0]:.1f}" y="{P(9380, 2530)[1] + 4:.1f}" font-size="9" text-anchor="middle" fill="#fff">קיר ההדף</text>')
g.append(rect([8814, 2034, 9216, 2500], 'var(--stand2)', lbl='R2'))
for hid, r, nm, ac in [('A', [8696, 1311, 9053, 1621], 'האנגר א׳', 'AC-RJ-01'), ('B', [8348, 1411, 8552, 1621], 'האנגר ב׳', 'AC-BJ-01'), ('C', [8148, 1456, 8338, 1621], 'האנגר ג׳', 'AC-LT-01')]:
    g.append(rect(r, 'var(--hgr)', 'var(--ink)', lbl=nm + ' · ' + ac, fs=10))
# הדרכים — A (כחול), B (סגול), C (ירוק); החוצה — קו מלא, חזרה — מקווקו
wayA = [[8770, 1466], [9200, 1466], [9310, 1466], [9359, 1480], [9392, 1519], [BX, 2040], R3]
g.append(path(wayA, '#2f6fd6', 4))
for x, col in [(8450, '#8a3ab9'), (8243, '#1f8a4c')]:
    out1 = [[x, 1531], [x, Y - 50]] + arc(x + 50, Y - 50, 50, math.pi, math.pi / 2) + [[BX + 40, Y]]
    out2 = [[BX + 40, Y]] + arc(BX + 40, Y + 40, 40, -math.pi / 2, -math.pi) + [[BX, 2040], R3]
    g.append(path(out1, col, 3)); g.append(path(out2, col, 3, '6 4'))
# נקודת ההרצה
x, y = P(*R3); g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#e8742a"/><text x="{x + 12:.1f}" y="{y + 4:.1f}" font-size="10" fill="var(--ink)">גלגל האף — האף צפונה, ההדף אל הקיר</text>')
svg_map = f'<svg viewBox="0 0 {(X1 - X0) * S:.0f} {(Y1 - Y0) * S:.0f}" role="img" aria-label="R3 והדרכים מההאנגרים">' + ''.join(g) + '</svg>'
# ---- הצבעים: ארבעה סגנונות, מלמעלה, "היה ב-3/4" מול "עכשיו ב-3/4 = כמו מלמעלה" ----
LIV = {'dots': dict(n='קונפטי', b='#ffffff', s='#ff4d6d', t='#3a86ff', m='#ffbe0b', d=['#ff4d6d', '#3a86ff', '#ffbe0b', '#06d6a0']),
       'split': dict(n='ארגזי הדרך (משא)', b='#e9ecef', s='#2b2f34', t='#e07a1a', m='#2b2f34'),
       'swoosh': dict(n='רוח הגאות', b='#f3f5f7', s='#13294b', t='#13294b', m='#7fd1ff'),
       'spine': dict(n='קו הרקיע', b='#eef2f6', s='#3a3f8f', t='#3a3f8f', m='#f2c230')}
def plane(w, lv, new):
    L, hw = 220, 15; o = []
    o.append(f'<g transform="translate(130 30)">')
    o.append(f'<path d="M-75,{L*.42} L75,{L*.42} L12,{L*.3} L-12,{L*.3} Z" fill="#d9dde2"/>' if False else '')
    o.append(f'<path d="M-95,{L*.5} L-14,{L*.36} L14,{L*.36} L95,{L*.5} L95,{L*.55} L14,{L*.5} L-14,{L*.5} L-95,{L*.55} Z" fill="#dfe3e8" stroke="#9aa4ad"/>')
    o.append(f'<path d="M-36,{L*.93} L-8,{L*.86} L8,{L*.86} L36,{L*.93} L36,{L*.96} L-36,{L*.96} Z" fill="{lv["t"]}"/>')
    o.append(f'<clipPath id="f{w}{new}"><path d="M0,0 C{hw},10 {hw},30 {hw},50 L{hw},{L*.9} C{hw},{L} -{hw},{L} -{hw},{L*.9} L-{hw},50 C-{hw},30 -{hw},10 0,0 Z"/></clipPath>')
    o.append(f'<g clip-path="url(#f{w}{new})"><rect x="-20" y="0" width="40" height="{L}" fill="{lv["b"]}"/>')
    tail = L * .8
    if new:
        if w == 'dots':
            i = 0; y = 34
            while y < tail - 6:
                for x in (-9, 0, 9):
                    r = 2.4 + 1.3 * ((i * 7) % 3); o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{lv["d"][i % 4]}"/>'); i += 1
                y += 11
        if w == 'split':
            o.append(f'<path d="M-20,{L*.47+8} L20,{L*.47-8} L20,{L} L-20,{L} Z" fill="{lv["t"]}"/><path d="M-20,{L*.47+2} L20,{L*.47-14}" stroke="{lv["s"]}" stroke-width="4"/>')
        if w == 'swoosh':
            o.append(f'<path d="M-20,{L*.12} C-14,{L*.35} 0,{L*.5} 0,{L*.66} L0,{L} L-20,{L} Z" fill="{lv["s"]}"/><path d="M20,{L*.12} C14,{L*.35} 0,{L*.5} 0,{L*.66} L0,{L} L20,{L} Z" fill="{lv["s"]}"/>')
            o.append(f'<path d="M-17,{L*.1} C-12,{L*.33} -2,{L*.48} -1,{L*.62}" stroke="{lv["m"]}" stroke-width="2.5" fill="none"/><path d="M17,{L*.1} C12,{L*.33} 2,{L*.48} 1,{L*.62}" stroke="{lv["m"]}" stroke-width="2.5" fill="none"/>')
        if w == 'spine':
            o.append(f'<rect x="-7" y="10" width="14" height="{L}" fill="{lv["s"]}"/><rect x="-8.5" y="10" width="1.6" height="{L}" fill="{lv["m"]}"/><rect x="6.9" y="10" width="1.6" height="{L}" fill="{lv["m"]}"/>')
    else:
        if w == 'spine': o.append(f'<rect x="-5" y="18" width="10" height="{L}" fill="{lv["s"]}"/>')
        if w == 'swoosh': o.append(f'<path d="M-16,{L*.35} L-12,{L*.5} L-9,{L*.5} L-13,{L*.35} Z" fill="{lv["s"]}"/><path d="M16,{L*.35} L12,{L*.5} L9,{L*.5} L13,{L*.35} Z" fill="{lv["s"]}"/>')
    o.append(f'<rect x="-20" y="{tail}" width="40" height="{L}" fill="{lv["t"]}"/></g>')
    o.append(f'<path d="M0,0 C{hw},10 {hw},30 {hw},50 L{hw},{L*.9} C{hw},{L} -{hw},{L} -{hw},{L*.9} L-{hw},50 C-{hw},30 -{hw},10 0,0 Z" fill="none" stroke="#56606a"/>')
    o.append(f'<rect x="-7" y="{L*.82}" width="14" height="22" rx="3" fill="{lv["t"]}" stroke="#56606a"/></g>')
    return f'<svg viewBox="0 0 260 270" role="img" aria-label="{lv["n"]}">' + ''.join(o) + '</svg>'
cards = ''
for w, lv in LIV.items():
    cards += f'<div class="card"><h4>{lv["n"]} · {w}</h4><div class="pair"><figure>{plane(w, lv, False)}<figcaption>היה ב-3/4 (הצייר הישן)</figcaption></figure><figure>{plane(w, lv, True)}<figcaption>עכשיו ב-3/4 — כמו מלמעלה</figcaption></figure></div></div>'
# ---- המסלול: חלונות הנחיתה / ההמראה במחזור (720 ש׳) — מהסימולציה כמו שרצה במשחק + הטיסה החדשה ----
def fc_wins(S, a):   # הכלל של fieldcalc: תפוס רק על המסלול ונמוך מ-40
    W = []; cur = None
    for g in a.legs:
        if not any(p[1] < S.HOLD - 10 and 4900 <= p[0] <= 9400 for p in g['p']) and not (len(g['p']) >= 2 and g['p'][0][0] < 4950 and g['p'][-1][0] >= 4950 and g['p'][-1][1] < S.HOLD):
            if cur is not None: W.append(cur); cur = None
            continue
        t = g['t0']
        while t <= g['t1'] + 1e-6:
            P = S.evalp(a, t); on = bool(P) and P[3] < 40 and 4900 <= P[0] <= 9400 and P[1] < S.HOLD - 10
            if on and cur is None: cur = [t, t]
            elif on: cur[1] = t
            elif cur is not None: W.append(cur); cur = None
            t += .25
    if cur: W.append(cur)
    return W
def rwy_svg():
    import io, contextlib
    sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-10/s15/tools')
    with contextlib.redirect_stdout(io.StringIO()):
        import s15_sim as S
    base = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldfix/tmp/'
    sim = json.load(open(base + 'sim_rt.json')); add = json.load(open(base + 'flights_fc3.json'))['add']
    rows = []
    for f in sim['flights'] + [a['flight'] for a in add]:
        a = S.Actor(f['id'], 'ac', f['model'], f['home'], f['L'], f['W']); a.legs = f['legs']
        rows.append((f['id'], f['model'], any(f['id'] == x['flight']['id'] for x in add), [[w[0] % 720, w[1] % 720 if w[1] % 720 > w[0] % 720 else w[1] % 720 + 720] for w in fc_wins(S, a)]))
    W, H, x0 = 900, 26 * len(rows) + 50, 150; k = (W - x0 - 10) / 720
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="המסלול במחזור">']
    for t in range(0, 721, 60): o.append(f'<line x1="{x0 + t * k:.1f}" y1="20" x2="{x0 + t * k:.1f}" y2="{H - 20}" stroke="var(--line)"/><text x="{x0 + t * k:.1f}" y="14" font-size="10" text-anchor="middle" fill="var(--mut)">{t}</text>')
    tot = 0
    for i, (fid, m, new, ws) in enumerate(rows):
        y = 26 + i * 26; o.append(f'<text x="{x0 - 8}" y="{y + 14}" font-size="11" text-anchor="end" fill="var(--ink)">{fid} · {m}{" (חדש)" if new else ""}</text>')
        for a, b in ws:
            for (p, q) in ([(a, min(b, 720))] + ([(0, b - 720)] if b > 720 else [])):
                o.append(f'<rect x="{x0 + p * k:.1f}" y="{y + 3}" width="{(q - p) * k:.1f}" height="16" rx="3" fill="{"#e8742a" if new else "#2f6fd6"}"/>'); tot += q - p
    o.append(f'<text x="{x0}" y="{H - 4}" font-size="11" fill="var(--ink)">שניות המחזור (720 = 6 שעות משחק) · המסלול תפוס {tot:.0f} ש׳ ({100 * tot / 720:.0f}%), בכלל של fieldcalc (רק על המסלול; מרווח 3 ש׳ ועוד 8 אחרי כבד) — המסלול איננו המגבלה</text></svg>')
    return ''.join(o)
try: RWY = rwy_svg()
except Exception as e: RWY = '<p class="mut">(הציור של המסלול — לא נוצר: ' + str(e)[:80] + ')</p>'
# ---- התור בשרוול ----
def bridge(cap):
    o = ['<svg viewBox="0 0 640 110" role="img" aria-label="התור בשרוול">', '<rect x="20" y="40" width="520" height="30" rx="6" fill="var(--tw)" stroke="var(--ink)"/>',
         '<text x="280" y="30" font-size="12" text-anchor="middle" fill="var(--ink)">השרוול — 193 פיקס׳ = 31 מקומות (רווח 0.8 מ׳)</text>', '<rect x="540" y="30" width="80" height="50" rx="8" fill="var(--hgr)" stroke="var(--ink)"/><text x="580" y="60" font-size="11" text-anchor="middle" fill="var(--ink)">הדלת · 0.85 ש׳</text>']
    for i in range(31): o.append(f'<circle cx="{530 - i * 16.5:.1f}" cy="55" r="5" fill="{"#3a86ff" if i < cap else "#d33"}"/>')
    o.append('<text x="10" y="100" font-size="11" fill="var(--ink)">נוסע מספר i נכנס לשרוול רק אחרי שנוסע i−31 עבר בדלת; עד אז מחכה בשער. בלי זה: 87 / 182 "נדחפו אל מחוץ לשרוול" ב-P2 / P3.</text></svg>')
    return ''.join(o)
def east_svg():
    cols = [4800, 6000, 7200, 8400, 9600]; rows = [-850, 0, 850, 1700, 2550]; s = 0.11; ox, oy = 4800, -850
    old = {'E0', 'F0', 'G0', 'E1', 'F1', 'G1', 'E2', 'F2', 'G2', 'E3', 'F3'}; new = {'G3', 'H0', 'H1', 'H2', 'H3'}
    poly = [[4800,-850],[9600,-850],[9600,2550],[7200,2550],[7200,1700],[7860,1700],[7860,1180],[7222,1180],[7222,1022],[5950,1022],[5950,580],[5750,580],[5750,780],[5430,780],[5430,725],[4800,725]]
    g = []
    for i in range(4):
        for j in range(4):
            x, y = cols[i], rows[j]; zid = 'EFGH'[i] + str(j)
            fill = '#4f7f47' if zid in old else ('#d9a03a' if zid in new else '#8a9aa6')
            g.append(f'<rect x="{(x-ox)*s:.1f}" y="{(y-oy)*s:.1f}" width="{1200*s:.1f}" height="{850*s:.1f}" fill="{fill}" stroke="#fff" stroke-width="1.5" opacity=".85"/>')
            g.append(f'<text x="{(x-ox+600)*s:.1f}" y="{(y-oy+425)*s+5:.1f}" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">{zid}</text>')
    pts = ' '.join(f'{(x-ox)*s:.1f},{(y-oy)*s:.1f}' for x, y in poly)
    g.append(f'<polygon points="{pts}" fill="none" stroke="#e23b3b" stroke-width="3" stroke-dasharray="7 4"/>')
    g.append(f'<rect x="{(5000-ox)*s:.1f}" y="{(-560-oy)*s:.1f}" width="{4300*s:.1f}" height="{60*s:.1f}" fill="#333"/>')
    g.append(f'<rect x="{(9325-ox)*s:.1f}" y="{(-850-oy)*s:.1f}" width="{150*s:.1f}" height="{2775*s:.1f}" fill="#555" opacity=".8"/>')
    W, H = 4800 * s, 3400 * s
    return f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="G3 ו-H0–H3 נכנסים לאזורים החיים">' + ''.join(g) + '</svg>'
EAST = east_svg()
html = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>השדה — תיקונים מיידיים</title>
<style>:root{{--bg:#f6f4ef;--ink:#1d2328;--mut:#5b6670;--card:#fff;--grass:#cfe3c2;--tw:#c9ccd0;--road:#9aa1a8;--stand:#e7e2d6;--stand2:#ece8de;--hgr:#dfe7f0;--line:#d8d3c8}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#15191d;--ink:#e8ecef;--mut:#9aa6b0;--card:#1f252b;--grass:#2c3d2a;--tw:#4a5057;--road:#61686f;--stand:#3a3833;--stand2:#34322e;--hgr:#2b3846;--line:#323a42}}}}
:root[data-theme="dark"]{{--bg:#15191d;--ink:#e8ecef;--mut:#9aa6b0;--card:#1f252b;--grass:#2c3d2a;--tw:#4a5057;--road:#61686f;--stand:#3a3833;--stand2:#34322e;--hgr:#2b3846;--line:#323a42}}
body{{background:var(--bg);color:var(--ink);font-family:system-ui,"Segoe UI",Arial,sans-serif;margin:0;padding:16px;line-height:1.55}}main{{max-width:1100px;margin:auto}}
h1{{font-size:1.5rem}}h2{{font-size:1.15rem;margin-top:2rem;border-bottom:1px solid var(--line);padding-bottom:4px}}h4{{margin:.2rem 0}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}}
.pair{{display:flex;gap:6px}}figure{{margin:0;flex:1;text-align:center}}figcaption{{font-size:.8rem;color:var(--mut)}}svg{{width:100%;height:auto}}
table{{border-collapse:collapse;width:100%;font-size:.9rem}}td,th{{border:1px solid var(--line);padding:4px 6px;text-align:right}}.mut{{color:var(--mut)}}.leg span{{display:inline-block;width:22px;height:4px;vertical-align:middle;margin-inline:6px}}</style></head><body><main>
<h1>השדה — תיקונים מיידיים (fieldfix, ‏17.11)</h1><p class="mut">הציור לפני הבנייה (כלל 13). הכול בקוד — בלי תמונות. מבוסס על הקוד של S7F298 ועל המדידה בתוך המשחק.</p>
<h2>המלאי — מה קיים ואיפה (כלל 16 / 19)</h2><table><tr><th>פריט</th><th>איפה</th><th>המצב</th><th>מה עושים</th></tr>
<tr><td>הצבעים ב-3/4</td><td>‏013:LIV / livOf (טבלה אחת) → ‏068:a34Liv → ‏068:liveryFns (הצייר של 3/4)</td><td>המספר והטבלה זהים מלמעלה וב-3/4 (נמדד: 19 מטוסים, אותו צבע). השוני — בצייר: dots בלי נקודות, split רק החצי התחתון, swoosh פס דק, spine פס צר</td><td>הצייר של 3/4 כמו 013:wrap (שדרוג, בלי טבלה חדשה)</td></tr>
<tr><td>R3 — מטוס קבוע</td><td>‏019m:s15HgrPose + ‏074q (מעמיד את AC-TP-01 ב-R3 כל הזמן)</td><td>חונה ב-R3 ביום ובלילה</td><td>ביום ריק; בלילה מטוס מההאנגרים, במחזור</td></tr>
<tr><td>s15pax</td><td>הענף s15pax ‏53605df · ‏074x3_S15pax.js</td><td>s15pax_flow נכשל: התור עולה על הקיבולת של השרוול; והבדיקה רצה גם כשכבוי (שורה 179)</td><td>קיבולת בתור; הבדיקה רק כשדולק</td></tr>
<tr><td>תמהיל הטיסות</td><td>‏019l:S15SIM (6 טיסות במחזור 720 ש׳), ‏074p:FL-C2</td><td>P1 / P6 (הענקים), GA1 (המנהלים), C1 (משא) — חונים בלי טיסה; המסלול תפוס ~76%</td><td>טיסה חדשה בכלי של S15 (s15_sim.py) מול כל מה שרץ במשחק: GA1 נכנס; לענקים ולמשא הגדול אין חלון</td></tr>
<tr><td>החניונים של S16</td><td>‏074v_S16d_lots.js (s16d ‏e021b47)</td><td>כבר ב-master: הרב-קומתי, חניון הצוות, ‏P‑RENT, ‏P‑WEST</td><td>נבדק — נעשה; לא נוגעים</td></tr></table>
<h2>(1) הצבעים ב-3/4 — כמו במבט הרגיל</h2><div class="cards">{cards}</div>
<h2>(2) R3 — בלי מטוס קבוע; הרצת מנועים במחזור</h2>
<p class="leg"><span style="background:#2f6fd6"></span>האנגר א׳ (AC-RJ-01) — הדרך הקיימת של HGR-OUT / HGR-BACK <span style="background:#8a3ab9"></span>האנגר ב׳ (AC-BJ-01) <span style="background:#1f8a4c"></span>האנגר ג׳ (AC-LT-01) — קו מלא: קדימה; מקווקו: דחיפה לאחור אל R3</p>
{svg_map}
<table><tr><th>שעה (שעון המשחק)</th><th>מה קורה</th></tr><tr><td>05:30–18:10</td><td>R3 ריק. כל המטוסים בתוך ההאנגרים.</td></tr><tr><td>18:10</td><td>המטוס של הלילה (במחזור: א׳ → ב׳ → ג׳) נגרר מההאנגר שלו אל R3 — בחלון שבו C ו-B פנויים (הבדיקה fieldfix_r3)</td></tr>
<tr><td>20:30–04:25</td><td>הרצת מנועים (ההדף אל הקיר)</td></tr><tr><td>04:45</td><td>חוזר באותה דרך אל ההאנגר</td></tr></table>
<p class="mut">לאישורך: AC-TP-01 (המטוס של היום ב-R3) לא במחזור — אין לו מקום ביום (בהאנגר א׳ כבר ה-RJ, והרחבה חוסמת את רחוב הבסיס, כמו שמצא 074q).</p>
<h2>מה היה במנוע הישן — התחזוקה וההאנגרים (S7F272 / 282 / 284; כלל 19א)</h2>
<table><tr><th>המנגנון בישן</th><th>מה פתר</th><th>מקבילה ב-S15</th><th>מה נעשה</th></tr>
<tr><td>עמדות תחזוקה M1–M3 בתוך ההאנגרים (042:365 — kind 'maint', ‏indoor, ‏live:false; ‏044:g77Prof — role 'maint', שירותים: גרירה וסדים בלבד)</td><td>מטוס עומד בהאנגר בלי שירותי סבב (לא נוסעים, לא כבודה); לא תופס עמדה בלוח</td><td>כן — 074k:s15bAc (מטוס בכל האנגר, S15B_L.hangars)</td><td>נשאר; ועליו — מחזור התחזוקה (החלפה עם הלוח)</td></tr>
<tr><td>הביקור החי G77_MLV (051:263 — g77MlvPlan / g77MlvStep): כל ~1500 ש׳ (±420) המטוס נגרר מההאנגר לרחבה, "בדיקת מערכות / הנעת מנוע אחרי טיפול" 40–75 ש׳, ונדחף חזרה; הגרר והמטוס משוריינים ב-AO (aoSamp / aoFreeK / aoCommit)</td><td>תנועה של תחזוקה בלי התנגשות — שריון במרחב־זמן לפני שמתחייבים</td><td>חלקית — 074zo: הרצה בלילה ב-R3 במחזור; הבדיקה fieldfix_r3 (כל 0.5 ש׳, הקופסאות של S15) במקום שריון</td><td>הובא: הטקסטים של G77_MLV.what כתווית "תחזוקה · …" מעל ההרצה (074zp2). השריון במרחב־זמן — עם המתכנן החדש (fieldthru)</td></tr>
<tr><td>הגג השקוף (046:s6aHangarXray, ‏D‑105): המכסה פתוח, במת עבודה, שני מכונאים</td><td>"ההאנגרים מראים מה בפנים"</td><td>הגג השקוף קיים; העבודה — לא</td><td>הובא: אותו ציור (s6aDrawLoader, העוגנים של APTT_SPEC) על המטוס של S15 בהאנגר (074zp2:ffmxWork)</td></tr>
<tr><td>רכב תחזוקה MX (046:14) וגרר התחזוקה בפתח ההאנגר (045:510)</td><td>הצוות והגרר של הביקור</td><td>הסוג MX קיים בצי של S15 (074r:S15K_VT)</td><td>הגרר — כבר בגרירות של R3 (LV-PT-01 באף)</td></tr>
<tr><td>החלפה בין ההאנגר ללוח</td><td>— לא היה בישן (live:false — התחזוקה לא קשורה לטיסות)</td><td>—</td><td>חדש לפי הבעלים (סעיף 9): 074zp2 — כל 3 ימים</td></tr></table>
<h2>(2ב) מחזור התחזוקה — "מתוקנים וחוזרים לטיסות" (הבעלים, סעיף 9; planrev 1)</h2>
<table><tr><th>האנגר</th><th>המטוס</th><th>הטיסה מאותו דגם</th><th>כל 3 ימי משחק</th></tr>
<tr><td>א׳ (AIR-BASE-1)</td><td>AC-RJ-01</td><td>FL-P4 (P4)</td><td rowspan="3">המטוס שבהאנגר "תוקן" — החברה והצבעים שלו עוברים לטיסה, והוא בלוח; המטוס שטס עד אז נכנס לתחזוקה — הוא בהאנגר, והוא שמריץ מנועים ב-R3 בלילה. כל זוג בהיסט של יום (לא שלושתם יחד). ההחלפה — רק כשהטיסה מחוץ לעולם (באוויר בין ההמראה לגישה) וההאנגר לא במבט: שום מטוס לא "מתחלף" מול העיניים.</td></tr>
<tr><td>ב׳ (AIR-BASE-2)</td><td>AC-BJ-01</td><td>FL-GA1 (GA1, המנהלים)</td></tr>
<tr><td>ג׳ (HAP3, על הרחבה)</td><td>AC-LT-01</td><td>FL-GA6 (GA6) — אותה חברה (GA): רק גוף המטוס מתחלף</td></tr></table>
<p class="mut">הבדיקה fieldfix_maint (בתוך roadAudit): אותו דגם בכל זוג, 3–4 החלפות ב-12 ימים לכל זוג, החברה בלו״ז = של הטיסה, צבעים לכל חברה, ויש רגע מחוץ לעולם בכל מחזור. ‎#ffmx=0 — בלי.
השלב הבא (לא בגרסה הזאת): הגרירה הנראית מהעמדה אל ההאנגר ביום ההחלפה — צריך חלון ב-C / B מול כל הלוח (אותה בדיקה של fieldfix_r3).</p>
<p class="mut">ההדף ב-R3 (planrev 4): המטוס ב-R3 (9369, 2180) עם האף צפונה — ההדף דרומה אל הגדר הדרומית של הרחבה (y ≈ 2545). הבסיס הדרומי של fieldcalc (H4: x 8480–9600, ‏y 2550–2830) מיד מאחוריה —
לתיאום: קיר הדף בגדר (x 9230–9510, y 2545) ובלילה (20:30–04:25) בלי חניה בבסיס בתוך x 9230–9510, y 2550–2700. ‏AC-TP-01 (המטוס הקבוע של R3 לפני): לא מצויר עכשיו — לאישורך: חניה קבועה ב-R1 / R3 ביום, או מטוס רביעי במחזור התחזוקה (חליפה עם FL-P4 כשאין RJ בהאנגר).</p>
<h2>(4) s15pax — התור בשרוול</h2>{bridge(31)}
<h2>(3) תמהיל הטיסות — מה נכנס ולמה לא יותר</h2><table><tr><th>עמדה</th><th>מטוס</th><th>היום</th><th>אחרי</th></tr>
<tr><td>GA1</td><td>AC-BJ-01 (מנהלים)</td><td>חונה קבוע</td><td><b>טיסת מנהלים FL-GA1</b> — ממריאה ב-24, נוחתת ב-330 (במחזור של 720), <b>326 ש׳ בעמדה</b> (163 דק׳ משחק) — יותר מזמן השירות של מטוס מנהלים במטריצה של fieldcalc (240–260: GPU 180, דלק 40, קייטרינג 60, שירותים 30, ניקיון 60). הגרר PT-GA1 בכיס AIR-GSE-GA1|GA2. רכבי השירות עצמם — עוד לא: s15k מתכנן לפני שהטיסה נכנסת (המתכנן החדש — fieldthru).</td></tr>
<tr><td>P1 / P6</td><td>AC-LG-01 (הענקים)</td><td>חונים קבוע</td><td>יישור לפי fieldcalc: הכלל הקודם ("אין חלון במסלול") — שגוי (ספר את כל רגל הגישה + 8 ש׳). בכלל של fieldcalc המסלול לא המגבלה; מעל הלוח של היום הם עדיין לא נכנסים — כל חלון נוגע בהסעה (A / B בלי המתנות, 12,000 צירופים לכל עמדה). נכנסים בלוח של fieldcalc כשהגדולים קודם (fc_sim_result_big.json: P1 ממריא 0 / נוחת 184, ‏P6 ‏41 / 289) — הלוח והמתכנן: fieldthru.</td></tr>
<tr><td>C1</td><td>AC-CG-01 (משא גדול)</td><td>חונה קבוע</td><td>כמו הענקים: נכנס בלוח של fieldcalc (ממריא 346 / נוחת 210); מעל הלוח של היום — לא. FL-C2 (AC-TB-01) נשאר.</td></tr>
{RWY}
<p class="mut">אין כאן "לאישורך" על צפיפות הלו״ז: הלוח החדש (כל השדה, עם המתנות בדרך כמו AO של הישן) — של fieldthru, הגאומטריה — של fieldcalc. הכלי שלי (ff_flights.py) עובד עכשיו בכלל של fieldcalc, ויכניס את הענקים מעל הלוח החדש כשיהיה.</p>
<p class="mut">הכלי: s15_sim.py של S15 (make_flight / ac_conflict) — כמו FL-C2 של s15i. בלי עריכה של 019l; חלק עוטף מוסיף את הטיסות.</p>
<h2>(6) החלק המזרחי של השדה — G3, ‏H0–H3 באזורים החיים (תלות מ-mapfix)</h2>
<p class="leg"><span style="background:#4f7f47"></span>חי כבר (ACTIVE_REGIONS) <span style="background:#d9a03a"></span>נכנס עכשיו (028z_ff_east_live.js) <span style="background:#e23b3b"></span>הגדר של השדה (019m:S15_POLY) — סגור לשחקן בלי היתר <span style="background:#555"></span>המסלול ומסלול ההסעה B</p>
{EAST}
<table><tr><th></th><th>לפני</th><th>אחרי</th></tr>
<tr><td>inActiveRegion ב-G3 / H0–H3</td><td>false — החסימה 'WORLD' (סוף העולם) באמצע שדה מצויר</td><td>true — החסימה היא הגדר של השדה ('APT-AIRFIELD'), כמו ב-G0–G2</td></tr>
<tr><td>ACTIVE_REGIONS / MAP_ACTIVE_IDS</td><td>52 / 51</td><td>57 / 56 (הבדיקות 059:maps_cover… ו-073 — מ-51 ל-56)</td></tr>
<tr><td>כשהצד האווירי ייפתח (S16)</td><td>החצי המזרחי חסום (סוף העולם)</td><td>פתוח כמו המערבי — לפי הגדר וההיתר בלבד</td></tr></table>
<p class="mut">‎#ffeast=0 (או ‎?ffeast=0) — בדיוק כמו קודם, להשוואה.</p>
</main></body></html>'''
open(out, 'w', encoding='utf-8').write(html); print('ok', len(html.encode()))
