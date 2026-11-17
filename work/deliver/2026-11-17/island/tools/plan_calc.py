# האי מאפס (D‑694) — החישוב: שטח, מוקדים, מרחק הליכה ← מספר התחנות (בזוגות); הרכבל; הרכבת. מדפיס JSON.
import json,math,sys
sys.path.insert(0,'/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools')
from plan_data import *
def area(poly):
    return abs(sum(poly[i][0]*poly[i-1][1]-poly[i-1][0]*poly[i][1] for i in range(len(poly))))/2
def clip(poly,r):
    x0,y0,x1,y1=r
    def cl(pts,inside,inter):
        out=[]
        for i in range(len(pts)):
            a,b=pts[i-1],pts[i]
            if inside(b):
                if not inside(a): out.append(inter(a,b))
                out.append(b)
            elif inside(a): out.append(inter(a,b))
        return out
    def ix(x):return lambda a,b:[x,a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])]
    def iy(y):return lambda a,b:[a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]),y]
    p=poly
    for ins,it in ((lambda q:q[0]>=x0,ix(x0)),(lambda q:q[0]<=x1,ix(x1)),(lambda q:q[1]>=y0,iy(y0)),(lambda q:q[1]<=y1,iy(y1))):
        p=cl(p,ins,it)
        if not p: return []
    return p
def plen(p): return sum(math.dist(p[i],p[i+1]) for i in range(len(p)-1))
def along(p,step):
    out=[];acc=0
    for i in range(len(p)-1):
        a,b=p[i],p[i+1];L=math.dist(a,b);n=max(1,int(L//step))
        for k in range(n):
            t=k/n;out.append(([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t],acc+L*t))
        acc+=L
    out.append((p[-1],acc));return out
R={}
# ---- 1. השטח ----
land_z={}
for z,r in ZONES.items():
    a=area(clip(LAND,r)) if clip(LAND,r) else 0
    if z=='D9': a+=area(MARINA_BASIN)   # המרינה: האגן נספר כחלק מהאזור (מים מוגנים)
    land_z[z]=round(a/100)   # מ"ר (100 פיקס׳² = 1 מ"ר)
R['land_m2']=land_z; R['land_total_m2']=sum(land_z.values())
R['zone_full_m2']=round(1200*850/100)
R['zones_equiv']=round(R['land_total_m2']/R['zone_full_m2'],2)
# ---- 2. התחנות ----
WALK=600   # 60 מ׳ — רדיוס ההליכה (בעיר: מרחק חציוני של 65 מ׳ בין זוגות תחנות, ממוצע 70 — city_plan.bus)
FOC=400    # 40 מ׳ — מוקד צריך תחנה במרחק הזה מהכניסה שלו
MINGAP=450 # 45 מ׳ — מרווח מינימלי בין תחנות על אותו קו (ושני מפרצים באורך 23 מ׳)
JUNC=150   # 15 מ׳ — לפחות מצומת (כמו בעיר: to_junction_m 11–27)
RD={r['id']:r['pts'] for r in ROADS}
spine=RD['ISL-SPINE-W']+[[4950,7480]]; mloop=RD['ISL-MAR-LOOP']
east=RD['ISL-E']; eloop=RD['ISL-E-LOOP']
junctions=[IL,[7330,7141],[4950,7400],[6600,7235],[6250,7240],[6700,7240],[5600,7240],[5800,7240],[4950,7240],[6150,7240],[4950,7480],[9380,7300],[9380,6960],[9300,6960],[8950,7700]]   # הבקר (סעיף 9): גם הצומת של דרך הפסגה (7960) והצמתים של רחובות ה-U, הכניסה לחניון הפארק והשער של חצר המשאיות
DRIVEWAYS=[[7960,7190]]   # הבקר (סעיף 9): דרך העפר לפסגה — דרך שירות בלי מעבר חצייה (כלל 21: חוצים רק בצמתים של השדרה)
cands=[]
for name,route,single,s0 in (('5',spine,False,0),('5',mloop,True,plen(spine)),('5א',east,False,0),('5א',eloop,True,plen(east))):
    for p,s in along(route,50):
        if min(math.dist(p,j) for j in junctions)<JUNC or math.dist(p,IL)<260: continue   # הכיכר: 15 מ׳ רדיוס + 11 מ׳
        if min(math.dist(p,j) for j in DRIVEWAYS)<80: continue   # כניסה של דרך שירות בלי מעבר חצייה (דרך העפר לפסגה) — 8 מ׳, כמו כניסה לחצר
        if not single and min(math.dist(p,j) for j in junctions)>400: continue   # כלל 21: מעבר חצייה רק בצומת — זוג תחנות עד 40 מ׳ מצומת
        cands.append({'line':name,'p':p,'s':s+s0,'single':single})
demand=[]
for pl in PLACES:
    x0,y0,x1,y1=pl['rect']
    for gx in range(int(x0),int(x1)+1,50):
        for gy in range(int(y0),int(y1)+1,50): demand.append({'p':[gx,gy],'w':1,'id':pl['id']})
    if pl['focal']: demand.append({'p':pl['at'],'w':40,'id':pl['id'],'focal':True})
    if pl.get('hub'):
        for ln in ('5','5א'): demand.append({'p':pl['at'],'w':40,'id':pl['id']+'·'+ln,'focal':True,'line':ln})   # (ד) תחנת המעבר: כל קו עוצר ליד הרכבת והרכבל
def covers(c,d):
    if d.get('line') and c['line']!=d['line']: return False
    if d.get('line'): return math.dist(c['p'],d['p'])<=450   # תחנת המעבר: 45 מ׳ — כולל המעבר בכיכר
    return math.dist(c['p'],d['p'])<=(FOC if d.get('focal') else WALK)
chosen=[]
def ok(c): return not any((c['line']==k['line'] and abs(c['s']-k['s'])<MINGAP) or math.dist(c['p'],k['p'])<MINGAP for k in chosen)
# (א) כל מוקד — תחנה במרחק 40 מ׳ מהכניסה; בוחרים את המקום שמכסה הכי הרבה מוקדים
foc=[d for d in demand if d.get('focal')]
for d in [d for d in foc if d.get('line')]:   # קודם תחנת המעבר (רכבת + רכבל) לכל קו — הכי קרוב לכיכר שמותר
    if not any(covers(c,d) for c in chosen):
        best=min((c for c in cands if ok(c) and covers(c,d)),key=lambda c:math.dist(c['p'],d['p']),default=None)
        if best: chosen.append(best)
while True:
    unf=[d for d in foc if not any(covers(c,d) for c in chosen)]
    if not unf: break
    best=max((c for c in cands if ok(c)),key=lambda c:(sum(1 for d in unf if covers(c,d)),-min(math.dist(c['p'],d['p']) for d in unf)),default=None)
    if not best or not any(covers(best,d) for d in unf): break
    chosen.append(best)
# (ב) כיסוי ההליכה של כל השטח הבנוי
while True:
    unc=[d for d in demand if not any(covers(c,d) for c in chosen)]
    if not unc: break
    best=None;bv=0
    for c in cands:
        if not ok(c): continue
        v=sum(d['w'] for d in unc if covers(c,d))
        if v>bv: bv=v;best=c
    if not best: break
    chosen.append(best)
unc=[d for d in demand if not any(covers(c,d) for c in chosen)]
tot=sum(d['w'] for d in demand if not d.get('focal')); cov=sum(d['w'] for d in demand if not d.get('focal') and any(covers(c,d) for c in chosen))
R['stops_rule']={'walk_m':WALK/10,'focal_m':FOC/10,'min_gap_m':MINGAP/10,'junction_m':JUNC/10,'city_median_m':65,'city_mean_m':70}
chosen.sort(key=lambda c:(c['line'],c['s']))
names={}
for c in chosen:
    near=sorted(PLACES,key=lambda pl:math.dist(pl['at'],c['p']))[:2]
    c['he']=' · '.join(n['he'].split(' — ')[0] for n in near)
# (ג) המרווח: לא יותר מ-90 מ׳ (1.3 × הממוצע של העיר) בין שתי תחנות על אותו קו
for ln in ('5','5א'):
    while True:
        ks=sorted([k for k in chosen if k['line']==ln],key=lambda k:k['s']);add=None
        for a,b in zip(ks,ks[1:]):
            if abs(b['s']-a['s'])>900:   # הבקר (סעיף 8): המרווח לאורך הדרך, לא בקו ישר
                mid=(a['s']+b['s'])/2;add=min((c for c in cands if c['line']==ln and ok(c)),key=lambda c:abs(c['s']-mid),default=None);break
        if not add: break
        chosen.append(add)
# קו 5א — נבנה (074l8): המקומות של הבנייה גוברים על הבחירה (אורך המפרץ 23 מ׳, היציאה מהמפרץ 17 מ׳ לפני הפינה, 2.5 מ׳ ויותר מהטבעת של המנחת)
BUILT_5A=[([8631,7533],'pair'),([9380,7514],'pair'),([9190,6960],'single')]
chosen=[c for c in chosen if c['line']!='5א']
def _s_on(route,p):
    best=None;acc=0
    for a,b in zip(route,route[1:]):
        L=math.dist(a,b);t=max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/(L*L or 1)));q=[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t];d=math.dist(q,p)
        if best is None or d<best[0]: best=(d,acc+L*t)
        acc+=L
    return best[1]
for p,k in BUILT_5A:
    chosen.append({'line':'5א','p':p,'single':k=='single','s':_s_on(east,p) if k=='pair' else plen(east)+_s_on(eloop,p),'built':True})
unc=[d for d in demand if not any(covers(c,d) for c in chosen)];cov=sum(d['w'] for d in demand if not d.get('focal') and any(covers(c,d) for c in chosen))
chosen.sort(key=lambda c:(c['line'],c['s']))
for c in chosen:
    near=sorted(PLACES,key=lambda pl:math.dist(pl['at'],c['p']))[:2]
    c['he']=' · '.join(n['he'].split(' — ')[0] for n in near)
NM={(8,7):'',}
R['stops']=[{'line':c['line'],'at':[round(c['p'][0]),round(c['p'][1])],'s_m':round(c['s']/10),'he':c['he'],'kind':'סופית — רציף אחד בלולאה' if c['single'] else 'זוג — מפרץ בכל צד'} for c in chosen]
R['stops_pairs']=sum(1 for c in chosen if not c['single']); R['stops_terminal']=sum(1 for c in chosen if c['single']); R['stops_bays']=2*R['stops_pairs']+R['stops_terminal']
R['coverage_pct']=round(100*cov/tot,1); R['uncovered_focal']=[d['id'] for d in unc if d.get('focal')]; R['built_5a']=True
R['spine_len_m']=round(plen(spine)/10); R['east_len_m']=round(plen(east)/10)
# אורך "רק לפי מרווח העיר": כמה זוגות היו יוצאים רק מהאורך
R['by_spacing_only']=math.ceil(R['spine_len_m']/70)+math.ceil(R['east_len_m']/70)
# ---- 3. הרכבל ----
cl=plen(CABLE); loop=2*cl; N=10; v=2.0
R['cable']={'stations':3,'one_way_m':round(cl/10),'loop_m':round(loop/10),'cabins':N,'min_cabins':8,'speed_mps':v,'spacing_m':round(loop/10/N,1),'headway_s':round(loop/10/N/v,1),'seats':8,'pph':round(3600/(loop/10/N/v)*8),'ride_min':round(cl/10/v/60,1),'old_m':round(math.dist(S13['cable'][0],S13['cable'][1])/10),'old_cabins':2}
# ---- 4. הרכבת ----
plat=math.dist(RAIL_A[0],RAIL_A[1])/10
R['train']={'platform_m':round(plat,1),'port_m':22.0,'car_m':15.4,'gap_m':1.4,'loco_m':0,'cars':4,'need_m':round(4*15.4+3*1.4,1),'fits':plat>=4*15.4+3*1.4,'freight_dock_m':round(math.dist(LOAD_PLAT[0],LOAD_PLAT[1])/10),'wagon_m':14.0,'freight_wagons':3,'freight_loco_m':19,'freight_need_m':round(19+3*14+3*1.4,1)}
print(json.dumps(R,ensure_ascii=False,indent=1))
json.dump(R,open('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/plan_calc.json','w'),ensure_ascii=False,indent=1)
