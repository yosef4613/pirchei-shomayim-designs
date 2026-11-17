#!/usr/bin/env python3
# fc_page.py — fieldcalc 17.11: הדף "השדה — הבירור, מטריצת השירות, החישוב והציור" מתוך fc_result.json (אותם נתונים כמו הבדיקה).
# ציור SVG בקוד בלבד (כלל 13 / 17): בלי תמונות, בלי קישורים חיצוניים. צפון למעלה, קואורדינטות העולם (10 פיקס׳ למטר).
import json, os, sys, html, math, subprocess, hashlib, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
R = json.load(open(os.path.join(HERE, 'fc_result.json'), encoding='utf-8'))
B = json.load(open(os.path.join(HERE, 's15_base.json'), encoding='utf-8')); D = B['S15D']
TL = json.load(open(os.path.join(HERE, 's15j_L.json'), encoding='utf-8'))
try: R2 = json.load(open(os.path.join(HERE, 'fc_result2.json'), encoding='utf-8'))
except Exception: R2 = None
E = html.escape
try: SP = json.load(open(os.path.join(HERE, 'fc_spots.json'), encoding='utf-8'))
except Exception: SP = None
NOW = subprocess.run(['bash', '-c', 'TZ=Asia/Jerusalem date "+%d.%m.%Y %H:%M"'], capture_output=True, text=True).stdout.strip()
HE = {m: a['he'] for m, a in R['ac'].items()}
CLS_COL = {'GA': '#6aa84f', 'EXEC': '#8e63c7', 'AMPH': '#2a9d8f', 'REG': '#3f7fc4', 'NB': '#2f5f9e', 'WIDE': '#1d3b6e', 'CARGO': '#b5651d'}

def rect(r, cls, extra=''):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="%s" %s/>' % (r[0], r[1], r[2] - r[0], r[3] - r[1], cls, extra)
def txt(x, y, s, cls='lb', size=None, anchor='middle'):
    st = (' style="font-size:%gpx"' % size) if size else ''
    return '<text x="%.1f" y="%.1f" class="%s" text-anchor="%s"%s>%s</text>' % (x, y, cls, anchor, st, E(s))
def shape(cx, ny, m, up=False):
    a = R['ac'][m]; L, W = a['L'] * 10, a['span'] * 10; ga = a['cls'] in ('GA', 'EXEC', 'AMPH'); fw = max(20, .12 * W)
    sgn = -1 if not up else 1
    wc = ny + sgn * (.35 if ga else .45) * L; ch = (.15 if ga else .18) * L; tail = ny + sgn * L
    col = CLS_COL.get(a['cls'], '#555')
    parts = [[cx - fw / 2, min(ny, tail), cx + fw / 2, max(ny, tail)], [cx - W / 2, wc - ch / 2, cx + W / 2, wc + ch / 2],
             [cx - .19 * W, min(tail, tail - sgn * .12 * L), cx + .19 * W, max(tail, tail - sgn * .12 * L)]]
    return ''.join(rect(p, 'ac', 'style="fill:%s"' % col) for p in parts)

def svg_main():
    X0, Y0, X1, Y1 = 4700, -900, 9700, 3250
    o = ['<svg viewBox="%d %d %d %d" class="map" role="img" aria-label="ציור השדה: המסלול, מסלולי ההסעה, העמדות, אולמות הכבודה וההרחבה הדרומית">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    o.append(rect([X0, Y0, X1, Y1], 'bg'))
    o.append(rect([6000, 2550, X1, Y1], 'sea')); o.append(rect([7200, 1700, 9600, 2550], 'land'))
    o.append('<polygon class="air" points="%s"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in D['fence']))
    for k in ('apron', 'apronS'): o.append(rect(D[k], 'apron'))
    o.append(rect(D['rwy'], 'rwy')); o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="cl"/>' % (D['rwy'][0] + 120, D['rcy'], D['rwy'][2] - 120, D['rcy']))
    o.append(txt(D['rwy'][0] + 90, D['rcy'] + 22, '09', 'rw', 60)); o.append(txt(D['rwy'][2] - 90, D['rcy'] + 22, '27', 'rw', 60))
    for k, lab in (('twa', 'מסלול הסעה A'), ('twb', 'B'), ('twc', 'מסלול הסעה C')):
        o.append(rect(D[k], 'twy'))
    o.append(txt(6400, D['tacy'] + 18, 'מסלול הסעה A — מערבה (09)', 'tw', 46))
    o.append(txt(D['tbcx'], 800, 'B', 'tw', 60)); o.append(txt(7600, D['tccy'] + 16, 'C', 'tw', 50))
    for l in D['links']:
        o.append(rect(l['rect'], 'twy')); o.append(txt(l['cx'], -330, l['id'], 'tw', 44))
    for s in D['service']: o.append(rect(s['rect'], 'road'))
    for b in TL['bld'].values(): o.append(rect(b['r'], 'bld'))
    for b in D['base']: o.append(rect(b['rect'], 'base')); o.append(txt((b['rect'][0] + b['rect'][2]) / 2, (b['rect'][1] + b['rect'][3]) / 2 + 10, b['label'].split(' — ')[0], 'lbs', 26))
    for pk, r in D['pockets'].items(): o.append(rect(r, 'pocket'))
    for b in D['bridges']: o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="br"/>' % (b['root'][0], b['root'][1], b['door'][0], b['door'][1]))
    for h in D['helipads']:
        c = h['c']; o.append('<circle cx="%d" cy="%d" r="%d" class="hp"/>' % (c[0], c[1], h['pad'] / 2 + 10)); o.append(txt(c[0], c[1] + 16, 'H', 'hpl', 48)); o.append(txt(c[0], c[1] + 120, h['id'], 'lbs', 30))
    plan = {}
    for f in R['schedule']: plan.setdefault(f['stand'], []).append(f)
    for sid, s in D['stands'].items():
        r = s['rect']; o.append(rect(r, 'stand' + (' r3' if sid == 'R3' else '') + (' alt' if sid == 'CH' else '')))
        if sid == 'CH': o.append(txt(r[0] + 60, r[1] + 40, 'CH — חלופה (C1 + C2)', 'lbs', 26, 'start')); continue
        fl = plan.get(sid)
        if fl: o.append(shape(s['cx'], s['nose'], fl[0]['model']))
        lab = sid + (' ×%d' % len(fl) if fl and len(fl) > 1 else '')
        o.append(txt(s['cx'], r[1] + 34 if sid not in ('GA1', 'GA2', 'GA3', 'GA4', 'GA5', 'GA6', 'GA7') else r[1] - 12, lab, 'st', 34))
    ru = D['runup']; o.append(rect(ru, 'runup')); o.append(rect(D['blast'], 'blast'))
    o.append(txt((ru[0] + ru[2]) / 2, ru[1] + 150, 'R3: ביום טיסות', 'lbs', 26)); o.append(txt((ru[0] + ru[2]) / 2, ru[1] + 185, 'בלילה הרצת מנועים', 'lbs', 26))
    # אולמות הכבודה
    for h in R['layout']['halls']:
        o.append(rect([h['belt'][0] - 6, h['lane'] - 16, h['belt'][1] + 6, h['lane'] + 16], 'hall' + (' today' if h.get('today') else '')))
    o.append(txt(7380, 1080, '5 עמדות כבודה', 'hl', 40))
    # ההרחבה הדרומית־מזרחית
    L = R['layout']; ex = L['exp']['rect']
    o.append(rect(ex, 'exp')); o.append(txt((ex[0] + ex[2]) / 2, ex[1] + 40, 'ההרחבה: בסיס הצי הדרומי (28 חניות)', 'hl', 34))
    if R2:
        bl = R2['blast']; o.append(rect(bl['hazard'], 'haz')); o.append(txt((bl['hazard'][0] + bl['hazard'][2]) / 2, bl['hazard'][3] - 20, 'אזור ההדף (20:30–04:25)', 'lbs', 24))
        o.append(rect(bl['road_fix'], 'road'))
        for g in bl['gse_fix']: o.append(rect(g['r'], 'gse'))
        for k, v in R2['service_roads']['cross'].items():
            o.append('<circle cx="%d" cy="%d" r="34" class="xc"/>' % (v['x'], (D['twc'][1] + D['twc'][3]) / 2)); o.append(txt(v['x'], D['twc'][3] + 60, '%s · %g%%' % (k, v['util']), 'xcl', 28))
        o.append(rect([8428, 2546, 8468, 2554], 'agate')); o.append(txt(8448, 2590, 'G-AMPH', 'xcl', 22))
        bay = R2['reserve']['bay_geom']['rect']; o.append(rect(bay, 'bay')); o.append(txt(bay[2] + 8, (bay[1] + bay[3]) / 2, 'מפרץ', 'lbs', 26, 'start'))
    else:
        o.append(rect(L['gse_road']['r'], 'road'))
        for g in L['gse_s']: o.append(rect(g['r'], 'gse'))
    a = L['amph']; o.append(rect(a['dock'], 'dock')); o.append(rect(a['ramp'], 'dock')); o.append(rect(a['lane'], 'wlane'))
    o.append('<polyline points="%s" class="wtaxi"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in a['taxi']))
    o.append(txt((a['lane'][0] + a['lane'][2]) / 2, a['lane'][1] + 64, '← מסלול המים של האמפיבי (נוחת מערבה)', 'wl', 40))
    o.append(txt(a['dock'][0] - 10, a['dock'][1] - 14, 'מזח צף', 'lbs', 28, 'start'))
    bs = L['bshop']; o.append(rect(bs['act'], 'like')); o.append(txt((bs['act'][0] + bs['act'][2]) / 2, bs['act'][1] + 140, 'המספנה והמעגן — LIKE-08 (לא זז)', 'lk', 30))
    o.append('<polyline points="%s" class="blane"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in bs['lane']))
    o.append(txt(8600, 2990, 'נתיב הסירות של המספנה', 'wl', 28))
    # B2 — האפשרות שנפסלה
    o.append(rect([9484, -55, 9596, 1925], 'opt')); o.append(txt(9540, 400, 'B2 נפסל', 'opt2', 30))
    o.append('<g class="nArrow"><line x1="4850" y1="3100" x2="4850" y2="2900"/><text x="4850" y="2870" text-anchor="middle">צפון</text></g>')
    o.append('<g class="scale"><line x1="4900" y1="3180" x2="5400" y2="3180"/><text x="5150" y="3160" text-anchor="middle">50 מ׳</text></g>')
    o.append('</svg>')
    return ''.join(o)

def svg_halls():
    X0, Y0, X1, Y1 = 6740, 850, 8540, 1050
    o = ['<svg viewBox="%d %d %d %d" class="map halls" role="img" aria-label="5 עמדות הכבודה בקומת הרחבה מתחת לאגף השערים">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    o.append(rect([X0, Y0, X1, Y1], 'bg')); o.append(rect(D['core'], 'bld'))
    src = next(s for s in D['service'] if s['id'] == 'AIR-SR_C')['rect']; o.append(rect([max(src[0], X0), src[1], min(src[2], X1), src[3]], 'road'))
    o.append(txt(6760 + 8, 840 + 30, 'שביל השירות SR_C — הגישה לדלתות', 'lbs', 12, 'start'))
    for st in TL['stairs']:
        r = R['layout']['p1_stairs_new'] if st['id'] == 'P1' else st['r']
        o.append(rect(r, 'stairs' + (' moved' if st['id'] == 'P1' else ''))); o.append(txt((r[0] + r[2]) / 2, r[3] + 12, 'מדרגות ' + st['id'] + (' (זזות)' if st['id'] == 'P1' else ''), 'lbs', 10))
        if st['id'] == 'P1': o.append(rect(st['r'], 'stairs old')); o.append(rect(R['layout']['p1_land_new'], 'stairs moved'))
    for b in D['bridges']:
        if b['root'][1] <= 890: o.append('<circle cx="%d" cy="%d" r="7" class="root"/>' % (b['root'][0], b['root'][1])); o.append(txt(b['root'][0], b['root'][1] - 10, 'שרוול ' + b['stand'], 'lbs', 10))
    L = R['layout']; TW = L['train']['W']; TLn = L['train']['L']
    drawn = set()
    for h in L['halls']:
        r = h['r']
        if h.get('annex'): o.append(rect(h['annex'], 'hallbox'))
        if h.get('hall') not in drawn:
            o.append(rect(r, 'hallbox' + (' today' if h.get('today') else '')))
            if h.get('hall'): drawn.add(h['hall'])
            for dr in (h['din'], h['dout']): o.append(rect([dr[0], 882, dr[1], 890], 'door'))
        xin = (h['din'][0] + h['din'][1]) / 2; xout = (h['dout'][0] + h['dout'][1]) / 2; y = h['lane']
        o.append('<polyline points="%d,860 %d,%d %d,%d %d,860" class="upath"/>' % (xin, xin, y, xout, y, xout))
        o.append(rect([h['belt'][0], h['belt'][2] - 3, h['belt'][1], h['belt'][2] + 3], 'belt'))
        x1 = xout - TW / 2 - 2; o.append(rect([x1 - TLn, y - TW / 2, x1, y + TW / 2], 'train'))
        o.append(txt((h['belt'][0] + h['belt'][1]) / 2, y + 4, h['id'], 'hid', 12))
    o.append('</svg>')
    return ''.join(o)

def svg_floor(after):
    X0, Y0, X1, Y1 = 6740, 870, 9180, 1215
    o = ['<svg viewBox="%d %d %d %d" class="map halls" role="img" aria-label="%s">' % (X0, Y0, X1 - X0, Y1 - Y0, 'קומת השערים אחרי' if after else 'קומת השערים היום')]
    o.append(rect([X0, Y0, X1, Y1], 'bg')); o.append(rect(D['core'], 'bld')); o.append(rect([7953, 1033, 9163, 1210], 'bld')); o.append(rect([7222, 1033, 7865, 1180], 'bld'))
    if not after:
        for z in TL['zones']:
            if z[0].startswith(('G-', 'CW-DF', 'BAG5', 'TE-FOOD', 'TE-BUS', 'TE-LNG')):
                o.append(rect(z[2], 'zone' + (' bag' if z[0] == 'BAG5' else ''))); o.append(txt((z[2][0] + z[2][2]) / 2, (z[2][1] + z[2][3]) / 2 + 4, z[0].replace('G-', 'שער '), 'lbs', 11))
        for g, v in TL['seats'].items():
            for q in v: o.append('<circle cx="%.0f" cy="%.0f" r="2.4" class="seat"/>' % (q[0], q[1]))
    else:
        try: LA = json.load(open(os.path.join(HERE, 's15j_layout_fc.json'), encoding='utf-8'))
        except Exception: LA = None
        if LA:   # הפריסה שנוצרה בפועל (s15j_layout_fc.py) — האזורים והמושבים
            for z in LA['zones']:
                if z[0].startswith(('G-', 'BAG5', 'BH-', 'TE-FOOD', 'TE-BUS', 'TE-LNG')):
                    bag = z[0].startswith(('BAG5', 'BH-'))
                    o.append(rect(z[2], 'zone' + (' bag' if bag else ''))); o.append(txt((z[2][0] + z[2][2]) / 2, z[2][1] + 14 if bag else (z[2][1] + z[2][3]) / 2 + 4, z[0].replace('G-', 'שער ').replace('BAG5', 'BH-3'), 'lbs', 11))
            for g, v in LA['seats'].items():
                for q in v: o.append('<circle cx="%.0f" cy="%.0f" r="2.4" class="seat"/>' % (q[0], q[1]))
        for h in R['layout']['halls']:
            if h.get('annex'): o.append(rect(h['annex'], 'zone bag'))
            if not LA: o.append(rect(h['r'], 'zone bag')); o.append(txt((h['r'][0] + h['r'][2]) / 2, 945, h['id'], 'lbs', 13))
        if not LA:
            for l in R['lounges']:
                o.append(rect(l['r'], 'zone')); o.append(txt((l['r'][0] + l['r'][2]) / 2, (l['r'][1] + l['r'][3]) / 2 + 4, 'טרקלין %s · %d מושבים' % (l['g'], l['cap']), 'lbs', 11))
    for st in TL['stairs']:
        o.append(rect(R['layout']['p1_stairs_new'] if (after and st['id'] == 'P1') else st['r'], 'stairs'))
        if after and st['id'] == 'P1': o.append(rect(R['layout']['p1_land_new'], 'stairs moved'))
    for b in D['bridges']:
        if b['root'][1] <= 890: o.append('<circle cx="%d" cy="%d" r="7" class="root"/>' % (b['root'][0], b['root'][1]))
    o.append('</svg>')
    return ''.join(o)
def table(head, rows, cls=''):
    return '<div class="tw"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, ''.join('<th>%s</th>' % E(str(h)) for h in head),
        ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % (c if isinstance(c, str) and c.startswith('<') else E(str(c))) for c in r) for r in rows))

def page():
    O = R['old']; N = R['new_today']; P = R['scen'][R['pick']]; Bs = R['scen']['base']
    moves_old = O['moves']; mv = P['rwy']['per1800']
    h = []
    h.append('<header><h1>השדה — הבירור של הישן, מטריצת השירות, החישוב והציור</h1>')
    h.append('<p class="cap">סבב 17.11 · fieldcalc · %s · הבסיס S7F299 (int299 930919a) · הישן S7F272 (196d990e34aa) · יחידות: 10 פיקס׳ עולם למטר; זמן — שניות עולם (0.5 דקת משחק לשנייה; מחזור S15SIM = 720 ש׳ = 6 שעות משחק). כל המספרים בדף מחושבים בכלי fc_calc.py מאותם נתונים.</p></header>' % E(NOW))
    h.append('<section class="kpis">')
    for k, v, sub in (('הישן — תנועות מסלול ב-1800 ש׳', '%d–%d' % (min(moves_old), max(moves_old)), 'נמדד עכשיו, 3 זרעים (777 / 31337 / 4242)'),
                      ('החדש היום', '%g' % N['moves1800'], '%d טיסות במחזור של 720 ש׳' % N['flights']),
                      ('התוכנית', '%g' % mv, '×%.1f מהישן · שלב א׳: %g (×%.1f)' % (mv / max(moves_old), Bs['rwy']['per1800'], Bs['rwy']['per1800'] / max(moves_old))),
                      ('מסוקים', '%g' % R['heli_plan']['moves1800'], 'הישן %d–%d · היום 5' % (min(O['heli']), max(O['heli']))),
                      ('עמדות כבודה', '5', 'אחת היום; 4 — מינימום'),
                      ('בדיקת המרווחים', '%d / %d' % (R['clear']['checks'] - R['clear']['fails'], R['clear']['checks']), 'עוברות · בדיקה עצמית: %d כישלונות בפריסה שגויה' % R['selftest']['fails'])):
        h.append('<div class="kpi"><div class="k">%s</div><div class="v">%s</div><div class="s">%s</div></div>' % (E(k), E(v), E(sub)))
    h.append('</section>')
    # 1. הבירור של הישן
    h.append('<section><h2>1. הבירור של השדה הישן (S7F272) — נמדד עכשיו במתכנן הישן עצמו</h2>')
    h.append('<p>הכלי q_old_ops.js מריץ בתוך הבנייה הישנה את המתכנן AO (‏044_core / 045_G7) בלי חיתוך, לחלון של 1800 ש׳, בשלושה זרעים — כמו הבודק. התוצאה זהה לביקורת (44–46): ‏<b>%s</b> תנועות. ההגדרות של הישן: ‏demand %.1f, ‏gap %s, ‏turn %s, ‏gaDwell %s, ‏cgDwell %s, ‏heliDwell %s, ‏heliAway %s.</p>' % (
        ' / '.join(map(str, moves_old)), 0.6, '25–170', '130–300', '200–600', '150–330', '100–300', '40–110'))
    rows = []
    for i, sd in enumerate((777, 31337, 4242)):
        rows.append([sd, O['moves'][i], O['land'][i], O['to'][i], O['exec_to'][i], O['heli'][i], O['stands'][i], '%s / %s' % tuple(O['gap'][i])])
    h.append(table(['זרע', 'תנועות מסלול', 'נחיתות', 'המראות', 'המראות מנהלים (BJ / CN)', 'תנועות מסוקים', 'עמדות שהשתמשו', 'מרווח בין תנועות: מינ׳ / חציון (ש׳)'], rows))
    tb = {}
    for t in O['turn']:
        for m, v in t.items(): tb.setdefault(m, []).append(v)
    rows = [[HE.get(m, m), m, '%d–%d' % (min(x[0] for x in v), max(x[2] for x in v)), sum(x[3] for x in v)] for m, v in sorted(tb.items(), key=lambda q: -max(x[2] for x in q[1]))]
    h.append('<h3>זמני הטיפול בעמדה (מהעצירה ועד הדחיפה), לפי סוג</h3>' + table(['סוג', 'דגם', 'ש׳', 'ביקורים (3 זרעים)'], rows))
    mixs = {}
    for mx in O['mix']:
        for m, v in mx.items(): mixs[m] = mixs.get(m, 0) + v
    h.append('<h3>התמהיל (נחיתות ב-3 הזרעים)</h3><p>%s</p>' % E(' · '.join('%s %d' % (HE.get(m, m), v) for m, v in sorted(mixs.items(), key=lambda q: -q[1]))))
    h.append('<h3>המסלול, ההסעה והמגבלות שנמדדו</h3><ul>')
    h.append('<li>נחיתה — מהגלגול ועד פינוי המסלול: %s ש׳ (מינ׳ / חציון / מקס׳); המראה — מהכניסה לקו ועד באוויר: %s ש׳; הסעה פנימה ~30 ש׳, החוצה ~70 ש׳, המתנה בקו ~3 ש׳.</li>' % (' / '.join(map(str, O['rotA'])), ' / '.join(map(str, O['rotD']))))
    why = {}
    for w in O['why']:
        for k, v in w.items(): why[k] = why.get(k, 0) + v
    WHE = {'no-fuel-vehicle': 'אין מכלית', 'stand-blocked-in-dwell': 'העמדה תפוסה', 'no-arrival-slot': 'אין חלון נחיתה', 'no-gpu-vehicle': 'אין GPU', 'no-cargo-train': 'אין רכבת מטען',
           'no-remote-ground-service': 'אין שירות במרוחקת', 'no-catering-vehicle': 'אין קייטרינג', 'no-baggage-vehicle': 'אין רכבת כבודה', 'no-nb-bus': 'אין אוטובוס', 'no-water-vehicle': 'אין מים',
           'no-cleaning-vehicle': 'אין ניקיון', 'no-lavatory-vehicle': 'אין שירותים', 'no-departure-chain': 'אין שרשרת המראה'}
    h.append('<li>הניסיונות שנדחו בתכנון (סכום 3 הזרעים) — מה חסר בישן: %s. כלומר: <b>המכליות וה-GPU היו צוואר הבקבוק של הישן</b>, לא המסלול.</li>' % E(' · '.join('%s %d' % (WHE.get(k, k), v) for k, v in sorted(why.items(), key=lambda q: -q[1])[:9])))
    fl = O['fleet']; h.append('<li>הצי הישן (זרע 777): %s — כלומר %d כלים, %d עבדו בחלון.</li>' % (E(' · '.join('%s %d/%d' % (k, v['n'], v['used']) for k, v in fl.items())), sum(v['n'] for v in fl.values()), sum(v['used'] for v in fl.values())))
    h.append('<li>העמדות של הישן: 16 בחוץ (P1–P3 בשרוול, ‏P4 לרחב / LG, ‏P5 / P6 מרוחקות, ‏C1–C3 מטען, ‏GA1–GA3, ‏GA7 / GA8, ‏O2; ‏GA4 חונה), 3 בהאנגרים (M1–M3), 7 מנחתים (H1–H6, ‏O1). הכבודה — 3 נקודות עבודה (MU-A, ‏MU-B, ‏MU-C).</li></ul></section>')
    # 2. החדש היום
    h.append('<section><h2>2. השדה החדש היום (S7F298) — מהמשחק עצמו (q_new_ops.js)</h2><ul>')
    h.append('<li>%d טיסות במחזור של 720 ש׳ → <b>%g</b> תנועות ב-1800 ש׳ (הביקורת מדדה 30). הלוח: %s.</li>' % (N['flights'], N['moves1800'], E(' · '.join('%s %s' % (q[0], HE.get(q[1], q[1])) for q in N['sched']))))
    h.append('<li>19 סימוני עמדות: 18 עצמאיות (CH חופפת ל-C1 / C2); בשימוש 6. ‏GA2–GA7 — האף ב-y 2028 כי הכביש חוצה את העמדה (D‑650): נכנסים רק דו-מנועי קל ומטוס קל; מטוס מנהלים — רק GA1. ‏R3 — מטוס התחזוקה (גרירה מהאנגר א׳) עומד שם 140–688 ש׳ בכל מחזור.</li>')
    h.append('<li>רכבי שירות: %d חניות, %d במסלול מתוזמן; כבודה — עצירה אחת באולם (BAG5): %s.</li>' % (N['spots'], N['veh'], E(' · '.join(N['hall']))))
    h.append('<li>נוסעים בשערים: %s (מצוירים לכל כיוון); 312 מושבים ב-7 אזורי שער.</li>' % E(' · '.join('%s %d' % (q['g'], q['nA']) for q in N['term'])))
    h.append('<li>הגאומטריה המדודה של S15SIM (הבסיס לחישוב): ריצת המראה %.2f ש׳, טיפוס עד היציאה %.2f, כניסה לקו %.2f, גישה %.1f, גלגול עד A3 %.1f ש׳.</li></ul></section>' % (R['K']['roll'], R['K']['climb'], R['K']['lineup'], R['K']['app'], R['K']['roll_out']))
    # 3. מטריצת השירות
    h.append('<section><h2>3. מטריצת השירות — כל סוג מטוס, כל שירות</h2><p>בכל תא: הרכב × כמה, והמשך ליד המטוס (ש׳). "מרוחקת" — רק בעמדה בלי שרוול (R, ‏C). המקור של כל משך — בכלי (fc_calc.py, ‏MATRIX — השדה note: ‏S15SIM או הישן). ההצעה לבדיקה החוסמת: <b>s15SvcAudit</b> — לכל טיסה בלוח, כל שירות שבשורה שלה מתוזמן (רכב, התחלה, סוף) בין העצירה לדחיפה; שירות חסר או חופף — כישלון.</p>')
    keys = ['push', 'gpu', 'stairs', 'bus', 'bags', 'belt', 'uld', 'uld2', 'fuel', 'cater', 'water', 'lav', 'clean', 'pax_walk', 'dock']
    SH = dict(R['svc_he']); SH['uld2'] = 'עגלות מכולות'
    rows = []
    order = ['AC-PR-01', 'AC-LT-01', 'AC-BJ-01', 'AC-CN-01', 'AC-AM-01', 'AC-TP-01', 'AC-RJ-01', 'AC-QJ-01', 'AC-NB-01', 'AC-MW-01', 'AC-LG-01', 'AC-TB-01', 'AC-CG-01', 'AC-HC-01']
    for m in order:
        S = R['matrix'][m]; row = [HE.get(m, m)]
        for k in keys:
            v = S.get(k)
            if not v: row.append('—'); continue
            vt = v.get('veh'); c = ('%s×%d' % (vt, v['n']) if vt else 'צוות') + ' · %d' % v['d'] + (' (מרוחקת)' if v.get('remote_only') else '')
            row.append(c)
        rows.append(row)
    h.append(table(['סוג'] + [SH.get(k, k) for k in keys], rows, 'mx'))
    h.append('<p class="small">מסוקים: דלק (מתדלק קטן), הסעת נוסעים ברגל / רכב, אמבולנס או ניידת בקריאה. בכל סוג גם: מכוון, סדי גלגלים וקונוסים. כבאות בהמתנה — בתדלוק עם נוסעים בתוך המטוס (לא בתוכנית — לאישורך).</p></section>')
    # 4. החישוב
    rt = R['rwy_theory']
    h.append('<section><h2>4. החישוב — כמה טיסות השדה החדש יכול, ומה מגביל</h2>')
    h.append('<h3>המסלול 09/27 (אחד)</h3><p>כללי המרווח (ש׳): נחיתה אחרי נחיתה — הסף אחרי שהקודמת פינתה +%d; המראה אחרי נחיתה — הריצה אחרי הפינוי +%d; נחיתה אחרי המראה — הסף אחרי שהמריאה +%d; המראה אחרי המראה +%d; אחרי כבד (LG / MW / CG / HC) — עוד %d. זמן הנחיתה על המסלול: %g ש׳ ביציאה A3, ‏%g ש׳ ביציאה המהירה A2 (קלים, אזוריים, מנהלים). זוג נחיתה + המראה של צר-גוף: %g ש׳ → עד <b>%g</b> תנועות ב-1800 ש׳ בתיאוריה (אזורי: %g).</p>' % (
        R['SEP']['AA'], R['SEP']['AD'], R['SEP']['DA'], R['SEP']['DD'], R['SEP']['wake'], R['ROT']['A3'], R['ROT']['A2'], rt['NB']['pair_s'], rt['NB']['moves_per1800'], rt['RJ']['moves_per1800']))
    h.append('<p>הכלי של S15 (s15_sim.py) סופר כ"תפוס" את כל רגל הגישה (10.8 ש׳ מקצה העולם) ועוד 8 ש׳ מכל צד — זוג נחיתה + המראה ≈ 58 ש׳ ולכן הוא מצא מקום ל-5–6 טיסות בלבד. עם הכללים שלמעלה המסלול <b>אינו</b> צוואר הבקבוק.</p>')
    h.append('<h3>הקישור הדרומי B + C — צוואר הבקבוק האמיתי</h3><p>כל המטוסים של העמדות הדרומיות (GA1–GA7, ‏R1–R3) עוברים ב-B (מסלול הסעה אחד ברוחב 15 מ׳, 2020 פיקס׳) ובחלק של C. נמדד במשחק (try6641): ‏48 ש׳ צפונה, 60 ש׳ דרומה (הסעה ב-60 פיקס׳/ש׳). בתוכנית — 90 פיקס׳/ש׳ בקטע הישר (≈ 17 קשר, כמו בשדה אמיתי): ‏37 / 49 ש׳. שני כיוונים לא נפגשים ב-B; אותו כיוון — 10 ש׳ ביניהם, בלי עקיפה. ב-C — רק הקטע המשותף. בהסעה של היום (60) נכנסות רק 17 מתוך 18 הטיסות (85 תנועות).</p>')
    rows = []
    for k, nm in (('base', 'שלב א׳ — 18 עמדות × סבב אחד'), ('max', 'סבב שני בעמדות הקלות — אם נכנס (%s)' % (', '.join(R['scen']['max'].get('added') or []) or 'לא נכנס אף אחד: B מלא')), ('b2', 'אפשרות B2 — מסלול הסעה מקביל לקלים')):
        v = R['scen'][k]; rows.append([nm, v['rwy']['moves'], v['rwy']['per1800'], '%.1f%%' % v['rwy']['util'], v['link']['traversals'], '%.1f%%' % v['link']['util'], ', '.join('%s' % m[0] for m in v['miss']) or '—'])
    h.append(table(['תרחיש', 'תנועות ב-720', 'ב-1800 ש׳', 'ניצול המסלול', 'מעברים ב-B', 'ניצול B', 'לא נכנסו'], rows))
    b2 = next((o for o in R['clear']['options'] if o['id'] == 'B2-option'), None)
    h.append('<p><b>B2 נפסל בבדיקת המרווחים:</b> %s. לכן התוכנית בלי B2; ‏B נשאר המגבלה של הדרום (%.0f%%).</p>' % (E(b2['det']) if b2 else '', R['scen'][R['pick']]['link']['util']))
    try:
        runs = []
        for fn, nm in (('fc_sim_result.json', 'הסדר: הדרום קודם'), ('fc_sim_result_big.json', 'הסדר: הגדולים קודם')):
            pth = os.path.join(HERE, fn)
            if os.path.exists(pth): runs.append((nm, json.load(open(pth, encoding='utf-8'))))
        if runs:
            h.append('<h3>האימות במחולל של S15 עצמו — והפער</h3><p>tools/fc_sim.py מריץ את s15_sim.py (הכלי שבנה את S15SIM — המסלולים, הפניות ובדיקת המעטפות OBB של כל מטוס מול כל מטוס וכל חונה, כל 2 ש׳) עם 3 שינויים בלבד: המסלול "תפוס" רק כשהמטוס עליו ונמוך מ-40, מרווח 3 ש׳ (+8 אחרי כבד), והעמדות הדרומיות דרך C ו-B.</p>')
            rows = [[nm, FS['flights'], FS['moves1800'], '×%.1f' % (FS['moves1800'] / max(O['moves'])), '%g%%' % FS['rwy_util'], ', '.join(q[0] for q in FS['sched']), ', '.join(FS['miss']) or '—'] for nm, FS in runs]
            h.append(table(['ריצה', 'טיסות', 'תנועות ב-1800', 'מול הישן', 'המסלול תפוס', 'נכנסו', 'לא נכנסו'], rows))
            h.append('<p><b>הפער מול החישוב:</b> המחולל של S15 קובע לכל טיסה נתיב קבוע בזמן — בלי המתנה בדרך (רק בקו ההמתנה של המסלול), והחיפוש שלו גס (דחיפה כל 12 ש׳, נחיתה כל 8). לכן מטוס שנתקל באחר במסלול ההסעה A או ב-B נדחה כולו, גם כשהמסלול עצמו פנוי (ניצול 57%). <b>כדי להגיע ל-90:</b> מחולל עם המתנות — בעמדה לפני הדחיפה, בנקודות ההמתנה של A / B / C ובכניסה לעמדה — כמו המתכנן הישן (AO, ‏044: הזמנות מרחב־זמן עם תור), וחיפוש עדין. זה הצעד הראשון של הבנייה של הלוח (סעיף "מה נשאר").</p>')
    except Exception:
        pass
    h.append('<h3>הלוח המוצע (מחזור של 720 ש׳)</h3>')
    rows = []
    for f in sorted(R['schedule'], key=lambda q: q['roll']):
        rows.append([f['stand'], HE.get(f['model'], f['model']), f['airline'], f['push'], f['roll'], f['thr'], f['onblock'], round(f['dwell']), f['hold_wait']])
    h.append(table(['עמדה', 'סוג', 'חברה', 'דחיפה', 'המראה', 'נחיתה (סף)', 'עצירה', 'עמידה (ש׳)', 'המתנה בקו'], rows))
    hp = R['heli_plan']
    h.append('<p>מסוקים (בלי המסלול): %s סבבים ב-720 ש׳ → %g תנועות ב-1800 ש׳ — כמו הישן (%d–%d). האמפיבי: 2 סבבים במחזור על מסלול המים (10 תנועות מים ב-1800 ש׳), בנוסף למה שיש היום ב-G6 / H6.</p></section>' % (
        E(' · '.join('%s %g' % kv for kv in hp['sorties720'].items())), hp['moves1800'], min(hp['old']), max(hp['old'])))
    # 5. כמה צריך
    h.append('<section><h2>5. כמה צריך מכל דבר</h2><h3>רכבי שירות (המינימום שבו כל שירות נכנס בחלון שלו, ועוד רזרבה מ-3 ומעלה)</h3>')
    rows = []; tot_n = tot_t = 0
    for k, v in R['fleet'].items():
        rows.append([v['he'], k, v['trips'], v['peak'], v['kmin'], '<b>%d</b>' % v['need'], v['today_spots'], v['old'] if v['old'] is not None else '—', '%d%%' % v['util']])
        tot_n += v['need']; tot_t += v['today_spots']
    h.append(table(['רכב', 'קוד', 'עבודות במחזור', 'שיא (זמנים קבועים)', 'מינימום', 'צריך', 'היום (חניות)', 'הישן', 'ניצול'], rows))
    h.append('<p>סה״כ הצי המתוזמן: <b>%d</b> (היום %d בשורות האלה). נוסף על זה בלי לוח: 3 כבאיות, אמבולנס, ניידת, 3 "עקוב אחריי", מכסחת, הסעת צוות. ההפרש — בבסיס הצי הדרומי בהרחבה (28 חניות — סעיף 9).</p>' % (tot_n, tot_t))
    h.append('<h3>אולמות הכבודה — התור לכל מספר עמדות (קצב 2.2 ש׳ ליחידה, הכנה 4, כניסה 10, פינוי 12)</h3>')
    rows = [[q['stations'], q['visits'], q['units_hour'], '%.1f%%' % q['util'], q['wait_mean'], q['wait_max'], q['late']] for q in R['halls']]
    h.append(table(['עמדות', 'ביקורים במחזור', 'יחידות לשעה', 'ניצול', 'המתנה ממוצעת', 'המתנה מקס׳', 'מחכות מעל 30 ש׳'], rows))
    h.append('<p><b>מסקנה:</b> עמדה אחת — 150% (התור לא נגמר); 4 — עדיין 2 רכבות שמחכות מעל 30 ש׳; <b>5 — בלי המתנה</b>. לכן 5 עמדות עצמאיות (ומינימום 4). ביעד של פי 2 מהישן (הבודק: 1,704–1,776 יחידות לשעה) — 5 עמדות בניצול ~40% (בתור משותף; לפי השיוך בפועל — סעיף 9).</p>')
    h.append('<h3>נוסעים ומושבים (נוסע מצויר לכל %d; היום ~1:11)</h3>' % R['VIS'])
    rows = [[g, v['seats'], v['peak'], v['avg'], '<span class="%s">%s</span>' % ('ok' if v['ok'] else 'bad', 'מספיק' if v['ok'] else 'חסרים %d' % (v['peak'] - v['seats']))] for g, v in R['pax']['gates'].items()]
    h.append(table(['שער', 'מושבים היום', 'ממתינים בשיא', 'ממוצע', 'מצב'], rows))
    h.append('<p>בסבב: %d נוסעים (נומינלי), %d מצוירים — מול 4.3 בממוצע ו-13 בשיא היום. חסרים מושבים ב-P6 (‏LG), ב-P1 וב-R.</p>' % (R['pax']['nominal_cycle'], R['pax']['visual_cycle']))
    c = R['crew']
    h.append('<h3>צוותים</h3><p>בשיא: %d ברכבים, %d מכוונים, %d באולמות הכבודה; ועוד מגדל %d וכבאות בכוננות %d → סגל של <b>%d</b> (שיא × 1.15).</p></section>' % (c['vehicles'], c['marshal'], c['hall'], c['tower'], c['arff_standby'], c['roster']))
    # 6. הציור
    h.append('<section><h2>6. הציור</h2><p class="cap">צפון למעלה, קנה מידה של העולם. בצבע — המטוס של הלוח בכל עמדה (גוף, כנף, זנב). כתום — 5 עמדות הכבודה; מקווקו אדום — R3 בלי מטוס קבוע (ביום טיסות, בלילה הרצת מנועים); ירוק־אפור מקווקו — ההרחבה הדרומית־מזרחית עם בסיס הצי, המזח הצף ומסלול המים של האמפיבי; סגול — המספנה והמעגן (LIKE-08, לא זזים).</p>')
    h.append('<div class="fig">%s</div>' % svg_main())
    h.append('<h3>עמדות הכבודה מתחת לאגף השערים (קומת הרחבה)</h3><p class="cap">לכל עמדה דלת כניסה ודלת יציאה משלה בקיר הצפוני (y 886), נתיב U, מסוע ועצירה — כמו האולם של היום (BAG5), שנשאר BH-3. הנתיב והמסוע בצפון האולם (y ≤ 950), כי במבט 3/4 הקיר של הטרמינל מסתיר את מה שמדרום ל-y ~943. ‏BH-5 — בקצה המזרחי של CE, עם תוספת בגג שקוף עד שביל השירות SR_E. הרכבת המצוירת — טרקטור + 2 עגלות במידות הציור (%.0f × %.0f).</p>' % (R['layout']['train']['L'], R['layout']['train']['W']))
    h.append('<div class="fig">%s</div>' % svg_halls())
    chg = R['clear'].get('changes') or []
    if chg:
        h.append('<p><b>מה זה דורש בקומת השערים:</b> כל עמדה חדשה נמצאת מתחת לטרקלין של שער (כך זה בשדה אמיתי). במבט 3/4 הטרקלין מסתיר אותה — לכן מעל כל עמדה רצפת זכוכית (כמו המעבר מעל BAG5 היום), והמושבים שבתוך הרצועה עוברים דרומה / לאגף מזרח. בסך הכול %d מושבים: %s. בכל מקרה חסרים מושבים לענקים (סעיף 5) — המושבים שזזים נכנסים לתוכנית המושבים החדשה של הטרמינל.</p>' % (
            sum(int(c['det'].split(' — ')[1].split(' ')[0]) for c in chg), E(' · '.join(c['det'].split(':')[0] + ' ' + c['det'].split('(')[1].split(')')[0] for c in chg))))
    h.append('<h3>קומת השערים — היום ואחרי ("ללטש ולעצב מחדש")</h3><p class="cap">היום: הטרקלינים של P1–P5 (נקודות — 312 המושבים) תופסים את הרצועה הצפונית, ורק BAG5 פנוי. אחרי: 5 עמדות הכבודה ברצועה הצפונית (y 905–1015, הנתיב והמסוע עד y 950 כמו BAG5), והטרקלינים ברצועה הדרומית (y 966–1028); ‏P6 ו-R — באגף מזרח. המדרגות ושורשי השרוולים — לא זזים.</p>')
    h.append('<div class="fig">%s</div><div class="fig">%s</div>' % (svg_floor(False), svg_floor(True)))
    rows = [[l['g'], l['today'], l['cap'], l['need'] if l['need'] is not None else '—', l.get('note', '')] for l in R['lounges']]
    h.append(table(['טרקלין', 'מושבים היום', 'אחרי', 'ממתינים בשיא (1:5)', 'הערה'], rows))
    rows = [[q['id'], q['he'], ' / '.join(q['serves']), '%s–%s' % tuple(q['din']), '%s–%s' % tuple(q['dout']), q['lane']] for q in R['layout']['halls']]
    h.append(table(['עמדה', 'מה', 'משרתת', 'דלת כניסה (x)', 'דלת יציאה (x)', 'הנתיב (y)'], rows))
    h.append('</section>')
    # 7. בדיקת המרווחים
    cl = R['clear']
    h.append('<section><h2>7. בדיקת המרווחים האוטומטית (fc_calc.py — לא ok=true קבוע)</h2>')
    h.append('<p>%d בדיקות · <b>%d כישלונות</b>. הבדיקה העצמית — פריסה שגויה בכוונה (מטוס מנהלים ב-GA5, אולם על המדרגות של P2) — נכשלת כמו שצריך: %s.</p>' % (cl['checks'], cl['fails'], E(', '.join(R['selftest']['ids']))))
    groups = {}
    for r in cl['list']:
        g = r['id'].split('-')[0]; groups.setdefault(g, [0, 0, 0, 0]); groups[g][0] += 1; groups[g][1] += (1 if (not r['ok'] and r['kind'] == 'FAIL') else 0); groups[g][2] += (1 if r['kind'] == 'INFO' else 0); groups[g][3] += (1 if r['kind'] in ('CHANGE', 'OPTION') and not r['ok'] else 0)
    GH = {'stand': 'המטוס בתוך העמדה', 'wingtip': 'קצות כנפיים בין עמדות', 'pocket': 'כיסי הציוד מול הגוף / הכנף / הזנב', 'BH': 'עמדות הכבודה', 'halls': 'בין האולמות', 'lanes': 'שני נתיבים באולם',
          'exp': 'ההרחבה', 'gse': 'בסיס הצי הדרומי', 'amph': 'האמפיבי', 'R3': 'הרצת המנועים ב-R3', 'B2': 'אפשרות B2'}
    rows = [[GH.get(g, g), v[0], v[1], v[2], v[3]] for g, v in groups.items()]
    h.append(table(['קבוצה', 'בדיקות', 'כישלונות', 'מידע בלבד', 'שינוי נדרש / אפשרות שנפסלה'], rows))
    h.append('<details><summary>כל הבדיקות</summary>%s</details></section>' % table(['', 'בדיקה', 'פירוט'], [['<span class="%s">%s</span>' % ('ok' if r['ok'] else ('bad' if r['kind'] == 'FAIL' else 'wait'), '✓' if r['ok'] else '✗'), r['id'], r['det']] for r in cl['list']]))
    # 8. לאישורך
    h.append('<section><h2>8. לאישורך · סתירות · תלות</h2><ul>')
    for li in ('ההנחות של המספרים: מושבים × תפוסה (צר-גוף 180 × 0.81 = 146, כמו הטיסה הישנה), נוסע מצויר לכל 5, יחידות כבודה (צר 12 לכל כיוון, רחב 24–32).',
               'זמני העמידה: צר 400, ‏LG ‏470, ‏CG ‏440 — רק עם רכבים כפולים לרחבים ולמטען (מסוע ×2, רכבת ×2, קייטרינג ×2, ‏HL + 2 גררי עגלות).',
               'כללי המרווח במסלול (2 / 2 / 3 / 4 + 8 אחרי כבד) — במקום הספירה של s15_sim.py (כל רגל הגישה + 8 מכל צד). בלי זה — 5–6 טיסות, כמו היום.',
               'מסלול אחד בכיוון אחד (09 ביום, 27 לפי רוח ביום משחק אחר); בלי המראות ונחיתות מנוגדות בבת אחת. החלפת הכיוון לא מוסיפה קיבולת — רק מקצרת הסעה לדרום.',
               'GA2–GA7 — רק קלים (הכביש חוצה את העמדות, D‑650); מנהלים — GA1 ו-R3 ביום. הענקים P1 / P6 טסים בכל מחזור. התמהיל המדויק במשחק — fieldfix.',
               'ההרחבה הדרומית־מזרחית (H4, ‏x 8480–9600, ‏y 2550–2830): בסיס צי דרומי (28 חניות) ומזח צף לאמפיבי; בלי עמדות מטוסים — אין אליהן דרך הסעה בלי לחתוך את R3. עמדות נוספות — רק עם קישור חדש לדרום (B2 נבדק ונפסל: 0.4 מ׳ מהגדר).',
               'מסלול המים של האמפיבי (y 3480–3580) — בין שטח הדיג של המכמורת TRAWL-1 (y 3080–3320, 05:20–17:00) לנתיב האוניות LANE-L1 (המצופים ב-y 3620). חוצה את נתיב הסירות של המספנה ואת שטח הדיג רק בהסעה, בחצייה אחת (H1 ↔ H2), כששניהם פנויים — busy() של 074zm, גם המכמורות; כמו ב-074zm (נתיב השיט ב-y 4350).',
               '5 עמדות הכבודה בקומת הרחבה של אגף השערים: BH-1 ‏6812–7016 (המדרגות של P1 עוברות לקיר המערבי ויורדות דרומה, המשטח בגובה השורש), ‏BH-2 ‏7165–7400, ‏BH-3 = BAG5 של היום, ‏BH-4 ‏8002–8235 (ממזרח למדרגות הנעות של P4), ‏BH-5 ‏8314–8505 (תוספת בגג שקוף). בלי להזיז מדרגות — 4 עמדות (המינימום).',
               'קומת השערים מתעצבת מחדש ("ללטש ולעצב מחדש"): הטרקלינים עוברים לרצועה הדרומית (y 966–1028), 197 מושבים זזים מעל העמדות; ‏P6 ו-R — באגף מזרח; בכל טרקלין יותר מושבים מהיום (סעיף 6).',
               'סתירה: S15D.stands רושם מטוס מנהלים כסוג של GA5–GA7, אבל האף שם ב-y 2028 והמטוס לא נכנס (הבדיקה stand-in-GA5 נכשלת עליו). ברירת המחדל: רק קלים שם.',
               'תלות: fieldfix — התמהיל, R3 בלילה, הצבעים; ‏missions / pier — M-F2-PICKUP על הלוח החדש; ‏perf — יותר נוסעים ורכבים מצוירים; ‏locks — השערים של הצד האווירי.'):
        h.append('<li>%s</li>' % E(li))
    h.append('</ul></section>')
    if R2: h.append(sec9())
    h.append(sec10())
    h.append(sec11())
    if SP: h.append(sec12())
    h.append(sec13())
    h.append(sec14())
    css = """:root{--bg:#f4f3ef;--card:#ffffff;--ink:#1c252c;--mut:#56616a;--line:#d6d2c6;--head:#e9e6dc;--acc:#c2571a;--ok:#1f7a3a;--bad:#b3261e;--wait:#b5650f;
--m-bg:#e8eee4;--m-air:#dfe6d8;--m-sea:#bcd6e6;--m-land:#dfe6d8;--m-apron:#cfd3d6;--m-rwy:#3c4248;--m-twy:#9aa1a7;--m-road:#e9d9a6;--m-bld:#b8b1a4;--m-base:#c9c2b5;--m-pocket:#f0e2b6;--m-hall:#e8892f;--m-exp:#cfd8c4;--m-like:#a58fcf;--m-txt:#1c252c}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15191d;--card:#1e2328;--ink:#e6e9ec;--mut:#a3adb6;--line:#343b42;--head:#262c32;--acc:#f08a4b;--ok:#5cc27a;--bad:#ff7a6e;--wait:#f0a54b;
--m-bg:#1b2420;--m-air:#24302a;--m-sea:#1d3446;--m-land:#24302a;--m-apron:#3a4045;--m-rwy:#0f1215;--m-twy:#5d656c;--m-road:#6b5f3a;--m-bld:#5e584f;--m-base:#4d483f;--m-pocket:#5c5236;--m-hall:#f08a4b;--m-exp:#36412f;--m-like:#7c66a8;--m-txt:#e6e9ec}}
:root[data-theme="dark"]{--bg:#15191d;--card:#1e2328;--ink:#e6e9ec;--mut:#a3adb6;--line:#343b42;--head:#262c32;--acc:#f08a4b;--ok:#5cc27a;--bad:#ff7a6e;--wait:#f0a54b;
--m-bg:#1b2420;--m-air:#24302a;--m-sea:#1d3446;--m-land:#24302a;--m-apron:#3a4045;--m-rwy:#0f1215;--m-twy:#5d656c;--m-road:#6b5f3a;--m-bld:#5e584f;--m-base:#4d483f;--m-pocket:#5c5236;--m-hall:#f08a4b;--m-exp:#36412f;--m-like:#7c66a8;--m-txt:#e6e9ec}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Arial,Helvetica,sans-serif;direction:rtl;line-height:1.5}
main{max-width:1400px;margin:0 auto;padding:16px}h1{font-size:26px;margin:6px 0}h2{font-size:20px;margin:26px 0 8px;border-bottom:2px solid var(--line);padding-bottom:4px}h3{font-size:16px;margin:16px 0 6px}
.cap,.small{color:var(--mut);font-size:13.5px}.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:12px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px}.kpi .k{font-size:13px;color:var(--mut)}.kpi .v{font-size:28px;font-weight:700;color:var(--acc)}.kpi .s{font-size:12.5px;color:var(--mut)}
.tw{overflow-x:auto;margin:6px 0}table{border-collapse:collapse;width:100%;font-size:13.5px;background:var(--card)}th,td{border:1px solid var(--line);padding:5px 7px;text-align:right;vertical-align:top}th{background:var(--head)}
table.mx td{font-size:12px;white-space:nowrap}.ok{color:var(--ok);font-weight:700}.bad{color:var(--bad);font-weight:700}.wait{color:var(--wait);font-weight:700}
.fig{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px;margin:10px 0}svg.map{width:100%;height:auto;display:block}
svg .bg{fill:var(--m-bg)}svg .sea{fill:var(--m-sea)}svg .land{fill:var(--m-land)}svg .air{fill:var(--m-air);stroke:#7d8a6e;stroke-width:6;stroke-dasharray:24 14}
svg .apron{fill:var(--m-apron)}svg .rwy{fill:var(--m-rwy)}svg .cl{stroke:#fff;stroke-width:6;stroke-dasharray:60 40}svg .twy{fill:var(--m-twy)}svg .road{fill:var(--m-road)}
svg .bld{fill:var(--m-bld)}svg .base{fill:var(--m-base);stroke:var(--line);stroke-width:2}svg .pocket{fill:var(--m-pocket);stroke:#b19a52;stroke-width:2}
svg .stand{fill:none;stroke:#fff;stroke-width:3;stroke-dasharray:10 8;opacity:.8}svg .stand.r3{stroke:#d33;stroke-width:6}svg .stand.alt{stroke:#999;stroke-dasharray:4 10}
svg .ac{opacity:.92}svg .br{stroke:#e6c84b;stroke-width:12}svg .hp{fill:none;stroke:#e8b92b;stroke-width:8}svg .runup{fill:none;stroke:#d33;stroke-width:4;stroke-dasharray:14 10}svg .blast{fill:#7b4b2a}
svg .hall{fill:var(--m-hall);opacity:.95}svg .hall.today{stroke:#fff;stroke-width:4}svg .exp{fill:var(--m-exp);stroke:#6f8a5d;stroke-width:6;stroke-dasharray:20 12}svg .gse{fill:#e9c46a;stroke:#8a6d1f;stroke-width:2}
svg .dock{fill:#8d6e4f}svg .bagf{stroke:rgba(20,24,28,.35);stroke-width:2}svg .bagrib{stroke:rgba(0,0,0,.25);stroke-width:3}svg .bagd{fill:rgba(20,24,28,.6)}svg .bagw{fill:#15181b}svg .bagz{stroke:rgba(235,238,240,.7);stroke-width:2}svg .bagh{fill:none;stroke:rgba(20,24,28,.6);stroke-width:4}svg .bags{fill:rgba(30,32,36,.5)}svg .bagt{fill:#f4efe0}svg .bagbb{fill:none;stroke:var(--m-txt);stroke-width:1.5;stroke-dasharray:6 5;opacity:.6}svg .baglab{font-size:22px;fill:var(--m-txt)}svg .spot0{fill:#7b8794;stroke:#4b5560;stroke-width:1.5}svg .spotN{fill:#e8892f;stroke:#7a3d0c;stroke-width:2}svg .spl{font-size:16px;fill:var(--m-txt)}svg .trawl{fill:rgba(120,90,40,.16);stroke:#8a6d3b;stroke-width:4;stroke-dasharray:18 10}svg .slane{fill:rgba(30,60,120,.08);stroke:#3a5a8c;stroke-width:3;stroke-dasharray:6 10}svg .buoy{fill:#2e8b57;stroke:#fff;stroke-width:3}svg .xzone{fill:rgba(179,38,30,.08);stroke:#b3261e;stroke-width:3;stroke-dasharray:10 8}svg .wlane{fill:none;stroke:#2a6f97;stroke-width:6;stroke-dasharray:30 18}svg .wtaxi{fill:none;stroke:#2a6f97;stroke-width:5;stroke-dasharray:12 10}
svg .like{fill:none;stroke:var(--m-like);stroke-width:8}svg .blane{fill:none;stroke:#557;stroke-width:5;stroke-dasharray:6 12}svg .opt{fill:none;stroke:#b3261e;stroke-width:4;stroke-dasharray:8 10}
svg text{fill:var(--m-txt);font-family:Arial,Helvetica,sans-serif}svg .rw{fill:#fff;font-weight:700}svg .tw{fill:#fff;font-weight:700}svg .st{font-weight:700;font-size:34px}svg .lbs{font-size:26px}svg .hpl{fill:#e8b92b;font-weight:700}
svg .hl{fill:var(--acc);font-weight:700}svg .wl{fill:#2a6f97;font-weight:700}svg .lk{fill:var(--m-like);font-weight:700}svg .opt2{fill:#b3261e;font-weight:700}
svg .nArrow line,svg .scale line{stroke:var(--m-txt);stroke-width:8}svg .nArrow text,svg .scale text{font-size:40px;font-weight:700}
svg.halls .hallbox{fill:#f3d3b3;stroke:var(--m-hall);stroke-width:2}svg.halls .hallbox.today{stroke-width:3;stroke-dasharray:6 4}svg .door{fill:#2b3138}svg .stairs{fill:#7d9bb5}svg .stairs.old{fill:none;stroke:#b3261e;stroke-dasharray:4 3}svg .stairs.moved{fill:#5d86ad}svg .root{fill:#e6c84b}
svg .zone{fill:#dfe6ee;stroke:#8aa0b4;stroke-width:1.5}svg .zone.bag{fill:#f3d3b3;stroke:var(--m-hall)}svg .seat{fill:#3f6fa6}svg .upath{fill:none;stroke:#2b3138;stroke-width:2;stroke-dasharray:5 4}svg .belt{fill:#4a4f55}svg .train{fill:#2e7d6b;opacity:.75}svg .hid{font-weight:700;fill:#fff}
svg .fence{stroke:#7d8a6e;stroke-width:8;stroke-dasharray:24 14}svg .circ{fill:none;stroke:#2a6f97;stroke-width:6;stroke-dasharray:4 14}svg .pt{fill:#2a6f97}svg .hold{fill:none;stroke:#b3261e;stroke-width:5}svg .busr{fill:none;stroke:#e9c46a;stroke-width:8;stroke-dasharray:14 8}svg .am{fill:#2a9d8f}svg .agate{fill:#b3261e}svg .haz{fill:#d33;opacity:.18;stroke:#d33;stroke-width:3;stroke-dasharray:10 8}svg .xc{fill:none;stroke:#b3261e;stroke-width:8}svg .xcl{fill:#b3261e;font-weight:700}svg .bay{fill:var(--m-twy);stroke:#b3261e;stroke-width:4;stroke-dasharray:10 6}
details{margin:8px 0}summary{cursor:pointer;color:var(--acc)}@media (max-width:700px){main{padding:10px 16px}h1{font-size:21px}table{font-size:12px}.kpi .v{font-size:22px}}"""
    doc = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>חישוב השדה החדש</title><style>%s</style></head><body><main>%s</main></body></html>' % (css, ''.join(h))
    return doc

def sec9():
    X = R2; h = ['<section><h2>9. אחרי הבקר (planrev 07:35) והמתאם (07:46) — מה נוסף לחישוב (fc_calc2.py)</h2>']
    h.append('<p class="cap">אותו לוח (סעיף 4) ואותן פונקציות של fc_calc.py; הכלי נכשל (קוד 1) אם עמדת כבודה מעל 60%%, חנייה באזור ההדף, דרך שירות שחוצה את B, או גרירת תחזוקה בלי חלון. התוצאה: <b>%s</b>.</p>' % ('עובר' if X['ok'] else 'נכשל — ' + E(' · '.join(X['fails']))))
    # היעד — מותנה
    g = X.get('generator') or {}
    rows = [[n.replace('fc_sim_result', '').replace('.json', '') or 'בסיס', v['flights'], v['moves1800'], '%g%%' % v['rwy_util'], 'כן' if v.get('waits') else 'לא', v.get('taxi') or 60, ', '.join(v['miss']) or '—'] for n, v in g.items()]
    h.append('<h3>(1) היעד — במחולל, לא רק בחישוב</h3><p>90 ב-1800 ש׳ בחישוב <b>מותנה</b> בשניים: מחולל עם המתנות בדרך (בעמדה אחרי הדחיפה ובחיבור אחרי הנחיתה — כמו התורים של AO) והסעה של 90 פיקס׳/ש׳ בקטעים הישרים של B / A. במחולל של S15 עצמו (fc_sim.py — הבדיקה של כל מטוס מול כל מטוס וכל חונה, OBB כל 2 ש׳):</p>')
    if rows: h.append(table(['ריצה', 'טיסות', 'תנועות ב-1800', 'המסלול תפוס', 'המתנות', 'הסעה', 'לא נכנסו'], rows))
    h.append('<p>הבדיקה החוסמת במשחק עם הלוח החדש: <b>__TC_FC.moves(1800) ≥ 90</b> (היום 30 — לכן היא נכנסת רק עם הלוח). ‏s15SvcAudit — כל שירות מהמטריצה לכל טיסה.</p>')
    rv = X['reserve']; b = rv['bay']
    rows = [['הלוח (סעיף 4)', rv['base']['flights'], rv['base']['rwy']['per1800'], '%g%%' % rv['base']['link']['util'], '—'],
            ['+ מפרץ המתנה באמצע B', b['flights'], b['rwy']['per1800'], '%g%%' % b['link']['util'], 'נכנס סבב שני: ' + (', '.join(b['added']) or '—')],
            ['+ B2 (מסלול לקלים לאורך הגדר)', rv['base']['flights'], rv['b2']['rwy']['per1800'], '%g%%' % rv['b2']['link']['util'], 'B יורד ל-%g%% — עתודה של B לסבבים נוספים; הגדר זזה 3 מ׳ (לאישורך)' % rv['b2']['link']['util']]]
    h.append('<h3>העתודה מעבר ל-90 (B הוא המגבלה)</h3>' + table(['תרחיש', 'טיסות', 'תנועות ב-1800', 'B תפוס', 'הערה'], rows))
    h.append('<p>%s. %s.</p>' % (E(rv['bay_geom']['he']), E(rv['b2']['note'])))
    # עמדות הכבודה
    ha = X['halls_assign']
    rows = [[k, ha['before']['per'][k]['visits'], '%g%%' % ha['before']['per'][k]['util'], ha['after']['per'][k]['visits'], '<b>%g%%</b>' % ha['after']['per'][k]['util'], ha['after']['per'][k]['wait_max']] for k in sorted(ha['after']['per'])]
    h.append('<h3>(2) עמדות הכבודה — לפי השיוך בפועל (תור של רכבת אחת לכל עמדה)</h3>' + table(['עמדה', 'ביקורים — לפני', 'ניצול — לפני', 'ביקורים — אחרי', 'ניצול — אחרי', 'המתנה מקס׳'], rows))
    asg = {}
    for u, hid in ha['after']['assign'].items(): asg.setdefault(hid, []).append(u.replace('/0', ' (רכבת 1)').replace('/1', ' (רכבת 2)') if u.split('/')[0] in ('P1', 'P6') else u.split('/')[0])
    h.append('<p>לפני (השיוך של הציור: P6 + R → BH-5): BH-5 ‏%d מתוך 20 ביקורים — %g%%. אחרי: %s — אף עמדה לא מעל %g%%, בלי המתנה. R עוברות מתחת לטרמינל (AIR-PASS), ולכן העמדות הקרובות למעבר (BH-3 / BH-4); ב-LG שתי הרכבות לשתי עמדות. במשחק (074zr): כל רכבת לעמדה שלה, ואם אין אליה נתיב בלי נגיעה — לקרובה הבאה (היום BT-P2 → BH-2).</p>' % (
        ha['before']['per']['BH-5']['visits'], ha['before']['per']['BH-5']['util'], E(' · '.join('%s: %s' % (k, ', '.join(v)) for k, v in sorted(asg.items()))), ha['after']['max']))
    p6 = X['p6_bh5']
    h.append('<p><b>P6 מול היציאה של BH-5</b> (הנתיב חוצה את המלבן של P6 ליד האף): החלונות החסומים — %s. %s. בלוח: %s.</p>' % (
        E(' · '.join('%s %g–%g' % (w, a, b) for a, b, w in p6['blocks'])), E(p6['rule']), E(' · '.join('%s/%s יוצאת ב-%g — מחכה %g ש׳' % (q['stand'], q['kind'], q['exit'], q['wait']) for q in p6['hits'])) or 'אין'))
    # דרכי השירות
    sr = X['service_roads']
    rows = [[k, v['x'], '%g%%' % v['util'], v['wait_mean'], v['wait_max'], len(v['windows'])] for k, v in sr['cross'].items()]
    h.append('<h3>(3) רכבי השירות שחוצים מסלולי הסעה</h3><p><b>אף דרך שירות לא חוצה את B</b> (נבדק על כל המלבנים של S15D.service מול B: %s). שתי נקודות חצייה של C: %s. הכלל: %s.</p>' % (
        'אין' if not sr['crossB'] else E(', '.join(sr['crossB'])), E(', '.join(sr['crossC'])), E(sr['rule'])))
    h.append(table(['נקודה', 'x', 'מטוסים בנקודה', 'המתנה ממוצעת לרכב (ש׳)', 'המתנה מקס׳', 'חלונות במחזור'], rows))
    h.append('<p>חציות של C במחזור: <b>%d</b> אם כל הצי בבסיס של היום (כל שירות לדרום — הלוך ב-XC_E וחזור ב-XC_W) → <b>%d</b> עם הבסיס הדרומי (רק רכבות הכבודה של R לאולמות בצפון, המכליות מחוות הדלק, המתדלק הקטן במילוי, והלימוזינה). רכב חוצה ב-%g ש׳; התפוסה של הרכבים בנקודה — %g%% → %g%%.</p>' % (
        sr['n_today'], sr['n_south'], sr['veh_cross_s'], sr['veh_occ_today'], sr['veh_occ_south']))
    h.append('<p class="small">הדרך לדרום: %s.<br>רכבות הכבודה של R: %s.</p>' % (E(sr['route_south']), E(sr['route_bags_R'])))
    fs = X['fleet_split']
    rows = [[v['he'], k, v['south'], v['north'], v['total_need'], ', '.join(v['south_stands']) or '—'] for k, v in fs['rows'].items()]
    h.append('<h3>(4) מי חונה בדרום ומי בצפון</h3>' + table(['רכב', 'קוד', 'בבסיס הדרומי', 'בצפון / באמצע', 'צריך (סעיף 5)', 'עמדות בדרום'], rows))
    h.append('<p>בבסיס הדרומי: %d רכבים ב-28 חניות (שתי שורות של 14 — הגבוהים מצפון לדרך, הנמוכים מדרום; רזרבה: %s). %s.</p>' % (fs['south_total'], E(', '.join('%s +%d' % (k, v) for k, v in fs['spare'].items() if v > 0)), E(fs['note'])))
    bl = X['blast']
    h.append('<h3>(5) ההדף של R3 בלילה מול הבסיס הדרומי</h3><p>הקיר %s; אזור ההדף מאחוריו %s, ‏%s. בפריסה הקודמת היו בתוכו %s%s. התיקון: %s → בתוך האזור: %s. נכנס לבדיקת המרווחים.</p>' % (
        bl['wall'], bl['hazard'], E(bl['hours']), E(', '.join(bl['gse_in']) or 'אין'), ' ודרך הבסיס' if bl['road_in'] else '', E(bl['fix']), E(', '.join(bl['gse_fix_in']) or 'אין')))
    # התחזוקה
    rows = [[m['hangar'], m['label'], ', '.join(HE.get(x, x) for x in m['models']), m['in_service'], m['airframes'], m['donor'], '%g / %g' % (m['donor_push'], m['donor_onblock']), m['tow_s'], 'C + B' if m['uses_B'] else 'C', ('%g–%g' % tuple(m['window'])) if m['window'] else '<span class="bad">אין</span>'] for m in X['maint']['rows']]
    h.append('<h3>(6) מחזור התחזוקה — "מתוקנים וחוזרים לטיסות"</h3><p>%s.</p>' % E(X['maint']['cycle']))
    h.append(table(['האנגר', 'מה', 'סוגים', 'בלוח', 'גופים (עם ההאנגר)', 'הטיסה שמקבלת', 'דחיפה / עצירה במחזור', 'גרירה (ש׳)', 'דרך', 'חלון פנוי במחזור'], rows))
    h.append('<p class="small">%s. הביצוע — עם fieldfix (המחזור של R3 כבר אצלם); הלוח הזה — המפרט.</p>' % E(X['maint']['note']))
    rd = X['rwy_dir']
    h.append('<h3>(7) כיוון המסלול מול B</h3><p>%s</p>' % E(rd['text']))
    spd = X['speeds']['rows']
    if spd and 'err' not in spd:
        rows = [[k, v['vmax'], v['vavg'], v['old'], '%+.0f%%' % ((v['vmax'] / v['old'] - 1) * 100)] for k, v in spd.items()]
        h.append('<h3>(8) הקצב — רכבי השירות מול הישן (נמדד במשחק, s15k_fleet)</h3>' + table(['רכב', 'מרבית (קמ״ש)', 'ממוצעת', 'הישן (מרבית)', 'הפרש'], rows))
        h.append('<p>רק MS (מדרגות, נסיעה של 6–9 מ׳ בתוך הכיס) ו-SH איטיים מהישן — אין להם נסיעה ארוכה. משכי הפעולות כמו בישן: מזוודה כל 2.2 ש׳ (הישן 2.2–3.5), מסוע 228–285 ש׳, דלק / קייטרינג / גרירה — לפי הטבלה בסעיף 3 (העמודה "הישן").</p>')
    h.append('<h3>(9) המטריצה — השלמות</h3><ul>')
    for li in ('LG / MW: נשארים עם מסוע ×2 ורכבת ×2 (כמו בישן, ושרשרת המזוודות של המשחק — s15bag — בנויה לכבודה פזורה); מכולות (HL + עגלות) — רק במטען. לאישורך.',
               'מנהלים (BJ / CN): נוסף מים (WT, ‏30 ש׳). הלימוזינה — רכב של העיר שנכנס בשער הצד האווירי G-STAFF (7860, 1495) → AIRROAD_W → BASE_ROAD → XC_E → TAIL_ROAD → GA1 / R3, ובחזרה דרך XC_W (2 חציות של C — בטבלה של סעיף 3); בלי שער חדש. לאישורך.',
               'המזח הצף [8180, 2600, 8470, 2640] — מחוץ לגדר (y 2550) ומחוץ להרחבה. הדרך אליו: שער חדש בגדר G-AMPH (x 8428–8468, בין המנחת O1 ל-R1) והרמפה [8433, 2548, 8463, 2602] יורדת ממנו למזח. הנוסעים — מהשער של R בטרמינל (TE-BUS, 56 מושבים) באוטובוס הרחבה של R, לאורך הרצועה שבין המנחתים לגדר (y 2500–2545) עד השער; המתדלק הקטן (FTs) והצוות — באותו שער (עד שההרחבה תיבנה — מהבסיס של היום, דרך XC_E). לאישורך.',
               'מסלול המים חוצה את נתיב הסירות של המספנה רק בהסעה. מי בודק: המטוס עצמו — כמו ב-074zm (busy() מול כלי השיט שבאמת שם: FISH3 — הסירות של השחקן ושל המספנה, סירת הנתב, המכמורות), בנקודת ההמתנה לפני החצייה ובקו לפני הגלגול; ההמראה / הנחיתה — רק כשהמסלול פנוי (אחרת המתנה / הקפה). סירה שמגיעה כשהאמפיבי בגלגול או בחצייה — עוצרת לפני המטוס (FISH3.HOOK.hit — אותה התנגשות כמו ב-074zm).'):
        h.append('<li>%s</li>' % E(li))
    h.append('</ul></section>')
    return ''.join(h)

OLD_MECH = [
 ('שרוול K‑72 עם רוטונדה (047:g77K72Parts / g77BridgePose, ‏AIR-09)', 'עגינה אמיתית בדלת, טלסקופ, סיבוב סביב הרוטונדה', 'קיים — 074k:s15grBrPose משתמש באותו מודל', 'נשאר'),
 ('QA‑79 (047 / 048, F9 "שרוולים"): כל עמדת שרוול × כל סוג × כל מצב', 'שלא נכנס לעמדה סוג שהשרוול לא מגיע אליו', 'חסר — s15c_bridges בודק רק את המטוס שבלוח', 'מוחזר: 074zr2_fc_bridges.js — 6 עמדות × 6 סוגים, עגינה ומנוחה; הבדיקה fc_bridge_types; הפרופיל של כל עמדה — למתכנן'),
 ('D‑106 (046): טורבו-פרופ בעמדת שרוול — הליכה מהטרמינל', 'סוג נמוך בעמדת שרוול', 'חסר', 'מסומן בפרופיל ("הליכה")'),
 ('F2_POCKETS / MU-A·B·C (049): נקודת כבודה לכל מודול; "החניה והאולם בלתי תלויים; רכבת שאולה משרתת את הטיסה שלה"', 'תור אחד לכל הכבודה, נסיעות ארוכות', 'אולם אחד (074p:S15I_HALL)', 'שודרג: 5 עמדות (074zr), שיוך לפי מודול (סעיף 9), נפילה לעמדה הקרובה'),
 ('AIR‑26 (049): הכבודה של העמדות המרוחקות — דרך השירות L, ה-GLINK, "דרך הלהקה"', 'רכבת לעמדה מרוחקת בלי לחצות מטוסים', 'חסר ל-R', 'בחישוב: XC_W ← AIR-PASS ובחזרה XC_E (סעיף 9); במשחק — עם הלוח החדש (fieldthru)'),
 ('AIR‑25 / AIR‑28 (043): רכב לא חונה על נתיב; בדיקה סטטית ודינמית', 'רכבים שעומדים בדרך', 'קיים — s15k_fleet (s15kStatic)', 'בבסיס הדרומי — אותו כלל (fc_calc2)'),
 ('K‑104 / K‑111 (045 / 043): גוף הרכב מול הגדר והמבנים, כל 0.2 ש׳', 'רכבים שחותכים פינות', 'חלקי — מול רכבים ומטוסים בלבד', 'עם הנתיבים של הלוח החדש (fieldthru)'),
 ('050 (הבעלים 16:17): כיס בין עמדות — חניה אדומה משלו', 'ציוד בתוך המעטפת של העמדה', 'קיים — S15D.pockets', 'נשאר; בדרום 28 חניות'),
 ('G2 / AIR‑64 / AIR‑65 (050): העמדות המרוחקות — אוטובוסים, מדרגות, "עקוב אחריי", מעלית', 'שירות מלא לעמדה מרוחקת', 'חלקי — R1 / R2 עם AB / MS', 'הכמויות בחישוב; הביצוע — fieldthru'),
 ('AIR‑36 Best-Fit + פרופילים של עמדות (044)', 'איזה סוג נכנס לאיזו עמדה', 'חלקי — S15D.stands.type', 'בחישוב (188 בדיקות) + הפרופיל של השרוולים'),
 ('K‑114 (045): מסוקים — גובה שיוט לכל מנחת, אחד בכל פעם', 'מסוקים שנפגשים', '—', 'fieldthru (בחישוב: 72.5 תנועות)'),
 ('האמפיבי: בישן נחת על המסלול וחנה ב-GA2 (043:g77BringNow)', '—', 'על המים — רק 074zm (G6 / H6)', 'מסלול מים בדרום השדה, מזח צף ורמפה — מעל 074zm'),
 ('ההרחבה: בישן "דרך הלהקה" y 590, רחבת ה-GA ב-NE (GA5 / GA6 בוטלו, D‑97)', '—', 'apronS מחובר לצפון רק ב-B', 'H4: בסיס צי דרומי (28 חניות), בלי עמדות מטוסים'),
]
def sec10():
    h = ['<section><h2>10. המנגנונים של השדה הישן — הגאומטריה (התיקון של 08:10)</h2><p class="cap">החלוקה: fieldcalc — העמדות, השרוולים, הכבודה, דרכי השירות, ההרחבה; fieldthru — המתכנן, הלו״ז ורכבי השירות (AO, ‏apttVehMove, ‏G77_BW / BX); fieldfix — התחזוקה וההאנגרים.</p>']
    h.append(table(['בישן (קובץ:פונקציה)', 'מה הוא פתר', 'בחדש (S15)', 'מה עושים'], [list(r) for r in OLD_MECH]))
    p = os.path.join(OUT, 'qa', 'bridges_try6649.json')
    if os.path.exists(p):
        B = json.load(open(p, encoding='utf-8')); TY = []
        for r in B['rows']:
            if r['ac'] not in TY: TY.append(r['ac'])
        st = []
        for r in B['rows']:
            if r['stand'] not in st: st.append(r['stand'])
        plan = {f['stand']: f['model'] for f in R['schedule']}
        rows = []
        for s_ in st:
            row = [s_ + (' (בלוח: %s)' % HE.get(plan[s_], plan[s_]) if s_ in plan else '')]
            for t in TY:
                r = next(q for q in B['rows'] if q['stand'] == s_ and q['ac'] == t)
                ok = r.get('ok'); d = r.get('dock') or {}; rs = r.get('rest') or {}
                cell = ('✓' if ok else '✗') + ' %s / %s / %s' % (d.get('door'), d.get('clr'), rs.get('clr'))
                if not r.get('inStand'): cell = '✗ לא נכנס בעמדה'
                row.append('<span class="%s">%s</span>' % ('ok' if ok else 'bad', E(cell)))
            rows.append(row)
        h.append('<h3>הפרופיל של עמדות השרוול (QA‑79 של הישן, על השרוולים של S15 — נמדד במשחק, try6649)</h3><p class="cap">בכל תא: התא מהדלת בעגינה / המנהרה מהגוף בעגינה / המנהרה מהגוף במנוחה (מ׳). עובר: עד 0.35 / לפחות 1.0 / לפחות 2.4, והמטוס בתוך העמדה.</p>')
        h.append(table(['עמדה'] + [HE.get(t, t) for t in TY], rows))
    if R2 and R2.get('stand_profile'):
        SP = R2['stand_profile']; TY = SP['types']; plan = {f['stand']: f['model'] for f in R['schedule']}
        rows = []
        for sid, r in SP['rows'].items():
            row = [sid]
            for t in TY:
                ok = r[t]; why = (SP['why'].get(sid) or {}).get(t) or []
                mark = '●' if plan.get(sid) == t else ''
                row.append('<span class="%s" title="%s">%s%s</span>' % ('ok' if ok else 'bad', E(', '.join(why)), '✓' if ok else '✗', mark))
            rows.append(row)
        h.append('<h3>פרופיל העמדות — כל עמדה × כל סוג (AIR‑35 / AIR‑36 של הישן) — למתכנן</h3><p class="cap">%s. ● — הסוג של הלוח. הסיבה של כל ✗ — בריחוף מעל התא (וב-fc_result2.json:stand_profile.why).</p>' % E(SP['note']))
        h.append(table(['עמדה'] + [HE.get(t, t) for t in TY], rows, 'mx'))
        h.append('<p>כל הצירופים של הלוח (P1 / P6 — LG, ‏P2 / P3 / P5 — צר-גוף, ‏P4 — אזורי) עוגנים. לא מתקבלים: LG ב-P2–P5 (לא נכנס בעמדה / התא מטר מהדלת — השרוול הקצר של P4 / P5 כבר באורך המינימלי), ‏MW ב-P4–P6 (במנוחה המנהרה 0.4–1.2 מ׳ מהגוף). הבדיקה fc_bridge_types (074zr2) נכשלת אם הלוח שם סוג כזה בעמדה כזו.</p>')
    h.append('</section>')
    return ''.join(h)

AM2 = dict(lane=[7300, 3480, 9450, 3580], cy=3530, lineup=9300, lift=8300, td=9200, stop=8500, H1=[8300, 2810], H2=[8300, 3415], moor=[8330, 2662],
           pier=[8180, 2600, 8470, 2640], ramp=[8433, 2548, 8463, 2602], gate=[8428, 2546, 8468, 2554],
           trawl_hull=[7531, 3035, 9454, 3365], ship_lane=[6900, 3620, 9600, 4020], buoys=[[7480, 3620], [8080, 3620], [7480, 4020], [8080, 4020]],
           circuit=[[8300, 3530], [7600, 3530], [7367, 3627], [7270, 3860], [7367, 4093], [7600, 4190], [9900, 4190], [10133, 4093], [10230, 3860], [10133, 3627], [9900, 3530], [9200, 3530]],
           taxi_out=[[8330, 2662], [8226, 2700], [8300, 2762], [8300, 2810], [8300, 3415], [8340, 3455], [9300, 3455], [9400, 3510], [9300, 3530]],
           taxi_in=[[8500, 3530], [8340, 3500], [8300, 3455], [8300, 3415], [8300, 2810], [8378, 2732], [8435, 2697], [8400, 2662], [8330, 2662]],
           bus=[[9015, 2470], [8860, 2520], [8480, 2525], [8448, 2540]])
def svg_amph():
    X0, Y0, X1, Y1 = 6900, 2250, 10500, 4300
    a = AM2; o = ['<svg viewBox="%d %d %d %d" class="map" role="img" aria-label="האמפיבי של השדה: מסלול המים, ההקפה, ההסעה, החצייה של נתיב הסירות, המזח הצף והשער">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    o.append(rect([X0, Y0, X1, Y1], 'sea')); o.append(rect([X0, Y0, X1, 2550], 'land'))
    o.append(rect([7205, 2250, 9544, 2545], 'apron'))
    for h in D['helipads']:
        c = h['c']; o.append('<circle cx="%d" cy="%d" r="%d" class="hp"/>' % (c[0], c[1], h['pad'] / 2 + 10)); o.append(txt(c[0], c[1] + 14, h['id'], 'hpl', 34))
    for sid in ('R1', 'R2', 'R3'):
        r = D['stands'][sid]['rect']; o.append(rect([r[0], max(r[1], 2250), r[2], r[3]], 'stand' + (' r3' if sid == 'R3' else ''))); o.append(txt((r[0] + r[2]) / 2, 2330, sid, 'st', 34))
    o.append('<line x1="7200" y1="2550" x2="9600" y2="2550" class="fence"/>'); o.append(txt(9300, 2580, 'הגדר (y 2550)', 'lbs', 26))
    bs = R['layout']['bshop']; o.append(rect(bs['act'], 'like')); o.append(txt((bs['act'][0] + bs['act'][2]) / 2, 2700, 'המספנה — LIKE-08 (לא זז)', 'lk', 30))
    o.append('<polyline points="%s" class="blane"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in bs['lane'])); o.append(txt(9000, 2990, 'נתיב הסירות של המספנה', 'wl', 28))
    o.append(rect(a['trawl_hull'], 'trawl')); o.append(txt(8450, 3215, 'שטח הדיג של המכמורת TRAWL-1 (S14, ‏05:20–17:00)', 'wl', 28))
    o.append(rect(a['ship_lane'], 'slane')); o.append(txt(7750, 3990, 'נתיב האוניות LANE-L1', 'wl', 28))
    for b in a['buoys']: o.append('<circle cx="%d" cy="%d" r="12" class="buoy"/>' % (b[0], b[1]))
    o.append(rect(a['lane'], 'wlane')); o.append(txt(7700, 3470, 'מסלול המים — ממריא ונוחת מערבה', 'wl', 34))
    o.append('<polyline points="%s" class="circ"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in a['circuit'])); o.append(txt(8900, 4170, 'ההקפה (שמאלית, מעל הים)', 'wl', 30))
    for k, x in (('גלגול', a['lineup']), ('ניתוק', a['lift']), ('נגיעה', a['td']), ('עצירה', a['stop'])):
        o.append('<circle cx="%d" cy="%d" r="14" class="pt"/>' % (x, a['cy'])); o.append(txt(x, a['cy'] - 24, k, 'lbs', 24))
    o.append('<polyline points="%s" class="wtaxi"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in a['taxi_out']))
    o.append('<polyline points="%s" class="wtaxi"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in a['taxi_in']))
    o.append('<rect x="8200" y="2780" width="200" height="635" class="xzone"/>'); o.append(txt(8150, 3000, 'אזור החצייה — busy()', 'lbs', 22, 'end'))
    for k in ('H1', 'H2'):
        p = a[k]; o.append('<circle cx="%d" cy="%d" r="16" class="hold"/>' % (p[0], p[1])); o.append(txt(p[0] + 26, p[1] + 8, k + ' — המתנה', 'lbs', 24, 'start'))
    o.append(rect(a['pier'], 'dock')); o.append(rect(a['ramp'], 'dock')); o.append(txt(a['pier'][0] - 8, a['pier'][1] + 30, 'מזח צף', 'lbs', 26, 'end'))
    o.append(rect(a['gate'], 'agate')); o.append(txt(8448, 2520, 'G-AMPH', 'xcl', 24))
    o.append('<polyline points="%s" class="busr"/>' % ' '.join('%d,%d' % (p[0], p[1]) for p in a['bus'])); o.append(txt(8700, 2510, 'אוטובוס R', 'lbs', 22))
    m = a['moor']; o.append('<ellipse cx="%d" cy="%d" rx="35" ry="9" class="am"/>' % (m[0], m[1])); o.append('<rect x="%d" y="%d" width="10" height="106" class="am"/>' % (m[0] - 5, m[1] - 53))
    o.append('<g class="nArrow"><line x1="7000" y1="4250" x2="7000" y2="4100"/><text x="7000" y="4070" text-anchor="middle">צפון</text></g>')
    o.append('</svg>'); return ''.join(o)
def sec11():
    h = ['<section><h2>11. האמפיבי של השדה — הציור (לפני הבנייה, כלל 13)</h2><p class="cap">בנוסף ל-074zm (G6 / H6, ‏y 4650 — לא זז). אותו צייר ואותה פיזיקה (074zm: מטוס אחד אמיתי, ההמתנות וההקפה לפי כלי השיט שבאמת שם); הבנייה — הרחבה של 074zm למופע שני (התצורה), לא מנגנון חדש.</p>']
    h.append('<div class="fig">%s</div>' % svg_amph())
    for li in ('מסלול המים y 3480–3580 (x 7300–9450): גלגול מ-9300 מערבה, ניתוק ב-8300; ההקפה שמאלית מעל הים — שתי פניות של חצי מעגל (רדיוס 33 מ׳, y עד 4190); הגישה ממזרח, נגיעה ב-9200, עצירה ב-8500 — כמו מסלול אמיתי, אותו כיוון בהמראה ובנחיתה.',
               'למה לא ב-y 3110 (התוכנית של 07:00): שם עובר שטח הדיג של המכמורת TRAWL-1 (S14D.trawl ‏[7700, 3080, 9200, 3320], שלוש שורות, 05:20–17:00). האודיט של try6652 מצא חפיפה עם המכמורת ועם נתיב הסירות — לכן המסלול זז דרומה, בין שטח הדיג לנתיב האוניות (LANE-L1).',
               'ההסעה: מהעצירה צפונה, המתנה ב-H2 (y 3415, מדרום לשטח הדיג), ואז חצייה אחת צפונה — דרך שטח הדיג ונתיב הסירות של המספנה (y 2905) — רק כששניהם פנויים (busy() של 074zm: הסירות של FISH3, סירת הנתב, המכמורות), H1 (y 2810 — 7 מ׳ מהסירות, כך שסירה לא נעצרת מול מטוס שמחכה לה), פניית פרסה ועגינה בפאה הדרומית של המזח הצף. בהמראה — אותה חצייה, מ-H1 דרומה.',
               'מה עושה סירה כשהאמפיבי חוצה: הסירות של השחקן והשכורות — נעצרות מול המטוס (FISH3.HOOK.hit, כמו מול מזח) עד שהוא עובר; המכמורת — לא נכנסת לחצייה, כי האמפיבי מחכה לה ב-H1 / H2. הזמנים של הסיורים — כמו aoSearch של המתכנן הישן: לכל סיור הדקה הקרובה לרצויה שבה אף מצב על המים לא נוגע במכמורת: 06:09, ‏08:26, ‏10:24, ‏12:31, ‏14:43 (5 סיורים; ה-6 — 16:00 — לא נכנס עד 18:00).',
               'הנוסעים: מהשער של R בטרמינל (56 מושבים) באוטובוס הרחבה של R — לאורך הרצועה שבין המנחתים לגדר — עד השער G-AMPH (x 8428–8468) והרמפה. המתדלק הקטן והצוות — באותו שער.',
               'הבדיקות (כמו ב-074zm): על המים, קצות הכנף, המצופים, באוויר — רק מעל הים, ההמשכיות, כלי השיט (המכמורות, סירת הנתב), האנשים — ועוד (fc_amph_water): ‏≥ 3 מ׳ מנתיב הסירות חוץ מהחצייה, בלי קפיצה בכיוון (עד 20° ב-0.25 שנ׳), והזמנים — אף סיור לא נוגע במכמורת (המתכנן רץ מחדש בבדיקה).',
               'לאישורך: השער בגדר (G-AMPH), המזח הצף והרמפה (מבנה חדש קטן במים, לפי הבקשה של הבעלים "נחיתת האמפיבי על המים בדרום"); מסלול המים ב-y 3530; 5 סיורים ביום.'):
        h.append('<p>%s</p>' % E(li))
    h.append('</section>'); return ''.join(h)

def svg_spots():
    X0, Y0, X1, Y1 = 4780, 150, 9660, 2600
    o = ['<svg viewBox="%d %d %d %d" class="map" role="img" aria-label="החניות של רכבי השירות החדשים בכיסים של היום">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    o.append(rect([X0, Y0, X1, Y1], 'land'))
    for k in ('apron', 'apronS'): o.append(rect(D[k], 'apron'))
    for k in ('twb', 'twc'): o.append(rect(D[k], 'twy'))
    o.append(rect(D['term'], 'bld'))
    for sid, s in D['stands'].items():
        if s.get('rect'): o.append(rect(s['rect'], 'stand')); r = s['rect']; o.append(txt((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 12, sid, 'st', 34))
    for aid, r in SP['areas'].items():
        if aid.startswith('AIR-GSE') or aid in ('AIR-BASE-4', 'AIR-BASE-8'): o.append(rect(r, 'pocket'))
    for vid, s in SP['spots'].items():
        if s.get('rect'): o.append(rect(s['rect'], 'spot0'))
    for q in SP['placed']:
        r = q['rect']; o.append(rect(r, 'spotN')); o.append(txt((r[0] + r[2]) / 2, r[1] - 6, q['id'], 'spl', 16))
    o.append('<g class="nArrow"><line x1="4900" y1="2550" x2="4900" y2="2400"/><text x="4900" y="2370" text-anchor="middle">צפון</text></g>')
    o.append('</svg>'); return ''.join(o)
def sec12():
    h = ['<section><h2>12. מקום לגררים ולרכבי שירות — החניות של הרכבים החדשים (בכיסים של היום)</h2>']
    h.append('<p class="cap">החישוב (סעיף 5, fc_result.json:fleet) אומר כמה חסר מכל סוג: %d רכבים חדשים (הגררים — עודף של 3). הבסיס הדרומי בהרחבה (H4) הוא במים — מילוי ים הוא שינוי של קו החוף (seatrees / mapfix), לכן היום: חניות בכיסים הקיימים, ליד העמדות שכל רכב משרת. '
             'כל חניה נבדקה במשחק (try6653, ‏tools/q_spots.js): בתוך הכיס, לא על דרך שירות / סימון חצייה / עמדה / מנחת / חניה קיימת (+0.6 מ׳), 3 מ׳ פנויים מלפנים, ו-≥ 0.3 מ׳ מכל רכב ומטוס של S15 בכל רגע של המחזור (כל 0.5 ש׳, אותן קופסאות של s15k). '
             'הרכבים עצמם, הנסיעות והלו״ז — fieldthru (החלוקה של 08:10); כאן — רק המקום.</p>' % (len(SP['placed']) + len(SP['failed'])))
    h.append('<div class="fig">%s</div>' % svg_spots())
    rows = [[q['id'], R['veh_he'].get(q['t'], q['t']), ', '.join(q['serves']), q['home'], '[%s]' % ', '.join(str(v) for v in q['rect']), 'דרומה' if q['h'] == 'S' else 'מזרחה', '%.1f מ׳' % q['gap']] for q in SP['placed']]
    h.append(table(['הרכב החדש', 'הסוג', 'משרת', 'הכיס', 'המלבן', 'האף', 'המרווח הקטן במחזור'], rows))
    if SP['failed']:
        h.append('<p><b>לא נמצא מקום:</b> %s</p>' % E(' · '.join('%s (%s): %s' % (q['id'], q['t'], '; '.join(q['why'])) for q in SP['failed'])))
    h.append('<p>%s</p>' % E('לאישורך: החניות של הרכבים החדשים בכיסים (במקום הבסיס הדרומי, עד שיוחלט על מילוי הים ב-H4). ל-fieldthru: tools/fc_spots.json — לכל רכב: home (הכיס), ‏rect, ‏h — כמו S15D.spots.'))
    h.append('</section>'); return ''.join(h)

def svg_bags():
    # שלושת הסוגים של 074zt_fc_bags.js (אותה גאומטריה: המשטח העליון, החזית הכהה, הפרטים) — פי 12, ולידם הקופסה של קודם
    S = 12; X = 10; K = .6; w, d, h = .62, .42, .34; sx, sy, zh = w * X * S, d * X * S, K * h * X * S
    o = ['<svg viewBox="0 0 980 300" class="map" role="img" aria-label="המזוודות: הקופסה של קודם ושלושת הסוגים החדשים">', '<rect x="0" y="0" width="980" height="300" class="apron"/>']
    def rr(x, y, ww, hh, r, cls, extra=''):
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" class="%s" %s/>' % (x, y, ww, hh, r, cls, extra)
    items = [('box', '#2f7fbf', 'קודם — קופסה'), ('hard', '#c2333a', 'קשיחה עם גלגלים'), ('soft', '#2f7fbf', 'רכה — כיס ורוכסן'), ('duffel', '#2e9e3e', 'תיק — רצועה וידיות')]
    for i, (k, col, lab) in enumerate(items):
        cx = 125 + i * 245; x0 = cx - sx / 2; yT = 150 - sy / 2 - zh; yF = 150 + sy / 2 - zh; m = min(sx, sy + zh)
        top = 'fill="%s" style="filter:brightness(1.18)"' % col; front = 'fill="%s" style="filter:brightness(.82)"' % col
        if k == 'box':
            o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0, yT, sx, sy, col)); o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" style="filter:brightness(.7)"/>' % (x0, yF, sx, zh, col))
        elif k == 'hard':
            o.append(rr(x0, yT, sx, sy, m * .16, 'bagf', top)); o.append(rr(x0, yF - m * .08, sx, zh + m * .08, m * .16, 'bagf', front))
            for f in (.3, .5, .7): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="bagrib"/>' % (x0 + sx * f, yF + zh * .12, x0 + sx * f, yF + zh * .82))
            o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bagd"/>' % (x0 + sx * .18, yT + sy * .44, sx * .64, sy * .12))
            for f in (.18, .75): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bagd"/>' % (x0 + sx * f, yT + sy * .3, sx * .07, sy * .4))
            wr = m * .09
            for f in (.14, .86): o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" class="bagw"/>' % (x0 + sx * f, yF + zh - wr, wr))
        elif k == 'soft':
            o.append(rr(x0, yT, sx, sy, m * .22, 'bagf', top)); o.append(rr(x0, yF - m * .06, sx, zh + m * .06, m * .2, 'bagf', front))
            o.append(rr(x0 + sx * .16, yF + zh * .34, sx * .68, zh * .5, m * .12, 'bagf', 'fill="%s" style="filter:brightness(.7)"' % col))
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="bagz"/>' % (x0 + sx * .08, yF + zh * .16, x0 + sx * .92, yF + zh * .16))
            o.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" class="bagh"/>' % (x0 + sx * .36, yT + sy * .55, cx, yT + sy * .1, x0 + sx * .64, yT + sy * .55))
        else:
            o.append(rr(x0, yT + sy * .05, sx, sy * .95, m * .42, 'bagf', top)); o.append(rr(x0, yF - m * .1, sx, zh + m * .1, m * .45, 'bagf', front))
            o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bags"/>' % (cx - sx * .06, yT + sy * .05, sx * .12, sy * .95 + zh))
            for f in (.3, .7): o.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" class="bagh"/>' % (x0 + sx * f - sx * .09, yT + sy * .6, x0 + sx * f, yT + sy * .15, x0 + sx * f + sx * .09, yT + sy * .6))
        if k in ('hard', 'duffel'): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bagt"/>' % (x0 + sx * .62, yT + sy * .62, sx * .14, sy * .22))
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bagbb"/>' % (x0 - 6, yT - 6, sx + 12, sy + zh + 12))
        o.append('<text x="%d" y="%d" text-anchor="middle" class="baglab">%s</text>' % (cx, 265, E(lab)))
    o.append('</svg>'); return ''.join(o)
def sec13():
    h = ['<section><h2>13. מזוודות מעוצבות במקום קוביות (הביקורת 14, ‏AIR-08) — הציור לפני הבנייה</h2>']
    h.append('<p class="cap">כל מזוודה בשדה מצוירת בפונקציה אחת — 074k:s15grBag (העגלות של רכבות הכבודה, המסוע, הידיים של המעמיסים ועמדות הכבודה). 074zt_fc_bags.js מחליף רק את הצורה — באותו מקום, באותן מידות (0.62 × 0.42 × 0.34 מ׳) ובאותו צבע; הסוג לפי הצבע (8 הצבעים → שלושה סוגים, כך שבכל עגלה המזוודות שונות זו מזו), ותווית לחצי מהן. בזום רחוק — הקופסה של קודם. הבדיקה fc_bags: כל סוג, בכל צבע, מצויר רק בתוך הקופסה של קודם (המסגרת המקווקוות למטה) — כך שאין נגיעה בשכנה בעגלה.</p>')
    h.append('<div class="fig">%s</div>' % svg_bags()); h.append('</section>'); return ''.join(h)
AIRROWS = [
 ('C08.01 · AIR-02 — ספירת עמדות שימושיות', 'נעשה (בחישוב)', 'בישן 19: 16 בחוץ (15 בשימוש) + 3 בהאנגרים. בחדש 19 סימונים → 18 עמדות עצמאיות: CH חופפת ל-C1 ול-C2 — עמדה מותנית (רק כששתיהן ריקות); GA5–GA7 — מותנות (רק קלים: האף ב-y 2028, D‑650); תחזוקה — 3 האנגרים + R3 בלילה (הרצת מנועים); חניה קבועה — 0 (R3 שוחררה). בלוח של התוכנית — 18 עמדות בשימוש (כולן חוץ מ-CH), מול 6 היום. המשפחות לכל עמדה — סעיף 10 (stand_profile) והשרוולים — fc_bridge_types.'),
 ('C08.03 · C09.04 · C14.05 · AIR-04 — עמדה אחת או 4–5', 'נעשה + במשחק', 'החישוב בעומס היעד (פי 2 מהישן, 20 ביקורים, 256 יחידות במחזור): עמדה אחת — 150% (המתנה ממוצעת 843 ש׳, 36 איחורים) — לא מספיקה; 2 — 75% (16); 3 — 50% (7); 4 — 37.6% (2); 5 — 30% (0). היום (30 תנועות) אחת בתפוסה 31.7% — מספיקה רק לעומס של היום. נבנו 5 (074zr, ‏BH-1…BH-5), השיוך לפי מודול — כל עמדה ≤ 31.6%, בלי המתנה.'),
 ('C10.04 · AIR-08 — הזזת השדה חצי אזור דרומה', 'נבדק — לא מומלץ (לאישורך)', 'המגבלה שנמדדה היא B (הקישור היחיד לדרום, 78%) ולא השטח: המסלול 68%, העמדות 18. הזזת כל השדה ב-425 פיקס׳ — המסלול, A / B / C, הטרמינל, החניונים והכביש לשדה זזים, ו-apronS נכנס לים (קו החוף — seatrees / mapfix). במקום זה: ההרחבה H4 (בסיס צי, 28 חניות — עד שיוחלט על מילוי הים, החניות בכיסים — סעיף 12), מפרץ המתנה באמצע B (19 טיסות / 95), והאמפיבי על המים (סעיף 11).'),
 ('C14.06 · AIR-08 — גאומטריה מול מה שנבדק בישן', 'נעשה בחלקו', 'הוחזרו: QA‑79 (כל עמדת שרוול × כל סוג — fc_bridge_types), הכיסים בין העמדות (050), נקודות הכבודה למודולים (049 → 5 עמדות), D‑106 (טורבו-פרופ בהליכה), AIR‑25 / 28 (רכב לא חונה על נתיב — s15k). פתוח: K‑104 / K‑111 — גוף הרכב מול הגדר והמבנים (היום רק מול רכבים ומטוסים) — עם הנתיבים של הלוח החדש (fieldthru).'),
 ('C14.08 · AIR-08 — מזוודות מעוצבות', 'נעשה (try6655)', '074zt_fc_bags.js — שלושה סוגים בציור 3/4, באותו מקום ובאותן מידות; הבדיקה fc_bags (סעיף 13).'),
 ('C16.06 · AIR-DRAW-01 — תעלת המים מעל המטוסים', 'פתוח — לא בתחום הגאומטריה', 'הסיבה נמצאה: 074j:drawAptProps — s15Details (שם גם water:ditch, ‏S15D.live של E0–H0) מצויר אחרי s15Live(now, "ground") — אחרי המטוסים; וכך גם ב-s15Render של הדף החי. התיקון: את water:ditch לצייר לפני s15Live (או בשכבת הקרקע). לבעלים של ציור השדה (fieldfix) — לפי הכרעת המתאם.'),
 ('C16.07 · AIR-09 — המסלול משני הכיוונים', 'נעשה (בחישוב)', '09 או 27 — אותו זמן ב-B לכל תנועה לדרום (B הוא הקישור היחיד); ב-27 עוד ~36 ש׳ הסעה על A. הדו-כיווני לא מוסיף קיבולת (סעיף 9ז). המדידה במחולל — fieldthru.'),
 ('C01.04 · C05.01 · C05.05 · C07.02 · C10.03 · AIR-01 — יותר טיסות', 'החישוב נעשה; המחולל — fieldthru', 'הישן 44–45 (נמדד), היום 30; התוכנית 90 ב-1800 ש׳ (×2.0), עתודה 95. מה שבגאומטריה כבר במשחק: 5 עמדות הכבודה, השרוולים × סוג, קומת השערים (270 + 89 + 56 מושבים), האמפיבי על המים. הלוח והמחולל — fieldthru.'),
 ('C05.02 · AIR-05 — סנכרון רכבי השירות', 'המקום — נעשה; הרכבים — fieldthru', 'כמה צריך (סעיף 5), דרכי השירות והחצייה של C (9ב), והחניות של הרכבים החדשים בכיסים (סעיף 12, ‏fc_spots.json).'),
 ('C05.03 · C05.04 · AIR-03 — מנהלים ושני הענקים', 'הגאומטריה — נעשתה', 'LG — רק P1 / P6 (השרוולים, סעיף 10); מנהלים — GA1 ו-R3 ביום. התמהיל והטיסות — fieldfix / fieldthru.'),
 ('C09.01–03 · AIR-06 — תחזוקה מתחלפת', 'המפרט — נעשה; הביצוע — fieldfix', 'סעיף 9ה: האנגר אחד ביום, הגרירות והחלונות; R3 בלי מטוס קבוע.'),
 ('C05.06 · AIR-07 — נוסעים מגוונים', 'לא בתחום', 'fieldfix (s15pax) / perf; המושבים בקומת השערים — נעשו (סעיף 9).'),
]
def sec14():
    h = ['<section><h2>14. הדף עם 66 ההערות (AIR_tasks_from_plan.md) — מה בתחום הגאומטריה נעשה ומה פתוח</h2>']
    h.append(table(['השורה', 'המצב', 'מה נעשה / מה פתוח'], [[E(a), E(b), E(c)] for a, b, c in AIRROWS]))
    h.append('</section>'); return ''.join(h)

if __name__ == '__main__':
    doc = page(); p = os.path.join(OUT, 'Fieldcalc_plan.html'); open(p, 'w', encoding='utf-8').write(doc)
    b = doc.encode('utf-8'); print(p, len(b), 'בתים · sha1', hashlib.sha1(b).hexdigest()[:12], '· data:image', doc.count('data:image'), '· <img', doc.count('<img'))
