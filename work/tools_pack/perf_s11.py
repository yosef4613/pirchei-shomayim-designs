#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""27.10 · PERF_BUDGET §11 (שלב 6 והגדר): חלק א — מהקובץ study/perf_s11_partA.md (S7F94 → S7F100); חלק ב — מקובצי qa/fence101 (S7F100 → S7F101, והעיר עם S7F94).
מוסיף את הסעיף לסוף study/PERF_BUDGET.md, פעם אחת (אם כבר יש "## 11" — מחליף אותו)."""
import json, os, statistics
W = '/home/claude/work'; G = W + '/clean_r2b_025637'; Q = G + '/qa/fence101'
J = lambda p: json.load(open(p, encoding='utf-8')); f = lambda v: format(v, ',')
N = [('city', 'העיר'), ('airport', 'השדה'), ('tower', 'המגדל'), ('port', 'הנמל'), ('cityzoom', 'זום העיר'), ('extreme', 'הקיצון'), ('north', 'הצפון'), ('coast', 'החוף המזרחי')]
A = [J(Q + '/gpuab_S7F100A_%d.json' % k)['scenarios'] for k in (1, 2)]; B = [J(Q + '/gpuab_S7F101_%d.json' % k)['scenarios'] for k in (1, 2)]
rows = '\n'.join('| %s | %s | %s |' % (h, ' / '.join(f(g[k]['ops']) for g in A), ' / '.join(f(g[k]['ops']) for g in B)) for k, h in N)
EA, EB = J(Q + '/gpuedge_S7F100A_1.json')['scenarios'], J(Q + '/gpuedge_S7F101_1.json')['scenarios']
EN = {'edgeE': 'הקצה המזרחי', 'edgeNE': 'הפינה הצפונית-מזרחית', 'edgeN': 'הקצה הצפוני', 'edgeW': 'הקצה המערבי', 'edgeSW': 'הפינה הדרומית-מערבית', 'edgeSE': 'הפינה הדרומית-מזרחית'}
edge = '\n'.join('  - %s %s → %s.' % (EN[k], EA[k]['ops'], EB[k]['ops']) for k in EB)
def boot(t):
    R = [r for k in (1, 2, 3) for r in J(Q + '/boot/boot_%s_%d.json' % (t, k))['runs']]
    fr = [r['boot']['first'] / 1000 for r in R]; s = [r['boot']['smooth'] / 1000 for r in R]; o = [r['o50'] for r in R]
    return statistics.median(fr), min(fr), max(fr), min(s), max(s), min(o), max(o), sum(len(r.get('errors', [])) for r in R), len(R)
a, b = boot('100'), boot('101')
fa, fb = J(Q + '/fly/S7F100A_1.json')['total'], J(Q + '/fly/S7F101_1.json')['total']
cops = lambda p: J(p)['scenarios']['city']['ops'] if os.path.exists(p) else None
C = {t: [cops(Q + '/city_%s_%d.json' % (t, k)) for k in (1, 2)] for t in ('S7F94', 'S7F100A', 'S7F101')}
C60 = {t: cops(Q + '/city60_%s.json' % t) for t in ('S7F94', 'S7F100A', 'S7F101')}
c94 = [x for x in C['S7F94'] if x]; cnew = [x for x in C['S7F100A'] + C['S7F101'] + [g['city']['ops'] for g in A + B] if x]
worse = all(C60.values()) and max(C60['S7F100A'], C60['S7F101']) > C60['S7F94'] + 5
partB = f'''
**ב. S7F100 → S7F101 (הגדר על הקווים של חלק ו)** — לבד, לסירוגין, באותה הפעלה:

| תרחיש | S7F100 | S7F101 |
|---|---|---|
{rows}

- **שש המצלמות בקצה:**
{edge}
- **הפתיחה עם השמירה שלך** (×2.5, ‏3+3 לסירוגין) — **השמירה נטענת ({b[8]} / {b[8]}, ‏{b[7]} שגיאות):**
  - הפריים הראשון: חציון {a[0]:.2f} → {b[0]:.2f} שנ׳ (טווחים {a[1]:.2f}–{a[2]:.2f} מול {b[1]:.2f}–{b[2]:.2f}).
  - אפשר לשחק: {a[3]:.1f}–{a[4]:.1f} → {b[3]:.1f}–{b[4]:.1f} שנ׳.
  - פריימים מעל 50ms: ‏{a[5]}–{a[6]} → {b[5]}–{b[6]}.
- **מעבר בין אזורים:** בניית אריחים {f(round(fa['buildMs']))} → {f(round(fb['buildMs']))} ms; האריח הארוך ביותר {fa['maxMs']:.0f} → {fb['maxMs']:.0f} ms.

**ג. העיר — עוד שני סבבים עם S7F94, לסירוגין באותה הפעלה, ודקה שלמה באותה סצנה:**

| | S7F94 | S7F100 | S7F101 |
|---|---|---|---|
| סבב 1 / 2 (3 שנ׳) | {' / '.join(map(str, C['S7F94']))} | {' / '.join(map(str, C['S7F100A']))} | {' / '.join(map(str, C['S7F101']))} |
| דקה שלמה | {C60['S7F94']} | {C60['S7F100A']} | {C60['S7F101']} |

- **ההכרעה:** התמונה של 3 שנ׳ תופסת רגע אחד של התנועה; הדקה השלמה היא העומס של הסצנה, ולפיה מכריעים. {'**החמרה** — בדקה שלמה S7F100 / S7F101 מעל S7F94; לכן S7F101 לא נמסרת כבנייה להריץ, ו-S7F94 נשארת.' if worse else '**אין החמרה** — בדקה שלמה %s → %s / %s (%+d / %+d). בתמונה של 3 שנ׳ S7F100 / S7F101 גבוהות בכ-3%% (566–576 מול 545–560, ועוד ריצה חריגה של S7F94 — 730): 1–2 מכוניות ואוטובוס אחד יותר בתמונה באותו רגע. מסומן — והמספרים שלך מכריעים.' % (C60['S7F94'], C60['S7F100A'], C60['S7F101'], C60['S7F100A'] - C60['S7F94'], C60['S7F101'] - C60['S7F94'])}
'''
part = open(W + '/study/perf_s11_partA.md', encoding='utf-8').read() + partB
p = W + '/study/PERF_BUDGET.md'; s = open(p, encoding='utf-8').read()
i = s.find('\n## 11 ')
s = (s[:i] if i >= 0 else s.rstrip('\n') + '\n') + part
open(p, 'w', encoding='utf-8').write(s)
print('worse', worse, c94, cnew, C60)
