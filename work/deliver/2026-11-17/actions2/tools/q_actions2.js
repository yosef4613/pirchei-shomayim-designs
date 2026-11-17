// actions2 — הבדיקה בתוך המשחק: 140 הפעולות + 8 ההגעות (check: בלי הפעלה לא זז; F → הרצף, הליכה ותנוחה, ורק אז התקדמות), שלבי הכרטיס (plainCheck),
// הסיפור הראשי (msCheck: שיחה / עבודה / סרט — לא נפתחים כשעוצרים ליד, F → הרצף → נפתח), התנוחות בצייר (poseCheck), הדמות האחת, הביקור, הטבלה, ZSTORY
return (()=>{const A=window.__TC_SACT;if(!A)return{ok:false,err:'אין __TC_SACT'};const t0=performance.now();const c=A.check(),t=A.table();
 let z=null;try{z=ZSTORY.check?ZSTORY.check():null}catch(e){z={err:String(e)}}
 let who=null;try{who=A.who?A.who():null}catch(e){who={err:String(e)}}const whoBad=Array.isArray(who)?who.filter(w=>w.road):[];
 const S=f=>{try{return f()}catch(e){return{ok:false,bad:[String(e&&e.message||e).slice(0,160)]}}};
 const fig=S(()=>A.figCheck()),vis=S(()=>A.visCheck()),plain=S(()=>A.plainCheck()),ms=S(()=>A.msCheck()),pose=S(()=>A.poseCheck());
 const ok=c.ok&&!whoBad.length&&!!vis.ok&&!!fig.ok&&!!plain.ok&&!!ms.ok&&!!pose.ok;
 return{ok,ms_total:Math.round(performance.now()-t0),n:c.n,noAuto:c.noAuto,anim:c.anim,kinds:c.kinds,bad:c.bad.slice(0,40),err:c.err,sameStory:c.sameStory,sameMoney:c.sameMoney,drive:c.drive,place:c.place||null,lookT:c.lookT||null,span:c.span||null,layer:c.layer||null,
  plain:{ok:plain.ok,n:plain.n,adv:plain.adv,walk:plain.walk,shake:plain.shake,talk:plain.talk,phone:plain.phone,bad:(plain.bad||[]).slice(0,20)},ms,pose,fig,vis,
  table:{stories:t.stories,steps:t.steps,plain:t.plain,converted:t.converted,left:t.left},engineErr:A.err(),zs:z&&{ok:z.ok,bad:(z.bad||[]).slice(0,10),err:z.err},whoBad,PS:{n:A.PS.n,done:A.PS.done,cancel:A.PS.cancel}}})()
