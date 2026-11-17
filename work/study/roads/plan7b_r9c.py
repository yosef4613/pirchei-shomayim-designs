# -*- coding: utf-8 -*-
"""3.11 · סבב 9ג של מפת הדרכים — הבעלים 14:21 (עם צילום): ברחוב התעשייה בצפון החניון (CL-T/3) המפה ציירה 2 נתיבים בכל כיוון,
והמפרצים של ST-12 נראו בתוך נתיב הנסיעה. התיקון — בציור בלבד, כל השאר כמו בסבב 9ב:
 · החתך של 'art21' (2+1): נתיב אחד מערבה (צפון), חציון, 2 נתיבים מזרחה (דרום) — כביש של 3 × 3.9 + 2.0 = 13.7 מ׳, מדרכות של 2.5 מ׳ (18.7 מ׳ בסך הכול);
   החציון והקו בין שני הנתיבים הדרומיים במקום האמיתי שלהם (לא באמצע).
 · המפרצים של ST-12 יושבים עכשיו על השפות האמיתיות (צפון y ‏3312, דרום y ‏3449) וחתוכים לתוך המדרכה, כמו בכל התחנות במפה.
    python3 plan7b_r9c.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)
                            הקבצים של סבב 9 ו-9ב ב-qa/tmp לא נכתבים מחדש (אין שינוי ברמזורים ובמעברים)."""
import json, os, sys, runpy, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9b as R9B          # round 9ב — its patches (C5) run on import; its __main__ does not
import plan7b_r9 as R9
import plan7b_r7 as R7
import plan7b_svg as SV
R8B = R9.R8B

# ---------------------------------------------------------------- the drawing of 'art21': 1 lane north, the median, 2 lanes south
_geom = SV.geom
def geom(CLS, cls, kind='road', lanes=None):
    if cls != 'art21': return _geom(CLS, cls, kind, lanes)
    c = CLS[cls]; L = c['lane_m'] * 10; med = c['median_m'] * 10
    nl, nr = 1, 2                                   # the left of the drawing direction (west → east) is north: 1 westbound lane; the right — 2 eastbound
    cw = (nl + nr) * L + med; tw = c['halfW'] * 2   # 137 / 187 px
    med_off = cw / 2 - nl * L - med / 2             # + = left (north) of the centre line: 19.5 px
    line_off = cw / 2 - nl * L - med - L            # the dashed line between the two eastbound lanes: −29.5 px
    return dict(cw=cw, tw=tw, med=0, med_w=med, med_off=med_off, lines=[(line_off, 1)], arrow=False, st='bridge' if kind == 'bridge' else 'arterial')
SV.geom = geom

_road_parts = SV.road_parts
def road_parts(pid, p, g, cut=(0, 0), caps=()):
    base, top, lane = _road_parts(pid, p, g, cut, caps)
    if g.get('med_off') is not None and g.get('med_w'):
        q = SV.trim(p, *cut) if (cut[0] or cut[1]) else p
        if q:
            m = f"<polyline points='{SV.pts(SV.offset(q, g['med_off']))}' class='rk' stroke='{SV.MED}' stroke-width='{SV.f1(g['med_w'])}'/>"
            k = lane.index('>') + 1; lane = lane[:k] + m + lane[k:]
    return base, top, lane
SV.road_parts = road_parts

# ---------------------------------------------------------------- the title and the record
_lay9b = SV.label_layout
def label_layout(P_):
    o = _lay9b(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ג'; P_['batch'] = '9ג'
    P_['r9c'] = dict(at='3.11.2026', by='הבעלים 14:21',
                     why='סבב 9ג: רחוב התעשייה בצפון החניון (CL-T/3) מצויר 2+1 — נתיב אחד מערבה ו-2 מזרחה; המפרצים של ST-12 על השפות האמיתיות')
    if isinstance(P_.get('classes'), dict) and 'art21' in P_['classes']:
        P_['classes']['art21'].update(lanesL=1, lanesR=2, drawn_cw_m=13.7,
                                      note9c='בציור: נתיב אחד מערבה (צפון), חציון 2.0, שני נתיבים מזרחה (דרום); השדה dirN נשאר 2 בגלל החישובים של סבב 9 — הקובע הוא lanes = 2+1')
    return o
SV.label_layout = label_layout

def page_r9c():
    H = ("<h2>סבב 9ג — מה השתנה (3.11.2026)</h2><p class='small'>לפי הבעלים (14:21, עם צילום): ברחוב התעשייה בצפון חניון הלילה המפה ציירה 2 נתיבים בכל כיוון, "
         "והמפרצים של התחנה נראו בתוך נתיב הנסיעה. עכשיו: נתיב אחד מערבה (בצד הצפוני), חציון, ו-2 נתיבים מזרחה (בצד הדרומי) — כביש של 13.7 מ׳ ומדרכות של 2.5 מ׳. "
         "שני המפרצים של התחנה יושבים על השפות וחתוכים לתוך המדרכה, כמו בכל התחנות במפה. כל השאר — כמו בסבב 9ב.</p>")
    p = os.path.join(HERE, 'city_plan.html'); T = open(p, encoding='utf-8').read(); k = T.index("<h2>סבב 9ב — C5")
    open(p, 'w', encoding='utf-8').write(T[:k] + H + T[k:])

if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
    p_ = os.path.join(HERE, 'city_plan.html'); T_ = open(p_, encoding='utf-8').read(); k_ = T_.index("<h2>הבדיקות</h2>")
    open(p_, 'w', encoding='utf-8').write(T_[:k_] + "<h2>סבב 8 — מה השתנה (3.11.2026)</h2><p class='small'>R-69, השדה הסולרי של E4, האוטובוסים (D‑394 / D‑395) והשמות — כמו בסבב 8. S6 (רחוב שער הנמל ב-x 3710) לא נכנס: רחוב שער הנמל חזר ל-x 3850 (הבעלים 09:59 / 11:26).</p>" + T_[k_:])
    R8B.page_r8b()
    R9.page_r9()
    R9B.page_r9b()
    page_r9c()
