#!/usr/bin/env python3
# fs_report.py <dump.json> — הסיכום של __TC_FS מתוך dump של המשחק
import json, sys
d = json.load(open(sys.argv[1])); r = d.get('fs') or {}
print('בנייה', d.get('build'), '· שגיאות דף', len(d.get('errs', [])), d.get('errs', [])[:3], '· זיכרון', d.get('mem'), '· זמן טעינה', d.get('ms'))
if isinstance(r, str): print('שגיאה', r); sys.exit()
A = r.get('audit') or {}
print('fieldsvc: מלאות', A.get('full'), '/', A.get('flights'), '·', A.get('pct'), '% · כיסא', A.get('wheelchairW'), '· נסיעות', r.get('trips'), '· ms', r.get('ms'), '· n', r.get('n'), '· err', r.get('err'))
for row in A.get('rows', []):
    print(' ', 'V' if row['full'] else 'X', row['id'], row['stand'], row['model'], row.get('mode'), 'ob', row['ob'], 'dw', row['dwell'], '| חסר', ' '.join(row['miss']) or '-', '| מחוץ', ' '.join(row['late']) or '-', '| בלי פעולה', ' '.join(row.get('noAct', [])) or '-', '| מיותר', ' '.join(row.get('extra', [])) or '-')
print('יומן:'); [print('  ', l) for l in r.get('log', [])]
print('דילוגים:'); [print('  ', l) for l in r.get('skip', [])]
