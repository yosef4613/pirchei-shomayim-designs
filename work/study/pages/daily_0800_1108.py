# -*- coding: utf-8 -*-
# 8.11 08:00 · הדוח של הבוקר — הלילה הראשון של הבונה החדש: הפיצול לקבצי מקור (D‑506), ההחלטות של הבעלים (D‑500 – D‑514),
# סבב הסדר (v6.92, מפת הדרכים 9ס), S7F266, והעבודה שרצה. מצטבר על daily.json (הגיבוי: daily.json.bak0800_1108).
# usage: DAILY_AT=07:55 python3 study/pages/daily_0800_1108.py && python3 study/pages/daily.py
import json, os, shutil, hashlib, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, 'daily.json')
W = os.path.dirname(os.path.dirname(HERE)); G = W + '/clean_r2b_025637'
B = F + '.bak0800_1108'
if not os.path.exists(B): shutil.copy(F, B)
D = json.load(open(B, encoding='utf-8'))
T = os.environ.get('DAILY_AT', '08:00')
EX = json.load(open(os.environ['DAILY_EXTRA'], encoding='utf-8')) if os.environ.get('DAILY_EXTRA') else {}
def bi(n):
    f = G + '/out/Turbo_City_v1_96_GATE77_%s.html' % n
    return hashlib.sha1(open(f, 'rb').read()).hexdigest()[:12], format(os.path.getsize(f), ',')
LAST = EX.get('last_build', 'S7F266')
bsha, bsz = bi(LAST)
D['updated'] = '08.11.2026 · ' + T; D['plan'] = EX.get('plan', 'v6.92')
D['build'] = '%s · %s · %s — הבנייה האחרונה. הדף הקבוע של הבנייה — בטבלת הדפים למטה' % (LAST, bsha, bsz)
D['next'] = EX.get('next', 'העדכון הבא — 20:00. העבודה ממשיכה בלי לחכות; ההתלבטויות — ב"מחכה לך".')
D['done'] = EX.get('done_top', []) + [
  'הבנייה מחדש מחבילת המסירה — S7F265 ‏(56754fb61661) והתוכנית v6.91 ‏(8078967d1cb5): ‏0 הבדלים.',
  'הבנייה מפוצלת לקבצי מקור (D‑506): ‏75 חלקים לפי אזור ומערכת, עם מעקב גרסאות; החיבור בחצי שנייה במקום כדקה וחצי של 550 טלאים, ו-S7F265 מתחבר זהה בית-בית.',
  'ההחלטות של הבעלים מהלילה נרשמו — D‑500 עד D‑514 — עם ברירות מחדל, בתוכנית ובכרטיס הכללים (כללים 33–37).',
  'סבב הסדר של הביקורת (R-83 – R-87): התוכנית v6.92 — מערכת שלבים אחת (S1–S16 ו-W1–W25), טבלת זמנים מ-8.11 עם השבת והמכסה, "מחכה לך" עם 24 שאלות פתוחות בלבד, "המצב עכשיו" לכל החלטה, פורמט אחד למספרים, שורת "מעודכן עד" בכל ציור; דף "מה תוקן בסבב הסדר".',
  'מפת הדרכים סבב 9ס: D2 החדש והדרך מהמעגל, ההורדה של המלון, האגם ב-B1 ו-B2, ‏S9a כמו שנבנה, סטטוס לכל מגרש מהמשחק, עמודת "היום" של הקווים מהמשחק, קו 4, השלבים עד S16, הצינור במקום המסילה לבית הזיקוק, הרציפים; טבלת התאמה מפה↔משחק — 947 שורות.',
  'S7F266: רציפי E3 לארבעה קרונות (D‑505), מסילת העקיפה לכל אורך E3 (D‑503), הצינור על עמודים גבוהים ב-C5 (D‑504), הכותרות מקבוע אחד, ‏M-BUS-01 במסלול של קו 1. נשלחה כקובץ ופורסמה.',
  'בדיקת סנכרון מורחבת שעוצרת מסירה (R-83 סעיף ט, ‏R-87 סעיף ה).'] + [x for x in D['done'] if x.startswith(('S7F265', 'S7F264'))][:2]
D['work'] = EX.get('work', [])
D['waiting'] = EX.get('waiting', []) + [x for x in D['waiting'] if x.startswith(('הכביש למרינה', 'הדרך החדשה מהמעגל', 'חניון הקיוסק'))]
D['approved'] = {'title': 'ההחלטות של הבעלים בלילה, ומה נעשה איתן',
  'head': ['מה', 'ההחלטה', 'מתי', 'איפה זה עכשיו'],
  'rows': EX.get('approved_rows', [])}
REVX = EX.get('review', {})
for r in D['review']:
    if r['id'] in REVX: r['done'], r['state'] = REVX[r['id']]
known = {r['id'] for r in D['review']}
for rid, sev, what in EX.get('review_new', []):
    if rid not in known:
        d_, s_ = REVX.get(rid, ('', 'פתוח'))
        D['review'].insert(0, {'id': rid, 'sev': sev, 'what': what, 'done': d_, 'state': s_})
D['agent3'] = EX.get('agent3', []) + D['agent3'][:6]
D['quota'] = [D['quota'][0]] + EX.get('quota', [])
D['risks'] = EX.get('risks', []) + D['risks'][:3]
BL = D['builds']
D['builds'] = [[b, *bi(b), st] for b, st in EX.get('builds', [])] + [x for x in BL if x[0] not in dict(EX.get('builds', []))]
PUB = json.load(open(W + '/deliver/published.json', encoding='utf-8'))
last = {}
for x in PUB: last[x['page']] = x
def key(x): d, h = x['at'].split(' '); dd, mm, yy = d.split('.'); return yy + mm + dd + h
pub = sorted((x for x in last.values() if x['at'].startswith('08.11.2026')), key=key, reverse=True)
D['published'] = [['הדוח היומי', 'Turbo_City_Daily_Report_0800_1108_page.html', 'בשורה הבאה של הדוח', '', '8.11 ' + T, 'https://claude.ai/artifact/BBoUF7HSKYqGmv8qZtNDs5']] + \
                 [[x['page'], os.path.basename(x['file']), x['sha1'][:12], format(x['size'], ','), x['at'].replace('08.11.2026 ', '8.11 '), x['url']] for x in pub if x['page'] != 'הדוח היומי']
L = D['links']
for x in pub:
    if not any(y[1] == x['url'] for y in L): L.append([x['page'], x['url'], 'הדף הקבוע (R-75)'])
for y in L:
    if y[1].endswith('1MGssovYKd8VWrx8vxCpiu'): y[2] = 'התוכנית ' + D['plan']
    if y[1].endswith('8VUftq9eJ3z8Nc3ZB4rPcX'): y[2] = 'קובץ המשחק האחרון שנמסר (%s — הקובץ נשלח להורדה)' % LAST
    if y[1].endswith('4oepJZx6JjZcHjTwYxDcNJ'): y[2] = 'מפת הדרכים — סבב 9ס'
json.dump(D, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(D['review']), len(D['published']), D['build'])
