// rails 17.11 — שליפת גוף של פונקציה / הגדרה מקובץ חלק (מאזן סוגריים, מדלג על מחרוזות והערות)
const fs=require('fs'),path=require('path');
function scanEnd(s,i){// i at '{' ; returns index after matching '}'
 let d=0;for(;i<s.length;i++){const c=s[i];
  if(c==='/'&&s[i+1]==='/'){i=s.indexOf('\n',i);if(i<0)return s.length;continue}
  if(c==='/'&&s[i+1]==='*'){i=s.indexOf('*/',i+2)+1;continue}
  if(c==="'"||c==='"'||c==='`'){const q=c;i++;while(i<s.length&&s[i]!==q){if(s[i]==='\\')i++;i++}continue}
  if(c==='{')d++;else if(c==='}'){d--;if(d===0)return i+1}}return -1}
function fnsrc(file,name){const s=fs.readFileSync(file,'utf8');const k=s.indexOf('function '+name+'(');if(k<0)throw new Error('no fn '+name+' in '+file);const b=s.indexOf('{',s.indexOf(')',k));return s.slice(k,scanEnd(s,b))}
function stmt(file,startsWith){const s=fs.readFileSync(file,'utf8');const k=s.indexOf(startsWith);if(k<0)throw new Error('no '+startsWith);let e=s.indexOf('\n',k);return s.slice(k,e<0?s.length:e)}
module.exports={fnsrc,stmt,scanEnd};
