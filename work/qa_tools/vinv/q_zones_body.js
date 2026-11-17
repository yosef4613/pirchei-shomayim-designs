;(()=>{const T=+(window.__VINV_T||300),RB=new Set(window.__VINV_REBUILT||[]);const R=VINV.check({T});
const zAt=a=>a&&a.length===2?VINV.zone(a[0],a[1]):'-';
const ap=R.appear.map(a=>Object.assign({zone:zAt(a.at)},a)),jp=R.jumps.map(j=>Object.assign({zone:zAt(j.to)},j));
const inR=x=>RB.has(x.zone);
const out={T:R.T,ms:R.ms,vehiclesChecked:R.vehiclesChecked,rebuilt:[...RB],
 rebuiltAppear:ap.filter(inR),rebuiltJumps:jp.filter(inR),rebuiltParked:R.parked.filter(inR),
 oldAppearBySource:{},oldJumps:jp.filter(x=>!inR(x)).length,oldParked:R.parked.filter(x=>!inR(x)).map(p=>p.id+' '+p.zone),
 allowed:R.allowed.map(a=>a.id+' — '+a.why),handoff:R.handoff.length};
for(const a of ap.filter(x=>!inR(x))){const k=a.src+' · '+a.what+' · '+a.zone;out.oldAppearBySource[k]=(out.oldAppearBySource[k]||0)+1}
out.ok=!out.rebuiltAppear.length&&!out.rebuiltJumps.length&&!out.rebuiltParked.length;return JSON.stringify(out)})()
