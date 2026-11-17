#!/usr/bin/env python3
# mem_sum.py <memcmp.json> — perf 17.11: סיכום של memcmp.js — לכל בנייה: השיא (כל התהליכים / ה-renderer / ‏gpu, ‏RSS ו-RssAnon), בטעינה / בסוף / אחרי gc,
# הערימה והקנבסים לפי הבעלים, והגידול לאורך מעברי הציור של people_on_road.
import json, sys
A = json.load(open(sys.argv[1]))
for r in A:
    print('==', r['build'], '·', f"{r['bytes']:,}", 'בתים · מוכן אחרי', r.get('readyS'), 'שנ׳ · people', r.get('peopleS'), 'שנ׳', '· שגיאה: ' + r['err'] if r.get('err') else '')
    pk = r['peak']; print('  שיא: כל התהליכים', pk['total'], 'מ"ב (anon', pk['anon'], ') · renderer', pk['renderer'], '(anon', pk['rendererAnon'], ') · gpu', pk['gpu'], '· מתי:', pk['at'])
    for k in ('atLoad', 'atEnd', 'afterGc'):
        x = r.get(k)
        if not x: continue
        p, s = x['page'], x['rss']
        by = {t: v['rss'] for t, v in s['by'].items()}
        print(f"  {k:8s} RSS {s['total']} ({by}) · heap {p.get('heapMB')} / {p.get('heapTotMB')} · canvas {p.get('canvasMB')} מ\"ב ב-{p.get('canvases')} · vrec {p.get('vrec')} · sbc {p.get('sbc')} · dom {p.get('dom')}")
        if p.get('by'): print('           הקנבסים לפי הבעלים:', ' · '.join(f"{b[0]} {b[2]}מ\"ב/{b[1]}" for b in p['by']))
    sm = r.get('sweepMem') or []
    if sm: print('  לאורך המעברים (s: heap / canvas):', ' · '.join(f"{m['s']:.0f}: {m['heap']}/{m['canvas']}" for m in sm))
    rs = r.get('rss') or []
    if rs:
        st = max(1, len(rs) // 12)
        print('  RSS לאורך הזמן (s ph: total / renderer / gpu):', ' · '.join(f"{x['s']} {x.get('ph') or ''}: {x['total']}/{x['by'].get('renderer', {}).get('rss', 0)}/{x['by'].get('gpu-process', {}).get('rss', 0)}" for x in rs[::st]))
    print('  people:', r.get('people'))
