#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ff_live.py <game.html> <out.html> — הדף החי של fieldfix: המשחק עצמו (הניסיון כמו שהוא, ‎#dev) עם לוח בעברית — כפתורי מצלמה ושעון:
הצבעים ב-3/4 (חדש / ישן, 3/4 / מלמעלה), R3 ביום ובלילה (המחזור של ההאנגרים, מעקב אחרי הגרירה), טיסת המנהלים FL-GA1 (מעקב), העלייה בשרוול. בלי תמונות.
(על פי deliver/2026-11-11/gacolor/tools/ga_live.py)"""
import sys, re, json, hashlib
src, out = sys.argv[1:3]
TITLE = 'השדה — תיקונים מיידיים'
H = open(src, encoding='utf-8').read()
btn = 'font:inherit;color:#0b1520;background:#f2c230;border:0;border-radius:7px;padding:3px 7px;cursor:pointer'
btn2 = 'font:inherit;color:#fff;background:#2b3a48;border:1px solid #5d7183;border-radius:7px;padding:3px 7px;cursor:pointer'
PLACES = [('קונפטי ב-P5 (נקודות)', 8186, 560, 1.1), ('הענק ב-P1 (קונפטי)', 6399, 640, .75), ('המשא ב-C1 (האחורי בצבע הזנב)', 5123, 420, .9),
          ('האנגרים א׳–ג׳', 8650, 1520, .8), ('R3 — רחבת ההרצה', 9369, 2260, 1.0), ('מסלול ההסעה C', 8800, 1840, .7), ('GA1 — המנהלים', 7350, 2010, 1.3), ('השרוול של P2', 7380, 900, 1.6)]
GAME_JS = ('window.__FFL={hm:function(h,m){try{wldAuto();gameClockSet(h,m)}catch(e){}return 1},'
           'r3:function(){try{var c=s15Clock(),S=FFR3.state(c);return (S.mem?S.mem.h.name+" · "+S.mem.ac:"")+(S.out?(S.tow?" · בגרירה":(S.runup?" · מריץ מנועים ב-R3":" · ב-R3")):" · בהאנגר — R3 ריק")}catch(e){return ""}},'
           'followTow:function(){try{var S=FFR3.state(s15Clock());if(!S.p)return 0;State.mapQa=true;Camera.x=S.p[0];Camera.y=S.p[1];return 1}catch(e){return 0}},'
           'ga1:function(){var a=S15_FL["FL-GA1"];if(!a)return 0;var P=s15PoseAt(a,s15Tc(s15Clock().abs));if(!P)return 0;State.mapQa=true;Camera.x=P[0];Camera.y=P[1]-S15_K*P[3];return 1},'
           'ga1At:function(k){var a=S15_FL["FL-GA1"];if(!a)return null;var T=S15SIM.T;for(var t=0;t<T;t+=1){var P=s15PoseAt(a,t);if(!P)continue;if(k==="park"&&P[4]===0)return t;if(k==="air"&&P[3]>40&&P[3]<200)return t;if(k==="push"&&P[4]===2)return t}return null},'
           'tcAt:function(tc){var T=S15SIM.T,base=Math.floor(s15Clock().abs/T)*T+tc;var m=(base/2)%1440;this.hm(Math.floor(m/60),Math.floor(m%60));return 1},'
           'liv:function(on){window.FFLIV=window.FFLIV||{};window.FFLIV.on=!!on;try{A34G.S.clear()}catch(e){}return 1},'
           'a34:function(on){try{S15A3.on=!!on}catch(e){}return 1}};1')
SS = [dict(n=n, v=[x, y, z]) for n, x, y, z in PLACES]
PANEL = ('<div id="tcZoneBar" style="position:fixed;top:8px;right:8px;z-index:2147483000;direction:rtl;font:600 12px/1.4 \'Segoe UI\',Arial,sans-serif;'
         'background:rgba(8,16,24,.88);color:#fff;padding:8px 10px;border-radius:10px;max-width:min(400px,calc(100vw - 32px));max-height:92vh;overflow:auto">'
         '<div style="display:flex;gap:6px;align-items:center;margin-bottom:4px"><span style="flex:1">' + TITLE + '</span><button id="tcFold" style="' + btn2 + '">הסתר</button></div>'
         '<div id="tcBody"><div style="margin:7px 0 3px;opacity:.85">המקומות</div><div id="tcBtnsA" style="display:flex;flex-wrap:wrap;gap:4px"></div>'
         '<div style="margin:7px 0 3px;opacity:.85">(1) הצבעים — אותו צייר</div><div style="display:flex;flex-wrap:wrap;gap:4px">'
         '<button id="lvNew" style="' + btn + '">3/4 אחרי — כמו מלמעלה</button><button id="lvOld" style="' + btn2 + '">3/4 לפני (הישן)</button><button id="lvTop" style="' + btn2 + '">מלמעלה</button></div>'
         '<div style="margin:7px 0 3px;opacity:.85">(2) R3 והמחזור של ההאנגרים (השעון של המשחק)</div><div style="display:flex;flex-wrap:wrap;gap:4px">'
         '<button id="r3Day" style="' + btn + '">12:00 — R3 ריק</button><button id="r3Tow" style="' + btn + '">18:10 — הגרירה (מעקב)</button><button id="r3Run" style="' + btn + '">22:00 — הרצת מנועים</button>'
         '<button id="r3Back" style="' + btn + '">04:45 — חזרה (מעקב)</button></div>'
         '<div style="margin:7px 0 3px;opacity:.85">(3) טיסת המנהלים FL-GA1 (AC-BJ-01)</div><div style="display:flex;flex-wrap:wrap;gap:4px">'
         '<button id="gaPark" style="' + btn + '">בעמדה</button><button id="gaPush" style="' + btn + '">נדחף ומסיע (מעקב)</button><button id="gaAir" style="' + btn + '">באוויר (מעקב)</button></div>'
         '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px"><button id="tcStop" style="' + btn2 + '">עצור מעקב</button><button id="tcDay" style="' + btn2 + '">יום</button><button id="tcNight" style="' + btn2 + '">לילה</button></div>'
         '<div id="tcInfo" style="margin-top:6px;font-weight:400;opacity:.9"></div>'
         '<div style="margin-top:6px;font-weight:400;opacity:.85">לחיצה מעבירה את המצלמה. גלגלת — זום. ‏F4 — חזרה למשחק. בכל לילה מטוס אחר: א׳ → ב׳ → ג׳.</div></div></div>'
         '<script>(function(){var S=' + json.dumps(SS, ensure_ascii=False) + ',fol=null;'
         'function ev(c){try{return window.__TC_DEV.ev(c)}catch(e){}}'
         'function night(n){ev("(()=>{c34Night("+n+");try{wtcInvalidate()}catch(e){}return 1})()")}'
         'function stop(){if(fol){clearInterval(fol);fol=null}}'
         'function go(s){stop();ev("(()=>{State.mapQa=true;Camera.x="+s.v[0]+";Camera.y="+s.v[1]+";Camera.zoom="+s.v[2]+";try{updateMapQaButton()}catch(e){}return 1})()")}'
         'function info(t){document.getElementById("tcInfo").textContent=t}'
         'function r3(){info(ev("window.__FFL.r3()")||"")}'
         'function follow(f,z){stop();ev("(()=>{Camera.zoom="+z+";return 1})()");var n=0;fol=setInterval(function(){n++;ev("window.__FFL."+f+"()");if(n%8==0)r3();if(n>600)stop()},120)}'
         'function at(h,m){ev("window.__FFL.hm("+h+","+m+")");night(h>=19||h<5?1:0)}'
         'S.forEach(function(s){var b=document.createElement("button");b.textContent=s.n;b.style.cssText="' + btn + '";b.onclick=function(){go(s)};document.getElementById("tcBtnsA").appendChild(b)});'
         'document.getElementById("lvNew").onclick=function(){ev("window.__FFL.a34(1)");ev("window.__FFL.liv(1)");info("3/4 — הצייר החדש (כמו מלמעלה)")};'
         'document.getElementById("lvOld").onclick=function(){ev("window.__FFL.a34(1)");ev("window.__FFL.liv(0)");info("3/4 — הצייר הישן (לפני)")};'
         'document.getElementById("lvTop").onclick=function(){ev("window.__FFL.a34(0)");info("מלמעלה (המבט הרגיל)")};'
         'document.getElementById("r3Day").onclick=function(){at(12,0);go(S[4]);setTimeout(r3,600)};'
         'document.getElementById("r3Run").onclick=function(){at(22,0);go(S[4]);setTimeout(r3,600)};'
         'document.getElementById("r3Tow").onclick=function(){at(18,10);follow("followTow",.9)};'
         'document.getElementById("r3Back").onclick=function(){at(4,45);follow("followTow",.9)};'
         'function ga(k,z){var t=ev("window.__FFL.ga1At(\\""+k+"\\")");if(t==null){info("FL-GA1 לא נמצא");return}ev("window.__FFL.tcAt("+t+")");night(0);follow("ga1",z);info("FL-GA1 — מטוס המנהלים")}'
         'document.getElementById("gaPark").onclick=function(){ga("park",1.4)};document.getElementById("gaPush").onclick=function(){ga("push",1.2)};document.getElementById("gaAir").onclick=function(){ga("air",1.0)};'
         'document.getElementById("tcStop").onclick=stop;document.getElementById("tcDay").onclick=function(){night(0)};document.getElementById("tcNight").onclick=function(){night(1)};'
         'document.getElementById("tcFold").onclick=function(){var b=document.getElementById("tcBody"),h=b.style.display==="none";b.style.display=h?"":"none";this.textContent=h?"הסתר":"הצג"};'
         'var t=0,iv=setInterval(function(){t++;try{if(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()&&t>6){ev(' + json.dumps(GAME_JS) + ');night(0);go(S[0]);clearInterval(iv)}}catch(e){}if(t>240)clearInterval(iv)},500)})();</script>')
H, n = re.subn(r'<title>[^<]*</title>', '<title>' + TITLE + '</title>', H, count=1); assert n == 1
j = H.find('<head>'); assert j >= 0
H = H[:j + 6] + '<script>/* דף חי: ממשק המצלמה של המשחק (#dev) */if(!/(^#|&)dev(&|$)/.test(location.hash))history.replaceState(null,"",location.pathname+location.search+"#dev");</script>' + H[j + 6:]
i = H.rfind('</body>'); assert i > 0
H = H[:i] + PANEL + H[i:]
open(out, 'w', encoding='utf-8').write(H)
b = H.encode('utf-8'); print('ok', out, len(b), hashlib.sha1(b).hexdigest()[:12])
