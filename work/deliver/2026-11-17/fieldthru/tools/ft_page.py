# -*- coding: utf-8 -*-
# ft_page.py <result.json> <world.json> <out.html> [measure.json] — fieldthru: דף הציור (כלל 13 / 17 — SVG בקוד, בלי תמונות): המספרים, טבלת המנגנונים של הישן,
# מפת השדה עם המסלולים של הטיסות החדשות, הלוח של המחזור (לכל עמדה) וציר המסלול
import sys, json, math, html, ft_sim as F
R = json.load(open(sys.argv[1], encoding='utf-8')); Wj = json.load(open(sys.argv[2], encoding='utf-8')); outp = sys.argv[3]
MEAS = json.load(open(sys.argv[4], encoding='utf-8')) if len(sys.argv) > 4 else None
M = F.M; T = F.T
old = [F.actor(o) for o in Wj['flights']]; new = [F.actor(o) for o in R['flights']]; ALL = old + new
newids = {a.id for a in new}
E = html.escape
def svg_map():
    X0, Y0, X1, Y1 = 4700, -900, 9700, 2650; Wpx = 1000; k = Wpx / (X1 - X0); Hpx = int((Y1 - Y0) * k)
    sx = lambda x: (x - X0) * k; sy = lambda y: (y - Y0) * k
    o = ['<svg viewBox="0 0 %d %d" class="map" role="img" aria-label="מפת השדה">' % (Wpx, Hpx)]
    o.append('<rect x="0" y="0" width="%d" height="%d" class="grass"/>' % (Wpx, Hpx))
    S = Wj['stands']
    def rect(r, cls, rx=0):
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="%s" rx="%d"/>' % (sx(r[0]), sy(r[1]), (r[2] - r[0]) * k, (r[3] - r[1]) * k, cls, rx)
    o.append(rect([4810, -55, 9163, 1033], 'apron')); o.append(rect([7205, 1925, 9544, 2545], 'apron'))
    o.append(rect([6000, 1033, 9163, 1210], 'term'))
    o.append(rect(F.RWY, 'rwy')); o.append(rect([4900, -285, 9450, -55], 'twy')); o.append(rect([9325, -170, 9475, 1925], 'twy')); o.append(rect([7259, 1775, 9475, 1925], 'twy'))
    for nm, x in (('A1', 5250), ('A2', 7150), ('A3', 9190)):
        o.append(rect([x - 100, -570, x + 100, -285], 'twy'))
        o.append('<text x="%.1f" y="%.1f" class="lbl">%s</text>' % (sx(x), sy(-500), nm))
    o.append('<text x="%.1f" y="%.1f" class="lbl">A</text><text x="%.1f" y="%.1f" class="lbl">B</text><text x="%.1f" y="%.1f" class="lbl">C</text>' % (sx(6000), sy(-150), sx(9400), sy(900), sx(8000), sy(1870)))
    act = {q[0] for q in Wj['sched']} | {q[0] for q in R['sched']}
    for sid, s in S.items():
        cls = 'st new' if ('FL-' + sid) in newids else ('st act' if sid in act else 'st')
        o.append(rect(s['rect'], cls, 2)); o.append('<text x="%.1f" y="%.1f" class="sl">%s</text>' % (sx(s['cx']), sy((s['rect'][1] + s['rect'][3]) / 2), sid))
    # המסלולים של הטיסות החדשות (קו האף)
    for a in new:
        pts = []
        for g in a.legs:
            if g.get('z0', 0) > 0 or g.get('z1', 0) > 0: pts.append(None); continue
            for p in g['p']: pts.append(p)
        segs = []; cur = []
        for p in pts:
            if p is None:
                if len(cur) > 1: segs.append(cur)
                cur = []
            else: cur.append(p)
        if len(cur) > 1: segs.append(cur)
        for sg in segs:
            o.append('<polyline points="%s" class="route"/>' % ' '.join('%.1f,%.1f' % (sx(p[0]), sy(p[1])) for p in sg if X0 <= p[0] <= X1))
    o.append('</svg>'); return '\n'.join(o)
def phases(a):
    # לכל טיסה: הקטעים במחזור — דחיפה, הסעה, המתנה בקו, מסלול / אוויר, הסעה פנימה, עמידה
    out = []
    for g in a.legs:
        if g.get('att'): continue
        if g.get('h') is not None: kind = 'park' if g.get('f') == 0 else 'wait'
        elif g.get('r'): kind = 'push'
        elif g.get('z0', 0) > 0 or g.get('z1', 0) > 0: kind = 'air'
        else: kind = 'taxi'
        out.append((g['t0'], g['t1'], kind))
    return out
def svg_gantt():
    rows = sorted(ALL, key=lambda a: (a.id not in newids, a.home)); H = 18; W0 = 90; Wd = 900; Hpx = H * (len(rows) + 2) + 30
    o = ['<svg viewBox="0 0 %d %d" class="gantt" role="img" aria-label="הלוח של המחזור">' % (W0 + Wd + 10, Hpx)]
    sx = lambda t: W0 + (t % T) / T * Wd
    for t in range(0, T + 1, 60):
        o.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d" class="grid"/><text x="%.1f" y="%d" class="tick">%d</text>' % (W0 + t / T * Wd, W0 + t / T * Wd, Hpx - 18, W0 + t / T * Wd, Hpx - 4, t))
    for i, a in enumerate(rows):
        y = 4 + i * H
        o.append('<text x="%d" y="%d" class="rl%s">%s · %s</text>' % (W0 - 6, y + 12, ' nw' if a.id in newids else '', a.home, a.model.replace('AC-', '').replace('-01', '')))
        for t0, t1, kind in phases(a):
            a0, a1 = t0 % T, (t0 % T) + (t1 - t0)
            for b0, b1 in ([(a0, min(a1, T))] + ([(0, a1 - T)] if a1 > T else [])):
                o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" class="g %s"/>' % (W0 + b0 / T * Wd, y + 2, max(.6, (b1 - b0) / T * Wd), H - 5, kind))
    y = 4 + len(rows) * H
    o.append('<text x="%d" y="%d" class="rl">המסלול</text>' % (W0 - 6, y + 12))
    for a in ALL:
        for w in F.flight_rwy_wins(a):
            o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" class="g rwy%s"/>' % (W0 + (w[0] % T) / T * Wd, y + 2, max(.8, (w[1] - w[0]) / T * Wd), H - 5, ' nwr' if a.id in newids else ''))
    o.append('</svg>'); return '\n'.join(o)
MECH = [
 ('AO.B — טבלת שמירה במרחב־זמן (044_core.js: aoCommit / aoFreeK; DT 0.25, מרווח M 6)', 'שום מטוס או רכב לא נוגע באחר — כל רגל נבדקת מול כל מה שכבר שמור', 'חלקי: s15_sim.py בודק רק אחרי (ac_conflict); לרכבים — s15k (074r)', 'ft_sim.py: Occ — טבלת שמירה (רסטר 16 פיקס׳ × שנייה) של כל השדה כפי שהוא רץ במשחק; ההכרעה — בדיקה מדויקת OBB כל 0.25 ש׳ (exact_flight)'),
 ('aoSearch / aoSearchG — הזמן הפנוי הראשון, קפיצה מעל קטע חסום', 'תזמון בלי חפיפה; תור במקום ביטול', 'לא: s15_sim.schedule מנסה כל 12 ש׳ ולוקח את הראשון', 'shifts_conflict: כל ההזזות בבת אחת (720), ובחירה לפי ההמתנה הקצרה'),
 ('aoHold / aoHoldLimit / aoCommitHold — המתנה במקום (בעמדה, בקו ההמתנה)', 'התור למסלול, העמידה בזמן השירות', 'חלקי: takeoff מחכה בקו ההמתנה עד 200 ש׳, בלי לבדוק שהמקום פנוי בזמן ההמתנה', 'free_prefix / seg_free: ההמתנה בקו ההמתנה ובעמדה נבדקת לכל שנייה; עד 45 ש׳ בקו'),
 ('AO.SEP — נעילת המסלול ±3 ש׳ סביב כל דגימה על הרצועה (aoSamp)', 'מרווח בין נחיתה להמראה', 'לא: "תפוס" כל רגל הגישה (10.8 ש׳) + 8 מכל צד — 58 ש׳ לזוג', 'הכלל של fieldcalc (הגובר): 3 ש׳ + 8 אחרי כבד, רק על המסלול — אותו SEP של הישן'),
 ('AO_ROLL — כניסה למסלול מחיבור באמצע לפי אורך הריצה של הסוג', 'הסעה קצרה, פחות זמן על המסלול', 'לא: כולם מ-A1, ויציאה רק ב-A3', 'dep1 / dep2 ‏link=A2 לסוגים שהריצה שלהם נכנסת; נחיתה עם יציאה ב-A2 (תוכנית האב F0: "יציאה מהירה באמצע")'),
 ('apttTaxi / apttVfn (042) — פרופיל ההסעה: vTaxi של הסוג, האצה 20, האטה 22, קשתות 34', 'קצב עבודה רגיל — לא "קפוא" (הבעלים, הביקורת סעיף 14)', 'לא: האטה אחת 60 → 18 לאורך כל הדרך (4 ק״מ)', 'prof_legs: אותם ערכים × 10 / 7.47 (הקנה של היום), רגליים בתאוצה קבועה (אותה צורה של רגל)'),
 ('apttTakeoff — הקשת אל המסלול ב-vArc 30', 'כניסה מהירה למסלול', 'לא: 18 → 22 (15–20 ש׳ על המסלול)', 'dep2: 18 → 40 — ההמראה תופסת את המסלול 12–15 ש׳'),
 ('apttVehMove — פרופיל הרכבים (האצה 18 / האטה 20, VMAX של הסוג)', 'רכבי שירות מהירים ומסונכרנים', 'כן — s15k (074r: s15kProfile + הסדר בלי חפיפה)', 'הגררים החדשים נכנסים לפני s15k (‏019l2) — עוברים את אותו s15kRun'),
 ('AF (afServeG / afCands, AF.GAP 2.5) — צי קבוע: רכב פנוי לכל משימה, משימה אחרי משימה', 'רכב אחד משרת כמה עמדות', 'לא: כל רכב — נסיעה קבועה אחת במחזור', 'tug_trip / trips_ok / veh_from_trips: PT-GA — נסיעה לכל טיסה של GA; גרר משלו לכל עמדה P'),
 ('G77_MLV (051: g77MlvPlan / g77MlvTug) — הגרירה לבדיקה אחרי טיפול, שוריינה במרחב־זמן ב-AO (aoSamp / aoFreeK / aoCommit)', 'הגרירה לא נוגעת בתנועה', 'לא: הגרירות של R3 (fieldfix, ‏074zo:FFR3) בזמנים קבועים — ונבדקות רק אחרי (fieldfix_r3)', 'tow_search: אחרי הלוח — לכל אחד מהשלושה הדקה הקרובה ל-18:00 / 18:10 / 04:45 שבה כל הדרך פנויה (±6 ש׳); מוחל בטעינה (074zv ← FTS.add.r3). המטוס של הלילה ב-R3 — מכשול קבוע לכל המחזור'),
 ('g77SvcPlan + G77_AC.svc — השירותים של כל סוג, בזמנים מהחסימה', 'אף שירות לא נשכח', 'המטריצה של fieldcalc + המדידה __TC_FC.svc', 'בשלב הזה: גרר לכל טיסה חדשה; שאר השירותים לטיסות החדשות — השלב הבא (מה נשאר)'),
 ('G77_BW / G77_BX — עבודת הכבודה (מסוע / ביד), 2.2–3.5 ש׳ למזוודה', 'העמסה בקצב', 'כן — 074r2 (s15bag)', 'בלי שינוי'),
 ('aoInit / aoStep — מתכנן חי בזמן המשחק (ביקוש 0.6)', 'לוח שמשתנה', 'לא: S15SIM מחזורי מראש — כל המערכות של השדה (השרוולים, הדלתות, הלוחות, s15k) בנויות עליו', 'לא מביאים את החי; מביאים את האלגוריתם — במחולל, שמייצר את הלוח המחזורי'),
]
IDLE_WHY = {'P6': 'LG — מתנגש בדחיפה / בהסעה עם P1 (0 אפשרויות יציאה); בינוני / מנהלים — בקו העצירה של fieldcalc (6–16 מ׳ אחורה) אחרי השרוולים לכל סוג (074zr2 של fieldcalc, בגל הבא)',
            'C1': 'CG / TB — הדחיפה מול P1 (LG) וגרר PT-C עסוק עם FL-C2', 'R1': 'הדחיפה עוברת על המטוס החונה ב-GA7 (PK-GA7) / על הכיס של BT-R', 'GA4': 'B / C והמסלול — עם R1 (מנהלים) אין חלון לנחיתה', 'P6': 'RJ / NB בקו העצירה של fieldcalc נכנסים בלוח (try7411 — 14 טיסות), אבל השרוול של P6 לא מגיע בעצירה הזו — אחרי 074zr2 (נכנס ב-S7F302) — בדיקה חוזרת',
            'R3': 'בלילה — הרצת המנועים של fieldfix (FFR3) עומדת ב-R3 כל המחזור (הבדיקה fieldfix_r3)', 'GA5': 'C / B והמסלול — אין חלון לנחיתה (B — מסלול הסעה יחיד לשני הכיוונים)',
            'GA7': 'C / B והמסלול — אין חלון לנחיתה', 'CH': ''}
def idle_note():
    act = {a.home for a in ALL}; idle = [k for k in Wj['stands'] if k not in act and k != 'CH']
    return '<p class="note">עמדות בלי טיסה (הבעלים ~10:05: "כל העמדות פעילות" — השלב הבא, עם העמדות של fieldcalc): ' + ' · '.join(E(k + (' — ' + IDLE_WHY[k] if IDLE_WHY.get(k) else '')) for k in idle) + '</p>' if idle else ''
def page():
    nf = len(ALL); mv = round(2 * nf * 1800 / T, 1)
    rows = []
    for a in new:
        ps = phases(a); park = [p for p in ps if p[2] == 'park']; pk = park[-1][1] - park[-1][0] if park else 0
        w = [p for p in ps if p[2] == 'wait']; hold = w[-1][1] - w[-1][0] if len(w) > 1 else 0
        dep = a.legs[0]['t0'] % T; land = [g for g in a.legs if g.get('z0', 0) > 0 and g.get('z1', 1) == 0]
        rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%.0f</td><td>%.0f</td><td>%s</td><td>%.0f</td></tr>' % (a.home, a.model, E(getattr(a, 'airline', '')), dep, hold, '%.0f' % (land[0]['t1'] % T) if land else '—', pk))
    mrows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(E(x) for x in r) for r in MECH)
    meas = ''
    if MEAS:
        meas = '<p class="note">במשחק (__TC_FC.moves(1800)): ' + E(json.dumps(MEAS, ensure_ascii=False)) + '</p>'
    css = '''
:root{--bg:#f6f4ef;--fg:#1d2329;--mut:#5b6670;--card:#fff;--line:#d9d4c8;--grass:#c9dcb5;--apron:#d8d6d0;--twy:#b9b6ae;--rwy:#55595e;--term:#9fb3c4;--st:#ecebe6;--act:#f2d9a6;--new:#ffb347;--route:#d2462f;--push:#7a5ba8;--taxi:#3c8dbc;--wait:#e0a100;--air:#8fc1e3;--park:#9aa5ad;--rwyb:#2c3338;--nwr:#d2462f}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16191d;--fg:#e6e8ea;--mut:#9aa3ab;--card:#1f2327;--line:#353b41;--grass:#2c3a27;--apron:#3a3d40;--twy:#4a4d50;--rwy:#202326;--term:#33475a;--st:#2b2f33;--act:#5d4a24;--new:#b86e14;--route:#ff7b61;--rwyb:#cfd5da}}
:root[data-theme="dark"]{--bg:#16191d;--fg:#e6e8ea;--mut:#9aa3ab;--card:#1f2327;--line:#353b41;--grass:#2c3a27;--apron:#3a3d40;--twy:#4a4d50;--rwy:#202326;--term:#33475a;--st:#2b2f33;--act:#5d4a24;--new:#b86e14;--route:#ff7b61;--rwyb:#cfd5da}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,"Segoe UI",Arial,sans-serif}
main{max-width:1060px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:4px 0 2px}h2{font-size:17px;margin:22px 0 8px}
.kp{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}.kp div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-width:120px}.kp b{display:block;font-size:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}th{color:var(--mut);font-weight:600}
svg{width:100%;height:auto;display:block}.grass{fill:var(--grass)}.apron{fill:var(--apron)}.twy{fill:var(--twy)}.rwy{fill:var(--rwy)}.term{fill:var(--term)}
.st{fill:var(--st);stroke:var(--line)}.st.act{fill:var(--act)}.st.new{fill:var(--new)}.sl{font-size:10px;text-anchor:middle;fill:var(--fg)}.lbl{font-size:12px;font-weight:700;text-anchor:middle;fill:var(--fg)}
.route{fill:none;stroke:var(--route);stroke-width:1.4;opacity:.75}
.grid{stroke:var(--line);stroke-width:.6}.tick{font-size:9px;fill:var(--mut);text-anchor:middle}.rl{font-size:10px;text-anchor:end;fill:var(--mut)}.rl.nw{fill:var(--fg);font-weight:700}
.g.push{fill:var(--push)}.g.taxi{fill:var(--taxi)}.g.wait{fill:var(--wait)}.g.air{fill:var(--air)}.g.park{fill:var(--park);opacity:.55}.g.rwy{fill:var(--rwyb)}.g.rwy.nwr{fill:var(--nwr)}
.lg{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--mut);margin:6px 0}.lg i{display:inline-block;width:12px;height:10px;margin-inline-end:4px;vertical-align:middle}
.note{color:var(--mut);font-size:13px}
@media (max-width:600px){h1{font-size:19px}.kp div{min-width:90px}}
'''
    return '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>לוח הטיסות בשדה</title><style>%s</style></head><body><main>
<h1>השדה — הרבה יותר טיסות (fieldthru, ‏17.11)</h1>
<p class="note">ציור בקוד (SVG), בלי תמונות. הנתונים — מהמחולל (ft_sim.py) על הסימולציה של המשחק, ובדיקה מדויקת של כל מטוס מול כל מטוס, רכב וחונה.</p>
<div class="kp"><div>הישן (S7F272)<b>44–45</b>תנועות מסלול ב-1800 ש׳</div><div>היום (S7F302)<b>35</b>7 טיסות במחזור</div><div>אחרי<b>%s</b>%d טיסות במחזור</div><div>פי<b>%.2f</b>מהישן</div><div>עמדות פעילות<b>%s</b>מתוך 19 (היעד: כולן)</div></div>
%s
<h2>המנגנונים של המנוע הישן → מה פתרו → יש בחדש? → איך הובאו</h2><div class="card"><table><tr><th>מנגנון ישן</th><th>מה פתר</th><th>יש בחדש?</th><th>איך מביאים / משדרגים</th></tr>%s</table></div>
<h2>המפה — העמדות והמסלולים של הטיסות החדשות</h2><div class="card">%s<div class="lg"><span><i style="background:var(--new)"></i>עמדה עם טיסה חדשה</span><span><i style="background:var(--act)"></i>טיסה של היום</span><span><i style="background:var(--route)"></i>הדרך של טיסה חדשה (על הקרקע)</span></div></div>
<h2>הלוח של המחזור (720 ש׳ = 6 שעות משחק)</h2><div class="card">%s<div class="lg"><span><i style="background:var(--push)"></i>דחיפה</span><span><i style="background:var(--taxi)"></i>הסעה</span><span><i style="background:var(--wait)"></i>המתנה (המנועים / קו ההמתנה)</span><span><i style="background:var(--air)"></i>מסלול / אוויר</span><span><i style="background:var(--park)"></i>עמידה</span><span><i style="background:var(--nwr)"></i>המסלול — טיסה חדשה</span></div></div>
<h2>הטיסות החדשות</h2><div class="card"><table><tr><th>עמדה</th><th>דגם</th><th>חברה</th><th>דחיפה (ש׳ במחזור)</th><th>המתנה בקו</th><th>נגיעה</th><th>עמידה (ש׳)</th></tr>%s</table></div>
<p class="note">לאישורך: זמני העמידה המינימליים (צר 330, ‏LG ‏360, אזורי 300, קלים 150 ש׳ — הטיסות של היום עומדות 311–420); ההסעה במהירות של הישן; ההמראה מ-A2 ויציאה ב-A2 לסוגים שהריצה שלהם נכנסת; הפנייה של הגדול אל A1 בשתי קשתות.</p>
</main></body></html>''' % (css, mv, nf, mv / 44.5, '%d' % len({a.home for a in ALL} - {'CH'}), meas + idle_note(), mrows, svg_map(), svg_gantt(), ''.join(rows))
open(outp, 'w', encoding='utf-8').write(page())
print('ok', outp)
