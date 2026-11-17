#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""28.10 · PERF_BUDGET §17 (שלב 7, חלקים 1–3 — שמות הרחובות, השלטים, שמות בעברית, 7 הצבעים: p349–p352) · S7F108 → S7F111, מקובצי
qa/s7f111/meas (w15measure.sh). מוסיף את הסעיף לסוף study/PERF_BUDGET.md, פעם אחת (אם כבר יש "## 17" — מחליף אותו)."""
import json, os, re, statistics
W = '/home/claude/work'; G = W + '/clean_r2b_025637'; Q = G + '/qa/s7f111/meas'; A_, B_ = 'S7F108', 'S7F111'
J = lambda p: json.load(open(p, encoding='utf-8')); f = lambda v: format(v, ',')
N = [('city', 'העיר'), ('airport', 'השדה'), ('tower', 'המגדל'), ('port', 'הנמל'), ('cityzoom', 'זום העיר'), ('extreme', 'הקיצון'), ('north', 'הצפון'), ('coast', 'החוף המזרחי')]
A = [J('%s/gpuab_%s_%d.json' % (Q, A_, k))['scenarios'] for k in (1, 2)]; B = [J('%s/gpuab_%s_%d.json' % (Q, B_, k))['scenarios'] for k in (1, 2)]
rows = '\n'.join('| %s | %s | %s |' % (h, ' / '.join(f(g[k]['ops']) for g in A), ' / '.join(f(g[k]['ops']) for g in B)) for k, h in N)
worse = [h for k, h in N if k != 'city' and min(g[k]['ops'] for g in B) > max(g[k]['ops'] for g in A) + 5]
EA, EB = J('%s/gpuedge_%s_1.json' % (Q, A_))['scenarios'], J('%s/gpuedge_%s_1.json' % (Q, B_))['scenarios']
edge = ', ‏'.join('%s → %s' % (EA[k]['ops'], EB[k]['ops']) for k in EB); eworse = [k for k in EB if EB[k]['ops'] > EA[k]['ops'] + 5]
c3 = {t: [J('%s/city_%s_%d.json' % (Q, t, k))['scenarios']['city']['ops'] for k in (1, 2)] for t in (A_, B_)}
c60 = {t: [J('%s/city60x_%s_%d.json' % (Q, t, k))['scenarios']['city'] for k in (1, 2, 3)] for t in (A_, B_)}
cm = {t: statistics.median([d['ops'] for d in v]) for t, v in c60.items()}
if cm[B_] > max(d['ops'] for d in c60[A_]) + 5: worse.append('העיר')
crow = lambda t: '| %s | %s | %s | %s |' % (t, ' | '.join(str(d['ops']) for d in c60[t]), cm[t], ' / '.join(f(d['frames']) for d in c60[t] if d.get('frames') is not None))
def boot(t):
    R = [r for k in (1, 2, 3) for r in J('%s/boot/boot_%s_%d.json' % (Q, t, k))['runs']]
    fr = [r['boot']['first'] / 1000 for r in R]; s = [r['boot']['smooth'] / 1000 for r in R]; o = [r['o50'] for r in R]
    return statistics.median(fr), min(fr), max(fr), min(s), max(s), min(o), max(o), sum(len(r.get('errors', [])) for r in R), len(R)
a, b = boot('108'), boot('111')
fly = {t: [J('%s/fly/%s_%d.json' % (Q, t, k))['total'] for k in (1, 2, 3)] for t in (A_, B_)}
frow = lambda t: '| %s | %s | %s |' % (t, ' / '.join('%.1f' % x['maxMs'] for x in fly[t]), ' / '.join(f(round(x['buildMs'])) for x in fly[t]))
fworse = statistics.median(x['maxMs'] for x in fly[B_]) > max(x['maxMs'] for x in fly[A_]) + 5
lg = open(G + '/qa/s7f111/w15measure.log', encoding='utf-8').read(); tm = re.findall(r'(\d\d:\d\d)', lg)
S = f'''
## 17 · שלב 7, חלקים 1–3 — שמות הרחובות והשלטים (p349, ‏p350), שמות בעברית (p351), 7 הצבעים (p352) · {A_} → {B_} · ‏28.10
**מה נמדד:** לבד על המכונה, לסירוגין, באותה הפעלה ({tm[1] if len(tm) > 1 else '—'}–{tm[-1] if tm else '—'}). בעולם השתנו התוויות (שם לכל רחוב פעם אחת בכל 720 px במקום תווית לכל קטע; לוחיות ושלטים ברוחב הטקסט) — הן בשכבה הסטטית; בטלפון — שכבת השמות (g7Ui) רצה על הטקסט אחרי כל ציור.

**1. פעולות ציור לפריים** — 8 התרחישים, שתי ריצות לכל בנייה:

| תרחיש | {A_} | {B_} |
|---|---|---|
{rows}

- **{'אין החמרה' if not worse else 'החמרה: ' + ', '.join(worse)}.**
- **שש המצלמות בקצה:** {edge}{'' if not eworse else ' — החמרה: ' + ', '.join(eworse)}.

**2. העיר** — התמונה של 3 שנ׳ (עוד שני סבבים): {A_} {' / '.join(map(str, c3[A_]))}, ‏{B_} {' / '.join(map(str, c3[B_]))}. דקה שלמה, 3 ריצות לכל בנייה לסירוגין:

| דקה שלמה | ריצה 1 | ריצה 2 | ריצה 3 | חציון | פריימים בדקה |
|---|---|---|---|---|---|
{crow(A_)}
{crow(B_)}

**3. הפתיחה עם השמירה שלך** (×2.5, ‏3+3 לסירוגין) — **השמירה נטענת ({b[8]} / {b[8]}, ‏{a[7] + b[7]} שגיאות):**
- הפריים הראשון: חציון {a[0]:.2f} → {b[0]:.2f} שנ׳ (טווחים {a[1]:.2f}–{a[2]:.2f} מול {b[1]:.2f}–{b[2]:.2f}).
- אפשר לשחק: {a[3]:.1f}–{a[4]:.1f} → {b[3]:.1f}–{b[4]:.1f} שנ׳.
- פריימים מעל 50ms: ‏{a[5]}–{a[6]} → {b[5]}–{b[6]}.

**4. מעבר בין אזורים** (w3fly, 3 ריצות לכל בנייה לסירוגין):

| בנייה | האריח הארוך ביותר (ms) | בניית האריחים (ms) |
|---|---|---|
{frow(A_)}
{frow(B_)}

- **{'אין החמרה' if not fworse else 'החמרה במעבר בין אזורים'}.**
'''
P = W + '/study/PERF_BUDGET.md'; T = open(P, encoding='utf-8').read()
i = T.find('\n## 17 ·')
T = (T[:i] if i >= 0 else T.rstrip('\n') + '\n') + S
open(P, 'w', encoding='utf-8').write(T)
print('§17 written · worse:', worse, eworse, '· city', cm, '· boot', round(a[0], 2), round(b[0], 2), '· fly', [x['maxMs'] for x in fly[A_]], [x['maxMs'] for x in fly[B_]])
