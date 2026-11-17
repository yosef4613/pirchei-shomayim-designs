# make_plan.py — הציור (כלל 13): דף SVG נקי, בלי תמונות. python3 make_plan.py <seat_stats.json> <out.html>
import json, sys, html
S = json.load(open(sys.argv[1], encoding='utf-8'))
st, au = S['stats'], S['audit']
X0, Y0, W, H = 0, -850, 9600, 8600
cols = [0,1200,2400,3600,4800,6000,7200,8400,9600]; rows = [-850,0,850,1700,2550,3400,4250,5200,6050,6900,7750]
SEA = set('F3 F4 B6 C6 D6 E6 D5 F5 G5 F6 B7 C7 D7 E7 A6 G4 H4 H5 G6 H6 A7 F7 H7 A8 B8 C8 D8 E8 F8 G8 H8 A9 B9 C9 D9 E9'.split())
k = 0.1
def sx(x): return round((x - X0) * k, 1)
def sy(y): return round((y - Y0) * k, 1)
g = []
for i in range(8):
    for j in range(10):
        z = 'ABCDEFGH'[i] + str(j)
        x, y, w, h = cols[i], rows[j], cols[i+1]-cols[i], rows[j+1]-rows[j]
        sea = z in SEA and z not in ('F9','G9','H9')
        g.append(f'<rect x="{sx(x)}" y="{sy(y)}" width="{w*k}" height="{h*k}" class="{"sea" if sea else "land"}{" hot" if z in ("B8","C8","D8") else ""}"/>')
        g.append(f'<text x="{sx(x)+4}" y="{sy(y)+12}" class="zl">{z}</text>')
for z in st['zones']:
    if z[0] == 'rect':
        r = z[2]; g.append(f'<rect x="{sx(r[0])}" y="{sy(r[1])}" width="{round((r[2]-r[0])*k,1)}" height="{round((r[3]-r[1])*k,1)}" class="nz"><title>{html.escape(z[1])}</title></rect>')
    else:
        g.append(f'<circle cx="{sx(z[2][0])}" cy="{sy(z[2][1])}" r="{round(z[3]*k,1)}" class="nz"><title>{html.escape(z[1])}</title></circle>')
seen = set(); nw = 0
for b in st['blocked']:
    key = (round(b['x']/8), round(b['y']/8))
    if key in seen: continue
    seen.add(key); nw += 1
    g.append(f'<g class="wx"><title>{html.escape(b["src"]+" · "+b["id"]+" · "+str(b["x"])+","+str(b["y"]))}</title><line x1="{sx(b["x"])-4}" y1="{sy(b["y"])-4}" x2="{sx(b["x"])+4}" y2="{sy(b["y"])+4}"/><line x1="{sx(b["x"])-4}" y1="{sy(b["y"])+4}" x2="{sx(b["x"])+4}" y2="{sy(b["y"])-4}"/></g>')
cnt = {}
for v in st['veg']:
    cnt[v[3]] = cnt.get(v[3], 0) + 1
    cl = 'vw' if v[3] == 'WATER' else 'vz'
    g.append(f'<circle cx="{sx(v[0])}" cy="{sy(v[1])}" r="2.2" class="{cl}"><title>{html.escape(v[2]+" · "+v[3]+" · "+str(v[0])+","+str(v[1]))}</title></circle>')
svg = f'<svg viewBox="0 0 {W*k} {H*k}" role="img" aria-label="מפת העולם: העצים שהוצאו">' + ''.join(g) + '</svg>'
rows_src = [
 ('VEG_D (074zg_veg_data.js) · הצייר 074zh_veg.js:vegInit / vegFurnInit', 'שכבת הצמחייה החדשה של 11.11 — 2,995 עצים בקבוצות ו-1,245 אפויים', 'בלי בדיקת מגרשים ומנחתים: 15 במגרש הכדורסל B4, 40 במגרש בית השחקן (5 בעיגול המנחת, 4 בבטיחות)'),
 ('019c_F3F4_s9.js · הגינה G-F4-PALM (T9-F34-46/49/52)', 'הדקלים של חוף F4', '3 גזעים בתוך הים (y 2600)'),
 ('B2/D2/D4/E5/B6/B5/C5/A4_TREES · 018:drawChunkTrees ו-062:wtcPaintL2', 'העצים של הקוד הישן (TurboCity.draw)', 'רק צמחי המים של האגם (TP-WP — מותרים)'),
 ('K34C.list · 067:k34Take', 'העצים הגבוהים בכל פריים (3/4)', 'נרשמים מכל צייר — שם עברו גם הדקלים של F4'),
 ('S12_TREES · 023b:s12Over / 023c', 'היער של A0–B1', '0 על מים'),
 ('C3LV (031) · העצים של כל רמת בית', 'התוכן של הבית לפי רמה', '0 בעיגול הבטיחות של המנחת (נבדק בכל 8 הרמות) — לא נוגע'),
]
tr = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>' for a,b,c in rows_src)
page = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>עצים בים</title>
<style>
:root{{--bg:#f6f4ef;--fg:#1d2329;--mut:#5d6670;--sea:#bcd6ea;--land:#e4e8d6;--hot:#e0574f;--nz:#7a4bd1;--card:#fff;--line:#d5d0c6}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#12161b;--fg:#e8ecef;--mut:#9aa5ae;--sea:#1d3a52;--land:#2b3324;--hot:#ff7a70;--nz:#b79bff;--card:#1a2027;--line:#33404b}}}}
:root[data-theme="dark"]{{--bg:#12161b;--fg:#e8ecef;--mut:#9aa5ae;--sea:#1d3a52;--land:#2b3324;--hot:#ff7a70;--nz:#b79bff;--card:#1a2027;--line:#33404b}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,sans-serif}}
main{{max-width:1000px;margin:0 auto;padding:16px}}
h1{{font-size:22px;margin:8px 0}} h2{{font-size:17px;margin:22px 0 8px}} p{{margin:6px 0}} .mut{{color:var(--mut)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;overflow:auto}}
svg{{width:100%;height:auto;display:block}}
.sea{{fill:var(--sea);stroke:var(--line);stroke-width:.6}} .land{{fill:var(--land);stroke:var(--line);stroke-width:.6}} .hot{{stroke:var(--hot);stroke-width:2.2}}
.zl{{font-size:9px;fill:var(--mut)}} .nz{{fill:none;stroke:var(--nz);stroke-width:1.4;stroke-dasharray:3 2}}
.wx line{{stroke:var(--hot);stroke-width:1.8}} .vw{{fill:var(--hot)}} .vz{{fill:var(--nz)}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{border-bottom:1px solid var(--line);padding:6px;text-align:right;vertical-align:top}}
.legend span{{display:inline-block;margin-left:14px}}
</style></head><body><main>
<h1>עצים בים, במגרשים ובמנחתים — מה נמצא ומה יוצא</h1>
<p class="mut">סוכן seatrees · סבב 17.11 · ציור בקוד בלבד (SVG), בלי תמונות. המקור: S7F298 (int298 7c2d0be).</p>
<h2>המפה</h2>
<div class="card">{svg}
<p class="legend"><span>✕ אדום — גזע על המים, לא מצויר ({nw})</span><span>● סגול — עץ חדש (VEG) שיוצא ממגרש / מנחת / מגרש הבית ({cnt.get("B4-COURT",0)} ב-B4, {sum(v for k2,v in cnt.items() if k2 not in ("B4-COURT","WATER"))} בבית ובמנחתים)</span><span>קו מקווקו — אזור בלי עצים חדשים</span><span>מסגרת אדומה — B8, ‏C8, ‏D8 (הצילום של הבעלים)</span></p></div>
<h2>המלאי — מאיפה באים העצים (כלל 16 / 19)</h2>
<div class="card"><table><tr><th>המקור</th><th>מה זה</th><th>מה נמצא</th></tr>{tr}</table></div>
<h2>מה נבנה</h2>
<p>שומר אחד לכל העולם (חלק חדש 074zh2_seatrees.js), מעל הקיים: בכל ציור של צמחייה — TurboCity.draw, ‏k34Take, ‏KIT34.draw / drawBody / drawShadow — נמדדת נקודת הגזע בעולם מתוך המטריצה של הציור עצמו (המצלמה, האריח או מעבר הסריקה). גזע על המים (הים או האגם, ולא מזח / רציף / גשר) — לא מצויר ולא נרשם. בלי קופסה של אזור.</p>
<p>הצמחייה החדשה (VEG) מסוננת פעם אחת כשהיא נטענת: גם מגרש הכדורסל B4 ומגרשי A4, מגרש בית השחקן C3-PH (התוכן של כל רמה נשאר), ועיגולי הבטיחות של המנחתים (הבית 7–8, השדה, האי).</p>
<h2>B8 · C8 · D8</h2>
<p>בבנייה הנקייה, במצלמה של הצילום (C8, זום 0.44, יום ולילה, קיץ וסתיו) — אין עצים בים, וגם הסריקה של כל העולם לא מצאה שם אף ציור של עץ. השומר חוסם כל עץ שמגיע לשם בכל אחת מנקודות החנק, כך שגם אם מצב מסוים במשחק של הבעלים יוצר אותם — הם לא יצוירו, והמקור נרשם ב-__TC_SEATREES.stats().</p>
<h2>הבדיקה החוסמת</h2>
<p>tree_sweep.js — סורק את כל האריחים ומזיז את המצלמה על כל העולם, ורושם כל ציור של צמחייה בנקודת העולם שלו; ועוד VEG, ‏K34C.list, ‏S12. נכשל אם נשאר גזע מצויר על המים, או עץ חדש במגרש B4, במנחת או במגרש הבית.</p>
</main></body></html>'''
open(sys.argv[2], 'w', encoding='utf-8').write(page)
print('ok', len(page))
