return (async()=>{
 const strip=h=>String(h||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
 const snap=tag=>{const c=gameClock(),L=LEAGUE4.st();let N=null,D=null;try{N=A34PLAY.nextMatch();D=N&&A34PLAY.dateOf(N.day)}catch(e){}
  let ph='';try{ph=strip(PHONE_VIEWS.news()).slice(0,260)}catch(e){ph='ERR '+e.message}
  let pm=null;try{pm=plcNextMatch()}catch(e){}
  return {tag,day:c.day,hhmm:c.hhmm,season:L.season,round:L.round,lastDay:L.lastDay,res:L.res.map(r=>r&&r.day),sign:LEAGUE4.signLine(),next:N&&{day:N.day,wd:D&&D.wd,dm:D&&D.dm},plc:pm,phone:ph,err:LEAGUE4.err()}};
 const out=[snap('start')];
 const step=async m=>{G84_CLOCK.base+=m;LEAGUE4.tick();await new Promise(r=>setTimeout(r,30))};
 for(let i=0;i<8*48;i++){await step(30);const c=gameClock();if(c.hour===12&&c.minute<30||c.hour===23&&c.minute>=30)out.push(snap('t'))}
 return out})()
