#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mb_live.py <game.html> <out.html> — הדף החי של לוח המשימות (D‑693, סבב 17.11): המשחק עצמו עם לוח בעברית וכפתורים.
הדפוס: deliver/2026-11-11/missions/tools/missions_live.py. בלי צילומים ובלי תמונות (כלל 17).
הלוח של המשימות רץ במשחק האמיתי; בדף החי (‎#dev) הוא מופעל בכפתור הראשון (או לבד אחרי הטעינה)."""
import sys, re, json
src, out = sys.argv[1], sys.argv[2]
title = 'לוח המשימות — D‑693'
G = [('הלוח', [
        ('להפעיל את הלוח (4 משימות צד)', "(()=>{__TC_MB.force(true);__TC_MB.tick();return 1})()"),
        ('הסיפור — הקבוצה הראשונה (1-3 · 1-4 · 1-5 בכל סדר)', "(()=>{__TC_MB.force(true);__TC_STORY.jump('1-3');return 1})()"),
        ('השלב הבא בסיפור', "(()=>{__TC_STORY.skip();return 1})()"),
        ('להשלים משימת צד אחת (הראשונה בלוח)', "(()=>{const S=__TC_MB.state(),it=S.items[0];if(!it)return 0;const id=it.key.slice(2);if(it.key[0]==='z'){if(S9STORY.step(id)<1)__TC_MB.act('acc',it.key);let g=0;while(!S9STORY.done(id)&&g++<12)S9STORY.advance(id)}else{__TC_MB.E.jobsDone.push(id);PlayerProfile.progression.completedMissions.push(id)}__TC_MB.tick();return 1})()"),
        ('הצעה עכשיו (כשיש 4–5)', "(()=>{const b=g77St().board;if(b)b.t=-1e9;__TC_MB.tick();return 1})()"),
        ('שעה קדימה', "(()=>{const c=gameClock();gameClockSet((c.hour+1)%24,c.minute);return 1})()"),
        ('שכבה גבוהה — "אירוע" ל-10 שנ׳ (TCBUSY): הכרטיס וההצעה מחכים', "(()=>{const M=__TC_MB;M.force(true);M.tick();const b=M.board(),k=b&&b.side[1]&&b.side[1].key;TCBUSY.set('event',{why:'הדף החי',ttl:10000});if(k){M.E.card=null;M.E.cardQ=M.E.cardQ.filter(x=>x.key!==k);M.E.cardQ.unshift({key:k,why:'side'})}return 1})()"),
        ('סוף מה שנבנה (פרק 5 — בקרוב): משימת ההמשך', "(()=>{const m=g77St().main,c=TCSTORY.D.chapters.find(x=>x.soon);if(!m||!c)return 0;__TC_MB.force(true);m.ch=c.id;m.mi=null;m.step=0;m.st={};m.par={};m.end=false;__TC_MB.tick();return 1})()"),
        ('סצנה של הסיפור ("הטנדר של סבא") — הכרטיס מחכה מתחתיה', "(()=>{const M=__TC_MB;M.force(true);M.tick();const b=M.board(),k=b&&b.side[0]&&b.side[0].key;if(k){M.E.card=null;M.E.cardQ=M.E.cardQ.filter(x=>x.key!==k);M.E.cardQ.unshift({key:k,why:'side'})}TCCUT.play('1-van');return 1})()")]),
     ('לראות', [
        ('הטלפון · יומן (המשימות הפעילות)', "(()=>{setPhoneOpen(true);openPhoneApp('journal');return 1})()"),
        ('הטלפון · הודעות', "(()=>{setPhoneOpen(true);g77Sp().thread=null;openPhoneApp('msgs');return 1})()"),
        ('הטלפון · עבודות', "(()=>{setPhoneOpen(true);openPhoneApp('missions');return 1})()"),
        ('המפה הגדולה (M)', "(()=>{setPhoneOpen(false);setMapOpen(true);return 1})()"),
        ('סגירה', "(()=>{setPhoneOpen(false);setMapOpen(false);return 1})()")])]
D = [{'g': g, 'b': [{'n': n, 'c': c} for n, c in items]} for g, items in G]
H = open(src, encoding='utf-8').read()
H, n = re.subn(r'<title>[^<]*</title>', '<title>' + title + '</title>', H, count=1); assert n == 1
btn = 'font:inherit;color:#0b1520;background:#4fdc78;border:0;border-radius:7px;padding:4px 8px;cursor:pointer'
btn2 = 'font:inherit;color:#fff;background:#2b3a48;border:1px solid #5d7183;border-radius:7px;padding:4px 8px;cursor:pointer'
NOTE = ('משימות צד על המפה — לפחות 4, לכל היותר 6; כשאחת נגמרת — מיד חדשה, בשטח הפתוח. בין 4 ל-6 — הצעה אחת לכל היותר, שלא נספרת עד "קבל". '
        'לכל משימה: הודעה (בשרשור — קבל / נווט / התקשר), כרטיס קופץ מימין, שורה ביומן, סמן במפה ויעד ניווט. '
        'הסיפור: 1 עד 3 משימות פתוחות יחד, בכל סדר — השורה של הסיפור כותבת "גם פתוחות". '
        'סדר השכבות (TCBUSY): טעינה > סרטון הפתיחה > סצנה > הדרכה > אירוע > כרטיס — כרטיס והצעה לא קופצים מעל שכבה גבוהה, אלא מחכים ובאים אחריה. '
        'בסוף מה שנבנה מהסיפור (פרק 5 — בקרוב) — משימת המשך אחת נספרת כמשימת הסיפור, כך שתמיד יש לפחות 1.')
PANEL = ('<div id="mbBar" style="position:fixed;bottom:8px;left:8px;z-index:2147483000;direction:rtl;font:600 12.5px/1.4 \'Segoe UI\',Arial,sans-serif;'
         'background:rgba(8,16,24,.92);color:#fff;padding:8px 10px;border-radius:10px;max-width:420px;max-height:62vh;overflow:auto">'
         '<div style="margin-bottom:4px">' + title + '</div><div id="mbCnt" style="margin-bottom:6px;color:#ffd36a">…</div>'
         '<div style="display:flex;gap:6px;margin-bottom:6px"><button id="mbFold" style="' + btn2 + '">הסתרה</button></div>'
         '<div id="mbBtns"></div><div id="mbNote" style="margin-top:6px;font-weight:400;opacity:.85">' + NOTE + '</div></div>'
         '<script>(function(){var D=' + json.dumps(D, ensure_ascii=False) + ';var B=document.getElementById("mbBtns");'
         'function ev(c){try{return window.__TC_DEV.ev(c)}catch(e){}}'
         'D.forEach(function(g){var h=document.createElement("div");h.textContent=g.g;h.style.cssText="margin:6px 0 3px;opacity:.8";B.appendChild(h);var w=document.createElement("div");w.style.cssText="display:flex;flex-wrap:wrap;gap:5px";B.appendChild(w);'
         'g.b.forEach(function(s){var b=document.createElement("button");b.textContent=s.n;b.style.cssText="' + btn + '";b.onclick=function(){ev(s.c);try{document.getElementById("game").focus()}catch(e){}};w.appendChild(b)})});'
         'document.getElementById("mbFold").onclick=function(){for(var k of ["mbBtns","mbNote"]){var x=document.getElementById(k);x.style.display=x.style.display==="none"?"":"none"}};'
         'var on=false;setInterval(function(){try{if(!(window.__TC_DEV&&window.__TC_DEV.ready&&window.__TC_DEV.ready()))return;if(!on){on=true;ev("(()=>{__TC_MB.force(true);return 1})()")}'
         'var s=ev("JSON.stringify(__TC_MB.state())");if(typeof s!=="string")return;var q=JSON.parse(s);document.getElementById("mbCnt").textContent="סיפור "+q.story+" / 3 · משימות צד "+q.side+" / 6 · הצעה ממתינה "+(q.offer?1:0)+" · בביצוע "+q.running+(q.sx?" · משימת ההמשך":"")+" · שכבה: "+(ev("TCBUSY.top()")||"—")}catch(e){}},1000)})();</script>')
j = H.find('<head>'); assert j >= 0
H = H[:j + 6] + '<script>/* דף חי: ממשק המצלמה של המשחק (#dev) */if(!/(^#|&)dev(&|$)/.test(location.hash))history.replaceState(null,"",location.pathname+location.search+"#dev");</script>' + H[j + 6:]
i = H.rfind('</body>'); assert i > 0
H = H[:i] + PANEL + H[i:]
open(out, 'w', encoding='utf-8').write(H)
print(out, len(H.encode('utf-8')))
