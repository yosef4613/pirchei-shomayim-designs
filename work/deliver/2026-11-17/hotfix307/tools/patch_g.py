# hotfix307: G (ע) — להתחיל שלב של משימה / של הסיפור; F נשאר למקום. שינוי ב-074zu_story_actions.js (החלק של actions2).
import sys
P=sys.argv[1]
s=open(P,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('count %d!=%d for %r'%(c,n,a[:80]))
    s=s.replace(a,b)
# 1. הטקסטים למשתמש
rep("+' · F כשמוצאים'","+' · G כשמוצאים'")
rep("+' · F בטבעת')","+' · G בטבעת')")
rep("toast('מצאת: '+c.nm+' — F להרים')","toast('מצאת: '+c.nm+' — G להרים')")
rep("toast('הפעולה נעצרה — חוזרים ל'+c.nm+' ולוחצים F')","toast('הפעולה נעצרה — חוזרים ל'+c.nm+' ולוחצים G')")
rep("toast('הפעולה נעצרה — F כדי להתחיל שוב')","toast('הפעולה נעצרה — G כדי להתחיל שוב')")
rep("toast('נעצר — F כדי להתחיל שוב')","toast('נעצר — G כדי להתחיל שוב')")
rep("toast('העבודה מתחילה ברכב — חוזרים לרכב, ואז F')","toast('העבודה מתחילה ברכב — חוזרים לרכב, ואז G')")
rep("<90?'F · להגיע עם '+q.nm+' ולהראות':'להמשיך עם '+q.nm+' — עד המקום (ברגל), ושם F'}","<90?'G · להגיע עם '+q.nm+' ולהראות':'להמשיך עם '+q.nm+' — עד המקום (ברגל), ושם G'}")
rep("return'F · '+(walk()||q.opt.boat?'':'לצאת מהרכב ו')+q.v","return'G · '+(walk()||q.opt.boat?'':'לצאת מהרכב ו')+q.v")
rep("' · מסתובבים באזור, וכשמוצאים — F'","' · מסתובבים באזור, וכשמוצאים — G'")
rep("+' · F ליד החפץ, ברגל')","+' · G ליד החפץ, ברגל')")
rep("return q.kind==='talk'?'F · '+out+'לגשת ולדבר עם '+(q.name||'הדמות'):q.kind==='job'?'F · '+out+'לקבל את העבודה'+(q.name?' מ'+q.name:'')+(q.label?' — '+q.label:''):'F · '+out+'לקנות כרטיס'",
    "return q.kind==='talk'?'G · '+out+'לגשת ולדבר עם '+(q.name||'הדמות'):q.kind==='job'?'G · '+out+'לקבל את העבודה'+(q.name?' מ'+q.name:'')+(q.label?' — '+q.label:''):'G · '+out+'לקנות כרטיס'")
rep("hud:msHud(true).replace(/^F · (לצאת מהרכב ו)?/,'')","hud:msHud(true).replace(/^G · (לצאת מהרכב ו)?/,'')")
rep("if(!E.qa)try{toast(msHud(true)||'F')}catch(e){}}","if(!E.qa)try{toast(msHud(true)||'G')}catch(e){}}")
# 2. הטבעות: G, וכיתוב ברור ליד הטבעת
rep("c.fillText(lab||'F',x,y-K*26+.3);c.restore()}",
    "c.fillText(lab||'G',x,y-K*26+.3);c.restore()}\n"
    " /* hotfix307: הכיתוב ליד הטבעת — מקש G בצהוב וטקסט (\"G · לדבר עם שמעון\"); מעל הדמות, כדי שלא יתכסה ב-F של המקום (\"F · להיכנס הביתה\") */\n"
    " function capt(c,x,y,txt){if(!txt)return;const z=Math.max(.45,Camera.zoom||1),fs=Math.max(4.6,12.5/z),pd=fs*.45,kw=fs*1.25;c.save();c.font='700 '+fs+'px Segoe UI,Arial';c.textBaseline='middle';\n"
    "  const t=String(txt).slice(0,40),tw=c.measureText(t).width,W=tw+kw+pd*3,H=fs*1.55,x0=x-W/2,y0=y-H;c.fillStyle='rgba(10,20,28,.86)';c.strokeStyle='rgba(84,214,150,.95)';c.lineWidth=Math.max(.4,1.1/z);\n"
    "  c.beginPath();if(c.roundRect)c.roundRect(x0,y0,W,H,H/2);else c.rect(x0,y0,W,H);c.fill();c.stroke();const kx=x0+W-pd-kw;c.fillStyle='#ffd36a';c.beginPath();if(c.roundRect)c.roundRect(kx,y0+H*.14,kw,H*.72,fs*.25);else c.rect(kx,y0+H*.14,kw,H*.72);c.fill();\n"
    "  c.fillStyle='#2a1500';c.textAlign='center';c.font='900 '+fs+'px Segoe UI,Arial';c.fillText('G',kx+kw/2,y0+H/2+fs*.04);c.fillStyle='#fff';c.textAlign='right';c.font='700 '+fs+'px Segoe UI,Arial';c.fillText(t,kx-pd,y0+H/2+fs*.04);c.restore();GK.capN++}")
rep("if(inView(P.x,P.y,60)&&Math.hypot(m.x-P.x,m.y-P.y)<800)ring(c,P.x,P.y+5,f?16:26,now,'F')}}",
    "if(inView(P.x,P.y,60)&&Math.hypot(m.x-P.x,m.y-P.y)<800){ring(c,P.x,P.y+5,f?16:26,now,'G');if(Math.hypot(m.x-P.x,m.y-P.y)<520)capt(c,P.x,P.y+5-K*26-6.5,msCap(mq))}}}")
rep("if(d.car){if(walk())ring(c,x,y,Math.min(r,60),now,'רכב')}else ring(c,x,y,Math.min(r,40),now,'F')}",
    "if(d.car){if(walk())ring(c,x,y,Math.min(r,60),now,'רכב')}else ring(c,x,y,Math.min(r,40),now,'G')}")
rep("ring(c,q.poi.x,q.poi.y,40,now,Math.hypot(m.x-q.poi.x,m.y-q.poi.y)<90?'F':'→')}return}",
    "ring(c,q.poi.x,q.poi.y,40,now,Math.hypot(m.x-q.poi.x,m.y-q.poi.y)<90?'G':'→')}return}")
rep("if(q.phase==='go'&&!cut()&&(q.k!=='find'||q.found))ring(c,P.x,P.y,Math.min(q.R,30),now,'F');",
    "if(q.phase==='go'&&!cut()&&(q.k!=='find'||q.found)){ring(c,P.x,P.y,Math.min(q.R,30),now,'G');{const m=me();if(Math.hypot(m.x-P.x,m.y-P.y)<520)capt(c,P.x,P.y-K*26-6.5,(walk()||q.opt.boat?'':'לצאת מהרכב ו')+q.v+(q.nm?' — '+q.nm:''))}}")
# 3. F — רק למקום; G — לשלב. F ליד טבעת שלא נלקח ע"י מקום — רמז "G"
OLD="{const I0=interactNearbyPoi;interactNearbyPoi=function(){try{if(VIS.v){visExit();return true}if(PS.q)return true;if(msF())return true;if(F())return true}catch(e){err('F',e)}return I0.apply(this,arguments)}}"
NEW=("{const I0=interactNearbyPoi;interactNearbyPoi=function(){try{if(VIS.v){visExit();return true}if(PS.q)return true}catch(e){err('F',e)}const r=I0.apply(this,arguments);   /* hotfix307: F — המקום בלבד (כניסה הביתה, מסך המקום); השלב — G */\n"
     "   try{if(!r&&!E.qa){const t=gNear();if(t){GK.fHint++;toast('השלב של המשימה — מקש G (לא F) · '+t)}}}catch(e){err('F-hint',e)}return r}}\n"
     " /* hotfix307 (הבעלים 18.11: \"התחלת משימות — כפתור אחר ולא F\"; \"שמעון מחכה … אין לי איך להתחיל\" — F ליד הבית נכנס הביתה, 074zz8): המקש G (ע במקלדת עברית) מתחיל את השלב ליד הטבעת —\n"
     "    הסיפור הראשי (msF), סיפורי האזורים / ההגעות (F); אותו רצף בדיוק כמו קודם. Shift+G — הגרף של הבדיקה (058:GraphKey) כמו קודם. בזמן הקלדה / תפריט / שיחה / סרט / טלפון / בתוך הבית — לא. */\n"
     " const GK={n:0,ok:0,fHint:0,capN:0,last:null};\n"
     " function msCap(q){if(!q)return'';const out=walk()?'':'לצאת מהרכב ו';return q.kind==='talk'?out+'לדבר עם '+(q.name||'הדמות'):q.kind==='job'?out+'לקבל את העבודה'+(q.name?' מ'+q.name:''):out+'לקנות כרטיס'}\n"
     " function gNear(){if(PS.q||cut())return'';const q=MS.cur,m=me();if(q&&q.at){const f=q.who?FIG[q.who]:null,P=f&&f.pt&&!f.hide?f.pt:q.at;if(Math.hypot(m.x-P.x,m.y-P.y)<(walk()?140:Math.max(q.r,120)))return msCap(q)}\n"
     "  const c=SA.cur;if(c&&c.phase==='go'&&c.pt&&Math.hypot(m.x-c.pt.x,m.y-c.pt.y)<Math.max(c.R||0,40)+20)return c.v+(c.nm?' — '+c.nm:'');return''}\n"
     " function gBlocked(){try{if(typeof TCO!=='undefined'&&(TCO.ui||(TCO.mode&&TCO.mode!=='game'&&TCO.mode!=='off')))return'menu'}catch(e){}try{if(g77S().open)return'dialog'}catch(e){}try{if(typeof TCSHOW!=='undefined'&&TCSHOW.on)return'show'}catch(e){}\n"
     "  try{if(State.paused)return'paused';if(State.phoneOpen)return'phone';if(State.mapOpen)return'map'}catch(e){}try{if(typeof HOMEIN!=='undefined'&&HOMEIN.H&&(HOMEIN.H.on||HOMEIN.H.walkIn))return'home'}catch(e){}return''}\n"
     " function storyKey(src){GK.n++;let r=false,why='';const b=gBlocked();if(b){GK.last={src,r,why:b};return false}\n"
     "  try{if(VIS.v){visExit();r=true;why='vis'}else if(PS.q){r=true;why='busy'}else if(msF()){r=true;why='ms'}else if(F()){r=true;why='sa'}}catch(e){err('G',e)}\n"
     "  if(!r&&!E.qa&&!cut()){let t='';const q=MS.cur;if(q&&q.at){t='G · '+msCap(q)+' — קרוב יותר לטבעת הירוקה'+(q.name?' (ליד '+q.name+')':'')}else if(SA.cur&&SA.cur.phase==='go'){hint(SA.cur)}else t='G — אין כאן שלב של משימה להתחיל (הטבעת הירוקה מסמנת איפה)';if(t)try{toast(t)}catch(e){}}\n"
     "  if(r)GK.ok++;GK.last={src,r,why,ms:!!MS.cur,sa:!!SA.cur,t:Math.round(pnow())};return r}\n"
     " window.addEventListener('keydown',e=>{try{if(e.ctrlKey||e.metaKey||e.altKey||e.shiftKey)return;if(!(e.code==='KeyG'||e.key==='g'||e.key==='G'||e.key==='ע'))return;const a=document.activeElement;if(a&&(a.tagName==='INPUT'||a.tagName==='TEXTAREA'||a.tagName==='SELECT'||a.isContentEditable))return;\n"
     "  e.preventDefault();e.stopImmediatePropagation();if(e.repeat)return;storyKey('key')}catch(x){err('gkey',x)}},true);   /* לפני 058 (GraphKey): G בלי Shift — של הסיפור */\n"
     " /* המקשים: G ברשימת המקשים (התפריט — TCSET.KEYS) ובשורת המקשים למטה (#help), אחרי F */\n"
     " try{const K=typeof TCSET!=='undefined'&&TCSET.KEYS;if(Array.isArray(K)&&!K.some(r=>r[0]==='G')){const i=K.findIndex(r=>r[0]==='F');K.splice(i<0?K.length:i+1,0,['G','ליד הטבעת הירוקה — להתחיל משימה / שלב בסיפור (לדבר, לקבל עבודה, להרים…)'])}}catch(e){err('keys',e)}\n"
     " try{const h=document.getElementById('help');if(h&&!h.querySelector('[data-g-key]')){let f=null;for(const x of h.querySelectorAll('.key'))if(x.textContent.trim()==='F'){f=x;break}const add='<span data-g-key=\"1\"><span class=\"key\">G</span> משימה / סיפור (ליד הטבעת) · </span>';\n"
     "  let n=f&&f.nextSibling;while(n&&!(n.nodeType===1&&n.classList&&n.classList.contains('key')))n=n.nextSibling;if(n){const t=document.createElement('span');t.innerHTML=add;h.insertBefore(t.firstChild,n)}else h.insertAdjacentHTML('beforeend',' · '+add)}}catch(e){err('help',e)}")
rep(OLD,NEW)
# 4. החשיפה לבדיקות
rep("window.__TC_SACT={SA,E,spec,arm,F,tick,","window.__TC_SACT={SA,E,spec,arm,F,storyKey,GK,gNear,tick,")
open(P,'w',encoding='utf-8').write(s)
print('ok')
