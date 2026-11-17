// q_of_diag.js (leftovers 17.11) — למה הלחיצה על האריח "סרטון הפתיחה" במסך הפתיחה נתקעת (tcofb: page.click ‏30 שנ׳): מסך הפתיחה (__TCO.open) → האריח → לחיצה (בתוך הדף, בלי לחכות) → מדידת הפערים של התהליכון הראשי ומשכי הצילומים.
return new Promise(res=>{const W=ms=>new Promise(r=>setTimeout(r,ms));const o={gaps:[],shots:[],lt:[]};(async()=>{try{
 try{new PerformanceObserver(l=>{for(const e of l.getEntries())o.lt.push([Math.round(e.startTime),Math.round(e.duration)])}).observe({entryTypes:['longtask']})}catch(e){o.ltErr=String(e)}
 const wrap=(obj,k,tag)=>{try{const f=obj&&obj[k];if(typeof f!=='function')return;obj[k]=function(){const t=performance.now();try{return f.apply(this,arguments)}finally{const d=performance.now()-t;if(d>40)o.shots.push([tag,Math.round(t),Math.round(d)])}}}catch(e){}};
 try{wrap(TCREAL,'shot','TCREAL.shot');wrap(TCCITY,'grab','TCCITY.grab');wrap(TCCITY,'shot','TCCITY.shot');wrap(TCCITY,'draw','TCCITY.draw')}catch(e){o.wrapErr=String(e)}
 __TCO.open('diag');for(let i=0;i<40;i++){await W(500);if(document.querySelector('#tcoRoot [data-act="tcofHome"]'))break}
 const b=document.querySelector('#tcoRoot [data-act="tcofHome"]');o.mode=TCO.mode;o.btn=!!b;o.fb=window.__TC_TCOFB?__TC_TCOFB():null;
 if(!b){res(o);return}
 let last=performance.now();const iv=setInterval(()=>{const n=performance.now();if(n-last>250)o.gaps.push([Math.round(last),Math.round(n-last)]);last=n},50);
 o.t0=Math.round(performance.now());setTimeout(()=>{const t=performance.now();b.click();o.clickMs=Math.round(performance.now()-t)},0);
 for(let i=0;i<50;i++){await W(500)}clearInterval(iv);
 let st=null;try{st=TCSHOW.stats()}catch(e){st=String(e)}
 o.after={show:!!TCSHOW.on,t:TCSHOW.on?+TCSHOW.on.t.toFixed(2):null,stats:st,of:TCOF.st,mode:TCO.mode,busy:TCBUSY.top(),ld:window.TCLD?TCLD.state().view+'/'+TCLD.state().on:null};
 try{TCSHOW.close(false)}catch(e){}
 o.gaps=o.gaps.slice(0,30);o.shots=o.shots.slice(0,40);o.lt=o.lt.filter(x=>x[0]>=o.t0-100).slice(0,40);
}catch(e){o.err=String(e&&e.stack||e).slice(0,400)}res(o)})()})
