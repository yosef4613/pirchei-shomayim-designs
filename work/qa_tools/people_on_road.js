// עותק (D‑604, 10.11): כמו qa_tools/people_on_road.js, ועוד: p34LibInit() לפני העטיפה של P34.draw (סעיף 6 בהחזרה של סוכן הביצועים).
// 3.11 · R-76 (הבעלים 10:10 / 10:50, סעיף 4): בדיקה חוסמת — אנשים בכביש. דוגמים את כל האנשים בעיר לאורך כמה דקות של משחק:
//  (א) לפי המצב — כל חצי שנייה (R-78, הביקורת 4.11 20:30; עד אז כל 5 שניות): הולכי הרגל (NPC_PEDESTRIANS), השחקן כשהוא ברגל, האנשים של
//      הפרטים החיים (TC_LIVE — "אנשים", לפי הרגליים), הגננים של האזורים, הנוסעים בשדה (F2_PEOPLE), והנוסעים של האוטובוסים — העולים
//      והיורדים (BUS_ALIGHTERS: BUS-BOARD-* ו-BUS-ALIGHT-*). נוסע בתוך המפרץ — בדרך בין הדלת למדרכה — נספר לחוד ולא נכשל; על נתיב — נכשל;
//  (ב) לפי הציור — כל 20 שניות עוברים על כל העיר (תצוגות של 1600×900 פיקסלים של העולם) ותופסים כל אדם שהמשחק מצייר
//      (P34.draw ו-TurboCity.draw של PE-*), מכל מקור — נוסעים, מבקרים, צוותים, עובדים — לפי הרגליים, בקואורדינטות של העולם.
// אדם שהרגליים שלו על נתיב נסיעה (בתוך הכביש, לא על המדרכה) ולא בתוך מעבר חצייה — כישלון. גם אדם בתוך מפרץ של אוטובוס — כישלון, חוץ ממי שיורד מהאוטובוס בדרך מהדלת למדרכה (p552). הדוח: מי (המזהה, או מי צייר אותו), איפה (x, y, אזור, הכביש), מתי.
// הקצב והמשך: דגימת מצב כל 0.5 שנ׳ של משחק, מעבר ציור כל 20 שנ׳, במשך 300 שנ׳ (ברירת המחדל; R-78 דורש לפחות 150). שניהם נכתבים בדוח (every, drawEvery, T).
// node tools/dev/people_on_road.js <game.html> [out.json] [seconds=300]     (Chromium — דרך tools_pack/nolock.sh; לא תחת PERF_LOCK). יציאה 1 — כישלון.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outArg, secArg] = process.argv.slice(2); if (!file) { console.error('usage: node people_on_road.js <game.html> [out.json] [seconds]'); process.exit(2) }
  if (fs.existsSync('/home/user/tc_root/tc/pkg/work/PERF_LOCK')) { console.error('PERF_LOCK — not now'); process.exit(2) }
  const T = +(secArg || 300);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(3000); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(400) }
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const Q = `(()=>{if(!window.P34&&typeof p34LibInit==='function'){try{p34LibInit()}catch(e){}}   /* D‑604 (עותק של סוכן הביצועים): צייר הדמויות נטען לפני העטיפה — אחרת זה מירוץ, ובהרצה שהוא נטען אחרי ההתחלה אף דמות של P34 לא נבדקת */
 const T=${T},EVERY=0.5,DRAW_EVERY=20,out={T,every:EVERY,drawEvery:DRAW_EVERY,samples:0,sweeps:0,views:0,people:0,drawn:0,tags:{},hits:[],sources:{},busPax:0,busInBay:0};
 const zone=(x,y)=>{const C='ABCDEFGH'[Math.max(0,Math.min(7,Math.floor(x/1200)))],R=[-850,0,850,1700,2550,3400,4250,5200,6050,6900,7750];let r=0;for(let i=0;i<R.length-1;i++)if(y>=R[i]&&y<R[i+1])r=i;return C+r};
 const RD=EDGES.filter(e=>!e.future).map(e=>{const a=_NODE_BY_ID[e.a],b=_NODE_BY_ID[e.b];if(!a||!b)return null;const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<1)return null;return{id:e.id,name:e.name||e.id,ax:a.x,ay:a.y,ux:dx/L,uy:dy/L,L,h:(TYPES[e.cls]||TYPES.local).width/2}}).filter(Boolean);
 const X=[...CROSSWALKS,...(typeof ZEBRA_XW!=='undefined'?ZEBRA_XW:[])].map(c=>{const e=RD.find(r=>r.id===c.roadId);return e?{x:c.x,y:c.y,ux:e.ux,uy:e.uy,h:e.h,dep:20}:null}).filter(Boolean);
 const onRoad=(x,y)=>{for(const r of RD){const px=x-r.ax,py=y-r.ay,t=px*r.ux+py*r.uy,o=Math.abs(-px*r.uy+py*r.ux);if(t>=0&&t<=r.L&&o<r.h-1){for(const c of X){const qx=x-c.x,qy=y-c.y;if(Math.abs(qx*c.ux+qy*c.uy)<=c.dep&&Math.abs(-qx*c.uy+qy*c.ux)<=c.h+2)return null}return r}}return null};
 const g=n=>{try{return eval(n)}catch(e){return undefined}};
 /* p552 (the coordinator 3.11): the bus bays too — a person inside a bay fails, unless on the way from the bus door when alighting (BUS_ALIGHTERS, stage 0) */
 const BB=g('BUS_BAY'),BAYS=BB?(g('BUS_PHYS')||[]).filter(p=>p.bay&&p.F).map(p=>({id:'BAY-'+p.id,name:'מפרץ האוטובוס '+p.id+' ('+p.stops.join(', ')+')',F:p.F,h:p.F.roadW/2})):[];
 const onBay=(x,y)=>{if(!BB)return null;const S=BB.stop/2,E=S+BB.entry;for(const b of BAYS){const F=b.F,dx=x-F.rx,dy=y-F.ry,s=Math.abs(dx*F.ux+dy*F.uy),d=dx*F.nx+dy*F.ny;if(s>E||d<b.h||d>b.h+BB.depth)continue;if(s<=S||d<=b.h+BB.depth*(E-s)/BB.entry)return b}return null};
 const atDoor=(x,y)=>{try{const P=g('P34G'),a=(g('BUS_ALIGHTERS')||[]).find(q=>q.id===(P&&P.k));return!!(a&&a.stage===0&&Math.hypot(a.x-x,a.y-y)<6)}catch(e){return false}};
 const along=(P,d)=>{let per=0;const seg=[];for(let k=0;k<P.length;k++){const a=P[k],b=P[(k+1)%P.length],l=Math.hypot(b[0]-a[0],b[1]-a[1]);seg.push([a,b,l]);per+=l}d=((d%per)+per)%per;let q=0;while(q<seg.length-1&&d>seg[q][2]){d-=seg[q][2];q++}const A=seg[q][0],B=seg[q][1],f=d/(seg[q][2]||1);return[A[0]+(B[0]-A[0])*f,A[1]+(B[1]-A[1])*f]};
 const seen={};const hit=(q,r,s)=>{const key=q.id+'|'+r.id;if(seen[key]){seen[key].n++;return}seen[key]={n:1};out.hits.push({who:q.id,kind:q.kind,x:Math.round(q.x),y:Math.round(q.y),zone:zone(q.x,q.y),road:r.id,roadName:r.name,t:s})};
 // (א) by the state
 const people=(now)=>{const L=[],t=now/1000;
  for(const n of (g('NPC_PEDESTRIANS')||[]))if(!(n.ghost>0))L.push({id:n.id,kind:'הולך רגל',x:n.x,y:n.y,cw:!!n.inCrosswalk});
  try{if(g77PlayerOnFoot())L.push({id:'PLAYER',kind:'השחקן ברגל',x:PlayerPed.x,y:PlayerPed.y})}catch(e){}
  for(const q of (g('F2_PEOPLE')||[]))if(!q.hidden&&Number.isFinite(q.x))L.push({id:q.id,kind:'נוסע בשדה',x:q.x,y:q.y,cw:!!q.crossing});
  /* R-78: the bus passengers, boarding and alighting (one list in the game) */
  for(const a of (g('BUS_ALIGHTERS')||[]))if(a&&Number.isFinite(a.x)&&Number.isFinite(a.y))L.push({id:a.id,kind:String(a.id).startsWith('BUS-BOARD')?'נוסע עולה לאוטובוס':'נוסע יורד מאוטובוס',x:a.x,y:a.y,bus:true});
  const Z=(g('TC_LIVE')||{zones:{}}).zones;for(const z in Z){let M=[];try{M=Z[z].movers(now,true)}catch(e){}for(const m of M)if(m.kind==='אנשים'){const b=m.box;L.push({id:m.id,kind:'עובד / פרט חי ('+z+')',x:(b[0]+b[2])/2,y:b[3]-3})}}
  for(const k of ['A34_BASE','C3D','D3ND','C4ND','D4ND','B3LOOKD','B4G']){const D=g(k);if(!D||!D.gardeners)continue;D.gardeners.forEach((q,i)=>{if(!q.path)return;const p=along(q.path,t*q.speed+i*37);L.push({id:k+'-GARDENER-'+(i+1),kind:'גנן',x:p[0],y:p[1]})})}
  return L};
 // (ב) by the drawing: every person the game draws on its own canvas, in world coordinates (the feet)
 const W=window.__POR={on:false,list:[]},MC=ctx,cvs=MC.canvas;
 const toWorld=(c,x,y)=>{const m=c.getTransform(),dx=m.a*x+m.c*y+m.e,dy=m.b*x+m.d*y+m.f,dpr=cvs.width/(cvs.clientWidth||innerWidth);return{x:Camera.x+(dx/dpr-innerWidth/2)/Camera.zoom,y:Camera.y+(dy/dpr-innerHeight/2)/Camera.zoom}};
 const who=()=>{const st=(new Error().stack||'').split('\\n').slice(3,7).map(l=>{const m=l.match(/at (?:async )?([\\w$.<>]+)/);return m?m[1]:'?'}).filter(n=>n!=='?'&&n!=='Object.draw');return st.slice(0,3).join(' < ')};
 const rec=(c,x,y,tag)=>{if(!W.on||c!==MC)return;const w=toWorld(c,x,y),bay=onBay(w.x,w.y);W.list.push({x:w.x,y:w.y,tag,by:(onRoad(w.x,w.y)||bay)?who():null,door:!!bay&&atDoor(w.x,w.y)})};
 const P0=window.P34&&P34.draw;if(P0)P34.draw=function(c,x,y,look){rec(c,x,y,'P34');return P0.apply(this,arguments)};
 const TD=TurboCity.draw;TurboCity.draw=function(c,a,x,y,o){if(W.on&&c===MC&&typeof a==='string'&&a.startsWith('PE-')){let fx=x,fy=y;try{const I=TurboCity.info(a,o||{}),f=I.an&&I.an.find(q=>q[0]==='Feet');fx=x+(f?f[1]:I.w/2);fy=y+(f?f[2]:I.h)}catch(e){}   /* the feet anchor, with the same options as the drawing */rec(c,fx,fy,a)}return TD.apply(this,arguments)};
 const views=[];for(let y=-400;y<7800;y+=900)for(let x=800;x<9700;x+=1600)views.push([x,y]);
 const cam0={x:Camera.x,y:Camera.y,zoom:Camera.zoom},mq=State.mapQa;
 const sweep=(s)=>{out.sweeps++;State.mapQa=true;for(const [x,y] of views){Camera.x=x;Camera.y=y;Camera.zoom=1.2;W.list=[];W.on=true;try{render(SIM_LOOP.simNow)}catch(e){out.renderErr=out.renderErr||String(e).slice(0,200)}W.on=false;out.views++;
   for(const q of W.list){out.drawn++;out.tags[q.tag]=(out.tags[q.tag]||0)+1;if(!q.by)continue;const r=onRoad(q.x,q.y)||(q.door?null:onBay(q.x,q.y));if(r)hit({id:'ציור: '+q.by+' ('+q.tag+')',kind:'אדם מצויר',x:q.x,y:q.y},r,s)}}
  Camera.x=cam0.x;Camera.y=cam0.y;Camera.zoom=cam0.zoom;State.mapQa=mq};
 const S=SIM_LOOP,H=S.h;if(S.simNow==null)S.simNow=performance.now();
 /* R-78: the state every half second of game time (EVERY), the drawing every DRAW_EVERY seconds */
 const KH=Math.round(1/EVERY),DK=Math.round(DRAW_EVERY/EVERY),NSTEP=Math.max(1,Math.round(EVERY/H));
 try{for(let k=0;k<=T*KH;k++){const s=k/KH;if(k>0){for(let i=0;i<NSTEP;i++){simStep(H,S.simNow+H*1000);S.simNow+=H*1000}}
  if(k%DK===0)sweep(s);
  out.samples++;const P=people(S.simNow);out.people=Math.max(out.people,P.length);let nb=0;
  for(const q of P){out.sources[q.kind]=(out.sources[q.kind]||0)+1;if(q.bus)nb++;if(q.cw)continue;const r=onRoad(q.x,q.y);if(r){hit(q,r,s);continue}const b=onBay(q.x,q.y);if(!b)continue;if(q.bus){out.busInBay++;continue}hit(q,b,s)}
  out.busPax=Math.max(out.busPax,nb)}}
 finally{if(P0)P34.draw=P0;TurboCity.draw=TD}
 out.sources['אדם מצויר (כל המקורות)']=out.drawn;
 for(const h of out.hits)h.times=seen[h.who+'|'+h.road].n;out.ok=!out.hits.length;return JSON.stringify(out)})()`;
  const R = JSON.parse(await ev(Q)); R.build = path.basename(file); R.at = new Date().toISOString(); R.errs = errs.slice(0, 6);
  const out = path.resolve(outArg || path.join('qa', 'people_on_road.json')); fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log('people_on_road ' + (R.ok ? 'עובר' : 'נכשל') + ' · ' + R.samples + ' דגימות מצב (כל ' + R.every + ' שנ׳) ו-' + R.sweeps + ' מעברי ציור (כל ' + R.drawEvery + ' שנ׳, ' + R.views + ' תצוגות) ב-' + R.T + ' שנ׳ · עד ' + R.people + ' אנשים בדגימת מצב, מהם עד ' + R.busPax + ' נוסעי אוטובוס · ' + R.busInBay + ' פעמים נוסע במפרץ, בין הדלת למדרכה · ' + R.drawn + ' אנשים מצוירים · ' + R.hits.length + ' על נתיב נסיעה' + (R.renderErr ? ' · שגיאת ציור: ' + R.renderErr : ''));
  console.log('  לפי המקור (מספר האנשים בכל הדגימות): ' + Object.entries(R.sources).map(([k, v]) => k + ' ' + v).join(' · '));
  for (const h of R.hits.slice(0, 60)) console.log('  ' + h.who + ' (' + h.kind + ') · ' + h.zone + ' · ' + h.roadName + ' · (' + h.x + ', ' + h.y + ') · שנ׳ ' + h.t + (h.times > 1 ? ' · ' + h.times + ' דגימות' : ''));
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1) });
