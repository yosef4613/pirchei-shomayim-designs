for(let i=0;i<8;i++){const h=i/8*Math.PI*2;const e=ZD.car('#2f6fd0',h,40,1);dr(e,120+i*180,150,1);const n=G2.car.sprite('VH-SD-02','#2f6fd0',h,40*4.85/4.85,1,16);dr(n,120+i*180,330,1)}
for(let i=0;i<8;i++){const h=i/8*Math.PI*2;const e=ZD.ped(G2.ped.LOOKS[i%6],'walk',h,.25,60,1);dr(e,120+i*180,560,1);const n=G2.ped.sprite(i%6,'walk',h,.25,60,1,16);dr(n,120+i*180,760,1)}
