import json, math, ft_sim as F
M=F.M
Wd=F.World(json.load(open('sim_base019l.json')))
S=[x for x in Wd.SP if x.id in ('SP-PT-C','SP-TG-C','SP-BL-C','SP-MS-C')]+[Wd.PK['C1'],Wd.PK['C2']] if 'C2' in Wd.PK else [x for x in Wd.SP if x.id in ('SP-PT-C','SP-TG-C','SP-BL-C','SP-MS-C')]+[Wd.PK['C1']]
SB=[(x,F.boxes_of(x,M.evalp(x,0),F.VK if x.kind=='veh' else 1)) for x in S]
def arcpts(c,r,a0,a1,n=None):
    n=n or max(6,int(abs(a1-a0)*r/10)); return [[c[0]+r*math.cos(a0+(a1-a0)*i/n),c[1]+r*math.sin(a0+(a1-a0)*i/n)] for i in range(n+1)]
def path(R1,th1,R2):
    # מ-W (כיוון π) פנייה ימינה (בכיוון השעון — y למטה: מ-W אל N) — קשת 1 ואז קשת 2
    p=[5250+0.0,-170.0]
    # נחשב אחורה: קודם מייצרים קשתות מנקודה כלשהי ומזיזים כך שהסוף ב-x 5250
    pts=[[0,0]]; h=math.pi
    for R,dth in ((R1,th1),(R2,math.pi/2-th1)):
        q=pts[-1]; c=[q[0]+R*math.cos(h+math.pi/2),q[1]+R*math.sin(h+math.pi/2)]; a0=h-math.pi/2   # ימינה: מרכז בצד ימין
        A=arcpts(c,R,a0,a0+dth); pts+=A[1:]; h=h+dth
    dx=5250-pts[-1][0]; dy=-170-pts[0][1]
    P=[[x+dx,y+dy] for x,y in pts]
    return [[P[0][0]+600,-170]]+P+[[5250,M.HOLD+40]], P[-1][1]
best=[]
for R1 in (260,320,400,500,600,750):
    for th1 in (15,20,25,30,35,40,45,50):
        for R2 in (60,80,100,130,160,200):
            P,yend=path(R1,math.radians(th1),R2)
            if yend < M.HOLD+40+10: continue
            a=M.Actor('x','ac','AC-LG-01','',668,648); a.t=0; F.pmove(a,P,60,40,18)
            t=0; mm=99
            while t<a.t:
                Q=M.pose(a,t)
                for b in M.boxes(a,Q):
                    for x,B in SB:
                        for m in (0,6,12,20,30):
                            if any(M.obb_hit((b[0],b[1],b[2],b[3]+m,b[4]+m),q) for q in B): mm=min(mm,m); break
                t+=.1
            best.append((mm,R1,th1,R2,round(yend)))
best.sort(reverse=True); print(best[:8])
