#!/usr/bin/env python3
# fs_check.py — fieldsvc: אותה בדיקה כמו fieldsvc_all במשחק, על dump של S15SIM (dump_game.js): לכל טיסה — השירותים במטריצה, מי הגיע, מתי, לפני הדחיפה?
import json, math, sys
NEED = {'AC-NB-01':['PT','BT','BL','FT','CT','WT','LV','SVC','r:GP','r:MS','r:AB'],'AC-LG-01':['PT','BT','BL','FT','CT','WT','LV','SVC'],'AC-MW-01':['PT','BT','BL','FT','CT','WT','LV','SVC'],
 'AC-RJ-01':['PT','BT','FT','CT','WT','LV','SVC','r:GP','r:MS','r:AB'],'AC-QJ-01':['PT','BT','FT','CT','WT','LV','SVC','r:GP','r:MS','r:AB'],'AC-TP-01':['PT','BT','FT','CT','LV','SVC','r:GP','r:AB'],
 'AC-CG-01':['PT','GP','FT','HL','TG'],'AC-HC-01':['PT','GP','FT','HL','TG'],'AC-TB-01':['PT','GP','FT','HL','TG'],
 'AC-BJ-01':['PT','FT','GP','CT','LV','SVC'],'AC-CN-01':['PT','FT','GP','CT','LV','SVC'],'AC-LT-01':['PT','FT'],'AC-PR-01':['PT','FT']}
PAX = {'AC-NB-01':146,'AC-LG-01':320,'AC-MW-01':240,'AC-RJ-01':61,'AC-QJ-01':80,'AC-TP-01':56,'AC-BJ-01':7,'AC-CN-01':4,'AC-LT-01':4,'AC-PR-01':2}
LEN = {'AC-LG-01':668,'AC-NB-01':376,'AC-RJ-01':317,'AC-CG-01':549,'AC-TB-01':120,'AC-LT-01':91,'AC-PR-01':83,'AC-BJ-01':144,'AC-CN-01':144}
SPAN = {'AC-LG-01':648,'AC-NB-01':358,'AC-RJ-01':260,'AC-CG-01':476,'AC-TB-01':200,'AC-LT-01':112,'AC-PR-01':110,'AC-BJ-01':158,'AC-CN-01':140}
PRM = .01
import re
CODE = re.compile(r'^(SVC|PT|BT|BL|CT|FT|WT|LV|MS|AB|SV|HL|TG|GP|SH|GC|FW|AL)-')
MAP = {'GC':'GP','FW':'FT'}
def code(i):
    m = CODE.match(i); c = m.group(1) if m else None; return MAP.get(c, c)
def need_old(f):
    remote = f['home'][0] in 'RC'
    n = [x.replace('r:', '') for x in NEED.get(f['model'], []) if not x.startswith('r:') or remote]
    if remote and PAX.get(f['model'], 0) * PRM >= .5: n.append('AL')
    return n
import fs_need
OPT={'SH','SV'}
def fhash(s):
    h = 7
    for ch in str(s): h = (h * 31 + ord(ch)) & 0xffffffff
    return h
SHORT = set()
def short_set(flights):
    by = {}
    for f in flights:
        if f.get('kind') and f['kind'] != 'ac': continue
        by.setdefault(f['model'], []).append(f)
    out = set()
    for L in by.values():
        L.sort(key=lambda f: fhash(f['id'])); k = int(.4 * len(L))
        for f in L[len(L) - k:]: out.add(f['id'])
    return out
def need(f):
    m, n = fs_need.need(f['model'], f['home'], f['id'] in SHORT); return n
def evalA(A):
    req={}
    for x in A['need']: req[x]=req.get(x,0)+1
    used=set();miss=[];late=[];extra=[]
    for x,k in req.items():
        okN=0;lateN=0
        for c in x.split('|'):
            for q in A['got'].get(c,[]):
                if q['v'] in used: continue
                if q['late'] or q['early']: lateN+=1; continue
                used.add(q['v']); okN+=1
                if okN>=k: break
        for i in range(okN,k):
            if lateN>0: late.append(x); lateN-=1
            else: miss.append(x)
    want={c for x in A['need'] for c in x.split('|')}
    for c,L in A['got'].items():
        if c in want or c in OPT: continue
        if any(not q['late'] and not q['early'] for q in L): extra.append(c)
    return miss,late,extra
def stand_leg(f):
    L = [g for g in f['legs'] if not g.get('att')]
    return max((g for g in L if g.get('h') is not None and g['f'] == 0), key=lambda g: g['t1'] - g['t0'])
def segd(p, a, b):
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1; u = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - ax - u * dx, p[1] - ay - u * dy)
def check(d, W=1800):
    global SHORT; SHORT = short_set(d['flights'])
    T = d['T']; F = []
    for f in d['flights']:
        if f.get('kind') and f['kind'] != 'ac': continue
        st = stand_leg(f); x, y = st['p'][0]; h = st.get('h', math.pi / 2); L = LEN.get(f['model'], f.get('L', 300))
        ng = (d.get('ngf') or {}).get(f['model'], .12) if isinstance(d.get('ngf'), dict) else .12
        nose = (x + math.cos(h) * ng * L, y + math.sin(h) * ng * L); tail = (nose[0] - math.cos(h) * L, nose[1] - math.sin(h) * L)
        F.append(dict(f=f, ob=st['t0'], off=st['t1'], nose=nose, tail=tail, span=SPAN.get(f['model'], 200), need=need(f), got={}))
    for v in d['veh']:
        c = code(v['id'])
        if not c: continue
        for g in v['legs']:
            if g['f'] != 8 or not g.get('p') or g.get('hall') or g.get('hallId'): continue
            p = g['p'][0]; best = None
            for A in F:
                for k in (0, T, -T, 2 * T, -2 * T):
                    a0, a1 = g['t0'] + k, g['t1'] + k
                    if a1 > A['ob'] and a0 < A['off']:
                        dd = segd(p, A['nose'], A['tail'])
                        if dd < A['span'] / 2 + 140 and (best is None or dd < best[0]): best = (dd, A, a0, a1)
            if best:
                dd, A, a0, a1 = best
                A['got'].setdefault(c, []).append(dict(v=v['id'], t0=round(a0 - A['ob'], 1), t1=round(a1 - A['ob'], 1), late=a1 > A['off'] + 1, early=a0 < A['ob'] - 2, d=round(dd)))
    rows = []
    for A in F:
        miss, late, extra = evalA(A)
        rows.append(dict(id=A['f']['id'], stand=A['f']['home'], model=A['f']['model'], ob=round(A['ob'] % T, 1), dwell=round(A['off'] - A['ob'], 1), need=A['need'],
                         got={k: v for k, v in A['got'].items()}, miss=miss, late=late, extra=extra, full=not miss and not late and not extra))
    per = W / T
    return dict(T=T, flights=len(rows), full=sum(r['full'] for r in rows), rows=rows, wc=sum(1 for r in rows if 'AL' in r['got']) * 2 * per)
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); R = check(d)
    print('טיסות', R['flights'], 'מלאות', R['full'], 'כיסא גלגלים ב-1800', R['wc'])
    for r in R['rows']:
        print(r['id'], r['stand'], r['model'], 'ob', r['ob'], 'dw', r['dwell'], 'חסר:', ' '.join(r['miss']) or '-', '| מחוץ:', ' '.join(r['late']) or '-', '| מיותר:', ' '.join(r['extra']) or '-', '| יש:', ' '.join(f"{k}({q[0]['t0']}–{q[0]['t1']})" for k, q in r['got'].items()))
    if len(sys.argv) > 2: json.dump(R, open(sys.argv[2], 'w'), ensure_ascii=False)
