#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lines_ready.py — טבלת המוכנות של הקווים (R-88, סוף S9a; בונה S7F267, 8.11.2026).
לכל קו 1–6 של מפת הדרכים: כל קטע במסלול (הלוך, ובקו דו-כיווני גם חזור) וכל תחנה — קיימים במשחק או לא.
  קטע — "כן" כשהוא בשלב שכבר נבנה (S1–S8, או הקטעים של S9a) וכל הנקודות שלו (כל 2 מ׳, בלי 3 מ׳ בקצוות) עד 4.5 מ׳ מכביש של המשחק.
  מפרץ — "כן" כשיש במשחק מפרץ (של קו או של תחנת מפה) עד 4.5 מ׳ ממרכז המפרץ של המפה; "חריג" — תחנה בשפת המדרכה בלי מפרץ; אחרת "לא".
  תחנת קצה בלי מפרץ (מעגל סיבוב, שער) — "כן" רק כשהאזור שלה נבנה והצומת קיים במשחק.
מפעילים רק קו שכל השורות שלו "כן" (הבעלים 5.11 08:36: "קו שיש לו את כל הכבישים שלו מוכנים אפשר להפעיל"); קו 4 — לא לפני S16 (D‑520); קו 5 — עם S13.
usage: python3 qa_tools/lines_ready.py <q_lines.json> <city_plan.json> <out.json> <out.html>"""
import sys, json, math, html, datetime
GQ, MP, OUT, OH = sys.argv[1:5]
G = json.load(open(GQ, encoding='utf-8')); P = json.load(open(MP, encoding='utf-8'))
TOL = 45
COLS = [0, 1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600]; ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
S9A_SEGS = {'LC-E3/1', 'LC-E3/2', 'LC-E3W/1', 'CL-I/1', 'CL-I/2', 'CL-I/3', 'CL-I/4', 'CL-I/5', 'CL-I/6', 'CL-I/7', 'CL-F/1'}
BUILT = {'S%d' % i for i in range(1, 9)}


def zone_at(x, y):
    i = next((k for k in range(8) if COLS[k] <= x < COLS[k + 1]), 7)
    j = next((k for k in range(10) if ROWS[k] <= y < ROWS[k + 1]), 9)
    return 'ABCDEFGH'[i] + str(j)


def dseg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


stage_zones = {t['stage']: t['zones'] for t in P['transition']['stages']}
BZ = set(z for s in BUILT for z in stage_zones.get(s, [])) | {'E3'}
GN = {n['id']: n for n in G['nodes']}
GL = []
for e in G['edges']:
    if e['future'] or e['a'] not in GN or e['b'] not in GN: continue
    pts = [[GN[e['a']]['x'], GN[e['a']]['y']]] + (e.get('pts') or []) + [[GN[e['b']]['x'], GN[e['b']]['y']]]
    GL.append((e['id'], pts))
MN = {n['id']: n for n in P['nodes']}
SEG = {}
for s in P['segments']: SEG.setdefault(frozenset([s['a'], s['b']]), []).append(s)
STOPS = {s['id']: s for s in P['bus']['stops']}


def seg_row(s):
    pts = s['pts']; L = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
    sm = []; acc = 0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; l = math.hypot(b[0] - a[0], b[1] - a[1]); t = 0
        while t <= l:
            if 30 <= acc + t <= L - 30: sm.append((a[0] + (b[0] - a[0]) * t / l, a[1] + (b[1] - a[1]) * t / l))
            t += 20
        acc += l
    if not sm: sm = [((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)]
    worst, used = 0, set()
    for p in sm:
        d, gi = min((min(dseg(p, q[k], q[k + 1]) for k in range(len(q) - 1)), i) for i, q in GL)
        worst = max(worst, d); used.add(gi)
    built = s.get('stage') in BUILT or s['id'] in S9A_SEGS
    ok = built and worst <= TOL
    why = ('בנוי — ' + ', '.join(sorted(used))) if ok else ('השלב %s עוד לא נבנה' % s.get('stage') if not built else 'אין כביש במשחק: %.1f מ׳ מהקרוב' % (worst / 10))
    nm = lambda n: n if any(c.isdigit() for c in n) else 'צומת ' + {'BRH': 'ראש הגשר', 'IL': 'האי'}.get(n, n)
    return {'kind': 'קטע', 'id': s['id'], 'what': '%s → %s' % (nm(s['a']), nm(s['b'])), 'cls': s.get('cls'), 'lanes': s.get('lanes'), 'stage': s.get('stage'),
            'zones': s.get('zones'), 'game': sorted(used) if worst <= TOL else [], 'dist_m': round(worst / 10, 1), 'ok': ok, 'state': 'כן' if ok else 'לא', 'why': why}


def bay_rows(st, path_pairs, twoway):
    rows = []
    if not st.get('bay_list'):
        node = st.get('node'); n = MN.get(node, {}); z = zone_at(*(st.get('at') or [n.get('x', 0), n.get('y', 0)]))
        g = min(((math.hypot(q['x'] - n.get('x', 0), q['y'] - n.get('y', 0)), q['id']) for q in G['nodes']), default=(1e9, None))
        ok = z in BZ and g[0] <= TOL
        rows.append({'kind': 'תחנה', 'id': st['id'], 'side': 'קצה', 'what': st['name'], 'zone': z, 'game': g[1] if g[0] <= TOL else None, 'dist_m': round(g[0] / 10, 1),
                     'ok': ok, 'state': 'כן' if ok else 'לא', 'why': ('תחנת קצה — %s קיים' % g[1]) if ok else ('תחנת קצה באזור %s — עוד לא נבנה' % z if z not in BZ else 'אין צומת במשחק')})
        return rows
    for b in st['bay_list']:
        a_, b_ = b['dir'].split('→')
        if not twoway and (a_, b_) not in path_pairs: continue
        poly = b['poly']; cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly); z = zone_at(cx, cy)
        best = min(((math.hypot(q['c'][0] - cx, q['c'][1] - cy), q) for q in G['bays']), key=lambda t: t[0])
        d, q = best; side = '%s/%+d' % (st['id'], b['side'])
        left = G.get('left', {}).get(side)
        if d <= TOL and q['bay']: state, ok, why = 'כן', True, 'מפרץ במשחק — %s (%s)' % (q['id'], ', '.join(q['stops']))
        elif d <= 80 and not q['bay']: state, ok, why = 'חריג', False, 'תחנה בשפת המדרכה בלי מפרץ — %s: %s (חריג לכלל 24, לאישורך)' % (q['id'], q.get('noBay') or '—')
        elif z not in BZ: state, ok, why = 'לא', False, 'האזור %s עוד לא נבנה' % z
        else: state, ok, why = 'לא', False, (left and ('לא נכנס היום: ' + left)) or 'אין מפרץ במשחק עד 4.5 מ׳ (הקרוב %s, ‏%.1f מ׳)' % (q['id'], d / 10)
        rows.append({'kind': 'תחנה', 'id': st['id'], 'side': side, 'what': st['name'], 'zone': z, 'game': q['id'] if d <= 80 else None, 'dist_m': round(d / 10, 1),
                     'ok': ok, 'state': state, 'why': why})
    return rows


out = {'id': 'lines_ready', 'title': 'טבלת המוכנות של הקווים — סוף S9a (R-88)', 'at': datetime.date.today().strftime('%-d.%-m.%Y'),
       'game': {'build': G.get('build'), 'lines_running': G.get('lines'), 'paused': G.get('paused'), 'buses': G.get('buses')},
       'map': {'file': 'study/roads/city_plan.json', 'version': P.get('version')},
       'rule': 'מפעילים רק קו שכל השורות שלו "כן" (הבעלים 5.11 08:36); קו 4 — לא לפני S16 (D‑520); קו 5 — עם S13',
       'built_zones': sorted(BZ), 'lines': []}
for r in P['routes']['bus']:
    rows = []; seen = set(); pairs = set()
    for seq in (r['path'], r.get('back') or []):
        for a, b in zip(seq, seq[1:]):
            pairs.add((a, b)); k = frozenset([a, b])
            if k in seen or a == b: continue
            seen.add(k)
            for s in SEG.get(k, []): rows.append(seg_row(s))
            if k not in SEG: rows.append({'kind': 'קטע', 'id': '%s–%s' % (a, b), 'what': '%s → %s' % (a, b), 'ok': False, 'state': 'לא', 'why': 'אין קטע במפה בין שני הצמתים'})
    for sid in r.get('stop_ids', []):
        if sid in STOPS: rows += bay_rows(STOPS[sid], pairs, r.get('twoway', True))
    n_ok = sum(1 for x in rows if x['ok']); ready = n_ok == len(rows)
    lid = r['id']
    if lid == '4': verdict, act = 'לא מופעל', 'D‑520: קו השדה לא מופעל עד S16 — אז עד חזית הטרמינל, בלי פרסה; 3 אוטובוסים ברזרבה'
    elif lid == '5': verdict, act = 'מחכה ל-S13', 'הגשר והאי — S13'
    elif ready: verdict, act = 'מוכן — מופעל', 'כל הקטעים וכל התחנות קיימים במשחק'
    else:
        miss = [x for x in rows if not x['ok']]
        verdict, act = 'לא מוכן', '%d שורות "לא" / "חריג": %s' % (len(miss), ' · '.join(sorted({(x['id'] + (' ' + x.get('side', '') if x.get('side') else '')).strip() for x in miss}))[:400])
    out['lines'].append({'line': lid, 'name': r['name'], 'color': r.get('color'), 'twoway': r.get('twoway', True), 'buses_d460': (r.get('d460') or {}).get('buses'),
                         'rows': rows, 'yes': n_ok, 'total': len(rows), 'ready': ready and lid not in ('4', '5'), 'verdict': verdict, 'why': act,
                         'game_route': G.get('routeText', {}).get(lid) or G.get('routeText', {}).get(int(lid)) if isinstance(G.get('routeText'), dict) else None})
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- the clean page (no pictures) ----
E = html.escape
cards = []
for L in out['lines']:
    trs = ''.join('<tr class="%s"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class="st">%s</td><td>%s</td></tr>' % (
        'yes' if x['ok'] else ('exc' if x['state'] == 'חריג' else 'no'), E(x['kind']), E(x.get('side') or x['id']), E(x.get('what') or ''),
        E(x.get('zone') or ', '.join(x.get('zones') or []) or ''), E(x['state']), E(x['why'])) for x in L['rows'])
    cards.append('<section class="line"><h2><span class="dot" style="background:%s"></span>קו %s — %s</h2><p class="verdict %s">%s · %d מתוך %d שורות "כן"</p><p class="why">%s</p>'
                 '<table><thead><tr><th>סוג</th><th>מזהה</th><th>מה</th><th>אזור</th><th>במשחק</th><th>הסבר</th></tr></thead><tbody>%s</tbody></table></section>' % (
                     E(L['color'] or '#888'), L['line'], E(L['name']), 'ok' if L['ready'] else 'not', E(L['verdict']), L['yes'], L['total'], E(L['why']), trs))
summ = ''.join('<tr><td><span class="dot" style="background:%s"></span>קו %s</td><td>%s</td><td>%d / %d</td><td>%s</td></tr>' % (
    E(L['color'] or '#888'), L['line'], E(L['name']), L['yes'], L['total'], E(L['verdict'])) for L in out['lines'])
page = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>מוכנות הקווים</title><style>
:root{--bg:#f6f5f1;--fg:#1d2124;--mut:#5d6468;--card:#fff;--line:#e2dfd6;--yes:#e6f3ea;--yesfg:#1d6b39;--no:#fbe9e7;--nofg:#9c2b1f;--exc:#fff4dc;--excfg:#8a5a00}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#15181a;--fg:#e8e6e1;--mut:#a3a8ab;--card:#1e2225;--line:#33383c;--yes:#173322;--yesfg:#8fd6a8;--no:#3a1d1a;--nofg:#f0a69b;--exc:#3a2e14;--excfg:#f0c977}}
:root[data-theme="dark"]{--bg:#15181a;--fg:#e8e6e1;--mut:#a3a8ab;--card:#1e2225;--line:#33383c;--yes:#173322;--yesfg:#8fd6a8;--no:#3a1d1a;--nofg:#f0a69b;--exc:#3a2e14;--excfg:#f0c977}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 "Segoe UI",Arial,sans-serif}main{max-width:1100px;margin:0 auto;padding:20px 16px 48px}
h1{font-size:24px;margin:0 0 6px}h2{font-size:19px;margin:0 0 6px;display:flex;align-items:center;gap:8px}.sub{color:var(--mut);margin:0 0 18px}
.dot{display:inline-block;width:12px;height:12px;border-radius:50%%;flex:none}section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0;overflow-x:auto}
table{border-collapse:collapse;width:100%%;font-size:13.5px}th,td{text-align:right;padding:5px 7px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--mut);font-weight:600}
tr.yes td.st{background:var(--yes);color:var(--yesfg);font-weight:700}tr.no td.st{background:var(--no);color:var(--nofg);font-weight:700}tr.exc td.st{background:var(--exc);color:var(--excfg);font-weight:700}
.verdict{font-weight:700;margin:2px 0}.verdict.ok{color:var(--yesfg)}.verdict.not{color:var(--nofg)}.why{color:var(--mut);margin:0 0 8px}ul{margin:6px 0;padding-inline-start:20px}
</style></head><body><main>
<h1>טבלת המוכנות של הקווים — סוף S9a</h1>
<p class="sub">מעודכן עד: %s · הבנייה %s · מפת הדרכים, סבב %s · הכלל (R-88, הבעלים 5.11 08:36): מפעילים רק קו שכל הקטעים וכל התחנות שלו קיימים במשחק. קו 4 — לא לפני S16 (D‑520). קו 5 — עם S13.</p>
<section><h2>הסיכום</h2><table><thead><tr><th>קו</th><th>השם</th><th>שורות "כן"</th><th>ההחלטה</th></tr></thead><tbody>%s</tbody></table>
<ul><li>קטע — "כן" כשהוא בשלב שכבר נבנה וכל הנקודות שלו עד 4.5 מ׳ מכביש של המשחק.</li><li>מפרץ — "כן" כשיש במשחק מפרץ עד 4.5 מ׳ ממרכז המפרץ של המפה; "חריג" — תחנה בשפת המדרכה בלי מפרץ (לאישורך); אחרת "לא".</li><li>האזורים הבנויים: %s.</li></ul></section>
%s
</main></body></html>''' % (E(out['at']), E(str(G.get('build'))), E(str(P.get('version'))), summ, E(', '.join(out['built_zones'])), ''.join(cards))
open(OH, 'w', encoding='utf-8').write(page)
print(' · '.join('קו %s: %d/%d %s' % (L['line'], L['yes'], L['total'], L['verdict']) for L in out['lines']))
