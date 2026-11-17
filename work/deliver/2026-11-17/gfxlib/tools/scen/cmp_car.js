c34LibInit();const sc=C34.len('VH-SD-02')/G2.car.len('VH-SD-02');
[0.39,2.75,4.32,5.9].forEach((h,i)=>{const Z=6;const o=C34.sprite('VH-SD-02','#2f6fd0',h,Z,16);g.save();g.translate(220+i*390,230);g.scale(Z,Z);g.drawImage(o.cv,-o.ox/Z,-o.oy/Z,o.cv.width/Z,o.cv.height/Z);try{C34.wheels(g,'VH-SD-02',0,0,o.k,16,0,-1,1)}catch(e){console.log(e.message)}g.restore();
 const e=G2.car.sprite('VH-SD-02','#2f6fd0',h,sc*Z,1,16,1.25);dr(e,220+i*390,560,1);const e2=G2.car.sprite('VH-SD-02','#2f6fd0',h,sc*Z,1,16,1);dr(e2,220+i*390,830,1)});
