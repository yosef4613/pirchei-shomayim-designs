# -*- coding: utf-8 -*-
"""1.11 round 6 (R-43, the review 11:50): every free parcel of 15 × 15 m or more in a zone of the city gets a use.
The free parcels are found by plan7b_free.scan on the finished map (roads at their section, rails, every lot and item, the bus terminal
and the platforms). Each parcel takes the use written for it here — from the master plan (its contents and its green), the uses table
(D-260: what the zone keeps or adds and the map had no place for) and the zone's own file for the zones built in the game.
A parcel is matched by a point inside it; a parcel with no row here takes the green of its zone from the master plan (a garden, a field,
trees) — and is listed in the check, so a new free parcel never goes by without a word.
use: the colour of the parcel on the map (LOTFILL); the green uses (park, fields, coast, forest) need no road — on foot from the road next to them."""
GREEN = ('park', 'fields', 'coast', 'forest')
MP = 'תוכנית האב (%s): '
UT = 'טבלת השימושים (D‑260): '
PLAN = {
    'C1': [((2650, 200), 'שדות הכפר', 'fields', MP % 'C1' + 'שדות; בלי מבנים גבוהים מתחת לנתיב הגישה לשדה.'),
           ((3450, 250), 'מטע עצי פרי', 'fields', MP % 'C1' + 'הירוק — שדות, עצי פרי בכפר.'),
           ((2520, 530), 'גינות הכפר ועצי פרי', 'fields', MP % 'C1' + 'הירוק — עצי פרי בכפר, ליד הבתים.')],
    'D1': [((3900, 120), 'שדה פתוח — צפון', 'fields', MP % 'D1' + 'שדות וחממות נמוכות.'),
           ((4680, 120), 'שדה פתוח — הפינה הצפונית-מזרחית', 'fields', MP % 'D1' + 'שדות.'),
           ((3700, 470), 'שדה פתוח — מערב', 'fields', MP % 'D1' + 'שדות.'),
           ((4580, 770), 'שדה פתוח — דרום', 'fields', MP % 'D1' + 'שדות.')],
    'A2': [((790, 1150), 'שדרת העצים של בית החולים', 'park', MP % 'A2' + 'הירוק — שדרת עצים וגינת החלמה.')],
    'C2': [((3100, 1350), 'פינת ישיבה, חניות נכים וטעינה לסופר', 'shop', UT + 'נוסף ב-C2 (במקום המכולת C2-MINI); על המגרש שפינתה תחנת הדלק, שעברה ל-C4.'),
           ((3110, 1060), 'שתי הווילות של C2 (C2-VILLA-1, ‏C2-VILLA-2)', 'home', UT + 'החניון האחורי מצטמצם לטובת מגרשים אמיתיים לשתי הווילות ועצים (EYE‑4).')],
    'D2': [((4030, 1200), 'קמפוס ההייטק — 3 מבנים בגבהים שונים וחצר פנימית', 'shop', MP % 'D2' + 'קמפוס ההייטק (D‑141); ' + UT + 'מגדל הקמפוס והחצר הפנימית.'),
           ((4450, 1020), 'כיכר המטה — הורדה, חניות אורחים ועצים', 'shop', UT + 'נוסף ב-D2: כיכר המטה.')],
    'E3': [((5170, 2400), 'מחסן החבילות של התחנה (E3-PARCELS)', 'rail', UT + 'נשאר ב-E3 — מסוף ומחסן מטען הרכבת, ליד התחנה.')],
    'F3': [((6400, 1950), 'חניון המרינה', 'coast', MP % 'F3' + 'חוף המרינה: חניון (y 1830–2000).')],
    'B4': [((1600, 2920), 'הגינה שבין N0 ל-N2 — עצים, ערוגות וספסלים', 'park', 'B4 v5 — מהקובץ של האזור (b4v5.json): 5 עצים, 4 ערוגות, 4 ספסלים וממטרה.'),
           ((2315, 2660), 'רצועת העצים לאורך שדרת המרכז', 'park', 'B4 v5 — מהקובץ של האזור (b4v5.json): 8 עצים, שיחים וספסל.')],
    'D4': [((4250, 2930), 'מגרש המכולות', 'work', MP % 'D4' + 'מחסנים, רציפי העמסה, מגרש מכולות (קיים).'),
           ((3735, 2645), 'מסוף ומחסן מטען הרכבת (D4-RAIL)', 'work', UT + 'נשאר ב-D4.')],
    'E4': [((5530, 3200), 'מוסך הרכבות ובקרת המסילה (E4-RAIL-WS, ‏E4-RAIL-CTRL)', 'rail', UT + 'נשארים ב-E4.'),
           ((5060, 3310), 'סדנת הצי של העירייה (E4-CITY-WS)', 'rail', UT + 'נשארת ב-E4.')],
    'F4': [((6350, 2990), 'חוף הרחצה ומגדל המציל', 'coast', MP % 'F4' + 'חוף רחצה x 6230–6520; ' + UT + 'מגדל מציל.'),
           ((6430, 2660), 'דקלים וצמחיית חוף', 'coast', MP % 'F4' + 'הירוק — דקלים וצמחיית חוף.')],
    'A4': [((640, 3095), 'מדשאת החימום בתוך מסלול הריצה', 'park', MP % 'A4' + 'מבני ספורט, מגרשים, מסלול — המדשאה שבתוך מסלול הריצה (סבב 7).')],
    'B5': [((1975, 3535), 'מדשאות הקמפוס', 'park', MP % 'B5' + 'הירוק — קמפוס ירוק עם מדשאות.')],
    'E5': [((5465, 3820), 'מסוף המטען ומחסן הרכבת (E5-FREIGHT, ‏E5-RAIL-WH)', 'rail', UT + 'נשארים ב-E5; נכנסים דרך מחסן הנמל שמול שדרת המזרח.'),
           ((5060, 3490), 'מחסן הנמל (E5-PORT-WH)', 'rail', UT + 'נשאר ב-E5.')],
    'A6': [((200, 4900), 'מטע', 'fields', MP % 'A6' + 'הירוק — שדות, מטעים.'),
           ((420, 4330), 'ערוגות השתילה והקציר (D‑208)', 'fields', MP % 'A6' + 'שתילה, קציר ומכירה (D‑208).')],
    'B6': [((2245, 4465), 'ביתן החוף (B6-PAVILION) ודיונות', 'coast', UT + 'נשאר ב-B6; ' + MP % 'B6' + 'הירוק — דיונות.'),
           ((1380, 4465), 'דקלים ופינת צל', 'coast', MP % 'B6' + 'הירוק — דקלים וצמחיית חוף.')],
    'C6': [((2655, 4605), 'שער הנמל המערבי ומשרד המכס (C6-GATE-W, ‏C6-CUSTOMS)', 'port', UT + 'נשארים ב-C6.')],
    'D6': [((4275, 4455), 'מחסן הנמל 1 (D6-WH1)', 'port', UT + 'נשאר ב-D6.')],
}
DEFAULT = {'home': ('גינה שכונתית', 'park'), 'shop': ('עצי רחוב ואדניות', 'park'), 'public': ('גינה ציבורית', 'park'), 'work': ('חיץ עצים', 'park'),
           'port': ('חיץ עצים', 'park'), 'rail': ('שיחים לאורך הגדר', 'park'), 'fields': ('שדה', 'fields'), 'coast': ('צמחיית חוף', 'coast')}


def name_for(z, kind, rect):
    """the use of a free parcel: its row in PLAN (a point inside it), or the green of its zone (and False — not planned)"""
    for (x, y), nm, use, why in PLAN.get(z, []):
        if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]: return nm, use, why, True
    nm, use = DEFAULT.get(kind, ('גינה', 'park'))
    return nm, use, 'אין לו שורה בתוכנית — הירוק של האזור.', False
