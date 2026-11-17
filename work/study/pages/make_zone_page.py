# -*- coding: utf-8 -*-
# 2.11 20:05 · הבעלים: "כלל ברזל — אין לתת לי תמונות, רק את האזור בקוד". דף אזור = קובץ המשחק כמו שהוא, עם לוח קטן בעברית שמזיז את המצלמה
# החופשית (State.mapQa, כמו כפתורי המבט של המשחק) אל חלקי האזור. בלי תמונות, הכול מצויר בקוד של המשחק.
# usage: python3 make_zone_page.py <game.html> <out.html> "<כותרת>" "<שם>:x,y,zoom;<שם>:x,y,zoom;..."
import sys, re, json
src, out, title, spots = sys.argv[1:5]
H = open(src, encoding='utf-8').read()
H, n = re.subn(r'<title>[^<]*</title>', '<title>' + title.replace('<', '') + '</title>', H, count=1); assert n == 1
S = [dict(n=p.split(':')[0], v=[float(x) for x in p.split(':')[1].split(',')]) for p in spots.split(';') if p.strip()]
PANEL = ('<div id="tcZoneBar" style="position:fixed;top:8px;right:8px;z-index:2147483000;direction:rtl;font:600 13px/1.4 \'Segoe UI\',Arial,sans-serif;'
         'background:rgba(8,16,24,.86);color:#fff;padding:8px 10px;border-radius:10px;max-width:300px">'
         '<div style="margin-bottom:6px">' + title.replace('<', '') + '</div><div id="tcZoneBtns" style="display:flex;flex-wrap:wrap;gap:6px"></div>'
         '<div style="margin-top:6px;font-weight:400;opacity:.85">לחיצה מעבירה את המצלמה למקום. ‏F4 — חזרה לנהיגה.</div></div>'
         '<script>(function(){var S=' + json.dumps(S, ensure_ascii=False) + ';var B=document.getElementById("tcZoneBtns");'
         'S.forEach(function(s){var b=document.createElement("button");b.textContent=s.n;b.style.cssText="font:inherit;color:#0b1520;background:#f2c230;border:0;border-radius:7px;padding:5px 9px;cursor:pointer";'
         'b.onclick=function(){go(s)};B.appendChild(b)});function go(s){try{window.__TC_DEV.ev("(()=>{State.mapQa=true;Camera.x="+s.v[0]+";Camera.y="+s.v[1]+";Camera.zoom="+s.v[2]+";try{updateMapQaButton()}catch(e){}return 1})()")}catch(e){}}'
         'var t=0,iv=setInterval(function(){t++;try{if(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()&&t>6){go(S[0]);clearInterval(iv)}}catch(e){}if(t>240)clearInterval(iv)},500)})();</script>')
j = H.find('<head>'); assert j >= 0
H = H[:j + 6] + '<script>/* דף אזור: ממשק המצלמה של המשחק (#dev) */if(!/(^#|&)dev(&|$)/.test(location.hash))history.replaceState(null,"",location.pathname+location.search+"#dev");</script>' + H[j + 6:]
i = H.rfind('</body>'); assert i > 0
H = H[:i] + PANEL + H[i:]
open(out, 'w', encoding='utf-8').write(H); print('ok', len(H.encode('utf-8')))
