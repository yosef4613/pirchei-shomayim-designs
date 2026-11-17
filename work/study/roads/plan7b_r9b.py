# -*- coding: utf-8 -*-
"""3.11 · סבב 9ב של מפת הדרכים — C5 לפי C5_Options_v2 (הבעלים 13:47 / 13:49): כל השאר כמו בסבב 9 (plan7b_r9).
 · 3 רציפים ישרים, כולם פעילים: כניסה ימינה פנימה משדרת הנמל, פנייה בחצר ורוורס לרציף; יציאה (ב) שמאלה (מזרחה) בפתח בחציון, ברמזור —
   מופע לפי דרישה של J31_42 עם חץ שמאלה, וקו עצירה חדש לתנועה מערבה ממזרח לפתח (לאישורך).
 · השירותים של הנהגים זזים בתוך החצר, לפינה הדרומית-מזרחית ליד הביתן (הכניסה לרציף 1 עוברת במקום שלהם).
    python3 plan7b_r9b.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)
                            + clean_r2b_025637/qa/tmp/signals_r9b.json ו-xw_t_r9b.json (הקבצים של סבב 9 לא נכתבים מחדש)"""
import json, os, sys, runpy, shutil, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
W = '/home/claude/tc/pkg/work'
import plan7b_r9 as R9
import plan7b_r7 as R7
import plan7b_svg as SV
R8B = R9.R8B
C5 = json.load(open(W + '/exp34/c5d5/c5_v2_final.json', encoding='utf-8'))
QA_REAL = R9.QA; QA_TMP = '/tmp/claude-0/-home-claude/7bb7c82b-9a44-5cd6-ab8f-054dc66a801d/scratchpad/qa_r9b'
os.makedirs(QA_TMP, exist_ok=True); R9.QA = QA_TMP                      # round 9's files stay as delivered; round 9ב writes its own names
MED = C5['median']; KRB = C5['kerb']; STOP_X = MED[1] + 12
ASKB = 'ברירת מחדל — לאישורך (13:49: מה שעובר במסלול הסיבוב)'

# the signal of J31_42: a phase on demand for the trucks that leave C5 to the left
for r in R9.SIG9:
    if r['node'] == 'J31_42':
        r['why'] += f"; סבב 9ב: מופע לפי דרישה ליציאה של המשאיות מ-C5 שמאלה (גלאי בשער, חץ ירוק), והתנועה מערבה עוצרת בקו עצירה חדש ב-x {STOP_X}"

_pre9 = R7.pre
def pre(S, DW, it, dw):
    _pre9(S, DW, it, dw)
    by = {i['id']: i for i in S}; bd = {d['id']: d for d in DW}
    t = by['C5-TRUCKS']
    t.update(label='חניון המשאיות — 3 רציפים: כניסה ימינה פנימה, יציאה שמאלה ברמזור (לאישורך)',
             why='סבב 9ב (C5_Options_v2, הבעלים 13:47 / 13:49): 3 רציפים ישרים, כולם פעילים — כניסה ימינה פנימה, פנייה בחצר ורוורס; '
                 f"יציאה שמאלה בפתח בחציון (x {MED[0]}–{MED[1]}), ברמזור. יציאה ימינה עוברת רק מרציף 3.", exit_b=dict(median=MED, kerb=KRB, stop_x=STOP_X))
    if 'C5-WC' in by:
        by['C5-WC'].update(rect=list(C5['wc']), why='סבב 9ב: זזו לפינה הדרומית-מזרחית של החצר, ליד הביתן — מחוץ לכל מסלולי הסיבוב (0.5 מ׳); הכניסה לרציף 1 עוברת במקום הקודם.')
    if 'DW-C5-TRUCKS-S' in bd:
        bd['DW-C5-TRUCKS-S'].update(label='הכניסה והיציאה של המשאיות — פנימה ימינה; החוצה שמאלה (מזרחה), בפתח בחציון וברמזור',
                                    why=f"סבב 9ב (C5_Options_v2): הפתח בשפה x {KRB[0]}–{KRB[1]}; הפתח בחציון x {MED[0]}–{MED[1]}; מופע לפי דרישה של J31_42 (חץ שמאלה); "
                                        'יציאה ימינה (א) — רק מרציף 3, ולכן לא ברירת המחדל.')
    for d_ in R9.DEC9:
        if d_['code'] == 'R9-C5':
            d_.update(code='R9-C5', what=f"C5 (סבב 9ב): 3 רציפים ישרים, כולם פעילים — כניסה ימינה פנימה, פנייה בחצר ורוורס לרציף; יציאה שמאלה (מזרחה) בפתח בחציון x {MED[0]}–{MED[1]}, "
                                         'ברמזור: מופע לפי דרישה של J31_42 עם חץ שמאלה, וקו עצירה חדש לתנועה מערבה; השירותים זזים ליד הביתן',
                      default=ASKB, alt='(א) ימינה — רק רציף 3 יוצא (רציפים 1 ו-2 עולים על הפינה ליד המעבר של J31_42); הדף C5_Options_v2')
R7.pre = pre

_lay9 = SV.label_layout
def label_layout(P_):
    o = _lay9(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ב'; P_['batch'] = '9ב'
    P_['r9b'] = dict(at='3.11.2026', by='הבעלים 13:47 / 13:49', c5=dict(median=MED, kerb=KRB, stop_x=STOP_X, wc=C5['wc'], docks=C5['docks']),
                     why='סבב 9ב: C5 — כניסה ימינה פנימה, יציאה שמאלה ברמזור (C5_Options_v2)')
    return o
SV.label_layout = label_layout

_lots9 = SV.lots_layer
def lots_layer(P_):
    o = _lots9(P_)
    return o.replace('>היציאה — (א) או (ב)<', '>כניסה ימינה, יציאה שמאלה<').replace('>בבדיקה<', '>ברמזור — לאישורך<')
SV.lots_layer = lots_layer

_bus9 = SV.bus_layer
def bus_layer(P_, M_):
    """round 9ב: the opening in the median of the port avenue in front of C5, and the new stop line of the westbound lanes east of it"""
    o = _bus9(P_, M_)
    if not o: return o
    add = (f"<rect x='{MED[0]}' y='4239' width='{MED[1] - MED[0]}' height='22' fill='{SV.STY['arterial'][0]}'/>"
           f"<line x1='{STOP_X}' y1='4164' x2='{STOP_X}' y2='4238' stroke='#ffffff' stroke-width='6'/>")
    k = o.rfind('</g>'); return o[:k] + add + o[k:]
SV.bus_layer = bus_layer

def page_r9b():
    D = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8')); c = D['r9b']['c5']; e = lambda x: html.escape(str(x))
    rows = ''.join(f"<tr><td class='id'>רציף {d['dock']}</td><td>{'עובר' if d['in_ok'] else 'לא עובר'}</td><td>{'עובר' if d['out_ok'] else 'לא עובר'}</td></tr>" for d in c['docks'])
    H = ("<h2>סבב 9ב — C5 (3.11.2026)</h2><p class='small'>לפי הבעלים (13:47 / 13:49) והדף C5_Options_v2: 3 רציפים ישרים, כניסה ויציאה רק משדרת הנמל. "
         f"כולם פעילים: כניסה ימינה פנימה, פנייה בחצר ורוורס לרציף; יציאה שמאלה (מזרחה) בפתח בחציון x {c['median'][0]}–{c['median'][1]}, ברמזור — מופע לפי דרישה של J31_42 עם חץ שמאלה, "
         f"וקו עצירה חדש לתנועה מערבה ב-x {c['stop_x']}. הפתח בשפה x {c['kerb'][0]}–{c['kerb'][1]}. השירותים של הנהגים זזים ליד הביתן. יציאה ימינה עוברת רק מרציף 3. לאישורך.</p>"
         "<div class='wrap'><table><tr><th>רציף</th><th>כניסה ימינה פנימה</th><th>יציאה שמאלה</th></tr>" + rows + "</table></div>")
    p = os.path.join(HERE, 'city_plan.html'); T = open(p, encoding='utf-8').read(); k = T.index("<h2>סבב 9 — מה השתנה")
    open(p, 'w', encoding='utf-8').write(T[:k] + H + T[k:])

if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
    p_ = os.path.join(HERE, 'city_plan.html'); T_ = open(p_, encoding='utf-8').read(); k_ = T_.index("<h2>הבדיקות</h2>")
    open(p_, 'w', encoding='utf-8').write(T_[:k_] + "<h2>סבב 8 — מה השתנה (3.11.2026)</h2><p class='small'>R-69, השדה הסולרי של E4, האוטובוסים (D‑394 / D‑395) והשמות — כמו בסבב 8. S6 (רחוב שער הנמל ב-x 3710) לא נכנס: רחוב שער הנמל חזר ל-x 3850 (הבעלים 09:59 / 11:26).</p>" + T_[k_:])
    R8B.page_r8b()
    R9.page_r9()
    page_r9b()
    for a, b in (('signals_r9.json', 'signals_r9b.json'), ('xw_t_r9.json', 'xw_t_r9b.json')):
        shutil.copyfile(os.path.join(QA_TMP, a), os.path.join(QA_REAL, b))
