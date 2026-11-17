# ציור מצב קיים של האזור (לבדיקה פנימית בעין בלבד) — מהמפה ומנתוני S13D / S14D
import json,re,sys
W='/home/user/tc_root/tc/pkg/work'
P=W+'/src_game_t17_island/parts/'
cp=json.load(open(W+'/study/roads/city_plan.json'))
s=open(P+'019h_S13_data.js').read(); S13=json.loads(re.search(r'const S13D=(\{.*?\});',s,re.S).group(1))
s=open(P+'019j_S14_data.js').read(); i=s.index('var S14D='); j=s.index('};',i); S14=json.loads(s[i+9:j+1])
X0,Y0,X1,Y1=[float(a) for a in sys.argv[2:6]] if len(sys.argv)>5 else (2400,4800,9700,7800)
sc=0.25
def pt(p): return f'{(p[0]-X0)*sc:.1f},{(p[1]-Y0)*sc:.1f}'
def pl(pts,st,close=False):
    tag='polygon' if close else 'polyline'
    return f'<{tag} points="{" ".join(pt(p) for p in pts)}" style="{st}"/>'
def rect(r,st): return f'<rect x="{(r[0]-X0)*sc:.1f}" y="{(r[1]-Y0)*sc:.1f}" width="{(r[2]-r[0])*sc:.1f}" height="{(r[3]-r[1])*sc:.1f}" style="{st}"/>'
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{(X1-X0)*sc:.0f}" height="{(Y1-Y0)*sc:.0f}">','<rect width="100%" height="100%" fill="#cfe3b0"/>']
o.append(pl(cp['terrain']['sea'],'fill:#8cc3e8;stroke:none',True))
o.append(pl(S13['islandPoly'],'fill:#bcd98f;stroke:#6a8a3a;stroke-width:1',True))
for w in S13['water']: o.append(pl(w,'fill:#8cc3e8;stroke:none',True))
for c in S13['contours']: o.append(pl(c,'fill:none;stroke:#9a8a5a;stroke-width:.6',True))
for g in cp['segments']: o.append(pl(g['pts'],'fill:none;stroke:#555;stroke-width:%s'%(2.5 if g.get('cls') in('arterial','main','avenue') else 1.6)))
for g in cp.get('site_roads',[]): o.append(pl(g.get('draw') or g['pts'],'fill:none;stroke:#777;stroke-width:1'))
for r in cp['rails']: o.append(pl(r['pts'],'fill:none;stroke:#8a4b1f;stroke-width:1.2;stroke-dasharray:3 1'))
for r in S13['siteRoads']: o.append(pl(r['pts'],'fill:none;stroke:#333;stroke-width:1.6'))
o.append(pl(S13['br'],'fill:none;stroke:#222;stroke-width:3'))
o.append(pl(S13['lane5'],'fill:none;stroke:#1a49c4;stroke-width:1.5;stroke-dasharray:6 3'))
for k,v in S14['lanes'].items(): o.append(pl(v['pts'],'fill:none;stroke:#0a2a90;stroke-width:1.2;stroke-dasharray:2 3'))
o.append(pl(S14['ferry_new'],'fill:none;stroke:#c41a8a;stroke-width:1.2;stroke-dasharray:5 3'))
o.append(pl(S13['lift']['poly'],'fill:#f0c040;stroke:#a07000',True))
rg=S13['rig']; o.append(rect(rg,'fill:#e05050;stroke:#800'))
o.append(pl(S13['cable'],'fill:none;stroke:#d00;stroke-width:1.5'))
for l in [l for l in S13['lots'] if l.get('rect')]: o.append(rect(l['rect'],'fill:none;stroke:#7a3aa0;stroke-width:.8'))
for b in [b for b in S13['build'] if b.get('rect')]: o.append(rect(b['rect'],'fill:#d8b0e8;stroke:#7a3aa0;stroke-width:.5'))
cols=[0,1200,2400,3600,4800,6000,7200,8400,9600]; rows=[-850,0,850,1700,2550,3400,4250,5200,6050,6900,7750]
for x in cols: o.append(f'<line x1="{(x-X0)*sc}" y1="0" x2="{(x-X0)*sc}" y2="{(Y1-Y0)*sc}" stroke="#000" stroke-width=".4" stroke-dasharray="4 4"/>')
for y in rows: o.append(f'<line x1="0" y1="{(y-Y0)*sc}" x2="{(X1-X0)*sc}" y2="{(y-Y0)*sc}" stroke="#000" stroke-width=".4" stroke-dasharray="4 4"/>')
for ci,x in enumerate(cols[:-1]):
    for ri,y in enumerate(rows[:-1]):
        o.append(f'<text x="{(x-X0)*sc+4}" y="{(y-Y0)*sc+12}" font-size="11" fill="#000">{"ABCDEFGH"[ci]}{ri}</text>')
o.append('</svg>')
open(sys.argv[1],'w').write('\n'.join(o))
