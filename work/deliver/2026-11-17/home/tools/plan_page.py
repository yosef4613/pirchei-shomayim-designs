#!/usr/bin/env python3
# plan_page.py — home (17.11): דף התוכנית של פנים הבית ב-8 הרמות. הציור — מאותו קוד שנכנס למשחק (parts/074zz7_home_in_data.js), בקנבס, בלי תמונות.
# שימוש: python3 plan_page.py <src_game_dir> <out.html>
import sys, json, html
src, out = sys.argv[1:3]
js = open(src + '/parts/074zz7_home_in_data.js', encoding='utf-8').read()
INTRO = '''
<p><b>מה הבעלים ביקש (17.11 ~14:15):</b> "בית השחקן כבר היה 8 רמות — התוכנית זה עיצוב בפנים שהוא נכנס לכל אחד מהם: חדר שינה עם מיטה לישון ולבחור כמה זמן זה מעביר במשחק,
חדר ארונות הלבשה, מטבח להכין אוכל וסלון לשבת לאכול… דברים שהשחקן קונה בחנויות העיר". זה מתוכנן: HOME-01 (שינה), HOME-02 (פנים בכל 8 הרמות), D‑492, D‑593, C13.03, C15.11.
ובנוסף (14:30): סטודיו העיצוב ברמה 6 — מבחוץ ומבפנים, עם F.</p>
<h3>מה כבר קיים — ועליו בונים (כלל 19א)</h3>
<ul>
<li><b>8 הרמות מבחוץ</b> — 031:C3LV, ‏032:c3Lv / C3PH_B (הציור של house8: House8_levels_plan.html). הגודל של כל בית כאן = הגודל שלו מבחוץ (030:def PH1…PH8, PH7W, PH8W, STUDIO), ומספר הקומות כמו מבחוץ.</li>
<li><b>הדלת</b> — 031:c3Door (9% מצד הדלת), ‏039:playerHomeServicePoint / nearbyPlayerHome; F בדלת פותח את מסך הבית (057:phoneHouse) — שם נוסף בראש "🚪 היכנס הביתה".</li>
<li><b>השינה</b> — HOME-01 (חלק 074zz6_home_sleep): TCSLEEP — אותה פעולה מהמיטה, מ-F בבית ומהמלון (074v:plcAct). השעון: 070:gameClock, התאורה: 074d:WLD.</li>
<li><b>חדר ההלבשה</b> — 074g/074h (D‑593): המסך עם השחקן המסתובב ב-3/4, רק מה שנקנה. הארון והמראה בבית פותחים אותו; בארון רואים את הבגדים שקנית.</li>
<li><b>החנויות והמלאי</b> — 028:SHOP_CATALOG / UNIQUE_SHOP_STOCK, ‏PlayerProfile.inventory. בכניסה הביתה המצרכים עוברים למזווה (PlayerProfile.home.pantry); בסופר "שיבולת" (C2-SUPER) נוספת מחלקת מצרכים.</li>
<li><b>השחקן</b> — הצייר של 3/4 (066:P34) עם ההופעה של היום (074g:p672Pl); עומד, הולך, יושב, אוכל.</li>
<li><b>העבודות, הגביעים, היומן</b> — האפליקציות הקיימות בטלפון (עבודות, הישגים); המחשב, מדף הגביעים והספרייה פותחים אותן.</li>
<li><b>המוסך המסתובב</b> — 074zz2_garage_studio (garage): הסטודיו ברמה 6 משתמש בו לעיצוב הרכב.</li>
</ul>
<h3>איך זה עובד במשחק</h3>
<ol>
<li>בדלת בחוץ — סימן F ו"F · להיכנס הביתה": הדמות הולכת עד הדלת, ועל המסך — בתוך הבית, במבואה (מצב פנים, מצלמה פנימית). כל אגף — מהדלת שלו ("F · להיכנס לאגף"), והסטודיו — "F · הסטודיו — עיצוב". מסך הבית (שדרוג, הצץ, רכבים, שמירה, שינה) — מ"לוח הבית" במבואה; ובהדרכה של משחק חדש, באמצע משימה או כשסיפור מחכה במסך הבית — F בדלת פותח את המסך, ובראשו "🚪 היכנס הביתה".</li>
<li>הולכים בחצים / WASD עם התנגשות בקירות וברהיטים. ליד כל דבר שאפשר לעשות — סימן F עגול, וכשמתקרבים — הכיתוב "F · לישון", "F · להתלבש", "F · לבשל"… (בצהוב — מה ש-F יעשה עכשיו). Esc או השטיח בדלת ("F · לצאת") — יוצאים, ליד הדלת בחוץ.</li>
<li>בכל קומה — המדרגות (F: עלייה / ירידה). הקיר הצפוני גבוה עם חלונות; שאר הקירות חתוכים — כמו בית בובות, רואים פנימה.</li>
<li>שדרוג רמה: המזווה, הבגדים והשמירה נשארים (הם בפרופיל, לא בבית); בפעם הבאה נכנסים לבית החדש.</li>
</ol>
<h3>הפעולות</h3>
<table class="acts"><tr><th>רהיט</th><th>F</th><th>מה קורה</th></tr>
<tr><td>מיטה</td><td>לישון</td><td>בוחרים כמה זמן: עד 07:00 / שעתיים / 4 / 8 שעות / עד המשחק הבא באצטדיון. השחקן שוכב במיטה, מעבר קצר, השעון והתאורה קדימה, שמירה.</td></tr>
<tr><td>ארון, מראה, קיר נעליים</td><td>להתלבש</td><td>חדר ההלבשה (D‑593) — רק מה שקנית בחנויות; בארון רואים את הבגדים בצבעים שלהם.</td></tr>
<tr><td>מקרר, מזווה</td><td>המקרר והמזווה</td><td>מה שקנית בסופר, בבית הקפה ובמסעדה (התוצרת של החווה נשארת בתיק — מוכרים אותה בשוק החווה). "פרוק קניות" מהתיק.</td></tr>
<tr><td>כיריים, אי</td><td>לבשל</td><td>מתכונים ממה שיש במזווה (חביתה, סלט, פסטה, כריך, עוף עם אורז, סלט פירות, ארוחת בוקר, ארוחת ערב, או לחמם ארוחה מוכנה). השחקן עומד ליד הכיריים, סיר ואדים, והמנה נכנסת למזווה.</td></tr>
<tr><td>שולחן האוכל, הבר</td><td>לשבת לאכול</td><td>השחקן יושב על הכיסא, הצלחת על השולחן, ואוכל (תנוחת אכילה של 3/4).</td></tr>
<tr><td>ספה, כורסה, אח</td><td>לשבת</td><td>יושבים; מול הטלוויזיה — החדשות של העיר והמשחק הבא באצטדיון.</td></tr>
<tr><td>מחשב</td><td>לבחור עבודה</td><td>לוח העבודות (האפליקציה הקיימת).</td></tr>
<tr><td>מדף הגביעים, חדר הגביעים</td><td>הגביעים</td><td>גביע לכל הישג / משימה שהושלמה — הגביעים על המדף גדלים עם המשחק.</td></tr>
<tr><td>מדף, ויטרינה, אולם התצוגה</td><td>מה שקנית</td><td>כל מה שקנית בחנויות העיר מוצג על המדפים (ובטבלה).</td></tr>
<tr><td>ארון כלים, מתלה חכות</td><td>הציוד</td><td>ערכות תיקון, מיכלי דלק, חכות ופיתיונות.</td></tr>
<tr><td>פינג־פונג, ביליארד, מכונת משחק, קונסולה</td><td>לשחק</td><td>משחק קצר שרואים (הכדור / הכדורים זזים).</td></tr>
<tr><td>הליכון, ספסל, משקולות</td><td>להתאמן</td><td>אימון קצר.</td></tr>
<tr><td>כורסאות הקולנוע</td><td>לראות סרט</td><td>המסך נדלק — אחד הסרטים של המשחק.</td></tr>
<tr><td>מקלחת, אמבטיה, כיור</td><td>להתרענן</td><td>המים זורמים.</td></tr>
<tr><td>מרפסת</td><td>לצאת למרפסת</td><td>המצלמה יוצאת אל העיר מהבית לכמה שניות, וחוזרת.</td></tr>
<tr><td>לוח הבית (במבואה)</td><td>לוח הבית</td><td>מסך הבית: שדרוג (+ "הצץ"), רכבים, שמירה, שינה.</td></tr>
<tr><td>הסטודיו (רמה 6)</td><td>עיצוב הרכב / הבית</td><td>הרכב שלך על במה מסתובבת (המוסך המסתובב); צבע החזית של הבית והגדר — תצוגה מקדימה, "החל" או "ביטול".</td></tr>
</table>
'''
page = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>פנים הבית — 8 רמות</title>
<style>
:root{{--bg:#f6f3ec;--fg:#1d2430;--mut:#5a6372;--card:#fff;--acc:#d0643b;--line:#e2dccf}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151a21;--fg:#e8e4da;--mut:#a3abb7;--card:#1e252e;--line:#2e3742}}}}
:root[data-theme="dark"]{{--bg:#151a21;--fg:#e8e4da;--mut:#a3abb7;--card:#1e252e;--line:#2e3742}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,"Segoe UI",Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:16px}} h1{{font-size:28px;margin:8px 0}} h2{{margin:34px 0 6px;font-size:24px}} h3{{margin:18px 0 6px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0}}
.lv{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}} .pal{{display:inline-flex;gap:3px;vertical-align:middle}} .pal i{{width:16px;height:16px;border-radius:4px;display:inline-block;border:1px solid #0002}}
canvas{{width:100%;height:auto;border-radius:10px;background:#d9d4c8;display:block}} .fl{{margin:8px 0 2px;font-weight:700;color:var(--mut)}}
table.acts{{border-collapse:collapse;width:100%;font-size:15px}} table.acts td,table.acts th{{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}}
.rooms{{font-size:14px;color:var(--mut)}} .new{{color:var(--acc);font-weight:700}} small{{color:var(--mut)}}
</style></head><body><main>
<h1>פנים הבית — 8 הרמות, השינה והסטודיו</h1>
<p><small>home · 17.11 · הציור נוצר מאותו קוד שנבנה במשחק (074zz7_home_in_data.js): החדרים, הקירות, הפתחים, הריהוט ונקודות הפעולה. מבט 3/4 כמו במשחק.</small></p>
<div class="card">{INTRO}</div>
<div id="levels"></div>
</main>
<script>{js}</script>
<script>
(function(){{
 const host=document.getElementById('levels'),AH=HIN.ACT_HE;let prevRooms=new Set();
 const person=(x,y)=>({{y,draw:(c,v)=>{{const X=v.x(x),Y=v.y(y),S=v.S;c.fillStyle='rgba(0,0,0,.25)';c.beginPath();c.ellipse(X,Y,.25*S,.1*S,0,0,6.28);c.fill();c.fillStyle='#2f6fd0';c.fillRect(X-.18*S,Y-1.25*S*HIN.FZ,.36*S,.75*S*HIN.FZ);c.fillStyle='#1f2a44';c.fillRect(X-.16*S,Y-.55*S*HIN.FZ,.32*S,.55*S*HIN.FZ);c.fillStyle='#d9a77e';c.beginPath();c.arc(X,Y-1.45*S*HIN.FZ,.16*S,0,6.28);c.fill();c.fillStyle='#2a1d14';c.beginPath();c.arc(X,Y-1.52*S*HIN.FZ,.15*S,Math.PI,0);c.fill()}}}});
 for(const L of HIN.LV){{const sec=document.createElement('section');const P=HIN.PAL[L.n];
  sec.innerHTML=`<h2>רמה ${{L.n}} / 8</h2><div class="lv"><b>${{L.he}}</b></div><div class="lv"><small>האופי: ${{P.he}}</small> <span class="pal">${{[P.wall,P.floor,P.wood,P.fab,P.acc,P.rug].map(c=>`<i style="background:${{c}}"></i>`).join('')}}</span></div>`;
  const allRooms=new Set();
  for(const S of L.sites){{const bn=S.b==='H'?'הבית':S.b==='S'?'סטודיו העיצוב':S.b==='W'?'האגף':S.b==='W1'?'האגף המערבי':'האגף המזרחי';
   for(let f=0;f<S.floors.length;f++){{const G=HIN.get(L.n,S.b,f),card=document.createElement('div');card.className='card';
    const fname=S.floors.length===1?'':f===0?' · קומת הכניסה':f===1?' · הקומה השנייה':' · הקומה השלישית';
    card.innerHTML=`<div class="fl">${{bn}}${{fname}} · ${{S.W}} × ${{S.D}} מ׳</div>`;const cv=document.createElement('canvas');card.appendChild(cv);
    const pad=.9,Dh=Math.max(...G.rooms.map(r=>r.y1)),Sx=Math.min(64,1100/(S.W+2*pad));cv.width=Math.round((S.W+2*pad)*Sx*1.5);cv.height=Math.round((Dh+2*pad+2.2)*Sx*1.5);
    const c=cv.getContext('2d');c.scale(1.5,1.5);c.fillStyle='#cdd5c6';c.fillRect(0,0,cv.width,cv.height);const v=HIN.V(c,Sx,pad*Sx,(pad+2.2)*Sx);
    const st=new Map();for(const it of G.items){{if(it.k==='bed1'||it.k==='bed2'||it.k==='bed3')st.set(it,{{}});if(it.k==='trophy')st.set(it,{{cups:4+L.n}});if(it.k==='vitrine'||it.k==='shelf')st.set(it,{{items:['#c8392b','#2f6fd0','#e0a43a','#2e8b57','#7a4fa0','#1f9aa6','#ee7d2d'].slice(0,3+L.n%5)}})}}
    const people=G.front?[person(G.doorX,S.D-.6)]:[];HIN.draw(c,G,v,0,{{labels:true,people,st}});
    // the action points
    for(const it of G.items)if(it.act&&it.ap){{c.fillStyle='rgba(208,100,59,.9)';c.beginPath();c.arc(v.x(it.ap[0]),v.y(it.ap[1]),Math.max(3,Sx*.07),0,6.28);c.fill()}}
    HIN.fMarks(c,v,G,{{all:true}});
    const acts={{}};for(const it of G.items)if(it.act&&it.act!=='exit')acts[AH[it.act]||it.act]=(acts[AH[it.act]||it.act]||0)+1;
    const rl=G.rooms.map(r=>{{const nw=!prevRooms.has(r.t);allRooms.add(r.t);return nw&&L.n>1?`<span class="new">${{r.he}}</span>`:r.he}}).join(' · ');
    const R=HIN.reach(G);const warn=(R.rooms.length||R.acts.length||G.unreach.length)?`<div style="color:#c0392b">בדיקה: ${{JSON.stringify([G.unreach,R.rooms,R.acts])}}</div>`:'';
    card.insertAdjacentHTML('beforeend',`<div class="rooms">החדרים: ${{rl}}</div><div class="rooms">F: ${{Object.keys(acts).join(' · ')}}${{G.front?' · לצאת (השטיח בדלת)':''}}</div>${{warn}}`);sec.appendChild(card)}}}}
  sec.insertAdjacentHTML('beforeend','<div class="rooms">בכתום — חדרים שאין ברמה הקודמת. סימני F — כל מה שאפשר לעשות, עם הכיתוב (במשחק הכיתוב מופיע כשמתקרבים); הנקודות הכתומות — איפה עומדים.</div>');
  for(const t of allRooms)prevRooms.add(t);host.appendChild(sec)}}
}})();
</script></body></html>'''
open(out, 'w', encoding='utf-8').write(page)
print(out, len(page.encode('utf-8')))
