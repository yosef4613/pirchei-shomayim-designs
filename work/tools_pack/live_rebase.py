#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""4.11 02:50 · live_rebase — a zone live page moved onto a new official build (the "reconstruct" method, as a tool).
The live page must differ from its own base only in whole lines that were replaced (the head script, the title, the zone bar before </body>).
Each replaced line is found in the new build by its position (from the start in the first half of the file, from the end in the second half),
and must be identical there to the line of the old base; the title line is taken by its place. Refuses an existing output.
usage: python3 live_rebase.py <live.html> <old_base.html> <new_base.html> <out.html> [--title 'כותרת']"""
import sys, os, difflib
a = sys.argv[1:]
title = None
if '--title' in a:
    i = a.index('--title'); title = a[i + 1]; del a[i:i + 2]
live, old, new, out = a
if os.path.exists(out): sys.exit('exists: ' + out)
rd = lambda f: open(f, encoding='utf-8').read().split('\n')
L, B0, B1 = rd(live), rd(old), rd(new)
sm = difflib.SequenceMatcher(None, B0, L, autojunk=False)
N = list(B1); n = 0
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op == 'equal': continue
    if op != 'replace' or a2 - a1 != 1 or b2 - b1 != 1: sys.exit('not a one-line replace: %s %d-%d / %d-%d' % (op, a1, a2, b1, b2))
    o = B0[a1]
    if o.startswith('<title>'):
        j = next(k for k, x in enumerate(B1) if x.startswith('<title>'))
    else:
        j = a1 if a1 < len(B0) / 2 else len(B1) - (len(B0) - a1)
        if B1[j] != o: sys.exit('line %d of the old base is not at %d in the new build' % (a1, j))
    N[j] = L[b1] if not (title and o.startswith('<title>')) else '<title>%s</title>' % title
    n += 1
open(out, 'w', encoding='utf-8').write('\n'.join(N))
s = '\n'.join(N)
print('ok', out, 'lines replaced', n, '· tcZoneBar', s.count('tcZoneBar'), '· live_f9fix', s.count('live_f9fix'))
