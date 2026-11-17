// שאילתה: צומת האי (IL) — מרומזר במקום הכיכר (הבעלים 17.11): ברשימות של הרמזורים, בלי RB2, המעברים, השלב עכשיו, ומה עומד בצומת
return (()=>{const R={};try{R.sig=SIGNAL_NODE_IDS.has('IL');R.rb=!!RB2.IL;R.signals=SIGNALS.filter(s=>s.node==='IL').map(s=>s.id+':'+s.crosswalkIds.length);
 R.xw=CROSSWALKS.filter(c=>c.signalNode==='IL').map(c=>[c.id,Math.round(c.x),Math.round(c.y)]);R.zeb=ZEBRA_XW.filter(z=>z.node==='IL'||(z.rb&&z.node==='IL')).length;
 try{const p=TrafficSignalController.currentFor('IL');R.phase=p?JSON.stringify(p).slice(0,200):null}catch(e){R.phaseErr=String(e).slice(0,100)}
 try{const n=NODES2.get('IL');R.n2={rb:!!(n&&n.rb),moves:n?(n.movements||[]).length:null,inside:n&&n.inside?n.inside.length:null,waiting:n&&n.waiting?n.waiting.length:null}}catch(e){R.n2Err=String(e).slice(0,100)}
 R.near=TRAFFIC_CARS.filter(v=>Math.hypot(v.x-8330,v.y-7320)<400).map(v=>[v.id,Math.round(v.x),Math.round(v.y),+(v.speed||0).toFixed(1),v.edgeId]).slice(0,12);
 try{R.p523=P523.modes.IL+' · '+JSON.stringify(P523.tRule.find(q=>q[0]==='IL'))}catch(e){}
}catch(e){R.err=String(e).slice(0,200)}return R})()
