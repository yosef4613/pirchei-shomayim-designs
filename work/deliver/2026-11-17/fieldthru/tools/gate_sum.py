# gate_sum.py <tryNNNN> — fieldthru: סיכום של הבדיקות החוסמות (q_ingame, rules_gate, people_on_road, stuckmax, data:image) מתוך qa/<try>
import sys, json, os, re
Q = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/qa/' + sys.argv[1]
def rd(n):
    try: return open(os.path.join(Q, n), encoding='utf-8').read()
    except OSError: return ''
print('runs:', rd('runs.tsv').replace('\n', ' | '))
print('static:', rd('static.txt').strip())
try:
    R = json.load(open(os.path.join(Q, 'ingame.json'))); ra = R['roadAudit']
    print('ingame:', R.get('build'), 'errors', len(R.get('errors') or []), 'roadAudit', ra['passed'], '/', ra['total'])
    for x in ra['failed']: print('  FAIL', x[:400])
    ft = [c for c in (ra.get('checks') or []) if 'fieldthru' in str(c)]
except Exception as e: print('ingame: —', e)
try:
    r = json.load(open(os.path.join(Q, 'rules.json'))); print('rules:', r.get('ok'), r.get('fails'))
except Exception as e: print('rules: —', str(e)[:80])
p = rd('people.log'); print('people:', p.strip()[-300:].replace('\n', ' | '))
s = rd('stuck.log'); print('stuck:', s.strip()[-300:].replace('\n', ' | '))
try:
    S = json.load(open(os.path.join(Q, 'sim.json'))); print('fts', S.get('fts'), 'fta', json.dumps({k: S['fta'][k] for k in ('seeds', 'minMoves', 'ok', 'stands', 'overlap', 'newNoTug', 'issues')} if isinstance(S.get('fta'), dict) else S.get('fta'), ensure_ascii=False)[:600])
    print('fc.moves', S['fc']['moves'], 'svc full', S['fc']['svc']['full'], '/', S['fc']['svc']['flights'])
except Exception as e: print('sim: —', str(e)[:80])
