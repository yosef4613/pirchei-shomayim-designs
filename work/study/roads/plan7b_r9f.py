# -*- coding: utf-8 -*-
"""3.11 · סבב 9ו של מפת הדרכים — הביקורת 23:16 (אחרי מה שהבעלים מצא ב-J46_16): D‑420 היה שגוי.
 · J46_42 (שדרת המזרח × שדרת הנמל × הכניסה לנמל): לפי הבעלים (11:28) המעבר בזרוע הצפונית נשאר, צמוד לצומת. עכשיו J46_42 הוא צומת T
   רגיל של D‑439: נשארים המעבר הצפוני (משמאל לנהג שיוצא משדרת הנמל) והמעבר המערבי (על הרחוב הצדדי); המעבר הדרומי (PT-E/1, מול שער החניונים) יוצא.
 · שאר הרשת, הציור והבדיקות — בלי שינוי. בדיקת D‑427 עם כלל צומת ה-T — J46_42 בתוכה, בלי החריג.
    python3 plan7b_r9f.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9e as R9E        # round 9ה — its patches (and through it 9ד, 9ג, 9ב, 9) run on import; its __main__ does not
import plan7b_r9d as R9D
import plan7b_r9c as R9C
import plan7b_r9b as R9B
import plan7b_r9 as R9
import plan7b_svg as SV
R7 = R9.R7; R8B = R9.R8B
R9.T_EXC.pop('J46_42', None)    # J46_42 is a T junction of D‑439 like any other
DONE9F = {}

_post9e = R7.post
def post(ctx):
    g = sys._getframe(1).f_globals
    g['__r9f_post'] = _post9e
    items = eval('__r9f_post(__r9f_ctx)', g, {'__r9f_ctx': ctx})
    XW = g['XW']
    back = [x for x in R9.D420 if x not in XW]       # the north crossing that D‑420 took out — back
    XW.extend(back)
    on = sorted(x['seg'] for x in XW if x['node'] == 'J46_42')
    DONE9F.update(north=[x['seg'] for x in back], on=on, t=[r for r in R9.XWT if r['node'] == 'J46_42'])
    for d in R9.DEC9:
        if d['code'] == 'D‑420':
            d['what'] = 'J46_42: המעבר בזרוע הצפונית נשאר, צמוד לצומת (הבעלים 11:28; סבב 9ו — D‑420 של 11:26 היה שגוי); כמו בכל צומת T — המעבר הדרומי (מול שער החניונים) יוצא'
            d['default'] = 'סבב 9ו (הביקורת 23:16)'
    return items
R7.post = post

_chk9e = R7.checks
def checks(ctx, I):
    g = sys._getframe(1).f_globals
    g['__r9f_chk'] = _chk9e
    out = list(eval('__r9f_chk(__r9f_ctx, __r9f_I)', g, {'__r9f_ctx': ctx, '__r9f_I': I}))
    XW = g['XW']; ADJ = g['ADJ']
    on46 = {x['seg'] for x in XW if x['node'] == 'J46_42'}
    n46 = [s_['id'] for o_, s_ in ADJ.get('J46_42', []) if R9._arm(g, 'J46_42', s_)[1] < -.9]
    s46 = [s_['id'] for o_, s_ in ADJ.get('J46_42', []) if R9._arm(g, 'J46_42', s_)[1] > .9]
    for i, c in enumerate(out):
        if isinstance(c, tuple) and str(c[0]).startswith('D‑427 עם כלל צומת ה-T'):
            det = str(c[2]); k = det.find('J46_42 — בזרוע הצפונית אין מעבר')
            rest = det[:k].rstrip(' ·') if k >= 0 else det
            bad = [b for b in (det.split(' · ', 1)[1].split('; ') if ' · ' in det[k:] else []) if not b.startswith('J46_42')] if k >= 0 else []
            ok46 = bool(n46) and n46[0] in on46 and not (s46 and s46[0] in on46) and len(on46) == 2
            if not ok46: bad.append(f"J46_42: {sorted(on46)}")
            out[i] = (c[0], (c[1] or not [b for b in bad if not b.startswith('J46_42')]) and ok46,
                      rest + f" J46_42 — צומת T כמו כל צומת (סבב 9ו, הבעלים 11:28): נשארו {', '.join(sorted(on46))}" + (' · ' + '; '.join(bad) if bad else '')) + tuple(c[3:])
    return out
R7.checks = checks

_lay9e = SV.label_layout
def label_layout(P_):
    o = _lay9e(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ו'; P_['batch'] = '9ו'
    return o
SV.label_layout = label_layout

def page_r9f():
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ו'; P_['batch'] = '9ו'
    xw46 = [x for x in P_['bus']['crosswalks'] if x['node'] == 'J46_42']
    P_['r9f'] = dict(at='3.11.2026', by='הביקורת 23:16 · הבעלים 11:28', why='סבב 9ו: J46_42 — המעבר הצפוני נשאר (D‑420 היה שגוי); המעבר הדרומי יוצא לפי D‑439',
                     j46_42=[x['seg'] for x in xw46], north_back=DONE9F.get('north'), t_row=DONE9F.get('t'))
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); T = open(ph, encoding='utf-8').read()
    H = ("<h2>סבב 9ו — מה השתנה (3.11.2026)</h2><p class='small'>לפי הבעלים (11:28) והביקורת (23:16): בצומת J46_42 (שדרת המזרח × שדרת הנמל × הכניסה לנמל) "
         "המעבר בזרוע הצפונית נשאר, צמוד לצומת — ההחלטה D‑420 של 11:26 (\"בזרוע הצפונית לא יהיה מעבר\") הייתה שגויה. "
         "עכשיו J46_42 הוא צומת T רגיל לפי כלל צומת ה-T (D‑439): נשארים המעבר הצפוני (משמאל לנהג שיוצא משדרת הנמל) והמעבר המערבי (על הרחוב הצדדי), "
         "והמעבר הדרומי, מול שער החניונים, יוצא. המעברים ב-J46_42 עכשיו: " + ', '.join(sorted(x['seg'] for x in xw46)) + ". שאר הרשת, הציור והבדיקות — בלי שינוי.</p>")
    k = T.index("<h2>סבב 9ה"); T = T[:k] + H + T[k:]
    T = T.replace('תוכנית הדרכים של כל העיר — סבב 9ה', 'תוכנית הדרכים של כל העיר — סבב 9ו')
    T = T.replace('מחוץ לכלל: J46_42 — בזרוע הצפונית אין מעבר כלל (D‑420); ', 'מחוץ לכלל: ')
    open(ph, 'w', encoding='utf-8').write(T)
    print('r9f J46_42', sorted(x['seg'] for x in xw46), 'north back', DONE9F.get('north'))
    assert len(xw46) == 2

if __name__ == '__main__':
    os.chdir(HERE)
    # the main of round 9ה, as it is (the build, the page, the note of round 8, the pages of 8ב … 9ה), and then 9ו
    src = open(os.path.join(HERE, 'plan7b_r9e.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    import textwrap; code = textwrap.dedent('\n'.join(body))
    exec(compile(code, 'plan7b_r9e.py:__main__', 'exec'), dict(globals(), page_r9e=R9E.page_r9e))
    page_r9f()
