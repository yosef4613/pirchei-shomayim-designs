
/* ==== POSTERS · סט 11 — הפוסטרים של המעצב (deliver/2026-11-12/set11/posters_original.html, ‏12.11 03:30; HANDOFF 4ב) ====
   כלל 19א: לא מנגנון חדש — הציור של המעצב (TC_EVENT_POSTERS, למעלה, כמו שהוא) נכנס לתוך שני המקומות הקיימים:
   (1) TCSHOW.poster / drawPosters (029c — מסכי המקום: הקולנוע, התיאטרון) — אותו קנבס, אותו גודל; קנבס רחב → "פוסטר למסך" (סרט 800×600,
       הצגה 960×600), צר → "פוסטר לחזית" 600×900. (2) המסגרות של 074n3 (3 בקולנוע, 4 בתיאטרון) — המקור שלהן נוצר ב-TCSHOW.poster, ולכן מקבל
   את החזית של המעצב; שתי הכרזות של המוזיאון — tcpoBanner מצייר את פוסטר התערוכה. תאורת הלילה — המנגנון הקיים של 074n3 (tcpoNight).
   כל ציור — בקוד (קנבס), בלי קובץ תמונה. בלי שינוי בבניין, בדלת או במסגרת (D‑605). כיבוי: __TC_POSTERS11.on(false) — חזרה לציור הקודם. */
var TCP11={on:true,err:null,n:{screen:0,src:0,banner:0,miss:0}};
function tcp11Err(e){TCP11.err=TCP11.err||String(e&&e.stack||e).slice(0,300)}
function tcp11A(){return (typeof window!=='undefined'&&window.TC_EVENT_POSTERS)||null}
function tcp11Key(kind,i){const A=tcp11A();if(!A||!TCP11.on)return null;let nm=null;try{const L=kind==='film'?TCSHOW.FILMS:TCSHOW.PLAYS;nm=L[i]&&L[i].name}catch(e){}
 const m=A.items.find(x=>x.kind===kind&&x.title===nm)||A.items.find(x=>x.kind===kind&&x.index===i);if(!m)TCP11.n.miss++;return m?m.key:null}
const TCP11_MUS={'תערוכה חדשה':'sea-to-city','אוסף הטבע':'nature-collection'};
// draws one designer poster into a box: the format by the box's shape; the margin (when the shapes differ) — the poster's own dark frame colour
function tcp11Fill(g,key,W,H,night){const A=tcp11A(),fmt=W>H*1.05?'screen':'facade';g.save();g.fillStyle=night?'#050a12':'#303938';g.fillRect(0,0,W,H);A.draw(g,key,fmt,0,0,W,H,{night:!!night});g.restore();return fmt}
(function tcp11Hook(){try{
 if(typeof TCSHOW==='undefined'||!TCSHOW||TCSHOW.__p11)return;const P0=TCSHOW.poster;TCSHOW.__p11=1;TCP11.P0=P0;
 TCSHOW.poster=function(cv,kind,i){const key=cv&&tcp11Key(kind,i);if(!key)return P0.apply(this,arguments);try{
   const live=!!cv.isConnected,d=live?Math.min(2,window.devicePixelRatio||1):1,w=(live&&cv.clientWidth)||240,h=(live&&cv.clientHeight)||(live?340:360);
   cv.width=Math.round(w*d);cv.height=Math.round(h*d);const c=cv.getContext('2d');c.setTransform(d,0,0,d,0,0);tcp11Fill(c,key,w,h,false);c.setTransform(1,0,0,1,0,0);
   if(live){cv.dataset.drawn='1';TCP11.n.screen++}else TCP11.n.src++;cv.dataset.p11=key}catch(e){tcp11Err(e);return P0.apply(this,arguments)}};
 TCSHOW.drawPosters=function(){for(const cv of document.querySelectorAll('canvas[data-tc-poster]')){if(cv.dataset.drawn)continue;const [k,i]=cv.dataset.tcPoster.split(':');TCSHOW.poster(cv,k,+i)}};
}catch(e){tcp11Err(e)}})();
if(typeof tcpoBanner==='function'){const B0=tcpoBanner;tcpoBanner=function(key,w,h){const k=TCP11.on&&tcp11A()&&TCP11_MUS[key];if(!k)return B0.apply(this,arguments);
 try{return tcpoOut(()=>tcpoCached('p11|'+k,TCB.bucket(Math.max(8,w)),TCB.bucket(Math.max(8,h)),(g,W,H)=>{tcp11Fill(g,k,W,H,false);TCP11.n.banner++}))}catch(e){tcp11Err(e);return B0.apply(this,arguments)}}}
window.__TC_POSTERS11={TCP11,stats:()=>({on:TCP11.on,api:!!tcp11A(),n:TCP11.n,err:TCP11.err,films:(()=>{try{return TCSHOW.FILMS.map((f,i)=>[f.name,tcp11Key('film',i)])}catch(e){return null}})(),plays:(()=>{try{return TCSHOW.PLAYS.map((f,i)=>[f.name,tcp11Key('play',i)])}catch(e){return null}})()}),
 on:v=>{TCP11.on=!!v;try{TCPO.src.clear();TCPO.pics.clear();TCPO.picB=0;TCPO.warm=0;TCPO.ready=false;for(const cv of document.querySelectorAll('canvas[data-tc-poster]'))delete cv.dataset.drawn;BLD40.clear();wtcInvalidate()}catch(e){}return TCP11.on}};
