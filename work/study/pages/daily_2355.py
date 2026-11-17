#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""29.10 23:55 · the daily report: the two pages of the coordinator's package (R-18 the courts of A4, R-24 the missions), D-292."""
import json, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily.json'); d = json.load(open(p, encoding='utf-8'))
d['updated'] = os.environ.get('UPDATED', '29.10.2026 · 23:55')
NEW = ['פורסמו לעינך (המנה של המתאם, 23:47–23:54): "מגרשי הספורט ב-A4" (R-18) — היום, אפשרות ב׳ (ברירת המחדל: הלולאה המקומית יוצאת, שלושת המגרשים בגודל ובסימון האמיתיים, חניון אחד) ואפשרות א׳ (הכבישים נשארים, הכדורגל ל-A3); '
       '"המשימות במשחק" (R-24) — 67 משימות ופעילויות ב-10 משפחות: 4 בטלפון במקום במקום (שלושת האימונים ב-A4 וההופעה ב-B5), 15 מקצועות רשומים בלי משימה, ומה שחסר בשאר — בעיקר בנקודת המגע (חבילה 5)']
d['done'] = NEW + [x for x in d['done'] if not x.startswith('פורסמו לעינך (המנה של המתאם')]
d['work'] = [w for w in d['work'] if w[0] != 'מ']
d['waiting'] = ['מגרשי הספורט ב-A4 (R-18) — אפשרות ב׳ (ברירת המחדל) או א׳; הדף "מגרשי הספורט ב-A4".',
                'רשימת המשימות (R-24) — ההצעות בטבלה הן ברירת המחדל; הדף "המשימות במשחק".'] + [x for x in d['waiting'] if not x.startswith(('מגרשי הספורט ב-A4', 'רשימת המשימות'))]
L = {x[0]: x for x in d['links']}
for t, u, w in [['מגרשי הספורט ב-A4', 'https://claude.ai/artifact/DPJH7xzEvqwGnqdFkVd94s', 'R-18 — לעינך'], ['המשימות במשחק', 'https://claude.ai/artifact/UWXzH5gGjKLczjWbBpgsPn', 'R-24 — לעינך']]:
    if t not in L: d['links'].insert(3, [t, u, w])
R = {r['id']: r for r in d['review']}
R['R-18'].update({'done': 'הדף "מגרשי הספורט ב-A4" פורסם (23:51): הגודל היום מול האמיתי (כדורסל 12.4 × 7.2 מ׳ מול 28 × 15), אפשרות ב׳ — ברירת המחדל — ואפשרות א׳, ומה זז בכל אחת; האימונים על המגרש — צעד 14.', 'state': 'מחכה לעינך'})
R['R-24'].update({'done': 'הדף "המשימות במשחק" פורסם (23:54): 67 משימות ופעילויות; 4 בטלפון במקום במקום; 15 מקצועות בלי משימה; לכל משפחה — מה חסר, הצעה, שעות ומתי.', 'state': 'מחכה לעינך'})
R['R-25']['done'] = R['R-25']['done'].replace('הזווית המזערית נשארה 25°.', 'הזווית המזערית נשארה 25° בכל העמדות P1–P4 (השרוולים הצמודים מכופפים ב-29°–37°).')
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('ok')
