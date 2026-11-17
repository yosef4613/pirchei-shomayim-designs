# -*- coding: utf-8 -*-
# ft_part.py <out.json> <src_game_dir> — כותב את התוספת של לוח הטיסות לחלק parts/019l2_ft_sched.js (מיד אחרי 019l, לפני 019m), ומכניס אותו ל-manifest (ואז refresh בכלי)
import sys, os, json, subprocess
R = json.load(open(sys.argv[1], encoding='utf-8')); G = sys.argv[2]
add = dict(flights=R['flights'], sched=R['sched'], veh=R['veh'], r3={k: [v['out'], v['back']] for k, v in (R.get('r3') or {}).items() if 'out' in v and 'back' in v})
info = ' · '.join(R['log'])
head = '''/* ==== fieldthru 17.11 · לוח הטיסות של השדה — עוד טיסות מעל הלוח של היום (הבעלים 17.11 07:55: "השדה גם חשוב שיהיה היום אני רוצה הרבה יותר טיסות מהשדה הקודם") ====
   מצאתי: ‏019l:S15SIM — 5 טיסות במחזור של 720 ש׳ (+ FL-C2 של 074p, ‏FL-GA1 של fieldfix — 074zp) = 35 תנועות מסלול ב-1800 ש׳; הישן (S7F272, המתכנן AO) — 44–45.
   הסיבה (fieldcalc): המחולל s15_sim.py — נתיבים קבועים בלי המתנה, והמסלול "תפוס" לאורך כל רגל הגישה; ובנוסף הגרירות של R3 (074zo) בזמנים קבועים.
   כאן — התוספת שנוצרה בכלי deliver/2026-11-17/fieldthru/tools/ft_sim.py (כלל 19א — אותו מחולל s15_sim.py: departure / takeoff / arrival / tug, והמנגנונים של AO
   הישן: טבלת שמירה במרחב־זמן לכל השדה, חיפוש של הזמן הפנוי הראשון (aoSearch), המתנה בקו ההמתנה (התור למסלול), מרווח של 3 ש׳ במסלול (AO.SEP / כלל
   fieldcalc), ההמראה מ-A2 לפי AO_ROLL, פרופיל ההסעה של הישן (apttTaxi: ‏vTaxi של הסוג, האצה / האטה, הקשתות), ורכב אחד של הצי לכמה עמדות (AF)).
   הבדיקה בכלי: מול כל מה שרץ במשחק (dump של הבנייה — כל הטיסות, הרכבים אחרי כל העטיפות, החונים, המסוק), ואז בדיקה מדויקת (OBB של s15SimAudit) כל 0.5 ש׳.
   הטיסות: ''' + info + '''
   הגרירות של R3 (FFR3 של fieldfix): הזמנים נבחרו אחרי הלוח (ft_sim.py:tow_search — השריון של G77_MLV ב-AO של הישן), ומוחלים בטעינה ב-074zv (FTS.add.r3).
   הטיסות של היום (019l: FL-P2 / P3 / P4 / R2 / GA6 — כשמסומנות ftu) — באותו פרופיל של הישן (הדחיפה 75 → 44 ש׳, ההסעה), אותה המראה ואותה נגיעה; הדחיפה מאוחרת יותר
   והעצירה בעמדה מוקדמת יותר — העמידה מתארכת, וכל רכבי השירות שבתוכה נשארים בתוכה (C14.07: "בחדש דברים קפואים / איטיים").
   מוכנס לפני 019m (S15_FL, ‏S15_MOVING, ‏s15StaticList) — כל השדה (הגררים, השרוולים, הלוחות, s15k) רואה את הטיסות כמו את של היום. ‎#ft=0 — בלי (להשוואה). ==== */
'''
js = head + 'var FTS={on:!/[#&]ft=0/.test(String((typeof location!=="undefined"&&location.hash)||"")),n:0,v:0,err:"",add:' + json.dumps(add, ensure_ascii=False, separators=(',', ':')) + '};\n'
js += '''(function(){try{if(!FTS.on||typeof S15SIM==='undefined')return;const A=FTS.add;
 for(const f of A.flights){const i=S15SIM.flights.findIndex(x=>x.id===f.id);if(i>=0){if(f.ftu){S15SIM.flights[i]=f;FTS.u=(FTS.u||0)+1}continue}S15SIM.flights.push(f);FTS.n++}   // ftu — טיסה של היום בפרופיל של הישן (אותה דחיפה / המראה / נגיעה)
 for(const q of A.sched){const i=S15SIM.sched.findIndex(x=>x[0]===q[0]);if(i>=0)S15SIM.sched[i]=q;else S15SIM.sched.push(q)}
 for(const v of A.veh){const i=S15SIM.veh.findIndex(x=>x.id===v.id);if(i>=0)S15SIM.veh[i]=v;else S15SIM.veh.push(v);FTS.v++}
}catch(e){FTS.err=String(e&&e.message||e).slice(0,200)}})();
'''
p = os.path.join(G, 'parts', '019l2_ft_sched.js'); open(p, 'w', encoding='utf-8').write(js)
m = json.load(open(os.path.join(G, 'manifest.json'), encoding='utf-8')); names = [q['name'] for q in m['parts']]
if '019l2_ft_sched.js' not in names:
    i = names.index('019l_S15_data.js'); m['parts'].insert(i + 1, dict(name='019l2_ft_sched.js', block=m['parts'][i]['block']))
    json.dump(m, open(os.path.join(G, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(subprocess.run(['python3', '/home/user/tc_root/tc/pkg/work/tools_pack/manifest_tool.py', 'refresh', G], capture_output=True, text=True).stdout.strip(), len(js), 'בתים')
