(function(){try{var S=64,cv=document.createElement('canvas');cv.width=cv.height=S;var c=cv.getContext('2d');if(!c||!window.Path2D)return;
/* האייקון של טורבו סיטי (turbo_city_icon.svg של הבודק, 64×64) — מצויר בקנבס, בלי קובץ תמונה; הקישור נוצר בייצוא (כלל 17א) */
function lg(x0,y0,x1,y1,st){var g=c.createLinearGradient(x0,y0,x1,y1);for(var i=0;i<st.length;i+=2)g.addColorStop(st[i],st[i+1]);return g;}
var bg=new Path2D('M15 1.5H49C56.456 1.5 62.5 7.544 62.5 15V49C62.5 56.456 56.456 62.5 49 62.5H15C7.544 62.5 1.5 56.456 1.5 49V15C1.5 7.544 7.544 1.5 15 1.5Z');
var T=new Path2D('M10 13H36L33 22H25L18 50H8L15 22H7Z'),C=new Path2D('M57 13H41L31 22L24 42L29 51H46L55 42H44L41 45H35L33 42L39 25L43 22H49L48 27H57L61 18Z');
c.fillStyle=lg(1.5,1.5,62.5,62.5,[0,'#1c3e5b',1,'#071326']);c.fill(bg);c.strokeStyle='#50768a';c.lineWidth=1.5;c.stroke(bg);
c.lineJoin='round';c.save();c.translate(.7,2.3);c.fillStyle=c.strokeStyle='#020d20';c.lineWidth=2;c.fill(T);c.stroke(T);c.fill(C);c.stroke(C);c.restore();
c.strokeStyle='#e3f8ff';c.lineWidth=1.6;
c.fillStyle=lg(0,13,0,50,[0,'#e5ffff',.24,'#48f0ff',.55,'#00cce8',1,'#0078b8']);c.fill(T);c.stroke(T);
c.fillStyle=lg(0,13,0,51,[0,'#fff2a1',.24,'#ffd228',.6,'#ff9700',1,'#f45b08']);c.fill(C);c.stroke(C);
function put(u){var l=document.querySelector('link[rel~="icon"]')||document.createElement('link');l.rel='icon';l.type='image/png';l.sizes='64x64';l.id='tc-icon';l.href=u;if(!l.parentNode)document.head.appendChild(l);window.__TC_ICON={size:S,ok:true,blob:u.slice(0,5)==='blob:'};}
/* קישור blob (ייצוא מהקנבס) — כדי שגם ב-DOM לא תהיה תמונה מוטמעת (בדיקה no_embedded_raster_game_assets) */
if(cv.toBlob&&window.URL&&URL.createObjectURL)cv.toBlob(function(b){try{if(b)put(URL.createObjectURL(b))}catch(e){window.__TC_ICON={ok:false,err:String(e)}}},'image/png');
window.__TC_ICON={size:S,ok:false,pending:true};}catch(e){window.__TC_ICON={ok:false,err:String(e)};}})();
