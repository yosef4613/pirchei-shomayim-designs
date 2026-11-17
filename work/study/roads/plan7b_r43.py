# -*- coding: utf-8 -*-
"""1.11 round 6 (R-43, the review 11:50 and 12:20): the zones whose uses the map was missing, drawn item by item.
C4 (the light industry) — detailed: every use of the uses table (D-260) with its real size (the game's own buildings, sizes.json)
  on the new network (AR-C on the west, LC-C4 "חצר המפעלים" in the middle, CL-T on the south). Fuel station 2 and fire station 2
  come here from C2 and from the north of C5 (the uses table: "שדרת המרכז מקבלת שני שירותים לכל העיר").
C5 (the refinery) — the north block that fire station 2 leaves gets the dispatch office, the substation, the docks and the fleet
  workshop; the café, the drivers' toilets and the gatehouse — inside the truck park (the uses table: "חניון המשאיות").
Where the new network does not leave a building where the game has it, it moves the least it can — written in its row, for the owner."""


def add(S, DW):
    def it(zone, id, kind, rect, label, why, **kw): S.append(dict(zone=zone, id=id, kind=kind, rect=rect, label=label, why=why, **kw))
    def dw(zone, id, road, at, label, why, to=None, lanes='1+1'): DW.append(dict(zone=zone, id=id, road=road, at=at, label=label, why=why, to=to, lanes=lanes))
    T = 'טבלת השימושים (D‑260): '
    # ================================================================ C4 — the light industry (detailed)
    # the west column, on שדרת המרכז (AR-C, edge x 2623) and חצר המפעלים (LC-C4, edge x 3056): from north to south
    it('C4', 'C4-HARDWARE', 'building', (2631, 2560, 2883, 2790), 'כלי עבודה תעשייתיים — חנות — 25 × 23 מ׳', T + 'הפינה הצפונית-מערבית של C4, על שדרת המרכז; הדלת לשדרה. המבנה של המשחק (sizes.json: ‏252 × 230 פיקסלים).', floors=1, real=(25.2, 23), use='shop')
    it('C4', 'C4-HARDWARE-P', 'parking', (2893, 2560, 3044, 2790), 'החניון של חנות כלי העבודה — 12 מקומות', 'מאחורי החנות; נכנסים מקצה רחוב חצר המפעלים.', stalls=12)
    dw('C4', 'DW-C4-HARDWARE', 'LC-C4', (3056, 2785), 'הכניסה לחניון של חנות כלי העבודה', 'בקצה רחוב חצר המפעלים — לא צומת.', to=(3040, 2775))
    it('C4', 'C4-FUEL', 'building', (2631, 2800, 2981, 2990), 'דלק טורבו 2 — 4 משאבות, גגון וחנות — 35 × 19 מ׳', T + 'על שדרת המרכז, בין חנות כלי העבודה למחסן (D‑243 (3)); מקבלת את עמדת השירות של B3 (D‑326). כניסה ויציאה ימינה בלבד מהשדרה.', floors=1, real=(35, 19))
    dw('C4', 'DW-C4-FUEL', 'AR-C', (2623, 2895), 'כניסה ויציאה לתחנת הדלק', 'ימינה בלבד משדרת המרכז, באמצע בין שני הצמתים.', to=(2634, 2895))
    it('C4', 'C4-FUEL-TANKER', 'yard', (2991, 2800, 3044, 2990), 'מפרץ המכלית של תחנת הדלק — 18 מ׳', 'בגב התחנה, מרחוב חצר המפעלים — המכלית לא עוצרת על השדרה (מכלית של 178 פיקסלים).')
    it('C4', 'C4-FIRE2', 'building', (2631, 3000, 2831, 3250), 'תחנת כיבוי 2 — 3 תאים — 20 × 25 מ׳', T + 'הקצה הדרום-מערבי של C4 על שדרת המרכז, בלוק אחד מבית הזיקוק (D‑243 (3), ‏D‑251); 3 תאים (2 כבאיות ומכלית קצף) שיוצאים ישר לשדרה, בלי עמוד בפתח.', floors=2, real=(20, 25), use='public')
    dw('C4', 'DW-C4-FIRE2', 'AR-C', (2623, 3125), 'רחבת היציאה של הכבאיות', 'ישר לשדרת המרכז — 30 מ׳ מהצומת עם רחוב התעשייה.', to=(2634, 3125))
    it('C4', 'C4-FIRE2-YARD', 'yard', (2631, 3260, 2831, 3333), 'חצר האימונים של הכבאים', 'מאחורי התאים, מול רחוב התעשייה.')
    it('C4', 'C4-DEPOT', 'building', (2841, 3000, 3015, 3235), 'מחסן הובלה קלה — 17 × 24 מ׳', T + 'נשאר ליד המקום שלו במשחק (D‑260: "במקומו"): 14 מ׳ מזרחה ו-1 מ׳ דרומה, כי רחוב חצר המפעלים החדש עובר במרכז הבלוק (לאישורך, D‑334).', floors=1, real=(17.4, 23.5))
    it('C4', 'C4-DEPOT-YARD', 'yard', (2841, 3245, 3044, 3333), 'חצר הפריקה של המחסן', 'משאית נכנסת מרחוב התעשייה ופורקת בדלת הדרומית של המחסן.')
    dw('C4', 'DW-C4-DEPOT', 'CL-T', (2930, 3341), 'הכניסה לחצר הפריקה של המחסן', '21 מ׳ מרחוב חצר המפעלים, 42 מ׳ משדרת המרכז.', to=(2930, 3300))
    # the north middle: the yard at the end of LC-C4 (the road ends in the yard of the factory, as on the map since round 3)
    it('C4', 'C4-YARD', 'yard', (3054, 2556, 3166, 2740), 'חצר הסיבוב בקצה רחוב חצר המפעלים', 'המשאית מסתובבת בקצה הרחוב ולא נכנסת לשדרה ברוורס.')
    # the east column, on LC-C4 (edge x 3164) and CL-T: a strip of trees, the factory, the docks, the dispatch office
    it('C4', 'C4-TREES', 'park', (3176, 2556, 3596, 2606), 'חיץ עצים מול C3', T + 'חיץ עצים מול השכנים (EYE‑2) — שורת עצים בין המפעל למגורים של C3.', use='park')
    it('C4', 'C4-FAB', 'building', (3186, 2616, 3490, 2874), 'מטרו עבודות מתכת — מפעל — 30 × 26 מ׳', T + 'נשאר כמעט במקומו (D‑260: "במקומו"): 24 מ׳ מזרחה, מעבר לקצה רחוב חצר המפעלים (לאישורך, D‑334); הדלת לחצר שמדרום.', floors=1, real=(30.4, 25.8))
    it('C4', 'C4-DOCKS-APRON', 'yard', (3176, 2884, 3390, 3104), 'חצר המפעל ומסוף הרציפים', 'החצר המשותפת של המפעל ושל הרציפים; נכנסים מרחוב חצר המפעלים.')
    dw('C4', 'DW-C4-DOCKS', 'LC-C4', (3164, 2994), 'הכניסה לחצר המפעל והרציפים', 'מרחוב חצר המפעלים, 41 מ׳ מרחוב התעשייה.', to=(3200, 2994))
    it('C4', 'C4-DOCKS', 'building', (3400, 2884, 3544, 3089), 'מסוף רציפי משאיות — 14 × 21 מ׳', T + 'במקומו בחצר (D‑260); הרציפים פונים לחצר המשותפת. 22 מ׳ מזרחה מהמקום שלו במשחק, כי רחוב חצר המפעלים עובר שם (לאישורך, D‑334).', floors=1, real=(14.4, 20.5))
    it('C4', 'C4-DISPATCH-P', 'parking', (3176, 3114, 3368, 3333), 'החניון של משרד השילוח — 14 מקומות', 'נכנסים מרחוב חצר המפעלים — לא מרחוב התעשייה, שבו עומדת התחנה של קו 5 (ST-15).', stalls=14)
    dw('C4', 'DW-C4-DISPATCH', 'LC-C4', (3164, 3220), 'הכניסה לחניון של משרד השילוח', 'מרחוב חצר המפעלים, 19 מ׳ מרחוב התעשייה.', to=(3200, 3220))
    it('C4', 'C4-DISPATCH', 'building', (3378, 3114, 3596, 3259), 'משרד שילוח C4 — 22 × 15 מ׳', T + 'במקומו (D‑260), בפינה הדרומית-מזרחית, ליד המקום שלו במשחק; הדלת לחניון.', floors=2, real=(21.8, 14.5))
    # ================================================================ C5 — the block that fire station 2 leaves (between LC-C5, CL-T and the truck park)
    W5 = T + 'נשאר בחצר של בית הזיקוק; '
    it('C5', 'C5-DISPATCH', 'building', (3176, 3500, 3394, 3645), 'משרד שילוח C5 — 22 × 15 מ׳', W5 + 'זז 15 מ׳ מהמקום שלו במשחק, שעליו עובר היום רחוב התעשייה החדש (לאישורך, D‑334); עיצוב ושלט משלו (ההערה של הטבלה על C4 ו-C5).', floors=2, r5=True)
    it('C5', 'C5-SUBSTATION', 'yard', (3404, 3467, 3596, 3645), 'תחנת המשנה — שנאים מגודרים — 19 × 18 מ׳', W5 + 'במקומה (D‑260), מזינה את בית הזיקוק; 15 מ׳ מזרחה מהמקום שלה במשחק.', r5=True)
    it('C5', 'C5-DOCKS', 'building', (3176, 3665, 3320, 3870), 'מסוף רציפי משאיות C5 — 14 × 21 מ׳', W5 + 'במקומו (D‑260) — כמעט בדיוק במקום שלו במשחק; הרציפים פונים לחניון המשאיות.', floors=1, r5=True)
    it('C5', 'C5-WORKSHOP', 'building', (3330, 3655, 3596, 3795), 'סדנה / מוסך צי — 27 × 14 מ׳', W5 + 'זז מקו רחוב התעשייה החדש אל הבלוק, 26 מ׳ דרומה (לאישורך, D‑334).', floors=1, r5=True)
    it('C5', 'C5-WORKSHOP-YARD', 'yard', (3330, 3805, 3596, 3870), 'חצר המוסך', 'פתוחה לחניון המשאיות.', r5=True)
    it('C5', 'C5-CAFE', 'building', (3470, 3890, 3540, 3950), 'בית קפה הנהגים — 7 × 6 מ׳', W5 + 'בחניון המשאיות, ליד השירותים של הנהגים — במקומו.', floors=1, r5=True, parent='C5-TRUCKS')
    it('C5', 'C5-WC', 'building', (3480, 3990, 3540, 4040), 'שירותים ציבוריים לנהגים — 6 × 5 מ׳', W5 + 'בחניון המשאיות — במקומם.', floors=1, r5=True, parent='C5-TRUCKS')
    it('C5', 'C5-GATE', 'building', (3195, 4060, 3235, 4100), 'ביתן שער הלוגיסטיקה — 4 × 4 מ׳', W5 + 'בשער של חניון המשאיות, ליד הכניסה מרחוב בית הזיקוק.', floors=1, r5=True, parent='C5-TRUCKS')
