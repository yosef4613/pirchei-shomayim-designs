# ציור PIL של מצב קיים — לבדיקה פנימית בעין בלבד (לא לדף)
import json,re,sys
from PIL import Image,ImageDraw
W='/home/user/tc_root/tc/pkg/work'
P=W+'/src_game_t17_island/parts/'
cp=json.load(open(W+'/study/roads/city_plan.json'))
s=open(P+'019h_S13_data.js').read(); S13=json.loads(re.search(r'const S13D=(\{.*?\});',s,re.S).group(1))
s=open(P+'019j_S14_data.js').read(); i=s.index('var S14D='); j=s.index('};',i); S14=json.loads(s[i+9:j+1])
X0,Y0,X1,Y1=[float(a) for a in sys.argv[2:6]] if len(sys.argv)>5 else (2400,4800,9700,7800)
sc=float(sys.argv[6]) if len(sys.argv)>6 else 0.25
im=Image.new('RGB',(int((X1-X0)*sc),int((Y1-Y0)*sc)),(207,227,176)); d=ImageDraw.Draw(im)
T=lambda p:((p[0]-X0)*sc,(p[1]-Y0)*sc)
def poly(pts,fill=None,outline=None): d.polygon([T(p) for p in pts],fill=fill,outline=outline)
def line(pts,c,w=1): d.line([T(p) for p in pts],fill=c,width=max(1,int(w)))
def rect(r,fill=None,outline=None): d.rectangle([T(r[:2]),T(r[2:])],fill=fill,outline=outline)
poly(cp['terrain']['sea'],(140,195,232))
poly(S13['islandPoly'],(188,217,143),(106,138,58))
for w in S13['water']: poly(w,(140,195,232))
for c in S13['contours']: line(c+[c[0]],(154,138,90))
for g in cp['segments']: line(g['pts'],(70,70,70),3 if g.get('cls') in('arterial','main','avenue') else 2)
for g in cp.get('site_roads',[]): line(g.get('draw') or g['pts'],(120,120,120),1)
for r in cp['rails']: line(r['pts'],(138,75,31),2)
for r in S13['siteRoads']: line(r['pts'],(40,40,40),2)
line(S13['br'],(20,20,20),4)
line(S13['lane5'],(26,73,196),2)
for k,v in S14['lanes'].items(): line(v['pts'],(10,42,144),1)
line(S14['ferry_new'],(196,26,138),1)
poly(S13['lift']['poly'],(240,192,64),(160,112,0))
rect(S13['rig'],(224,80,80),(128,0,0))
line(S13['cable'],(220,0,0),2)
for l in S13['lots']:
    if l.get('rect'): rect(l['rect'],None,(122,58,160))
for b in S13['build']:
    if b.get('rect'): rect(b['rect'],(216,176,232),(122,58,160))
cols=[0,1200,2400,3600,4800,6000,7200,8400,9600]; rows=[-850,0,850,1700,2550,3400,4250,5200,6050,6900,7750]
for x in cols: line([(x,Y0),(x,Y1)],(0,0,0),1)
for y in rows: line([(X0,y),(X1,y)],(0,0,0),1)
for ci,x in enumerate(cols[:-1]):
    for ri,y in enumerate(rows[:-1]):
        if X0<=x+10<=X1 and Y0<=y+10<=Y1: d.text(T((x+15,y+15)),"ABCDEFGH"[ci]+str(ri),fill=(0,0,0))
im.save(sys.argv[1])
