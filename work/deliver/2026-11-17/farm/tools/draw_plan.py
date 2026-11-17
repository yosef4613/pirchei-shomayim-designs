# farm · 17.11 — הציור (כלל 13): המפה של החלקות, הגידולים בארבעה שלבים, והתות. SVG בקוד בלבד, בלי תמונות.
import sys,os,random,html
sys.path.insert(0,os.path.dirname(__file__));from plots import PLOTS,EXISTING_S12_POI,NOT_PLOTS,MARKETS
OUT=sys.argv[1]
CROP={'wheat':'חיטה','corn':'תירס','sunflower':'חמניות','veg':'ירקות','tomato':'עגבניות','cucumber':'מלפפונים','strawberry':'תותים','pepper':'פלפלים','melon':'מלונים','potato':'תפוחי אדמה','onion':'בצל'}
BEDS=['veg','tomato','cucumber','strawberry','pepper'];FIELD=['wheat','corn','sunflower','melon','potato','onion']
NEW={'pepper','melon','potato','onion'}
def soil(w,h,empty):
    o=f'<rect width="{w}" height="{h}" fill="#8a6a42"/>'
    for y in range(8,h,14):o+=f'<line x1="4" y1="{y}" x2="{w-4}" y2="{y}" stroke="#5a4026" stroke-opacity=".55" stroke-width="3"/>'
    return o
def plant(crop,stage,x,y,R):
    o=''
    if stage==1:  # נבט
        if crop in('wheat','onion'):return f'<path d="M{x} {y}l-1.5 -4M{x} {y}l1.5 -4" stroke="#7cc35a" stroke-width="1.1"/>'
        return f'<ellipse cx="{x-1.6}" cy="{y-1}" rx="1.8" ry="1" fill="#79c255"/><ellipse cx="{x+1.6}" cy="{y-1}" rx="1.8" ry="1" fill="#6db24c"/>'
    if crop=='strawberry':
        for a,dx,dy in((0,-2.6,-.6),(1,2.6,-.6),(2,0,-2.8)):o+=f'<circle cx="{x+dx}" cy="{y+dy}" r="2.4" fill="{"#3f8f3a" if a!=2 else "#56a64a"}" stroke="#2c6a2a" stroke-width=".4"/>'
        if stage==2:
            if R.random()<.6:o+=f'<g transform="translate({x+3.2},{y+1.4})"><circle r="1.5" fill="#fff"/><circle r=".6" fill="#f2c32e"/></g>'
        if stage==3:
            for k in range(2):
                bx=x+(-3 if k else 3.4);by=y+2.2
                o+=f'<path d="M{bx-1.9} {by-1} Q{bx} {by-2.2} {bx+1.9} {by-1} Q{bx+1.4} {by+2.2} {bx} {by+3.2} Q{bx-1.4} {by+2.2} {bx-1.9} {by-1}Z" fill="#d42a35" stroke="#8e1420" stroke-width=".35"/>'
                o+=f'<path d="M{bx-1.4} {by-1.2}l1.4 -1 1.4 1" stroke="#2f7a2a" stroke-width=".8" fill="none"/>'
                for sx,sy in((-.6,0),(.7,.3),(0,1.3),(-.3,2.1)):o+=f'<circle cx="{bx+sx}" cy="{by+sy}" r=".22" fill="#f4dc6a"/>'
        return o
    if crop=='tomato':
        o+=f'<line x1="{x}" y1="{y+2}" x2="{x}" y2="{y-7}" stroke="#8a6a3a" stroke-width=".9"/>'
        o+=f'<circle cx="{x-1.6}" cy="{y-3}" r="2.8" fill="#2f7a34"/><circle cx="{x+1.8}" cy="{y-4.5}" r="2.6" fill="#3e8c3a"/>'
        if stage==3:
            for dx,dy in((-2.2,-1),(1.8,-2.2),(.2,-5.6)):o+=f'<circle cx="{x+dx}" cy="{y+dy}" r="1.5" fill="#d9402c" stroke="#8e2014" stroke-width=".3"/>'
        elif stage==2:o+=f'<circle cx="{x+1}" cy="{y-2}" r="1" fill="#8ccb5a"/>'
        return o
    if crop=='cucumber':
        o+=f'<ellipse cx="{x}" cy="{y-2}" rx="3.6" ry="2.6" fill="#5f9e3e"/><ellipse cx="{x+2.5}" cy="{y-4}" rx="2.4" ry="1.8" fill="#79b650"/>'
        if stage==3:o+=f'<rect x="{x-2}" y="{y-1}" width="1.6" height="5" rx=".8" fill="#2f6a26"/><rect x="{x+1.4}" y="{y-.4}" width="1.4" height="4.4" rx=".7" fill="#356f2a"/>'
        elif stage==2:o+=f'<circle cx="{x-1}" cy="{y}" r=".9" fill="#f2d33a"/>'
        return o
    if crop=='pepper':
        o+=f'<circle cx="{x}" cy="{y-2.2}" r="3.4" fill="#2e6e30"/><circle cx="{x+1.4}" cy="{y-3.6}" r="2" fill="#3f8a3c"/>'
        if stage==3:
            for dx,c in((-2.2,'#d6312a'),(1.9,'#f0c21e'),(0,'#e2761e')):o+=f'<ellipse cx="{x+dx}" cy="{y+.6}" rx="1.1" ry="1.8" fill="{c}"/>'
        return o
    if crop=='veg':
        if R.random()<.5:o+=f'<circle cx="{x}" cy="{y-1}" r="3.2" fill="#9fd36a"/><circle cx="{x}" cy="{y-1}" r="1.6" fill="#c9ea95"/>'
        else:o+=f'<path d="M{x} {y}l-2 -4M{x} {y}l0 -5M{x} {y}l2 -4" stroke="#4f9a3a" stroke-width="1.2"/>'+(f'<path d="M{x-.9} {y}h1.8l-.9 2.6z" fill="#e8822a"/>' if stage==3 else '')
        return o
    if crop=='wheat':
        c='#d9be5a' if stage==3 else '#8fbf4f'
        for dx in(-2,0,2):o+=f'<line x1="{x+dx}" y1="{y+2}" x2="{x+dx+.6}" y2="{y-5}" stroke="{c}" stroke-width=".9"/>'+(f'<ellipse cx="{x+dx+.7}" cy="{y-5.6}" rx=".9" ry="1.9" fill="#e6c766" stroke="#a88a2e" stroke-width=".3"/>' if stage==3 else '')
        return o
    if crop=='corn':
        o+=f'<line x1="{x}" y1="{y+2}" x2="{x}" y2="{y-10}" stroke="#5f8f36" stroke-width="1.3"/><path d="M{x} {y-3}q-5 -1 -6 -4M{x} {y-6}q5 -1 6 -4" stroke="#6fa544" stroke-width="1.2" fill="none"/>'
        if stage==3:o+=f'<ellipse cx="{x+1.6}" cy="{y-4.5}" rx="1.1" ry="2.4" fill="#e9c94a" stroke="#8aa64a" stroke-width=".6"/><path d="M{x} {y-10}l-1 -2M{x} {y-10}l1 -2" stroke="#c9a85a" stroke-width=".6"/>'
        return o
    if crop=='sunflower':
        o+=f'<line x1="{x}" y1="{y+2}" x2="{x}" y2="{y-8}" stroke="#5f8f36" stroke-width="1.1"/><ellipse cx="{x-2}" cy="{y-3}" rx="2" ry="1" fill="#5f9a3a"/>'
        if stage==3:o+=f'<circle cx="{x}" cy="{y-9}" r="3.6" fill="#f2c72e"/><circle cx="{x}" cy="{y-9}" r="1.6" fill="#6b4a1e"/>'
        else:o+=f'<circle cx="{x}" cy="{y-8.5}" r="1.6" fill="#6f9e3a"/>'
        return o
    if crop=='melon':
        o+=f'<path d="M{x-5} {y}q3 -3 6 0t5 0" stroke="#4f8a34" stroke-width="1" fill="none"/><ellipse cx="{x-2}" cy="{y-1.6}" rx="2.4" ry="1.5" fill="#5f9e3e"/>'
        if stage==3:o+=f'<ellipse cx="{x+2.4}" cy="{y+.8}" rx="3" ry="2.4" fill="#e2cf86" stroke="#a08a44" stroke-width=".4"/><path d="M{x} {y+.4}l4.6 .6M{x+1} {y-.8}l3 3" stroke="#b9a35c" stroke-width=".3"/>'
        return o
    if crop=='potato':
        o+=f'<ellipse cx="{x}" cy="{y+1}" rx="4.6" ry="2" fill="#7a5a36"/><circle cx="{x-1.6}" cy="{y-1.6}" r="2.4" fill="#4f8f3c"/><circle cx="{x+1.8}" cy="{y-1.8}" r="2.2" fill="#5ea046"/>'
        if stage>=2:o+=f'<circle cx="{x}" cy="{y-3.4}" r=".8" fill="{"#f4f0e6" if stage==2 else "#b48ad6"}"/>'
        if stage==3:o+=f'<ellipse cx="{x+3.6}" cy="{y+1.6}" rx="1.4" ry="1" fill="#d9b77a"/>'
        return o
    if crop=='onion':
        for dx in(-1.2,0,1.2):o+=f'<line x1="{x+dx*.4}" y1="{y}" x2="{x+dx*1.6}" y2="{y-6}" stroke="#5fae4a" stroke-width=".8"/>'
        if stage==3:o+=f'<ellipse cx="{x}" cy="{y+.6}" rx="1.9" ry="1.6" fill="#c98a4a" stroke="#8a5a2a" stroke-width=".3"/>'
        return o
    return o
def patch(crop,stage,w=132,h=66,seed=1):
    R=random.Random(seed);o=soil(w,h,stage==0)
    if crop=='strawberry' and stage>0:
        for y in range(8,h,14):o+=f'<rect x="3" y="{y-4}" width="{w-6}" height="8" rx="2" fill="#d9c38a" opacity=".9"/>'
    if stage>0:
        step={'wheat':5,'onion':5,'corn':9,'sunflower':9,'melon':13}.get(crop,9)
        for y in range(10,h,14):
            for x in range(6,w-4,step):o+=plant(crop,stage,x+R.uniform(-.8,.8),y,R)
    return f'<svg viewBox="0 0 {w} {h}" width="{w*1.6:.0f}" height="{h*1.6:.0f}" role="img"><title>{CROP[crop]}</title>{o}</svg>'
ST=['ריק — אדמה חרושה','נבט','גדל (פריחה)','מוכן לקטיף']
gallery=''
for c in BEDS+FIELD:
    gallery+=f'<div class="crop"><h4>{CROP[c]}{" <em>חדש</em>" if c in NEW else ""} <small>{"ערוגות / חממה" if c in BEDS else "שדה פתוח"}</small></h4><div class="st">'+''.join(f'<figure>{patch(c,s,seed=hash(c)%97+s)}<figcaption>{ST[s]}</figcaption></figure>' for s in range(4))+'</div></div>'
# the strawberry, big: old vs new (the old = pink stripes, painted in code as in s11Field)
old='<svg viewBox="0 0 132 66" width="264" height="132"><rect width="132" height="66" fill="#8a6a42"/>'+''.join(f'<line x1="4" y1="{y}" x2="128" y2="{y}" stroke="#d63a4f" stroke-width="4.5"/>' for y in range(8,66,11))+'</svg>'
straw=f'<div class="cmp"><figure>{old}<figcaption>היום (s11Field, ‏#d63a4f): פסים ורודים</figcaption></figure><figure>{patch("strawberry",3,seed=5).replace("width=\"211\" height=\"106\"","width=\"264\" height=\"132\"")}<figcaption>החדש: שיח תות נמוך (3 עלים), ערוגה עם חיפוי קש, פרי אדום בצורת לב עם גביע ירוק וזרעים</figcaption></figure></div>'
# the map
X0,Y0,X1,Y1=2380,-870,4820,870;S=.3
def mx(x):return (x-X0)*S
def my(y):return (y-Y0)*S
m=f'<svg viewBox="0 0 {(X1-X0)*S:.0f} {(Y1-Y0)*S:.0f}" class="map" role="img"><title>מפת החלקות בצפון</title><rect width="100%" height="100%" fill="#dfe6d2"/>'
m+=f'<rect x="{mx(2400)}" y="{my(-850)}" width="{2400*S}" height="{240*S}" fill="#cfe0b8" stroke="#9a9" stroke-dasharray="4 3"/><text x="{mx(3600)}" y="{my(-730)}" class="t">נתיב הגישה למסלול 09 — גידול נמוך בלבד (D‑164)</text>'
m+=f'<rect x="{mx(4350)}" y="{my(-610)}" width="{450*S}" height="{360*S}" fill="none" stroke="#c9a400" stroke-dasharray="3 2"/><text x="{mx(4575)}" y="{my(-560)}" class="t s">אורות הגישה</text>'
for pid,lab,r in NOT_PLOTS:
    m+=f'<rect x="{mx(r[0])}" y="{my(r[1])}" width="{(r[2]-r[0])*S}" height="{(r[3]-r[1])*S}" fill="#c7d3b4" stroke="#8a9a7a" stroke-width=".8"/>'
    if pid not in('C0-CLOVER','D0-CLOVER'):m+=f'<text x="{mx((r[0]+r[2])/2)}" y="{my((r[1]+r[3])/2)}" class="t s g">{pid}</text>'
for pid,z,lab,r,kind,df,poi,src,low in PLOTS:
    col='#e9a03a' if src=='gh' else ('#7fb24a' if kind=='field' else '#c8603a')
    m+=f'<rect x="{mx(r[0])}" y="{my(r[1])}" width="{(r[2]-r[0])*S}" height="{(r[3]-r[1])*S}" fill="{col}" fill-opacity=".55" stroke="#3a2a1a" stroke-width="1"/>'
    m+=f'<text x="{mx((r[0]+r[2])/2)}" y="{my((r[1]+r[3])/2)-3}" class="t">{pid}</text><text x="{mx((r[0]+r[2])/2)}" y="{my((r[1]+r[3])/2)+9}" class="t s">{CROP[df]}{" · נמוך" if low else ""}</text>'
    p=poi or EXISTING_S12_POI[pid]
    m+=f'<circle cx="{mx(p[0])}" cy="{my(p[1])}" r="4.5" fill="{"#ffe08a" if poi else "#9bd86a"}" stroke="#14202a"/><text x="{mx(p[0])}" y="{my(p[1])+2.4}" class="t f">F</text>'
for (pid,lab),(x,y) in zip(MARKETS[1:],[(4384,170),(3268,590)]):
    m+=f'<rect x="{mx(x)-6}" y="{my(y)-6}" width="12" height="12" fill="#2f6b45" stroke="#fff"/><text x="{mx(x)}" y="{my(y)+20}" class="t s">{pid} · זרעים ומכירה</text>'
m+=f'<line x1="{mx(4300)}" y1="{my(200)}" x2="{mx(4300)}" y2="{my(760)}" stroke="#666" stroke-width="3"/><line x1="{mx(3110)}" y1="{my(-600)}" x2="{mx(3110)}" y2="{my(760)}" stroke="#666" stroke-width="3"/><line x1="{mx(2400)}" y1="{my(760)}" x2="{mx(4800)}" y2="{my(760)}" stroke="#666" stroke-width="4"/>'
for z,(x,y) in {'C0':(2440,-20),'D0':(3640,-20),'C1':(2440,820),'D1':(3640,820)}.items():m+=f'<text x="{mx(x)}" y="{my(y)}" class="t z">{z}</text>'
m+='</svg>'
rows=''.join(f'<tr><td>{pid}</td><td>{z}</td><td>{html.escape(lab)}</td><td>{"חממה" if src=="gh" else ("ערוגות" if kind=="beds" else "שדה פתוח")}</td><td>{CROP[df]}</td><td>{"נקודה קיימת" if not poi else "נקודה חדשה (%d, %d)"%poi}</td><td>{"רק נמוכים: חיטה, מלונים, תפוחי אדמה, בצל" if low else ", ".join(CROP[c] for c in (BEDS if kind=="beds" else FIELD))}</td></tr>' for pid,z,lab,r,kind,df,poi,src,low in PLOTS)
nr=''.join(f'<li><b>{p}</b> — {html.escape(l)}</li>' for p,l,r in NOT_PLOTS)
H=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>חלקות החקלאות</title>
<style>:root{{--bg:#f6f4ee;--fg:#1d2420;--mut:#5d655f;--card:#fff;--line:#d8d4c8}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151a17;--fg:#e8ece6;--mut:#a5ada7;--card:#1f2622;--line:#36403a}}}}
:root[data-theme="dark"]{{--bg:#151a17;--fg:#e8ece6;--mut:#a5ada7;--card:#1f2622;--line:#36403a}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 "Segoe UI",Arial,sans-serif;margin:0;padding:16px}}main{{max-width:1180px;margin:auto}}
h1{{font-size:24px;margin:.2em 0}}h2{{font-size:18px;margin:1.4em 0 .4em;border-bottom:1px solid var(--line)}}.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:10px 0;overflow-x:auto}}
.map{{width:100%;height:auto;max-width:760px;display:block}}.t{{font:600 10px Arial;text-anchor:middle;fill:#1d2420}}.t.s{{font-size:8px;font-weight:400}}.t.g{{fill:#556}}.t.f{{font-size:7px;font-weight:700}}.t.z{{font-size:16px;text-anchor:start;fill:#3a4a3a}}
.crop{{margin:10px 0}}.crop h4{{margin:4px 0}}.crop em{{background:#2f6b45;color:#fff;font-style:normal;border-radius:4px;padding:0 5px;font-size:12px}}.crop small{{color:var(--mut);font-weight:400}}
.st{{display:flex;flex-wrap:wrap;gap:8px}}figure{{margin:0}}figcaption{{font-size:12px;color:var(--mut);max-width:270px}}svg{{max-width:100%;height:auto;border-radius:6px}}.cmp{{display:flex;flex-wrap:wrap;gap:16px}}
table{{border-collapse:collapse;font-size:13px;min-width:720px}}td,th{{border:1px solid var(--line);padding:4px 6px;text-align:right}}.lg span{{display:inline-block;width:12px;height:12px;border-radius:2px;margin:0 4px -1px 4px}}</style></head><body><main>
<h1>חקלאות — 17 חלקות זריעה במקום 3, ותות שנראה כמו תות</h1>
<p>הציור לפני הבנייה (כלל 13). הבקשה: Review_part2 §7–8 ו-Owner_requests §13 — "בגידולי הקרקע צריך יותר מקומות שאפשר לגדל… בחממות ובשדות בכפר ליד השדה" · "שתות יראה תות ולא פסים ורודים".</p>
<h2>מה כבר קיים (המלאי, כלל 16)</h2><div class="card"><ul>
<li><b>מחזור הקרקע</b> — 074v_farm.js (פריט 18, ‏D‑208): ‏FARM_CROPS (7 גידולים), ‏FARM_FIELDS — רק 3 חלקות: A6-VEG, ‏A6-WHEAT, ‏A6-CORN; ‏farmSow / farmStart / farmStep / farmSell, הכרטיסים (farmFieldCard, ‏farmMarketCards), השמירה worldPersistent.farmA6. משודרג — לא נכתב מחדש.</li>
<li><b>הציור של A6</b> — s11Field (023a): שורות ישרות בצבע של הגידול. התות = #d63a4f — הפסים הוורודים. אין צמח, אין פרי, אין שלבים (רק "ריק" ו"מלא").</li>
<li><b>הצפון (S12)</b> — 019f_S12_data: 4 חממות ב-D1 (עגבניות, מלפפונים, פלפלים, תותים), 4 שדות ב-D1, 3 שדות בכפר C1, ו-10 שדות ב-C0/D0; הציור s12Field ו-s12GreenhouseRoof (023b); המקומות S12_POIS עם F (038h) — אבל מסך מידע בלבד, בלי זריעה.</li>
<li><b>המטמון של הקרקע</b> (WTC, ‏062) — הקרקע נצרבת לאריחים. שינוי בשדה צריך wtcDirty על המלבן שלו, אחרת הציור הישן נשאר באריח.</li>
<li>הסיפורים של S12 (C1, ‏D1, ‏C0, ‏D0) והמכונות החיות (C0-L1 הקומביין, ‏D0-L1, ‏C1-L1…) — בלי שינוי.</li></ul></div>
<h2>המפה — הצפון (C0, ‏D0, ‏C1, ‏D1)</h2><div class="card">{m}<p class="lg"><span style="background:#e9a03a"></span>חממה <span style="background:#c8603a"></span>ערוגות <span style="background:#7fb24a"></span>שדה פתוח <span style="background:#c7d3b4"></span>לא חלקת זריעה · ● ירוק = נקודת F קיימת · ● צהוב = נקודת F חדשה · ■ = זרעים ומכירה</p>
<p>ב-A6 נשארות 3 החלקות של היום (A6-VEG, ‏A6-WHEAT, ‏A6-CORN) והמטע. סה״כ: 3 + 17 = <b>20 חלקות</b>.</p></div>
<h2>התות — לפני ואחרי</h2><div class="card">{straw}</div>
<h2>כל הגידולים — 4 שלבים</h2><div class="card"><p>11 גידולים (7 של היום + 4 חדשים: פלפלים, מלונים, תפוחי אדמה, בצל). כל שלב נצרב לאריח הקרקע פעם אחת (לא בכל פריים); בזום רחוק (&lt;0.3) — שורות בצבע, כמו היום.</p>{gallery}</div>
<h2>החלקות</h2><div class="card"><table><tr><th>מזהה</th><th>אזור</th><th>שם</th><th>סוג</th><th>ברירת מחדל</th><th>F</th><th>אפשר לגדל</th></tr>{rows}</table></div>
<h2>לא נרשמו כחלקות (ולמה)</h2><div class="card"><ul>{nr}</ul></div>
<h2>איך זה עובד</h2><div class="card"><ul>
<li>כל חלקה: מזהה, גבולות (המלבן של המפרט), נקודת F בשולי השביל, הגידולים שמתאימים, זרעים, 4 שלבי גדילה, קטיף (ביד / קומביין בשדה פתוח), מכירה — אותו מנגנון של A6, אותה שמירה (farmA6.crops).</li>
<li>זרעים ומכירה גם בבית האריזה (D1-PACK) ובחנות הכפר (C1-SHOP) — כדי שלא צריך לנסוע ל-A6 בשביל זרעים.</li>
<li>בתחילת המשחק כל חלקה חדשה "גדלה" בגידול של המפרט (מה שרואים היום) — אין שינוי במראה עד שהשחקן קוטף.</li>
<li>הסיפורים של S12 (המלפפונים בחממה, החיטה ב-C0, המלונים ב-D0) — ממשיכים כמו היום; הכרטיס של החלקה מופיע מתחת לכרטיס של הסיפור.</li></ul></div>
<h2>לאישורך</h2><div class="card"><ul><li>האספסת, רצועות התלתן ושדה המרעה — לא חלקות (מספוא והגבלת גובה).</li><li>ליד אורות הגישה (D0-POTATO) — רק גידולים נמוכים.</li><li>4 גידולים חדשים בשביל החלקות של הצפון; האיזון כמו של A6 (40–60 לדקה לחלקה).</li><li>זרעים ומכירה בבית האריזה ובחנות הכפר.</li></ul></div>
</main></body></html>'''
open(OUT,'w',encoding='utf-8').write(H);print(OUT,len(H))
