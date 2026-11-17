// rails 17.11 — הגאומטריה של ההצעה: מעבר בין שתי מסילות מקבילות בשתי קשתות משיקות (S של שתי קשתות שוות, בלי פינה), לפי רדיוס יעד
// axis 'y' — המסילות אנכיות (x קבוע, y משתנה); axis 'x' — אופקיות.
function s2len(h,R){const c=1-Math.abs(h)/(2*R);if(c<-1)return null;const th=Math.acos(c);return{L:2*R*Math.sin(th),th}}
function s2arc(x0,y0,x1,y1,axis,n=24){// מחזיר נקודות מ-(x0,y0) ל-(x1,y1); שתי קשתות שוות
 const along=axis==='y'?y1-y0:x1-x0,lat=axis==='y'?x1-x0:y1-y0,L=Math.abs(along),h=Math.abs(lat),sa=Math.sign(along)||1,sl=Math.sign(lat)||1;
 const th=2*Math.atan2(h,L),R=L/(2*Math.sin(th));const pts=[];
 for(let i=0;i<=2*n;i++){let a,l;if(i<=n){const t=th*i/n;a=R*Math.sin(t);l=R*(1-Math.cos(t))}else{const t=th*(2*n-i)/n;a=L-R*Math.sin(t);l=h-R*(1-Math.cos(t))}
  pts.push(axis==='y'?[+(x0+sl*l).toFixed(3),+(y0+sa*a).toFixed(3)]:[+(x0+sa*a).toFixed(3),+(y0+sl*l).toFixed(3)])}
 pts[0]=[x0,y0];pts[pts.length-1]=[x1,y1];return{pts,R,th:th*180/Math.PI}}
function frogDeg(R,g=26){return Math.acos(1-g/R)*180/Math.PI}
module.exports={s2len,s2arc,frogDeg};
