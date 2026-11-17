// rails 17.11 — דף הציור: כל הפיצולים וההשתלבויות במפה, ציון לכל אחד, ולפני / אחרי לבעייתיים. SVG בקוד בלבד (כללים 13 / 17).
const fs=require('fs'),path=require('path');const {load,drawBefore,SvgCtx}=require('./render_lib.js');const {P}=require('./proposals.js');const {frogDeg}=require('./geom.js');
const [wt,netf,measf,outf,measAf]=process.argv.slice(2);const net=JSON.parse(fs.readFileSync(netf,'utf8'));const M=JSON.parse(fs.readFileSync(measf,'utf8'));const MA=measAf?JSON.parse(fs.readFileSync(measAf,'utf8')):null;
const S=Object.fromEntries(net.segs.map(g=>[g.id,g])),N=Object.fromEntries(net.nodes.map(n=>[n.id,n]));
const m=v=>(v/10).toFixed(1);
// ---- the junctions, grouped by place, with a verdict
const ZONE=j=>{const x=j.x,y=j.y;if(y<2000&&x>5850)return'E3';if(y<3420&&x>5700)return'E4';if(y<4290&&x<5860&&y>3400)return'E5';if(y>=4200&&y<4800&&x>5700&&x<6000)return'E6 · תחנת הנמל';if(y>5000&&y<5250&&x<5800)return'E6 / D6 / C6 · הנמל';if(x>=5800&&y<5300)return'הים — הצומת מזרחית לחוף';return'האי'};
const PHOTO=new Set(['B-J','ISL-J0A','ES-JB','EAST-JN']);
const ISL4=new Set(['ISL-XA','ISL-XB']);
const seen=new Set(),rows=[];
for(const j of M.junctions){const key=[j.node,j.div.replace(/\(.*/,'')].join('|');if(seen.has(key))continue;seen.add(key);
 const R=j.rmin_px,f=j.frog_deg;let st,cls;
 if(PHOTO.has(j.node)){st='מצויר לא טוב (הצילום)';cls='bad'}
 else if(R<120){st='חד מדי';cls='sharp'}else if(R<190){st='גבולי';cls='edge'}else{st='תקין';cls='ok'}
 rows.push({...j,zone:ZONE(j),st,cls,div:j.div.replace(/\(.*/,''),isl4:ISL4.has(j.node)})}
for(const x of M.crossings)rows.push({node:'צומת בלי מסוט',x:x.x,y:x.y,div:x.a+' × '+x.b,parent:'',rmin_px:null,frog_deg:x.angle_deg,frog_at:null,sep44_at:null,zone:'הים — הצומת מזרחית לחוף',st:'חופף — מסילה מעל מסילה (הצילום)',cls:'bad',diamond:true});
const order=['E3','E4','E5','E6 · תחנת הנמל','E6 / D6 / C6 · הנמל','הים — הצומת מזרחית לחוף','האי'];rows.sort((a,b)=>order.indexOf(a.zone)-order.indexOf(b.zone)||a.y-b.y||a.x-b.x);
const COL={ok:'#2e9d5b',edge:'#d99a1e',sharp:'#d2452f',bad:'#8a3cc9'};
const cnt=k=>rows.filter(r=>r.cls===k).length;
// ---- overview map
function overview(){const vb=[2450,450,7200,7300],c=[];const sx=v=>v,sy=v=>v;
 c.push(`<rect x="${vb[0]}" y="${vb[1]}" width="${vb[2]}" height="${vb[3]}" fill="var(--sea)"/>`);
 c.push(`<rect x="2450" y="450" width="3550" height="4760" fill="var(--land)"/>`);
 for(const g of net.segs){const p=g.pts.map(q=>[Math.min(q[0],9800),q[1]]);c.push(`<polyline points="${p.map(q=>q.join(',')).join(' ')}" fill="none" stroke="var(--trk)" stroke-width="16" stroke-linejoin="round"/>`)}
 for(const r of rows){const R=r.diamond?44:34;c.push(`<circle cx="${r.x}" cy="${r.y}" r="${R}" fill="${COL[r.cls]}" fill-opacity=".9" stroke="#fff" stroke-width="6"/>`)}
 const lab=[[5420,1500,'E3 · התחנה המרכזית'],[5350,2900,'E4 · תחנת החוף'],[5280,3850,'E5 · החצר'],[5250,4500,'E6 · תחנת הנמל'],[3500,5010,'הנמל · C6 / D6 / E6'],[6200,4930,'הצומת שבצילום'],[7550,6300,'הגשר לאי (island4)'],[6800,5000,'← למזרח']];
 for(const [x,y,t] of lab)c.push(`<text x="${x}" y="${y}" font-size="120" fill="var(--ink)" text-anchor="middle" font-weight="700" paint-order="stroke" stroke="var(--bg)" stroke-width="22">${t}</text>`);
 c.push(`<rect x="6040" y="4980" width="560" height="320" fill="none" stroke="${COL.bad}" stroke-width="14" stroke-dasharray="40 24"/>`);
 return`<svg viewBox="${vb.join(' ')}" class="map" role="img" aria-label="מפת המסילות וכל הפיצולים">${c.join('')}</svg>`}
// ---- the photo spot: before / after with the game's own drawing code
function photo(){const box=[6250,5000,6640,5300];const out={};for(const [tag,wp] of[['before',false],['after',true]]){const L=load(wt,JSON.parse(JSON.stringify(net)),wp);const c=new SvgCtx();drawBefore(L,c,box,{sea:'#1d5b88'});out[tag]=c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],'100%',' class="shot"')}return out}
// ---- land areas (E4 / E3): before = the turnouts of 038d on the old geometry; after = the built geometry and the junction drawing (038d2)
function land(box,after){const L=load(wt,JSON.parse(JSON.stringify(net)),after);const G=L.G,c=new SvgCtx();G.ctx=c;
 c.fillStyle='#cfc8b4';c.fillRect(box[0]-100,box[1]-100,box[2]-box[0]+200,box[3]-box[1]+200);
 for(const x of[5800,5900]){c.fillStyle='#666b6d';c.fillRect(x-24,box[1]-50,48,box[3]-box[1]+100);c.fillStyle='#413d37';for(let y=2558;y<box[3]+50;y+=16)if(y>box[1]-60)c.fillRect(x-20,y,40,5);c.strokeStyle='#c6cbd0';c.lineWidth=3;for(const dx of[-13,13]){c.beginPath();c.moveTo(x+dx,box[1]-50);c.lineTo(x+dx,box[3]+50);c.stroke()}}
 const segs=Object.values(L.RAIL_SEG_BY_ID);for(const g of segs){if(/^(A-|B-|T1|T2)/.test(g.id)&&g.pts.length===2)continue;if(!g.pts.some(p=>p[0]>box[0]-80&&p[0]<box[2]+80&&p[1]>box[1]-80&&p[1]<box[3]+80))continue;c.save();G.rlTrack({id:g.id,pts:g.pts});c.restore()}
 for(const J of G.TCT_J){try{J._p=null;G.tctDraw(c,J)}catch(e){}}
 if(after&&G.RJX)for(const Z of G.RJX.zones)G.rjxDraw(c,Z);
 return c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],'100%',' class="sk"')}
// ---- a proposal: before / after of the centre lines and rails (the same simple drawing for both — the shape, not the paint)
function sketch(key,after){const p=P[key],box=p.box,c=new SvgCtx();const L=load(wt,JSON.parse(JSON.stringify(net)),false);const G=L.G;G.ctx=c;
 c.fillStyle='#e9e4d6';c.fillRect(box[0]-50,box[1]-50,box[2]-box[0]+100,box[3]-box[1]+100);
 const segs=net.segs.map(g=>after&&p.segs[g.id]?{...g,pts:p.segs[g.id]()}:g).map(g=>({...g,_rails:null}));
 const vis=g=>g.pts.some(q=>q[0]>box[0]-80&&q[0]<box[2]+80&&q[1]>box[1]-80&&q[1]<box[3]+80);const Ls=segs.filter(vis);
 // after: the straight parts move with their nodes (the mains are drawn whole anyway)
 for(const k of[0,1,2])for(const g of Ls){c.save();G.rlTrackLayer(g,k);c.restore()}
 // the junction marks and the radius labels
 const hl=Object.keys(p.segs);for(const g of Ls){if(!hl.includes(g.id))continue;const pts=g.pts,mid=pts[Math.floor(pts.length/2)];
  const R=Math.round(require('./geom.js').s2len?0:0);c.strokeStyle=after?'#2e9d5b':'#d2452f';c.lineWidth=4;c.setLineDash([10,8]);c.beginPath();pts.forEach((q,i)=>i?c.lineTo(q[0],q[1]):c.moveTo(q[0],q[1]));c.stroke();c.setLineDash([])}
 return c.svg([box[0],box[1],box[2]-box[0],box[3]-box[1]],'100%',' class="sk"')}
function rmin(pts){let mn=1e9;for(let i=2;i<pts.length-2;i++){const a=pts[i-2],b=pts[i],cc=pts[i+2],ab=Math.hypot(b[0]-a[0],b[1]-a[1]),bc=Math.hypot(cc[0]-b[0],cc[1]-b[1]),ca=Math.hypot(a[0]-cc[0],a[1]-cc[1]),ar=Math.abs((b[0]-a[0])*(cc[1]-a[1])-(cc[0]-a[0])*(b[1]-a[1]))/2;if(ar>1e-6)mn=Math.min(mn,ab*bc*ca/(4*ar))}return mn}
const ph=photo();
const BUILT=new Set(['E4-THROAT','E3-BYPN','E6-XOVER','E5-YARD']);const props=Object.entries(P).filter(([k])=>!BUILT.has(k)).map(([k,p])=>{const lines=Object.entries(p.segs).map(([id,f])=>{const b=S[id],a=f(),rb=rmin(b.pts),ra=rmin(a);return`<tr><td>${id}</td><td>${m(rb)} מ׳ · לב ${frogDeg(Math.max(rb,26.1)).toFixed(0)}°</td><td>${m(ra)} מ׳ · לב ${frogDeg(ra).toFixed(0)}°</td></tr>`}).join('');
 return`<section class="card"><h3>${p.title}</h3><p>${p.note}</p><div class="pair"><figure><figcaption>לפני</figcaption>${sketch(k,false)}</figure><figure><figcaption>אחרי (מוצע)</figcaption>${sketch(k,true)}</figure></div>
 <table class="mini"><thead><tr><th>קטע</th><th>היום — רדיוס מינימלי</th><th>מוצע</th></tr></thead><tbody>${lines}</tbody></table></section>`}).join('');
const BUILTN=new Set(['SW-A-N','SW-P1','SW-12','J-2','SW-23','J-3','SW-LS','SW-A-S','BYP-N']);const AF={};if(MA)for(const j of MA.junctions)AF[j.node+'|'+j.div.replace(/\(.*/,'')]=j;
const stA=r=>{if(r.diamond)return['מצויר כצומת (לבבות + פסי הגנה)','ok'];const a=AF[r.node+'|'+r.div]||r,R=a.rmin_px,f=a.frog_deg,pre=PHOTO.has(r.node)?'מצויר מחדש · ':'';return R<120?[pre+'חד מדי','sharp']:R<190?[pre+(BUILTN.has(r.node)?(r.node==='BYP-N'?'גבולי — 15 מ׳ (רציף 2 צמוד)':'גבולי — רדיוס של חצר (לאישורך)'):'גבולי (לא שונה)'),'edge']:[pre+'תקין','ok']};
for(const r of rows){const a=AF[r.node+'|'+r.div];r.aR=a?a.rmin_px:r.rmin_px;r.aF=a?a.frog_deg:r.frog_deg;[r.ast,r.acls]=stA(r);if(r.diamond){r.aR=null;r.aF=r.frog_deg}}
const cntA=k=>rows.filter(r=>r.acls===k).length;
const trs=rows.map(r=>`<tr><td><span class="dot" style="background:${COL[r.cls]}"></span>${r.st}${r.isl4?' · של island4':''}</td><td>${r.zone}</td><td>${r.node}</td><td>${r.div}</td><td class="n">${Math.round(r.x)}, ${Math.round(r.y)}</td><td class="n">${r.rmin_px==null?'—':m(r.rmin_px)+' מ׳'}</td><td class="n">${r.frog_deg==null?'—':r.frog_deg+'°'}</td><td><span class="dot" style="background:${COL[r.acls]}"></span>${r.ast}</td><td class="n">${r.aR==null?'—':m(r.aR)+' מ׳'}</td><td class="n">${r.aF==null?'—':r.aF+'°'}</td></tr>`).join('');
const e5b=land([5600,3480,5860,4280],false),e5a=land([5600,3480,5860,4280],true),e6b=land([5730,4080,5960,4580],false),e6a=land([5730,4080,5960,4580],true),e4b=land([5745,2660,6030,3400],false),e4a=land([5745,2660,6030,3400],true),e3b=land([5840,1680,6020,2040],false),e3a=land([5840,1680,6020,2040],true);
// the map: the colour after the build; a ring where it changed
const ov=overview().replace(/<circle cx="([\d.]+)" cy="([\d.]+)" r="(\d+)" fill="([^"]+)"/g,(q,x,y,r,f)=>{const R=rows.find(o=>Math.abs(o.x-x)<.6&&Math.abs(o.y-y)<.6);if(!R)return q;const ch=R.acls!==R.cls;return(ch?`<circle cx="${x}" cy="${y}" r="${+r+22}" fill="none" stroke="${COL[R.cls]}" stroke-width="12"/>`:'')+`<circle cx="${x}" cy="${y}" r="${r}" fill="${COL[R.acls]}"`});
const html=`<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>חיבורי הרכבת</title>
<style>:root{--bg:#f6f3ec;--ink:#1f2328;--mut:#5b6168;--card:#fff;--line:#d9d3c4;--sea:#cfe0ea;--land:#ece6d6;--trk:#5b6168}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181b;--ink:#e8e6e1;--mut:#a3a8ad;--card:#1e2226;--line:#33393f;--sea:#17303f;--land:#23262a;--trk:#9aa1a7}}
:root[data-theme="dark"]{--bg:#15181b;--ink:#e8e6e1;--mut:#a3a8ad;--card:#1e2226;--line:#33393f;--sea:#17303f;--land:#23262a;--trk:#9aa1a7}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,"Segoe UI",Arial,sans-serif}main{max-width:1100px;margin:0 auto;padding:20px 16px 60px}
h1{font-size:26px;margin:.2em 0}h2{font-size:20px;margin:1.6em 0 .5em}h3{font-size:17px;margin:.2em 0 .4em}p{margin:.4em 0}.mut{color:var(--mut)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:12px 0}.kpi{display:flex;flex-wrap:wrap;gap:10px}.kpi div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 14px}.kpi b{font-size:22px;display:block}
.map{width:100%;height:auto;border-radius:10px;border:1px solid var(--line)}.shot,.sk{width:100%;height:auto;border-radius:8px;display:block}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media (max-width:700px){.pair{grid-template-columns:1fr}}.pair.narrow{max-width:560px}figure{margin:0}figcaption{font-weight:700;margin-bottom:4px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}td.n{direction:ltr;text-align:left;white-space:nowrap}.dot{display:inline-block;width:11px;height:11px;border-radius:50%;margin-left:6px;vertical-align:-1px}
.wrap{overflow-x:auto}.mini{margin-top:8px}.legend span{margin-left:14px;white-space:nowrap}</style></head><body><main>
<h1>חיבורי הרכבת וההשתלבויות — מדידה, ציון, ומה נבנה</h1>
<p class="mut">סבב 17.11 · סוכן המסילות · מעל S7F303 · כל המספרים נמדדו מהגאומטריה של המשחק (10 פיקס׳ = 1 מ׳). הציורים — בקוד בלבד, בקוד הציור של המשחק עצמו (המסוטים של 038d, הסיפונים והמסילות של 040, והציור החדש של הצמתים — 038d2).</p>
<div class="kpi"><div><b>${rows.length}</b>פיצולים והשתלבויות (וצומת אחד בלי מסוט)</div><div><b style="color:${COL.ok}">${cnt('ok')} ← ${cntA('ok')}</b>תקין (לפני ← אחרי)</div><div><b style="color:${COL.edge}">${cnt('edge')} ← ${cntA('edge')}</b>גבולי</div><div><b style="color:${COL.sharp}">${cnt('sharp')} ← ${cntA('sharp')}</b>חד מדי</div><div><b style="color:${COL.bad}">${cnt('bad')} ← ${cntA('bad')}</b>מצויר לא טוב / חופף</div></div>
<section class="card"><h3>הקנה מידה</h3><p>"תקין" — רדיוס של 19 מ׳ ומעלה — כמו הקשתות שכבר אושרו: פס א׳ לאי 25 מ׳, פס ב׳ לאי 19 מ׳, הקשתות בנמל 19–20 מ׳. "גבולי" — 12–19 מ׳. "חד מדי" — פחות מ-12 מ׳. הלב (הזווית שבה הפס הפנימי חוצה את הפס של המסילה הראשית) נגזר מהרדיוס ומופיע בטבלה. מה שנבנה: 25 מ׳ בקו הראשי (לב 26°–27°), 15 מ׳ בחצר הצפופה (לב 31°–34°) — בשתי קשתות משיקות, בלי פינה ובלי קצה חד.</p></section>
<section class="card"><h3>הציור של כל מסוט (הבעלים 20:15: "לא משתלב אלא עולה על הקיים")</h3><p>בכל המסוטים — בצמתים שנבנו וגם בכל שאר המסוטים במפה: (1) הענף יוצא משיק לפס של הקו הראשי; (2) באזור המסוט — אדנים ארוכים משותפים לשני הקווים, והאדנים של הענף מתחילים רק אחריהם (שכבה אחת); (3) להבים, לב ופסי הגנה — פעם אחת; (4) הפס של הקו הראשי והפס הפנימי של הענף נחתכים בלב ונפגשים בו — אף פס לא מצויר מעל פס אחר. הגאומטריה לא השתנתה.</p></section>
<h2>המפה (הצבע — אחרי; טבעת — הצבע שהיה)</h2><p class="legend"><span><span class="dot" style="background:${COL.ok}"></span>תקין</span><span><span class="dot" style="background:${COL.edge}"></span>גבולי</span><span><span class="dot" style="background:${COL.sharp}"></span>חד מדי</span><span><span class="dot" style="background:${COL.bad}"></span>מצויר לא טוב / חופף</span></p>
${ov}
<h2>1. המקום שבצילום — הצומת מזרחית לחוף (x 6050–6580) · נבנה</h2>
<section class="card"><p><b>מה קרה:</b> כל קטע צויר לבד, ואחרי זה הלוח של המסוט של מסילת ההיפוך (J-F6-SID) צבע מעל ראש שתי מסילות האי — הן נעלמות מתחת ללוח וחוזרות; הלוח צייר את מעקה הסיפון בתוך הפס הדרומי (y 5151); הסיפון והאדנים של מסילות האי עלו על שפת הסיפון ועל האדנים של הפס הדרומי; ופס א׳ לאי חוצה את הפס הדרומי (31.7°) בלי לב ובלי פסי הגנה.</p>
<p><b>מה נבנה:</b> ציור אחד לכל הצומת, בשכבות — סיפון אחד עם מעקה רק בשפה החיצונית, מצע, אדנים (ארוכים מתחת לשני הפסים בכל מסוט), כל הפסים רציפים, להבי מסוט, מוט ועמוד הפעלה, לבבות ופסי הגנה — גם בצומת. הגאומטריה והרכבות — כמו שהן (פס א׳ 25 מ׳, פס ב׳ 18 מ׳, הקשת B-LINK ‏40 מ׳, מסילת ההיפוך 27 מ׳).</p>
<div class="pair"><figure><figcaption>לפני (S7F303)</figcaption>${ph.before}</figure><figure><figcaption>אחרי (נבנה)</figcaption>${ph.after}</figure></div>
<p class="mut">לאישורך: המסוט של מסילת ההיפוך (EAST-JN, ‏x 6460) יושב בתוך האזור של המסוט לאי (הלב של פס א׳ ב-x 6492) — מסוט כפול, מצויר נכון. להזיז אותו 5 מ׳ מזרחה זה להזיז את הקשת שלו לתוך מפתח השיט של המרינה — של island4; לא נגעתי.</p></section>
<h2>2. E4 — ראש תחנת החוף (X-BA, ‏XS, ‏BYP-SC, ‏XN) · נבנה</h2>
<section class="card"><p><b>היה:</b> ארבעה מעברים קצרים בין פס א׳ לפס ב׳ (10 מ׳ זה מזה) — S של 12–17 מ׳ אורך, רדיוס 4.8–7.3 מ׳ ולב 35°–48°: חד מדי.</p>
<p><b>נבנה:</b> X-BA ו-XS — מעבר כפול (מספריים) באותו קטע, כל אחד שתי קשתות R 25 מ׳ (30 מ׳ אורך, לב 26°), וצומת באמצע (74°) עם לבבות ופסי הגנה; המעקף יוצא מפס ב׳ ב-y 3015 (R 26 מ׳) — יחד עם XS מסוט משולש; XN — R 25 מ׳ מ-y 3042. ציור אחד לכל ראש התחנה, אדנים ארוכים מתחת למעברים. XBA-B נשאר ב-y 2702 (מדרום לגשר UX-1), ‏SW-N-A ב-3342.</p>
<p class="mut">אושר (D‑704, מחליף את D‑536): SW-S-A עבר ל-y 2702, ‏XBA-A ל-3002, ‏SW-S-B ל-3002, המעקף ל-3015. הרכבות (FRT-1, ‏FRT-4, ‏RL-PS-01) — אותם מסלולים; המרחקים לפי הצמתים החדשים.</p>
<div class="pair narrow"><figure><figcaption>לפני</figcaption>${e4b}</figure><figure><figcaption>אחרי (נבנה)</figcaption>${e4a}</figure></div></section>
<h2>3. E3 — הקצה הצפוני של המעקף (BYP-NC) · נבנה (15 מ׳)</h2>
<section class="card"><p>היה: 8.7 מ׳, לב 38°. נבנה: R 15 מ׳ (לב 34°) — הקשת מתחילה ב-y 1922 במקום 1900; המסוט על פס ב׳ נשאר ב-y 1720. לא 25 מ׳: בקשת של 25 מ׳ המעקף צמוד לפס ב׳ עד y ~1880, והרכבת של רציף 2 (RL-PS-01, הראש ב-y 1830) נגעה ברכבת המשא שעוברת במעקף (נמצא בבדיקה) — ב-15 מ׳ יש 4.8 מ׳ בין המרכזים שם.</p>
<div class="pair narrow"><figure><figcaption>לפני</figcaption>${e3b}</figure><figure><figcaption>אחרי (נבנה)</figcaption>${e3a}</figure></div></section>
<h2>4. E6 — המעבר צפונית לתחנת הנמל (XOVER) · נבנה</h2>
<section class="card"><p>היה: 17 מ׳ אורך על 10 מ׳ רוחב — 6.8 מ׳, לב 38°. נבנה: R 25 מ׳ (לב 26°). הרציף של תחנת הנמל מתחיל ב-y 4470, ולכן הקצה על פס א׳ נשאר (4462) והעוקץ על פס ב׳ עלה מ-4290 ל-4162 (בתוך E5 — אין שם מסוט אחר; רכבת הים FRT-3 לא נוסעת בפס ב׳). FRT-1 ו-FRT-4 — אותו מסלול.</p>
<div class="pair narrow"><figure><figcaption>לפני</figcaption>${e6b}</figure><figure><figcaption>אחרי (נבנה)</figcaption>${e6a}</figure></div></section>
<h2>5. E5 — החצר (LEAD-N, ‏X12, ‏X23, ‏LEAD-S) · נבנה</h2>
<section class="card"><p>היה: 4.9–7.5 מ׳, לב 36°–42°. המסילות בחצר 4.8 מ׳ זו מזו — נבנה רדיוס של חצר: 15 מ׳ (גבולי — לאישורך), בשתי קשתות משיקות. הסולם התארך דרומה (SW-P1 ‏3748, ‏SW-12 ‏3764, ‏J-2 ‏3927, ‏SW-23 ‏3943, ‏J-3 ‏4106, ‏SW-LS ‏4064), ופס 3 התארך עד הבולם ב-y 4130 (בתוך גדר החצר). המסוטים על פס א׳ לא זזו. קטר התמרון עובד באותו מקום; קרון ההופר עבר ל-Y2-DOOR (Y2-B התקצר).</p>
<div class="pair narrow"><figure><figcaption>לפני</figcaption>${e5b}</figure><figure><figcaption>אחרי (נבנה)</figcaption>${e5a}</figure></div></section>
<section class="card"><h3>האי — המעבר ISL-X (אחרי המפתח המתרומם)</h3><p>7 מ׳ ולב 37° — חד מדי. על הגשר של island4: ההצעה (R 19 מ׳ — מעבר של כ-18 מ׳) עוברת אליו דרכך.</p></section>
<section class="card" hidden><h3>-</h3><p>החצר צפופה (4.8 מ׳ בין המסילות, הבולם של פס 3 ב-y 4022) — רדיוס של 15 מ׳ דורש להאריך את פס 3 ולהזיז את הקרונות העומדים.</p></section>
<h2>כל הפיצולים</h2><div class="wrap"><table><thead><tr><th>לפני</th><th>מקום</th><th>צומת</th><th>המסילה המתפצלת</th><th>x, y</th><th>רדיוס מינימלי</th><th>לב</th><th>מהעוקץ ללב</th><th>אחרי</th><th>רדיוס</th><th>לב</th></tr></thead><tbody>${trs}</tbody></table></div>
<p class="mut">מסילות מקבילות: בים ובנמל 3.8 מ׳ בין המרכזים (הסיפונים נוגעים — מצויר כסיפון אחד); הפסים הראשיים 10 מ׳; החצר 4.8 מ׳. נמדדו גם כל החפיפות של מצע במצע — כולן בתוך אזורי מסוט או מסילות מקבילות. אחרי הבנייה: שני צמתים בלי מסוט (פס א׳ לאי × הפס הדרומי; ‏X-BA × XS במעבר הכפול) — שניהם מצוירים כצומת, ואין מסילה שמצוירת מעל מסילה.</p>
</main></body></html>`;
fs.writeFileSync(outf,html);console.log('ok',outf,(html.length/1024).toFixed(0)+'KB',rows.length,'rows');
