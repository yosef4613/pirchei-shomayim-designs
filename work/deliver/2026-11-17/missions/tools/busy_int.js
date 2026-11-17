// busy_int.js — בדיקת השכבות יחד (TCBUSY + הסצנה + ההדרכה + האירוע + הלוח), על ניסיון בדיקה שמחבר את הענפים. ‎node qa_tools/probe_c2.js <try> busy_int.js <out>
return (()=>{const R={why:[]},B=window.TCBUSY,K=['loading','opening','cutscene','tutorial','event'];if(!B)return JSON.stringify({ok:false,why:['no TCBUSY']});
const g=(f)=>{try{return f()}catch(e){return 'ERR:'+String(e&&e.message||e).slice(0,80)}};
R.init=B.state();R.mx={};
for(const k of K){B.set(k,{why:'int',ttl:5000});const P=B.PRI,row={top:B.top()};
 row.cut=g(()=>__TC_CUT.whyBusy());row.tut=g(()=>__TC_TUT.wait());row.evt=g(()=>typeof evtCut==='function'?evtCut():'none');row.card=B.blocks('card');
 const exp={cut:P[k]>P.cutscene,tut:P[k]>P.tutorial,evt:P[k]>P.event,card:P[k]>P.card};
 if(row.top!==k)R.why.push(k+':top='+row.top);
 if(exp.cut!==/^layer:/.test(String(row.cut)))R.why.push(k+':cut='+row.cut);
 if(typeof row.tut==='string'&&!/^ERR/.test(row.tut)&&exp.tut!==/^busy:/.test(row.tut))R.why.push(k+':tut='+row.tut);
 if(row.evt!=='none'&&exp.evt!==!!row.evt)R.why.push(k+':evt='+row.evt);
 if(exp.card!==row.card)R.why.push(k+':card='+row.card);
 B.clear(k);R.mx[k]=row}
R.after=B.state();if(R.after.on.length)R.why.push('left:'+R.after.on.join(','));
R.qa={};for(const [n,f] of [['mb',()=>{const q=__TC_MB.qa();return{ok:q.ok,why:q.why,busy:q.busy,cut:q.cut}}]])R.qa[n]=g(f);
R.end=B.state();R.ok=!R.why.length;return JSON.stringify(R)})()
