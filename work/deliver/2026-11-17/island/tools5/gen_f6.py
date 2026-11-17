# island5 (17.11): הציור של מעבר הסירות מתחת למסילות ב-F6 — מבט על (לפני / אחרי) וחזית מדרום. SVG בקוד בלבד (כלל 17).
import sys,math
sys.path.insert(0,'/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools5')
from f6_geom import *
def P(pts): return ' '.join(f'{p[0]:.0f},{p[1]:.0f}' for p in pts)
N1=[[6000,5120],[6460,5120],[6493,5119],[6525,5114],[6557,5106],[6589,5096],[6619,5082],[6649,5070],[6681,5060],[6713,5054],[6745,5051],[7800,5050]]
A1=[[6375,5120],[6434,5127],[6491,5147],[6541,5180],[6583,5223],[6613,5274],[6632,5331],[6637,5390],[6628,5450],[6615,5508],[6609,5568],[6615,5627],[6632,5685],[6661,5737],[6700,5783],[6746,5821],[6795,5855],[6844,5890],[6893,5925],[6942,5959],[6991,5994],[7140,6100]]
def off(Pp,d):
    o=[]
    for i,p in enumerate(Pp):
        a=Pp[max(0,i-1)];b=Pp[min(len(Pp)-1,i+1)];dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy) or 1
        o.append([p[0]-dy/L*d,p[1]+dx/L*d])
    return o
B1=[[6373,5158]]+off(A1,38)[3:]
TR={'N1':N1,'B4':[[6000,5120],[7800,5120]],'S2':[[6000,5158],[7800,5158]],'A1':A1,'B1':B1}
def rails(a,clip=None):
    for k,pts in TR.items():
        a(f'<polyline points="{P(pts)}" fill="none" stroke="#3e4448" stroke-width="66" stroke-linejoin="round"/>')
    for k,pts in TR.items():
        a(f'<polyline points="{P(pts)}" fill="none" stroke="#a3a6a7" stroke-width="61" stroke-linejoin="round"/>')
    for k,pts in TR.items():
        a(f'<polyline points="{P(pts)}" fill="none" stroke="#666b6d" stroke-width="40" stroke-linejoin="round"/>')
        a(f'<polyline points="{P(pts)}" fill="none" stroke="#413d37" stroke-width="36" stroke-dasharray="5 10"/>')
        for d in (-13,13): a(f'<polyline points="{P(off(pts,d))}" fill="none" stroke="#c6cbd0" stroke-width="3"/>')
def buoy(a,x,y,col,lab=None,faded=False):
    op=' opacity=".35"' if faded else ''
    a(f'<circle cx="{x}" cy="{y}" r="13" fill="{"#d23a2c" if col=="r" else "#2f9a4a"}" stroke="#111" stroke-width="3"{op}/>')
    if lab: a(f'<text class="dt" x="{x+18}" y="{y+8}" style="font-size:20px"{op}>{lab}</text>')
def arrows(a,pts,col,dash=''):
    a(f'<polyline points="{P(pts)}" fill="none" stroke="{col}" stroke-width="7" {dash} marker-end="url(#f6ar)" opacity=".9"/>')
def head(a,vb,label):
    a(f'<svg class="plan" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">')
    a('<defs><marker id="f6ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker>'
      '<marker id="f6ar2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c0281e"/></marker>'
      '<pattern id="f6wv" width="90" height="44" patternUnits="userSpaceOnUse"><path d="M0,22 q22,-10 45,0 t45,0" fill="none" stroke="#bfe2f6" stroke-width="4"/></pattern></defs>')
    a(f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="#9fd0ee"/><rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="url(#f6wv)" opacity=".6"/>')
VB=(6150,4280,1650,1520)
def common(a):
    a(f'<polygon points="{P([[6150,4280],[6230,4280],[6230,5200],[6150,5200]])}" fill="#d9d2bd" stroke="#8d8466" stroke-width="5"/>')
    # המטוס האמפיבי (074zm) — לא זז
    x0,x1,y,h=AMPH_RWY
    a(f'<rect x="{x0}" y="{y-h}" width="{x1-x0}" height="{2*h}" fill="#6a2c91" opacity=".08" stroke="#6a2c91" stroke-width="4" stroke-dasharray="20 12"/>')
    a(f'<polyline points="{P(AMPH_TAXI)}" fill="none" stroke="#6a2c91" stroke-width="8" stroke-dasharray="22 12" opacity=".8"/>')
    a('<circle cx="7000" cy="4350" r="16" fill="#fff" stroke="#6a2c91" stroke-width="5"/><circle cx="6540" cy="4350" r="16" fill="#fff" stroke="#6a2c91" stroke-width="5"/>')
    a('<text class="dt" x="7330" y="4470" fill="#6a2c91" style="font-size:24px">מסלול המים של המטוס האמפיבי (074zm)</text><text class="dt" x="7065" y="4330" fill="#6a2c91" style="font-size:22px">H2 — המתנה</text><text class="dt" x="6300" y="4330" fill="#6a2c91" style="font-size:22px">H1</text>')
    rails(a)
    a('<rect x="6290" y="5016" width="330" height="230" fill="none" stroke="#b3360f" stroke-width="5" stroke-dasharray="14 10"/><text class="dt" x="6255" y="5275" fill="#b3360f" style="font-size:22px">צומת המסילות (JX-SEA — הסוכן rails)</text>')
    a('<text class="dt" x="7560" y="5040" style="font-size:22px">N1 · y 5050</text><text class="dt" x="7560" y="5112" style="font-size:22px">B4 · y 5120</text><text class="dt" x="7560" y="5190" style="font-size:22px">S2 · y 5158</text>')
    a('<text class="dt" x="6650" y="5640" style="font-size:22px">מסילות האי (A1 / B1)</text>')
    a('<text class="lbl" x="6280" y="4400" style="font-size:30px">F5 / F6 — נתיב השיט של המרינה (F3) דרומה</text>')
    for i,y in enumerate((3450,3650,3850,4050,4250,4450)):
        if y<VB[1]: continue
        buoy(a,6600,y,'r','R'+str(i+1)); buoy(a,6950,y,'g','G'+str(i+1))
def f6_before():
    o=[];a=o.append;head(a,VB,'מעבר הסירות ב-F6 — היום');common(a)
    for x in (6585,6965):
        a(f'<rect x="{x-12}" y="5020" width="24" height="170" fill="#7d8186" stroke="#333" stroke-width="3"/>')
    a('<polyline points="6585,5153 6615,5105 6935,5105 6965,5153" fill="none" stroke="#2e6d8f" stroke-width="7"/><polyline points="6585,5087 6615,5039 6935,5039 6965,5087" fill="none" stroke="#2e6d8f" stroke-width="5" opacity=".55"/>')
    for i in range(8):
        x=6615+i*40; a(f'<polyline points="{x},5105 {x+20},5153 {x+40},5105" fill="none" stroke="#2e6d8f" stroke-width="3"/>')
    for k,(x,y) in BUOY_OLD.items(): buoy(a,x,y,'r' if '-R' in k else 'g',k[3:])
    for k,(x,y) in S10_BUOYS_OLD.items(): buoy(a,x,y,'r' if '-R' in k else 'g',k[3:])
    arrows(a,PILOT_N_OLD,'#c0281e','stroke-dasharray="20 12"');arrows(a,PILOT_S_OLD,'#c0281e','stroke-dasharray="20 12"')
    a('<text class="dt" x="6640" y="4960" fill="#c0281e" style="font-size:22px">סירת הנתב (038c)</text>')
    notes=['1. המפתח (x 6585–6965) צמוד לצומת המסילות — מסוטים ופסים עוברים זה מעל זה ממש ליד הנתיב',
           '2. הקשת של N1 (מהמסוט ב-6460 עד 6765) עוברת בתוך המפתח — המסילה עולה ויורדת מעל הסירות',
           '3. המסבך הכחול רק מעל B4 — לא מעל N1 ו-S2 (נוספו ב-S13 / S16c); העמודים תלויים מתחת לסיפון אחד',
           '4. patchDecks מכיר רק EAST-A/B/C ו-ISL-ARC/BR — סירה מתחת ל-N1 / B4 / S2 לא מכוסה (גג שקוף — כלל 15)',
           '5. sidingRail (021v) עוד מצייר את מסילת ההיפוך הישנה — עם בולם ב-x 7186 על מסילה שממשיכה עד הקצה']
    for i,t in enumerate(notes): a(f'<text class="dt" x="7790" y="{5330+i*44}" text-anchor="end" style="font-size:23px">{t}</text>')
    a('</svg>');return ''.join(o)
def walls(a,sx):
    xw=CX-CLR//2-FW//2 if sx<0 else CX+CLR//2+FW//2
    xf=xw+sx*FLARE
    for (y0,y1,y2) in (WALL_N,WALL_S):
        a(f'<polyline points="{xw},{y0} {xw},{y1} {xf},{y2}" fill="none" stroke="#7a5a32" stroke-width="10" stroke-linejoin="round"/>')
        for y in range(min(y0,y1),max(y0,y1)+1,20): a(f'<circle cx="{xw}" cy="{y}" r="4.5" fill="#3a2e22"/>')
        a(f'<circle cx="{xf+sx*4}" cy="{y2+(6 if y2>5200 else -6)}" r="15" fill="#5b4a36" stroke="#2a2018" stroke-width="3"/>')
        a(f'<circle cx="{xf+sx*4}" cy="{y2+(6 if y2>5200 else -6)}" r="6" fill="{"#e23b2e" if sx<0 else "#33c25a"}"/>')
def pier(a,x0,x1):
    c=(x0+x1)/2
    pts=[[x0,PY[0]],[c,PY[0]-NOSE],[x1,PY[0]],[x1,PY[1]],[c,PY[1]+NOSE],[x0,PY[1]]]
    a(f'<polygon points="{P(pts)}" fill="#cbc7bc" stroke="#6e6a60" stroke-width="4"/>')
    fx=x1 if c<CX else x0-FW
    a(f'<rect x="{fx}" y="{PY[0]-NOSE+8}" width="{FW}" height="{PY[1]-PY[0]+2*NOSE-16}" fill="#8a6a3a"/>')
def f6_after():
    o=[];a=o.append;head(a,VB,'מעבר הסירות ב-F6 — ההצעה: מזרחה ובעיצוב חדש');
    # התעלה — מים עמוקים מסומנים (לפני המסילות, כדי שהן מעליה)
    ch=[[6600,4470],[6800,JOG[1]],[6800,5760],[7200,5760],[7200,JOG[1]],[6950,4470]]
    a(f'<polygon points="{P(ch)}" fill="#1f5f9a" opacity=".16"/>')
    common(a)
    for k,(x,y) in BUOY_OLD.items():
        if k in BUOY_MOVE: a(f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="#555" stroke-width="3" stroke-dasharray="6 5" opacity=".7"/>')
    pier(a,*XW);pier(a,*XE)
    walls(a,-1);walls(a,1)
    # הקשת מלמעלה: שתי קורות הקשירה ושתי הקשתות (מעל שפת הסיפון), והקשרים העליונים
    xa0,xa1=(XW[0]+XW[1])/2,(XE[0]+XE[1])/2
    for y in (YN,YS): a(f'<line x1="{xa0}" y1="{y}" x2="{xa1}" y2="{y}" stroke="#f4f6f7" stroke-width="12" stroke-linecap="round"/><line x1="{xa0}" y1="{y}" x2="{xa1}" y2="{y}" stroke="#7d8a94" stroke-width="2"/>')
    for x in range(int(CX-140),int(CX+141),70): a(f'<line x1="{x}" y1="{YN}" x2="{x}" y2="{YS}" stroke="#f4f6f7" stroke-width="5" opacity=".85"/>')
    for x in range(int(CX-140),int(CX+140),70): a(f'<line x1="{x}" y1="{YN}" x2="{x+70}" y2="{YS}" stroke="#f4f6f7" stroke-width="3" opacity=".6"/><line x1="{x+70}" y1="{YN}" x2="{x}" y2="{YS}" stroke="#f4f6f7" stroke-width="3" opacity=".6"/>')
    for k,(x,y) in BUOY_MOVE.items(): buoy(a,x,y,'r' if '-R' in k else 'g',k[3:])
    for k,(x,y) in S10_BUOYS.items(): buoy(a,x,y,'r' if '-R' in k else 'g',k[3:])
    arrows(a,PILOT_N,'#1d3f8f');arrows(a,PILOT_S,'#1d3f8f')
    a('<text class="dt" x="7065" y="4885" fill="#1d3f8f" style="font-size:22px">סירת הנתב — בצד ימין של התעלה</text>')
    a(f'<line x1="{CX-CLR//2}" y1="5470" x2="{CX+CLR//2}" y2="5470" stroke="#111" stroke-width="3"/><text class="dt" x="{CX}" y="5462" text-anchor="middle" style="font-size:24px">40 מ׳ בין הפגושים</text>')
    a(f'<text class="dt" x="{CX}" y="4995" text-anchor="middle" style="font-size:22px">קשת קשורה · 46 מ׳</text>')
    notes=['מרכז המעבר: x 7000 (היום 6775) — 22 מ׳ מזרחה, מחוץ לצומת ולקשת של N1; שלוש המסילות ישרות',
           'קשת קשורה אחת מעל שלוש המסילות (N1, ‏B4, ‏S2), שני עמודים עם חרטום, פגושים, קירות הנחיה ודולפינים עם אורות',
           'הנתיב: כמו היום עד y 4470 (החצייה של המטוס ב-y 4350 לא זזה), עיקול עד y 4790, וישר אל המעבר',
           'R7–R9 / G7–G9 זזים; R10 / G10 — דרומה (y 5700); סירת הנתב — במסלול החדש, שמאלה ממסלול המטוס']
    for i,t in enumerate(notes): a(f'<text class="dt" x="7790" y="{5590+i*44}" text-anchor="end" style="font-size:23px">{t}</text>')
    a('</svg>');return ''.join(o)
def f6_elev():
    # חזית מדרום: 10 פיקס׳ = 1 מ׳ גם לגובה; y = −גובה; המים ב-0
    o=[];a=o.append
    a('<svg class="plan" viewBox="6600 -300 800 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="מעבר הסירות — חזית מדרום">')
    a('<rect x="6600" y="-300" width="800" height="300" fill="#dff0fa"/><rect x="6600" y="0" width="800" height="100" fill="#7fb9dd"/>')
    for x in range(6600,7400,40): a(f'<path d="M{x},6 q10,-5 20,0 t20,0" fill="none" stroke="#c6e6f6" stroke-width="2"/>')
    zd=82;zc=int(CLEAR*10)
    # הגשר הנמוך משני הצדדים — סיפון, עמודים כל 12 מ׳
    for x0,x1 in ((6600,XW[0]),(XE[1],7400)):
        a(f'<rect x="{x0}" y="{-zd-6}" width="{x1-x0}" height="14" fill="#8e9396" stroke="#3e4448" stroke-width="2"/>')
        x=x0+40
        while x<x1-20: a(f'<rect x="{x-6}" y="{-zd+8}" width="12" height="{zd-8}" fill="#7a7f83"/>');x+=120
    # העמודים: גוף, כיפה, פגושים
    for x0,x1 in (XW,XE):
        a(f'<rect x="{x0}" y="{-zc+4}" width="{x1-x0}" height="{zc+20}" fill="#b9b5aa" stroke="#6e6a60" stroke-width="3"/><rect x="{x0-4}" y="{-zc-2}" width="{x1-x0+8}" height="8" fill="#8f8b80"/>')
        fx=x1 if x0<CX else x0-FW
        a(f'<rect x="{fx}" y="-46" width="{FW}" height="56" fill="#8a6a3a"/>')
        for k in range(4): a(f'<rect x="{fx-1}" y="{-44+k*13}" width="{FW+2}" height="3" fill="#5a4426"/>')
        gx=fx-14 if x0<CX else fx+FW+2
        a(f'<rect x="{gx}" y="-60" width="12" height="62" fill="#fff" stroke="#222" stroke-width="1.5"/>')
        for k in range(7): a(f'<rect x="{gx}" y="{-60+k*9}" width="12" height="4" fill="#222"/>')
        lx=x1-4 if x0<CX else x0+4
        a(f'<circle cx="{lx}" cy="{-zc-10}" r="5" fill="#e23b2e"/>')
    # הסיפון של המעבר וקורות הקשירה
    xa0,xa1=(XW[0]+XW[1])/2,(XE[0]+XE[1])/2
    a(f'<rect x="{xa0}" y="{-zd-8}" width="{xa1-xa0}" height="{zd-zc+8}" fill="#e9edf0" stroke="#6f7c86" stroke-width="3"/>')
    # הקשת וההיתלים (רשת)
    hs=(xa1-xa0)/2;R=RISE*10
    arch=[[xa0+i*(xa1-xa0)/60,-zd-8-R*(1-((xa0+i*(xa1-xa0)/60-CX)/hs)**2)] for i in range(61)]
    for i in range(1,12):
        xt=xa0+i*(xa1-xa0)/12
        for d in (-55,55):
            xh=max(xa0,min(xa1,xt+d));yh=-zd-8-R*(1-((xh-CX)/hs)**2)
            a(f'<line x1="{xt}" y1="{-zd-8}" x2="{xh}" y2="{yh}" stroke="#7d8a94" stroke-width="1.6"/>')
    a(f'<polyline points="{P(arch)}" fill="none" stroke="#6f7c86" stroke-width="13" stroke-linecap="round"/><polyline points="{P(arch)}" fill="none" stroke="#f4f6f7" stroke-width="9" stroke-linecap="round"/>')
    for i in range(3,58,4):
        x,y=arch[i];a(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#ffd27a"/>')
    a(f'<rect x="{CX-70}" y="{-zd+2}" width="140" height="16" fill="#1d4f91"/><text x="{CX}" y="{-zd+14}" text-anchor="middle" style="font:700 12px Arial;fill:#fff">מעבר שיט · 7.0 מ׳</text>')
    for dx in (-8,8): a(f'<circle cx="{CX+dx}" cy="{-zc+6}" r="4.5" fill="#2e9d4a"/>')
    # רכבת משא על S2 (מלפנים) — קווי מתאר
    a(f'<rect x="6830" y="{-zd-46}" width="150" height="38" rx="3" fill="#a5532e" opacity=".85"/><rect x="6990" y="{-zd-46}" width="150" height="38" rx="3" fill="#2f6a8f" opacity=".85"/>')
    for x in (6850,6960,7010,7120): a(f'<circle cx="{x}" cy="{-zd-7}" r="5" fill="#222"/>')
    # יאכטה במעבר
    a(f'<path d="M6930,-4 L7075,-4 L7090,-22 L6918,-22 Z" fill="#fafafa" stroke="#333" stroke-width="2"/><rect x="6965" y="-40" width="70" height="18" fill="#f2f2f2" stroke="#333" stroke-width="2"/><rect x="6985" y="-56" width="34" height="16" fill="#e8e8e8" stroke="#333" stroke-width="2"/><line x1="7002" y1="-56" x2="7002" y2="-64" stroke="#333" stroke-width="2"/>')
    # המידות
    a(f'<line x1="{CX-CLR//2}" y1="40" x2="{CX+CLR//2}" y2="40" stroke="#111" stroke-width="2"/><line x1="{CX-CLR//2}" y1="30" x2="{CX-CLR//2}" y2="50" stroke="#111" stroke-width="2"/><line x1="{CX+CLR//2}" y1="30" x2="{CX+CLR//2}" y2="50" stroke="#111" stroke-width="2"/>')
    a(f'<text x="{CX}" y="68" text-anchor="middle" style="font:700 16px Arial;fill:#111">40 מ׳ בין הפגושים</text>')
    a(f'<line x1="7290" y1="0" x2="7290" y2="{-zc}" stroke="#111" stroke-width="2"/><text x="7300" y="{-zc/2}" style="font:700 15px Arial;fill:#111">7.0 מ׳</text>')
    a(f'<line x1="7330" y1="{-zd-8}" x2="7330" y2="{-zd-8-R}" stroke="#111" stroke-width="2"/><text x="7340" y="{-zd-8-R/2}" style="font:700 15px Arial;fill:#111">10 מ׳</text>')
    a(f'<text x="6610" y="-270" style="font:700 17px Arial;fill:#1d2228">חזית מדרום (מים — 0; הפסים — ‎+8.2 מ׳; קנה מידה אמיתי, 10 פיקס׳ = 1 מ׳)</text>')
    a(f'<text x="6610" y="{-zd-20}" style="font:600 13px Arial;fill:#1d2228">הגשר הנמוך — עמודים כל 12 מ׳</text>')
    a('</svg>');return ''.join(o)
F6_BEFORE=f6_before();F6_AFTER=f6_after();F6_ELEV=f6_elev()
if __name__=='__main__':
    open('/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/f6_test.html','w').write('<html dir="rtl"><body style="background:#fff">'+F6_BEFORE+F6_AFTER+F6_ELEV+'</body></html>')
    print(len(F6_BEFORE),len(F6_AFTER),len(F6_ELEV))
