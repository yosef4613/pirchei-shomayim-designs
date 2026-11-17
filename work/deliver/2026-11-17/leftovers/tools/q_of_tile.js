// q_of_tile.js (leftovers 17.11) — האריח "סרטון הפתיחה" במסך הפתיחה (074zf9:tcofBtn של loading → TCOF.play('home')), בתוך הדף ובלי page.click של playwright
// (ב-tcofb של loading הלחיצה נתקעה 30 שנ׳: התהליכון הראשי חסום ~13 שנ׳ בחימום הצילומים החיים של הסרטון — q_of_diag). ‎#dev → __TCO.open → האריח → לחיצה → הסרטון מעל מסך הפתיחה → Esc → הבית והפוקוס → שוב → Enter מדלג בלי להיכנס למשחק.
return new Promise(res=>{const W=ms=>new Promise(r=>setTimeout(r,ms));const o={c:{}};const ck=(k,v,d)=>{o.c[k]={ok:!!v,d}};const key=k=>window.dispatchEvent(new KeyboardEvent('keydown',{key:k,code:k,bubbles:true,cancelable:true}));
 const until=async(f,ms)=>{const t=performance.now();while(performance.now()-t<ms){let v=false;try{v=f()}catch(e){}if(v)return Math.round(performance.now()-t);await W(250)}return -1};
 (async()=>{try{
 __TCO.open('tile');const q=()=>document.querySelector('#tcoRoot [data-act="tcofHome"]');const tb=await until(q,20000);let b=q();
 ck('tile',b&&/סרטון הפתיחה/.test(b.innerText)&&b.querySelectorAll('svg').length===1&&b.querySelectorAll('img').length===0&&TCO.mode==='open',{ms:tb,txt:b&&b.innerText,mode:TCO.mode});
 if(!b){res(o);return}
 b.focus();setTimeout(()=>b.click(),0);const t1=await until(()=>TCSHOW.on,60000);
 ck('click_plays_over_opening',t1>=0&&TCSHOW.on.full&&TCSHOW.on.prod.id==='tc-opening'&&TCO.mode==='open'&&__TC_TCOFB().plays===1,{ms:t1,mode:TCO.mode,fb:__TC_TCOFB()});
 ck('tcbusy_opening',TCBUSY.top()==='opening'&&TCBUSY.blocks('card')&&TCBUSY.blocks('tutorial'),{top:TCBUSY.top()});
 await W(8000);let s=TCSHOW.stats();ck('runs',TCSHOW.on&&s.frames>30&&TCSHOW.on.t>0.5,{t:TCSHOW.on&&+TCSHOW.on.t.toFixed(2),frames:s.frames,p95:s.p95,max:s.max});
 key('Escape');const t2=await until(()=>!TCSHOW.on,15000);await W(800);b=q();const top=TCO.stack[TCO.stack.length-1];
 ck('esc_back_home',t2>=0&&TCO.mode==='open'&&top&&top.screen==='home'&&!!b,{ms:t2,mode:TCO.mode,scr:top&&top.screen,last:TCOF.st.last});
 ck('focus_on_tile',document.activeElement&&document.activeElement.dataset.act==='tcofHome',document.activeElement&&document.activeElement.dataset.act);
 if(b){setTimeout(()=>b.click(),0);const t3=await until(()=>TCSHOW.on,60000);ck('again_plays',t3>=0&&__TC_TCOFB().plays===2,{ms:t3,plays:__TC_TCOFB().plays});
  await W(1500);key('Enter');const t4=await until(()=>!TCSHOW.on,15000);await W(800);const tp=TCO.stack[TCO.stack.length-1];
  ck('enter_skips_stays_open',t4>=0&&TCO.mode==='open'&&tp&&tp.screen==='home',{ms:t4,mode:TCO.mode,scr:tp&&tp.screen,last:TCOF.st.last})}
 ck('busy_cleared',!TCBUSY.is('opening'),{top:TCBUSY.top()});
 ck('no_errors',!TCOF.st.err&&!__TC_TCOFB().err&&!(TCSHOW.ST&&TCSHOW.ST.err),{of:TCOF.st.err,fb:__TC_TCOFB().err,show:TCSHOW.ST&&TCSHOW.ST.err});
 o.ok=Object.values(o.c).every(x=>x.ok);o.pass=Object.values(o.c).filter(x=>x.ok).length+'/'+Object.keys(o.c).length;
}catch(e){o.err=String(e&&e.stack||e).slice(0,400)}res(o)})()})
