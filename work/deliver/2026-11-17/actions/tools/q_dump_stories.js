// מלאי: כל סיפורי האזורים (S9STORY.ST) — לכל שלב: המקום, הכותרת, הכפתור, והשדות שיש לו (drive / fix / wait / act / enter / clock / job ...)
return (()=>{const ST=window.__TC_S9STORY.ST,reg=navPoiRegistry(),out=[];
 for(const [id,S] of Object.entries(ST)){const st=[];
  for(let k=0;k<S.steps.length;k++){const s=S.steps[k],keys=Object.keys(s).filter(q=>!['poi','title','text','btn','msg','who','_w','waitText'].includes(q));
   const p=reg[s.poi];st.push({k:k+1,poi:s.poi,title:s.title,btn:s.btn==null?null:String(s.btn),keys,x:p?Math.round(p.x):null,y:p?Math.round(p.y):null,chunk:p?(p.chunk||null):null,text:String(s.text||'').slice(0,240)})}
  out.push({id,zone:S.zone,name:S.name,n:S.steps.length,start:S.start,steps:st})}
 return out})()
