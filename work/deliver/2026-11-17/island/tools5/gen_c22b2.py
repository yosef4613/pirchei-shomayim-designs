# island5 (17.11): שלב 2ג-2ב-2 — המרינה ב-½ D9, סגירת האגן העליון והחלק הצפוני של התעלה, השדרה. SVG בקוד בלבד.
def P(pts): return ' '.join(f'{p[0]:.0f},{p[1]:.0f}' for p in pts)
E9C=[[5000,7749],[5000,7010],[5100,6994],[5200,6985],[5320,6988],[5395,6991],[5395,7032],[5545,7032],[5545,6997],[5620,7005],[5672,7024],[5722,7052],[5764,7088],[5786,7130],[5790,7200],[5790,7290],[6180,7290]]
F9=[[6171,7470],[6170,7420],[6182,7320],[6176,7210],[6185,7130],[6195,7095],[6235,7030],[6305,6993],[6430,6975],[6610,6985],[6800,6970],[7000,6990],[7200,6975],[7200,7750],[6171,7750]]
# המרינה: יבשה בצורת U (שובר הגלים בצפון, המזח המערבי, הרציף הדרומי), האגן, הכניסה בצפון-מזרח
MAR_LAND=[[4200,7400],[4830,7400],[4830,7432],[4240,7432],[4240,7640],[4960,7640],[4960,7432],[4960,7400],[5000,7400],[5000,7750],[4200,7750]]
BASIN=[4240,7432,4960,7640]
PONT=(4300,4900,7536)
AVE=[[6900,7262],[6800,7228],[5800,7228],[5690,7255]]
MST=[[5100,7255],[5100,7680],[5000,7680]]
CLOSE=[[5672,7024],[5722,7052],[5764,7088],[5786,7130],[5790,7200],[5790,7290],[6180,7290],[6182,7320],[6176,7210],[6185,7130],[6195,7095],[6235,7030],[6100,7008],[5900,7008],[5760,7012]]
def svg():
    o=[];a=o.append
    a('<svg class="plan" viewBox="4100 6880 2900 880" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="שלב 2ג-2ב-2 — המרינה, האגן העליון והשדרה">')
    a('<defs><pattern id="hb3" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="24" height="24" fill="#dfe9c8"/><line x1="0" y1="0" x2="0" y2="24" stroke="#8fae5a" stroke-width="5"/></pattern>'
      '<marker id="ar11" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d3f8f"/></marker></defs>')
    a('<rect x="4100" y="6880" width="2900" height="880" fill="#9fd0ee"/>')
    a(f'<polygon points="{P(E9C+[[6180,7750],[5000,7750]])}" fill="#bfe08f" stroke="#4f7a25" stroke-width="7"/>')
    a(f'<polygon points="{P(F9)}" fill="#cfe6a8" stroke="#6f8f45" stroke-width="7"/>')
    # האגן העליון והחלק הצפוני של התעלה — נסגרים
    a(f'<polygon points="{P(CLOSE)}" fill="url(#hb3)" stroke="#6f8f45" stroke-width="5" stroke-dasharray="18 10"/>')
    a('<rect x="6080" y="7092" width="442" height="146" fill="url(#hb3)" stroke="#6f8f45" stroke-width="5" stroke-dasharray="18 10"/>')
    a('<text class="dt" x="5830" y="7150">האגן העליון והחלק הצפוני של התעלה — נסגרים</text>')
    # צוק הים — עיגול הסיבוב
    a('<circle cx="4250" cy="6990" r="400" fill="none" stroke="#7a5a3a" stroke-width="5" stroke-dasharray="14 10"/><text class="dt" x="4130" y="7375" fill="#7a5a3a">"צוק הים" — עיגול הסיבוב במעגן D8 (עד y 7390)</text>')
    # המרינה
    a(f'<polygon points="{P(MAR_LAND)}" fill="#d9d2bd" stroke="#6b6b60" stroke-width="6"/>')
    a(f'<rect x="{BASIN[0]}" y="{BASIN[1]}" width="{BASIN[2]-BASIN[0]}" height="{BASIN[3]-BASIN[1]}" fill="#86c2e6" stroke="#4d7f9e" stroke-width="4"/>')
    a('<rect x="4200" y="7398" width="630" height="36" fill="#8f8f88" stroke="#555" stroke-width="3"/><text class="dt" x="4260" y="7392">שובר הגלים</text>')
    for x in (4262,4302,4342,4382): a(f'<rect x="{x-4}" y="7566" width="8" height="74" fill="#9a7a52"/>')
    for x in (4282,4322,4362): a(f'<rect x="{x-10}" y="7578" width="20" height="52" rx="8" fill="#fff" stroke="#3a4a58" stroke-width="2"/>')
    for x in (4282,4352): a(f'<rect x="{x-29}" y="7436" width="58" height="22" rx="9" fill="#fff" stroke="#3a4a58" stroke-width="2"/>')
    a('<rect x="4640" y="7596" width="300" height="14" fill="#9a7a52"/>')
    for k in range(7): a(f'<rect x="{4660+k*260/6-4:.0f}" y="7508" width="8" height="90" fill="#9a7a52"/>')
    for k in range(6): a(f'<rect x="{4660+(k+.5)*260/6-11:.0f}" y="7525" width="22" height="58" rx="9" fill="#ffd27a" stroke="#6b4a2a" stroke-width="2"/>')
    a('<rect x="4475" y="7605" width="50" height="22" rx="9" fill="#f2c230" stroke="#6b4a2a" stroke-width="2"/><text class="dt" x="4440" y="7598" style="font-size:18px">"דג הזהב"</text>')
    a('<circle cx="4520" cy="7530" r="60" fill="none" stroke="#1d3f8f" stroke-width="3" stroke-dasharray="10 8"/><text class="dt" x="4470" y="7520" style="font-size:18px" fill="#1d3f8f">אגן סיבוב</text>')
    a('<text class="dt" x="4660" y="7500" style="font-size:20px">IS-BOATS — 6 סירות האי</text><text class="dt" x="4250" y="7488" style="font-size:18px">סירות התושבים</text>')
    a('<circle cx="4830" cy="7416" r="12" fill="#2fa84f" stroke="#111" stroke-width="3"/><circle cx="4960" cy="7416" r="12" fill="#d23a2c" stroke="#111" stroke-width="3"/><text class="dt" x="4840" y="7360" fill="#1d3f8f">הכניסה (13 מ׳)</text>')
    a('<polyline points="4895,7330 4895,7420 4895,7480" fill="none" stroke="#1d3f8f" stroke-width="8" marker-end="url(#ar11)"/>')
    a('<rect x="4252" y="7662" width="168" height="60" fill="#5d7fa8" stroke="#2b4058" stroke-width="4"/><text class="dt" x="4268" y="7690" fill="#fff" style="font-size:20px">משרד + בית קפה</text>')
    a('<rect x="4726" y="7656" width="266" height="88" fill="#a9a9a2" stroke="#555" stroke-width="3"/><text class="dt" x="4740" y="7710" style="font-size:20px">חניה (עם רחוב המרינה)</text>')
    a('<rect x="4560" y="7654" width="152" height="88" fill="#b98f5a" stroke="#6b4a2a" stroke-width="4"/><text class="dt" x="4570" y="7700" style="font-size:20px">המספנה</text>')
    a('<rect x="4600" y="7600" width="36" height="52" fill="#b4b2a8" stroke="#555" stroke-width="3"/>')
    # הכבישים: השדרה, הצלע הדרומית של הלולאה (דו-סטרית), דרך החוף המערבי, רחוב המרינה
    a('<polyline points="5690,7255 5690,7175 5100,7175 5100,7255" fill="none" stroke="#585858" stroke-width="50"/>')
    a('<polyline points="6900,7262 6900,7548 5690,7548 5690,7255" fill="none" stroke="#585858" stroke-width="80"/>')
    a(f'<polyline points="{P(AVE)}" fill="none" stroke="#1d3f8f" stroke-width="70" stroke-linejoin="round" opacity=".8"/>')
    a(f'<polyline points="{P(AVE)}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="24 18"/>')
    a(f'<polyline points="{P(MST)}" fill="none" stroke="#1d3f8f" stroke-width="60" stroke-dasharray="30 18" opacity=".55"/><circle cx="5000" cy="7680" r="62" fill="none" stroke="#1d3f8f" stroke-width="6" stroke-dasharray="14 10"/>')
    a('<text class="dt" x="5900" y="7150" fill="#1d3f8f">שדרת האי (1+1, נבנתה) — מרחבת הנמל מערבה ב-y 7228, על האגן העליון והתעלה</text>')
    a('<text class="dt" x="5140" y="7640" fill="#1d3f8f" transform="rotate(-90 5140 7640)">רחוב המרינה — הבא (2ב-2)</text>')
    # הקיים
    a('<rect x="5220" y="7300" width="370" height="390" fill="#e8743b" fill-opacity=".75" stroke="#8a3a12" stroke-width="5"/><text class="dt" x="5300" y="7500">האולם</text>')
    a('<rect x="5850" y="7310" width="220" height="150" fill="#c06c84" stroke="#6b2a3a" stroke-width="5"/><text class="dt" x="5858" y="7395" fill="#fff">מלון החוף</text>')
    for i in range(6):
        x=6130+i*112; a(f'<rect x="{x}" y="7330" width="64" height="56" fill="#d9a066" stroke="#6b4a2a" stroke-width="4"/>')
    a('<rect x="5405" y="6575" width="130" height="450" rx="30" fill="#6a2c91" opacity=".3"/><text class="dt" x="5420" y="6960" fill="#6a2c91">המעבורת</text>')
    # הסירות של האי עוברות למרינה
    a('<path d="M6300,7170 C5800,7120 5200,6900 4880,7330" fill="none" stroke="#c0281e" stroke-width="6" stroke-dasharray="20 12" marker-end="url(#ar11)"/><text class="dt" x="6230" y="7065" fill="#c0281e">IS-BOATS (6) וסירת הדייג — אל המרינה</text>')
    a('</svg>');return ''.join(o)
C22B2_SVG=svg()
