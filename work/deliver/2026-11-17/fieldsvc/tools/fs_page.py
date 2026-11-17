#!/usr/bin/env python3
# fs_page.py — fieldsvc 17.11: דף הציור "סבב הקרקע לכל סוג" (SVG בקוד, בלי תמונות). פלט: deliver/2026-11-17/fieldsvc/Fieldsvc_plan.html
import json, os, sys, html, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fs_turn import CATS, services, fleet, PRM, FC
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'Fieldsvc_plan.html')
DIMS = {t[0]: (t[2], t[3]) for t in json.load(open(os.path.join(FC, 'ac_types.json')))['types']}
E = html.escape
COL = dict(SV='#e8b92b', PT='#3c4651', FT='#d6403a', FTs='#d6403a', CT='#2f6fd0', WT='#2d8fd8', LV='#7a6a3a', SVC='#5aa9a0', GP='#f08a24', BT='#8a5cc4', BL='#b07a2a',
           MS='#9aa4ad', AB='#1f8a5a', AL='#e04f8f', HL='#c9a227', TG='#6b5bd0', BR='#6f7a85', PW='#22262b', WC='#e04f8f')
NAME = dict(SV='מכוון', PT='גרר', FT='מכלית דלק', FTs='מתדלק קטן', CT='קייטרינג', WT='מים', LV='שירותים', SVC='ניקיון', GP='חשמל קרקע', BT='רכבת כבודה', BL='מסוע',
            MS='מדרגות', AB='אוטובוס', AL='אמבוליפט', HL='מעמיס מכולות', TG='גרר מכולות', BR='שרוול', PW='כבל 400 הרץ', WC='כיסא גלגלים')

def plane_svg(c, remote):
    """ציור מלמעלה: האף למעלה (צפון), צד השירות מימין; כל רכב במקום שלו ליד המטוס (מטרים, לפי ההיגיון של 042:g77SvcSpot / 046:s6aPortAD)"""
    L, S = DIMS.get(c['ac'], (30, 30)); hw = max(1.4, L * .055); W, H = 420, 380
    k = min(250 / max(L, 1), 190 / max(S, 1)) * (1.0 if L > 20 else .8); cx, top = W / 2 - 10, 70
    X = lambda x: cx + x * k; Y = lambda y: top + y * k
    s = [f'<svg viewBox="0 0 {W} {H}" class="pl" role="img" aria-label="{E(c["he"])} — המקום של כל רכב">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="10" class="apron"/>')
    # קו העצירה וקו האמצע
    s.append(f'<line x1="{X(0)}" y1="{Y(-14)}" x2="{X(0)}" y2="{Y(L+6)}" class="cl"/>')
    if c.get('heli'):
        s.append(f'<circle cx="{X(0)}" cy="{Y(L/2)}" r="{L*.75*k}" class="pad"/><text x="{X(0)}" y="{Y(L/2)+4}" class="padH">H</text>')
        s.append(f'<ellipse cx="{X(0)}" cy="{Y(L*.45)}" rx="{hw*k*1.3}" ry="{L*.32*k}" class="ac"/><line x1="{X(-S/2)}" y1="{Y(L*.45)}" x2="{X(S/2)}" y2="{Y(L*.45)}" class="rot"/><line x1="{X(0)}" y1="{Y(L*.45-S/2)}" x2="{X(0)}" y2="{Y(L*.45+S/2)}" class="rot"/>')
    else:
        wy = L * (.42 if c['k'] not in ('exec', 'private', 'cargo') else .45); sw = L * .16
        s.append(f'<path d="M{X(0)},{Y(0)} C{X(hw*1.1)},{Y(0)} {X(hw)},{Y(L*.06)} {X(hw)},{Y(L*.1)} L{X(hw)},{Y(L*.82)} L{X(hw*.4)},{Y(L)} L{X(-hw*.4)},{Y(L)} L{X(-hw)},{Y(L*.82)} L{X(-hw)},{Y(L*.1)} C{X(-hw)},{Y(L*.06)} {X(-hw*1.1)},{Y(0)} {X(0)},{Y(0)} Z" class="ac"/>')
        s.append(f'<path d="M{X(hw)},{Y(wy)} L{X(S/2)},{Y(wy+sw*1.2)} L{X(S/2)},{Y(wy+sw*1.55)} L{X(hw)},{Y(wy+sw*1.1)} Z M{X(-hw)},{Y(wy)} L{X(-S/2)},{Y(wy+sw*1.2)} L{X(-S/2)},{Y(wy+sw*1.55)} L{X(-hw)},{Y(wy+sw*1.1)} Z" class="ac"/>')
        ts = S * .32; s.append(f'<path d="M{X(hw*.5)},{Y(L*.88)} L{X(ts)},{Y(L*.97)} L{X(ts)},{Y(L*1.0)} L{X(-ts)},{Y(L*1.0)} L{X(-ts)},{Y(L*.97)} L{X(-hw*.5)},{Y(L*.88)} Z" class="ac"/>')
    sv = services(c, remote); have = {x['code'] for x in sv}
    def veh(code, x, y, l, w, rot=0, lab=None):
        col = COL.get(code, '#888'); lab = lab or code
        s.append(f'<g transform="translate({X(x):.1f},{Y(y):.1f}) rotate({rot})"><rect x="{-l*k/2:.1f}" y="{-w*k/2:.1f}" width="{l*k:.1f}" height="{w*k:.1f}" rx="2" fill="{col}" class="veh"/></g>')
        s.append(f'<text x="{X(x):.1f}" y="{Y(y)+3:.1f}" class="vl">{E(lab)}</text>')
    def hose(x0, y0, x1, y1, col, dash=False):
        s.append(f'<path d="M{X(x0):.1f},{Y(y0):.1f} Q{(X(x0)+X(x1))/2+6:.1f},{(Y(y0)+Y(y1))/2+6:.1f} {X(x1):.1f},{Y(y1):.1f}" stroke="{col}" class="hose{" dash" if dash else ""}"/>')
    vs = 1.0 if L > 20 else .7   # הרכבים בקנה מידה (מ׳)
    if c.get('heli'):
        veh('SV', 0, -L * .5, 1.2, 1.2, 0, 'מכוון'); veh('FTs', L * .9, L * .45, 6 * vs, 2.3 * vs, 90, 'FTs'); hose(L * .9 - 1.5, L * .45, hw, L * .45, COL['FT'])
    elif c.get('ga'):
        veh('SV', 0, -6, 1.2, 1.2, 0, '•'); veh('PT', 0, -4.2, 3.2, 1.8, 90)
        veh('FT', S / 2 + 3.5, L * .5, 6.5, 2.3, 90); hose(S / 2 + 2.2, L * .5, S * .3, L * .5, COL['FT'])
        if c['k'] == 'exec':
            veh('GP', hw + 4, L * .05, 3, 1.8, 90); hose(hw + 3, L * .05, hw * .3, L * .09, COL['PW'])
            veh('CT', hw + 5.2, L * .2, 7, 2.5, 0); veh('SVC', hw + 4.5, L * .38, 5, 2, 90)
            veh('LV', hw + 4, L * .8, 6, 2.3, 90); hose(hw + 3, L * .8, hw, L * .86, COL['LV'])
    elif c.get('cargo'):
        veh('SV', 0, -6, 1.2, 1.2, 0, '•'); veh('PT', 0, -5, 6, 2.6, 90)
        veh('GP', hw + 4, L * .04, 3, 1.8, 90); hose(hw + 3, L * .04, hw * .3, L * .09, COL['PW'])
        veh('HL', -hw - 5, L * .22, 9, 3.2, 0); veh('TG', -hw - 12, L * .4, 9, 2.4, 90)
        veh('FT', S / 2 + 3.5, L * .48, 9, 2.5, 90); hose(S / 2 + 2.2, L * .48, S * .3, L * .5, COL['FT'])
    else:
        veh('SV', 0, -7, 1.2, 1.2, 0, '•'); veh('PT', 0, -5, 6, 2.6, 90)
        br = c['bridge'] and not remote
        if br:
            s.append(f'<path d="M{X(-hw-28)},{Y(L*.06)} L{X(-hw-14)},{Y(L*.1)} L{X(-hw-.5)},{Y(L*.115)}" class="bridge"/><circle cx="{X(-hw-14)}" cy="{Y(L*.1)}" r="{2.2*k}" class="rot2"/><text x="{X(-hw-16)}" y="{Y(L*.1)-8}" class="vl dark">שרוול</text>')
            if c['k'] == 'giant': s.append(f'<path d="M{X(-hw-28)},{Y(L*.22)} L{X(-hw-14)},{Y(L*.25)} L{X(-hw-.5)},{Y(L*.27)}" class="bridge"/>')
            hose(-hw - 1.5, L * .115, -hw * .3, L * .09, COL['PW'])
        else:
            veh('GP', hw + 4, L * .04, 3, 1.8, 90); hose(hw + 3, L * .04, hw * .3, L * .09, COL['PW'])
            if 'MS' in have:
                veh('MS', -hw - 4, L * .12, 7.5, 2.5, 0, 'MS')
                if c['k'] in ('large', 'giant'): veh('MS', -hw - 4, L * .84, 7.5, 2.5, 0, 'MS')
            veh('AB', -hw - 13, L * .3, 13.5, 3, 90)
            if 'AL' in have: veh('AL', hw + 5, L * .12, 7.5, 2.6, 0, 'AL')
        if c['k'] in ('medium', 'small'):
            veh('BT', hw + 6, L * .32, 3, 1.8, 90, 'BT'); [veh('BT', hw + 6, L * .32 + 3.3 + i * 3.4, 3, 1.8, 90, '') for i in range(2)]
        else:
            veh('BL', hw + 3.2, L * .26, 7.5, 2.1, 25); veh('BT', hw + 9, L * .3, 3, 1.8, 90, 'BT'); [veh('BT', hw + 9, L * .3 + 3.3 + i * 3.4, 3, 1.8, 90, '') for i in range(2)]
            if c['k'] == 'giant': veh('BL', hw + 3.2, L * .7, 7.5, 2.1, -25)
        veh('SVC', hw + 13, L * .12, 5, 2, 90)
        if 'WT' in have: veh('WT', hw + 4, L * .74, 6.5, 2.4, 90); hose(hw + 2.8, L * .74, hw, L * .8, COL['WT'])
        veh('LV', hw + 10, L * .74, 6.5, 2.4, 90, 'LV'); hose(hw + 8.8, L * .76, hw, L * .86, COL['LV'], True)
        veh('CT', hw + 5.4, L * .88, 7, 2.5, 0); 
        if c['k'] == 'giant': veh('CT', hw + 5.4, L * .2, 7, 2.5, 0)
        wy = L * .42; veh('FT', S / 2 * .62 + 1, wy + L * .16 * 1.35 + 4.5, 9, 2.5, 0); hose(S / 2 * .62 - 2, wy + L * .16 * 1.35 + 3.2, S / 2 * .55, wy + L * .16 * 1.2, COL['FT'])
    # סרגל קנה מידה
    s.append(f'<line x1="20" y1="{H-18}" x2="{20+10*k}" y2="{H-18}" class="sc"/><text x="{20+10*k+30}" y="{H-14}" class="vl dark">10 מ׳</text>')
    s.append(f'<text x="{W-14}" y="22" class="ttl" text-anchor="start">↑ האף · צד השירות — מימין</text>')
    s.append('</svg>'); return ''.join(s)

def gantt_svg(c, remote):
    sv = services(c, remote); D = c['D']; t_min = min(-25, min(x['t0'] for x in sv)); t_max = max(D + 85, max(x['t0'] + x['d'] for x in sv))
    W, rowh = 640, 19; H = 34 + rowh * len(sv) + 16; x0, x1 = 150, W - 14; X = lambda t: x0 + (t - t_min) / (t_max - t_min) * (x1 - x0)
    s = [f'<svg viewBox="0 0 {W} {H}" class="gt" role="img" aria-label="{E(c["he"])} — הסדר והזמנים">']
    s.append(f'<rect x="{X(0):.1f}" y="22" width="{X(D)-X(0):.1f}" height="{H-34}" class="dwell"/>')
    for t in range(0, int(t_max) + 1, 50 if t_max < 300 else 100):
        s.append(f'<line x1="{X(t):.1f}" y1="20" x2="{X(t):.1f}" y2="{H-12}" class="grid"/><text x="{X(t):.1f}" y="15" class="tk">{t}</text>')
    s.append(f'<text x="{X(0)+3:.1f}" y="{H-2}" class="tk">עצירה (on-block)</text><text x="{X(D)-3:.1f}" y="{H-2}" class="tk" text-anchor="end">דחיפה · {D} ש׳</text>')
    for i, x in enumerate(sv):
        y = 26 + i * rowh; col = COL.get(x['code'], '#888')
        s.append(f'<text x="{x0-8}" y="{y+12}" class="rl">{E(x["he"])}{" ×"+str(x["n"]) if x["n"]>1 and "×" not in x["he"] else ""}</text>')
        s.append(f'<rect x="{X(x["t0"]):.1f}" y="{y+2}" width="{max(3, X(x["t0"]+x["d"])-X(x["t0"])):.1f}" height="{rowh-6}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{X(x["t0"]+x["d"])+4:.1f}" y="{y+12}" class="tk" text-anchor="start">{x["t0"]}–{x["t0"]+x["d"]}</text>')
    s.append('</svg>'); return ''.join(s)

def card(c, remote, tag):
    sv = services(c, remote)
    rows = ''.join(f'<tr><td><span class="sw" style="background:{COL.get(x["code"],"#888")}"></span>{E(x["he"])}</td><td class="n">{x["t0"]}–{x["t0"]+x["d"]}</td><td>{E(x["where"])}</td><td>{E(x["see"])}</td><td class="src">{E(x["src"])}</td></tr>' for x in sv)
    wc = c['pax'] * PRM
    prm = (f'צפי כיסא גלגלים: {c["pax"]} נוסעים × {PRM:.0%} = {wc:.1f} לטיסה — ' + ('אמבוליפט לדלת R1 (בעמדה בלי שרוול)' if (wc >= .5 and remote) else 'בשרוול, מלווה דוחף את הכיסא (בלי רכב)' if (wc >= .5) else 'אין (ברגל / לימוזינה)')) if c['pax'] else 'אין נוסעים'
    return f'''<section class="card" id="{c['k']}{tag}"><h3>{E(c['he'])} · {E(c['ac'])}{(' · גם '+E(c['also'])) if c['also'] else ''}{E(tag and ' — עמדה מרוחקת' or '')}</h3>
<p class="meta">עמדות: {E(c['stands'])} · עמידה {c['D']} ש׳ · נוסעים {c['pax']} · {E(prm)}</p>
<div class="two">{plane_svg(c, remote)}{gantt_svg(c, remote)}</div>
<table class="t"><thead><tr><th>שירות</th><th>ש׳ מהעצירה</th><th>איפה ליד המטוס</th><th>מה רואים</th><th>המצייר (הישן → S15)</th></tr></thead><tbody>{rows}</tbody></table></section>'''

def fleet_table(title, sched, note):
    F = fleet(sched); codes = [c for c in ['PT', 'FT', 'FTs', 'CT', 'WT', 'LV', 'SVC', 'GP', 'BT', 'BL', 'MS', 'AB', 'AL', 'HL', 'TG'] if c in F]
    rows = ''.join(f'<tr><td><span class="sw" style="background:{COL.get(k,"#888")}"></span>{E(NAME.get(k,k))} ({k})</td><td class="n">{F[k]["visits"]}</td><td class="n">{F[k]["busy"]}</td><td class="n">{F[k]["peak"]}</td><td class="n b">{F[k]["need"]}</td></tr>' for k in codes)
    return f'<div class="ft"><h4>{E(title)}</h4><p class="meta">{E(note)}</p><table class="t"><thead><tr><th>רכב</th><th>ביקורים במחזור</th><th>שניות עסוק (כולל נסיעה)</th><th>שיא בו-זמני</th><th>צריך</th></tr></thead><tbody>{rows}</tbody></table></div>'


def need_section():
    import fs_need
    R = fs_need.table(); MODE = {'bridge':'שרוול','remote':'מרוחקת','ga':'GA','cargo':'משא'}
    allc = ['PT','BT','BL','FT','CT','WT','LV','SVC','GP','MS','AB','AL','HL','TG']
    head = ''.join(f'<th title="{E(fs_need.HE.get(c,c))}">{E(fs_need.HE.get(c,c))}</th>' for c in allc)
    body = []
    for r in R:
        seen = {}
        for c in r['cells']: seen.setdefault((c['mode'], tuple(c['need'])), []).append(c['stand'])
        if not seen:
            body.append(f'<tr><td>{E(r["code"])} · {E(r["he"])}</td><td colspan="{len(allc)+2}" class="meta">{"אין עמדה בשדה היום (נכנס רק ב-" + " ".join(r["fits"]) + ")" if r["fits"] else "לא נכנס באף עמדה — " + ("האמפיבי: על המים (074zs)" if r["code"]=="AM" else "")}</td></tr>')
        for (md, n), ss in seen.items():
            cells = []
            for c in allc:
                k = sum(1 for x in n if x == c or (('|' in x) and c in x.split('|')))
                alt = any('|' in x and c in x.split('|') for x in n)
                cells.append(f'<td class="n{" b" if k else ""}">{("×"+str(k) if k>1 else "✓") + (" (או)" if alt else "") if k else "—"}</td>')
            body.append(f'<tr><td>{E(r["code"])} · {E(r["he"])}</td><td>{E(" ".join(ss))}</td><td>{E(MODE.get(md,md))}</td>{"".join(cells)}</tr>')
    nots = ''.join(f'<li>{E(r["code"])}: נכנס גם ב-{E(" ".join(r["not_policy"]))} — לא לפי המדיניות</li>' for r in R if r['not_policy'])
    return f'''<h2>1א. מה כל מטוס צריך בכל עמדה (הבדיקה: בדיוק זה — 0 חסרים, 0 מיותרים)</h2>
<p class="meta">העמדות — מה שנכנס לפי Stands_matrix של fieldcalc, ומתוכו לפי גודל (פרטי ומנהלים לא ב-P; נוסעים לא בעמדות המשא; הגדולים ב-P1 / P6). השירותים — המטריצה של fieldcalc (074zq:NEED) לפי מצב העמדה: שרוול → בלי מדרגות, אוטובוס וחשמל קרקע (400 הרץ מהשרוול), כיסא גלגלים בשרוול; מרוחקת → מדרגות (חוץ ממדרגות מובנות: TP ומנהלים), אוטובוס, חשמל קרקע, אמבוליפט לפי נוסעים; פרטי ומנהלים — בלי רכבי כבודה; משא — בלי נוסעים, עם מעמיס מכולות, עגלות מכולות, גרר, דלק וחשמל; המשא הענק (HC) על שתי עמדות יחד (fieldthru2) — הכול כפול, מעמיס בדלת הצד ובאף. מותר ולא חובה: הסעת צוות, "עקוב אחריי". (הבעלים 15:35 / 15:40) חובה בכל טיסת נוסעים: מזוודות (חוץ מפרטי ומנהלים), קייטרינג (קטן למנהלים ולאזוריים — RJ / TP, מלא לשאר), דלק, גרר; בלי שרוול — גם מדרגות ואוטובוס. מים ושירותים — לפי אורך הטיסה: לפחות 60% מהטיסות של כל סוג (בטבלה — טיסה ארוכה; ‏40% הקצרות של כל סוג — בלי). משא — ציוד המטען 100%.</p>
<div style="overflow-x:auto"><table class="t"><thead><tr><th>סוג</th><th>עמדות</th><th>מצב</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>
<ul class="meta">{nots}</ul>'''

def old_section():
    f = os.path.join(HERE, 'old_vs_new.html')
    return open(f, encoding='utf-8').read() if os.path.exists(f) else ''
def main(extra=None):
    fc = json.load(open(os.path.join(FC, 'fc_result.json')))
    S18 = [(s['stand'], s['model'], s['onblock']) for s in fc['schedule']]
    cards = []
    for c in CATS:
        cards.append(card(c, False, ''))
        if c['k'] in ('large', 'medium'): cards.append(card(c, True, '-r'))
    fl = [fleet_table('הלוח של fieldcalc — 18 טיסות (היעד 90 תנועות)', S18, 'fc_result.json:schedule — הזמנים של העצירה; לכל שירות: נסיעה הלוך / חזור + העבודה')]
    for t, sch, note in (extra or []): fl.append(fleet_table(t, sch, note))
    findings = open(os.path.join(HERE, 'findings.html'), encoding='utf-8').read() if os.path.exists(os.path.join(HERE, 'findings.html')) else ''
    page = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>סבב הקרקע בשדה</title>
<style>
:root{{--bg:#f4f1ea;--fg:#1d232a;--mut:#5d6670;--card:#fffdf8;--line:#d9d3c7;--apron:#c9ccc8;--ac:#ffffff;--acs:#3a4048;--grid:#e3ddd0;--dw:#eef4ff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#15191d;--fg:#e9e6df;--mut:#a3abb3;--card:#1e2328;--line:#343b43;--apron:#3a4045;--ac:#dfe3e7;--acs:#9aa4ad;--grid:#2c3238;--dw:#1d2a3a}}}}
:root[data-theme="dark"]{{--bg:#15191d;--fg:#e9e6df;--mut:#a3abb3;--card:#1e2328;--line:#343b43;--apron:#3a4045;--ac:#dfe3e7;--acs:#9aa4ad;--grid:#2c3238;--dw:#1d2a3a}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,"Segoe UI",Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:18px 16px 60px}} h1{{font-size:24px;margin:6px 0}} h2{{font-size:19px;margin:28px 0 8px;border-bottom:2px solid var(--line);padding-bottom:4px}}
h3{{font-size:17px;margin:0 0 4px}} h4{{margin:4px 0}} .meta{{color:var(--mut);margin:2px 0 8px}} .card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0}}
.two{{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start}} .two svg.pl{{flex:0 0 360px;max-width:100%}} .two svg.gt{{flex:1 1 520px;max-width:100%}}
.t{{border-collapse:collapse;width:100%;margin-top:8px;font-size:13.5px}} .t th,.t td{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:right;vertical-align:top}} .t th{{color:var(--mut);font-weight:600}}
.n{{direction:ltr;text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}} .b{{font-weight:700}} .src{{color:var(--mut);font-size:12px;direction:ltr;text-align:right}}
.sw{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-left:6px;vertical-align:middle}}
.ft{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;margin:10px 0}} .fts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:10px}}
svg .apron{{fill:var(--apron)}} svg .cl{{stroke:#e8b92b;stroke-width:1.2;stroke-dasharray:6 5}} svg .ac{{fill:var(--ac);stroke:var(--acs);stroke-width:1.2}} svg .veh{{stroke:rgba(0,0,0,.45);stroke-width:.6}}
svg .vl{{font-size:9.5px;fill:#fff;text-anchor:middle;font-weight:700;paint-order:stroke;stroke:rgba(0,0,0,.55);stroke-width:2px}} svg .vl.dark{{fill:var(--fg);stroke:none;font-weight:600}}
svg .hose{{fill:none;stroke-width:1.8}} svg .hose.dash{{stroke-dasharray:3 2}} svg .bridge{{fill:none;stroke:#6f7a85;stroke-width:7;stroke-linecap:round;opacity:.85}} svg .rot2{{fill:#4b545d}}
svg .sc{{stroke:var(--fg);stroke-width:2}} svg .ttl{{font-size:11px;fill:var(--fg)}} svg .pad{{fill:none;stroke:#e8b92b;stroke-width:2}} svg .padH{{font-size:22px;fill:#e8b92b;text-anchor:middle}} svg .rot{{stroke:var(--acs);stroke-width:2}}
svg .dwell{{fill:var(--dw)}} svg.map{{width:100%;max-width:820px}} svg .fence{{fill:none;stroke:#5a6470;stroke-width:1.5;stroke-dasharray:4 3}} svg .road{{fill:#a9aba3}} svg .road.ow{{fill:#b9a98a}} svg .pocket{{fill:none;stroke:#c8352e;stroke-width:.8}} svg .base{{fill:#d9d4c7;stroke:#8c8678;stroke-width:.6}} svg .lab{{font-size:8px;fill:var(--fg);text-anchor:middle}} svg .stand{{fill:#3a4048}} svg .st{{stroke:#111;stroke-width:.8;opacity:.9}} svg .stl{{font-size:9px;fill:var(--fg);font-weight:700}} svg .grid{{stroke:var(--grid);stroke-width:1}} svg .tk{{font-size:10px;fill:var(--mut);text-anchor:middle;direction:ltr}} svg .rl{{font-size:11.5px;fill:var(--fg);text-anchor:end}}
.note{{background:var(--card);border-right:4px solid #2f6fd0;padding:8px 12px;border-radius:6px;margin:10px 0}}
@media (max-width:640px){{.two svg.pl{{flex-basis:100%}} .t{{font-size:12.5px}} .src{{display:none}}}}
</style></head><body><main>
<h1>השדה — כל טיסה מקבלת את כל השירותים, ורואים כל רכב עובד</h1>
<p class="meta">fieldsvc · 17.11 · הציור לפני הבנייה (כלל 13) · SVG בקוד, בלי תמונות · הזמנים — שניות של המחזור (720 ש׳ = 6 שעות משחק), מהעצירה בעמדה</p>
{findings}
{need_section()}
{old_section()}
<h2>1. סבב הקרקע לכל סוג</h2>
<p class="meta">לכל סוג: איפה כל רכב עומד ליד המטוס (האף למעלה, צד השירות מימין, השרוול / המדרגות משמאל), הסדר והזמנים, ומה רואים אותו עושה. הזמנים — מ-042:g77SvcPlan של המנוע הישן ומטריצת השירות של fieldcalc.</p>
{''.join(cards)}
<h2>2. כמה רכבים צריך — כל הלו״ז בלי איחור</h2>
<p class="meta">שיא בו-זמני של ביקורים (כולל הנסיעה מהבית ובחזרה) במחזור; "צריך" = השיא, ועוד עתודה כשהרכבים עסוקים יותר מ-80%. רכב אחד משרת טיסה אחרי טיסה (AF של הישן).</p>
<div class="fts">{''.join(fl)}</div>
<h2>3. כיסא גלגלים</h2>
<div class="note">לפי אחוז הנוסעים, לא בכל טיסה: צפי = נוסעים × {PRM:.0%} (הנחה — לאישורך). בעמדה עם שרוול — הנוסע עובר בשרוול עם מלווה (בלי רכב). בעמדה מרוחקת / בלי שרוול, כשהצפי ≥ 0.5 — אמבוליפט (כמו G77_AMB של הישן, 050): מגיע אחרי שאוטובוס ההגעה יצא, נעמד בניצב לדלת הימנית הקדמית (R1), הארגז עולה על המספריים (6 ש׳), הבמה נשלפת לסף, הנוסע שנחת יורד בכיסא עם המלווה (9 ש׳), הנוסע שיוצא עולה (9 ש׳), הארגז יורד, והרכב חוזר — לפני שאוטובוס היציאה מגיע. צר-גוף ב-R2: 1.5 לטיסה → בכל סבב. מנהלים / פרטי — ברגל או בלימוזינה.</div>
{open(os.path.join(HERE,'stations.html'),encoding='utf-8').read() if os.path.exists(os.path.join(HERE,'stations.html')) else ''}
<h2>4. הבדיקה החוסמת (fieldsvc_all — בתוך roadAudit)</h2>
<div class="note">לכל טיסה בלו״ז (מחזור שלם — כל הטיסות של כל שעות המשחק): בדיוק מה שהטבלה של סעיף 1א אומרת לסוג ולעמדה שלה — 0 חסרים, 0 מיותרים (רכב שלא צריך לסוג הזה נשאר בבית בביקור הזה); כשהסוג מתחלף בסבב (fieldthru2) — "צריך" מחושב מחדש והשירות מתוכנן לסוג החדש בזמן שהמטוס באוויר — רכב עם רגל עבודה ליד המטוס, שמתחילה אחרי העצירה ונגמרת לפני תחילת הדחיפה (0 איחורים בגלל רכב); לכל רכב בעבודה — מצייר פעולה (צינור / הרמה / מסוע / מדרגות / כבל / גרר); לפחות 2 שירותי כיסא גלגלים; ועוד s15k_fleet ו-s15_sim_no_overlap (0 נגיעות), ‏q_ingame, ‏rules_gate, ‏stuckmax 150, ‏people_on_road, ‏0 שגיאות, זיכרון ≤ +50 מ״ב.</div>
</main></body></html>'''
    open(OUT, 'w', encoding='utf-8').write(page)
    b = page.encode('utf-8'); print(OUT, len(b), hashlib.sha1(b).hexdigest()[:12], 'img:', page.count('<img'), 'data:image:', page.count('data:image'))
if __name__ == '__main__':
    ex = []
    if os.path.exists(os.path.join(HERE, 'sched_extra.json')):
        for t, sch, note in json.load(open(os.path.join(HERE, 'sched_extra.json'))): ex.append((t, [tuple(x) for x in sch], note))
    main(ex)
