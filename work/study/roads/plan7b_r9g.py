# -*- coding: utf-8 -*-
"""4.11 · סבב 9ז של מפת הדרכים — הפתחים החדשים שבמשחק (S7F232, ‏S7F237):
 · B4 — היציאה המזרחית של שוק העיר לרחוב LC-B (הבעלים 3.11 23:43; ‏p576_b4exit ב-S7F232): הפתח במשחק ב-x 1702–1722, ‏y 3287–3337, על המדרכה המערבית של LC-B.
 · A5 — כניסת המלון (הבעלים 4.11 00:18; ‏p577_a5pol ב-S7F237): נתיב הורדה חד-סטרי מתחת לגגון, כניסה מצפון ויציאה מדרום (D‑427).
   יוצא DW-A5-HOTEL; נכנסים DW-A5-HOTEL-IN (x 532–552, ‏y 3492–3528) ו-DW-A5-HOTEL-OUT (x 532–552, ‏y 3614–3650); נתיב ההורדה 484–520 × 3500–3652.
   החניון הציבורי מצפון לתחנת המשטרה (770–930 × 3468–3552) — דרך הפתח הקיים DW-A5-POL.
 · שאר הרשת, הציור והבדיקות — בלי שינוי.
    python3 plan7b_r9g.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete)"""
import json, os, sys, runpy, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan7b_r9f as R9F        # round 9ו — its patches (and through it 9ה … 9) run on import; its __main__ does not
import plan7b_sites as ST       # after the rounds' patches (they change what the sites add); its import appends B4 / B3 / C3 (plan7b_zones6.add)
import plan7b_svg as SV
WHY_B4 = 'הבעלים 3.11 23:43 — "גם לא תוקן היציאה המזרחית לרחוב במכולת שוק העיר ב-B4"; במשחק מ-S7F232 (p576_b4exit), הפתח ב-x 1702–1722, ‏y 3287–3337.'
WHY_A5 = 'הבעלים 4.11 00:18 — כניסה של מלון אמיתי מתחת לגגון; במשחק מ-S7F237 (p577_a5pol): נתיב הורדה חד-סטרי, כניסה מצפון ויציאה מדרום, בלי מעבר (D‑427), המדרכה ממשיכה.'
OUT = {'DW-A5-HOTEL'}
NEW = [dict(zone='B4', id='DW-B4-MKT-E', road='LC-B', at=(1740, 3312), label='היציאה המזרחית של שוק העיר', why=WHY_B4, to=(1668, 3300), lanes='1'),   # the build snaps the mouth to y 3300 (the end of the LC-B segment); the stub stays straight
       dict(zone='A5', id='DW-A5-HOTEL-IN', road='LC-A5', at=(542, 3510), label='הכניסה להורדה של המלון (מצפון)', why=WHY_A5, to=[(502, 3510), (502, 3576), (460, 3576)], lanes='1'),   # the last stretch — the lobby under the canopy (456–478 × 3544–3606)
       dict(zone='A5', id='DW-A5-HOTEL-OUT', road='LC-A5', at=(542, 3632), label='היציאה מההורדה של המלון (לדרום)', why=WHY_A5, to=[(502, 3576), (502, 3632)], lanes='1')]
ST.DW[:] = [d for d in ST.DW if d['id'] not in OUT and d['id'] not in {n['id'] for n in NEW}] + NEW

_lay9f = SV.label_layout
def label_layout(P_):
    o = _lay9f(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ז'; P_['batch'] = '9ז'
    return o
SV.label_layout = label_layout

def page_r9g():
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9ז'; P_['batch'] = '9ז'
    got = {d['id']: d for d in P_['driveways'] if d['id'] in {n['id'] for n in NEW}}
    gone = [d['id'] for d in P_['driveways'] if d['id'] in OUT]
    P_['r9g'] = dict(at='4.11.2026', by='הבעלים 3.11 23:43, ‏4.11 00:18', why='סבב 9ז: הפתחים החדשים שבמשחק — היציאה של שוק העיר ב-B4, נתיב ההורדה של המלון ב-A5',
                     added={k: dict(at=v['at'], to_junction_m=v.get('to_junction_m'), lanes=v['lanes']) for k, v in got.items()}, removed=sorted(OUT))
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); T = open(ph, encoding='utf-8').read()
    rows = ''.join(f"<li>{v['id']} — {v['label']}: על {v['road']}, {v.get('to_junction_m')} מ׳ מהצומת הקרוב, נתיב אחד</li>" for v in got.values())
    H = ("<h2>סבב 9ז — מה השתנה (4.11.2026)</h2><p class='small'>הפתחים החדשים שכבר במשחק נכנסו למפה. "
         "ב-B4: היציאה המזרחית של שוק העיר לרחוב LC-B (הבעלים 3.11 23:43; במשחק מ-S7F232). "
         "ב-A5: כניסת המלון — נתיב הורדה חד-סטרי מתחת לגגון, כניסה מצפון ויציאה מדרום, בלי מעבר חצייה (D‑427), והמדרכה ממשיכה (הבעלים 4.11 00:18; במשחק מ-S7F237). "
         "הפתח הישן DW-A5-HOTEL יצא. החניון הציבורי החדש מצפון לתחנת המשטרה משתמש בפתח הקיים DW-A5-POL. שאר הרשת, הציור והבדיקות — בלי שינוי.</p><ul class='small'>" + rows + "</ul>")
    k = T.index("<h2>סבב 9ו"); T = T[:k] + H + T[k:]
    T = T.replace('תוכנית הדרכים של כל העיר — סבב 9ו', 'תוכנית הדרכים של כל העיר — סבב 9ז')
    open(ph, 'w', encoding='utf-8').write(T)
    print('r9g added', {k: (v['at'], v.get('to_junction_m')) for k, v in got.items()}, 'removed', gone or sorted(OUT))
    assert len(got) == 3 and not gone

if __name__ == '__main__':
    os.chdir(HERE)
    # the main of round 9ו, as it is (it runs 9ה's main and its own page), and then 9ז
    src = open(os.path.join(HERE, 'plan7b_r9f.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    import textwrap; code = textwrap.dedent('\n'.join(body))
    exec(compile(code, 'plan7b_r9f.py:__main__', 'exec'), dict(vars(R9F)))   # in 9ו's own globals (R7, R8B, R9E …), as when 9ו runs by itself
    page_r9g()
