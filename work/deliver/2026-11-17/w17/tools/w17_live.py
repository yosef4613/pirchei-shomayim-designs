#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""w17_live.py <game.html> <out.html> — "ניסיון לבעלים" של w17 (17.11): המשחק עצמו (#dev) עם לוח בעברית —
מכונית־העל השנייה "שביט" (VH-SP-06): מקרוב באולם, האולם (ליד טריז), על הכביש, חונה ליד המלון, השחקן ליד החונה (E), דלתות הפרפר;
לעלות על כל כלי: השחקן ליד קטנוע / אופנוע / אופניים / ג׳יפ / טרקטורון (ואז E), ליד אופנוע המשטרה (E נותן את הסיבה); הסוכנות (הקטלוג).
בלי תמונות. הדפוס: sp05/tools/sp05_live.py (כלל 19א)."""
import sys, json, re, hashlib
src, out = sys.argv[1], sys.argv[2]
title = 'w17 — לעלות על כל כלי · מכונית־העל "שביט"'
H = open(src, encoding='utf-8').read()
H, n = re.subn(r'<title>[^<]*</title>', '<title>' + title + '</title>', H, count=1); assert n == 1
btn = 'font:inherit;color:#0b1520;background:#7fd0f2;border:0;border-radius:7px;padding:4px 8px;cursor:pointer'
NOTE = ('שביט (SP-06) — טיפה ארוכה ועגולה, תא קטן קדימה, סנפיר על הזנב, חוט אור לכל רוחב החזית, טבעות אור מאחור, חישוקי דיסק, דלתות פרפר; כחול קרח / אדום / סגול. '
        'הכלים של W17: הכפתור מעמיד את השחקן ליד הכלי — ואז E במקלדת: הוא עולה ורוכב (WASD), E שוב — יורד. הכלי שאול: חוזר למקומו 90 שנ׳ אחרי שמתרחקים. '
        'אחרי לחיצה — רגע עד שהצייר מכין את התמונה.')
GO = ("(function(k){var C=Camera;clearInterval(window.__w7F);window.__w7F=0;try{setPhoneOpen(false)}catch(e){}"
      "var cam=function(x,y,z){State.mapQa=true;C.x=x;C.y=y;C.zoom=z};var free=function(){State.mapQa=false};try{c34LibInit()}catch(e){}var S=__TC_SP06.find('parked');"
      "var walkTo=function(x,y,h){if(PlayerProfile.mode!=='walk'){PlayerCar.speed=0;try{exitVehicle()}catch(e){}}PlayerPed.x=x-Math.sin(h||0)*20;PlayerPed.y=y+Math.cos(h||0)*20;C.x=x;C.y=y;C.zoom=4.2;free()};"
      "if(k==='close'){if(!S)return 'אין כרגע שביט חונה';cam(S.x,S.y-2,9);return 'מקרוב — שביט חונה ליד מלון הים F3'}"
      "if(k==='hall'){var T=__TC_SP05.find('parked');if(!T)return 'אין';cam(T.x,T.y-2,8);return 'טריז (SP-05) חונה ליד המלון הגדול D2 — להשוואה'}"
      "if(k==='road'){var L=TRAFFIC_CARS.filter(function(q){return q.asset==='VH-SP-06'});if(!L.length)return 'אין כרגע על הכביש';var q=L[0];window.__w7F=setInterval(function(){try{cam(q.x,q.y,5.5)}catch(e){}},40);return 'על הכביש — המצלמה אחרי '+q.id}"
      "if(k==='park'||k==='walk'){var P=__TC_SP06.find('parked');if(!P)return 'אין כרגע שביט חונה';if(k==='park'){cam(P.x,P.y,5.5);return 'שביט חונה ליד המלון'}walkTo(P.x,P.y,P.h);return 'השחקן ליד שביט — E: דלת הפרפר עולה והוא נכנס'}"
      "if(k==='open'){var v=!window.__w7O;window.__w7O=v;__TC_SP06.doors(v);return v?'הדלתות פתוחות — על הכביש ובחניה':'הדלתות סגורות (באולם — תמיד למעלה)'}"
      "if(k==='h21'){gameClockSet(21,0);return 'לילה — 21:00: חוט האור, הטבעות האדומות'}if(k==='h9'){gameClockSet(9,0);try{c34Night(0)}catch(e){}return 'יום — 09:00'}"
      "if(/^v:/.test(k)){var t=k.slice(2),o=null;if(t==='JP'||t==='AT'){var A=W17.off.filter(function(a){return a.type===t})[0];if(!A)return 'אין';var p=A.plan[0].at;walkTo(p.x,p.y,p.h);"
      "return (t==='JP'?'ליד הג׳יפ':'ליד הטרקטורון')+' בתחנה שלו — E כשהוא עומד בה (הוא יוצא לסיבוב ב-'+(t==='JP'?'84':'120')+' השניות האחרונות של כל 6 דקות)'}"
      "o=VehicleWorld.extra.filter(function(q){return q.asset==='W17-'+t})[0];if(!o){var v2=TRAFFIC_CARS.filter(function(q){return q.asset==='W17-'+t})[0];if(!v2)return 'אין כרגע';walkTo(v2.x,v2.y,v2.heading);return 'ליד '+W17R.he[t]+' בתנועה — E: '+(w17rWhyNot(v2,true)||'')}"
      "walkTo(o.x,o.y,o.heading);return 'השחקן ליד '+W17R.he[t]+' ('+o.id+') — E'+(W17R.lock[t]?': '+W17R.lock[t]:' כדי לעלות')}"
      "if(k==='dealer'){walkTo(4380,2262,0);return 'ליד הסוכנות D3 — F לכניסה: '+Object.keys(VEHICLE_CATALOG).length+' דגמים בקטלוג'}"
      "return k})")
STATUS = ("(()=>{try{const c=__TC_SP06.census(),r=__TC_W17R.stats(),n=nearestDriveableVehicle();"
          "return 'שביט בעיר: '+c.traffic+' על הכביש · '+c.parked+' חונה · באולם: '+(c.showroom.slot?'כן':'לא')+' · השחקן: '+(PlayerProfile.mode==='vehicle'?'ב'+((W17R.he[(PlayerCar.asset||'').slice(4,6)])||PlayerCar.asset):'ברגל')+(n?' · E: '+n.id:'')+(r.blocked?' · '+r.blocked.msg:'')}catch(e){return ''}})()")
G = [{'g': 'שביט (SP-06)', 'b': [{'n': 'מקרוב', 'k': 'close'}, {'n': 'טריז להשוואה', 'k': 'hall'}, {'n': 'על הכביש', 'k': 'road'}, {'n': 'חונה ליד המלון', 'k': 'park'}, {'n': 'השחקן ליד החונה (E)', 'k': 'walk'}, {'n': 'דלתות פתוחות / סגורות', 'k': 'open'}]},
     {'g': 'לעלות על כל כלי (ואז E)', 'b': [{'n': 'קטנוע', 'k': 'v:SC'}, {'n': 'אופנוע', 'k': 'v:MC'}, {'n': 'אופניים', 'k': 'v:BK'}, {'n': 'ג׳יפ', 'k': 'v:JP'}, {'n': 'טרקטורון', 'k': 'v:AT'}, {'n': 'קטנוע שליח (סיבה)', 'k': 'v:CR'}]},
     {'g': 'הסוכנות והשעה', 'b': [{'n': 'ליד הסוכנות D3 (F)', 'k': 'dealer'}, {'n': 'לילה', 'k': 'h21'}, {'n': 'יום', 'k': 'h9'}]}]
PANEL = ('<div id="tcZoneBar" style="position:fixed;top:8px;right:8px;z-index:2147483000;direction:rtl;font:600 12.5px/1.4 \'Segoe UI\',Arial,sans-serif;'
         'background:rgba(8,16,24,.88);color:#fff;padding:8px 10px;border-radius:10px;max-width:380px;max-height:86vh;overflow:auto">'
         '<div style="margin-bottom:6px">' + title + ' <button id="tcFold" style="' + btn + '">−</button></div>'
         '<div id="tcZoneBtns"></div>'
         '<div id="spMsg" style="margin-top:6px;font-weight:400;color:#c8f59a"></div>'
         '<div id="spLine" style="margin-top:6px;font-weight:400;color:#ffe08a"></div>'
         '<div style="margin-top:6px;font-weight:400;opacity:.85">' + NOTE + '</div>'
         '<script>(function(){var D=' + json.dumps(G, ensure_ascii=False) + ';var B=document.getElementById("tcZoneBtns");'
         'D.forEach(function(g){var h=document.createElement("div");h.textContent=g.g;h.style.cssText="margin:6px 0 3px;opacity:.8";B.appendChild(h);var w=document.createElement("div");w.style.cssText="display:flex;flex-wrap:wrap;gap:5px";B.appendChild(w);'
         'g.b.forEach(function(s){var b=document.createElement("button");b.textContent=s.n;b.style.cssText="' + btn + '";b.onclick=function(){go(s.k)};w.appendChild(b)})});'
         'function ev(c){try{return window.__TC_DEV.ev(c)}catch(e){}}'
         'function go(k){var r=ev(' + json.dumps(GO) + '+"("+JSON.stringify(k)+")");var m=document.getElementById("spMsg");if(m)m.textContent=r||k}window.__w7go=go;'
         'document.getElementById("tcFold").onclick=function(){var x=document.getElementById("tcZoneBtns");x.style.display=x.style.display==="none"?"":"none"};'
         'setInterval(function(){try{if(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()){var t=ev(' + json.dumps(STATUS) + ');if(t)document.getElementById("spLine").textContent=t}}catch(e){}},1000);'
         'var t=0,iv=setInterval(function(){t++;try{if(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()&&t>6){go("close");clearInterval(iv)}}catch(e){}if(t>240)clearInterval(iv)},500)})();</script></div>')
j = H.find('<head>'); assert j >= 0
H = H[:j + 6] + '<script>/* דף חי: ממשק המצלמה של המשחק (#dev) */if(!/(^#|&)dev(&|$)/.test(location.hash))history.replaceState(null,"",location.pathname+location.search+"#dev");</script>' + H[j + 6:]
i = H.rfind('</body>'); assert i > 0
H = H[:i] + PANEL + H[i:]
open(out, 'w', encoding='utf-8').write(H)
b = H.encode('utf-8'); print('ok', out, len(b), hashlib.sha1(b).hexdigest()[:12], 'data:image', H.count('data:image'))
