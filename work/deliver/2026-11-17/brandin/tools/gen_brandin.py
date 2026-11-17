#!/usr/bin/env python3
# gen_brandin.py — brandin 17.11: מייצר את parts/074v_brandin.js מהתבנית brandin_tpl.js, מהקוד של המעצב (set7_share) ומהסימונים של בעל הבית
#  (airlogos/owner_marks_1117.json — רק keep). גם כותב out/keep_inventory.json (הבירור: לכל פריט keep — הרמה, המשטח במשחק, הגודל).
#  usage: python3 gen_brandin.py <worktree>
import sys, json, re, collections, os
W = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/'
SH = W + 'set7_share/'
HERE = os.path.dirname(os.path.abspath(__file__))
WT = sys.argv[1]
def cat(p):
    s = open(SH + p, encoding='utf-8').read(); return json.loads(s[s.index('['):s.rindex(']') + 1])
CITY = {m['id']: m for m in cat('city-signs/catalog.js') if not m.get('engine')}
OPS = {m['id']: m for m in cat('airport-ops/ops_catalog.js')}
R = json.load(open(W + 'airlogos/owner_marks_1117.json', encoding='utf-8'))['reviews']
LVJ = json.load(open(W + 'brandin/out/review_lv.json', encoding='utf-8'))
LV = LVJ['LV']
def cid(i):
    for a, b in (('drop', 'kiss'), ('cellar', 'wine')):
        if i not in CITY and a in i: i = i.replace(a, b)
    return i
SRC = {'c2Sign': 'c2', 'd2Sign': 'd2', 'extra-s9': 's9', 'south-identity': 's9', 'utility-plate': 'e4', 'bld40': 'b4', 'marquee': 'mq'}
def stype(sid):
    t = re.sub(r'^[^:]*::', '', sid or ''); return SRC.get(re.sub(r'-?\d+$', '', t), t)
# ---- the faces the review counted as in the game (per face, from the review's level line)
def face_ok(rid, m, k, f):
    lv = LV[rid]
    if lv[0] == 'ok': return True
    if lv[0] == 'part' and lv[1].startswith('במשחק '):
        miss = lv[1].split('חסרים:', 1)[1] if 'חסרים:' in lv[1] else ''
        return (f.get('text') or k) not in [x.strip() for x in miss.split(',')]
    return False
ops_keep, city_keep, lib_keep, post_keep, air_keep = [], [], [], [], []
inv = []
for key, v in R.items():
    pre, i = key.split(':', 1)
    keeps = [p for p, mk in v['parts'].items() if mk == 'keep']
    redo = [p for p, mk in v['parts'].items() if mk == 'redo']
    if pre == 'ops':
        if keeps: ops_keep.append(i)
        m = OPS[i]
        inv.append({'key': key, 'region': 'השדה', 'sec': 'ops', 'name': m.get('sourceText') or m['name'], 'part': 'sign', 'mark': 'keep' if keeps else 'redo', 'level': LV['ops:' + i][0], 'where': m['sourceRenderer'] + ' (' + m['family'] + ')', 'size': '%g×%g' % (m['formats']['sign']['w'], m['formats']['sign']['h']), 'anchor': m['source'].get('anchor')})
    elif pre == 'library':
        if keeps: lib_keep.append(i)
        inv.append({'key': key, 'region': '62 הזהויות', 'sec': 'library', 'name': i, 'part': 'logo', 'mark': 'keep' if keeps else 'redo', 'level': 'ok', 'where': 'TC_BRANDS (074m) — מסך המקום, המפה, השלטים', 'size': 'לוגו'})
    elif pre == 'poster':
        if keeps: post_keep.append(i)
        for p in v['parts']:
            inv.append({'key': key, 'region': 'פוסטרים', 'sec': 'poster', 'name': i, 'part': p, 'mark': v['parts'][p], 'level': 'ok', 'where': '074n3s_posters_set11 (TCSHOW.poster / המסגרות של 074n3)', 'size': '600×900' if p == 'facade' else '960×600'})
    elif pre == 'airport':
        for p, mk in v['parts'].items():
            inv.append({'key': key, 'region': 'השדה', 'sec': 'airport', 'name': i, 'part': p, 'mark': mk, 'level': 'ok' if (p == 'logo' and i == 'rental') else 'part', 'where': ('TC_BRANDS.rental — הלוגו המאושר המקורי (מסך המקום, הקיוסק)' if (p == 'logo' and i == 'rental') else '074v_airlogos (זמני — יוחלף בעיצוב החדש של בעל הבית)'), 'size': '900×600' if p == 'logo' else ''})
            if mk == 'keep': air_keep.append(i + ':' + p)
    elif pre == 'city':
        m = CITY[cid(i)]; rid = i
        o = {k: m.get(k) for k in ('id', 'placeId', 'name', 'brandKey', 'brandName', 'color', 'role')}
        fm = {}
        for p in keeps:
            f = m['formats'][p]
            q = {'w': f['w'], 'h': f['h'], 'kind': f.get('kind'), 'text': f.get('text')}
            if p not in ('logo', 'proposal'):
                q['src'] = stype(f.get('sourceFaceId'))
                if face_ok(rid, m, p, f): q['ok'] = 1
            fm[p] = q
        for p, mk in v['parts'].items():
            f = m['formats'][p]
            if p == 'logo': where, lvl = 'מסך המקום (F) — הלוגו של הכותרת', 'part' if LV[rid][0] != 'drawn' else 'drawn'
            elif p == 'proposal': where, lvl = 'אין משטח שלט במבנה (D‑631) → מסך המקום (F), מתחת לכותרת', 'drawn'
            else:
                st = stype(f.get('sourceFaceId'))
                where = {'c2': '060:c2Sign (חזית C2)', 'd2': '019:d2Sign (חזית D2)', 's9': '019b:s9Sign (שלט על הפאה)', 'e4': '019b:e4Plate (לוח מתקן)', 'b4': 'BLD40 (ציור הבניין)', 'mq': 'BLD40 B5THEA — המרקיזה'}.get(st, st)
                lvl = 'ok' if face_ok(rid, m, p, f) else ('drawn' if LV[rid][0] == 'drawn' else 'part')
            inv.append({'key': key, 'region': {'city': 'העיר', 'airport': 'השדה', 'island': 'האי', 'port': 'הנמל'}[LV[rid][2]], 'sec': 'city', 'name': m['name'], 'part': p, 'mark': mk, 'level': lvl, 'where': where, 'size': '%g×%g' % (round(f['w'], 1), round(f['h'], 1)), 'text': f.get('text'), 'place': m.get('placeId')})
        if fm:
            o['formats'] = fm; city_keep.append(o)
# ---- the ops rows, trimmed to what the designer's code reads
opsT = []
for i in ops_keep:
    m = OPS[i]
    o = {k: m[k] for k in ('id', 'name', 'family', 'kind', 'color', 'ink', 'sourceText', 'originals') if k in m}
    o['formats'] = {'sign': {'w': m['formats']['sign']['w'], 'h': m['formats']['sign']['h']}}
    s = m.get('source') or {}
    o['source'] = {k: s[k] for k in ('night_text', 'source_data') if s.get(k) is not None}
    if 'source_data' in o['source']: o['source']['source_data'] = {k: v for k, v in o['source']['source_data'].items() if k in ('kind', 'gate')}
    opsT.append(o)
# ---- the aliases: the library's key → the game's key with the same name
gm = open(WT + '/parts/074m_brands_data.js', encoding='utf-8').read()
LIB = json.load(open(SH + 'library/index.json', encoding='utf-8'))
alias = {}
for b in LIB['brands']:
    k = b['key']
    if re.search(r'["\']?' + re.escape(k) + r'["\']?\s*:\s*\{', gm[:4000000]) is None:
        pass
alias.update({'restaurant': 'table', 'pharmacy': 'vine', 'bank': 'bay'})
# ---- the designer's code, without the loading and the export (the drawing — as it is)
def strip(src, names, api_line, extra=None):
    out = []; depth = 0
    for ln in src.split('\n'):
        if depth > 0:
            depth += ln.count('{') - ln.count('}'); continue
        mm = re.match(r'^(?:async\s+)?function\s+(\w+)\(', ln)
        if mm and mm.group(1) in names:
            depth = ln.count('{') - ln.count('}'); continue
        if ln.startswith('var api={load') or ln.startswith('root.TC_CITY={'): ln = api_line
        if extra: ln = extra(ln)
        out.append(ln)
    s = '\n'.join(out)
    s = s.replace("(typeof window!=='undefined'?window:globalThis);", '(TCBI_R);').replace('(typeof window!=="undefined"?window:globalThis);', '(TCBI_R);')
    return s
opsr = open(SH + 'airport-ops/renderer.js', encoding='utf-8').read()
opsr = strip(opsr, {'load', 'json', 'exportCode', 'exportHtml'}, "var api={draw:draw};root.TC_AIRPORT_OPS=api;",
             lambda l: l.replace("var pending={},script=typeof document!=='undefined'?document.currentScript:null,base=script&&script.src?new URL('./',script.src).href:null;", 'var pending={};')
             .replace('function part(c,p,x,y,w,h){', 'function part(c,p,x,y,w,h){if(p&&p.__draw){p.__draw(c,x,y,w,h);return;}'))
cityr = open(SH + 'city-signs/renderer.js', encoding='utf-8').read()
cityr = strip(cityr, {'load', 'url', 'request', 'safe', 'source', 'exportCode', 'exportHtml'}, "root.TC_CITY={draw:draw};",
              lambda l: l.replace("var own=typeof document!=='undefined'?document.currentScript:null,base=own&&own.src?new URL('./',own.src).href:null;", ''))
fav = open(SH + 'favicon-code.js', encoding='utf-8').read().replace('(typeof window!=="undefined"?window:globalThis);', '(TCBI_R);').replace('if(typeof module!=="undefined"&&module.exports)module.exports=api;', '')
opsr = opsr.replace("if(typeof module!=='undefined'&&module.exports)module.exports=api;", '')
cityr = cityr.replace("if(typeof module!=='undefined'&&module.exports)module.exports=root.TC_CITY;", '')
for s in (opsr, cityr, fav):
    assert 'TCBI_R' in s and 'globalThis' not in s, 'root'
    assert '</script' not in s.lower()
# ---- the filter (nfkiss): neutral ids, the place ids as the game has them, and what the game already knows (TCS12_ROWS: the name, the brand,
#      the colour) is not written again — filled at run time (fewer words in the part)
s12 = open(WT + '/parts/074v_signs12.js', encoding='utf-8').read()
ROWS12 = {r[0]: r for r in json.loads(re.search(r'const TCS12_ROWS=(\[.*?\]);', s12, re.S).group(1))}
KEYS = sorted({m['brandKey'] for m in city_keep if m.get('brandKey')})
for n, m in enumerate(city_keep):
    m['id'] = 'k%d' % n
    pid = (m.get('placeId') or '').replace('KISS', 'DROP')
    m['placeId'] = pid
    r = ROWS12.get(pid)
    for f in m['formats'].values():
        if f.get('text') == m['name']: f['text'] = None
        if f.get('text') is None: f.pop('text', None)
    LBN = {b['key']: b['name'] for b in LIB['brands']}
    if m.get('brandName') == m['name']: m.pop('brandName')
    elif m.get('brandKey') and m.get('brandName') == LBN.get(m['brandKey']): m.pop('brandName'); m['bnB'] = 1
    if r and r[1] == m['name']: m.pop('name')
    if r and (r[2] or None) == (m.get('brandKey') or None): m.pop('brandKey', None); m['bk12'] = 1
    elif m.get('brandKey'): m['brandKey'] = KEYS.index(m['brandKey'])
    if r and r[3] == m.get('color'): m.pop('color')
    if m.get('role') == 'city': m.pop('role')
missing12 = [m['placeId'] for m in city_keep if 'name' not in m and m['placeId'] not in ROWS12]
assert not missing12, missing12
def js(v): return json.dumps(v, ensure_ascii=False, separators=(',', ':'))
keep = {'library': lib_keep, 'poster': post_keep, 'ops': ops_keep, 'airport': air_keep, 'city': len(city_keep)}
t = open(HERE + '/brandin_tpl.js', encoding='utf-8').read()
t = t.replace('/*@OPS@*/', js(opsT)).replace('/*@CITY@*/', js(city_keep)).replace('/*@KEYS@*/', js(KEYS)).replace('/*@ALIAS@*/', js(alias)).replace('/*@KEEP@*/', js(keep))
RF = json.load(open(HERE + '/refined_data.json', encoding='utf-8'))
for b in RF['brands'].values():
    for q in b['parts'].values(): q.pop('src', None); q.pop('face', None)
t = t.replace('/*@REFINED@*/', js(RF))
t = t.replace('/*@FAVICON@*/', fav.strip()).replace('/*@OPSR@*/', opsr.strip()).replace('/*@CITYR@*/', cityr.strip())
open(WT + '/parts/074v_brandin.js', 'w', encoding='utf-8').write(t)
json.dump(inv, open(W + 'brandin/out/keep_inventory.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
c = collections.Counter((x['sec'], x['mark'], x['level']) for x in inv)
print('074v_brandin.js', len(t.encode()), 'בתים · ops', len(opsT), '· city', len(city_keep), '· library', len(lib_keep), '· poster', len(post_keep))
for k in sorted(c): print(k, c[k])
