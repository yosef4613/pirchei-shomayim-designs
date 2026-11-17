c34LibInit();p34LibInit();const sc=C34.len('VH-SD-02')/G2.car.len('VH-SD-02');
[1,2].forEach((Z,r)=>{for(let i=0;i<8;i++){const h=i/8*Math.PI*2+.39;const o=C34.sprite('VH-SD-02','#d23a3a',h,Z,16);g.save();g.translate(40+i*70*Z,60+r*200);g.scale(Z,Z);g.drawImage(o.cv,-o.ox/Z,-o.oy/Z,o.cv.width/Z,o.cv.height/Z);try{C34.wheels(g,'VH-SD-02',0,0,o.k,16,0,-1,1)}catch(e){}g.restore();
 const e=G2.car.sprite('VH-SD-02','#d23a3a',h,sc*Z,1,16);dr(e,40+i*70*Z,110+r*200,1)}});
