# -*- coding: utf-8 -*-
"""4.11 · סבב 9ח של מפת הדרכים — ההורדה של המלון ב-A5 הפוכה (S7F238, ‏p577d … p577l): ההסעה והמונית האמיתיות נוסעות בכיוון השעון, רק פניות ימינה ברמזורים,
ולכן נתיב ההורדה צפונה: הכניסה מדרום (A5-CC-HOTEL-S במשחק, ‏x 532–552, ‏y 3614–3650) והיציאה לצפון (A5-CC-HOTEL-N, ‏y 3492–3528).
 · במפה המזהים נשארים DW-A5-HOTEL-IN (כניסה) ו-DW-A5-HOTEL-OUT (יציאה) — רק המקום והכיוון מתחלפים.
 · שאר הרשת, הציור והבדיקות — בלי שינוי.
    python3 plan7b_r9h.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, runpy, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9g as R9G        # round 9ז — its patches (and through it 9ו … 9) run on import, and its driveways are in plan7b_sites; its __main__ does not
import plan7b_sites as ST
import plan7b_svg as SV
WHY = ('הבעלים 4.11 00:18 — כניסה של מלון אמיתי; במשחק מ-S7F238 (p577d … p577l): ההסעה והמונית נוסעות בכיוון השעון, רק פניות ימינה ברמזורים, '
       'ולכן נתיב ההורדה צפונה — הכניסה מדרום והיציאה לצפון; בלי מעבר (D‑427), המדרכה ממשיכה.')
SET = {'DW-A5-HOTEL-IN': dict(at=(542, 3632), to=[(502, 3632), (502, 3576), (460, 3576)], label='הכניסה להורדה של המלון (מדרום)', why=WHY),
       'DW-A5-HOTEL-OUT': dict(at=(542, 3510), to=[(502, 3576), (502, 3510)], label='היציאה מההורדה של המלון (לצפון)', why=WHY)}
for d in ST.DW:
    if d['id'] in SET: d.update(SET[d['id']])
assert sum(1 for d in ST.DW if d['id'] in SET) == 2

_lay9g = SV.label_layout
def label_layout(P_):
    o = _lay9g(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ח'; P_['batch'] = '9ח'
    return o
SV.label_layout = label_layout

def page_r9h():
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ח'; P_['batch'] = '9ח'
    got = {d['id']: d for d in P_['driveways'] if d['id'] in SET}
    P_['r9h'] = dict(at='4.11.2026', by='S7F238 (p577d … p577l)', why='סבב 9ח: נתיב ההורדה של המלון צפונה — הכניסה מדרום, היציאה לצפון',
                     moved={k: dict(at=v['at'], to_junction_m=v.get('to_junction_m')) for k, v in got.items()})
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); T = open(ph, encoding='utf-8').read()
    rows = ''.join(f"<li>{v['id']} — {v['label']}: על {v['road']}, {v.get('to_junction_m')} מ׳ מהצומת הקרוב, נתיב אחד</li>" for v in got.values())
    H = ("<h2>סבב 9ח — מה השתנה (4.11.2026)</h2><p class='small'>ההורדה של המלון ב-A5 הפוכה: במשחק (S7F238) ההסעה והמונית האמיתיות נוסעות בכיוון השעון, "
         "ורק פונות ימינה ברמזורים, ולכן נתיב ההורדה מתחת לגגון נוסע צפונה — נכנסים מהפתח הדרומי ויוצאים בפתח הצפוני. "
         "המזהים במפה נשארו (DW-A5-HOTEL-IN לכניסה, DW-A5-HOTEL-OUT ליציאה); רק המקום והכיוון התחלפו. שאר הרשת, הציור והבדיקות — בלי שינוי.</p><ul class='small'>" + rows + "</ul>")
    k = T.index("<h2>סבב 9ז"); T = T[:k] + H + T[k:]
    T = T.replace('תוכנית הדרכים של כל העיר — סבב 9ז', 'תוכנית הדרכים של כל העיר — סבב 9ח')
    open(ph, 'w', encoding='utf-8').write(T)
    print('r9h moved', {k: (v['at'], v.get('to_junction_m')) for k, v in got.items()})
    assert len(got) == 2 and got['DW-A5-HOTEL-IN']['at'][1] > got['DW-A5-HOTEL-OUT']['at'][1]

if __name__ == '__main__':
    os.chdir(HERE)
    # the main of round 9ז, as it is (it runs 9ו's main and its own page), in 9ז's own globals, and then 9ח
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    code = textwrap.dedent('\n'.join(body))
    exec(compile(code, 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    page_r9h()
