# rails 17.11 — רסטר פנימי (PIL) לפעולות של SvgCtx — רק לבדיקה בעין שלי; לא נכנס לשום דף (כלל 17)
import json, sys, re, math
from PIL import Image, ImageDraw, ImageChops
def col(c):
    c=c.strip()
    if c=='none': return None
    m=re.match(r'rgba?\(([^)]*)\)',c)
    if m:
        v=[float(x) for x in m.group(1).split(',')]; a=v[3] if len(v)>3 else 1
        return (int(v[0]),int(v[1]),int(v[2]),int(255*a))
    if c.startswith('#'):
        h=c[1:]
        if len(h)==3: h=''.join(ch*2 for ch in h)
        return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),255)
    return (128,128,128,255)
def parse(d):
    subs=[];cur=None
    for m in re.finditer(r'([MLZCQ])([^MLZCQ]*)',d):
        k,a=m.group(1),[float(x) for x in m.group(2).split()] if m.group(2).strip() else []
        if k=='M': cur=[(a[0],a[1])] if a else []; subs.append([cur,False])
        elif k=='L':
            if cur is None: cur=[];subs.append([cur,False])
            cur.append((a[0],a[1]))
        elif k in 'CQ': cur.append((a[-2],a[-1]))
        elif k=='Z' and subs: subs[-1][1]=True
    return subs
def dashify(pts,dash):
    if not dash or sum(dash)<=0: return [pts]
    out=[];i=0;rem=dash[0];on=True;cur=[pts[0]] if pts else []
    for j in range(1,len(pts)):
        a,b=pts[j-1],pts[j];L=math.hypot(b[0]-a[0],b[1]-a[1]);pos=0
        while L-pos>rem:
            pos+=rem;t=pos/L;p=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
            if on: cur.append(p);out.append(cur)
            else: cur=[p]
            on=not on;i=(i+1)%len(dash);rem=dash[i]
        rem-=(L-pos)
        if on: cur.append(b)
    if on and len(cur)>1: out.append(cur)
    return out
def render(js,box,W,outp,ss=2):
    D=json.load(open(js)); ops,clips=D['ops'],D['clips']
    x0,y0,x1,y1=box; sc=W*ss/(x1-x0); H=int((y1-y0)*sc)
    T=lambda p:((p[0]-x0)*sc,(p[1]-y0)*sc)
    img=Image.new('RGBA',(W*ss,H),(0,0,0,255)); mcache={}
    def mask(cid):
        if cid in mcache: return mcache[cid]
        c=clips[cid]; m=Image.new('L',img.size,0); dr=ImageDraw.Draw(m)
        for pts,cl in parse(c['d']):
            if len(pts)>2: dr.polygon([T(p) for p in pts],fill=255)
        if c.get('parent'): m=ImageChops.multiply(m,mask(c['parent']))
        mcache[cid]=m; return m
    for o in ops:
        cc=col(o['c'])
        if not cc: continue
        cc=(cc[0],cc[1],cc[2],int(cc[3]*o.get('a',1)))
        layer=img if not o.get('clip') else Image.new('RGBA',img.size,(0,0,0,0))
        dr=ImageDraw.Draw(layer,'RGBA')
        subs=parse(o['d'])
        if o['t']=='f':
            for pts,cl in subs:
                if len(pts)>2: dr.polygon([T(p) for p in pts],fill=cc)
        else:
            w=max(1,int(round(o['w']*sc)))
            for pts,cl in subs:
                if cl and pts: pts=pts+[pts[0]]
                for seg in dashify([T(p) for p in pts],[v*sc for v in o.get('dash',[])]):
                    if len(seg)>1: dr.line(seg,fill=cc,width=w,joint='curve')
                    if o.get('cap')=='round' and w>2:
                        for p in (seg[0],seg[-1]): dr.ellipse([p[0]-w/2,p[1]-w/2,p[0]+w/2,p[1]+w/2],fill=cc)
        if o.get('clip'):
            a=layer.getchannel('A'); a=ImageChops.multiply(a,mask(o['clip'])); layer.putalpha(a); img.alpha_composite(layer)
    img=img.resize((W,int(H/ss)),Image.LANCZOS).convert('RGB'); img.save(outp)
if __name__=='__main__':
    render(sys.argv[1],[float(v) for v in sys.argv[2].split(',')],int(sys.argv[3]),sys.argv[4])
