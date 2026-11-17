// הבדיקה של הפעולות: כל שלב בטבלה (__TC_SACT.check) + הטבלה "כמה הוסבו מתוך כמה" + שגיאות המנוע + מי כאן (הדמויות — לא על נתיב נסיעה)
return (()=>{const A=window.__TC_SACT;if(!A)return{ok:false,err:'אין __TC_SACT'};const c=A.check(),t=A.table();
 let z=null;try{z=ZSTORY.check?ZSTORY.check():null}catch(e){z={err:String(e)}}
 let who=null;try{who=A.who?A.who():null}catch(e){who={err:String(e)}}
 const whoBad=Array.isArray(who)?who.filter(w=>w.road):[];
 let fig=null;try{fig=A.figCheck?A.figCheck():null}catch(e){fig={ok:false,bad:[String(e)]}}
 let vis=null;try{vis=A.visCheck?A.visCheck():null}catch(e){vis={ok:false,bad:[String(e)]}}
 return{ok:c.ok&&!whoBad.length&&(!vis||!!vis.ok)&&(!fig||!!fig.ok),vis,fig,n:c.n,kinds:c.kinds,bad:c.bad.slice(0,40),err:c.err,sameStory:c.sameStory,sameMoney:c.sameMoney,table:{stories:t.stories,steps:t.steps,plain:t.plain,converted:t.converted,left:t.left,storiesWithoutAction:t.storiesWithoutAction,storiesWithoutActionNow:t.storiesWithoutActionNow,waitConverted:t.waitConverted},waitChecked:c.wait||0,place:c.place||null,lookT:c.lookT||null,span:c.span||null,layer:c.layer||null,rows:t.rows,engineErr:A.err(),zs:z&&{ok:z.ok,bad:(z.bad||[]).slice(0,10),err:z.err},who,whoBad}})()
