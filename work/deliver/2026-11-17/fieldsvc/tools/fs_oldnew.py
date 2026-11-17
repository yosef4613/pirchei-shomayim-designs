#!/usr/bin/env python3
# fs_oldnew.py — fieldsvc: הישן (S7F272, המתכנן AO) מול S7F302 מול היעד — לכל טיסה בחלון: כמה מהשירותים שהיא צריכה (טבלת "צריך") הגיעו, ומתי.
import json, os, sys, statistics as ST
HERE = os.path.dirname(os.path.abspath(__file__)); QA = os.path.join(HERE, '..', 'qa')
sys.path.insert(0, HERE); import fs_need
OLDMAP = {'PT':'PT','PW':'PT','BT':'BT','CU':'TG','CS':'CT','BL':'BL','FT':'FT','FW':'FT','CT':'CT','CS':'CT','WT':'WT','LV':'LV','SVC':'SVC','GP':'GP','GC':'GP','MS':'MS','AB':'AB','HL':'HL','SH':'SH','SV':'SV','EMS':'AL'}
SV = ['PT','BT','BL','FT','CT','WT','LV','SVC','GP','MS','AB','AL','HL','TG']
HE = fs_need.HE
def old_rows(O):
    rows = []
    import fs_check
    SH = fs_check.short_set([dict(id=f['code'], model=f['ac']) for f in O['fl'] if not f['parked'] and f['push'] is not None])
    for f in O['fl']:
        if f['parked'] or f['onb'] is None or f['push'] is None or f['ac'] not in fs_need.NEED: continue   # רק סבבים שהושלמו בחלון (עצירה ← דחיפה)
        sid = f['sd'] or ''
        mode = 'cargo' if f['kind'] == 'cargo' else 'ga' if (f['ac'] in ('AC-PR-01','AC-LT-01','AC-BJ-01','AC-CN-01','AC-AM-01')) else ('bridge' if f['bridge'] and not f['remote'] else 'remote')
        n = [x.replace('r:','') for x in fs_need.NEED[f['ac']] if not x.startswith('r:') or mode == 'remote']
        if f['ac'] in fs_need.WL and f['code'] not in SH: n += ['WT', 'LV']
        if mode == 'remote' and fs_need.PAX.get(f['ac'],0) * fs_need.PRM >= .5: n.append('AL')
        got = {}
        for q in f['tasks']:
            c = OLDMAP.get(q['type']) or ('AL' if 'EMS' in q['v'] else None)
            if not c: continue
            s0 = q['s0'] if q['s0'] is not None else q['t0']; s1 = q['s1'] if q['s1'] is not None else q['t1']
            ok = s0 >= f['onb'] - 2 and (f['push'] is None or s1 <= f['push'] + 6)   # בישן הבמה / המסוע נסגרים עד 5 ש׳ אחרי תחילת הדחיפה
            got.setdefault(c, []).append(dict(v=q['v'], t0=round(s0 - f['onb'],1), t1=round(s1 - f['onb'],1), ok=ok))
        if f.get('amb'): got.setdefault('AL', []).append(dict(v='V-EMS2', t0=round(f['amb']['at'] - f['onb'],1), t1=round(f['amb']['done'] - f['onb'],1), ok=True))
        req = {}
        for x in n: req[x] = req.get(x,0) + 1
        miss = []
        for x, k in req.items():
            okN = len({q['v'] for c in x.split('|') for q in got.get(c, []) if q['ok']})
            miss += [x] * max(0, k - okN)
        rows.append(dict(id=f['code'], stand=sid, model=f['ac'], mode=mode, need=n, got=got, miss=miss, own=f['want'], full=not miss))
    return rows
def summary(rows, label):
    per = {}
    for r in rows:
        for x in set(r['need']):
            c = x.split('|')[0]; p = per.setdefault(c, dict(need=0, got=0, t0=[], d=[]))
            p['need'] += 1
            L = [q for cc in x.split('|') for q in r['got'].get(cc, []) if q.get('ok', True) and not q.get('late') and not q.get('early')]
            if L: p['got'] += 1; p['t0'].append(L[0]['t0']); p['d'].append(L[0]['t1'] - L[0]['t0'])
    return dict(label=label, flights=len(rows), full=sum(1 for r in rows if r['full']), per={c: dict(need=p['need'], got=p['got'], t0=round(ST.median(p['t0'])) if p['t0'] else None, d=round(ST.median(p['d'])) if p['d'] else None) for c, p in per.items()})
def html(S):
    cols = ''.join(f'<th>{s["label"]}</th>' for s in S)
    rows = [f'<tr><td><b>טיסות בחלון</b></td>{"".join("<td class=n>"+str(s["flights"])+"</td>" for s in S)}</tr>',
            f'<tr><td><b>עם כל השירותים שצריך</b></td>{"".join("<td class=n><b>"+str(s["full"])+" / "+str(s["flights"])+(" ("+str(round(100*s["full"]/s["flights"]))+"%)" if s["flights"] else "")+"</b></td>" for s in S)}</tr>']
    for c in SV:
        cells = []
        for s in S:
            p = s['per'].get(c)
            cells.append('<td class=n>' + (f'{p["got"]} / {p["need"]}' + (f' · +{p["t0"]} ש׳, {p["d"]} ש׳' if p['t0'] is not None else '') if p else '—') + '</td>')
        rows.append(f'<tr><td>{HE.get(c,c)}</td>{"".join(cells)}</tr>')
    return '<div style="overflow-x:auto"><table class="t"><thead><tr><th>שירות (קיבלו / צריכים · התחלה מהעצירה, משך — חציון)</th>' + cols + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
if __name__ == '__main__':
    S = []; notes = []
    if os.path.exists(os.path.join(QA, 'old_svc_272.json')):
        O = json.load(open(os.path.join(QA, 'old_svc_272.json'))); R = old_rows(O); S.append(summary(R, f'הישן S7F272 (AO, {O["W"]} ש׳, זרע {O["seed"]})'))
        own_full = sum(1 for r in R if all(any(q['ok'] for c in [ {'catering':'CT','cleaning':'SVC','water':'WT','lavatory':'LV','gpu':'GP','belt':'BL','highloader':'HL','fuel':'FT','push':'PT','bags':'BT'}.get(w)] if c for q in r['got'].get(c,[])) for w in r['own'] if w in ('catering','cleaning','water','lavatory','gpu','belt','highloader','fuel','push','bags')))
        notes.append(f'בישן — לפי מה שהסוג היה אמור לקבל בישן עצמו (G77_AC.svc + g77Need: מים / שירותים רק ל-50% מהטיסות, קייטרינג לפי סוג): {own_full} / {len(R)} קיבלו את כל מה שהישן תכנן.')
        json.dump(R, open(os.path.join(QA, 'old_rows.json'), 'w'), ensure_ascii=False)
    import fs_check
    for f, lab in [('dump_s7f302.json', 'S7F302 (7 טיסות במחזור)'), ('dump_8041.json', 'הלו״ז של fieldthru (13) — לפני fieldsvc'), ('try8047/dump.json', 'עם fieldsvc (try8047)')]:
        p = os.path.join(QA, f)
        if not os.path.exists(p): continue
        d = json.load(open(p))
        if 'לפני' in lab: d['veh'] = [v for v in d['veh'] if not v.get('fsv')]
        C = fs_check.check(d)
        rows = [dict(need=r['need'], got={c: [dict(t0=q['t0'], t1=q['t1'], late=q['late'], early=q['early']) for q in L] for c, L in r['got'].items()}, full=r['full']) for r in C['rows']]
        S.append(summary(rows, lab))
    open(os.path.join(HERE, 'old_vs_new.json'), 'w').write(json.dumps(S, ensure_ascii=False))
    h = '<h2>0א. הישן מול היום מול היעד — כל שירות שהטיסה צריכה</h2><p class="meta">המדידה: בישן — המתכנן AO עצמו (046/044, בנייה S7F272 — אותו שדה ישן של S7F282 / S7F284), חלון של 1800 ש׳, כל טיסה שהגיעה לעמדה: אילו רכבים עבדו לידה (המשימות של AO.fleet עם הקוד שלה) בין העצירה לדחיפה; היום — S15SIM (dump מהמשחק), כל רגל עבודה משויכת לטיסה אחת. "צריך" — הטבלה של סעיף 1א.</p>' + html(S) + ''.join(f'<p class="meta">{n}</p>' for n in notes)
    open(os.path.join(HERE, 'old_vs_new.html'), 'w', encoding='utf-8').write(h)
    for s in S: print(s['label'], s['full'], '/', s['flights'], {c: (p['got'], p['need']) for c, p in s['per'].items()})
