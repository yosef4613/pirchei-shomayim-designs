# -*- coding: utf-8 -*-
# ft2_p6.py <add.json> <src_game_dir> — fieldthru2: מוסיף ללוח של fieldthru (parts/019l2_ft_sched.js — FTS.add) את התוצאה של ft2_gen.py (למשל P6),
# בלי לגעת בשאר: טיסות ולו״ז — נוספים / מוחלפים לפי המזהה; רכבים — מוחלפים לפי המזהה; זמני הגרירות של R3 — מההרצה החדשה (נבחרו מול הלוח עם התוספת)
import sys, os, json, re
R = json.load(open(sys.argv[1], encoding='utf-8')); G = sys.argv[2]; p = os.path.join(G, 'parts', '019l2_ft_sched.js')
s = open(p, encoding='utf-8').read(); k0 = s.index(',add:') + 5; k1 = s.index('};\n(function(){try{if(!FTS.on')
A = json.loads(s[k0:k1])
def put(L, items, key):
    for it in items:
        i = next((j for j, x in enumerate(L) if key(x) == key(it)), None)
        if i is None: L.append(it)
        else: L[i] = it
for f in R['flights']: f['ft'] = 1; f['ft2'] = 1
put(A['flights'], R['flights'], lambda x: x['id']); put(A['sched'], R['sched'], lambda x: x[0]); put(A['veh'], R['veh'], lambda x: x['id'])
if R.get('r3'): A['r3'] = {k: [v['out'], v['back']] for k, v in R['r3'].items() if 'out' in v and 'back' in v}
info = ' · '.join(x for x in R['log'] if not x.startswith('R3:'))
tag = '   fieldthru2 (17.11): נוסף — '
hdr = s[:k0 - len(',add:')]
if tag in hdr: hdr = re.sub(re.escape(tag) + r'.*\n', '', hdr)
i = hdr.index('==== */'); hdr = hdr[:i] + 'fieldthru2 (17.11) — עמדה נוספת בלו״ז (ft2_gen.py מעל העולם של S7F303, אותו מחולל): ' + info.replace('*/', '') + '\n   ' + hdr[i:]
out = hdr[:hdr.rindex('var FTS=')] + hdr[hdr.rindex('var FTS='):] + ',add:' + json.dumps(A, ensure_ascii=False, separators=(',', ':')) + s[k1:]
open(p, 'w', encoding='utf-8').write(out); print('ok', len(A['flights']), 'טיסות בתוספת', [f['id'] for f in A['flights']], len(out))
