// q_cvchurn.js — perf 17.11: מי יוצר קנבסים בכל פריים (ב-memcmp: ‏S7F300 — 1,140 קנבסים זמניים של "render0" בפתיחה מול מעט ב-S7F299; 67 מ"ב / 1,425 בסוף people_on_road).
// node qa_tools/probe_c2.js <game.html> q_cvchurn.js <out.json> — סופר כל getContext ראשון של קנבס (כל קנבס חדש) לפי הפונקציה והשורה בקובץ, ובכמה בתים:
// (א) 8 שנ׳ של פריימים רגילים; (ב) מעבר ציור אחד על כל העיר כמו people_on_road (60 תצוגות, זום 1.2, render). השורה → החלק: deliver/2026-11-10/perf/runs/pm_<commit>.json.
return (async()=>{const o={};const C={},g0=HTMLCanvasElement.prototype.getContext;let on=null;
 const own=()=>{const L=Error.stackTraceLimit;Error.stackTraceLimit=8;const st=String(new Error().stack).split('\n').slice(2);Error.stackTraceLimit=L;const r=[];
  for(const l of st){if(/getContext|q_cvchurn|__PM/.test(l))continue;const m=l.match(/at (?:new )?(?:([^\s(]+) )?\(?.*?:(\d+):\d+\)?\s*$/);if(m){r.push((m[1]||'(anon)')+':'+m[2]);if(r.length>=3)break}}return r.join(' < ')||'?'};
 HTMLCanvasElement.prototype.getContext=function(){if(on&&!this.__cvc){this.__cvc=1;const k=own(),e=C[on][k]||(C[on][k]=[0,0]);e[0]++;e[1]+=(this.width|0)*(this.height|0)*4}return g0.apply(this,arguments)};
 const top=ph=>Object.entries(C[ph]).sort((a,b)=>b[1][0]-a[1][0]).slice(0,14).map(([k,v])=>[k,v[0],+(v[1]/1048576).toFixed(1)]);
 try{C.idle={};on='idle';const t=performance.now();await new Promise(r=>setTimeout(r,8000));on=null;const s=(performance.now()-t)/1000;
  o.idle={sec:+s.toFixed(1),n:Object.values(C.idle).reduce((a,v)=>a+v[0],0),top:top('idle')};
  C.sweep={};const cam0={x:Camera.x,y:Camera.y,zoom:Camera.zoom},mq=State.mapQa;let views=0;on='sweep';const t1=performance.now();
  try{State.mapQa=true;for(let y=-400;y<7800;y+=900)for(let x=800;x<9700;x+=1600){Camera.x=x;Camera.y=y;Camera.zoom=1.2;try{render(SIM_LOOP.simNow)}catch(e){o.renderErr=o.renderErr||String(e).slice(0,160)}views++}}
  finally{on=null;Camera.x=cam0.x;Camera.y=cam0.y;Camera.zoom=cam0.zoom;State.mapQa=mq}
  o.sweep={views,ms:Math.round(performance.now()-t1),n:Object.values(C.sweep).reduce((a,v)=>a+v[0],0),top:top('sweep')};
 }catch(e){o.err=String(e&&e.stack||e).slice(0,400)}finally{HTMLCanvasElement.prototype.getContext=g0}
 return o})()
