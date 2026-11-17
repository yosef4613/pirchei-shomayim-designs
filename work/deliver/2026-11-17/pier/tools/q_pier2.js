return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={};await S(2500);o.clock=gameClock().hhmm;
 /* שלוש פעמים, בסדר שאלות שונה (התשובה של 074d נשמרת למשבצת לפי הנקודה הראשונה) */
 o.walk=[PIERX.walk()];
 const col=(x,y0,y1,st)=>{const r=[];let last=null;for(let y=y0;y<=y1;y+=st){let b=null;try{b=personBlockedAt(x,y)}catch(e){b='ERR'}b=b||'ok';if(b!==last){r.push(y+':'+b);last=b}}return r.join(' | ')};
 for(const x of[2101,2104,2115,2126,2129,1885,1895,1905,3716])o['x'+x]=col(x,4940,5040,1);
 o.walk.push(PIERX.walk());
 try{const a=WATERWALK.audit(40);o.audit={ok:a.ok,walk:a.walkOnWater,walkEx:a.walkEx,car:a.carOnWater,exitsBad:a.exitsBad,deckBad:a.deckBad,ppl:a.peopleInWater}}catch(e){o.auditErr=String(e).slice(0,200)}
 /* הרצועות שנפתחו: כמה נקודות ים (WATER בלי התיקון) נפתחו לכל משטח */
 try{const L=WATERWALK.decks(),R=PLAYER_PERSON_RADIUS,rows=[];for(const d of L){const q=d.r;let n=0,tot=0;for(let x=q[0]-8;x<=q[2]+8;x+=1)for(let y=q[1]-8;y<=q[3]+8;y+=(y>q[1]+2&&y<q[3]-2?Math.max(1,q[3]-q[1]-6):1)){if(x>=q[0]&&x<=q[2]&&y>=q[1]&&y<=q[3])continue;const w=WATERWALK.water(x,y,true);if(!w)continue;tot++;if(PIERX.inRoot(x,y,R)&&!personBlockedAt(x,y,R))n++}if(n)rows.push(d.id+':'+q.join(',')+' open '+n+'/'+tot)}o.opened=rows}catch(e){o.openedErr=String(e).slice(0,200)}
 o.walk.push(PIERX.walk());o.err=PIERX.err();o.ok=o.walk.every(w=>w.ok)&&!o.err;return o})()
