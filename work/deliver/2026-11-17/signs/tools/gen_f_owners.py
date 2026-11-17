#!/usr/bin/env python3
# gen_f_owners.py — הערות הבקר (planrev/signs.txt §1): לכל אחד מ-128 המסכים של Review_part2 (73 בלי כפתור + 55 רק ניווט) — מה הפעולה שלו ולמי.
# הקלט: הטבלאות של Review_part2; הפלט: W/deliver/2026-11-17/signs/F_owners_128.tsv
import re, sys, collections
W='/home/user/tc_root/tc/pkg/work'; R=W+'/deliver/2026-11-12/review/Review_part2_F_logos_vehicles_island_airfield_1112.md'
L=open(R,encoding='utf-8').read().split('\n')
def table(h0,h1):
    i=next(k for k,l in enumerate(L) if l.startswith(h0)); j=next(k for k,l in enumerate(L) if l.startswith(h1))
    out=[]
    for l in L[i:j]:
        if not l.startswith('| ') or l.startswith('| מקום') or l.startswith('|---'): continue
        c=[x.strip() for x in l.strip('|').split('|')]; out.append(c)
    return out
A=table('## פירוט כל המסכים ללא כפתור','## פירוט המסכים הכוללים רק ניווט'); B=table('## פירוט המסכים הכוללים רק ניווט','## כל המקומות שקיבלו')
INFO='מידע חי'
# (owner, the action) — the first matching rule wins
RULES=[
 (r'^(S16-RENT)$','actions','F‑01: השכרה מלאה — דגם, מחיר, משך, רישיון, קבלה והחזרה'),
 (r'^(C1-FUEL)$','actions','F‑03: תדלוק הרכב הסמוך — כמות, מחיר, מילוי'),
 (r'^(F3-HOTEL|S16-HOTEL)$','actions','F‑04: קבלה, לינה / שמירה, שירותי המלון (למחזר את מנגנון הלינה הקיים)'),
 (r'^(B7-SORT|B7-NETS|B7-PIER2-HEAD)$','pier','F‑08: פריט נראה, הרמה / שימוש, אנימציה ותוצאה שנשמרת; קישור למשימה'),
 (r'^(F3-FUEL-KIOSK|F3-FUEL-DOCK)$','pier','תדלוק סירה במזח (הסירה הסמוכה — כמות ומחיר)'),
 (r'^(B1-PIER-N)$','pier','דיג / עגינה במזח (מנגנון הדיג הקיים של B2 / B6)'),
 (r'^IS-SHOP$','island','F‑05: מלאי, מחירים, קנייה (תיק וכסף)'),
 (r'^IS-CABLE-(LOW|TOP)$','island','F‑06: כרטיס, עלייה, נסיעה נראית, ירידה (הרכבל של 8 קרונות)'),
 (r'^IS-HELI$','island','F‑07: הזמנת טיסת נוף — מחיר, זמן, זמינות'),
 (r'^IS-','island','לפי האי החדש (D‑694): מקום שנשאר — פעולה או מידע חי; מקום שיוצא — יוצא גם מהקטלוג והשלט'),
 (r'^(C1-GARDEN|C1-BARN|C1-YARD|C1-WORKSHOP|D1-|C0-WHEAT|D0-MELON|C0-GATE-W|D0-GATE-E)','farm','גידול: זריעה / השקיה / קטיף / מכירה בחלקה (המנגנון של 3 החלקות — לכל החלקות)'),
 (r'^A5-POLICE$','police','תשלום קנס כשנתפסים, רישיונות (D‑691)'),
 (r'^DW-D6-CARRIER$','carrier','פריקת המוביל / קבלת רכב מהמוביל'),
 (r'^(E6-BERTH|C6-BERTH|D6-BERTH|D6-SERVICE|C6-OIL-PIER|C6-OIL|LN-D6-RAMP|LB-JOINT)$','sealife','מידע חי מהים: האונייה ברציף / הבאה, הגוררות, הנפט בצינור, מצב הגשר — ופעולה כשיש עבודה'),
 (r'^(APT-|RA-OFFICE|S16-CARGO-GATE|S15-FENCE)','fieldfix','השדה: לוח טיסות / שאטלים חי, איסוף נוסע / מטען (המנגנון "מצויר → חי" של fieldfix)'),
 (r'^(E3-PARCELS|E3-TERMINAL|E3-TAXI)$','actions','להתחיל את העבודה כאן (איסוף ראשון במקום) — לא רק "נווט לאיסוף"'),
 (r'^(E4-|E6-|C6-|D6-|D5-|ST-COAST-HALL|P-D6-IM)','actions','להתחיל עבודה / סיור במקום (הרמה, בדיקה, מסירה — עם תוצאה בעולם), ומידע חי של המקום'),
 (r'^(C5-WORKSHOP|C5-BAYS|C5-WAREHOUSE|C5-SUBSTATION|E3-PARKING|F4-WC|D2-OFFICE-1)$','actions','פעולה של המקום (תיקון משאית / טעינה / בדיקת מכל / חניה / השכרת שמשייה / משרד) עם תוצאה'),
 (r'^(C1-ST19|S16-AIR1|F6-LX-1|F6-LX-2)$','signs',INFO+' (שלב 4, נבנה): מצב המחסומים / האוטובוס הבא בכל קו (tcStopEta), הרכבת הקרובה, אנשים ורכבים בסביבה, השעה + רענון'),
 (r'^(C1-H[1-4])$','signs',INFO+' (שלב 4, נבנה): השעה, האור בבית, אנשים ורכבים בחצר + רענון; "מי גר כאן" — אין היום נתון של דיירים (לא מומצא)'),
 (r'^A5-SQUARE$','signs','קיים: לוח חי ב-074v_places:plcSquare (המשחק באצטדיון, הסרט, ההצגה) + 3 כפתורי ניווט — אין מה להוסיף בסבב הזה'),
 (r'^(PR-F3|G-F6-POCKET|B1-HILL|B1-PICNIC|F4-VOLLEY|A1-|A0-|B0-)','signs',INFO+' (שלב 4, נבנה): השעה ושלב היום, אנשים ורכבים בסביבה, הרכבת הקרובה + רענון; עוד לא: אוניות / מטוסים בטווח ראייה (הגל הבא)'),
]
rows=[]
for src,T in (('בלי כפתור',A),('רק ניווט',B)):
    for c in T:
        name,id_=c[0],c[1]; extra=c[2] if len(c)>2 else ''
        o=next(((ow,ac) for rx,ow,ac in RULES if re.search(rx,id_)),('signs',INFO+' (ברירת מחדל)'))
        rows.append((id_,name,src,extra,o[0],o[1]))
out=W+'/deliver/2026-11-17/signs/F_owners_128.tsv'
with open(out,'w',encoding='utf-8') as f:
    f.write('מזהה\tמקום\tהיום (Review_part2)\tהכפתורים / הלוגו היום\tלמי\tהפעולה הנדרשת\n')
    for r in rows: f.write('\t'.join(r)+'\n')
c=collections.Counter(r[4] for r in rows)
print(len(rows),'מסכים ·',' · '.join(f'{k} {v}' for k,v in c.most_common()),'→',out)
