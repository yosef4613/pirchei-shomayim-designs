# האי מאפס (D‑694) — דף הציור והחישוב (כלל 13). SVG בקוד בלבד, בלי תמונות (כלל 17).
import json,sys,math,html
sys.path.insert(0,'/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools')
from plan_data import *
C=json.load(open(W+'/deliver/2026-11-17/island/plan_calc.json'))
OUT=W+'/deliver/2026-11-17/island/Island_D694_plan.html'
VB=(3500,5650,9800,7790)
def P(pts): return ' '.join(f'{p[0]:.0f},{p[1]:.0f}' for p in pts)
def rect(r,cls,extra=''): return f'<rect class="{cls}" x="{r[0]}" y="{r[1]}" width="{r[2]-r[0]}" height="{r[3]-r[1]}" {extra}/>'
STOPN=['צומת האי · הרכבת והרכבל · האכסניה','כפר ההר · השוק','מסוף המעבורת · הרכבל (תחנת הנמל)','מלון החוף · שכונת הנמל','אולם הכדורסל · חוף המערב','המרינה (סופית)','תחנת האי — היציאה הדרומית · החניון','מסוף המשא · חצר המשאיות','מנחת האי · פארק החוף · בסיס האסדה (סופית)']
stops=C['stops']
for i,s in enumerate(stops): s['name']=STOPN[i] if i<len(STOPN) else s['he']
def seg_dir(pts,p):
    best=None
    for a,b in zip(pts,pts[1:]):
        L=math.dist(a,b)
        if L<1: continue
        t=max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/L/L))
        q=[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t];d=math.dist(q,p)
        if best is None or d<best[0]: best=(d,[(b[0]-a[0])/L,(b[1]-a[1])/L])
    return best[1]
RD={r['id']:r for r in ROADS}
svg=[]
A=svg.append
A(f'<svg class="plan" viewBox="{VB[0]} {VB[1]} {VB[2]-VB[0]} {VB[3]-VB[1]}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="תוכנית האי החדש — מבט על">')
A('<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker>'
  '<pattern id="wv" width="120" height="60" patternUnits="userSpaceOnUse"><path d="M0,30 q30,-14 60,0 t60,0" fill="none" stroke="#bfe2f6" stroke-width="5"/></pattern></defs>')
A(f'<rect x="{VB[0]}" y="{VB[1]}" width="{VB[2]-VB[0]}" height="{VB[3]-VB[1]}" fill="#9fd0ee"/><rect x="{VB[0]}" y="{VB[1]}" width="{VB[2]-VB[0]}" height="{VB[3]-VB[1]}" fill="url(#wv)" opacity=".6"/>')
# היבשה של העיר (צפון) — כדי להראות את ראש הגשר
A(f'<polygon points="{P([[3500,5650],[6230,5650],[6230,5200],[3500,5200]])}" fill="#d9d2bd" stroke="#8d8466" stroke-width="6"/>')
A('<text class="lbl" x="4400" y="5440">העיר — החוף הדרומי (D7 / E7)</text>')
# האי הישן — קו מקווקו (להשוואה)
A(f'<polygon points="{P([p for p in S13["coast"] if p[1]<=7750])}" fill="none" stroke="#b0412e" stroke-width="10" stroke-dasharray="40 30" opacity=".75"/>')
# היבשה החדשה
A(f'<polygon points="{P(LAND)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="10"/>')
A('<polyline points="4800,7005 4900,6992 5200,6978 5500,6992 5800,6982 5950,6988" fill="none" stroke="#efd99a" stroke-width="80" stroke-linecap="round" opacity=".95"/>')
for c in S13['contours']: A(f'<polygon points="{P(c)}" fill="none" stroke="#a89466" stroke-width="5" opacity=".55"/>')
A('<ellipse cx="7700" cy="7520" rx="520" ry="200" fill="#4f8a3a" opacity=".35"/>')
for i in range(70):
    x=7180+((i*397)%880); y=7340+((i*233)%340)
    if (x-7700)**2/520**2+(y-7520)**2/200**2<1 and not (7650<x<7830 and 7400<y<7540): A(f'<circle cx="{x}" cy="{y}" r="22" fill="#3f7a2f" opacity=".7"/>')
# המרינה
A(f'<polygon points="{P(MARINA_BASIN)}" fill="#8fc9ec" stroke="#5a7a8a" stroke-width="6"/>')
for b in BREAKWATER: A(f'<polyline points="{P(b)}" fill="none" stroke="#7c7c78" stroke-width="34" stroke-linecap="square"/>')
for pt in PONTOONS:
    A(rect(pt,'pont'))
    for k in range(7):
        y=pt[1]+30+k*42
        for sx in (-1,1): A(f'<ellipse cx="{(pt[0]+pt[2])/2+sx*48:.0f}" cy="{y}" rx="34" ry="11" fill="#fbfbf7" stroke="#55606a" stroke-width="3"/>')
# נתיבי השיט
for pts,lab,col in ((LANE_MAIN,'נתיב השיט הראשי — מזרח ↔ מערב, מתחת למפתח המתרומם; אחרי D — לדרום־מערב (בין B ל-C)','#1d3f8f'),(LANE_FERRY,'המעבורת — A6 ↔ נמל האי (F9)','#a3227a'),(LANE_MARINA,'יציאת המרינה','#2a7a8a'),(LANE_RIG,'ספינת האספקה ↔ האסדה','#8a4a10')):
    A(f'<polyline points="{P(pts)}" fill="none" stroke="{col}" stroke-width="12" stroke-dasharray="70 40" marker-end="url(#ar)" marker-start="url(#ar)"/>')
A('<text class="lane" x="5000" y="6420">נתיב השיט הראשי: מזרח ↔ מערב</text><text class="lane" x="4300" y="6540">↙ אחרי D — לדרום־מערב (בין B ל-C)</text>')
A('<text class="lane" x="9750" y="5770">מהמזרח (H7) אל המפתח</text>')
# הגשר והמפתח
A(f'<polygon points="{P(LIFT)}" fill="#f0c24a" stroke="#9c7400" stroke-width="6" opacity=".9"/>')
A(f'<polyline points="{P([[6060,5200],[6060,5260],[6090,5350],[6224,5460],[6420,5714],[6624,5924],[8267.5,7088],IL])}" fill="none" stroke="#3b3b3b" stroke-width="130" stroke-linejoin="round"/>')
A(f'<polyline points="{P([[6060,5200],[6060,5260],[6090,5350],[6224,5460],[6420,5714],[6624,5924],[8267.5,7088],IL])}" fill="none" stroke="#f3f3f3" stroke-width="4" stroke-dasharray="30 30"/>')
A('<text class="lbl" x="6700" y="5900" transform="rotate(35 6700 5900)">גשר האי — קיים, לא משתנה (D‑634)</text><text class="lbl" x="7380" y="6330" transform="rotate(35 7380 6330)">המפתח המתרומם</text>')
# האסדה, הצינור, מזח האספקה
A(rect(RIG,'rig')); A('<text class="lbl" x="8870" y="6130">אסדת הגז (נשארת במקום — D‑618)</text>')
A(f'<polyline points="{P(PIPE)}" fill="none" stroke="#7a4a1a" stroke-width="8" stroke-dasharray="20 14"/>')
A(rect(SUPPLY_PIER,'pier'))
# המסילה
for tr in (RAIL_A,RAIL_B,FREIGHT,FREIGHT2):
    A(f'<polyline points="{P(tr)}" fill="none" stroke="#6b4a2a" stroke-width="16"/><polyline points="{P(tr)}" fill="none" stroke="#e9e2d0" stroke-width="5" stroke-dasharray="6 10"/>')
A(f'<polygon points="{P([[8432.6,6923.1],[9248.7,7501.1],[9179.3,7599.1],[8363.3,7021.1]])}" fill="#bdb6a6" opacity=".55"/>')
A(f'<polygon class="yard" points="{P(TRUCK_YARD)}"/><polygon class="plat" points="{P(LOAD_PLAT)}"/>')
_a,_b=S13['sb'];_u=[(_b[0]-_a[0])/1000.05,(_b[1]-_a[1])/1000.05];_ang=math.degrees(math.atan2(_u[1],_u[0]))
for k,f in enumerate((.62,.71,.80)):   # 3 קרונות המשא בפס ב׳, מול הרציף (הקטר מאחור — דוחף פנימה)
    x=_a[0]+(_b[0]-_a[0])*f;y=_a[1]+(_b[1]-_a[1])*f;A(f'<rect x="-66" y="-14" width="132" height="28" rx="4" fill="#4a4f55" stroke="#222" stroke-width="3" transform="translate({x:.0f},{y:.0f}) rotate({_ang:.0f})"/>')
for k,f in enumerate((.64,.74,.84)):   # עמדות המשאיות, ניצבות לרציף
    x=_a[0]+(_b[0]-_a[0])*f-_u[1]*118;y=_a[1]+(_b[1]-_a[1])*f+_u[0]*118;A(f'<rect x="-50" y="-15" width="100" height="30" rx="6" fill="#e2a33a" stroke="#6b4a10" stroke-width="3" transform="translate({x:.0f},{y:.0f}) rotate({_ang+90:.0f})"/>')
for q in PARKING:
    r=q['rect'];A(f'<rect x="{r[0]}" y="{r[1]}" width="{r[2]-r[0]}" height="{r[3]-r[1]}" fill="#cfd3d6" stroke="#5c6670" stroke-width="4"/><text x="{(r[0]+r[2])/2:.0f}" y="{(r[1]+r[3])/2+14:.0f}" font="700 40px Arial" style="font:700 40px Arial" fill="#2b4a8a" text-anchor="middle">P</text>')
# הכבישים
for r in ROADS:
    if r['id']=='BR-I': continue
    pts=P(r['pts']); cls=r['cls']
    if cls=='collector': A(f'<polyline points="{pts}" class="rd"/><polyline points="{pts}" class="rdc"/>')
    elif cls=='loop': A(f'<polyline points="{pts}" class="rd lp"/><polyline points="{pts}" class="rdc"/>')
    elif cls=='local': A(f'<polyline points="{pts}" class="rd lo"/>')
    else: A(f'<polyline points="{pts}" class="trk"/>')
A(f'<circle cx="{IL[0]}" cy="{IL[1]}" r="150" fill="#5c5c5c"/><circle cx="{IL[0]}" cy="{IL[1]}" r="72" fill="#a9cf86" stroke="#fff" stroke-width="5"/>')
# חיצי הלולאות (חד-סטרי, בכיוון הנסיעה; לולאת המזרח — החיצים החדשים של 12:55 בכתום)
for r in ROADS:
    if r['cls']!='loop': continue
    new=r['id']=='ISL-E-LOOP'
    for a,b in zip(r['pts'],r['pts'][1:]):
        if math.dist(a,b)<120: continue
        x=(a[0]+b[0])/2;y=(a[1]+b[1])/2;ang=math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
        if new: A(f'<path d="M-44,-28 L44,0 L-44,28 z" fill="#ff8a1f" stroke="#7a3a00" stroke-width="5" transform="translate({x:.0f},{y:.0f}) rotate({ang:.0f})"/>')
        else: A(f'<path d="M-26,-16 L26,0 L-26,16 z" fill="#fff" stroke="#333" stroke-width="3" transform="translate({x:.0f},{y:.0f}) rotate({ang:.0f})"/>')
A('<path d="M9480,7640 L9480,7330" stroke="#ff8a1f" stroke-width="16" marker-end="url(#ar)"/><text class="dt" x="9410" y="7740" style="font-size:34px;fill:#7a3a00">חדש (12:55): ישר צפונה ← מסביב ← לנתיב היורד</text>')
for r in ROADS:   # דרכים דו-סטריות: חץ לכל כיוון, בצד ימין (תנועה מימין)
    if r['cls'] not in ('collector','local'): continue
    for a,b in zip(r['pts'],r['pts'][1:]):
        L=math.dist(a,b)
        if L<260: continue
        u=[(b[0]-a[0])/L,(b[1]-a[1])/L];n=[-u[1],u[0]];x=(a[0]+b[0])/2;y=(a[1]+b[1])/2;ang=math.degrees(math.atan2(u[1],u[0]))
        for sd in (1,-1): A(f'<path d="M-16,-9 L16,0 L-16,9 z" fill="#fff" transform="translate({x+n[0]*22*sd:.0f},{y+n[1]*22*sd:.0f}) rotate({ang+(0 if sd>0 else 180):.0f})"/>')
# המקומות
for i,pl in enumerate(PLACES,1):
    r=pl['rect']; A(rect(r,'pl')); A(f'<circle cx="{pl["at"][0]}" cy="{pl["at"][1]}" r="34" fill="#6a2c91"/><text class="pn" x="{pl["at"][0]}" y="{pl["at"][1]+12}">{i}</text>')
# הרכבל
A(f'<polyline points="{P(CABLE)}" fill="none" stroke="#c0281e" stroke-width="7"/>')
loop=CABLE+CABLE[-2::-1]
L=[math.dist(loop[i],loop[i+1]) for i in range(len(loop)-1)]; tot=sum(L)
for k in range(C['cable']['cabins']):
    s=tot*k/C['cable']['cabins']; i=0
    while s>L[i]: s-=L[i]; i+=1
    a,b=loop[i],loop[i+1]; t=s/L[i]; x=a[0]+(b[0]-a[0])*t; y=a[1]+(b[1]-a[1])*t
    n=[-(b[1]-a[1])/L[i],(b[0]-a[0])/L[i]]
    A(f'<rect x="{x+n[0]*16-14:.0f}" y="{y+n[1]*16-11:.0f}" width="28" height="22" rx="5" fill="#e0402f" stroke="#5a0f0a" stroke-width="3"/>')
for st in CABLE: A(f'<rect x="{st[0]-55}" y="{st[1]-40}" width="110" height="80" rx="8" fill="#f6e3d6" stroke="#c0281e" stroke-width="7"/>')
# התחנות — מפרץ בכל צד (זוג), או רציף אחד בלולאה (סופית)
for i,s in enumerate(stops,1):
    p=s['at']; rid='ISL-E-LOOP' if (s['line']=='5א' and 'סופית' in s['kind']) else 'ISL-MAR-LOOP' if 'סופית' in s['kind'] else ('ISL-E' if s['line']=='5א' else ('ISL-MAR-IN' if p[0]==4950 else 'ISL-SPINE-W'))
    if 'סופית' in s['kind']:   # הרציף מימין לכיוון הנסיעה בלולאה
        u=seg_dir(RD[rid]['pts'],p); n=[-u[1],u[0]]; ang=math.degrees(math.atan2(u[1],u[0])); cx=p[0]+n[0]*66; cy=p[1]+n[1]*66
        A(f'<rect x="-115" y="-16" width="230" height="32" rx="10" fill="#ffffff" stroke="{"#1f5fd1" if s["line"]=="5" else "#178a54"}" stroke-width="6" transform="translate({cx:.0f},{cy:.0f}) rotate({ang:.0f})"/>')
        col="#1f5fd1" if s['line']=='5' else "#178a54"; A(f'<circle cx="{p[0]}" cy="{p[1]}" r="38" fill="{col}" stroke="#fff" stroke-width="6"/><text class="sn" x="{p[0]}" y="{p[1]+13}">{i}</text>'); continue
    u=seg_dir(RD[rid]['pts'],p); n=[-u[1],u[0]]; ang=math.degrees(math.atan2(u[1],u[0]))
    sides=(1,) if 'סופית' in s['kind'] else (1,-1)
    for sd in sides:
        cx=p[0]+n[0]*66*sd; cy=p[1]+n[1]*66*sd
        A(f'<rect x="-115" y="-16" width="230" height="32" rx="10" fill="#ffffff" stroke="{"#1f5fd1" if s["line"]=="5" else "#178a54"}" stroke-width="6" transform="translate({cx:.0f},{cy:.0f}) rotate({ang:.0f})"/>')
    col="#1f5fd1" if s['line']=='5' else "#178a54"
    A(f'<circle cx="{p[0]}" cy="{p[1]}" r="38" fill="{col}" stroke="#fff" stroke-width="6"/><text class="sn" x="{p[0]}" y="{p[1]+13}">{i}</text>')
# רשת האזורים
cols=[3600,4800,6000,7200,8400,9600]; rows=[5200,6050,6900,7750]
for x in cols: A(f'<line x1="{x}" y1="{VB[1]}" x2="{x}" y2="{VB[3]}" class="grid"/>')
for y in rows: A(f'<line x1="{VB[0]}" y1="{y}" x2="{VB[2]}" y2="{y}" class="grid"/>')
for ci,x in enumerate(cols[:-1]):
    for ri,y in enumerate(rows[:-1]):
        z='DEFGH'[ci]+str(7+ri)
        A(f'<text class="zid{" zon" if z in ZONES else ""}" x="{x+30}" y="{y+70}">{z}</text>')
A('<rect x="4200" y="6900" width="600" height="850" fill="none" stroke="#e8590c" stroke-width="12" stroke-dasharray="50 30"/><text class="zh" x="4230" y="6890">½ D9 — המרינה</text>')
A('<text class="lbl" x="5000" y="7150">E9 — חדש</text><text class="lbl" x="9000" y="6560">H8 — חדש</text>')
A('</svg>')
SVG='\n'.join(svg)

# ---- פרטים: זוג תחנות טיפוסי ולולאה סופית (מידות אמיתיות, 10 פיקס׳ = 1 מ׳) ----
def detail_pair():
    o=['<svg class="det" viewBox="-40 -150 1100 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="זוג תחנות טיפוסי">']
    o.append('<rect x="-40" y="-150" width="1100" height="300" fill="#cfe6a8"/>')
    o.append('<rect x="-40" y="-74" width="1100" height="148" fill="#d6d2c6"/>')   # מדרכות
    o.append('<rect x="-40" y="-44" width="1100" height="88" fill="#585858"/><line x1="-40" y1="0" x2="1060" y2="0" stroke="#f2f2f2" stroke-width="2" stroke-dasharray="20 20"/>')
    o.append('<rect x="-40" y="-44" width="120" height="88" fill="#4a4a4a"/>')     # הצומת
    o.append('<rect x="-40" y="-150" width="120" height="76" fill="#585858"/>')    # הרחוב הניצב
    for k in range(6): o.append(f'<rect x="{90+k*0}" y="{-40+k*14}" width="40" height="8" fill="#fff"/>')
    for k in range(6): o.append(f'<rect x="{-30+k*16}" y="-70" width="8" height="24" fill="#fff"/>')
    # מפרץ צפוני (כיוון מערבה) ומפרץ דרומי (מזרחה) — כניסה 4 מ׳, עצירה 15, יציאה 4, עומק 3
    for sd,x0 in ((1,240),(-1,560)):
        y=44 if sd>0 else -44; d=30*sd
        o.append(f'<polygon points="{x0},{y} {x0+40},{y+d} {x0+190},{y+d} {x0+230},{y}" fill="#5f5f5f" stroke="#fff" stroke-width="2"/>')
        o.append(f'<rect x="{x0+50}" y="{y+(4 if sd>0 else -29)}" width="122" height="25" rx="5" fill="{"#1f5fd1"}" stroke="#0c2a66" stroke-width="2"/>')
        o.append(f'<rect x="{x0+60}" y="{y+d+(6 if sd>0 else -26)}" width="60" height="20" fill="rgba(180,220,245,.6)" stroke="#2b6a90" stroke-width="2"/>')
        o.append(f'<circle cx="{x0+150}" cy="{y+d+(16 if sd>0 else -16)}" r="5" fill="#d0342c"/>')
    o.append('<text x="350" y="125" class="dt">מפרץ: 4 + 15 + 4 מ׳, עומק 3 מ׳ (כמו בעיר) · הקואץ׳ 12.2 מ׳ · סככה עם גג שקוף על המדרכה</text>')
    o.append('<text x="1000" y="-110" class="dt">צומת עם מעברי חצייה — כאן חוצים (כלל 21); המפרץ הראשון 15 מ׳ ויותר מהצומת</text>')
    o.append('<text x="980" y="-55" class="dt" fill="#fff">מערבה ←</text><text x="980" y="30" class="dt" fill="#fff">→ מזרחה</text>')
    o.append('</svg>'); return '\n'.join(o)
def detail_loop():
    o=['<svg class="det" viewBox="4180 7240 1020 510" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="המרינה ולולאת המרינה — סוף קו 5">']
    o.append('<rect x="4180" y="7240" width="1020" height="510" fill="#9fd0ee"/>')
    o.append(f'<polygon points="{P([[4800,7240],[5200,7240],[5200,7750],[4200,7750],[4200,7700],[4800,7700]])}" fill="#cfe6a8"/>')
    o.append(f'<polygon points="{P(MARINA_BASIN)}" fill="#8fc9ec" stroke="#5a7a8a" stroke-width="5"/>')
    for b in BREAKWATER: o.append(f'<polyline points="{P(b)}" fill="none" stroke="#7c7c78" stroke-width="30" stroke-linecap="square"/>')
    for pt in PONTOONS:
        o.append(f'<rect x="{pt[0]}" y="{pt[1]}" width="{pt[2]-pt[0]}" height="{pt[3]-pt[1]}" fill="#f4f1e6" stroke="#6b6b60" stroke-width="3"/>')
        for k in range(7):
            y=pt[1]+25+k*44
            for sx in (-1,1): o.append(f'<ellipse cx="{(pt[0]+pt[2])/2+sx*46:.0f}" cy="{y}" rx="32" ry="10" fill="#fbfbf7" stroke="#55606a" stroke-width="2.5"/>')
    lp=[[4950,7400],[4850,7400],[4850,7700],[5150,7700],[5150,7400],[4950,7400]]
    o.append(f'<polyline points="{P(lp)}" fill="none" stroke="#585858" stroke-width="50" stroke-linejoin="round"/>')
    o.append(f'<polyline points="{P([[4950,7240],[4950,7400]])}" fill="none" stroke="#585858" stroke-width="88"/>')
    o.append('<rect x="4880" y="7430" width="240" height="90" fill="#cfd3d6" stroke="#5c6670" stroke-width="3"/><text x="5000" y="7485" class="dt" text-anchor="middle">P · 16</text>')
    o.append('<rect x="4880" y="7530" width="240" height="60" fill="#e9e3d2" stroke="#8a7a5a" stroke-width="3"/><text x="5000" y="7568" class="dt" text-anchor="middle">משרד, השכרה, קופה</text>')
    o.append('<rect x="4880" y="7600" width="240" height="80" fill="#efe2c4" stroke="#8a6a3a" stroke-width="3"/><text x="5000" y="7648" class="dt" text-anchor="middle">המספנה — מנוף הרמה</text>')
    o.append('<polygon points="4805,7510 4805,7546 4805,7656 4805,7690" fill="none"/>')
    o.append('<polygon points="4825,7485 4795,7515 4795,7665 4825,7695" fill="#5f5f5f" stroke="#fff" stroke-width="2"/><rect x="4800" y="7530" width="22" height="122" rx="5" fill="#1f5fd1"/>')   # המפרץ והקואץ׳ — בצד המערבי, מול המרינה
    for (x,y,a) in ((4900,7400,180),(4850,7550,90),(5000,7700,0),(5150,7550,270)):
        o.append(f'<path d="M-16,-10 L16,0 L-16,10 z" fill="#fff" transform="translate({x},{y}) rotate({a})"/>')
    o.append(f'<circle cx="{SHIP_TURN[0]}" cy="{SHIP_TURN[1]}" r="{SHIP_TURN[2]}" fill="none" stroke="#b0412e" stroke-width="6" stroke-dasharray="30 20"/><text x="4210" y="7275" class="dt" fill="#b0412e">קצה עיגול הסיבוב של "צוק הים" (y 7299)</text>')
    o.append('<text x="4840" y="7735" class="dt">הקואץ׳ נוסע דרומה בצלע המערבית — הרציף מימין, מול המרינה (הלולאה נגד כיוון השעון)</text>')
    o.append('</svg>'); return '\n'.join(o)


# ---- גרסה 6: הבעלים 17.11 10:45 — הצומת המרומזר במקום הכיכר, המפתח באמצע, ההר מערבה, הרכבל — הפסגה היא התחנה האחרונה ----
OW_DS=180   # המפתח זז לאורך ציר הגשר לכיוון העיר (פיקס׳): ממרכז ב-s 610 (019h2) ל-s 430 — אמצע הדרך במים בין ראש הגשר לחוף האי
OW_U=(0.816035,0.578002)
OW_LIFT_C0=S13['lift']['center']; OW_D=(-OW_DS*OW_U[0],-OW_DS*OW_U[1])
OW_LIFT_NEW=[[x+OW_D[0],y+OW_D[1]] for x,y in LIFT]; OW_LIFT_C=[OW_LIFT_C0[0]+OW_D[0],OW_LIFT_C0[1]+OW_D[1]]
OW_SUMMIT0=S13['summit']; OW_SUMMIT=[6790,7560]; OW_KX=1.1   # 1.1: קו הגובה התחתון נגמר ב-x ≈ 5660 — האולם (E9) והמרינה נשארים במישור
def ow_cont(c): return [[OW_SUMMIT[0]+(x-OW_SUMMIT0[0])*OW_KX,y+(OW_SUMMIT[1]-OW_SUMMIT0[1])*0] for x,y in c]
OW_LANE=[[12600,5700],[8420,5700],[8020,5672],[round(OW_LIFT_C[0]),round(OW_LIFT_C[1])],[6690,6284],[6580,6400],[6470,6450],[5700,6450],[3300,6450]]
OW_CABLE=[[8545,7265],[7742,7470],[6760,7620]]
def owner_svg():
    o=[]; a=o.append
    a('<svg class="plan" viewBox="5300 5100 4400 2750" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="גרסה 6 — הצומת, המפתח, ההר והרכבל">')
    a('<defs><marker id="ar6" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker></defs>')
    a('<rect x="5300" y="5100" width="4400" height="2750" fill="#9fd0ee"/>')
    a(f'<polygon points="{P([[5300,5650],[6230,5650],[6230,5100],[5300,5100]])}" fill="#d9d2bd" stroke="#8d8466" stroke-width="6"/>')
    a(f'<polygon points="{P(LAND)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="10"/>')
    for c in S13['contours']: a(f'<polygon points="{P(c)}" fill="none" stroke="#8c8c8c" stroke-width="5" stroke-dasharray="24 18" opacity=".6"/>')
    for i,c in enumerate(S13['contours']): a(f'<polygon points="{P(ow_cont(c))}" fill="#9a7b4f" fill-opacity="{.06+.035*i:.3f}" stroke="#7a5a2a" stroke-width="7"/>')
    a(f'<text class="lbl" x="{OW_SUMMIT0[0]-60}" y="{OW_SUMMIT0[1]-40}" fill="#666">✕ הפסגה של היום</text>')
    a(f'<polygon points="{OW_SUMMIT[0]},{OW_SUMMIT[1]-70} {OW_SUMMIT[0]-55},{OW_SUMMIT[1]+25} {OW_SUMMIT[0]+55},{OW_SUMMIT[1]+25}" fill="#7a5a2a"/><text class="lbl" x="{OW_SUMMIT[0]-380}" y="{OW_SUMMIT[1]-90}">▲ הפסגה החדשה — ההר זז 87 מ׳ מערבה ומתרחב פי 1.1</text>')
    a(f'<polyline points="{P(LANE_MAIN[:8])}" fill="none" stroke="#6b7c8f" stroke-width="10" stroke-dasharray="40 40" opacity=".7"/>')
    a(f'<polyline points="{P(OW_LANE)}" fill="none" stroke="#1d3f8f" stroke-width="14" stroke-dasharray="70 40" marker-end="url(#ar6)" marker-start="url(#ar6)"/>')
    br=[[6060,5200],[6060,5260],[6090,5350],[6224,5460],[6420,5714],[6624,5924],[8267.5,7088],IL]
    a(f'<polyline points="{P(br)}" fill="none" stroke="#3b3b3b" stroke-width="130" stroke-linejoin="round"/>')
    a(f'<polygon points="{P(LIFT)}" fill="none" stroke="#9c7400" stroke-width="8" stroke-dasharray="30 20"/>')
    a(f'<polygon points="{P(OW_LIFT_NEW)}" fill="#f0c24a" stroke="#9c7400" stroke-width="8" opacity=".95"/>')
    a(f'<text class="lbl" x="{OW_LIFT_C[0]-700}" y="{OW_LIFT_C[1]-170}">המפתח המתרומם — 18 מ׳ לכיוון העיר: באמצע הדרך במים</text>')
    a(f'<text class="lbl" x="7560" y="6520" fill="#7a6000">(המקום של היום — מקווקו)</text>')
    a('<text class="lane" x="7900" y="5990">נתיב השיט — עובר מתחת למפתח החדש</text>')
    a(f'<polyline points="{P(OW_CABLE)}" fill="none" stroke="#c0281e" stroke-width="14"/>')
    for (x,y),lab,dx in zip(OW_CABLE,['תחנת העמק — ליד הצומת','תחנת היער — באמצע המדרון (העליונה של היום)','הפסגה — התחנה האחרונה: קפה ותצפית'],(-120,-300,-520)):
        a(f'<rect x="{x-45}" y="{y-35}" width="90" height="70" fill="#fff" stroke="#c0281e" stroke-width="8"/><text class="lbl" x="{x+dx}" y="{y+95}">{lab}</text>')
    A_=[p for p in PLACES if p['id']=='ISL-ARENA'][0]['rect']; a(f'<rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="{A_[3]-A_[1]}" fill="#e8743b" stroke="#8a3a12" stroke-width="10"/><rect x="{A_[0]+45}" y="{A_[1]+80}" width="280" height="150" fill="#d9a066" stroke="#fff" stroke-width="5"/><text class="lbl" x="{A_[0]-80}" y="{A_[3]+70}">אולם הכדורסל — שמור ל-arena</text>')
    a(f'<circle cx="{IL[0]}" cy="{IL[1]}" r="70" fill="#585858"/><circle cx="{IL[0]-40}" cy="{IL[1]-90}" r="18" fill="#2fa84f"/><circle cx="{IL[0]+90}" cy="{IL[1]+10}" r="18" fill="#e0b020"/><circle cx="{IL[0]-95}" cy="{IL[1]+20}" r="18" fill="#d33"/><text class="lbl" x="{IL[0]+110}" y="{IL[1]-80}">הצומת המרומזר — במקום כיכר האי</text>')
    EL=[[9380,7300],[9380,6960],[9000,6960],[9000,7170],[9130,7300],[9380,7300]]
    a(f'<polyline points="{P(EL)}" fill="none" stroke="#585858" stroke-width="70" stroke-linejoin="round"/><polyline points="{P([[9380,7300],[9380,7690]])}" fill="none" stroke="#585858" stroke-width="90"/>')
    for p_,q_ in zip(EL,EL[1:]):
        if math.dist(p_,q_)<120: continue
        x=(p_[0]+q_[0])/2;y=(p_[1]+q_[1])/2;ang=math.degrees(math.atan2(q_[1]-p_[1],q_[0]-p_[0]))
        a(f'<path d="M-44,-28 L44,0 L-44,28 z" fill="#ff8a1f" stroke="#7a3a00" stroke-width="5" transform="translate({x:.0f},{y:.0f}) rotate({ang:.0f})"/>')
    a('<path d="M9405,7680 L9405,7330" stroke="#ff8a1f" stroke-width="14" marker-end="url(#ar6)"/><path d="M9355,7330 L9355,7680" stroke="#ff8a1f" stroke-width="14" marker-end="url(#ar6)"/>')
    a('<text class="lbl" x="8470" y="6870" fill="#7a3a00" style="font-size:38px">לולאת המזרח (12:55): ישר צפונה, מסביב, ובחזרה לנתיב היורד</text>')
    a('</svg>'); return ''.join(o)
def owner_junction():
    o=[]; a=o.append
    a('<svg class="det" viewBox="-520 -520 1040 1040" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="הצומת המרומזר — מבט על">')
    a('<rect x="-520" y="-520" width="1040" height="1040" fill="#cfe6a8"/>')
    legs=[('גשר האי (מצפון, BR-I14 — 2+2)',(8267.5-8330,7088-7320),124),('דרך הנמל והכפר (IS-W1 — 1+1)',(8108.5-8330,7230-7320),96),('דרך התחנה (IS-E1 — 1+1)',(8526-8330,7459-7320),96)]
    import math
    for lab,(dx,dy),w in legs:
        L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; x1,y1=ux*520,uy*520
        a(f'<line x1="0" y1="0" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#e8e3d4" stroke-width="{w+40}"/>')
    for lab,(dx,dy),w in legs:
        L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; x1,y1=ux*520,uy*520; nx,ny=-uy,ux
        a(f'<line x1="0" y1="0" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#585858" stroke-width="{w}"/>')
        a(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{ux*110:.0f}" y2="{uy*110:.0f}" stroke="#fff" stroke-width="3" stroke-dasharray="22 18"/>')
        sx,sy=ux*150,uy*150
        a(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{sx-nx*w/2:.0f}" y2="{sy-ny*w/2:.0f}" stroke="#fff" stroke-width="7"/>')   # קו העצירה — בנתיב הנכנס
        for k in range(-3,4):
            cx,cy=ux*195+nx*k*14,uy*195+ny*k*14
            a(f'<line x1="{cx-ux*14:.0f}" y1="{cy-uy*14:.0f}" x2="{cx+ux*14:.0f}" y2="{cy+uy*14:.0f}" stroke="#fff" stroke-width="8"/>')   # מעבר חצייה
        hx,hy=sx-nx*(w/2+26),sy-ny*(w/2+26)
        a(f'<rect x="{hx-10:.0f}" y="{hy-24:.0f}" width="20" height="48" rx="5" fill="#222"/><circle cx="{hx:.0f}" cy="{hy-12:.0f}" r="6" fill="#d33"/><circle cx="{hx:.0f}" cy="{hy+10:.0f}" r="6" fill="#2fa84f"/>')
        a(f'<text class="lbl" x="{ux*330-150:.0f}" y="{uy*330+(60 if uy>0 else -40):.0f}" style="font-size:34px">{lab}</text>')
    a('</svg>'); return ''.join(o)
OWNER_SVG=owner_svg(); OWNER_J=owner_junction()

# ---- 17.11 ~12:40 — שלב 2ג-1 (נבנה): היבשה של E9 לפני האולם — כמו במשחק (019h5 / 019j2) ----
E9C=[[5000,7749],[5000,7010],[5100,6994],[5200,6985],[5320,6988],[5450,6993],[5560,6998],[5620,7005],[5672,7024],[5700,7060],[5712,7120],[5716,7220],[5718,7300],[5720,7400],[5722,7500],[5724,7600],[5728,7660],[5750,7690],[5800,7700],[5900,7702],[6000,7702],[6080,7701],[6158,7700]]
E9WALK=[[6475,7560],[6492,7600],[6492,7700],[6470,7724],[6150,7726],[5800,7726],[5740,7716],[5664,7660],[5660,7560],[5660,7420],[5640,7380],[5590,7360]]
FERRY=[[5600,6500],[5950,7150],[5900,7366],[6519,7366]]
def _qb(a,c,b,n=16): return [[(1-t)**2*a[0]+2*(1-t)*t*c[0]+t*t*b[0],(1-t)**2*a[1]+2*(1-t)*t*c[1]+t*t*b[1]] for t in [i/n for i in range(n+1)]]
SHIP_OLD=[[4320,6850],[4600,6850]]+_qb([4600,6850],[5250,6860],[5300,7450],32)[1:]+[[5300,7750]]
SHIP_NEW=[[4320,6850]]+_qb([4320,6850],[4460,6850],[4460,6990])[1:]+[[4460,7750]]
TUG_IN=[[4820,6450],[4880,6980],[4600,7040],[4460,7200],[4460,7354]]
TUG_BACK=[[4580,7700],[4700,7600],[4720,7100],[4800,6700],[4820,6450]]
def e9_svg():
    o=[]; a=o.append
    a('<svg class="plan" viewBox="3900 6350 2800 1450" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="שלב 2ג-1 — היבשה של E9 כמו במשחק">')
    a('<defs><marker id="ar7" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker></defs>')
    a('<rect x="3900" y="6350" width="2800" height="1450" fill="#9fd0ee"/>')
    a('<rect x="3900" y="7750" width="2800" height="50" fill="#55606a" opacity=".35"/><text class="dt" x="3920" y="7790">קצה העולם (y 7750)</text>')
    isl=[[6158,7700],[6180,7610],[6176,7520],[6170,7420],[6182,7320],[6176,7210],[6185,7130],[6195,7095],[6235,7030],[6305,6993],[6430,6975],[6700,6980],[6700,7750],[6150,7750]]
    a(f'<polygon points="{P(isl)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="8"/>')
    for b in S13['water']: a(f'<polygon points="{P(b)}" fill="#9fd0ee" stroke="#5a7d96" stroke-width="5"/>')
    a(f'<polygon points="{P(E9C+[[6158,7750],[5000,7750]])}" fill="#bfe08f" stroke="#4f7a25" stroke-width="10"/>')
    a(f'<polyline points="{P(E9WALK)}" fill="none" stroke="#b9a476" stroke-width="30" stroke-linejoin="round"/>')
    A_=[p for p in PLACES if p['id']=='ISL-ARENA'][0]['rect']
    a(f'<rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="{A_[3]-A_[1]}" fill="#e8743b" fill-opacity=".85" stroke="#8a3a12" stroke-width="8"/><rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="90" fill="#f4c49a" stroke="#8a3a12" stroke-width="4"/>')
    a(f'<text class="lbl" x="{A_[0]+20}" y="{A_[1]+200}">ISL-ARENA</text><text class="dt" x="{A_[0]+20}" y="{A_[1]+245}">אולם הכדורסל — arena</text><text class="dt" x="{A_[0]+20}" y="{A_[1]+60}">הרחבה והכניסה</text>')
    a(f'<polyline points="{P(FERRY)}" fill="none" stroke="#6a2c91" stroke-width="130" opacity=".22" stroke-linejoin="round"/><polyline points="{P(FERRY)}" fill="none" stroke="#6a2c91" stroke-width="8" stroke-dasharray="40 20"/>')
    a('<text class="dt" x="5770" y="6620" fill="#6a2c91">המעבורת (074zf) — בתעלה, הגוף 45 × 13 מ׳</text>')
    a(f'<polyline points="{P(SHIP_OLD)}" fill="none" stroke="#c0281e" stroke-width="10" stroke-dasharray="30 20" opacity=".8"/><text class="dt" x="5060" y="6900" fill="#c0281e">היציאה של "צוק הים" עד היום — דרך (5300, 7450)</text>')
    a(f'<polyline points="{P(SHIP_NEW)}" fill="none" stroke="#1d3f8f" stroke-width="135" opacity=".18" stroke-linejoin="round"/><polyline points="{P(SHIP_NEW)}" fill="none" stroke="#1d3f8f" stroke-width="12" marker-end="url(#ar7)"/>')
    a(f'<polyline points="{P(TUG_IN)}" fill="none" stroke="#2c7a3a" stroke-width="6" stroke-dasharray="16 12" marker-end="url(#ar7)"/><polyline points="{P(TUG_BACK)}" fill="none" stroke="#2c7a3a" stroke-width="6" stroke-dasharray="16 12" marker-end="url(#ar7)"/>')
    a('<text class="dt" x="3930" y="7480" fill="#1d3f8f">היציאה החדשה: x 4460 (019j2)</text><text class="dt" x="4740" y="7560" fill="#2c7a3a">"עוז" חוזרת</text>')
    a('<rect x="3926" y="6782" width="788" height="135" fill="#7a5a3a" opacity=".55"/><text class="dt" x="3930" y="6770">"צוק הים" במעגן D8 (79 מ׳)</text>')
    for bx,by,nm in [(4550,6650,'L3-2100'),(3850,6740,'L2-1000'),(3850,7140,'L2-600'),(5990,7092,'L4')]: a(f'<circle cx="{bx}" cy="{by}" r="16" fill="#2fa84f" stroke="#111" stroke-width="3"/><text class="dt" x="{bx+22}" y="{by-14}">{nm}</text>')
    a('<text class="lbl" x="5080" y="7080">E9 — יבשה (5000–5726)</text><text class="dt" x="5770" y="7740">הסוללה — 5 מ׳ (y 7700–7750)</text><text class="dt" x="6200" y="7270">האגנים של F9 — פתוחים לתעלה</text>')
    a('<text class="dt" x="5420" y="7620" fill="#6b5a3a">השביל (חצץ)</text>')
    a('</svg>'); return ''.join(o)
E9_SVG=e9_svg()

# ---- 17.11 ~13:05 — שלב 2ג-2: סדר הבנייה (הצעה) — המעבורת, האגנים, הדרך לאולם ----
def c22_svg():
    o=[]; a=o.append
    a('<svg class="plan" viewBox="4900 6450 2700 1350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="שלב 2ג-2 — שני השלבים">')
    a('<defs><marker id="ar8" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker></defs>')
    a('<rect x="4900" y="6450" width="2700" height="1350" fill="#9fd0ee"/>')
    isl=[[6158,7700],[6180,7610],[6176,7520],[6170,7420],[6182,7320],[6176,7210],[6185,7130],[6195,7095],[6235,7030],[6305,6993],[6430,6975],[6610,6985],[6800,6970],[7000,6990],[7200,6975],[7420,6990],[7600,6970],[7600,7800],[6150,7800]]
    a(f'<polygon points="{P(isl)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="8"/>')
    a(f'<polygon points="{P(E9C+[[6158,7800],[5000,7800]])}" fill="#bfe08f" stroke="#4f7a25" stroke-width="8"/>')
    for b in S13['water']: a(f'<polygon points="{P(b)}" fill="#9fd0ee" stroke="#5a7d96" stroke-width="5"/>')
    # שלב א׳: מילוי הקצה הדרומי של התעלה והדרך מהנמל של F9 אל E9
    a(f'<polygon points="{P([[5726,7530],[6176,7530],[6176,7700],[5726,7700]])}" fill="#e3d9a8" stroke="#8a7a45" stroke-width="6" stroke-dasharray="20 12"/>')
    rd=[[6900,7262],[6890,7560],[6150,7565],[5760,7590],[5665,7560],[5665,7130],[5250,7130],[5250,7250],[5665,7250]]
    a(f'<polyline points="{P(rd)}" fill="none" stroke="#585858" stroke-width="64" stroke-linejoin="round"/><polyline points="{P(rd)}" fill="none" stroke="#f2f2f2" stroke-width="4" stroke-dasharray="26 22"/>')
    A_=[p for p in PLACES if p['id']=='ISL-ARENA'][0]['rect']
    a(f'<rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="{A_[3]-A_[1]}" fill="#e8743b" stroke="#8a3a12" stroke-width="8"/><text class="dt" x="{A_[0]+30}" y="{A_[1]+200}">האולם</text>')
    a('<rect x="5300" y="7020" width="340" height="95" fill="#d8d3c6" stroke="#6b4a2a" stroke-width="5"/><text class="dt" x="5310" y="7075">מסוף המעבורת החדש</text>')
    fer=[[5600,6500],[5470,6620],[5470,6790]]
    a(f'<polyline points="{P(fer)}" fill="none" stroke="#6a2c91" stroke-width="10" stroke-dasharray="40 20" marker-end="url(#ar8)"/><rect x="5405" y="6565" width="130" height="450" fill="#6a2c91" opacity=".25"/>')
    a('<polyline points="5600,6500 5950,7150 5900,7366 6519,7366" fill="none" stroke="#c0281e" stroke-width="8" stroke-dasharray="20 16" opacity=".8"/><text class="dt" x="5980" y="7120" fill="#c0281e">היום: המעבורת אל האגן התחתון</text>')
    a('<rect x="5680" y="7270" width="0" height="0"/><rect x="5410" y="7140" width="240" height="95" fill="#fff" stroke="#555" stroke-width="4"/><text class="dt" x="5420" y="7195">P — 16 (בתוך הלולאה)</text>')
    for (x,y) in [(5700,7360),(5630,7360)]: a(f'<rect x="{x-12}" y="{y-60}" width="24" height="120" rx="6" fill="#fff" stroke="#1f5fd1" stroke-width="5"/>')
    a('<text class="dt" x="5720" y="7330" fill="#1f5fd1">זוג תחנות — "אולם הכדורסל"</text>')
    a('<text class="lbl" x="6200" y="7660" style="font-size:36px">שלב א׳ — הדרך: מהרחבה של הנמל (E69_73) דרומה, מערבה מתחת לאגן, על הסוללה, צפונה אל האולם</text>')
    a('<text class="dt" x="6300" y="6900">שלב ב׳ — סגירת האגנים והתעלה, השדרה (y 7240) לאורך כל האי, המרינה</text>')
    a('</svg>'); return ''.join(o)
C22_SVG=c22_svg()
# ---- 17.11 ~14:05 (island4) — שלב 2ג-2א כמו שנבנה: מסוף המעבורת בחוף הצפוני של E9, הדרך מרחבת הנמל, לולאת המסוף והחניון ----
E9C2=[[5000,7749],[5000,7010],[5100,6994],[5200,6985],[5320,6988],[5395,6991],[5395,7032],[5545,7032],[5545,6997],[5620,7005],[5672,7024],[5722,7052],[5764,7088],[5786,7130],[5790,7200],[5790,7300],[5790,7400],[5792,7458],[5810,7470],[5900,7471],[6000,7471],[6100,7470],[6171,7470]]
def c22a_svg():
    o=[]; a=o.append
    a('<svg class="plan" viewBox="4900 6380 2200 1420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="שלב 2ג-2א — כמו שנבנה">')
    a('<defs><marker id="ar9" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#d9480f"/></marker>'
      '<marker id="ar9b" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker></defs>')
    a('<rect x="4900" y="6380" width="2200" height="1420" fill="#9fd0ee"/><rect x="4900" y="7750" width="2200" height="50" fill="#55606a" opacity=".35"/>')
    isl=[[6171,7470],[6170,7420],[6182,7320],[6176,7210],[6185,7130],[6195,7095],[6235,7030],[6305,6993],[6430,6975],[6610,6985],[6800,6970],[7000,6990],[7100,6985],[7100,7750],[6171,7750]]
    a(f'<polygon points="{P(isl)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="8"/>')
    a(f'<polygon points="{P(E9C2+[[6171,7750],[5000,7750]])}" fill="#bfe08f" stroke="#4f7a25" stroke-width="8"/>')
    # המילוי (הקצה הדרומי של התעלה) והחוף המזרחי החדש — מקווקו
    a(f'<polygon points="{P([[5724,7470],[6171,7470],[6158,7700],[5750,7690],[5724,7600]])}" fill="#e3d9a8" stroke="#8a7a45" stroke-width="5" stroke-dasharray="18 10"/>')
    a(f'<polyline points="{P([[5672,7024],[5700,7060],[5712,7120],[5716,7220],[5718,7300],[5720,7400],[5722,7470]])}" fill="none" stroke="#4f7a25" stroke-width="4" stroke-dasharray="10 10" opacity=".7"/>')
    for b in [[[6080,7290],[6800,7290],[6822,7312],[6822,7448],[6800,7470],[6080,7470]],[[6080,7092],[6522,7092],[6522,7238],[6080,7238]]]: a(f'<polygon points="{P(b)}" fill="#9fd0ee" stroke="#5a7d96" stroke-width="5"/>')
    a('<rect x="6080" y="7470" width="742" height="52" fill="#cfe6a8" stroke="#8a7a45" stroke-width="3" stroke-dasharray="10 8"/>')
    # הכבישים: IS-H1 / H2 / H3 (רחוב מקומי — 9.6 מ׳ + מדרכות) ולולאת המסוף (חד-סטרי 5 מ׳)
    rd=[[6900,7262],[6900,7548],[5690,7548],[5690,7255]]
    a(f'<polyline points="{P(rd)}" fill="none" stroke="#d7d3c8" stroke-width="136" stroke-linejoin="miter"/><polyline points="{P(rd)}" fill="none" stroke="#585858" stroke-width="96" stroke-linejoin="miter"/><polyline points="{P(rd)}" fill="none" stroke="#f2d64b" stroke-width="3" stroke-dasharray="22 16"/>')
    lp=[[5690,7255],[5690,7175],[5100,7175],[5100,7255],[5690,7255]]
    a(f'<polyline points="{P(lp)}" fill="none" stroke="#d7d3c8" stroke-width="90" stroke-linejoin="miter"/><polyline points="{P(lp)}" fill="none" stroke="#585858" stroke-width="50" stroke-linejoin="miter"/>')
    for (x0,y0,x1,y1) in [(5690,7240,5690,7190),(5640,7175,5160,7175),(5100,7190,5100,7240),(5150,7255,5640,7255)]: a(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#d9480f" stroke-width="7" marker-end="url(#ar9)"/>')
    for (x0,y0,x1,y1) in [(6870,7330,6870,7520),(6930,7520,6930,7330),(6800,7572,5760,7572),(5760,7524,6800,7524),(5714,7520,5714,7300),(5666,7300,5666,7520)]: a(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#1d3f8f" stroke-width="5" stroke-dasharray="26 18" marker-end="url(#ar9b)" opacity=".8"/>')
    # החניון בתוך הלולאה
    for (x0,n) in [(5110,11),(5562,3)]:
        a(f'<rect x="{x0}" y="7078" width="{n*25}" height="50" fill="#55595d" stroke="#fff" stroke-width="2"/>')
        for i in range(n+1): a(f'<line x1="{x0+i*25}" y1="7080" x2="{x0+i*25}" y2="7128" stroke="#fff" stroke-width="2"/>')
    a('<rect x="5112" y="7081" width="46" height="45" fill="#2f6fd1" opacity=".6"/><rect x="5337" y="7081" width="46" height="45" fill="#2fa84f" opacity=".6"/><text class="dt" x="5115" y="7065">P — 14 (11 + 3)</text>')
    # האולם, הרחבה, התחנות
    A_=[p for p in PLACES if p['id']=='ISL-ARENA'][0]['rect']
    a(f'<rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="{A_[3]-A_[1]}" fill="#e8743b" fill-opacity=".8" stroke="#8a3a12" stroke-width="6"/><rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="90" fill="#f4c49a" stroke="#8a3a12" stroke-width="3"/>')
    a(f'<text class="lbl" x="{A_[0]+30}" y="{A_[1]+220}">אולם הכדורסל</text><text class="dt" x="{A_[0]+30}" y="{A_[1]+262}">ISL-ARENA (arena)</text><text class="dt" x="{A_[0]+20}" y="{A_[1]+58}">הרחבה והכניסה</text>')
    for (x,y) in [(5753,7410),(5627,7410)]: a(f'<rect x="{x-15}" y="{y-115}" width="30" height="230" rx="6" fill="#fff" stroke="#1f5fd1" stroke-width="5"/>')
    a('<text class="dt" x="5805" y="7400" fill="#1f5fd1">זוג תחנות "אולם הכדורסל"</text><text class="dt" x="5805" y="7432" fill="#1f5fd1">IAR-N / IAR-S — מפרץ בכל צד</text>')
    # המסוף: המזח, הגשרון, הנתיבים, הסככה והקופה; המעבורת עוגנת
    a('<rect x="5380" y="7032" width="262" height="100" fill="#d7d3c8" stroke="#6b4a2a" stroke-width="3"/><rect x="5420" y="7034" width="96" height="98" fill="#585858"/>')
    a('<rect x="5405" y="7026" width="130" height="22" fill="#8c9398" stroke="#222" stroke-width="2"/>')
    a('<rect x="5468" y="7052" width="48" height="96" fill="#bfe3ff" fill-opacity=".55" stroke="#4a90c2" stroke-width="3"/><rect x="5512" y="7070" width="38" height="30" fill="#f2f2f2" stroke="#333" stroke-width="3"/>')
    a('<line x1="5492" y1="7150" x2="5492" y2="7060" stroke="#d9480f" stroke-width="6" marker-end="url(#ar9)"/><line x1="5448" y1="7050" x2="5448" y2="7140" stroke="#1d3f8f" stroke-width="6" marker-end="url(#ar9b)"/>')
    for y in (7076,7124): a(f'<rect x="5483" y="{y-22}" width="18" height="44" rx="4" fill="#ffd8a8" stroke="#8a3a12" stroke-width="2"/>')
    a('<rect x="4900" y="6360" width="2200" height="180" fill="#1d3f8f" opacity=".10"/><line x1="4900" y1="6450" x2="7100" y2="6450" stroke="#1d3f8f" stroke-width="5" stroke-dasharray="30 20"/><text class="dt" x="5600" y="6430" fill="#1d3f8f">הנתיב של אוניות המטען (038f) — y 6450, רוחב 18 מ׳</text>')
    a('<rect x="5405" y="6575" width="130" height="450" rx="30" fill="#6a2c91" opacity=".35" stroke="#6a2c91" stroke-width="5"/><text class="dt" x="5560" y="6640" fill="#6a2c91">המעבורת עוגנת (450 × 130)</text><text class="dt" x="5560" y="6674" fill="#6a2c91">קצה B בשקע של החוף, אל הגשרון</text>')
    a('<polyline points="5000,5900 5470,6370 5470,6575" fill="none" stroke="#6a2c91" stroke-width="8" stroke-dasharray="40 20"/>')
    a(f'<polyline points="{P(FERRY)}" fill="none" stroke="#c0281e" stroke-width="6" stroke-dasharray="20 16" opacity=".75"/><text class="dt" x="5975" y="7065" fill="#c0281e">עד היום: המעבורת בתעלה אל האגן התחתון</text>')
    a('<rect x="4960" y="6800" width="420" height="96" fill="#fff4d6" stroke="#d9480f" stroke-width="4"/><text class="dt" x="4975" y="6837" fill="#b3360f">מסוף המעבורת — החוף הצפוני של E9</text><text class="dt" x="4975" y="6873" fill="#b3360f">שונה מגרסה 6 — לאישור הבעלים</text>')
    # מדרון ההשקה, חניית הנגררים, משרד הנמל
    a('<rect x="5830" y="7390" width="110" height="90" fill="#b4b2a8" stroke="#555" stroke-width="3"/><text class="dt" x="5790" y="7385">מדרון ההשקה</text>')
    a('<rect x="5800" y="7640" width="370" height="104" fill="#8f8f88" stroke="#555" stroke-width="3"/><text class="dt" x="5830" y="7705" fill="#fff">חניית הנגררים</text><rect x="6400" y="7646" width="60" height="50" fill="#c9b48a" stroke="#555" stroke-width="3"/>')
    a('<text class="dt" x="6205" y="7582" fill="#fff">IS-H2 — דרך הנמל, מתחת לאגנים</text><text class="dt" x="6945" y="7420">IS-H1</text><text class="dt" x="5440" y="7290" fill="#d9480f">לולאת המסוף — נגד כיוון השעון</text>')
    a('<text class="dt" x="6215" y="7270">האגנים — פתוחים לתעלה</text><text class="dt" x="5815" y="7230">התעלה — 38 מ׳</text><text class="dt" x="6890" y="7225">E69_73</text>')
    a('</svg>'); return ''.join(o)
C22A_SVG=c22a_svg()
# ---- 17.11 ~14:00 (island4) — שלב 2ג-2ב: ההצעה (ב-1 בלי תלות; ב-2 עם sealife) ----
def c22b_svg():
    o=[]; a=o.append
    a('<svg class="plan" viewBox="3500 6300 3700 1500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="שלב 2ג-2ב — ההצעה">')
    a('<defs><marker id="ar10" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker>'
      '<pattern id="hb1" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="24" height="24" fill="#e9dfb0"/><line x1="0" y1="0" x2="0" y2="24" stroke="#b9a35a" stroke-width="6"/></pattern>'
      '<pattern id="hb2" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="24" height="24" fill="#dfe9c8"/><line x1="0" y1="0" x2="0" y2="24" stroke="#8fae5a" stroke-width="5"/></pattern></defs>')
    a('<rect x="3500" y="6300" width="3700" height="1500" fill="#9fd0ee"/><rect x="3500" y="7750" width="3700" height="50" fill="#55606a" opacity=".35"/>')
    isl=[[6171,7470],[6170,7420],[6182,7320],[6176,7210],[6185,7130],[6195,7095],[6235,7030],[6305,6993],[6430,6975],[6610,6985],[6800,6970],[7000,6990],[7200,6975],[7200,7750],[6171,7750]]
    a(f'<polygon points="{P(isl)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="8"/>')
    a(f'<polygon points="{P(E9C2+[[6171,7750],[5000,7750]])}" fill="#bfe08f" stroke="#4f7a25" stroke-width="8"/>')
    # ב-1: סגירת האגן התחתון והחלק הדרומי של התעלה (מ-y 7290)
    a(f'<polygon points="{P([[5790,7290],[6080,7290],[6800,7290],[6822,7312],[6822,7448],[6800,7470],[5810,7470],[5792,7458]])}" fill="url(#hb1)" stroke="#8a7a45" stroke-width="5"/>')
    # ב-2: סגירת האגן העליון והחלק הצפוני של התעלה; ½ D9 והמרינה
    a(f'<polygon points="{P([[5672,7024],[5790,7000],[6000,6995],[6235,7030],[6195,7095],[6185,7130],[6176,7210],[6182,7290],[5790,7290],[5790,7130],[5764,7088],[5722,7052]])}" fill="url(#hb2)" stroke="#6f8f45" stroke-width="4" stroke-dasharray="16 10"/>')
    a('<rect x="6080" y="7092" width="442" height="146" fill="url(#hb2)" stroke="#6f8f45" stroke-width="4" stroke-dasharray="16 10"/>')
    a(f'<polygon points="{P([[4200,7250],[5000,7250],[5000,7750],[4200,7750]])}" fill="url(#hb2)" stroke="#6f8f45" stroke-width="4" stroke-dasharray="16 10"/>')
    a('<rect x="4230" y="7310" width="560" height="380" fill="#9fd0ee" stroke="#5a7d96" stroke-width="5"/>')
    for x in (4340,4490,4640): a(f'<rect x="{x}" y="7340" width="20" height="320" fill="#9a7a52"/>')
    a('<polyline points="4200,7700 4200,7280 4680,7280" fill="none" stroke="#6b6b6b" stroke-width="18"/>')
    a('<text class="dt" x="4250" y="7740">המרינה ב-½ D9 (ב-2) — 42 מקומות</text>')
    # הכבישים של 2ג-2א (קיימים)
    rd=[[6900,7262],[6900,7548],[5690,7548],[5690,7255]]
    a(f'<polyline points="{P(rd)}" fill="none" stroke="#585858" stroke-width="96" stroke-linejoin="miter"/>')
    lp=[[5690,7255],[5690,7175],[5100,7175],[5100,7255],[5690,7255]]
    a(f'<polyline points="{P(lp)}" fill="none" stroke="#585858" stroke-width="50" stroke-linejoin="miter"/>')
    # ב-2: השדרה y 7240 ממערב לרחבת הנמל עד המרינה
    a('<polyline points="6900,7262 6600,7238 6176,7238 5790,7238 5690,7255 5100,7255 4950,7255 4950,7300" fill="none" stroke="#1d3f8f" stroke-width="22" stroke-dasharray="40 20" opacity=".75"/>')
    a('<text class="dt" x="6200" y="7215" fill="#1d3f8f">ב-2: השדרה (y 7240) — מרחבת הנמל אל המרינה</text>')
    # ב-1: המלון, הבתים, החניה, החוף
    A_=[p for p in PLACES if p['id']=='ISL-ARENA'][0]['rect']
    a(f'<rect x="{A_[0]}" y="{A_[1]}" width="{A_[2]-A_[0]}" height="{A_[3]-A_[1]}" fill="#e8743b" fill-opacity=".75" stroke="#8a3a12" stroke-width="5"/><text class="dt" x="{A_[0]+40}" y="{A_[1]+200}">האולם</text>')
    a('<rect x="5850" y="7310" width="220" height="150" fill="#c06c84" stroke="#6b2a3a" stroke-width="6"/><text class="dt" x="5858" y="7395" fill="#fff">מלון החוף</text>')
    for i in range(6):
        x=6130+i*112; a(f'<rect x="{x}" y="7320" width="64" height="56" fill="#d9a066" stroke="#6b4a2a" stroke-width="4"/><rect x="{x-8}" y="7380" width="80" height="70" fill="#a8cf7a" opacity=".7"/>')
    a('<text class="dt" x="6140" y="7310">שכונת הנמל — 6 בתים (חזית לדרך הנמל)</text>')
    a('<rect x="5800" y="7640" width="370" height="104" fill="#8f8f88" stroke="#555" stroke-width="3"/><text class="dt" x="5815" y="7705" fill="#fff">חניון המלון והאולם — 14 + 4 לנגררים</text>')
    a('<rect x="5030" y="6995" width="350" height="70" fill="#f0e2b0" stroke="#c2a35a" stroke-width="3"/><text class="dt" x="5040" y="6985">חוף המערב (ב-1)</text>')
    a('<rect x="5762" y="7196" width="138" height="60" fill="#b4b2a8" stroke="#555" stroke-width="3"/><text class="dt" x="5800" y="7120">מדרון ההשקה — מלולאת המסוף אל התעלה (ב-1)</text>')
    # המעבורת ואוניית "צוק הים": היום, ובשלב ב-2 (sealife)
    a('<rect x="5405" y="6575" width="130" height="450" rx="30" fill="#6a2c91" opacity=".3"/>')
    a('<circle cx="4250" cy="6990" r="400" fill="none" stroke="#7a5a3a" stroke-width="5" stroke-dasharray="14 10"/><rect x="3856" y="6922" width="788" height="135" fill="#7a5a3a" opacity=".55"/><text class="dt" x="3870" y="6905">"צוק הים" במעגן D8 — עכשיו (4250, 6990); עיגול הסיבוב במקום</text>')
    a('<polyline points="4320,6850 4460,6990 4460,7750" fill="none" stroke="#c0281e" stroke-width="8" stroke-dasharray="26 18" opacity=".6"/><text class="dt" x="4480" y="7150" fill="#c0281e">עד 14:30: היציאה ב-x 4460 (חסמה את ½ D9)</text>')
    a('<polyline points="4250,6990 3800,6990 3640,7080 3565,7300 3560,7750" fill="none" stroke="#1d3f8f" stroke-width="10" marker-end="url(#ar10)"/><text class="dt" x="3620" y="7400" fill="#1d3f8f">נבנה (14:30, באישור המתאם): "עוז" מסובבת אותה במקום ומושכת אותה ב-L2 — ההגעה הפוכה</text>')
    for bx,by in [(3850,7140),(3850,7540),(3850,6740),(4550,6650)]: a(f'<circle cx="{bx}" cy="{by}" r="14" fill="#2fa84f" stroke="#111" stroke-width="3"/>')
    a('<text class="lbl" x="5120" y="6600" style="font-size:34px">ב-1 (מקווקו צהוב) — בלי תלות · ב-2 (מקווקו ירוק) — אחרי היציאה החדשה של "צוק הים"</text>')
    a('</svg>'); return ''.join(o)
C22B_SVG=c22b_svg()
# ---- island5 (17.11 ~16:00): מעבר הסירות מתחת למסילות ב-F6 — מזרחה ובעיצוב חדש (הבעלים 16:15) ----
sys.path.insert(0,'/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools5')
import gen_f6
F6_BEFORE,F6_AFTER,F6_ELEV=gen_f6.F6_BEFORE,gen_f6.F6_AFTER,gen_f6.F6_ELEV
import gen_c22b2
F6_SECTION=(open('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools5/f6_section.html',encoding='utf-8').read()+open('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools5/f6_c22b2.html',encoding='utf-8').read().replace('{C22B2_SVG}',gen_c22b2.C22B2_SVG)).replace('{F6_BEFORE}',F6_BEFORE).replace('{F6_AFTER}',F6_AFTER).replace('{F6_ELEV}',F6_ELEV).replace('{F6_GAME}',open('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools5/game_day.svg',encoding='utf-8').read())
# ---- טבלאות ----
def tr(*c,h=False):
    t='th' if h else 'td'; return '<tr>'+''.join(f'<{t}>{x}</{t}>' for x in c)+'</tr>'
places_tbl=''.join(tr(str(i),html.escape(p['he']),p['zone'],'כן' if p['focal'] else '—') for i,p in enumerate(PLACES,1))
stops_tbl=''.join(tr(str(i),s['line'],html.escape(s['name']),f"{s['at'][0]}, {s['at'][1]}",str(s['s_m']),s['kind']) for i,s in enumerate(stops,1))
lz=C['land_m2']
land_tbl=''.join(tr(z,f"{lz[z]:,}",f"{lz[z]/C['zone_full_m2']*100:.0f}%") for z in ['D9','E9','F9','G9','H9','H8'])
cb=C['cable'];trn=C['train']
INV=[
 ('היבשה והים','019h_S13_data.js: S13D.coast / islandPoly / water · 061a_S13_land.js (חור בטבעת הים, isWater)','מורחבת: E9, ‏H8, ‏½ D9; האגנים הישנים של F9 נסגרים; הנמל עובר לחוף הצפוני'),
 ('ההר, היער, הפסגה, הכפר והאכסניה','S13D.contours / nature / lots (IS-VILLAGE, ‏IS-HOSTEL, ‏IS-SUMMIT) · 019i_S13_draw.js','נשארים (הבעלים לא העיר עליהם) — הכפר מקבל רחוב וחנות'),
 ('גשר האי והמפתח המתרומם','019h2_S13_bridge2.js (D‑634) · 038f_S13_live.js (מחזור הפתיחה, האונייה) · 016: BR-I1…BR-I14','נשאר בדיוק כמו שהוא (כלל 5); הנחיתה BR-L ‏→ כיכר האי IL'),
 ('כיכר האי IL','016: RB2.IL ‏(8330, 7320), ‏xw לשלוש הזרועות','נשארת — הזרוע המערבית = שדרת האי; הזרוע המזרחית = דרך התחנה'),
 ('דרכי האי','016: IS-W1…W7, ‏IS-E1/E1B/E2, ‏IS-L1…L5 (הלולאה של ST-21), ‏E69_73 / E880_760 (ראשי סיבוב) · 074w (s16c) · 074l7 (ISE-0)','מוחלפות: שדרה אחת 1+1 עם מפרצים, שתי לולאות סופיות חד-סטריות; בלי ראשי סיבוב ובלי ISE-0'),
 ('קו 5 (הקואץ׳)','074l_line5_coach.js (הצייר — Setra 12.2 מ׳) · 074l5_line5_run.js (LINE5B, ‏ST-21/ST-22) · 038j (סככות)','הצייר והמנוע נשארים (כלל 19א); המסלול והתחנות באי — חדשים; קו 5א חדש'),
 ('תחנת האי והרכבת','S13D.sa / sb, ‏S13_PLAT (רציף 100 מ׳) · 040b_S16c_island_train.js (RL-PS-02 — קרון אחד)','הרציף נשאר (מתאים גם ל-5); הרכבת — 4 קרונות בפס א׳ (נבנה); מסוף המשא — בפס ב׳ של התחנה'),
 ('הרכבל','038i_S13_life.js: CB / cabPose / cabDraw (jig-back, שני תאים, 79 מ׳)','משודרג: לולאה סובבת, 10 תאים, 3 תחנות, 183 מ׳ — שלב 1'),
 ('המעבורת','074zf_ferry.js (D‑678, 450 × 130) · 049 A6_FERRY · S14D.ferry_new','נמל האי עובר לחוף הצפוני של F9 (תלות: sealife — ferry2)'),
 ('אסדת הגז וספינת האספקה','021u_H8_s10b_rig.js (RIG, ‏SV-RIG מ-E6, ‏PIPE)','האסדה נשארת; מזח אספקה ותחנת קבלת גז ב-H8 (לאישורך: הבית של SV-RIG עובר ל-H8)'),
 ('המגדלור והמנחת','S13_LIGHT ‏(9355, 6975) · IS-HELI · 038i (LH, ‏heliPose)','המגדלור עובר לכף של H8 מול המפתח; המנחת — בתוך לולאת המזרח'),
 ('נתיבי השיט','S13D.lane5 · S14D.lanes L1–L4 · S14D.ship (מגיעה מדרום ב-x 3560)','מזרח ↔ מערב; אחרי D — דרום־מערב בין B ל-C (תלות: sealife)'),
 ('המקומות (F)','038j_S13_places.js (IS-STATION, ‏IS-SHOP, ‏IS-CABLE-LOW/TOP, ‏IS-HELI, ‏IS-ST21/22 …)','16 מקומות עם תוכן אמיתי (טבלה למטה)'),
]
inv_tbl=''.join(tr(html.escape(a),html.escape(b),html.escape(c)) for a,b,c in INV)
cb0=C['cable']['cabins'];cl0=C['cable']['one_way_m']
PAGE=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>האי מאפס — תוכנית</title>
<style>
:root{{--bg:#f6f4ee;--fg:#1d2228;--mut:#5b6470;--card:#fff;--line:#d9d4c7;--acc:#1f5fd1}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16191d;--fg:#e8e6e1;--mut:#a6adb6;--card:#1f2328;--line:#353a41;--acc:#7aa7ff}}}}
:root[data-theme="dark"]{{--bg:#16191d;--fg:#e8e6e1;--mut:#a6adb6;--card:#1f2328;--line:#353a41;--acc:#7aa7ff}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 "Segoe UI",Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:16px}}
h1{{font-size:24px;margin:8px 0 4px}} h2{{font-size:19px;margin:26px 0 8px;border-bottom:2px solid var(--line);padding-bottom:4px}}
.sub{{color:var(--mut)}} .card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:10px 0}}
.plan{{width:100%;height:auto;background:#9fd0ee;border-radius:8px;border:1px solid var(--line)}}
table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{border:1px solid var(--line);padding:5px 7px;text-align:right;vertical-align:top}} th{{background:rgba(127,127,127,.12)}}
.wrap{{overflow-x:auto}} .k{{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:-2px;margin-left:5px}}
.big{{font-size:22px;font-weight:700;color:var(--acc)}} .grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}}
.ok{{color:#178a54;font-weight:700}} ul{{margin:6px 0;padding-right:20px}}
svg .rd{{fill:none;stroke:#585858;stroke-width:88;stroke-linejoin:round;stroke-linecap:round}} svg .rd.lp{{stroke:#7a5a3a}} svg .rd.lo{{stroke-width:60;stroke:#6e6e6e}}
svg .rdc{{fill:none;stroke:#f2f2f2;stroke-width:4;stroke-dasharray:30 30}} svg .trk{{fill:none;stroke:#a07a4a;stroke-width:22;stroke-dasharray:24 12}}
svg .pl{{fill:rgba(106,44,145,.06);stroke:#6a2c91;stroke-width:6;stroke-dasharray:24 12}} svg .pn,svg .sn{{fill:#fff;font:700 38px Arial;text-anchor:middle}}
svg .rig{{fill:#d64a3c;stroke:#6b120a;stroke-width:8}} svg .pier{{fill:#9a9a94;stroke:#555;stroke-width:4}} svg .pont{{fill:#f4f1e6;stroke:#6b6b60;stroke-width:4}}
svg .plat{{fill:#d8d3c6;stroke:#6b4a2a;stroke-width:4}} svg .yard{{fill:rgba(160,120,60,.15);stroke:#6b4a2a;stroke-width:5;stroke-dasharray:18 10}}
svg .grid{{stroke:#203040;stroke-width:4;stroke-dasharray:30 30;opacity:.45}} svg .zid{{font:700 60px Arial;fill:#203040;opacity:.55}} svg .zid.zon{{fill:#b3360f;opacity:.95}}
svg .dt{{font:600 26px Arial;fill:#1d2228}} .det{{width:100%;height:auto;margin:8px 0;border:1px solid var(--line);border-radius:8px}} svg .lbl{{font:600 44px Arial;fill:#1d2228}} svg .lane{{font:600 46px Arial;fill:#1d3f8f}} svg .zh{{font:700 46px Arial;fill:#b3360f}}
</style></head><body><main>
<h1>האי מאפס — התוכנית והחישוב (D‑694)</h1>
<div class="sub">טורבו סיטי · סבב 17.11.2026 · הסוכן island · ציור בלבד (SVG בקוד) — הבנייה מתחילה במקביל לבקר התוכניות (כלל 20) · <b>גרסה 13 (island5, ‏16:35): סעיפים 0ג ו-0ד — נבנו (0ג — מעבר השיט ב-F6; 0ד — המרינה, סגירת האגן העליון והשדרה; רחוב המרינה — הבא) · גרסה 12 (16:05; ‏16:12 — המראה במשחק, מהקוד; ‏16:17 — סעיף 0ד: שלב 2ג-2ב-2, המרינה ב-½ D9, האגן העליון והשדרה — ההצעה): סעיף 0ג — מעבר הסירות מתחת למסילות ב-F6 (הבעלים 16:15): מזרחה ובעיצוב חדש — ההצעה</b> · גרסה 11 (13:57, לפי TZ=Asia/Jerusalem — island4): סעיף 0ב-2 — שלב 2ג-2ב, ההצעה (ב-1 בלי תלות, ב-2 עם sealife) · גרסה 10 (13:40): סעיף 0ב-1 — שלב 2ג-2א נבנה (מסוף המעבורת ב-E9, הדרך אל האולם, לולאת המסוף, החניון והתחנות) · גרסה 9 (13:05): סעיף 0ב — שלב 2ג-2, סדר הבנייה (הצעה) · גרסה 8 (12:45): הבעלים 12:55 — לולאת המזרח הפוכה (סעיף 0, החיצים החדשים בכתום) · גרסה 7 (12:40): סעיף 0א — שלב 2ג-1 נבנה (היבשה של E9 לפני האולם, הסוללה, היציאה החדשה של "צוק הים") · גרסה 6 (10:37): הבעלים (ההודעה של המתאם) — סעיף 0 (הצומת המרומזר במקום הכיכר, המפתח באמצע, ההר מערבה, הפסגה — התחנה האחרונה של הרכבל) · גרסה 5 (09:45): מעל גרסה 4 (09:05) — רכבת המשא עוברת לפס הדרומי (סעיף 6), פארק החוף של H8 נבנה, קו 5א — כבוי כברירת מחדל (סעיף 9)</div>

<div class="card"><b>בקצרה:</b> האי גדל ל-<b>5.5 אזורים</b> — E9, ‏F9, ‏G9, ‏H9, ‏H8, ומרינה על <b>החצי המזרחי של D9</b> (<b>בפועל — {C['zones_equiv']:.1f} אזורים של יבשה ומים מוגנים</b>: ‏H8 רק בדרום, כי האסדה נשארת; לאישורך). הגשר המתרומם, ההר, היער והכפר נשארים; כל התחבורה באי מתוכננת מחדש:
שדרה אחת לכל אורך האי (1+1) עם <b>{C['stops_pairs']} זוגות של תחנות</b> (מפרץ בכל צד) ו-<b>{C['stops_terminal']} תחנות סופיות</b> בלולאות חד-סטריות — <b>{len(stops)} תחנות, {C['stops_bays']} מפרצים</b> (המינימום של הבעלים: 4).
רכבת נוסעים של {trn['cars']} קרונות (נבנתה), רכבת משא עם רציף פריקה וחצר משאיות בפס ב׳ של תחנת האי, ורכבל סובב של {cb0} תאים בשלוש תחנות ({cl0} מ׳ — פי 2.3 מהיום; נבנה).</div>

<h2>0. הבעלים 17.11 (בהודעות של המתאם — "10:45", ‏"12:05") — גרסה 6: הצומת, המפתח המתרומם, ההר, הרכבל ואולם הכדורסל</h2>
<div class="card"><b>מילה במילה:</b> "באי ובכל העיר בכבישים ראשים לא אהבתי את הכיכרות הם עדיין לא מספיק מסונכרנים למנוע הרכבים וגורמים לבעיות … ואפילו יותר גרוע הכיכר באי שם חייב רמזור כניסה / הגשר המתרומם צריך יותר באמצע פחות קרוב לאי / ההר באי צריך לזוז ולהתרחב מערבה הרכבל תחנה אחרונה בפסגה"; ו-"אני רוצה באי איצטדיון כדור סל עם ליגה וקבוצות כמו בכדור רגל עם משחקים חיים" (12:05 — הבנייה של האולם, הליגה והמשחק — הסוכן arena; כאן — המקום).</div>
<div class="wrap">{OWNER_SVG}</div>
<div class="card"><ol>
<li><b>כיכר האי ← צומת מרומזר</b> (הציור למטה): שלוש זרועות — הגשר מצפון (הרחוב הראשי, עם דרך התחנה), דרך הנמל והכפר ממערב (המשנית — T-rule), דרך התחנה לדרום-מזרח. המנגנון הקיים בלבד: SIGNAL_NODE_IDS ‏+ P523 (מצב, T-rule) ‏+ TrafficSignalController — שלב ירוק לגשר ↔ התחנה, שלב לפנייה שמאלה מוגנת, שלב לדרך המערבית, ושלב להולכי רגל; קו עצירה ומעבר חצייה בכל זרוע; העיגול, האי והמזרקה של הכיכר יוצאים מהציור (RB2.IL). <b>בונים עכשיו</b> (שלב 6א).</li>
<li><b>המפתח המתרומם — באמצע:</b> היום (019h2, ‏D‑634: ‏104 מ׳, s 90–1130) המרכז שלו 155 מ׳ מראש הגשר ו-119 מ׳ מחוף האי לאורך הגשר, והקצה הדרום-מזרחי 33 מ׳ מהחוף של האי. זז {OW_DS//10} מ׳ לאורך ציר הגשר לכיוון העיר: המרכז ({OW_LIFT_C[0]:.0f}, {OW_LIFT_C[1]:.0f}) במקום ({OW_LIFT_C0[0]:.0f}, {OW_LIFT_C0[1]:.0f}) — 137 / 137 מ׳, בדיוק באמצע הדרך במים; הקצה הקרוב לאי — 44 מ׳ מהחוף. <b>מה זה מזיז:</b> ה-S של ראש הגשר מתקצר (הקטע הישר של הסיפון מתחיל ב-s ≈ −110 במקום 0 — 019h2, הכלי gen_s13b.py), מגדלי המפתח והמשקולות, המחסומים והאותות לפני המפתח (בכביש ובמסילה), נתיב השיט הראשי עובר מתחת למרכז החדש (הקו הכחול), והעמודים של הגשר לא בתעלה. <b>שלב 6ב</b> — אחרי 6א; תיאום עם sealife (האוניות והגוררות בנתיב).</li>
<li><b>ההר — מערבה ורחב יותר:</b> הפסגה עוברת ל-({OW_SUMMIT[0]}, {OW_SUMMIT[1]}) — 87 מ׳ מערבה; קווי הגובה מתרחבים פי {OW_KX} במזרח-מערב (מ-x ≈ 5660 עד 8230 — האולם והמרינה ב-E9 נשארים במישור), על האגנים של F9 שנסגרים בשלב 2ג; הכפר והאכסניה נשארים — על המדרון הצפוני והמזרחי; היער — על כל ההר. <b>שלב 6ג</b> — עם שלב 2ג (E9 והנמל בחוף הצפוני).</li>
<li><b>הבעלים (12:05) — אולם כדורסל באי, עם ליגה ומשחקים חיים (הסוכן arena):</b> המקום השמור — <b>ISL-ARENA, ‏E9, המלבן [5220, 7300, 5590, 7690]</b> (37 × 39 מ׳): מגרש 28 × 15 מ׳, יציעים לכ-800 צופים בשני הצדדים הארוכים, לובי וקופה ברחבה מול השדרה (y 7300–7390). זוג תחנות של קו 5 ממש מול הכניסה (x 5400, ‏"אולם הכדורסל · חוף המערב"); החניה — חניון האולם, המלון והחוף (P-HOTEL, ‏20, ברחוב ה-U ממזרח), ובימי משחק גם חניון המרינה (16). המלון זז מזרחה ל-[5860, 7300, 6090, 7690]. היבשה של E9 — שלב 2ג (island); עד אז הבניין רק בתוכנית.</li>
<li><b>הבעלים (12:55) — לולאת המזרח הפוכה:</b> "באי איפה ש-16 הכיוון הפוך בתנועה — שם צריך להמשיך ישר לעשות את הסיבוב עם הכביש ולהשתלב בנתיב היורד בחזור". הלולאה סביב המנחת (ליד 15–19 ותחנה 9) — עכשיו נגד כיוון השעון במפה: מדרך המזרח (x 9380) ממשיכים <b>ישר צפונה</b> בצלע המזרחית, מערבה בצלע הצפונית (התחנה הסופית של 5א — הרציף מימין, בצד הצפוני), דרומה בצלע המערבית, מזרחה בצלע הדרומית — ומשתלבים <b>בנתיב היורד</b> של דרך המזרח (ימינה, בלי לחצות נתיב). החיצים החדשים — בכתום בציור הראשי (סעיף 1) ובציור למטה. במשחק: 016 — IS-EL1–EL5 הפוכים, הבדיקה isl17_east_road_and_loop — נגד כיוון השעון.</li>
<li><b>הרכבל — התחנה האחרונה בפסגה:</b> תחנת העמק (ליד הצומת) ← תחנת היער (התחנה העליונה של היום — עכשיו באמצע המדרון) ← <b>הפסגה — התחנה האחרונה</b>, במקום תחנת הנמל של היום (6760, 7620): הקפה והתצפית עוברים לשם. אותו קו סובב — 10 תאים, 183 מ׳. <b>שלב 6ג</b>, יחד עם ההר.</li>
</ol></div>
<h3>הצומת המרומזר במקום הכיכר — מבט על (קנה מידה אמיתי, 10 פיקס׳ = 1 מ׳)</h3>
<div class="wrap">{OWNER_J}</div>
<h2>0א. שלב 2ג-1 — נבנה (17.11 ~12:40): היבשה של E9 לפני האולם — כמו במשחק</h2>
<div class="card">היבשה של E9 בין x 5000 ל-5726 (החוף הצפוני ב-y 6985–7010, כמו בתוכנית), עם המקום השמור לאולם הכדורסל, וסוללה של 5 מ׳ לאורך הקצה הדרומי עד F9 — מתחת לאגן התחתון ולמגלשת הסירות.
עד שלב 2ג-2 (סגירת האגנים של F9 והמעבורת לחוף הצפוני) — <b>תעלה של 45 מ׳ בין E9 ל-F9</b>: המעבורת ממשיכה בנתיב שלה אל האגן התחתון, ושני האגנים פתוחים לים. <b>היציאה של "צוק הים"</b> (עד היום — קשת דרומה דרך (5300, 7450), על היבשה החדשה)
עוברת לנתיב x 4460: סיבוב חד ימינה מהמעגן בגרירה של "עוז", ודרומה ממערב ליבשה (22 מ׳ ויותר מהחוף בכל רגע, הגוף כולו); "עוז" מגיעה מצפון-מזרח וחוזרת צפונה ב-x 4700–4800. כשהמרינה ב-½ D9 תיבנה — היציאה מערבה דרך L2 (sealife).
השביל (חצץ) — מקצה דרך הנמל של F9, לאורך מגלשת הסירות והסוללה, עד הרחבה של האולם. הכבישים, השדרה והתחנות — שלב 2ג-2.</div>
<div class="wrap">{E9_SVG}</div>
<h2>0ב. שלב 2ג-2 — סדר הבנייה (הצעה, 13:05): המעבורת, האגנים והדרך לאולם ברכב</h2>
<div class="card"><b>מה מצאתי:</b> המעבורת של היום (074zf, הצד של האי — g.G8, ‏boardPath / offPath, ‏DOCK) קשורה בקואורדינטות קבועות לנמל של F9: התור ב-IS-WAIT (x 6835–7140), הירידה ב-x 6878 מהרחבה E69_73, הרציף הצף IS-FERRY-LANDING (022) והנקודה G8-FERRY (022 / 049 / 038g / 074d). כל עוד היא נכנסת לאגן התחתון דרך התעלה — אי אפשר לסגור את התעלה והאגנים, ואין דרך לרכב אל E9.
<b>ההצעה — שני שלבים, כל אחד עם שורת "מוכן למיזוג" משלו:</b>
<ol><li><b>שלב א׳ (2ג-2א) — מגיעים לאולם ברכב:</b> המסוף של המעבורת עובר לחוף הצפוני של <b>E9</b> (מסוף חדש מול האולם, על יבשה ריקה — בלי הקואורדינטות הישנות; המעבורת מגיעה מ-(5600, 6500) ישר דרומה); הקצה הדרומי של התעלה מתמלא (y 7530–7700); דרך חדשה מהרחבה של הנמל (E69_73 — כבר לא ראש סיבוב) דרומה בתוואי של דרך הנמל המצוירת, מערבה מתחת לאגן התחתון, על הסוללה, וצפונה אל האולם; לולאה חד-סטרית קטנה מצפון לאולם עם חניון (16) ותור המעבורת; זוג תחנות של קו 5 "אולם הכדורסל". האגנים נשארים (פתוחים לתעלה מצפון).</li>
<li><b>שלב ב׳ (2ג-2ב):</b> סגירת שני האגנים והתעלה, השדרה (y 7240) מהצומת עד E9, רחובות ה-U, השכונה, המלון והחוף, והמרינה ב-½ D9 (עם היציאה של "צוק הים" דרך L2 — sealife).</li></ol>
<b>לאישורך:</b> בתוכנית (גרסה 6) המסוף על החוף הצפוני של F9 (x 6250–6750); בהצעה — על החוף הצפוני של E9, ליד האולם. הסיבה: כך בונים אותו לפני סגירת האגנים, והדרך לאולם נפתחת בשלב אחד. בשלב ב׳ החוף של F9 נשאר לרציף הדייגים ולחוף.</div>
<div class="wrap">{C22_SVG}</div>
<h3>0ב-1. שלב 2ג-2א — נבנה (island4, ‏17.11 ~13:40): מגיעים לאולם הכדורסל ברכב — כמו במשחק</h3>
<div class="card"><b>מסוף המעבורת — בחוף הצפוני של E9</b> (הכרעת המתאם; <b>שונה מגרסה 6 — לאישור הבעלים</b>: שם המסוף היה בחוף הצפוני של F9): מעגן בשקע של החוף (15 × 4 מ׳) שהמעבורת נכנסת אליו בניצב — מגיעה מ-(5000, 5900) ← (5470, 6370) וישר דרומה, קצה B אל הגשרון (בלי סיבוב ובלי נסיעה לאחור, כמו ב-A6). למה בשקע ולא על מזח: הקצה הצפוני של המעבורת העוגנת (y 6575) חייב להישאר מדרום לנתיב של אוניות המטען (038f — y 6450, רוחב 18 מ׳: עד y 6540). במסוף שני נתיבים: <b>עלייה</b> במזרח (x 5492, צפונה — 2 מקומות המתנה מתחת לסככה שקופה, D‑622, והקופה לידם) ו<b>ירידה</b> במערב (x 5448, דרומה) — ימינה אל הצלע הצפונית של הלולאה; הנתיבים לא נחתכים. הולכי רגל עולים מהרצועה בצד המזרחי של הגשרון (F).
<br><b>הדרך:</b> מרחבת הנמל E69_73 דרומה (IS-H1 — בתוואי של דרך הנמל המצוירת), מערבה מתחת לאגן התחתון ועל הקצה הדרומי של התעלה שמולא (IS-H2), וצפונה לאורך האולם (IS-H3) — רחוב מקומי 1+1 עם מדרכות; בסוף — <b>לולאת המסוף</b> חד-סטרית נגד כיוון השעון במפה (IS-HL1–HL4, כמו לולאת המזרח שהבעלים ביקש: ממשיכים ישר צפונה, ובחזרה — ימינה אל הנתיב היורד), עם <b>חניון של 14</b> לאורך הצלע הצפונית שלה (11 ממערב למסוף ו-3 ממזרח לו; 2 לנכים, 2 לטעינה) ו<b>זוג תחנות "אולם הכדורסל"</b> (מפרץ בכל צד של IS-H3; קו 5 של התוכנית יעצור בהן כשהשדרה תיבנה, 2ג-2ב).
<br><b>מה זז:</b> החוף המזרחי של E9 — ל-x 5790 (התעלה 38 מ׳ במקום 45, והאגנים פתוחים אליה); האגן התחתון — עד y 7470 (המעבורת כבר לא נכנסת; המעגן הישן נשאר לסירות); מדרון ההשקה — אל התעלה, וחניית הנגררים ומשרד הנמל — מדרום לדרך; הקופה והסככה (IS-WAIT) — במסוף החדש. במשחק: 016 (הצמתים ISH-1…6 והקטעים), ‏019h5 (היבשה, המסוף, הציור), ‏074zf (המעבורת — הצד של האי), ‏074zf2 (המקומות, התחנות, הבדיקה isl17_e9_road). הספירות: 135 צמתים / 148 קטעים.</div>
<div class="wrap">{C22A_SVG}</div>
<h3>0ב-2. שלב 2ג-2ב — ההצעה (island4, ‏17.11 ~13:57): שני חלקים, כי החלק השני תלוי ב-sealife</h3>
<div class="card"><b>מה מצאתי:</b> שני האגנים של F9 והתעלה הם הבית של הסירות של האי (המעגן IS-BOATS — 6 סירות, סירת הדייג שיוצאת וחוזרת, סירות החתירה — 038i: moored / fishBoat / rowBoats); אי אפשר לסגור אותם לפני שיש מרינה. המרינה בתוכנית — ב-½ D9 (x 4230–4790), אבל אוניית המטען "צוק הים" יוצאת היום מהמעגן ב-D8 דרומה בנתיב x 4460 (019j2 — הוו של 019k), בדיוק דרך ½ D9. ההגעה שלה — כבר היום ב-L2 (x 3560, מדרום): היציאה יכולה להיות ההגעה הפוכה — "עוז" מסובבת אותה במעגן ומושכת אותה מערבה אל L2. זה התחום של sealife (019k: התסריט של האונייה והגוררת) — דרך המתאם.
<ol><li><b>ב-1 (בלי תלות) — נבנה (try8005, ‏14:00; בבדיקה):</b> האגן התחתון — שכבר ריק (המעבורת עברה ל-E9) — והחלק הדרומי של התעלה (מ-y 7290) נסגרים. על היבשה החדשה, בין רציף האגנים לדרך הנמל: <b>מלון החוף</b> (22 × 15 מ׳, 4 קומות, ליד האולם), <b>שכונת הנמל</b> — 6 בתים עם חזית וגינה מול דרך הנמל (IS-H2), <b>חניון המלון והאולם</b> (14 ו-4 לנגררים, מדרום לדרך — במקום חניית הנגררים), מדרון ההשקה — מלולאת המסוף אל החלק הצפוני של התעלה, ו<b>חוף המערב</b> בצפון-מערב E9. האגן העליון והסירות — נשארים, פתוחים לתעלה מצפון.</li>
<li><b>ב-2 (היציאה של "צוק הים" ב-L2 — נבנתה, try8009, בבדיקה):</b> ½ D9 — יבשה עם <b>המרינה</b> (42 מקומות, שובר גלים, משרד ומספנה), הסירות עוברות אליה; האגן העליון והחלק הצפוני של התעלה נסגרים; <b>השדרה</b> (y 7240) מרחבת הנמל, לאורך האולם (הצלע הדרומית של לולאת המסוף נעשית דו-סטרית) ועד המרינה; ואז קו 5 אל המרינה (תחנות 1–6).</li></ol>
<b>לאישורך:</b> הסדר ב-1 ← ב-2; השכונה עם חזית לדרך הנמל (במקום רחוב U מהשדרה — השדרה מגיעה רק ב-2; ה-U יתווסף אז מצפון לבתים). <b>שימו לב (6ג):</b> הפסגה החדשה (6790, 7505) — 4 מ׳ מצפון לדרך הנמל IS-H2 (y 7548); לכן 6ג אחרי ב-2: השדרה מחליפה את IS-H2, והבתים מקבלים כניסה מהשדרה.</div>
<div class="wrap">{C22B_SVG}</div>
{F6_SECTION}

<h2>1. הציור — מבט על</h2>
<div class="wrap">{SVG}</div>
<div class="card grid2">
<div><span class="k" style="background:#cfe6a8;border:2px solid #6f8f45"></span>היבשה החדשה · <span class="k" style="border:2px dashed #b0412e"></span>קו החוף של האי הישן</div>
<div><span class="k" style="background:#585858"></span>שדרת האי 1+1 · <span class="k" style="background:#7a5a3a"></span>לולאה סופית חד-סטרית</div>
<div><span class="k" style="background:#1f5fd1"></span>תחנה של קו 5 · <span class="k" style="background:#178a54"></span>תחנה של קו 5א · מלבן לבן = מפרץ</div>
<div><span class="k" style="background:#c0281e"></span>הרכבל — 3 תחנות, 10 תאים · <span class="k" style="background:#6b4a2a"></span>מסילה</div>
<div><span class="k" style="background:#1d3f8f"></span>נתיבי שיט · <span class="k" style="background:#f0c24a"></span>המפתח המתרומם</div>
<div><span class="k" style="background:#6a2c91"></span>מקום עם F (מספר ← הטבלה בסעיף 5)</div>
</div>

<h2>2. מה מצאתי (כלל 16 / 19) — מה נשאר, מה משודרג, מה יוצא</h2>
<div class="wrap"><table>{tr('מה','איפה בקוד','בתוכנית החדשה',h=True)}{inv_tbl}</table></div>
<div class="card"><b>מה שבור היום (לא מתקנים — יוצא עם התכנון, D‑694):</b> קו 5 כבוי כברירת מחדל — נעילה ב-ISE-0 / בלולאה של ST-21; ‏ST-22 בלי דרך מהעיר (IS-W6/W7 בכיוון ‎-1); ראשי סיבוב שצוירו כעיגולים קבועים; הרכבל — 2 תאים בלבד (cabPose נותן 2 מיקומים); הרכבת — קרון אחד; אין רכבת משא לאי (D‑23).</div>

<h2>3. החישוב — כמה תחנות צריך</h2>
<div class="grid2">
<div class="card"><div class="big">{C['land_total_m2']:,} מ"ר</div>יבשה ומים מוגנים באי החדש (אזור מלא = {C['zone_full_m2']:,} מ"ר) · השדרה: {C['spine_len_m']} מ׳ · דרך המזרח: {C['east_len_m']} מ׳</div>
<div class="card"><div class="big">{len(stops)} תחנות · {C['stops_bays']} מפרצים</div>{C['stops_pairs']} זוגות (מפרץ בכל צד) + {C['stops_terminal']} סופיות · כיסוי ההליכה: <span class="ok">{C['coverage_pct']}%</span> מהשטח הבנוי · כל המוקדים מכוסים · קו 5: תחנות 1–6, קו 5א: תחנות 7–9</div>
<div class="card"><div class="big">65–70 מ׳</div>המרחק בין זוגות תחנות בעיר (חציון 65, ממוצע 70 — 19 זוגות ב-city_plan.bus). זה תקן ההליכה של המשחק, ולפיו האי.</div>
</div>
<div class="card"><b>השיטה (אפשר לבדוק — tools/plan_calc.py):</b>
<ul><li><b>רדיוס הליכה 60 מ׳</b> — כל נקודה בשטח הבנוי (רשת של 5 מ׳ על כל המגרשים) צריכה תחנה במרחק הזה; כמו בעיר (מחצית המרווח הממוצע + הדרך הצידה).</li>
<li><b>מוקד — עד 40 מ׳</b> מהכניסה שלו: המרינה, המלון והחוף, המעבורת, שכונת הנמל, הכפר, האכסניה, תחנת האי, הרכבל (שתי התחנות התחתונות), המנחת, מסוף המשא, בסיס האסדה.</li>
<li><b>תחנת המעבר</b> — כל קו עוצר ליד תחנת הרכבת והרכבל (עד 45 מ׳, כולל המעבר בכיכר).</li>
<li><b>בין תחנות:</b> לפחות 45 מ׳ (שני מפרצים של 23 מ׳), ולא יותר מ-90 מ׳ <b>לאורך הדרך</b> (1.3 × הממוצע בעיר); לפחות 15 מ׳ מצומת עם מעבר חצייה, 8 מ׳ מכניסה של דרך שירות (דרך העפר לפסגה — בלי מעבר חצייה), ו-26 מ׳ ממרכז הכיכר.
 <b>3 חריגים מוצדקים</b> (אין שם מקום חוקי לזוג, וכל המגרשים בקטע — עד 60 מ׳ מתחנה): תחנה 5 ← המרינה (6): ‏195 מ׳ לאורך הדרך, מהם 122 מ׳ בלולאה החד-סטרית — בקו ישר 90 מ׳; תחנה 7 ← 8 ‏({stops[7]['s_m']-stops[6]['s_m']} מ׳) ו-8 ← 9 ‏({stops[8]['s_m']-stops[7]['s_m']} מ׳) — לאורך סוף המסילה וחצר המשאיות, בלי מגרשים שצריכים תחנה.</li>
<li><b>זוגות:</b> על דרך דו-סטרית — מפרץ בכל צד (40 + 150 + 40 פיקס׳, עומק 30 — כמו בעיר); בלולאה הסופית — רציף אחד שבו יורדים ועולים.</li>
<li>רק לפי האורך (בלי מוקדים) היו יוצאים {C['by_spacing_only']} זוגות; לפי מוקדים וכיסוי — {C['stops_pairs']} זוגות + {C['stops_terminal']} סופיות.</li></ul></div>
<div class="wrap"><table>{tr('#','קו','התחנה','x, y','מ׳ מתחילת הקו באי','סוג',h=True)}{stops_tbl}</table></div>
<div class="wrap"><table>{tr('אזור','מ"ר','מהאזור',h=True)}{land_tbl}</table></div>
<div class="card"><b>H8 — רק הדרום (29%):</b> אסדת הגז נשארת במקום (D‑595 / D‑618) במלבן [8860, 6160, 9090, 6340], והלפיד מגיע עד (9210, 6468) בגובה 50 מ׳. החוף של H8 נמתח 27 מ׳ דרומה מהאסדה ו-14 מ׳ מקצה הלפיד; נתיב השיט מהמזרח (y 5800) נשאר 30 מ׳ ויותר מהיבשה. <b>לאישורך:</b> אם הבעלים רוצה את כל H8 יבשה — האסדה זזה צפונה ל-H7.</div>

<h2>4. הקווים</h2>
<div class="card"><b>קו 5</b> (הקואץ׳ מהעיר, 12.2 מ׳): ‏E3 ← הגשר ← כיכר האי ← שדרת האי מערבה: תחנות 1–5 ← לולאת המרינה (תחנה 6, סופית) ← בחזרה באותה דרך. <br>
<b>קו 5א</b> (אותו קואץ׳, מהעיר): ‏E3 ← הגשר ← כיכר האי ← דרך התחנה: תחנה 7 ← מסביב לסוף המסילה: תחנה 8 ← לולאת המזרח סביב המנחת, נגד כיוון השעון (תחנה 9, סופית — הרציף מימין, בצד המנחת) ← בחזרה. <br>
<b>כשהמפתח מורם:</b> הקואץ׳ והמכוניות עוצרים בקו העצירה, 9 מ׳ לפני המגדל של המפתח, בשני הצדדים (המחסומים ואזורי "שמור פנוי" של 038f): אזהרה 30 שנ׳ ← הרמה 40 ← האונייה עוברת ← הורדה 40 — כ-3 דקות, לכל היותר פעם ב-6 דקות. התור עומד על הגשר הקבוע (כ-90 מ׳ בכל צד לפני המפתח), לא על המפתח ולא בכיכר. <br>
אין ראש סיבוב ואין רוורס: כל קו מסתובב בלולאה חד-סטרית — לולאת המזרח ולולאת המרינה — שתיהן נגד כיוון השעון (המזרח — מ-12:55, הבעלים) — כך שהרציף (מימין לקואץ׳) תמיד בצד של המקום: המנחת, המרינה. התורים לא עומדים על הגשר — המפרץ הראשון 26 מ׳ ויותר מהכיכר, והלולאות רחוקות מהגשר. ההמתנה בסוף הקו — במפרץ של הלולאה (30 שנ׳, כמו בעיר).</div>

<h2>4א. פרטים — זוג תחנות טיפוסי ולולאה סופית</h2>
<div class="wrap">{detail_pair()}</div>
<div class="wrap">{detail_loop()}</div>
<div class="card">כל זוג תחנות — עד 40 מ׳ מצומת עם מעברי חצייה (כלל 21: חוצים רק בצומת), ו-15 מ׳ לפחות ממנו. בלולאה הסופית — רציף אחד בצד של הבלוק (מימין לקואץ׳), ומקום המתנה לפני הרציף; התור לא מגיע לשדרה.</div>

<h2>5. המקומות (F — תוכן אמיתי בכל אחד)</h2>
<div class="wrap"><table>{tr('#','המקום','אזור','מוקד',h=True)}{places_tbl}</table></div>

<h2>6. הרכבת</h2>
<div class="grid2">
<div class="card"><div class="big">{trn['cars']} קרונות · {trn['need_m']} מ׳</div><b>תחנת האי:</b> הרציף האמצעי (קיים, בין פס א׳ לפס ב׳) — {trn['platform_m']:.0f} מ׳ של משטח; כל הרכבת ברציף, בפס א׳ (הבעלים: "צריך" 4, "מתאים אפילו אולי ל-5" — נכנסים גם 5). <b>נבנה</b> (RL-PS-02, ‏040b).</div>
<div class="card"><div class="big">רציף הנמל בעיר · 22 + 38 מ׳</div>נמדד — הרציף האמצעי הוא כל המשטח המצויר (021: ‏PORT_PLATFORM = 4.8 × 22 מ׳). ההארכה צפונה — אי אפשר בלי לשנות מסילה (סתירה, כלל 5): צפונה מ-y 4470 עובר המעבר XOVER בין הפסים (020: ‏SW-X-A (5800, 4462) ← SW-X-B (5900, 4290)). <b>ברירת המחדל (נבנית):</b> הרציף ממשיך דרומה מהקצה שלו לאורך הצד החיצוני של הקשת B-LINK — 38 מ׳ נוספים, באותו רוחב ובאותו מרחק מהפס, עד 8 מ׳ מהמסילה של EAST-A; כך 3 מתוך 4 הקרונות מול רציף, והדלתות שלהם נפתחות. <b>לאישורך.</b></div>
<div class="card"><div class="big">מסוף המשא — פס ב׳ של תחנת האי</div>הבקר מצא שהסוט ב-H8 עובר במים ועל המגדלור, וגם הקשת לא נכנסת ברדיוס של המשחק (40 מ׳) בין התחנה לחוף — לכן המסוף עובר לפס ב׳ של התחנה (הנוסעים בפס א׳): <b>רציף פריקה של {trn['freight_dock_m']} מ׳</b> בצד הדרומי-מערבי של הקצה המזרחי (ממזרח לאולם), עם גגון שקוף (D‑622 — המשאיות מתחתיו), וחצר משאיות בין הרציף לדרך המזרח, השער ב-(8950, 7700). <br>
<b>נבנה (072y):</b> רכבת משא של קרון סגור וקטר (37 מ׳) — הקרון מקדימה והקטר מאחור (דוחף לתוך התחנה, מושך בחזרה). <b>המקור בעיר (גרסה 5):</b> הקצה המזרחי של המסילה הדרומית של הנמל (Q2-E, רציף W2) ← Q2-EE (ישר) ← הפס הדרומי EAST-S0 / EAST-S1 ← המסוט ES-JB ← פס ב׳ (ISL-B1) ← הגשר; מאז s16c (D‑665) פס ב׳ יוצא מהפס הדרומי, ומ-Q-BASE (הפס הצפוני) אין אליו דרך בלי היפוך. בפס הדרומי אף רכבת אחרת לא נוסעת; בעיר 25 שנ׳ (טעינה), ובאי — עד הסבב הבא. מלגזה מעבירה משטחים מהקרון אל מחסן מסוף המשא. <b>לאישורך:</b> רכבת של 3 קרונות (65 מ׳) — אפשרית בפס הדרומי (Q2-E ארוכה מספיק), צריכה בדיקה של הבלוקים מול רכבת העבודה של W2. לוח זמנים בחלון שבו אין רכבת אחרת בצומת ועל המפתח (כמו RL-PS-02). <b>המפתח והרכבות:</b> המפתח עולה רק כשאין רכבת על המפתח בלוח הזמנים בכל החלון של הפתיחה (038f: ‏s13TrainBusy — אזהרה, מחסומים, הרמה, 140 שנ׳ מעבר והורדה), והאות לרכבת אדום כל זמן שהמפתח לא למטה — כך שרכבת לא מגיעה למפתח מורם; אם בכל זאת — היא עוצרת באות, והקרון הראשון (זה שנדחף מקדימה) עומד לפני המגדל, לא על המפתח. <b>בזמן הפריקה בפס ב׳</b> — אף רכבת נוסעים לא מתוכננת לפס ב׳ (RL-PS-02 נכנסת רק לפס א׳; הבדיקה של החלק תבדוק את זה).</div>
<div class="card"><b>משאיות הפיזור (כלל 25 — מקור ויעד):</b> מהחצר אל: {'; '.join(f'<b>{a}</b> — {b}' for a,b in TRUCK_DROPS)}; ובחזרה לחצר. כל משאית — רכב של הסימולציה עם מקור (חצר המשאיות) ויעד (מפרץ הפריקה).</div>
</div>
<div class="card"><b>סתירה (כלל 5):</b> D‑23 ו-GATE‑76 — "אין רכבת משא בענף האי". הבעלים ביקש במפורש (12.11): "רכבת משא — אזור פריקה וטעינה ומשאיות פיזור באי". ברירת המחדל: הבקשה המפורשת של הבעלים; GATE‑76 מתעדכן — <b>לאישורך</b>.</div>

<h2>7. הרכבל</h2>
<div class="grid2">
<div class="card"><div class="big">{cb['cabins']} תאים</div>(לפחות 8) — לולאה סובבת אחת, תא כל {cb['spacing_m']} מ׳, ‏{cb['speed_mps']} מ׳/שנ׳ על הקו, תא כל {cb['headway_s']} שנ׳ בכל תחנה, 8 נוסעים בתא ← כ-{cb['pph']:,} נוסעים בשעה.</div>
<div class="card"><div class="big">{cb['one_way_m']} מ׳</div>(היום: {cb['old_m']} מ׳, 2 תאים) — שלוש תחנות: <b>תחנת העמק</b> ליד כיכר האי ← <b>הפסגה</b> (התחנה העליונה והקפה, קיימת) ← <b>תחנת הנמל</b> בשכונת הנמל (חדשה). נסיעה של {cb['ride_min']} דק׳ לכל קטע.</div>
<div class="card">בתחנות התאים מאטים, הדלתות נפתחות, נוסעים יורדים ועולים (נראים), והתא ממשיך. לילה (00:00–06:00): התאים חונים בתחנות לפי הסדר. לשחקן: F בכל תחנה — כרטיס, תור, עלייה, נסיעה נראית וירידה בתחנה אחרת. <b>גג שקוף</b> בשלוש התחנות (D‑622 — התאים עוברים מתחת לגג).</div>
</div>

<h2>8. המרינה, הנמל ונתיבי השיט</h2>
<div class="card"><ul>
<li><b>המרינה (½ D9):</b> אגן מוגן של 56 × 38 מ׳ בדרום של ½ D9 (y 7310–7690), שובר גלים במערב ובצפון, הכניסה בצפון-מזרח לאורך החוף המערבי של E9. <b>גרסה 4 (נמצא בתכנון של שלב 2ג):</b> מעל האגן נשאר מרחב התמרון של אוניית התפזורת "צוק הים" במעגן D8 — עיגול הסיבוב של אונייה של 79 מ׳ (39 מ׳ סביב (4250, 6905)); המשרד, החניון והמספנה — בתוך לולאת המרינה ב-E9; 3 מזחים צפים — 42 מקומות (14 בכל מזח, 7 בכל צד); מספנה עם מנוף הרמה ומדרון השקה; המשרד, השכרה וקנייה של סירות, ומקום חניה לסירה של השחקן (לעלות בכל מקום ולעגון כאן / בנמל האי / ב-B7 — הבעלים, סעיף 16).</li>
<li><b>נמל האי (F9):</b> על החוף הצפוני — הרמפה של המעבורת, נתיבי ההמתנה והקופה, ורציף הדייגים. האגנים הישנים שבתוך F9 נסגרים (E9 יבשה). <b>הזרימה:</b> דרך הנמל חד-סטרית — נכנסים מהשדרה ב-x 6600 צפונה אל 3 נתיבי ההמתנה (6 רכבים בכל אחד, הקופה בכניסה, סככה עם גג שקוף — D‑622), עולים לרמפה; היורדים מהמעבורת יוצאים מהרמפה מערבה בנתיב נפרד, ודרומה ב-x 6250 אל השדרה. בלי מבוי סתום ובלי רוורס.</li>
<li><b>זכות קדימה:</b> נתיב המעבורת חוצה את הנתיב הראשי ליד (6290, 6450) — המעבורת מחכה לאונייה שבנתיב הראשי (בתיאום עם sealife).</li>
<li><b>נתיבי השיט:</b> הנתיב הראשי בא מהמזרח ב-H7, עובר מתחת למפתח המתרומם ב-G8, ממשיך מערבה לאורך שורה 8 (E8, ‏D8), ואחרי D פונה לדרום־מערב ויוצא בין B ל-C. אף נתיב לא עובר דרך יבשה; האונייה לא נעלמת (s13DrawLiftLow — תלות ב-sealife).</li>
<li><b>האסדה:</b> מזח אספקה ב-H8 (ספינת האספקה גרה כאן במקום ב-E6 — <b>לאישורך</b>), הצינור מהאסדה לתחנת קבלת הגז.</li></ul></div>

<h2>9. שלבי הבנייה</h2>
<div class="card"><ol>
<li><b>הרכבל — {cb0} תאים, 3 תחנות</b> (שדרוג של CB / cabPose ב-038i — כל הקו והתחנות על היבשה של היום, כך שהשלב הזה לא תלוי בשלב 2). <b>נבנה</b> — הענף t17_island, ‏019h4_ISL17_gondola.js.</li>
<li><b>רכבת האי — {trn['cars']} קרונות.</b> <b>נבנה</b> (040b).</li>
<li><b>2ב + 3א — המזרח:</b> דרך המזרח ולולאת המזרח (סביב המנחת; מ-12:55 נגד כיוון השעון — הבעלים), המגדלור לכף של H8, ותחנות 7–9 של קו 5א (מפרצים של המפה); הקואץ׳ של קו 5 נוסע במסלול של 5א עד שהשדרה המערבית תיבנה. <b>נבנה</b> (074w4, ‏074l8). קו 5א — <b>כבוי כברירת מחדל</b> (‎?l5on — דולק), כמו קו 5 ב-master: כשהקואצ׳ים בשירות נכשלות שתי בדיקות של חניון הלילה ב-D5 (d5_wash_inside_depot, ‏parked_cars_exactly_inside_marked_stalls_citywide) — בבירור.</li>
<li><b>2א — H8 מצטרף לאי:</b> החוף הדרומי של H8, תחנת קבלת הגז, מזח האספקה, הצינור מהאסדה עד החוף, F בבסיס. <b>נבנה</b> (אותו חלק — ISL17H8).</li>
<li><b>היבשה החדשה</b> (E9, ‏½ D9 — המרינה, סגירת האגנים הישנים של F9; נמל האי עובר לחוף הצפוני; היציאה של אוניית הנמל D7 עוברת לנתיב מערבה ← דרום־מערב בין B ל-C) ו<b>הכבישים</b>: השדרה, שתי הלולאות, רחבת הנמל, דרך המלון, דרך המזרח — והוצאת IS-W / IS-E / IS-L ‏/ E69_73 / E880_760.</li>
<li><b>התחנות וקווים 5 ו-5א</b> — מפרצים לפי הטבלה; בדיקה: נסיעה מלאה בשני הכיוונים, מפגש של שני אוטובוסים, פתיחת הגשר באמצע.</li>
<li><b>מסוף המשא</b> בפס ב׳ של תחנת האי ורכבת המשא — <b>נבנה</b> (072y; גרסה 5 — דרך הפס הדרומי), ו-F במסוף המשא (מצב הרכבת). <b>פארק החוף של H8 — נבנה</b> (019h4: טיילת לאורך החוף, מצפה בכף, ספסלים, פנסים, שולחנות פיקניק, מגרש משחקים; אנשים בטיילת — 038i), בלי החניון ובלי דרך הכניסה מהלולאה (ISL-GAS-IN — עם הכניסה לבסיס הגז). משאיות הפיזור (073a LOGI) — בהמשך: ברשת של האי היום אין מקום לחזור (עץ של רחובות עם קצוות — כיכר, ראש סיבוב ולולאה אחת), והמתכנן של LOGI לא עושה פרסה; צריך את הלולאות של השדרה (שלב 2ג / 3). המגדלור על הכף של H8 — <b>נבנה</b>.</li>
<li><b>המרינה, נמל האי והמעבורת</b> (בתיאום עם sealife), ו<b>המקומות עם F</b> (בתיאום עם signs).</li></ol></div>

<h2>10. לאישורך / סתירות / תלות</h2>
<div class="card"><ul>
<li><b>לאישורך:</b> קו 5א (במקום קו אחד שחוזר על עצמו) · H8 רק בדרום (האסדה נשארת) — בפועל {C['zones_equiv']:.1f} אזורים · המגדלור עובר לכף של H8 · ספינת האספקה גרה ב-H8 · מסוף המשא בפס ב׳ של תחנת האי (לא ב-H8) · תחנת נמל לרכבל · האגנים הישנים של F9 נסגרים · התחנות הסופיות — רציף אחד בלולאה החד-סטרית (לא זוג) · ברציף הנמל בעיר — קרון אחד מול הרציף.</li>
<li><b>סתירה:</b> D‑23 / GATE‑76 (אין משא לאי) מול הבקשה של הבעלים — הולכים לפי הבעלים.</li>
<li><b>נמצא במלאי — חוסם את E9 ואת המרינה:</b> אוניית התפזורת "צוק הים" והגוררת "עוז" (019k: SHIP_ESC_OUT / SHIP_OUT / h2) יוצאות היום מהמעגן ב-D8 בקשת דרומה דרך E9 (5300, 7450) אל (5300, 9300); המעבורת (074zf) נכנסת לאגן הישן של F9 דרך (5900–5950, 7150–7366). לפני שהיבשה של E9 ושל ½ D9 נבנית — היציאה עוברת לנתיב מערבה ← דרום־מערב בין B ל-C (סיבוב במקום עם הגוררת), והמעבורת — לנמל החדש בחוף הצפוני.</li>
<li><b>תלות:</b> sealife — נתיבי השיט, ferry2 והאוניות; seatrees — העצים בים (B8–D8); buses — מנוע הקווים (בלי לשנות אותו); signs — השלטים והמותגים של המקומות; locks — הנעילה של האי בפרקים; mapfix — עדכון המפה (city_plan.island).</li></ul></div>
<h2>11. הערות הבקר (planrev, ‏07:25) — מה תוקן</h2>
<div class="card"><ol>
<li>מסילת המשא במים — יצאה; המסוף בפס ב׳ של התחנה, על היבשה (סעיף 6).</li>
<li>המגדלור — עבר לכף של H8, כולו על היבשה ([8700, 6680, 8790, 6760]); אין מסילה לידו.</li>
<li>הדרך לחצר המשאיות — השער ב-(8950, 7700) מדרך המזרח; הכניסה לבסיס הגז ולחניון הפארק — מהצלע הצפונית של הלולאה (שמאלה פנימה ושמאלה החוצה — הלולאה חד-סטרית; תוקן בגרסה 5).</li>
<li>לולאת המזרח — חצים בציור; מ-12:55 (הבעלים) נגד כיוון השעון: מדרך המזרח ממשיכים ישר צפונה ומשתלבים בחזרה בנתיב היורד; התחנה הסופית בצלע הצפונית, הרציף מימין — בצד הצפוני.</li>
<li>מספר התחנות — {len(stops)} תחנות, {C['stops_pairs']} זוגות + {C['stops_terminal']} סופיות = {C['stops_bays']} מפרצים; המרווח נמדד עכשיו לאורך הדרך, ונוסף זוג ליד מסוף המשא (תחנה 8). הרכבל — {cl0} מ׳.</li>
<li>הרכבת — {trn['cars']} קרונות, שני הקצוות כתובים (סעיף 6); רציף הנמל נמדד — 22 מ׳ הם כל המשטח.</li>
<li>המרינה — 42 מקומות בכל מקום.</li>
<li>מרווחים מעל 90 מ׳ — 3 חריגים מוצדקים, כתובים בסעיף 3.</li>
<li>תחנה 1 — דרך העפר לפסגה היא דרך שירות בלי מעבר חצייה (8 מ׳); חוצים בצמתים של השדרה.</li>
<li>בלי מבוי סתום: דרך המלון, רחוב השכונה ודרך הנמל — רחובות U ששני הקצוות שלהם בשדרה; שביל הכפר — להולכי רגל.</li>
<li>המעבורת — שני הכיוונים (סעיף 8).</li>
<li>מקור ויעד — רכבת המשא מרציף W2 בנמל (המסילה הדרומית); המשאיות אל 5 מפרצי פריקה (סעיף 6).</li>
<li>חניות — {len(PARKING)} חניונים (P בציור).</li>
<li>חצים — על כל הלולאות, ובכל דרך דו-סטרית חץ לכל כיוון.</li>
<li>הגשר מורם — סעיף 4.</li>
<li>גג שקוף — ברציף הפריקה, בסככת ההמתנה של המעבורת ובתחנות הרכבל.</li>
<li>17–19 — בלאישורך (סעיף 10) ובסעיף 8 (זכות קדימה).</li></ol></div>
<div class="sub">הנתונים: deliver/2026-11-17/island/tools/plan_data.py · החישוב: plan_calc.py ‏→ plan_calc.json · הדף: gen_page.py</div>
</main></body></html>'''
open(OUT,'w').write(PAGE)
print(OUT,len(PAGE))
