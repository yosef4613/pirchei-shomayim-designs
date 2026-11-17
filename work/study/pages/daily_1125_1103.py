# -*- coding: utf-8 -*-
# 3.11 · הדוח היומי: R-76 (מעברי חצייה רק בצמתים, אנשים בכביש) — S7F214 ומפת הדרכים סבב 8ב; הרשימה של כל מעבר שיצא או זז, לפי אזור (R-76 סעיף 2, הביקורת 10:45 סעיף 9).
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, 'daily.json'); W = os.path.dirname(os.path.dirname(HERE))
T = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now().strftime('%H:%M')
D = json.load(open(F, encoding='utf-8'))
R = json.load(open(os.path.join(W, 'clean_r2b_025637', 'qa', 'tmp', 'r76_removed.json'), encoding='utf-8'))
rows = []
for z, L in sorted(R['game']['byZone'].items()):
    for x in L: rows.append([z, x['id'], '%s (%s)' % (x.get('roadName') or '', x.get('road') or ''), x.get('junction') or '', x.get('why') or ''])
M = R.get('map', {})
for z, L in sorted((M.get('byZone') or {}).items()):
    for x in L:
        if isinstance(x, dict): rows.append([z + ' · במפה', x.get('id') or '', '%s (%s)' % (x.get('roadName') or '', x.get('road') or ''), x.get('junction') or x.get('to') or '', x.get('why') or ''])
D['xw76'] = {'title': 'R-76 — כל מעבר חצייה שיצא או זז לקו העצירה, לפי אזור (במשחק S7F214 ובמפה סבב 8ב)',
             'rows': rows, 'note': 'במשחק: %d יצאו, %d זזו לקו העצירה, %d נשארו ברמזור ו-1 בלי רמזור (צמוד לצומת). במפה (סבב 8ב): %s זזו, %s יצאו — כל 104 המעברים בצומת. הקובץ: r76_removed.json.' % (
                 R['game']['out'], R['game']['moved'], R['game']['kept']['signal'], M.get('moved', '?') if not isinstance(M.get('moved'), list) else len(M['moved']), M.get('out', '?') if not isinstance(M.get('out'), list) else len(M['out']))}
D['updated'] = '03.11.2026 · ' + T; D['plan'] = 'v6.55'
D['build'] = 'S7F214 · 8fca253dbdc4 (הדף הקבוע 0ebba2e2b316 · 4,966,210; נשלחה אליך)'
D['next'] = ('איפה עצרתי (' + T + '): R-76 במשחק ובמפה — עובר (S7F214, סבב 8ב). עכשיו: הציור v5 של C5/D5 והמסוף; אחריו סבב האנימציות (C3, ‏B3, ‏A3/A4, ‏B4, ‏D3). '
             'לאישורך מ-R-76: עד 1 מ׳ אחרי קו העצירה; ירוק להולכים עם הירוק המקביל, ורכב שפונה נותן זכות קדימה; בלי רמזור — הרכב עוצר להולך; ומה עושים בצמתים בלי רמזור (בלי מעברים, הולכים חוזרים משפת המדרכה).')
new_done = ['R-76 (S7F214, ‏p521x): מעבר רק בצומת — במשחק 14 יצאו ו-22 זזו לקו העצירה; רמזור עם פחות מ-3 זרועות יצא (A6-NM, ‏B5SE, ‏AIR-1); גרף ההולכים — במדרכה בלבד (810 קטעים, 0 על נתיב); '
            'ירוק להולכים עם הירוק המקביל; בדיקות קבועות חדשות: מעבר רחוק מצומת, גרף ההליכה, ואנשים בכביש (0 בחמש דקות משחק). המפה, סבב 8ב: 33 מעברים זזו, כל 104 בצומת.',
            'S7F213: הפרטים החיים של C4 (15 מ-6 סוגים) והמשימות של D5 מוסתרות; הדף החי של C4 — דף קבוע חדש.', 'התוכנית v6.55: D‑403 – D‑418, ‏D‑314 (המסוף 6 + 10).']
D['done'] = new_done + [x for x in D['done'] if not any(x[:30] == y[:30] for y in new_done)][:5]
json.dump(D, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(rows))
