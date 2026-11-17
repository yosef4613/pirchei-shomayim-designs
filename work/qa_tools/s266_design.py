#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s266_design.py <out.html> [stamp] — ציור התוכנית של S7F266 (כלל 20): הרציפים של E3, הגגונים, מסילת העקיפה, והצינור PIPE-REF ב-C5.
דף נפרד ונקי, הכול מצויר בקוד (SVG), בלי צילומים. הקואורדינטות — של העולם במשחק (10 פיקס׳ למטר בהגדלה של העיר), צפון למעלה, מזרח מימין.
המקורות: study/roads/city_plan.json (המסילות BYPASS ו-REF-SPUR, התחנה ST-E3), והמידות של המשחק S7F265 (נמדדו בתוך המשחק)."""
import sys, json, hashlib, os, html, datetime
W = '/home/user/tc_root/tc/pkg/work'
out = sys.argv[1]; stamp = sys.argv[2] if len(sys.argv) > 2 else datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
PLAN = os.path.join(W, 'clean_r2b_025637/out/qa_s266/city_plan_snapshot.json')
P = json.load(open(PLAN, encoding='utf-8')); psha = hashlib.sha1(open(PLAN, 'rb').read()).hexdigest()[:12]
R = {r['id']: r for r in P['rails']}
BYP_MAP = R['BYPASS']['pts']; SPUR_MAP = R['REF-SPUR']['pts']
# the bypass as built (S7F266): x 5978 along E3, the deck and the south approach; the curve to MAIN-B is the map's curve, 0.78 of its offset
def byp_game():
    pts = [[5978, 2780], [5978, 1900]]
    for x, y in BYP_MAP:
        if 1720 <= y < 1900 and x <= 6000: pts.append([round(5900 + (x - 5900) * 0.78, 1), y])
    return pts
BYP = byp_game()
PIPE_X = 2728
PIPE_COLS = [3686, 3760, 3842, 3890, 3946, 4026]
RISER = 4118
VALVE = [2708, 4034, 2738, 4070]

def poly(pts): return ' '.join('%g,%g' % (p[0], p[1]) for p in pts)
def rect(x0, y0, x1, y1, cls, extra=''): return '<rect x="%g" y="%g" width="%g" height="%g" class="%s" %s/>' % (x0, y0, x1 - x0, y1 - y0, cls, extra)
FLIP = {'start': 'end', 'end': 'start', 'middle': 'middle'}   # the page is rtl: 'end' here = the text ends at x and extends to the left
def text(x, y, t, cls='lb', anchor='middle', extra=''): return '<text x="%g" y="%g" class="%s" text-anchor="%s" %s>%s</text>' % (x, y, cls, FLIP[anchor], extra, html.escape(t))
def compass(x, y, s):
    return ('<g class="cmp" transform="translate(%g %g) scale(%g)"><circle r="26" class="cmpbg"/><path d="M0,-22 L7,4 L0,0 L-7,4 Z" class="cmpn"/>'
            '<text y="-27" class="cmpt" text-anchor="middle">צפון</text><text x="34" y="5" class="cmpt" text-anchor="end">מזרח</text>'
            '<text x="-34" y="5" class="cmpt" text-anchor="start">מערב</text></g>') % (x, y, s)

# ------------------------------------------------------------------ E3
def e3_svg():
    X0, Y0, X1, Y1 = 5540, 1640, 6260, 2810
    g = ['<svg viewBox="%d %d %d %d" class="map" role="img" aria-label="E3 — הרציפים ומסילת העקיפה">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    g.append(rect(X0, Y0, X1, Y1, 'grass'))
    # roads: the field road (north), CL-F/1 (east), the island road under UX-1 (south)
    g.append(rect(X0, 1552, X1, 1648, 'road')); g.append(text(5620, 1604, 'כביש השדה', 'rd'))
    g.append(rect(6002, 1760, 6238, 2640, 'walk')); g.append(rect(6022, 1760, 6218, 2640, 'road')); g.append(text(6120, 2200, 'CL-F/1 · דרך המרינה', 'rd', extra='transform="rotate(-90 6120 2200)"'))
    g.append(rect(6002, 1782, 6238, 1790, 'barrier')); g.append(rect(5540, 2538, 6238, 2702, 'road')); g.append(text(5640, 2626, 'דרך האי · CL-I/4', 'rd'))
    # station building, concourse, parcels, yard, E3-PB
    g.append(rect(5550, 1708, 5728, 1768, 'bld')); g.append(text(5639, 1742, 'בניין התחנה', 'lbs'))
    g.append(rect(5700, 2016, 5736, 2078, 'pave')); g.append(text(5696, 2052, 'מעבר לרציף 1', 'lbs', 'end'))
    g.append(rect(5470, 2190, 5634, 2478, 'lot')); g.append(text(5596, 2210, 'E3-PB', 'lbs'))
    g.append(rect(5634, 2290, 5736, 2536, 'yard')); g.append(rect(5664, 2238, 5712, 2401, 'bld')); g.append(text(5688, 2330, 'חבילות', 'lbs', extra='transform="rotate(-90 5688 2330)"'))
    for x in (5638, 5680): g.append(rect(x, 2428, x + 42, 2536, 'dock'))
    g.append(rect(5722, 2428, 5764, 2536, 'gone')); g.append(text(5630, 2420, 'רציף פריקה 3 יוצא', 'lbs', 'end'))
    # the rail corridor
    g.append(rect(5736, 1700, 6000, 2530, 'corr'))
    for x in (5800, 5900):
        g.append(rect(x - 24, 1640, x + 24, 2810, 'bal')); g.append('<line x1="%d" y1="1640" x2="%d" y2="2810" class="rail"/>' % (x, x))
    g.append('<polyline points="%s" class="balb"/>' % poly(BYP)); g.append('<polyline points="%s" class="railb"/>' % poly(BYP))
    g.append('<polyline points="%s" class="mapline"/>' % poly([p for p in BYP_MAP if p[1] <= 2810]))
    # UX-1 deck
    g.append(rect(5752, 2530, 6046, 2710, 'deck')); g.append(text(5900, 2724, 'UX-1 · גשר הרכבת · 3 מסילות', 'lbs'))
    # platforms: old extents and new
    for x, w in ((5736, 38), (5826, 48)):
        g.append(rect(x, 1760, x + w, 2530, 'plat')); g.append(rect(x, 1850, x + w, 2290, 'platold'))
    # the glass hall (LIKE-02) and the platform canopies of the extensions
    g.append(rect(5722, 1840, 5938, 2298, 'hall')); g.append(text(5830, 2075, 'LIKE-02 · הגג השקוף נשאר', 'lbh'))
    for x0, x1 in ((5738, 5772), (5830, 5870)):
        g.append(rect(x0, 1772, x1, 1838, 'cano')); g.append(rect(x0, 2300, x1, 2518, 'cano'))
    # stairs (in place), the end railings, the fences
    for x, w in ((5738, 34), (5832, 36)): g.append(rect(x, 2252, x + w, 2284, 'stairs'))
    for x0, x1 in ((5736, 5774), (5826, 5874)):
        g.append('<line x1="%d" y1="1761" x2="%d" y2="1761" class="endr"/>' % (x0, x1)); g.append('<line x1="%d" y1="2529" x2="%d" y2="2529" class="endr"/>' % (x0, x1))
    for x, y0, y1 in ((5773, 1700, 1756), (6000, 1700, 2530), (5736, 2300, 2530), (5736, 1768, 1850)): g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="fence"/>' % (x, y0, x, y1))
    for x, y0, y1 in ((5928, 1715, 2544), (5773, 2294, 2544)): g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="fenceold"/>' % (x, y0, x, y1))
    # furniture marks in the extensions: benches, ticket machines, lamps
    for x, y in ((5755, 1800), (5850, 1800), (5755, 2340), (5850, 2340), (5755, 2430), (5850, 2430), (5755, 2500), (5850, 2500)): g.append('<circle cx="%d" cy="%d" r="5" class="lamp"/>' % (x, y))
    for x, y in ((5742, 1776), (5842, 1776), (5742, 2490), (5848, 2490)): g.append(rect(x, y, x + 10, y + 16, 'tvm'))
    # the relay cabin of the turnout and the service path between MAIN-B and the bypass
    g.append(rect(5950, 1728, 5990, 1760, 'bld')); g.append(text(5996, 1752, 'בית ממסרים', 'lbs', 'start'))
    g.append(rect(5926, 1960, 5954, 2520, 'path'))
    g.append('<circle cx="5900" cy="1720" r="7" class="sw"/>'); g.append(text(5884, 1716, 'מסוט · חיבור ל-MAIN-B', 'lbs', 'end'))
    g.append(rect(5966, 2768, 5990, 2778, 'buf')); g.append(text(6004, 2778, 'בולמים (סוף זמני, E4)', 'lbs', 'start'))
    # zone lines
    for y, t in ((1700, 'גבול E2 / E3 · y 1700'), (2550, 'גבול E3 / E4 · y 2550')): g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="zone"/>' % (X0, y, X1, y)); g.append(text(X1 - 6, y - 6, t, 'zl', 'end'))
    g.append('<line x1="6000" y1="1640" x2="6000" y2="2810" class="zone2"/>'); g.append(text(6006, 1660, 'E / F · x 6000', 'zl', 'start'))
    # labels
    g.append(text(5755, 2390, 'רציף 1', 'lbp', extra='transform="rotate(-90 5755 2390)"')); g.append(text(5850, 2390, 'רציף 2', 'lbp', extra='transform="rotate(-90 5850 2390)"'))
    for x, t in ((5800, 'MAIN-A'), (5900, 'MAIN-B')): g.append(text(x, 2800, t, 'lbs'))
    g.append(text(5978, 2160, 'מסילת העקיפה · x 5978', 'lbb', extra='transform="rotate(-90 5978 2160)"'))
    g.append(text(6050, 1880, 'קו המפה · x 6000', 'lbm', 'start'))
    # dimension: 770 px
    g.append('<line x1="5700" y1="1760" x2="5700" y2="2530" class="dim"/>'); g.append(text(5694, 2140, '770 פיקס׳ · 4 קרונות ומרווח', 'lbd', extra='transform="rotate(-90 5694 2140)"'))
    g.append(compass(6150, 2440, 1.3))
    g.append('</svg>'); return '\n'.join(g)

# ------------------------------------------------------------------ C5
def c5_svg():
    X0, Y0, X1, Y1 = 2380, 3440, 3170, 4400
    g = ['<svg viewBox="%d %d %d %d" class="map" role="img" aria-label="C5 — הצינור PIPE-REF">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    g.append(rect(X0, Y0, X1, Y1, 'grass'))
    g.append(rect(2392, 3400, 2628, 4400, 'walk')); g.append(rect(2412, 3400, 2608, 4400, 'road')); g.append(text(2510, 3700, 'שדרת המרכז', 'rd', extra='transform="rotate(-90 2510 3700)"'))
    g.append(rect(2380, 4132, 3170, 4368, 'walk')); g.append(rect(2380, 4152, 3170, 4348, 'road')); g.append(text(2830, 4300, 'שדרת הנמל · AR-S1W', 'rd'))
    g.append(rect(3042, 3400, 3178, 4152, 'walk')); g.append(rect(3062, 3400, 3158, 4152, 'road')); g.append(text(3110, 3640, 'רחוב בית הזיקוק', 'rd', extra='transform="rotate(-90 3110 3640)"'))
    g.append(rect(2952, 4348, 3048, 4400, 'road'))
    g.append(rect(2636, 3490, 3036, 4124, 'refy'))
    g.append(rect(2662, 3522, 2950, 3678, 'bund')); g.append(text(2806, 3668, 'חוות המכלים · מאצרה', 'lbs'))
    for cx, cy, r, t in ((2712, 3600, 40, 'T-101'), (2806, 3600, 40, 'T-102'), (2900, 3602, 36, 'T-103')): g.append('<circle cx="%d" cy="%d" r="%d" class="tank"/>' % (cx, cy, r)); g.append(text(cx, cy + 4, t, 'lbs'))
    for cx in (2972, 3012): g.append('<circle cx="%d" cy="3546" r="17" class="tank"/>' % cx)
    for a, b in (((2664, 3700), (3020, 3700)), ((2984, 3706), (2984, 3934)), ((2912, 3934), (2984, 3934)), ((2700, 3706), (2700, 3730))): g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="rack"/>' % (a[0], a[1], b[0], b[1]))
    g.append(rect(2664, 3722, 2882, 3892, 'pad'))
    for cx, cy, r in ((2700, 3792, 18), (2752, 3806, 14), (2794, 3818, 11)): g.append('<circle cx="%d" cy="%d" r="%d" class="eq"/>' % (cx, cy, r))
    g.append(rect(2812, 3738, 2870, 3790, 'eq')); g.append(rect(2896, 3742, 2966, 3792, 'bld')); g.append(rect(2694, 3852, 2754, 3868, 'eq'))
    g.append(rect(2664, 3910, 2724, 3972, 'eq')); g.append('<circle cx="2696" cy="4012" r="18" class="fire"/>'); g.append(rect(2668, 4052, 2704, 4080, 'bld'))
    for r in ((2880, 3790, 3036, 3860), (2990, 3805, 3030, 4112), (2664, 4072, 3030, 4112), (2730, 3896, 2990, 3932)): g.append(rect(*r, 'iroad'))
    g.append(rect(2740, 3936, 2908, 4064, 'cano')); g.append(text(2824, 4004, 'עמדת המילוי המקורה', 'lbs'))
    # the cancelled spur (map) and the pipe
    g.append('<polyline points="%s" class="spur"/>' % poly([[2780, 3950], [2780, 4440]])); g.append(text(2790, 4380, 'REF-SPUR · בוטלה (D‑504)', 'lbm', 'start'))
    g.append('<line x1="%d" y1="3620" x2="%d" y2="%d" class="pipelow"/>' % (PIPE_X, PIPE_X, PIPE_COLS[0]))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="pipe"/>' % (PIPE_X, PIPE_COLS[0], PIPE_X, PIPE_COLS[-1]))
    g.append('<line x1="%d" y1="4030" x2="%d" y2="4070" class="pipelow"/>' % (PIPE_X, PIPE_X)); g.append('<line x1="%d" y1="4070" x2="%d" y2="%d" class="sleeve"/>' % (PIPE_X, PIPE_X, RISER))
    for y in PIPE_COLS + [RISER]: g.append(rect(PIPE_X - 12, y - 3, PIPE_X + 12, y + 3, 'bent')); g.append(rect(PIPE_X - 3, y - 3, PIPE_X + 3, y + 3, 'col'))
    g.append(rect(*VALVE, 'valve')); g.append(text(2700, 4054, 'תחנת מגופים', 'lbb', 'end'))
    g.append('<circle cx="%d" cy="%d" r="5" class="cap"/>' % (PIPE_X, RISER)); g.append(text(PIPE_X - 10, 4142, 'עמוד דרומי עם אוגן — ההמשך מעל השדרה עם S10', 'lbs', 'end'))
    g.append(text(PIPE_X - 10, 3712, 'PIPE-REF · x 2728', 'lbb', 'end')); g.append(text(PIPE_X + 14, 4096, 'שרוול מתחת לדרך', 'lbs', 'start'))
    g.append('<line x1="%d" y1="4250" x2="%d" y2="4250" class="zone"/>' % (X0, X1)); g.append(text(X1 - 6, 4244, 'גבול C5 / C6 · y 4250 (באמצע השדרה)', 'zl', 'end'))
    g.append(compass(2470, 3510, 1.3))
    g.append('</svg>'); return '\n'.join(g)

# ------------------------------------------------------------------ the pipe bridge, side view (north on the right)
def elev_svg():
    # x axis = world y (north → south from right to left? keep north on the right like a look from the east): we draw from the east, north on the right
    S = 1.25; H = 10 * 1.125  # px per metre (world), height scale
    ys = PIPE_COLS; yN, yS = 3600, 4140
    def X(y): return 40 + (yS - y) * S
    def Z(m): return 300 - m * H * 1.6
    g = ['<svg viewBox="0 0 %d 352" class="elev" role="img" aria-label="מבט מהצד על גשר הצינורות">' % int(X(yN) + 60)]
    g.append('<line x1="20" y1="300" x2="%d" y2="300" class="ground"/>' % int(X(yN) + 40))
    for a, b, t, over in ((3896, 3932, 'דרך שירות', True), (4072, 4112, 'שרוול מתחת לדרך', False)):
        g.append('<rect x="%g" y="298" width="%g" height="6" class="iroadE"/>' % (X(b), (b - a) * S)); g.append('<text x="%g" y="322" class="lbs" text-anchor="middle">%s</text>' % (X((a + b) / 2), t))
        if over:
            g.append('<line x1="%g" y1="300" x2="%g" y2="%g" class="dim"/>' % (X((a + b) / 2), X((a + b) / 2), Z(8.2)))
            g.append('<text x="%g" y="%g" class="lbd" text-anchor="end">8.2 מ׳ חופשי</text>' % (X((a + b) / 2) + 4, Z(4)))
    g.append('<rect x="%g" y="%g" width="%g" height="%g" class="tankE"/>' % (X(3620) - 6, Z(14), 60, 300 - Z(14))); g.append('<text x="%g" y="%g" class="lbs" text-anchor="middle">T-101</text>' % (X(3620) + 24, Z(14) - 6))
    g.append('<rect x="%g" y="%g" width="%g" height="%g" class="valveE"/>' % (X(VALVE[3]), Z(2.2), (VALVE[3] - VALVE[1]) * S, 300 - Z(2.2)))
    g.append('<text x="%g" y="%g" class="lbs" text-anchor="middle">תחנת מגופים</text>' % (X((VALVE[1] + VALVE[3]) / 2), Z(2.2) - 26))
    top = Z(8.6)
    path = 'M%g,%g L%g,%g L%g,%g L%g,%g L%g,%g L%g,%g' % (X(3622), Z(.9), X(ys[0]), Z(.9), X(ys[0]), top, X(4030), top, X(4030), Z(.9), X(4070), Z(.9))
    g.append('<path d="%s" class="pipeE"/>' % path)
    g.append('<path d="M%g,%g L%g,%g L%g,%g L%g,%g L%g,%g" class="pipeS"/>' % (X(4070), Z(.9), X(4070), Z(-1.2), X(RISER), Z(-1.2), X(RISER), Z(.9), X(RISER), top))
    for y in ys + [RISER]:
        g.append('<line x1="%g" y1="300" x2="%g" y2="%g" class="colE"/>' % (X(y), X(y), top + 4)); g.append('<line x1="%g" y1="%g" x2="%g" y2="%g" class="beamE"/>' % (X(y) - 7, top + 4, X(y) + 7, top + 4))
    for y in (ys[0], ys[-1], RISER):
        g.append('<line x1="%g" y1="300" x2="%g" y2="%g" class="ladder"/>' % (X(y) + 5, X(y) + 5, top + 2))
    g.append('<line x1="%g" y1="%g" x2="%g" y2="%g" class="rail2"/>' % (X(ys[-1]), top - 9, X(ys[0]), top - 9))
    g.append('<text x="%g" y="%g" class="lbd" text-anchor="middle">שביל תחזוקה עם מעקה · ‏2 צינורות על קורות רוחב · עמוד כל 5–9 מ׳</text>' % ((X(ys[-1]) + X(ys[0])) / 2, top - 16))
    g.append('<circle cx="%g" cy="%g" r="4" class="cap"/>' % (X(RISER), top))
    g.append('<text x="%g" y="346" class="lbs" text-anchor="end">← דרום</text><text x="%g" y="346" class="lbs" text-anchor="start">צפון →</text>' % (20, X(yN) + 40))
    g.append('</svg>'); return '\n'.join(g)

DIFF = [
    ('מסילת העקיפה ב-E3, על הגשר ובגישה הדרומית', 'x 6000', 'x 5978 — 2.2 מ׳ מערבה, אותה צורה; הקשת אל MAIN-B היא הקשת של המפה, ב-0.78 מההיסט שלה',
     'הקו של המפה עובר על השפה המערבית של המדרכה של CL-F/1 (x 6002). תוואי המסילה במשחק 4.4 מ׳ — ב-x 6000 הוא היה עולה על המדרכה. לאישורך.'),
    ('הסוף הדרומי של מסילת העקיפה', 'ממשיכה ב-E4 ומתחברת ל-MAIN-B ב-y 2900', 'בולמים מדרום לגשר (y 2774, ב-E4) — סוף זמני',
     'D‑503: החלק שב-E4 נבנה עם S9. הקשת ב-E4 תצטרך להזיז עמוד אחד של קו המתח של E4 (5963, 2760). לאישורך.'),
    ('הצינור PIPE-REF ב-C5', 'המסדרון של REF-SPUR, x 2780', 'x 2728 — 5.2 מ׳ מערבה',
     'ב-x 2780 הצינור היה עובר דרך עמדת המילוי המקורה וצמוד לעמודה C-103. ב-x 2728 — הכי קרוב, בלי לעבור דרך מבנה (בין העמודות C-101 ו-C-102). לאישורך.'),
    ('הסוף הדרומי של הצינור ב-C5', 'עד גבול האזור, y 4250', 'עד העמוד הדרומי ליד הגדר של בית הזיקוק (y 4118), עם אוגן',
     'הגבול עובר באמצע שדרת הנמל. גשר מעל השדרה הוא מפתח אחד, והעמוד הדרומי שלו ב-C6 — נבנה עם S10. לאישורך.'),
    ('הרציפים של ST-E3', 'y 1850–2290 (מפת הדרכים 9נ)', 'y 1760–2530, באותו רוחב',
     'D‑505 — ההחלטה של הבעלים. המפה מתעדכנת בסבב 9ס (סוכן המפה). לא סטייה; לסנכרון.'),
]
APPROVE = [
    'הרכבת שעומדת ברציף (4 קרונות) — לא הוצבה. שתי המסילות שליד הרציפים נושאות את רכבות המשא לשדה: FRT-1 על MAIN-A ו-FRT-4 על MAIN-B, בשני הכיוונים. רכבת שחונה שם הייתה עומדת בדרך שלהן, וזה נגד כלל 25. ברירת המחדל: הרכבת נכנסת כשהחיבור הדרומי של מסילת העקיפה נבנה (S9, ב-E4, ‏y 2900), ו-FRT-4 עוברת אליה. אז MAIN-B ליד רציף 2 פנויה, והרכבת עומדת שם, בין y 1800 ל-2530. לאישורך.',
    'התנועה של רכבות המשא לא השתנתה. מסילת העקיפה מחוברת ל-MAIN-B בצפון (y 1720), ונגמרת בבולמים בדרום. FRT-4 יכולה לעבור אליה רק אחרי החיבור ב-E4.',
    'רציף הפריקה 3 של מסוף החבילות יוצא, ואיתו הטנדר שחנה בו. החצר צרה יותר: 10.2 מ׳ במקום 13.8 מ׳, ונשארים בה שני רציפים.',
]
MOVED = [
    ('E3-DOCK-3 — רציף פריקה 3 של מסוף החבילות (x 5722–5764, ‏y 2428–2536)', 'יוצא — הרציף 1 מתארך דרומה ומכסה את החלק המזרחי שלו'),
    ('PC-E3-DOCK-3 — טנדר המשלוחים שחנה ברציף 3', 'יוצא, יחד עם הרציף'),
    ('E3-YARD-PARCEL — חצר המסוף (x 5634–5772)', 'מתקצרת ל-x 5634–5736'),
    ('הגדר המערבית של מסדרון המסילה (x 5773, ‏y 2294–2544)', 'יוצאת — במקומה גדר לאורך השפה המערבית של הרציף, מול החצר (x 5736)'),
    ('הגדר המערבית בצפון (x 5773, ‏y 1715–1846)', 'מתקצרת ל-y 1700–1756'),
    ('הגדר המזרחית של המסדרון (x 5928, ‏y 1715–2544)', 'יוצאת — מסילת העקיפה בתוך המסדרון; גדר חדשה ב-x 6000, ‏y 1700–2530'),
    ('הגישה הצפונית של מסילת העקיפה על הגשר, עם הבולמים (y 2460–2530)', 'מתחלפת במסילה הרציפה'),
    ('שלט שמות הרציפים בקצה הדרומי של הגג (y 2276)', 'נשאר; שלטים חדשים בקצוות של ההארכות'),
    ('C5 — "בור הצינור" הזמני ליד בית המשאבות (2683, 4080)', 'יוצא — תחנת המגופים מחליפה אותו'),
    ('C5 — שאריות השלוחה בקוד: הנתונים של השלוחה ושל שער המסילה, המקום של המסילה בעמדת המילוי, הציור של המסילה ושל מעבר המסילה LX-3', 'יוצאים (כבר לא היו מצוירים במשחק)'),
]

def page():
    css = """
:root{--bg:#f6f4ef;--fg:#1d2329;--muted:#5d6670;--card:#ffffff;--line:#d9d4c9;--grass:#cfe1bf;--road:#6f757b;--walk:#d8d2c4;--bld:#9aa6b2;--bal:#8b8f90;--rail:#3b4148;
--plat:#e9c46a;--platold:#b5832a;--hall:#8ecae6;--cano:#219ebc;--byp:#c1121f;--map:#7b2cbf;--pipe:#0b6e4f;--valve:#f4a261;--zone:#e76f51;--deck:#adb5bd;--lot:#c8ccd0;--yard:#a7a9ac;--fence:#264653;--gone:#e63946}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14181c;--fg:#e8eaed;--muted:#a3abb3;--card:#1c2228;--line:#333b44;--grass:#29402a;--road:#3d4349;--walk:#57534a;--bld:#5f6b78;--bal:#55595a;--rail:#c9ced3;--plat:#c9a24a;--platold:#e0a13a;--hall:#3f7ea0;--cano:#4cc9f0;--lot:#4a5056;--yard:#3f4246;--fence:#9ad1c8;--deck:#6c757d}}
:root[data-theme="dark"]{--bg:#14181c;--fg:#e8eaed;--muted:#a3abb3;--card:#1c2228;--line:#333b44;--grass:#29402a;--road:#3d4349;--walk:#57534a;--bld:#5f6b78;--bal:#55595a;--rail:#c9ced3;--plat:#c9a24a;--platold:#e0a13a;--hall:#3f7ea0;--cano:#4cc9f0;--lot:#4a5056;--yard:#3f4246;--fence:#9ad1c8;--deck:#6c757d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,'Segoe UI',Arial,sans-serif}
main{max-width:1080px;margin:0 auto;padding:20px 16px 48px}h1{font-size:1.5rem;margin:.2em 0}h2{font-size:1.15rem;margin:1.6em 0 .4em}
.meta{color:var(--muted);font-size:.92rem}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
.map,.elev{width:100%;height:auto;display:block}.two{display:grid;grid-template-columns:1fr;gap:12px}@media(min-width:900px){.two{grid-template-columns:1fr 1fr}}
table{width:100%;border-collapse:collapse;font-size:.92rem}th,td{border-bottom:1px solid var(--line);padding:7px 6px;text-align:right;vertical-align:top}th{color:var(--muted);font-weight:600}
.tw{overflow-x:auto}.key{display:flex;flex-wrap:wrap;gap:8px 14px;font-size:.88rem;color:var(--muted)}.key i{display:inline-block;width:18px;height:10px;border-radius:2px;margin-inline-end:5px;vertical-align:middle}
.ok{color:#2a9d8f;font-weight:600}.ap{color:#e76f51;font-weight:600}ul{padding-inline-start:20px}li{margin:.3em 0}
.grass{fill:var(--grass)}.road{fill:var(--road)}.walk{fill:var(--walk)}.bld{fill:var(--bld)}.pave{fill:var(--walk)}.lot{fill:var(--lot)}.yard{fill:var(--yard)}.dock{fill:none;stroke:#e9c46a;stroke-width:2}
.gone{fill:none;stroke:var(--gone);stroke-width:3;stroke-dasharray:6 4}.corr{fill:none;stroke:var(--fence);stroke-width:1;stroke-dasharray:3 5}.bal{fill:var(--bal)}.rail{stroke:var(--rail);stroke-width:4}
.balb{fill:none;stroke:var(--bal);stroke-width:44;stroke-linejoin:round}.railb{fill:none;stroke:var(--byp);stroke-width:6;stroke-linejoin:round}.mapline{fill:none;stroke:var(--map);stroke-width:3;stroke-dasharray:10 7}
.deck{fill:var(--deck);opacity:.85}.plat{fill:var(--plat)}.platold{fill:none;stroke:var(--platold);stroke-width:2;stroke-dasharray:5 4}.hall{fill:var(--hall);opacity:.45;stroke:var(--fg);stroke-width:2}
.cano{fill:var(--cano);opacity:.55;stroke:var(--cano);stroke-width:2}.stairs{fill:#343a40}.endr{stroke:var(--fence);stroke-width:4}.fence{stroke:var(--fence);stroke-width:4}.fenceold{stroke:var(--gone);stroke-width:3;stroke-dasharray:8 6}
.lamp{fill:#ffd166;stroke:#6c584c;stroke-width:1.5}.tvm{fill:#1d4f91}.path{fill:var(--walk);opacity:.8}.sw{fill:#e9c46a;stroke:var(--fg);stroke-width:2}.buf{fill:var(--gone)}
.zone{stroke:var(--zone);stroke-width:2.5;stroke-dasharray:14 8}.zone2{stroke:var(--zone);stroke-width:1.5;stroke-dasharray:4 8}.barrier{fill:var(--gone)}
.lb,.lbs,.lbb,.lbm,.lbh,.lbp,.lbd,.rd,.zl{font-family:system-ui,'Segoe UI',Arial,sans-serif;fill:var(--fg)}.lbs{font-size:15px}.lbb{font-size:18px;font-weight:700;fill:var(--byp)}.lbm{font-size:16px;fill:var(--map)}
.lbh{font-size:16px;font-weight:700}.lbp{font-size:14px;font-weight:700}.lbd{font-size:15px;fill:var(--muted)}.rd{font-size:20px;fill:#fff;font-weight:600}.zl{font-size:15px;fill:var(--zone);font-weight:600}
.dim{stroke:var(--muted);stroke-width:2;stroke-dasharray:3 3}.cmpbg{fill:var(--card);stroke:var(--fg);stroke-width:1.5}.cmpn{fill:var(--gone)}.cmpt{font-size:12px;font-weight:700;fill:var(--fg)}
.refy{fill:#d6d0c4;stroke:var(--fence);stroke-width:3}.bund{fill:#bdb6a6;stroke:#8d8676;stroke-width:2}.tank{fill:#eef0f1;stroke:#7d868c;stroke-width:2}.rack{stroke:#9aa1a6;stroke-width:8}
.pad{fill:#c9c4b6}.eq{fill:#a5adb4;stroke:#6c757d;stroke-width:1}.fire{fill:#c0392b}.iroad{fill:#7c8288}.spur{fill:none;stroke:var(--muted);stroke-width:5;stroke-dasharray:10 8}
.pipe{stroke:var(--pipe);stroke-width:9}.pipelow{stroke:var(--pipe);stroke-width:5;stroke-dasharray:6 4}.bent{fill:#5c6770}.col{fill:#1d2329}.valve{fill:var(--valve);stroke:var(--fence);stroke-width:3}.cap{fill:var(--pipe);stroke:var(--fg);stroke-width:1.5}
.ground{stroke:var(--muted);stroke-width:2}.iroadE{fill:#7c8288}.tankE{fill:#eef0f1;stroke:#7d868c;stroke-width:2}.valveE{fill:var(--valve)}.pipeE{fill:none;stroke:var(--pipe);stroke-width:5;stroke-linejoin:round}.pipeS{fill:none;stroke:var(--pipe);stroke-width:4;stroke-dasharray:6 4;stroke-linejoin:round}.sleeve{stroke:var(--pipe);stroke-width:4;stroke-dasharray:2 4}
.colE{stroke:#5c6770;stroke-width:4}.beamE{stroke:#5c6770;stroke-width:3}.ladder{stroke:#e9c46a;stroke-width:2;stroke-dasharray:2 2}.rail2{stroke:#e9c46a;stroke-width:2}
"""
    key = [('var(--plat)', 'הרציף החדש'), ('var(--platold)', 'הרציף של היום (מקווקו)'), ('var(--hall)', 'הגג השקוף LIKE-02 — נשאר'), ('var(--cano)', 'סוככי הרציף בהארכות'),
           ('var(--byp)', 'מסילת העקיפה'), ('var(--map)', 'הקו של המפה'), ('var(--fence)', 'גדר'), ('var(--gone)', 'יוצא'), ('var(--zone)', 'גבול אזור')]
    keyc = [('var(--pipe)', 'PIPE-REF על עמודים'), ('var(--valve)', 'תחנת מגופים מגודרת'), ('var(--muted)', 'REF-SPUR של המפה — בוטלה'), ('#5c6770', 'עמוד וקורת רוחב')]
    K = lambda L: '<div class="key">' + ''.join('<span><i style="background:%s"></i>%s</span>' % (c, html.escape(t)) for c, t in L) + '</div>'
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(html.escape(x) for x in r) for r in DIFF)
    mv = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (html.escape(a), html.escape(b)) for a, b in MOVED)
    ap = ''.join('<li>%s</li>' % html.escape(a) for a in APPROVE)
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ציור S7F266</title><style>{css}</style></head><body><main>
<h1>S7F266 — הרציפים של E3, מסילת העקיפה והצינור ב-C5</h1>
<div class="meta">ציור התוכנית לפני הבנייה (כלל 20). הכול מצויר בקוד, לפי הקואורדינטות של המשחק. צפון למעלה, מזרח מימין.<br>
מעודכן עד {html.escape(stamp)} · מול מפת הדרכים, סבב {html.escape(P.get('batch', ''))} ‏(city_plan.json, ‏{psha}) · ההחלטות D‑503, ‏D‑504, ‏D‑505</div>
<h2>E3 — הרציפים, הגגונים ומסילת העקיפה</h2>
<div class="card">{e3_svg()}{K(key)}</div>
<div class="card"><ul>
<li>שני הרציפים מתארכים משני הקצוות, ל-y ‏1760–2530 (77 מ׳ במשחק), באותו רוחב: רציף 1 — 3.8 מ׳, ורציף 2 (רציף אי) — 4.8 מ׳. זה מספיק לרכבת נוסעים של 4 קרונות RL-PS-01 (כ-736 פיקס׳), עם מרווח.</li>
<li>הגג השקוף LIKE-02 נשאר כמו שהוא (y ‏1840–2298). בהארכות — סוככי רציף בסגנון שלו: מסגרת פלדה וזכוכית, רק מעל הרציף, נמוכים יותר.</li>
<li>לכל האורך: פס מישושי צהוב, וקו בטיחות לבן. בהארכות: ספסלים, 4 מכונות כרטיסים נוספות, פנסים עם אלומה בלילה, שלטים בעברית ("רציף 1", "רציף 2", "קרון 1–4"), ומעקה בקצה של כל רציף.</li>
<li>מדרגות המעבר התת-קרקעי נשארות במקומן (y ‏2252–2284). הגדרות מתקצרות לפי הרציף. בין MAIN-B למסילת העקיפה — שביל שירות וחריץ כבלים. ליד המסוט — בית ממסרים.</li>
<li>מסילת העקיפה: מהגשר UX-1 צפונה, לכל האורך של E3, ובקשת של המפה אל MAIN-B ב-y ‏1720, עם מסוט. בסוף הדרומי — בולמים (סוף זמני, ב-E4).</li>
</ul></div>
<h2>C5 — הצינור PIPE-REF על עמודים גבוהים</h2>
<div class="card">{c5_svg()}{K(keyc)}</div>
<div class="card">{elev_svg()}<div class="meta">מבט מהצד, מהמזרח (צפון מימין). הגבהים בקנה מידה; המרחקים לאורך — מוקטנים.</div></div>
<div class="card"><ul>
<li>מחוות המכלים (מהמכל T-101), דרומה ב-x ‏2728, עד הגדר הדרומית של בית הזיקוק: ‏7 עמודי בטון עם קורות רוחב מפלדה, ושני צינורות בצבע אחד.</li>
<li>גובה הצינור 8.6 מ׳. מעל דרך השירות יש גובה חופשי של 8.2 מ׳. אף עמוד לא עומד על כביש, על מדרכה או בכניסה.</li>
<li>לכל האורך יש שביל תחזוקה עם מעקה, ויש סולמות בעמוד הצפוני, בתחנת המגופים ובעמוד הדרומי. הצל נופל מהשמש האחת, לדרום-מזרח.</li>
<li>בקצה הדרומי הצינור יורד לתחנת מגופים מגודרת, עם שני מגופים, ארון מכשירים, שער, שלט ופנס. משם הוא עובר בשרוול מתחת לדרך השירות, ועולה שוב על העמוד הדרומי. שם הוא נסגר באוגן, וההמשך מעל שדרת הנמל — עם S10.</li>
<li>כל השאריות של שלוחת בית הזיקוק יוצאות מהמשחק.</li>
</ul></div>
<h2>איפה הציור שונה מהמפה</h2>
<div class="card tw"><table><thead><tr><th>מה</th><th>במפה</th><th>בציור</th><th>למה</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>מה זז או יוצא מהרצועות</h2>
<div class="card tw"><table><thead><tr><th>מה היה שם</th><th>מה קורה לו</th></tr></thead><tbody>{mv}</tbody></table></div>
<h2>לאישורך</h2>
<div class="card"><ul>{ap}</ul></div>
<div class="meta">לא מחכים לאישור — הבנייה ממשיכה לפי הציור הזה, וכל שינוי שלך נכנס בניסיון הבא.</div>
</main></body></html>"""

open(out, 'w', encoding='utf-8').write(page())
b = open(out, 'rb').read(); print('ok', out, len(b), hashlib.sha1(b).hexdigest()[:12])
