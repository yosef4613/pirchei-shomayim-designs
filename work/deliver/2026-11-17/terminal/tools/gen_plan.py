#!/usr/bin/env python3
# gen_plan.py — terminal 17.11: הציור (כלל 13) — אולם המזוודות, שרשרת המסועים, הקצה המזרחי והשאטל. SVG בקוד, בלי תמונות.
# node/python: python3 gen_plan.py → ../Terminal_plan.html
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, 's15j_L.json'), encoding='utf-8'))
D = json.load(open(os.path.join(HERE, 's15d.json'), encoding='utf-8'))
G = json.load(open(os.path.join(HERE, 'term_geo.json'), encoding='utf-8'))   # הגאומטריה החדשה — אותו קובץ נכנס למשחק (074zx_terminal.js)
OUT = os.path.join(os.path.dirname(HERE), 'Terminal_plan.html')

def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def rect(r, cls='', extra=''): return f'<rect x="{r[0]}" y="{r[1]}" width="{r[2]-r[0]}" height="{r[3]-r[1]}" class="{cls}" {extra}/>'
def pl(P, cls='', extra=''): return '<polyline points="' + ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in P) + f'" class="{cls}" {extra}/>'
def txt(x, y, s, cls='t', extra=''): return f'<text x="{x}" y="{y}" class="{cls}" {extra}>{esc(s)}</text>'
def loop_pts(c, pad=0, n=14):
    cx, y0, y1, r = c['cx'], c['y0'], c['y1'], c['r'] + pad
    P = [[cx + r, y0], [cx + r, y1]]
    for k in range(1, n): a = math.pi * k / n; P.append([cx + r * math.cos(a), y1 + r * math.sin(a)])
    P += [[cx - r, y1], [cx - r, y0]]
    for k in range(1, n): a = math.pi + math.pi * k / n; P.append([cx + r * math.cos(a), y0 + r * math.sin(a)])
    P.append([cx + r, y0]); return P
def arrow_marks(P, every=60, cls='arw'):
    out = []; acc = 0
    for i in range(1, len(P)):
        a, b = P[i - 1], P[i]; l = math.hypot(b[0] - a[0], b[1] - a[1])
        if l < 1e-6: continue
        s = every - acc
        while s < l:
            x = a[0] + (b[0] - a[0]) * s / l; y = a[1] + (b[1] - a[1]) * s / l; ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            out.append(f'<path d="M-3,-2.4 L2.6,0 L-3,2.4 Z" class="{cls}" transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f})"/>'); s += every
        acc = (acc + l) % every
    return ''.join(out)

CAR = G['carousels']; CH = G['chain']; SH = G['shuttle']; EAST = G['east']

# ------------------------------------------------------------ ציור 1: השרשרת — מהעמדות של הכבודה אל 3 המסועים
def fig_chain():
    X0, Y0, X1, Y1 = 6790, 872, 8540, 1196
    s = [f'<svg viewBox="{X0} {Y0} {X1-X0} {Y1-Y0}" role="img" aria-label="שרשרת המסועים">']
    s.append(rect([X0, Y0, X1, 886], 'apron'))
    s.append(rect(L['bld']['CW']['r'], 'core')); s.append(rect(L['bld']['CC']['r'], 'core')); s.append(rect(L['bld']['CE']['r'], 'core'))
    s.append(rect(L['bld']['TW']['r'], 'termb')); s.append(rect([L['bld']['TE']['r'][0], 1033, X1, 1210], 'termb')); s.append(rect([6790, 1033, 7222, 1180], 'termb'))
    s.append(rect(L['pass'], 'road')); s.append(txt(7909, 1150, 'המעבר (כביש)', 'tm', 'transform="rotate(-90 7909 1150)"'))
    for z in L['zones']:
        if z[0].startswith('G-'): s.append(rect(z[2], 'gate'))
    for k, r in L['bagHalls'].items():
        rr = r if k != 'BH-5' else [8314, 905, 8505, 961]
        s.append(rect(rr, 'hall')); s.append(txt((rr[0] + rr[2]) / 2, rr[1] + 12, k, 'tb'))
    # המסועים של היום בתוך העמדות (מיון + אל הקרוסלה) — אפור
    for h in CH['halls']:
        s.append(pl(h['belt'], 'beltold')); s.append(pl(h['toCar'], 'beltold'))
        if h.get('cut'): x, y = h['toCar'][-1]; s.append(f'<g class="cut"><line x1="{x-6}" y1="{y-6}" x2="{x+6}" y2="{y+6}"/><line x1="{x-6}" y1="{y+6}" x2="{x+6}" y2="{y-6}"/></g>')
    # החדש: המחברים (מתחת לרצפת השערים — מקווקו כהה; מעל המעבר — גשר)
    for c in CH['lines']:
        s.append(pl(c['pts'], 'beltnew')); s.append(arrow_marks(c['pts'], 46))
    br = CH['bridge']; s.append(rect(br['r'], 'bridge')); s.append(txt((br['r'][0] + br['r'][2]) / 2, br['r'][1] - 4, 'גשר מסוע מעל המעבר', 'tm'))
    for c in CAR:
        s.append(pl(loop_pts(c, 4), 'carout')); s.append(pl(loop_pts(c), 'carin')); s.append(pl(c['feed'], 'beltnew'))
        s.append(txt(c['cx'], c['y1'] + 30, c['id'], 'tb'))
    s.append(txt(7600, 1172, 'אולם המזוודות (TW-BAG) — 3 מסועים', 'tm'))
    s.append(txt(7030, 1110, 'ביקורת גבולות / מכס ←', 'tm')); s.append(txt(8250, 1120, 'אגף מזרח', 'tm'))
    s.append(txt(6900, 900, 'הרחבה (P1–P6)', 'tm'))
    s.append('</svg>')
    return ''.join(s)

# ------------------------------------------------------------ ציור 2: אולם המזוודות — 3 מסועים מאורכים, לוח לכל אחד
def fig_hall():
    X0, Y0, X1, Y1 = 7380, 1000, 7870, 1186
    s = [f'<svg viewBox="{X0} {Y0} {X1-X0} {Y1-Y0}" role="img" aria-label="אולם המזוודות">']
    s.append(rect([X0, Y0, X1, 1033], 'core')); s.append(rect([X0, 1033, 7865, 1180], 'termb2'))
    s.append(f'<line x1="{X0}" y1="1033" x2="7865" y2="1033" class="wall"/>')
    for x, y in L['cols']:
        if X0 < x < X1 and y > 1033: s.append(rect([x - 3.5, y - 3.5, x + 3.5, y + 3.5], 'col'))
    for it in L['items']:
        if it['k'] == 'trolleys': s.append(rect(it['r'], 'troll')); s.append(txt((it['r'][0] + it['r'][2]) / 2, it['r'][3] + 8, 'עגלות', 'ts'))
        if it['k'] == 'counter' and it['r'][0] > 7700: s.append(rect(it['r'], 'desk')); s.append(txt(it['r'][0] - 2, it['r'][1] + 6, 'אבידות', 'ts', 'text-anchor="end"'))
        if it['k'] == 'wc' and it['r'][0] > 7700: s.append(rect(it['r'], 'wc')); s.append(txt((it['r'][0] + it['r'][2]) / 2, 1146, 'שירותים', 'ts'))
    # המחברים שמגיעים מקומת הרחבה (מתחת לרצפת השערים)
    for c in CH['lines']:
        P = [p for p in c['pts'] if X0 - 200 < p[0] < X1 + 200]
        s.append(pl(c['pts'], 'beltnew thin', f'clip-path="url(#clipH)"'))
    for c in CAR:
        s.append(pl(loop_pts(c, 4), 'carout')); s.append(pl(loop_pts(c, -4), 'carplate')); s.append(rect([c['cx'] - c['spine'], c['y0'], c['cx'] + c['spine'], c['y1']], 'spine'))
        s.append(arrow_marks(loop_pts(c), 22, 'arw2')); s.append(pl(c['feed'], 'feed'))
        # הלוח על הקיר מעל ההזנה
        bx, by = c['board']
        s.append(rect([bx - 42, by - 30, bx + 42, by - 2], 'board')); s.append(txt(bx, by - 23, c['id'] + ' · מזוודות', 'tbd'))
        for i, row in enumerate(c['sample']): s.append(txt(bx + 39, by - 15.5 + i * 5.4, row, 'tbr'))
        for sp in c['spots']: s.append(f'<circle cx="{sp[0]}" cy="{sp[1]}" r="2.2" class="pax"/>')
    s.append(pl(G['walk']['claim'], 'walk')); s.append(arrow_marks(G['walk']['claim'], 40, 'arw3'))
    s.append(txt(7425, 1084, 'מביקורת הגבולות', 'ts', 'text-anchor="start"')); s.append(txt(7425, 1176, '→ המכס והיציאה (מערבה)', 'ts', 'text-anchor="start"'))
    s.append('<defs><clipPath id="clipH"><rect x="7380" y="1000" width="490" height="60"/></clipPath></defs>')
    s.append('</svg>')
    return ''.join(s)

# ------------------------------------------------------------ ציור 3: הקצה המזרחי — הישיבה, הלוח, תחנת השאטל
def fig_east():
    X0, Y0, X1, Y1 = 8600, 1030, 9220, 1320
    s = [f'<svg viewBox="{X0} {Y0} {X1-X0} {Y1-Y0}" role="img" aria-label="הקצה המזרחי">']
    s.append(rect([X0, 1033, 9163, 1210], 'termb2')); s.append(rect([X0, 1210, X1, 1320], 'apron'))
    for sv in D['service']:
        if sv['id'] in ('AIR-BASE_ST', 'AIR-BASE_E'): s.append(rect(sv['rect'], 'road'))
    s.append(f'<line x1="{X0}" y1="1210" x2="9163" y2="1210" class="wall"/><line x1="9163" y1="1033" x2="9163" y2="1210" class="wall"/>')
    for z in L['zones']:
        if z[2][0] >= 8470 and z[2][1] > 1030 and z[2][0] < X1: s.append(rect(z[2], 'zone')); s.append(txt((z[2][0] + z[2][2]) / 2, z[2][1] + 9, z[1].split(' — ')[0], 'ts'))
    for it in L['items']:
        if it['k'] == 'shop' and it['r'][0] > 8600: s.append(rect(it['r'], 'shop')); s.append(txt((it['r'][0] + it['r'][2]) / 2, (it['r'][1] + it['r'][3]) / 2 + 2, it['name'], 'ts'))
        if it['k'] == 'seats' and it['x0'] > 8600:
            s.append(f'<line x1="{it["x0"]}" y1="{it["y"]}" x2="{it["x1"]}" y2="{it["y"]}" class="seat"/>')
    for row in EAST['newRows']:
        s.append(f'<line x1="{row["x0"]}" y1="{row["y"]}" x2="{row["x1"]}" y2="{row["y"]}" class="seatnew"/>')
    b = EAST['board']; s.append(rect([b[0] - b[2] / 2 - 10, b[1] - 26, b[0] + b[2] / 2 + 10, b[1] - 2], 'board'))
    s.append(txt(b[0], b[1] - 16, 'הסעה לעמדות המרוחקות', 'tbd'))
    for i, row in enumerate(EAST['boardSample']): s.append(txt(b[0] + b[2] / 2 + 7, b[1] - 10 + i * 5.2, row, 'tbr'))
    dr = EAST['door']; s.append(rect([dr[0], 1206, dr[1], 1214], 'door')); s.append(txt((dr[0] + dr[1]) / 2, 1203, 'DB', 'ts'))
    st = SH['stop']; s.append(rect(st['shelter'], 'shelter')); s.append(txt((st['shelter'][0] + st['shelter'][2]) / 2, st['shelter'][3] + 8, 'תחנת השאטל · גג שקוף', 'ts'))
    bx, by = st['bus']; s.append(rect([bx - 62, by - 14, bx + 62, by + 14], 'bus')); s.append(txt(bx, by + 3, 'AB-R2 (עולים) / AB-R1 (נוחתים)', 'tbw'))
    s.append(pl(G['walk']['east'], 'walk')); s.append(arrow_marks(G['walk']['east'], 30, 'arw3'))
    for q in st['queue']: s.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="2.4" class="pax"/>')
    s.append(txt(9190, 1300, '↓ אל AIR-BASE_E', 'ts'))
    s.append('</svg>')
    return ''.join(s)

# ------------------------------------------------------------ ציור 4: הלולאה של השאטל בצד האוויר
def fig_route():
    X0, Y0, X1, Y1 = 7780, 1180, 9620, 2560
    s = [f'<svg viewBox="{X0} {Y0} {X1-X0} {Y1-Y0}" role="img" aria-label="מסלול השאטל">']
    s.append(rect([X0, Y0, X1, Y1], 'apron'))
    s.append(rect(D['twc'], 'twy')); s.append(txt(8600, 1860, 'מסלול הסעה C', 'tw'))
    s.append(rect(D['twb'], 'twy'))
    s.append(rect([7953, 1180, 9163, 1210], 'termb')); s.append(txt(8560, 1200, 'הטרמינל — אגף מזרח', 'tm'))
    for bse in D['base']: s.append(rect(bse['rect'], 'bld')); s.append(txt((bse['rect'][0] + bse['rect'][2]) / 2, (bse['rect'][1] + bse['rect'][3]) / 2, bse['label'].split(' — ')[0], 'ts'))
    for sv in D['service']:
        r = sv['rect']
        if r[0] > 7700 and r[1] > 1100: s.append(rect(r, 'road'))
    for k in ('R1', 'R2', 'R3'):
        r = D['stands'][k]['rect']; s.append(rect(r, 'stand')); s.append(txt((r[0] + r[2]) / 2, r[1] + 90, k, 'tb'))
    s.append(pl(SH['loop'], 'route')); s.append(arrow_marks(SH['loop'], 140, 'arw4'))
    st = SH['stop']['bus']; s.append(f'<circle cx="{st[0]}" cy="{st[1]}" r="16" class="stopc"/>'); s.append(txt(st[0], st[1] - 22, 'תחנת השאטל (DB)', 'tb'))
    for k, p in SH['standStops'].items(): s.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="16" class="stopc"/>'); s.append(txt(p[0] - 60, p[1] + 40, 'השאטל ליד ' + k, 'tb'))
    s.append(f'<circle cx="7982" cy="1585" r="14" class="stopc"/>'); s.append(txt(7982, 1570, 'AB-R2 בבסיס 8', 'tb'))
    s.append(f'<circle cx="8791" cy="2522" r="14" class="stopc"/>'); s.append(txt(8700, 2540, 'AB-R1 בכיס', 'tb'))
    for x in SH['crossings']: s.append(f'<circle cx="{x[0]}" cy="{x[1]}" r="12" class="xc"/>'); s.append(txt(x[0] + (40 if x[0] > 9000 else -40), x[1], x[2], 'ts'))
    s.append('</svg>')
    return ''.join(s)

CSS = '''
:root{--bg:#f6f4ef;--fg:#1d2329;--mut:#5b6670;--card:#fff;--line:#d9d4c8;--apron:#d9d7d1;--core:#e6e1d6;--term:#efeae0;--gate:#dfe6ee;--hall:#cfc8bb;--road:#7d8287;--old:#8d959b;--new:#e0772b;--board:#10161e;--pax:#2f6fd0;--seat:#7a8a9c;--seatnew:#e0772b;--route:#d2462f;--twy:#b9b6ae;--bld:#c9ccd0;--stand:#e8e6e0}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16191d;--fg:#e6e8ea;--mut:#9aa3ab;--card:#1f2327;--line:#353b41;--apron:#33363a;--core:#2c2f33;--term:#2a2d30;--gate:#2b3440;--hall:#3a3833;--road:#55595e;--old:#7d858b;--twy:#45474a;--bld:#3c4045;--stand:#2e3134}}
:root[data-theme="dark"]{--bg:#16191d;--fg:#e6e8ea;--mut:#9aa3ab;--card:#1f2327;--line:#353b41;--apron:#33363a;--core:#2c2f33;--term:#2a2d30;--gate:#2b3440;--hall:#3a3833;--road:#55595e;--old:#7d858b;--twy:#45474a;--bld:#3c4045;--stand:#2e3134}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Segoe UI",Arial,sans-serif}
main{max-width:1080px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:4px 0}h2{font-size:17px;margin:24px 0 8px}p{margin:6px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;margin:10px 0}
.find{border-inline-start:4px solid var(--new)}
ul{margin:4px 0;padding-inline-start:20px}li{margin:3px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}td,th{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}th{color:var(--mut);font-weight:600}
.tw{overflow-x:auto}
svg{width:100%;height:auto;display:block}
.apron{fill:var(--apron)}.core{fill:var(--core)}.termb{fill:var(--term);stroke:var(--line)}.termb2{fill:var(--term)}.gate{fill:var(--gate)}.hall{fill:var(--hall);stroke:#9a9384;stroke-width:.8}
.road{fill:var(--road);opacity:.55}.twy{fill:var(--twy)}.bld{fill:var(--bld);stroke:var(--line)}.stand{fill:var(--stand);stroke:var(--line);stroke-dasharray:6 4}.zone{fill:none;stroke:var(--line);stroke-dasharray:3 2}
.wall{stroke:var(--fg);stroke-width:1.6}.col{fill:var(--mut)}
.beltold{fill:none;stroke:var(--old);stroke-width:5}.beltnew{fill:none;stroke:var(--new);stroke-width:5;stroke-linejoin:round}.beltnew.thin{stroke-width:4;opacity:.8}
.feed{fill:none;stroke:var(--new);stroke-width:4}.cut line{stroke:#d22;stroke-width:2.4}
.bridge{fill:none;stroke:var(--new);stroke-width:2;stroke-dasharray:4 2}
.carout{fill:#8d959b;stroke:#5d666c;stroke-width:1}.carin{fill:none;stroke:var(--new);stroke-width:2}.carplate{fill:#c3c9ce;stroke:none}.spine{fill:#3d4448}
.arw{fill:#fff}.arw2{fill:#e0772b}.arw3{fill:var(--pax)}.arw4{fill:var(--route)}
.board{fill:var(--board);stroke:#5e6b78;stroke-width:.6}
.pax{fill:var(--pax)}.walk{fill:none;stroke:var(--pax);stroke-width:1.4;stroke-dasharray:3 2}
.troll{fill:#b9c4cf}.desk{fill:#5a6b7c}.wc{fill:#dfe7ea;stroke:var(--line)}.shop{fill:#efe2cc;stroke:var(--line)}
.seat{stroke:var(--seat);stroke-width:3.2}.seatnew{stroke:var(--seatnew);stroke-width:3.2}
.door{fill:#e8b92b}.shelter{fill:rgba(140,190,225,.35);stroke:#6aa0c8;stroke-width:.8}.bus{fill:#f2f2ee;stroke:#2f6fd0;stroke-width:1.6}
.route{fill:none;stroke:var(--route);stroke-width:7;stroke-linejoin:round;opacity:.85}.stopc{fill:none;stroke:var(--route);stroke-width:4}.xc{fill:#ffd25a;stroke:#8a6a00;stroke-width:2}
text{fill:var(--fg);font-family:system-ui,Arial,sans-serif}
.t{font-size:10px}.tb{font-size:11px;font-weight:700;text-anchor:middle}.tm{font-size:9px;text-anchor:middle;fill:var(--mut)}.ts{font-size:6.4px;text-anchor:middle;fill:var(--mut)}
.tbd{font-size:5px;font-weight:700;text-anchor:middle;fill:#ffd25a}.tbr{font-size:3.9px;text-anchor:end;fill:#f2f4f7}.tbw{font-size:9px;font-weight:700;text-anchor:middle;fill:#13294b}.tw{font-size:22px;text-anchor:middle;fill:var(--mut)}
#fr svg .tb{font-size:30px}#fr svg .ts{font-size:20px}#fr svg .tm{font-size:24px}
.leg span{display:inline-block;width:22px;height:6px;border-radius:2px;vertical-align:middle;margin-inline-end:6px}
'''

def page():
    F = G['found']
    h = ['<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>הטרמינל: מזוודות ושאטל</title><style>' + CSS + '</style></head><body><main>']
    h.append('<h1>הטרמינל — אולם המזוודות, שרשרת המסועים, הקצה המזרחי והשאטל</h1>')
    h.append('<p style="color:var(--mut)">17.11 · הציור לפני הבנייה (כלל 13) · הכול מצויר בקוד · הבסיס: S7F302</p>')
    h.append('<div class="card find"><b>מה מצאתי במשחק היום</b><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in F) + '</ul></div>')
    h.append('<h2>1 · השרשרת: מכל עמדת כבודה אל אחד מ-3 המסועים</h2>')
    h.append('<p>אפור — המסועים של היום בתוך העמדות; ✕ אדום — המקום שבו המסוע נגמר היום. כתום — החדש: תעלת מסוע מכוסה בקומת הרחבה (מתחת לרצפת השערים), גשר מסוע מעל המעבר, וההזנה מהקיר אל המסוע באולם. כל מזוודה נוסעת על הקו הזה בזמן אמת — בלי קפיצה.</p>')
    h.append('<div class="card">' + fig_chain() + '</div>')
    h.append('<div class="card tw"><table><tr><th>המסוע באולם</th><th>מאיפה מגיעות המזוודות</th><th>הטיסות (לפי העמדה של הרכבת)</th><th>הדרך</th></tr>' +
             ''.join(f'<tr><td>{esc(c["id"])}</td><td>{esc(" · ".join(c["from"]))}</td><td>{esc(c["stands"])}</td><td>{esc(c["path"])}</td></tr>' for c in CAR) + '</table></div>')
    h.append('<h2>2 · אולם המזוודות: 3 מסועים מאורכים, לוח לכל אחד</h2>')
    h.append('<p>כל מסוע — לולאה סביב שורה: המזוודות יורדות מההזנה בקיר אל הצד המזרחי, נוסעות דרומה, מסתובבות בקצה וחוזרות צפונה בצד המערבי. הנוסעים עומדים משני הצדדים. מעל ההזנה — לוח "מזוודות" של המסוע: מספר המסוע, הטיסות, מאיפה, והמצב (בדרך / על הסרט / הסתיים). נוסע הולך רק למסוע שבלוח של הטיסה שלו, ולוקח את המזוודה שלו (באותו צבע) כשהיא עוברת לידו.</p>')
    h.append('<div class="card">' + fig_hall() + '</div>')
    h.append('<h2>3 · הקצה המזרחי של הטרמינל: עוד ישיבה, לוח לעמדות המרוחקות, תחנת שאטל</h2>')
    h.append('<p>' + esc(EAST['text']) + '</p>')
    h.append('<div class="card">' + fig_east() + '</div>')
    h.append('<h2>4 · השאטל בצד האוויר — לולאה חד-סטרית, בלי לחצות מסלול</h2>')
    h.append('<p>' + esc(SH['text']) + '</p>')
    h.append('<div class="card" id="fr">' + fig_route() + '</div>')
    h.append('<div class="card tw"><table><tr><th>#</th><th>מה קורה</th><th>מי</th></tr>' + ''.join(f'<tr><td>{i+1}</td><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for i, (a, b) in enumerate(SH['steps'])) + '</table></div>')
    h.append('<h2>5 · מה משתנה, ובאיזה קובץ</h2><div class="card tw"><table><tr><th>מה</th><th>איפה</th></tr>' + ''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in G['files']) + '</table></div>')
    h.append('<h2>6 · הבדיקה</h2><div class="card"><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in G['tests']) + '</ul></div>')
    h.append('<h2>7 · לאישורך (ברירת המחדל שנבחרה)</h2><div class="card"><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in G['ask']) + '</ul></div>')
    h.append('</main></body></html>')
    return '\n'.join(h)

if __name__ == '__main__':
    html = page(); open(OUT, 'w', encoding='utf-8').write(html)
    print(OUT, len(html.encode('utf-8')), 'בתים', 'data:image' in html, '<img' in html)
