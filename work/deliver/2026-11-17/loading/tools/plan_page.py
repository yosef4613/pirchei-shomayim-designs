#!/usr/bin/env python3
# plan_page.py — הציור של מסך הטעינה (כלל 13): הכרטיסים עצמם (אותו קוד של 009c), זרימת המסכים, השלבים, והמלאי. בלי תמונות.
import os, hashlib
W = '/home/user/tc_root/tc/pkg/work'
part = open(W + '/src_game_t17_loading/parts/009c_loading.js', encoding='utf-8').read()
out = W + '/deliver/2026-11-17/loading/Loading_plan.html'
flow = '''<svg viewBox="0 0 1000 300" class="flow" role="img" aria-label="מתי מופיע מסך הטעינה">
<defs><marker id="fa" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#ffd27a"/></marker></defs>
<g font-family="Segoe UI,Arial" font-size="15" text-anchor="middle">
<rect x="800" y="20" width="180" height="70" rx="12" fill="#1f4a72" stroke="#8cecff"/><text x="890" y="50" fill="#fff" font-weight="800">פתיחת הדף</text><text x="890" y="72" fill="#cfe6ff" font-size="13">boot · מתחת ללוגו</text>
<rect x="560" y="20" width="200" height="70" rx="12" fill="#1f4a72" stroke="#8cecff"/><text x="660" y="50" fill="#fff" font-weight="800">מסך הפתיחה מוכן</text><text x="660" y="72" fill="#cfe6ff" font-size="13">strip · פס דק בתחתית</text>
<rect x="300" y="20" width="220" height="70" rx="12" fill="#5a3f28" stroke="#ffd27a"/><text x="410" y="50" fill="#fff" font-weight="800">"המשך" / "משחק חדש" / שמירה</text><text x="410" y="72" fill="#ffe6b0" font-size="13">full · מסך מלא עד שהעיר מוכנה</text>
<rect x="40" y="20" width="220" height="70" rx="12" fill="#244a6e" stroke="#4fd17a"/><text x="150" y="50" fill="#fff" font-weight="800">משחקים</text><text x="150" y="72" fill="#cfe6ff" font-size="13">העולם חוזר לרוץ</text>
<path d="M798 55H764M558 55H524M298 55H264" stroke="#ffd27a" stroke-width="3" marker-end="url(#fa)"/>
<rect x="40" y="150" width="920" height="130" rx="14" fill="#0e2238" stroke="#3b5670"/>
<text x="500" y="178" fill="#ffd27a" font-weight="800">בתוך המשחק — אותו מסך מלא בכל טעינה</text>
<g font-size="14" fill="#eef7ff"><rect x="70" y="196" width="190" height="64" rx="10" fill="#1f4a72"/><text x="165" y="222">F7 · טעינת שמירה</text><text x="165" y="244" fill="#cfe6ff" font-size="12">SaveManager.load / loadString</text>
<rect x="290" y="196" width="190" height="64" rx="10" fill="#1f4a72"/><text x="385" y="222">מעבר בין שמירות</text><text x="385" y="244" fill="#cfe6ff" font-size="12">מסך "שמירות" · ייבוא</text>
<rect x="510" y="196" width="190" height="64" rx="10" fill="#1f4a72"/><text x="605" y="222">שדה התעופה ממשיך</text><text x="605" y="244" fill="#cfe6ff" font-size="12">G77_LDS — במקום החלון הישן</text>
<rect x="730" y="196" width="200" height="64" rx="10" fill="#1f4a72"/><text x="830" y="222">זום רחוק / אזור כבד</text><text x="830" y="244" fill="#cfe6ff" font-size="12">40% חסרים או מכוסים · 0.35 שנ׳</text></g></g></svg>'''
steps = '''<table class="tb"><tr><th>שלב</th><th>המקור (מה נמדד)</th><th>מוכן כש…</th></tr>
<tr><td>קוד המשחק</td><td>הסקריפט הגדול רץ עד הסוף (החלק 074zf9 מסמן)</td><td>עד אז — פס מבהיק, בלי מספר מומצא</td></tr>
<tr><td>השמירה</td><td>TCO.mode: boot → open / ‏TCO.entered / ‏SaveManager.load</td><td>השמירה הוחלה</td></tr>
<tr><td>מפת הבסיס</td><td>MAPBASE.next / MAPBASE.total (028 — אריח אחד בכל פריים)</td><td>MAPBASE.done</td></tr>
<tr><td>אריחי העיר</td><td>האריחים במסך שעוד מצוירים חי כי לא נבנו (wtcPass, המונה miss של 062)</td><td>0 חסרים — 3 פריימים רצופים</td></tr>
<tr><td>כלי הרכב</td><td>התמונות של מבט 3/4 שבתור (C34.queued, ‏065) ורכבים במסך שמחכים (C34G.n.wait)</td><td>התור ריק, או אף רכב לא מחכה 20 פריימים</td></tr>
<tr><td>שדה התעופה</td><td>G77_LDS.job — n / total (053 / 054)</td><td>העבודה הסתיימה</td></tr>
<tr><td>עדכון המפה <i>(חדש 17.11, משקל 0)</i></td><td>האפייה השנייה של mapfix (074zp — MAPBASE.rebake, ‏MAPBASE.next מתאפס)</td><td>לא מחכים לה: המפה כבר שלמה (התמונה הקודמת נשארת) — רק נראית בשורה</td></tr></table>
<p class="note">הפס לא חוזר אחורה באותה טעינה (17.11): אחוז שכבר הוצג נשאר עד שהמדידה עוברת אותו — גם כשהמצלמה של הרקע עוברת לאריחים חדשים, וגם באפייה השנייה של mapfix (קודם: 87% ← 82%).</p>'''
home = '''<svg viewBox="0 0 1000 250" class="flow" role="img" aria-label="מסך הפתיחה עם האריח סרטון הפתיחה"><g font-family="Segoe UI,Arial" text-anchor="middle">
<text x="500" y="30" fill="#ffd27a" font-size="15" font-weight="800">מסך הבית של מסך הפתיחה (074zc · sHome) — האריח החמישי מתווסף רק כש-TCOF קיים</text>
<rect x="250" y="44" width="500" height="58" rx="14" fill="#ffb020"/><text x="500" y="80" fill="#2a1500" font-size="19" font-weight="900">▶ המשך</text>
<g font-size="15" font-weight="800" fill="#eaf6ff">
<rect x="806" y="118" width="170" height="92" rx="14" fill="#16324f" stroke="#8cecff" stroke-opacity=".45"/><text x="891" y="182">משחק חדש</text>
<rect x="616" y="118" width="170" height="92" rx="14" fill="#16324f" stroke="#8cecff" stroke-opacity=".45"/><text x="701" y="182">שמירות</text>
<rect x="426" y="118" width="170" height="92" rx="14" fill="#16324f" stroke="#8cecff" stroke-opacity=".45"/><text x="511" y="182">הגדרות</text>
<rect x="236" y="118" width="170" height="92" rx="14" fill="#16324f" stroke="#8cecff" stroke-opacity=".45"/><text x="321" y="182">איך משחקים</text>
<rect x="24" y="118" width="192" height="92" rx="14" fill="#1d3f5f" stroke="#ffd27a" stroke-width="2.5"/>
<g transform="translate(104 128) scale(1.1)" fill="none" stroke="#8cecff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="7" width="25" height="18" rx="3.5"/><path d="M3.5 12h25M9 7l-2.6 5M15 7l-2.6 5M21 7l-2.6 5M27 7.4l-2.4 4.6"/><path d="M13.6 15.2v6.4l5.6-3.2z" fill="#ffb020" stroke="#ffb020"/></g>
<text x="120" y="182">סרטון הפתיחה</text><text x="120" y="200" font-size="11.5" font-weight="600" fill="#9fc2da">73 שנ׳ · אפשר לדלג</text></g>
<text x="500" y="238" fill="#a9c6dd" font-size="13">לחיצה / Enter — TCOF.play('home'): הסרטון במסך מלא מעל מסך הפתיחה (הנגן 029c), Esc / Enter — דילוג, ובסוף חוזרים למסך הבית והפוקוס על האריח. בלי TCOF — ארבעה אריחים כמו קודם.</text></g></svg>'''
inv = '''<ul class="inv">
<li><b>009b_opening_logo.js</b> — המסך הראשון: הלוגו של הבעלים (TCLOGO) ו"העיר נטענת…" — בלי התקדמות, בלי טיפים; הלוגו מופיע רק אחרי שהסקריפט הגדול נגמר (פריסה אסינכרונית). <i>נשאר, ו-TCLD יושב מתחתיו.</i></li>
<li><b>074zc_opening.js · TCO</b> — מסך הפתיחה: המשך / משחק חדש / שמירות / הגדרות / איך משחקים / תפריט Esc; הרקע — 11 צילומים מהעולם (TCCITY.grab), כל אחד נבנה כמה שניות. <i>נשאר כמו שהוא; עד שהצילום הראשון מוכן — העיר המצוירת של TCLD מאחור.</i></li>
<li><b>054_core_p283.js · g77LdsUi</b> — חלון "טוען את שדה התעופה…" עם פס כחול ואחוזים. <i>עכשיו ההתקדמות שלו עוברת למסך הטעינה; החלון הישן — רק גיבוי.</i></li>
<li><b>028 MAPBASE · 061/062 WTC · 065 C34</b> — המנגנונים שבונים את המפה, האריחים והרכבים בהדרגה. <i>רק קוראים מהם (כלל 19א) — זו ההתקדמות האמיתית.</i></li>
<li><b>מה היה חסר:</b> בכניסה מהתפריט, ב-F7, במעבר שמירות ובזום רחוק — לא היה שום מסך: העולם הופיע חצי בנוי. אין איורים ואין טיפים בשום מקום.</li></ul>'''
html = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>מסך הטעינה — הציור</title><style>
:root{--bg:#07101c;--ink:#eef7ff;--mut:#a9c6dd;--gold:#ffd27a}body{margin:0;background:radial-gradient(ellipse at 50% 0,#173a5c,#07101c 60%);color:var(--ink);font:16px/1.6 "Segoe UI","Noto Sans Hebrew",Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 80px}h1{color:var(--gold);margin:.2em 0}h2{color:var(--gold);margin-top:1.8em;border-bottom:1px solid rgba(255,210,122,.25);padding-bottom:4px}
.sub{color:var(--mut)}.flow{width:100%;height:auto;background:#0b1a2b;border-radius:16px}.tb{width:100%;border-collapse:collapse}.tb td,.tb th{border-bottom:1px solid #22384f;padding:8px;text-align:right;vertical-align:top}.tb th{color:var(--gold)}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}.gc{background:#0e2238;border-radius:16px;padding:12px;box-shadow:0 0 0 1px rgba(255,210,122,.2)}.gc svg{width:100%;height:auto;display:block;border-radius:12px}.gc h3{color:var(--gold);margin:.5em 0 .2em;font-size:18px}.gc p{margin:0;color:#d7e9f8;font-size:14.5px}
kbd{display:inline-block;min-width:1.4em;text-align:center;font:800 .88em Arial;color:#2a1500;background:linear-gradient(180deg,#fff0b8,#ffb020);border-radius:6px;padding:0 .4em;box-shadow:0 2px 0 #9a5200}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}.btns button{font:700 15px "Segoe UI",Arial;background:#ffb020;color:#2a1500;border:0;border-radius:10px;padding:8px 14px;cursor:pointer}.btns button.x{background:#2a5a86;color:#fff}
.inv li{margin:.4em 0}.inv i{color:var(--mut)}.note{background:#0e2238;border-right:4px solid var(--gold);padding:10px 14px;border-radius:8px}
</style></head><body><main>
<h1>מסך הטעינה ומסך הפתיחה — הציור</h1><div class="sub">טורבו סיטי · 17.11 · הסוכן loading · הציור הוא הקוד עצמו (009c_loading.js) — SVG בקוד, בלי אף תמונה.</div>
<h2>מתי הוא מופיע</h2>__FLOW__
<h2>החי — לחיצה מציגה את המסך האמיתי</h2><p class="sub">אותו קוד שבמשחק. האיורים מתחלפים כל 5 שנ׳; ההתקדמות כאן מדומה בכפתורים (במשחק — מהמדידות).</p>
<div class="btns"><button data-v="boot">פתיחה (מתחת ללוגו)</button><button data-v="strip">פס דק במסך הפתיחה</button><button data-v="full">מסך מלא במשחק</button><button data-v="go">התקדמות +20%</button><button class="x" data-v="off">סגירה (או Esc)</button></div>
<h2>השלבים — התקדמות אמיתית</h2>__STEPS__
<h2>האיורים והטיפים — 10 כרטיסים</h2><div class="gal">__GAL__</div>
<h2>מסך הפתיחה — "סרטון הפתיחה" (17.11, תלות מ-opening)</h2>__HOME__
<h2>מה מצאתי (המלאי — כלל 19)</h2>__INV__
<p class="note">ברירות המחדל (לאישורך): בזמן מסך מלא בתוך המשחק — העולם מושהה והמקשים לא עוברים (F5/F11/F12 עוברים); מקסימום 25 שנ׳. זום רחוק / אזור כבד — רק כשיותר מ-40% מהמסך חסר יותר משליש שנייה, פעם ב-20 שנ׳ לכל היותר. ב-#dev ובבדיקות — כבוי, כמו מסך הפתיחה (‎#loading מכריח).</p>
</main><script>window.__TCO_SKIP=true;</script><script>__PART__</script><script>
(function(){var G=document.querySelector('.gal');TCLD._css();G.innerHTML='<svg width="0" height="0" style="position:absolute">'+TCLD._grad()+'<defs><marker id="ldArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#ffd27a"/></marker></defs></svg>'+TCLD.cards.map(function(c){return'<div class="gc">'+c.a+'<h3>'+c.t+'</h3><p>'+c.p+'</p></div>'}).join('');
 var f={code:0,save:0,map:0,tiles:0,cars:0};function bump(){for(var k in f){if(f[k]<1){f[k]=Math.min(1,f[k]+.5);TCLD.set(k,f[k],f[k]<1?Math.round(f[k]*24)+'/24':'');return}}}
 document.querySelector('.btns').addEventListener('click',function(e){var v=e.target.getAttribute('data-v');if(!v)return;if(v==='off'){TCLD.hide('demo');return}if(v==='go'){bump();return}
  f={code:1,save:v==='boot'?0:1,map:.25,tiles:0,cars:0};TCLD.hide('demo');TCLD.show(v==='full'?'save':v==='strip'?'strip':'boot',{view:v,force:true,steps:['code','save','map','tiles','cars']});for(var k in f)TCLD.set(k,f[k],k==='map'?'6/24':'');if(v==='boot')TCLD.set('save',null,'נקראת');if(v!=='strip')document.getElementById('tcldRoot').style.pointerEvents='all';document.getElementById('tcldRoot').onclick=function(){TCLD.hide('demo')}});
 addEventListener('keydown',function(e){if(e.key==='Escape')TCLD.hide('demo')})})();
</script></body></html>'''
html = html.replace('__FLOW__', flow).replace('__STEPS__', steps).replace('__INV__', inv).replace('__HOME__', home).replace('__GAL__', '').replace('__PART__', part.replace('</script', '<\\/script'))
open(out, 'w', encoding='utf-8').write(html)
b = html.encode('utf-8'); print(out, len(b), hashlib.sha1(b).hexdigest()[:12], 'data:image' in html, '<img' in html)
