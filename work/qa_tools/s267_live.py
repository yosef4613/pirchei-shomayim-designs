#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s267_live.py <game.html> <out.html> — הדף החי של S7F267 (סוף S9a): המשחק עצמו (הבנייה הרשמית כמו שהיא) עם לוח קטן בעברית שמזיז את המצלמה
החופשית אל המקומות של הבנייה, וכפתורי יום ולילה. בדפוס של study/pages/make_zone_page.py (בלי צילומים — הכול מצויר בקוד של המשחק)."""
import sys, re, json, hashlib
src, out = sys.argv[1:3]
TITLE = 'S7F267 — סוף S9a: הגג של E3, המפרצים והמסוף'
SPOTS = [('המסוף בבוקר', 5300, 1975, 1.0), ('הגג השקוף', 5830, 2145, 1.0), ('מעברי המסוף', 5620, 1980, 1.9), ('ST-01 מזרח', 4700, 2229, 1.8),
         ('ST-03 דרום', 2114, 1700, 1.8), ('ST-10 מזרח', 4720, 2924, 1.8), ('ST-11 מערב', 3650, 1054, 1.8), ('כיכר הספורט', 1200, 2600, 1.7),
         ('הקווים — מפה', 3000, 2600, 0.3)]
H = open(src, encoding='utf-8').read()
H, n = re.subn(r'<title>[^<]*</title>', '<title>' + TITLE + '</title>', H, count=1); assert n == 1
S = [dict(n=a, v=[x, y, z]) for a, x, y, z in SPOTS]
btn = 'font:inherit;color:#0b1520;background:#f2c230;border:0;border-radius:7px;padding:5px 9px;cursor:pointer'
btn2 = 'font:inherit;color:#fff;background:#2b3a48;border:1px solid #5d7183;border-radius:7px;padding:5px 9px;cursor:pointer'
PANEL = ('<div id="tcZoneBar" style="position:fixed;top:8px;right:8px;z-index:2147483000;direction:rtl;font:600 13px/1.4 \'Segoe UI\',Arial,sans-serif;'
         'background:rgba(8,16,24,.86);color:#fff;padding:8px 10px;border-radius:10px;max-width:320px">'
         '<div style="margin-bottom:6px">' + TITLE + '</div><div id="tcZoneBtns" style="display:flex;flex-wrap:wrap;gap:6px"></div>'
         '<div style="display:flex;gap:6px;margin-top:6px"><button id="tcDay" style="' + btn2 + '">יום</button><button id="tcNight" style="' + btn2 + '">לילה</button></div>'
         '<div style="margin-top:6px;font-weight:400;opacity:.85">לחיצה מעבירה את המצלמה למקום. גלגלת — זום. ‏F4 — חזרה לנהיגה.</div></div>'
         '<script>(function(){var S=' + json.dumps(S, ensure_ascii=False) + ';var B=document.getElementById("tcZoneBtns");'
         'S.forEach(function(s){var b=document.createElement("button");b.textContent=s.n;b.style.cssText="' + btn + '";b.onclick=function(){go(s)};B.appendChild(b)});'
         'function ev(c){try{return window.__TC_DEV.ev(c)}catch(e){}}'
         'function go(s){if(s.n==="המסוף בבוקר")night(0);ev("(()=>{State.mapQa=true;Camera.x="+s.v[0]+";Camera.y="+s.v[1]+";Camera.zoom="+s.v[2]+";try{updateMapQaButton()}catch(e){}return 1})()")}'
         'function night(n){ev("(()=>{c34Night("+n+");try{wtcInvalidate()}catch(e){}return 1})()")}'
         'document.getElementById("tcDay").onclick=function(){night(0)};document.getElementById("tcNight").onclick=function(){night(1)};'
         'var t=0,iv=setInterval(function(){t++;try{if(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()&&t>6){go(S[0]);clearInterval(iv)}}catch(e){}if(t>240)clearInterval(iv)},500)})();</script>')
j = H.find('<head>'); assert j >= 0
H = H[:j + 6] + '<script>/* דף חי: ממשק המצלמה של המשחק (#dev) */if(!/(^#|&)dev(&|$)/.test(location.hash))history.replaceState(null,"",location.pathname+location.search+"#dev");</script>' + H[j + 6:]
i = H.rfind('</body>'); assert i > 0
H = H[:i] + PANEL + H[i:]
open(out, 'w', encoding='utf-8').write(H)
b = H.encode('utf-8'); print('ok', out, len(b), hashlib.sha1(b).hexdigest()[:12])
