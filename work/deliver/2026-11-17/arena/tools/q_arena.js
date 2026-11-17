// q_arena.js — בדיקה חוסמת (arena 17.11): מופעי המחצית באצטדיון (024b / SPORT2.HT) — לפחות 4, מתחלפים בין משחקי הליגה, כל מופע מצויר בכל
// רגע של המחצית בלי שגיאה (ציור אמיתי של a3Live לקנבס צדדי), המסלולים על הדשא ובחזרה למנהרה, הכרטיס ב-F9 והשורה בדף האצטדיון (F).
// הרצה: node W/qa_tools/probe_c2.js <build> q_arena.js <out.json>
return (async()=>{const why=[],bad=w=>why.push(w),R={};
 try{R.audit=TCARENA.audit();if(!R.audit.ok)bad('audit: '+R.audit.why.join(' | '))}catch(e){bad('audit: '+e.message)}
 const cv=document.createElement('canvas');cv.width=1280;cv.height=800;const c=cv.getContext('2d');
 const n=SPORT2.HT.L.length;R.shows=[];
 for(let k=0;k<n;k++){const r=SPORT2.dev.half(k),idx=r.idx;let draws=0,people=0,err=null,names=new Set();
  for(let s=0;s<=16;s+=.5){const u=194+s;c.setTransform(4,0,0,4,-(625-160)*4,-(2205-100)*4);const Q=[];try{SPORT2.a3Live(c,Q,idx,u,2);Q.sort((a,b)=>a[0]-b[0]);for(const q of Q)q[1]();draws+=Q.length}catch(e){err=err||String(e.message)}
   const I=SPORT2.a3Info(idx,u);if(I.ht)names.add(I.ht.id);if(s===7)people=Q.length}
  const e2=SPORT2.err();if(err||e2)bad('מופע '+k+': '+(err||e2));if(names.size!==1||![...names][0])bad('מופע '+k+': a3Info.ht '+[...names].join(','));
  R.shows.push({k,id:r.k,name:r.name,draws,itemsAt7:people});if(people<10)bad('מופע '+k+': מעט מדי בציור באמצע המופע ('+people+')')}
 if(n<4)bad('פחות מ-4 מופעים');
 const ids=[];for(let d=2;d<2+3*8;d+=3)ids.push(SPORT2.HT.pick({sb:d}).id);R.rotate=ids;if(new Set(ids.slice(0,4)).size<4)bad('4 משחקים רצופים בלי 4 מופעים שונים: '+ids.join(','));
 try{if(!PERF.hud)perfHudToggle();tcF9Show('events');const cd=TCF9.el.querySelector('[data-arena-card]');R.f9=cd?cd.querySelectorAll('button[data-arena]').length:0;if(R.f9<n)bad('F9: '+R.f9+' כפתורים');perfHudToggle()}catch(e){bad('F9: '+e.message)}
 try{const h=plcStadium();R.plc=/מופע המחצית/.test(h);if(!R.plc)bad('הדף של האצטדיון בלי מופע המחצית')}catch(e){bad('plc: '+e.message)}
 R.err=TCARENA.err()||SPORT2.err()||null;if(R.err)bad('err: '+R.err);
 return Object.assign({ok:!why.length,why:why.slice(0,12)},R)})()
