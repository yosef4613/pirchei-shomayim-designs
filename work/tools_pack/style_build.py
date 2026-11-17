# -*- coding: utf-8 -*-
"""style_build.py — builds study/style/city_style.json, the one source of the city's design (the owner 2.11 07:00: "מדריך הסגנון של העיר").
Every value is taken from the game or from the documents, never typed fresh: each one carries its source (file + the exact string), and the
builder checks that the string is really in that file (a missing string stops the build). Where two sources disagree, the value is the
default and the conflict is listed with id ס-N and state "לאישורך".
usage: python3 tools_pack/style_build.py   → study/style/city_style.json"""
import json, re, hashlib, os, sys
W = '/home/claude/tc/pkg/work'
OUT = W + '/study/style/city_style.json'
import os as _os
GAME = _os.environ.get('TC_STYLE_GAME', 'clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F193.html')   # 2.11 08:32: בנייה אחרת — דרך style_check.py --game
SRC = {
 'G':   (GAME, 'קובץ המשחק ' + ((__import__('re').findall(r'S7F\d+', GAME) or ['S7F193'])[-1])),
 'CP':  ('study/roads/city_plan.json', 'מפת הדרכים · סבב 7'),
 'IN':  ('study/zone_spec/00_intro.md', 'תנאי הקבלה · המבוא'),
 'A4':  ('study/zone_spec/A4.md', 'תנאי הקבלה · A4'),
 'B3':  ('study/zone_spec/B3.md', 'תנאי הקבלה · B3'),
 'B4':  ('study/zone_spec/B4.md', 'תנאי הקבלה · B4'),
 'C3':  ('study/zone_spec/C3.md', 'תנאי הקבלה · C3'),
 'D3':  ('study/zone_spec/D3.md', 'תנאי הקבלה · D3'),
 'C4':  ('study/zone_spec/C4.md', 'תנאי הקבלה · C4'),
 'D4':  ('study/zone_spec/D4.md', 'תנאי הקבלה · D4'),
 'RC':  ('RULES_CARD.md', 'כרטיס הכללים'),
 'OW':  ('inbox_owner/owner_2026-11-02_0655_review_process_style.txt', 'הכללים של הבעלים (2.11, 07:00)'),
 'NJ':  ('plan600/data/new.json', 'ההחלטות (new.json)'),
 'O76': ('inbox_owner/owner_2026-11-03_1027_R76_terminal.txt', 'הבעלים 3.11 10:10 / 10:27 — R-76'),
 'R1051': ('inbox_owner/owner_2026-11-03_1051_review_notes_lane_stop.txt', 'הביקורת 3.11 10:51 — תוספות ל-R-76'),
 'UJ':  ('plan600/data/uses.json', 'טבלת השימושים (uses.json)'),
 'UT':  ('study/uses/USES_TABLE.md', 'טבלת השימושים (USES_TABLE.md)'),
 'REQ': ('exp34/c4d4/req_c4d4.json', 'גיליון הדרישות של C4 · D4'),
 'A34': ('exp34/a34/a34v1.py', 'מקור הנתונים של A3 · A4'),
 'P367':('clean_r2b_025637/tools/patches/p367_lampspacing.py', 'הטלאי p367 (מרחק הפנסים)'),
 'P441':('clean_r2b_025637/tools/patches/p441_busstops.py', 'הטלאי p441 (התחנות)'),
 'P469':('clean_r2b_025637/tools/patches/p469_special.py', 'הטלאי p469 (חניות נכים וחשמל)'),
 'ZA':  ('clean_r2b_025637/tools/patches/a34v1.json', 'הנתונים של A3 · A4'),
 'ZB3': ('clean_r2b_025637/tools/patches/b3v5.json', 'הנתונים של B3'),
 'ZB4': ('clean_r2b_025637/tools/patches/b4v5.json', 'הנתונים של B4'),
 'ZC3': ('clean_r2b_025637/tools/patches/c3v3.json', 'הנתונים של C3'),
 'ZD3': ('clean_r2b_025637/tools/patches/d3v1.json', 'הנתונים של D3'),
 'ZCD': ('clean_r2b_025637/tools/patches/c4d4v1.json', 'הנתונים של C4 · D4'),
}
TXT = {}
def text(k):
    if k in TXT: return TXT[k]
    p = W + '/' + SRC[k][0]; raw = open(p, encoding='utf-8').read()
    alt = ''
    if p.endswith('.json'):
        try: alt = json.dumps(json.load(open(p, encoding='utf-8')), ensure_ascii=False)
        except Exception: alt = ''
    TXT[k] = (raw, alt); return TXT[k]
def norm(s): return re.sub(r'[‎‏]', '', s)
MISSING = []
def S(k, s):
    """one source: the file key and the exact string (checked)"""
    raw, alt = text(k)
    if s not in raw and s not in alt and norm(s) not in norm(raw) and norm(s) not in norm(alt):
        MISSING.append((k, s))
    return {'f': k, 's': s}
def sha(p):
    b = open(W + '/' + p, 'rb').read(); return hashlib.sha1(b).hexdigest()[:12], len(b)

G = text('G')[0]
# ---------------------------------------------------------------- the building types of the game (BLD40–45), for the palettes and heights
def bld_types():
    T = {}
    for m in re.finditer(r"def\('([A-Z0-9_]+)',\s*(?:[\w.]+\()?\s*(\w+Type)\(\{", G):
        tid, fn = m.group(1), m.group(2); i = m.end(); d = 1; j = i
        while d and j < len(G):
            c = G[j]; d += (c == '{') - (c == '}'); j += 1
        body = G[i:j - 1]; kv = {}
        for k, v in re.findall(r"(\w+)\s*:\s*('(?:[^'\\]|\\.)*'|-?[\d.]+|true|false)", body):
            if k in kv: continue
            kv[k] = v.strip("'") if v.startswith("'") else (v == 'true' if v in ('true', 'false') else float(v))
        kv['fn'] = fn; kv['def'] = G[m.start():m.start() + 60].split('(')[0] + "('" + tid + "'"
        T[tid] = kv
    return T
TYPES = bld_types()
FN_WALL = {'houseType': ('#e3d5b6', 'stone', '#f2ede2'), 'rowType': (None, 'render', None), 'aptType': ('#e6d8bb', 'stone', '#f5f2eb'),
           'aptL2Type': ('#e6d8bb', 'stone', '#f5f2eb'), 'shopType': ('#ece8de', 'render', None), 'whType': ('#d8dde0', 'metal', None),
           'officeType': ('#eef0ee', 'render', None), 'garageType': (None, 'render', None), 'studioType': ('#f4f2ec', 'glass', None),
           'factoryType': ('#c98f6b', 'render', None), 'marketType': ('#e6e9ea', 'metal', None), 'schoolType': ('#f3efe6', 'render', None),
           'clinicType': ('#f6f5f1', 'render', None), 'boothType': ('#f1f1ee', 'render', None)}
FN_ROOF = {'houseType': 'רעפים', 'rowType': 'רעפים', 'aptType': 'שטוח', 'aptL2Type': 'שטוח', 'shopType': 'שטוח', 'whType': 'שטוח עם פסי תאורה',
           'officeType': 'שטוח', 'garageType': 'שטוח', 'studioType': 'שטוח', 'factoryType': 'משור', 'marketType': 'שטוח עם לוחות סולאריים',
           'schoolType': 'שטוח', 'clinicType': 'שטוח', 'boothType': 'שטוח'}
FN_FLATCOL = {'houseType': '#d3d2cc', 'aptType': '#cfd0cb', 'aptL2Type': '#cbcdc9', 'shopType': '#cfccc4', 'whType': '#c3c8cb', 'officeType': '#cfd1ce',
              'garageType': '#cfcac0', 'studioType': '#d9d6cf', 'factoryType': '#b9b3a8', 'marketType': '#d4d7d6', 'schoolType': '#cdd0cd',
              'clinicType': '#d2d5d3', 'boothType': '#e9ecee'}
MAT_HE = {'stone': 'אבן', 'render': 'טיח', 'metal': 'מתכת', 'glass': 'זכוכית', 'concrete': 'בטון'}
def type_look(tid):
    t = TYPES.get(tid) or {}; fn = t.get('fn', '')
    dw, dm, drender = FN_WALL.get(fn, (None, 'render', None))
    mat = t.get('mat') or dm
    if fn == 'houseType' and not t.get('mat'): mat = 'stone'
    wall = t.get('wall') or (drender if (mat == 'render' and drender) else dw)
    flat = bool(t.get('flat')) or fn not in ('houseType', 'rowType')
    tile = (fn in ('houseType', 'rowType') and not t.get('flat')) or bool(t.get('tile'))
    roofk = 'רעפים' if tile else FN_ROOF.get(fn, 'שטוח')
    roof = (t.get('roof') or '#b65f3d') if tile else (t.get('roofCol') or FN_FLATCOL.get(fn))
    return {'type': tid, 'fn': fn, 'mat': MAT_HE.get(mat, mat), 'wall': wall, 'roof': roof, 'roof_kind': roofk,
            'floors': int(t.get('nf') or t.get('floors') or {'houseType': 2, 'rowType': 2, 'clinicType': 2, 'aptType': 5, 'aptL2Type': 5, 'schoolType': 3, 'officeType': 2}.get(fn, 1)),
            'he': t.get('he', '')}

# ---------------------------------------------------------------- the zones that are built, and their districts
ZONES = {
 'A3': {'rect': [0, 1700, 1200, 2550], 'district': 'המערב', 'data': ['ZA'], 'he': 'קריית הספורט — צפון'},
 'A4': {'rect': [0, 2550, 1200, 3400], 'district': 'המערב', 'data': ['ZA'], 'he': 'קריית הספורט, הכבאות והאמבולנסים'},
 'B3': {'rect': [1200, 1700, 2400, 2550], 'district': 'המגורים', 'data': ['ZB3'], 'he': 'שכונת הבתים'},
 'B4': {'rect': [1200, 2550, 2400, 3400], 'district': 'המגורים', 'data': ['ZB4'], 'he': 'השכונה הצפופה'},
 'C3': {'rect': [2400, 1700, 3600, 2550], 'district': 'המגורים', 'data': ['ZC3'], 'he': 'הווילות ובית השחקן'},
 'D3': {'rect': [3600, 1700, 4800, 2550], 'district': 'המרכז', 'data': ['ZD3'], 'he': 'שירותי הרכב והווילות'},
 'C4': {'rect': [2400, 2550, 3600, 3400], 'district': 'התעשייה', 'data': ['ZCD'], 'he': 'התעשייה הקלה'},
 'D4': {'rect': [3600, 2550, 4800, 3400], 'district': 'התעשייה', 'data': ['ZCD'], 'he': 'מרכז ההפצה'},
}
def zone_buildings():
    P = W + '/clean_r2b_025637/tools/patches/'
    out = {}
    for f, z, zs in [('a34v1.json', None, ['A3', 'A4']), ('b3v5.json', None, ['B3']), ('b4v5.json', None, ['B4']), ('c3v3.json', None, ['C3']),
                     ('d3v1.json', None, ['D3']), ('c4d4v1.json', 'c4', ['C4']), ('c4d4v1.json', 'd4', ['D4'])]:
        D = json.load(open(P + f)); D = D[z] if z else D
        for b in D['buildings']:
            x0, y0 = b.get('foot', [b['x'], b['y']])[:2]
            zz = [k for k in zs if ZONES[k]['rect'][0] <= x0 < ZONES[k]['rect'][2] and ZONES[k]['rect'][1] <= y0 < ZONES[k]['rect'][3]]
            out[b['id']] = {'zone': zz[0] if zz else zs[0], 'type': b['type'], 'kind': b.get('kind')}
    return out
BLD = zone_buildings()

def palettes():
    P = {}
    for bid, b in BLD.items():
        d = ZONES[b['zone']]['district']; L = type_look(b['type'])
        p = P.setdefault(d, {'zones': [], 'walls': {}, 'roofs': {}, 'roof_kinds': {}, 'materials': {}, 'types': {}})
        if b['zone'] not in p['zones']: p['zones'].append(b['zone'])
        for key, val in [('walls', L['wall']), ('roofs', L['roof']), ('roof_kinds', L['roof_kind']), ('materials', L['mat'])]:
            if val: p[key].setdefault(val, set()).add(b['type'])
        p['types'][b['type']] = {k: L[k] for k in ('fn', 'mat', 'wall', 'roof', 'roof_kind', 'floors', 'he')}
    for d, p in P.items():
        for key in ('walls', 'roofs', 'roof_kinds', 'materials'):
            p[key] = [{'v': v, 'types': sorted(t)} for v, t in sorted(p[key].items())]
        p['zones'].sort()
    return P

# ---------------------------------------------------------------- the guide
def R(rid, he, v, unit, src, check=None, conflict=None, note=None):
    r = {'id': rid, 'he': he, 'v': v, 'unit': unit, 'src': src}
    if check: r['check'] = check
    if conflict: r['conflict'] = conflict
    if note: r['note'] = note
    return r

GROUPS = []
def group(gid, he, rules): GROUPS.append({'id': gid, 'he': he, 'rules': rules})

group('scale', 'קנה מידה ומידות — טבלה אחת', [
 R('S-01', 'קנה המידה של העולם', 10, 'פיקסלים למטר', [S('G', 'var SZ_TABLE={ppm:10,'), S('CP', '10 px = 1 מ׳; נתיב 44 px'), S('NJ', 'קנה מידה אחד לכל העולם — 10 פיקסלים למטר')]),
 R('S-02', 'ההגדלה של העיר — רכבים, אנשים וחניות', 1.125, 'פי', [S('G', 'game:1.125'), S('NJ', 'חניה אמיתית של 2.5 × 5 מ׳, בהגדלה של פי 1.125 של העיר')], check='C-27'),
 R('S-03', 'גובה קומה', [3.0, 3.3], 'מ׳', [S('OW', 'קומה 3–3.3 מ׳')], check='C-19', conflict='ס-10'),
 R('S-04', 'דלת כניסה (כנף אחת)', [1.0, 2.1], 'מ׳ (רוחב × גובה)', [S('OW', 'דלת 1 × 2.1 מ׳')], check='C-20'),
 R('S-05', 'חניה', [28, 56], 'פיקסלים (2.8 × 5.6 מ׳)', [S('OW', 'חניה 2.8 × 5.6 מ׳'), S('NJ', 'גודל החניה: 2.8 × 5.6 מ׳')], check='C-07', conflict='ס-6'),
 R('S-06', 'אדם', 19.7, 'פיקסלים (1.97 מ׳)', [S('OW', 'אדם 1.97 מ׳'), S('G', 'personH:19.7')], check='C-27'),
 R('S-07', 'הסמיטריילר בגודל הטבלה', [185.6, 28.7], 'פיקסלים (16.5 × 2.55 מ׳ × 1.125)', [S('G', "Semi:[16.5,2.55,'סמיטריילר']"), S('REQ', 'הסמי של המשחק — 185.6 × 28.7 פיקס׳')]),
 R('S-08', 'הסטייה המותרת מהטבלה — אורך / רוחב', [0.05, 0.08], 'חלק', [S('G', 'tolL:.05,tolW:.08')], check='C-27'),
 R('S-09', 'רוחב נתיב', 44, 'פיקסלים (4.4 מ׳)', [S('G', 'const SCALE={lane:44,'), S('CP', 'הנתיב ברשת של היום נשאר 4.4 מ׳ (44 px)')], conflict='ס-5'),
])

KIT = {
 'main':     {'he': 'עורק ראשי', 'map': 'main · עורק ראשי 3+3', 'width_px': 254, 'lanes': 6, 'lane_px': 39, 'median_px': 20, 'sidewalk_px': 25, 'speed_kmh': 70,
              'lamp': {'asset': 'SL-AV2', 'kit': 'lamp_double', 'he': 'פנס שדרה (שתי זרועות)', 'h_m': 9, 'spacing_px': 185}, 'trees': {'spacing_px': [50, 60], 'both_sides': True},
              'crosswalk_depth_px': 34, 'center': 'חציון של 20 פיקס׳ בין שני קווים צהובים כפולים (‎#f2c83e, ‏2.2 ו-1.4 פיקס׳)', 'lanes_line': 'קו לבן מקווקו (‎#f3f1dc, ‏2 פיקס׳, ‏16 / 15) בין 3 הנתיבים'},
 'arterial': {'he': 'עורק', 'map': 'arterial · עורק 2+2', 'width_px': 196, 'lanes': 4, 'lane_px': 44, 'median_px': 8, 'sidewalk_px': 20, 'speed_kmh': 70,
              'lamp': {'asset': 'SL-AV2', 'kit': 'lamp_double', 'he': 'פנס שדרה (שתי זרועות)', 'h_m': 9, 'spacing_px': 185}, 'trees': {'spacing_px': [50, 60], 'both_sides': True},
              'crosswalk_depth_px': 34, 'center': 'קו צהוב כפול (‎#f2c83e, ‏2.2 פיקס׳) משני צדי חציון של 8 פיקס׳', 'lanes_line': 'קו לבן מקווקו (‎#f3f1dc, ‏2 פיקס׳, ‏16 / 15)'},
 'avenue':   {'he': 'שדרה עירונית (מאסף)', 'map': 'collector · מאסף 1+1', 'width_px': 124, 'lanes': 2, 'lane_px': 44, 'median_px': 0, 'sidewalk_px': 20, 'speed_kmh': 50,
              'lamp': {'asset': 'SL-AVE', 'kit': 'lamp_avenue', 'he': 'פנס שדרה (זרוע אחת)', 'h_m': 8, 'spacing_px': 155}, 'trees': {'spacing_px': [50, 60], 'both_sides': True},
              'crosswalk_depth_px': 30, 'center': 'קו צהוב רציף (‎#f0c83c, ‏2.1 פיקס׳)', 'lanes_line': '—'},
 'local':    {'he': 'רחוב מקומי', 'map': 'local · מקומי 1+1 (וגם החיבור הזמני)', 'width_px': 96, 'lanes': 2, 'lane_px': 44, 'median_px': 0, 'sidewalk_px': 20, 'speed_kmh': 30,
              'lamp': {'asset': 'SL-RES', 'kit': 'lamp_res', 'he': 'פנס שכונה', 'h_m': 4.5, 'spacing_px': 130}, 'trees': {'spacing_px': None, 'both_sides': False},
              'crosswalk_depth_px': 30, 'center': 'קו מקווקו בהיר (‎#eee9bb, ‏2.1 פיקס׳, ‏14 / 12)', 'lanes_line': '—'},
 'lane':     {'he': 'סמטה (חצר מרוצפת, ללא מוצא)', 'map': '— (מגרש משותף, לא כביש בגרף)', 'width_px': None, 'lanes': None, 'lane_px': None, 'median_px': None, 'sidewalk_px': None, 'speed_kmh': None,
              'lamp': {'asset': 'SL-RES', 'kit': 'lamp_res', 'he': 'פנס שכונה', 'h_m': 4.5, 'spacing_px': 200}, 'trees': {'spacing_px': None, 'both_sides': False},
              'crosswalk_depth_px': None, 'center': '—', 'lanes_line': '—'},
}
for k in KIT:
    L = KIT[k]['lamp']
    if L['spacing_px']: L['min_gap_px'] = max(36, L['spacing_px'] / 2) if k != 'lane' else None
TYPE_SRC = {
 'main': [S('G', "main:{width:SCALE.main,sidewalk:SCALE.mainWalk,lanes:6,median:SCALE.mainMedian,speed:70,label:'עורק ראשי 6 נתיבים'}"), S('G', 'main:254,mainLane:39,mainMedian:20,mainWalk:25')],
 'arterial': [S('G', "arterial:{width:SCALE.arterial,sidewalk:SCALE.sidewalk,lanes:4,median:SCALE.median,speed:70,label:'עורק 4 נתיבים'}"), S('G', 'arterial:196,sidewalk:20,median:8')],
 'avenue': [S('G', "avenue:{width:SCALE.avenue,sidewalk:SCALE.sidewalk,lanes:2,median:0,speed:50,label:'שדרה עירונית'}"), S('G', 'avenue:124')],
 'local': [S('G', "local:{width:SCALE.local,sidewalk:SCALE.sidewalk,lanes:2,median:0,speed:30,label:'רחוב מקומי'}"), S('G', 'local:96')],
 'lane': [S('NJ', 'עם פנס כל 20 מ׳ — בלי ראש סיבוב, כי כל סמטה עד 45 מ׳'), S('ZB3', '["SL-RES", 1396, 2054, 22]')],
}
LAMP_SRC = [S('G', "spacing=/^TC-(E6|D6|C6)-/.test(e.globalRoadId)?320:(e.cls==='arterial'||e.cls==='main')?185:e.cls==='avenue'?155:130,asset=(e.cls==='arterial'||e.cls==='main')?'SL-AV2':e.cls==='avenue'?'SL-AVE':'SL-RES'"),
            S('G', "'SL-RES':['lamp_res',1,'L'],'SL-AVE':['lamp_avenue',1,'L']"), S('G', "'SL-AV2':['lamp_double',1,'L']"), S('OW', 'אותו פנס ואותו מרחק בין הפנסים.')]
LAMP_HALF_SRC = [S('P367', "a lamp p365 moves or adds keeps half the street's spacing from every other lamp"), S('G', 'return Math.max(36,sp/2)')]
TREE_SRC = [S('OW', 'עץ כל 5–6 מ׳ בשני צדי השדרה.')]
WALK_SRC = [S('OW', 'אותה אבן שפה, ומדרכה ברוחב קבוע לכל סוג דרך.'), S('G', "strokeEdge(e,roadType(e).sidewalk*2+8,'rgba(0,0,0,.32)')"),
            S('G', "CONTINUITY_PROTOCOL={version:2,laneWidth:SCALE.lane,surface:'asphalt-v1',sidewalk:'paver-v1',markings:'world-phase-v2'}")]
kit_rules = []
for k, v in KIT.items():
    n = len(kit_rules) + 1
    if k != 'lane':
        kit_rules.append(R('K-%02d' % n, v['he'] + ' — החתך', {'רוחב': v['width_px'], 'נתיבים': v['lanes'], 'נתיב': v['lane_px'], 'חציון': v['median_px'], 'מדרכה': v['sidewalk_px']},
                           'פיקסלים', TYPE_SRC[k], check='C-05', conflict='ס-2'))
    kit_rules.append(R('K-%02d' % (len(kit_rules) + 1), v['he'] + ' — הפנס והמרחק', {'פנס': v['lamp']['asset'], 'בערכת ה-3/4': v['lamp']['kit'], 'מרחק מרבי': v['lamp']['spacing_px'], 'מרחק מזערי': v['lamp'].get('min_gap_px')},
                       'פיקסלים', (LAMP_SRC + LAMP_HALF_SRC) if k != 'lane' else TYPE_SRC['lane'], check='C-01 · C-02 · C-03', conflict='ס-1'))
    if v['trees']['spacing_px']:
        kit_rules.append(R('K-%02d' % (len(kit_rules) + 1), v['he'] + ' — עצי הרחוב', {'מרחק': v['trees']['spacing_px'], 'בשני הצדדים': True}, 'פיקסלים', TREE_SRC, check='C-04', conflict='ס-3'))
kit_rules.append(R('K-%02d' % (len(kit_rules) + 1), 'רחוב מקומי — עצי הרחוב', 'לא נקבע מרחק; נספר ומוצג', '—', [S('B3', 'עצי רחוב בכל רחוב'), S('IN', 'עץ כל 48–64 px לאורך כל מדרכה ראשית')], conflict='ס-3'))
kit_rules.append(R('K-%02d' % (len(kit_rules) + 1), 'אבן השפה והמדרכה — אחת לכל העיר', 'שפת הכביש, קו שוליים לבן 5 פיקס׳ פנימה, ריצוף מדרכה אחד (‎paver-v1) וקו צל של 4 פיקס׳ בקצה החיצוני', '—', WALK_SRC + [S('G', "off=t.width/2-5;edgeLine(e,off,'rgba(245,245,235,.58)',1.3)")], check='C-05'))
kit_rules.append(R('K-%02d' % (len(kit_rules) + 1), 'אין פנס, עמוד או עץ ב-±40 פיקס׳ מציר של כניסה', 40, 'פיקסלים', [S('IN', 'אין פנס, עמוד או עץ ב-±40 px מציר כניסה (K‑187)'), S('G', 'var K187={R:40,')], check='C-04 · C-15'))
group('kit', 'ערכת הרחוב לכל סוג דרך', kit_rules)

group('marks', 'סימון הכבישים — אחד לכל העיר', [
 R('M-01', 'קו האמצע וקווי הנתיבים לפי סוג הדרך', {KIT[k]['he']: KIT[k]['center'] for k in ('main', 'arterial', 'avenue', 'local')}, '—',
   [S('G', "edgeLine(e,-SCALE.median/2,'#f2c83e',2.2)"), S('G', "edgeLine(e,0,e.cls==='avenue'?'#f0c83c':'#eee9bb',2.1,e.cls==='local'?[14,12]:[])"), S('G', "edgeLine(e,-(SCALE.median/2+SCALE.lane),'#f3f1dc',2,[16,15])")], check='C-13'),
 R('M-02', 'קו שוליים', '1.3 פיקס׳, לבן שקוף, 5 פיקס׳ מהשפה', '—', [S('G', "off=t.width/2-5;edgeLine(e,off,'rgba(245,245,235,.58)',1.3)")]),
 R('M-03', 'מעבר חצייה', {'פס': 5, 'רווח': 6, 'עומק בעורק ובעורק ראשי': 34, 'עומק בשאר': 30, 'שוליים': 8}, 'פיקסלים',
   [S('G', "depth=(e.cls==='arterial'||e.cls==='main')?34:30,stripe=5,gap=6"), S('G', "ctx.fillStyle='rgba(248,248,241,.92)'")], check='C-13'),
 R('M-03א', 'המקום של מעבר חצייה — רק בצומת', {'איפה': 'רק בצומת (3 זרועות לפחות), צמוד לקו העצירה — עד 1 מ׳ (10 פיקס׳) אחריו; המספר — לאישור הבעלים',
     'אין': 'אין מעבר באמצע בלוק, ליד תחנה או בכניסה למגרש; אין "מרחק מרבי בין מעברים" ואין "מעבר ליד כל תחנה" (R-68 תוקן)',
     'ברמזור': 'מעבר בכל זרוע; הולכי הרגל עם הירוק של הרכבים שנוסעים לידם באותו כיוון (בלי שלב "אדום לכולם"), ורכב שפונה נותן להם זכות קדימה',
     'בלי רמזור': 'מעבר בלי רמזור, הרכב נותן זכות קדימה',
     'ההולכים': 'כל מסלול הליכה עובר במדרכה עד המעבר בצומת; ליד תחנה — הנוסעים הולכים לצומת'}, '—',
   [S('O76', 'מעבר חצייה רק בצומת, צמוד לקו העצירה. אין מעבר באמצע בלוק, ליד תחנה או בכניסה למגרש.'), S('O76', 'מעבר חצייה רחוק מצומת הוא כישלון'), S('RC', 'מעבר חצייה — רק בצומת, צמוד לקו העצירה, ומסונכרן עם הרמזור של הצומת'),
    S('O76', 'שני הסעיפים האלה מבוטלים, ו-R-68 תוקן בדף הביקורת'),
    S('R1051', 'הולכי הרגל מקבלים ירוק יחד עם הירוק של הרכבים שנוסעים לידם באותו כיוון. רכב שפונה נותן להם זכות קדימה.'),
    S('R1051', 'בצומת בלי רמזור יש מעבר בלי רמזור, והרכב נותן זכות קדימה. זו ברירת מחדל, לאישור הבעלים.'),
    S('R1051', 'כל מסלול הליכה עובר במדרכה עד המעבר בצומת.')], check='C-29'),
 R('M-04', 'קו עצירה בכל גישה לרמזור; קו "תן זכות קדימה" מקווקו בזרוע המשנית', {'עובי': 3, 'מקווקו': [4, 3]}, 'פיקסלים',
   [S('G', "var G7_SL={on:true,w:3,col:'rgba(246,246,238,.92)',minor:'yield',dash:[4,3]"), S('CP', 'כל השאר → עצור/תן זכות קדימה')], check='C-13'),
 R('M-05', 'חץ ונתיב שמאלה בכל גישה לרמזור', 'חץ צבוע על הנתיב בכל גישה לרמזור', '—', [S('CP', 'ברמזור — נתיב שמאלה וחץ בכל גישה'), S('OW', 'סימון כבישים אחד: קווי נתיב, חצים, קווי עצירה ומעברי חצייה באותו עיצוב בכל העיר.')], check='C-13'),
])

group('signs', 'תמרורים ושלטי רחוב — משפחה אחת, בעברית', [
 R('T-01', 'משפחת התמרורים', ['RF-STP (עצור · תן זכות · אין כניסה · חד-סטרי)', 'RF-SPD (30 · 50 · 70 · 90)', 'RF-DIR', 'RF-PRK', 'RF-BUS', 'RF-STR'], '—',
   [S('G', "const RF=[['RF-STP','Regulatory Sign',['Stop','Yield','No Entry','One Way']"), S('G', "'RF-STP':[['sign_stop','sign_yield','sign_noentry'],1,'S'],'RF-SPD':['sign_speed',1,'S']"), S('OW', 'משפחה אחת של תמרורים ושלטי רחוב, בעברית.')], check='C-11'),
 R('T-02', 'תמרור עצור או תן זכות בכל זרוע משנית של צומת בלי רמזור', 'RF-STP ליד כל קו "תן זכות"', '—', [S('CP', 'כל השאר → עצור/תן זכות קדימה'), S('G', "minor:'yield'")], check='C-11'),
 R('T-03', 'שם הרחוב על הכביש', {'גופן': 13, 'כל': 720, 'קטע מזערי': 200}, 'פיקסלים', [S('G', 'G7_RN={px:13,minLen:200,gap:720'), S('IN', 'טקסט: עברית, בלי קודים, לפחות 11 px על המסך')], check='C-12'),
])

group('stop', 'תחנת אוטובוס — עיצוב אחד', [
 R('B-01', 'המפרץ', {'כניסה': 40, 'עצירה': 150, 'יציאה': 40, 'עומק': 30}, 'פיקסלים', [S('G', 'BUS_BAY={entry:40,stop:150,exit:40,depth:30}'), S('CP', '"bay": {"entry": 40, "stop": 150, "exit": 40, "depth": 30}')], check='C-14', conflict='ס-8'),
 R('B-02', 'מפרץ של 15 מ׳ לפחות ו-20 מ׳ לפחות מצומת', {'מפרץ': 150, 'מצומת': 200}, 'פיקסלים', [S('RC', 'תחנה: מפרץ של 15 מ׳ לפחות, 20 מ׳ לפחות מצומת')], check='C-14', conflict='ס-7'),
 R('B-03', 'הסככה, השלט והספסל', {'סככה': 'PR-35 · bus_shelter, בהגדלה 0.76', 'שלט': 'RF-BUS · sign_bus, בהגדלה 25/48', 'משטח ההמתנה': '14 מ׳ (66 + 74 פיקס׳)'}, '—',
   [S('G', 'const BUS_STOP_SHELTER_SCALE=.76;'), S('G', 'const BUS_STOP_SIGN_SCALE=25/48;'), S('G', "'PR-35':['bus_shelter',0,'F',1]"), S('G', 'BUS_SITE_BACK=66,BUS_SITE_FWD=74'), S('OW', 'תחנת אוטובוס: אותה סככה, אותו שלט, ספסל ומפרץ.')], check='C-14'),
])

group('park', 'חניון וכניסה למגרש', [
 R('P-01', 'קווי החניה וגודל החניה', [28, 56], 'פיקסלים', [S('NJ', 'גודל החניה: 2.8 × 5.6 מ׳'), S('OW', 'חניון: אותם קווים, חניות נכים וחשמל בעיצוב האחיד, ותאורה.')], check='C-07', conflict='ס-6'),
 R('P-02', 'חניות נכים וחשמל בכל חניון של 10 ומעלה', {'נכים': '2%', 'חשמל': '5%', 'לפחות': '1 + 1'}, '—',
   [S('NJ', 'בכל חניון של 10 ומעלה 2% לנכים ו-5% לחשמל (בעיגול כלפי מעלה), לפחות 1 + 1'), S('G', 'needA=n>=10?Math.max(1,Math.ceil(n*.02)):0,needE=n>=10?Math.max(1,Math.ceil(n*.05)):0')], check='C-08', conflict='ס-11'),
 R('P-03', 'העיצוב האחיד של חניית נכים וחשמל', 'נכים: מקום כחול, מסגרת לבנה, סמל ותמרור; חשמל: מקום ירוק, סמל, עמדת טעינה עם כבל ותמרור', '—',
   [S('NJ', 'נכים: מקום כחול, מסגרת לבנה, סמל ותמרור; חשמל: מקום ירוק, סמל, עמדת טעינה עם כבל ותמרור'), S('RC', 'חניות נכים וחשמל: צייר אחד לכל העיר')], check='C-08'),
 R('P-04', 'תאורה בחניון — פנס עד 25 מ׳ מכל חניה', 250, 'פיקסלים', [S('G', 'פנס בטווח 25 מ׳ מכל דלת של העסקים ב-D3'), S('OW', 'חניון: אותם קווים, חניות נכים וחשמל בעיצוב האחיד, ותאורה.')], check='C-09'),
 R('P-05', 'פנס עד 25 מ׳ מכל דלת', 250, 'פיקסלים', [S('OW', 'פנס עד 25 מ׳ מכל דלת.')], check='C-10'),
 R('P-06', 'כניסה למגרש: הנמכת שפה ובלי מדרכה באמצע', 'הנמכה בכל כניסה', '—', [S('OW', 'כניסה למגרש: הנמכת שפה, ובלי מדרכה באמצע.'), S('RC', 'בלי מדרכה באמצע חיבור. הנמכה בכל כניסה.')], check='C-15'),
])

group('edge', 'גבולות', [
 R('E-01', 'גדר חיה באותו סגנון בבתים ובווילות — בגבול של כל מגרש', 'גדר חיה בכל מגרש של בית או וילה', '—', [S('OW', 'גדר חיה באותו סגנון בבתים.'), S('C3', 'גדר חיה בכל גבול מגרש')], check='C-16'),
 R('E-02', 'חומה בתעשייה', 'חומה בגבול של חצרות התעשייה', '—', [S('OW', 'חומה בתעשייה.'), S('D4', 'גדר אבטחה')], check='C-16', conflict='ס-12'),
 R('E-03', 'חיץ עצים בין תעשייה למגורים', {'C4 מול C3': '20 עצים לפחות', 'D4 מול הווילות של D3': '20 עצים לפחות'}, '—',
   [S('OW', 'חיץ עצים בין תעשייה למגורים.'), S('C4', 'חיץ ירוק מול המגורים — שורת עצים או גדר חיה לאורך הגבול: 20–40 עצים.'), S('D4', 'חיץ ירוק — 20–40 עצים (החוזה: 38)')], check='C-16', conflict='ס-13'),
])

group('height', 'גובה לפי שימוש', [
 R('H-01', 'בניין דירות', 4, 'קומות לכל היותר', [S('OW', 'דירות עד 4 קומות.'), S('NJ', 'בניין דירות עד 4 קומות')], check='C-18', conflict='ס-9'),
 R('H-02', 'בית ספר וסופר', 2, 'קומות לכל היותר', [S('OW', 'בית ספר וסופר עד 2.'), S('NJ', 'בית ספר וסופר עד 2 קומות')], check='C-18'),
 R('H-03', 'בית פרטי ווילה', 2, 'קומות', [S('NJ', '15 בתים פרטיים בשתי קומות'), S('UJ', 'טביעה 150×108 על מגרש 245×215')], check='C-18'),
])

group('std', 'תקן אחד לכל העיר', [
 R('N-01', 'מנחת לפי המסוק שנוחת בו', {'קל (R44)': {'מנחת': 10, 'טבעת': 17.5}, 'H130': {'מנחת': 11, 'טבעת': 19}, 'AW139': {'מנחת': 14, 'טבעת': 25}}, 'מ׳ (קוטר)',
   [S('RC', 'מנחת: בקוטר הרוטור של המסוק שנוחת בו (קל 10 מ׳, ‏H130 ‏11 מ׳, ‏AW139 ‏14 מ׳), טבעת מקווקוות פי 1.5 מאורך המסוק'), S('NJ', 'פי 1.5 מאורך המסוק — 17.5, ‏19 ו-25 מ׳')], check='C-23', conflict='ס-14'),
 R('N-02', 'מסוק אמיתי על כל מנחת שתוכנן לו', 'מסוק על כל מנחת', '—', [S('RC', 'ומסוק אמיתי על כל מנחת שתוכנן לו (R-61)')], check='C-23'),
 R('N-03', 'תאי החירום לפי תנאי הקבלה', {'A4 — תחנת הכיבוי': 5, 'A4 — בסיס האמבולנסים': 5, 'C4 — תחנת כיבוי 2': 3}, 'תאים',
   [S('A4', '5 חניות כיבוי — 3 כבאיות ו-2 פנויות'), S('A4', '5 חניות צרות — 4 אמבולנסים (65 px) ואחת פנויה'), S('UT', 'C4 — מגרש כ-30×20 מ׳: 3 תאים (2 כבאיות ומכלית קצף)')], check='C-24', conflict='ס-15'),
 R('N-04', 'מגרשי ספורט בגודל אמיתי', {'כדורגל': [85, 55], 'קט-רגל': [40, 20], 'כדורסל': [28, 15], 'טניס': [23.77, 10.97]}, 'מ׳',
   [S('OW', 'מגרשי ספורט בגודל אמיתי.'), S('A34', '# 85 × 55 מ׳'), S('A34', '# 40 × 20 מ׳'), S('A34', '# 28 × 15 מ׳ (FIBA)'), S('A34', '# 23.77 × 10.97 מ׳')], check='C-25'),
 R('N-05', 'תאורת לילה — אותו צבע ואותה עוצמה, ואלומה על הקרקע לכל פנס', {'ראש הפנס': '#fff3c4 בשקיפות 0.92', 'הילה': 'אותו צבע (255,243,196) בשקיפות 0.45', 'אלומה על הקרקע': 'אותו צבע (255,243,196) בשקיפות 0.45, בכל פנס'}, '—',   # 2.11 (p493, המבקר על S7F197): צבע אחד ועוצמה אחת, כמו שכתב הבעלים
   [S('OW', 'תאורת לילה אחידה: אותו צבע אור ואותה עוצמה.'), S('OW', 'ולכל פנס יש אלומת אור על הקרקע'), S('G', "lc=N?'#fff3c4':'#cfd8de'"), S('G', "g.addColorStop(0,'rgba(255,243,196,.45)')")], check='C-26', conflict='ס-16'),
 R('N-06', 'אנשים ממשפחה אחת, רכבים באותו קנה מידה', 'טבלת הגדלים של המשחק (D‑238)', '—', [S('OW', 'מה שזז: כל האנשים מאותה משפחה, וכל הרכבים באותו קנה מידה.'), S('G', 'the sizes table in the code (D‑238)')], check='C-27'),
])

group('design', 'רמת העיצוב והמגוון', [
 R('D-01', 'לפחות 3 דגמים או גוונים לכל סוג מבנה, ואף פעם לא שני מבנים זהים זה ליד זה', 3, 'דגמים', [S('OW', 'מגוון: לפחות 3 דגמים או גוונים לכל סוג מבנה, ואף פעם לא שני מבנים זהים אחד ליד השני.')], check='C-21'),
 R('D-02', 'מתקן אופניים ליד כל בניין ציבורי או מסחרי (עד 25 מ׳ מהדלת)', 250, 'פיקסלים', [S('OW', 'מתקן אופניים ליד בניין ציבורי או מסחרי.'), S('G', "'PR-29':['bike_rack',0,'F',1]")], check='C-22'),
 R('D-03', 'פרטי המבנה', 'חלונות עם מסגרות, דלת עם סוכך, מרפסות ומזגנים; על הגג מעקה, לוחות סולאריים ודוד; שלט עם לוגו; שביל מרוצף, ערוגות, עצים ומסתור לפחים', '—',
   [S('OW', 'חלונות עם מסגרות, דלת עם סוכך, מרפסות ומזגנים.'), S('OW', 'על הגג: מעקה, לוחות סולאריים ודוד.'), S('OW', 'שביל מרוצף מהמדרכה לדלת, ערוגות, עצים ומסתור לפחים.')],
   note='נבדק בעין בגיליון המבנים, לא בבדיקה הזאת'),
 R('D-04', 'פלטה לכל רובע — צבעים, סוגי גגות וחומרים', 'ראו את הפלטות', '—', [S('OW', 'פלטה לכל רובע: צבעים, סוגי גגות וחומרים. יש מגוון, אבל בתוך הפלטה.')], check='C-17', conflict='ס-17'),
])

group('seam', 'תפרים בין אזורים', [
 R('Z-01', 'הכביש, המדרכה, שורת העצים ושורת הפנסים ממשיכים בלי קפיצה', {'ציר': 2, 'שורה': 4}, 'פיקסלים (סטייה מרבית)', [S('OW', 'תפרים בין אזורים: הכביש, המדרכה והשורה של העצים והפנסים ממשיכים בלי קפיצה.'), S('G', "laneWidth:SCALE.lane,surface:'asphalt-v1',sidewalk:'paver-v1'")], check='C-28'),
])

CONFLICTS = [
 {'id': 'ס-1', 'item': 'המרחק בין הפנסים לפי סוג הדרך', 'default': 'המחולל של המשחק: עורק ועורק ראשי 185, שדרה 155, רחוב 130 פיקס׳ (וסמטה 200); לכל היותר המרחק הזה, ולפחות חצי ממנו',
  'options': [{'he': 'המשחק — 185 / 155 / 130 פיקס׳', 'src': [LAMP_SRC[0]]}, {'he': 'תנאי הקבלה — עורק 120, שדרה 140, רחוב 180 פיקס׳', 'src': [S('B3', 'פנסים לפי הכלל: עורק כל 120, שדרה כל 140, רחוב כל 180 px'), S('IN', 'פנס כל 120 / 140 / 180 px')]},
              {'he': 'הסמטאות — פנס כל 20 מ׳', 'src': TYPE_SRC['lane']}]},
 {'id': 'ס-2', 'item': 'רוחב המדרכה לפי סוג הדרך', 'default': 'המשחק: 20 פיקס׳ (2 מ׳) בכל סוג, ו-25 פיקס׳ (2.5 מ׳) בעורק הראשי — בלי רצועת דשא',
  'options': [{'he': 'המשחק — 20 / 25 פיקס׳', 'src': [S('G', 'sidewalk:20'), S('G', 'mainWalk:25')]}, {'he': 'המפה — עורק ועורק ראשי 2.5 מ׳, מאסף 2.0, מקומי 1.5', 'src': [S('CP', '"walk_m": 2.5'), S('CP', '"walk_m": 1.5')]},
              {'he': 'תנאי הקבלה — עורק: מדרכה 40 + דשא 20; שדרה: 36; רחוב: 30 פיקס׳', 'src': [S('B3', 'מדרכה 40 + דשא 20 בשני הצדדים'), S('B3', 'שדרה 1+1, מדרכה 36'), S('B3', 'רחובות מקומיים (מדרכה 30)')]}]},
 {'id': 'ס-3', 'item': 'המרחק בין עצי הרחוב', 'default': 'הבעלים 07:00: עץ כל 50–60 פיקס׳ בשני הצדדים של כל עורק ראשי, עורק ושדרה, בכל רובע; ברחוב מקומי — לא נקבע מרחק (נספר בלבד)',
  'options': [{'he': 'הבעלים — כל 5–6 מ׳, בשני צדי השדרה', 'src': TREE_SRC}, {'he': 'המבוא — 48–64 פיקס׳ במרכז ובמגורים, 160 בשדרות של שאר העיר', 'src': [S('IN', 'עץ כל 48–64 px לאורך כל מדרכה ראשית'), S('IN', 'בשדרה עץ כל 160')]},
              {'he': 'A4 — עץ כל 160 פיקס׳ לאורך שדרת הספורט', 'src': [S('A4', 'עץ כל 160 px לאורך שדרת הספורט')]}, {'he': 'B3, ‏C3, ‏D3 — כל 48–64 פיקס׳ בשני הצדדים', 'src': [S('C3', 'עץ כל 48–64 px בשני הצדדים')]}]},
 {'id': 'ס-4', 'item': 'מה נחשב "שדרה" לכלל העצים — לפי סוג הדרך או לפי השם', 'default': 'לפי סוג הדרך (עורק ראשי, עורק ושדרה); "שדרת הקריה" ב-A3 היא רחוב מקומי — לא; "רחוב התעשייה" היא שדרה — כן',
  'options': [{'he': 'לפי הסוג בגרף', 'src': [S('OW', 'ערכת רחוב לכל סוג דרך:')]}, {'he': 'לפי השם', 'src': [S('CP', "שדרת הקריה") if False else S('G', 'שדרת הקריה — A3')]}]},
 {'id': 'ס-5', 'item': 'רוחב הנתיב והרוחב של הדרך', 'default': 'הרשת של היום: נתיב 44 פיקס׳ ורוחב לפי המשחק (96 / 124 / 196); העורק הראשי כבר במפה (נתיב 39, רוחב 254); נתיב של 3.9 מ׳ רק בדרך שנבנית מחדש לפי 7ב',
  'options': [{'he': 'המשחק — 44 פיקס׳', 'src': [S('G', 'const SCALE={lane:44,')]}, {'he': 'המפה — 3.9 מ׳', 'src': [S('CP', '"lane_m": 3.9')]}, {'he': 'הכלל של המפה', 'src': [S('CP', 'נתיב של 3.9 מ׳ (אפשרות ב׳, ×1.125) רק בדרכים שנבנות מחדש לפי 7ב')]}]},
 {'id': 'ס-6', 'item': 'גודל החניה', 'default': '28 × 56 פיקס׳ (2.8 × 5.6 מ׳) — הבעלים 07:00 ו-D‑327, כמו בכל העיר מ-S7F186',
  'options': [{'he': '2.8 × 5.6 מ׳', 'src': [S('OW', 'חניה 2.8 × 5.6 מ׳'), S('NJ', 'גודל החניה: 2.8 × 5.6 מ׳')]}, {'he': '62 × 32 פיקס׳', 'src': [S('IN', 'חניות: 62 × 32')]}, {'he': '3.8 × 7.6 מ׳', 'src': [S('NJ', 'וחניה אחת בגודל 3.8 × 7.6 מ׳')]}]},
 {'id': 'ס-7', 'item': 'המרחק של תחנה מצומת', 'default': 'כלל 10: 20 מ׳ (200 פיקס׳) לפחות מכל צומת; איפה שאין מקום — D‑332 עם סיבה כתובה (כמו בגיליון של C4 · D4)',
  'options': [{'he': 'כלל 10 — 20 מ׳ מכל צומת', 'src': [S('RC', '20 מ׳ לפחות מצומת')]}, {'he': 'D‑332 — 20 מ׳ לפני הצומת שלפנים ו-10 מ׳ אחרי הצומת שמאחור', 'src': [S('NJ', '20 מ׳ לפני הצומת שלפנים, 10 מ׳ אחרי הצומת שמאחור')]}]},
 {'id': 'ס-8', 'item': 'אורך המפרץ והשפה הישרה של התחנה', 'default': 'המפרץ של המשחק והמפה: 150 פיקס׳ עצירה + 40 + 40, עומק 30 — עומד בכלל 10',
  'options': [{'he': 'המשחק והמפה — 40 + 150 + 40, עומק 30', 'src': [S('G', 'BUS_BAY={entry:40,stop:150,exit:40,depth:30}')]}, {'he': 'B3 ו-C3 — 200 פיקס׳ שפה ישרה, 60 מהצומת', 'src': [S('B3', 'תחנת קו 1 בשדרה — 200 px שפה ישרה, 60 px מהצומת')]},
              {'he': 'D3 — מפרץ של 366 × 40 בקטע של 486 לפחות', 'src': [S('D3', 'מפרץ של 366 × 40 מחוץ לנתיב, בקטע של 486 px לפחות')]}]},
 {'id': 'ס-9', 'item': 'גובה בניין דירות', 'default': 'עד 4 קומות (הבעלים 07:00, ‏D‑319)',
  'options': [{'he': 'עד 4 קומות', 'src': [S('OW', 'דירות עד 4 קומות.'), S('NJ', 'בניין דירות עד 4 קומות')]}, {'he': '5–6 קומות', 'src': [S('UJ', '30–40 × 12–15 מ׳, ‏5–6 קומות')]}]},
 {'id': 'ס-10', 'item': 'גובה קומה במבנה של חלל אחד (חנות, מחסן, מפעל, מוסך, תחנת כיבוי)', 'default': 'הכלל של 3–3.3 מ׳ חל על מבנה עם קומות (מגורים, משרד, בית ספר, מרפאה); מבנה של חלל אחד נבדק לפי הגובה שלו בלבד',
  'options': [{'he': 'הבעלים — קומה 3–3.3 מ׳ בכל מבנה', 'src': [S('OW', 'קומה 3–3.3 מ׳')]}, {'he': 'המשחק — חנות, מחסן ומפעל בחלל אחד של 4.2–9.5 מ׳', 'src': [S('G', "def('WHD4', whType({ W: 48, D: 12, H: 8,"), S('G', "def('HWSTORE', shopType({ W: 20, D: 21, H: 7.2,")]}]},
 {'id': 'ס-11', 'item': 'אחוז חניות הנכים והחשמל ליד שירותים', 'default': 'D‑333 בכל חניון: 2% נכים ו-5% חשמל, לפחות 1 + 1',
  'options': [{'he': 'D‑333 — 2% / 5%', 'src': [S('NJ', 'בכל חניון של 10 ומעלה 2% לנכים ו-5% לחשמל')]}, {'he': 'המבוא — 8% / 6% ליד שירותים', 'src': [S('IN', 'כל חניון — 5% טעינה ו-2% נכים (8% / 6% ליד שירותים)')]},
              {'he': 'B4 — המרפאה: 8% טעינה ו-6% נכים', 'src': [S('B4', 'המרפאה מוגדרת יעד מוגדל: 8% טעינה ו-6% נכים בחניון שלה')]}]},
 {'id': 'ס-12', 'item': 'הגבול של התעשייה — חומה או גדר', 'default': 'חומה (הבעלים 07:00) בגבול החיצוני של חצרות התעשייה; גדר האבטחה של D4 נשארת סביב החצר',
  'options': [{'he': 'חומה', 'src': [S('OW', 'חומה בתעשייה.')]}, {'he': 'גדר אבטחה', 'src': [S('D4', 'גדר אבטחה')]}]},
 {'id': 'ס-13', 'item': 'חיץ העצים — כמה ואיפה', 'default': 'C4: לפחות 20 עצים מול C3 (כמו ברירת המחדל ס-8 בגיליון של C4 · D4), בלי חיץ נוסף מול B4; D4: לפחות 20 עצים לאורך הגבול הצפוני מול הווילות של D3',
  'options': [{'he': 'C4 — 20–40 עצים', 'src': [S('C4', 'חיץ ירוק מול המגורים — שורת עצים או גדר חיה לאורך הגבול: 20–40 עצים.')]}, {'he': 'הגיליון של C4 · D4', 'src': [S('REQ', '20 עצים לפחות על C4-TREES מול C3')]},
              {'he': 'D4 — 20–40 עצים (החוזה: 38)', 'src': [S('D4', 'חיץ ירוק — 20–40 עצים (החוזה: 38)')]}]},
 {'id': 'ס-14', 'item': 'גודל המנחת', 'default': 'הטבלה של כלל 12 (קל 10, ‏H130 ‏11, ‏AW139 ‏14 מ׳; טבעת פי 1.5 מאורך המסוק)',
  'options': [{'he': 'כלל 12 ו-D‑353', 'src': [S('RC', 'קל 10 מ׳, ‏H130 ‏11 מ׳, ‏AW139 ‏14 מ׳')]}, {'he': 'המפה — 18 מ׳ ומעלה; D‑267 — ‏15 מ׳ למסוק המנהלים', 'src': [S('NJ', 'במפה — 18 מ׳ ומעלה'), S('NJ', 'להגדיל את אחד המנחתים, כך שיתאים למסוק של 15 מ׳')]}]},
 {'id': 'ס-15', 'item': 'תחנת הכיבוי של A4 — 5 תאים', 'default': 'D‑354: ‏5 תאים — 3 כבאיות, מכלית קצף ותא פנוי',
  'options': [{'he': 'A4 — 3 כבאיות ו-2 פנויות', 'src': [S('A4', '5 חניות כיבוי — 3 כבאיות ו-2 פנויות')]}, {'he': 'טבלת השימושים — 3 כבאיות, מכלית קצף ותא פנוי', 'src': [S('UT', '5 תאים: 3 כבאיות, מכלית קצף ותא פנוי')]}]},
 {'id': 'ס-16', 'item': 'צבע האור בלילה', 'default': 'נסגר (2.11, p482 ו-p493): צבע אחד ‎#fff3c4 (255,243,196) בכל פנס — הראש בשקיפות 0.92, כל הילה וכל אלומה על הקרקע בשקיפות 0.45, כמו שכתב הבעלים: "אותו צבע אור ואותה עוצמה"',
  'options': [{'he': 'ראש הפנס', 'src': [S('G', "lc=N?'#fff3c4':'#cfd8de'")]}, {'he': 'ערכת ה-3/4 — הראש', 'src': [S('G', "c.fillStyle = lt ? 'rgba(255,243,196,.92)'")]},
              {'he': 'ההילה של הפנס ושל פנס בחצר', 'src': [S('G', "'rgba(255,243,196,.45)', 'rgba(255,243,196,0)'")]},
              {'he': 'האלומה על הקרקע', 'src': [S('G', "g.addColorStop(0,'rgba(255,243,196,.45)')")]}]},
 {'id': 'ס-17', 'item': 'הרובע של A3 ושל D3 (לפלטה)', 'default': 'לפי תנאי הקבלה: D3 ברובע המרכז; A3 עם A4 ברובע המערב (אותו בלוק — קריית הספורט)',
  'options': [{'he': 'תנאי הקבלה — D3: המרכז; A4: המערב', 'src': [S('D3', 'רובע: המרכז'), S('A4', 'רובע: המערב')]}, {'he': 'המשחק — D3 וילות, A3 מגורים', 'src': [S('G', "['D3',3,2,'villa','וילות + רכב']"), S('G', "['A3',0,2,'res','ספורט צפון']")]},
              {'he': 'המפה — A3 ו-A4 בבלוק אחד', 'src': [S('CP', 'קריית הספורט, הכבאות וה-EMS')]}]},
]

CHECKS = [
 ('C-01', 'הפנס לפי סוג הדרך', 'כל פנס על המדרכה של הקטע מהסוג של הערכה'),
 ('C-02', 'המרחק המרבי בין פנסים', 'הפער הגדול בין שני פנסים סמוכים באותו צד, וגם מהצומת לפנס הראשון'),
 ('C-03', 'המרחק המזערי בין פנסים', 'אין שני פנסים באותו צד קרובים מחצי המרחק'),
 ('C-04', 'עצי השדרה', 'בכל צד של עורק ראשי, עורק ושדרה: הפער בין עצים 50–60, אחרי שמורידים כניסות, מעברים ומפרצים'),
 ('C-05', 'החתך והמדרכה', 'הרוחב, מספר הנתיבים והמדרכה של כל קטע — כמו בערכה של הסוג'),
 ('C-07', 'מידות החניות', 'כל חניה של מכונית: 28 × 56'),
 ('C-08', 'חניות נכים וחשמל', 'בכל חניון של 10 ומעלה: לפחות 2% ו-5%, ולפחות 1 + 1'),
 ('C-09', 'תאורה בחניון', 'כל חניה עד 250 פיקס׳ מפנס'),
 ('C-10', 'פנס ליד כל דלת', 'כל כניסה של מבנה עד 250 פיקס׳ מפנס'),
 ('C-11', 'תמרורים', 'משפחה אחת; תמרור עצור או תן זכות בכל קו "תן זכות"'),
 ('C-12', 'שמות הרחובות', 'עברית בלבד, בלי קוד של אזור'),
 ('C-13', 'סימון', 'קו עצירה בכל גישה לרמזור, קו "תן זכות" בזרוע משנית, חץ בכל גישה לרמזור'),
 ('C-14', 'תחנות', 'מפרץ, ערכה אחידה ו-20 מ׳ לפחות מצומת'),
 ('C-15', 'כניסות', 'כל כניסה למגרש — הנמכה'),
 ('C-16', 'גבולות', 'גדר חיה בכל מגרש מגורים; חומה בתעשייה; חיץ עצים'),
 ('C-17', 'הפלטה', 'צבע הקיר, צבע הגג, החומר וסוג הגג — בתוך הפלטה של הרובע'),
 ('C-18', 'גובה לפי שימוש', 'מספר הקומות לפי השימוש'),
 ('C-19', 'גובה קומה', '3–3.3 מ׳ בכל קומה'),
 ('C-20', 'הדלת', 'כנף של 1 × 2.1 מ׳ (5% סטייה)'),
 ('C-21', 'מגוון', 'לפחות 3 דגמים לכל סוג מבנה; אין שני מבנים זהים זה ליד זה'),
 ('C-22', 'מתקן אופניים', 'ליד כל בניין ציבורי או מסחרי, עד 250 פיקס׳ מהדלת'),
 ('C-23', 'מנחתים', 'קוטר המנחת והטבעת לפי המסוק, ומסוק על המנחת'),
 ('C-24', 'תאי חירום', 'מספר התאים לפי תנאי הקבלה'),
 ('C-25', 'מגרשי ספורט', 'הגודל של המגרש כמו בגודל האמיתי'),
 ('C-26', 'תאורת לילה', 'צבע אחד לכל הפנסים, ואלומה על הקרקע'),
 ('C-27', 'אנשים ורכבים', 'כל רכב ואדם באזור — בגודל הטבלה'),
 ('C-29', 'מעבר חצייה רק בצומת', 'כל מעבר (עם רמזור ובלי) — בצומת של 3 זרועות לפחות, ולא יותר מ-1 מ׳ אחרי קו העצירה (R-76)'),
 ('C-28', 'תפרים', 'סוג, רוחב וציר של הכביש, המדרכה, ושורות הפנסים והעצים — בין כל שני אזורים שכנים'),
]

METHOD = {
 'side_line': 'לכל קטע בגרף ולכל צד: הקו של אמצע המדרכה (חצי הרוחב + חצי המדרכה מהציר); הקטע שייך לאזור שבו עובר הקו הזה',
 'junction_band': 'ליד צומת לא מודדים בתוך הרצועה של הדרך החוצה (חצי הרוחב שלה + המדרכה)',
 'lamp_band_px': 6, 'tree_band_px': 40,
 'openings': 'כניסות (±40 של K‑187), מעברי חצייה (העומק + 10 מכל צד) ומפרצי תחנה (66 + 74 + 40 + 40) לא נספרים בפער של העצים',
 'neighbor_gap_px': 150, 'lot_gap_px': 70, 'hedge_near_px': 10, 'buffer_band_px': 100,
 'seam_window': 'פי 1.5 מהמרחק של הסוג מכל צד של התפר',
}

def main():
    pal = palettes()
    src = {}
    for k, (p, he) in SRC.items():
        h, n = sha(p); src[k] = {'file': p, 'he': he, 'sha1': h, 'bytes': n}
    guide = {
     'id': 'city_style', 'title': 'מדריך הסגנון של העיר', 'version': '1.0', 'at': '2.11.2026', 'build': 'S7F193',
     'basis': [S('OW', 'כל אזור לוקח את העיצוב ממקור אחד, "מדריך הסגנון של העיר", ולא מעצב מחדש.'), S('RC', 'הכול ממדריך הסגנון של העיר (קובץ נתונים אחד) ובדיקה אוטומטית מולו — אפס חריגות או חריגה עם סיבה')],
     'sources': src, 'zones_built': ZONES, 'groups': GROUPS, 'kit': KIT,
     'parking': {'stall_px': [28, 56], 'acc_pct': 0.02, 'ev_pct': 0.05, 'min_lot': 10, 'min_each': 1, 'lamp_radius_px': 250, 'door_lamp_radius_px': 250,
                 'not_car_lots': 'BAYS|TRUCK|TAXI|KISS|SHUTTLE|SERVICE|DOCK|TRAILER|INSPECTION|BUS|CARGO|HOLD|LOADING|DISPLAY'},
     'stop': {'bay': {'entry': 40, 'stop': 150, 'exit': 40, 'depth': 30}, 'min_bay_px': 150, 'min_junction_px': 200, 'pad_px': [66, 74],
              'shelter': {'asset': 'PR-35', 'scale': 0.76}, 'sign': {'asset': 'RF-BUS', 'scale': round(25 / 48, 4)}},
     'signs': {'family': ['RF-STP', 'RF-SPD', 'RF-DIR', 'RF-PRK', 'RF-BUS', 'RF-STR', 'RF-BOL', 'RF-GRD', 'RF-JER', 'RF-BAR', 'RF-CON'], 'minor_arm': 'RF-STP', 'near_px': 40,
               'names': {'px': 13, 'gap': 720, 'min_len': 200}},
     'markings': {'stop_line_px': 3, 'yield_dash': [4, 3], 'crosswalk': {'stripe': 5, 'gap': 6, 'depth_major': 34, 'depth': 30, 'margin': 8}, 'arrows_at_signals': True},
     'boundaries': {'hedge_zones': ['B3', 'C3', 'D3'], 'wall_zones': ['C4', 'D4'], 'buffer': {'C4': {'side': 'N', 'min': 20}, 'D4': {'side': 'N', 'min': 20}}},
     'heights': {'apartment_max': 4, 'school_max': 2, 'market_max': 2, 'house_floors': 2, 'floor_m': [3.0, 3.3], 'door_m': [1.0, 2.1], 'tol': 0.05,
                 'kinds_with_floors': ['residential', 'villa', 'school', 'clinic', 'office']},
     'helipads': {'table': {'light': {'pad_m': 10, 'ring_m': 17.5, 'he': 'מסוק קל (R44)'}, 'H130': {'pad_m': 11, 'ring_m': 19, 'he': 'H130'}, 'AW139': {'pad_m': 14, 'ring_m': 25, 'he': 'AW139'}},
                  'pads': [{'zone': 'A4', 'id': 'A4-HELI', 'path': 'A34D.heli', 'r': 'r', 'safe': 'safe', 'heli': 'AW139', 'probe': ['var Hc = D.heli;', 3000, 'AC-HL-0'], 'why': [S('NJ', 'היום — ב-A4 מנחת של 20 מ׳ בלי מסוק (לפי D‑149 — מסוק רפואי ומסוק כיבוי)')]},
                           {'zone': 'C3', 'id': 'C3-VPAD', 'path': 'C3D.vpad', 'r': 'r', 'safe': 'safety', 'heli': 'light', 'probe': ['if (VP && window.TurboCity)', 300, 'AC-HL-01'], 'why': [S('NJ', 'בווילה 4 — מנחת של 9 מ׳ למסוק עם רוטור של 10.06 מ׳'), S('G', "TurboCity.draw(ctx, 'AC-HL-01', VP.c[0] - vi.w / 2")]},
                           {'zone': 'C3', 'id': 'C3-HOME', 'path': 'ZC3.levels.pad', 'r': 'r', 'safe': 'safety', 'heli': 'AW139', 'probe': ["C3LV[c3Lv()-1].pad?' · the big helicopter'", 60, 'helicopter'], 'why': [S('NJ', 'בבית השחקן מנחת של 16 מ׳ עם מסוק של 16.66 מ׳'), S('G', "' · the big helicopter'")]}]},
     'emergency': {'A4-FIRE': {'zone': 'A4', 'path': 'A34D.baysFire', 'need': 5}, 'A4-EMS': {'zone': 'A4', 'path': 'A34D.baysEms', 'need': 5}, 'C4-FIRE2': {'zone': 'C4', 'type': 'FIRESTN2', 'need': 3}},
     'sports': {'zone': 'A4', 'courts': {'פנים מגרש הכדורגל (A3)': {'path': 'ZA.stad', 'm': [85, 55]}, 'פנים מגרש הקט-רגל': {'path': 'ZA.foot5In', 'm': [40, 20]},
                                         'פנים מגרש הכדורסל': {'path': 'ZA.basketIn', 'm': [28, 15]}, 'פנים מגרש הטניס': {'path': 'ZA.tennisIn', 'm': [23.77, 10.97]}}},
     'night': {'head': '#fff3c4', 'glow': 'rgba(255,240,180,.75)', 'glow_r_px': 10, 'ground_beam': True, 'beam': 'rgba(255,225,150,.45)'},
     'design': {'variety_min': 3, 'bike_rack': 'PR-29', 'bike_radius_px': 250, 'public_kinds': ['shop', 'school', 'clinic', 'public', 'sport', 'office', 'service', 'emergency']},
     'seams': {'axis_tol_px': 2, 'row_tol_px': 4, 'pairs': [['A3', 'A4'], ['A3', 'B3'], ['A4', 'B4'], ['B3', 'B4'], ['B3', 'C3'], ['B4', 'C4'], ['C3', 'C4'], ['C3', 'D3'], ['C4', 'D4'], ['D3', 'D4']]},
     'palettes': pal, 'conflicts': CONFLICTS, 'checks': [{'id': a, 'he': b, 'what': c} for a, b, c in CHECKS], 'method': METHOD,
     'exceptions_file': 'study/style/style_exceptions.json',
    }
    guide['counts'] = {'rules': sum(len(g['rules']) for g in GROUPS), 'checks': len(CHECKS), 'conflicts': len(CONFLICTS), 'sources': len(SRC)}
    if MISSING:
        for k, s in MISSING: print('חסר במקור', k, s)
        sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(guide, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(OUT, guide['counts'])

if __name__ == '__main__':
    main()
