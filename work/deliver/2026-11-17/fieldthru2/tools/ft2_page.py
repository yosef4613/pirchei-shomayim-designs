# -*- coding: utf-8 -*-
# ft2_page.py <world.json> <var.json> <exp_dir> <out.html> [probe.json] — fieldthru2: דף הציור (כלל 13 / 17 — SVG בקוד, בלי תמונות):
# 18 העמדות (מה נכנס לפי גודל, פעילה?, למה לא, מה צריך), המגוון בכל עמדה בשעה, מטוס המשא הענק על C1 + C2, והדרך ל-88–92 (מה כל שינוי מוסיף — במחולל)
import sys, os, json, re, html
W = json.load(open(sys.argv[1], encoding='utf-8')); V = json.load(open(sys.argv[2], encoding='utf-8')); EXP = sys.argv[3]; outp = sys.argv[4]
PROBE = json.load(open(sys.argv[5], encoding='utf-8')) if len(sys.argv) > 5 and os.path.exists(sys.argv[5]) else None
SEQ = None
if os.environ.get('FT2_SEQ') and os.path.exists(os.environ['FT2_SEQ']):
    _S = json.load(open(os.environ['FT2_SEQ'], encoding='utf-8'))
    SEQ = {x['stand']: [(x['vars'][j] or {'ac': x['base']})['ac'] for j in x['seq']] for x in _S['seqs'].values()}
SM = json.load(open('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldcalc/tools/stands_matrix.json', encoding='utf-8'))
E = html.escape
CODE = lambda m: m[3:5]
TY = {t['m']: t for t in SM['types']}
CLS = {'AC-PR-01': 'GA', 'AC-LT-01': 'GA', 'AC-BJ-01': 'EXEC', 'AC-CN-01': 'EXEC', 'AC-AM-01': 'AMPH', 'AC-TB-01': 'CARGO', 'AC-TP-01': 'REG', 'AC-RJ-01': 'REG', 'AC-QJ-01': 'REG', 'AC-NB-01': 'NB', 'AC-MW-01': 'WIDE', 'AC-CG-01': 'CARGO', 'AC-LG-01': 'XL', 'AC-HC-01': 'CARGO'}
GROUP_OK = {'P': {'REG', 'NB', 'WIDE', 'XL'}, 'C': {'CARGO'}, 'R': {'REG', 'NB', 'EXEC'}, 'G': {'GA', 'EXEC'}}
SIZE = {'AC-PR-01': 1, 'AC-LT-01': 1, 'AC-AM-01': 1, 'AC-BJ-01': 2, 'AC-CN-01': 2, 'AC-TB-01': 2, 'AC-TP-01': 3, 'AC-RJ-01': 3, 'AC-QJ-01': 3, 'AC-NB-01': 4, 'AC-MW-01': 5, 'AC-CG-01': 5, 'AC-LG-01': 6, 'AC-HC-01': 6}
SZC = {1: '#7fb069', 2: '#4f9d9a', 3: '#3c78b4', 4: '#6a5acd', 5: '#c0732a', 6: '#b8323b'}
SZN = {1: 'קל / פרטי', 2: 'מנהלים / משא קטן', 3: 'אזורי', 4: 'צר-גוף', 5: 'גדול (רחב-גוף / משא)', 6: 'ענק'}
HE = {t['m']: t['he'] for t in SM['types']}; HE['AC-HC-01'] = 'משא ענק'
ORDER = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'C1', 'C2', 'R1', 'R2', 'R3', 'GA1', 'GA2', 'GA3', 'GA4', 'GA5', 'GA6', 'GA7']
act = {q[0]: q for q in W['sched']}
def exp(n):
    p = os.path.join(EXP, n + '.log')
    if not os.path.exists(p): return None
    s = open(p, encoding='utf-8').read(); m = re.search(r'טיסות (\d+) · תנועות מסלול ב-1800 ש׳ ([\d.]+)', s)
    lines = [l for l in s.splitlines() if re.match(r'^(P|R|GA|C)\d', l)]
    return dict(n=int(m.group(1)), mv=float(m.group(2)), lines=lines) if m else dict(n=None, mv=None, lines=lines)
X = {k: exp(k) for k in ('e1_p6', 'e2_r3', 'e3_ga', 'e4_ga_b2', 'e5_all')}
def mv(k): return ('%.0f' % X[k]['mv']) if X.get(k) and X[k].get('mv') is not None else '…'
VAR = {r['stand']: r for r in V.values()}
VL = {r['stand']: r for r in json.load(open(os.environ['FT2_VAR_LOOSE'], encoding='utf-8')).values()} if os.environ.get('FT2_VAR_LOOSE') else VAR
BR = {}
if PROBE:
    for r in PROBE.get('rows', []): BR[(r['stand'], r['ac'])] = r
def fits(sid): return [m for m, r in SM['stands'].get(sid, {}).get('row', {}).items() if r.get('ok')]
def by_size(sid): return sorted([m for m in fits(sid) if CLS.get(m) in GROUP_OK.get(sid[0], set())], key=lambda m: SIZE.get(m, 0))
def chip(m, cls=''):
    return '<span class="ch %s" style="--c:%s" title="%s">%s</span>' % (cls, SZC[SIZE.get(m, 3)], E(HE.get(m, m)), CODE(m))
# ---- הסבב המוצע לכל עמדה (5 סבבים = שעה של משחק אמיתי; 720 ש׳ = 6 שעות שעון המשחק)
def seq_of(sid):
    if SEQ is not None:
        if sid in SEQ: return SEQ[sid]
        q = act.get(sid)
        return [q[1]] * 4 if q else None
    D0 = {'P1': ['AC-LG-01', 'AC-NB-01', 'AC-LG-01', 'AC-QJ-01', 'AC-RJ-01'], 'P2': ['AC-NB-01', 'AC-RJ-01', 'AC-NB-01', 'AC-QJ-01', 'AC-NB-01'], 'P3': ['AC-NB-01', 'AC-QJ-01', 'AC-NB-01', 'AC-RJ-01', 'AC-NB-01'],
          'P5': ['AC-RJ-01', 'AC-NB-01', 'AC-QJ-01', 'AC-RJ-01', 'AC-TP-01'], 'R2': ['AC-NB-01', 'AC-BJ-01', 'AC-NB-01', 'AC-CN-01', 'AC-NB-01'], 'GA2': ['AC-LT-01', 'AC-PR-01', 'AC-LT-01', 'AC-PR-01', 'AC-LT-01'], 'P6': ['AC-RJ-01'] * 5}
    if sid in D0: return D0[sid]
    q = act.get(sid)
    if not q: return None
    base = q[1]; ok = [v['ac'] for v in VAR.get(sid, {}).get('ok', [])]
    if not ok: return [base] * 5
    s = [base]; i = 0
    while len(s) < 5:
        s.append(ok[i % len(ok)] if len(s) % 2 == 1 or len(ok) > 2 else base); i += 1
    return s
REASON = {
 'P4': ('פעילה — סוג אחד', 'מחזור התחזוקה של fieldfix (074zp2): הטיסה מחליפה מטוס עם האנגר א׳ — אותו דגם (RJ). מגוון כאן — רק אם גם מטוס ההאנגר מתחלף.'),
 'GA1': ('פעילה — סוג אחד', 'מחזור התחזוקה (האנגר ב׳ — BJ).'),
 'GA6': ('פעילה — סוג אחד', 'מחזור התחזוקה (האנגר ג׳ — LT).'),
 'C2': ('פעילה — סוג אחד', 'טיסת המשא של 074p (FL-C2, ‏TB) עם רכבת הכבודה TG-C בשני ביקורים — משא בלבד; פעם ביום משחק מתפנה למטוס המשא הענק (למטה).'),
 'C1': ('פעילה — סוג אחד', 'CG (מטען סילון) לא נכנס בחלון: העמידה קצרה מ-340 ש׳ ונוגע ב-FL-R2 בהסעה — השלב הבא: חלון אחר ל-C1. פעם ביום משחק — המשא הענק על C1 + C2.'),
 'R1': ('פעילה — סוג אחד', 'BJ / TP / RJ: העמידה קצרה (הדחיפה של R1 צמודה לנגיעה) או נוגע ב-FL-GA1 / ‏FL-R2 בדרך. השלב הבא: חלון אחר ל-R1.'),
 'GA3': ('פעילה — סוג אחד', 'LT: העמידה קצרה / נוגע ב-FL-R1 בדרך — השלב הבא.'),
 'P6': ('לא פעילה — נבנתה, לא במיזוג הזה', 'במחולל ‏RJ ב-P6 נכנס (14 טיסות, %s תנועות), ונבנה במשחק (try8092). אבל שתי בדיקות נכשלו: s15pax — התור לשרוול ב-P6 עם RJ בקו העצירה שלו (80 פיקס׳ אחורה), ו-fc_bridge_types — הבדיקה של fieldcalc מודדת את הסוג בקו של העמדה ולא בקו של הסוג. לכן במיזוג הזה P6 נשארת בלי טיסה; התיקון — השלב הבא. השרוול עצמו עוגן ב-RJ בקו שלו (נמדד, ft2_probe.js).'),
 'R3': ('לא פעילה', 'בלילה (20:30–04:25) מטוס מההאנגרים מריץ בה מנועים (fieldfix, ‏074zo) — והלילה ארוך ממחזור, ולכן היא תפוסה בכל המחזור. גם כשהיא פנויה (e2: בלי מטוס הלילה) — אין חלון: ההסעה אליה נוגעת בתנועה על B / C (17,201 התנגשויות בחיפוש). צריך: הרצת המנועים במקום אחר (fieldfix) + קישור שני לדרום.'),
 'GA4': ('לא פעילה', 'B הוא הקישור היחיד בין הדרום לצפון: כל טיסה לדרום עוברת עליו פעמיים, והוא תפוס (fieldcalc: ‏78% בלוח המלא). במחולל (e3) — אין חלון: ההסעה מהנגיעה לעמדה נוגעת בתנועה על B / C.'),
 'GA5': ('לא פעילה', 'כמו GA4. ובנתונים: הסוג של העמדה — מנהלים, אבל האף ב-y 2028 → רק קלים (fieldcalc).'),
 'GA7': ('לא פעילה', 'כמו GA5.'),
}
rows = []
for sid in ORDER:
    s = W['stands'][sid]; mx = s.get('type'); q = act.get(sid); sq = seq_of(sid)
    allowed = by_size(sid); ok = [v['ac'] for v in VAR.get(sid, {}).get('ok', [])]
    st, why = REASON.get(sid, ('פעילה — מגוון', ''))
    MULTI = {k for k in ORDER if len(set(seq_of(k) or [])) > 1}
    if sid in ('P2', 'R2', 'GA2') and sid not in MULTI:
        st = 'פעילה — סוג אחד'; why = 'יש גרסאות (' + ' '.join(CODE(v['ac']) for v in VL.get(sid, {}).get('ok', [])) + ') — אבל לא באותו רגע דחיפה ועצירה כמו בלוח: הכבודה, הנוסעים והשירות מתוזמנים לפיו בטעינה (בדיקת הכבודה של s15j). בזמן המדויק הן נוגעות ב-FL-R2 / ‏FL-C1 בקו ההמתנה.'
    if sid in MULTI:
        st = 'פעילה — מגוון'; why = '"אותו מסלול" — אותן רגליים, אותם זמנים ואותו גרר, רק הסוג (או גרסה באותו רגע דחיפה ועצירה); נבדק במדויק מול כל מה שרץ במשחק: ' + ' '.join(CODE(m) for m in ok)
        no = VAR.get(sid, {}).get('no', {})
        if no: why += ' · לא: ' + ' · '.join('%s — %s' % (CODE(k), v.split(' ·')[0][:70]) for k, v in no.items())
    if sid == 'P6' and '%s' in why: why = why % mv('e1_p6')
    bad_br = [CODE(m) for m in ok if (sid, m) in BR and not BR[(sid, m)].get('ok')]
    if bad_br: why += ' · השרוול בקו העצירה לא מגיע: ' + ' '.join(bad_br) + ' (יוצאים מהסבב)'
    rows.append('<tr class="%s"><td><b>%s</b></td><td>%s<br><span class="mut">%s</span></td><td class="chips">%s</td><td>%s</td><td class="chips">%s</td><td><span class="pill %s">%s</span></td><td class="why">%s</td></tr>' % (
        'idle' if st.startswith('לא') else '', sid, chip(mx) if mx else '—', E(SZN.get(SIZE.get(mx, 0), '')), ''.join(chip(m) for m in allowed),
        (chip(q[1]) + ' <span class="mut">' + E(q[2] or '') + '</span>') if q else '—', ''.join(chip(m) for m in sorted(set(sq or []), key=lambda m: -SIZE.get(m, 0))) if sq else '—',
        'ok' if st.startswith('פעילה — מגוון') else ('one' if st.startswith('פעילה') else ('in' if 'נכנסת' in st else 'no')), E(st), E(why)))
TABLE = '<table><thead><tr><th>עמדה</th><th>הגודל (הסוג של העמדה)</th><th>מה נכנס לפי גודל (fieldcalc, ‏stands_matrix; פרטי / מנהלים — לא ב-P1–P6)</th><th>היום (בלוח)</th><th>בסבב (שעה)</th><th>מצב</th><th>למה / מה צריך</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
# ---- רצועת המגוון: עמדה × 5 סבבים
def svg_strip():
    st = [s for s in ORDER if seq_of(s)]; H = 26; W0 = 60; CW = 120; Hp = H * len(st) + 34
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="הסוג בכל עמדה בכל סבב">' % (W0 + 4 * CW + 10, Hp)]
    for k in range(4): o.append('<text x="%d" y="16" class="tick">%s</text>' % (W0 + k * CW + CW // 2, ['00:00–06:00', '06:00–12:00', '12:00–18:00', '18:00–24:00'][k]))
    for i, sid in enumerate(st):
        y = 26 + i * H; o.append('<text x="%d" y="%d" class="rl">%s</text>' % (W0 - 8, y + 16, sid))
        for k, m in enumerate(seq_of(sid)):
            c = SZC[SIZE.get(m, 3)]; o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s" opacity=".9"/><text x="%d" y="%d" class="cl">%s</text>' % (W0 + k * CW + 4, y + 2, CW - 8, H - 6, c, W0 + k * CW + CW // 2, y + 16, E(CODE(m) + ' · ' + HE.get(m, m)[:14])))
    o.append('</svg>'); return '\n'.join(o)
# ---- המפה
def svg_map():
    X0, Y0, X1, Y1 = 4700, -900, 9800, 2650; Wpx = 1000; k = Wpx / (X1 - X0); Hpx = int((Y1 - Y0) * k)
    sx = lambda x: (x - X0) * k; sy = lambda y: (y - Y0) * k
    def rect(r, cls, rx=0, extra=''):
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="%s" rx="%d" %s/>' % (sx(r[0]), sy(r[1]), (r[2] - r[0]) * k, (r[3] - r[1]) * k, cls, rx, extra)
    o = ['<svg viewBox="0 0 %d %d" class="map" role="img" aria-label="מפת השדה — העמדות לפי מצב">' % (Wpx, Hpx), '<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2e9e44"/></marker></defs>', '<rect width="%d" height="%d" class="grass"/>' % (Wpx, Hpx)]
    o.append(rect([4810, -55, 9163, 1033], 'apron')); o.append(rect([7205, 1925, 9544, 2545], 'apron')); o.append(rect([6000, 1033, 9163, 1210], 'term'))
    o.append(rect([5000, -810, 9300, -570], 'rwy')); o.append(rect([4900, -285, 9450, -55], 'twy')); o.append(rect([9325, -170, 9475, 1925], 'twy')); o.append(rect([7259, 1775, 9475, 1925], 'twy'))
    for nm, x in (('A1', 5250), ('A2', 7150), ('A3', 9190)): o.append(rect([x - 100, -570, x + 100, -285], 'twy')); o.append('<text x="%.1f" y="%.1f" class="lbl">%s</text>' % (sx(x), sy(-480), nm))
    o.append('<text x="%.1f" y="%.1f" class="lbl">A</text><text x="%.1f" y="%.1f" class="lbl">B</text><text x="%.1f" y="%.1f" class="lbl">C</text><text x="%.1f" y="%.1f" class="lbl">המסלול 09 / 27</text>' % (sx(6600), sy(-140), sx(9400), sy(1450), sx(8200), sy(1880), sx(7150), sy(-700)))
    # ההצעות (גאומטריה — לאישור הבעלים): B2 לקלים לאורך הגדר המזרחית; מפרץ המתנה באמצע B (fieldcalc)
    o.append(rect([8245, -570, 8445, -285], 'appr')); o.append('<text x="%.1f" y="%.1f" class="al">A3 חדש (D‑701)</text>' % (sx(8345), sy(-600)))
    o.append(rect([9285, -170, 9325, 1925], 'appr')); o.append(rect([9475, -170, 9515, 1925], 'appr'))
    for x, up in ((9345, 1), (9455, 0)): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="lane" marker-end="url(#ar)"/>' % (sx(x), sy(1500 if up else 300), sx(x), sy(300 if up else 1500)))
    o.append('<text x="%.1f" y="%.1f" class="al" transform="rotate(-90 %.1f %.1f)">B — נתיב יוצא ↑ / נתיב נכנס ↓ (D‑701)</text>' % (sx(9580), sy(900), sx(9580), sy(900)))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="lane" marker-end="url(#ar)"/><text x="%.1f" y="%.1f" class="al">המראה הפוכה (27) — רק כשהמסלול והאוויר פנויים</text>' % (sx(9000), sy(-720), sx(5600), sy(-720), sx(7300), sy(-760)))
    for sid in ORDER + ['CH']:
        s = W['stands'][sid]; st = REASON.get(sid, ('פעילה — מגוון',))[0] if sid not in ('P1', 'P2', 'P3', 'P5', 'R2', 'GA2') else 'פעילה — מגוון'
        if sid == 'CH': continue
        cls = 'st ok' if st.startswith('פעילה — מגוון') else ('st one' if st.startswith('פעילה') else ('st in' if 'נכנסת' in st else 'st no'))
        o.append(rect(s['rect'], cls, 2)); o.append('<text x="%.1f" y="%.1f" class="sl">%s</text>' % (sx(s['cx']), sy((s['rect'][1] + s['rect'][3]) / 2), sid))
    r = W['stands']['CH']['rect']; o.append(rect(r, 'chp', 3)); o.append('<text x="%.1f" y="%.1f" class="pl">CH = C1 + C2 — משא ענק</text>' % (sx((r[0] + r[2]) / 2), sy(r[1]) - 4))
    o.append('</svg>'); return '\n'.join(o)
# ---- המשא הענק: ציר זמן של יום משחק (4 סבבים)
def svg_hc():
    Wp = 960; H = 150; o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="יום משחק — 4 סבבים, המשא הענק בסבב אחד">' % (Wp, H)]
    cw = (Wp - 80) / 4
    for k in range(4):
        x = 70 + k * cw; o.append('<text x="%.0f" y="16" class="tick">%s</text>' % (x + cw / 2, ['00:00–06:00', '06:00–12:00', '12:00–18:00', '18:00–24:00'][k]))
        for j, (sid, y) in enumerate((('C1', 30), ('C2', 62), ('CH', 94))):
            if k == 1:
                if sid == 'CH': o.append('<rect x="%.0f" y="%d" width="%.0f" height="24" rx="5" fill="%s"/><text x="%.0f" y="%d" class="cl">HC — משא ענק על שתי העמדות (שריון של שתיהן לכל העמידה)</text>' % (x + cw * .18, y, cw * .7, SZC[6], x + cw * .53, y + 16))
                else: o.append('<rect x="%.0f" y="%d" width="%.0f" height="24" rx="5" class="res"/><text x="%.0f" y="%d" class="cl2">משוריינת ל-HC (הטיסה של %s לא מגיעה בסבב הזה)</text>' % (x + 4, y, cw - 8, x + cw / 2, y + 16, sid))
            elif sid != 'CH':
                o.append('<rect x="%.0f" y="%d" width="%.0f" height="24" rx="5" fill="%s" opacity=".85"/><text x="%.0f" y="%d" class="cl">TB — משא קטן (כרגיל)</text>' % (x + 4, y, cw - 8, SZC[2], x + cw / 2, y + 16))
    for j, (sid, y) in enumerate((('C1', 30), ('C2', 62), ('CH', 94))): o.append('<text x="60" y="%d" class="rl">%s</text>' % (y + 16, sid))
    o.append('<text x="%d" y="140" class="tick">יום משחק = 4 סבבים של 720 ש׳ (6 שעות שעון המשחק כל אחד)</text>' % (Wp // 2)); o.append('</svg>'); return '\n'.join(o)
def svg_mw():
    # MW מול P3 — הנתיב והזמן, לא הגודל: הישן (A4) מול החדש (A2, כמו LG)
    X0, X1 = 5900, 9400; Wp = 960; k = Wp / (X1 - X0); sx = lambda x: (x - X0) * k; Y = {'rwy': 40, 'a': 120, 'st': 210}
    o = ['<svg viewBox="0 0 %d 300" role="img" aria-label="הנתיב של MW אל P1 — דרך A4 (עבר מול P3) ודרך A2 (כמו LG)">' % Wp]
    o.append('<rect x="0" y="%d" width="%d" height="26" class="rwyb"/><text x="%.0f" y="%d" class="cw">המסלול — הנחיתה מכיוון מערב (09)</text>' % (Y['rwy'] - 13, Wp, Wp / 2, Y['rwy'] + 5))
    o.append('<rect x="0" y="%d" width="%d" height="18" class="twyb"/><text x="12" y="%d" class="t2">A</text>' % (Y['a'] - 9, Wp, Y['a'] + 5))
    for nm, x in (('A2', 7150), ('A4 (ה-A3 של היום)', 9190)):
        o.append('<rect x="%.0f" y="%d" width="18" height="%d" class="twyb"/><text x="%.0f" y="%d" class="t2">%s</text>' % (sx(x) - 9, Y['rwy'] + 13, Y['a'] - Y['rwy'] - 22, sx(x) + 14, Y['rwy'] + 46, nm))
    for sid, cx, w in (('P1', 6399, 64.8), ('P2', 6977, 35.8), ('P3', 7380, 35.8), ('P4', 7783, 31.7), ('P5', 8186, 31.7), ('P6', 8764, 31.7)):
        o.append('<rect x="%.0f" y="%d" width="%.0f" height="60" rx="4" class="stb"/><text x="%.0f" y="%d" class="t2">%s</text>' % (sx(cx) - w * 10 * k / 2, Y['st'], w * 10 * k, sx(cx), Y['st'] + 36, sid))
    # P3 נדחפת (0–24 ש׳ במחזור)
    o.append('<path d="M%.0f,%d L%.0f,%d" class="push" marker-end="url(#ar2)"/><text x="%.0f" y="%d" class="t3">P3 נדחפת אל A (0–24 ש׳)</text>' % (sx(7380), Y['st'] - 4, sx(7380), Y['a'] + 10, sx(7380) + 8, Y['a'] + 40))
    # MW הישן: גלגול עד A4, ואז מערבה לאורך A — עובר מול P3 בדיוק כשהיא נדחפת
    o.append('<path d="M%.0f,%d L%.0f,%d L%.0f,%d L%.0f,%d L%.0f,%d" class="old" marker-end="url(#ar3)"/>' % (sx(6000), Y['rwy'], sx(9190), Y['rwy'], sx(9190), Y['a'] - 4, sx(6399), Y['a'] - 4, sx(6399), Y['st']))
    o.append('<text x="%.0f" y="%d" class="t4">MW — לפני: יוצא ב-A4, נוסע מערבה לאורך A, ועובר מול P3 ב-24 ש׳ — כשהיא נדחפת</text>' % (sx(8200), Y['a'] - 20))
    # MW עכשיו (= LG): יוצא ב-A2, מערבה אל P1 — לא עובר מול P3
    o.append('<path d="M%.0f,%d L%.0f,%d L%.0f,%d L%.0f,%d L%.0f,%d" class="new" marker-end="url(#ar4)"/>' % (sx(6000), Y['rwy'] + 6, sx(7150), Y['rwy'] + 6, sx(7150), Y['a'] + 4, sx(6420), Y['a'] + 4, sx(6420), Y['st']))
    o.append('<text x="%.0f" y="%d" class="t5">MW עכשיו — כמו LG: יוצא ב-A2 ומגיע ל-P1 בלי לעבור מול P3</text>' % (sx(6600), Y['st'] + 80))
    o.append('<defs><marker id="ar2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7a5ba8"/></marker><marker id="ar3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/></marker><marker id="ar4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2e9e44"/></marker></defs>')
    o.append('</svg>'); return '\n'.join(o)
# ---- 88–92
def opt_rows():
    def gx(n):
        p = os.path.join(EXP, n + '.log')
        if not os.path.exists(p): return '…'
        m = re.findall(r'טיסות (\d+) · תנועות מסלול ב-1800 ש׳ ([\d.]+)', open(p, encoding='utf-8').read()); return ('%.0f' % float(m[-1][1])) if m else '…'
    R = [('היום (S7F303 — try7412)', 'לא', '65', '13 טיסות, 13 / 18 עמדות'),
         ('P6 — טיסת RJ (בקו העצירה של fieldcalc) — נבנה (try8082)', 'לא', mv('e1_p6'), '14 טיסות, 14 / 18 עמדות'),
         ('R3 ביום — בלי מטוס הלילה (הרצת המנועים במקום אחר)', 'לא (של fieldfix)', mv('e2_r3'), 'אין חלון: ההסעה מהנגיעה אל R3 נוגעת בתנועה על B / C'),
         ('GA4 / GA5 / GA7 — כמו היום', 'לא', mv('e3_ga'), 'אין חלון: B / C — הקישור היחיד לדרום'),
         ('D‑701: ‏A3 החדש + המראה הפוכה (27) מ-A3 / A4 — מעל הלוח עם P6', 'כן — אושר', gx('x3_all_d701'), 'GA4 / GA5 / GA7 / R3 — עדיין אין חלון: הנחיתה לדרום (ההסעה מהיציאה דרך A המזרחי / B / C) נוגעת ב-6 הטיסות של הדרום'),
         ('D‑701 + שני נתיבים ב-B (יוצא / נכנס) — מעל הלוח עם P6', 'כן — אושר', gx('y2_all_lanes'), 'אותו דבר — הנתיבים עוזרים רק כשגם הטיסות של היום עוברות לנתיבים'),
         ('הדרום מחדש עם D‑701 (9 עמדות יחד, 4 סדרים)', 'כן — אושר', '65', 'רק 4 טיסות לדרום נכנסות (היום 5): בלי המתנה בדרך הנחיתה, C — נתיב אחד'),
         ('D‑701: הנוחתים יוצאים ב-A3 החדש (גלגול קצר ב-845 פיקס׳)', 'כן — אושר', '70', 'רק 4 מתוך 14 נכנסים בלי לגעת (P4 / P5 / C1 / P6); המסלול תפוס 61.7% → 60.2%'),
         ('כל הלוח מאפס במחולל של היום (16 עמדות, 2 סדרים, עם D‑701 ובלי)', '—', '50–60', 'המחולל החמדני (טיסה אחרי טיסה, בלי לחזור אחורה) ממלא פחות מהלוח של היום (14); צריך מתכנן עם חזרה אחורה'),
         ('תכנון מחדש של כל הלוח יחד (18 עמדות) עם D‑701', 'כן — אושר', 'השלב הבא', 'הזמנים של 14 הטיסות של היום קבועים — העוד 4 צריכות חלונות שנוצרים רק כשמתכננים הכול יחד'),
         ('LG / MW ב-P6 דרך A4 (27)', 'כן — אושר', '0 חלונות', '"פנוי לגמרי" (כל הבלוק + 10 ש׳) לא קורה כשהמסלול תפוס 58% ב-09'),
         ('מפרץ המתנה באמצע B (fieldcalc)', 'כן — לאישור', '95 (בחישוב של fieldcalc)', 'לא במחולל'),
         ('המשא הענק על C1 + C2 (פעם ביום משחק)', 'לא', '−2 בסבב שלו', 'לא נבנה בסבב הזה (CH לא נמדדה במטריצה של fieldcalc)')]
    return '<table><thead><tr><th>שינוי</th><th>שינוי גאומטריה?</th><th>תנועות מסלול ב-1800 ש׳ (במחולל)</th><th>הערה</th></tr></thead><tbody>' + ''.join('<tr><td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % tuple(E(x) for x in r) for r in R) + '</tbody></table>'
nact = sum(1 for s in ORDER if s in act); nvar = sum(1 for s in ORDER if len(set(seq_of(s) or [])) > 1)
CSS = ''':root{--bg:#f6f4ef;--fg:#1d2329;--mut:#5b6670;--card:#fff;--line:#d9d4c8;--grass:#c9dcb5;--apron:#d8d6d0;--twy:#b9b6ae;--rwy:#55595e;--term:#9fb3c4;--ok:#8cc084;--one:#f2d9a6;--in:#ffb347;--no:#e3a3a3;--prop:#e07b00;--res:#e9e4d8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16191d;--fg:#e6e8ea;--mut:#9aa3ab;--card:#1f2327;--line:#353b41;--grass:#2c3a27;--apron:#3a3d40;--twy:#4a4d50;--rwy:#202326;--term:#33475a;--ok:#3f6b39;--one:#5d4a24;--in:#9a5a10;--no:#6b3434;--prop:#ff9d2e;--res:#33373c}}
:root[data-theme="dark"]{--bg:#16191d;--fg:#e6e8ea;--mut:#9aa3ab;--card:#1f2327;--line:#353b41;--grass:#2c3a27;--apron:#3a3d40;--twy:#4a4d50;--rwy:#202326;--term:#33475a;--ok:#3f6b39;--one:#5d4a24;--in:#9a5a10;--no:#6b3434;--prop:#ff9d2e;--res:#33373c}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,"Segoe UI",Arial,sans-serif}main{max-width:1180px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:6px 0}h2{font-size:18px;margin:22px 0 8px}.mut{color:var(--mut);font-size:12px}
.kp{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}.kp div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-width:130px}.kp b{display:block;font-size:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}th{color:var(--mut);font-weight:600}
tr.idle td{background:color-mix(in srgb,var(--no) 18%,transparent)}td.why{font-size:12px;max-width:380px}
.ch{display:inline-block;min-width:24px;text-align:center;padding:1px 5px;margin:1px;border-radius:5px;background:var(--c);color:#fff;font-size:11px;font-weight:700}
.pill{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;white-space:nowrap}.pill.ok{background:var(--ok)}.pill.one{background:var(--one)}.pill.in{background:var(--in)}.pill.no{background:var(--no)}
svg{width:100%;height:auto;display:block}.grass{fill:var(--grass)}.apron{fill:var(--apron)}.twy{fill:var(--twy)}.rwy{fill:var(--rwy)}.term{fill:var(--term)}
.st{stroke:var(--line)}.st.ok{fill:var(--ok)}.st.one{fill:var(--one)}.st.in{fill:var(--in)}.st.no{fill:var(--no)}.sl{font-size:10px;text-anchor:middle;fill:var(--fg)}.lbl{font-size:12px;font-weight:700;text-anchor:middle;fill:var(--fg)}
.prop{fill:none;stroke:var(--prop);stroke-width:2;stroke-dasharray:6 4}.prop2{fill:var(--prop);opacity:.35;stroke:var(--prop);stroke-dasharray:4 3}.pl{font-size:11px;font-weight:700;fill:var(--prop);text-anchor:middle}
.appr{fill:#2e9e44;opacity:.45}.lane{stroke:#2e9e44;stroke-width:3}.al{font-size:11px;font-weight:700;fill:#1f7a33;text-anchor:middle}.rwyb{fill:var(--rwy)}.twyb{fill:var(--twy)}.stb{fill:var(--one);stroke:var(--line)}.cw{font-size:12px;fill:#fff;text-anchor:middle}.t2{font-size:12px;fill:var(--fg);text-anchor:middle;font-weight:700}.t3{font-size:11px;fill:#7a5ba8}.t4{font-size:12px;fill:#c0392b;text-anchor:middle;font-weight:700}.t5{font-size:12px;fill:#1f7a33;text-anchor:middle;font-weight:700}.push{stroke:#7a5ba8;stroke-width:3;fill:none}.old{stroke:#c0392b;stroke-width:3;fill:none;stroke-dasharray:8 5}.new{stroke:#2e9e44;stroke-width:3;fill:none}.chp{fill:none;stroke:#b8323b;stroke-width:2.5;stroke-dasharray:8 4}
.tick{font-size:11px;fill:var(--mut);text-anchor:middle}.rl{font-size:12px;text-anchor:end;fill:var(--fg);font-weight:700}.cl{font-size:11px;fill:#fff;text-anchor:middle;font-weight:600}.cl2{font-size:11px;fill:var(--fg);text-anchor:middle}.res{fill:var(--res);stroke:var(--line);stroke-dasharray:4 3}
.lg{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--mut);margin:6px 0}.lg i{display:inline-block;width:12px;height:10px;margin-inline-end:4px;vertical-align:middle;border-radius:2px}
ul{margin:4px 0;padding-inline-start:20px}li{margin:3px 0}
@media (max-width:640px){main{padding:10px 16px}td.why{max-width:none}}'''
LEG = ''.join('<span><i style="background:%s"></i>%s</span>' % (SZC[k], E(v)) for k, v in SZN.items())
page = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מגוון סוגים בעמדות</title><style>%s</style></head><body><main>
<h1>השדה: כל עמדה — כמה סוגים, כל העמדות פעילות, משא ענק, והדרך ל-88–92</h1>
<p class="mut">fieldthru2 · 17.11 · מעל t17_fieldthru ‏a7ef45d (S7F303). הבעלים 17.11: "3 סוגי מטוסים הענק ו2 גדולים … חברות תעופה מגוונות ולא כל פעם אותו מטוס מאותו חברה" · "העמדות הגדולות הם לא רק למטוסי ענק … צריך שכל העמדות יהיו פעילות" · (14:35) "בדיקה רצינית של כל מטוס בכל עמדה … לחשב עמדות לפי גודל — כמובן שפרטי לא יהיה ב-P1–6" · (14:40) "מטוס המשא הענק שיחנה על 2 העמדות יחד כשהם פנויים".</p>
<div class="kp"><div><b>%d / 18</b>עמדות עם טיסה היום</div><div><b>%d</b>עמדות עם כמה סוגים בשעה</div><div><b>65</b>תנועות ב-1800 ש׳ במיזוג הזה (עם P6 במחולל — %s)</div><div><b>44–45</b>הישן</div></div>
<h2>מה מצאתי</h2><div class="card"><ul>
<li>היום כל עמדה עם טיסה — סוג אחד: ‏019l2_ft_sched.js (fieldthru) קובע model + legs פעם אחת בטעינה; בכל סבב מתחלפת רק החברה (074zv:ftrAt).</li>
<li>מה שמחושב לפי הסוג בטעינה ונשמר: השרוול (המטמון S15GR.bpar של העמדה), הנוסעים (S15J.plan), המכוון (S15E.plans), הגרר (הנסיעה לפי זמן הדחיפה ומקום האף של הסוג), רכבי השירות (fieldsvc).</li>
<li>הכלי של fieldthru (ft_sim.py:variant_of) כבר מצא גרסאות לסוג אחר באותם חלונות מסלול — כאן הוא משודרג: אותו רגע בקו ההמתנה (לא יושב בקו כשאחרים עוברים), עצירה בעמדה עד 60 ש׳ אחרי הלוח, הגרר מתוכנן מחדש לכל גרסה, והכול נבדק מול כל מה שרץ במשחק (הטיסות, 35 הרכבים, החונים, המסוק).</li>
<li>CH כבר קיימת בנתונים (S15D.stands.CH, ‏AC-HC-01 — 69 × 73 מ׳) — חופפת ל-C1 + C2, ואף טיסה לא חונה בה. זה המקום של המשא הענק.</li></ul></div>
<h2>המפה — כל העמדות לפי מצב</h2><div class="card">%s<div class="lg"><span><i style="background:var(--ok)"></i>פעילה — כמה סוגים</span><span><i style="background:var(--one)"></i>פעילה — סוג אחד</span><span><i style="background:var(--in)"></i>נכנסת עכשיו (P6)</span><span><i style="background:var(--no)"></i>לא פעילה</span><span><i style="background:var(--prop)"></i>הצעה — שינוי גאומטריה, לאישור הבעלים</span><span><i style="background:#b8323b"></i>CH — שתי העמדות יחד</span></div></div>
<h2>18 העמדות — מה נכנס לפי גודל, פעילה?, למה לא, ומה צריך</h2><div class="card">%s<div class="lg">%s</div><p class="mut">"נכנס לפי גודל" — המטריצה של fieldcalc (stands_matrix.json: המעטפת בעמדה, הכיסים, קווי העצירה) ועוד הכלל של הבעלים: P1–P6 — אזורי / צר-גוף / רחב-גוף / ענק בלבד; C — משא; R — אזורי / צר-גוף / מנהלים; GA — קלים / מנהלים. "בסבב" — מה שעבר במחולל מול כל מה שרץ במשחק; ועמדת שרוול — רק סוג שהשרוול מגיע אליו בקו העצירה שלו.</p></div>
<h2>המגוון — הסוג בכל עמדה ביום משחק (4 סבבים)</h2><div class="card">%s<p class="mut">כל סבב (720 ש׳) — ביקור אחד: נחיתה, עמידה, דחיפה והמראה של אותו סוג. ההחלפה — רק כשהמטוס מחוץ לעולם (בין ההמראה לגישה, כמו החלפת החברה), כך שאף מטוס לא משתנה מול העיניים. עם כל סוג — מחדש: הנסיעה של הגרר, השרוול (האורך והמנוחה לסוג), הנוסעים (מספר לפי הסוג), המכוון. החברה ממשיכה להתחלף בכל סבב (מהמאגר של הסוג). הסבב מאומת לכל סבב במשחק (הבדיקה fieldthru_variety: כל סבב — 0 חפיפות, השרוול עוגן, הגרר צמוד).</p></div>
<h2>הגדולים (הבעלים 15:20) — LG / MW / CG ו-HC</h2><div class="card"><ul>
<li><b>P1 — LG ו-MW לסירוגין:</b> ‏00:00 ‏LG · ‏06:00 ‏MW · ‏12:00 ‏LG · ‏18:00 ‏MW — כל אחד פעמיים ביום משחק. נבדק במחולל סבב-סבב, כל הטיסות של הסבב יחד, וגם מול הרכבים.</li>
<li><b>הבעיה של MW עם P3 (הבעלים 17:35: "איך מטוס גדול … חוסם את P3, ולמה הענק לא חוסם?") — לא הגודל, אלא הנתיב והזמן:</b> MW יצא מהמסלול ב-A4 (הכלל של המחולל אסר על הגדולים — חוץ מ-LG — לצאת ב-A2). מ-A4 הוא נסע מערבה לאורך A, ועבר מול P3 בדיוק כשהיא נדחפת אל A (0–24 ש׳ במחזור). LG יוצא ב-A2 — ממערב ל-P3 — ולכן לא עובר שם. ב-P1 עצמה MW קטן מ-LG ונכנס בלי בעיה. עכשיו MW נוסע בדיוק בנתיב ובזמנים של LG ("אותו מסלול") — וזה נפתר. %s</li>
<li><b>מה בחרתי:</b> ‏MW ב-P1 יוצא מהמסלול ב-A2 (כמו LG; גלגול של 175 מ׳) במקום ב-A4. ההסעה שלו קצרה יותר, ולכן הוא כבר בעמדה כש-P3 נדחפת. "MW רק ב-P6" לא אפשרי: מ-P6 אין לו קו המראה. מ-A2 הגלגול קצר מדי; מ-A1 ההסעה חוצה את כל A (0 חלונות); ‏27 מ-A4 אף פעם לא "פנוי לגמרי".</li>
<li><b>הבינוניים בין הגדולים:</b> ב-P2 / P3 / P5 / P6 (צר-גוף / אזורי / 4 מנועים). ב-P1 אין להם מקום אם LG ו-MW צריכים להופיע פעמיים ביום (4 סבבים).</li>
<li><b>CG ב-C1 — לא בסבב הזה (גם בסבב משא בלי C2, ft2_cargo.py):</b> גם עם המתנה בדרך (plan_flight2) ויציאה ב-A2 — רק 5–10 אפשרויות דחיפה, והנחיתה נוגעת בתנועה בכל הזמנים. הסיבה הקודמת: ל-CG צריך לפחות 340 ש׳ עמידה, ובחלון של C1 ההסעה האיטית שלו מ-A4 משאירה פחות; וב-A2 הוא נוגע ב-FL-R2 בהסעה. צריך חלון אחר ל-C1 — השלב הבא.</li>
<li><b>HC (המשא הענק) — לא בסבב הזה:</b> מדדתי את CH בכלי של fieldcalc (ft2_ch.py — אותן בדיקות של fc_stands.check). במלבן שבנתונים (y 160–743) הוא לא נכנס: HC באורך 69 מ׳, והעמדה בעומק 58 מ׳. עם האף ב-y 940 הוא חוצה את הגדר של המשחק (y 725). בתוך הגדר — האף ב-y 715 לכל היותר, ואז הזנב ב-y 25: על A1, והכנף של LG על A מגיעה עד y 154. צריך: להזיז את הגדר של רחבת המשא דרומה עד y ~1000 (כמו D.FENCE) — לאישור הבעלים.</li>
<li><b>הגרר בעמדה הגדולה:</b> לכל סוג נוסע בשורה y 989, מדרום לאף — לא רק לענק. בשורה 864 הוא עבר מתחת לאף של סוג קטן יותר; נמצא בכלי ותוקן.</li><li><b>הגדולים גם ב-P6 (הבעלים 17:35) — נבדק בלו״ז, בלי שינוי גאומטריה:</b> מ-P6 לגדול יש רק המראה 27 מ-A4 / A3 החדש (09 מ-A1 — 0 חלונות; מ-A2 הגלגול קצר מדי). המראה הפוכה של גדול תופסת את המסלול ~16 ש׳ (הגלגול והטיפוס עד 12 מ׳), ועוד 10 ש׳ אחרי, ועוד 10 ש׳ מכל צד — "פנוי לגמרי". לכן צריך פער של 55–60 ש׳ בלי שום תנועה. בלוח של היום הפער הגדול ביותר 34.5 ש׳. הזזה של טיסה אחת (GA6 ב-8 ש׳ מוקדם) פותחת 42.5 ש׳ — עדיין לא מספיק (ft2_p6big.py, במחולל: 0 חלונות ל-LG ול-MW). הצעד הבא: להזיז שתי טיסות (למשל GA6 ו-P4) כך שייפתח פער של 60 ש׳ פעם במחזור — "חלון 27" קבוע, בלי לבטל אף תנועה. אם זה לא נכנס, החלופה היא לעצור נחיתה אחת בכל מחזור: ‎−5 תנועות ב-1800 ש׳.</li></ul></div>
<h2>מטוס המשא הענק — על C1 + C2 יחד (CH)</h2><div class="card">%s<ul>
<li><b>הזוג:</b> C1 + C2 (רחבת המשא המערבית) — העמדה המשותפת CH כבר בנתונים (x 4810–5690), עם קו עצירה אחד באמצע (האף ב-y 940), בלי שרוול. שאר הזוגות: P1 + P2 / P5 + P6 — שרוולים וטרמינל באמצע; R1 + R2 — רחוקות מ-B ובלי מקום לזנב של 69 מ׳ — לא.</li>
<li><b>מתי:</b> פעם ביום משחק — בסבב 06:00–12:00 (ברירת המחדל, לאישורך: פעמיים ביום = −4 תנועות). שתי העמדות משוריינות לכל העמידה; הטיסות של C1 ושל C2 לא מגיעות בסבב הזה (המטוסים שלהן "בדרך"), ורכבי השירות שלהן נשארים בבית — חוץ מאלה של HC.</li>
<li><b>התנועות:</b> בסבב של HC — 2 תנועות במקום 4 (−2). בחלון של 1800 ש׳ שעובר עליו: 63 במקום 65 (או 68 במקום 70 עם P6).</li>
<li><b>הדגם:</b> AC-HC-01 בקטלוג המטוסים (TurboCity; נבדק בדפדפן לפני הבנייה) — אם לא מצויר, דגם חדש בקוד באותו סגנון.</li>
<li><b>השירות שלו</b> (מעמיס מכולות, עגלות, גרר, דלק) — של fieldsvc: מקבל את חלון העמידה ואת המקום (CH) מהממשק FTV.</li></ul></div>
<h2>הדרך ל-88–92 — מה כל שינוי מוסיף (במחולל, מעל הלוח של היום)</h2><div class="card">%s<p class="mut"><b>מה המחולל מראה:</b> עם 14 טיסות המסלול תפוס 58%% (26 חלונות במחזור). הפער הממוצע בין חלונות (~12 ש׳) קצר מחלון נחיתה עם המרווחים (3 ש׳ + 8 אחרי כבד), ולכן עוד נחיתות לא נכנסות — גם עם D‑701, המתנה בדרך ושני נתיבים ב-B וב-C. הדרך ל-88–92: לקצר את הזמן של כל תנועה על המסלול (יציאה מהירה בזווית; כל הנוחתים יוצאים ב-A3 החדש), ואז הנתיבים של B / C. (fieldcalc חישב עד 131 תנועות למסלול לבד — בלי ההסעה.) המגבלה בדרום — B: הקישור היחיד בין הדרום לצפון; כל טיסה לדרום עוברת עליו פעמיים, ובכיוונים מנוגדים. בונים עכשיו רק מה שלא משנה גאומטריה (P6, המגוון, המשא הענק); B2 / מפרץ ההמתנה — לאישור הבעלים.</p></div>
<h2>איך זה נבנה — ולמי</h2><div class="card"><ul>
<li><b>במחולל:</b> deliver/2026-11-17/fieldthru2/tools/ft2_var.py (שדרוג של ft_sim.py:variant_of — כלל 19א) → גרסה לכל סוג + נסיעת הגרר שלה; ‏ft2_seq.py — הסבב (5 סבבים) נבדק סבב-סבב: כל הטיסות של אותו סבב יחד.</li>
<li><b>במשחק:</b> חלק חדש parts/074zv1_ft_types.js — FTV: הגרסאות + הסבב; ההחלפה מחוץ לעולם (כמו ffmxSet של fieldfix ו-ftrAt); אחריה — הנסיעה של הגרר מתחלפת כשהוא בבית; המטמונים של העמדה מתאפסים (השרוול, הנוסעים, המכוון); ‎#ftv=0 — בלי.</li>
<li><b>ל-fieldsvc (ממשק):</b> ‏FTV.onSwap(fn) — לכל החלפה: הטיסה, הסוג החדש, חלון העמידה; ו-FTV.visits(fid) — כל הסוגים של הטיסה וחלונות העמידה שלהם — כדי שהשירות לכל סוג ייבנה לכל הגרסאות. עד אז — רכבי השירות של היום נשארים בזמנים ובמקומות שלהם, והגרסאות נבדקו מולם (0 נגיעות).</li>
<li><b>הבדיקה החוסמת:</b> fieldthru_types (חדש, בתוך roadAudit) — לכל אחד מ-4 הסבבים של היום: כל הטיסות בגרסה של הסבב, s15SimAudit — 0 חפיפות, השרוול עוגן בכל עמדת שרוול, גרר צמוד בכל דחיפה, ואחר כך הכול חוזר בדיוק; ‏fieldthru_variety — הסוגים והחברות לכל עמדה; ‏fieldthru_ops — 3 זרעים.</li></ul></div>
</main></body></html>''' % (CSS, nact, nvar, mv('e1_p6'), svg_map(), TABLE, LEG, svg_strip(), svg_mw(), svg_hc(), opt_rows())
open(outp, 'w', encoding='utf-8').write(page); print('ok', len(page), outp)
