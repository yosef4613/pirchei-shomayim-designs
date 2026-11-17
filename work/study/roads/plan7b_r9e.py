# -*- coding: utf-8 -*-
"""3.11 · סבב 9ה של מפת הדרכים — הבעלים 20:59 ("הצבעים של התחנות ברצפה לא תואמים לצבע הקו באמת"): צבעי הקווים במפה = צבעי הקווים במשחק.
 · קווים 1–4: הצבעים של המשחק (BUS_LINE_COLORS — אותו מקור של שלט התחנה, מפת הקווים והאוטובוס): 1 ‏#2f6fd0, ‏2 ‏#28a66a, ‏3 ‏#e8892a, ‏4 ‏#aa71dc.
 · קווים 5 ו-6 (עוד לא במשחק): צבעים חדשים שלא דומים לאף קו — 5 ‏#d0342c (אדום), ‏6 ‏#12a5a8 (טורקיז) — לאישורך.
 בלי שינוי ברשת, בציור ובבדיקות; רק הצבעים.
    python3 plan7b_r9e.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_net as NET
import plan7b_r9d as R9D          # round 9ד — its patches (and through it 9ג, 9ב, 9) run on import; its __main__ does not
import plan7b_r9c as R9C
import plan7b_r9b as R9B
import plan7b_r9 as R9
import plan7b_svg as SV
R8B = R9.R8B
GAME = {'1': '#2f6fd0', '2': '#28a66a', '3': '#e8892a', '4': '#aa71dc', '5': '#d0342c', '6': '#12a5a8'}
OLD = {}
for ln in NET.ROUTES['bus']:
    OLD[ln['id']] = ln['color']; ln['color'] = GAME[ln['id']]

_lay9d = SV.label_layout
def label_layout(P_):
    o = _lay9d(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ה'; P_['batch'] = '9ה'
    return o
SV.label_layout = label_layout

def page_r9e():
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ה'; P_['batch'] = '9ה'
    P_['r9e'] = dict(at='3.11.2026', by='הבעלים 20:59', why='סבב 9ה: צבעי הקווים במפה כמו במשחק (1–4); לקווים 5 ו-6 צבעים חדשים', old=OLD, new=GAME)
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); T = open(ph, encoding='utf-8').read()
    rows = ''.join(f"<tr><td>קו {k}</td><td><span style='display:inline-block;width:14px;height:14px;background:{OLD[k]};vertical-align:-2px'></span> {OLD[k]}</td>"
                   f"<td><span style='display:inline-block;width:14px;height:14px;background:{GAME[k]};vertical-align:-2px'></span> {GAME[k]}</td></tr>" for k in sorted(GAME))
    H = ("<h2>סבב 9ה — מה השתנה (3.11.2026)</h2><p class='small'>לפי הבעלים (20:59): צבעי הקווים במפה הם עכשיו הצבעים של המשחק — אותו צבע בשלט התחנה, במפרץ במסוף, במפת הקווים ובאוטובוס. "
         "לקווים 5 ו-6, שעוד לא במשחק, נבחרו צבעים שלא דומים לאף קו אחר (לאישורך). הרשת, הציור והבדיקות — בלי שינוי.</p>"
         "<table><tr><th>הקו</th><th>לפני</th><th>עכשיו</th></tr>" + rows + "</table>")
    k = T.index("<h2>סבב 9ד"); T = T[:k] + H + T[k:]
    T = T.replace('תוכנית הדרכים של כל העיר — סבב 9ד', 'תוכנית הדרכים של כל העיר — סבב 9ה')
    T = T.replace('.sw-bus{background:linear-gradient(90deg,#1f5fd1 0 33%,#0f8f8a 33% 66%,#2e9e3e 66%)}', '.sw-bus{background:linear-gradient(90deg,#2f6fd0 0 33%,#28a66a 33% 66%,#e8892a 66%)}')
    open(ph, 'w', encoding='utf-8').write(T)
    left = [c for c in OLD.values() if c in json.dumps(P_.get('routes'), ensure_ascii=False)]
    print('r9e colors', GAME, 'old left in routes', left); assert not left

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
    R9D.page_r9d()
    page_r9e()
