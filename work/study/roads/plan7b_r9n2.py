# -*- coding: utf-8 -*-
"""5.11 · סבב 9נ — התצוגה של הדף בלבד (הבעלים 02:21: "אין בתוכנית הדרכים עדכון מה נעשה מלפני כמה ימים — העדכון האחרון שם סבב 7 מ-2.11").
 · מריץ את סבב 9נ כמו שהוא (plan7b_r9n — אותם נתונים ואותן בדיקות), ואחר כך משנה רק את הדף:
   1. שורת הכותרת: "סבב 9נ · <התאריך> · עודכן <השעה>" — בלי "7ב" ובלי התאריך הישן.
   2. מיד אחרי הכותרת: "מה נעשה מאז 2.11 — כל הסבבים" — טבלה מ-9נ עד 8, החדש למעלה; השעה של כל סבב — מהדף שנמסר (W/deliver), וקישור לסעיף שלו.
   3. הסעיפים של הסבבים מהחדש לישן (9נ … 8), ורק אחריהם סבב 7 — בלי לשנות בהם מילה; לפני כל סעיף עוגן.
    python3 plan7b_r9n2.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete/roads_before_r9n2)"""
import os, re, sys, time, json, textwrap, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
E = html.escape
import plan7b_r9n as R9N        # round 9נ — its patches and wrappers run on import; its __main__ runs below, as it is
DELIVER = '/home/claude/tc/pkg/work/deliver'
# (the round, its heading in the page, the anchor, the delivered page, one line of what changed)
ROUNDS = [('9נ', '<h2>סבב 9נ', 'r9n', '2026-11-05/Turbo_City_Road_Plan_R9n.html', 'J31_16 (שדרת השדה × רחוב הווילות) — רמזור לפי דרישה; היציאה מרחוב הווילות ימינה בלבד.'),
          ('9מ', '<h2>סבב 9מ', 'r9m', '2026-11-04/Turbo_City_Road_Plan_R9m.html', 'C2 לפי הציור שאושר — מגרש אחד: הקניון, הסופר "שיבולת", חניון משותף של 96 חניות ושישה פתחים.'),
          ('9ל', '<h2>סבב 9ל', 'r9l', '2026-11-04/Turbo_City_Road_Plan_R9l.html', 'המעבר בלי רמזור על שדרת המזרח ב-J46_185 יצא; הכניסה DW-D4-01 יצאה — במשחק אין שם פתח.'),
          ('9כ', '<h2>סבב 9כ', 'r9k', '2026-11-04/Turbo_City_Road_Plan_R9k.html', 'השער המערבי של מסוף האוטובוסים — כביש 1+1 אמיתי ברשת, מחוץ למעבר החצייה; הקווים עוברים בו.'),
          ('9י', '<h2>סבב 9י', 'r9j', '2026-11-04/Turbo_City_Road_Plan_R9j.html', 'המסוף של E3 עם שתי כניסות ושתי יציאות; היציאה של סוכנות הרכב; הכניסה ל-B1-P; הנקודות הלוגיסטיות.'),
          ('9ט', '<h2>סבב 9ט', 'r9i', '2026-11-04/Turbo_City_Road_Plan_R9i.html', 'ההורדה של המלון ב-A5 חוזרת דרומה, עם הצד של רחוב הדאונטאון.'),
          ('9ח', '<h2>סבב 9ח', 'r9h', '2026-11-04/Turbo_City_Road_Plan_R9h.html', 'ההורדה של המלון ב-A5 הפוכה, צפונה (בוטל בסבב 9ט).'),
          ('9ז', '<h2>סבב 9ז', 'r9g', '2026-11-04/Turbo_City_Road_Plan_R9g.html', 'הפתחים החדשים שבמשחק — היציאה של שוק העיר ב-B4 וכניסת המלון ב-A5.'),
          ('9ו', '<h2>סבב 9ו', 'r9f', '2026-11-03/Turbo_City_Road_Plan_R9f.html', 'J46_42 — המעבר בזרוע הצפונית נשאר (D‑420 היה שגוי).'),
          ('9ה', '<h2>סבב 9ה', 'r9e', '2026-11-03/Turbo_City_Road_Plan_R9e.html', 'צבעי הקווים במפה — כמו במשחק.'),
          ('9ד', '<h2>סבב 9ד', 'r9d', '2026-11-03/Turbo_City_Road_Plan_R9d.html', 'נוסח בלבד: כלל R-15 אחד, והמסוף E3 — 6 מפרצי עלייה ו-10 מקומות המתנה.'),
          ('9ג', '<h2>סבב 9ג', 'r9c', '2026-11-03/Turbo_City_Road_Plan_R9c.html', 'רחוב התעשייה בצפון החניון מצויר 2+1, והמפרצים של ST-12 על השפות.'),
          ('9ב', '<h2>סבב 9ב', 'r9b', '2026-11-03/Turbo_City_Road_Plan_R9b.html', 'C5 — שלושה רציפים: כניסה ימינה, ויציאה שמאלה ברמזור.'),
          ('9', '<h2>סבב 9 — ', 'r9', '2026-11-03/Turbo_City_Road_Plan_R9.html', 'C5, ‏D5 ו-E3; רמזור בכל צומת; כלל צומת ה-T.'),
          ('8ב', '<h2>סבב 8ב', 'r8b', '2026-11-03/Turbo_City_Road_Plan_R8b.html', 'מעברי החצייה — רק בצומת, צמודים לקו העצירה (R-76).'),
          ('8', '<h2>סבב 8 — ', 'r8', '2026-11-03/Turbo_City_Road_Plan_R8.html', 'R-69, השדה הסולרי של E4, האוטובוסים והשמות.')]
H7 = '<h2>סבב 7 — מה נוסף למפה'
HEAD_OLD = re.compile(r"<div class='mut'>7ב · [^<·]*· [^<·]*· <span class='small'>")
R9N2_LINE = 'השלבים עד S16 במפה — הים ב-S14, השדה ב-S15 ו-S16 (D‑463, D‑464); ותצוגת הדף: הכותרת, הטבלה הזו וסדר הסעיפים.'

# ---------------------------------------------------------------- 4 · the stages up to S16 (הבעלים 02:23: "גם חסרים שם S14, ‏15, ‏16")
NEW = '/home/claude/tc/pkg/work/plan600/data/new.json'            # the master plan: the stage of each of the 80 zones (zoneSync)
SCH = '/home/claude/tc/pkg/work/plan600/data/schedule_s7_s16.json'  # the schedule S7 … S16
STG = [f'S{i}' for i in range(1, 17)]
# one colour per stage — neighbours on the map differ; the new ones strong: the sea blue, the airside orange, the landside purple
COL = dict(zip(STG, ['#f1ce63', '#fabfd2', '#59a14f', '#ffbe7d', '#bab0ac', '#79706e', '#ff9d9a', '#d7b5a6',
                     '#9d7660', '#86bcb6', '#b6992d', '#8cd17d', '#d37295', '#4e79a7', '#f28e2b', '#b07aa1']))
WHAT = {'S14': 'הים — האוניות, הסירות והדיג (D‑463); E7 ו-E8 נשארים ב-S13 בגלל הגשר',
        'S15': 'השדה, הצד האווירי (D‑464; בתוכנית הישנה — שלב 8)',
        'S16': 'השדה, צד היבשה, ובסוף — השחקן בשדה (D‑464; בתוכנית הישנה — שלבים 9 ו-10)'}

def plan_stages(P, SV):
    """the stage of every zone by the master plan; S1 … S13 must be the map's own, as they are"""
    Z = json.load(open(NEW, encoding='utf-8'))['zoneSync']['zones']; PS = {z: v['stage'] for z, v in Z.items()}
    sch = [r['id'] for r in json.load(open(SCH, encoding='utf-8'))['rows']]
    assert set(PS) == set(SV.ZN) and {'S14', 'S15', 'S16'} <= set(sch)
    ORD = {z: t['stage'] for t in P['transition']['stages'] for z in t['zones']}
    assert all(PS[z] == s for z, s in ORD.items()), [(z, s, PS[z]) for z, s in ORD.items() if PS[z] != s]
    new = {z: s for z, s in PS.items() if z not in ORD and s != '—'}
    assert set(new.values()) == {'S14', 'S15', 'S16', 'S15–S16'} and len(new) == 27, new
    return PS, new

def lot_stage(l, PS):
    s = PS[l['zone']]
    if s == 'S15–S16': s = 'S15' if l['airside'] else 'S16'   # F2: the terminal S15, the front S16 (D‑464)
    assert s in ('S15', 'S16'), l['id']; return s

def stg_group(PS, SV):
    o = [f"<pattern id='stp16' width='70' height='70' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='35' height='70' fill='{COL['S16']}' fill-opacity='.85'/></pattern>",
         "<g id='stg' style='pointer-events:none'>"]
    for z in SV.ZN:
        s = PS[z]
        if s == '—': continue
        x0, y0, x1, y1 = SV.zrect(z); first = s.split('–')[0]
        o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='{COL[first]}' fill-opacity='.55' stroke='#3b3f47' stroke-width='6'/>")
        if '–' in s: o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='url(#stp16)' fill-opacity='.6'/>")
    return ''.join(o) + '</g>'
def stg_labels(PS, SV):
    """the stage of each zone, in its north-west corner — the same size on the screen at every zoom, like the other names"""
    o = []
    for z in SV.ZN:
        if PS[z] == '—': continue
        x0, y0, x1, y1 = SV.zrect(z)
        o.append(f"<g class='lb' data-k='99' transform='translate({x0 + 40} {y0 + 40})'><g class='s'><text class='stl' y='11' style='direction:ltr'>{E(PS[z])}</text></g></g>")
    return ''.join(o)

def chips():
    return (''.join(f"<span class='stc'><i style='background:{COL[s]}'></i>{s}</span>" for s in STG)
            + f"<span class='stc'><i style='background:{COL['S15']};background-image:repeating-linear-gradient(45deg,{COL['S16']} 0 4px,transparent 4px 8px)'></i>S15–S16</span>"
            + "<span class='stc' style='font:400 12px system-ui,sans-serif'><i style='background:none;border:1px solid #999'></i>בלי שלב</span>")

def stages_view(H, P, nok, nck):
    import plan7b_svg as SV
    PS, new = plan_stages(P, SV); air = {l['id']: l for l in P['air']['lots']}
    def one(old, new_, n=1):
        nonlocal H; assert H.count(old) == n, (old, H.count(old)); H = H.replace(old, new_)
    # a · the hover data of the city map: the zones, the airport lots and roads, the engine run-up
    a = H.index('<script>window.__MAP=') + len('<script>window.__MAP='); b = H.index(';</script>', a); s0 = H[a:b]
    D = json.loads(s0.replace('<\\/', '</')); assert json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') == s0
    info = D['info']; nz = 0
    for x0, y0, x1, y1, k in D['zones']:
        z = next(z for z in SV.ZN if tuple(SV.zrect(z)) == (x0, y0, x1, y1))
        if z not in new: continue
        pu = P['zones'].get(z, {}).get('purpose', '')
        old = f"<b>{E(z)} — {E(SV.ZN[z][0])}</b><div class='tl'>{E(pu)}</div>"; assert info[k] == old, (z, info[k])
        st = 'שלב S15–S16 (הטרמינל — S15, החזית — S16)' if new[z] == 'S15–S16' else 'שלב ' + new[z]
        info[k] = f"<b>{E(z)} — {E(SV.ZN[z][0])}</b><div class='tl'>{E(pu) + ' · ' if pu else ''}{E(st)}</div>"; nz += 1
    n15 = n16 = nr = nu = 0
    for k, t in enumerate(info):
        m = re.search(r"(AIR-[A-Z0-9-]+) · ([A-H][0-9]) · עתידי — שלב 8 · ", t)
        if m:
            l = air[m.group(1)]; assert l['zone'] == m.group(2); s = lot_stage(l, PS)
            info[k] = t.replace(' · עתידי — שלב 8 · ', f' · עתידי — שלב {s} · ', 1); n15 += s == 'S15'; n16 += s == 'S16'; continue
        if 'השדה העתידי (שלב 8) · ' in t: info[k] = t.replace('השדה העתידי (שלב 8) · ', 'השדה העתידי, צד היבשה (שלב S16) · ', 1); nr += 1; continue
        if 'תוכנית האב (H3): מקום חדש בשלב 8 ' in t: info[k] = t.replace('מקום חדש בשלב 8 ', 'מקום חדש בשלב S15 ', 1); nu += 1
    left = [t for t in info if re.search(r'שלב 8\b', t)]
    assert nz == 27 and n15 + n16 == len(air) and nr == len(P['air']['roads']) and nu == 1 and not left, (nz, n15, n16, nr, nu, left)
    H = H[:a] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + H[b:]
    # b · the texts of the page (not the sections of the rounds, which stay word for word)
    one("<b>העתיד:</b> השדה של שלב 8 (חלק ו, D‑262)", "<b>העתיד:</b> השדה של S15–S16 (חלק ו, D‑262; D‑464)")
    one("השדה העתידי — שלב 8 (חלק ו, D‑262)", "השדה העתידי — S15–S16 (חלק ו, D‑262)", 4)
    # c · the zone cards
    one("השדה — צד היבשה מערב · שלב —</span>", "השדה — צד היבשה מערב · שלב S16</span>")
    one("השדה — החזית · שלב —</span>", "השדה — החזית · שלב S15–S16</span>")
    # d · the transition table: S14, S15, S16 (no network segments of their own; the airport roads are in the airport layer)
    i = H.index("<tr><td class='id'>S13</td>"); j = H.index('</tr>', i) + 5; assert H[j:j + 9] == '\n</table>'
    byst = {s: [z for z in SV.ZN if PS[z] == s] for s in ('S14', 'S15', 'S16')}
    zs = {'S14': ', '.join(byst['S14']), 'S15': ', '.join(byst['S15']) + ', והטרמינל ב-F2', 'S16': ', '.join(byst['S16']) + ', והחזית של F2'}
    H = H[:j] + ''.join(f"<tr><td class='id'>{s}</td><td class='id'>{E(zs[s])}</td><td>{E(WHAT[s])}</td><td>0</td><td>0</td><td class='tmp'>—</td><td>—</td></tr>" for s in ('S14', 'S15', 'S16')) + H[j:]
    # e · the layer "שלבים" in the city map (off at first), its colour in the legend
    one("<g id='terrain'>", stg_group(PS, SV) + "<g id='terrain'>")
    i = H.index("class='m city'"); j = H.index("<use class='L-bus' href='#bus'/>", i) + len("<use class='L-bus' href='#bus'/>"); assert j < H.index('</svg>', i)
    H = H[:j] + "<g class='L-stages' style='pointer-events:none'><use href='#stg'/>" + stg_labels(PS, SV) + "</g>" + H[j:]   # the city map only
    one("<span class='sw sw-names'></span>שמות</button>", "<span class='sw sw-names'></span>שמות</button><button type='button' class='lt' data-l='stages' aria-pressed='false'><span class='sw sw-stages'></span>שלבים</button>")
    one(".off-names .L-names{display:none}", ".off-names .L-names,.off-stages .L-stages{display:none}"
        f"\n.sw-stages{{background:linear-gradient(90deg,{COL['S1']},{COL['S8']},{COL['S16']})}}.stc{{display:inline-flex;align-items:center;gap:4px;margin-inline-end:10px;font:600 12px ui-monospace,Menlo,Consolas,monospace;white-space:nowrap}}"
        ".stc i{width:16px;height:11px;border-radius:2px;display:inline-block;opacity:.8}"
        ".stl{font:700 12px ui-monospace,Menlo,Consolas,monospace;fill:#1d2733;text-anchor:start;paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round}")
    one("</style></head><body>", "</style></head><body class='off-stages'>")
    one("<span><b>אזור</b> — גבול, מזהה ושם</span></div>", "<span><b>אזור</b> — גבול, מזהה ושם</span></div>"
        "<div class='lgi' style='grid-column:1/-1'><span><b>שלבים</b> (הכפתור \"שלבים\" מעל המפה): " + chips() + "</span></div>")
    # f · the section of 9נ2, before 9נ
    rows = ''.join(f"<tr><td class='id'>{s}</td><td class='id'>{E(zs[s])}</td><td>{E(WHAT[s])}</td><td class='small'>{'בלי שלב' if s == 'S14' else 'בלי שלב; המגרשים והדרכים של השדה — \"שלב 8\"'}</td></tr>" for s in ('S14', 'S15', 'S16'))
    rows += f"<tr><td class='id'>—</td><td class='id'>{E(', '.join(z for z in SV.ZN if PS[z] == '—'))}</td><td>ים פתוח — גם בתוכנית בלי שלב</td><td class='small'>בלי שלב</td></tr>"
    sec = (f"<a id='r9n2'></a><h2>סבב 9נ2 — השלבים עד S16 במפה, ותצוגת הדף</h2>"
           "<div class='box'><b>מה ביקשו:</b> הבעלים 02:21 — \"אין בתוכנית הדרכים עדכון של מה שנעשה מלפני כמה ימים\"; 02:23 — \"גם חסרים שם S14, ‏15, ‏16\". "
           f"<b>הדרכים לא השתנו</b> — אותם כבישים, צמתים ובדיקות ({nok} מתוך {nck}); השתנה רק מה שהדף מציג.</div>"
           "<h3>1 · הדף</h3><ul><li>שורת הכותרת — הסבב האחרון, התאריך ושעת העדכון.</li><li>מיד אחריה — \"מה נעשה מאז 2.11\": כל הסבבים, החדש למעלה, עם קישור לסעיף של כל סבב.</li>"
           "<li>הסעיפים — מהחדש לישן, ואחריהם סבב 7; בלי לשנות בהם מילה.</li></ul>"
           "<h3>2 · השלבים — עד S16</h3><p>המקור: טבלת הזמנים של תוכנית האב (S7 עד S16) והשלב של כל אזור בתוכנית האב; D‑463 (הים) ו-D‑464 (השדה). "
           "S1 עד S13 במפה — כמו בתוכנית, בלי שינוי. 27 אזורים שהיו במפה בלי שלב קיבלו את השלב שלהם:</p>"
           "<div class='zc'><svg class='m' viewBox='-200 -950 9900 8800' role='img' aria-label='השלבים של כל האזורים'><use href='#terrain'/><use href='#stg'/>" + stg_labels(PS, SV) + "</svg>"
           f"<div class='small' style='margin-top:6px'>{chips()}</div></div>"
           "<div class='wrap'><table><tr><th>השלב</th><th>האזורים</th><th>מה</th><th>במפה לפני</th></tr>" + rows + "</table></div>"
           "<h3>מה שונה בדף</h3><ul>"
           f"<li>השלב של {nz} האזורים — בריחוף מעל האזור במפת העתיד, בכרטיסים של E2 ו-F2, ובטבלת המעבר (שורות S14, S15 ו-S16, בלי קטעים חדשים של הרשת).</li>"
           f"<li>\"שלב 8\" של השדה הוחלף לפי טבלת הזמנים: {n15} מגרשים בשדה ← S15, {n16} ← S16 (לפי האזור; ב-F2 — הצד האווירי S15 וצד היבשה S16); "
           f"{nr} הדרכים של צד היבשה ← S16; הרצת המנועים ב-H3 ← S15; השם של השדה במפה ובשורת העתיד ← S15–S16.</li>"
           "<li>שכבה חדשה במפת העתיד: \"שלבים\" — כבויה בהתחלה, לחיצה מדליקה; צבע לכל שלב, גם במקרא.</li>"
           "<li><b>לא שונה:</b> סבב 7 ושם הבדיקה שלו (\"סבב 7 — השדה (שלב 8)\") — כך נכתבו אז; המסילות והאי עם המספרים הישנים (שלבים 12, 14, 17 ו-18) — "
           "לטבלת הזמנים אין להם עדיין שלב S משלהם, ולכן הם נשארו; זו שאלה פתוחה.</li></ul>")
    one("<a id='r9n'></a><h2>סבב 9נ", sec + "<a id='r9n'></a><h2>סבב 9נ")
    return H, dict(zones=nz, s15=n15, s16=n16, roads=nr)

def when(rel):
    p = os.path.join(DELIVER, rel)
    if rel.startswith('2026-11-05/Turbo_City_Road_Plan_R9n.html') and not os.path.exists(p): return time.localtime()
    return time.localtime(os.path.getmtime(p))
def fmt(t): return f"{t.tm_mday}.{t.tm_mon} {t.tm_hour:02d}:{t.tm_min:02d}"

def page_view(nok, nck):
    ph = os.path.join(HERE, 'city_plan.html'); H = open(ph, encoding='utf-8').read()
    H = re.sub(r"<a id='r[0-9][a-z]?'></a>", '', H)                                   # a second run: the anchors again, once
    now = time.localtime()
    # 1 · the header line
    assert len(HEAD_OLD.findall(H)) == 1
    H = HEAD_OLD.sub(f"<div class='mut'>סבב 9נ · {now.tm_mday}.{now.tm_mon}.{now.tm_year} · עודכן {now.tm_hour:02d}:{now.tm_min:02d} · <span class='small'>", H, count=1)
    # 3 · the rounds newest first, then round 7 (each section as it is, word for word)
    pos = [H.index(h) for _, h, _, _, _ in ROUNDS]; assert all(H.count(h) == 1 for _, h, _, _, _ in ROUNDS)
    assert pos == sorted(pos), 'the rounds are not newest first'
    a = H.index(H7); b = H.index('<h2>', a + 4); sec7 = H[a:b]
    H = H[:a] + H[b:]
    k = H.index('<h2>הבדיקות</h2>'); assert k > H.index(ROUNDS[-1][1])
    H = H[:k] + sec7 + H[k:]
    for _, h, anc, _, _ in ROUNDS:
        H = H.replace(h, f"<a id='{anc}'></a>" + h, 1)
    # 2 · right after the header: everything since 2.11
    rows = f"<tr><td><a href='#r9n2'>סבב 9נ2</a></td><td class='small'>{fmt(now)}</td><td class='small'>{E(R9N2_LINE)}</td></tr>"
    rows += ''.join(f"<tr><td><a href='#{anc}'>סבב {E(r)}</a></td><td class='small'>{fmt(when(rel))}</td><td class='small'>{E(line)}</td></tr>" for r, h, anc, rel, line in ROUNDS)
    S = ("<h2>מה נעשה מאז 2.11 — כל הסבבים</h2><p class='small'>החדש ביותר למעלה. השעה — מתי נמסר הדף של הסבב; לחיצה על הסבב מובילה לסעיף שלו בדף. "
         f"הסעיפים המלאים — למטה, מהחדש לישן, ורק אחריהם סבב 7. הבדיקות: {nok} מתוך {nck} עוברות.</p>"
         "<div class='wrap'><table><tr><th>הסבב</th><th>מתי</th><th>מה השתנה</th></tr>" + rows + "</table></div>")
    m = re.search(r"<div class='mut'>סבב 9נ · [^\n]*?</div>", H); assert m
    H = H[:m.end()] + '\n' + S + H[m.end():]
    # 4 · the stages up to S16, and the section of 9נ2
    H, got = stages_view(H, json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8')), nok, nck)
    open(ph, 'w', encoding='utf-8').write(H)
    order = [m.group(1) for m in re.finditer(r'<h2>(סבב [0-9][^ <]*)', H)]
    print('r9n2', dict(order=order, header=re.search(r"<div class='mut'>(סבב 9נ[^<]*)", H).group(1), stages=got))
    assert order[0] == 'סבב 9נ2' and order[1:17] == ['סבב ' + r for r, *_ in ROUNDS] and order[17] == 'סבב 7' and H.count("<h2>מה נעשה מאז 2.11") == 1
    assert H.index("<h2>מה נעשה מאז 2.11") < H.index("מה חדש בסבב 7") < H.index('<h2>מפת העתיד')

if __name__ == '__main__':
    os.chdir(HERE)
    ph = os.path.join(HERE, 'city_plan.html')
    if "<h2>מה נעשה מאז 2.11" in open(ph, encoding='utf-8').read():   # a second run: back to the page of 9נ as delivered (the same bytes), and 9נ again from it
        open(ph, 'w', encoding='utf-8').write(open(os.path.join(DELIVER, ROUNDS[0][3]), encoding='utf-8').read())
    src = open(os.path.join(HERE, 'plan7b_r9n.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9n.py:__main__', 'exec'), dict(vars(R9N)))   # round 9נ, as it is
    import json
    P = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8'))
    page_view(sum(1 for c in P['checks'] if c['ok']), len(P['checks']))
