import json,sys
from PIL import Image,ImageDraw
d=json.load(open(sys.argv[1])); out=sys.argv[2]; bx=[float(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [4800,-300,9600,2600]
S=float(sys.argv[4]) if len(sys.argv)>4 else .25
W=int((bx[2]-bx[0])*S); H=int((bx[3]-bx[1])*S); im=Image.new('RGB',(W,H),(205,208,204)); g=ImageDraw.Draw(im)
X=lambda x:(x-bx[0])*S; Y=lambda y:(y-bx[1])*S
R=lambda r,**k:g.rectangle([X(r[0]),Y(r[1]),X(r[2]),Y(r[3])],**k)
for r in d['service']: R(r['rect'],fill=(170,170,160),outline=(120,120,110))
for k,r in d['pockets'].items(): R(r,outline=(200,30,30),width=1)
for k,s in d['stands'].items():
    g.text((X(s['cx'])-8,Y(s['nose'])+4),k,fill=(0,0,120))
spans={'AC-LG-01':(668,648),'AC-NB-01':(376,358),'AC-RJ-01':(317,260),'AC-TB-01':(120,200),'AC-LT-01':(91,112),'AC-PR-01':(83,110),'AC-BJ-01':(144,158),'AC-CN-01':(144,140),'AC-CG-01':(549,476)}
for f in d['flights']:
    st=f['legs'][-1]; x,y=st['p'][0]; h=st.get('h',1.5708); L,Sp=spans.get(f['model'],(300,300))
    import math
    c,s_=math.cos(h),math.sin(h)
    ngf=.12; nx,ny=x+c*ngf*L,y+s_*ngf*L  # nose approx
    tx,ty=nx-c*L,ny-s_*L
    g.line([X(nx),Y(ny),X(tx),Y(ty)],fill=(255,255,255),width=max(2,int(Sp*.1*S)))
    wx,wy=nx-c*L*.48,ny-s_*L*.48; px,py=-s_,c
    g.line([X(wx-px*Sp/2),Y(wy-py*Sp/2),X(wx+px*Sp/2),Y(wy+py*Sp/2)],fill=(255,255,255),width=max(2,int(L*.08*S)))
    g.text((X(nx)+3,Y(ny)-10),f['id'],fill=(0,0,0))
for k,sp in d['spots'].items():
    r=sp['rect']; R(r,fill=(90,90,200)); 
for v in d['veh']:
    for gg in v['legs']:
        if gg['f']==8 and gg.get('p'):
            x,y=gg['p'][0]; g.ellipse([X(x)-3,Y(y)-3,X(x)+3,Y(y)+3],fill=(230,120,0)); g.text((X(x)+3,Y(y)),v['id'],fill=(120,40,0))
        if gg['f']==1 and len(gg.get('p',[]))>1:
            g.line([(X(p[0]),Y(p[1])) for p in gg['p']],fill=(60,140,60),width=1)
im.save(out); print(W,H)
