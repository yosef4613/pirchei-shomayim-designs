// בדיקה: מכל מזח ומשטח מעל המים אפשר להגיע ברגל ליבשה (הצפה על רשת של 6 פיקס׳ עם personBlockedAt)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  await p.goto('file://' + path.resolve(process.argv[2]) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{try{
    const L=[];const add=(id,q)=>{if(q&&q.length===4)L.push({id,q})};
    try{F34_DECKS.forEach((q,i)=>add('F34#'+i,q))}catch(e){}
    try{F56_DECKS.forEach((q,i)=>add('F56#'+i,q))}catch(e){}
    try{B2_FISH_PLATFORMS.forEach(p=>(p.rects||[]).forEach((q,i)=>add(p.id+'#'+i,q)))}catch(e){}
    try{add('B1-BOAT-PIER',B12.boatPier)}catch(e){}
    const water=(x,y)=>{try{if(w3IsSea(x,y))return true}catch(e){}try{if(typeof b2LakeIn==='function'&&b2LakeIn(x,y))return true}catch(e){}return false};
    const bad=[];let n=0;
    for(const d of L){n++;const q=d.q,cx=(q[0]+q[2])/2,cy=(q[1]+q[3])/2,S=6;let sx=cx,sy=cy;
      if(personBlockedAt(sx,sy,3)){let f=false;for(let k=0;k<40&&!f;k++){const x=q[0]+Math.random()*(q[2]-q[0]),y=q[1]+Math.random()*(q[3]-q[1]);if(!personBlockedAt(x,y,3)){sx=x;sy=y;f=true}}if(!f){bad.push(d.id+':אין נקודה פתוחה');continue}}
      const seen=new Set(),Q=[[sx,sy]];let ok=false,steps=0;
      while(Q.length&&steps<9000){const [x,y]=Q.shift();steps++;if(!water(x,y)){ok=true;break}
        for(const [dx,dy] of [[S,0],[-S,0],[0,S],[0,-S]]){const nx=x+dx,ny=y+dy,k=Math.round(nx/S)+','+Math.round(ny/S);if(seen.has(k))continue;seen.add(k);if(Math.abs(nx-cx)>900||Math.abs(ny-cy)>900)continue;if(!personBlockedAt(nx,ny,3))Q.push([nx,ny])}}
      if(!ok)bad.push(d.id+':'+q.map(Math.round).join(','))}
    return JSON.stringify({decks:n,bad})}catch(e){return 'ERR '+e}})()`));
  console.log(r); await b.close();
})();
