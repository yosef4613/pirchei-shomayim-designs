#!/usr/bin/env python3
# fc_amph_refactor.py — fieldcalc 17.11: 074zm (AMPH) → מפעל של מופעים amphMake(CFG) (כלל 19א — אותו מנגנון, בלי מנגנון חדש). בלי CFG — בדיוק כמו היום
# (כל ההחלפות הן "CFG.X || הערך של היום"). שימוש: python3 fc_amph_refactor.py <074zm_amph_water.js>
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, ('נמצא %d פעמים' % s.count(a), a[:90])
    s = s.replace(a, b)
rep("var AMPH=(function(){'use strict';", "function amphMake(CFG){'use strict';CFG=CFG||{};   /* fieldcalc 17.11: מופע לפי תצורה (בלי CFG — המטוס של G6 / H6 כמו קודם) */")
rep("const RWY={y:4650,x0:7300,x1:9400,half:150,td:8500,stop:7850,lineup:7400,lift:8400};", "const RWY=CFG.RWY||{y:4650,x0:7300,x1:9400,half:150,td:8500,stop:7850,lineup:7400,lift:8400};")
rep("const DECK=[6230,4000,6300,4060],MOOR=[6318,4062,PI/2],H1=[6540,4350],H2=[7000,4350];", "const DECK=CFG.DECK||[6230,4000,6300,4060],MOOR=CFG.MOOR||[6318,4062,PI/2],H1=CFG.H1||[6540,4350],H2=CFG.H2||[7000,4350];")
# המסלולים: כל אחד — מהתצורה, אם יש
i = s.index("const TAXI_OUT=[[6318,4062]"); j = s.index(";", s.index("TAXI_LU=", i)) + 1
seg = s[i:j]
seg2 = seg.replace("const TAXI_OUT=[", "const TAXI_OUT=CFG.TAXI_OUT||[", 1).replace("CROSS_OUT=[H1,H2]", "CROSS_OUT=CFG.CROSS_OUT||[H1,H2]", 1).replace("TAXI_LU=[H2", "TAXI_LU=CFG.TAXI_LU||[H2", 1)
s = s[:i] + seg2 + s[j:]
i = s.index("const TAXI_IN1=[[RWY.stop,RWY.y]"); j = s.index(";", s.index("TAXI_IN2=", i)) + 1
seg = s[i:j]
seg2 = seg.replace("const TAXI_IN1=[", "const TAXI_IN1=CFG.TAXI_IN1||[", 1).replace("CROSS_IN=[H2,H1]", "CROSS_IN=CFG.CROSS_IN||[H2,H1]", 1).replace("TAXI_IN2=[H1", "TAXI_IN2=CFG.TAXI_IN2||[H1", 1)
s = s[:i] + seg2 + s[j:]
rep("const FLIGHT=[[RWY.lift,4650,0]", "const FLIGHT=CFG.FLIGHT||[[RWY.lift,4650,0]")
rep("const FINAL_AT=[11460,4975];", "const FINAL_AT=CFG.FINAL_AT||[11460,4975];")
rep("const ORBIT_R=380;", "const ORBIT_R=CFG.ORBIT_R||380;")
rep("const SPOT={wait:[6246,4046],watch:[6252,4012],side:[6292,4054],pilot:[6286,4040]};", "const SPOT=CFG.SPOT||{wait:[6246,4046],watch:[6252,4012],side:[6292,4054],pilot:[6286,4040]};")
rep("const WALK=[[6330,3256],[6262,3250],[6216,3262],[6216,3700],[6216,4030],SPOT.wait];", "const WALK=CFG.WALK||[[6330,3256],[6262,3250],[6216,3262],[6216,3700],[6216,4030],SPOT.wait];")
rep("const TOURS=[480,630,780,930];", "const TOURS=CFG.TOURS||[480,630,780,930];")
rep("const ZONES={cross:[6470,4230,7070,4470],rwy:[7240,4470,9460,4830]};", "const ZONES=CFG.ZONES||{cross:[6470,4230,7070,4470],rwy:[7240,4470,9460,4830]};")
# בלי אנשים (מופע של השדה — כמו מטוסי ה-GA של S15): הטייס במטוס, בלי הליכה
rep("function people(s,d){const I=itins(d),o=[],inPlane={pil:false,pax:null};", "function people(s,d){if(CFG.noPeople)return{o:[],inPlane:{pil:true,pax:null}};const I=itins(d),o=[],inPlane={pil:false,pax:null};")
rep("push('amph_people',!pb.length,", "if(CFG.noPeople)pb.length=0;push('amph_people',!pb.length,CFG.noPeople?'בלי אנשים במופע הזה (הטייס במטוס, כמו מטוסי ה-GA של S15)':")
rep("push('amph_tours',s1.length===4&&", "push('amph_tours',s1.length===TOURS.length&&")
# המצלמה של הרגעים — מהתצורה, אם יש
rep("   setClockS(s);ST.follow=fol;cam(x,y,z);return msg}", "   if(CFG.CAM&&CFG.CAM[k]){const q=CFG.CAM[k];x=q[0];y=q[1];z=q[2];if(q[3])msg=q[3]}setClockS(s);ST.follow=fol;cam(x,y,z);return msg}")
rep("return{AC,L,WS,RWY,DECK,MOOR,H1,H2,G,ZONES,TOURS,", "return{CFG,AC,L,WS,RWY,DECK,MOOR,H1,H2,G,ZONES,TOURS,")
rep("})();\n/* ---- החיבורים", "}\nvar AMPH=amphMake();\n/* ---- החיבורים")
open(p, 'w', encoding='utf-8').write(s)
print('ok', p, len(s.encode('utf-8')))
