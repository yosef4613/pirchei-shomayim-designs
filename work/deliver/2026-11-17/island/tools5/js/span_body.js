 /* island5 (17.11, הבעלים 16:15: "הגשר מעבר מהמרינה של הסירות מתחת למסילות לא נראת טוב בכלל תזיז אותה מזרחה ותתכנן את המראה של מעבר הסירות שם מחדש"):
    המעבר זז 22 מ׳ מזרחה — המרכז ב-x 7000 (היה 6775): העמוד המערבי אחרי צומת המסילות (JX-SEA) ואחרי הקשת של N1, ושלוש המסילות (N1 ‏5050, ‏B4 ‏5120, ‏S2 ‏5158)
    ישרות לכל רוחב המעבר. לא יותר מזרחה: דרך ההסעה ומסלול המים של המטוס האמפיבי (074zm, ‏H2 (7000, 4350) ← (7290, 4620), ‏y 4650 מ-x 7300).
    העיצוב החדש: קשת קשורה לבנה אחת מעל שלוש המסילות (46 מ׳ בין המסבים, 10 מ׳ מעל הסיפון, היתלים ברשת, קשרי רוח), שני עמודים של 5 מ׳ עם חרטום
    מצפון ומדרום, פגושי עץ ולוח גובה, תעלה של 40 מ׳ בין הפגושים (מים עמוקים מסומנים), קירות הנחיה על כלונסאות ודולפינים עם אורות. הציור — Island_D694_plan.html, סעיף 0ג. */
 const KZ=S9K*S9HM,CX=7000,CH={x0:6800,x1:7200},SPAN={x0:6769,x1:7231,clear:7.0,rail:8.2,rise:10,pierHalf:25,piers:[[6744,6794],[7206,7256]],fw:6},
  PY=[5005,5203],NOSE=30,YN=5013,YS=5195,WATER=Math.round(SPAN.rail*S9HM*S9K),ISL_OPEN={y0:5770,y1:6010,drop:[5800,5980]},
  WALLS=[{x:6797,sx:-1,col:'r'},{x:7203,sx:1,col:'g'}],WN=[5012,4905,4868],WSo=[5252,5330,5365],FL=25,JOG=[4470,4790],
  OLD={CH:{x0:6600,x1:6950},SPAN:{x0:6585,x1:6965}};
 const PX0=SPAN.piers[0][0]-12,PX1=SPAN.piers[1][1]+12,inSpan=x=>x>PX0&&x<PX1,SPAN_IDS=/^(EAST-B|EAST-B4|EAST-N1|EAST-C|EAST-S1|EAST-S2|SIDING-F6)$/;
 const edgeW=y=>y<=JOG[0]?6600:y>=JOG[1]?CH.x0:6600+(CH.x0-6600)*(y-JOG[0])/(JOG[1]-JOG[0]),edgeE=y=>y<=JOG[0]?6950:y>=JOG[1]?CH.x1:6950+(CH.x1-6950)*(y-JOG[0])/(JOG[1]-JOG[0]);
 /* ---- 1. העמודים של הגשר הנמוך: אין עמוד בין שני העמודים של המעבר (בכל המסילות שעוברות שם) ---- */
 {const pR=rlPiers;rlPiers=function(g){const had=!!(g&&g._piers);const out=pR.apply(this,arguments);if(had&&g._s10v)return out;
   if(g&&SPAN_IDS.test(g.id)){g._piers=out.filter(q=>!inSpan(q.x));g._s10v=1;return g._piers}
   if(g&&g.id==='ISL-BR'){g._piers=out.filter(q=>!(q.y>ISL_OPEN.drop[0]&&q.y<ISL_OPEN.drop[1]));g._s10v=1;return g._piers}return out}}
 try{for(const id of['EAST-B4','EAST-N1','EAST-C','EAST-S1','EAST-S2','ISL-BR']){const g=RAIL_SEG_BY_ID[id];if(g){g._piers=null;g._s10v=0}}F56_SIDING._piers=null}catch(e){er('piers',e)}
 /* ---- 2. מסילת ההיפוך הישנה (019d): N1 (020a) הוא אותו קו ומצויר ב-drawLineRail — כאן כבר לא מציירים אותה (יצאו הבולם ב-x 7186 והשלט "ההמשך עם G6") ---- */
 function sidingRail(){}
 try{const i=S9_HOOKS.rail.indexOf(f56Rail);if(i>=0)S9_HOOKS.rail[i]=sidingRail;else er('siding-hook','f56Rail not found')}catch(e){er('siding-hook',e)}
 /* ---- 3. הציור ---- */
 const archH=x=>{const u=(x-CX)/((SPAN.x1-SPAN.x0)/2);return u*u>=1?0:SPAN.rise*KZ*(1-u*u)};
 const LAMP={r:['#b8322a','#ff3b30','rgba(255,60,40,.5)'],g:['#2e9d4a','#3bff6a','rgba(60,255,110,.5)'],w:['#f3e3b0','#ffe9a8','rgba(255,230,160,.45)']};
 function lamp(c,x,y,k,N,t,flash){const L=LAMP[k],on=!flash||((t+x*.0013)%3)<1;c.fillStyle=N?(on?L[1]:'#3a3030'):L[0];c.beginPath();c.arc(x,y,2.6,0,TAU);c.fill();
  if(N&&on){c.save();c.globalCompositeOperation='lighter';const g=c.createRadialGradient(x,y,0,x,y,14);g.addColorStop(0,L[2]);g.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=g;c.fillRect(x-14,y-14,28,28);c.restore()}}
 /* העמוד: החרטום הצפוני (מעל המים, מצפון לסיפון של N1), הגוף מתחת לסיפונים, והחרטום הדרומי עם הפאות שיורדות אל המים (3/4: המים ‎+WATER פיקס׳ מתחת לסיפון) */
 function pierDraw(c,xa,xb,N){const xc=(xa+xb)/2,h=WATER,yN=PY[0],yS=PY[1],side=xc<CX?1:-1,fx=side>0?xb:xa-SPAN.fw,lit=s=>s9Hex(s,N?.55:1);
  c.fillStyle='rgba(255,255,255,.3)';c.beginPath();c.ellipse(xc,yN-NOSE+6,(xb-xa)*.7,8,0,0,TAU);c.fill();
  c.fillStyle=lit('#cdc9be');c.beginPath();c.moveTo(xa,yS);c.lineTo(xa,yN);c.lineTo(xc,yN-NOSE);c.lineTo(xb,yN);c.lineTo(xb,yS);c.closePath();c.fill();
  c.strokeStyle=lit('#7b776c');c.lineWidth=1.4;c.beginPath();c.moveTo(xa,yN+6);c.lineTo(xa,yN);c.lineTo(xc,yN-NOSE);c.lineTo(xb,yN);c.lineTo(xb,yN+6);c.stroke();
  /* הפגושים בצד של התעלה — לכל אורך העמוד; רואים את החלק שמתחת לסיפון הדרומי */
  c.fillStyle=lit('#8a6a3a');c.fillRect(fx,yN-NOSE+12,SPAN.fw,yS+h-(yN-NOSE+12));c.fillStyle=lit('#5a4426');for(let y=yN-NOSE+18;y<yS+h-4;y+=12)c.fillRect(fx-1,y,SPAN.fw+2,2.4);
  /* החרטום הדרומי: כיפה, ושתי פאות אל המים */
  const t0=[xa,yS],t1=[xc,yS+NOSE],t2=[xb,yS];
  c.fillStyle=lit('#b5b1a6');c.beginPath();c.moveTo(t0[0],t0[1]);c.lineTo(t1[0],t1[1]);c.lineTo(t1[0],t1[1]+h);c.lineTo(t0[0],t0[1]+h);c.closePath();c.fill();
  c.fillStyle=lit('#8f8b81');c.beginPath();c.moveTo(t1[0],t1[1]);c.lineTo(t2[0],t2[1]);c.lineTo(t2[0],t2[1]+h);c.lineTo(t1[0],t1[1]+h);c.closePath();c.fill();
  c.fillStyle='rgba(0,0,0,.14)';c.beginPath();c.moveTo(t0[0],t0[1]+h-7);c.lineTo(t1[0],t1[1]+h-7);c.lineTo(t2[0],t2[1]+h-7);c.lineTo(t2[0],t2[1]+h);c.lineTo(t1[0],t1[1]+h);c.lineTo(t0[0],t0[1]+h);c.closePath();c.fill();   /* קו המים — רטוב */
  c.fillStyle=lit('#d9d5ca');c.beginPath();c.moveTo(t0[0],t0[1]-4);c.lineTo(t1[0],t1[1]-4);c.lineTo(t2[0],t2[1]-4);c.lineTo(t2[0],t2[1]);c.lineTo(t1[0],t1[1]);c.lineTo(t0[0],t0[1]);c.closePath();c.fill();   /* כיפת האבן */
  /* לוח הגובה מול התעלה: לבן עם פסים שחורים, כל 1 מ׳ */
  {const gx=side>0?xc+(xb-xc)*.45:xa+(xc-xa)*.25,gy=yS+NOSE*.55+6;c.fillStyle='#f6f6f2';c.fillRect(gx,gy,7,30);c.fillStyle='#202428';for(let k=0;k<5;k++)c.fillRect(gx,gy+2+k*6,7,3)}
  c.fillStyle='rgba(255,255,255,.35)';c.beginPath();c.ellipse(xc,yS+NOSE+h,(xb-xa)*.7,6,0,0,TAU);c.fill()}
 function spanRail(c,now,N){if(!e3InView(PX0-40,4960,PX1-PX0+80,340,40))return;c.save();
  try{for(const [a,b] of SPAN.piers)pierDraw(c,a,b,N)}catch(e){er('spanRail',e)}c.restore()}
 /* הקשת הקשורה: הקשת האחורית (צפון) והקדמית (דרום), ההיתלים ברשת, קשרי הרוח למעלה, קורות הקשירה בשפת הסיפונים, המסבים, השלט והאורות */
 function archDraw(c,N,t){const x0=SPAN.x0,x1=SPAN.x1,n=48,W=s9Hex('#f2f5f7',N?.6:1),E=s9Hex('#66737d',N?.6:1),Hc=s9Hex('#8d99a3',N?.55:1);
  const rib=Y=>{c.beginPath();for(let i=0;i<=n;i++){const x=x0+(x1-x0)*i/n,y=Y-archH(x);i?c.lineTo(x,y):c.moveTo(x,y)}};
  const hangers=(Y,lw)=>{c.strokeStyle=Hc;c.lineWidth=lw;c.beginPath();for(let i=1;i<12;i++){const xt=x0+(x1-x0)*i/12;for(const d of[-55,55]){const xh=Math.max(x0+6,Math.min(x1-6,xt+d));c.moveTo(xt,Y);c.lineTo(xh,Y-archH(xh))}}c.stroke()};
  const tie=(Y,w)=>{c.fillStyle=E;c.fillRect(x0-7,Y-w/2-1.2,x1-x0+14,w+2.4);c.fillStyle=W;c.fillRect(x0-6,Y-w/2,x1-x0+12,w)};
  c.lineCap='round';c.lineJoin='round';
  c.save();c.globalAlpha=.62;hangers(YN,1);rib(YN);c.strokeStyle=E;c.lineWidth=6.5;c.stroke();c.strokeStyle=W;c.lineWidth=4.2;c.stroke();c.restore();
  tie(YN,5);
  c.save();c.globalAlpha=.75;c.strokeStyle=W;c.lineWidth=2;c.beginPath();const xs=[CX-140,CX-70,CX,CX+70,CX+140];
  for(const x of xs){c.moveTo(x,YN-archH(x));c.lineTo(x,YS-archH(x))}for(let i=0;i<xs.length-1;i++){const a=xs[i],b=xs[i+1];c.moveTo(a,YN-archH(a));c.lineTo(b,YS-archH(b));c.moveTo(b,YN-archH(b));c.lineTo(a,YS-archH(a))}c.stroke();c.restore();
  hangers(YS,1.5);tie(YS,7);
  rib(YS);c.strokeStyle=E;c.lineWidth=8.5;c.stroke();c.strokeStyle=W;c.lineWidth=5.8;c.stroke();c.strokeStyle='rgba(255,255,255,.75)';c.lineWidth=1.4;c.stroke();
  for(const x of[x0,x1]){c.fillStyle=s9Hex('#48515a',N?.6:1);c.fillRect(x-8,YS-5,16,10);c.fillRect(x-7,YN-4,14,8)}   /* המסבים */
  c.fillStyle='#1d4f91';c.fillRect(CX-30,YS+5,60,11);c.strokeStyle='#f2f5f7';c.lineWidth=.8;c.strokeRect(CX-30,YS+5,60,11);s9Txt(c,'7.0 מ׳',CX,YS+10.6,7,'#ffffff');
  if(N){for(let i=2;i<n;i+=2){const x=x0+(x1-x0)*i/n;lamp(c,x,YS-archH(x)-3.5,'w',N,t,false)}}
  for(const dx of[-9,9])lamp(c,CX+dx,YS+24,'g',N,t,false);
  for(const [a,b] of SPAN.piers){const x=a<CX?b+3:a-3;lamp(c,x,PY[1]+8,'r',N,t,false);lamp(c,x,PY[0]-8,'r',N,t,false)}}
 function spanOver(c,now,N){if(!e3InView(PX0-40,4900,PX1-PX0+80,420,40))return;c.save();
  try{archDraw(c,N,now/1000);if(Camera.zoom>.45)s9Txt(c,'מעבר השיט של המרינה · 40 מ׳ · גובה חופשי 7.0 מ׳',CX,5300,6.5,'rgba(255,255,255,.95)',240)}catch(e){er('spanOver',e)}c.restore()}
 /* ---- 4. התעלה, קירות ההנחיה, הדולפינים והמצופים מדרום ---- */
 const BUOYS=[{id:'BY-R10',x:6800,y:5700,col:'red'},{id:'BY-G10',x:7200,y:5700,col:'green'}];
 const WALL_P=[],DOLPH=[];for(const w of WALLS)for(const Y of[WN,WSo]){WALL_P.push({w,P:[[w.x,Y[0]],[w.x,Y[1]],[w.x+w.sx*FL,Y[2]]]});DOLPH.push({x:w.x+w.sx*(FL+4),y:Y[2]+(Y[2]>5200?6:-6),col:w.col})}
 const along=(P,step)=>{const o=[];for(let i=1;i<P.length;i++){const a=P[i-1],b=P[i],L=Math.hypot(b[0]-a[0],b[1]-a[1]),k=Math.max(1,Math.round(L/step));for(let j=i>1?1:0;j<=k;j++)o.push([a[0]+(b[0]-a[0])*j/k,a[1]+(b[1]-a[1])*j/k])}return o};
 function channel(c,N){c.save();const A=N?.2:.13,col=a=>N?'rgba(4,20,40,'+a+')':'rgba(14,64,110,'+a+')';
  let g=c.createLinearGradient(0,JOG[0],0,JOG[0]+220);g.addColorStop(0,col(0));g.addColorStop(1,col(A));c.fillStyle=g;
  c.beginPath();c.moveTo(6600,JOG[0]);c.lineTo(CH.x0,JOG[1]);c.lineTo(CH.x0,4996);c.lineTo(CH.x1,4996);c.lineTo(CH.x1,JOG[1]);c.lineTo(6950,JOG[0]);c.closePath();c.fill();
  g=c.createLinearGradient(0,5262,0,5780);g.addColorStop(0,col(A));g.addColorStop(1,col(0));c.fillStyle=g;c.fillRect(CH.x0,5262,CH.x1-CH.x0,518);c.restore()}
 function walls(c,N,t){const lit=s=>s9Hex(s,N?.5:1);
  for(const {w,P} of WALL_P){const pts=along(P,18);
   c.fillStyle='rgba(255,255,255,.22)';for(const p of pts){c.beginPath();c.ellipse(p[0],p[1]+1,5,2.4,0,0,TAU);c.fill()}
   for(const p of pts){c.fillStyle=lit('#3e3226');c.fillRect(p[0]-2.4,p[1]-11,4.8,11);c.fillStyle=lit('#6b5638');c.beginPath();c.ellipse(p[0],p[1]-11,2.4,1.3,0,0,TAU);c.fill()}
   c.strokeStyle=lit('#8a6a3a');c.lineWidth=3.6;c.lineCap='round';c.beginPath();P.forEach((p,i)=>i?c.lineTo(p[0],p[1]-7):c.moveTo(p[0],p[1]-7));c.stroke();
   c.strokeStyle=lit('#a8854e');c.lineWidth=1.2;c.beginPath();P.forEach((p,i)=>i?c.lineTo(p[0],p[1]-8.4):c.moveTo(p[0],p[1]-8.4));c.stroke()}
  for(const d of DOLPH){c.fillStyle='rgba(255,255,255,.26)';c.beginPath();c.ellipse(d.x,d.y+1,15,6,0,0,TAU);c.fill();
   for(const [dx,dy] of[[-7,-3],[7,-3],[-7,3],[7,3],[0,-6],[0,6]]){c.fillStyle=lit('#3e3226');c.fillRect(d.x+dx-2.6,d.y+dy-13,5.2,13)}
   c.fillStyle=lit('#5b4a36');c.beginPath();c.ellipse(d.x,d.y-13,11,6,0,0,TAU);c.fill();c.strokeStyle=lit('#2a2018');c.lineWidth=1;c.stroke();
   c.fillStyle=d.col==='r'?lit('#c4372b'):lit('#2f8a46');c.fillRect(d.x-1.5,d.y-27,3,14);lamp(c,d.x,d.y-29,d.col,N,t,true)}}
 function buoys(c,now,N){if(!e3InView(6760,5660,480,80,40))return;const t=now/1000;for(const b of BUOYS){try{BOAT34.buoy(c,b.x,b.y,b.col,t,N?1:0,true)}catch(e){c.fillStyle=b.col==='red'?'#d23a2c':'#2f9a4a';c.beginPath();c.arc(b.x,b.y,5,0,TAU);c.fill()}}}
 /* ---- 5. כלי שיט מתחת לסיפון: אחרי שהכלי צויר — הסיפונים שמעליו בשקיפות (כלל 15), של כל המסילות של הגשרים (RL_BRIDGES) ---- */
 const DECKS=()=>(typeof RL_BRIDGES!=='undefined'?RL_BRIDGES:['EAST-B4','EAST-N1','EAST-C','EAST-S2']).map(id=>RAIL_SEG_BY_ID[id]).filter(Boolean);
 function decksAt(x0,y0,x1,y1){return DECKS().filter(g=>{const b=rlBBox(g);if(!(b.x0-40<x1&&b.x1+40>x0&&b.y0-40<y1&&b.y1+40>y0))return false;const cx=(x0+x1)/2,cy=(y0+y1)/2,r=Math.hypot(x1-x0,y1-y0)/2+RL_DECK_W/2;return polyD(cx,cy,g.pts)<r})}
 function patchDecks(c,P){try{const x0=Math.min(...P.map(q=>q[0]))-6,x1=Math.max(...P.map(q=>q[0]))+6,y0=Math.min(...P.map(q=>q[1]))-6,y1=Math.max(...P.map(q=>q[1]))+6;
   const hits=decksAt(x0,y0,x1,y1);if(!hits.length)return false;
   c.save();c.beginPath();c.rect(x0,y0,x1-x0,y1-y0);c.clip();c.globalAlpha=.62;const pc=ctx;ctx=c;   /* שקוף למחצה — רואים את הכלי שמתחת (הבעלים: גג שקוף מעל כל מקום שכלי עובר תחתיו) */
   try{for(const g of hits)rlDeck(g);for(const k of[0,1,2])for(const g of hits){if(typeof rlTrackLayer==='function')rlTrackLayer(g,k);else if(k===0)rlTrack(g)}}finally{ctx=pc}c.restore();return true}catch(e){er('patch',e);return false}}
 const UNDER=q=>!!q&&q.x>PX0&&q.x<PX1&&q.y>4990&&q.y<5240;
 try{window.__S10V_UNDER=UNDER}catch(e){}
 function water(c,now,N){try{const t=now/1000;if(e3InView(6560,4440,900,1360,40)){channel(c,N);walls(c,N,t)}buoys(c,now,N);
   if(typeof F56LIVE!=='undefined'&&F56LIVE.pilotPose){const q=F56LIVE.pilotPose(now);if(q&&q.stop!=='berth'&&UNDER(q)){F56LIVE.pilotDraw(c,now);const cs=Math.cos(q.h),sn=Math.sin(q.h),L=70,B=26;patchDecks(c,[[q.x+L*cs-B*sn,q.y+L*sn+B*cs],[q.x-L*cs-B*sn,q.y-L*sn+B*cs],[q.x-L*cs+B*sn,q.y-L*sn-B*cs],[q.x+L*cs+B*sn,q.y+L*sn-B*cs]])}}}catch(e){er('water',e)}}
 S9_HOOKS.rail.push(spanRail);S9_HOOKS.over.push(spanOver);S9_HOOKS.water.push(water);
