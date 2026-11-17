#!/usr/bin/env python3
# zc_sum.py <zc.json> [...] — perf 17.11: סיכום של zoomcycle.js: לכל שלב (out/in/f4/jump) — פריימים, ‏dt מקסימלי, >50 / >100 מ"ש, אריחים חיים / מכוסים,
# והירוק: החלק הירוק במסך בכל פריים מול הערך היציב של אותו מצב (סוף השלב) — "קפיצת ירוק" = פריים שבו הירוק גבוה ביותר מ-0.12 מהיציב והאפור נמוך.
import json, sys, statistics as st
for f in sys.argv[1:]:
    R = json.load(open(f)); rows = R.get('rows') or []
    print('==', f, '· build', R.get('build'), '· ready', R.get('readyS'), 's · start', R.get('start'))
    ph = {}
    for r in rows:
        ph.setdefault(r[12], []).append(r)
    tot = {'green_jump_frames': 0, 'frames': 0}
    for k, L in ph.items():
        if not L: continue
        tail = L[-8:] if len(L) > 12 else L[-3:]
        g0 = st.median([x[10] for x in tail]); y0 = st.median([x[11] for x in tail])
        gj = [x for x in L if x[10] - g0 > .12 and x[11] < y0 - .05]
        dts = [x[1] for x in L]
        tot['green_jump_frames'] += len(gj); tot['frames'] += len(L)
        if k.startswith(('out', 'in')) and k not in ('out1', 'in1', 'out2', 'in2', 'out10', 'in10', 'out20', 'in20', 'out6', 'in6') : continue
        print(f"{k:7s} n={len(L):4d} maxdt={max(dts):6.0f} >50={sum(d>50 for d in dts):3d} >100={sum(d>100 for d in dts):3d} live={sum(x[3] for x in L):4d} map={sum(x[4] for x in L):4d} prev={sum(x[5] for x in L):4d} full={sum(x[7] for x in L):4d} built={sum(x[6] for x in L):4d} green: max {max(x[10] for x in L):.2f} stable {g0:.2f} · gray stable {y0:.2f} · green-jump frames {len(gj)}")
    print('total frames', tot['frames'], '· green-jump frames', tot['green_jump_frames'])
    if rows and len(rows[0]) > 13:
        H = {}
        for r in rows:
            k = str(r[12]).rstrip('0123456789') or str(r[12]); o = H.setdefault(k, [0]*8)
            l1h, th, ph_, l1c, sd, dd, ep = r[13:20]; o[0] += max(0, l1h - l1c); o[1] += l1c; o[2] += th; o[3] += ph_; o[4] += sd; o[5] += dd; o[6] += ep; o[7] += 1 if (l1h - l1c) > 0 else 0
        print('holes by phase [L1 holes left, L1 covered, T holes, P/O holes, stale drawn, tiles dropped by dirty, invalidations, frames with an L1 hole]:')
        for k, o in H.items(): print('  ', k, o)
        tt = [sum(o[i] for o in H.values()) for i in range(8)]; print('   total', tt)
    print('perf17', json.dumps(R.get('perf17'), ensure_ascii=False))
    for k in ('mem0', 'memEnd'):
        m = R.get(k) or {}
        print(k, 'heap', m.get('heapMB'), 'canvas', m.get('canvasMB'), 'canvases', m.get('canvases'), 'tiles', m.get('tiles'), 'pool', m.get('pool'), 'mapbase', m.get('mapbase'))
    for k, m in (R.get('memAt') or {}).items():
        print('memAt', k, 'heap', m.get('heapMB'), 'canvas', m.get('canvasMB'), 'tiles', m.get('tiles'))
    print('treeBad', json.dumps(R.get('treeBad'), ensure_ascii=False)[:1500])
    print('wtcErrs', json.dumps(R.get('wtcErrs'), ensure_ascii=False)[:1500])
    print('errs', json.dumps(R.get('errs'), ensure_ascii=False)[:800])
    print('narrow', json.dumps(R.get('narrowEnd'), ensure_ascii=False)[:1500], json.dumps(R.get('narrowErrs'), ensure_ascii=False)[:600])
    print('qx', json.dumps(R.get('qx'), ensure_ascii=False)[:3000])
