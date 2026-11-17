# בדיקה פנימית בעין בלבד: התוכנית מעל המצב הקיים (PIL)
import json,sys,math
sys.path.insert(0,'/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools')
from plan_data import *
from PIL import Image,ImageDraw
C=json.load(open(W+'/deliver/2026-11-17/island/plan_calc.json'))
X0,Y0,X1,Y1,sc=[float(a) for a in sys.argv[2:7]] if len(sys.argv)>6 else (3500,5700,9700,7800,0.29)
im=Image.new('RGB',(int((X1-X0)*sc),int((Y1-Y0)*sc)),(140,195,232)); d=ImageDraw.Draw(im)
T=lambda p:((p[0]-X0)*sc,(p[1]-Y0)*sc)
def poly(pts,fill=None,outline=None): d.polygon([T(p) for p in pts],fill=fill,outline=outline)
def line(pts,c,w=1): d.line([T(p) for p in pts],fill=c,width=max(1,int(w)))
def rect(r,fill=None,outline=None): d.rectangle([T(r[:2]),T(r[2:])],fill=fill,outline=outline)
poly(LAND,(196,222,150),(90,120,50))
for c in S13['contours']: line(c+[c[0]],(170,160,110))
poly(MARINA_BASIN,(120,180,225))
for b in BREAKWATER: line(b,(90,90,90),4)
for p in PONTOONS: rect(p,(230,230,220))
for l in (LANE_MAIN,LANE_FERRY,LANE_MARINA,LANE_RIG): line(l,(20,60,170),2)
poly(LIFT,(240,192,64)); rect(RIG,(224,80,80)); line(PIPE,(120,60,10),1)
rect(SUPPLY_PIER,(150,150,150))
for r in ROADS:
    col={'bridge':(30,30,30),'collector':(60,60,60),'loop':(200,90,20),'local':(100,100,100),'track':(150,120,80)}[r['cls']]
    line(r['pts'],col,int(88*sc) if r['cls'] in('collector','bridge','loop') else 3)
for p in PLACES: rect(p['rect'],None,(120,40,160))
line(RAIL_A,(110,60,20),2); line(RAIL_B,(110,60,20),2)
poly(TRUCK_YARD,None,(110,60,20)); poly(LOAD_PLAT,(200,200,200))
for q in PARKING: rect(q['rect'],(205,210,215),(60,70,90))
for r in ROADS:
    if r['cls']=='loop':
        for a,b in zip(r['pts'],r['pts'][1:]):
            mx,my=T(((a[0]+b[0])/2,(a[1]+b[1])/2)); dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy) or 1; ux,uy=dx/L,dy/L
            d.polygon([(mx+ux*8,my+uy*8),(mx-ux*6-uy*6,my-uy*6+ux*6),(mx-ux*6+uy*6,my-uy*6-ux*6)],fill=(255,255,255))
line(CABLE,(220,0,0),2)
for s in C['stops']:
    x,y=T(s['at']); col=(0,120,255) if s['line']=='5' else (0,170,90)
    d.ellipse([x-5,y-5,x+5,y+5],fill=col,outline=(0,0,0))
cols=[0,1200,2400,3600,4800,6000,7200,8400,9600]; rows=[-850,0,850,1700,2550,3400,4250,5200,6050,6900,7750]
for x in cols: line([(x,Y0),(x,Y1)],(0,0,0),1)
for y in rows: line([(X0,y),(X1,y)],(0,0,0),1)
for ci,x in enumerate(cols[:-1]):
    for ri,y in enumerate(rows[:-1]):
        if X0<=x+10<=X1 and Y0<=y+10<=Y1: d.text(T((x+15,y+15)),"ABCDEFGH"[ci]+str(ri),fill=(0,0,0))
im.save(sys.argv[1])
