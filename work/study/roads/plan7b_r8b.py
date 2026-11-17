# -*- coding: utf-8 -*-
"""3.11 · סבב 8ב של מפת הדרכים — R-76 (הבעלים 10:10 / 10:50, הביקורת 10:51): מעבר חצייה רק בצומת, צמוד לקו העצירה.
    python3 plan7b_r8b.py      → city_plan.json, names.json, city_plan.html  (לפני כל הרצה: עותק של שלושתם ל-W/_to_delete)
המודול טוען את סבב 8 (plan7b_r8 — כל מה שהוא עושה נשאר) ומוסיף:
 1. המעברים של המפה (bus.crosswalks): המרחק מהצומת נמדד לפי הרחוב שחוצים — הזרועות הניצבות (|cos| < 0.7), לא ההמשך של אותו רחוב.
    עד היום ההמשך של העורק נספר כ"רחוב שחוצים", והמעבר על העורק נבנה 4–11 מ׳ אחרי הפינה (באמצע הבלוק). מעבר בצומת של פחות מ-3 זרועות — יוצא.
 2. בדיקה קבועה: כל מעבר — בצומת של 3 זרועות לפחות, ועד 1 מ׳ אחרי הקו שלו (קצה הרחוב שחוצים + 1 מ׳).
 3. הנוסעים של המעבורת ב-A6 הולכים במדרכה עד המעבר בצומת (לא חוצים באמצע דרך החווה).
 4. ברשימה (r8b.crosswalks) — לכל מעבר שזז או יצא: האזור, הכביש, והצומת שאליו הוא עובר או "יוצא"."""
import json, math, os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan7b_r8 as R8          # round 8 (its wrappers are installed on import)
import plan7b_r7 as R7
import plan7b_svg as SV

R8B = dict(at='3.11.2026', moved=[], out=[], kept=0, ferry=None)

def _perp_half(g, k, s_):
    """the half width of the street a crossing on s_ at junction k crosses: the arms that are not the continuation of s_ (|cos| < .7)"""
    N, ADJ, CLS = g['N'], g['ADJ'], g['CLS']; n = N[k]
    p_ = s_['pts']; q_ = p_[1] if s_['a'] == k else p_[-2]; ex, ey = q_[0] - n['x'], q_[1] - n['y']; el = math.hypot(ex, ey) or 1
    h = 0
    for oo, t in ADJ[k]:
        if t is s_: continue
        pt = t['pts']; r_ = pt[1] if t['a'] == k else pt[-2]; qx, qy = r_[0] - n['x'], r_[1] - n['y']; ql = math.hypot(qx, qy) or 1
        if abs((ex * qx + ey * qy) / (el * ql)) < .7: h = max(h, CLS[t['cls']]['halfW'])
    return h

_post8 = R7.post
def post(ctx):
    g = sys._getframe(1).f_globals   # the build's globals (round 8's post reads them from its caller — called here through them)
    g['__r8b_post8'] = _post8
    items = eval('__r8b_post8(__r8b_ctx)', g, {'__r8b_ctx': ctx})
    N, ADJ, XW = g['N'], g['ADJ'], g['XW']; segby = {s_['id']: s_ for s_ in g['SEG']}; roads = {r['id']: r for r in g['Rd']}
    keep = []
    for x in XW:
        k = x['node']; s_ = segby.get(x['seg']); n = N[k]; rd = roads.get(s_['road']) if s_ else None
        name = (rd or {}).get('name', s_['road'] if s_ else x['seg']); jl = n.get('label') or k
        if not s_ or len(ADJ[k]) < 3:
            R8B['out'].append(dict(zone=n.get('zone'), road=x['seg'], roadName=name, node=k, junction='יוצא', why='לא בצומת (%d זרועות)' % len(ADJ[k])))
            continue
        if n.get('kind') != 'roundabout':
            hc = _perp_half(g, k, s_)
            if hc:
                d0, d1 = round(hc + 10), round(hc + 50)
                if x['d0'] - d0 >= 5:
                    R8B['moved'].append(dict(zone=n.get('zone'), road=x['seg'], roadName=name, node=k, junction='זז לקו העצירה בצומת ' + jl,
                                             from_m=round(x['d0'] / 10, 1), to_m=round(d0 / 10, 1)))
                x['d0'], x['d1'] = d0, d1
        keep.append(x)
    XW[:] = keep; R8B['kept'] = len(keep)
    # the ferry passengers of A6: on the sidewalk to the crossing at the junction (not across the farm road in the middle)
    for s in ctx['SITES']:
        w = s.get('why') or ''
        if 'הנוסעים חוצים את דרך החווה במעבר חציה' in w:
            cx, cy = (s['rect'][0] + s['rect'][2]) / 2, (s['rect'][1] + s['rect'][3]) / 2
            best = min(keep, key=lambda q: math.hypot(N[q['node']]['x'] - cx, N[q['node']]['y'] - cy))
            jl = N[best['node']].get('label') or best['node']
            s['why'] = w.replace('הנוסעים חוצים את דרך החווה במעבר חציה', 'הנוסעים הולכים במדרכה עד המעבר בצומת (' + jl + ') — לא חוצים באמצע הדרך (R-76)')
            R8B['ferry'] = dict(site=s['id'], junction=best['node'], label=jl)
    return items
R7.post = post

_chk8 = R7.checks
def checks(ctx, I):
    g = sys._getframe(1).f_globals
    g['__r8b_chk8'] = _chk8
    out = list(eval('__r8b_chk8(__r8b_ctx, __r8b_I)', g, {'__r8b_ctx': ctx, '__r8b_I': I}))
    N, ADJ, XW = g['N'], g['ADJ'], g['XW']; segby = {s_['id']: s_ for s_ in g['SEG']}; bad = []
    for x in XW:
        k = x['node']; s_ = segby[x['seg']]
        if len(ADJ[k]) < 3: bad.append(f"{x['seg']} ב-{k}: לא בצומת"); continue
        hc = 175 if N[k].get('kind') == 'roundabout' else (_perp_half(g, k, s_) or 0)
        if hc and x['d0'] > hc + 10 + 10: bad.append(f"{x['seg']} ב-{k}: {(x['d0'] - hc - 10) / 10:.1f} מ׳ אחרי הקו")
    out.append(('R-76 — מעבר חצייה רק בצומת (3 זרועות לפחות), צמוד לקו העצירה: עד 1 מ׳ אחרי הקו (קצה הרחוב שחוצים + 1 מ׳)', not bad,
                f"{len(XW)} מעברים; זזו לפינה: {len(R8B['moved'])}; יצאו: {len(R8B['out'])}" + (' · לא: ' + ' | '.join(bad) if bad else ' · כולם בצומת וצמודים לקו')))
    return out
R7.checks = checks

_lay8 = SV.label_layout
def label_layout(P_):
    o = _lay8(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 8ב'; P_['batch'] = '8ב'; P_['at'] = '3.11.2026'
    P_['r8b'] = dict(at=R8B['at'], why='R-76 (הבעלים 10:10 / 10:50, הביקורת 10:51): מעבר חצייה רק בצומת, צמוד לקו העצירה',
                     crosswalks=dict(kept=R8B['kept'], moved=R8B['moved'], out=R8B['out']), ferry=R8B['ferry'],
                     rule='המרחק של מעבר מהצומת — לפי הרחוב שחוצים (הזרועות הניצבות), קצה הרחוב + 1 מ׳ עד + 5 מ׳; בצומת עם רמזור — מעבר בכל זרוע; '
                          'הולכי הרגל עם הירוק המקביל ורכב שפונה נותן זכות קדימה; בלי רמזור — הרכב נותן זכות קדימה (ברירת מחדל, לאישור הבעלים)')
    return o
SV.label_layout = label_layout


def page_r8b():
    """the page: a section of round 8b (R-76) — every crossing that moved or went out, by zone — before the section of round 8"""
    import html
    e = lambda x: html.escape(str(x)); D = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8')); R = D['r8b']; X = R['crosswalks']
    rows = sorted(X['moved'] + X['out'], key=lambda q: (q['zone'] or '', q['node'], q['road']))
    H = ["<h2>סבב 8ב — מעברי החצייה (R-76, 3.11.2026)</h2><p class='small'>" + e(R['rule']) + f" · {X['kept']} מעברים במפה; זזו לקו העצירה: {len(X['moved'])}; יצאו: {len(X['out'])}.</p>",
         "<div class='wrap'><table><tr><th>אזור</th><th>הכביש</th><th>הקטע</th><th>הצומת / יוצא</th><th>היה</th><th>עכשיו</th></tr>"]
    H += [f"<tr><td class='id'>{e(q['zone'])}</td><td>{e(q['roadName'])}</td><td class='small'>{e(q['road'])}</td><td>{e(q['junction'])}</td>"
          f"<td class='small'>{e(str(q.get('from_m', '—')) + ' מ׳' if q.get('from_m') is not None else '—')}</td><td class='small'>{e(str(q.get('to_m')) + ' מ׳' if q.get('to_m') is not None else q.get('why', '—'))}</td></tr>" for q in rows]
    H.append("</table></div>")
    if R.get('ferry'): H.append(f"<p class='small'>המעבורת ב-A6 ({e(R['ferry']['site'])}): הנוסעים הולכים במדרכה עד המעבר בצומת {e(R['ferry']['label'])}.</p>")
    p = os.path.join(HERE, 'city_plan.html'); T = open(p, encoding='utf-8').read(); k = T.index("<h2>סבב 8 — מה השתנה")
    open(p, 'w', encoding='utf-8').write(T[:k] + ''.join(H) + T[k:])


if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
    R8.page_r8()
    page_r8b()
