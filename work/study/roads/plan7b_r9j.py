# -*- coding: utf-8 -*-
"""4.11 · סבב 9י של מפת הדרכים — המסוף של E3 עם שתי כניסות ושתי יציאות (D‑469, הבעלים 10:30 / 10:31; הבעלים 18:15: "יש תוכנית דרכים חדשה, שבה למסוף יש 2 כניסות ויציאות?"),
והשינויים של היום בפתחים: היציאה החדשה של הסוכנות לשדרת המזרח (D‑480, אושר 16:21), הכניסה לחניון B1-P מערבה (אושר 18:11), ותיעוד הנקודות הלוגיסטיות (D‑477).
 · השער הצפון-מערבי החדש: מהצד המזרחי של שדרת המזרח (AR-E, הנתיבים צפונה), 20 מ׳ מ-J46_16 — כניסה ימינה פנימה ויציאה ימינה החוצה, בנתיבים נפרדים עם אי ביניהם.
 · השער הדרומי (E54_20): כניסה ויציאה נפרדות — הכניסה בנתיב המזרחי (מי שעולה צפונה ב-LC-E3), היציאה בנתיב המערבי, עם אי של 2 מ׳.
 · בתוך המסוף: חד-סטרי סביב כל אי — בצד הצפוני מזרחה ובצד הדרומי מערבה — כך שהדלת הימנית של האוטובוס פונה תמיד לרציף.
 · שאר הרשת, הציור והבדיקות — בלי שינוי. הסעיפים של 9ט ו-9ח נשארים בדף כהיסטוריה.
    python3 plan7b_r9j.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, textwrap, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9i as R9I       # round 9ט — on import: 9ח … 9 and the hotel driveways of 9ט
import plan7b_r9g as R9G
import plan7b_sites as ST
import plan7b_svg as SV
E = html.escape
WHY_T = ('הבעלים 4.11 10:30 / 10:31 (D‑469): "כשיהיו 6 קווים, הכניסה והיציאה מהמסוף יהיו צוואר בקבוק … נוספים 2 כניסות ו-2 יציאות, כל קו לפי מה שמסתדר לקו". '
         'השער החדש מהצד המזרחי של שדרת המזרח, 20 מ׳ מ-J46_16 (R-18): ימינה פנימה וימינה החוצה, בנתיבים נפרדים.')
NEW = [dict(zone='E3', id='DW-E3-BUS-NW', road='AR-E', at=(4752, 1805), label='השער הצפון-מערבי של מסוף האוטובוסים — כניסה ויציאה נפרדות', why=WHY_T,
            to=[(4880, 1805)], lanes='1+1'),
       dict(zone='D3', id='DW-D3-DEALER-OUT', road='AR-E', at=(4448, 2271), label='היציאה של סוכנות הרכב לשדרת המזרח — ימינה בלבד',
            why='הבעלים 16:21 (D‑480): המגרש של הסוכנות בלי מוצא; מוביל הרכב יוצא קדימה, ימינה בלבד, מדרום למפרץ של ST-01.', to=[(4400, 2271)], lanes='1')]
for d in NEW:
    ST.DW[:] = [x for x in ST.DW if x['id'] != d['id']]; ST.DW.append(d)
for d in ST.DW:
    if d['id'] == 'DW-B1-P':
        d.update(at=(2250, 706), to=(2250, 680), why='מדרך הפארק; זזה מערבה ל-x 2230–2270, כי הייתה על מעבר החצייה של כיכר הכפר בזרוע של LC-B1 (הבעלים 18:11).')
# the dealer's new exit (D‑480) is 1 m south of the southbound bay of ST-01: the bay keeps the round-5 rule, with its reason (R-63) — given to the build as it runs
import runpy
_RP = runpy.run_path
ST01_WHY = ('היציאה החדשה של סוכנות הרכב (D‑480, אושרה 16:21) נמצאת מיד אחרי המפרץ: פתח ימינה בלבד, למוביל רכב שבא מדי פעם — לא צומת; '
            'המפרץ נשאר לפי הכלל של סבב 5 (20 מ׳ ממרכז הצומת)')
def _run_path(path, init_globals=None, run_name=None):
    if os.path.basename(path) == 'plan7b_build.py':
        src = open(path, encoding='utf-8').read(); key = "STOP_DEC = {"
        assert src.count(key) == 1
        src = src.replace(key, key + repr('וילות ושירותי רכב (D3)') + ': ' + repr(ST01_WHY) + ', ', 1)
        g = dict(init_globals or {}); g.update(__name__=run_name or '<run_path>', __file__=path)
        exec(compile(src, path, 'exec'), g); return g
    return _RP(path, init_globals=init_globals, run_name=run_name)
runpy.run_path = _run_path
TITLE = 'תוכנית הדרכים של כל העיר — סבב 9י'
_lay = SV.label_layout
def label_layout(P_):
    o = _lay(P_); P_['title'] = TITLE; P_['batch'] = '9י'; return o
SV.label_layout = label_layout

GATES = {'nw': dict(road='AR-E', at=[4752, 1805], into=[4880, 1805], lane_in=[4752, 1820, 4880, 1820], lane_out=[4880, 1790, 4752, 1790], island_m=2,
                    turn_in='ימינה פנימה מהנתיבים צפונה של שדרת המזרח, אל הנתיב הדרומי של השער', turn_out='יציאה בנתיב הצפוני של השער, ימינה החוצה — צפונה, אל J46_16'),
         's': dict(node='E54_20', at=[5400, 2170], lane_in=[5420, 2200, 5420, 2170], lane_out=[5380, 2170, 5380, 2200], island_m=2,
                   turn_in='מי שעולה צפונה ב-LC-E3 נכנס בנתיב המזרחי', turn_out='יציאה בנתיב המערבי, דרומה ב-LC-E3')}
FLOW = 'חד-סטרי סביב כל אי: בצד הצפוני של האי מזרחה, ובצד הדרומי מערבה — הדלת הימנית של האוטובוס פונה תמיד לרציף; כל קו נכנס ויוצא בשער שמתאים למסלול שלו.'
POINTS = [('D3', 'מפרץ המכלית בתחנת הדלק', [4228, 1766, 4406, 1800], 'קיים בקוד — עכשיו גם במפה'),
          ('D3', 'היציאה של הסוכנות לשדרת המזרח', [4400, 2232, 4448, 2310], 'חדש — לבנייה, D‑480'),
          ('D3', 'חניות התצוגה החדשות לאורך הקיר הדרומי של האולם', [4210, 2194, 4351, 2218], 'חדש — לבנייה'),
          ('D4', 'רציף הסמי החמישי', [4066, 3125, 4231, 3155], 'חדש — לבנייה'),
          ('D4', 'שלוש עמדות משאית ארגז ברצועת המחסן הגדול', [3918, 2752, 4430, 2826], 'קיים — מופעל'),
          ('B4', 'מפרץ הפריקה של הסופר', [1342, 3206, 1482, 3241], 'חדש — לבנייה'),
          ('C4', 'מפרץ הפריקה של "ארגז הכלים"', [2869, 2562, 3042, 2800], 'חדש — בחניון החנות'),
          ('C5', 'שתי עמדות מילוי מכליות, במקום המסילה', [2880, 3900, 2990, 4040], 'חדש — לבנייה; המסילה REF-SPUR יוצאת'),
          ('D5', 'מפרץ המכלית בחניון הלילה', [3891, 3962, 3923, 4092], 'קיים — המסלול: ממזרח, יציאה בצפון'),
          ('A2', 'הרציף, החצר הטכנית ומקום המכלית של בית החולים', [480, 735, 1118, 1250], 'נבנה ב-S7F248')]
NOTE_D4 = 'DW-D4-01 (מצפון למחסן הגדול) קיים במפה, ובמשחק אין שם פתח — דשא וגדר. משאית הארגז נכנסת בשער המזרחי של D4. בסבב הבא הוא יוצא מהמפה, יחד עם הגישה של המחסן.'

def terminal_svg(T):
    x0, y0, x1, y1 = 4420, 1580, 5760, 2260; W_ = x1 - x0; H_ = y1 - y0
    o = ['<svg viewBox="%d %d %d %d" role="img" aria-label="המסוף עם שני השערים" style="width:100%%;max-width:900px;height:auto;background:#f4f2ec;border-radius:10px">' % (x0, y0, W_, H_),
         '<defs><marker id="ar9j" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0L10,5L0,10z" fill="#c8372d"/></marker><marker id="ar9jb" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0L10,5L0,10z" fill="#2a6fdb"/></marker><marker id="ar9jk" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0L10,5L0,10z" fill="#333"/></marker></defs>']
    o.append('<rect x="4448" y="1580" width="304" height="680" fill="#8d949b"/><text x="4600" y="2240" font-size="30" text-anchor="middle" fill="#fff">שדרת המזרח</text><text x="4520" y="1960" font-size="44" text-anchor="middle" fill="#fff">↓</text><text x="4680" y="1960" font-size="44" text-anchor="middle" fill="#fff">↑</text>')
    o.append('<rect x="5360" y="2170" width="80" height="90" fill="#8d949b"/><text x="5520" y="2245" font-size="28" fill="#333" text-anchor="middle">LC-E3</text>')
    r = T['rect']; o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#b9bec4" stroke="#555" stroke-width="4"/>' % (r[0], r[1], r[2] - r[0], r[3] - r[1]))
    for p in T['platforms']:
        q = p['rect']; o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#e9e3d2" stroke="#777"/><text x="%d" y="%d" font-size="26" text-anchor="middle">אי %s</text>' % (q[0], q[1], q[2] - q[0], q[3] - q[1], (q[0] + q[2]) // 2, q[3] - 4, p['id']))
    for h in T['hold']:
        q = h['rect']; o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#666" stroke-dasharray="10 6"/>' % (q[0], q[1], q[2] - q[0], q[3] - q[1]))
    g = GATES['nw']; o.append('<rect x="4752" y="1782" width="128" height="46" fill="#8d949b"/>')
    o.append('<line x1="4752" y1="1820" x2="4870" y2="1820" stroke="#c8372d" stroke-width="7" marker-end="url(#ar9j)"/>')
    o.append('<line x1="4870" y1="1790" x2="4762" y2="1790" stroke="#2a6fdb" stroke-width="7" marker-end="url(#ar9jb)"/>')
    o.append('<text x="4816" y="1770" font-size="26" text-anchor="middle">השער הצפון-מערבי</text>')
    o.append('<line x1="5420" y1="2250" x2="5420" y2="2180" stroke="#c8372d" stroke-width="7" marker-end="url(#ar9j)"/>')
    o.append('<line x1="5380" y1="2180" x2="5380" y2="2250" stroke="#2a6fdb" stroke-width="7" marker-end="url(#ar9jb)"/>')
    o.append('<text x="5250" y="2215" font-size="26" text-anchor="middle">השער הדרומי</text>')
    for (xa, ya, xb, yb) in [(5080, 1877, 5520, 1877), (5520, 1943, 5080, 1943), (5080, 2047, 5520, 2047), (5520, 2113, 5080, 2113)]:
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#333" stroke-width="5" stroke-dasharray="26 14" marker-end="url(#ar9jk)"/>' % (xa, ya, xb, yb))
    o.append('<g transform="translate(5690,1640)"><path d="M0,-40 L16,0 L0,-10 L-16,0 Z" fill="#222"/><text x="0" y="30" font-size="28" text-anchor="middle">צפון</text></g>')
    o.append('<text x="5700" y="2010" font-size="30" text-anchor="middle" fill="#222">מזרח</text><text x="4600" y="1660" font-size="30" text-anchor="middle" fill="#fff">מערב</text>')
    o.append('</svg>')
    return ''.join(o)

def page_r9j():
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = TITLE; P_['batch'] = '9י'
    got = {d['id']: d for d in P_['driveways'] if d['id'] in ('DW-E3-BUS-NW', 'DW-D3-DEALER-OUT', 'DW-B1-P')}
    T = P_['bus']['terminal']; T['gates'] = GATES; T['flow'] = FLOW
    P_['logi_points'] = [dict(zone=z, what=w, rect=r, state=s) for z, w, r, s in POINTS]
    P_['r9j'] = dict(at='4.11.2026', by='הבעלים 10:30 / 10:31 / 16:21 / 18:11 / 18:15',
                     why='סבב 9י: המסוף עם 2 כניסות ו-2 יציאות (D‑469); היציאה של הסוכנות; הכניסה ל-B1-P מערבה; הנקודות הלוגיסטיות במפה (D‑477)',
                     moved={k: dict(at=v['at'], to_junction_m=v.get('to_junction_m')) for k, v in got.items()}, note_d4=NOTE_D4)
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); H0 = open(ph, encoding='utf-8').read()
    rows = ''.join("<li>%s — %s: על %s, %s מ׳ מהצומת הקרוב, %s</li>" % (E(v['id']), E(v['label']), E(v['road']), v.get('to_junction_m'), 'נתיב אחד' if v.get('lanes') == '1' else 'כניסה ויציאה') for v in got.values())
    prow = ''.join('<li>%s — %s (%s)</li>' % (E(z), E(w), E(s)) for z, w, r, s in POINTS)
    S9 = ("<h2>סבב 9י — מה השתנה (4.11.2026)</h2><p class='small'>המסוף של E3 מקבל שתי כניסות ושתי יציאות (D‑469). "
          "<b>השער הצפון-מערבי</b> — חדש, מהצד המזרחי של שדרת המזרח, 20 מ׳ מהצומת J46_16: " + E(GATES['nw']['turn_in']) + "; " + E(GATES['nw']['turn_out']) + "; שני נתיבים נפרדים עם אי ביניהם. "
          "<b>השער הדרומי</b> — כניסה ויציאה נפרדות: " + E(GATES['s']['turn_in']) + "; " + E(GATES['s']['turn_out']) + ", עם אי של 2 מ׳. "
          "<b>בתוך המסוף</b> — " + E(FLOW) + "</p>" + terminal_svg(T) +
          "<p class='small'>החץ האדום — כניסה, הכחול — יציאה, המקווקו — הזרימה סביב האיים. המלבנים המקווקווים בצפון — מקומות ההמתנה.</p>"
          "<p class='small'>עוד בסבב הזה:</p><ul class='small'>" + rows + "</ul>"
          "<p class='small'>הנקודות הלוגיסטיות שנרשמו במפה (D‑477 — כל נקודה גם בקוד וגם במפה):</p><ul class='small'>" + prow + "</ul>"
          "<p class='small'>" + E(NOTE_D4) + "</p>")
    k = H0.index('<h2>סבב 9ט'); H0 = H0[:k] + S9 + H0[k:]
    H0 = H0.replace('תוכנית הדרכים של כל העיר — סבב 9ט', TITLE)
    open(ph, 'w', encoding='utf-8').write(H0)
    print('r9j', {k: (v['at'], v.get('to_junction_m')) for k, v in got.items()})
    assert len(got) == 3 and H0.count('<h2>סבב 9י') == 1 and H0.count('<h2>סבב 9ט') == 1 and H0.count('<h2>סבב 9ח') == 1

if __name__ == '__main__':
    os.chdir(HERE)
    rec9h, prev9i, sec9h = R9I.keep_9h()
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    R9I.page_r9i(rec9h, sec9h)
    page_r9j()
