# mk_page.py — f9fix (17.11): דף נקי (קוד בלבד, בלי תמונות) — לוח הבדיקה F9: כל כפתור בלשוניות "אירועים" ו"אזורים", לפני ואחרי.
# python3 mk_page.py <before.json> <after.json> <out.html>
import json, sys, html, re
before, after, out = sys.argv[1:4]
B = json.load(open(before, encoding='utf-8')); A = json.load(open(after, encoding='utf-8'))
E = lambda s: html.escape(str(s if s is not None else ''))

def key(e):
    d = e['data']; return json.dumps(d, sort_keys=True, ensure_ascii=False)

bmap = {key(e): e for e in B['events']}
sa, sb = A['summary'], B['summary']

# --- the drawing: the panel, its tabs, and the cards of the events tab; the zones as a grid of 8 columns x 11 rows ---
cards = []
for e in A['events']:
    c = e['card'] or 'בלי כותרת'
    if not cards or cards[-1][0] != c: cards.append([c, 0, 0, 0])
    cards[-1][1] += 1; cards[-1][2] += 1 if e['ok'] else 0
    cards[-1][3] += 1 if key(e) in bmap else 0
W = 1100; y = 120; svg = []
svg.append(f'<rect x="10" y="10" width="{W-20}" height="__H__" rx="16" class="pan"/>')
svg.append('<text x="1070" y="46" class="ttl" text-anchor="start">לוח בדיקה (F9)</text>')
tabs = [('ביצועים', 0), ('אזורים', 1), ('בדיקות', 0), ('אירועים', 1), ('זמן', 0), ('בדיקה בעין', 0)]
x = 760
for t, hot in tabs:
    w = 14 * len(t) + 26
    svg.append(f'<rect x="{x-w}" y="26" width="{w}" height="30" rx="8" class="{"tabOn" if hot else "tab"}"/><text x="{x-w/2}" y="46" text-anchor="middle" class="tt">{E(t)}</text>')
    x -= w + 8
svg.append('<text x="1070" y="96" class="h" text-anchor="start">לשונית "אירועים" — הכרטיסים (מספר הכפתורים · לפני → אחרי)</text>')
for c, n, ok, was in cards:
    st = 'ok' if ok == n else 'bad'
    svg.append(f'<rect x="560" y="{y}" width="510" height="30" rx="8" class="card {st}"/>')
    svg.append(f'<text x="1058" y="{y+20}" text-anchor="start" class="ct">{E(c)}</text>')
    svg.append(f'<text x="572" y="{y+20}" text-anchor="end" class="cn">{n} כפתורים · לפני: {"חסר בלשונית" if was == 0 else "רק מהפתיחה השנייה"} → אחרי: {ok}/{n} עובדים</text>')
    y += 36
yz = 120
svg.append('<text x="530" y="96" class="h" text-anchor="start">לשונית "אזורים" — הרשימה של הפרטים החיים נפתחת?</text>')
zb = {z['zone']: z for z in B['zones']}; za = {z['zone']: z for z in A['zones']}
cols = 'ABCDEFGH'; cw, ch = 58, 30
for r in range(-1, 10):
    for i, C in enumerate(cols):
        z = C + str(r) if r >= 0 else None
        if z is None: continue
        zx = 530 - (8 - i) * cw; zy = yz + r * (ch + 4)   # A on the left, as on the map
        a = za.get(z)
        if not a:
            svg.append(f'<rect x="{zx}" y="{zy}" width="{cw-4}" height="{ch}" rx="6" class="none"/>'); continue
        st = 'ok' if a['ok'] else 'bad'
        n = a.get('liveN'); ns = (a.get('stories') or 0) + (a.get('quests') or 0)
        svg.append(f'<rect x="{zx}" y="{zy}" width="{cw-4}" height="{ch}" rx="6" class="z {st}"/><text x="{zx+(cw-4)/2}" y="{zy+13}" text-anchor="middle" class="zt">{z}</text><text x="{zx+(cw-4)/2}" y="{zy+26}" text-anchor="middle" class="zn">{n if n is not None else "—"} · {ns}ס</text>')
yb = max(y, yz + 10 * (ch + 4)) + 16
svg.append(f'<text x="530" y="{yb}" class="lg" text-anchor="start">בכל משבצת: האזור, מספר הפרטים החיים ברשימה (— = בלי שכבה חיה) · ומספר הסיפורים (ס — החיים + של המשחק)</text>')
svg.append(f'<text x="530" y="{yb+18}" class="lg" text-anchor="start">לפני התיקון (S7F298): אף אזור לא נפתח — {sb["zones"]["bad"]} מתוך {sb["zones"]["total"]} עם שגיאה</text>')
H = yb + 40
svg_s = '\n'.join(svg).replace('__H__', str(H - 20))

# --- the table of the buttons ---
def short(t): return re.sub(r'\s+', ' ', t or '')[:110]
rows = []
for e in A['events']:
    b = bmap.get(key(e))
    if b is None: bef = '<span class="bad">לא הופיע בלשונית</span>'
    else: bef = '<span class="ok">עבד</span>' if b['ok'] else '<span class="bad">לא עבד</span>'
    aft = '<span class="ok">✓ עובד</span>' if e['ok'] else '<span class="bad">✗ ' + E((e['errs'] or [e.get('clickErr') or 'אין שינוי'])[0])[:120] + '</span>'
    what = '; '.join(short(t) for t in e['toasts'][:2]) or ('המצלמה זזה' if e['moved'] else '')
    if e['post'].get('show'): what = 'המסך המלא של ההצגה נפתח' + (' · ' + what if what else '')
    if e['post'].get('vt'): what = 'בדיקת הקולות נפתחה' + (' · ' + what if what else '')
    if e['post'].get('phone'): what = 'המסך הגדול נפתח (' + E(e['post'].get('app')) + ')' + (' · ' + what if what else '')
    rows.append(f'<tr><td>{E(e["card"])}</td><td><b>{E(e["label"])}</b><div class="mut">{E(short(e["row"].replace(e["label"], "", 1)))}</div></td><td>{E(e["expect"])}</td><td>{bef}</td><td>{aft}<div class="mut">{E(what)}</div></td></tr>')
zrows = []
for z in A['zones']:
    b = zb.get(z['zone'])
    bef = '<span class="bad">לא נפתח — ' + E((b['errs'] or ['?'])[0])[:80] + '</span>' if b and not b['ok'] else ('<span class="ok">נפתח</span>' if b else '—')
    zb_btn = [x for x in A['zoneButtons'] if x['zone'] == z['zone']]
    okb = sum(1 for x in zb_btn if x['ok'])
    aft = ('<span class="ok">✓ נפתח</span>' if z['ok'] else '<span class="bad">✗</span>') + f' · {z["liveN"] if z["liveN"] is not None else 0} פרטים חיים · {z["stories"] or 0} סיפורים חיים · {z.get("quests") or 0} סיפורי משחק · כפתורים {okb}/{len(zb_btn)}'
    zrows.append(f'<tr><td><b>{E(z["zone"])}</b></td><td>{E(short(z["head"]))}</td><td>{bef}</td><td>{aft}</td></tr>')

page = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>F9 — אירועים ואזורים</title>
<style>
:root{{--bg:#f4f6f8;--fg:#14202b;--mut:#5a6b78;--card:#fff;--line:#d5dde3;--ok:#1f8a4c;--bad:#c2372b;--pan:#0c1620;--tab:#22313d;--tabOn:#1d4a6b}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0b1218;--fg:#e6f1f8;--mut:#8fb0c6;--card:#111c25;--line:#24343f;--ok:#63d99a;--bad:#ff8a80}}}}
:root[data-theme="dark"]{{--bg:#0b1218;--fg:#e6f1f8;--mut:#8fb0c6;--card:#111c25;--line:#24343f;--ok:#63d99a;--bad:#ff8a80}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 "Segoe UI",Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:18px 16px 40px}}h1{{font-size:22px;margin:4px 0 6px}}h2{{font-size:18px;margin:22px 0 8px}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0}}
.mut{{color:var(--mut);font-size:13px}}.ok{{color:var(--ok);font-weight:600}}.bad{{color:var(--bad);font-weight:600}}
.wrap{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;font-size:14px}}td,th{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top}}th{{color:var(--mut);font-weight:600}}
svg{{width:100%;height:auto;display:block;direction:rtl}}svg .pan{{fill:var(--pan)}}svg .tab{{fill:var(--tab)}}svg .tabOn{{fill:var(--tabOn);stroke:#62c8f4}}svg text{{font-family:"Segoe UI",Arial,sans-serif}}
svg .ttl{{fill:#ffe08a;font-size:18px;font-weight:700}}svg .tt{{fill:#e6f1f8;font-size:13px}}svg .h{{fill:#dff7ff;font-size:14px;font-weight:700}}
svg .card{{stroke-width:1.5}}svg .card.ok,svg .z.ok{{fill:#123a28;stroke:#63d99a}}svg .card.bad,svg .z.bad{{fill:#3a1714;stroke:#ff8a80}}svg .none{{fill:#ffffff08;stroke:#ffffff14}}
svg .ct{{fill:#fff;font-size:13px;font-weight:600}}svg .cn{{fill:#b9d3e3;font-size:12px}}svg .zt{{fill:#fff;font-size:12px;font-weight:700}}svg .zn{{fill:#b9d3e3;font-size:11px}}svg .lg{{fill:#8fb0c6;font-size:12px}}
</style></head><body><main>
<h1>לוח הבדיקה F9 — האירועים והאזורים</h1>
<div class="mut">f9fix · 17.11 · נבדק על {E(A["build"])} מול {E(B["build"])} (S7F298) · לחיצה על כל כפתור, בדפדפן</div>
<div class="box"><b>מה היה שבור:</b> מ-11.11 מנוע הסיפור החדש תפס את השם שממנו F9 קרא את רשימת הסיפורים של האזורים. כל פתיחה של לשונית "אירועים" נעצרה בשגיאה
(הלשונית נשארה ריקה, ובפתיחה השנייה הופיעו רק 3 כרטיסים מתוך 8), וכל לחיצה על אזור בלשונית "אזורים" זרקה שגיאה — הרשימה של הפרטים החיים לא נפתחה.
<br><b>התיקון:</b> ל-F9 הפניה משלו לרשימת הסיפורים; ושגיאה בחלק אחד של הלשונית כבר לא מרוקנת את כולה — היא נכתבת בתוכה.
<br><b>הסבב השני (אחרי הבקר):</b> באזורים הופיעו רק 20 הסיפורים החיים הקצרים (ב-9 אזורים) — סיפורי המשחק (הדמויות, השלבים, הטלפון, התגמול) לא הוצגו בכלל, ולכן רוב האזורים נראו "0 סיפורים".
עכשיו כל אזור מראה גם את סיפורי המשחק שלו: המצב, השעות, מקום ההתחלה, ושלושה כפתורים — "למקום", "להתחיל עכשיו", "בדיקה מההתחלה עד הסוף". ובלשונית "בדיקות" — שורה חדשה לכל סיפורי המשחק.
{('<br><b>הסיפורים בלשונית:</b> ' + str(sa['stories']['live']) + ' חיים · ' + str(sa['stories']['game']) + ' של המשחק · ' + str(sa['stories']['zonesWith']) + ' אזורים עם סיפור; בלי סיפור: ' + (', '.join(sa['stories']['zonesWithout']) or 'אין')) if sa.get('stories') else ''}</div>
<div class="box"><b>אחרי:</b> אירועים — <span class="{'ok' if sa['events']['bad']==0 else 'bad'}">{sa['events']['ok']}/{sa['events']['total']} כפתורים עובדים</span> ·
אזורים — <span class="{'ok' if sa['zones']['bad']==0 else 'bad'}">{sa['zones']['ok']}/{sa['zones']['total']} נפתחים</span> ·
הכפתורים שבתוך האזורים — <span class="{'ok' if sa['zoneButtons']['bad']==0 else 'bad'}">{sa['zoneButtons']['ok']}/{sa['zoneButtons']['total']}</span> ·
שגיאות בדף: <span class="{'ok' if sa['pageErrors']==0 else 'bad'}">{sa['pageErrors']}</span>
<br><b>לפני:</b> אירועים — {B['tabs']['events']['buttons']} כפתורים בפתיחה הראשונה (שגיאה), {B['tabs']['events'].get('buttonsSecondOpen','?')} בשנייה · אזורים — {sb['zones']['ok']}/{sb['zones']['total']} נפתחים · שגיאות בדף: {sb['pageErrors']}</div>
<h2>הציור — הלוח והלשוניות</h2><div class="box wrap"><svg viewBox="0 0 {W} {H}" role="img" aria-label="לוח הבדיקה F9">{svg_s}</svg></div>
<h2>לשונית "אירועים" — כל כפתור</h2><div class="box wrap"><table><tr><th>כרטיס</th><th>כפתור</th><th>מה אמור לקרות</th><th>לפני</th><th>אחרי — מה קרה</th></tr>{''.join(rows)}</table></div>
<h2>לשונית "אזורים" — כל אזור</h2><div class="box wrap"><table><tr><th>אזור</th><th>השורה</th><th>לפני</th><th>אחרי</th></tr>{''.join(zrows)}</table></div>
<div class="mut">הדף בקוד בלבד (SVG וטבלאות) — בלי תמונות.</div>
</main></body></html>'''
open(out, 'w', encoding='utf-8').write(page)
print(out, len(page))
