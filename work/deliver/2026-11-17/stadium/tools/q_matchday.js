return (async()=>{
 const out=[];let last='';
 const c0=gameClock();G84_CLOCK.base+=(2-c0.day)*1440+(19*60-c0.min);   // day 2, 19:00
 for(let i=0;i<300;i++){G84_CLOCK.base+=1;LEAGUE4.tick();let I={};try{I=A34PLAY.matchInfo()}catch(e){}const L=LEAGUE4.st(),M=A34PLAY.matchNow();let S=null;try{S=M&&SPORT2.a3Sess(M.idx)}catch(e){}
  const k=[L.round,!!M,I.live,I.on,S&&S.overT,LEAGUE4.signLine(),(A34PLAY.nextMatch()||{}).day].join('|');
  if(k!==last){last=k;const c=gameClock();out.push({t:c.hhmm,u:M&&M.u,round:L.round,live:I.live,on:I.on,g:[I.g1,I.g2],overT:S&&S.overT,dur:S&&S.dur,sign:LEAGUE4.signLine(),next:(A34PLAY.nextMatch()||{}).day,res:L.res[0]&&L.res[0].m.map(m=>m.g.join(':')+(m.st?'*':'')).join(' ')})}
  await new Promise(r=>setTimeout(r,5))}
 return out})()
