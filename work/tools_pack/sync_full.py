# -*- coding: utf-8 -*-
"""8.11.2026 · sync_full — ההרחבה של בדיקת הסנכרון שעוצרת מסירה (R-83 סעיף ט 1–8, ‏R-87 סעיף ה 1–6).
נקרא מ-sync_check.py. כל בדיקה מחזירה {id, name, ok, fails:[{what, reason, fix}], note}. מה שלא נבדק — מסומן ok=None עם הסיבה.
המקורות: התוכנית (הנתונים שבתוך הדף, plan-data), מפת הדרכים (city_plan.json + __MAP שבתוך city_plan.html), המשחק (הנתונים שבתוך ה-HTML,
והשליפה בדפדפן — tools_pack/sync_game_dump.js, נשמרת לפי ה-sha1 של הבנייה ב-plan600/out/game_dump_<sha1>.json)."""
import os, re, json, math, subprocess, datetime as dt

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = 'ABCDEFGH'
GRID_ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
TOL = 45   # 4.5 מ׳ (10 פיקס׳ למטר)
ZRE = re.compile(r'(?<![A-Za-z0-9])([A-H][0-9])(?![0-9])')


def zone_at(x, y):
    c = int(x // 1200)
    if c < 0 or c > 7: return None
    for r in range(10):
        if GRID_ROWS[r] <= y < GRID_ROWS[r + 1]: return COLS[c] + str(r)
    return None


def F(what, reason, fix=''):
    return {'what': what, 'reason': reason, 'fix': fix}


def chk(cid, name, fails, note='', ok=None):
    return {'id': cid, 'name': name, 'ok': (not fails) if ok is None else ok, 'n': len(fails), 'fails': fails[:400], 'more': max(0, len(fails) - 400), 'note': note}


def grab(H, marker, start=0):
    i = H.index(marker, start) + len(marker)
    while H[i] in ' \t\n=': i += 1
    d = 0; j = i; q = None
    while True:
        c = H[j]
        if q:
            if c == '\\': j += 2; continue
            if c == q: q = None
        elif c in '"\'`': q = c
        elif c in '{[': d += 1
        elif c in '}]':
            d -= 1
            if d == 0: return H[i:j + 1]
        j += 1


# ---------------- the sources ----------------
def game_dump(build, sha):
    # 8.11 (v6.93): the second dump also reads the map stops of the game (S6_MAP_STOPS) and the crossings of the terminal (P560Y.xs)
    js2 = os.path.join(WORK, 'plan600', 'tools', 'sync_game_dump2.js')
    js, out = ((js2, os.path.join(WORK, 'plan600', 'out', 'game_dump2_%s.json' % sha)) if os.path.exists(js2)
               else (os.path.join(WORK, 'tools_pack', 'sync_game_dump.js'), os.path.join(WORK, 'plan600', 'out', 'game_dump_%s.json' % sha)))
    if not os.path.exists(out):
        try:
            subprocess.run(['node', js, build, out], timeout=900, check=True, capture_output=True)
        except Exception as e:
            return None, 'השליפה מהמשחק נכשלה: %s' % str(e)[:160]
    return json.load(open(out, encoding='utf-8')), ''


def game_static(build):
    H = open(build, encoding='utf-8').read()
    o = {}
    m = re.search(r'<title>([^<]*)', H); o['title'] = m.group(1).strip() if m else ''
    m = re.search(r"\bBUILD='([^']*)'", H); o['BUILD'] = m.group(1) if m else ''
    m = re.search(r"FILE_SCOPE='([^']*)'", H); o['FILE_SCOPE'] = m.group(1) if m else ''
    try:
        t = grab(H, 'const BUS_LINE_INFO=')
        o['lineInfo'] = {k: [a, b] for k, a, b in re.findall(r"(\d+):\['([^']*)','([^']*)'", t)}
    except Exception: o['lineInfo'] = {}
    return o


def map_page():
    p = os.path.join(WORK, 'study', 'roads', 'city_plan.html')
    H = open(p, encoding='utf-8').read()
    o = {'file': p}
    m = re.search(r'<title>([^<]*)', H); o['title'] = m.group(1).strip() if m else ''
    m = re.search(r'<h1[^>]*>([^<]*)', H); o['h1'] = m.group(1).strip() if m else ''
    rounds = re.findall(r"<td><a href='#r[^']*'>סבב ([^<]+)</a></td>", H)
    o['lastRound'] = rounds[0].strip() if rounds else ''
    try: o['map'] = json.loads(grab(H, '__MAP='))
    except Exception: o['map'] = None
    o['linesToday'] = {}
    k = H.find('<th>אוטובוסים היום</th>')
    if k > 0:
        tb = H[k:H.find('</table>', k)]
        for row in re.findall(r'<tr>(.*?)</tr>', tb, re.S):
            m = re.match(r"\s*<td><span class='tag'[^>]*>(\d)</span></td>", row)
            if not m: continue
            tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
            route = re.sub(r'<[^>]+>', ' ', tds[1].split('<div')[0]).strip() if len(tds) > 1 else ''
            o['linesToday'][m.group(1)] = {'route': route, 'buses': re.sub(r'<[^>]+>', '', tds[2]).strip() if len(tds) > 2 else ''}
    return o


# ---------------- the checks ----------------
def check_versions(P, PH, MJ, MP, GS, GD):
    """ט1 — הגרסה זהה בכותרת, בכותרת הראשית, בנתונים ובשורת הבנייה — בתוכנית, במפה ובמשחק"""
    fails = []
    v = P['meta'].get('title', '')
    vv = re.search(r'v\d+\.\d+', v); vv = vv.group(0) if vv else v
    t = re.search(r'<title>([^<]*)', PH); t = t.group(1) if t else ''
    side = re.search(r'<small>([^<]*)</small>', PH); side = side.group(1) if side else ''
    if vv not in t: fails.append(F('התוכנית — הכותרת', 'בכותרת "%s" אין את הגרסה %s' % (t, vv), 'build_v600.py'))
    if vv not in side: fails.append(F('התוכנית — הכותרת בצד', 'בכותרת "%s" אין את הגרסה %s' % (side, vv), 'build_v600.py'))
    if P['meta'].get('build') and P['meta']['build'] not in P['meta'].get('runLine', ''):
        fails.append(F('התוכנית — שורת הבנייה', 'הבנייה בראש (%s) לא בשורת הבנייה' % P['meta']['build'], 'plan_sync.py'))
    # the map: one version field for the title, the h1 and the table of the rounds (R-83 ז1)
    lr = MP.get('lastRound', '')
    for k, he in (('title', 'הכותרת של הדף'), ('h1', 'הכותרת הראשית')):
        if lr and ('סבב ' + lr) not in MP.get(k, ''):
            fails.append(F('מפת הדרכים — ' + he, '"%s" — אבל הסבב האחרון בטבלת הסבבים הוא %s' % (MP.get(k, ''), lr), 'סוכן המפה: שדה גרסה אחד לכותרת, לכותרת הראשית ולטבלה (R-83 ז1)'))
    if lr and MJ.get('batch') != lr:
        fails.append(F('מפת הדרכים — הנתונים', 'בנתונים batch=%s, ובטבלת הסבבים %s' % (MJ.get('batch'), lr), 'סוכן המפה'))
    # the game: the build in the title, the h1 and BUILD (R-83 ח1)
    b = (GD or {}).get('buildCode') or ''
    for k, he in (('title', 'הכותרת'), ('BUILD', 'שורת הבנייה (BUILD)')):
        val = (GD or {}).get(k) or GS.get(k, '')   # 8.11 (v6.93): the title and BUILD of the page while it runs (TC_REL writes them)
        if b and b.lower() not in val.lower():
            fails.append(F('המשחק — ' + he, '"%s" — בלי %s' % (val, b), 'הבונה: כותרת, BUILD ו-FILE_SCOPE מקבוע גרסה אחד (R-83 ח1)'))
    h1 = ((GD or {}).get('h1') or [''])[0]
    if b and b.lower() not in h1.lower():
        fails.append(F('המשחק — הכותרת הראשית', '"%s" — עבודה ישנה בשדה, בלי %s' % (h1, b), 'הבונה (R-83 ח1)'))
    fs = (GD or {}).get('FILE_SCOPE') or GS.get('FILE_SCOPE', '')
    if re.search(r'S6R|STANDS', fs) or (b and fs and b.lower() not in fs.lower()):
        fails.append(F('המשחק — FILE_SCOPE', '"%s" — לא של הבנייה %s' % (fs, b), 'הבונה (R-83 ח1)'))
    return chk('ט1', 'הגרסה זהה בכותרת, בכותרת הראשית, בנתונים ובשורת הבנייה — בתוכנית, במפה ובמשחק', fails)


def check_zone_stages(P):
    """ט2 — לכל אזור שלב (או "—" עם סיבה), והשלב בטבלת האזורים = השלב בתיאור השלב"""
    fails = []
    inStage = {}
    for s in P['stages']:
        for z in s.get('zones', []) or []: inStage.setdefault(z, set()).add(s['id'])
    for z, o in P['zones'].items():
        stg = (o.get('stage') or '').strip()
        if not stg or stg == '—':
            if not o.get('noStageWhy'): fails.append(F(z, 'בלי שלב ובלי סיבה רשומה', 'בתוכנית: שלב או סיבה'))
            continue
        want = set(re.findall(r'S\d+a?', stg))
        have = inStage.get(z, set())
        if want - have:
            fails.append(F(z, 'בטבלת האזורים %s, ובתיאור השלבים האזור רשום רק ב-%s' % (stg, ', '.join(sorted(have)) or 'אף שלב'), 'בתוכנית: השדה zones של השלב'))
        extra = {x for x in have if x.startswith('S') and x not in want and not (x == 'S9a' and 'S9' in want)}
        if extra:
            fails.append(F(z, 'רשום גם בשלבים %s, ובטבלת האזורים %s' % (', '.join(sorted(extra)), stg), 'בתוכנית'))
    return chk('ט2', 'לכל אזור שלב, והשלב בטבלת האזורים זהה לשלב שבתיאור השלב', fails)


def check_stages(P):
    """ט3 — אין שני שלבים עם אותו מספר; סכום השעות = הסך הכול; כל אחוז בין 0 ל-100"""
    fails = []
    ids = [s['id'] for s in P['stages']]
    for i in sorted({x for x in ids if ids.count(x) > 1}): fails.append(F(i, 'שני שלבים עם אותו מספר'))
    nums = {}
    for i in ids:
        m = re.match(r'^[SW]?(\d+)', i)
    tot = sum(s['hours'] for s in P['stages']); done = sum(s['hours'] * (s.get('progress') or 0) / 100 for s in P['stages'])
    m = re.search(r'נעשו כ-(\d+) מתוך ([\d.]+) שע׳', P['meta'].get('statusText', ''))
    if not m: fails.append(F('שורת המצב', 'אין "נעשו כ-N מתוך T שע׳"'))
    else:
        if abs(float(m.group(2)) - tot) > 0.01: fails.append(F('הסך הכול', 'שורת המצב %s, וסכום השלבים %.2f' % (m.group(2), tot)))
        if abs(int(m.group(1)) - done) > 0.51: fails.append(F('נעשו', 'שורת המצב %s, ומהשלבים %.2f' % (m.group(1), done)))
    for s in P['stages']:
        pr = s.get('progress') or 0
        if pr < 0 or pr > 100: fails.append(F(s['id'], 'האחוז %s מחוץ ל-0–100' % pr))
    old = [i for i in ids if re.match(r'^\d', i)]
    if old: fails.append(F('המספור', 'שלבים במספור הישן: ' + ', '.join(old), 'D‑521: S1–S16 לשלבי המפה, W לשאר'))
    return chk('ט3', 'אין שני שלבים עם אותו מספר; סכום השעות שווה לסך הכול; כל אחוז בין 0 ל-100', fails, 'סך הכול %.2f שע׳, נעשו %.2f' % (tot, done))


def active_texts(P):
    """the text the owner reads in the current plan — without the history"""
    out = []
    out += [P['meta'].get('statusText', ''), P['meta'].get('runLine', '')]
    for d in P['decisions']: out += [' · '.join([d.get('topic', ''), d.get('text', ''), d.get('status', ''), d.get('now', '')])]
    for k in P['defects']: out += [k.get('topic', ''), k.get('text', ''), k.get('status', '')]
    for s in P['stages']:
        out += [s.get('name', ''), s.get('purpose', ''), s.get('builds', ''), s.get('behavior', '')] + list(s.get('done') or []) + list(s.get('remaining') or []) + list(s.get('acceptance') or [])
    for r in P.get('ownerPending') or []: out += [r.get('what', ''), r.get('dflt', '')]
    for b in P.get('bands2') or []:
        out.append(b.get('note', ''))
        for r in b.get('rows', []): out += [str(c) for c in r]
    if P.get('next15'): out += [r.get('step', '') for r in P['next15'].get('rows', [])]
    for iid, it in P['items'].items():
        if not it.get('h'): out += [it.get('t', ''), it.get('st', '')]
    return out


def check_refs(P):
    """ט4 — כל K, ‏D ו-R שמוזכרים קיימים כרשומה"""
    fails = []
    D = {d['id'] for d in P['decisions']}; K = {k['id'] for k in P['defects']}
    R = set()
    for a in [P.get('audit')] + [P.get('auditPrev')] + list(P.get('auditOlder') or []) + [P.get('auditReview')]:
        if a: R |= {f['id'] for f in a.get('findings', [])}
    alias = {}
    for b in P.get('bands2') or []:
        if b.get('id') == 'aliases':
            for r in b['rows']: alias[r[0]] = r[1]
    gaps = {g['id'] for g in (P.get('refGaps') or [])}
    seen = {}
    for t in active_texts(P):
        for m in re.finditer(r'(?<![A-Za-z0-9‑\-])([DKR])[‑\-](\d{1,3})(?![\d\w])', t):
            k, n = m.group(1), int(m.group(2))
            key = ('R-%02d' % n) if k == 'R' else '%s‑%d' % (k, n)
            seen[key] = seen.get(key, 0) + 1
    for key, cnt in sorted(seen.items()):
        if key in gaps: continue
        if key.startswith('D‑') and key not in D: fails.append(F(key, 'מוזכר %d פעמים, ואין רשומה בהחלטות' % cnt, 'רשומה, או "הוחלף ב-…"'))
        elif key.startswith('K‑') and key not in K: fails.append(F(key, 'מוזכר %d פעמים, ואין רשומה בפגמים' % cnt, 'רשומה סגורה עם הבנייה'))
        elif key.startswith('R-') and key not in R and key.replace('R-0', 'R-') not in R: fails.append(F(key, 'מוזכר %d פעמים, ואין רשומה בממצאי הביקורת' % cnt, 'מספר R רק מדף הביקורת (R-83 ה3)'))
    return chk('ט4', 'כל K, ‏D ו-R שמוזכרים בתוכנית קיימים כרשומה', fails, '%d מספרים שונים מוזכרים; %d פערים רשומים עם סיבה' % (len(seen), len(gaps)))


def check_pending(P):
    """ט5 — ברשימת "מחכה לך" אין נושא בסטטוס "הוחלט" או "יוצא מהרשימה" """
    fails = []
    DD = {d['id']: d for d in P['decisions']}
    for r in P.get('ownerPending') or []:
        d = DD.get(r.get('where'))
        txt = (r.get('what', '') + ' ' + r.get('dflt', ''))
        if 'יוצא מהרשימה' in txt: fails.append(F(r.get('where'), 'כתוב "יוצא מהרשימה"'))
        if re.match(r'^\s*(הוחלט|אושר|נבנה|נסגר)', r.get('dflt', '')): fails.append(F(r.get('where'), 'ברירת המחדל מתחילה ב"%s" — זה לא נושא פתוח' % r['dflt'][:20]))
        if d is not None and not r.get('sub') and re.match(r'^\s*(הוחלט|נסגר)', d.get('now', '')):
            fails.append(F(r.get('where'), 'המצב עכשיו "%s" — ונשאר ברשימה בלי שאלת משנה' % d['now'][:40]))
    return chk('ט5', 'ברשימת "מחכה לך" אין נושא שהוחלט או שיוצא מהרשימה', fails, '%d נושאים ברשימה' % len(P.get('ownerPending') or []))


def route_zones(GD, line):
    E = {e['id']: e for e in GD['edges']}; N = {n['id']: n for n in GD['nodes']}
    seq = []
    for st in GD['routes'].get(str(line), []):
        e = E.get(st['edgeId'])
        if not e: continue
        a, b = N.get(e['a']), N.get(e['b'])
        pts = ([[a['x'], a['y']]] if a else []) + list(e.get('pts') or []) + ([[b['x'], b['y']]] if b else [])
        if st.get('dirSign', 1) < 0: pts = pts[::-1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):   # every zone the edge passes, in order (samples every 10 px)
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) // 10))
            for i in range(n + 1):
                z = zone_at(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
                if z and (not seq or seq[-1] != z): seq.append(z)
    return seq


def check_lines(MP, GS, GD):
    """ט6 + ה5 — עמודת "היום" בטבלת הקווים במפה, ‏BUS_LINE_INFO — זהים למסלולים שבמשחק"""
    fails = []
    if not GD: return chk('ט6', 'עמודת "היום" של הקווים במפה ו-BUS_LINE_INFO — זהים למשחק', [], 'לא נבדק — אין שליפה מהמשחק', ok=None)
    for ln in [str(x) for x in GD.get('lines', [])]:
        g = route_zones(GD, ln); gs = set(g)
        mt = MP['linesToday'].get(ln, {}).get('route', '')
        ms = set(ZRE.findall(mt))
        if ms != gs:
            fails.append(F('קו %s — המפה' % ln, 'במפה "%s" (%s); במשחק %s' % (mt, ', '.join(sorted(ms)), ' → '.join(g)),
                           'סוכן המפה: העמודה נגזרת בסקריפט מהמשחק (R-83 ז3)'))
        nb = MP['linesToday'].get(ln, {}).get('buses', '').strip()
        if nb.isdigit() and int(nb) != int(GD.get('busVehicles', 0) or 0):
            fails.append(F('קו %s — אוטובוסים היום' % ln, 'במפה %s, ובמשחק %d אוטובוסים בשירות (כל הקווים)' % (nb, GD.get('busVehicles', 0)), 'סוכן המפה: נגזר מהמשחק'))
        li = GS.get('lineInfo', {}).get(ln)
        if li:
            ls = set(ZRE.findall(li[1]))
            if ls != gs:
                fails.append(F('קו %s — BUS_LINE_INFO' % ln, 'בטקסט של המשחק "%s"; המסלול במשחק %s' % (li[1], ' → '.join(g)), 'הבונה: הטקסט נגזר מהמסלול (R-86 ג6)'))
    mb = GD.get('mbus') or {}
    if mb:
        g1 = set(route_zones(GD, '1')); ms = set(ZRE.findall(mb.get('routeLabel', '')))
        if ms != g1:
            fails.append(F('M-BUS-01', 'המסלול "%s" — לא קו 1 של המשחק (%s)' % (mb.get('routeLabel'), ', '.join(sorted(g1))), 'הבונה: D‑524 — המשימה נוסעת במסלול של קו 1'))
    return chk('ט6', 'עמודת "היום" של הקווים במפה, ‏BUS_LINE_INFO והמשימה M-BUS-01 — זהים למסלולים שבמשחק', fails)


def check_schedule(P, now):
    """ט7 — כל תאריך בטבלת הצעדים הבאים מאוחר מעכשיו, ומחשב את העצירות ואת השבת"""
    fails = []
    rows = (P.get('next15') or {}).get('rows', [])
    y = now.year
    def parse(s):
        out = []
        for d, mo, h, mi in re.findall(r'(\d{1,2})\.(\d{1,2})\s+(\d{1,2}):(\d{2})', s):
            out.append(dt.datetime(y, int(mo), int(d), int(h), int(mi)))
        return out
    def shab(t): return (t.weekday() == 4 and (t.hour, t.minute) > (16, 30)) or (t.weekday() == 5 and (t.hour, t.minute) < (17, 30))
    for r in rows:
        for t in parse(r.get('when', '')):
            if t < now - dt.timedelta(minutes=30): fails.append(F('שורה %s' % r.get('n'), '%s — לפני עכשיו (%s)' % (t.strftime('%d.%m %H:%M'), now.strftime('%d.%m %H:%M')), 'לחשב מחדש (R-83 א)'))
            if shab(t): fails.append(F('שורה %s' % r.get('n'), '%s — בתוך השבת' % t.strftime('%d.%m %H:%M'), 'לחשב מחדש'))
    if any(r.get('when', '').startswith('נעשה') for r in rows): fails.append(F('טבלת הצעדים הבאים', 'יש בה שורות שכבר נעשו', 'R-83 ו3: רק עתיד'))
    m = re.search(r'(\d+)', (P.get('next15') or {}).get('title', ''))
    if not m or int(m.group(1)) != len(rows): fails.append(F('הכותרת', 'בכותרת "%s", ובטבלה %d שורות' % ((P.get('next15') or {}).get('title', ''), len(rows))))
    return chk('ט7', 'כל תאריך בטבלת הזמנים מאוחר מעכשיו, ומחושב עם העצירות והשבת', fails, '%d שורות' % len(rows))


def check_english(P):
    """ט8 — אין משפט באנגלית במה שהבעלים רואה (שלוש מילים באנגלית ברצף, שאינן קודים)"""
    fails = []
    W = r"(?<![\w‑\-/.])[A-Za-z][a-z]{2,}(?![\w‑\-/.])"
    rx = re.compile(W + r"(?:[ ,]+" + W + r"){2,}")
    n = 0
    for t in active_texts(P):
        for m in rx.finditer(t):
            n += 1
            if len(fails) < 60: fails.append(F(m.group(0)[:60], 'משפט באנגלית: "…%s…"' % t[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ')))
    res = chk('ט8', 'אין משפט באנגלית במה שהבעלים רואה (בתוכנית הנוכחית, בלי ההיסטוריה)', fails, '%d מקומות' % n)
    res['n'] = n
    return res


def built_zones():
    import sync_check as _SC
    Z = _SC.zone_builds()
    return {z for z, o in Z.items() if not o.get('part')}, Z


def near(p, L, tol=TOL):
    best = None; bd = 1e9
    for q in L:
        d = math.hypot(p[0] - q[0], p[1] - q[1])
        if d < bd: bd = d; best = q
    return (bd <= tol), bd, best


def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; L2 = (bx - ax) ** 2 + (by - ay) ** 2
    if L2 == 0: return math.hypot(p[0] - ax, p[1] - ay)
    t = max(0, min(1, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / L2))
    return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))


def check_map_game(MJ, MP, GD):
    """ה1 — כל קטע דרך, צומת (כולל סוג השליטה), מעבר חצייה ומפרץ תחנה — במפה ובמשחק, בשני הכיוונים, באזורים שנבנו; יותר מ-4.5 מ׳ — כישלון"""
    fails = []
    if not GD: return chk('ה1', 'המפה מול המשחק', [], 'לא נבדק — אין שליפה', ok=None)
    BZ, _ = built_zones()
    inb = lambda x, y: zone_at(x, y) in BZ
    # junctions and their control
    sig = {s['node'] for s in MJ.get('signals', [])}; rab = {r['node'] for r in MJ.get('roundabouts', [])}; riro = {r['node'] for r in MJ.get('riro', [])}
    mj = [(n['x'], n['y'], n['id'], 'רמזור' if n['id'] in sig else 'כיכר' if n['id'] in rab else 'ימינה בלבד' if n['id'] in riro else 'אחר') for n in MJ['nodes'] if n.get('deg', 3) >= 3 and inb(n['x'], n['y'])]
    gsig = set(GD['signals'])
    gj = [(n['x'], n['y'], n['id'], 'רמזור' if n['id'] in gsig else 'אחר') for n in GD['nodes'] if inb(n['x'], n['y']) and n.get('kind') in ('intersection', 'roundabout', 'major', '')]   # 'major' — a junction of the main road (J37_16, ‏AIR-W0)
    for x, y, i, c in mj:
        ok, d, q = near((x, y), gj)
        if not ok: fails.append(F('צומת %s (%s)' % (i, zone_at(x, y)), 'במפה (%d, %d), ובמשחק אין צומת עד 4.5 מ׳ (הקרוב: %s, ‏%.1f מ׳)' % (x, y, q[2] if q else '—', d / 10), 'סבב 9ס או הבונה'))
        elif c == 'רמזור' and q[3] != 'רמזור': fails.append(F('צומת %s' % i, 'במפה רמזור, ובמשחק (%s) בלי רמזור' % q[2]))
        elif c in ('אחר', 'ימינה בלבד') and q[3] == 'רמזור' and c != 'כיכר':
            fails.append(F('צומת %s' % i, 'במפה %s, ובמשחק (%s) רמזור' % (c if c != 'אחר' else 'עצור / זכות קדימה', q[2]), 'R-86 ג2: לקבוע מה נכון'))
    for x, y, i, c in gj:
        if c != 'רמזור': continue
        ok, d, q = near((x, y), [(a, b, n, cc) for a, b, n, cc in mj])
        if not ok: fails.append(F('רמזור %s (%s)' % (i, zone_at(x, y)), 'במשחק, ואין צומת במפה עד 4.5 מ׳ (%.1f מ׳)' % (d / 10), 'חיבור זמני — לרשום חריג עם תאריך היציאה (R-86 ג2)'))
    # crosswalks
    def xwpos(c):   # the middle of the crossing: from the junction (at) along the arm (u), between d0 and d1
        u = c.get('u') or [0, 0]; m = ((c.get('d0') or 0) + (c.get('d1') or 0)) / 2
        return (c['at'][0] + u[0] * m, c['at'][1] + u[1] * m)
    mx = [(xwpos(c)[0], xwpos(c)[1], c.get('node'), c.get('seg')) for c in MJ['bus'].get('crosswalks', []) if inb(*xwpos(c))]
    gx = [(c['x'], c['y'], c.get('node') or c['id'], c.get('road')) for c in GD.get('xw', []) + GD.get('zebra', []) if inb(c['x'], c['y'])]
    for x, y, nd, sg in mx:
        ok, d, q = near((x, y), gx)
        if not ok: fails.append(F('מעבר %s / %s' % (nd, sg), 'במפה (%d, %d), ובמשחק אין מעבר עד 4.5 מ׳ (%.1f מ׳)' % (x, y, d / 10), 'R-86 ג3'))
    for x, y, nd, sg in gx:
        ok, d, q = near((x, y), mx)
        if not ok: fails.append(F('מעבר במשחק %s / %s' % (nd, sg), '(%d, %d) — ובמפה אין מעבר עד 4.5 מ׳ (%.1f מ׳)' % (x, y, d / 10), 'R-86 ג3'))
    # bus bays
    mb = []
    for s in MJ['bus'].get('stops', []):
        for b in s.get('bay_list', []) or []:
            if b.get('pole') and inb(*b['pole']): mb.append((b['pole'][0], b['pole'][1], s.get('name', ''), b.get('dir', '')))
    term = {t['id'] for t in (GD.get('term') or {}).values()}   # the terminal bays of E3 — compared with the yard, not with the bays of the streets
    gb = [(s['x'], s['y'], s['id'], s.get('label', '')) for s in GD.get('stops', []) + GD.get('mapStops', []) if s.get('x') is not None and inb(s['x'], s['y']) and s['id'] not in term and not s.get('terminal')]
    for x, y, nm, dr in mb:
        ok, d, q = near((x, y), gb, 80)
        if not ok: fails.append(F('מפרץ "%s" (%s)' % (nm, dr), 'במפה (%d, %d), ובמשחק אין תחנה עד 8 מ׳ (%.1f מ׳)' % (x, y, d / 10), 'סוף S9a — התחנות של המפה (R-86 ג5)'))
    for x, y, i, lb in gb:
        ok, d, q = near((x, y), mb, 80)
        if not ok: fails.append(F('תחנה במשחק %s' % i, '(%d, %d) — ובמפה אין מפרץ עד 8 מ׳ (%.1f מ׳)' % (x, y, d / 10), 'R-86 ג5'))
    # the crossings inside the terminal of E3 (D‑423): the map (bus.terminal.r9.crossings) against the game (P560Y.xs) — the distance
    # between the two rectangles (0 when they overlap); a crossing drawn longer in the game is the same crossing
    TT = MJ['bus'].get('terminal') or {}
    mt = [(c['r'], c['id']) for c in (TT.get('crossings') or (TT.get('r9') or {}).get('crossings') or []) if c.get('r')]
    gt = [(c['r'], c['id']) for c in GD.get('termXw', []) if len(c.get('r') or []) == 4]
    def rd(a, b):
        dx = max(0, max(a[0], b[0]) - min(a[2], b[2])); dy = max(0, max(a[1], b[1]) - min(a[3], b[3])); return math.hypot(dx, dy)
    if 'termXw' in GD:
        for A_, B_, he in ((mt, gt, 'במפה'), (gt, mt, 'במשחק')):
            for r, i in A_:
                d = min([rd(r, q) for q, _ in B_] or [1e9])
                if d > TOL: fails.append(F('מעבר במסוף %s (%s)' % (i, he), '(%d, %d – %d, %d) — ובצד השני אין מעבר במסוף עד 4.5 מ׳ (%.1f מ׳)' % (r[0], r[1], r[2], r[3], d / 10), 'R-86 ג3 — D‑423'))
    # road segments: the middle of every map segment in a built zone — on a game edge; and back
    GE = []
    Nn = {n['id']: n for n in GD['nodes']}
    for e in GD['edges']:
        pts = e.get('pts') or ([[Nn[e['a']]['x'], Nn[e['a']]['y']], [Nn[e['b']]['x'], Nn[e['b']]['y']]] if e['a'] in Nn and e['b'] in Nn else [])
        if len(pts) >= 2: GE.append((e['id'], pts))
    ME = [(sg['id'], sg['pts']) for sg in MJ['segments'] if len(sg.get('pts', [])) >= 2]
    def on(p, L):
        bd = 1e9; bi = None
        for i, pts in L:
            for a, b in zip(pts, pts[1:]):
                d = seg_dist(p, a, b)
                if d < bd: bd = d; bi = i
        return bd, bi
    for i, pts in ME:
        a, b = pts[len(pts) // 2 - 1], pts[len(pts) // 2]; p = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if not inb(*p): continue
        d, gi = on(p, GE)
        if d > TOL: fails.append(F('קטע %s (%s)' % (i, zone_at(*p)), 'האמצע במפה (%d, %d), והקטע הקרוב במשחק (%s) %.1f מ׳ משם' % (p[0], p[1], gi, d / 10), 'סבב 9ס או הבונה (R-86 ג4)'))
    for i, pts in GE:
        a, b = pts[len(pts) // 2 - 1], pts[len(pts) // 2]; p = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if not inb(*p): continue
        d, mi = on(p, ME)
        if d > TOL: fails.append(F('קטע במשחק %s (%s)' % (i, zone_at(*p)), 'האמצע (%d, %d) — ובמפה אין דרך עד 4.5 מ׳ (%.1f מ׳; הקרוב %s)' % (p[0], p[1], d / 10, mi), 'דרך פנימית או ישנה — לרשום ברשימת "ייצא" או במפה (R-86 ג4)'))
    note = 'האזורים הבנויים: %s · צמתים במפה %d / במשחק %d · מעברים %d / %d · מפרצים %d / תחנות (של הקווים ושל המפה) %d · מעברי המסוף %d / %d · המגרשים — רק הסטטוס (ה2); ההשוואה של המגרשים בשני הכיוונים לא נעשתה' % (
        ', '.join(sorted(BZ)), len(mj), len(gj), len(mx), len(gx), len(mb), len(gb), len(mt), len(gt))
    return chk('ה1', 'המפה מול המשחק בשני הכיוונים באזורים שנבנו: קטעי דרך, צמתים וסוג השליטה, מעברי חצייה, מפרצי תחנה (4.5 מ׳)', fails, note)


def check_lot_status(MP):
    """ה2 — הסטטוס של מגרש באזור שנבנה — לא "עתידי" """
    fails = []
    M = MP.get('map')
    if not M: return chk('ה2', 'מגרש באזור שנבנה — לא "עתידי"', [], 'לא נבדק — אין __MAP', ok=None)
    BZ, _ = built_zones()
    for r in M['lots']:
        x0, y0, x1, y1, ii = r[:5]
        z = zone_at((x0 + x1) / 2, (y0 + y1) / 2)
        if z not in BZ: continue
        info = M['info'][ii] if ii < len(M['info']) else ''
        if 'עתידי' in info:
            nm = re.sub(r'<[^>]+>', ' ', info).strip()[:70]
            fails.append(F('%s — %s' % (z, nm), 'במפה "עתידי", והאזור נבנה', 'סבב 9ס: הסטטוס נגזר מהמשחק ומטבלת השלבים (R-86 ג1)'))
    return chk('ה2', 'מגרש באזור שנבנה — לא "עתידי"', fails)


def check_drawings(P):
    """ה3 — גיליון או ציור שהתאריך שלו מוקדם מהבנייה האחרונה של האזור — "לא מעודכן" """
    fails = []
    _, Z = built_zones()
    def d_(s):
        m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', s or '')
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None
    rows = []
    for b in P.get('bands2') or []:
        if b.get('id') == 'drawings': rows = b['rows']
    if not rows: fails.append(F('הציורים', 'אין טבלת "מעודכן עד" לציורים', 'D‑521 / R-85'))
    for r in rows:
        name, upto, zones, state = r[0], r[1], r[2], r[3]
        dd = d_(upto)
        for z in ZRE.findall(zones):
            if z in Z and dd and d_(Z[z].get('date')) and d_(Z[z]['date']) > dd and not re.match(r'^(היסטוריה|לא מעודכן|הוחלף)', state):
                fails.append(F(name, 'מעודכן עד %s, ו-%s נבנה אחר כך (%s)' % (upto, z, Z[z]['last']), 'לסמן "לא מעודכן" או לעדכן'))
    return chk('ה3', 'ציור או גיליון שמוקדם מהבנייה האחרונה של האזור שלו — מסומן "לא מעודכן"', fails, '%d ציורים' % len(rows))


def check_stop_zone(GD):
    """ה4 — האזור שרשום בתחנה — האזור שלפי המיקום שלה"""
    fails = []
    if not GD: return chk('ה4', 'האזור שרשום בתחנה', [], 'לא נבדק', ok=None)
    for s in GD.get('stops', []):
        z = zone_at(s['x'], s['y'])
        if s.get('chunk') and z and s['chunk'] != z:
            fails.append(F(s['id'], 'רשום %s, ועומד ב-%s (%d, %d)' % (s['chunk'], z, s['x'], s['y']), 'הבונה: D‑523 — chunk = האזור שבו התחנה עומדת; serves — האזור שהיא משרתת'))
    return chk('ה4', 'האזור שרשום בתחנה הוא האזור שלפי המיקום שלה', fails)


def check_uturn(GD):
    """ה6 — כל קו בלי פרסה, או חריגה רשומה"""
    fails = []
    if not GD: return chk('ה6', 'בלי פרסה', [], 'לא נבדק', ok=None)
    E = {e['id']: e for e in GD['edges']}
    for ln, rt in GD['routes'].items():
        seq = [(s['edgeId'], s['dirSign']) for s in rt]
        for i in range(1, len(seq)):
            if seq[i][0] == seq[i - 1][0] and seq[i][1] != seq[i - 1][1]:
                e = E.get(seq[i][0], {})
                fails.append(F('קו %s' % ln, 'פרסה על %s (%s) — האוטובוס חוזר באותו קטע' % (seq[i][0], e.get('name', '')), 'D‑520: קו 4 לא מופעל עד S16, וב-S16 — עד חזית הטרמינל בלי פרסה'))
    return chk('ה6', 'כל קו בלי פרסה (כלל שלב 13), או חריגה רשומה', fails)


def check_history(P):
    """ו4 / ו6 — הטקסט הישן (v5.62, ‏59 אזורים) והכפילויות — כמה עוד בתוכנית הנוכחית"""
    n562 = n59 = 0
    for t in active_texts(P):
        n562 += t.count('v5.62')
        if 'D‑164' not in t: n59 += len(re.findall(r'59 (?:ה)?אזורים(?! \(עודכן)|59 Chunks', t))   # a record that already says "80 (D‑164)" — updated
    note = '"v5.62" — %d פעמים, "59 אזורים" — %d פעמים, בתוכנית הנוכחית (בלי ההיסטוריה)' % (n562, n59)
    fails = [F('59 אזורים', '%d אזכורים בטקסט הנוכחי' % n59, 'לעדכן ל-80 או לסמן "הוחלף"')] if n59 else []
    return chk('ו4', 'הטקסט הישן — "59 אזורים" רק בפרק ההיסטוריה', fails, note)


def run_all(plan_path, build, gsha, MJ, now=None):
    now = now or dt.datetime.now(dt.timezone(dt.timedelta(hours=2))).replace(tzinfo=None)
    PH = open(plan_path, encoding='utf-8').read()
    o = '<script type="application/json" id="plan-data">'
    i = PH.index(o) + len(o); j = PH.index('</script>', i)
    P = json.loads(PH[i:j].replace('<\\/', '</'))
    GS = game_static(build); GD, err = game_dump(build, gsha)
    if GD:
        m = re.search(r'(S7F\d+)', os.path.basename(build), re.I); GD['buildCode'] = m.group(1).upper() if m else ''
    MP = map_page()
    C = [check_versions(P, PH, MJ, MP, GS, GD), check_zone_stages(P), check_stages(P), check_refs(P), check_pending(P), check_lines(MP, GS, GD),
         check_schedule(P, now), check_english(P), check_map_game(MJ, MP, GD), check_lot_status(MP), check_drawings(P), check_stop_zone(GD), check_uturn(GD), check_history(P)]
    # 8.11 (v6.93): the known failures (plan600/data/sync_known.json) — reported apart; a check fails only on a failure that is not known
    try: KN = json.load(open(os.path.join(WORK, 'plan600', 'data', 'sync_known.json'), encoding='utf-8'))['known']
    except Exception: KN = []
    for c in C:
        ks = [k for k in KN if k['check'] == c['id']]
        if not ks or c['ok'] is None: continue
        known, new = [], []
        for f in c['fails']:
            k = next((k for k in ks if re.search(k['match'], f['what'])), None)
            (known if k else new).append(dict(f, known=k['why']) if k else f)
        c['fails'] = new; c['known'] = known; c['n'] = len(new); c['nKnown'] = len(known); c['ok'] = not new
        c['note'] = (c['note'] + ' · ' if c['note'] else '') + '%d כישלונות ידועים עם סיבה (sync_known.json)' % len(known)
    return C, err
