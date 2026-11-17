#!/usr/bin/env python3
# story56 — בונה את parts/074zd2_story56_data.js מ-s56_data.py (המקור האחד), ואת רשימת השורות להקלטה.
# שימוש: python3 s56_build.py <src_game_dir>
import json, os, sys, copy
sys.path.insert(0, os.path.dirname(__file__))
import s56_data as S
SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
VREC = json.load(open(os.path.join(HERE, 'vrec56.json'), encoding='utf-8'))
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
STRIP = ('where', 'do', 'scene')

def clean(ch):
    c = copy.deepcopy(ch)
    for m in c['missions']:
        for s in m['steps']:
            for k in STRIP: s.pop(k, None)
    return c

lines = {}
for vid, who in S.VOICE.items():
    v = VREC[vid]; chid = S.WHO[who]
    lines[vid] = {'who': chid, 'text': v['text'], 'sec': round(v['sec'] or len(v['text']) / 10, 1), 'src': vid.replace('-', '‑')}

ch5, ch6, chf = clean(S.CH5), clean(S.CH6), clean(S.CHF)

EXT = r'''
/* the states and the watches of chapters 5–6 (TC_STORY_EXT — the engine 074ze adds them to its STATE / WATCH at its load). In the check of the story (TCSTORY.E.qa) — like the
   states of the engine: the check sets the watch (E.qa.watch), and a state is done. */
var TC_STORY_EXT={
 state:{
  /* 6‑2: the penalties of A4 (057:a4FinishPractice — the last practice), 3 of 5 after the step began */
  pen3:m=>{try{if(TCSTORY.E.qa)return true;const a=ensureA4Sports(),L=a&&a.last,t0=(m&&m.st&&m.st.rt)||0;return !!(L&&L.kind==='penalty'&&(Date.parse(L.at)||0)>=t0-1000&&(L.score||0)>=3)}catch(e){return false}},
  /* 6‑3: 3 fish caught after the step began (any water — the inventory of the fishing, 074a / D‑570) */
  fish63:m=>{try{if(TCSTORY.E.qa)return true;const f=ensureFishingSchema(),t0=(m&&m.st&&m.st.rt)||0;return (f.inventory||[]).filter(q=>q&&!q.qa&&(Date.parse(q.caughtAt)||0)>=t0-1000).length>=3}catch(e){return false}}},
 watch:{
  /* 5‑5: "the view from the helicopter" (the scene 5‑flight, 074zw) — over; without a scene (an automatic test, no cutscenes) — after 20 s */
  flight55:()=>s56Watch('5-flight',20000,180000,['st-eliyahu','מגדל, כאן אליהו — נחתנו במנחת של האי. הארגז במרפאה. חוזרים הביתה.']),
  /* 5‑7: the tug of the port (S14 / sealife) — the scene 5‑tug, or the tow now, or 4 minutes */
  tug57:()=>s56Watch('5-tug',40000,240000,['s9-moshe','היא בפנים. ראית? בלי לגעת באף מצוף.'],()=>{try{const I=TCCUT.tugInfo();return !!(I&&I.now)}catch(e){return false}})}};
function s56Watch(id,noScene,most,say,alt){let T;try{T=TCSTORY}catch(e){return false}const Q=T.E.qa;if(Q)return !!Q.watch;const m=T.M();if(!m)return false;const st=m.st||(m.st={}),t=Date.now()-(st.rt||Date.now());
 let marked=false,busy=false;try{marked=!!g77St().flags['cut:'+id]}catch(e){}try{const C=TCCUT.ST;busy=!!(C.on&&C.on.id===id)||C.q.some(q=>q.id===id)}catch(e){}
 const ok=(marked&&!busy&&t>2500)||(!marked&&t>noScene)||t>most||(!!alt&&!busy&&t>noScene&&alt());
 if(ok&&!st.s56said){st.s56said=1;try{g77MsgIn(say[0],say[1])}catch(e){}}return ok}
'''

js = '''/* ===== 17.11 · story56 — פרקים 5 ו-6 והסוף: "משחק גמור"; והפתיחה ברורה (הבעלים ~13:30, אחרי S7F301). הציור: deliver/2026-11-17/story56/Story56_plan.html.
   מצאתי (כלל 19): פרקים 5 ו-6 היו רק שם ו"בקרוב" (missions:[]), ובלי פרק סיום — המנוע (074ze:chapterEnd / step) נעצר בפרק 5 לתמיד. התסריט של 10.11 (story_data.py)
   כתב את שניהם ואת "פסטיבל העיר", וההודעות הקוליות V‑5 / V‑6 / V‑F כבר מוקלטות במשחק (074zf:TCVREC_STORY). לכן — שדרוג של אותם נתונים (כלל 19א), לא מנגנון חדש:
   - כאן (לפני המנוע): הדמויות החדשות, השורות הקוליות (הטקסט בדיוק כמו בהקלטה), השיחות, העבודות (MISSION_DEFS), המשימות של פרקים 5, 6 והסוף ('F'), והשדרוג
     של שתי השיחות של הפתיחה (מי אני, מאיפה באתי, למה אני פה, מה התפקיד) — ומצבים / תצפיות של הפרקים (TC_STORY_EXT).
   - החלק 074zw_story56_live.js (אחרי הסצנות): הסצנות, הסערה, הכרטיס "מי אני" ביומן, ומה שאחרי הסוף.
   נבנה בכלי deliver/2026-11-17/story56/tools/s56_build.py מ-s56_data.py — לא עורכים ביד. ===== */
''' + EXT + '''
(function(){const D=(typeof TC_STORY!=='undefined'&&TC_STORY)||null;if(!D)return;
 Object.assign(D.chars,%s);
 Object.assign(D.lines,%s);
 Object.assign(D.dialogs,%s);
 Object.assign(D.jobs,%s);
 const put=(c)=>{const i=D.chapters.findIndex(q=>q.id===c.id);if(i>=0){const o=D.chapters[i];delete o.soon;Object.assign(o,c)}else{const j=D.chapters.findIndex(q=>q.id==='6');D.chapters.splice(j>=0?j+1:D.chapters.length,0,c)}};
 put(%s);
 put(%s);
 put(%s);
 D.s56={v:1,whoami:%s,after:%s};
})();
''' % (J(S.CHARS), J(lines), J(S.DIALOGS), J(S.JOBS), J(ch5), J(ch6), J(chf), J(S.WHOAMI), J(S.AFTER))
out = os.path.join(SRC, 'parts', '074zd2_story56_data.js')
open(out, 'w', encoding='utf-8').write(js)
print(out, len(js.encode('utf-8')))

# the lines to record (voice3, later): the new texts said by the characters (dialogs + messages) — not the 27 recorded lines
rec = []
def said(who, t, where):
    if who in ('st-letter',): return
    rec.append((where, who, t))
for did, d in S.DIALOGS.items():
    for k, r in d['rows'].items():
        said(r.get('who', d['who']), r['text'], did + '/' + k)
for C in (S.CH5, S.CH6, S.CHF):
    for m in C['missions']:
        for a in m.get('on', []) + m.get('done', []):
            if 'msg' in a: said(a['msg'][0], a['msg'][1], m['id'])
            if 'bubble' in a: said(a['bubble'][0], a['bubble'][1], m['id'] + ' (בועה)')
NM = {k: v[0] for k, v in S.CHARS.items()}
NM.update({'st-aharon': 'סבא אהרן', 'st-shimon': 'שמעון', 'st-shmulik': 'שמוליק', 'st-david': 'דוד', 'st-naftali': 'נפתלי', 'st-eliyahu': 'אליהו', 's9-avi': 'אברהם', 's9-moshe': 'משה', 's9-yossi': 'יוסף'})
p = os.path.join(HERE, '..', 'voice_lines_to_record.txt')
with open(p, 'w', encoding='utf-8') as f:
    f.write('story56 · 17.11 — השורות החדשות של פרקים 5, 6, הסוף והפתיחה המשודרגת, להקלטה בהמשך (voice3). היום — טקסט בלבד במשחק.\n')
    f.write('(27 ההודעות V‑5 / V‑6 / V‑F כבר מוקלטות — 074zf; הן לא כאן.) המבנה: מקום · דמות · הטקסט ({name} — השם של השחקן, לא מוקלט).\n\n')
    for w, who, t in rec: f.write('%s · %s · %s\n' % (w, NM.get(who, who), t))
print(p, len(rec))
