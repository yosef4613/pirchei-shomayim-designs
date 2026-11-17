#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""4.11 · signal_gate — R-79 (הביקורת 20:30), בדיקה שעוצרת מסירה: כל צומת במשחק עם 3 זרועות ומעלה — או שיש בו רמזור, או שיש לו סיבה
   ברשימה tools_pack/nosignal_reasons.json, מתוך D‑427 או D‑430 בלבד (כיכר, רחוב ללא מוצא, כניסה לחניון / לחצר, מיזוג או רמפה, שער של
   אזור סגור, מפגש עם מסילה, דרך בתוך אזור סגור), עם ההחלטה שהיא נשענת עליה. אחרת — כישלון.
   זרוע = כביש במשחק שאינו עתידי (EDGES, ‏future=false). הקלט — xw_dump.json של clean_r2b_025637/tools/dev/xw_dump.js (אותו קלט של xw_gate.py).
usage: python3 signal_gate.py <xw_dump.json> <out.json> [--md <out.md>] [--reasons <file>]
היציאה: 0 — עובר; 1 — יש צומת בלי רמזור ובלי סיבה, או סיבה שאינה מ-D‑427 / D‑430."""
import sys, os, json, argparse
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('dump'); ap.add_argument('out'); ap.add_argument('--md')
ap.add_argument('--reasons', default=os.path.join(W, 'tools_pack', 'nosignal_reasons.json'))
A = ap.parse_args()
G = json.load(open(A.dump, encoding='utf-8')); RS = json.load(open(A.reasons, encoding='utf-8'))['rows']
RULES = ('D‑427', 'D‑430'); KINDS = ('כיכר', 'רחוב ללא מוצא', 'כניסה לחניון', 'כניסה לחצר', 'מיזוג או רמפה', 'שער של אזור סגור', 'מפגש עם מסילה', 'דרך בתוך אזור סגור')
arms = {}
for e in G['edges']:
    if e.get('future'): continue
    for k in (e['a'], e['b']): arms.setdefault(k, []).append(e['id'])
SIG = set(G['signals']); BY = {r['node']: r for r in RS}
J = sorted(k for k, v in arms.items() if len(v) >= 3)
rows, bad, stale = [], [], []
for k in J:
    if k in SIG: rows.append(dict(node=k, arms=len(arms[k]), state='רמזור')); continue
    r = BY.get(k)
    if not r: bad.append(dict(node=k, arms=arms[k], why='אין רמזור ואין סיבה ברשימה')); continue
    if r.get('rule') not in RULES or r.get('kind') not in KINDS or not r.get('why') or not r.get('src'):
        bad.append(dict(node=k, arms=arms[k], why='הסיבה ברשימה לא מ-D‑427 / D‑430, או בלי סוג, הסבר או מקור')); continue
    rows.append(dict(node=k, arms=len(arms[k]), state='בלי רמזור', rule=r['rule'], kind=r['kind']))
for k, r in BY.items():
    if k in SIG or len(arms.get(k, [])) < 3: stale.append(dict(node=k, why='יש בו רמזור' if k in SIG else 'פחות מ-3 זרועות במשחק'))
ok = not bad
res = dict(build=G.get('build', ''), junctions=len(J), signals=sum(1 for r in rows if r['state'] == 'רמזור'), reasons=sum(1 for r in rows if r['state'] != 'רמזור'),
           bad=bad, stale=stale, ok=ok, rows=rows)
json.dump(res, open(A.out, 'w'), ensure_ascii=False, indent=1)
line = 'signal_gate %s · %d צמתים עם 3 זרועות ומעלה · %d עם רמזור · %d עם סיבה (D‑427 / D‑430) · %d בלי רמזור ובלי סיבה' % ('עובר' if ok else 'נכשל', len(J), res['signals'], res['reasons'], len(bad))
if stale: line += ' · %d שורות ישנות ברשימה (לא כישלון): %s' % (len(stale), ', '.join(s['node'] for s in stale))
print(line)
for b in bad: print('  ', b['node'], '·', b['why'], '·', ', '.join(b['arms']))
if A.md:
    with open(A.md, 'w', encoding='utf-8') as f:
        f.write(line + '\n\n| הצומת | זרועות | המצב | הסיבה |\n|---|---|---|---|\n')
        for r in rows: f.write('| %s | %d | %s | %s |\n' % (r['node'], r['arms'], r['state'], (r.get('kind', '') + ' · ' + r.get('rule', '')) if r.get('rule') else '—'))
        for b in bad: f.write('| %s | %d | **נכשל** | %s |\n' % (b['node'], len(b['arms']), b['why']))
sys.exit(0 if ok else 1)
