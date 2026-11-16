'use strict';
const STORE='pirchei_shomayim_design_feedback_v1';
const $=id=>document.getElementById(id);
const questions=[...document.querySelectorAll('fieldset[data-question]')];
const sections=[...document.querySelectorAll('section[data-section]')];
const inputs=()=>[...document.querySelectorAll('#questions input[name],#questions textarea[name]')];
const key=el=>(el.type==='checkbox'||el.type==='radio')?el.name+'::'+el.value:el.name;
const isChoice=el=>el.type==='checkbox'||el.type==='radio';
let storageAvailable=true;
function storageNotice(){
 $('storage-state').textContent=storageAvailable?'התשובות נשמרות בדפדפן באותו מכשיר. הן אינן נשלחות אוטומטית.':'הדפדפן אינו מאפשר שמירה מקומית כרגע. אפשר למלא, אבל לפני הסגירה צריך להעתיק או להוריד את התשובות.';
}
function persist(){
 try{
  const values={};
  for(const el of inputs())values[key(el)]=isChoice(el)?el.checked:el.value;
  values._recipient=$('recipient').value;
  localStorage.setItem(STORE,JSON.stringify(values));
  storageAvailable=true;
 }catch{storageAvailable=false}
 storageNotice();
}
function restore(){
 try{
  const values=JSON.parse(localStorage.getItem(STORE)||'{}');
  if(values&&typeof values==='object'){
   for(const el of inputs()){
    const value=values[key(el)];
    if(isChoice(el))el.checked=value===true;
    else if(typeof value==='string')el.value=value;
   }
   if(typeof values._recipient==='string')$('recipient').value=values._recipient;
  }
 }catch{storageAvailable=false}
 storageNotice();
}
function answer(question){
 const selected=[...question.querySelectorAll('input:checked')].map(el=>el.value);
 const parts=selected.length?['בחירות: '+selected.join(' | ')]:[];
 for(const area of question.querySelectorAll('textarea.free')){
  const value=area.value.trim();
  if(value)parts.push(area.dataset.summaryLabel+':\n'+value);
 }
 return parts.join('\n\n');
}
function build(){
 const answered=questions.filter(q=>answer(q)).length;
 const date=new Date().toLocaleDateString('he-IL',{timeZone:'Asia/Jerusalem'});
 const lines=['משוב על חמש הדוגמאות וחומרים לאתר — פרחי שמיים','מולא בתאריך: '+date,`נענו ${answered} מתוך ${questions.length} שאלות`,'קישור לדוגמאות: https://yosef4613.github.io/pirchei-shomayim-designs/',''];
 for(const section of sections){
  lines.push('━━━━━━━━━━━━━━━━━━━━━━━━',section.querySelector('h2').textContent,'━━━━━━━━━━━━━━━━━━━━━━━━');
  for(const question of section.querySelectorAll('fieldset[data-question]')){
   lines.push(question.dataset.number+'. '+question.querySelector('.qtitle').textContent,answer(question)||'לא נענה','');
  }
 }
 lines.push('סוף המשוב');
 return {text:lines.join('\n'),answered};
}
function update(){
 const result=build();
 $('summary').value=result.text;
 $('count').replaceChildren(document.createTextNode(result.answered+' '));
 const suffix=document.createElement('span');suffix.textContent='מתוך '+questions.length+' שאלות';$('count').append(suffix);
 $('mcount').textContent=`${result.answered} מתוך ${questions.length} שאלות נענו`;
 $('bar').style.width=$('mbar').style.width=(result.answered/questions.length*100)+'%';
 $('bar').parentElement.setAttribute('aria-valuenow',String(result.answered));
 sections.forEach((section,i)=>{
  const local=[...section.querySelectorAll('fieldset[data-question]')];
  $('n'+i).textContent=local.filter(q=>answer(q)).length+'/'+local.length;
 });
}
function notice(message,error=false){$('status').textContent=message;$('status').classList.toggle('warning',error)}
async function copy(){
 const text=$('summary').value;
 try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return true}}catch{}
 const temporary=document.createElement('textarea');temporary.value=text;temporary.style.cssText='position:fixed;top:-9999px;opacity:0';temporary.setAttribute('aria-hidden','true');
 document.body.append(temporary);temporary.focus();temporary.select();let ok=false;
 try{ok=document.execCommand('copy')}catch{}
 temporary.remove();return ok;
}
function manualCopy(){
 $('summary').focus();$('summary').select();
 notice('לא התאפשרה העתקה אוטומטית. הסיכום סומן — אפשר להעתיק אותו ידנית ולשלוח במייל.',true);
}
function resize(area){area.style.height='auto';area.style.height=Math.max(area.closest('.review-fields')?125:100,area.scrollHeight+2)+'px'}
restore();update();
for(const area of document.querySelectorAll('textarea.free')){
 if(area.value)resize(area);
 area.addEventListener('input',()=>resize(area));
}
const change=()=>{persist();update()};
$('questions').addEventListener('input',change);
$('questions').addEventListener('change',change);
$('recipient').addEventListener('input',persist);
$('copy').addEventListener('click',async()=>{update();if(await copy())notice('כל התשובות הועתקו. אפשר להדביק אותן במייל ולצרף חומרים.');else manualCopy()});
$('mail').addEventListener('click',async()=>{
 const recipient=$('recipient');
 if(recipient.value.trim()&&!recipient.checkValidity()){notice('כתובת המייל אינה תקינה. אפשר לתקן אותה או להשאיר את השדה ריק.',true);recipient.focus();return}
 update();
 if(!await copy()){manualCopy();return}
 notice('התשובות הועתקו. יש להדביק אותן בהודעה שנפתחה, לצרף חומרים לפי הצורך וללחוץ על שליחה.');
 location.href='mailto:'+encodeURIComponent(recipient.value.trim())+'?subject='+encodeURIComponent('משוב על הדוגמאות וחומרים לאתר פרחי שמיים');
});
$('download').addEventListener('click',()=>{
 update();const blob=new Blob(['\uFEFF',$('summary').value],{type:'text/plain;charset=utf-8'});
 const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='משוב_על_הדוגמאות_פרחי_שמיים.txt';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);
 notice('קובץ המשוב נוצר. אפשר לצרף אותו ואת החומרים למייל.');
});
$('clear').addEventListener('click',()=>{
 if(!confirm('לנקות את כל התשובות בשאלון המשוב הזה? לא ניתן לבטל את הפעולה.'))return;
 for(const el of inputs()){if(isChoice(el))el.checked=false;else el.value=''}
 $('recipient').value='';
 try{localStorage.removeItem(STORE)}catch{}
 for(const area of document.querySelectorAll('textarea.free'))area.style.height='';
 update();notice('תשובות המשוב נוקו. שאלון האפיון המקורי לא השתנה.');
});
