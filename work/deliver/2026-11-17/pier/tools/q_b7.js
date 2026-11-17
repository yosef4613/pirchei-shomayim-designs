return (async()=>{const o={};const col=(x,y0,y1)=>{const r=[];let last=null;for(let y=y0;y<=y1;y+=2){let b=null;try{b=personBlockedAt(x,y)}catch(e){b='ERR'}b=b||'ok';let w='';try{w=WATERWALK.isWater(x,y)?'w':'l'}catch(e){}b=b+'/'+w;if(b!==last){r.push(y+':'+b);last=b}}return r.join(' | ')};
 for(const x of[1895,2105,2115,2125])o['x'+x]=col(x,4850,5060);
 const row=(y,x0,x1)=>{const r=[];let last=null;for(let x=x0;x<=x1;x+=2){let b=personBlockedAt(x,y)||'ok';if(b!==last){r.push(x+':'+b);last=b}}return r.join(' | ')};
 o.row4990=row(4990,2000,2250);o.row4970=row(4970,2000,2250);o.row4940=row(4940,2000,2250);
 o.decks=WATERWALK.decks().filter(d=>/B7/.test(d.id)).map(d=>d.id+':'+d.r.join(','));o.roots=o.decks.length;try{o.r2=PIERX.roots([2100,5000,2130,5420]);o.r1=PIERX.roots([1880,5000,1910,5420])}catch(e){}
 return o})()
