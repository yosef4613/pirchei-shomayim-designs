for(const l of [0,1]){const m=G2.car.model('VH-SD-02',l);console.log('lod',l,'polys',m.polys.length)}
const m=G2.car.model('VH-SD-02',0),P=m.polys.map(q=>q.c==='__PAINT__'?Object.assign({},q,{c:'#d23a3a'}):q);
for(const o of [{shadow:false,flat:true},{flat:true},{shadow:false},{},{}]){let t=performance.now();for(let i=0;i<8;i++)G2.render(P,i*.7,10,1,Object.assign({ao:.35,foot:m.foot},o));console.log(JSON.stringify(o),((performance.now()-t)/8).toFixed(1),'ms')}
