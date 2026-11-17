# -*- coding: utf-8 -*-
"""3.11 · סבב 9ד של מפת הדרכים — הביקורת 15:40 (R-77 (4)): נוסח בלבד, בלי שינוי בציור, ברשת ובבדיקות:
 · כלל R-15 אחד: "לפחות 60 מ׳ בין צמתים לאורך כל דרך; בעורק לפחות 75 מ׳ בין רמזורים" — עם רשימת החריגות בבדיקות (היום בכללים כתוב 90).
 · המסוף E3: "6 מפרצי עלייה ו-10 מקומות המתנה (6 מאחורי האיים, 4 בנתיב ההמתנה)" במקום "12 מפרצים ו-4 מקומות המתנה" — אותם 16 מקומות;
   המספרים מחושבים מהנתונים של סבב 9 (bus.terminal.r9), לא מוקלדים.
    python3 plan7b_r9d.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9c as R9C          # round 9ג — its patches run on import (and through it 9ב, 9); its __main__ does not
import plan7b_r9b as R9B
import plan7b_r9 as R9
import plan7b_svg as SV
R8B = R9.R8B

R15_OLD = 'לפחות 60 מ׳ בין צמתים לאורך כל דרך; בעורק לפחות 90 מ׳ בין רמזורים'
R15_NEW = 'לפחות 60 מ׳ בין צמתים לאורך כל דרך; בעורק לפחות 75 מ׳ בין רמזורים — החריגות ברשימה אחת, בבדיקה של R-15 (הרמזורים הקרובים מתואמים בגל ירוק)'

_lay9c = SV.label_layout
def label_layout(P_):
    o = _lay9c(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ד'; P_['batch'] = '9ד'
    P_['r9d'] = dict(at='3.11.2026', by='הביקורת 15:40 (R-77)',
                     why='סבב 9ד: נוסח בלבד — כלל R-15 אחד (75 מ׳ בין רמזורים בעורק, עם רשימת החריגות), והמסוף E3 — 6 מפרצי עלייה ו-10 מקומות המתנה')
    return o
SV.label_layout = label_layout

def terminal_words(P_):
    r9 = P_['bus']['terminal']['r9']
    nb, np_, nh = len(r9['board']), len(r9['park']), len(r9['holds'])
    return nb, np_ + nh, f'{nb} מפרצי עלייה ו-{np_ + nh} מקומות המתנה', f'{np_} מאחורי האיים, {nh} בנתיב ההמתנה'

def fix_texts(T, P_):
    """the old words → the new ones; every replacement is counted (an old phrase left behind fails)"""
    nb, nw, short, split = terminal_words(P_)
    nbays = len(P_['bus']['terminal']['bays'])
    REP = [(R15_OLD, R15_NEW),
           (f'מסוף האוטובוסים של E3 — {nbays} מפרצים ו-4 מקומות המתנה', f'מסוף האוטובוסים של E3 — {short}'),
           (f'(12 מפרצים ו-4 מקומות המתנה)', f'({short})'),
           (f'מסוף האוטובוסים של E3 — 12 מפרצים ומקומות המתנה', f'מסוף האוטובוסים של E3 — {short}'),
           ('מסוף E3 — לפחות 12 מפרצים (שניים לכל קו בבת אחת) ושטח המתנה מסומן',
            f'מסוף E3 — {short} ({split}): {nb + nw} מקומות, שניים לכל קו בבת אחת, ושטח המתנה מסומן'),
           ('בשני רציפים (6 קווים × 2)', f'בשני רציפים — {nb} לעלייה (אחד לכל קו, בצבע של הקו) ו-{nbays - nb} לחניה מאחורי האיים')]
    cnt = {}
    for a, b in REP:
        cnt[a] = T.count(a); T = T.replace(a, b)
    return T, cnt

def page_r9d():
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    J = json.dumps(P_, ensure_ascii=False, indent=1); J, cj = fix_texts(J, P_)
    P2 = json.loads(J); P2['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ד'; P2['batch'] = '9ד'
    P2['r9d'] = dict(at='3.11.2026', by='הביקורת 15:40 (R-77)', why='נוסח בלבד: כלל R-15 אחד, והמסוף E3 — ' + terminal_words(P_)[2])
    json.dump(P2, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); T = open(ph, encoding='utf-8').read(); T, ch = fix_texts(T, P_)
    nb, nw, short, split = terminal_words(P_)
    H = ("<h2>סבב 9ד — מה השתנה (3.11.2026)</h2><p class='small'>לפי הביקורת (15:40, ‏R-77): נוסח בלבד — בלי שינוי בציור, ברשת ובבדיקות. "
         "כלל R-15 כתוב עכשיו פעם אחת: לפחות 60 מ׳ בין צמתים לאורך כל דרך, ובעורק לפחות 75 מ׳ בין רמזורים; החריגות — ברשימה אחת, בבדיקה של R-15 "
         f"(הרמזורים הקרובים מתואמים בגל ירוק). המסוף E3: {short} ({split}) — אותם {nb + nw} מקומות, בנוסח של סבב 9.</p>")
    k = T.index("<h2>סבב 9ג"); T = T[:k] + H + T[k:]
    T = T.replace('תוכנית הדרכים של כל העיר — סבב 9ג', 'תוכנית הדרכים של כל העיר — סבב 9ד')
    open(ph, 'w', encoding='utf-8').write(T)
    left = [a for a in (R15_OLD, '12 מפרצים ו-4 מקומות המתנה', '12 מפרצים ומקומות המתנה', 'לפחות 12 מפרצים') if a in T or a in json.dumps(P2, ensure_ascii=False)]
    print('r9d json', cj); print('r9d html', ch); print('left', left)
    assert not left, left

if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
    p_ = os.path.join(HERE, 'city_plan.html'); T_ = open(p_, encoding='utf-8').read(); k_ = T_.index("<h2>הבדיקות</h2>")
    open(p_, 'w', encoding='utf-8').write(T_[:k_] + "<h2>סבב 8 — מה השתנה (3.11.2026)</h2><p class='small'>R-69, השדה הסולרי של E4, האוטובוסים (D‑394 / D‑395) והשמות — כמו בסבב 8. S6 (רחוב שער הנמל ב-x 3710) לא נכנס: רחוב שער הנמל חזר ל-x 3850 (הבעלים 09:59 / 11:26).</p>" + T_[k_:])
    R8B.page_r8b()
    R9.page_r9()
    R9B.page_r9b()
    R9C.page_r9c()
    page_r9d()
