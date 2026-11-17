#!/usr/bin/env python3
# zc_both.py <zc.json>... — closezoom: הקריטריון של perf בהחזרה שלו — "קפיצת ירוק" = פריים שבו החלק הירוק גבוה ב-0.12 מעל *שני* המצבים היציבים
# (סוף השלב הקודם וסוף השלב הזה) והאפור נמוך משניהם ב-0.05. לכל קובץ: הסכום, ולפי שלב.
import json, sys, statistics as st
for f in sys.argv[1:]:
    R = json.load(open(f)); rows = R.get('rows') or []; ph = []
    for r in rows:
        if not ph or ph[-1][0] != r[12]: ph.append((r[12], []))
        ph[-1][1].append(r)
    stab = []
    for k, L in ph:
        tail = L[-8:] if len(L) > 12 else L[-3:]
        stab.append((st.median([x[10] for x in tail]), st.median([x[11] for x in tail])))
    tot = 0; where = {}
    for i, (k, L) in enumerate(ph):
        g0, y0 = stab[i]; g1, y1 = stab[i - 1] if i else stab[i]
        n = sum(1 for x in L if x[10] > max(g0, g1) + .12 and x[11] < min(y0, y1) - .05)
        if n: where[k] = n
        tot += n
    print(f, '· green jumps (both stable states):', tot, where, '· errs', len(R.get('errs') or []), '· treeBad', len(R.get('treeBad') or []))
