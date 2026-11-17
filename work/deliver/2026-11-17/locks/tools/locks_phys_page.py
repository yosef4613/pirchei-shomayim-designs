#!/usr/bin/env python3
# locks_phys_page.py <out.html> — הציור (כלל 13) של הנעילה הפיזית והניווט החוקי (locks, 17.11). מעל Story_locks_plan.html של 11.11 (כלל 19א). SVG בקוד בלבד, בלי תמונות.
import sys, os, html, hashlib
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-11/story/tools'); import story_locks as L
E = html.escape
COL = {'S': '#2e7d4f', '1': '#2f6fd0', '2': '#a5600b', '3': '#6a3fb5', '4': '#127a8a', '5': '#b2453b', '6': '#55606b'}
ORD = ['S', 'O', '1', '2', '3', '4', '5', '6']
cw, chh, ox, oy = 34, 24, 18, 18
import json
ZONE_ORIG = dict(L.ZONE_CH); L.ZONE_CH['E3'] = '1'; L.ZONE_CH['F7'] = '5'   # 17.11 (ד): E3 נפתח עם D3 (פרק 1) — כמו במשחק (074zu: REACH_FIX), לאישורך
RJ = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else None
if RJ and 'result' in RJ: RJ = RJ['result']
def open_at(z, stage):  # stage: the chapter now ('O'..'4'); a chapter that is not built ('5','6' — בקרוב) — like the last built one (D‑17.11)
    c = L.ZONE_CH[z]
    return c == 'S' or ORD.index(stage) >= ORD.index(c)
def stage_svg(stage, title, marks=None, orig=False):
    ZC = ZONE_ORIG if orig else L.ZONE_CH
    op_at = (lambda z, st: ZC[z] == 'S' or ORD.index(st) >= ORD.index(ZC[z]))
    W, H = ox + 8 * cw + 6, oy + 10 * chh + 6
    s = ['<figure class="mapf"><svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="width:100%%;height:auto;direction:ltr">' % (W, H, E(title))]
    s.append('<defs><pattern id="h%s" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#20262d"/><line x1="0" y1="0" x2="0" y2="6" stroke="#39424c" stroke-width="2"/></pattern></defs>' % stage)
    for i, c in enumerate('ABCDEFGH'): s.append('<text x="%d" y="12" text-anchor="middle" font-size="9" fill="currentColor">%s</text>' % (ox + i * cw + cw / 2, c))
    for r in range(10):
        s.append('<text x="8" y="%d" text-anchor="middle" font-size="9" fill="currentColor">%d</text>' % (oy + r * chh + chh / 2 + 3, r))
        for i, c in enumerate('ABCDEFGH'):
            z = c + str(r); k = ZC[z]; x, y = ox + i * cw, oy + r * chh; op = op_at(z, stage)
            s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="%s" opacity="%s"/>' % (x + .5, y + .5, cw - 1, chh - 1, COL[k] if op else 'url(#h%s)' % stage, '.9' if op else '1'))
            s.append('<text x="%d" y="%d" text-anchor="middle" font-size="8" fill="%s">%s</text>' % (x + cw / 2, y + chh / 2 + 3, '#fff' if op else '#ffd36a', z if op else z + '·' + k))
    # the wall: every side between an open zone and a locked zone
    for r in range(10):
        for i, c in enumerate('ABCDEFGH'):
            z = c + str(r)
            if not op_at(z, stage): continue
            x, y = ox + i * cw, oy + r * chh
            for di, dr, x1, y1, x2, y2 in [(1, 0, x + cw, y, x + cw, y + chh), (-1, 0, x, y, x, y + chh), (0, 1, x, y + chh, x + cw, y + chh), (0, -1, x, y, x + cw, y)]:
                ni, nr = i + di, r + dr
                if 0 <= ni < 8 and 0 <= nr < 10 and not op_at('ABCDEFGH'[ni] + str(nr), stage):
                    s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#ffb020" stroke-width="2.6" stroke-dasharray="4 2" stroke-linecap="round"/>' % (x1, y1, x2, y2))
    if marks:
        for r in range(10):
            for i, c in enumerate('ABCDEFGH'):
                z = c + str(r); x, y = ox + i * cw, oy + r * chh
                if z in marks.get('cut', []):
                    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#ff3b3b" stroke-width="3"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ff3b3b" stroke-width="2.5"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ff3b3b" stroke-width="2.5"/>' % (x + 1.5, y + 1.5, cw - 3, chh - 3, x + 4, y + 4, x + cw - 4, y + chh - 4, x + cw - 4, y + 4, x + 4, y + chh - 4))
                elif z in marks.get('reached', []):
                    s.append('<circle cx="%d" cy="%d" r="2.6" fill="#b8ffcf"/>' % (x + cw - 5, y + 5))
        for (a1, a2) in marks.get('corr', []):
            (i1, r1), (i2, r2) = [('ABCDEFGH'.index(q[0]), int(q[1])) for q in (a1, a2)]
            s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#7CFFB2" stroke-width="3.2" stroke-linecap="round" marker-end="url(#ar%s)"/>' % (ox + i1 * cw + cw / 2, oy + r1 * chh + chh / 2, ox + i2 * cw + cw / 2, oy + r2 * chh + chh / 2, stage))
        s.insert(2, '<defs><marker id="ar%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7CFFB2"/></marker></defs>' % stage)
    s.append('</svg><figcaption>%s</figcaption></figure>' % E(title))
    return ''.join(s)
maps = ''.join(stage_svg(st, t) for st, t in [('O', 'פתיחה — הבית של סבא'), ('1', 'פרק 1 — העיר'), ('2', 'פרק 2 — מאחורי הקלעים'), ('3', 'פרק 3 — השמיים'), ('4', 'פרק 4 — הים · וגם כשפרק 5 / 6 "בקרוב"')])
leg = ''.join('<span class="chip" style="background:%s;color:#fff">%s</span>' % (COL[k], E(L.NAMES[k])) for k in ['S', '1', '2', '3', '4', '5', '6']) + '<span class="chip" style="background:#20262d;color:#ffd36a">נעול (פ׳ N)</span><span class="chip" style="background:transparent;border:2px dashed #ffb020">הקיר — גבול שאי אפשר לעבור</span>'
# the 3/4 sketch of the edge of a locked zone (rule 13: what the player sees)
sketch = '''<svg viewBox="0 0 640 300" role="img" aria-label="הגבול של אזור נעול במבט 3/4" style="width:100%;max-width:640px;height:auto;direction:ltr">
<rect width="640" height="300" fill="#5b7f4e"/>
<polygon points="0,140 640,110 640,190 0,220" fill="#4a4f55"/><polygon points="0,132 640,102 640,110 0,140" fill="#9aa1a8"/><polygon points="0,220 640,190 640,198 0,228" fill="#9aa1a8"/>
<line x1="0" y1="180" x2="640" y2="150" stroke="#e8e4d0" stroke-width="3" stroke-dasharray="18 14"/>
<rect x="355" y="0" width="285" height="300" fill="#0b1118" opacity=".34"/>
<line x1="350" y1="0" x2="362" y2="300" stroke="#ffb020" stroke-width="6" stroke-dasharray="16 10" opacity=".95"/>
<line x1="350" y1="0" x2="362" y2="300" stroke="#ffe7a8" stroke-width="1.5" opacity=".8"/>
<g transform="translate(336,62)"><rect x="-2" y="0" width="4" height="40" fill="#6d737a"/><rect x="-46" y="-26" width="92" height="30" rx="5" fill="#1c2733" stroke="#ffb020" stroke-width="2"/><text x="0" y="-12" font-size="11" fill="#ffd36a" text-anchor="middle" font-weight="700">נעול · פרק 2</text><text x="0" y="0" font-size="9" fill="#e8eef4" text-anchor="middle">D4 — רק לעובדים</text></g>
<g transform="translate(300,171) rotate(-2.7)"><rect x="-34" y="-13" width="68" height="26" rx="7" fill="#c8372d"/><rect x="-18" y="-11" width="30" height="22" rx="4" fill="#9fd2ff" opacity=".85"/><rect x="-34" y="-13" width="68" height="26" rx="7" fill="none" stroke="#7d1f19" stroke-width="2"/></g>
<g transform="translate(212,222)"><circle r="6" fill="#f0c39a"/><rect x="-5" y="5" width="10" height="16" rx="3" fill="#2f6fd0"/></g>
<g transform="translate(150,22)"><rect x="0" y="0" width="300" height="44" rx="10" fill="#0c1620" opacity=".92" stroke="#8a5a12"/><text x="150" y="18" font-size="12" fill="#ffd36a" text-anchor="middle" font-weight="700">אזור נעול (D4) · נפתח בפרק 2 — מאחורי הקלעים</text><text x="150" y="34" font-size="10" fill="#eef5fa" text-anchor="middle">יוסף מתחנת הכוח יפתח לך את השער (פרק 2)</text></g>
<text x="500" y="260" font-size="13" fill="#ffd36a" text-anchor="middle">הצד הנעול — מוחשך מעט</text><text x="160" y="270" font-size="13" fill="#fff" text-anchor="middle">הצד הפתוח</text>
</svg>'''
# the legal route (a sketch): home C3 → B2 in chapter 1 — not through C1 / B1
route = '''<svg viewBox="0 0 420 260" role="img" aria-label="ניווט חוקי: המסלול עוקף אזור נעול" style="width:100%;max-width:420px;height:auto;direction:ltr">
<g font-size="11" text-anchor="middle">
<rect x="10" y="10" width="130" height="80" fill="url(#hR)"/><rect x="140" y="10" width="130" height="80" fill="url(#hR)"/><rect x="270" y="10" width="130" height="80" fill="url(#hR)"/>
<rect x="10" y="90" width="130" height="80" fill="#2f6fd0" opacity=".85"/><rect x="140" y="90" width="130" height="80" fill="#2f6fd0" opacity=".85"/><rect x="270" y="90" width="130" height="80" fill="#2e7d4f" opacity=".85"/>
<rect x="10" y="170" width="130" height="80" fill="#2f6fd0" opacity=".85"/><rect x="140" y="170" width="130" height="80" fill="#2e7d4f" opacity=".85"/><rect x="270" y="170" width="130" height="80" fill="#2e7d4f" opacity=".85"/>
<defs><pattern id="hR" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#20262d"/><line x1="0" y1="0" x2="0" y2="6" stroke="#39424c" stroke-width="2"/></pattern></defs>
<line x1="10" y1="90" x2="400" y2="90" stroke="#ffb020" stroke-width="3" stroke-dasharray="6 3"/>
<text x="75" y="54" fill="#ffd36a">A1 · פ׳ 5</text><text x="205" y="54" fill="#ffd36a">B1 · פ׳ 5</text><text x="335" y="54" fill="#ffd36a">C1 · פ׳ 3</text>
<text x="75" y="134" fill="#fff">A2</text><text x="205" y="134" fill="#fff">B2 — היעד</text><text x="335" y="134" fill="#fff">C2</text><text x="75" y="214" fill="#fff">A3</text><text x="205" y="214" fill="#fff">B3</text><text x="335" y="214" fill="#fff">C3 — הבית</text>
<polyline points="350,225 350,160 300,140 225,140" fill="none" stroke="#39d9ff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<polyline points="350,225 360,70 205,60 205,120" fill="none" stroke="#ff5a5a" stroke-width="3" stroke-dasharray="5 4"/>
<circle cx="215" cy="140" r="7" fill="#ffe08a"/>
<text x="290" y="70" fill="#ff9a9a" font-size="10">היום: דרך C1 / B1 (נעול)</text><text x="300" y="158" fill="#bff4ff" font-size="10">החדש: רק בשטח הפתוח</text>
</g></svg>'''
means = [
 ('ברגל', 'הצעד שחוצה מאזור פתוח לאזור נעול מתבטל (כמו קיר) — אותו מקום שבו נעצרים מול גדר. הכרטיס "אזור נעול · נפתח ב…" עולה (פעם ב-6 שנ׳).'),
 ('רכב — שלך, שאול, רכב תנועה שעלית עליו, רכב עבודה זמני, מבחן', 'אותו קיר לרכב: הרכב נעצר בגבול (מהירות 0, בלי נזק), אפשר לחזור אחורה ולהסתובב. הבדיקה — על כל הגוף (מרכז, חזית, אחור), לא רק על המרכז.'),
 ('סירה (דיג, השכרה, סירה שלך, מבחן הסירה)', 'הסירה נעצרת בגבול האזור הנעול בים (אותו קיר, על המים) וחוזרת צעד אחד אחורה.'),
 ('מעבורת לאי (ברגל וברכב)', 'לא עולים כשהצד השני נעול — "המעבורת לאי נפתחת ב…"; היום: A6 ↔ G8 (פרק 5).'),
 ('מונית', 'יעד באזור נעול — לא ברשימה, ולא יוצאים אליו; המסלול של המונית — רק בשטח הפתוח (אם אין — "אין עדיין דרך פתוחה ליעד").'),
 ('מסוק / מטוס קל של השחקן (police — רישיון טיס, 074zv_flight)', 'אותו קיר גם באוויר: המסוק נעצר בקו, המטוס מסתובב אחורה (אי אפשר לעצור מטוס באוויר). לא ממריאים כשהבסיס (H2 / ‏GA3) באזור נעול. מבחן שהמסלול שלו עובר מעל אזור נעול — לא מתחיל (״המבחן עובר מעל F3 — נעול · נפתח בפרק 4״). אין ״לעוף מעל ולנחות רק בפתוח״ — מעל אזור נעול לא עוברים בשום דרך (HANDOFF §2).'),
 ('כל כלי של w17 (אופניים, קטנוע, אופנוע, ג׳יפ, טרקטורון; 074zv_w17_ride)', 'הם רכב של השחקן (PlayerCar במצב רכב) — אותו קיר; לא עולים על כלי שעומד באזור נעול (גם ג׳יפ / טרקטורון בתחנה שלו).'),
 ('אזור שנוסף לחיים (tcLiveAdd של fieldfix — המנגנון האחד; גם tcLiveRegion של island)', 'הקיר נשען על הטבלה של הסיפור לפי התא — לא על ACTIVE_REGIONS — לכן תא שנכנס לחיים (השדה המזרחי G3, ‏H0–H3; ‏H8 של האי) נשאר נעול עד הפרק שלו. תא בלי פרק בטבלה — מקבל את lockCh או את הפרק האחרון; שטח walk יכול לקבל פרק מאוחר משלו (lockCh), למשל היבשה של H8 עם האי (פרק 6).'),
 ('אוטובוס, רכבת, רכבל', 'השחקן לא נוסע בהם היום (נבדק שוב 17.11: גם הרכבל החדש של island — 019h4 — בלי עלייה של השחקן); חובה לבונים: עלייה רק בתחנה פתוחה, ירידה רק בתחנה פתוחה, תחנה נעולה — לא ברשימה, דרך TCLOCK.lockedAt.'),
 ('גרירה למוסך (074v_econ2_tow — רק למוסך ב-D3)', 'כשהמוסך באזור נעול (בפתיחה) — לא גוררים לשם: הכפתור כבוי עם הסיבה "המוסך ב-D3 נעול — אין גרירה · נפתח ב…" (17.11 ג). אחרת השחקן חוזר לשטח הפתוח והרכב נשאר במוסך הנעול.'),
 ('קפיצה (טעינת שמירה, גרירה, סוף נסיעה, שינה, בדיקה)', 'אם השחקן מוצא את עצמו באזור נעול בלי צעד רגיל לשם — הוא עובר לנקודה הקרובה בשטח הפתוח (על הכביש הקרוב), עם הודעה.'),
]
jsk = """<svg viewBox="0 0 520 210" width="100%" style="max-width:620px;display:block;margin:auto" role="img" aria-label="הצומת האחרון לפני הגבול">
<rect x="0" y="0" width="520" height="210" rx="10" fill="#2b3a2a"/><rect x="340" y="0" width="180" height="210" fill="#0b0f14" opacity=".35"/>
<line x1="340" y1="0" x2="340" y2="210" stroke="#ffb020" stroke-width="4" stroke-dasharray="12 8"/>
<rect x="0" y="92" width="520" height="30" fill="#4a4f55"/><rect x="150" y="0" width="30" height="210" fill="#4a4f55"/>
<g fill="#fff">"""+''.join('<polygon points="%d,103 %d,107 %d,111"/>'%(x,x+12,x) for x in (40,90,220,270,300))+"""</g>
<rect x="296" y="96" width="34" height="18" rx="4" fill="#39d9ff"/><text x="313" y="109" font-size="10" text-anchor="middle" fill="#0b2530">אתה</text>
<rect x="246" y="96" width="34" height="18" rx="4" fill="#b9c0c7"/><rect x="200" y="96" width="34" height="18" rx="4" fill="#b9c0c7"/>
<rect x="186" y="58" width="96" height="20" rx="5" fill="#1c2733" stroke="#ffb020"/><text x="234" y="72" font-size="11" text-anchor="middle" fill="#ffd36a">לפנים נעול · פרק 1</text>
<rect x="346" y="58" width="70" height="20" rx="5" fill="#1c2733" stroke="#ffb020"/><text x="381" y="72" font-size="11" text-anchor="middle" fill="#ffd36a">נעול · פרק 1</text>
<path d="M300 130 C 250 160, 190 160, 168 140" fill="none" stroke="#39d9ff" stroke-width="3" stroke-dasharray="6 4"/><polygon points="164,132 160,146 173,142" fill="#39d9ff"/>
<text x="430" y="150" font-size="12" fill="#fff" text-anchor="middle">אזור נעול</text><text x="70" y="40" font-size="12" fill="#fff">הצומת האחרון</text>
<text x="240" y="190" font-size="11" fill="#cfe" text-anchor="middle">חד-סטרי לתוך הנעול, או תנועה שמחכה מאחוריך — אחרי 4 שנ׳ בקיר: לצומת, בכיוון חוקי</text></svg>"""
air = """<svg viewBox="0 0 520 170" width="100%" style="max-width:620px;display:block;margin:auto" role="img" aria-label="הקיר באוויר">
<rect width="520" height="170" rx="10" fill="#1f4b6b"/><rect x="300" y="0" width="220" height="170" fill="#0b0f14" opacity=".35"/><line x1="300" y1="0" x2="300" y2="170" stroke="#ffb020" stroke-width="4" stroke-dasharray="12 8"/>
<g transform="translate(250,60)"><ellipse rx="22" ry="9" fill="#e8eaed"/><line x1="-34" y1="-12" x2="34" y2="-12" stroke="#e8eaed" stroke-width="3"/><line x1="0" y1="-12" x2="0" y2="-4" stroke="#e8eaed" stroke-width="2"/></g>
<text x="250" y="96" font-size="11" fill="#fff" text-anchor="middle">המסוק נעצר בקו</text>
<g transform="translate(240,130)"><polygon points="30,0 -20,-6 -30,0 -20,6" fill="#ffd36a"/><polygon points="0,0 -8,-20 -14,-20 -6,0 -14,20 -8,20" fill="#ffd36a"/></g>
<path d="M276 128 C 300 110, 300 150, 276 136" fill="none" stroke="#ffd36a" stroke-width="2" stroke-dasharray="4 3"/><text x="160" y="160" font-size="11" fill="#fff" text-anchor="middle">המטוס מסתובב אחורה</text>
<text x="410" y="90" font-size="12" fill="#fff" text-anchor="middle">אזור נעול (גם מעליו)</text></svg>"""
mt = ''.join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (E(a), E(b)) for a, b in means)
fixes = [
 ('ארבע הכשרות שדה (כבודה, מטען, שער, הכוונה), תדלוק וגרירה', 'נפתחות כבר בפתיחה / אחרי LIC‑03', 'העבודה נבדקת גם לפי האזור שלה (E2 — רחבת ההכשרה): נפתחות בפרק 3'),
 ('סיפור של אזור — הכלל', 'נבדק רק האזור של הסיפור (S.zone)', 'נבדקים כל האזורים של כל השלבים; נקודה עד 40 פיקסלים מעבר לקו — "על הקו", נגישה מהצד הפתוח'),
 ('ZS‑B4 — בית הספר', 'בפתיחה; נקודת חניית צוות ב-C4', 'הנקודה 1 פיקסל בתוך C4 (x ‏2401) — על הקו, מגיעים אליה מ-B4 (רדיוס 90): נשאר פתוח'),
 ('סיפורי השדה H2, ‏G3, ‏H3', 'בפרק 3; נקודות ליד הגדר ב-F3', 'הנקודה 18 פיקסלים בתוך F3 — על הקו: נשאר בפרק 3'),
 ('S13‑ST‑F7', 'בפרק 4; חנות האי ב-H9', 'מעבר אמיתי לאזור מאוחר — נעול עד פרק 6'),
 ('S10‑ST‑E6', 'בפרק 4; תחנת הנמל ב-F6', 'הנקודה 4 פיקסלים בתוך F6 — על הקו: נשאר בפרק 4'),
 ('ניווט: 1‑5, ‏1‑6, ‏2‑6, ‏3‑3, ‏3‑6, ‏4‑5', '8 קטעים עוברים באזור סגור', 'המסלול מחושב רק בדרכים שבשטח הפתוח; אם אין — לא מנווטים דרך נעול (הודעה)'),
 ('סיפורי אזורים בשעה שלהם', 'מתחילים גם כשהסיפור הראשי לא התחיל (הבדיקה של הנעילה רצה רק כשיש סיפור ראשי)', 'הבדיקה רצה תמיד במצב סיפור; גם ההזמנה בשעה (038a) וכפתור ההתחלה במסך המקום שואלים את אותו שער'),
 ('פרקים 5 / 6 ("בקרוב")', 'פותחים את כל העיר', 'נשארים נעולים: הכול עד פרק 4 פתוח, האזורים של 5 / 6 — נעולים עד שהפרק נבנה ומתחיל'),
]
ft = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (E(a), E(b), E(c)) for a, b, c in fixes)
# 17.11 (ד) · הבעלים 10:15 — השטח הפתוח והמחובר מהבית בכל שלב (הבדיקה lock_reach / q_lock_reach.js — המספרים מהמשחק)
STN = {'O': 'פתיחה', '1': 'פרק 1', '2': 'פרק 2', '3': 'פרק 3', '4': 'פרק 4', '5~': 'פרק 5 "בקרוב"'}
def reach_marks(st):
    op = [c + str(r) for r in range(10) for c in 'ABCDEFGH']
    return {'cut': st.get('cut', []), 'reached': [z for z in op if z not in st.get('cut', []) and z not in st.get('empty', [])]}
reach_sec = ''
if RJ:
    B, A = (RJ.get('before') or {}).get('stages', {}), (RJ.get('after') or {}).get('stages', {})
    bm = ''.join(stage_svg(k.rstrip('~') if k != '5~' else '4', 'לפני — ' + STN.get(k, k), dict(reach_marks(v)), orig=True) for k, v in B.items() if v.get('cut'))
    corr = {'1': [('D3', 'E3')]}
    am = ''.join(stage_svg(k.rstrip('~') if k != '5~' else '4', 'אחרי — ' + STN.get(k, k), dict(reach_marks(v), corr=corr.get(k.rstrip('~'), []))) for k, v in A.items())
    def row(k, v, b):
        j, a = v['jobs'], v['areas']
        return '<tr><td>%s</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td><td>%d / %d</td><td>%s</td><td>%d (+%d ממתינות)</td><td>%d (+%d)</td><td>%s</td></tr>' % (
            E(STN.get(k, k)), v['open'], v['reached'], E(', '.join(b.get('cut', [])) or '0'), E(', '.join(v['cut']) or '0'), v['story']['pts'], v['story']['steps'], E(', '.join(v['story']['bad']) or '0'),
            j['offered'], j['hidden'], a['offered'], a['hidden'], E(' · '.join(j['hid'][:6] + a['hid'][:3]) or '—'))
    tb = ''.join(row(k, v, B.get(k, {})) for k, v in A.items())
    reach_sec = ('<h2>10. השטח הפתוח והמחובר מהבית — בכל שלב (17.11 ד, הבעלים 10:15)</h2><div class="card">"כל משימה בכל שלב חייב לבדוק שזה יהיה רק בתוך מה שפתוח באותו שלב ושגם כל הדרך פתוחה שלא יצא שלב שנתקעים". '
        'החישוב במשחק (TCLOCK.openReach): מהבית ב-C3 — הליכה ברשת של 30 פיקסלים (כל מקום שאפשר ללכת בו ושלא נעול) ועוד כל הכבישים שכולם בשטח הפתוח, וצומת ↔ השטח שסביבו. '
        'אזור פתוח שיש בו שטח חי (הליכה או צומת) ואין אליו דרך — <b>מנותק</b> (כישלון). עבודה / סיפור אזור שאחד המקומות שלו מחוץ לשטח המחובר — לא מוצעים באותו שלב ("נפתח בהמשך הסיפור — כשתיפתח הדרך אליו"), ונפתחים לבד כשהדרך נפתחת.</div>'
        + ('<h3>לפני התיקון (הטבלה כמו שהייתה)</h3><div class="maps">' + bm + '</div>' if bm else '')
        + '<h3>אחרי — ה-✕ האדום: מנותק · הנקודה הירוקה: מחובר מהבית · החץ: המסדרון שמחבר</h3><div class="maps">' + am + '</div>'
        + '<div class="tw"><table><tr><th>שלב</th><th>אזורים פתוחים</th><th>מחוברים מהבית</th><th>מנותקים לפני</th><th>מנותקים אחרי</th><th>הסיפור הראשי: נקודות / שלבים</th><th>נקודות מחוץ לפתוח</th><th>עבודות מוצעות</th><th>סיפורי אזור מוצעים</th><th>ממתינות (דוגמאות: המקום שאין אליו דרך)</th></tr>' + tb + '</table></div>'
        + '<div class="card ask"><b>לאישורך:</b> E3 עבר מ"מההתחלה" לפרק 1 — הוא נפתח יחד עם D3, הדרך היחידה אליו (המסדרון D3 → E3). החלופה — לפתוח את D3 כבר בפתיחה — מקלקלת את פרק 1 ("סע למוסך ב-D3" היא המשימה שפותחת אותו). '
        'F7 עבר מפרק 4 לפרק 5: בפרק 4 הוא פתוח אבל מנותק (מ-E7 אין מעבר — הנמל), והדרך אליו היא דרך F6 (פרק 5); אין בו עבודה / שלב של פרק 4. '
        'הים: מפרק 4 (הסירות) — נקודה בים (מקום דיג) נחשבת מחוברת כשיש אליה מים פתוחים מהחוף המחובר; עלייה ליבשה מהים — לא נחשבת. '
        'סיפורי האזור S15-ST-H2 / G3 / H3 (נקודה 18 פיקס׳ בתוך F3, מעבר לגדר) ו-S10-ST-E6 (E6-STATION בתוך F6) — לא מוצעים עד שיש אליהם דרך (פרק 4 / פרק 5); קודם (סעיף "לאישורך" 3) הם נחשבו "על הקו". '
        'אזור "לא בנוי / ים" (אין בו שטח הליכה וצומת) — לא נספר כמנותק.</div>')
H = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>נעילה פיזית וניווט חוקי</title><style>:root{--bg:#f6f4ef;--card:#fff;--ink:#1f2328;--mut:#5d6670;--line:#dcd7cc;--chip:#eef1f6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181c;--card:#1e2329;--ink:#e8eaed;--mut:#a3adb8;--line:#343b44;--chip:#28303a}}
:root[data-theme="dark"]{--bg:#15181c;--card:#1e2329;--ink:#e8eaed;--mut:#a3adb8;--line:#343b44;--chip:#28303a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Segoe UI",Arial,sans-serif}main{max-width:1080px;margin:0 auto;padding:16px}h1{font-size:26px;margin:8px 0 4px}h2{font-size:20px;margin:26px 0 8px;border-bottom:2px solid var(--line);padding-bottom:4px}
.sub{color:var(--mut)}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:10px 0}.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;background:var(--card);font-size:14px}th,td{border:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top}th{background:var(--chip)}
.chip{display:inline-block;border-radius:8px;padding:0 8px;margin:2px;font-size:13px}.ask{border-right:4px solid #a5600b}.maps{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}.mapf{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px}.mapf figcaption{font-size:13px;text-align:center;color:var(--mut)}
code{background:var(--chip);border-radius:4px;padding:0 4px;font-size:13px}</style></head><body><main>
<h1>נעילה פיזית אמיתית + ניווט חוקי בכל שלב</h1><p class="sub">הציור לפני הבנייה (כלל 13) · 17.11.2026 · הסוכן locks · מעל הציור של 11.11 (Story_locks_plan.html — מה נפתח באיזה פרק), באותה טבלה בדיוק. רק בשמירה במצב 'story'; במצב 'open' (השמירה של הבעלים) — כלום לא משתנה.</p>
<h2>1. מה קיים, ומה חסר (כלל 16 / 19)</h2><div class="card"><b>קיים</b> (074ze_story_engine.js): שער אחד <code>TCSTORY.locked(kind, id)</code> — אזור, מקום, עבודה, רישיון, סיפור של אזור; טבלת הנעילות (074zd: <code>locks</code>); המפה מחשיכה אזור נעול; כרטיס "אזור נעול" כשנכנסים; מסך מקום נעול; עבודה נעולה לא ברשימה.<br><b>חסר / שבור</b> (הביקורת 12.11, סעיפים 2, 13–17): (1) אין קיר — הולכים ונוסעים לאזור נעול (C3 → D3); (2) הניווט מצייר מסלולים דרך אזורים נעולים; (3) פרק שלא נבנה ("בקרוב") פותח את כל העיר; (4) הכשרות השדה ונקודות של סיפורים מחוץ לאזור שלהם; (5) סיפורי אזורים בשעה שלהם מתחילים גם כשהסיפור הראשי לא רץ.</div>
<h2>2. המפה בכל שלב — מה פתוח, ואיפה הקיר</h2><div class="maps">''' + maps + '''</div><div class="card">''' + leg + '''<p class="sub" style="margin:6px 0 0">הקו הכתום — כל צלע בין אזור פתוח לאזור נעול: את הקו הזה אי אפשר לחצות בשום אמצעי. הקו זז עם הסיפור. פרק שעוד לא נבנה (5, 6) — הקו נשאר כמו בפרק 4.</p></div>
<h2>3. מה רואים בעולם (מבט 3/4)</h2><div class="card">''' + sketch + '''<p class="sub">בגבול: קו כתום מקווקו על הקרקע (רק במצב סיפור, רק ליד המצלמה), הצד הנעול מוחשך מעט, ושלט קטן על המדרכה בכל כביש שחוצה את הגבול: "נעול · פרק N". הרכב נעצר בקו; הכרטיס של היום עולה למעלה. התנועה של העיר ממשיכה (כללים 25 / 32) — הקיר רק לשחקן, ואין שינוי של דרך, כניסה או כיוון (D‑605).</p></div>
<h2>4. כל דרכי המעבר — איך כל אחת נחסמת</h2><div class="tw"><table><tr><th>האמצעי</th><th>מה קורה</th></tr>''' + mt + '''</table></div>
<h2>5. ניווט חוקי</h2><div class="card">''' + route + '''<p>החישוב של הניווט (<code>recalcNavigation</code> → <code>shortestNodePath</code>) מקבל מסנן: קטע דרך שעובר באזור נעול — לא בחישוב. כך גם המונית כשאתה בתוכה. יעד באזור נעול — לא מנווטים אליו ("נעול · נפתח ב…"). אין דרך פתוחה ליעד פתוח — הודעה "אין עדיין דרך פתוחה", ולא קו דרך נעול; עבודה כזאת לא מוצעת עד שנפתחת דרך (הביקורת סעיף 15).</p></div>
<h2>6. התיקונים לפי הביקורת</h2><div class="tw"><table><tr><th>מה</th><th>היום</th><th>אחרי</th></tr>''' + ft + '''</table></div>
<h2>7. הבדיקה החוסמת</h2><div class="card">בתוך המשחק (roadAudit → <code>locks_physical</code>), במצב 'story', בכל שלב (פתיחה, 1, 2, 3, 4, ו-5 "בקרוב"): (1) לכל צלע של הקיר — ניסיון לחצות ברגל, ברכב ובסירה (במים) → נחסם, והשחקן נשאר בצד הפתוח; (2) הליכה אמיתית (updatePed) מ-C3 ל-D3 ונסיעה אמיתית (updateCar) על הכביש C3 → D3 בפתיחה — נעצרים בקו; (3) מונית ומעבורת ליעד נעול — לא יוצאות; (4) כל הניווטים של המשימות והעבודות הפתוחות — 0 קטעים באזור נעול; (5) קפיצה לאזור נעול → חזרה לשטח הפתוח; (6) במצב 'open' — 0 שינוי. בלי עקבות (המצב חוזר).</div>
<h2>9. תוספת 17.11 (ב) — לפי הבקר: אוויר, הכלים של w17, אזורים שנוספו לחיים, הצומת האחרון</h2>
<div class="card">''' + air + '''<p class="sub">הטיסה של השחקן (police) — אותו קיר גם באוויר. מבחן המסוק של היום עובר מעל המרינה (F3, פרק 4), אבל הרישיון בשדה (פרק 3): בפרק 3 המבחן לא מתחיל — "המבחן עובר מעל F3 · נפתח בפרק 4". (תלות police: להזיז את הטבעת "מעל המרינה" לשטח של פרק 3 — אז המבחן נפתח כבר בפרק 3.)</p></div>
<div class="card">''' + jsk + '''<p class="sub">כביש שחוצה לאזור נעול: שלט "נעול · פרק N" בקו, ושלט "לפנים נעול · פרק N" בצומת האחרון לפני הקו (שם אפשר לפנות). מי שעומד בקיר 4 שנ׳ בכביש חד-סטרי שנכנס לנעול, או כשרכב של העיר מחכה מאחוריו — הרכב שלו עובר לצומת האחרון, בכיוון חוקי, עם הודעה. בכביש דו-סטרי בלי תור — רק רמז ("אחורה ופונים בצומת"). רכבי העיר — בלי שינוי: עומדים מאחורי השחקן כמו מאחורי כל רכב עומד, ונוסעים ברגע שהוא זז (כללים 25 / 32).</p></div>
<div class="card"><b>אזור שנוסף לחיים:</b> fieldfix (G3, ‏H0–H3 — השדה המזרחי, פרק 3) ו-island (H8 — פרק 5 בטבלה; היבשה של האי) נכנסים ל-ACTIVE_REGIONS — אבל הקיר לא קורא את ACTIVE_REGIONS, אלא את הטבלה של הסיפור לפי התא (currentChunkId). לכן שני השינויים לא פותחים שום אזור נעול. מעל זה — הבטחה: tcLiveAdd / tcLiveRegion עטופים; כל רשומה נבדקת (אילו תאים, איזה פרק), תא בלי פרק — מקבל את lockCh או את הפרק האחרון, ושטח walk יכול לקבל פרק מאוחר משלו: <code>tcLiveAdd(id, {mode:'walk', rect, lockCh:'6'})</code>. האי החדש: E9 ו-D9 (המרינה) — בטבלה כבר בפרק 6, יחד עם F9–H9 (האי); H8 — פרק 5 ("הגשר והים הפתוח"), ולכן ההצעה (לאישורך): היבשה של H8 — עם האי (lockCh 6).</div>
<h2>8. המספרים מהמשחק (try6282, הבדיקה locks_physical)</h2><div class="tw"><table><tr><th>שלב</th><th>אזורים נעולים</th><th>צלעות של הקיר</th><th>שלטים (כביש שחוצה)</th><th>ניסיונות חצייה (רגל / רכב / סירה)</th></tr><tr><td>פתיחה</td><td>74</td><td>16</td><td>14</td><td>144 / 144 נחסמו</td></tr><tr><td>פרק 1</td><td>67</td><td>14</td><td>12</td><td>126 / 126</td></tr><tr><td>פרק 2</td><td>61</td><td>14</td><td>13</td><td>126 / 126</td></tr><tr><td>פרק 3</td><td>43</td><td>16</td><td>11</td><td>144 / 144</td></tr><tr><td>פרק 4</td><td>23</td><td>18</td><td>5</td><td>162 / 162</td></tr><tr><td>פרק 5 "בקרוב"</td><td>23</td><td>18</td><td>5</td><td>162 / 162 — כמו פרק 4</td></tr></table></div><div class="card">הליכה אמיתית מ-C3 מזרחה — נעצרת ב-x ‏3599.7 (D3 מתחיל ב-3600); נסיעה אמיתית על 3 כבישים שחוצים לאזור נעול — נעצרת; במצב 'open' אותה הליכה ואותה נסיעה עוברות. הניווט של 29 השלבים של הסיפור הראשי — 0 נקודות באזור נעול.</div>
<div class="card ask"><b>סתירה (כלל 5):</b> בפתיחה E3 מסומן "מההתחלה" אבל מוקף אזורים נעולים (D3, ‏E2, ‏E4, ‏F3) — אין אליו דרך פתוחה; ו-B3 / B4 מחוברים ברשת הניווט רק דרך B2 (פרק 1) — מגיעים ברגל / בדשא מ-C3. ברירת המחדל: הטבלה נשארת (הפתיחה — 2 שלבים ליד הבית). ההצעה: לפתוח את D3 / B2 בפתיחה, או להעביר את E3 לפרק 1.</div>
<div class="card ask"><b>לאישורך (ברירות המחדל שנבחרו):</b> (1) הקיר הוא גבול האזור עצמו (המלבן של 1,200 × 850), ולא מחסום על הכביש — כי הכבישים, הכניסות והכיוונים לא משתנים (D‑605) והתנועה של העיר ממשיכה. (2) פרק שעוד לא נבנה — נשאר נעול (לא "פותח את העיר"); אחרי פרק 4 העיר פתוחה עד פרק 4, והסיפור כותב "בקרוב". (3) שמירה שבה השחקן כבר באזור שנעשה נעול (למשל שמירה בפרק 5 "בקרוב" מלפני התיקון) — השחקן עובר לנקודה הפתוחה הקרובה, עם הודעה. (4) מסלול דרך אזור נעול כשאין אחר — לא מוצג ("אין עדיין דרך פתוחה"). (5) נקודה של סיפור עד 40 פיקסלים מעבר לקו — לא סיבה לנעילה.</div>
''' + reach_sec + '''</main></body></html>'''
open(sys.argv[1], 'w', encoding='utf-8').write(H); b = H.encode('utf-8'); print('ok', sys.argv[1], format(len(b), ','), hashlib.sha1(b).hexdigest()[:12])
