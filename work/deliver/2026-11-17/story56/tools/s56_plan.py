#!/usr/bin/env python3
# story56 — הציור (כלל 13 / 20): לוח הסיפור כולו — הפתיחה, פרק 5, פרק 6, הסוף. נבנה מ-s56_data.py (אותו מקור של הנתונים במשחק). SVG בקוד, בלי תמונות.
import json, os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import s56_data as S
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'Story56_plan.html')
LK = json.load(open(os.path.join(os.path.dirname(__file__), 'locks302.json'), encoding='utf-8'))
E = html.escape
CHC = {'S': '#5b7c99', '1': '#4f8a5b', '2': '#8a6d3b', '3': '#3d7fa8', '4': '#2f8f8f', '5': '#b0503a', '6': '#7a5aa8'}
NAMES = {'S': 'מההתחלה', '1': 'פרק 1', '2': 'פרק 2', '3': 'פרק 3', '4': 'פרק 4', '5': 'פרק 5', '6': 'פרק 6'}
WHO = {k: v[0] for k, v in S.CHARS.items()}
WHO.update({'st-aharon': 'סבא אהרן', 'st-shimon': 'שמעון', 'st-shmulik': 'שמוליק', 'st-david': 'דוד', 'st-naftali': 'נפתלי', 'st-eliyahu': 'אליהו',
            's9-avi': 'אברהם', 's9-moshe': 'משה', 's9-yossi': 'יוסף', 'st-letter': 'המכתב של סבא'})

def grid(ch, steps):
    """מפת האזורים A–H × 0–9: הצבע — הפרק שפותח; מסגרת עבה — פתוח בפרק הזה; נקודה ממוספרת — מקום של צעד"""
    order = ['S', 'O', '1', '2', '3', '4', '5', '6', 'F']
    lvl = order.index(ch) if ch in order else 99
    cols = 'ABCDEFGH'; w, h = 34, 22
    out = ['<svg viewBox="0 0 %d %d" class="grid" role="img" aria-label="מפת האזורים">' % (len(cols) * w + 24, 10 * h + 20)]
    for i, c in enumerate(cols):
        out.append('<text x="%d" y="12" class="gl">%s</text>' % (24 + i * w + w / 2, c))
    for r in range(10):
        out.append('<text x="10" y="%d" class="gl">%d</text>' % (20 + r * h + h / 2 + 4, r))
        for i, c in enumerate(cols):
            z = c + str(r); k = LK['zones'].get(z, 'S'); op = order.index(k) <= lvl
            x, y = 24 + i * w, 16 + r * h
            out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" fill-opacity="%s" stroke="var(--ln)" stroke-width="%s"/>' % (x + 1, y + 1, w - 2, h - 2, CHC[k], '.85' if op else '.16', '1.6' if op else '.4'))
    for n, z in steps:
        if not z or len(z) != 2 or z[0] not in cols: continue
        i = cols.index(z[0]); r = int(z[1]); x, y = 24 + i * w + w / 2, 16 + r * h + h / 2
        out.append('<circle cx="%d" cy="%d" r="8" fill="var(--bg)" stroke="var(--ink)" stroke-width="1.4"/><text x="%d" y="%d" class="gn">%s</text>' % (x, y + 1, x, y + 4.5, n))
    out.append('</svg>')
    return ''.join(out)

def zones_of(where):
    import re
    return re.findall(r'\b([A-H][0-9])\b', where or '')

def kind(s):
    for k, t in [('talk', 'שיחה'), ('job', 'נהיגה / עבודה'), ('area', 'סיפור אזור'), ('license', 'רישיון'), ('state', 'פעולה במשחק'), ('show', 'הצגה'), ('watch', 'צפייה בעולם')]:
        if k in s: return t
    return ''

def chapter(C, intro):
    cards, pts, n = [], [], 0
    for mi in C['missions']:
        rows = []
        for s in mi['steps']:
            n += 1
            for z in zones_of(s.get('where'))[:1]: pts.append((n, z))
            rows.append('<tr><td class="n">%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                n, E(kind(s)), E(s.get('where', '')), E(s.get('do', '')), E(s.get('scene', '')) or '—'))
        aft = mi['start'].get('after'); aft = ' + '.join(aft) if isinstance(aft, list) else (aft or '')
        cards.append('<div class="mi"><div class="mh"><b>%s · %s</b><span class="who">%s</span></div><div class="mt">%s</div>'
                     '<div class="ma">אחרי: %s · %s</div><table><tr><th>#</th><th>סוג</th><th>איפה</th><th>מה השחקן עושה בפועל</th><th>סצנה</th></tr>%s</table></div>' % (
            E(mi['id']), E(mi['name']), E(WHO.get(mi['giver'], mi['giver'])), E(mi['text']), E(aft), ('פרס ' + str(mi['reward'])) if mi.get('reward') else 'בלי פרס כסף', ''.join(rows)))
    return ('<section class="ch" style="--c:%s"><h2>%s · %s</h2><p class="goal">%s</p>%s<div class="two"><div class="cards">%s</div><div class="side">%s<p class="note">צבע — הפרק שפותח את האזור; מלא — פתוח בפרק הזה; עיגול — מקום של צעד (המספר בטבלה).</p></div></div></section>' % (
        CHC.get(C['id'], '#a5600b'), E(C['no']), E(C['name']), E(C['goal']), intro, ''.join(cards), grid(C['id'], pts)))

def flow(C):
    """הזרימה: אילו משימות פתוחות יחד (D‑693 — 2–3 בכל סדר)"""
    ms = C['missions']; ids = [m['id'] for m in ms]; lev = {}
    for m in ms:
        a = m['start'].get('after'); A = a if isinstance(a, list) else [a]
        lev[m['id']] = 1 + max([lev.get(x, 0) for x in A if x in ids] or [0])
    L = max(lev.values()); W = 120; H = 44; byl = {}
    for m in ms: byl.setdefault(lev[m['id']], []).append(m['id'])
    pos = {}
    for l, L2 in byl.items():
        for j, i in enumerate(L2): pos[i] = (20 + (L - l) * (W + 26), 14 + j * (H + 12))
    hh = 14 + max(len(v) for v in byl.values()) * (H + 12)
    out = ['<svg viewBox="0 0 %d %d" class="flow">' % (20 + L * (W + 26), hh)]
    for m in ms:
        a = m['start'].get('after'); A = a if isinstance(a, list) else [a]
        for x in A:
            if x in pos:
                x1, y1 = pos[x]; x2, y2 = pos[m['id']]
                out.append('<path d="M%d %d C%d %d %d %d %d %d" fill="none" stroke="var(--mut)" stroke-width="1.4" marker-end="url(#ar)"/>' % (x1, y1 + H / 2, x1 - 14, y1 + H / 2, x2 + W + 14, y2 + H / 2, x2 + W, y2 + H / 2))
    for m in ms:
        x, y = pos[m['id']]
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="var(--card)" stroke="var(--c)" stroke-width="1.6"/><text x="%d" y="%d" class="fl">%s</text><text x="%d" y="%d" class="fs">%s</text>' % (
            x, y, W, H, x + W / 2, y + 18, E(m['id']), x + W / 2, y + 34, E(m['name'])))
    out.insert(1, '<defs><marker id="ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="var(--mut)"/></marker></defs>')
    out.append('</svg>')
    return '<div class="flowbox"><b>הזרימה — משימות שנפתחות יחד ונבחרות בכל סדר (D‑693):</b>%s</div>' % ''.join(out)

def opening():
    w = ''.join('<li>%s</li>' % E(t) for t in S.WHOAMI)
    dlg = S.DIALOGS['d-O-shimon']['rows']
    seq = ['a', 'w', 'y', 'r', 'b', 'c']
    bub = ''.join('<div class="bub"><span>%s</span>%s</div>' % ('שמעון' if k != 'a' else 'שמעון (בשדה / ליד הבית)', E(dlg[k]['text'])) for k in seq)
    svg = ('<svg viewBox="0 0 640 150" class="strip">'
           + ''.join('<g transform="translate(%d 10)"><rect width="140" height="120" rx="10" fill="var(--card)" stroke="#a5600b"/><text x="70" y="26" class="fl">%s</text><text x="70" y="50" class="fs">%s</text><text x="70" y="70" class="fs">%s</text><text x="70" y="102" class="fn">%s</text></g>' % (
               10 + i * 157, E(a), E(b), E(c), E(d)) for i, (a, b, c, d) in enumerate([
               ('שוט 1', 'הבית של סבא', 'פתיחה', '4.5 שנ׳'), ('שוט 2', 'אתה — הנכד של אהרן', 'באת מעבר לים', '3.4 שנ׳'),
               ('שוט 3', 'בית, טנדר ורשימה', 'התפקיד: לעבוד ולעזור', '3.4 שנ׳'), ('שוט 4', 'שמעון ליד הבית', 'מנופף — "כאן!"', '8.5 שנ׳')]))
           + '</svg>')
    return ('<section class="ch" style="--c:#a5600b"><h2>הפתיחה · מי אני, מאיפה באתי, למה אני פה, מה התפקיד</h2>'
            '<p class="goal">בסצנה הראשונה (O‑home — ארבעה שוטים, 20 שנ׳) ובשיחה הראשונה עם שמעון — ארבע שורות קצרות, לא טקסט ארוך. ביומן — כרטיס קבוע "מי אני" בארבע שורות.</p>'
            + svg + '<div class="two"><div><h3>השיחה הראשונה (d‑O‑shimon, משודרגת)</h3>%s</div><div><h3>הכרטיס ביומן: "מי אני"</h3><ul class="who4">%s</ul>'
            '<h3>המכתב של סבא (d‑O‑letter)</h3>%s</div></div></section>') % (bub, w, ''.join('<div class="bub"><span>המכתב</span>%s</div>' % E(r['text']) for r in S.DIALOGS['d-O-letter']['rows'].values()))

def ending():
    return ('<section class="ch" style="--c:#a5600b"><h2>סוף המשחק — ומה אחריו</h2><svg viewBox="0 0 640 140" class="strip">'
            + ''.join('<g transform="translate(%d 10)"><rect width="140" height="110" rx="10" fill="var(--card)" stroke="#a5600b"/><text x="70" y="28" class="fl">%s</text><text x="70" y="52" class="fs">%s</text><text x="70" y="72" class="fs">%s</text></g>' % (10 + i * 157, E(a), E(b), E(c)) for i, (a, b, c) in enumerate([
                ('המרינה בלילה', 'הזיקוקים והסירות', '"הסוף"'), ('המרפסת באי', 'סבא אהרן', 'V‑F‑06 — "לילה טוב"'), ('הכותרת', 'הרשימה של סבא — גמורה', 'העיר פתוחה'), ('חזרה לשחקן', 'המשחק ממשיך', 'בלי נעילות')]))
            + '</svg><ul class="who4"><li>אחרי הסוף: מצב "סיפור" נפתח כולו (TCSTORY: m.end → כל האזורים פתוחים), שום משימה של הסיפור לא נשארת פתוחה.</li>'
            '<li>ביומן: "הרשימה של סבא — גמורה" ו"מה עכשיו" — הקריירות, משימות הצד והסיפורים של האזורים, הליגה, הסירה והמסוק.</li>'
            '<li>סבא שולח מדי פעם הודעה מהאי — לכל היותר פעם ביום משחק, בערב (שש הודעות קצרות שמתחלפות).</li>'
            '<li>ברוך שולח אחרי הגמר את ההודעה המוקלטת לפי התוצאה האמיתית של הליגה (V‑F‑05א / V‑F‑05ב).</li></ul></section>')

FOUND = [
 ('מה יש היום', '074zd_story_data.js: TC_STORY — פתיחה (O‑1) ופרקים 1–4 (30 משימות); פרקים 5 ו-6 — רק שם ו"בקרוב" (missions:[]), אין פרק סיום.'),
 ('מה קורה כשפרק 4 נגמר', '074ze_story_engine.js:chapterEnd — עובר לפרק 5, ושם step() לא קורא שוב ל-chapterEnd כי אין משימות: הסיפור נשאר לתמיד בפרק 5 "בקרוב" (היומן: "פרק 5 · בקרוב"), והנעילה נשארת ברמה של פרק 4 (lvl). הסצנה 5‑soon מראה "בקרוב".'),
 ('התסריט', 'deliver/2026-11-10/story/tools/story_data.py — פרק 5 (8 משימות, הסערה), פרק 6 (7 משימות) וסיום "פסטיבל העיר" (4 משימות), עם 27 הודעות קוליות V‑5 / V‑6 / V‑F — וכולן כבר מוקלטות במשחק (074zf_story_vrec_data.js, ‏TCVREC_STORY).'),
 ('הנעילות', 'הטבלה (TC_STORY.locks) כבר נותנת לפרק 5: F6, הים הפתוח G5–H8, היער A0–B1; לפרק 6: האי G9 / H9 / F9 / E8 ו-A9–E9. ‏074zu_locks_phys.js:storyOpens — משימה פותחת לבד את האזורים שהצעדים שלה צריכים.'),
 ('מה משתמשים בו', 'שיחות (g77DlgAdd), עבודות של MISSION_DEFS עם רכב (כבאית VS‑FR‑01, גרר VS‑TW‑01, ניידת VS‑PL‑01, משאית VH‑TR‑01, האוטובוס M‑BUS‑01), סיפורי אזורים (S11‑ST‑A6, ‏S13‑ST‑F9, ‏S9‑ST‑F6), אימון הפנדלים של A4, הדיג, מבחן המסוק LIC‑16 (074zv_flight), מבחן האוטובוס LIC‑05, ההצגה בתיאטרון (TCSHOW), הגוררת של הנמל (S14), מזג האוויר (WEATHER.force — גשם בזמן הסערה), הסצנות (TC_CUTS) והדיוקנאות (TCPOR).'),
 ('מה חסר (ולכן נבנה)', 'נתוני הפרקים 5, 6 והסוף (חלק חדש 074zd2_story56_data.js); הסצנות, הסערה, היומן "מי אני" ואחרי הסוף (חלק חדש 074zw_story56_live.js); ב-074ze — שורה אחת של הרחבה (מצבים / תצפיות מבחוץ) ותיקון אחד בבדיקה: כשאין פרק "בקרוב" — הבדיקה מצפה לסוף (m.end).'),
]
APPROVE = [
 'תרופות לאי (5‑5): אין עדיין טיסה אוטומטית בין מנחתים — במקומה "מבט מהמסוק": רק המצלמה טסה מבית החולים לאי (שום כלי טיס לא מצויר), והשחקן נשאר ב-A2. כשתהיה טיסה בין מנחתים — הצעד הזה יהפוך לטיסה.',
 'המנחת בבית (5‑8): התודה של ראש העיר + רישיון המסוק (המבחן הקיים בשדה). המנחת בבית והמסוק הפרטי — לא נבנים כאן (זה של בית השחקן / house8).',
 'האימון (6‑2): 3 מתוך 5 במשחון הפנדלים הקיים (בתסריט: 5 מתוך 8 פנדלים וקליעות).',
 'הקטיף (6‑4): סיפור האזור "ארגז התפוחים לאי" (A6) — אם השחקן כבר עשה אותו כסיפור צד, הצעד הזה נסגר מיד (כמו בפרקים 2–4).',
 'הקו לפסטיבל (6‑7): קו 1 (אין עדיין עבודה של נהג בקו 6) — כמו שהתסריט אומר ב"מבוי סתום".',
 'הגמר באצטדיון והמצעד: לא נבנים כאן (arena / sealife); בערב הפסטיבל — ההצגה בתיאטרון והחברים על הטיילת.',
]

def main():
    css = ''':root{--bg:#f6f3ee;--card:#ffffff;--ink:#1d2731;--mut:#5d6b78;--ln:#c9c2b6;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141a20;--card:#1d252e;--ink:#e8eef3;--mut:#9fb0be;--ln:#3a4652;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141a20;--card:#1d252e;--ink:#e8eef3;--mut:#9fb0be;--ln:#3a4652;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "Segoe UI","Noto Sans Hebrew",Arial,sans-serif;direction:rtl}
main{max-width:1180px;margin:0 auto;padding:18px 16px 60px}h1{font-size:26px;margin:6px 0 2px}h2{font-size:20px;margin:0 0 6px;color:var(--c)}h3{font-size:15px;margin:12px 0 6px}
.sub{color:var(--mut);margin:0 0 16px}.ch{background:var(--card);border:1px solid var(--ln);border-top:5px solid var(--c);border-radius:12px;padding:14px 16px;margin:16px 0}
.goal{color:var(--mut);margin:0 0 10px}.two{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:16px}@media (max-width:860px){.two{grid-template-columns:1fr}}
.mi{border:1px solid var(--ln);border-radius:10px;padding:9px 11px;margin:0 0 10px}.mh{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}.who{color:var(--c);font-weight:700}
.mt{margin:3px 0}.ma{color:var(--mut);font-size:13px;margin-bottom:6px}table{width:100%;border-collapse:collapse;font-size:13px}th,td{border-top:1px solid var(--ln);padding:4px 6px;text-align:right;vertical-align:top}
th{color:var(--mut);font-weight:600}td.n{width:24px;font-weight:700;color:var(--c)}.grid{width:100%;max-width:320px;display:block}.gl{font-size:10px;fill:var(--mut);text-anchor:middle}.gn{font-size:10px;font-weight:700;fill:var(--ink);text-anchor:middle}
.note{font-size:12px;color:var(--mut)}.flowbox{margin:4px 0 12px;overflow-x:auto}.flow{min-width:420px;width:100%;max-height:260px}.fl{font-size:13px;font-weight:700;fill:var(--ink);text-anchor:middle}.fs{font-size:11px;fill:var(--mut);text-anchor:middle}.fn{font-size:11px;fill:#a5600b;text-anchor:middle}
.strip{width:100%;max-width:660px;display:block;margin:6px 0}.bub{border:1px solid var(--ln);border-radius:12px;padding:6px 10px;margin:0 0 6px;background:var(--bg)}.bub span{display:block;font-size:12px;color:var(--mut)}
.who4{margin:4px 0;padding-inline-start:18px}.who4 li{margin:3px 0}.found td:first-child{font-weight:700;white-space:nowrap;color:#a5600b}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.legend span{display:inline-flex;align-items:center;gap:5px;font-size:13px}.legend i{width:14px;height:14px;border-radius:3px;display:inline-block}'''
    legend = ''.join('<span><i style="background:%s"></i>%s</span>' % (CHC[k], NAMES[k]) for k in ['S', '1', '2', '3', '4', '5', '6'])
    found = '<section class="ch" style="--c:#a5600b"><h2>מה מצאתי (כלל 19)</h2><table class="found">%s</table></section>' % ''.join('<tr><td>%s</td><td>%s</td></tr>' % (E(a), E(b)) for a, b in FOUND)
    appr = '<section class="ch" style="--c:#a5600b"><h2>לאישורך — מה שונה מהתסריט ולמה</h2><ul class="who4">%s</ul></section>' % ''.join('<li>%s</li>' % E(t) for t in APPROVE)
    body = ''.join([
        '<main><h1>לוח הסיפור · פרקים 5 ו-6 והסוף</h1><p class="sub">story56 · 17.11 · הציור לפני הבנייה (כלל 13 / 20). הפתיחה ברורה, פרק 5 "העיר צריכה אותך", פרק 6 "העיר שלי", והסוף "פסטיבל העיר" — עד שהמשחק גמור וממשיך חופשי.</p>',
        '<div class="legend">%s</div>' % legend, found, opening(),
        chapter(S.CH5, flow(S.CH5)), chapter(S.CH6, flow(S.CH6)), chapter(S.CHF, flow(S.CHF)), ending(), appr,
        '<p class="note">הבדיקה החוסמת: הסיפור כולו משמירה נקייה (הפתיחה עד הסוף, 0 שגיאות, סצנת הסיום), כל צעד במקום שקיים, באזור פתוח באותו שלב ומחובר מהבית (TCLOCK.reach) — ועוד הסט הקבוע.</p></main>'])
    doc = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>לוח הסיפור 5–6</title><style>%s</style></head><body>%s</body></html>' % (css, body)
    open(OUT, 'w', encoding='utf-8').write(doc)
    print(OUT, len(doc.encode('utf-8')))
main()
