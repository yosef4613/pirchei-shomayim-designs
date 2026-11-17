for(let L=0;L<6;L++){for(let i=0;i<4;i++){const e=G2.ped.sprite(L,'walk',[0,1.57,3.14,4.71][i],i/4+.1,60,1,16);dr(e,80+L*260+i*58,250,1)}
 for(let f=0;f<6;f++){const e=G2.ped.sprite(L,f<3?'walk':'run',L%2?0:1.57,(f%3)/3,60,1,16);dr(e,80+L*260+(f%3)*75,500+(f<3?0:230),1)}}
