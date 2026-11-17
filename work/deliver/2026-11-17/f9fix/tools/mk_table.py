# mk_table.py — f9fix: טבלת הכפתורים (טקסט להחזרה) מתוך שתי ריצות של f9_buttons.js — לפני ואחרי.
# python3 mk_table.py <before.json> <after.json>
import json, sys, re
B = json.load(open(sys.argv[1], encoding='utf-8')); A = json.load(open(sys.argv[2], encoding='utf-8'))
key = lambda e: json.dumps(e['data'], sort_keys=True, ensure_ascii=False)
bm = {key(e): e for e in B['events']}
sh = lambda t: re.sub(r'\s+', ' ', t or '')[:90]
print('לשונית "אירועים" — %d כפתורים (לפני: %d בפתיחה הראשונה, %d בשנייה)' % (A['tabs']['events']['buttons'], B['tabs']['events']['buttons'], B['tabs']['events'].get('buttonsSecondOpen', 0)))
for e in A['events']:
    b = bm.get(key(e))
    bef = 'לא הופיע (הלשונית נעצרה בשגיאה S.filter)' if b is None else ('עבד' if b['ok'] else 'לא עבד: ' + sh((b['errs'] or [''])[0] or (b['toasts'] or [''])[0]))
    what = sh('; '.join(e['toasts'][:1])) or ('המסך המלא נפתח' if e['post'].get('show') else 'בדיקת הקולות נפתחה' if e['post'].get('vt') else 'המסך הגדול נפתח' if e['post'].get('phone') else 'המצלמה זזה' if e['moved'] else '')
    aft = ('עובד' if e['ok'] else 'נכשל: ' + sh((e['errs'] or [e.get('clickErr') or 'בלי שינוי'])[0])) + (' · ' + what if what else '') + (' · התחיל בשנייה %s' % e['phase'] if e.get('phase') is not None else '')
    print('- [%s] %s %s → לפני: %s → אחרי: %s' % (e['card'], e['label'], ('(' + sh(e['row'].replace(e['label'], '', 1))[:60] + ')') if e['label'] in ('עכשיו',) else '', bef, aft))
zb = {z['zone']: z for z in B['zones']}
okz = [z for z in A['zones'] if z['ok']]
print('לשונית "אזורים" — %d אזורים: לפני %d/%d נפתחים (כל לחיצה: %s); אחרי %d/%d נפתחים' % (len(A['zones']), B['summary']['zones']['ok'], B['summary']['zones']['total'], sh((B['zones'][0]['errs'] or [''])[0]) if B['zones'] else '', len(okz), len(A['zones'])))
c = {}
for x in A['zoneButtons']:
    t = [k for k in ('cam', 'box', 'story', 'act') if k in x['data']][0]
    c.setdefault(t, [0, 0]); c[t][0] += 1; c[t][1] += 1 if x['ok'] else 0
nm = {'cam': '"קפיצה לאזור"', 'box': '"מצלמה" של פרט חי', 'story': '"מההתחלה" של סיפור', 'act': '"זזים בפועל"'}
print('הכפתורים שבתוך האזורים: ' + ' · '.join('%s %d/%d' % (nm[k], v[1], v[0]) for k, v in c.items()))
print('שגיאות בדף (אחרי): %d · לפני: %d' % (A['summary']['pageErrors'], B['summary']['pageErrors']))
