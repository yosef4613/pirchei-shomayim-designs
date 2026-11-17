const m=G2.car.model('VH-SD-02');const gl=m.polys.filter(q=>q.m==='glass'&&q.two);
console.log('panes',gl.length, gl.map(q=>q.P.length+':'+G2.polyNormal(q.P).map(v=>v.toFixed(2)).join(',')).join(' | '));
const P=m.polys.map(q=>q.m==='glass'&&q.two?Object.assign({},q,{c:'#ff0000',m:'matte',a:1}):(q.c==='__PAINT__'?Object.assign({},q,{c:'#2f6fd0'}):q));
const e=G2.render(P,.39,140,1,{});dr(e,400,450,1);
