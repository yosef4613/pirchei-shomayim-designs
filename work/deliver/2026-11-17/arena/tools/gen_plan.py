# arena 17.11 — הציור (כלל 13): אולם הכדורסל באי, הליגה, המשחק החי ומופעי המחצית. SVG בקוד בלבד, בלי תמונות.
import html
OUT='/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/arena/draw/Arena_plan.html'
E=html.escape
TEAMS=[('MGD','המגדלור','מגדלורי האי','#1f3f8a','#f4f4f0','#f2c230','light'),('RKB','הרכבל','רכבלי ההר','#c0392b','#1f2326','#f4f4f0','cable'),
 ('MRN','המרינה','מפרשי המרינה','#f4f4f0','#1f5fd1','#1f5fd1','sail'),('GSR','הגשר','קשתות הגשר','#e67e22','#2b2f33','#2b2f33','bridge'),
 ('KFR','הכפר','צוקי הכפר','#2e8b57','#f2c230','#f2c230','peak'),('MNH','המנחת','מסוקי המנחת','#6a3fb5','#c9ced3','#c9ced3','heli')]
SYM={'light':'<path d="M10 20l1-12h2l1 12z"/><path d="M9 8h6M12 4v2M7 6L4 5M17 6l3-1"/>','cable':'<path d="M3 5l18 4"/><path d="M12 7v3"/><rect x="8" y="10" width="8" height="7" rx="1.5"/>',
 'sail':'<path d="M12 3v15M12 4l7 12h-7M12 6l-6 10h6"/><path d="M4 19c3 2 13 2 16 0"/>','bridge':'<path d="M3 16h18M5 16c2-6 12-6 14 0M8 16v-3M12 16v-4M16 16v-3"/>',
 'peak':'<path d="M3 19l6-10 3 4 3-6 6 12z"/>','heli':'<path d="M4 7h16M12 7v3"/><path d="M7 13a5 3 0 0 0 10 0a5 3 0 0 0-10 0M17 13h4M8 17l-1 2M16 17l1 2"/>'}
def badge(t,s):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 1l9 3v7c0 6-4 10-9 12C7 21 3 17 3 11V4z" fill="{t[3]}" stroke="{t[5]}" stroke-width="1.6"/><g fill="none" stroke="{t[5]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(4.8 4.4) scale(.6)">{SYM[t[6]]}</g></svg>'
# ---- 1. מבט על: E9 — השדרה, האולם, רחוב ה-U, החניון והמלון (קואורדינטות העולם; 10 = מטר) ----
def site():
    X0,Y0,X1,Y1=5080,7180,6150,7720; W=1000; k=W/(X1-X0); H=int((Y1-Y0)*k)
    P=lambda x,y:(round((x-X0)*k,1),round((y-Y0)*k,1)); R=lambda a,b,c,d:(*P(a,b),round((c-a)*k,1),round((d-b)*k,1))
    s=[f'<svg viewBox="0 0 {W} {H}" class="map" role="img" aria-label="מבט על — אולם הכדורסל באי ב-E9">']
    s.append(f'<rect width="{W}" height="{H}" fill="#cfe3c4"/>')
    x,y,w,h=R(X0,Y0,X1,7205); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#9cc8e6"/><text x="{w/2}" y="{h-4}" class="lbl" text-anchor="middle">הים (החוף הצפוני של E9 — של island)</text>')
    for (a,b,c,d,t) in [(X0,7225,X1,7255,'שדרת האי ISL-SPINE-W (של island)'),(5590,7240,5610,7570,''),(5790,7240,5810,7570,''),(5590,7550,5810,7570,'')]:
        x,y,w,h=R(a,b,c,d); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#6b7178"/>')
        if t: s.append(f'<text x="{x+12}" y="{y+h/2+4}" class="lbl w">{E(t)}</text>')
    x,y=P(5700,7560); s.append(f'<text x="{x}" y="{y+22}" class="lbl" text-anchor="middle">רחוב ה-U של המלון (ISL-BEACH)</text>')
    x,y,w,h=R(5630,7290,5770,7530); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#d9d9d9" stroke="#888"/><text x="{x+w/2}" y="{y+h/2}" class="lbl" text-anchor="middle">P-HOTEL</text><text x="{x+w/2}" y="{y+h/2+16}" class="sm" text-anchor="middle">20 מקומות; בימי משחק</text><text x="{x+w/2}" y="{y+h/2+30}" class="sm" text-anchor="middle">+ חניון המרינה</text>')
    x,y,w,h=R(5860,7300,6090,7690); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e8d7b9" stroke="#a08a5f"/><text x="{x+w/2}" y="{y+h/2}" class="lbl" text-anchor="middle">מלון החוף המערבי</text>')
    # האולם
    x,y,w,h=R(5220,7300,5590,7690); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#eef1f4" stroke="#1f3f8a" stroke-width="3"/>')
    x,y,w,h=R(5220,7300,5590,7390); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e2dccf"/><text x="{x+w/2}" y="{y+14}" class="sm" text-anchor="middle">הרחבה (island: 7300–7390)</text>')
    x,y,w,h=R(5300,7330,5510,7386); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f6e3a8" stroke="#a08a5f"/><text x="{x+w/2}" y="{y+h/2+5}" class="lbl" text-anchor="middle">לובי, קופה ומזנון</text>')
    x,y,w,h=R(5232,7394,5560,7472); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#b9c3cf"/><text x="{x+w/2}" y="{y+h/2+5}" class="lbl" text-anchor="middle">היציע הצפוני — 10 שורות (~520)</text>')
    x,y,w,h=R(5232,7638,5560,7686); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#c9d1da"/><text x="{x+w/2}" y="{y+h/2+5}" class="lbl" text-anchor="middle">היציע הדרומי — 3 שורות נמוכות (~160)</text>')
    x,y,w,h=R(5265,7480,5545,7630); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#d9a066" stroke="#fff" stroke-width="2"/>')
    cx,cy=P(5405,7555); s.append(f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y+h}" stroke="#fff" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="{18*k}" fill="none" stroke="#fff" stroke-width="2"/>')
    for hx,sgn in ((5265,1),(5545,-1)):
        a,b=P(hx,7555); s.append(f'<path d="M{a} {b-67*k} h{sgn*29*k} a{67*k} {67*k} 0 0 {0 if sgn>0 else 1} 0 {134*k} h{-sgn*29*k}" fill="none" stroke="#fff" stroke-width="2"/><circle cx="{a+sgn*15.75*k}" cy="{b}" r="4" fill="#e65100"/>')
    s.append(f'<text x="{cx}" y="{cy+48*k}" class="lbl w" text-anchor="middle">המגרש 28 × 15 מ׳</text>')
    x,y,w,h=R(5563,7487,5588,7625); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#8fa3b8"/><text x="{x+w/2}" y="{y+h/2}" class="sm" text-anchor="middle" transform="rotate(-90 {x+w/2} {y+h/2})">חדרי הלבשה</text>')
    a,b=P(5572,7627); s.append(f'<circle cx="{a}" cy="{b}" r="6" fill="#1f3f8a"/>')
    for bx in (5330,5440):
        x,y,w,h=R(bx,7634,bx+40,7638); s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#2b2f33"/>')
    a,b=P(5405,7318); s.append(f'<rect x="{a-9}" y="{b-9}" width="18" height="18" rx="9" fill="#ffb020"/><text x="{a}" y="{b+5}" text-anchor="middle" class="lbl">F</text><text x="{a-14}" y="{b+5}" class="sm" text-anchor="end">IS-ARENA — ברחבה, מול הלובי</text>')
    pts=' '.join(f'{P(*q)[0]},{P(*q)[1]}' for q in [(6100,7560),(5900,7700),(5660,7700),(5660,7360),(5590,7360)]); s.append(f'<polyline points="{pts}" fill="none" stroke="#a8916a" stroke-width="5" stroke-dasharray="2 3"/>')
    a,b=P(5668,7520); s.append(f'<text x="{a+4}" y="{b}" class="sm">השביל של island (ברגל — עד שלב 2ג-2)</text>')
    x,y,w,h=R(5220,7300,5590,7690); s.append(f'<text x="{x+6}" y="{y+h+16}" class="sm">ISL-ARENA ‏[5220, 7300, 5590, 7690] — ISL17E9.arena של island (019h5): הרחבה 7300–7390, האולם 7390–7690 (37 × 30 מ׳)</text>')
    s.append('</svg>'); return ''.join(s)
# ---- 2. מבט 3/4: גג שקוף, היציעים, הלוח ----
def view34():
    s=['<svg viewBox="0 0 1000 470" class="map" role="img" aria-label="מבט 3/4 — האולם עם גג שקוף">','<rect width="1000" height="470" fill="#dfe8ee"/>']
    s.append('<polygon points="120,380 880,380 940,440 60,440" fill="#c9d1da"/><text x="500" y="430" class="lbl" text-anchor="middle">היציע הדרומי — נמוך (1.6 מ׳)</text>')
    s.append('<polygon points="200,170 800,170 840,360 160,360" fill="#d9a066" stroke="#fff" stroke-width="2"/><line x1="500" y1="170" x2="500" y2="360" stroke="#fff" stroke-width="2"/><ellipse cx="500" cy="265" rx="45" ry="30" fill="none" stroke="#fff" stroke-width="2"/>')
    s.append('<polygon points="150,60 850,60 800,170 200,170" fill="#b9c3cf"/>'+''.join(f'<line x1="{150+i*4}" y1="{60+i*9.2}" x2="{850-i*4}" y2="{60+i*9.2}" stroke="#97a3b0"/>' for i in range(12))+'<text x="500" y="120" class="lbl" text-anchor="middle">היציע הצפוני — 12 שורות</text>')
    s.append('<rect x="440" y="22" width="120" height="34" fill="#0d1013" stroke="#4b535a"/><text x="500" y="44" class="lbl" text-anchor="middle" fill="#ffaa28">54 : 49 · רבע 3</text>')
    for hx,d in ((215,1),(785,-1)): s.append(f'<line x1="{hx-d*20}" y1="265" x2="{hx-d*20}" y2="205" stroke="#3a3f44" stroke-width="5"/><rect x="{hx-d*20-(0 if d>0 else 6)}" y="186" width="6" height="34" fill="#fff" stroke="#333"/><ellipse cx="{hx+d*4}" cy="214" rx="9" ry="3" fill="none" stroke="#e65100" stroke-width="3"/>')
    for i in range(10): s.append(f'<circle cx="{300+i*42}" cy="{240+(i%3)*30}" r="7" fill="{"#1f3f8a" if i<5 else "#e67e22"}"/>')
    s.append('<polygon points="100,40 900,40 960,400 40,400" fill="#9fd3ff" fill-opacity=".12" stroke="#5a8fb8" stroke-width="2" stroke-dasharray="8 6"/>'+''.join(f'<line x1="{100+i*100}" y1="40" x2="{40+i*115}" y2="400" stroke="#5a8fb8" stroke-opacity=".35"/>' for i in range(9)))
    s.append('<text x="960" y="30" class="lbl" text-anchor="end">גג שקוף (כלל 15) — מסגרת וזכוכית; רואים את המשחק מבחוץ בכל זום</text></svg>'); return ''.join(s)
# ---- 3. הלוח: הכדורגל והכדורסל לא באותו יום ----
def cal():
    s=['<svg viewBox="0 0 1000 120" class="map" role="img" aria-label="ימי המשחקים">']
    for d in range(1,13):
        x=1000-d*80; s.append(f'<rect x="{x}" y="10" width="74" height="96" rx="6" fill="#fff" stroke="#ccd"/><text x="{x+37}" y="30" text-anchor="middle" class="lbl">יום {d}</text>')
        if d>=2 and (d-2)%3==0: s.append(f'<rect x="{x+6}" y="40" width="62" height="26" rx="4" fill="#1f5fd1"/><text x="{x+37}" y="58" text-anchor="middle" class="sm w">כדורגל 19:30</text>')
        if d>=3 and (d-3)%3==0: s.append(f'<rect x="{x+6}" y="72" width="62" height="26" rx="4" fill="#e65100"/><text x="{x+37}" y="90" text-anchor="middle" class="sm w">כדורסל 19:00</text>')
    s.append('</svg>'); return ''.join(s)
rows=''.join(f'<tr><td>{badge(t,28)}</td><td><b>{E(t[2])}</b><br><small>{E(t[1])} · {t[0]}</small></td><td><span class="sw" style="background:{t[3]}"></span><span class="sw" style="background:{t[4]}"></span><span class="sw" style="background:{t[5]}"></span></td></tr>' for t in TEAMS)
page=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>אולם הכדורסל באי</title>
<style>:root{{--bg:#f5f6f8;--fg:#1d232a;--card:#fff;--mut:#5c6670;--ac:#1f3f8a}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,Arial,sans-serif}}main{{max-width:1040px;margin:0 auto;padding:16px}}
h1{{font-size:24px;margin:8px 0}}h2{{font-size:18px;margin:22px 0 8px;color:var(--ac)}}.card{{background:var(--card);border:1px solid #dde2e8;border-radius:10px;padding:12px 14px;margin:10px 0}}.mut{{color:var(--mut)}}
.map{{width:100%;height:auto;display:block;border-radius:8px}}.lbl{{font:600 13px system-ui,Arial;fill:#1d232a}}.sm{{font:12px system-ui,Arial;fill:#1d232a}}.w{{fill:#fff}}table{{border-collapse:collapse;width:100%}}td,th{{padding:6px;border-bottom:1px solid #eef;text-align:right;vertical-align:middle}}
.sw{{display:inline-block;width:18px;height:18px;border-radius:4px;border:1px solid #0003;margin-left:4px}}ul{{margin:6px 0;padding-right:20px}}code{{background:#eef1f5;padding:0 4px;border-radius:4px}}</style></head><body><main>
<h1>אולם הכדורסל באי + ליגת הכדורסל + עוד מופעי מחצית בכדורגל</h1>
<p class="mut">arena · 17.11 · הציור לפני הבנייה (כלל 13). הבקשה: "אני רוצה באי איצטדיון כדור סל עם ליגה וקבוצות כמו בכדור רגל עם משחקים חיים וכו׳ / וגם נוסף כבר בכדור רגל יותר הצגות הפסקת אמצע?"</p>
<div class="card"><b>המלאי — מה כבר קיים ומשודרג (כללים 16, 19, 19א)</b><ul>
<li>הכדורגל: <code>024_A3_A4</code> (matchNow / nextMatch לפי שעון המשחק, כל 3 ימים מיום 2 ב-19:30), <code>024a SPORT2</code> (המשחק החי בפיזיקה, הגולים, החגיגות, הטקס, מופע מחצית אחד), <code>074f LEAGUE4</code> (6 קבוצות, 5 מחזורים, גמר, הטלפון "חדשות העיר" — CITYNEWS).</li>
<li>הכדורסל: <code>SPORT2</code> כבר מריץ 5 על 5 בפיזיקה במגרש של A4 (כדרור, מסירה, זריקה בקשת, טבעת ולוח, ריבאונד, שופט, לוח נקודות) — <b>אותה סימולציה עוברת לאולם</b>: התלבושות של שתי הקבוצות, דלת ומסלול מחדרי ההלבשה, ושתי מחציות עם החלפת סלים.</li>
<li>המקום באי: <code>ISL17E9.arena</code> של island (019h5, שלב 2ג-1 — היבשה של E9 נבנתה ב-17.11): הרחבה, הלובי והקופה מצפון (7300–7390), האולם 7390–7690. האולם מופיע רק כשהיבשה קיימת (ISL17E9.ok / landAt); בלי — רק בתצוגה מ-F9. השדרה, התחנות והחניונים — שלב 2ג-2 של island; עד אז מגיעים ברגל בשביל.</li></ul></div>
<h2>1 · המקום — מבט על (E9)</h2><div class="card">{site()}<p class="mut">הכניסה מהשדרה (צפון), לובי וקופה; היציע הגבוה בצפון והנמוך בדרום — כדי שבמבט 3/4 רואים את המגרש. חדרי ההלבשה בקצה המזרחי; הקבוצות יוצאות מהדלת אל הפינה של המגרש. F מול הכניסה.</p></div>
<h2>2 · האולם במבט 3/4 — גג שקוף</h2><div class="card">{view34()}</div>
<h2>3 · ליגת הכדורסל של האי — 6 קבוצות</h2><div class="card"><table><tr><th>סמל</th><th>קבוצה</th><th>צבעים</th></tr>{rows}</table>
<p class="mut">כמו ליגת הכדורגל: עונה = 5 מחזורים (כל קבוצה פוגשת כל קבוצה), 3 משחקים בכל מחזור — אחד חי באולם, שניים "באולמות אחרים" (תוצאה מוגרלת); אחרי 5 מחזורים — גמר באולם בין שתי הראשונות, והאלופה חוגגת עם הגביע על המגרש. ניצחון — 2 נקודות, הפסד — 1 (כמו בכדורסל). הטבלה, התוצאות והידיעות — בטלפון ("חדשות העיר" — פרק חדש "כדורסל באי"), בדף המקום (F) וב-F9.</p></div>
<h2>4 · הלוח — לפי שעון המשחק, בלי התנגשות</h2><div class="card">{cal()}<p class="mut">הכדורגל: כל 3 ימים מיום 2 ב-19:30 (קיים). הכדורסל: כל 3 ימים מיום 3 ב-19:00 — תמיד ביום אחר. ימים שעברו בלי צפייה (שינה, קפיצה בזמן) — המחזור משוחק בתוצאה מוגרלת, כדי שהטבלה תתקדם.</p></div>
<h2>5 · המשחק החי</h2><div class="card"><ul><li>הקהל נכנס, שתי הקבוצות יוצאות מחדרי ההלבשה, כדור ביניים.</li><li>מחצית ראשונה — 5 על 5 בפיזיקה (SPORT2), שופט עם משרוקית, לוח תוצאות על הקיר הצפוני: שמות, ניקוד, זמן.</li>
<li>המחצית: הקבוצות לחדרי ההלבשה, ועל המגרש — מופע המחצית של הכדורסל.</li><li>מחצית שנייה — הסלים מתחלפים; בסוף — שריקה, התוצאה נכנסת לטבלה, הקבוצות יוצאות.</li><li>F באולם: המשחק הבא / התוצאה עכשיו, הטבלה, כרטיס וצפייה (המצלמה נכנסת לאולם).</li></ul></div>
<h2>6 · מופעי המחצית</h2><div class="card"><b>בכדורגל — 4 מופעים שמתחלפים בכל משחק בליגה</b> (נבנה — 024b):<ul><li>מתופפים ונערים עם דגלים (הקיים).</li><li>נערים בתרגילי כדור — ג'אגלינג בזוגות עם נגיחה, מסירות מעל הראש, בעיטה גבוהה ותפיסה.</li>
<li>הדגל הענק ודגלי הליגה — 8 פורשים ומניפים דגל ענק בצבעי הקבוצה המארחת, ו-6 נושאי דגלים — לכל קבוצה בליגה.</li><li>מגדלי נערים וקפיצות — 3 מגדלים של שלושה על הכתפיים, וקפיצות מלפנים.</li></ul>
<b>בכדורסל:</b> קפיצות לסל מהטרמפולינה — טור של נערים רץ, קופץ מהטרמפולינה ומטביע; ותרגילי כדרור בשורות. <span class="mut">תצוגת אופנועים / רכבים — לא נבנתה: כלי רכב שמופיע על הדשא ונעלם סותר את הכלל של כלי הרכב בסימולציה (לאישורך).</span></div>
<h2>7 · תלות ותיאום</h2><div class="card"><ul><li><b>island</b> — היבשה של E9 (2a8e51c, שלב 2ג-1 — נבנתה) ממוזגת לפני ענף הכדורסל; השדרה, התחנה של קו 5 מול הכניסה והחניונים (שלב 2ג-2). בלי היבשה: הליגה והמשחקים רצים (הטלפון, F9), והאולם — בתצוגה מ-F9.</li><li><b>signs</b> — השלט של האולם והשמות. <b>locks</b> — E9 בטבלת הנעילות.</li></ul></div>
</main></body></html>'''
open(OUT,'w').write(page); print(OUT, len(page))
