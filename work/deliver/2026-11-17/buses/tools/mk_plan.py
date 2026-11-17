#!/usr/bin/env python3
# mk_plan.py — הציור (כלל 13): מפת השכבות של האוטובוסים מעל V2, והמדידה (q_busbeh) — בסיס מול הניסיון. SVG בקוד, בלי תמונות.
import json, sys, os, html, datetime
Q = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/buses/qa'
OUT = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/buses/Buses_plan.html'
def J(n):
    p = os.path.join(Q, n)
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return None
base, new = J(sys.argv[1]) if len(sys.argv) > 1 else None, J(sys.argv[2]) if len(sys.argv) > 2 else None
E = html.escape
LAYERS = [
 # (שכבה, איפה, מה עושה לאוטובוס, מה עושה מכונית באותו מצב, הקביעה)
 ('הפרופיל "bus" של V2 — מרווח 1.35, עצירה בשפה, המסוף הישן, airport4, שומר הקיפאון', '071: routeSegments2 / stopPoint2 / externalCap2 / busCurb2 / busTick / busFreezeWatch2; 056:217', 'לא רץ: BUS_LINES_PAUSED=true מרוקן את BUS_VEHICLES (0 אוטובוסים); כ-30 חלקים קוראים את הרשימה הריקה', '—', 'שריד כבוי. ברירת המחדל: נשאר כבוי ולא נמחק (כלל 2); לא מחברים את LN אליו — מי שמתקן אוטובוסים מתקן ב-LN (074f ומעליו, ‏074zu)'),
 ('המנוע של הקווים LN — כל קווים 1–6 (גם הקואץ׳ של קו 5 וקו 4 של השדה)', '074f + 074n (2, 6) + 074t (4) + 074l5 (5)', 'רכב של V2 בפרופיל c5 (כמו משאית אספקה) בכביש; מחוץ ל-V2 בדרך משלו (ln-path) במפרץ, בשער, במסוף ובחניון', 'רכב של V2 בפרופיל car', 'הדרך האחת'),
 ('bend — עצירה לפני פנייה חדה בצומת מעבר', '074p (8): holdLines2 / leBendLanes', 'עוצר כל עוד יש רכב כלשהו עד 260 פיקס׳ בנתיב שממול — גם עומד ורחוק, שלא נוגע בגוף', 'אין כלל כזה: נוסעת, ונעצרת רק בגוף שלפניה (hardBlock2)', 'עצירה בלי סיבה כשהרכב ממול עומד מחוץ לגוף. תוקן: 074zu (3) — עוצר רק כשיש מי שייפגש עם הגוף; ובלי תקרה — היה: אחרי 30 שנ׳ רצופות מול רכב שעומד בשטח של הגוף, הרכב נסוג (השחרור של המנוע), בלי שהאוטובוס נכנס לגוף'),
 ('bay-full — לא נכנס לצומת כשהמפרץ שאחריו תפוס', '074p (2): movementReady2; ‏074n; ‏074l5', 'מחכה בקו העצירה של הצומת', 'V2: לא נכנסת לצומת בלי מקום ביציאה (gate:space)', 'משלים (המפרץ מחוץ לנתיב)'),
 ('rb-bus — מי שנכנס לכיכר מחכה לגוף של האוטובוס', '074j: lcRbBusYield (מ-rbYield2)', 'האחרים מחכים לו', 'V2: נותנת זכות למי שבטבעת', 'משלים (הגוף הארוך)'),
 ('היציאה מהמפרץ — פער בנתיב', '074f: lnMergeBy (+ lcBayHold / lcBayHoldGate של 074j)', 'מחכה לפער של 280 פיקס׳ ממי שנוסע, 40 ממי שעומד', 'V2: laneChangeClear2 — מרווח + 1.2 שנ׳ ממי שמאחור', 'כפול לכלל של V2 — בכלי אחר; נשאר (האוטובוס מחוץ לנתיב, ו-V2 לא יודע להכניס אותו)'),
 ('הנסיעה בדרך משלו — "המתנה הדדית, האוטובוס ראשון"', '074f: lnDrive (B.ign אחרי 8 שנ׳) + lcCycleGo (074j)', 'אחרי 8 שנ׳ מול מכונית עומדת — עובר דרך הגוף שלה', 'V2: לא עוברת דרך גוף; נסיגה (backout / laneBack)', 'דחיפה — עובר דרך מכונית. תוקן: 074zu (4) — מכונית שמחכה לרמזור / להולך רגל / בנסיגה: האוטובוס מחכה לה כמו מכונית (עד 40 שנ׳); המתנה הדדית: המכונית נסוגה בשחרור של המנוע (laneBack + השרשרת (19), ‏backout); המעבר דרך הגוף — רק כמוצא אחרון (אחרי 30 שנ׳ בהמתנה הדדית, 70 מול מכונית שמחכה לדבר שלה), נספר, היעד 0'),
 ('המסוף E3 — נעילות W / X / Y, רציפים, מרווח', '074g / 074h / 074p (9, 10, 14, 16, 17)', 'מחכה לנעילה / לרציף / למרווח', '—', 'של הקווים בלבד'),
 ('תווית ההמתנה waitBy', '074f / 074g / 074j / 074p', 'נקבעת ואף פעם לא יורדת (חוץ משתיים) — תווית ישנה ב-F9 ובבדיקות; 074p (12) קורא אותה', '—', 'תוקן: 074zu'),
]
RELEASE = [
 ('backout — נסיגה מצומת', '071: backoutStep2 (BACKOUT_AFTER 12 שנ׳) + 074p (15)', 'כל רכבי V2 (גם אוטובוס הקווים בכביש)'),
 ('ghost_yield + laneBack — נסיגה מרוח של רכב מערכת', '071: ghostYield2 (אחרי 3 שנ׳, 44 פיקס׳) / laneBackStep2', 'מכוניות מול אוטובוס בדרך משלו, מכלית, משאית'),
 ('הנסיגה בשרשרת (19)', '074p: laneBackStep2 — מבקש גם ממי שמאחור', 'מכוניות'),
 ('keep-clear — אזורים שלא עוצרים בהם', '071: keepClearOk2 (closures2)', 'כל רכבי V2'),
 ('"האוטובוס ראשון" — מעבר דרך הגוף', '074f: lnDrive (B.ign) / 074j: lcCycleGo; ‏074zu (4) — מכונית: רק כמוצא אחרון אחרי 30 / 70 שנ׳ (נספר); לפני כן — הנסיגה של המנוע', 'אוטובוסי הקווים בדרך משלהם'),
 ('שומר הקיפאון של האוטובוסים', '071: busFreezeWatch2', 'לא רץ (BUS_VEHICLES ריק)'),
]
def svg():
    W, H = 760, 430
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="השכבות של האוטובוסים מעל מנוע הכבישים" class="dia">']
    def box(x, y, w, h, t, sub='', cls='b'):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="{cls}"/>')
        s.append(f'<text x="{x+w/2}" y="{y+22}" class="t">{E(t)}</text>')
        for i, line in enumerate(sub.split('\n') if sub else []):
            s.append(f'<text x="{x+w/2}" y="{y+42+i*17}" class="s">{E(line)}</text>')
    box(250, 20, 260, 120, 'V2 — מנוע הכבישים (071)', 'מכוניות · מוניות · משאיות · אוטובוסי הקווים\nתורים, שערים, רמזורים, keep-clear\nhardBlock2 · backout · ghost_yield', 'core')
    box(20, 20, 200, 120, 'הפרופיל "bus" הישן', 'BUS_VEHICLES = 0\nBUS_LINES_PAUSED (056)\nשריד — לא רץ', 'dead')
    box(540, 20, 200, 120, 'LN — הקווים 1–6', 'בפרופיל c5 בכביש\n074f · 074n · 074t · 074l5\n(קואץ׳ קו 5, קו 4 של השדה)', 'ln')
    s.append('<line x1="540" y1="80" x2="512" y2="80" class="ar"/>')
    s.append('<line x1="220" y1="80" x2="248" y2="80" class="arx"/>')
    hooks = [('bend', '074p (8)', 'עוצר בלי סיבה'), ('bay-full', '074p (2)', 'משלים'), ('rb-bus', '074j', 'משלים'), ('מפרץ: פער', '074f', 'כפול'), ('המסוף W/X/Y', '074g/p', 'של הקווים'), ('"ראשון" — דרך הגוף', '074f', 'דוחף')]
    for i, (a, b, c) in enumerate(hooks):
        x = 20 + (i % 3) * 245; y = 175 + (i // 3) * 95
        cls = 'warn' if c in ('עוצר בלי סיבה', 'דוחף') else ('dup' if c == 'כפול' else 'ok')
        box(x, y, 230, 80, a, b + '\n' + c, cls)
        s.append(f'<line x1="{x+115}" y1="{y}" x2="{380 if i<3 else 640}" y2="{142}" class="thin"/>')
    s.append(f'<text x="380" y="{H-14}" class="s">אדום — שם האוטובוס מתנהג אחרת מהמכונית בלי צורך · צהוב — כלל כפול לכלל של V2 · ירוק — משלים (הגוף הארוך)</text>')
    s.append('</svg>')
    return '\n'.join(s)
def meas(R, label):
    if not R: return f'<p class="muted">{E(label)}: עוד לא נמדד.</p>'
    sh = R.get('share') or {}
    rows = ''.join(f'<tr><td>{E(k)}</td><td>{v["n"]}</td><td>{round(100*v["stopShare"])}%</td><td>{v["bend"]}</td><td>{v["rbYieldToBus"]}</td><td>{v["ghostYield"]}</td><td>{v["laneBack"]}</td><td>{v["backout"]}</td></tr>' for k, v in sorted(sh.items()))
    lg = R.get('longest') or {}
    lrows = ''.join(f'<tr><td>{E(k)}</td><td>{v["s"]}</td><td>{E(str(v["why"]))}</td><td>{E(str(v["id"]))}</td><td>{E(str(v.get("lane")))}</td></tr>' for k, v in sorted(lg.items()))
    bk = R.get('bendBlocker') or {}
    bks = ' · '.join(f'{E(k)}: {v}' for k, v in bk.items()) or '—'
    bf = R.get('busFirst') or {}; au = R.get('aud') or {}; fs = (au.get('first') if isinstance(au, dict) else None) or {}
    bfs = f'"האוטובוס ראשון" — מעבר דרך מכונית: {bf.get("n", "?")} פעמים' + (f' · המתנה במקום מעבר: {fs.get("hold", 0)} (נגמרו כשהמכונית נסעה / נסוגה: {fs.get("free", 0)}, בקשות נסיגה: {fs.get("backReq", 0)}, מעבר כמוצא אחרון: {fs.get("passN", 0)})' if fs else '')
    return (f'<h3>{E(label)} — {E(R["build"])} · {R["secs"]} שנ׳ משחק ({E(str(R.get("clk0")))}–{E(str(R.get("clk1")))})</h3>'
            f'<p>{E(bfs)}</p>'
            f'<div class="tw"><table><tr><th>סוג</th><th>רכבים</th><th>זמן עמידה</th><th>bend</th><th>rb-bus</th><th>ghost_yield</th><th>laneBack</th><th>backout</th></tr>{rows}</table></div>'
            f'<p>מי עצר את האוטובוס ב-bend (טיקים): {bks}</p>'
            f'<div class="tw"><table><tr><th>סוג</th><th>העמידה הארוכה (שנ׳)</th><th>הסיבה</th><th>רכב</th><th>נתיב / שלב</th></tr>{lrows}</table></div>')
REV = [
 ('1. "האוטובוס ראשון" — לא דרך הגוף', 'תוקן (074zu (4), ‏80654ab): מכונית שמחכה לדבר שלה — האוטובוס מחכה לה כמו מכונית (עד 40 שנ׳); המתנה הדדית / סיבה לא ידועה / אחרי 40 שנ׳ — המכונית נסוגה בשחרור של המנוע (laneBack + השרשרת (19) של 074p; בצומת — backout), בקשה כל 6 שנ׳; המעבר דרך הגוף — רק כמוצא אחרון אחרי 120 שנ׳ בלי תזוזה, נספר (BSV.passN) — היעד 0 בלילה של הקווים.'),
 ('2. המדידה', 'q_busbeh — הבסיס S7F299 מול הניסיון, לכל קו: זמן העמידה והסיבות (הטבלה למטה); ‏stuckmax 1500 והלילה של הקווים — בהחזרה.'),
 ('3. אוטובוס תקוע', 'עותק מתוקן: deliver/2026-11-17/buses/tools/stuckmax_bus.js — אותה ספירה של stuckmax.js, ועוד אוטובוסי הקווים לפי המקום (לא לפי v.stuck); בדיקה חוסמת אצלי. הכלי המשותף צריך את התיקון — בהחזרה.'),
 ('4. השריד', 'ברירת המחדל: נשאר כבוי (BUS_LINES_PAUSED של הבעלים, p475) ולא נמחק; ‏BUS_VEHICLES ריק, וכ-30 החלקים שקוראים אותו עוברים על רשימה ריקה. לא מחברים את LN אליו — מתקנים אוטובוסים ב-LN (074f ומעליו, ‏074zu).'),
 ('5. האי (קווים 5 ו-5א)', 'LN נוסע בכביש ב-V2 לפי מסלול של קטעים (c5.route) — לולאה סופית חד-סטרית היא מסלול, בלי ראש סיבוב (כך כבר היום: הלולאה של ST-21 / ‏ISE-0, ‏074l5 / ‏074l7). ההמתנה של 30 שנ׳ במפרץ של הלולאה — שלב ‏bay (layover), לא בשלבי הנסיעה ש-LN.aud.frz סופר. הגשר המתרומם: הקואץ׳ בכביש עוצר במחסומים כמו כל רכב; המחזור 10+40+10+40 = ~100 שנ׳ עצירה, פחות מ-180 של LN.aud.frz — לא נספר כקיפאון; ב-stuckmax_bus נרשם מצב הגשר ליד כל עמידה. תלות: island.'),
 ('6. חזית הטרמינל (pier)', 'bay-full (074p (2)) סופר רק אוטובוסים של הקווים במפרץ (lnBayFree, ‏074f) — רכב של השחקן במפרץ לא נועל את הקו בצומת; ליד המפרץ עצמו האוטובוס מחכה לגוף של השחקן (lnDrive לא עובר אף פעם דרך PLAYER-CAR). תלות: pier.'),
]
def compare(B, N):
    if not B or not N: return '<p class="muted">ההשוואה — כשיש את שתי ההרצות.</p>'
    def top(R, t):
        L = (R.get('reasons') or {}).get(t) or []
        return ' · '.join(f'{E(str(w))} {c}' for w, c in L[:4]) or '—'
    ts = sorted(set(k for k in list((B.get('share') or {}).keys()) + list((N.get('share') or {}).keys()) if k.startswith('ln') or k in ('coach5', 'car', 'taxi')))
    rows = ''
    for t in ts:
        b = (B.get('share') or {}).get(t) or {}; n = (N.get('share') or {}).get(t) or {}
        rows += f'<tr><td>{E(t)}</td><td>{b.get("stopS", "—")}</td><td>{n.get("stopS", "—")}</td><td>{round(100*b.get("stopShare",0))}% → {round(100*n.get("stopShare",0))}%</td><td class="code">{top(B, t)}</td><td class="code">{top(N, t)}</td></tr>'
    return f'<h3>בסיס מול ניסיון — לכל קו: שניות עמידה (סכום על כל הרכבים מהסוג) והסיבות העיקריות</h3><div class="tw"><table><tr><th>סוג</th><th>הבסיס (שנ׳)</th><th>הניסיון (שנ׳)</th><th>חלק העמידה</th><th>הסיבות — הבסיס</th><th>הסיבות — הניסיון</th></tr>{rows}</table></div>'

def rbsec():
    import os
    Qd = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/buses/qa/'
    def L(n):
        try: return json.load(open(Qd + n, encoding='utf-8'))
        except Exception: return None
    B = L('rb_base299d.json') or L('rb_base299.json'); N = L('rb_try6932.json')
    names = {'J12_25': 'כיכר הספורט (ליד האצטדיון)', 'J12_42': 'כיכר העיר (LC-SQ-E)', 'J25_08': 'כיכר הכפר', 'IL': 'כיכר האי (island)'}
    rows = ''
    for id in ['J12_25', 'J12_42', 'J25_08', 'IL']:
        b = ((B or {}).get('rb') or {}).get(id) or {}; n = ((N or {}).get('rb') or {}).get(id) or {}
        lb = (b.get('longest') or [[None]])[0][0] if b.get('longest') else 0; ln_ = (n.get('longest') or [[None]])[0][0] if n.get('longest') else (0 if n else '—')
        rows += (f'<tr><td>{E(names[id])}</td><td>{b.get("vehicles","—")} → {n.get("vehicles","—")}</td><td>{b.get("stops5","—")} → {n.get("stops5","—")}</td>'
                 f'<td>{b.get("stops30","—")} → {n.get("stops30","—")}</td><td>{lb} → {ln_}</td><td>{round(100*b.get("stopShare",0)) if b else "—"}% → {round(100*n.get("stopShare",0)) if n else "—"}%</td></tr>')
    sv = (
     '<svg class="dia" viewBox="0 0 640 400" role="img" aria-label="כיכר הספורט: ארבע הזרועות, כיוון הטבעת, הכניסה מדרום שחיכתה, והתור ההוגן">'
     '<rect class="core" x="290" y="0" width="60" height="400"/><rect class="dup" x="0" y="170" width="640" height="60"/>'
     '<circle cx="320" cy="200" r="92" fill="var(--bg)" stroke="var(--line)" stroke-width="2"/><circle cx="320" cy="200" r="58" fill="none" stroke="var(--acc)" stroke-width="2" stroke-dasharray="7 6"/>'
     '<circle cx="320" cy="200" r="34" class="ok" stroke="var(--line)"/><text class="s" x="320" y="204">אי</text>'
     '<path class="ar" fill="none" d="M 262 190 A 58 58 0 0 0 312 258"/><path class="ar" fill="none" d="M 330 258 A 58 58 0 0 0 378 208"/><path class="ar" fill="none" d="M 376 186 A 58 58 0 0 0 328 142"/><path class="ar" fill="none" d="M 310 142 A 58 58 0 0 0 264 186"/>'
     '<text class="t" x="320" y="24">B3-CLW-S — הציר הראשי, צפון</text><text class="t" x="320" y="392">B4-CLW-N — הציר הראשי, דרום</text>'
     '<text class="t" x="70" y="160">A3-RD — האצטדיון</text><text class="t" x="566" y="160">B3-LCSCH</text>'
     '<rect class="warn" x="330" y="300" width="22" height="56"/><text class="s" x="452" y="318">הכניסה מדרום — בבסיס: עד 86 שנ׳</text><text class="s" x="452" y="336">(אוטובוסים של קו 6, ‏rb-yield)</text>'
     '<rect class="warn" x="150" y="176" width="22" height="22"/><rect class="warn" x="330" y="76" width="22" height="22"/><rect class="warn" x="468" y="202" width="22" height="22"/><rect class="warn" x="334" y="282" width="14" height="14"/>'
     '<text class="s" x="150" y="252">ריבוע אדום קטן — רמזור כניסה (הצעה, לאישורך)</text>'
     '<line class="arx" x1="172" y1="208" x2="300" y2="300"/><text class="s" x="196" y="300">התור ההוגן: הכניסה שלפני (מערב / צפון)</text><text class="s" x="196" y="316">עוצרת לרגע כשהדרומית מחכה ראשונה 6 שנ׳</text>'
     '</svg>')
    return (f'<h2>הכיכרות בכבישים הראשיים (הבעלים 17.11 ~10:45)</h2>'
            f'<p>בצומת רגיל של V2 יש תור הוגן (tryGrant2: מי שמחכה ראשון ותנועה שלו מתנגשת בשלי — נכנס לפניי). בכיכר, rbRebuild2 מוחק את ההתנגשויות של כל התנועות, ולכן התור ההוגן לא חל: כניסה שהזרם בטבעת עובר מולה מחכה בלי סוף. התיקון (074zu (6)): אותו תור הוגן גם בכיכר — לפי הכניסות שהדרך שלי בטבעת עוברת מולן.</p>'
            f'{sv}<h3>לפני → אחרי (q_rb.js, ‏1500 שנ׳ במהירות; הבסיס S7F299 → try6932, המיזוג של S7F302)</h3><div class="tw"><table><tr><th>הכיכר</th><th>רכבים</th><th>עמידות מעל 5 שנ׳</th><th>מעל 30</th><th>הארוכה (שנ׳)</th><th>זמן בעמידה</th></tr>{rows}</table></div>'
            f'<p class="muted">רמזור כניסה (הצעה, לאישורך): אם כיכר הספורט לא נשארת זורמת — מנורה לכל כניסה לפני המעבר, אדום לזרוע שלפני כניסה שמחכה מעל 15 שנ׳ (לפי התור). היום הבדיקה p573_roundabouts_as_the_map (058) אוסרת רמזור בכיכר.</p>')
now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
L = ''.join(f'<tr><td>{E(a)}</td><td class="code">{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td><b>{E(e)}</b></td></tr>' for a, b, c, d, e in LAYERS)
Rr = ''.join(f'<tr><td>{E(a)}</td><td class="code">{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in RELEASE)
page = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>מפת האוטובוסים</title><style>
:root{{--bg:#f7f6f2;--fg:#1d1d1b;--mut:#6b6a64;--line:#d9d6cc;--core:#e6eefb;--ln:#e7f5ea;--dead:#eeeeee;--warn:#fde3df;--dup:#fff4cf;--ok:#e3f3e6;--acc:#2f6fd0}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#17181a;--fg:#ecebe6;--mut:#a3a199;--line:#3a3a38;--core:#1f2d44;--ln:#1e3526;--dead:#2a2a2a;--warn:#4a2522;--dup:#463c1c;--ok:#1f3a26;--acc:#7aa7ff}}}}
:root[data-theme="dark"]{{--bg:#17181a;--fg:#ecebe6;--mut:#a3a199;--line:#3a3a38;--core:#1f2d44;--ln:#1e3526;--dead:#2a2a2a;--warn:#4a2522;--dup:#463c1c;--ok:#1f3a26;--acc:#7aa7ff}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,sans-serif;margin:0;padding:16px;max-width:980px;margin-inline:auto}}
h1{{font-size:22px;margin:8px 0}} h2{{font-size:18px;margin-top:28px}} h3{{font-size:15px}} .muted{{color:var(--mut)}}
.dia{{width:100%;height:auto;display:block}} .dia rect{{stroke:var(--line);stroke-width:1.5}} .dia .core{{fill:var(--core)}} .dia .ln{{fill:var(--ln)}} .dia .dead{{fill:var(--dead);stroke-dasharray:6 4}}
.dia .warn{{fill:var(--warn)}} .dia .dup{{fill:var(--dup)}} .dia .ok{{fill:var(--ok)}} .dia .t{{font-weight:700;font-size:14px;text-anchor:middle;fill:var(--fg)}} .dia .s{{font-size:12px;text-anchor:middle;fill:var(--mut)}}
.dia .ar{{stroke:var(--acc);stroke-width:3}} .dia .arx{{stroke:var(--mut);stroke-width:2;stroke-dasharray:4 4}} .dia .thin{{stroke:var(--line);stroke-width:1}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:13.5px}} td,th{{border-bottom:1px solid var(--line);padding:6px;text-align:right;vertical-align:top}} th{{color:var(--mut);font-weight:600}}
.code{{font-family:ui-monospace,monospace;font-size:12px;direction:ltr;text-align:left;unicode-bidi:plaintext}}
</style></head><body>
<h1>מפת האוטובוסים</h1>
<p class="muted">סבב 17.11 · buses · הבסיס S7F299 (int299 930919a) · עודכן {now:%H:%M} · הבעלים 12.11 01:40: "יותר פושים ופחות זהירים איפה שצריך, ועוצרים סתם איפה שלא צריך".</p>
<h2>השכבות — מי מזיז את האוטובוס, ומה מעליו</h2>
{svg()}
<h2>כל שכבה מול מה שמכונית עושה באותו מצב</h2>
<div class="tw"><table><tr><th>השכבה</th><th>איפה</th><th>האוטובוס</th><th>מכונית (V2)</th><th>הקביעה</th></tr>{L}</table></div>
<h2>מנגנוני השחרור בפקק</h2>
<div class="tw"><table><tr><th>המנגנון</th><th>איפה</th><th>על מי</th></tr>{Rr}</table></div>
<h2>הערות הבקר (planrev 07:35) — מה נעשה</h2>
<div class="tw"><table><tr><th>ההערה</th><th>מה נעשה</th></tr>{''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b in REV)}</table></div>
<h2>המדידה — האוטובוסים מול המכוניות</h2>
<p class="muted">הרצה מהירה בתוך המשחק (q_busbeh.js): כל שנייה — כל רכב בכביש, הסוג, האם עומד ולמה. "ln1"–"ln6" — אוטובוסי הקווים לפי קו, "coach5" — הקואץ׳ של קו 5.</p>
{compare(base, new)}
{meas(base, 'הבסיס')}
{meas(new, 'הניסיון')}
{rbsec()}
</body></html>'''
open(OUT, 'w', encoding='utf-8').write(page); print(OUT, len(page))
