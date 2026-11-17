# טורבו סיטי — גיבוי מלא לסבב הבא (17.11, אחרי S7F306 (נבדק: 193 ענפים, master b8eb692).

הענף הזה מחזיק את כל מה שצריך כדי להמשיך בשיחה חדשה. המשחק עצמו (הגרסה שפורסמה) נמצא בענף main, בתיקייה turbo-city/.

## מה יש כאן
| מה | איפה |
|---|---|
| קוד המשחק — כל 193 הענפים והתגים (master = S7F306 + int306) | `src_game.bundle` |
| ההוראות, ההחלטות והמסירה לסבב הבא | `work/HANDOFF_NEXT.md` (להתחיל בסעיף "אחרי סבב 17.11"), `work/DECISIONS_1110.md`, `work/HANDOFF_1111.md` (היומן) |
| כל הבקשות של הבעלים, מילה במילה | `work/deliver/2026-11-12/review/Owner_requests_all_1112.txt` |
| כלי המסירה, המיזוג והבדיקות | `work/tools_pack/` (deliver_rel.sh, join_game.py, bslot.sh, split_any.py…), `work/qa_tools/`, `work/study/` |
| העבודה של 17.11 — תדריכים, החזרות של הסוכנים, כלים וציורים | `work/deliver/2026-11-17/` (briefs_1117.md, model_plan.md, ‏*/handback.txt, merge6/tools, nfkiss/tools, ledger/tools) |
| חידוש 02 + 03 של המעצב — מאושרים (D‑706), להכנסה | `work/deliver/2026-11-17/set7_watch/next_0030/` |
| התיק למעצב — הקבוצות ועטיפות המטוסים | `work/deliver/2026-11-17/designer_brief_1117/` |
| קבצים שהבעלים העלה (בלי תמונות) | `work/inbox_owner/` |

לא נכללו: הניסיונות (_try), תוצרי הבדיקות, תמונות, ספריות חיצוניות (threed/vendor) והבניות הישנות — אפשר לבנות הכול מחדש מהקוד.

## שחזור (בשיחה חדשה)
```bash
git clone -b src-backup-1117 --single-branch https://github.com/yosef4613/pirchei-shomayim-designs /tmp/tc_backup
mkdir -p /home/user/tc_root/tc/pkg && cp -r /tmp/tc_backup/work /home/user/tc_root/tc/pkg/work
git init -b restore_tmp /home/user/tc_root/tc/pkg/work/src_game
git -C /home/user/tc_root/tc/pkg/work/src_game fetch /tmp/tc_backup/src_game.bundle '+refs/heads/*:refs/heads/*' '+refs/tags/*:refs/tags/*'
git -C /home/user/tc_root/tc/pkg/work/src_game checkout master
mkdir -p /home/user/tc_root/tc/pkg/work/clean_r2b_025637/out/_try
```
אחר כך: לקרוא את `work/HANDOFF_NEXT.md` ואת `work/DECISIONS_1110.md`, ולבדוק ש-`git -C .../src_game describe --tags master` מחזיר S7F306 (נבדק: 193 ענפים, master b8eb692).

## מה הבא (בקצרה — הפירוט ב-HANDOFF_NEXT)
1. hotfix307 — מקש נפרד (G) להתחלת משימה, תגמול כספי למשימות; בדיקת הסינון t15 מוכנה (turbo-city/nftest/r307 ב-main). אחרי "הכל עבר" — למסור S7F307.
2. brandin2 — חידוש 02 + 03 של המעצב למשחק (מאושר).
3. קבוצת טורבו בכדורסל (לשאול: להחליף אחת או 8 קבוצות).
4. השדה: fieldsvc2, ‏P6, יציאה מהירה, גדר המטען, העמדות הדרומיות. האוטובוסים: קווים 5 / 5א, קו 4.
5. כשהמעצב יחזיר: לוגואים לקבוצות ועטיפות המטוסים.
