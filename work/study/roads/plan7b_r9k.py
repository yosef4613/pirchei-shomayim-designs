# -*- coding: utf-8 -*-
"""4.11 · סבב 9כ של מפת הדרכים — השער המערבי של מסוף האוטובוסים ב-E3 נעשה כביש דו-סטרי אמיתי ברשת, והקווים עוברים דרכו.
הבעלים 18:40 (על 9י, עם צילום): "בתוכנית לא השתנו הקווים שיוצאים ונכנסים ממערב, וגם זה לא מסומן ככביש דו-סטרי" · "וגם קצת לזוז דרומה — לא על המעבר חצייה";
D‑469 (10:30 / 10:31): "נוספים 2 כניסות ו-2 יציאות, כל קו לפי מה שמסתדר לקו".
 · הרשת: J46_185 — צומת ימינה בלבד חדש על שדרת המזרח ב-(4600, 1860); E49_185 — הקצה של השער ב-(4920, 1860), מעבר לפינה המעוגלת של חצר המסוף;
   LC-E3W "השער המערבי של המסוף" — מקומי 1+1 ביניהם. נכנסים בנתיב הדרומי (מערב → מזרח), יוצאים בנתיב הצפוני; ימינה פנימה מהנתיבים צפונה, ימינה החוצה — צפונה.
   הכביש של השער מתחיל ב-y 1821 — 1.9 מ׳ דרומית למעבר של הזרוע הדרומית של J46_16 (y 1762–1802). DW-E3-BUS-NW של 9י יוצא.
 · המספור של הקטעים: הצומת מפצל את AR-E/1. AR-E/1 נשאר הקטע הארוך (J46_185–J46_25: ‏ST-01, הכניסות של D3, החיבור הזמני TMP-S4-3), הקטע הקצר
   J46_16–J46_185 הוא AR-E/1a, ו-AR-E/2 ו-AR-E/3 לא זזים (הסבבים הקודמים, המעברים שבמשחק — mapnode + seg — ו-r9f מפנים אליהם).
 · צומת ימינה בלבד על עורק עם חציון רציף הוא צומת רק לצד שלו: הכניסות והמפרצים שבצד השני של החציון לא נמדדים ממנו (שם אין פנייה).
   R-15 (26 מ׳ מ-J46_16) — חריגה עם סיבה. המעברים של הקטעים החדשים — במקום האמיתי שלהם (R-76) כבר כשהמפרצים של ST-01 נקבעים.
 · הקווים (ההצעה לבעלים): 1, ‏2, ‏4 ו-6 יוצאים בשער המערבי (ימינה, צפונה); 1 ו-3 חוזרים מ-J46_25 צפונה ונכנסים בו (ימינה פנימה);
   3 יוצא דרומה, 5 לאי, 6 חוזר מצפון — בשער הדרומי. קו שנוסע אחרת בכל כיוון מקבל 'back' — המסלול של הכיוון השני.
 · שתי בדיקות חדשות: השער המערבי, ובצומת ימינה בלבד אין פנייה שמאלה. הסעיפים של 9י, ‏9ט ו-9ח נשארים בדף כהיסטוריה.
    python3 plan7b_r9k.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete/roads_before_r9k)"""
import json, os, sys, textwrap, html, math, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
E = html.escape

# ================================================================ 1 · the network — before the rounds are imported (round 9 reads the junctions on import)
import plan7b_net as NET
Y_W, X_W = 1860, 4920          # the gate's axis; its end, past the round corner of the yard (the north edge of its carriageway meets the asphalt at x 4912)
J_W, E_W, R_W, S_W = 'J46_185', 'E49_185', 'LC-E3W', 'LC-E3W/1'
TERM_NODES = {'E54_20', E_W}   # the two gates of the terminal: a line starts and ends at the terminal through either
WHY_J = ('הבעלים 4.11 18:40 (D‑469): השער המערבי של מסוף האוטובוסים — כביש דו-סטרי, דרומית למעבר של J46_16. ימינה פנימה מהנתיבים צפונה של שדרת המזרח '
         'וימינה החוצה, צפונה; החציון ממשיך — אין שמאלה. בלי רמזור: רחוב ללא מוצא (חצר המסוף). בנתיב הימני צפונה מול השער — קופסה צהובה (ברירת מחדל, לאישורך).')
NET.n(J_W, 4600, Y_W, 'riro', 'שדרת המזרח × השער המערבי של המסוף (ימינה בלבד)', WHY_J)
NET.n(E_W, X_W, Y_W, 'end', 'השער המערבי של מסוף האוטובוסים (E3) — כניסה ויציאה של החצר',
      'הקצה של השער על האספלט של חצר המסוף, מעבר לפינה המעוגלת (רדיוס 14 מ׳): הכביש מגיע לחצר בכל הרוחב שלו.')
NET.r(R_W, 'השער המערבי של המסוף', 'local', [J_W, E_W],
      'סבב 9כ (הבעלים 18:40, D‑469): השער המערבי של מסוף האוטובוסים — נתיב אחד לכל כיוון: נכנסים בנתיב הדרומי (ממערב למזרח), יוצאים בנתיב הצפוני; '
      'ימינה פנימה מהנתיבים צפונה של שדרת המזרח וימינה החוצה, צפונה אל J46_16. כביש ללא מוצא — רק החצר של המסוף.',
      truck=False, note='רק האוטובוסים ורכב השירות של המסוף')
RD = {r['id']: r for r in NET.R}
AR = RD['AR-E']; AR['nodes'].insert(AR['nodes'].index('J46_16') + 1, J_W)
AR['seg_ids'] = {0: 'AR-E/1a', 1: 'AR-E/1', 2: 'AR-E/2', 3: 'AR-E/3'}   # read by the build (the patch below); AR-E/2 and AR-E/3 keep their numbers
AR['why'] = AR['why'] + (' סבב 9כ: הצומת J46_185 (השער המערבי של המסוף, ימינה בלבד) מפצל את AR-E/1 — הקטע הקצר J46_16–J46_185 הוא AR-E/1a, '
                         'ו-AR-E/1 הוא עכשיו J46_185–J46_25; שאר המספרים לא זזים.')
WAIT_W = ('השער של חצר המסוף נבנה עם המסוף (E3), בשלב S9 — לפני כן החצר החדשה לא קיימת, והוא היה מוביל אל E3 של היום')
SPLIT = {'AR-E/1a', 'AR-E/1', S_W}       # the segments new in this round: their crosswalks are where R-76 puts them already when the bays are placed

def _ins(p):   # every path that went J46_16 ↔ J46_25 goes through the new junction
    q = [p[0]]
    for a, b in zip(p, p[1:]):
        if {a, b} == {'J46_16', 'J46_25'}: q.append(J_W)
        q.append(b)
    return q
for kind in NET.ROUTES:
    for rt in NET.ROUTES[kind]:
        rt['path'] = _ins(rt['path'])
        if rt.get('back'): rt['back'] = _ins(rt['back'])
        if rt.get('stops'): rt['stops'] = [tuple([J_W, 'J46_25'] + list(s[2:])) if set(s[:2]) == {'J46_16', 'J46_25'} else s for s in rt['stops']]
LN = {l['id']: l for l in NET.ROUTES['bus']}
OLD_PATHS = {k: list(v['path']) for k, v in LN.items()}
def _cut(p, a, last=False):
    i = (len(p) - 1 - p[::-1].index(a)) if last else p.index(a); return i
for k in ('1', '2', '4', '6'):   # out through the west gate: right, north to J46_16, and on as today
    p = OLD_PATHS[k]; core = p[_cut(p, 'J46_16'):]
    if k == '1': core = core[:_cut(core, 'J46_25', last=True) + 1] + [J_W, E_W]   # 1, anticlockwise: back from J46_25 north — right in
    LN[k]['path'] = [E_W, J_W] + core
    if LN[k]['twoway']: LN[k]['back'] = p[::-1]   # the other direction: as today, through the south gate (from the west gate it would be a left turn)
p3 = OLD_PATHS['3']; k25 = _cut(p3, 'J46_25'); ring = p3[k25:_cut(p3, 'J46_25', last=True) + 1]
LN['3']['path'] = p3[:k25] + ring + [J_W, E_W]          # out south, as today; back from J46_25 north — right in at the west gate
LN['3']['back'] = p3[:k25] + ring[::-1] + [J_W, E_W]    # the other direction of the ring: the same
WHY_L = {'1': 'נגד כיוון השעון — יוצא בשער המערבי (ימינה, צפונה אל J46_16) וחוזר מ-J46_25 צפונה, ימינה פנימה בשער המערבי; עם כיוון השעון — בשער הדרומי, כמו קודם (מהשער המערבי אין יציאה דרומה).',
         '2': 'יוצא בשער המערבי (ימינה, צפונה אל J46_16); חוזר מצפון בשער הדרומי — לשער המערבי זו הייתה פנייה שמאלה.',
         '3': 'יוצא בשער הדרומי, כמו קודם; בשני הכיוונים חוזר מ-J46_25 צפונה ונכנס בשער המערבי, ימינה פנימה.',
         '4': 'יוצא בשער המערבי (ימינה, צפונה אל J46_16); חוזר מהשדה בשער הדרומי — לשער המערבי זו הייתה פנייה שמאלה.',
         '5': 'יוצא ונכנס בשער הדרומי, כמו קודם — אל האי בדרך האי.',
         '6': 'יוצא בשער המערבי (ימינה, צפונה אל J46_16); חוזר מצפון בשער הדרומי — לשער המערבי זו הייתה פנייה שמאלה.'}
for k, w in WHY_L.items(): LN[k]['why'] = LN[k]['why'] + ' סבב 9כ: ' + w

# ================================================================ 2 · the rounds (9י … 9 — their patches run on import), and this round's wrappers
import plan7b_r9j as R9J
import plan7b_r9i as R9I
import plan7b_r9g as R9G
import plan7b_r9 as R9
import plan7b_r7 as R7
import plan7b_sites as ST
import plan7b_svg as SV
ST.DW[:] = [d for d in ST.DW if d['id'] != 'DW-E3-BUS-NW']   # 9י's gate was a driveway — now it is a road

R15_EXC = {('AR-E', 'J46_16', J_W): ('השער המערבי של מסוף האוטובוסים (סבב 9כ, הבעלים 18:40, D‑469): ימינה בלבד בצד המזרחי, והחציון ממשיך — אין שמאלה ואין רמזור; '
                                     'הוא חייב לעמוד בין המעבר של J46_16 לבין המפרץ של ST-01. בנתיב הימני צפונה מול השער — קופסה צהובה, '
                                     'כדי שהתור לרמזור של J46_16 לא יחסום אותו (ברירת מחדל, לאישורך)')}
R15_GOT = []
def r15_txt():
    return (' חריגה עם סיבה (סבב 9כ): ' + '; '.join(R15_GOT) + '.') if R15_GOT else ''

def _riro_side(g, k):
    """the direction of the side arm of a right-in/right-out junction on a road with a median (None — any other node)"""
    N_, ADJ, CLS = g['N'], g['ADJ'], g['CLS']; n = N_.get(k)
    if not n or n['kind'] != 'riro' or len(ADJ.get(k, [])) != 3: return None
    def u(s_):
        p = s_['pts']; q = p[1] if s_['a'] == k else p[-2]; L = math.hypot(q[0] - n['x'], q[1] - n['y']) or 1
        return ((q[0] - n['x']) / L, (q[1] - n['y']) / L)
    us = [(s_, u(s_)) for o_, s_ in ADJ[k]]
    for i in range(3):
        for j in range(i + 1, 3):
            (s1, u1), (s2, u2) = us[i], us[j]
            if u1[0] * u2[0] + u1[1] * u2[1] < -.98 and s1['road'] == s2['road'] and CLS[s1['cls']]['median_m'] > 0 and CLS[s2['cls']]['median_m'] > 0:
                return next(uu for ss, uu in us if ss is not s1 and ss is not s2)
    return None
def far_side(g, k, x, y):
    """a point on the other side of the median from a right-in/right-out junction: the junction is not there"""
    sd = _riro_side(g, k); n = g['N'][k]
    return bool(sd) and (x - n['x']) * sd[0] + (y - n['y']) * sd[1] < 0
def junc_for(g, k, s_, r, side):
    """is node k a junction for a bay on this side of the segment (r — the right of travel a→b)"""
    if k not in g['JUNC']: return False
    sd = _riro_side(g, k)
    return not (sd and r[0] * side * sd[0] + r[1] * side * sd[1] < 0)
def perp_half(g, k, s_):   # as round 8b (R-76): the half width of the street the crossing on s_ at k crosses
    N_, ADJ, CLS = g['N'], g['ADJ'], g['CLS']; n = N_[k]
    p_ = s_['pts']; q_ = p_[1] if s_['a'] == k else p_[-2]; ex, ey = q_[0] - n['x'], q_[1] - n['y']; el = math.hypot(ex, ey) or 1; h = 0
    for oo, t in ADJ[k]:
        if t is s_: continue
        pt = t['pts']; r_ = pt[1] if t['a'] == k else pt[-2]; qx, qy = r_[0] - n['x'], r_[1] - n['y']; ql = math.hypot(qx, qy) or 1
        if abs((ex * qx + ey * qy) / (el * ql)) < .7: h = max(h, CLS[t['cls']]['halfW'])
    return h
def xw_final(g):   # the crosswalks of the new junction — at the stop line (R-76) from the start
    sb = {s_['id']: s_ for s_ in g['SEG']}
    for x in g['XW']:
        if x['node'] == J_W: hc = perp_half(g, x['node'], sb[x['seg']]); x['d0'], x['d1'] = round(hc + 10), round(hc + 50)
def xw_at(g, x):   # where a crosswalk is, for the bays of the segments new in this round: its real place (R-76)
    if x['seg'] in SPLIT and g['N'][x['node']]['kind'] != 'roundabout':
        sb = g.setdefault('_r9k_sb', {s_['id']: s_ for s_ in g['SEG']}); hc = perp_half(g, x['node'], sb[x['seg']])
        if hc: return round(hc + 10), round(hc + 50)
    return x['d0'], x['d1']
def pairs_all(rt):
    out = list(zip(rt['path'], rt['path'][1:]))
    if rt.get('back'): out += list(zip(rt['back'], rt['back'][1:]))
    return out
def walk(line):
    out = [(a, b, False) for a, b in zip(line['path'], line['path'][1:])]
    if line.get('back'): out += [(a, b, True) for a, b in zip(line['back'], line['back'][1:])]
    return out
def plen_nodes(seq, SEGBY): return sum(SEGBY[frozenset((a, b))]['len_m'] * 10 for a, b in zip(seq, seq[1:]))
def open_cycle(line, SEGBY, L_, v_px, LAY):   # an out-and-back line: out on its path, back on 'back' (or the path reversed)
    Lb = plen_nodes(line['back'], SEGBY) if line.get('back') else L_
    return (L_ + Lb) / v_px + 2 * LAY
def ring_buses(line, SEGBY, L_, v_px, LAY, runs, cyc):
    if line.get('back') and runs == 2:
        return math.ceil(cyc / line['headway_s']) + math.ceil((plen_nodes(line['back'], SEGBY) / v_px + LAY) / line['headway_s'])
    return runs * math.ceil(cyc / line['headway_s'])
def term_bad(line):
    out = []; p = line['path']; closed = p[0] == p[-1] or {p[0], p[-1]} <= TERM_NODES
    if closed and p[-1] not in TERM_NODES: out.append(f"קו {line['id']} לא חוזר למסוף")
    b = line.get('back')
    if b:
        if closed and not (b[0] in TERM_NODES and b[-1] in TERM_NODES): out.append(f"קו {line['id']} — הכיוון השני לא מהמסוף ובחזרה")
        if not closed and not (b[0] == p[-1] and b[-1] in TERM_NODES): out.append(f"קו {line['id']} — החזרה לא מהקצה אל המסוף")
    return out

ST01_WHY = ('סבב 9כ: הקטע נחתך בשער המערבי של המסוף (J46_185 — ימינה בלבד, בצד המזרחי); היציאה של סוכנות הרכב (D‑480) מיד אחרי המפרץ דרומה; '
            'המפרץ נשאר לפי הכלל של סבב 5 (20 מ׳ ממרכז הצומת)')
PATCH = [   # (old text of plan7b_build.py, new text) — each must occur exactly once
    ("STOP_DEC = {", "STOP_DEC = {" + repr('וילות ושירותי רכב (D3)') + ': R9K.ST01_WHY, '),
    ("SEG.append(dict(id=f\"{rd['id']}/{i + 1}\", road=rd['id']", "SEG.append(dict(id=rd.get('seg_ids', {}).get(i, f\"{rd['id']}/{i + 1}\"), road=rd['id']"),
    ("        d = pos[b] - pos[a]; mins[rd['cls']] = min(mins.get(rd['cls'], 1e9), d)\n",
     "        d = pos[b] - pos[a]\n"
     "        if (rd['id'], a, b) in R9K.R15_EXC: R9K.R15_GOT.append(f\"{rd['id']}: {a}–{b} {d / 10:.0f} מ׳ — {R9K.R15_EXC[(rd['id'], a, b)]}\"); continue\n"
     "        mins[rd['cls']] = min(mins.get(rd['cls'], 1e9), d)\n"),
    ("\n# angles: every junction's arms", "\nchecks[-1]['det'] += R9K.r15_txt()\n# angles: every junction's arms"),
    ("        for a, b in zip(rt['path'], rt['path'][1:]):\n            if not any(o == b", "        for a, b in R9K.pairs_all(rt):\n            if not any(o == b"),
    ("            for a, b in zip(rt['path'], rt['path'][1:]):\n                s = next(", "            for a, b in R9K.pairs_all(rt):\n                s = next("),
    ("    near = min(math.hypot(N[x]['x'] - d['at'][0], N[x]['y'] - d['at'][1]) for x in JUNC)",
     "    near = min(math.hypot(N[x]['x'] - d['at'][0], N[x]['y'] - d['at'][1]) for x in JUNC if not R9K.far_side(globals(), x, d['at'][0], d['at'][1]))"),
    ("\ndef seg_frame(a, b):", "\nR9K.xw_final(globals())\ndef seg_frame(a, b):"),
    ("for s in SEG:\n    if s['id'] in STAGE_WAIT:", "STAGE_WAIT[R9K.S_W] = ('S9', R9K.WAIT_W)\nfor s in SEG:\n    if s['id'] in STAGE_WAIT:"),
    ("        if x['node'] == a: out.append((x['d0'] - 20, x['d1'] + 20, 'מעבר חצייה ' + a))\n        else: out.append((L_ - x['d1'] - 20, L_ - x['d0'] + 20, 'מעבר חצייה ' + b))",
     "        d0_, d1_ = R9K.xw_at(globals(), x)\n        if x['node'] == a: out.append((d0_ - 20, d1_ + 20, 'מעבר חצייה ' + a))\n        else: out.append((L_ - d1_ - 20, L_ - d0_ + 20, 'מעבר חצייה ' + b))"),
    ("(200 if a == ahead else 100)) if a in JUNC else 50; eb = (cross_hw(b, s_['road']) + (200 if b == ahead else 100)) if b in JUNC else 50",
     "(200 if a == ahead else 100)) if R9K.junc_for(globals(), a, s_, r, side) else 50; eb = (cross_hw(b, s_['road']) + (200 if b == ahead else 100)) if R9K.junc_for(globals(), b, s_, r, side) else 50"),
    ("lo, hi = (200 if a in JUNC else 50), L_ - (200 if b in JUNC else 50) - BAYL",
     "lo, hi = (200 if R9K.junc_for(globals(), a, s_, r, side) else 50), L_ - (200 if R9K.junc_for(globals(), b, s_, r, side) else 50) - BAYL"),
    ("ja = (t0 - cross_hw(a, s_['road'])) if a in JUNC else None; jb = (L_ - t0 - BAYL - cross_hw(b, s_['road'])) if b in JUNC else None",
     "ja = (t0 - cross_hw(a, s_['road'])) if R9K.junc_for(globals(), a, s_, r, sd) else None; jb = (L_ - t0 - BAYL - cross_hw(b, s_['road'])) if R9K.junc_for(globals(), b, s_, r, sd) else None"),
    ("    if line['twoway']: dirs |= {(b, a) for a, b in dirs}",
     "    if line['twoway']: dirs |= (set(zip(line['back'], line['back'][1:])) if line.get('back') else {(b, a) for a, b in dirs})"),
    ("    closed = line['path'][0] == line['path'][-1]\n", "    closed = line['path'][0] == line['path'][-1] or {line['path'][0], line['path'][-1]} <= R9K.TERM_NODES\n"),
    ("runs = 2 if line['twoway'] else 1; buses = runs * math.ceil(cyc / line['headway_s'])",
     "runs = 2 if line['twoway'] else 1; buses = R9K.ring_buses(line, SEGBY, L_, v_px, LAYOVER, runs, cyc)"),
    ("    else: cyc = 2 * L_ / v_px + 2 * LAYOVER; runs = 1", "    else: cyc = R9K.open_cycle(line, SEGBY, L_, v_px, LAYOVER); runs = 1"),
    ("    for a, b in zip(line['path'], line['path'][1:]):\n        r_ = SEGBY[frozenset((a, b))]['road']\n        if not line['road_seq'] or line['road_seq'][-1] != r_: line['road_seq'].append(r_)",
     "    for a, b, bk_ in R9K.walk(line):\n        r_ = SEGBY[frozenset((a, b))]['road']\n        seq_ = line.setdefault('road_seq_back', []) if bk_ else line['road_seq']\n        if not seq_ or seq_[-1] != r_: seq_.append(r_)"),
    ("    if not (line['path'][0] == 'E54_20'): stop_bad.append(f\"קו {line['id']} לא יוצא מהמסוף\")",
     "    if not (line['path'][0] in R9K.TERM_NODES): stop_bad.append(f\"קו {line['id']} לא יוצא מהמסוף\")\n    stop_bad.extend(R9K.term_bad(line))"),
]
def patch_build(src):
    for a, b in PATCH:
        assert src.count(a) == 1, ('plan7b_build.py changed — not once:', a[:80], src.count(a))
        src = src.replace(a, b, 1)
    return src
_run_path9j = runpy.run_path
def _run_path(path, init_globals=None, run_name=None):
    if os.path.basename(path) == 'plan7b_build.py':   # round 9י's patch (the reason of ST-01) is here too, with this round's text
        src = patch_build(open(path, encoding='utf-8').read())
        g = dict(init_globals or {}); g.update(__name__=run_name or '<run_path>', __file__=path, R9K=sys.modules[__name__])
        exec(compile(src, path, 'exec'), g); return g
    return _run_path9j(path, init_globals=init_globals, run_name=run_name)
runpy.run_path = _run_path

# ---------------------------------------------------------------- the checks of this round
def _turn(N_, p, k, q):
    a, b, c = N_[p], N_[k], N_[q]; d1 = (b['x'] - a['x'], b['y'] - a['y']); d2 = (c['x'] - b['x'], c['y'] - b['y'])
    cr = d1[0] * d2[1] - d1[1] * d2[0]; dt = d1[0] * d2[0] + d1[1] * d2[1]; L = (math.hypot(*d1) * math.hypot(*d2)) or 1
    if dt < 0 and abs(cr) / L < .2: return 'פרסה'
    return 'ישר' if abs(cr) / L < .2 else ('ימינה' if cr > 0 else 'שמאלה')   # y down: a right turn has a positive cross product
def runs_of(rt, kind):
    p = rt['path']
    if rt.get('back'): return [('הלוך', p), ('חזור', rt['back'])]
    if kind == 'bus' and not rt.get('twoway'): return [('לולאה', p)]
    return [('הלוך', p), ('חזור', p[::-1])]
def gate_of(n): return {E_W: 'מערבי', 'E54_20': 'דרומי'}.get(n)
def line_gates():
    out = {}
    for ln in NET.ROUTES['bus']:
        ex, en = set(), set()
        for nm, seq in runs_of(ln, 'bus'):
            if gate_of(seq[0]): ex.add(gate_of(seq[0]))
            if gate_of(seq[-1]): en.add(gate_of(seq[-1]))
        out[ln['id']] = (ex, en)
    return out
WANT = {'out_w': {'1', '2', '4', '6'}, 'in_w': {'1', '3'}, 'out_s': {'1', '3', '5'}, 'in_s': {'1', '2', '4', '5', '6'}}
DONE9K = {}
_chk9j = R7.checks
def checks(ctx, I):
    g = sys._getframe(1).f_globals
    g['__r9k_chk'] = _chk9j
    out = list(eval('__r9k_chk(__r9k_ctx, __r9k_I)', g, {'__r9k_ctx': ctx, '__r9k_I': I}))
    N_, XW, SEG, TERM, CW = g['N'], g['XW'], g['SEG'], g['TERM'], g['CW']; sb = {s_['id']: s_ for s_ in SEG}; bad = []
    rd = next((r for r in g['Rd'] if r['id'] == R_W), None); s_ = sb.get(S_W)
    if not rd or not s_ or rd['nodes'] != [J_W, E_W] or rd['lanes'] != '1+1' or not g['CLS'][s_['cls']]['twoway']: bad.append('אין כביש 1+1 של השער')
    if N_[J_W]['kind'] != 'riro' or J_W not in next(r for r in g['Rd'] if r['id'] == 'AR-E')['nodes']: bad.append(f'{J_W} לא צומת ימינה בלבד על שדרת המזרח')
    cw = CW(s_['cls']) if s_ else 78; hw = g['CLS'][s_['cls']]['halfW'] if s_ else 54
    x16 = next((x for x in XW if x['node'] == 'J46_16' and x['seg'] == 'AR-E/1a'), None)
    z1 = x16['at'][1] + x16['d1'] if x16 else 0
    gap, gap_w = (Y_W - cw / 2 - z1) / 10, (Y_W - hw - z1) / 10
    if not x16 or gap <= 0 or gap_w < 0: bad.append(f'על המעבר של J46_16 ({gap:.1f} מ׳)')
    x0, y0, x1, y1 = TERM['rect']; R = TERM['corner_r']; yn = Y_W - cw / 2
    xa = (x0 + R - math.sqrt(max(0.0, R * R - (y0 + R - yn) ** 2))) if yn < y0 + R else x0
    if N_[E_W]['x'] < xa: bad.append(f'לא מגיע לאספלט (x {N_[E_W]["x"]} < {xa:.0f})')
    G = line_gates()
    got = {'out_w': {k for k, (ex, en) in G.items() if 'מערבי' in ex}, 'in_w': {k for k, (ex, en) in G.items() if 'מערבי' in en},
           'out_s': {k for k, (ex, en) in G.items() if 'דרומי' in ex}, 'in_s': {k for k, (ex, en) in G.items() if 'דרומי' in en}}
    for k_ in WANT:
        if got[k_] != WANT[k_]: bad.append(f"{k_}: {sorted(got[k_], key=int)} ולא {sorted(WANT[k_], key=int)}")
    onw = sorted({ln['id'] for ln in NET.ROUTES['bus'] if any({a, b} == {J_W, E_W} for a, b in pairs_all(ln))}, key=int)
    xw_w = sorted(x['seg'] for x in XW if x['node'] == J_W)
    st1 = next((st for st in g['STOPS'] if st.get('key') == frozenset((J_W, 'J46_25')) or st.get('key') == sorted((J_W, 'J46_25'))), None)
    bays = '; '.join(f"{bb['dir']}: y {min(q[1] for q in bb['poly']):.0f}–{max(q[1] for q in bb['poly']):.0f}, {bb['near_m']} / {bb['far_m'] if bb['far_m'] is not None else '—'} מ׳{' (חריגה)' if bb.get('relaxed') else ''}" for bb in (st1 or {}).get('bay_list', []))
    DONE9K.update(gap=round(gap, 1), gap_walk=round(gap_w, 1), asphalt_x=round(xa, 1), gates={k: dict(out=sorted(v[0]), back=sorted(v[1])) for k, v in G.items()}, on_gate=onw, xw=xw_w,
                  st01=[dict(dir=bb['dir'], y=[min(q[1] for q in bb['poly']), max(q[1] for q in bb['poly'])], near_m=bb['near_m'], far_m=bb['far_m'], relaxed=bb.get('relaxed')) for bb in (st1 or {}).get('bay_list', [])])
    out.append(('סבב 9כ — השער המערבי של המסוף: כביש 1+1 ברשת (J46_185 ימינה בלבד ← E49_185), דרומית למעבר של J46_16 ועד האספלט של המסוף; כל קו בשער שמתאים לו (הבעלים 18:40)',
                not bad,
                f"LC-E3W ‏{s_['len_m'] if s_ else '—'} מ׳, נתיב לכל כיוון — נכנסים בדרומי, יוצאים בצפוני; הכביש מתחיל {gap:.1f} מ׳ דרומית למעבר של הזרוע הדרומית של J46_16 "
                f"(המדרכה שלו — {gap_w:.1f} מ׳), והקצה ב-x {N_[E_W]['x']} — מעבר לפינה המעוגלת (האספלט ב-x {xa:.0f} בשפה הצפונית). "
                f"יוצאים בשער המערבי: {', '.join(sorted(got['out_w'], key=int))}; נכנסים בו: {', '.join(sorted(got['in_w'], key=int))}; "
                f"יוצאים בשער הדרומי: {', '.join(sorted(got['out_s'], key=int))}; נכנסים בו: {', '.join(sorted(got['in_s'], key=int))}. "
                f"הקווים על השער: {', '.join(onw)}. המעברים ב-J46_185: {', '.join(xw_w)}. ST-01: {bays}." + (' · לא: ' + '; '.join(bad) if bad else '')))
    # no left turn at a right-in/right-out junction, on every route of the map
    rr = [k for k, n in N_.items() if n['kind'] == 'riro']; tb = []; cnt = {}
    for kind, L_ in NET.ROUTES.items():
        for rt in L_:
            for nm, seq in runs_of(rt, kind):
                for p_, k_, q_ in zip(seq, seq[1:], seq[2:]):
                    if k_ in rr:
                        t = _turn(N_, p_, k_, q_); cnt[(k_, t)] = cnt.get((k_, t), 0) + 1
                        if t in ('שמאלה', 'פרסה'): tb.append(f"{rt['id']} ({nm}): {p_} → {k_} → {q_} {t}")
    out.append(('סבב 9כ — בצומת ימינה בלבד אין פנייה שמאלה: כל הקווים (אוטובוס, משאיות, חירום) עוברים ישר או פונים ימינה', not tb,
                ' · '.join(f"{k}: " + ', '.join(f"{t} {c}" for (k2, t), c in sorted(cnt.items()) if k2 == k) for k in sorted(rr)) + '.' + (' לא: ' + '; '.join(tb) if tb else '')))
    return out
R7.checks = checks

# ---------------------------------------------------------------- the drawing: the gate's lanes and arrows, the yard reached, the lines through the gate
TITLE = 'תוכנית הדרכים של כל העיר — סבב 9כ'
_lay9j = SV.label_layout
def label_layout(P_):
    o = _lay9j(P_); P_['title'] = TITLE; P_['batch'] = '9כ'; return o
SV.label_layout = label_layout

_model9j = SV.model
def model(P_, GR_=None):
    """the median and the lane lines of the avenue go on through the right-in/right-out junction (no opening, no left turn)"""
    M_ = _model9j(P_, GR_)
    for k_, end in (('AR-E/1a', 1), ('AR-E/1', 0)):
        if k_ in M_['cuts']: c = list(M_['cuts'][k_]); c[end] = 0; M_['cuts'][k_] = tuple(c)
    return M_
SV.model = model

def _chev(x, y, ux, uy, h=12):
    return f"M{SV.f1(x - ux * 12 - uy * h)},{SV.f1(y - uy * 12 + ux * h)}L{SV.f1(x + ux * 6)},{SV.f1(y + uy * 6)}L{SV.f1(x - ux * 12 + uy * h)},{SV.f1(y - uy * 12 - ux * h)}"
ARROW_X = 4846
_rp9j = SV.road_parts
def road_parts(pid, p, g, cut=(0, 0), caps=()):
    """the gate: two-way, one lane each way — a chevron in each lane, in its direction (in: the south lane eastbound; out: the north lane westbound)"""
    base, top, lane = _rp9j(pid, p, g, cut, caps)
    if pid == SV.sid(S_W):
        q = g['cw'] / 4; col = SV.STY[g['st']][1] or '#666'
        ch = _chev(ARROW_X, Y_W + q, 1, 0) + _chev(ARROW_X, Y_W - q, -1, 0)
        lane = lane[:-4] + f"<path d='{ch}' class='arw' stroke='{col}'/>" + '</g>'
    return base, top, lane
SV.road_parts = road_parts

def _pieces(seq, have):
    out = []; cur = None
    for a, b in zip(seq, seq[1:]):
        if frozenset((a, b)) in have: cur = None; continue
        if cur is None: cur = [a]; out.append(cur)
        cur.append(b)
    return out
def _with_back(lines):   # each line with 'back': its path, and the pieces of its back that the path does not have — for the drawing
    ext = []
    for ln in lines:
        ext.append(ln)
        if ln.get('back'):
            have = {frozenset(x) for x in zip(ln['path'], ln['path'][1:])}
            ext += [dict(ln, path=pc) for pc in _pieces(ln['back'], have)]
    return ext
_bus9j = SV.bus_layer
def bus_layer(P_, M_):
    """the lines drawn on both their runs; the west gate opens the yard's edge; the yellow box in the right lane northbound in front of the gate"""
    P2 = dict(P_, routes=dict(P_['routes'], bus=_with_back(P_['routes']['bus'])))
    o = _bus9j(P2, M_)
    if not o: return o
    T_ = P_['bus']['terminal']; gx, gy = T_['gate']; key = f"<rect x='{gx - 45}' y='{gy - 4}' width='90' height='14' fill='#5b636e'/>"
    assert o.count(key) == 1
    CL = M_['CLS']; hc = round(CL['local']['lane_m'] * 10); kx1 = 4600 + CL['main']['halfW'] - CL['main']['walk_m'] * 10; ln_ = CL['main']['lane_m'] * 10
    add = (f"<rect x='4874' y='{Y_W - hc}' width='{X_W + 6 - 4874}' height='{2 * hc}' fill='#5b636e'/>"
           f"<rect x='{SV.f1(kx1 - ln_)}' y='{Y_W - hc}' width='{SV.f1(ln_)}' height='{2 * hc}' fill='url(#kcp)' stroke='#f2c200' stroke-width='4'/>")
    return o.replace(key, key + add, 1)
SV.bus_layer = bus_layer

def bus_badges(P):
    """as plan7b_svg.bus_badges — with the back of each line, and a fixed order among equals"""
    if not P.get('bus'): return []
    SEGBY = {frozenset((s['a'], s['b'])): s for s in P['segments']}; use = {}
    def keys(ln): return [frozenset(x) for x in pairs_all(ln)]
    for ln in P['routes']['bus']:
        for k in keys(ln): use.setdefault(k, set()).add(ln['id'])
    out = []
    for ln in P['routes']['bus']:
        cand = sorted(set(keys(ln)), key=lambda k: (len(use[k]), -SEGBY[k]['len_m'], sorted(k)))
        picked = []
        for k in cand:
            s = SEGBY[k]; p = s['pts']; mx, my = (p[0][0] + p[-1][0]) / 2, (p[0][1] + p[-1][1]) / 2
            if s['len_m'] < 50 or any(math.hypot(mx - a, my - b) < 2500 for a, b in picked): continue
            ids = sorted(use[k], key=int); i = ids.index(ln['id']); off = (i - (len(ids) - 1) / 2) * 18
            dx, dy = p[-1][0] - p[0][0], p[-1][1] - p[0][1]; L = math.hypot(dx, dy) or 1; mx += dy / L * off; my -= dx / L * off
            picked.append((mx, my)); out.append((ln, mx, my))
            if len(picked) == 2: break
    return out
SV.bus_badges = bus_badges

_hov9j = SV.hover_data
def hover_data(P_, GR_, M_):
    """the hover card of a line on the segments of its back too"""
    s = _hov9j(P_, GR_, M_); pre, suf = "<script>window.__MAP=", ";</script>"
    assert s.startswith(pre) and s.endswith(suf)
    D = json.loads(s[len(pre):-len(suf)]); SEGBY = {frozenset((x['a'], x['b'])): x for x in P_['segments']}; e = SV.e; n_add = 0
    for ln in P_['routes']['bus']:
        if not ln.get('back'): continue
        t = (f"<b>קו {e(ln['id'])} — {e(ln['name'])}</b><div>{'בשני הכיוונים' if ln['twoway'] else 'לולאה בכיוון אחד'} · {ln['len_km']} ק״מ · כל {ln['headway_s']} שנ׳ · "
             f"{ln['buses']} אוטובוסים</div><div class='tl'>{e(ln['why'])}</div>")
        ti = D['info'].index(t); have = {frozenset(x) for x in zip(ln['path'], ln['path'][1:])}
        for a, b in zip(ln['back'], ln['back'][1:]):
            if frozenset((a, b)) in have: continue
            have.add(frozenset((a, b))); sg = SEGBY[frozenset((a, b))]['pts']
            for i in range(len(sg) - 1): D['bus'].append([round(sg[i][0], 1), round(sg[i][1], 1), round(sg[i + 1][0], 1), round(sg[i + 1][1], 1), 30, ti]); n_add += 1
    DONE9K['hover_back'] = n_add
    return pre + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + suf
SV.hover_data = hover_data

_ji9j = SV.junction_icons
def junction_icons(P_, nodes=None, near=None):
    """on a stage map (nodes = the nodes built by then), J46_185 is a junction only from the stage that builds the gate (E49_185 built)"""
    if nodes is not None and J_W in nodes and E_W not in nodes: nodes = set(nodes) - {J_W}
    return _ji9j(P_, nodes=nodes, near=near)
SV.junction_icons = junction_icons

# ================================================================ 3 · the page: the section of round 9כ (before 9י — which stays as it was, as history)
FLOW = ('חד-סטרי סביב כל אי: בצד הצפוני של האי מזרחה, ובצד הדרומי מערבה — הדלת הימנית של האוטובוס פונה תמיד לרציף. '
        'מי שנכנס בשער המערבי עובר מיד לנתיב הצפוני של החצר (מזרחה) — מצפון לבניין הסדרן; מי שיוצא בו מגיע מהצד המערבי של האיים, צפונה, ופונה אל הנתיב הצפוני של השער.')
def gates_rec():
    G = line_gates()
    w = dict(junction=J_W, node=E_W, road=R_W, at=[4600, Y_W], to=[X_W, Y_W], lane_in=[4752, Y_W + 19.5, X_W, Y_W + 19.5], lane_out=[X_W, Y_W - 19.5, 4752, Y_W - 19.5],
             turn_in='ימינה פנימה מהנתיבים צפונה של שדרת המזרח, אל הנתיב הדרומי של השער', turn_out='יציאה בנתיב הצפוני של השער, ימינה החוצה — צפונה, אל J46_16',
             lines_out=sorted((k for k, v in G.items() if 'מערבי' in v[0]), key=int), lines_in=sorted((k for k, v in G.items() if 'מערבי' in v[1]), key=int))
    s = dict(R9J.GATES['s'], lines_out=sorted((k for k, v in G.items() if 'דרומי' in v[0]), key=int), lines_in=sorted((k for k, v in G.items() if 'דרומי' in v[1]), key=int))
    return {'w': w, 's': s}

def keep_9j():
    """the 9י record and its section of the page, as they are now (before this run rebuilds the files) — history"""
    P_ = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8'))
    T = open(os.path.join(HERE, 'city_plan.html'), encoding='utf-8').read()
    a = T.index('<h2>סבב 9י'); b = T.index('<h2>סבב 9ט'); assert a < b
    return P_['r9j'], T[a:b]

def _chips(ids, col, x, y, r=17):
    o = []
    for i, k in enumerate(ids):
        cx = x + i * (2 * r + 6)
        o.append(f"<circle cx='{cx}' cy='{y}' r='{r}' fill='{col[k]}' stroke='#fff' stroke-width='3'/><text x='{cx}' y='{y + 8}' font-size='23' font-weight='700' text-anchor='middle' fill='#fff'>{E(k)}</text>")
    return ''.join(o)
def terminal_svg(P_):
    T = P_['bus']['terminal']; G = T['gates']; col = {l['id']: l['color'] for l in P_['routes']['bus']}
    x0, y0, x1, y1 = 4060, 1450, 5770, 2430
    o = [f"<svg viewBox='{x0} {y0} {x1 - x0} {y1 - y0}' role='img' aria-label='המסוף עם שני השערים, סבב 9כ' style='width:100%;max-width:980px;height:auto;background:#f4f2ec;border-radius:10px'>",
         "<defs><marker id='ar9k' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0L10,5L0,10z' fill='#c8372d'/></marker>"
         "<marker id='ar9kb' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0L10,5L0,10z' fill='#2a6fdb'/></marker>"
         "<marker id='ar9kk' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0L10,5L0,10z' fill='#333'/></marker>"
         "<pattern id='kc9k' width='24' height='24' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='24' stroke='#f2c200' stroke-width='5'/></pattern></defs>"]
    rd = '#8d949b'
    o.append(f"<rect x='{x0}' y='1448' width='{4900 - x0}' height='304' fill='{rd}'/><text x='4250' y='1612' font-size='28' text-anchor='middle' fill='#fff'>שדרת השדה</text>")
    o.append(f"<rect x='4448' y='1600' width='304' height='{y1 - 1600}' fill='{rd}'/><rect x='4590' y='1752' width='20' height='{y1 - 1752}' fill='#9cbf86'/>")
    o.append("<text x='4520' y='2330' font-size='44' text-anchor='middle' fill='#fff'>↓</text><text x='4680' y='2330' font-size='44' text-anchor='middle' fill='#fff'>↑</text>"
             "<text x='4600' y='2410' font-size='26' text-anchor='middle' fill='#333'>שדרת המזרח</text>")
    o.append("<text x='4600' y='1560' font-size='24' text-anchor='middle' fill='#fff'>J46_16</text>")
    o.append(''.join(f"<rect x='{x}' y='1762' width='12' height='40' fill='#fff'/>" for x in range(4478, 4722, 22)))            # the crossing of J46_16 (south arm)
    o.append("<text x='4300' y='1790' font-size='22' text-anchor='middle' fill='#333'>המעבר של J46_16</text><line x1='4385' y1='1782' x2='4470' y2='1782' stroke='#333' stroke-width='2'/>")
    # the gate: the road, its centre line, its crossing, the lanes in and out
    o.append(f"<rect x='4752' y='{Y_W - 54}' width='{4895 - 4752}' height='108' fill='#e2ded3'/><rect x='4752' y='{Y_W - 39}' width='{4895 - 4752}' height='78' fill='{rd}'/>")
    o.append(f"<line x1='4812' y1='{Y_W}' x2='4890' y2='{Y_W}' stroke='#fff' stroke-width='4' stroke-dasharray='14 10'/>")
    o.append(''.join(f"<rect x='4762' y='{y}' width='40' height='9' fill='#fff'/>" for y in range(Y_W - 36, Y_W + 36, 17)))   # the crossing on the gate
    o.append(''.join(f"<rect x='{x}' y='{Y_W + 64}' width='12' height='40' fill='#fff'/>" for x in range(4478, 4722, 22)))     # the crossing on the avenue (T rule)
    o.append(f"<rect x='4688' y='{Y_W - 39}' width='39' height='78' fill='url(#kc9k)' stroke='#f2c200' stroke-width='4'/>")      # the yellow box
    o.append(f"<path d='M4708,{Y_W + 150} Q4708,{Y_W + 20} 4800,{Y_W + 20} L4888,{Y_W + 20}' fill='none' stroke='#c8372d' stroke-width='8' marker-end='url(#ar9k)'/>")
    o.append(f"<path d='M4888,{Y_W - 20} L4800,{Y_W - 20} Q4708,{Y_W - 20} 4708,{Y_W - 48}' fill='none' stroke='#2a6fdb' stroke-width='8' marker-end='url(#ar9kb)'/>")
    for st in P_['bus']['stops']:   # ST-01 — both bays
        if st.get('id') == 'ST-01':
            for bb in st['bay_list']:
                o.append(f"<polygon points='{SV.pts(bb['poly'])}' fill='#5b636e' stroke='#f2c200' stroke-width='4' stroke-dasharray='12 8'/>")
                px, py = bb['pole']; o.append(f"<text x='{px + (-44 if px < 4600 else 44)}' y='{py + 8}' font-size='22' text-anchor='middle' fill='#333'>ST-01</text>")
    # the yard
    tx0, ty0, tx1, ty1 = T['rect']; R = T['corner_r']
    o.append(f"<rect x='{tx0}' y='{ty0}' width='{tx1 - tx0}' height='{ty1 - ty0}' rx='{R}' fill='#b9bec4' stroke='#555' stroke-width='4'/>")
    o.append(f"<rect x='4874' y='{Y_W - 39}' width='{X_W + 6 - 4874}' height='78' fill='#b9bec4'/>")
    for p in T['platforms']:
        q = p['rect']; o.append(f"<rect x='{q[0]}' y='{q[1]}' width='{q[2] - q[0]}' height='{q[3] - q[1]}' fill='#e9e3d2' stroke='#777'/><text x='{(q[0] + q[2]) // 2}' y='{q[3] - 4}' font-size='26' text-anchor='middle'>אי {E(p['id'])}</text>")
    for h in T['hold']:
        q = h['rect']; o.append(f"<rect x='{q[0]}' y='{q[1]}' width='{q[2] - q[0]}' height='{q[3] - q[1]}' fill='none' stroke='#666' stroke-dasharray='10 6'/>")
    wb = (T.get('r9') or {}).get('west', {}).get('building')
    if wb: o.append(f"<rect x='{wb[0]}' y='{wb[1]}' width='{wb[2] - wb[0]}' height='{wb[3] - wb[1]}' fill='#e8dcc4' stroke='#6b5a3a' stroke-width='3'/><text x='{(wb[0] + wb[2]) / 2}' y='{(wb[1] + wb[3]) / 2 + 9}' font-size='22' text-anchor='middle' fill='#6b5a3a'>סדרן</text>")
    for (xa, ya, xb, yb) in [(5080, 1877, 5520, 1877), (5520, 1943, 5080, 1943), (5080, 2047, 5520, 2047), (5520, 2113, 5080, 2113)]:
        o.append(f"<line x1='{xa}' y1='{ya}' x2='{xb}' y2='{yb}' stroke='#333' stroke-width='5' stroke-dasharray='26 14' marker-end='url(#ar9kk)'/>")
    o.append(f"<path d='M4896,{Y_W + 20} C4950,{Y_W + 20} 4960,1840 5040,1840' fill='none' stroke='#c8372d' stroke-width='6' stroke-dasharray='18 10' marker-end='url(#ar9k)'/>")
    o.append(f"<path d='M4914,2010 L4914,1905 Q4914,{Y_W - 20} 4896,{Y_W - 20}' fill='none' stroke='#2a6fdb' stroke-width='6' stroke-dasharray='18 10' marker-end='url(#ar9kb)'/>")
    # the south gate
    o.append(f"<rect x='5360' y='{ty1}' width='80' height='{y1 - ty1}' fill='{rd}'/><text x='5400' y='2410' font-size='24' text-anchor='middle' fill='#fff'>LC-E3</text>")
    o.append("<line x1='5420' y1='2270' x2='5420' y2='2180' stroke='#c8372d' stroke-width='7' marker-end='url(#ar9k)'/><line x1='5380' y1='2180' x2='5380' y2='2270' stroke='#2a6fdb' stroke-width='7' marker-end='url(#ar9kb)'/>")
    # the gates and their lines
    w, s = G['w'], G['s']
    o.append("<rect x='4075' y='1830' width='250' height='240' rx='10' fill='#fff' stroke='#333' stroke-width='2'/>"
             "<text x='4200' y='1866' font-size='25' font-weight='700' text-anchor='middle'>השער המערבי</text>"
             f"<text x='4200' y='1900' font-size='21' text-anchor='middle' fill='#2a6fdb'>יוצאים</text>{_chips(w['lines_out'], col, 4200 - (len(w['lines_out']) - 1) * 20, 1932)}"
             f"<text x='4200' y='1984' font-size='21' text-anchor='middle' fill='#c8372d'>נכנסים</text>{_chips(w['lines_in'], col, 4200 - (len(w['lines_in']) - 1) * 20, 2016)}"
             f"<text x='4200' y='2058' font-size='19' text-anchor='middle' fill='#555'>{E(J_W)} · {E(R_W)}</text>"
             f"<line x1='4325' y1='1850' x2='4760' y2='{Y_W}' stroke='#333' stroke-width='2' stroke-dasharray='6 5'/>")
    o.append("<rect x='5470' y='2190' width='290' height='230' rx='10' fill='#fff' stroke='#333' stroke-width='2'/>"
             "<text x='5615' y='2226' font-size='25' font-weight='700' text-anchor='middle'>השער הדרומי</text>"
             f"<text x='5615' y='2260' font-size='21' text-anchor='middle' fill='#2a6fdb'>יוצאים</text>{_chips(s['lines_out'], col, 5615 - (len(s['lines_out']) - 1) * 20, 2292)}"
             f"<text x='5615' y='2344' font-size='21' text-anchor='middle' fill='#c8372d'>נכנסים</text>{_chips(s['lines_in'], col, 5615 - (len(s['lines_in']) - 1) * 20, 2376)}"
             "<text x='5615' y='2412' font-size='19' text-anchor='middle' fill='#555'>E54_20</text>")
    o.append("<g transform='translate(5715,1520)'><path d='M0,-44 L17,0 L0,-11 L-17,0 Z' fill='#222'/><text x='0' y='32' font-size='28' text-anchor='middle'>צפון</text></g>")
    o.append("<text x='5735' y='1990' font-size='30' text-anchor='middle' fill='#222'>מזרח</text><text x='4140' y='2300' font-size='30' text-anchor='middle' fill='#222'>מערב</text>")
    o.append('</svg>')
    return ''.join(o)

def _run_rows(P_):
    rows = []; G = line_gates()
    for ln in P_['routes']['bus']:
        cells_o, cells_b = [], []
        for nm, seq in runs_of(ln, 'bus'):
            ring = (seq[0] in TERM_NODES and seq[-1] in TERM_NODES)
            if ring and ln.get('twoway'):
                xs = [P_['_N'][k]['x'] for k in seq]; ys = [P_['_N'][k]['y'] for k in seq]
                a2 = sum(xs[i] * ys[i + 1] - xs[i + 1] * ys[i] for i in range(len(seq) - 1)) + xs[-1] * ys[0] - xs[0] * ys[-1]
                nm = 'עם כיוון השעון' if a2 > 0 else 'נגד כיוון השעון'   # y down: a positive area turns clockwise on the screen
            lead = f"{nm}: " if (ln.get('twoway') or ring) else ''
            if seq[0] in TERM_NODES:
                why = 'ימינה, צפונה אל J46_16' if seq[0] == E_W else ('דרומה בשדרת המזרח — מהשער המערבי אין יציאה דרומה' if 'J46_34' in seq[:8] and ln['id'] != '5' else 'דרך האי, כמו קודם')
                cells_o.append(f"{lead}<b>{gate_of(seq[0])}</b> — {why}")
            if seq[-1] in TERM_NODES:
                tail = seq[-4:]
                if seq[-1] == E_W: why = 'מ-J46_25 צפונה, ימינה פנימה'
                elif [x for x in seq[-8:] if x in ('J46_16', J_W, 'J46_25')][:3] == ['J46_16', J_W, 'J46_25']: why = 'מצפון בשדרת המזרח — לשער המערבי זו הייתה פנייה שמאלה'
                else: why = 'מדרך האי, כמו קודם'
                cells_b.append(f"{lead}<b>{gate_of(seq[-1])}</b> — {why}")
        lk = f"{ln['len_km']} / {ln['len_back_km']}" if ln.get('len_back_km') is not None else f"{ln['len_km']}"
        rows.append(f"<tr><td><span class='tag' style='background:{ln['color']}'>{E(ln['id'])}</span></td><td>{E(ln['name'])}</td><td class='small'>{'<br>'.join(cells_o)}</td><td class='small'>{'<br>'.join(cells_b)}</td><td class='small'>{lk} ק\"מ</td></tr>")
    return ''.join(rows)

def page_r9k(rec9j, sec9j):
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = TITLE; P_['batch'] = '9כ'
    T = P_['bus']['terminal']; T['gates'] = gates_rec(); T['flow'] = FLOW
    P_['logi_points'] = [dict(zone=z, what=w, rect=r, state=s) for z, w, r, s in R9J.POINTS]   # round 9י's points — the build does not keep them
    P_['r9j'] = rec9j
    SB = {frozenset((x['a'], x['b'])): x for x in P_['segments']}
    for ln in P_['routes']['bus']:
        if ln.get('back'): ln['len_back_km'] = round(sum(SB[frozenset((a, b))]['len_m'] for a, b in zip(ln['back'], ln['back'][1:])) / 1000, 2)
    ck = [c for c in P_['checks'] if c['name'].startswith('סבב 9כ')]
    P_['r9k'] = dict(at='4.11.2026', by='הבעלים 18:40 (D‑469: 10:30 / 10:31)',
                     why='סבב 9כ: השער המערבי של המסוף — כביש דו-סטרי אמיתי ברשת (J46_185 ימינה בלבד, LC-E3W 1+1, E49_185), דרומית למעבר של J46_16; הקווים עוברים בו — כל קו לפי מה שמסתדר לו',
                     junction=J_W, end=E_W, road=R_W, y=Y_W, gate_out=DONE9K.get('gates'), on_gate=DONE9K.get('on_gate'), crosswalks=DONE9K.get('xw'), st01=DONE9K.get('st01'),
                     gap_m=DONE9K.get('gap'), gap_walk_m=DONE9K.get('gap_walk'), asphalt_x=DONE9K.get('asphalt_x'), removed=['DW-E3-BUS-NW'], before=dict(gate_9j=R9J.GATES['nw']),
                     seg_ids=dict(new='AR-E/1a — J46_16–J46_185', kept='AR-E/1 — עכשיו J46_185–J46_25; AR-E/2 ו-AR-E/3 לא זזים'),
                     rules=['ימינה בלבד על עורק עם חציון רציף — צומת רק לצד שלו: הכניסות והמפרצים שבצד השני של החציון לא נמדדים ממנו',
                            'R-15: ‏J46_16–J46_185 ‏26 מ׳ — חריגה עם סיבה (' + R15_EXC[('AR-E', 'J46_16', J_W)] + ')'],
                     hover_back=DONE9K.get('hover_back'), checks=[dict(name=c['name'], ok=c['ok']) for c in ck])
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    P_['_N'] = {n['id']: n for n in P_['nodes']}
    ph = os.path.join(HERE, 'city_plan.html'); H0 = open(ph, encoding='utf-8').read()
    nck = len(P_['checks']); nok = sum(1 for c in P_['checks'] if c['ok'])
    st1 = DONE9K.get('st01') or []
    st1t = '; '.join(f"{'דרומה' if b['dir'].startswith(J_W) else 'צפונה'} — y {b['y'][0]:.0f}–{b['y'][1]:.0f}" for b in st1)
    S9 = ("<h2>סבב 9כ — מה השתנה (4.11.2026)</h2><p class='small'>הבעלים (18:40, על 9י): &quot;בתוכנית לא השתנו הקווים שיוצאים ונכנסים ממערב, וגם זה לא מסומן ככביש דו-סטרי&quot;, "
          "ו&quot;קצת לזוז דרומה — לא על המעבר חצייה&quot; (D‑469: 2 כניסות ו-2 יציאות, כל קו לפי מה שמסתדר לו). "
          f"<b>השער המערבי של המסוף</b> הוא עכשיו כביש אמיתי ברשת: <b>LC-E3W</b>, מקומי 1+1 עם קו אמצע, מהצומת החדש <b>{J_W}</b> על שדרת המזרח "
          f"(ימינה בלבד) עד <b>{E_W}</b> על האספלט של החצר, מעבר לפינה המעוגלת. הוא זז 5.5 מ׳ דרומה (מ-y 1805 ל-y {Y_W}): הכביש שלו מתחיל "
          f"{DONE9K.get('gap')} מ׳ דרומית למעבר של הזרוע הדרומית של J46_16. נכנסים בנתיב הדרומי (ממערב למזרח) — ימינה פנימה מהנתיבים צפונה; "
          "יוצאים בנתיב הצפוני — ימינה החוצה, צפונה אל J46_16. החציון של שדרת המזרח ממשיך — אין פנייה שמאלה. "
          "הכניסה DW-E3-BUS-NW של 9י יצאה.</p>" + terminal_svg(P_) +
          "<p class='small'>החץ האדום — כניסה, הכחול — יציאה; המקווקו — הדרך בתוך החצר. הפסים הלבנים — מעברי חצייה; הפסים הצהובים — קופסה צהובה בנתיב הימני צפונה מול השער. "
          "המלבנים המקווקווים בצפון — מקומות ההמתנה.</p>"
          "<h3>כל קו — באיזה שער הוא יוצא ובאיזה הוא חוזר</h3><div class='wrap'><table><tr><th>קו</th><th>שם</th><th>יוצא בשער</th><th>חוזר בשער</th><th>האורך (כל כיוון)</th></tr>" + _run_rows(P_) + "</table></div>"
          "<p class='small'>קו שנוסע בכל כיוון בדרך אחרת רשום עכשיו עם שני מסלולים — הלוך וחזור (או שני הכיוונים של הטבעת); שכבת &quot;קווי אוטובוס&quot; במפה מציירת את שניהם, "
          "ולכן הקווים 1, 2, 3, 4 ו-6 עוברים עכשיו בשער המערבי.</p>"
          "<h3>מה עוד זז, ולמה</h3><ul class='small'>"
          f"<li><b>בתוך המסוף:</b> {E(FLOW)}</li>"
          f"<li><b>מעברי חצייה ב-{J_W}:</b> לפי כלל צומת ה-T — מעבר על השער, ומעבר על שדרת המזרח בזרוע הדרומית (משמאל לנהג שיוצא מהשער); בזרוע הצפונית אין — "
          "לפי אותו כלל — ושם, צמוד לשער, עובר המעבר של J46_16.</li>"
          f"<li><b>R-15 (60 מ׳ בין צמתים):</b> {J_W} נמצא 26 מ׳ מ-J46_16 — חריגה עם סיבה: {E(R15_EXC[('AR-E', 'J46_16', J_W)])}.</li>"
          "<li><b>ימינה בלבד עם חציון רציף:</b> הצומת קיים רק בצד המזרחי של שדרת המזרח. לכן הכניסות של תחנת הדלק (בצד המערבי) והמפרץ דרומה של ST-01 לא נמדדים ממנו — בצד שלהם אין פנייה. "
          f"ST-01: {E(st1t)} — המפרץ דרומה במקום שלו, והמפרץ צפונה זז דרומה, 20 מ׳ מהשער, לפי הכלל (D‑332).</li>"
          "<li><b>המספור של הקטעים:</b> הצומת החדש מפצל את AR-E/1. AR-E/1 נשאר הקטע הארוך (J46_185–J46_25: ‏ST-01, הכניסות של D3 והחיבור הזמני TMP-S4-3), "
          "הקטע הקצר J46_16–J46_185 נקרא AR-E/1a, ו-AR-E/2 ו-AR-E/3 לא זזו — כמו שהסבבים הקודמים והמעברים שבמשחק מפנים אליהם.</li>"
          f"<li><b>הבדיקות:</b> {nok} מתוך {nck} עוברות, ובהן שתי בדיקות חדשות — השער המערבי, ובצומת ימינה בלבד אין פנייה שמאלה.</li></ul>")
    k = H0.index('<h2>סבב 9ט'); H0 = H0[:k] + S9 + sec9j + H0[k:]
    for old in ('תוכנית הדרכים של כל העיר — סבב 9ט', 'תוכנית הדרכים של כל העיר — סבב 9י'):
        H0 = H0.replace(old, TITLE)
    open(ph, 'w', encoding='utf-8').write(H0)
    print('r9k', dict(gap=DONE9K.get('gap'), st01=DONE9K.get('st01'), gates={k: (v['lines_out'], v['lines_in']) for k, v in T['gates'].items()}, checks=f'{nok}/{nck}'))
    assert H0.count('<h2>סבב 9כ') == 1 and H0.count('<h2>סבב 9י') == 1 and H0.count('<h2>סבב 9ט') == 1 and H0.count('<h2>סבב 9ח') == 1

if __name__ == '__main__':
    os.chdir(HERE)
    rec9h, prev9i, sec9h = R9I.keep_9h()
    rec9j, sec9j = keep_9j()
    # the main of round 9ז, as it is (it runs 9ו … 9 and their pages), in 9ז's own globals — with this round's network, routes and patches
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    R9I.page_r9i(rec9h, sec9h)
    page_r9k(rec9j, sec9j)
