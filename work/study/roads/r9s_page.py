# -*- coding: utf-8 -*-
"""8.11 · סבב 9ס — הדף: אותו דף של הסבבים הקודמים (city_plan.html של 9נ2), עם השינויים של הסבב:
הכותרות מהשדה version, השכבות שבראש הדף (המגרשים, הדרכים, המסילות, הצינור, השלבים) — כך שכל המפות בדף מתעדכנות יחד, הריחוף, טבלאות הקווים,
ציורי השלבים S14–S16, שורת "מעודכן עד" בכל ציור, והסעיף של סבב 9ס עם טבלת ההתאמה. בלי צילומים — כל ציור ב-SVG."""
import json, re, html, math, time
from collections import Counter, defaultdict
E = html.escape
ASK = 'לאישורך'


STG = [f'S{i}' for i in range(1, 17)]
COL = dict(zip(STG, ['#f1ce63', '#fabfd2', '#59a14f', '#ffbe7d', '#bab0ac', '#79706e', '#ff9d9a', '#d7b5a6',
                     '#9d7660', '#86bcb6', '#b6992d', '#8cd17d', '#d37295', '#4e79a7', '#f28e2b', '#b07aa1']))   # the colours of the stages — as in round 9נ2


def f1(v): return f"{v:.0f}" if abs(v - round(v)) < .05 else f"{v:.1f}"


def span(H, gid, start=0):
    i = H.index(f"<g id='{gid}'", start); d = 0
    for m in re.finditer(r"<g[ >]|</g>", H[i:]):
        if m.group(0).startswith('<g'): d += 1
        else:
            d -= 1
            if d == 0: return i, i + m.end()
    raise ValueError(gid)


def one(H, old, new, n=1):
    assert H.count(old) == n, (old[:120], H.count(old)); return H.replace(old, new)


def rect_re(r):
    x0, y0, x1, y1 = r
    return re.compile(r"<rect x='%s' y='%s' width='%s' height='%s'[^>]*/>" % tuple(re.escape(f1(v)) for v in (x0, y0, x1 - x0, y1 - y0)))


SFILL = {'building': '#8e9aa8', 'parking': '#d6dade', 'drop': '#d6dade', 'svc': '#cfd2d6', 'water': '#7fb3d9', 'island': '#9cbf86', 'court': '#e8b48a',
         'pier': '#8b6b4a', 'park': '#a8d59a'}


# ---------------------------------------------------------------------- the layers at the top of the page (every map uses them)
def layers(H, P, G, info):
    built = lambda l: (l.get('status') or {}).get('state', '').startswith('קיים')
    # a · the lots: the replaced ones out of the drawing (they stay in the data, marked), the hatch of "future" off every lot that is built
    a, b = span(H, 'lots'); L = H[a:b]; a7, b7 = span(H, 'r7'); R7 = H[a7:b7]
    gone = fut = 0
    for l in P['lots'] + P['r7']['items'] + P['sites']:
        r = l.get('rect')
        if not (isinstance(r, list) and len(r) == 4 and all(isinstance(t, (int, float)) for t in r)): continue
        st = (l.get('status') or {}).get('state', '')
        rx = rect_re(r)
        if st == 'הוחלף':
            L, k1 = rx.subn('', L); R7, k2 = rx.subn('', R7); gone += k1 + k2
        elif built(l) or st.startswith('קיים באזור'):
            fx = re.compile(rx.pattern.replace("[^>]*/>", r"[^>]*class='fut'[^>]*/>"))
            L, k1 = fx.subn('', L); R7, k2 = fx.subn('', R7); fut += k1 + k2
    # b · the zones as built in the game, from the game: D2 (D‑496), B2 and B1 (the lake, the piers, the golf)
    o = ["<g id='r9s-built'>"]
    lk = P['terrain']['lake_game']['pts']
    o.append(f"<polygon points='{' '.join(f'{f1(x)},{f1(y)}' for x, y in lk)}' fill='#a9cfe8' stroke='#5b8db5' stroke-width='5'/>")
    for l in P.get('r9s_lots', []):
        r = l['rect']; fill = SFILL.get(l['kind'], '#d6dade')
        if l.get('parts'):
            for q in l['parts']: o.append(f"<rect x='{f1(q[0])}' y='{f1(q[1])}' width='{f1(q[2] - q[0])}' height='{f1(q[3] - q[1])}' fill='{fill}' stroke='#5a4330' stroke-width='3'/>")
        else:
            o.append(f"<rect x='{f1(r[0])}' y='{f1(r[1])}' width='{f1(r[2] - r[0])}' height='{f1(r[3] - r[1])}' fill='{fill}' stroke='#556' stroke-width='{4 if l['kind'] == 'building' else 3}'/>")
    for d in P.get('r9s_driveways', []):
        r = d['rect']; o.append(f"<rect x='{f1(r[0])}' y='{f1(r[1])}' width='{f1(r[2] - r[0])}' height='{f1(r[3] - r[1])}' fill='#ebebe7' stroke='#8a867c' stroke-width='3'/>")
    B = G['B12']
    for n, x0, y0, x1, y1, _ in B['holes']:
        o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='#7fbf6a' stroke='#4c7a3b' stroke-width='2'/><text x='{(x0 + x1) / 2:.0f}' y='{(y0 + y1) / 2 + 9:.0f}' class='r9h'>{n}</text>")
    o.append("</g>")
    L = L[:-4] + ''.join(o) + '</g>'
    H = H[:a7] + R7 + H[b7:]; a, b = span(H, 'lots'); H = H[:a] + L + H[b:]
    info.update(lots_out=gone, fut_off=fut)
    # c · the road of 09:07 (D2-LCH), in the three passes of the network
    segs = [s for s in P['segments'] if s['road'] == 'D2-LCH']
    pb = ''.join(f"<g id='b-{s['id'].replace('/', '-')}'><polyline points='{' '.join(f'{f1(x)},{f1(y)}' for x, y in s['pts'])}' class='rk' stroke='#6f6b62' stroke-width='94'/>"
                 f"<polyline points='{' '.join(f'{f1(x)},{f1(y)}' for x, y in s['pts'])}' class='rk' stroke='#e2ded3' stroke-width='90'/></g>" for s in segs)
    pc = ''.join(f"<g id='c-{s['id'].replace('/', '-')}'><polyline points='{' '.join(f'{f1(x)},{f1(y)}' for x, y in s['pts'])}' class='rk' stroke='#ffffff' stroke-width='70'/></g>" for s in segs)
    pl = ''.join(f"<g id='l-{s['id'].replace('/', '-')}'><polyline points='{' '.join(f'{f1(x)},{f1(y)}' for x, y in s['pts'])}' class='ln' stroke='#8f8f8f'/></g>" for s in segs)
    for gid, add in (('rdb', pb), ('rdc', pc), ('rdl', pl)):
        a, b = span(H, gid); H = H[:b - 4] + add + H[b - 4:]
    # d · the ends of the villas' streets, where the game has them (E31_23, E39_19)
    for n in P['nodes']:
        if n.get('at_was'):
            ox, oy = n['at_was']; nx, ny = n['x'], n['y']
            for s in P['segments']:
                if s['a'] == n['id'] or s['b'] == n['id']:
                    for pre in ('b-', 'c-', 'l-'):
                        a, b = span(H, pre + s['id'].replace('/', '-')); g = H[a:b]
                        g2 = g.replace(f"{f1(ox)},{f1(oy)}", f"{f1(nx)},{f1(ny)}").replace(f"cx='{f1(ox)}' cy='{f1(oy)}'", f"cx='{f1(nx)}' cy='{f1(ny)}'")
                        H = H[:a] + g2 + H[b:]
            a, b = span(H, 'jx'); g = H[a:b].replace(f"cx='{f1(ox)}' cy='{f1(oy)}'", f"cx='{f1(nx)}' cy='{f1(ny)}'"); H = H[:a] + g + H[b:]
            H = H.replace(f"translate({f1(ox)} {f1(oy)})'><g class='s'><use href='#ic-", f"translate({f1(nx)} {f1(ny)})'><g class='s'><use href='#ic-")
    # e · שדרת הקריה ends at A3W (60, 2550); the aisle of the car park A3-P
    for gid in ('b-s-A3-SPORTS-RD', 'c-s-A3-SPORTS-RD', 'l-s-A3-SPORTS-RD'):
        a, b = span(H, gid); g = H[a:b].replace("1164,2550 115,2550 115,1760", "1164,2550 60,2550"); H = H[:a] + g + H[b:]
    a, b = span(H, 'l-s-A3-SPORTS-RD')
    H = H[:b - 4] + "<line x1='1000' y1='2515' x2='1000' y2='2585' class='zeb' stroke='#c4c4c4' stroke-width='40'/>" + H[b - 4:]   # the west arm of the sports roundabout
    a, b = span(H, 'rds'); H = H[:b - 4] + ("<g id='sx-A3-P-AISLE'><polyline points='115,2482 115,1760' class='rk' stroke='#c9ccd0' stroke-width='60' stroke-dasharray='30 18'/></g>") + H[b - 4:]
    # f · J18_16, the arm of רחוב השכונה: the crossing 8.5 m from the junction (as in the game); J385_42 on AR-S/3 — as in the game
    H = one(H, "<line x1='1835' y1='1743' x2='1765' y2='1743' class='zeb' stroke='#c4c4c4' stroke-width='40'/>", "<line x1='1835' y1='1685' x2='1765' y2='1685' class='zeb' stroke='#c4c4c4' stroke-width='40'/>")
    c = next(x for x in P['bus']['crosswalks'] if x['node'] == 'J385_42' and x['seg'] == 'AR-S/3')
    xm = c['at'][0] + c['u'][0] * (c['d0'] + c['d1']) / 2
    H = one(H, "<line x1='3939' y1='4166' x2='3939' y2='4334' class='zeb' stroke='#ffffff' stroke-width='40'/>", f"<line x1='{f1(xm)}' y1='4166' x2='{f1(xm)}' y2='4334' class='zeb' stroke='#ffffff' stroke-width='40'/>")
    # g · J18_25 — a signal (every view draws its own icon)
    k = H.count("translate(1800 2550)'><g class='s'><use href='#ic-stop'/>"); H = H.replace("translate(1800 2550)'><g class='s'><use href='#ic-stop'/>", "translate(1800 2550)'><g class='s'><use href='#ic-signal'/>")
    info['j1825_icons'] = k
    # h · the rails: REF-SPUR cancelled (grey, dashed, with its label), the platforms of E3 (D‑505), the pipe PIPE-REF (a new layer)
    a, b = span(H, 'rails'); R = H[a:b]
    rs = next(r for r in P['rails'] if r['id'] == 'REF-SPUR'); pp = ' '.join(f'{f1(x)},{f1(y)}' for x, y in (p[:2] for p in rs['pts']))
    n_rs = R.count(f"points='{pp}'")
    R = re.sub(r"<polyline points='%s'[^>]*/>" % re.escape(pp), '', R)
    R = R.replace("<rect x='5736' y='1850' width='38' height='440'", "<rect x='5736' y='1760' width='38' height='770'").replace("<rect x='5826' y='1850' width='48' height='440'", "<rect x='5826' y='1760' width='48' height='770'")
    R = R[:-4] + (f"<g id='r9s-refspur'><polyline points='{pp}' fill='none' stroke='#a9a9a9' stroke-width='14' stroke-dasharray='30 30' opacity='.8'/>"
                  "<text x='2700' y='4600' class='r9t' style='fill:#7a7a7a' transform='rotate(-90 2700 4600)'>REF-SPUR — בוטלה (D‑504)</text></g>") + '</g>'
    H = H[:a] + R + H[b:]
    info['refspur_drawn'] = n_rs
    pipe = P['pipes'][0]; q = ' '.join(f'{f1(x)},{f1(y)}' for x, y in pipe['pts'])
    po = [f"<g id='pipes'><polyline points='{q}' fill='none' stroke='#5b3a1a' stroke-width='22' stroke-linejoin='round'/><polyline points='{q}' fill='none' stroke='#d98c2b' stroke-width='12' stroke-linejoin='round'/>"]
    L_ = 0; acc = 0
    for i in range(len(pipe['pts']) - 1):
        (x0, y0), (x1, y1) = pipe['pts'][i], pipe['pts'][i + 1]; l = math.hypot(x1 - x0, y1 - y0)
        t = (120 - acc) if acc else 0
        while t <= l:
            px, py = x0 + (x1 - x0) * t / max(l, 1e-9), y0 + (y1 - y0) * t / max(l, 1e-9)
            po.append(f"<rect x='{f1(px - 14)}' y='{f1(py - 14)}' width='28' height='28' fill='#5b3a1a'/>"); t += 120
        acc = (acc + l) % 120
    vx, vy = pipe['valve']
    po.append(f"<rect x='{vx - 40}' y='{vy - 30}' width='80' height='60' fill='#f2d6a8' stroke='#5b3a1a' stroke-width='5'/><text x='{vx + 60}' y='{vy + 12}' class='r9t' style='fill:#5b3a1a;text-anchor:start'>תחנת מגופים</text>")
    po.append(f"<text x='{pipe['pts'][-1][0] + 60}' y='{pipe['pts'][-1][1] + 420}' class='r9t' style='fill:#5b3a1a;text-anchor:start'>PIPE-REF — צינור על עמודים (D‑504)</text></g>")
    a, b = span(H, 'rails'); H = H[:b] + ''.join(po) + H[b:]
    H = H.replace("<use class='L-rails' href='#rails'/>", "<use class='L-rails' href='#rails'/><use class='L-rails' href='#pipes'/>")
    # i · the stages layer: every zone with its stage
    a, b = span(H, 'stg'); g = H[a:b]
    return H


def stg_layer(H, P, PS, COL):
    a, b = span(H, 'stg')
    import plan7b_svg as SV
    o = [f"<g id='stg' style='pointer-events:none'>"]
    for z in SV.ZN:
        s = PS.get(z, '—')
        if s == '—': continue
        x0, y0, x1, y1 = SV.zrect(z); parts = re.split(r'\s*[–/]\s*', s); first = parts[0]
        o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='{COL[re.match(r"S\d+", first).group(0)]}' fill-opacity='.55' stroke='#3b3f47' stroke-width='6'/>")
        if len(parts) > 1:
            sec = parts[-1] if parts[-1].startswith('S') else 'S' + parts[-1]
            if f"id='stp-{sec}'" not in ''.join(o):
                o.insert(1, f"<pattern id='stp-{sec}' width='70' height='70' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='35' height='70' fill='{COL[re.match(r"S\d+", sec).group(0)]}' fill-opacity='.85'/></pattern>")
            o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='url(#stp-{sec})' fill-opacity='.6'/>")
    H = H[:a] + ''.join(o) + '</g>' + H[b:]
    # the stage name in the corner of each zone (the city map and the section of 9נ2)
    def lab(z):
        x0, y0, _, _ = SV.zrect(z)
        return f"<g class='lb' data-k='99' transform='translate({x0 + 40} {y0 + 40})'><g class='s'><text class='stl' y='11' style='direction:ltr'>{E(PS[z])}</text></g></g>"
    add = ''.join(lab(z) for z in SV.ZN if PS.get(z, '—') != '—' and f"transform='translate({SV.zrect(z)[0] + 40} {SV.zrect(z)[1] + 40})'><g class='s'><text class='stl'" not in H)
    H = H.replace("<g class='L-stages' style='pointer-events:none'><use href='#stg'/>", "<g class='L-stages' style='pointer-events:none'><use href='#stg'/>" + add)
    for z in SV.ZN:   # a zone whose stage changed (G2, G3, H3 → S15–S16)
        x0, y0, _, _ = SV.zrect(z)
        H = re.sub(r"(transform='translate\(%d %d\)'><g class='s'><text class='stl' y='11' style='direction:ltr'>)[^<]*(</text>)" % (x0 + 40, y0 + 40), r"\g<1>" + PS.get(z, '—') + r"\g<2>", H)
    return H


# ---------------------------------------------------------------------- the hover data (__MAP)
def hover(H, P, G, PS, info):
    pre = '<script>window.__MAP='; a = H.index(pre) + len(pre); b = H.index(';</script>', a)
    D = json.loads(H[a:b].replace('<\\/', '</'))
    I = D['info']
    def st_txt(st):
        s = st.get('state', ''); t = s
        if st.get('stage'): t += ' — שלב ' + st['stage']
        if st.get('build'): t += ' (' + st['build'] + ')'
        if st.get('by') and s != 'קיים': t += ' · ' + st['by']
        return t
    byid = {}
    for coll in (P['lots'], P['sites'], P['r7']['items'], P['island']['lots'], P['air']['lots']):
        for l in coll: byid[l['id']] = l
    n = 0
    for k, t in enumerate(I):
        m = re.search(r"<div class='tl'>([A-Z0-9][A-Za-z0-9-]*) · ([A-H][0-9]) · ([^<]*)</div>", t)
        if not m: continue
        l = byid.get(m.group(1))
        if not l or not l.get('status'): continue
        I[k] = t[:m.start(3)] + E(st_txt(l['status'])) + t[m.end(3):]; n += 1
    info['hover_lots'] = n
    # the new lots of D2, B2 and B1, and the new road
    for l in P.get('r9s_lots', []):
        r = l['rect']; I.append(f"<b>{E(l['label'])}</b><div class='tl'>{E(l['id'])} · {E(l['zone'])} · {E(st_txt(l['status']))}</div><div class='tl'>סבב 9ס — מהמשחק</div>")
        D['lots'].append([r[0], r[1], r[2], r[3], len(I) - 1])
    for d in P.get('r9s_driveways', []):
        r = d['rect']; I.append(f"<b>{E(d['label'])}</b><div class='tl'>{E(d['game'])} · D2 · {E(st_txt(d['status']))}</div>"); D['lots'].append([r[0], r[1], r[2], r[3], len(I) - 1])
    for s in P['segments']:
        if s['road'] == 'D2-LCH':
            (x0, y0), (x1, y1) = s['pts'][0], s['pts'][-1]
            I.append(f"<b>הדרך לחניון החנויות</b> <span class='tl'>(D2-LCH)</span><div>דרך גישה 1+1 — 7 מ׳ ומדרכה של מטר מכל צד ({ASK})</div>"
                     f"<div class='tl'>קטע {E(s['id'])}, {s['len_m']} מ׳ · הבעלים 8.11 09:07 · נבנה ב-S7F265 (במשחק {E(s['game'])})</div>")
            D['segs'].append([x0, y0, x1, y1, 90, len(I) - 1])
    for nd in P['nodes']:
        if nd['id'] in ('K43_10', 'K43_11'):
            I.append(f"<b>{E(nd['label'])}</b> <span class='tl'>({E(nd['id'])})</span><div class='tl'>{E(nd['why'])}</div>"); D['nodes'].append([nd['x'], nd['y'], 40, len(I) - 1])
    # the junction names, the zones and their stages
    MN = {x['id']: x for x in P['nodes']}
    for k, t in enumerate(I):
        for nid in ('J18_16', 'J31_42', 'J18_25'):
            if f"(J" in t and f"({nid})" in t and MN[nid].get('label_was'):
                I[k] = t.replace(E(MN[nid]['label_was']), E(MN[nid]['label']))
            if nid == 'J18_25' and '(J18_25)' in I[k]:
                I[k] = I[k].replace('עצור / זכות קדימה', 'רמזור (סבב 9ס — כמו במשחק)')
    l4 = next(l for l in P['routes']['bus'] if l['id'] == '4'); st20 = next(s_ for s_ in P['bus']['stops'] if s_['id'] == 'ST-20')
    REP = [("<b>מסילת העקיפה למשא (D‑130) — עוקפת את התחנה, אל מסוף רכבת–אוויר</b><div class='tl'>עתידית — שלב 14", "<b>מסילת העקיפה למשא (D‑130) — עוקפת את התחנה, אל מסוף רכבת–אוויר</b><div class='tl'>E3 — נבנה ב-S7F266 (D‑503); E4 — עם S9"),
           ("<b>מסילת בית הזיקוק (D‑177)</b><div class='tl'>עתידית — שלב 14", "<b>מסילת בית הזיקוק (D‑177)</b><div class='tl'>בוטלה (D‑504) — במקומה הצינור PIPE-REF"),
           ('עתידית — שלב 12', 'עתידית — S13'), ('עתידי — שלב 17', 'עתידי — S9 (D‑503)'),
           ("<b>קו 4 — השדה</b><div>בשני הכיוונים · 0.08 ק״מ · כל 60 שנ׳ · 3 אוטובוסים</div>", "<b>קו 4 — השדה</b><div>לא מופעל עד S16 (R-84) · 0.08 ק״מ בעיר, עד AP1 · 3 אוטובוסים ברזרבה (D‑460)</div>"),
           (E(l4['why_was']), E(l4['why'])), (l4['why_was'], l4['why']), (E(st20['name_was']), E(st20['name'])), (st20['name_was'], st20['name'])]
    nr = Counter()
    for k, t in enumerate(I):
        for a_, b_ in REP:
            if a_ in t: t = t.replace(a_, b_); nr[a_[:24]] += 1
        I[k] = t
    info['hover_texts'] = dict(nr)
    import plan7b_svg as SV
    for z4 in D['zones']:
        x0, y0, x1, y1, k = z4
        z = next(q for q in SV.ZN if tuple(SV.zrect(q)) == (x0, y0, x1, y1))
        s = PS.get(z, '—'); why = (P.get('zone_stage_why') or {}).get(z)
        t = I[k]
        if 'שלב' not in t or why:
            body = re.sub(r"<div class='tl'>.*$", '', t)
            pu = P['zones'].get(z, {}).get('purpose', '')
            I[k] = body + f"<div class='tl'>{E(pu + ' · ' if pu else '')}שלב {E(s)}{E(' — ' + why) if why else ''}</div>"
        if z == 'B1':
            I[k] = re.sub(r"<div class='tl'>.*$", '', t) + "<div class='tl'>פארק צפוני והרחבת האגם · האגם, המזחים, הסירה, הפיקניק והחניון — נבנו ב-S8 (S7F252); שאר הפארק — S12</div>"
    H = H[:a] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + H[b:]
    return H


# ---------------------------------------------------------------------- the two tables of the lines
def lines_tables(H, P, G, GL):
    RN = {r['id']: r['name'] for r in P['roads']}; ST = {s['id']: s for s in P['bus']['stops']}
    TXT = P['lines_today'].get('text_game', {})
    rows = []
    for l in P['routes']['bus']:
        d = l['d460']; stops = [ST[i].get('name') or i for i in l.get('stop_ids', []) if i in ST]
        rows.append(f"<tr><td><span class='tag' style='background:{l['color']}'>{l['id']}</span></td><td>{E(l['name'])}<div class='small mut'>{'בשני הכיוונים' if l['twoway'] else 'לולאה בכיוון אחד'}</div></td>"
                    f"<td class='small'>{E(' ← '.join(RN.get(r, r) for r in l['road_seq']))}</td>"
                    f"<td>{E(l.get('len_note') or (str(l['len_km']) + ' ק״מ'))}</td><td class='small'><b>{len(stops) + 1}</b>: מסוף E3 · {E(' · '.join(stops))}</td>"
                    f"<td>כל {d['every_min']} דק׳ · סיבוב {d['round_min']} דק׳</td><td>{d['buses']}</td><td class='small'>{E(l['why'])}</td></tr>")
    T1 = ("<div class='wrap'><table><tr><th>קו</th><th>שם</th><th>המסלול המתוכנן</th><th>אורך</th><th>תחנות</th><th>מרווח (D‑460)</th><th>אוטובוסים (D‑460)</th><th>למה</th></tr>\n"
          + '\n'.join(rows) + "\n</table></div>")
    rows = []; tot_p = 0
    for l in P['routes']['bus']:
        g = GL.get(l['id']); d = l['d460']; tot_p += d['buses']
        if g:
            zs = ' → '.join(g['zones']); today = f"{zs}<div class='small mut'>{g['len_km']} ק״מ · {len(g['stops'])} תחנות: {E(', '.join(g['stops']))}{' · פרסה' if g['uturn'] else ''}</div>"
            txt = TXT.get(l['id']); tx = f"<div class='small mut'>הטקסט בטלפון במשחק: {E(txt)}{' — לא כמו המסלול' if txt and txt.replace(' ', '') != zs.replace(' ', '') else ''}</div>" if txt else ''
        else: today, tx = 'אין היום', ''
        chg = {'1': 'הקו מופעל בסוף S9a אם כל הקטעים והתחנות שלו קיימים (R-88); עובר לטבעת של המפה עם האזורים B6, ‏C6 ו-D6',
               '2': 'בסוף S9a (R-88), בלי C1 ו-D1 עד S12 — ' + ASK, '3': 'בסוף S9a (R-88); C6 ו-D6 — עם S10',
               '4': 'לא מופעל עד S16 (R-84): ב-S16 עד חזית הטרמינל, מפרצים ל-13.5 מ׳, בלי פרסה; 3 אוטובוסים ברזרבה',
               '5': 'קו חדש — עם האי (S13)', '6': 'קו חדש — כשהאזורים שלו נבנים; עוד לא נבדק אילו דרכים ותחנות חסרים לו'}[l['id']]
        rows.append(f"<tr><td><span class='tag' style='background:{l['color']}'>{l['id']}</span></td><td class='small'>{today}{tx}</td><td>0</td><td>{E(l['name'])}</td><td>{d['buses']}</td><td class='small'>{E(chg)}</td></tr>")
    rows.append(f"<tr><td></td><td><b>סך הכול</b></td><td><b>0</b></td><td></td><td><b>{tot_p}</b></td><td class='small'>ועוד 4 ברזרבה — 48 המקומות (33 בחניון הלילה, 15 במסוף)</td></tr>")
    T2 = ("<div class='wrap'><table><tr><th>קו</th><th>היום במשחק (S7F265) — נגזר מהמסלול</th><th>אוטובוסים היום</th><th>במפה</th><th>אוטובוסים (D‑460)</th><th>מה מתחלף ומתי</th></tr>\n"
          + '\n'.join(rows) + "\n</table></div>")
    i = H.index("<h3>אוטובוס — 6 קווים חדשים"); j = H.index("<div class='wrap'><table>", i); k = H.index("</table></div>", j) + len("</table></div>")
    H = H[:j] + T1 + H[k:]
    i = H.index("<h3>מספרי הקווים והצי"); j = H.index("<div class='wrap'><table>", i); k = H.index("</table></div>", j) + len("</table></div>")
    p0 = H.index("<p class='mut small'>", i)
    H = H[:p0] + ("<p class='mut small'>סבב 9ס (R-86 ג.6, סבב הסדר 16:40 ז.3): עמודת \"היום\" נגזרת בסקריפט מהמסלולים שבקוד המשחק — האזורים שהקו עובר בהם, "
                  "האורך והתחנות — ולא נכתבת ביד. ב-S7F265 יש לקווים 1–4 תחנות, ו-0 אוטובוסים בשירות (הקווים מושהים עד סוף S9a). המספרים במפה — לפי D‑460. "
                  "קווים 1–4 נשארים במספרים שלהם, קו 5 — המרינה, החוף והאי, קו 6 — המערב (D‑243, ‏D‑337).</p>") + H[j:]
    j = H.index("<div class='wrap'><table>", i); k = H.index("</table></div>", j) + len("</table></div>")
    H = H[:j] + T2 + H[k:]
    return H


# ---------------------------------------------------------------------- the stage drawings S14–S16, the rows of the transition table
def stage_cards(H, P, PS, COL):
    import plan7b_svg as SV
    i = H.index("<h2>המעבר — אזור אחרי אזור"); j = H.index("<div class='grid st'", i); k = H.index("</div><p class='mut small'>אותו מקרא", j)
    cards = []
    for t in P['transition']['stages']:
        if t['stage'] not in ('S14', 'S15', 'S16'): continue
        zs = [z for z in SV.ZN if PS.get(z) == t['stage'] or (PS.get(z) == 'S15–S16' and t['stage'] in ('S15', 'S16'))]
        if not zs: continue
        R = [SV.zrect(z) for z in zs]; x0 = min(r[0] for r in R) - 300; y0 = min(r[1] for r in R) - 300; x1 = max(r[2] for r in R) + 300; y1 = max(r[3] for r in R) + 300
        fr = ''.join(f"<rect x='{r[0]}' y='{r[1]}' width='{r[2] - r[0]}' height='{r[3] - r[1]}' fill='{COL[t['stage']]}' fill-opacity='.35' stroke='#1f5fd1' stroke-width='14'/>" for r in R)
        nm = ''.join(f"<text x='{(r[0] + r[2]) / 2:.0f}' y='{(r[1] + r[3]) / 2 + 30:.0f}' class='r9z'>{z}</text>" for z, r in zip(zs, R))
        cards.append(f"<div class='zc'><svg class='m' viewBox='{x0} {y0} {x1 - x0} {y1 - y0}' role='img' aria-label='{t['stage']}'><use href='#terrain'/><use class='L-lots' href='#lots'/>"
                     f"<g class='L-roads'><g opacity='.5'><use href='#roads'/></g></g><use class='L-rails' href='#rails'/>{fr}{nm}</svg>"
                     f"<b class='id'>{t['stage']}</b> <span class='pill'>{E(t['why'])}</span></div>")
    H = H[:k] + ''.join(cards) + H[k:]
    return H, len(cards)


# ---------------------------------------------------------------------- "מעודכן עד" under every drawing
def upd_lines(H, P, VER, BUILD, DATE):
    a = H.index('<main>'); hs = [(m.start(), re.sub('<[^>]+>', '', m.group(1))) for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", H)]
    out = []; last = 0; n = 0; stack = []
    for m in re.finditer(r"<svg[^>]*>|</svg>", H):
        if m.group(0) != '</svg>': stack.append(m.group(0)); continue
        op = stack.pop() if stack else ''
        if m.start() < a or stack or not re.search(r"class='m[ ']|role='img'", op): continue   # only the maps and the drawings (not the icons of the legend)
        h2 = ''
        for p_, t in hs:
            if p_ < m.start(): h2 = t
        if h2.startswith('סבב ') and not h2.startswith('סבב ' + VER):
            txt = f"ציור של {h2.split(' — ')[0]} — היסטוריה; המצב היום — במפות שלמעלה, מעודכן עד {BUILD} · סבב {VER} · {DATE}"
        else:
            txt = f"מעודכן עד: {BUILD} · סבב {VER} · {DATE}"
        out.append(H[last:m.end()]); out.append(f"<div class='upd'>{E(txt)}</div>"); last = m.end(); n += 1
    out.append(H[last:])
    return ''.join(out), n


# ---------------------------------------------------------------------- the drawings of the section of 9ס
def sec_svg(vb, label, body, uses=('terrain', 'lots', 'roads', 'rails', 'pipes', 'bus')):
    u = ''.join(f"<use href='#{x}'/>" if x in ('terrain',) else f"<use class='L-{'lots' if x == 'lots' else ('rails' if x in ('rails', 'pipes') else ('roads' if x == 'roads' else 'bus'))}' href='#{x}'/>" for x in uses)
    return f"<div class='zc'><svg class='m' viewBox='{vb}' role='img' aria-label='{E(label)}'>{u}{body}</svg><b>{E(label)}</b></div>"


def t_(x, y, s, cls='r9t', anchor='middle', extra=''):
    return f"<text x='{f1(x)}' y='{f1(y)}' class='{cls}' style='text-anchor:{anchor}{extra}'>{E(s)}</text>"


def section(P, G, rows, BZ, LOG, info, VER, BUILD, DATE, nok, nck):
    o = [f"<a id='r9s'></a><h2>סבב {VER} — המפה מעודכנת למה שנבנה ({BUILD}), מסונכרנת עם המשחק ועם ההחלטות של 8.11</h2>"]
    o.append("<div class='box'><b>מה ביקשו:</b> הביקורת של 7.11 20:30 — R-84 (קו 4), ‏R-85 (ציורים שלא עודכנו), ‏R-86 (המפה מול המשחק, שורה אחר שורה); "
             "סבב הסדר — ההודעה של 16:40, סעיף ז (מפת הדרכים), וההודעה של 17:45: סעיף א (קו 4), סעיף ב.5 (הציורים של D2, ‏B2 ו-B1, ושורת \"מעודכן עד\"), סעיף ג (1–8). "
             "וההחלטות של הבעלים מ-8.11: D‑502 (אין \"עתידי\" בתוך אזור), D‑503 (המסילות באזור נבנות עם האזור), D‑504 (REF-SPUR בוטלה — צינור), D‑505 (רציפי E3). "
             f"<b>המקור:</b> המשחק {BUILD} ‏({E(P['synced_with']['sha1'])}), מורץ בדפדפן (probe_s7f265.js). <b>הדרכים שהבעלים אישר לא שונו</b> — מה שבנוי מתואר כמו במשחק, ומה שעוד לא בנוי — כמו בתוכנית. "
             f"הבדיקות של המפה: {nok} מתוך {nck} עוברות (כמו בסבב 9נ2 — הרשת לא השתנתה מלבד מה שכתוב כאן).</div>")
    # what was done, by the items of the review
    o.append("<h3>מה נעשה — לפי הסעיפים</h3><div class='wrap'><table><tr><th>הסעיף</th><th>מה</th><th>מה נעשה</th></tr>")
    for x in LOG: o.append(f"<tr><td class='id'>{E(x['sec'])}</td><td>{E(x['item'])}</td><td class='small'>{E(x['what'])}</td></tr>")
    o.append("</table></div>")
    # the drawings
    D2 = []
    for l in P.get('r9s_lots', []):
        if l['zone'] == 'D2' and l['kind'] in ('building', 'parking') and l['id'] not in ('D2-PHARMACY', 'D2-OPTICS', 'D2-BARBER', 'D2-PHONES', 'D2-BOOKS', 'D2-POST'):
            r = l['rect']; D2.append(t_((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 8, l['label'].split(' — ')[0][:18], 'r9s'))
    road = ''.join(f"<polyline points='{' '.join(f'{f1(x)},{f1(y)}' for x, y in s['pts'])}' fill='none' stroke='#c8372d' stroke-width='12' stroke-dasharray='26 14'/>" for s in P['segments'] if s['road'] == 'D2-LCH')
    drop = ("<path d='M4590,1240 L4500,1240' stroke='#1f5fd1' stroke-width='8' fill='none' marker-end='url(#r9a)'/><path d='M4500,1290 L4590,1290' stroke='#1f5fd1' stroke-width='8' fill='none' marker-end='url(#r9a)'/>")
    mk = "<defs><marker id='r9a' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0L10,5L0,10z' fill='#1f5fd1'/></marker></defs>"
    o.append("<h3>הציורים — כמו שנבנו</h3><div class='grid2'>")
    D2.append(t_(4009, 925, 'שורת החנויות — 6 חנויות', 'r9s'))
    o.append(sec_svg('3560 700 1280 1020', 'D2 — כמו שנבנה (D‑496, ‏S7F264), עם הדרך מהמעגל (09:07) וההורדה של המלון (09:09)',
                     mk + road + drop + ''.join(D2) + t_(4200, 830, 'K43_10', 'r9s', 'end') + t_(4200, 1068, 'K43_11', 'r9s', 'end')))
    LB = [t_(1690, 1120, 'מיני גולף — 9 גומות', 'r9s'), t_(1376, 1395, 'מגרש המשחקים', 'r9s'), t_(1700, 310, 'המזח הצפוני', 'r9s'), t_(1500, 700, 'המזח המערבי', 'r9s'),
          t_(1850, 1150, 'המזח הדרומי', 'r9s'), t_(1960, 730, 'מזח הסירה', 'r9s'), t_(1690, 110, 'פינת הפיקניק', 'r9s'), t_(2270, 570, 'החניון של B1', 'r9s'),
          t_(1300, 840, 'B1', 'r9z', 'start'), t_(1300, 900 + 860, 'B2', 'r9z', 'start')]
    br = G['B12']['boatRoute']; boat = f"<polyline points='{' '.join(f'{x},{y}' for x, y in br)}' fill='none' stroke='#1f5fd1' stroke-width='5' stroke-dasharray='14 10'/>"
    o.append(sec_svg('1200 60 1300 1540', 'B1 ו-B2 — האגם, שלושת מזחי הדיג, מזח הסירה, המיני גולף של 9 גומות (S7F252)', boat + ''.join(LB)))
    o.append(sec_svg('2350 3350 1300 2000', 'הצינור PIPE-REF (D‑504) — במקום מסילת בית הזיקוק שבוטלה',
                     t_(2840, 3900, 'חוות המכלים — C5', 'r9s', 'start') + t_(2990, 5180, 'מזח הנפט', 'r9s', 'start') + t_(2400, 4230, 'גבול C5 / C6', 'r9s', 'start') +
                     "<line x1='2400' y1='4250' x2='3600' y2='4250' stroke='#1f5fd1' stroke-width='6' stroke-dasharray='20 14'/>" +
                     t_(3000, 4120, 'C5 — נבנה ב-S7F266', 'r9s', 'start') + t_(3000, 4420, 'C6 — עם S10', 'r9s', 'start')))
    o.append(sec_svg('5250 1650 900 1050', 'E3 — הרציפים y ‏1760–2530 (D‑505), ומסילת העקיפה (D‑503)',
                     "<rect x='5700' y='1760' width='220' height='770' fill='none' stroke='#c8372d' stroke-width='8' stroke-dasharray='24 14'/>" +
                     t_(5690, 1740, 'y 1760', 'r9s', 'end') + t_(5690, 2560, 'y 2530', 'r9s', 'end') + t_(5640, 2150, 'שני הרציפים — 4 קרונות', 'r9s', 'end') +
                     t_(6040, 2300, 'העקיפה — E3: S7F266', 'r9s', 'start')))
    o.append("</div>")
    # the lines, today and planned
    # the matching table
    c = Counter((r['kind'], r['dir'], r['ok']) for r in rows)
    KH = {'lot': 'מגרשים', 'segment': 'קטעי דרך', 'driveway': 'פתחים', 'junction': 'צמתים', 'crosswalk': 'מעברי חצייה', 'bay': 'מפרצי תחנה'}
    o.append("<h3>המפה מול המשחק — טבלת ההתאמה (בשני הכיוונים)</h3>"
             f"<p class='small'>הקובץ המלא: map_vs_game_9s.json ({len(rows)} שורות). כל מגרש, קטע דרך, פתח, צומת (כולל סוג השליטה), מעבר חצייה ומפרץ תחנה באזורים שנבנו "
             f"({E(', '.join(BZ))}, ושל S9a גם הקטעים שמחוץ ל-E3) — מהמפה למשחק ומהמשחק למפה, עם מרחק. יותר מ-4.5 מ׳ — לא תואם, עם הסבר ועם \"מי מתקן\".</p>"
             "<div class='wrap'><table><tr><th>מה</th><th>מהמפה למשחק — תואם / לא</th><th>מהמשחק למפה — תואם / לא</th></tr>")
    for k in ('lot', 'segment', 'driveway', 'junction', 'crosswalk', 'bay'):
        o.append(f"<tr><td>{KH[k]}</td><td>{c[(k, 'map→game', True)]} / <b>{c[(k, 'map→game', False)]}</b></td><td>{c[(k, 'game→map', True)]} / <b>{c[(k, 'game→map', False)]}</b></td></tr>")
    o.append("</table></div>")
    bad = [r for r in rows if not r['ok']]
    fx = Counter(r['fix'] for r in bad)
    o.append("<p class='small'>מי מתקן את מה שלא תואם: " + ' · '.join(f"{E(k)} — {v}" for k, v in fx.most_common()) + "</p>")
    o.append("<details><summary><b>כל מה שלא תואם</b> — " + str(len(bad)) + " שורות</summary><div class='wrap'><table><tr><th>מה</th><th>כיוון</th><th>במפה</th><th>במשחק</th><th>אזור</th><th>מרחק (מ׳)</th><th>הסבר</th><th>מי מתקן</th></tr>")
    DIR = {'map→game': 'מפה ← משחק', 'game→map': 'משחק ← מפה'}
    for r in sorted(bad, key=lambda r: (r['kind'], r['zone'] or '', r['map'] or r['game'] or '')):
        o.append(f"<tr><td>{KH[r['kind']]}</td><td class='small'>{DIR[r['dir']]}</td><td class='id'>{E(r['map'] or '—')}</td><td class='id'>{E(r['game'] or '—')}</td><td class='id'>{E(r['zone'] or '')}</td>"
                 f"<td>{'' if r['dist_m'] is None else r['dist_m']}</td><td class='small'>{E(r['note'])}</td><td class='small'>{E(r['fix'] or '')}</td></tr>")
    o.append("</table></div></details>")
    # what was replaced
    rp = P.get('replaced', [])
    o.append(f"<details><summary><b>מה הוחלף</b> — {len(rp)} פריטים (לא נמחקו: בנתונים עם \"הוחלף ב-…\")</summary><div class='wrap'><table><tr><th>מזהה</th><th>מה</th><th>מה היה</th><th>הוחלף ב-</th></tr>"
             + ''.join(f"<tr><td class='id'>{E(x['id'])}</td><td>{E(x['kind'])}</td><td class='small'>{E(x['label'][:90])}</td><td class='small'>{E(x['by'])}</td></tr>" for x in rp) + "</table></div></details>")
    # to approve
    asks = [x for x in LOG if ASK in x['what']]
    o.append("<h3>לאישורך — ברירות המחדל של הסבב</h3><ul>" + ''.join(f"<li><b>{E(x['item'])}</b> — {E(x['what'])}</li>" for x in asks) + "</ul>")
    return ''.join(o)


def texts(H, P, info):
    """the texts of the page that were not right (the review 17:45 א, ב.5, ג; D‑503 … D‑505) — in the body of the page and in the hover data; the sections of the old rounds stay word for word"""
    cut = H.index("<a id='r9n2'></a>"); mp = H.index('<script>window.__MAP=')
    A, Bd, C = H[:cut], H[cut:mp], H[mp:]
    n = Counter()
    def rep(old, new, where=('A', 'C')):
        nonlocal A, C
        if 'A' in where: n[old[:30]] += A.count(old); A = A.replace(old, new)
        if 'C' in where: n[old[:30]] += C.count(old); C = C.replace(old, new)
    # the labels of the old D2 (the names layer, in every view) — the new D2 in the same places, at the new buildings
    for old, new in (("translate(4009 913)'><g class='s'><text class='blt' y='3.3'>דואר<", "translate(4009 913)'><g class='s'><text class='blt' y='3.3'>שורת החנויות<"),
                     ("translate(4420 1220)'><g class='s'><text class='blt' y='3.3'>המלון העסקי<", "translate(4395 1095)'><g class='s'><text class='blt' y='3.3'>המלון הגדול<"),
                     ("translate(4035 1210)'><g class='s'><text class='blt' y='3.3'>קמפוס ההייטק<", "translate(4050 1336)'><g class='s'><text class='blt' y='3.3'>אופק טכנולוגיות<"),
                     ("translate(4450 920)'><g class='s'><text class='blt' y='3.3'>כיכר המטה<", "translate(4543 917)'><g class='s'><text class='blt' y='3.3'>מגדל המטה<"),
                     ("translate(4700 1014.5)'><g class='s'><text class='blt' y='3.3'>משרדים ומגדלים<", "translate(4700 950)'><g class='s'><text class='blt' y='3.3'>הקולנוע<")):
        rep(old, new, ('A',))
    pu = P['zones']['D2']['purpose']
    rep("<span class='pill'>עסקים, מלונות וההייטק · ", f"<span class='pill'>{E(pu)} · ", ('A',))
    # the rails and the stations
    def row(rid, f):
        nonlocal A
        for m in list(re.finditer(r"<tr><td class='id'>%s</td>.*?</tr>" % re.escape(rid), A))[::-1]:
            A = A[:m.start()] + f(m.group(0)) + A[m.end():]; n['row ' + rid] += 1
    row('BYPASS', lambda t: t.replace('עתידית — שלב 14', 'E3 — נבנה ב-S7F266 (D‑503); E4 — עם S9'))
    row('REF-SPUR', lambda t: t.replace('עתידית — שלב 14', 'בוטלה (D‑504) — במקומה הצינור PIPE-REF'))
    for r in ('ISL-A', 'ISL-B', 'ISL-ST-A', 'ISL-ST-B'): row(r, lambda t: t.replace('עתידית — שלב 12', 'עתידית — S13 (D‑503: המסילות לאי עם S13)'))
    row('ST-COAST', lambda t: t.replace('עתידי — שלב 17', 'עתידי — S9 (D‑503)'))
    row('ST-ISLAND', lambda t: t.replace('עתידי — שלב 12', 'עתידי — S13'))
    row('ST-E3', lambda t: t.replace('<td>קיים</td>', '<td>קיים; הרציפים y ‏1760–2530 — נבנה ב-S7F266 (D‑505)</td>'))
    for r in ('LX-3', 'LX-4'): row(r, lambda t: t.replace('(עתידי, שלב 14).', '— בוטל (D‑504): המסילה יצאה, והצינור עובר מעל שדרת הנמל על עמודים גבוהים.'))
    i0 = A.index('<h2>המסילות'); i1 = A.index('<h3>תחנות ומסופים', i0); n['rails s13'] += A[i0:i1].count('עתידית — שלב 12')
    A = A[:i0] + A[i0:i1].replace('עתידית — שלב 12', 'עתידית — S13') + A[i1:]
    rep('קו הנוסעים (עתידי, שלב 17)', 'קו הנוסעים (עתידי — תחנת החוף עם S9, האי עם S13; D‑503)', ('A',))
    m = re.search(r"<tr><td class='id'>[^<]*</td><td>מסילת העקיפה למשא.*?</tr>", A)
    if m: A = A[:m.start()] + m.group(0).replace('עתידית — שלב 14', 'E3 — נבנה ב-S7F266 (D‑503); E4 — עם S9') + A[m.end():]; n['row BYPASS'] += 1
    # line 4 and ST-20: not "as today"
    l4 = next(l for l in P['routes']['bus'] if l['id'] == '4'); st20 = next(s for s in P['bus']['stops'] if s['id'] == 'ST-20')
    rep(E(l4['why_was']), E(l4['why'])); rep(l4['why_was'], l4['why'])
    rep(E(st20['name_was']), E(st20['name'])); rep(st20['name_was'], st20['name'])
    H = A + Bd + C
    info['texts'] = dict(n)
    return H


def page(H, P, G, rows, BZ, PS, GL, LOG):
    import plan7b_r9s as R
    VER, BUILD, DATE = P['version'], R.BUILD, R.DATE          # one field: P['version']
    info = {}
    now = time.localtime()
    # 1 · the title, the main title, the header line — from one field
    H = re.sub(r"<title>[^<]*</title>", f"<title>מפת הדרכים · סבב {VER}</title>", H, count=1)
    H = re.sub(r"<h1>[^<]*</h1>", f"<h1>{E(P['title'])}</h1>", H, count=1)
    m = re.search(r"<div class='mut'>סבב 9נ · [^<]*?· <span class='small'>", H); assert m
    H = H[:m.start()] + f"<div class='mut'>סבב {E(VER)} · {DATE} · עודכן {now.tm_hour:02d}:{now.tm_min:02d} · מסונכרן עם המשחק {BUILD} · <span class='small'>" + H[m.end():]
    # the table of the rounds: a row for this round, at the top
    i = H.index("<h2>מה נעשה מאז 2.11 — כל הסבבים</h2>"); j = H.index("<tr><td><a href='#r9n2'>", i)
    H = H[:j] + (f"<tr><td><a href='#r9s'>סבב {E(VER)}</a></td><td class='small'>{now.tm_mday}.{now.tm_mon} {now.tm_hour:02d}:{now.tm_min:02d}</td>"
                 f"<td class='small'>{E('המפה מעודכנת ל-' + BUILD + ' ומסונכרנת עם המשחק: D2 החדש, הדרך מהמעגל (09:07) וההורדה של המלון (09:09), B1/B2 והאגם, S9a, ההחלטות D‑502–D‑505, הסטטוס של כל מגרש, הקווים מהמשחק, השלבים S13–S16 וטבלת ההתאמה.')}</td></tr>") + H[j:]
    H = H.replace("<h2>מה נעשה מאז 2.11 — כל הסבבים</h2>", "<h2>מה נעשה מאז 2.11 — כל הסבבים</h2>", 1)
    # 2 · the layers
    H = layers(H, P, G, info)
    H = stg_layer(H, P, PS, COL)
    # 3 · the hover data
    H = hover(H, P, G, PS, info)
    # 4 · the texts: the junction names, J18_25, ST-03, the stage cards and the stage table
    for nid in ('J18_16', 'J31_42'):
        n = next(x for x in P['nodes'] if x['id'] == nid)
        H = H.replace(E(n['label_was']), E(n['label'])).replace(n['label_was'], n['label'])
    H = H.replace("(ימינה בלבד) · ", "· ") if False else H
    H = texts(H, P, info)
    # the zone cards: the stage of every zone as in the plan (B1 — S8 / S12; E3 — S9a)
    def pill(m):
        z = m.group(1); return f"<b>{z}</b> <span class='pill'>{m.group(2)} · שלב {E(PS.get(z, m.group(3)))}</span>"
    cut = H.index("<a id='r9n2'></a>")
    H = re.sub(r"<b>([A-H][0-9])</b> <span class='pill'>([^<]*?) · שלב ([^<]*)</span>", pill, H[:cut]) + H[cut:]
    H = one(H, "<h3>B1 — פארק צפוני והרחבת האגם</h3>", "<h3>B1 — פארק צפוני והרחבת האגם</h3><p class='small'><b>סבב 9ס:</b> חלק מ-B1 כבר נבנה ב-S8 (S7F252) — האגם, המזח הצפוני, "
             "המזח המערבי, מזח הסירה וסירת המשוטים, פינת הפיקניק והחניון של B1 (בציור של סבב 9ס). השאר — S12.</p>")
    H = lines_tables(H, P, G, GL)
    H, ns = stage_cards(H, P, PS, COL); info['stage_cards'] = ns
    for s, zs in (('S14', 'S14'), ('S15', 'S15'), ('S16', 'S16')):
        pass
    # 5 · the section of 9ס, before the section of 9נ2
    nok = sum(1 for c in P['checks'] if c['ok']); nck = len(P['checks'])
    sec = section(P, G, rows, BZ, LOG, info, VER, BUILD, DATE, nok, nck)
    H = one(H, "<a id='r9n2'></a><h2>סבב 9נ2", sec + "<a id='r9n2'></a><h2>סבב 9נ2")
    # 6 · "מעודכן עד" under every drawing
    H, nu = upd_lines(H, P, VER, BUILD, DATE); info['upd'] = nu
    H = one(H, "</style></head>", ".upd{font-size:12px;color:var(--mut);margin-top:4px}.r9t{font:600 44px system-ui,sans-serif;fill:#1d2733;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:8px}"
             ".r9s{font:600 30px system-ui,sans-serif;fill:#1d2733;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:6px}.r9z{font:700 90px ui-monospace,Menlo,monospace;fill:#1d2733;text-anchor:middle;opacity:.7}"
             ".r9h{font:700 22px system-ui,sans-serif;fill:#fff;text-anchor:middle}</style></head>")
    return H, info
