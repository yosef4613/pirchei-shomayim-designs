#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-66 (2.11) — בדיקת הסנכרון: התוכנית מול מפת הדרכים מול המשחק, לכל אחד מ-80 האזורים — המצב, השלב והשם.

המצב של אזור מחושב (לא מוקלד) מקובץ המשחק ומהמפה, באחד מחמשת הנוסחים:
  "נבנה מחדש — שלב S, הבנייה"  — במשחק יש לאזור קובץ אזור חדש (window.<Z>LOOK / <Z>LOOK=…), הבנייה = הבנייה הראשונה שנמסרה ושיש בה אותו
  "ישן — ייבנה מחדש בשלב S"     — האזור חי במשחק (ACTIVE_REGIONS) בלי קובץ אזור חדש
  "השדה — ישן, ייבנה מחדש בשלב S15 / S16"  — אזור של השדה (terrain.airport במפה) שחי במשחק (4.11: "מוקפא" — רק התיקונים הקטנים)
  "עתידי — שלב S"               — לא חי במשחק ואינו ים (בשדה: "עתידי — שלב 8")
  "ים"                           — השם במפה הוא מים (ים, מימי הנמל, נתיב שיט / מטען / האוניות, מפרץ)
השלב — השלב של האזור במפה (transition.stages, ‏S1–S13); בשדה — "שלב 8"; ים בלי שלב — "—".
השם — השם במפה (names.json); האי (D‑259, ‏island.label במפה: F9 + G9 + H9) — "האי".

usage: python3 sync_check.py [--build <game.html>] [--plan <plan.html> | none] [--map city_plan.json] [--names names.json] [--out result.json] [--zonesOnly]
       8.11: עם --plan — גם הבדיקה המלאה (tools_pack/sync_full.py: ט1–ט8 של R-83, ‏ה1–ה6 של R-87); לכל כישלון — מה, הסיבה ואיפה התיקון.
       בלי --plan: התוכנית האחרונה ב-plan600/out; ‏--plan none — רק המפה מול המשחק. הפלט: קובץ json (ברירת המחדל plan600/out/sync_<הבנייה>.json) ושורה אחת.
       קוד יציאה 0 — אפס הבדלים, 1 — יש הבדלים (לכל הבדל: מה, בין מה למה, ואיפה התיקון)."""
import sys, os, re, json, glob, hashlib, argparse

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF_BUILD = os.path.join(WORK, 'clean_r2b_025637', 'out', 'Turbo_City_v1_96_GATE77_S7F198.html')
DEF_MAP = os.environ.get('SYNC_MAP') or os.path.join(WORK, 'study', 'roads', 'city_plan.json')   # 8.11: SYNC_MAP — a saved copy of the map (the rebuild of an older plan)
DEF_NAMES = os.path.join(WORK, 'study', 'roads', 'names.json')
DAILY = os.path.join(WORK, 'study', 'pages', 'daily.json')
STATUS = sorted(glob.glob(os.path.join(WORK, 'STATUS_*.md')))
PLAN_NEW = os.path.join(WORK, 'plan600', 'data', 'new.json')
COLS = 'ABCDEFGH'
ZONES = [c + str(r) for r in range(10) for c in COLS]
WATER = re.compile(r'^(ים|מימי הנמל|נתיב שיט|נתיב מטען|נתיב האוניות|מפרץ)')


def grab(H, marker, start=0):
    """the JS literal ({…} or […]) after a marker, by bracket matching (strings aware)"""
    i = H.index(marker, start) + len(marker)
    while H[i] in ' \t\n=': i += 1
    op = H[i]; d = 0; j = i; q = None
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


def zones_of(code):
    """'A34' → A3, A4 · 'C4D4' → C4, D4 · 'B3' → B3"""
    out = []
    for L, digs in re.findall(r'([A-H])(\d+)', code):
        out += [L + d for d in digs]
    return out


ZONE_BUILDS = os.path.join(WORK, 'tools_pack', 'zone_builds.json')
ZONE_BUILDS_PLAN = os.path.join(WORK, 'plan600', 'data', 'zone_builds.json')   # 8.11 (v6.93): what the later builds touched — over the table of tools_pack
def zone_builds():
    try: Z = json.load(open(ZONE_BUILDS, encoding='utf-8'))['zones']
    except Exception: Z = {}
    if os.environ.get('ZONE_BUILDS_EXTRA', '') != 'none' and os.path.exists(ZONE_BUILDS_PLAN):   # ZONE_BUILDS_EXTRA=none — only the first table (the rebuild of v6.92)
        try: Z = dict(Z, **json.load(open(ZONE_BUILDS_PLAN, encoding='utf-8'))['zones'])
        except Exception: pass
    return Z


def build_no(path):
    m = re.search(r'S7F(\d+)', os.path.basename(path)); return int(m.group(1)) if m else -1


def module_markers(H):
    """the zone modules of the rebuilt zones in the game file: {zone: marker}"""
    mk = {}
    for rx in (r'window\.([A-H][0-9A-H]*)LOOK\s*=\s*\{', r'G0\.([A-H][0-9A-H]*)LOOK\s*=\s*create\(\)', r'__TC_([A-H][0-9A-H]*)LOOK=\{audit',
               r'\b([A-H][0-9])_BUILDINGS\.filter\(o=>o\.bld4\d\)'):   # the zone look modules, and the zone buildings of the new building engine (BLD40 …)
        for m in re.finditer(rx, H):
            for z in zones_of(m.group(1)):
                L = mk.setdefault(z, [])
                if m.group(0) not in L: L.append(m.group(0))
    # 3.11 20:35: E3 was rebuilt (S7F228, p560_e3b — the terminal yard) without a LOOK module; its marker is the yard of p560
    for rx, z in ((r'window\.__TC_P560Y=', 'E3'), (r'window\.__TC_D2=', 'D2'), (r'\bC2_MID_AISLES=', 'C2')):   # 8.11 (R-87): D2 (S7F264) and C2 (S7F256) — their markers
        mm = re.search(rx, H)
        if mm: mk.setdefault(z, []).append(mm.group(0))
    return mk


def delivered_builds():
    """the builds that were delivered — from the daily report (builds: "נמסרה"), the status file and the plan data"""
    out = set()
    try:
        for b in json.load(open(DAILY, encoding='utf-8')).get('builds', []):
            if str(b[3]).startswith('נמסרה'): out.add(b[0])
    except Exception: pass
    txt = ''
    for f in STATUS + [PLAN_NEW]:
        try: txt += open(f, encoding='utf-8').read() + '\n'
        except Exception: pass
    for m in re.finditer(r'(S7F\d{3}) נמסרה|נמסר(?:ה|ו)? (?:ב-|עם )?\(?(S7F\d{3})|נמסר[^"\n;]{0,30}\((S7F\d{3}) ·', txt):
        out.add(next(g for g in m.groups() if g))
    for m in re.finditer(r'נבנו ונמסרו: ([^;"\n]*)', txt):
        out.update(re.findall(r'S7F\d{3}', m.group(1)))
    return out


def game_facts(build):
    H = open(build, encoding='utf-8').read()
    names = json.loads(grab(H, 'TC_NAMES='))['zones']
    act = grab(H, 'const ACTIVE_REGIONS=')
    active = set()
    for tok in re.findall(r'[A-Z0-9_]+', act):
        m = re.match(r'^([A-H][0-9])(?:_REGION)?$', tok)
        if m: active.add(m.group(1))
    mk = module_markers(H)
    for z in zone_builds():   # 8.11: a zone of the table of the builds is rebuilt, also when its module has no marker
        if z not in mk: mk[z] = ['zone_builds.json']
    # the build that rebuilt each zone: the first build (in the folder of the build, up to it) that has the marker, then the first delivered one from there
    folder = os.path.dirname(os.path.abspath(build)); me = build_no(build)
    seq = sorted([f for f in glob.glob(os.path.join(folder, 'Turbo_City_v1_96_GATE77_S7F*.html')) if 180 <= build_no(f) <= me], key=build_no)
    first = {}
    texts = {}
    for f in seq:
        missing = [z for z in mk if z not in first]
        if not missing: break
        t = open(f, encoding='utf-8', errors='replace').read()
        for z in missing:
            if any(x in t for x in mk[z]): first[z] = build_no(f)   # the earliest of the markers of the zone
    dl = delivered_builds()
    built = {}
    for z, n in first.items():
        cand = [b for b in seq if build_no(b) >= n and 'S7F%d' % build_no(b) in dl]
        built[z] = {'first': 'S7F%d' % n, 'build': 'S7F%d' % build_no(cand[0]) if cand else 'S7F%d' % n, 'delivered': bool(cand)}
    # 8.11 (R-87, סעיף ד1): the build of the current version of every zone and the last build that touched it — from the table of the
    # builds (tools_pack/zone_builds.json; the build folder has only one build now, so the first build cannot be computed from it)
    ZB = zone_builds()
    for z, o in ZB.items():
        if build_no('S7F' + o['build'][4:]) <= me or True:
            built[z] = {'first': o['build'], 'build': o['build'], 'last': o.get('last', o['build']), 'delivered': True, 'why': o.get('why', ''),
                        'part': o.get('part'), 'rest': o.get('rest'), 'date': o.get('date', '')}
    # what the game has in each zone now: the labelled items with an id of the zone, the stalls, and the counts of the zone data
    labels = {}
    for m in re.finditer(r'''["']?id["']?\s*:\s*["']([A-H][0-9])-([A-Z0-9-]+)["']([^{}]{0,240})''', H):
        z, rest = m.group(1), m.group(3)
        lm = re.search(r'''["']?label["']?\s*:\s*["']([^"']{2,60})["']''', rest)
        if lm:
            L = labels.setdefault(z, [])
            if lm.group(1) not in L: L.append(lm.group(1))
    stalls = {}
    for m in re.finditer(r'''["']?id["']?\s*:\s*["']([A-H][0-9])-[A-Z0-9-]*-S\d+["']''', H):
        stalls[m.group(1)] = stalls.get(m.group(1), 0) + 1
    data = {}
    for key, zs in (('C3D=', ['C3']), ('D3ND=', ['D3']), ('C4ND=', ['C4']), ('D4ND=', ['D4']), ('B3LOOKD=', ['B3'])):
        try:
            o = json.loads(grab(H, key))
            for z in zs: data[z] = {k: len(v) for k, v in o.items() if isinstance(v, list)}
        except Exception: pass
    sha = hashlib.sha1(H.encode('utf-8')).hexdigest()[:12]
    return {'names': names, 'active': active, 'modules': mk, 'built': built, 'labels': labels, 'stalls': stalls, 'data': data,
            'sha': sha, 'size': len(H.encode('utf-8')), 'build': 'S7F%d' % me}


def map_facts(mp, nm):
    C = json.load(open(mp, encoding='utf-8')); N = json.load(open(nm, encoding='utf-8'))['zones']
    stage = {z: s['stage'] for s in C['transition']['stages'] for z in s['zones']}
    for z, v in C['zones'].items():
        if v.get('stage'): stage.setdefault(z, v['stage'])
    air = set()
    for x0, y0, x1, y1 in C['terrain']['airport']:
        for z in ZONES:
            c, r = COLS.index(z[0]), int(z[1])
            if x0 <= c * 1200 and (c + 1) * 1200 <= x1 and y0 <= GRID_ROWS[r] and GRID_ROWS[r + 1] <= y1: air.add(z)
    island = set(re.findall(r'[A-H][0-9]', C.get('island', {}).get('label', '')))
    purpose = {z: v.get('purpose', '') for z, v in C['zones'].items()}
    return {'names': N, 'stage': stage, 'air': air, 'island': island, 'purpose': purpose, 'round': C.get('title', '')}


GRID_ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
# 4.11 (the owner 01:24–01:27): S14 — the sea A7–E9 (without E7 / E8, in S13 with the bridge); S15 — the field, the airside (stage 8); S16 — the field, the landside (stage 9, with the player in the field, stage 10)
STAGE_OVER = {'E3': 'S9a'}   # 8.11 (D‑521): E3 — the first part of S9 in the plan (S9a); on the map — S9
SEA_S14 = ({c + r for c in 'ABCDE' for r in '789'} - {'E7', 'E8'}) | {'G4', 'H4', 'G5', 'H5'}   # 8.11 (R-83 ב4, ‏D‑521): G4, H4, G5, H5 — the open sea in S14
FIELD_STAGE = {'E2': 'S16', 'F2': 'S15–S16', 'G2': 'S15–S16', 'G3': 'S15–S16', 'H3': 'S15–S16'}   # 8.11 (R-83 ג, ‏D‑464): by the content — G2 the staff parking, G3 + H3 the long parking and the rental — S16   # E2 — the landside (the security gate, the cargo, the parking); F2 — the terminal: its airside in S15, the frontage in S16; the rest of the field — S15


def expected(G, M):
    """the one state, stage and name of every zone — from the game and the map"""
    out = {}
    for z in ZONES:
        mname = M['names'].get(z, '')
        name = 'האי' if z in M['island'] else mname
        if z in M['air']: stg = FIELD_STAGE.get(z, 'S15')   # 4.11 (the owner 01:24–01:27): the field is rebuilt — S15 the airside, S16 the landside
        else: stg = STAGE_OVER.get(z) or M['stage'].get(z) or ('S14' if z in SEA_S14 else '—')   # S14 — the sea, A7–E9 (E7 / E8 — S13, the bridge)
        if z in G['modules'] and z in G['active']:
            bz = G['built'].get(z, {}); b = bz.get('build', '?')
            if bz.get('part'):   # 8.11 (R-87): B1 — in two parts
                stg = '%s / %s' % (bz['part'], bz.get('rest') or stg)
                st, kind = 'נבנה בחלקו — %s: %s (עודכן לאחרונה ב-%s); השאר — שלב %s' % (bz['part'], b, bz.get('last', b), bz.get('rest') or '—'), 'rebuilt'
            else:
                st, kind = 'נבנה מחדש — שלב %s, %s' % (stg, b) + (' · עודכן לאחרונה ב-%s' % bz['last'] if bz.get('last') and bz['last'] != b else ''), 'rebuilt'
        elif z in M['air'] and z in G['active']:
            st, kind = 'השדה — ישן, ייבנה מחדש בשלב %s (עד אז — בלי תיקונים קטנים)' % stg, 'airport'
        elif z in G['active']:
            st, kind = 'ישן — ייבנה מחדש בשלב %s' % stg, 'old'
        elif z not in M['island'] and WATER.match(mname):
            st, kind = ('ים — ייבנה בשלב %s' % stg if stg.startswith('S') else 'ים'), 'sea'
        else:
            st, kind = 'עתידי — %s' % (('שלב ' + stg) if stg.startswith('S') else stg), 'future'
        out[z] = {'state': st, 'kind': kind, 'stage': stg, 'name': name, 'mapName': mname, 'gameName': G['names'].get(z, '')}
    return out


def describe(z, G, e):
    """what the zone has in the game now — computed from the game file"""
    L = [x for x in G['labels'].get(z, []) if not re.match(r'^(חניה|חניות)\b', x)]
    parts = []
    if e['kind'] == 'rebuilt':
        parts.append('במשחק (%s): קובץ אזור חדש' % G['build'])
        if G['built'].get(z, {}).get('why'): parts.append('הבניות: ' + G['built'][z]['why'])   # 8.11 (R-87): the builds that touched the zone
    elif e['kind'] in ('old', 'airport'):
        parts.append('במשחק (%s): התוכן הישן, מלפני B4' % G['build'])
    elif e['kind'] == 'sea':
        parts.append('במשחק: ים' + (' — ובו עדיין התוכן הישן של האי, שיוצא בשלב %s' % e['stage'] if G['labels'].get(z) else ''))
    else:
        parts.append('במשחק: עוד לא בנוי')
    if L: parts.append('מה יש בו: ' + ', '.join(L[:8]) + (' ועוד %d' % (len(L) - 8) if len(L) > 8 else ''))
    cnt = counts(z, G)
    if cnt: parts.append(cnt)
    return ' · '.join(parts)


def counts(z, G):
    """the counts the game file has for the zone: the stalls with an id of the zone, and the lists of the zone data"""
    d = G['data'].get(z, {})
    cnt = []
    if G['stalls'].get(z): cnt.append('חניות %d' % G['stalls'][z])
    for k, he in (('buildings', 'מבנים'), ('trees', 'עצים'), ('lamps', 'פנסים'), ('pools', 'בריכות'), ('containers', 'מכולות'), ('hedges', 'קטעי גדר חיה')):
        if d.get(k): cnt.append('%s %d' % (he, d[k]))
    return ' · '.join(cnt)


def compute(build=DEF_BUILD, mp=DEF_MAP, nm=DEF_NAMES):
    G = game_facts(build); M = map_facts(mp, nm); E = expected(G, M)
    for z in ZONES: E[z]['desc'] = describe(z, G, E[z]); E[z]['counts'] = counts(z, G)
    return G, M, E


PLAN_META = {}
def plan_zones(plan):
    H = open(plan, encoding='utf-8').read()
    o = '<script type="application/json" id="plan-data">'
    i = H.index(o) + len(o); j = H.index('</script>', i)
    D = json.loads(H[i:j].replace('<\\/', '</'))
    PLAN_META.clear(); PLAN_META.update(D.get('meta', {}))   # R-77: the build at the top of the plan and the delivery line
    return D['zones'], D.get('meta', {}).get('title', ''), hashlib.sha1(H.encode('utf-8')).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', default=DEF_BUILD); ap.add_argument('--plan', help='the plan page; default — the newest in plan600/out; "none" — the map and the game only')
    ap.add_argument('--map', default=DEF_MAP)
    ap.add_argument('--names', default=DEF_NAMES); ap.add_argument('--out')
    ap.add_argument('--zonesOnly', action='store_true', help='only the 80 zones (the check of v6.91)')
    a = ap.parse_args()
    G, M, E = compute(a.build, a.map, a.names)
    diffs = []
    plan_meta = None; PZ = None
    if a.plan is None:   # the newest plan of plan600/out (not the extra page)
        cand = [f for f in glob.glob(os.path.join(WORK, 'plan600', 'out', 'Turbo_City_Master_Plan_v*.html')) if not f.endswith('_page.html')]
        def ver(f):
            m = re.search(r'_v(\d+)_(\d+)\.html$', f); return (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        a.plan = max(cand, key=ver) if cand else ''
    if a.plan and a.plan != 'none':
        PZ, title, psha = plan_zones(a.plan); plan_meta = {'file': os.path.basename(a.plan), 'title': title, 'sha': psha}
    for z in ZONES:
        e = E[z]
        # the name: the map (names.json) — the game (TC_NAMES is made from it at the build) — the plan; the island of the map (island.label, D‑259)
        if e['gameName'] != e['mapName']:
            diffs.append({'zone': z, 'what': 'השם', 'pair': 'המשחק מול המפה', 'plan': None, 'map': e['mapName'], 'game': e['gameName'], 'fix': 'בבנייה הבאה של המשחק (TC_NAMES נבנה מ-names.json)'})
        pname = (PZ.get(z) or {}).get('name') if PZ is not None else e['name']
        if pname != e['mapName']:
            diffs.append({'zone': z, 'what': 'השם', 'pair': 'התוכנית מול המפה והמשחק' if PZ is not None else 'האי במפה (island.label) מול השם במפה (names.json)',
                          'plan': pname, 'map': e['mapName'], 'game': e['gameName'],
                          'fix': ('במפה: names.json — zones.%s ‏"%s" ← "%s" (האי: %s, ‏D‑259), ואז במשחק בבנייה הבאה' % (z, e['mapName'], e['name'], ' + '.join(sorted(M['island']))))
                                 if z in M['island'] else 'בתוכנית: השם לפי המפה'})
        if PZ is not None:
            p = PZ.get(z) or {}
            for k, he in (('state', 'המצב'), ('stage', 'השלב')):
                if p.get(k, '') != e[k]:
                    diffs.append({'zone': z, 'what': he, 'pair': 'התוכנית מול המשחק והמפה', 'plan': p.get(k, ''), 'computed': e[k], 'fix': 'בתוכנית: v600_step49.py (zoneSync) מחדש על הבנייה'})
    if PZ is not None:   # R-77 (the review 15:40): the build at the top of the plan, the delivery line and the state of the zones — from the same build
        mb = PLAN_META.get('build', ''); rl = PLAN_META.get('runLine', '')
        if mb != G['build']:
            diffs.append({'zone': '—', 'what': 'הבנייה בראש התוכנית', 'pair': 'התוכנית מול הבנייה', 'plan': mb, 'computed': G['build'], 'fix': 'בתוכנית: plan600/tools/plan_sync.py על הבנייה'})
        if G['build'] not in rl:
            diffs.append({'zone': '—', 'what': 'שורת המסירה', 'pair': 'התוכנית מול הבנייה', 'plan': rl[:120], 'computed': G['build'], 'fix': 'בתוכנית: plan600/tools/plan_sync.py על הבנייה'})
        zb = PLAN_META.get('zonesBuild', '')
        if zb != G['build']:
            diffs.append({'zone': '—', 'what': 'מצב האזורים מחושב מ', 'pair': 'התוכנית מול הבנייה', 'plan': zb, 'computed': G['build'], 'fix': 'בתוכנית: plan600/tools/plan_sync.py על הבנייה'})
    counts = {}
    for z in ZONES: counts[E[z]['kind']] = counts.get(E[z]['kind'], 0) + 1
    res = {'build': G['build'], 'buildSha': G['sha'], 'buildSize': G['size'], 'map': M['round'], 'plan': plan_meta, 'zones': len(ZONES),
           'counts': counts, 'rebuilt': {z: G['built'].get(z) for z in sorted(G['modules']) if z in G['active']},
           'diffs': diffs, 'nDiffs': len(diffs), 'table': {z: E[z] for z in ZONES}}
    he = {'rebuilt': 'נבנו מחדש', 'old': 'ישנים', 'airport': 'השדה הישן', 'future': 'עתידיים', 'sea': 'ים'}
    line = ('סנכרון %s · %s%s: %d אזורים — %s · הבדלים: %d' % (
        G['build'], G['sha'], (' · התוכנית ' + plan_meta['title'] + ' ' + plan_meta['sha']) if plan_meta else '', len(ZONES),
        ', '.join('%s %d' % (he[k], counts.get(k, 0)) for k in ('rebuilt', 'old', 'airport', 'future', 'sea')), len(diffs)))
    # 8.11 (R-83 ט 1–8, ‏R-87 ה 1–6): the full check that stops a delivery — the plan, the map and the game (tools_pack/sync_full.py)
    nbad = 0
    if a.plan and a.plan != 'none' and not a.zonesOnly:
        import sync_full
        C, err = sync_full.run_all(a.plan, a.build, G['sha'], json.load(open(a.map, encoding='utf-8')))
        res['checks'] = C; res['dumpErr'] = err
        nbad = sum(1 for c in C if c['ok'] is False)
        line += ' · הבדיקה המלאה: %d מתוך %d עוברות (%s)' % (sum(1 for c in C if c['ok']), len(C), ', '.join('%s %s' % (c['id'], 'עובר' if c['ok'] else ('נכשל (%d)' % c['n']) if c['ok'] is False else 'לא נבדק') for c in C))
    res['line'] = line
    out = a.out or os.path.join(WORK, 'plan600', 'out', 'sync_%s.json' % G['build'])   # never next to the game (its folders are not written)
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(line)
    return 0 if not diffs and not nbad else 1


if __name__ == '__main__':
    sys.exit(main())
