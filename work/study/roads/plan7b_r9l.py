# -*- coding: utf-8 -*-
"""4.11 · סבב 9ל של מפת הדרכים — הבעלים 20:47: "תבטל את המעבר המיותר הזה — יש עוד מעבר כמה מטרים ממנו".
 · J46_185 (השער המערבי של המסוף, סבב 9כ): המעבר בלי רמזור על שדרת המזרח (בזרוע הדרומית) יוצא; המעבר של J46_16, כמה מטרים צפונה, נשאר.
   המעבר על השער עצמו (LC-E3W/1, לאורך המדרכה של שדרת המזרח) נשאר — אין מעבר אחר על השער.
   J46_185 רשום כחריג של כלל צומת ה-T (R9.T_EXC), והבדיקה של D‑427 בודקת אותו כחריג: על שדרת המזרח אין מעבר, ועל השער — כן.
 · DW-D4-01 (הכניסה למחסן מרחוב המוסכים) יוצא: במשחק אין שם פתח (דשא וגדר). המחסן (D4-01) — בשער המזרחי של D4 (DW-D4-04, משדרת המזרח), כמו במשחק.
 · שאר הרשת, הציור והבדיקות — כמו בסבב 9כ. הסעיפים של 9כ, ‏9י, ‏9ט ו-9ח נשארים בדף כהיסטוריה.
    python3 plan7b_r9l.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete/roads_before_r9l)"""
import json, os, sys, textwrap, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
E = html.escape
import plan7b_r9k as R9K        # round 9כ — its network, routes, patches and wrappers (and through it 9י … 9) run on import; its __main__ does not
import plan7b_r9j as R9J
import plan7b_r9i as R9I
import plan7b_r9g as R9G
import plan7b_r9 as R9
import plan7b_r7 as R7
import plan7b_svg as SV
J_W = R9K.J_W
WHY185 = 'צומת ימינה בלבד של שער המסוף; מעבר J46_16 במרחק כמה מטרים (הבעלים 4.11 20:47)'
R9.T_EXC[J_W] = WHY185          # the T rule does not pick a crossing here: the one on the avenue is out, the one on the gate stays
DONE9L = {}

# ---------------------------------------------------------------- 1 · the crossing on the avenue at J46_185 — out, from the start (the bays see the map as it is)
_xw9k = R9K.xw_final
def xw_final(g):
    _xw9k(g)
    gone = [x for x in g['XW'] if x['node'] == J_W and g['SEG'] and next(s for s in g['SEG'] if s['id'] == x['seg'])['road'] == 'AR-E']
    g['XW'][:] = [x for x in g['XW'] if not any(x is y for y in gone)]
    DONE9L['xw_out'] = sorted(x['seg'] for x in gone)
R9K.xw_final = xw_final

# ---------------------------------------------------------------- 2 · DW-D4-01 out: the warehouse through the east gate of D4 (as in the game)
DW_OUT, LOT_W, DW_GATE = 'DW-D4-01', 'D4-01', 'DW-D4-04'
WHY_D4 = ('סבב 9ל: הכניסה מרחוב המוסכים (DW-D4-01) יצאה — במשחק אין שם פתח (דשא וגדר); '
          'המחסן נגיש בשער המזרחי של D4 (DW-D4-04, משדרת המזרח), דרך מגרש המכולות — כמו במשחק.')
_post9k = R7.post
def post(ctx):
    g = sys._getframe(1).f_globals
    g['__r9l_post'] = _post9k
    items = eval('__r9l_post(__r9l_ctx)', g, {'__r9l_ctx': ctx})
    lot = next(l for l in ctx['LOTS'] if l['id'] == LOT_W)
    assert lot.get('dw') == DW_OUT and any(d['id'] == DW_GATE for d in g['LOT_DW'])
    for key in ('LOT_DW', 'SITE_ROADS'): g[key][:] = [o for o in g[key] if o['id'] != DW_OUT]
    lot.update(dw=DW_GATE, front='AR-E', why=WHY_D4)
    DONE9L['d4'] = dict(lot=LOT_W, label=lot['label'], out=DW_OUT, via=DW_GATE)
    return items
R7.post = post

# ---------------------------------------------------------------- 3 · the check of the T rule: J46_185 checked as a listed exception (not skipped)
_chk9k = R7.checks
def checks(ctx, I):
    g = sys._getframe(1).f_globals
    g['__r9l_chk'] = _chk9k
    out = list(eval('__r9l_chk(__r9l_ctx, __r9l_I)', g, {'__r9l_ctx': ctx, '__r9l_I': I}))
    sb = {s_['id']: s_ for s_ in g['SEG']}
    on = sorted(x['seg'] for x in g['XW'] if x['node'] == J_W)
    ok = on == [R9K.S_W] and not any(sb[s]['road'] == 'AR-E' for s in on)
    DONE9L['xw_on'] = on; hit = 0
    for i, c in enumerate(out):
        if isinstance(c, tuple) and str(c[0]).startswith('D‑427 עם כלל צומת ה-T'):
            hit += 1
            out[i] = (c[0], c[1] and ok, c[2] + f" · חריג רשום: {J_W} — {WHY185}: על שדרת המזרח אין מעבר; על השער — {', '.join(on) or 'אין'}" + ('' if ok else ' — לא כך במפה')) + tuple(c[3:])
    assert hit == 1
    lot = next((l for l in ctx['LOTS'] if l['id'] == LOT_W), {})
    DONE9L['d4_ok'] = not any(d['id'] == DW_OUT for d in g['LOT_DW'] + g['SITE_ROADS']) and lot.get('dw') == DW_GATE
    return out
R7.checks = checks

TITLE = 'תוכנית הדרכים של כל העיר — סבב 9ל'
_lay9k = SV.label_layout
def label_layout(P_):
    o = _lay9k(P_); P_['title'] = TITLE; P_['batch'] = '9ל'; return o
SV.label_layout = label_layout

# ---------------------------------------------------------------- 4 · the page: the section of round 9ל (before 9כ — which stays as it was)
def keep_9k():
    """the 9כ record and its section of the page, as they are now — history"""
    P_ = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8'))
    T = open(os.path.join(HERE, 'city_plan.html'), encoding='utf-8').read()
    a = T.index('<h2>סבב 9כ'); b = T.index('<h2>סבב 9י'); assert a < b
    return P_['r9k'], T[a:b]

def small_svg(after):
    """J46_185 before and after — north up, west on the left, east on the right"""
    Y = R9K.Y_W; x0, y0, x1, y1 = 4300, 1560, 4960, 2060; rd = '#8d949b'
    o = [f"<svg viewBox='{x0} {y0} {x1 - x0} {y1 - y0}' role='img' aria-label='J46_185 {'אחרי' if after else 'לפני'}' style='width:100%;height:auto;background:#f4f2ec;border-radius:8px'>"]
    o.append("<rect x='4880' y='1770' width='400' height='600' rx='140' fill='#b9bec4' stroke='#555' stroke-width='4'/>")
    o.append(f"<rect x='{x0}' y='1448' width='{x1 - x0}' height='304' fill='{rd}'/>")
    o.append(f"<rect x='4448' y='1600' width='304' height='{y1 - 1600}' fill='{rd}'/><rect x='4590' y='1752' width='20' height='{y1 - 1752}' fill='#9cbf86'/>")
    o.append("<text x='4600' y='1690' font-size='26' text-anchor='middle' fill='#fff'>J46_16</text><text x='4380' y='1690' font-size='24' text-anchor='middle' fill='#fff'>שדרת השדה</text>")
    o.append(''.join(f"<rect x='{x}' y='1762' width='12' height='40' fill='#fff'/>" for x in range(4478, 4722, 22)))
    o.append(f"<rect x='4752' y='{Y - 54}' width='140' height='108' fill='#e2ded3'/><rect x='4752' y='{Y - 39}' width='{4926 - 4752}' height='78' fill='{rd}'/>")
    o.append(f"<rect x='4874' y='{Y - 39}' width='52' height='78' fill='#b9bec4'/>")
    o.append(''.join(f"<rect x='4762' y='{y}' width='40' height='9' fill='#fff'/>" for y in range(Y - 36, Y + 36, 17)))
    if after:
        o.append(f"<rect x='4473' y='{Y + 64}' width='254' height='40' fill='none' stroke='#c8372d' stroke-width='5' stroke-dasharray='14 9'/>"
                 f"<text x='4372' y='{Y + 94}' font-size='26' text-anchor='middle' fill='#c8372d'>יצא</text>")
    else:
        o.append(''.join(f"<rect x='{x}' y='{Y + 64}' width='12' height='40' fill='#fff'/>" for x in range(4478, 4722, 22)))
    o.append(f"<text x='4815' y='{Y - 64}' font-size='22' text-anchor='middle' fill='#333'>השער</text><text x='4815' y='{Y + 88}' font-size='22' text-anchor='middle' fill='#333'>J46_185</text>")
    o.append("<text x='4600' y='2045' font-size='22' text-anchor='middle' fill='#fff'>שדרת המזרח</text>")
    o.append("<g transform='translate(4815,2012)'><path d='M0,-36 L14,0 L0,-9 L-14,0 Z' fill='#222'/><text x='0' y='26' font-size='20' text-anchor='middle'>צפון</text></g>")
    o.append("<text x='4372' y='1880' font-size='28' text-anchor='middle' fill='#222'>מערב</text><text x='4925' y='2030' font-size='26' text-anchor='middle' fill='#222'>מזרח</text>")
    o.append('</svg>')
    return ''.join(o)

def page_r9l(rec9j, sec9j, rec9k, sec9k):
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = TITLE; P_['batch'] = '9ל'
    T = P_['bus']['terminal']; T['gates'] = R9K.gates_rec(); T['flow'] = R9K.FLOW   # as round 9כ wrote them (the build does not keep them)
    P_['logi_points'] = [dict(zone=z, what=w, rect=r, state=s) for z, w, r, s in R9J.POINTS]
    P_['r9j'] = rec9j; P_['r9k'] = rec9k
    SB = {frozenset((x['a'], x['b'])): x for x in P_['segments']}
    for ln in P_['routes']['bus']:
        if ln.get('back'): ln['len_back_km'] = round(sum(SB[frozenset((a, b))]['len_m'] for a, b in zip(ln['back'], ln['back'][1:])) / 1000, 2)
    nck = len(P_['checks']); nok = sum(1 for c in P_['checks'] if c['ok'])
    P_['r9l'] = dict(at='4.11.2026', by='הבעלים 20:47', why='סבב 9ל: המעבר בלי רמזור על שדרת המזרח ב-J46_185 יצא (מעבר J46_16 כמה מטרים צפונה); DW-D4-01 יצא — במשחק אין שם פתח',
                     xw_out=DONE9L.get('xw_out'), xw_on=DONE9L.get('xw_on'), t_exception={J_W: WHY185}, d4=DONE9L.get('d4'), checks=f'{nok}/{nck}')
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); H0 = open(ph, encoding='utf-8').read()
    fig = lambda after, cap: f"<figure style='margin:0;flex:1 1 280px;max-width:440px'>{small_svg(after)}<figcaption class='small'>{cap}</figcaption></figure>"
    S9 = ("<h2>סבב 9ל — מה השתנה (4.11.2026)</h2>"
          f"<p class='small'>הבעלים (20:47): המעבר בלי רמזור על שדרת המזרח בזרוע הדרומית של {J_W} (השער המערבי של המסוף) יצא — מעבר J46_16, כמה מטרים צפונה, נשאר. "
          f"המעבר על השער עצמו, לאורך המדרכה של שדרת המזרח, נשאר. בבדיקה של כלל צומת ה-T {J_W} רשום כחריג: {E(WHY185)}.</p>"
          "<p class='small'>DW-D4-01 (הכניסה למחסן מרחוב המוסכים) יצא מהמפה — במשחק אין שם פתח (דשא וגדר); המחסן נגיש בשער המזרחי של D4 (DW-D4-04, משדרת המזרח), כמו במשחק. "
          f"הבדיקות: {nok} מתוך {nck} עוברות.</p>"
          "<div style='display:flex;flex-wrap:wrap;gap:12px;margin:6px 0 14px'>" + fig(False, 'לפני — סבב 9כ: מעבר על שדרת המזרח ומעבר על השער') +
          fig(True, 'אחרי — סבב 9ל: המעבר על שדרת המזרח יצא; המעבר של J46_16 והמעבר על השער נשארו') + "</div>")
    k = H0.index('<h2>סבב 9ט'); H0 = H0[:k] + S9 + sec9k + sec9j + H0[k:]
    for old in ('תוכנית הדרכים של כל העיר — סבב 9ט', 'תוכנית הדרכים של כל העיר — סבב 9י', 'תוכנית הדרכים של כל העיר — סבב 9כ'):
        H0 = H0.replace(old, TITLE)
    open(ph, 'w', encoding='utf-8').write(H0)
    print('r9l', dict(xw_out=DONE9L.get('xw_out'), xw_on=DONE9L.get('xw_on'), d4=DONE9L.get('d4'), d4_ok=DONE9L.get('d4_ok'), checks=f'{nok}/{nck}'))
    assert DONE9L.get('xw_out') == ['AR-E/1', 'AR-E/1a'] and DONE9L.get('d4_ok')
    assert all(H0.count('<h2>סבב ' + r) == 1 for r in ('9ל', '9כ', '9י', '9ט', '9ח'))
    assert H0.index('<h2>סבב 9ל') < H0.index('<h2>סבב 9כ') < H0.index('<h2>סבב 9י') < H0.index('<h2>סבב 9ט')

if __name__ == '__main__':
    os.chdir(HERE)
    rec9h, prev9i, sec9h = R9I.keep_9h()
    rec9j, sec9j = R9K.keep_9j()
    rec9k, sec9k = keep_9k()
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    R9I.page_r9i(rec9h, sec9h)
    page_r9l(rec9j, sec9j, rec9k, sec9k)
