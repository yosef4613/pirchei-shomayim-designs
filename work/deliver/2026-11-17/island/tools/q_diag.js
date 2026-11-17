// שאילתה (עם ‎?l5on‎): למה נכשלות d5_wash_inside_depot ו-parked_cars_exactly_inside_marked_stalls_citywide כשקו 5א בשירות — הרכבים שלא בתוך המקום שלהם, החפיפות בחניון, ומצב הקואצ׳ים
return (()=>{const R={l5:{on:L5R.on,why:L5R.why,run:ISL5A.run},bad:[],coaches:[]};
 try{const P=baseParkedCars().filter(o=>o.slotRect);for(const o of P){const info=parkedCarInfo(o).info,turn=Math.abs(Math.round((o.heading||0)/(Math.PI/2)))%2,d=turn?{w:info.fp[3],h:info.fp[2]}:{w:info.fp[2],h:info.fp[3]},m=1.5,r=o.slotRect;
  const ok=d.w<=r.w+m&&d.h<=r.h+m&&o.x>=r.x+d.w/2-m&&o.x<=r.x+r.w-d.w/2+m&&o.y>=r.y+d.h/2-m&&o.y<=r.y+r.h-d.h/2+m;if(!ok)R.bad.push([o.id,Math.round(o.x),Math.round(o.y),+(o.heading||0).toFixed(2),[r.x,r.y,r.w,r.h].map(Math.round),[d.w,d.h].map(v=>+v.toFixed(1)),o.depot||''])}}catch(e){R.badErr=String(e)}
 try{const W=d5WashAudit();R.d5={ok:W.ok,hits:W.hits,n:W.n}}catch(e){R.d5Err=String(e)}
 try{for(const [id] of LN5.fleet){const p=PARKED_CARS.find(q=>q.id===id),b=(LN.bus||[]).find(q=>q.id===id||q.v&&q.v.id===id);R.coaches.push([id,p?[Math.round(p.x),Math.round(p.y),+(p.heading||0).toFixed(2),p.slotRect?[p.slotRect.x,p.slotRect.y].map(Math.round):null]:null,b?(b.ph||'')+'@'+(b.at||'')+'>'+(b.target||''):null])}}catch(e){R.cErr=String(e)}
 try{R.clock=gameClock().hhmm}catch(e){}
 return R})()
