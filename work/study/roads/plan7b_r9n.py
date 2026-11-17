# -*- coding: utf-8 -*-
"""5.11 · סבב 9נ של מפת הדרכים — J31_16 (שדרת השדה × רחוב הווילות) נעשה רמזור. הבעלים 4.11 23:59: "חסר רמזור לצומת יציאה וכניסה לרחוב הווילות
(יציאה משם ימינה בלבד)"; במשחק מ-S7F259 (p614_arn_j3116, ‏p650_j3116_seam).
 · J31_16: מ"ימינה בלבד" לרמזור לפי דרישה — רחוב הווילות מקבל ירוק רק כשמחכה בו רכב או הולך רגל. נכנסים משני הכיוונים: משדרת השדה מערבה —
   שמאלה עם חץ (החציון נפתח), ממזרחה — ימינה. היציאה מרחוב הווילות — ימינה בלבד, עם תמרור. המעברים לפי D‑439: בזרוע המערבית וברחוב הווילות.
 · R-15: הכלל של 75 מ׳ בין רמזורים בעורק חל עכשיו גם על העורק הראשי (3+3); J31_16 נמצא 60 מ׳ מ-J25_16 ומ-J37_16 — חריגה עם סיבה.
 · התפר בין C2 ל-C3 ברחוב הווילות (במשחק: N31, מ-y 1700 ל-y 1800) — במפה הגבול בין האזורים הוא קו הרשת הקבוע, ואין עליו נקודה; רק הערה בסעיף.
    python3 plan7b_r9n.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete/roads_before_r9n)"""
import json, os, sys, textwrap, html, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
E = html.escape
import plan7b_r9m as R9M        # round 9מ (and through it 9ל … 9) — its patches and wrappers run on import; its __main__ does not
import plan7b_r9k as R9K
import plan7b_r9j as R9J
import plan7b_r9i as R9I
import plan7b_r9g as R9G
import plan7b_r9 as R9
import plan7b_net as NET
import plan7b_svg as SV

K31 = 'J31_16'
SRC = 'הבעלים 4.11 23:59'
WHY31 = ('הבעלים 4.11 23:59: "חסר רמזור לצומת יציאה וכניסה לרחוב הווילות (יציאה משם ימינה בלבד)"; במשחק מ-S7F259. רמזור לפי דרישה: רחוב הווילות מקבל ירוק '
         'רק כשמחכה בו רכב או הולך רגל. משדרת השדה מערבה — שמאלה עם חץ, והחציון נפתח; ממזרחה — ימינה. היציאה מרחוב הווילות — ימינה בלבד, עם תמרור.')
n31 = NET.N[K31]; BEFORE31 = dict(kind=n31['kind'], label=n31['label'], why=n31['why'])
n31.update(kind='signal', label='שדרת השדה × רחוב הווילות (רמזור לפי דרישה; היציאה ימינה בלבד)', why=WHY31)

# round 9's list of the signals (it was read on import): J31_16 is a signal now — by the owner, not by the rule of 11:38
row = next(r for r in R9.SIG9 if r['node'] == K31)
row.update(label=n31['label'], after='signal', mode='לפי דרישה', why='סבב 9נ (' + SRC + '): רמזור לפי דרישה; היציאה מרחוב הווילות ימינה בלבד, עם תמרור')
sg = R9.DONE9['signals']
if K31 in sg['none']: sg['none'].remove(K31)
if K31 not in sg['new']: sg['new'].append(K31)
for d in R9.DEC9:
    if d['code'] == 'R9-SIG':
        d['what'] = f"רמזור בכל צומת: {len(sg['new'])} חדשים, {len(sg['kept'])} שהיו; בלי רמזור: {len(sg['none'])} (כיכרות, שערים, אזור סגור, רחוב ללא מוצא) — J31_16 רמזור לפי דרישה מסבב 9נ ({SRC})"

# R-15: the 75 m between signals on an arterial — the main arterial (3+3) too; J31_16's two neighbours with the reason
WHY15 = 'בקשת הבעלים; רמזור לפי דרישה, מתואם בגל ירוק (' + SRC + ')'
R9K.R15_SIG_EXC = {('AR-N', 'J25_16', K31): WHY15, ('AR-N', K31, 'J37_16'): WHY15}   # the signal rule only (the 60 m between junctions holds)
def r15_txt():
    return (' חריגות עם סיבה: ' + '; '.join(R9K.R15_GOT) + '.') if R9K.R15_GOT else ''
R9K.r15_txt = r15_txt

# the signal of J31_16: the side street right only (its approach has no left lane — by the owner); the phases on demand
def r9n_sig(g):
    s = next(x for x in g['SIG'] if x['node'] == K31)
    for a in s['approaches']:
        if a['road'] == 'LC-C3': a.update(through=0, left=0, arrow=False, right_only=True, sign='ימינה בלבד')
        elif a['from'] == 'J37_16': a.update(left=1, arrow=True, left_into='LC-C3')
        else: a.update(left=0, arrow=False, right_into='LC-C3')
    s.update(phases=['שדרת השדה — ישר', 'שדרת השדה מערבה — חץ שמאלה אל רחוב הווילות', 'רחוב הווילות — ימינה בלבד; ירוק רק לפי דרישה (רכב או הולך רגל)'],
             demand=True, why=WHY31)
    DONE9N['sig'] = s
def r9n_r16_txt():
    return f" חריגה עם סיבה: {K31} — מרחוב הווילות ימינה בלבד, עם תמרור, ומשדרת השדה מזרחה אין שמאלה (אין זרוע צפונית) — {SRC}."
R9K.r9n_sig = r9n_sig; R9K.r9n_r16_txt = r9n_r16_txt
R9K.PATCH += [
    ("    if rd['cls'] == 'arterial':\n        sg = ", "    if rd['cls'] in ('arterial', 'main'):\n        sg = "),
    ("            if pos[b] - pos[a] < 750: viol.append(f\"{rd['id']}: רמזורים {a}–{b} {(pos[b] - pos[a]) / 10:.0f} מ׳ (< 75)\")",
     "            if pos[b] - pos[a] < 750 and (rd['id'], a, b) in R9K.R15_SIG_EXC: R9K.R15_GOT.append(f\"{rd['id']}: רמזורים {a}–{b} {(pos[b] - pos[a]) / 10:.0f} מ׳ (< 75) — {R9K.R15_SIG_EXC[(rd['id'], a, b)]}\")\n"
     "            elif pos[b] - pos[a] < 750: viol.append(f\"{rd['id']}: רמזורים {a}–{b} {(pos[b] - pos[a]) / 10:.0f} מ׳ (< 75)\")"),
    ("r16 = [s['node'] for s in SIG if any(a['left'] == 0 and N[a['from']]['kind'] != 'gate' for a in s['approaches'])]",
     "R9K.r9n_sig(globals())\nr16 = [s['node'] for s in SIG if any(a['left'] == 0 and N[a['from']]['kind'] != 'gate' and not (s['node'] == R9K.r9n_K31 and a.get('road') in ('LC-C3', 'AR-N')) for a in s['approaches'])]"),
    ("\n# connectivity and the must-reach places", "\nchecks[-1]['det'] += R9K.r9n_r16_txt()\n# connectivity and the must-reach places"),
]
R9K.r9n_K31 = K31
DONE9N = {}

TITLE = 'תוכנית הדרכים של כל העיר — סבב 9נ'
_lay9m = SV.label_layout
def label_layout(P_):
    o = _lay9m(P_); P_['title'] = TITLE; P_['batch'] = '9נ'
    XW = [x for x in P_['bus']['crosswalks'] if x['node'] == K31]; DONE9N['xw'] = sorted(x['seg'] for x in XW)
    return o
SV.label_layout = label_layout

_hov9m = SV.hover_data
def hover_data(P_, GR_, M_):
    """the hover card of J31_16: the approach of the villas' street is right only"""
    s = _hov9m(P_, GR_, M_); pre, suf = "<script>window.__MAP=", ";</script>"
    D = json.loads(s[len(pre):-len(suf)]); n = 0
    for i, t in enumerate(D['info']):
        if '(J31_16)' in t and '(<bdi>E31_23</bdi>): 0 ישר' in t:
            D['info'][i] = (t.replace('(<bdi>E31_23</bdi>): 0 ישר (הגישה של השדה)', '(<bdi>E31_23</bdi>): ימינה בלבד, עם תמרור')
                             .replace('(<bdi>J25_16</bdi>): 3 ישר (הגישה של השדה)', '(<bdi>J25_16</bdi>): 3 ישר, ימינה אל רחוב הווילות')); n += 1
    assert n == 1, n
    return pre + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + suf
SV.hover_data = hover_data

# ---------------------------------------------------------------- the page: the section of 9נ before 9מ (9מ … 9ח stay as they were)
def keep():
    P_ = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8'))
    T = open(os.path.join(HERE, 'city_plan.html'), encoding='utf-8').read()
    def sec(a, b): i = T.index(a); j = T.index(b); assert i < j; return T[i:j]
    return dict(rec={k: P_[k] for k in ('r9j', 'r9k', 'r9l', 'r9m')}, s9m=sec('<h2>סבב 9מ', '<h2>סבב 9ל'), s9l=sec('<h2>סבב 9ל', '<h2>סבב 9כ'),
                s9k=sec('<h2>סבב 9כ', '<h2>סבב 9י'), s9j=sec('<h2>סבב 9י', '<h2>סבב 9ט'))

def j31_svg(after):
    x0, y0, x1, y1 = 2830, 1380, 3390, 1960; rd = '#8d949b'; wk = '#e2ded3'
    o = [f"<svg viewBox='{x0} {y0} {x1 - x0} {y1 - y0}' role='img' aria-label='J31_16 {'אחרי' if after else 'לפני'}' style='width:100%;height:auto;background:#f4f2ec;border-radius:8px'>",
         "<defs><marker id='a9n" + ('a' if after else 'b') + "' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0L10,5L0,10z' fill='#c8372d'/></marker>"
         "<marker id='b9n" + ('a' if after else 'b') + "' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0L10,5L0,10z' fill='#2a6fdb'/></marker></defs>"]
    ma, mb = ('a9na', 'b9na') if after else ('a9nb', 'b9nb')
    o.append(f"<rect x='{x0}' y='1448' width='{x1 - x0}' height='304' fill='{wk}'/><rect x='{x0}' y='1473' width='{x1 - x0}' height='254' fill='{rd}'/>")
    o.append(f"<rect x='3056' y='1727' width='108' height='{y1 - 1727}' fill='{wk}'/><rect x='3071' y='1727' width='78' height='{y1 - 1727}' fill='{rd}'/>")
    if after: o.append(f"<rect x='{x0}' y='1590' width='{2990 - x0}' height='20' fill='#9cbf86'/><rect x='3240' y='1590' width='{x1 - 3240}' height='20' fill='#9cbf86'/>")
    else: o.append(f"<rect x='{x0}' y='1590' width='{x1 - x0}' height='20' fill='#9cbf86'/>")
    o.append(''.join(f"<rect x='3006' y='{y}' width='40' height='12' fill='#fff'/>" for y in range(1478, 1722, 22)))       # the crossing on the west arm (D‑439)
    o.append(''.join(f"<rect x='{x}' y='1762' width='12' height='40' fill='#fff'/>" for x in range(3076, 3146, 20)))        # the crossing on the villas' street
    o.append(f"<path d='M2870,1690 L3040,1690 Q3090,1690 3090,1745' fill='none' stroke='#c8372d' stroke-width='9' marker-end='url(#{ma})'/>")       # right in, from the east-bound lanes
    o.append(f"<path d='M3130,1745 Q3130,1690 3180,1690 L3340,1690' fill='none' stroke='#2a6fdb' stroke-width='9' marker-end='url(#{mb})'/>")      # right out
    if after:
        o.append(f"<path d='M3350,1568 L3200,1568 Q3095,1568 3095,1660 L3095,1745' fill='none' stroke='#c8372d' stroke-width='9' marker-end='url(#{ma})'/>")  # left in, with the arrow
        for (x, y) in ((2990, 1435), (3220, 1435), (3175, 1790)):   # the signal heads
            o.append(f"<g transform='translate({x},{y})'><rect x='-11' y='-30' width='22' height='60' rx='5' fill='#222'/><circle cy='-17' r='6' fill='#d62d20'/><circle r='6' fill='#e8b500'/><circle cy='17' r='6' fill='#1e9e3a'/></g>")
        o.append("<g transform='translate(3205,1858)'><circle r='26' fill='#1f5fd1' stroke='#fff' stroke-width='4'/><path d='M-10,12 L-10,-2 Q-10,-10 -2,-10 L8,-10' fill='none' stroke='#fff' stroke-width='5'/><path d='M4,-17 L13,-10 L4,-3 Z' fill='#fff'/></g>")
        o.append("<text x='3110' y='1890' font-size='24' text-anchor='middle' fill='#333'>ימינה בלבד</text>")
    else:
        o.append("<text x='3110' y='1890' font-size='24' text-anchor='middle' fill='#333'>ימינה בלבד, בלי רמזור</text>")
    o.append("<text x='3110' y='1555' font-size='24' text-anchor='middle' fill='#fff'>שדרת השדה</text><text x='3110' y='1945' font-size='22' text-anchor='middle' fill='#333'>רחוב הווילות</text>"
             "<text x='3285' y='1660' font-size='22' text-anchor='middle' fill='#fff'>J31_16</text>")
    o.append("<g transform='translate(3345,1850)'><path d='M0,-36 L14,0 L0,-9 L-14,0 Z' fill='#222'/><text x='0' y='26' font-size='20' text-anchor='middle'>צפון</text></g>")
    o.append("<text x='2880' y='1850' font-size='26' text-anchor='middle' fill='#222'>מערב</text><text x='3345' y='1420' font-size='26' text-anchor='middle' fill='#222'>מזרח</text>")
    o.append('</svg>')
    return ''.join(o)

def page_r9n(K):
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = TITLE; P_['batch'] = '9נ'
    T = P_['bus']['terminal']; T['gates'] = R9K.gates_rec(); T['flow'] = R9K.FLOW
    P_['logi_points'] = [dict(zone=z, what=w, rect=r, state=s) for z, w, r, s in R9J.POINTS]
    for k, v in K['rec'].items(): P_[k] = v
    SB = {frozenset((x['a'], x['b'])): x for x in P_['segments']}
    for ln in P_['routes']['bus']:
        if ln.get('back'): ln['len_back_km'] = round(sum(SB[frozenset((a, b))]['len_m'] for a, b in zip(ln['back'], ln['back'][1:])) / 1000, 2)
    nck = len(P_['checks']); nok = sum(1 for c in P_['checks'] if c['ok'])
    sig = next(s for s in P_['signals'] if s['node'] == K31)
    r15 = next(c for c in P_['checks'] if c['name'].startswith('R-15'))
    P_['r9n'] = dict(at='5.11.2026', by=SRC + ' (במשחק S7F259)', why='סבב 9נ: J31_16 — רמזור לפי דרישה; היציאה מרחוב הווילות ימינה בלבד', before=BEFORE31,
                     after=dict(kind='signal', label=n31['label'], why=WHY31, phases=sig['phases'], demand=sig.get('demand')), crosswalks=DONE9N.get('xw'),
                     r15=[x for x in R9K.R15_GOT if K31 in x], seam=dict(game='N31: התפר C2/C3 מ-y 1700 ל-y 1800 (S7F259, p650_j3116_seam)',
                     map='במפה הגבול בין האזורים הוא קו הרשת הקבוע (y 1700); אין עליו נקודה, והקטע LC-C3/1 שייך ל-C2, ‏C3 ו-C4 ונבנה עם C3 (S4) — לא השתנה'),
                     checks=f'{nok}/{nck}')
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); H0 = open(ph, encoding='utf-8').read()
    fig = lambda after, cap: f"<figure style='margin:0;flex:1 1 280px;max-width:440px'>{j31_svg(after)}<figcaption class='small'>{cap}</figcaption></figure>"
    xw = ', '.join(DONE9N.get('xw') or [])
    S9 = ("<h2>סבב 9נ — מה השתנה (5.11.2026)</h2>"
          f"<p class='small'>הבעלים (4.11 23:59): J31_16 — שדרת השדה × רחוב הווילות — הוא עכשיו <b>רמזור לפי דרישה</b>, כמו במשחק מ-S7F259: רחוב הווילות מקבל ירוק רק כשמחכה בו רכב או הולך רגל. "
          "נכנסים משני הכיוונים — משדרת השדה מערבה שמאלה עם חץ (החציון נפתח), וממזרחה ימינה; היציאה מרחוב הווילות — ימינה בלבד, עם תמרור. "
          f"המעברים לפי D‑439: בזרוע המערבית וברחוב הווילות ({E(xw)}). J31_16 יצא מרשימת צומתי ימינה בלבד ונוסף לרמזורים.</p>"
          "<p class='small'>R-15: הכלל של 75 מ׳ בין רמזורים בעורק נבדק עכשיו גם בעורק הראשי. J31_16 נמצא 60 מ׳ מ-J25_16 ו-60 מ׳ מ-J37_16 — חריגה עם סיבה: "
          f"{E(WHY15)}. התפר בין C2 ל-C3 ברחוב הווילות (במשחק N31, מ-y 1700 ל-y 1800): במפה הגבול בין האזורים הוא קו הרשת הקבוע ואין עליו נקודה, ולכן במפה אין מה להזיז. "
          f"הבדיקות: {nok} מתוך {nck} עוברות.</p>"
          "<div style='display:flex;flex-wrap:wrap;gap:12px;margin:6px 0 14px'>" + fig(False, 'לפני — ימינה פנימה וימינה החוצה, החציון רציף') +
          fig(True, 'אחרי — רמזור לפי דרישה: שמאלה עם חץ ממערבה (החציון נפתח), ימינה ממזרחה; היציאה ימינה בלבד') + "</div>")
    k = H0.index('<h2>סבב 9ט'); H0 = H0[:k] + S9 + K['s9m'] + K['s9l'] + K['s9k'] + K['s9j'] + H0[k:]
    for old in ('תוכנית הדרכים של כל העיר — סבב 9ט', 'תוכנית הדרכים של כל העיר — סבב 9י', 'תוכנית הדרכים של כל העיר — סבב 9כ',
                'תוכנית הדרכים של כל העיר — סבב 9ל', 'תוכנית הדרכים של כל העיר — סבב 9מ'):
        H0 = H0.replace(old, TITLE)
    open(ph, 'w', encoding='utf-8').write(H0)
    print('r9n', dict(sig=dict(phases=sig['phases'], approaches=sig['approaches']), xw=DONE9N.get('xw'), r15=P_['r9n']['r15'], riro=[r['node'] for r in P_['riro']], checks=f'{nok}/{nck}'))
    assert sig and K31 not in [r['node'] for r in P_['riro']] and len(P_['r9n']['r15']) == 2 and r15['ok']
    assert all(H0.count('<h2>סבב ' + r) == 1 for r in ('9נ', '9מ', '9ל', '9כ', '9י', '9ט', '9ח'))
    assert H0.index('<h2>סבב 9נ') < H0.index('<h2>סבב 9מ') < H0.index('<h2>סבב 9ל') < H0.index('<h2>סבב 9כ') < H0.index('<h2>סבב 9י') < H0.index('<h2>סבב 9ט')

if __name__ == '__main__':
    os.chdir(HERE)
    rec9h, prev9i, sec9h = R9I.keep_9h()
    K = keep()
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    R9I.page_r9i(rec9h, sec9h)
    page_r9n(K)
