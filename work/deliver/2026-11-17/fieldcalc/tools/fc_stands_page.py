#!/usr/bin/env python3
# fc_stands_page.py — הדף Stands_matrix.html (הבעלים 17.11 11:10): מפה של כל העמדות, כמה סוגים נכנסים בכל אחת, הטבלה עמדה × סוג עם הסיבה, ומי בלוח היום.
# SVG בקוד בלבד (כלל 13 / 17), בלי תמונות. הנתונים — stands_matrix.json (fc_stands.py).
import os, json, html, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); E = html.escape
M = json.load(open(os.path.join(HERE, 'stands_matrix.json'), encoding='utf-8'))
D = json.load(open(os.path.join(HERE, 's15_base.json'), encoding='utf-8'))['S15D']
NOW = subprocess.run(['bash', '-c', 'TZ=Asia/Jerusalem date "+%d.%m.%Y %H:%M"'], capture_output=True, text=True).stdout.strip()
T = M['types']; TM = {t['m']: t for t in T}; ST = M['stands']
SZ = {'S': ('קטן — מוטה עד 20 מ׳', 'sz-s'), 'M': ('בינוני — 20–40 מ׳', 'sz-m'), 'L': ('גדול — 40–60 מ׳', 'sz-l'), 'XL': ('ענק — מעל 60 מ׳', 'sz-xl')}
GROUP = [('עמדות השרוול (צפון, מול הטרקלינים)', ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']), ('המטען (מערב)', ['C1', 'C2', 'CH']),
         ('העמדות המרוחקות (דרום)', ['R1', 'R2', 'R3']), ('פרטי ומנהלים (דרום, מול ה-GA)', ['GA1', 'GA2', 'GA3', 'GA4', 'GA5', 'GA6', 'GA7'])]
def biggest(s):
    z = ST[s]['sizes']; return z[-1] if z else None
def rect(r, cls, extra=''): return '<rect x="%d" y="%d" width="%d" height="%d" class="%s" %s/>' % (r[0], r[1], r[2] - r[0], r[3] - r[1], cls, extra)
def txt(x, y, s, cls, anchor='middle'): return '<text x="%d" y="%d" text-anchor="%s" class="%s">%s</text>' % (x, y, anchor, cls, E(s))
def use_txt(s):
    u = ST[s]['use']
    return ' · '.join('%s (%s)' % (TM[m]['code'] if m in TM else m, src) for m, src in u) if u else '—'
def svg_map(X0=4760, Y0=-300, X1=9700, Y1=2620, k=1.0):
    o = ['<svg viewBox="%d %d %d %d" class="map" role="img" aria-label="מפת העמדות בשדה: לכל עמדה הגודל המרבי שנכנס, מספר הסוגים, קווי העצירה, ומי בלוח היום">' % (X0, Y0, X1 - X0, Y1 - Y0)]
    o.append(rect([X0, Y0, X1, Y1], 'land'))
    for kk in ('apron', 'apronS'): o.append(rect(D[kk], 'apron'))
    for kk in ('twa', 'twb', 'twc'): o.append(rect(D[kk], 'twy'))
    o.append(rect(D['rwy'], 'rwy')); o.append(rect(D['term'], 'bld')); o.append(txt((D['term'][0] + D['term'][2]) / 2, D['term'][3] - 30, 'הטרמינל ואגף השערים', 'lbl'))
    for h in M['hangars']:
        o.append(rect(h['rect'], 'hgr')); r = h['rect']; o.append(txt((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 10, h['label'].split(' — ')[0], 'lbls'))
    for h in M['helipads']:
        c = h['c']; o.append('<circle cx="%d" cy="%d" r="%d" class="hp"/>' % (c[0], c[1], (h['pad'] or 100) / 2)); o.append(txt(c[0], c[1] + 12, h['id'], 'lbls'))
    for s, q in ST.items():
        r = q['rect']; b = biggest(s); cls = 'st ' + (SZ[b][1] if b else 'sz-none') + (' ch' if s == 'CH' else '')
        o.append(rect(r, cls))
        cx = q['cx']; ny = q['nose']
        # קווי העצירה: העבה — של העמדה; הדקות — לפי סוג (המטוס זז אחורה)
        stops = sorted({q['row'][m].get('stop') for m in q['row'] if q['row'][m]['ok'] and q['row'][m]['shift']} - {None})
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="stop0"/>' % (cx - 30, ny, cx + 30, ny))
        for y in stops: o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="stop1"/>' % (cx - 18, y, cx + 18, y))
        if s != 'CH':
            used = bool(q['use']); w = r[2] - r[0]; f = (1 if w > 250 else (.62 if k == 1 else .78)) * (k if w > 250 else 1); cx2 = (r[0] + r[2]) / 2; y0 = r[1] + 6
            o.append('<text x="%d" y="%d" text-anchor="middle" style="font-size:%dpx;font-weight:bold">%s</text>' % (cx2, y0 + 52 * f, 52 * f, E(s)))
            o.append('<text x="%d" y="%d" text-anchor="middle" style="font-size:%dpx">%s</text>' % (cx2, y0 + 96 * f, 38 * f, E('%d סוגים' % q['n_ok'])))
            o.append('<text x="%d" y="%d" text-anchor="middle" class="%s" style="font-size:%dpx">%s</text>' % (cx2, y0 + 136 * f, 'use' if used else 'unused', 32 * f, E(('בלוח: ' + ', '.join(TM[m]['code'] for m, _ in q['use'])) if used else 'ריקה בלוח')))
        else:
            o.append(txt((r[0] + r[2]) / 2, r[3] + 34, 'CH (מקווקו) — חופפת ל-C1 / C2', 'lbls'))
    o.append('<g class="nArrow"><line x1="4900" y1="2560" x2="4900" y2="2400"/><text x="4900" y="2370" text-anchor="middle">צפון</text></g>')
    o.append('</svg>'); return ''.join(o)
def legend():
    h = ['<div class="legend">']
    for k, (lab, cls) in SZ.items(): h.append('<span><i class="sw %s"></i>%s</span>' % (cls, E(lab)))
    h.append('<span><i class="sw sz-none"></i>לא בשימוש לטיסות</span><span><i class="ln0"></i>קו העצירה של העמדה</span><span><i class="ln1"></i>קו עצירה לסוג קטן יותר (המטוס עוצר אחורה)</span></div>')
    return ''.join(h)
def cell(s, m):
    c = ST[s]['row'][m]
    if c['ok'] and not c['shift']: return '<td class="ok" title="%s">✓</td>' % E(c['service'])
    if c['ok']: return '<td class="ok2" title="%s">✓ +%.0f מ׳</td>' % (E('קו עצירה לסוג: המטוס עוצר %.0f מ׳ אחורה. בעצירה של העמדה: %s · %s' % (c['shift'] / 10, '; '.join(c['why']), c['service'])), c['shift'] / 10)
    return '<td class="no" title="%s">✗</td>' % E('; '.join(c['why']))
def table():
    h = ['<div class="tw"><table class="mx"><thead><tr><th>עמדה</th><th>מתוכנן ל-</th>']
    for t in T: h.append('<th class="%s"><span class="v">%s</span><small>%s</small></th>' % (SZ[t['size']][1], E(t['code']), E(t['he'])))
    h.append('<th>כמה</th><th>בלוח היום</th></tr></thead><tbody>')
    for gname, L in GROUP:
        h.append('<tr class="grp"><td colspan="%d">%s</td></tr>' % (len(T) + 4, E(gname)))
        for s in L:
            q = ST[s]; d = q['design']
            h.append('<tr><th>%s</th><td>%s</td>' % (E(s), E(TM[d]['code'] if d in TM else (d or '—'))))
            if s == 'CH': h.append('<td colspan="%d" class="note">חופפת ל-C1 ול-C2 — עמדה מותנית: רק כששתיהן ריקות (מטען כבד). לא נספרת כעמדה עצמאית.</td><td>—</td><td>—</td></tr>' % len(T)); continue
            for t in T: h.append(cell(s, t['m']))
            h.append('<td class="n">%d<small> (%d בעצירה של העמדה)</small></td><td>%s</td></tr>' % (q['n_ok'], q['n_now'], E(use_txt(s))))
    h.append('</tbody></table></div>'); return ''.join(h)
def types_table():
    h = ['<table class="tt"><thead><tr><th>הקוד</th><th>הסוג</th><th>אורך</th><th>מוטה</th><th>הגודל</th><th>כמה עמדות מקבלות</th></tr></thead><tbody>']
    for t in T:
        n = sum(1 for s in ST if s != 'CH' and ST[s]['row'][t['m']]['ok']); n0 = sum(1 for s in ST if s != 'CH' and ST[s]['row'][t['m']]['ok'] and not ST[s]['row'][t['m']]['shift'])
        h.append('<tr><td><b>%s</b></td><td>%s</td><td>%.1f מ׳</td><td>%.1f מ׳</td><td><i class="sw %s"></i>%s</td><td>%d (%d בעצירה של העמדה)</td></tr>' % (E(t['code']), E(t['he']), t['L'], t['W'], SZ[t['size']][1], E(SZ[t['size']][0].split(' — ')[0]), n, n0))
    h.append('</tbody></table>'); return ''.join(h)
def ga_section():
    ex = [s for s in ST if s != 'CH' and ST[s]['row']['AC-BJ-01']['ok'] and ST[s]['row']['AC-CN-01']['ok']]
    ex0 = [s for s in ex if not ST[s]['row']['AC-BJ-01']['shift']]
    pr = [s for s in ST if s != 'CH' and ST[s]['row']['AC-PR-01']['ok'] and ST[s]['row']['AC-LT-01']['ok']]
    h = ['<section><h2>פרטי ומנהלים — 2 סוגים פרטיים (PR, ‏LT) ו-2 סוגי מנהלים (BJ, ‏CN)</h2>']
    h.append('<p>%s</p>' % E('היום: עמדת מנהלים אחת בדרום — GA1 (בלוח: BJ של fieldfix). GA2–GA7 — רק פרטיים: האף ב-y 2028 כי דרך השירות TAIL_ROAD / GA_SPUR עוברת בתוך העמדות (D‑650), ומטוס מנהלים (14.4 מ׳) לא נכנס בין המסלול C לדרך. R3 מקבלת מנהלים ביום (בלילה — הרצת המנועים).'))
    h.append('<p>%s</p>' % E('מקבלות את שני סוגי המנהלים בעצירה של העמדה: %s. עם קו עצירה לסוג (המטוס עוצר אחורה): %s. מקבלות את שני הסוגים הפרטיים: %s.' % (', '.join(ex0), ', '.join(s for s in ex if s not in ex0), ', '.join(pr))))
    h.append('<p>%s</p>' % E('כמה צריך: בישן (S7F272, ‏1800 ש׳) — 3 נחיתות ו-2 המראות של מנהלים, 8 + 8 של פרטיים, על 5 עמדות GA (GA1, GA2, GA3, GA7, GA8). פי 2 — ~6 נחיתות מנהלים ב-1800 ש׳; עמדה אחת מחזיקה ~2.5 סבבים במחזור של 720 ש׳ (עמידה 240–260 ש׳) — כלומר 3 עמדות מנהלים נותנות פי 2 עם עתודה, ו-6 עמדות פרטיות.'))
    h.append('<ol><li>%s</li><li>%s</li><li>%s</li></ol>' % (
        E('נבנה (try6656, ‏074zt2_fc_stops.js): קו עצירה לכל סוג בכל עמדה — צבוע בצהוב עם קודי הסוגים, והנתונים S15D.stands[עמדה].stops למחולל. מכאן: מנהלים ב-GA1, ‏R1 (BJ / CN — 4 מ׳ אחורה, כך שהכנף לא מעל הכיס R1|R2; R1 ריקה היום בלוח) ו-R3 ביום → 3 עמדות מנהלים; פרטיים ב-GA2–GA7 (6). הטיסות עצמן — בלוח של fieldthru.'),
        E('השלב הבא (לאישורך): GA5–GA7 למנהלים — להזיז את TAIL_ROAD כ-5 מ׳ דרומה (y 2090–2134, בין קו האף החדש לכיסים של GA) כך שהאף ב-y 2079 → 6 עמדות מנהלים; צריך גם את הנסיעות של רכבי השירות על הדרך (fieldthru).'),
        E('ההרחבה הדרומית (H4) היא במים — עמדות שם רק עם מילוי ים ודרך הסעה שלא חוצה את R3; היום לא.')))
    h.append('</section>'); return ''.join(h)
def page():
    big = [s for s in ('P1', 'P6', 'C1') if s in ST]
    h = ['<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>העמדות והסוגים</title><style>%s</style></head><body><main>' % CSS]
    h.append('<header><h1>העמדות בשדה — כמה סוגי מטוסים נכנסים בכל עמדה</h1><p class="sub">fieldcalc · %s · מהגאומטריה של המשחק (S15D) ומהמדידה של השרוולים במשחק (q_bridges) · ציור SVG בקוד</p></header>' % E(NOW))
    n_used = sum(1 for s in ST if s != 'CH' and ST[s]['use'])
    h.append('<section class="kpi"><div><b>19</b><span>סימוני עמדה</span></div><div><b>18</b><span>עמדות עצמאיות (CH חופפת)</span></div><div><b>%d</b><span>עם טיסה בלוח היום</span></div><div><b>3</b><span>האנגרים (תחזוקה)</span></div><div><b>%d</b><span>סוגי מטוסים</span></div></section>' % (n_used, len(T)))
    h.append('<section><h2>המפה</h2><p>%s</p>%s<div class="fig">%s</div><h3>הדרום בהגדלה — פרטי, מנהלים והמרוחקות</h3><div class="fig">%s</div></section>' % (E('הצבע — הגודל המרבי שנכנס בעמדה; בתוך העמדה — כמה סוגים נכנסים ומי בלוח היום. העמדות הגדולות (%s) מקבלות גם בינוניים וקטנים: הקו העבה הוא קו העצירה של העמדה, הדקים — קווי עצירה לסוגים קטנים יותר (המטוס עוצר אחורה, כך שהכנף לא מעל כיס הציוד שליד האף).' % ', '.join(big)), legend(), svg_map(), svg_map(7180, 1860, 9600, 2580, .8)))
    h.append('<section><h2>עמדה × סוג</h2><p>%s</p>%s</section>' % (E('✓ — נכנס בקו העצירה של העמדה · ✓ +X מ׳ — נכנס בקו עצירה לסוג (X מטר אחורה) · ✗ — לא נכנס (העבר את העכבר / הקש על התא לסיבה). הבדיקה: המעטפת (מוטה × אורך) בתוך העמדה, לא על דרך שירות (חוץ מחצייה מסומנת), בלי כיס ציוד מתחת לגוף / לכנף / לזנב, 3 מ׳ (קלים — 2) מקצה הכנף של השכנים כשהם בסוג המתוכנן שלהם, ובעמדות השרוול — השרוול עוגן במשחק (רק בקו של העמדה; בקו אחר — מדרגות ואוטובוס). כל העמדות דורשות גרר לדחיפה לאחור (האף אל העמדה).'), table()))
    h.append('<section><h2>הסוגים</h2>%s</section>' % types_table())
    h.append(ga_section())
    unused = [s for s in ST if s != 'CH' and not ST[s]['use']]
    h.append('<section><h2>כל העמדות פעילות — מה חסר</h2><p>%s</p></section>' % E('בלוח היום (S15SIM + fieldfix + fieldthru) — %d עמדות עם טיסה; בלי טיסה: %s. הסיבות לפי fieldthru: P6 — ‏LG בו-זמנית עם P1 והכנף של NB / RJ על הכיס של PT-P6 (בטבלה: NB / RJ נכנסים ב-P6 בקו עצירה של 6–8 מ׳ אחורה); ‏R1 — הדחיפה עוברת על המטוס החונה של GA7 (לסוג קטן — מנהלים — הדחיפה קצרה); ‏R3 — הרצת המנועים בלילה (ביום פנויה); ‏GA5 / GA7 — אין חלון במסלול. הגאומטריה כאן — קווי העצירה לפי סוג — נמסרת ל-fieldthru (stands_matrix.json).' % (sum(1 for s in ST if s != 'CH' and ST[s]['use']), ', '.join(unused))))
    h.append('<footer>הנתונים: deliver/2026-11-17/fieldcalc/tools/stands_matrix.json (fc_stands.py — בדיקה עצמית: %s) · הכלי: fc_stands_page.py</footer></main></body></html>' % ('עוברת' if M['selftest'] else 'נכשלת'))
    return ''.join(h)
CSS = """:root{--bg:#f4f3ef;--card:#fff;--ink:#1c252c;--mut:#56616a;--line:#d6d2c6;--head:#e9e6dc;--ok:#1f7a3a;--ok2:#9a6a00;--bad:#b3261e;
--land:#dfe6d8;--apron:#cfd3d6;--twy:#9aa1a7;--rwy:#3c4248;--bld:#b8b1a4;--hgr:#c9c2b5;--s:#5aa469;--m:#3f7fc4;--l:#8e63c7;--xl:#c2571a;--none:#a7a7a7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15191d;--card:#1e2328;--ink:#e6e9ec;--mut:#a3adb6;--line:#343b42;--head:#262c32;--ok:#5cc27a;--ok2:#f0b54b;--bad:#ff7a6e;
--land:#24302a;--apron:#3a4045;--twy:#5d656c;--rwy:#0f1215;--bld:#5e584f;--hgr:#4d483f}}
:root[data-theme="dark"]{--bg:#15191d;--card:#1e2328;--ink:#e6e9ec;--mut:#a3adb6;--line:#343b42;--head:#262c32;--ok:#5cc27a;--ok2:#f0b54b;--bad:#ff7a6e;--land:#24302a;--apron:#3a4045;--twy:#5d656c;--rwy:#0f1215;--bld:#5e584f;--hgr:#4d483f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Arial,Helvetica,sans-serif;line-height:1.5}main{max-width:1280px;margin:0 auto;padding:16px}
h1{font-size:24px;margin:8px 0}h2{font-size:19px;margin:0 0 8px}.sub{color:var(--mut);margin:0 0 12px}section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:12px 0}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.kpi div{background:var(--head);border-radius:8px;padding:10px}.kpi b{font-size:26px;display:block}.kpi span{color:var(--mut);font-size:13px}
.fig{overflow-x:auto}.map{width:100%;min-width:760px;height:auto;display:block}
svg .land{fill:var(--land)}svg .apron{fill:var(--apron)}svg .twy{fill:var(--twy)}svg .rwy{fill:var(--rwy)}svg .bld{fill:var(--bld)}svg .hgr{fill:var(--hgr);stroke:var(--mut);stroke-width:3}
svg .hp{fill:none;stroke:#e9c46a;stroke-width:5}svg .st{fill-opacity:.28;stroke-width:6}svg .sz-s{fill:var(--s);stroke:var(--s)}svg .sz-m{fill:var(--m);stroke:var(--m)}svg .sz-l{fill:var(--l);stroke:var(--l)}svg .sz-xl{fill:var(--xl);stroke:var(--xl)}svg .sz-none{fill:var(--none);stroke:var(--none)}
svg .ch{fill:none;stroke-dasharray:24 14;stroke-width:4}svg .stop0{stroke:var(--ink);stroke-width:8}svg .stop1{stroke:var(--ink);stroke-width:3;opacity:.7}
h3{font-size:16px;margin:14px 0 6px}svg text{fill:var(--ink);font-family:Arial,Helvetica,sans-serif}svg .stl{font-size:52px;font-weight:bold}svg .stls{font-size:36px;font-weight:bold}svg .cnt{font-size:38px}svg .cnts{font-size:26px}svg .use{font-size:30px;fill:var(--ok)}svg .unused{font-size:28px;fill:var(--bad)}
svg .lbl{font-size:44px}svg .lbls{font-size:28px}svg .nArrow line{stroke:var(--ink);stroke-width:8}svg .nArrow text{font-size:36px}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin:6px 0 10px;font-size:14px}.legend span{display:inline-flex;align-items:center;gap:6px}
.sw{display:inline-block;width:16px;height:16px;border-radius:3px;opacity:.85}.sw.sz-s{background:var(--s)}.sw.sz-m{background:var(--m)}.sw.sz-l{background:var(--l)}.sw.sz-xl{background:var(--xl)}.sw.sz-none{background:var(--none)}
.ln0,.ln1{display:inline-block;width:22px;border-top:4px solid var(--ink)}.ln1{border-top-width:2px;opacity:.7}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid var(--line);padding:4px 6px;text-align:center;vertical-align:middle}thead th{background:var(--head);position:sticky;top:0}
thead th small{display:block;font-weight:normal;color:var(--mut);font-size:11px;white-space:nowrap}thead th.sz-s{border-top:5px solid var(--s)}thead th.sz-m{border-top:5px solid var(--m)}thead th.sz-l{border-top:5px solid var(--l)}thead th.sz-xl{border-top:5px solid var(--xl)}
td.ok{color:var(--ok);font-weight:bold}td.ok2{color:var(--ok2);font-weight:bold;white-space:nowrap}td.no{color:var(--bad)}td.n{font-weight:bold}td.n small{font-weight:normal;color:var(--mut)}td.note{text-align:right;color:var(--mut)}
tr.grp td{background:var(--head);text-align:right;font-weight:bold}tbody th{background:var(--head)}.tt td:nth-child(2){text-align:right}footer{color:var(--mut);font-size:12px;margin:12px 0}
@media (max-width:600px){main{padding:8px 16px}h1{font-size:20px}}"""
if __name__ == '__main__':
    doc = page(); p = os.path.join(OUT, 'Stands_matrix.html'); open(p, 'w', encoding='utf-8').write(doc)
    b = doc.encode('utf-8'); print(p, len(b), 'בתים · sha1', hashlib.sha1(b).hexdigest()[:12], '· data:image', doc.count('data:image'), '· <img', doc.count('<img'))
