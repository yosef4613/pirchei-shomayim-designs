// q_spots.js — fieldcalc: חניות לרכבי השירות החדשים (מה שהחישוב אומר שחסר: fc_result.json:fleet — need מול today_spots) בכיסים של היום
// קריאה בלבד. לכל רכב חדש: הכיס המועדף ליד העמדות שהוא משרת → המקום הקרוב ביותר לעמדה שבו המלבן (המידות של הסוג, האף דרומה; אם לא נכנס — מזרחה)
// בתוך הכיס, לא על דרך שירות / סימון חצייה / מנחת / חניה קיימת (+0.6 מ׳), עם 3 מ׳ פנויים מלפנים, ו-≥ 0.3 מ׳ מכל רכב ומטוס של S15 בכל רגע של המחזור (כל 0.5 ש׳ — אותן קופסאות של s15k).
return (()=>{const t0=performance.now(),o={placed:[],failed:[]};try{
 const T=S15SIM.T,N=Math.round(T/.5),PI=Math.PI;
 const boxes=[],seen=new Set();const add=(b,id,kind)=>{const k=Math.round(b.x)+','+Math.round(b.y)+','+Math.round(Math.atan2(b.s,b.c)*30)+','+Math.round(b.hx)+','+Math.round(b.hy);if(seen.has(k))return;seen.add(k);boxes.push({x:b.x,y:b.y,c:b.c,s:b.s,hx:b.hx,hy:b.hy,R:Math.hypot(b.hx,b.hy),id,kind})};
 for(const v of S15SIM.veh){const S=s15kSample(v,v.legs,N);for(const a of S){if(!a)continue;for(const b of a.b)add(b,v.id,'veh')}}
 for(const q of s15kStatic())add(q.b[0],q.id,'stat');
 const AC=s15kAcBoxes(N);for(const L of AC)for(const a of L)for(const b of a.b)add(b,a.id,'ac');
 o.nBoxes=boxes.length;
 const D=S15D,rect=r=>({x0:r[0],y0:r[1],x1:r[2],y1:r[3]}),ov=(a,b,m)=>a[0]-m<b[2]&&a[2]+m>b[0]&&a[1]-m<b[3]&&a[3]+m>b[1];
 const FORB=[];for(const s of D.service||[])FORB.push([s.rect,0,'דרך '+s.id]);for(const s of D.xmarks||[])FORB.push([s.rect,0,'חצייה '+s.id]);
 /* העמדות עצמן לא אסורות (הכיסים בתוך המלבן של העמדה, מחוץ למעטפת) — המטוסים: הקופסאות של כל טיסה בכל רגע (למעלה) ושל המטוסים והמסוקים החונים קבוע (s15StaticList) */
 try{for(const q of s15StaticList()){if(q.heli){add(s15kObb(q.x,q.y,0,2*(q.r||120),2*(q.r||120)),q.key,'heli');continue}const f=S15SIM.flights.find(x=>x.model===q.id),a={kind:'ac',model:q.id,L:q.r,W:(f&&f.W)||q.r};for(const b of s15Boxes(a,[q.x,q.y,q.th,0]))add(s15kObb(b[0],b[1],b[2],2*b[3]+8,2*b[4]+8),q.key,'ac-park')}}catch(e){o.parkErr=String(e).slice(0,200)}
 for(const [id,s] of Object.entries(D.spots||{}))if(s.rect)FORB.push([s.rect,6,'חניה '+id]);
 for(const h of D.helipads||[]){const c=h.c,r=(h.pad||100)/2+20;FORB.push([[c[0]-r,c[1]-r,c[0]+r,c[1]+r],0,'מנחת '+h.id])}
 const AREA=Object.assign({},D.pockets);for(const b of D.base||[])AREA[b.id]=b.rect;
 const DIM={GP:[22,30],BT:[22,30],PT:[22,60],WT:[22,60],LV:[22,56],SVC:[22,62],MS:[22,75],BL:[22,75],CT:[28,85],FT:[28,100],AB:[28,124],TG:[22,45],FTs:[26,75]};
 const NEW=[['AB-R3','AB',['R1','R2'],['AIR-GSE-R1|R2','AIR-BASE-8']],['AB-R4','AB',['R1','R2'],['AIR-GSE-R1|R2','AIR-BASE-8']],
  ['BL-P3','BL',['P3'],['AIR-GSE-P2|P3','AIR-GSE-P3|P4']],['BL-P5','BL',['P5'],['AIR-GSE-P4|P5','AIR-GSE-P5|P6']],['BL-R','BL',['R2'],['AIR-GSE-R1|R2','AIR-GSE-R2|R3']],
  ['BT-P1B','BT',['P1'],['AIR-GSE-P1W','AIR-GSE-P1|P2-w']],['BT-P6B','BT',['P6'],['AIR-GSE-P6E','AIR-GSE-P6W']],['BT-R2','BT',['R2'],['AIR-GSE-R1|R2','AIR-GSE-R2|R3']],
  ['CT-P2','CT',['P2'],['AIR-GSE-P1|P2','AIR-GSE-P1|P2-w','AIR-GSE-P2|P3']],['CT-P4','CT',['P4','P5'],['AIR-GSE-P4|P5','AIR-GSE-P3|P4']],['CT-R','CT',['R1','R2'],['AIR-GSE-R1|R2','AIR-GSE-R2|R3']],
  ['FT-4','FT',['P1','P6','R1'],['AIR-BASE-4','AIR-BASE-8']],
  ['GP-C','GP',['C1','C2'],['AIR-GSE-CN','AIR-GSE-CE','AIR-GSE-CW']],['GP-GA1','GP',['GA1'],['AIR-GSE-GA1|GA2','AIR-GSE-GA2|GA3']],['GP-R1','GP',['R1'],['AIR-GSE-R1|R2']],
  ['GP-R2','GP',['R2'],['AIR-GSE-R1|R2','AIR-GSE-R2|R3']],['GP-R3','GP',['R3'],['AIR-GSE-R2|R3','AIR-GSE-R1|R2']],
  ['LV-P2','LV',['P2','P3'],['AIR-GSE-P1|P2-w','AIR-GSE-P2|P3']],['MS-R3','MS',['R1','R2'],['AIR-GSE-R2|R3','AIR-GSE-R1|R2']],
  ['SVC-P1','SVC',['P1','P2'],['AIR-GSE-P1|P2-w','AIR-GSE-P1W']],['WT-P6','WT',['P5','P6'],['AIR-GSE-P5|P6','AIR-GSE-P6W']]];
 const cen=id=>{const s=D.stands[id];if(!s||!s.rect)return null;const r=s.rect;return[(r[0]+r[2])/2,(r[1]+r[3])/2]};
 /* רשת של 64 פיקס׳: כל קופסה בכל התאים שהיא נוגעת בהם — כדי לבדוק כל מקום רק מול מה שקרוב אליו */
 const GS=64,GR=new Map(),gk=(i,j)=>i*100003+j,put=b=>{const i0=Math.floor((b.x-b.R)/GS),i1=Math.floor((b.x+b.R)/GS),j0=Math.floor((b.y-b.R)/GS),j1=Math.floor((b.y+b.R)/GS);for(let i=i0;i<=i1;i++)for(let j=j0;j<=j1;j++){const k=gk(i,j);let L=GR.get(k);if(!L)GR.set(k,L=[]);L.push(b)}};
 for(const b of boxes)put(b);let stamp=0;
 const gapAll=(c,id0)=>{stamp++;let g=1e9,w='';const i0=Math.floor((c.x-c.R-8)/GS),i1=Math.floor((c.x+c.R+8)/GS),j0=Math.floor((c.y-c.R-8)/GS),j1=Math.floor((c.y+c.R+8)/GS);
  for(let i=i0;i<=i1;i++)for(let j=j0;j<=j1;j++){const L=GR.get(gk(i,j));if(!L)continue;for(const b of L){if(b.st===stamp||b.id===id0)continue;b.st=stamp;const z=s15kGap(c,b);if(z<g){g=z;w=b.kind+' '+b.id}if(g<3)return[g,w]}}return[g,w]};
 for(const [vid,t,serves,pref] of NEW){const dm=DIM[t];let done=null,why=[];
  const tgt=serves.map(cen).filter(Boolean),tx=tgt.reduce((a,p)=>a+p[0],0)/Math.max(1,tgt.length),ty=tgt.reduce((a,p)=>a+p[1],0)/Math.max(1,tgt.length);
  for(const aid of pref){const A=AREA[aid];if(!A){why.push(aid+': אין');continue}
   for(const hd of ['S','E']){const w=hd==='S'?dm[0]:dm[1],h=hd==='S'?dm[1]:dm[0];const C=[];
    for(let x=A[0]+4;x+w<=A[2]-4;x+=6)for(let y=A[1]+4;y+h<=A[3]-4;y+=6)C.push([x,y,Math.hypot(x+w/2-tx,y+h/2-ty)]);
    C.sort((a,b)=>a[2]-b[2]);let nF=0,nD=0;
    for(const [x,y] of C){const r=[x,y,x+w,y+h],fr=hd==='S'?[x,y+h,x+w,y+h+30]:[x+w,y,x+w+30,y+h];
     if(FORB.some(f=>ov(r,f[0],f[1]))||FORB.some(f=>f[1]>0&&ov(fr,f[0],0))){nF++;continue}
     const c=s15kObb(x+w/2,y+h/2,hd==='S'?PI/2:0,h+6,w+6);c.R=Math.hypot(c.hx,c.hy);const [g,wh]=gapAll(c,null);if(g<3){nD++;continue}
     done={id:vid,t,serves,home:aid,rect:r.map(Math.round),h:hd,gap:+(g/10).toFixed(2),near:wh,dist:Math.round(Math.hypot(x+w/2-tx,y+h/2-ty))};break}
    if(done)break;why.push(aid+'/'+hd+': '+C.length+' מקומות, '+nF+' על דרך / חניה, '+nD+' נוגעים ברכב / מטוס')}
   if(done)break}
  if(done){o.placed.push(done);FORB.push([done.rect,6,'חדש '+vid]);const c=s15kObb((done.rect[0]+done.rect[2])/2,(done.rect[1]+done.rect[3])/2,done.h==='S'?PI/2:0,done.h==='S'?dm[1]:dm[0],done.h==='S'?dm[0]:dm[1]);add(c,vid,'new');const nb=boxes[boxes.length-1];if(nb&&nb.id===vid)put(nb)}
  else o.failed.push({id:vid,t,why})}
 o.ms=Math.round(performance.now()-t0);o.N=N;o.T=T;o.areas=Object.fromEntries(Object.entries(AREA).map(([k,v])=>[k,v]));o.spots=Object.fromEntries(Object.entries(D.spots).map(([k,v])=>[k,{t:v.t,home:v.home,rect:v.rect,h:v.h}]));
}catch(e){o.err=String(e&&e.stack||e).slice(0,600)}return o})()
