#!/usr/bin/env python3
# sync_part.py — terminal: מכניס את tools/term_geo.json לחלק (בין /*TMNL_G*/ … /*TMNL_G*/), כמו S15J_L של 074x
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
part = sys.argv[1] if len(sys.argv) > 1 else '/home/user/tc_root/tc/pkg/work/src_game_t17_terminal/parts/074zx_terminal.js'
G = json.load(open(os.path.join(HERE, 'term_geo.json'), encoding='utf-8'))
# למשחק — רק הגאומטריה (לא טקסטי הציור)
DROP = {'text', 'steps', 'boardSample', 'sample', 'path', 'stands', 'from', 'loop', 'stop', 'standStops', 'crossings', 'newRows'}
def lean(o):
    if isinstance(o, dict): return {k: lean(v) for k, v in o.items() if k not in DROP}
    if isinstance(o, list): return [lean(v) for v in o]
    return o
keep = lean({k: G[k] for k in ('carousels', 'chain', 'east', 'shuttle')})
s = open(part, encoding='utf-8').read()
js = json.dumps(keep, ensure_ascii=False, separators=(',', ':'))
s2, n = re.subn(r'/\*TMNL_G\*/.*?/\*TMNL_G\*/', lambda m: '/*TMNL_G*/' + js + '/*TMNL_G*/', s, count=1, flags=re.S)
assert n == 1
open(part, 'w', encoding='utf-8').write(s2); print('sync', len(js), 'תווים')
