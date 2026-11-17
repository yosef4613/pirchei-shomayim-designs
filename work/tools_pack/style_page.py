# -*- coding: utf-8 -*-
"""style_page.py — the page of the city style guide: deliver/2026-11-02/Turbo_City_City_Style_Guide.html (Hebrew, right to left, one file,
no outside resources). It reads study/style/city_style.json and the last check (study/style/style_check_<build>.json) and draws the street
sections, the stall and the stop in plain SVG. usage: python3 tools_pack/style_page.py"""
import json, re, os, hashlib, html, sys
W = '/home/claude/tc/pkg/work'
GD = json.load(open(W + '/study/style/city_style.json', encoding='utf-8'))
CK = json.load(open(os.environ.get('TC_STYLE_CK', W + '/study/style/style_check_s7f193.json'), encoding='utf-8'))
OUT = os.environ.get('TC_STYLE_OUT', W + '/deliver/2026-11-02/Turbo_City_City_Style_Guide.html')
E = lambda s: html.escape(str(s), quote=True)

def heb_ok(t):
    t = re.sub(r'https?://\S+', ' ', t); t = re.sub(r'\b[\w.\-]+\.(?:html|json|md|js|py|png|txt|zip)\b', ' ', t); t = re.sub(r'\b[0-9a-f]{12,40}\b', ' ', t)
    for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-‑/.']*", t):
        w = w.strip('.-‑/\'')
        if not w or re.search(r'\d', w) or len(w) == 1: continue
        if re.search(r'[_\-‑]', w) and w.upper() == w: continue
        return False
    return True
GLOSS = {'walk_m': 'רוחב המדרכה (מ׳)', 'lane_m': 'רוחב הנתיב (מ׳)', 'sidewalk': 'מדרכה', 'mainWalk': 'מדרכה בעורק הראשי', 'lane': 'נתיב', 'median': 'חציון', 'spacing': 'מרחק',
         'personH': 'גובה האדם', 'ppm': 'פיקסלים למטר', 'game': 'ההגדלה', 'tolL': 'סטייה באורך', 'tolW': 'סטייה ברוחב', 'width': 'רוחב', 'lanes': 'נתיבים', 'speed': 'מהירות',
         'depth': 'עומק', 'stripe': 'פס', 'gap': 'רווח', 'entry': 'כניסה', 'stop': 'עצירה', 'exit': 'יציאה', 'minLen': 'קטע מזערי', 'px': 'פיקס׳', 'main': 'עורק ראשי',
         'arterial': 'עורק', 'avenue': 'שדרה', 'local': 'רחוב מקומי', 'asset': 'הפנס', 'yield': 'תן זכות', 'helicopter': 'מסוק', 'shelter': 'סככה'}
CODE_SRC = {'G', 'CP', 'P367', 'P441', 'P469', 'ZA', 'ZB3', 'ZB4', 'ZC3', 'ZD3', 'ZCD', 'A34', 'REQ'}
def tokens(s):
    """a code string shown by its codes only: the constants, the assets, the numbers and the colours, the known keys in Hebrew, and its Hebrew"""
    out = []
    for m in re.finditer(r"#[0-9a-fA-F]{3,6}|[A-Za-z][A-Za-z0-9]*(?:[_\-‑][A-Za-z0-9]+)*|\.?\d[\d.]*|[\u0590-\u05ff][\u0590-\u05ff\s׳״\-–]*[\u0590-\u05ff׳]", s):
        v = m.group(0).strip()
        if v in GLOSS: v = GLOSS[v]
        if len(v) == 1 and not v.isdigit(): continue
        if v and heb_ok(v) and v not in out: out.append(v)
    return out[:9]
def show_src(sr):
    f = os.path.basename(GD['sources'][sr['f']]['file']); s = sr['s']; s2 = re.sub(r'(?<=\d) ?px\b', ' פיקס׳', s)
    if heb_ok(s2) and len(s2) <= 240: body = '„' + E(s2) + '“'
    else:
        tk = tokens(s); kind = 'מחרוזת בקוד' if sr['f'] in CODE_SRC else 'מחרוזת במסמך'
        body = kind + ((' · ' + ' · '.join(E(t) for t in tk)) if tk else '') + ' <span class="mut">(המלאה בקובץ הנתונים)</span>'
    return '<span class="src"><b>%s</b> %s</span>' % (E(f), body)
def fmt_v(v, unit=''):
    if isinstance(v, dict):
        return ' · '.join('%s: %s' % (E(k), fmt_v(x)) for k, x in v.items())
    if isinstance(v, list):
        if len(v) == 2 and all(isinstance(x, (int, float)) for x in v): return '%s × %s' % (num(v[0]), num(v[1])) if unit.startswith('פיקס') or unit.startswith('מ׳ (') else '%s–%s' % (num(v[0]), num(v[1]))
        return ' · '.join(fmt_v(x) for x in v)
    if isinstance(v, bool): return 'כן' if v else 'לא'
    if isinstance(v, (int, float)): return num(v)
    if v is None: return '—'
    s = str(v); return E(s) if heb_ok(s) else ' · '.join(E(t) for t in tokens(s))
def num(x):
    if isinstance(x, float) and x.is_integer(): x = int(x)
    return E(('%g' % x) if isinstance(x, float) else x)
def clean(s):
    s = str(s); s = re.sub(r'rgba\(([^)]*)\)', lambda m: 'צבע ' + m.group(1), s)
    return E(s) if heb_ok(s) else E(' '.join(w for w in s.split() if heb_ok(w)))

CHECK_HE = {c['id']: c['he'] for c in GD['checks']}
Z = GD['zones_built']; S = CK['summary']; SP = CK['seam_summary']
tot_dev = sum(S[z]['dev'] for z in S); tot_rows = sum(S[z]['rows'] for z in S)
seam_dev = sum(q['dev'] for q in SP.values()); seam_rows = sum(q['rows'] for q in SP.values())

# ---------------------------------------------------------------- the drawings
def svg_section(cls):
    k = GD['kit'][cls]; w, sw, med = k['width_px'], k['sidewalk_px'], k['median_px']; n = k['lanes']; lane = k['lane_px']
    sc = 1.9; band = w + 2 * sw; X0 = 20; H = 150; Wsvg = band * sc + 40
    x = lambda v: X0 + v * sc
    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="חתך %s" class="sec">' % (Wsvg, H + 40, E(k['he']))]
    parts.append('<rect x="%.1f" y="30" width="%.1f" height="%d" class="walk"/>' % (x(0), sw * sc, H - 60))
    parts.append('<rect x="%.1f" y="30" width="%.1f" height="%d" class="walk"/>' % (x(sw + w), sw * sc, H - 60))
    parts.append('<rect x="%.1f" y="30" width="%.1f" height="%d" class="asph"/>' % (x(sw), w * sc, H - 60))
    parts.append('<line x1="%.1f" y1="30" x2="%.1f" y2="%d" class="curb"/><line x1="%.1f" y1="30" x2="%.1f" y2="%d" class="curb"/>' % (x(sw), x(sw), H - 30, x(sw + w), x(sw + w), H - 30))
    for e in (sw + 5, sw + w - 5): parts.append('<line x1="%.1f" y1="30" x2="%.1f" y2="%d" class="edge"/>' % (x(e), x(e), H - 30))
    mid = sw + w / 2
    if med:
        parts.append('<rect x="%.1f" y="30" width="%.1f" height="%d" class="med"/>' % (x(mid - med / 2), med * sc, H - 60))
        for o in (-med / 2, med / 2): parts.append('<line x1="%.1f" y1="30" x2="%.1f" y2="%d" class="yel"/>' % (x(mid + o), x(mid + o), H - 30))
        per = n // 2
        for kk in range(1, per):
            for sgn in (-1, 1): parts.append('<line x1="%.1f" y1="30" x2="%.1f" y2="%d" class="lanel"/>' % (x(mid + sgn * (med / 2 + lane * kk)), x(mid + sgn * (med / 2 + lane * kk)), H - 30))
    else:
        parts.append('<line x1="%.1f" y1="30" x2="%.1f" y2="%d" class="%s"/>' % (x(mid), x(mid), H - 30, 'yel' if cls == 'avenue' else 'cen'))
    for cx in (sw / 2, sw + w + sw / 2):
        parts.append('<circle cx="%.1f" cy="62" r="5" class="lamp"/><circle cx="%.1f" cy="%d" r="6" class="tree"/>' % (x(cx), x(cx), H - 50))
    parts.append('<text x="%.1f" y="22" class="lbl" text-anchor="middle">%s מ׳ · %d נתיבים</text>' % (x(mid), num(w / 10), n))
    parts.append('<text x="%.1f" y="%d" class="lbl" text-anchor="middle">%s</text>' % (x(sw / 2), H - 14, num(sw / 10)))
    parts.append('<text x="%.1f" y="%d" class="lbl" text-anchor="middle">%s</text>' % (x(sw + w + sw / 2), H - 14, num(sw / 10)))
    sp = k['lamp']['spacing_px']; ts = k['trees']['spacing_px']
    parts.append('<text x="%.1f" y="%d" class="lbl2" text-anchor="middle">פנס כל %s מ׳ לכל היותר%s</text>' % (x(mid), H + 8, num(sp / 10), (' · עץ כל %s–%s מ׳ בשני הצדדים' % (num(ts[0] / 10), num(ts[1] / 10))) if ts else ''))
    parts.append('</svg>'); return ''.join(parts)
def svg_stalls():
    s = 3.2; W0, H0 = GD['parking']['stall_px']; out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="שלוש חניות" class="sec">' % (3 * W0 * s + 120, H0 * s + 70)]
    for i, (cls, he) in enumerate((('st', 'רגילה'), ('acc', 'נכים'), ('ev', 'חשמל'))):
        x0 = 40 + i * (W0 * s + 20)
        out.append('<rect x="%.1f" y="24" width="%.1f" height="%.1f" class="%s"/>' % (x0, W0 * s, H0 * s, cls))
        if cls == 'acc': out.append('<rect x="%.1f" y="30" width="%.1f" height="%.1f" class="frame"/><circle cx="%.1f" cy="%.1f" r="14" class="sym"/>' % (x0 + 6, W0 * s - 12, H0 * s - 12, x0 + W0 * s / 2, 24 + H0 * s / 2))
        if cls == 'ev': out.append('<rect x="%.1f" y="%.1f" width="16" height="26" rx="3" class="sym"/><rect x="%.1f" y="10" width="10" height="16" class="chg"/>' % (x0 + W0 * s / 2 - 8, 24 + H0 * s / 2 - 13, x0 + W0 * s - 14))
        out.append('<text x="%.1f" y="%.1f" class="lbl" text-anchor="middle">%s</text>' % (x0 + W0 * s / 2, H0 * s + 44, he))
    out.append('<text x="%d" y="%.1f" class="lbl2">2.8 × 5.6 מ׳</text>' % (3 * W0 * s + 100, 24 + H0 * s / 2))
    out.append('</svg>'); return ''.join(out)
def svg_stop():
    b = GD['stop']['bay']; s = 2.2; L = b['entry'] + b['stop'] + b['exit']; Wd = L * s + 120; road = 44 * s
    y0 = 30; yc = y0 + road; d = b['depth'] * s; x0 = 60
    pts = [(x0, yc), (x0 + b['entry'] * s, yc + d), (x0 + (b['entry'] + b['stop']) * s, yc + d), (x0 + L * s, yc)]
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="מפרץ התחנה" class="sec">' % (Wd, yc + d + 90)]
    out.append('<rect x="10" y="%d" width="%d" height="%.1f" class="asph"/>' % (y0, Wd - 20, road))
    out.append('<polygon points="%s" class="asph"/>' % ' '.join('%.1f,%.1f' % p for p in pts))
    out.append('<rect x="10" y="%.1f" width="%d" height="%.1f" class="walk"/>' % (yc + d, Wd - 20, 20 * s))
    out.append('<polyline points="%s" class="curbp"/>' % ' '.join('%.1f,%.1f' % p for p in [(10, yc)] + pts + [(Wd - 10, yc)]))
    sx = x0 + (b['entry'] + b['stop'] * .55) * s
    out.append('<rect x="%.1f" y="%.1f" width="54" height="16" class="shel"/><rect x="%.1f" y="%.1f" width="30" height="5" class="bench"/>' % (sx, yc + d + 10, sx + 12, yc + d + 30))
    out.append('<circle cx="%.1f" cy="%.1f" r="5" class="signp"/>' % (x0 + (b['entry'] + b['stop'] * .15) * s, yc + d + 14))
    for a, bb, t in ((0, b['entry'], 'כניסה %s מ׳' % num(b['entry'] / 10)), (b['entry'], b['entry'] + b['stop'], 'עצירה %s מ׳' % num(b['stop'] / 10)), (b['entry'] + b['stop'], L, 'יציאה %s מ׳' % num(b['exit'] / 10))):
        out.append('<text x="%.1f" y="%.1f" class="lbl" text-anchor="middle">%s</text>' % (x0 + (a + bb) / 2 * s, yc + d + 72, t))
    out.append('<text x="%.1f" y="%.1f" class="lbl2" text-anchor="middle">עומק %s מ׳ · סככה, ספסל ושלט אחד בכל העיר</text>' % (x0 + L * s / 2, y0 - 10, num(b['depth'] / 10)))
    out.append('</svg>'); return ''.join(out)

# ---------------------------------------------------------------- the sections
def zone_table():
    rows = []
    for z in list(Z.keys()) + ['העיר']:
        q = S.get(z)
        if not q: continue
        top = sorted(q['by_check'].items(), key=lambda kv: -kv[1])[:4]
        rows.append('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td class="n">%d</td><td class="n">%d</td><td class="n %s">%d</td><td class="n">%d</td><td>%s</td></tr>' % (
            E(z), E(Z[z]['he'] if z in Z else 'הקוד של כל העיר'), E(Z[z]['district'] if z in Z else '—'), q['rows'], q['ok'], 'bad' if q['dev'] else 'good', q['dev'], q['dev_reason'],
            ' · '.join('%s %s (%d)' % (E(c), E(CHECK_HE.get(c, '')), n) for c, n in top) or '—'))
    return '<table class="t"><thead><tr><th>אזור</th><th>מה יש בו</th><th>רובע</th><th>בדיקות</th><th>תקין</th><th>חריגות</th><th>עם סיבה</th><th>החריגות העיקריות</th></tr></thead><tbody>%s</tbody></table>' % ''.join(rows)
def seam_table():
    rows = []
    for p, q in sorted(SP.items()):
        devs = [s for s in CK['seams'] if s['pair'] == p and not s['ok']]
        rows.append('<tr><td><b>%s</b></td><td class="n">%d</td><td class="n %s">%d</td><td>%s</td></tr>' % (E(p), q['rows'], 'bad' if q['dev'] else 'good', q['dev'], ' · '.join(clean(s['item']) + ': ' + clean(s['have']) for s in devs) or 'הכביש, המדרכה והשורות ממשיכים'))
    return '<table class="t"><thead><tr><th>תפר</th><th>בדיקות</th><th>חריגות</th><th>מה נמצא</th></tr></thead><tbody>%s</tbody></table>' % ''.join(rows)
def conflicts():
    out = []
    for c in GD['conflicts']:
        opts = ''.join('<li>%s<div class="srcs">%s</div></li>' % (E(o['he']), ' '.join(show_src(s) for s in o['src'])) for o in c['options'])
        out.append('<div class="cf"><div class="cfh"><span class="tag">%s</span> <b>%s</b> <span class="pill">לאישורך</span></div><div class="dflt">ברירת המחדל: %s</div><ul>%s</ul></div>' % (E(c['id']), E(c['item']), E(c['default']), opts))
    return ''.join(out)
def kit_table():
    hd = '<tr><th>סוג</th><th>במפה</th><th>רוחב</th><th>נתיבים</th><th>נתיב</th><th>חציון</th><th>מדרכה</th><th>פנס</th><th>מרחק פנסים</th><th>עצים</th><th>מעבר חצייה</th></tr>'
    rows = []
    for k, v in GD['kit'].items():
        rows.append('<tr><td><b>%s</b></td><td>%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td>%s · %s</td><td class="n">%s–%s</td><td>%s</td><td class="n">%s</td></tr>' % (
            E(v['he']), clean(v['map']), num(v['width_px']) if v['width_px'] else '—', num(v['lanes']) if v['lanes'] else '—', num(v['lane_px']) if v['lane_px'] else '—', num(v['median_px']) if v['median_px'] is not None else '—',
            num(v['sidewalk_px']) if v['sidewalk_px'] else '—', E(v['lamp']['asset']), E(v['lamp']['he']), num(v['lamp'].get('min_gap_px') or 0) if v['lamp'].get('min_gap_px') else '—', num(v['lamp']['spacing_px']),
            ('כל %s–%s, בשני הצדדים' % (num(v['trees']['spacing_px'][0]), num(v['trees']['spacing_px'][1]))) if v['trees']['spacing_px'] else 'לא נקבע (ס-3)', num(v['crosswalk_depth_px']) if v['crosswalk_depth_px'] else '—'))
    return '<p class="mut">כל המידות בפיקסלים של העולם (10 פיקס׳ = 1 מ׳).</p><table class="t">%s%s</table>' % (hd, ''.join(rows))
def groups():
    out = []
    for g in GD['groups']:
        rows = []
        for r in g['rules']:
            tags = (' <span class="tag">%s</span>' % E(r['check'])) if r.get('check') else ''
            tags += (' <span class="pill">%s · לאישורך</span>' % E(r['conflict'])) if r.get('conflict') else ''
            note = ('<div class="mut">%s</div>' % E(r['note'])) if r.get('note') else ''
            rows.append('<tr><td class="id">%s</td><td><b>%s</b>%s%s</td><td>%s <span class="mut">%s</span></td><td class="srcs">%s</td></tr>' % (
                E(r['id']), E(r['he']), tags, note, fmt_v(r['v'], r['unit']), E(r['unit']) if heb_ok(r['unit']) else '', ' '.join(show_src(s) for s in r['src'])))
        out.append('<h3>%s</h3><table class="t rules"><thead><tr><th>מספר</th><th>הכלל</th><th>הערך</th><th>המקור</th></tr></thead><tbody>%s</tbody></table>' % (E(g['he']), ''.join(rows)))
    return ''.join(out)
def palettes():
    out = []
    for d, p in GD['palettes'].items():
        zs = [z for z in Z if Z[z]['district'] == d]
        sw = lambda L: ''.join('<span class="sw"><i style="background:%s"></i>%s<small>%d דגמים</small></span>' % (E(c['v']), E(c['v']) if heb_ok(c['v']) else '', len(c['types'])) for c in L)
        out.append('<div class="pal"><h3>רובע %s <span class="mut">· %s</span></h3><div><b>קירות</b> %s</div><div><b>גגות</b> %s</div><div><b>חומרים</b> %s · <b>סוגי גג</b> %s</div></div>' % (
            E(d), ', '.join(zs), sw(p['walls']), sw(p['roofs']), ' · '.join(E(m['v']) for m in p['materials']), ' · '.join(E(m['v']) for m in p['roof_kinds'])))
    return ''.join(out)
def checks_list():
    return '<table class="t"><thead><tr><th>בדיקה</th><th>מה נבדק</th><th>איך</th></tr></thead><tbody>%s</tbody></table>' % ''.join(
        '<tr><td class="id">%s</td><td><b>%s</b></td><td>%s</td></tr>' % (E(c['id']), E(c['he']), E(c['what'])) for c in GD['checks'])
def method():
    M = GD['method']; items = [('קטע הרחוב', M['side_line']), ('ליד צומת', M['junction_band']), ('פערים בעצים', M['openings']), ('בתפר', 'חלון של ' + M['seam_window'] + '; שורה היא אותו קו אם המרחק מהציר שווה עד 4 פיקס׳'),
             ('עצי רחוב', 'עץ שייך לצד של הרחוב אם הוא בין השפה ל-40 פיקס׳ אחרי המדרכה'), ('מבנים שכנים', 'שני מבנים "זה ליד זה" — עד 150 פיקס׳ בין הטביעות'),
             ('חיץ העצים', 'עצים ב-100 פיקס׳ הראשונים של האזור מהגבול מול המגורים'), ('תחנה', 'מקצה משטח ההמתנה (66 / 74 פיקס׳) עד שפת הצומת')]
    return '<ul class="m">%s</ul>' % ''.join('<li><b>%s:</b> %s</li>' % (E(a), E(b)) for a, b in items)
def zone_details():
    out = []
    for z in list(Z.keys()) + ['העיר']:
        R = [r for r in CK['rows'] if r['zone'] == z]
        if not R: continue
        dev = [r for r in R if r['ok'] is False]; ok = [r for r in R if r['ok']]; info = [r for r in R if r['ok'] is None]
        def tr(r):
            st = '<span class="ok">תקין</span>' if r['ok'] else ('<span class="mut">מידע</span>' if r['ok'] is None else '<span class="dev">חריגה</span>')
            rs = E(r['reason']) if r.get('reason') else ('—' if r['ok'] is not False else 'אין')
            return '<tr><td class="id">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (E(r['check']), clean(r['item']), clean(r['need']), clean(r['have']), st, rs)
        head = '<tr><th>בדיקה</th><th>כלל</th><th>נדרש</th><th>יש</th><th>תקין / חריגה</th><th>סיבה רשומה</th></tr>'
        out.append('<details%s><summary><b>%s</b> — %s · %d חריגות מתוך %d בדיקות</summary><table class="t">%s%s</table></details>' % (
            ' open' if z == 'העיר' else '', E(z), E(Z[z]['he'] if z in Z else 'הקוד של כל העיר'), len(dev), len(dev) + len(ok), head, ''.join(tr(r) for r in dev + ok + info)))
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (E(s['pair']), clean(s['item']), clean(s['need']), clean(s['have']), '<span class="ok">תקין</span>' if s['ok'] else '<span class="dev">חריגה</span>', E(s['reason']) if s.get('reason') else ('—' if s['ok'] else 'אין')) for s in CK['seams'])
    out.append('<details><summary><b>התפרים</b> — %d חריגות מתוך %d בדיקות</summary><table class="t"><tr><th>תפר</th><th>כלל</th><th>נדרש</th><th>יש</th><th>תקין / חריגה</th><th>סיבה רשומה</th></tr>%s</table></details>' % (seam_dev, seam_rows, rows))
    return ''.join(out)
def files():
    L = [('study/style/city_style.json', 'מדריך הסגנון — קובץ הנתונים'), ('tools_pack/style_check.py', 'הבדיקה'), ('tools_pack/style_dump.js', 'השאילתה מהמשחק'),
         ('tools_pack/style_build.py', 'הבונה של המדריך (מאמת כל מחרוזת במקור)'), ('tools_pack/style_page.py', 'הבונה של הדף'), ('study/style/style_exceptions.json', 'החריגות הרשומות (ריק — אין עדיין אף סיבה)'),
         ('study/style/dump_' + os.environ.get('TC_STYLE_B', 's7f193') + '.json', 'העובדות מהמשחק ' + os.environ.get('TC_STYLE_B', 's7f193').upper()), ('study/style/style_check_' + os.environ.get('TC_STYLE_B', 's7f193') + '.json', 'תוצאת הבדיקה')]
    rows = []
    for p, he in L:
        b = open(W + '/' + p, 'rb').read(); rows.append('<tr><td>%s</td><td>%s</td><td class="n">%s</td><td class="n">%s</td></tr>' % (E(os.path.basename(p)), E(he), hashlib.sha1(b).hexdigest()[:12], '{:,}'.format(len(b))))
    return '<table class="t"><thead><tr><th>קובץ</th><th>מה</th><th>טביעה</th><th>בתים</th></tr></thead><tbody>%s</tbody></table>' % ''.join(rows)
def sources():
    return '<table class="t"><thead><tr><th>מקור</th><th>קובץ</th><th>טביעה</th><th>בתים</th></tr></thead><tbody>%s</tbody></table>' % ''.join(
        '<tr><td>%s</td><td>%s</td><td class="n">%s</td><td class="n">%s</td></tr>' % (E(v['he']), E(os.path.basename(v['file'])), v['sha1'], '{:,}'.format(v['bytes'])) for v in GD['sources'].values())

CSS = """
:root{--bg:#f4f7fb;--surface:#fff;--ink:#0b1a2b;--ink2:#41546b;--line:#d6dee8;--soft:#e9eff6;--amber:#c98200;--coral:#d9363c;--teal:#0f8f93;--sky:#2a7fc9;--green:#1f9d5a;
--walk:#d9d3c4;--asph:#4b5057;--med:#7d8a6a;--yel:#f2c83e;--lane:#f3f1dc;--tree:#3f8a3a;--lamp:#ffb020;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b1a2b;--surface:#11243a;--ink:#f4f7fb;--ink2:#a9b8ca;--line:#24405e;--soft:#16304b;--amber:#ffb020;--coral:#ff5a5f;--teal:#19c3c7;--sky:#5ab8ff;--green:#3ddc84;
--walk:#8f8a7e;--asph:#2b3036;--med:#56634a;--tree:#5fb85a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0b1a2b;--surface:#11243a;--ink:#f4f7fb;--ink2:#a9b8ca;--line:#24405e;--soft:#16304b;--amber:#ffb020;--coral:#ff5a5f;--teal:#19c3c7;--sky:#5ab8ff;--green:#3ddc84;--walk:#8f8a7e;--asph:#2b3036;--med:#56634a;--tree:#5fb85a;color-scheme:dark}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans Hebrew","Segoe UI",Arial,sans-serif;font-size:15px;line-height:1.6}
.wrap{max-width:1180px;margin:0 auto;padding:24px 16px 64px}
header h1{font-size:30px;margin:0 0 4px;letter-spacing:-.01em}header p{margin:0;color:var(--ink2)}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.meta span{background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:20px 0}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px}.kpi b{display:block;font-size:26px;font-variant-numeric:tabular-nums}.kpi span{color:var(--ink2);font-size:13px}
section{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 18px 10px;margin:18px 0}
h2{font-size:21px;margin:0 0 10px}h3{font-size:16px;margin:16px 0 6px}
.t{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 12px}.t th,.t td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top}
.t th{background:var(--soft);font-weight:600;position:sticky;top:0}.t .n{text-align:left;font-variant-numeric:tabular-nums;white-space:nowrap}.t .id{white-space:nowrap;color:var(--ink2);font-variant-numeric:tabular-nums}
.scroll{overflow-x:auto}.bad{color:var(--coral);font-weight:700}.good{color:var(--green);font-weight:700}
.ok{color:var(--green)}.dev{color:var(--coral);font-weight:600}.mut{color:var(--ink2);font-size:12.5px}
.tag{display:inline-block;background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:0 6px;font-size:12px;margin-inline-start:4px}
.pill{display:inline-block;background:color-mix(in srgb,var(--amber) 18%,transparent);color:var(--ink);border:1px solid var(--amber);border-radius:999px;padding:0 8px;font-size:12px;margin-inline-start:4px}
.src{display:block;font-size:12.5px;color:var(--ink2)}.src b{color:var(--ink);font-weight:600}.srcs{min-width:260px}
.cf{border:1px solid var(--line);border-inline-start:4px solid var(--amber);border-radius:10px;padding:10px 12px;margin:10px 0}.cfh{margin-bottom:4px}.dflt{font-weight:600}.cf ul{margin:6px 0 0;padding-inline-start:20px}
.secs{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}.secs figure{margin:0;background:var(--soft);border-radius:10px;padding:8px}.secs figcaption{font-weight:600;margin-bottom:4px}
svg.sec{width:100%;height:auto;display:block}svg .walk{fill:var(--walk)}svg .asph{fill:var(--asph)}svg .med{fill:var(--med)}svg .curb{stroke:#2d2f33;stroke-width:3}
svg .edge{stroke:#f5f5eb;stroke-width:1.4;opacity:.7}svg .yel{stroke:var(--yel);stroke-width:2.4}svg .cen{stroke:#eee9bb;stroke-width:2.2;stroke-dasharray:9 7}svg .lanel{stroke:var(--lane);stroke-width:2;stroke-dasharray:10 9}
svg .lamp{fill:var(--lamp);stroke:#2d2f33;stroke-width:1.2}svg .tree{fill:var(--tree)}svg .lbl{fill:var(--ink);font-size:12px}svg .lbl2{fill:var(--ink2);font-size:12px}
svg .st{fill:#5f6468;stroke:#f2f2ea;stroke-width:2}svg .acc{fill:#2f6fd0;stroke:#fff;stroke-width:2}svg .ev{fill:#1f9d5a;stroke:#fff;stroke-width:2}svg .frame{fill:none;stroke:#fff;stroke-width:2}svg .sym{fill:#fff}svg .chg{fill:#2d2f33}
svg .curbp{fill:none;stroke:#2d2f33;stroke-width:2.5}svg .shel{fill:#59626b}svg .bench{fill:#8a5a35}svg .signp{fill:#2f6fd0;stroke:#fff;stroke-width:1.5}
.pal{border-top:1px solid var(--line);padding:6px 0}.pal div{margin:4px 0}.sw{display:inline-flex;align-items:center;gap:4px;margin:2px 0 2px 10px;font-size:12.5px;font-variant-numeric:tabular-nums}
.sw i{display:inline-block;width:18px;height:18px;border-radius:4px;border:1px solid var(--line)}.sw small{color:var(--ink2)}
details{border:1px solid var(--line);border-radius:10px;margin:8px 0;padding:6px 10px;background:var(--surface)}summary{cursor:pointer;padding:4px 0}
ul.m{margin:4px 0;padding-inline-start:20px}ul.m li{margin:3px 0}
@media (max-width:640px){header h1{font-size:24px}.t{font-size:12.5px}.srcs{min-width:180px}}
"""

def page():
    n = GD['counts']
    body = []
    body.append('<header><h1>מדריך הסגנון של העיר</h1><p>המקור האחד לעיצוב של כל אזור: ערכת רחוב לכל סוג דרך, סימון, תמרורים, תחנה, חניון, גבולות, פלטה לכל רובע, גבהים ותקן אחד — וכל ערך עם המקור שלו. מתחת — מה הבדיקה האוטומטית מצאה בשמונת האזורים הבנויים ובתפרים ביניהם.</p>'
                '<div class="meta"><span>הבנייה ' + os.environ.get('TC_STYLE_B', 's7f193').upper() + '</span><span>2.11.2026</span><span>%d כללים</span><span>%d בדיקות אוטומטיות</span><span>%d סתירות לאישורך</span><span>%d מקורות</span></div></header>' % (n['rules'], n['checks'], n['conflicts'], n['sources']))
    body.append('<div class="kpis"><div class="kpi"><b>%d</b><span>שורות בדיקה באזורים</span></div><div class="kpi"><b class="bad">%d</b><span>חריגות באזורים</span></div><div class="kpi"><b>0</b><span>חריגות עם סיבה רשומה</span></div><div class="kpi"><b class="bad">%d</b><span>חריגות בתפרים, מתוך %d</span></div><div class="kpi"><b>%d</b><span>סתירות לאישורך</span></div></div>' % (tot_rows, tot_dev, seam_dev, seam_rows, n['conflicts']))
    body.append('<section><h2>1. התוצאה לכל אזור</h2><p class="mut">הדרישה: אפס חריגות, או חריגה שנרשמה עם סיבה בקובץ style_exceptions.json. הבדיקה רק מודדת — שום דבר באזורים לא שונה.</p><div class="scroll">%s</div><h3>התפרים בין אזורים שכנים</h3><div class="scroll">%s</div></section>' % (zone_table(), seam_table()))
    body.append('<section><h2>2. לאישורך — הסתירות בין המקורות</h2><p class="mut">בכל סתירה: ברירת המחדל שהמדריך והבדיקה משתמשים בה, והאפשרויות עם המקור של כל אחת. שום בחירה לא נעשתה בשקט.</p>%s</section>' % conflicts())
    body.append('<section><h2>3. ערכת הרחוב לכל סוג דרך</h2>%s<div class="secs"><figure><figcaption>עורק ראשי</figcaption>%s</figure><figure><figcaption>עורק</figcaption>%s</figure><figure><figcaption>שדרה עירונית</figcaption>%s</figure><figure><figcaption>רחוב מקומי</figcaption>%s</figure>'
                '<figure><figcaption>חניה רגילה, נכים וחשמל</figcaption>%s</figure><figure><figcaption>תחנת אוטובוס</figcaption>%s</figure></div><p class="mut">השרטוטים בקנה מידה אחד לכל חתך; הנקודה הכתומה — פנס, העיגול הירוק — עץ.</p></section>' % (
                    kit_table(), svg_section('main'), svg_section('arterial'), svg_section('avenue'), svg_section('local'), svg_stalls(), svg_stop()))
    body.append('<section><h2>4. כל הכללים והמקור של כל ערך</h2><p class="mut">המקור: הקובץ והמחרוזת המדויקת (קיצור הפיקסלים של המסמך מוצג כאן „פיקס׳“). מחרוזת מהקוד מוצגת לפי הקודים שבה; המלאה — בקובץ הנתונים city_style.json, והבונה בודק שכל מחרוזת באמת בקובץ שלה.</p><div class="scroll">%s</div></section>' % groups())
    body.append('<section><h2>5. הפלטה לכל רובע</h2><p class="mut">מה שיש בנתונים של האזורים הבנויים: צבע הקיר וצבע הגג כמו בקוד של המבנה, החומר וסוג הגג. אזור חדש בוחר מתוך הפלטה של הרובע שלו.</p>%s</section>' % palettes())
    body.append('<section><h2>6. הבדיקות האוטומטיות ושיטת המדידה</h2><div class="scroll">%s</div>%s</section>' % (checks_list(), method()))
    body.append('<section><h2>7. התוצאה המלאה — שורה לכל בדיקה</h2>%s</section>' % zone_details())
    body.append('<section><h2>8. המקורות והקבצים</h2><h3>המקורות שהמדריך נלקח מהם</h3><div class="scroll">%s</div><h3>הקבצים של המדריך</h3><div class="scroll">%s</div></section>' % (sources(), files()))
    return '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מדריך הסגנון של העיר</title><style>%s</style></head><body><div class="wrap">%s</div></body></html>' % (CSS, ''.join(body))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(page())
b = open(OUT, 'rb').read(); print(os.path.basename(OUT), hashlib.sha1(b).hexdigest()[:12], len(b))
