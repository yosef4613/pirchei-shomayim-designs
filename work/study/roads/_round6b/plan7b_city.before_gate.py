# 1.11 (the owner 31.10 23:10, R-36): the full map of the future — the airport of stage 8 (part ו of the master plan), the island of
# D-259 and its bridge with two tracks, the rails of the port, and a lot with a road to it in every zone of the city.
# Read only from the plan's data: plan600/data/part_f_geo.json, part_f2_geo.json, part_d_geo.json, maps2.json (air-262, island).
import json, math
W = '/home/claude/work'
F = json.load(open(W + '/plan600/data/part_f_geo.json'))
F2 = json.load(open(W + '/plan600/data/part_f2_geo.json'))
D = json.load(open(W + '/plan600/data/part_d_geo.json'))
U = json.load(open(W + '/plan600/data/uses.json'))

def R(r): return [round(v, 1) for v in r]
# ---------------------------------------------------------------- the airport of stage 8 (D-262 — the layout after the owner's change)
# the runway and the taxiways from the drawing air-262 of the master plan; everything else from part ו (part_f_geo / part_f2_geo)
def airport():
    L = []   # the lots of the airport: (id, label, kind, rect, airside)
    def lot(id, he, kind, r, airside=True, **kw): L.append(dict(id=id, label=he, kind=kind, rect=R(r), airside=airside, zone=zone_of(r), future=True, stage='8', **kw))
    lot('AIR-RWY', 'המסלול 09/27 — 430 × 24 מ׳', 'runway', [5000, -810, 9300, -570])
    lot('AIR-TWA', 'מסלול ההסעה A', 'taxi', [4900, -285, 9450, -55])
    lot('AIR-TWB', 'מסלול ההסעה B', 'taxi', [9325, -170, 9475, 1925])
    lot('AIR-TWC', 'מסלול ההסעה C', 'taxi', [7259, 1775, 9475, 1925])
    lot('AIR-APRON', 'רחבת העמדות', 'apron', [4810, -55, 9163, 1033])
    lot('AIR-APRON-S', 'רחבת המרוחקות, ה-GA והמנחתים', 'apron', [7205, 1925, 9544, 2545])
    t = F['terminal']; lot('AIR-TERM', 'הטרמינל', 'building', [t['x0'], t['y0'], t['x1'], t['y1']], airside=False, floors=3)
    c = F['core']; lot('AIR-CORE', 'אגף השערים והשרוולים', 'building', [c['x0'], c['y0'], c['x1'], c['y1']], floors=2)
    ct = F['cargoT']; lot('AIR-CARGO', 'מסוף המטען', 'building', [ct['x0'], ct['y0'], ct['x1'], ct['y1']], airside=False, floors=2)
    m = F['land']['MSCP']; lot('AIR-MSCP', 'החניון הרב-קומתי — 4 קומות', 'parking', [m['x0'], m['y0'], m['x1'], m['y1']], airside=False, floors=4)
    m = F['land']['CREW']; lot('AIR-CREW', 'חניון הצוות והעובדים', 'parking', [m['x0'], m['y0'], m['x1'], m['y1']], airside=False)
    for k, b in enumerate(F['base']):
        he, x0, y0, x1, y1 = b[:5]; lot(f'AIR-BASE-{k + 1}', he.split(' (')[0], 'building', [x0, y0, x1, y1], floors=1)
    for k, (he, r) in enumerate(F['aprons']): lot(f'AIR-HAP-{k + 1}', he, 'apron', r)
    for st in F2['stands']: lot('AIR-' + st['id'], f"עמדה {st['id']}", 'stand', st['box'], code=st['id'])
    # 1.11 (round 5, D-262 — the owner 28.10 22:30): the helipad H1 by the terminal is not built and P5 stays a bridge stand; part_f2_geo
    # still holds the proposal of D-252 (P5 out, H1 in its place). P5 takes the box between P4 and the arm of P6, as P2–P4 (nose at y 768).
    if not any(st['id'] == 'P5' for st in F2['stands']): lot('AIR-P5', 'עמדה P5', 'stand', [7984, 352, 8402, 886], code='P5')
    for h in F2['helipads']:
        if h['id'] == 'H1': continue
        lot('AIR-' + h['id'], f"מנחת {h['id']}", 'pad', h['fato'], code=h['id'])
    lot('AIR-LAND-E2', 'צד היבשה של המטען — חצר המשאיות והשערים', 'yard', [4850, 1060, 5700, 1440], airside=False)
    # the roads of the landside (one way, two lanes — at the plan's width of 3.9 m a lane, with sidewalks) and the link from the
    # passenger gate under the rail bridge; the access road of part ו is put on the line of the marina road (x 6120, 4 m east)
    roads = [dict(id='AIR-ACCESS', label='כביש הגישה לטרמינל — חד-סטרי צפונה', pts=[[6120, 1760], [6120, 1254]], lanes=2, oneway=True),
             dict(id='AIR-FRONT', label='חזית הטרמינל — חד-סטרי מזרחה, נתיב מפרצים', pts=[[6120, 1254], [7145, 1254], [7860, 1254]], lanes=2, oneway=True),
             dict(id='AIR-CONN', label='המחבר — חד-סטרי דרומה', pts=[[7145, 1254], [7145, 1760]], lanes=2, oneway=True),
             dict(id='AIR-SOUTH', label='דרך החזרה — חד-סטרי מערבה, 2 נתיבים (חלק ו)', pts=[[7145, 1760], [6750, 1760]], lanes=2, oneway=True),
             # 1.11 00:44 (the owner): from the 3+3 avenue to the terminal never under 2 lanes each way — 2+2 under the rail bridge; the drop
             # 3 → 2 in one marked taper after the gate (x 4800–5400), not at a junction
             dict(id='AIR-PAX', label='דרך הנוסעים — 2 נתיבים לכל כיוון, משער הנוסעים מתחת לגשר הרכבת', pts=[[4800, 1600], [6120, 1600]], lanes=4, oneway=False, cls='arterial',
                  taper=dict(x0=4800, x1=5400, side=1, label='הצרה מסומנת: 3 → 2 נתיבים')),
             dict(id='AIR-CARGO-RD', label='דרך המטען — משער המטען אל מסוף המטען', pts=[[4800, 1250], [5560, 1250], [5560, 990]], lanes=2, oneway=False)]
    side = [dict(id='AIR-' + sv[0], label=sv[1], rect=sv[2:6], lanes=sv[6]) for sv in F['service']]
    fence = F['airside'] + [F['airside'][0]]
    rail = F['rail']
    return dict(lots=L, roads=roads, service=side, fence=fence, rail=rail, label='השדה העתידי — שלב 8 (חלק ו, D‑262)',
                front_bays=[dict(label=b[0], rect=b[1:5]) for b in F['frontBays']])

# ---------------------------------------------------------------- the island of D-259 (F9 + G9 + H9) and its bridge with two tracks
COAST = [[6150, 7750], [6158, 7700], [6180, 7610], [6176, 7520], [6170, 7420], [6182, 7320], [6176, 7210], [6185, 7130], [6195, 7095], [6235, 7030], [6305, 6993],
         [6430, 6975], [6610, 6985], [6800, 6970], [7000, 6990], [7200, 6975], [7420, 6990], [7650, 6966], [7880, 6975], [8090, 6958], [8300, 6930], [8420, 6905],
         [8560, 6925], [8760, 6942], [8960, 6950], [9150, 6946], [9290, 6918], [9400, 6912], [9500, 6940], [9600, 6955], [9600, 7750]]
# the mountain: the contour lines of the plan's drawing (every second point), from the foot to the summit — schematic, the heights in stage 3
CONTOURS = [[[8968, 7433], [8946, 7515], [8911, 7595], [8864, 7673], [8802, 7749], [8718, 7750], [8606, 7750], [8471, 7750], [8322, 7750], [8172, 7750], [8032, 7750], [7901, 7750], [7772, 7750], [7634, 7750], [7481, 7750], [7314, 7750], [7147, 7750], [6995, 7750], [6874, 7750], [6786, 7750], [6729, 7750], [6690, 7671], [6662, 7591], [6642, 7512], [6633, 7433], [6646, 7354], [6686, 7278], [6753, 7209], [6839, 7147], [6932, 7090], [7024, 7036], [7115, 6978], [7211, 6917], [7323, 6857], [7457, 6807], [7610, 6778], [7772, 6776], [7929, 6800], [8069, 6844], [8191, 6895], [8301, 6946], [8411, 6991], [8527, 7032], [8650, 7075], [8768, 7127], [8868, 7192], [8936, 7267], [8968, 7349]], [[8820, 7442], [8801, 7515], [8769, 7586], [8728, 7656], [8673, 7723], [8598, 7750], [8499, 7750], [8378, 7750], [8246, 7750], [8114, 7750], [7989, 7750], [7872, 7750], [7758, 7750], [7636, 7750], [7499, 7750], [7352, 7750], [7203, 7750], [7068, 7750], [6960, 7750], [6882, 7750], [6831, 7726], [6798, 7654], [6773, 7582], [6754, 7512], [6747, 7442], [6758, 7372], [6794, 7305], [6853, 7243], [6929, 7188], [7012, 7138], [7094, 7089], [7174, 7038], [7260, 6983], [7359, 6930], [7478, 6886], [7614, 6861], [7758, 6859], [7897, 6880], [8022, 6919], [8130, 6964], [8228, 7009], [8325, 7049], [8429, 7086], [8537, 7124], [8643, 7170], [8731, 7228], [8792, 7295], [8820, 7368]], [[8672, 7451], [8655, 7515], [8628, 7577], [8592, 7638], [8544, 7696], [8478, 7750], [8392, 7750], [8286, 7750], [8171, 7750], [8055, 7750], [7946, 7750], [7844, 7750], [7744, 7750], [7637, 7750], [7518, 7750], [7389, 7750], [7259, 7750], [7141, 7750], [7047, 7750], [6979, 7750], [6934, 7700], [6904, 7636], [6883, 7574], [6867, 7512], [6860, 7451], [6870, 7390], [6901, 7331], [6953, 7277], [7020, 7229], [7092, 7185], [7163, 7142], [7234, 7098], [7309, 7050], [7395, 7004], [7499, 6965], [7618, 6943], [7744, 6941], [7866, 6960], [7975, 6994], [8069, 7034], [8155, 7073], [8240, 7108], [8330, 7139], [8425, 7173], [8517, 7214], [8594, 7264], [8647, 7322], [8672, 7386]], [[8524, 7460], [8510, 7515], [8486, 7568], [8456, 7620], [8414, 7670], [8358, 7716], [8284, 7750], [8194, 7750], [8095, 7750], [7996, 7750], [7903, 7750], [7816, 7750], [7730, 7750], [7638, 7750], [7536, 7750], [7426, 7750], [7315, 7750], [7214, 7750], [7133, 7750], [7075, 7727], [7037, 7673], [7012, 7618], [6993, 7565], [6979, 7512], [6974, 7460], [6982, 7408], [7009, 7357], [7053, 7311], [7110, 7270], [7172, 7232], [7233, 7196], [7293, 7158], [7357, 7117], [7432, 7077], [7520, 7044], [7622, 7025], [7730, 7024], [7834, 7040], [7927, 7068], [8008, 7103], [8082, 7136], [8154, 7166], [8232, 7193], [8313, 7222], [8392, 7257], [8458, 7300], [8503, 7350], [8524, 7404]], [[8377, 7469], [8364, 7514], [8345, 7559], [8319, 7602], [8285, 7644], [8238, 7682], [8177, 7714], [8102, 7736], [8020, 7749], [7937, 7750], [7860, 7750], [7787, 7750], [7716, 7750], [7640, 7750], [7555, 7750], [7463, 7750], [7371, 7750], [7287, 7750], [7220, 7733], [7171, 7691], [7140, 7646], [7118, 7601], [7103, 7556], [7092, 7513], [7087, 7469], [7094, 7426], [7116, 7384], [7153, 7345], [7200, 7311], [7252, 7280], [7303, 7249], [7353, 7217], [7406, 7184], [7468, 7151], [7542, 7123], [7626, 7107], [7716, 7106], [7803, 7119], [7880, 7143], [7948, 7172], [8008, 7200], [8069, 7224], [8133, 7247], [8201, 7271], [8266, 7300], [8321, 7336], [8359, 7377], [8376, 7423]], [[8229, 7478], [8219, 7514], [8204, 7550], [8183, 7584], [8156, 7617], [8119, 7648], [8070, 7673], [8010, 7691], [7944, 7701], [7878, 7704], [7816, 7705], [7759, 7708], [7702, 7714], [7641, 7723], [7574, 7733], [7500, 7737], [7427, 7732], [7360, 7715], [7306, 7688], [7268, 7655], [7242, 7619], [7226, 7583], [7213, 7548], [7204, 7513], [7200, 7478], [7206, 7443], [7224, 7410], [7253, 7379], [7291, 7352], [7332, 7327], [7372, 7303], [7412, 7277], [7455, 7250], [7504, 7224], [7563, 7202], [7631, 7190], [7702, 7188], [7771, 7199], [7833, 7218], [7887, 7241], [7935, 7263], [7983, 7283], [8035, 7301], [8089, 7320], [8141, 7343], [8185, 7372], [8215, 7405], [8229, 7441]], [[8081, 7487], [8074, 7514], [8062, 7540], [8047, 7566], [8027, 7591], [7999, 7614], [7962, 7633], [7918, 7646], [7869, 7653], [7820, 7656], [7773, 7656], [7730, 7658], [7688, 7663], [7643, 7670], [7592, 7677], [7538, 7680], [7483, 7676], [7433, 7664], [7393, 7644], [7364, 7619], [7345, 7592], [7332, 7565], [7323, 7539], [7316, 7513], [7314, 7487], [7318, 7461], [7331, 7436], [7353, 7413], [7381, 7393], [7412, 7374], [7442, 7356], [7472, 7337], [7504, 7317], [7540, 7298], [7584, 7281], [7635, 7272], [7688, 7271], [7740, 7279], [7786, 7293], [7826, 7310], [7862, 7327], [7898, 7342], [7936, 7355], [7976, 7369], [8015, 7386], [8048, 7408], [8070, 7432], [8081, 7460]], [[7933, 7496], [7928, 7514], [7921, 7531], [7911, 7548], [7897, 7565], [7879, 7580], [7855, 7592], [7825, 7601], [7793, 7606], [7761, 7608], [7730, 7608], [7702, 7609], [7674, 7612], [7644, 7617], [7611, 7621], [7575, 7624], [7538, 7621], [7506, 7613], [7479, 7600], [7460, 7583], [7448, 7566], [7440, 7548], [7434, 7530], [7429, 7513], [7427, 7496], [7430, 7479], [7439, 7462], [7453, 7447], [7472, 7434], [7492, 7422], [7512, 7410], [7532, 7397], [7552, 7384], [7577, 7371], [7606, 7360], [7639, 7354], [7674, 7353], [7708, 7359], [7738, 7368], [7765, 7379], [7789, 7390], [7812, 7400], [7838, 7409], [7864, 7418], [7890, 7430], [7912, 7444], [7926, 7460], [7933, 7478]], [[7785, 7505], [7783, 7514], [7779, 7522], [7775, 7530], [7768, 7538], [7759, 7546], [7748, 7552], [7733, 7556], [7718, 7558], [7702, 7559], [7687, 7559], [7674, 7560], [7660, 7561], [7646, 7564], [7629, 7566], [7612, 7567], [7594, 7566], [7578, 7562], [7566, 7555], [7557, 7547], [7551, 7539], [7546, 7530], [7544, 7522], [7541, 7513], [7541, 7505], [7542, 7497], [7546, 7489], [7553, 7481], [7562, 7475], [7572, 7469], [7582, 7463], [7591, 7457], [7601, 7451], [7613, 7444], [7627, 7439], [7643, 7436], [7660, 7436], [7676, 7438], [7691, 7443], [7704, 7448], [7716, 7454], [7727, 7458], [7739, 7463], [7752, 7467], [7764, 7473], [7775, 7480], [7782, 7488], [7785, 7496]]]
WATER = [[[6080, 7290], [6800, 7290], [6822, 7312], [6822, 7500], [6800, 7522], [6080, 7522]], [[6080, 7092], [6522, 7092], [6522, 7238], [6080, 7238]]]
def island():
    L = []
    def lot(id, he, kind, r, **kw): L.append(dict(id=id, label=he, kind=kind, rect=R(r), zone=zone_of(r), future=True, stage=kw.pop('stage', '12'), **kw))
    lot('IS-STATION', 'מבנה תחנת האי', 'building', [8640, 7395, 8760, 7465], floors=2)
    lot('IS-SHOP', 'חנות האי ושירותים', 'building', [8530, 7430, 8630, 7480], floors=1)
    lot('IS-P', 'חניון התחנה — 30 מקומות', 'parking', [8445, 7600, 8640, 7725], stalls=30)
    lot('IS-TURN', 'רחבת הסיבוב של קו 3', 'yard', [8740, 7640, 8890, 7740])
    lot('IS-CABLE-LOW', 'התחנה התחתונה של הרכבל', 'building', [8470, 7250, 8550, 7320], floors=1, stage='18')
    lot('IS-CABLE-TOP', 'התחנה העליונה וקפה הפסגה', 'building', [7675, 7418, 7809, 7522], floors=1, stage='18')
    lot('IS-VILLAGE', 'כפר ההר — 5 בתים', 'building', [7144, 7186, 7494, 7453], floors=1)
    lot('IS-HOSTEL', 'אכסניית ההר', 'building', [7680, 7192, 7900, 7324], floors=2)
    lot('IS-HOSTEL-P', 'החניה של האכסניה', 'parking', [7905, 7240, 8035, 7295], stalls=6)
    lot('IS-LIGHT', 'המגדלור ובית השומר', 'building', [9215, 6930, 9420, 7045], floors=2)
    lot('IS-HELI', 'מנחת האי — קוטר 20 מ׳', 'pad', [9020, 7000, 9220, 7200])
    lot('IS-FERRY', 'מעגן המעבורת — 486 × 140', 'pier', [6276, 7296, 6762, 7436], stage='18')
    lot('IS-BOATS', '6 מקומות לסירות', 'pier', [6222, 7094, 6522, 7236], stage='18')
    lot('IS-WAIT', 'נתיבי ההמתנה למעבורת, הסככה והקופה', 'yard', [6835, 7312, 7140, 7536])
    lot('IS-SLIP', 'מדרון השקה וחניית נגררים', 'yard', [6120, 7590, 6470, 7700])
    lot('IS-BEACH', 'חוף החול', 'beach', [6320, 6995, 7300, 7085])
    lot('IS-SUMMIT', 'יער הפסגה והתצפית', 'park', [7200, 7340, 8060, 7690])
    roads = [dict(id='IS-HARBOR', label='דרך הנמל — אל המעבורת והמדרון', cls='local', pts=[[6900, 7262], [6900, 7560], [6475, 7560]]),
             dict(id='IS-LANE', label='שביל הכפר', cls='service', pts=[[7330, 7141], [7330, 7186]]),
             dict(id='IS-SVC', label='דרך השירות למגדלור ולמנחת — מסביב לסוף המסילה (עתידית, לא נבדקה)', cls='service', pts=[[8890, 7690], [9290, 7690], [9290, 7050]]),
             dict(id='IS-TRACK', label='דרך עפר לפסגה (שירות)', cls='track', pts=[[7960, 7295], [7960, 7440], [7809, 7470]])]
    cable = [[8509.1, 7286.7], [7742, 7470]]
    return dict(coast=COAST, water=WATER, lots=L, roads=roads, cable=cable, summit=[7660, 7505], contours=CONTOURS, label='האי — F9 + G9 + H9 (D‑259)')

# ---------------------------------------------------------------- the rails: today's lines, and the future ones of the plan
def offset_line(p, d):
    out = []
    for i in range(len(p)):
        ns = []
        for j in (i - 1, i):
            if 0 <= j < len(p) - 1:
                dx, dy = p[j + 1][0] - p[j][0], p[j + 1][1] - p[j][1]; l = math.hypot(dx, dy) or 1; ns.append((dy / l, -dx / l))
        nx, ny = sum(n[0] for n in ns), sum(n[1] for n in ns); l = math.hypot(nx, ny) or 1
        out.append([round(p[i][0] + nx / l * d, 1), round(p[i][1] + ny / l * d, 1)])
    return out
# ---------------------------------------------------------------- 1.11 00:21 (the owner): the rails, all of them, end to end
# Sources (read only): the game today (RAIL_SEGS / PORT_TRACKS / the port rail graph / RA_TRACKS / E3_PLATFORMS / PORT_PLATFORM in
# Turbo_City_v1_96_GATE77_S7F177), part ד (the island line, the reversing siding, the coast strip with the freight bypass of D-130 at
# x 5967–6033), part ו (Rail–Air: T1 x 5800, T2 x 5900 to the buffers at y 580 — D-01, D-03, D-14), the master plan (E3 the central
# station, the coast station west of MAIN-A, D-130 / QA-68; E5 the yard of 3 tracks; C6 / D6 / E6 the quay tracks), D-177 (the refinery).
# Every line ends only at a buffer (a station, a terminal, the yard, the end of a quay track), at the edge of the world, or on another
# line (a turnout) — the check "המסילות" proves it.
def _arc(cx, cy, r, a0, a1, n=24): return [[round(cx + r * math.cos(a0 + (a1 - a0) * i / n), 1), round(cy + r * math.sin(a0 + (a1 - a0) * i / n), 1)] for i in range(n + 1)]
def _bez(p0, p1, p2, p3, n=14):
    out = []
    for i in range(n + 1):
        t = i / n; a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append([round(a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], 1), round(a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1], 1)])
    return out
def _sv(x0, y0, x1, y1): ym = (y0 + y1) / 2; return _bez((x0, y0), (x0, ym), (x1, ym), (x1, y1))   # an S along y (a crossover / a turnout)
def _sh(x0, y0, x1, y1): xm = (x0 + x1) / 2; return _bez((x0, y0), (xm, y0), (xm, y1), (x1, y1))   # an S along x
def _off(p, d):
    out = []
    for i in range(len(p)):
        a = p[max(0, i - 1)]; b = p[min(len(p) - 1, i + 1)]; ux, uy = b[0] - a[0], b[1] - a[1]; l = math.hypot(ux, uy) or 1
        out.append([round(p[i][0] - uy / l * d, 1), round(p[i][1] + ux / l * d, 1)])
    return out
ASW_A = math.asin(110 / 150); P2J_X = round(5400 + 150 * math.cos(ASW_A), 1)
def rails(RAIL=None):
    """every track of the city: id, the Hebrew name, the kind, today / future (with the stage), the points, and its two ends:
    ('join', line) on another line, ('buffer', where), ('door', where) or ('edge', where)"""
    out = []
    def L(id, he, kind, pts, ends, state='today', stage=None, note=''):
        out.append(dict(id=id, label=he, kind=kind, pts=[[round(x, 1), round(y, 1)] for x, y in pts], ends=ends, state=state, stage=stage, note=note))
    TA = [[round(x, 1), round(y, 1)] for x, y in D['TRACK_A']]; SA, SB = D['STATION_A'], D['STATION_B']
    # the main line: two tracks from the buffers of Rail–Air (y 580) through the central station (E3), the yard (E5) and the port platform
    L('MAIN-A', 'הקו הראשי — פס א׳ (דרומה)', 'main', [[5800, 580], [5800, 4720]] + _arc(5400, 4720, 400, 0, math.pi / 2)[1:],
      [('buffer', 'בולמים במסוף רכבת–אוויר (y 580)'), ('join', 'W1')], note='T1 של רכבת–אוויר מצפון לגשר; בדרום — קשת R400 אל מסילת הרציף (Q-E)')
    L('MAIN-B', 'הקו הראשי — פס ב׳ (צפונה)', 'main', [[5900, 580], [5900, 4720]] + _arc(6300, 4720, 400, math.pi, math.pi / 2)[1:],
      [('buffer', 'בולמים במסוף רכבת–אוויר (y 580)'), ('join', 'EAST')], note='T2 של רכבת–אוויר; בדרום — B-LINK אל מסילת הנמל המזרחית (B-J)')
    L('X-S', 'מעבר פסים מצפון לחצר (XS)', 'xover', _sv(5900, 2980, 5800, 2808), [('join', 'MAIN-B'), ('join', 'MAIN-A')])
    L('X-N', 'מעבר פסים מצפון לחצר (XN)', 'xover', _sv(5900, 3170, 5800, 3342), [('join', 'MAIN-B'), ('join', 'MAIN-A')])
    L('X-P', 'מעבר פסים ליד רציף הנמל (XOVER)', 'xover', _sv(5800, 4462, 5900, 4290), [('join', 'MAIN-A'), ('join', 'MAIN-B')])
    # the port: three tracks along the quay — the parking track P (y 5080), work track W1 (y 5120), work track W2 (y 5158)
    L('W1', 'מסילת העבודה W1 של הרציף (y 5120) — מנופי E6', 'port', [[2560, 5120], [6000, 5120]],
      [('buffer', 'סוף מסילת הרציף (C6)'), ('join', 'EAST')])
    L('W2', 'מסילת העבודה W2 של הרציף (y 5158) — מנופי C6', 'port', [[2585, 5158], [5600, 5158]] + _sh(5600, 5158, 5795, 5120)[1:],
      [('buffer', 'סוף מסילת הרציף (C6)'), ('join', 'W1')])
    L('X-Q2', 'מעבר פסים W1–W2', 'xover', _sh(3760, 5120, 3957, 5158), [('join', 'W1'), ('join', 'W2')])
    L('P1', 'מסילת החניה P1 (y 5080) — רכבת העבודה של C6', 'port', [[2620, 5080], [3563, 5080]] + _sh(3563, 5080, 3760, 5120)[1:],
      [('buffer', 'סוף מסילת החניה (C6)'), ('join', 'W1')])
    L('P2', 'מסילת החניה P2 (y 5080) — קרונות התפזורת של D6 / E6', 'port',
      [[4345, 5080], [P2J_X, 5080]] + _arc(P2J_X, 4830, 250, math.pi / 2, ASW_A, 16)[1:],
      [('buffer', 'סוף מסילת החניה (D6)'), ('join', 'MAIN-A')])
    L('EAST', 'מסילת הנמל המזרחית (EAST-LINE) — על גשרים, יוצאת מהעולם', 'east', [[6000, 5120], [9600, 5120]],
      [('join', 'W1'), ('edge', 'יוצאת מהמפה מזרחה (FRT-2 / FRT-3)')])
    # the yard of E5: three tracks from the depot doors, two leads and the spur to the port platform
    L('Y-LEAD-N', 'כניסה צפונית לחצר', 'yard', _sv(5800, 3576, 5746, 3716), [('join', 'MAIN-A'), ('join', 'Y1')])
    L('Y1', 'חצר הרכבות — פס 1', 'yard', [[5746, 3592], [5746, 4120]], [('door', 'דלת המוסך 1'), ('join', 'Y-LEAD-S')])
    L('Y-LEAD-S', 'כניסה דרומית לחצר', 'yard', _sv(5746, 4120, 5800, 4236), [('join', 'Y1'), ('join', 'MAIN-A')])
    L('Y2', 'חצר הרכבות — פס 2', 'yard', [[5698, 3592], [5698, 4050]], [('door', 'דלת המוסך 2'), ('buffer', 'בולמים בחצר')])
    L('Y-X12', 'מסוט פס 1–2', 'xover', _sv(5746, 3732, 5698, 3832), [('join', 'Y1'), ('join', 'Y2')])
    L('Y3', 'חצר הרכבות — פס 3', 'yard', [[5650, 3592], [5650, 4022]], [('door', 'דלת המוסך 3'), ('buffer', 'בולמים בחצר')])
    L('Y-X23', 'מסוט פס 2–3', 'xover', _sv(5698, 3848, 5650, 3948), [('join', 'Y2'), ('join', 'Y3')])
    L('SPUR', 'שלוחת הנמל מהחצר (PORT-SPUR)', 'yard', [[5746, 4120], [5746, 4700]], [('join', 'Y1'), ('buffer', 'בולמים מול הרציף')])
    # the freight bypass (D-130): a third track for the freight of the airport, around the passenger station — in the coast strip
    # (x 5967–6033, beside the fence and the coast road), from MAIN-B in the south to MAIN-B north of the station; stage 14
    # 1.11 (R-47, the owner 10:54): the split moves north of the crossovers — at y 2900 on MAIN-B, after X-P (4290), X-N (3170) and X-S (2980):
    # a freight train from the port (W1 → MAIN-A → X-P) or from the yard (Y-LEAD-N → MAIN-A → X-N) is on MAIN-B before the split, and goes
    # round the station without a reversal (the routes check, plan7b_rails.py)
    L('BYPASS', 'מסילת העקיפה למשא (D‑130) — עוקפת את התחנה, אל מסוף רכבת–אוויר', 'freight',
      _sv(5900, 2900, 6000, 2720) + [[6000, 1900]] + _sv(6000, 1900, 5900, 1720)[1:],
      [('join', 'MAIN-B'), ('join', 'MAIN-B')], state='future', stage='14',
      note='רכבות המשא לשדה (FRT-1 / FRT-4) לא עוברות ליד הרציפים של E3; יוצאת מ-MAIN-B ב-y 2900, מצפון לשלושת מעברי הפסים — כך גם רכבת מהנמל ומהחצר עולה עליה בלי להתהפך (R-47)')
    # the island (part ד, D-187, D-242, D-259): from the switch on EAST at (6380, 5120) — two tracks on the whole bridge, the S and the deck
    pA = TA + [[round(SA[0][0], 1), round(SA[0][1], 1)]]
    pB = [TA[2]] + _off(TA, 45)[8:] + [[round(SB[0][0], 1), round(SB[0][1], 1)]]
    L('ISL-A', 'המסילה לאי — פס א׳', 'island', pA, [('join', 'EAST'), ('join', 'ISL-ST-A')], state='future', stage='12',
      note='מהמסוט על EAST-B (6380, 5120), דרך ה-S ועל הסיפון המשותף (D‑187)')
    L('ISL-B', 'המסילה לאי — פס ב׳', 'island', pB, [('join', 'ISL-A'), ('join', 'ISL-ST-B')], state='future', stage='12',
      note='מתפצל מפס א׳ אחרי המסוט; 4.5 מ׳ ממנו לכל אורך הגשר (D‑242), ונפתח לרוחב התחנה')
    L('ISL-ST-A', 'תחנת האי — פס א׳', 'island', SA, [('join', 'ISL-A'), ('buffer', 'בולמים בתחנת האי')], state='future', stage='12')
    L('ISL-ST-B', 'תחנת האי — פס ב׳', 'island', SB, [('join', 'ISL-B'), ('buffer', 'בולמים בתחנת האי')], state='future', stage='12')
    L('SIDING', 'מסילת ההיפוך של רכבת השדה (חלק ד)', 'siding', D['SIDING'], [('join', 'EAST'), ('buffer', 'בולמים בסוף מסילת ההיפוך')], state='future', stage='12')
    # the refinery spur (D-177): crude in tank cars from the oil terminal to the refinery of C5 — from the parking track P1; stage 14
    L('REF-SPUR', 'מסילת בית הזיקוק (D‑177)', 'freight', _arc(2930, 4930, 150, math.pi / 2, math.pi, 12) + [[2780, 3950]], [('join', 'P1'), ('buffer', 'בולמים בבית הזיקוק (C5)')],   # 1.11 (R-47): a real turnout — a curve of R 150 from P1 westbound to the north (it was a right angle)
      state='future', stage='14')
    return out
# the stations and the terminals (rects in px)
STATIONS = [dict(id='ST-E3', label='התחנה המרכזית (E3) — 2 רציפים', kind='pax', rects=[[5736, 1850, 5774, 2290], [5826, 1850, 5874, 2290]], state='today'),
            dict(id='ST-COAST', label='תחנת החוף (D‑130) — רציף ממערב לפס א׳', kind='pax', rects=[[5736, 2700, 5774, 3560]], state='future', stage='17'),
            dict(id='ST-PORT', label='רציף הנמל — בין שני הפסים', kind='pax', rects=[[5826, 4470, 5874, 4690]], state='today'),
            dict(id='ST-RAILAIR', label='מסוף רכבת–אוויר — העמסת מכולות (קיים)', kind='freight', rects=[[5752, 790, 5948, 1516]], state='today'),
            dict(id='ST-ISLAND', label='תחנת האי — רציף של 1,000 מ׳ בין שני הפסים', kind='pax', poly='island', state='future', stage='12')]
# the passenger line (stage 17): E3 → the coast station → the port platform → the island, and back on track B — no reversing on the line
def pax_line():
    TA = [[round(x, 1), round(y, 1)] for x, y in D['TRACK_A']]; SA, SB = D['STATION_A'], D['STATION_B']
    south = [[5800, 1850], [5800, 4720]] + _arc(5400, 4720, 400, 0, math.pi / 2)[1:] + [[6380, 5120]] + TA[1:] + [list(SA[0]), list(SA[1])]
    north = [list(SB[1]), list(SB[0])] + (_off(TA, 45)[8:])[::-1] + [TA[2], [6380, 5120], [6300, 5120]] + _arc(6300, 4720, 400, math.pi / 2, math.pi)[1:] + [[5900, 1850]]
    return dict(id='PAX', label='קו הנוסעים (עתידי, שלב 17): E3 ← תחנת החוף ← רציף הנמל ← האי', south=south, north=north, stage='17',
                stops=['ST-E3', 'ST-COAST', 'ST-PORT', 'ST-ISLAND'])

# ---------------------------------------------------------------- helpers
COLS = [0, 1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600]; ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
def zone_of_pt(x, y):
    i = next((k for k in range(8) if COLS[k] <= x < COLS[k + 1]), None); j = next((k for k in range(10) if ROWS[k] <= y < ROWS[k + 1]), None)
    return None if i is None or j is None else 'ABCDEFGH'[i] + str(j)
def zone_of(r): return zone_of_pt((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)

# ---------------------------------------------------------------- the uses of every zone (uses.json): the names of the lots
def zone_uses():
    out = {}
    for t in U['types']:
        for a in t.get('target', []):
            if isinstance(a, dict) and a.get('zone'): out.setdefault(a['zone'], []).append(t.get('he') or t['type'])
    return out
# the size of a lot by the kind of the zone: frontage × depth (m)
LOTSIZE = {'home': (28, 34), 'shop': (42, 44), 'work': (50, 55), 'port': (60, 60), 'rail': (55, 55), 'forest': (120, 110), 'fields': (110, 110),
           'park': (60, 60), 'coast': (50, 40), 'public': (40, 40), 'sport': (50, 50), 'air': (60, 60)}
LOTFILL = {'home': '#f3dfb8', 'shop': '#f2c7b8', 'work': '#d9cfe6', 'port': '#c9d3dd', 'rail': '#d8d1c4', 'forest': '#b9d6a3', 'fields': '#e2d68f',
           'park': '#b8dda6', 'coast': '#f1e2b2', 'public': '#c9dced', 'sport': '#bfe3c6', 'air': '#d6d6d0'}
