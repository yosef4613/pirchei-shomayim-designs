# -*- coding: utf-8 -*-
"""4.11 · סבב 9ט של מפת הדרכים — ההורדה של המלון ב-A5 חוזרת דרומה (הבעלים 11:26, עם צילום):
"הכיוון לא נכון — זה צריך להיות עם הזרימה של הצד של הכביש שיורד למטה, וגם לא צריך לעלות על המדרכה; צריך להיות כניסה ויציאה לרכבים".
 · הצד של LC-A5 שליד המלון (המערבי) זורם דרומה, ולכן נתיב ההורדה תחת הגגון זורם דרומה: הכניסה בפתח הצפוני (x 532–552, ‏y 3492–3528),
   בפנייה ימינה מהנתיב הדרומי, והיציאה בפתח הדרומי (y 3614–3650), בפנייה ימינה חזרה אליו. זה המקום והכיוון של סבב 9ז; סבב 9ח (צפונה) בוטל.
 · כל פתח — כניסת רכב אמיתית בנתיב אחד, כמו שאר הכניסות בעיר; בלי מעבר (D‑427), המדרכה ממשיכה עם שפה מונמכת; נתיב ההורדה כולו בתוך המגרש.
 · שאר הרשת, הציור והבדיקות — בלי שינוי. הסעיף של סבב 9ח נשאר בדף כהיסטוריה (נלקח מהדף ומהנתונים של 9ח לפני ההרצה).
    python3 plan7b_r9i.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9h as R9H        # round 9ח — on import it runs 9ז … 9 and its own (northbound) swap; its __main__ does not
import plan7b_r9g as R9G
import plan7b_sites as ST
import plan7b_svg as SV
WHY = ('הבעלים 4.11 11:26 — ההורדה זורמת עם הצד הקרוב של LC-A5, שזורם דרומה: נכנסים בפתח הצפוני ויוצאים בפתח הדרומי, '
       'שתיהן בפנייה ימינה; כניסות רכב אמיתיות, בלי מעבר (D‑427), המדרכה ממשיכה; סבב 9ח (צפונה) בוטל.')
SET = {'DW-A5-HOTEL-IN': dict(at=(542, 3510), to=[(502, 3510), (502, 3576), (460, 3576)], label='הכניסה להורדה של המלון (מצפון)', why=WHY),
       'DW-A5-HOTEL-OUT': dict(at=(542, 3632), to=[(502, 3576), (502, 3632)], label='היציאה מההורדה של המלון (לדרום)', why=WHY)}
for d in ST.DW:
    if d['id'] in SET: d.update(SET[d['id']])
assert sum(1 for d in ST.DW if d['id'] in SET) == 2

TITLE = 'תוכנית הדרכים של כל העיר — סבב 9ט'
_lay = SV.label_layout
def label_layout(P_):
    o = _lay(P_)
    P_['title'] = TITLE; P_['batch'] = '9ט'
    return o
SV.label_layout = label_layout

def keep_9h():
    """the 9ח record and page section, as they are now (before this run rebuilds the files)"""
    P_ = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8'))
    T = open(os.path.join(HERE, 'city_plan.html'), encoding='utf-8').read()
    a = T.index('<h2>סבב 9ח'); b = T.index('<h2>סבב 9ז')
    rec = P_['r9h']; assert rec['moved']['DW-A5-HOTEL-IN']['at'][1] > rec['moved']['DW-A5-HOTEL-OUT']['at'][1]
    return rec, P_.get('r9i'), T[a:b]

def page_r9i(rec9h, sec9h):
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = TITLE; P_['batch'] = '9ט'
    got = {d['id']: d for d in P_['driveways'] if d['id'] in SET}
    P_['r9h'] = rec9h
    P_['r9i'] = dict(at='4.11.2026', by='הבעלים 11:26', why='סבב 9ט: נתיב ההורדה של המלון דרומה, עם הצד הקרוב של LC-A5 — הכניסה מצפון, היציאה לדרום',
                     moved={k: dict(at=v['at'], to_junction_m=v.get('to_junction_m')) for k, v in got.items()})
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); T = open(ph, encoding='utf-8').read()
    rows = ''.join(f"<li>{v['id']} — {v['label']}: על {v['road']}, {v.get('to_junction_m')} מ׳ מהצומת הקרוב, נתיב אחד</li>" for v in got.values())
    H = ("<h2>סבב 9ט — מה השתנה (4.11.2026)</h2><p class='small'>הבעלים 11:26: ההורדה של המלון ב-A5 זורמת עם הצד של LC-A5 שליד המלון, "
         "שזורם דרומה — נכנסים בפתח הצפוני ויוצאים בפתח הדרומי, שתיהן בפנייה ימינה. סבב 9ח, שהפך אותה צפונה לפי מה שנבנה, בוטל. "
         "כל פתח הוא כניסת רכב אמיתית בנתיב אחד, כמו שאר הכניסות בעיר: בלי מעבר (D‑427), המדרכה ממשיכה עם שפה מונמכת, "
         "ונתיב ההורדה כולו בתוך המגרש של המלון. שאר הרשת, הציור והבדיקות — בלי שינוי.</p><ul class='small'>" + rows + "</ul>")
    k = T.index('<h2>סבב 9ז'); T = T[:k] + H + sec9h + T[k:]
    for old in ('תוכנית הדרכים של כל העיר — סבב 9ז', 'תוכנית הדרכים של כל העיר — סבב 9ח'):
        T = T.replace(old, TITLE)
    open(ph, 'w', encoding='utf-8').write(T)
    print('r9i moved', {k: (v['at'], v.get('to_junction_m')) for k, v in got.items()})
    assert len(got) == 2 and got['DW-A5-HOTEL-IN']['at'][1] < got['DW-A5-HOTEL-OUT']['at'][1]
    assert T.count('<h2>סבב 9ט') == 1 and T.count('<h2>סבב 9ח') == 1 and T.count('<h2>סבב 9ז') == 1

if __name__ == '__main__':
    os.chdir(HERE)
    rec9h, prev9i, sec9h = keep_9h()
    if prev9i is not None:     # a re-run: the files are already 9ט; the 9ח section and record were kept in them
        pass
    # the main of round 9ז, as it is (it runs 9ו's main and its own page), in 9ז's own globals — with this round's driveways in ST.DW
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    page_r9i(rec9h, sec9h)
