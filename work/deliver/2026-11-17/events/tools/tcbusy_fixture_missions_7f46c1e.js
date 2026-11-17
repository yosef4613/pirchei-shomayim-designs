
/* ===== 17.11 · TCBUSY — סדר השכבות: מנגנון "עסוק" אחד (הסוכן missions, בבקשת המתאם והבקר; הממצא של המיזוג S7F299: הכרטיס של הלוח מעל סצנה).
   רץ בגוף 9 (לפני מסך הטעינה והסקריפט הגדול) — כדי שכל אחד יוכל להשתמש בו מהרגע הראשון. לא מצייר כלום ולא משנה כלום בעצמו: רק עונה "מי על המסך".
   העדיפויות (גבוה → נמוך): loading 60 (מסך הטעינה / מסך הפתיחה) > opening 50 (סרטון הפתיחה) > cutscene 40 (סצנה של הסיפור) > tutorial 30 (ההדרכה)
     > event 20 (אירוע אקראי) > card 10 (כרטיס משימה / הצעה).
   הכלל: שכבה עולה רק כש-TCBUSY.blocks(kind) === false (אין שכבה גבוהה ממנה על המסך). מה שנחסם — נדחה ולא נזרק, ועולה כשמתפנה (when / בדיקה חוזרת).
   הממשק:
     TCBUSY.set(kind[, {why, ttl}])  השכבה שלי עכשיו על המסך. ttl (מ"ש, ברירת מחדל 5 דק׳) — ביטחון: נגמרת לבד אם ה-clear לא הגיע (שגיאה); ttl:0 — בלי סוף.
     TCBUSY.clear(kind)              ירדה מהמסך.
     TCBUSY.probe(kind, fn)          במקום set / clear: fn() → true כשהשכבה על המסך (נקראת רק כששואלים — בלי שעון ובלי מצב שיכול להיתקע).
     TCBUSY.is([kind])               kind על המסך? בלי kind — משהו על המסך.
     TCBUSY.top()                    השכבה הגבוהה שעל המסך ('' כשאין).
     TCBUSY.blocks(kind)             שכבה גבוהה מ-kind על המסך → kind מחכה.
     TCBUSY.when(kind, fn)           fn פעם אחת, כש-kind כבר לא חסום (מיד — אם לא חסום עכשיו).
     TCBUSY.on(fn)                   מאזין: fn(kind, on) בכל set / clear.
     TCBUSY.Z                        ה-z-index לכל שכבה: loading 9650 · opening 9600 · cutscene 9500 · tutorial 60 · event 58 · card 55.
     TCBUSY.PRI, TCBUSY.state()      לבדיקות.
   מחוברים כבר (probe — קריאה בלבד, בלי שינוי בקבצים שלהם): loading — TCLD.st.on ו-TCO ב-'boot' / 'open'; opening — TCSHOW.on (הנגן של הסרטים, 029c); cutscene — TCCUT.playing() / body.tcCutOn;
   tutorial — הכרטיס #tcTut של TCTUT על המסך; card — הכרטיס #tcMbCard של הלוח (074zu_mission_board). event — מתחבר ב-set / clear או ב-probe. ===== */
var TCBUSY=(function(){
 var PRI={loading:60,opening:50,cutscene:40,tutorial:30,event:20,card:10},Z={loading:9650,opening:9600,cutscene:9500,tutorial:60,event:58,card:55};
 var S={},P={},W=[],L=[],n={set:0,clear:0,exp:0,when:0,err:0},err=null,iv=0;
 function now(){return Date.now()}
 function pri(k){return PRI[k]||0}
 function bad(e){n.err++;if(!err)err=String(e&&e.stack||e).slice(0,300)}
 function setOn(k){var s=S[k];if(!s)return false;if(s.until&&now()>s.until){delete S[k];n.exp++;emit(k,false);return false}return true}
 function probeOn(k){var L2=P[k];if(!L2)return false;for(var i=0;i<L2.length;i++){try{if(L2[i]())return true}catch(e){}}return false}
 function is(k){if(k)return setOn(k)||probeOn(k);for(var q in PRI)if(is(q))return true;return false}
 function top(){var b='',p=-1;for(var q in PRI)if(PRI[q]>p&&is(q)){b=q;p=PRI[q]}return b}
 function blocks(k){var p=pri(k);for(var q in PRI)if(PRI[q]>p&&is(q))return true;return false}
 function emit(k,on){for(var i=0;i<L.length;i++){try{L[i](k,on)}catch(e){bad(e)}}if(!on)flush()}
 function set(k,o){if(!PRI[k])return false;o=o||{};var t=o.ttl==null?300000:+o.ttl;S[k]={at:now(),why:o.why||'',until:t>0?now()+t:0};n.set++;emit(k,true);return true}
 function clear(k){if(!S[k])return false;delete S[k];n.clear++;emit(k,false);return true}
 function probe(k,fn){if(!PRI[k]||typeof fn!=='function')return false;(P[k]||(P[k]=[])).push(fn);return true}
 function flush(){if(!W.length){if(iv){clearInterval(iv);iv=0}return}var keep=[];for(var i=0;i<W.length;i++){var w=W[i];if(blocks(w.k)){keep.push(w);continue}n.when++;try{w.fn()}catch(e){bad(e)}}W=keep;if(!W.length&&iv){clearInterval(iv);iv=0}}
 function when(k,fn){if(typeof fn!=='function')return false;if(!blocks(k)){n.when++;try{fn()}catch(e){bad(e)}return true}W.push({k:k,fn:fn});if(!iv)iv=setInterval(flush,250);return false}   /* the probes do not call back — a short check while something waits */
 function on(fn){if(typeof fn==='function')L.push(fn)}
 function state(){var o={top:top(),on:[],wait:W.length,n:n,err:err};for(var q in PRI)if(is(q))o.on.push(q);return o}
 /* what is already in the game (read only) */
 probe('loading',function(){return typeof TCLD!=='undefined'&&TCLD.st&&!!TCLD.st.on});
 probe('loading',function(){return typeof TCO!=='undefined'&&(TCO.mode==='boot'||TCO.mode==='open')});
 probe('opening',function(){return typeof TCSHOW!=='undefined'&&!!TCSHOW.on});   /* the player of the films (029c): the opening film (opening) and the films of the city — full screen */
 probe('cutscene',function(){return (typeof TCCUT!=='undefined'&&TCCUT.playing())||!!(document.body&&document.body.classList.contains('tcCutOn'))});
 probe('tutorial',function(){if(typeof TCTUT==='undefined'||!TCTUT.T||!TCTUT.T.on)return false;var d=document.getElementById('tcTut');return !!(d&&d.style.display==='block')});
 probe('card',function(){var d=document.getElementById('tcMbCard');return !!(d&&d.style.display==='block')});
 return {PRI:PRI,Z:Z,set:set,clear:clear,probe:probe,is:is,top:top,blocks:blocks,when:when,on:on,state:state}})();
window.TCBUSY=TCBUSY;
