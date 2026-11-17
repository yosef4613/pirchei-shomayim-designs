#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cut_live.py <game.html> <out.html> — הדף החי של סצנות הסיפור (17.11, cutscenes): המשחק עצמו עם לוח כפתורים בעברית — כל סצנה, ‏"הסיפור מההתחלה"
ו"קפיצה לפרק". בלי צילומים ובלי תמונות — הכול מצויר בקוד של המשחק. הדפוס: deliver/2026-11-10/bus/tools/bus_live.py."""
import sys, json, re, hashlib
src, out = sys.argv[1], sys.argv[2]
title = 'סצנות הסיפור — בתוך המשחק'
B = [('הסיפור', [('הסיפור מההתחלה — הסצנה של הפתיחה מתנגנת לבד', 'begin'), ('קפיצה לפרק 1 (הטנדר)', 'j:1-2'), ('קפיצה לפרק 2', 'j:2-1'), ('קפיצה לפרק 3 (הנחיתה הבאה)', 'j:3-1'), ('קפיצה לפרק 4', 'j:4-1')]),
     ('פתיחה ופרק 1', [('שמעון מחכה ליד הבית', 'O-home'), ('העיר', '1-city'), ('הטנדר מתניע', '1-van'), ('קו 3 יוצא לנמל', '1-bus3'), ('פרק 1 הושלם', 'end:1')]),
     ('פרק 2', [('מאחורי הקלעים', '2-backstage'), ('אוניית הרכבים עגנה', '2-ship'), ('פרק 2 הושלם', 'end:2')]),
     ('פרק 3', [('מטוס נוחת (מחכה לנחיתה הבאה)', '3-landing'), ('הטיסה של חמש ממריאה (מחכה להמראה הבאה)', '3-takeoff'), ('האורות בשדות', '3-lights'), ('פרק 3 הושלם', 'end:3')]),
     ('פרק 4 והלאה', [('הים', '4-sea'), ('הגוררת מושכת (מחכה לגרירה, אם היא בקרוב)', '4-tug'), ('פרק 4 הושלם', 'end:4'), ('פרק 5 — בקרוב', '5-soon'), ('פרק 6 — בקרוב', '6-soon')])]
H = open(src, encoding='utf-8').read()
H, n = re.subn(r'<title>[^<]*</title>', '<title>' + title + '</title>', H, count=1); assert n == 1
D = [{'g': g, 'b': [{'n': a, 'k': k} for a, k in items]} for g, items in B]
btn = 'font:inherit;color:#0b1520;background:#f2c230;border:0;border-radius:7px;padding:4px 8px;cursor:pointer'
btn2 = 'font:inherit;color:#fff;background:#2b3a48;border:1px solid #5d7183;border-radius:7px;padding:4px 8px;cursor:pointer'
NOTE = ('כל כפתור מנגן סצנה בתוך המשחק החי: המצלמה זזה, הדמויות יוצאות מהמקום, הכתובית למטה. Esc / רווח / "דלג" — חזרה למשחק. '
        '"הסיפור מההתחלה" — הסיפור מתחיל, והסצנה של הפתיחה מתנגנת לבד (כמו במשחק חדש). "קפיצה לפרק" — הסיפור קופץ למשימה, והסצנה שלה מתנגנת לבד; '
        'פרק 3 — "מטוס נוחת" מחכה לנחיתה האמיתית הבאה בשדה, ו"הטיסה של חמש" — להמראה האמיתית הבאה (הזמן — בשורה הצהובה). בשלב של שיחה — הדמות עומדת ליד המקום ומחכה.')
GO = ("(function(k){try{setPhoneOpen(false)}catch(e){}if(State.mapQa)try{toggleMapQa()}catch(e){}State.paused=false;if(PlayerProfile.activeMission)try{missionFail('live')}catch(e){PlayerProfile.activeMission=null}PlayerProfile.activeMission=null;TCCUT.auto(true);"
      "if(k==='begin'){TCSTORY.begin();TCSTORY.bringNow();return 'הסיפור התחיל — הסצנה של הפתיחה'}"
      "if(k.indexOf('j:')===0){TCSTORY.jump(k.slice(2));TCSTORY.bringNow();return 'קפיצה למשימה '+k.slice(2)}"
      "var r=TCCUT.play(k,{why:'live'});var s=TCCUT.scene(k);return (s?s.name:k)+(r==='queued'?' — מחכה לרגע':'')})")
STATUS = ("(()=>{try{const s=TCCUT.state(),L=TCCUT.landInfo(),K=TCCUT.takeoffInfo?TCCUT.takeoffInfo():null,G=TCCUT.tugInfo?TCCUT.tugInfo():null,m=TCSTORY.M();return(s.on?'מתנגנת: '+(TCCUT.scene(s.on.id)||{}).name+' · שוט '+(s.on.shot+1):'אין סצנה עכשיו')+(s.q.length?' · בתור: '+s.q.join(', '):'')+"
          "'\\nהנחיתה הבאה בשדה: בעוד '+(L?Math.max(0,Math.round(L.dt)):'—')+' שנ׳ · ההמראה הבאה: בעוד '+(K?Math.max(0,Math.round(K.dt)):'—')+' שנ׳ · הגרירה: '+(G?(G.now?'עכשיו':'בעוד '+Math.round(G.dtSec/60)+' דק׳'):'—')+(m?' · הסיפור: '+m.ch+' / '+(m.mi||'—')+' שלב '+m.step:'')+(s.presence.length?' · מחכה במקום: '+s.presence.join(', '):'')+' · נוגנו '+s.played}catch(e){return ''}})()")
PANEL = ('<div id="tcCutBar" style="position:fixed;top:8px;right:8px;z-index:2147483000;direction:rtl;font:600 12.5px/1.4 \'Segoe UI\',Arial,sans-serif;'
         'background:rgba(8,16,24,.88);color:#fff;padding:8px 10px;border-radius:10px;max-width:390px;max-height:86vh;overflow:auto">'
         '<div style="margin-bottom:6px">' + title + '</div>'
         '<div style="display:flex;gap:6px;margin-bottom:6px"><button id="tcDay" style="' + btn2 + '">יום</button><button id="tcNight" style="' + btn2 + '">לילה</button><button id="tcFold" style="' + btn2 + '">הסתרה</button></div>'
         '<div id="tcCutBtns"></div>'
         '<div id="tcCutMsg" style="margin-top:6px;font-weight:400;color:#9fe0b0"></div>'
         '<div id="tcCutLine" style="margin-top:6px;font-weight:400;color:#ffe08a;white-space:pre-line"></div>'
         '<div style="margin-top:6px;font-weight:400;opacity:.85">' + NOTE + '</div>'
         '<script>(function(){var D=' + json.dumps(D, ensure_ascii=False) + ';var B=document.getElementById("tcCutBtns");'
         'D.forEach(function(g){var h=document.createElement("div");h.textContent=g.g;h.style.cssText="margin:6px 0 3px;opacity:.8";B.appendChild(h);var w=document.createElement("div");w.style.cssText="display:flex;flex-wrap:wrap;gap:5px";B.appendChild(w);'
         'g.b.forEach(function(s){var b=document.createElement("button");b.textContent=s.n;b.style.cssText="' + btn + '";b.onclick=function(){go(s)};w.appendChild(b)})});'
         'function ev(c){try{return window.__TC_DEV.ev(c)}catch(e){}}'
         'function go(s){var r=ev(' + json.dumps(GO) + '+"("+JSON.stringify(s.k)+")");var m=document.getElementById("tcCutMsg");if(m)m.textContent=r||s.n}'
         'function night(n){ev("(()=>{c34Night("+(n?1:0)+");try{wtcInvalidate()}catch(e){}return 1})()")}'
         'document.getElementById("tcDay").onclick=function(){night(0)};document.getElementById("tcNight").onclick=function(){night(1)};'
         'document.getElementById("tcFold").onclick=function(){var x=document.getElementById("tcCutBtns");x.style.display=x.style.display==="none"?"":"none"};'
         'setInterval(function(){try{if(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()){var t=ev(' + json.dumps(STATUS) + ');if(t)document.getElementById("tcCutLine").textContent=t}}catch(e){}},1000);'
         '})();</script>')
j = H.find('<head>'); assert j >= 0
H = H[:j + 6] + '<script>/* דף חי: ממשק המצלמה של המשחק (#dev) */if(!/(^#|&)dev(&|$)/.test(location.hash))history.replaceState(null,"",location.pathname+location.search+"#dev");</script>' + H[j + 6:]
i = H.rfind('</body>'); assert i > 0
H = H[:i] + PANEL + H[i:]
open(out, 'w', encoding='utf-8').write(H)
b = H.encode('utf-8'); print('ok', out, len(b), hashlib.sha1(b).hexdigest()[:12], sum(len(x['b']) for x in D), 'כפתורים')
