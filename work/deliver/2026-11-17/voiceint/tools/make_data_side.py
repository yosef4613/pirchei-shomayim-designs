# make_data_side.py — קול 3 (17.11, voiceint): השורות המוקלטות של החברים, אנשי הקשר ונותני משימות הצד → Ogg Opus → TCVREC_SIDE (חלק במשחק).
# עותק של storyvoice/tools/make_data_story.py (שהוא עותק של voice2/tools/make_data2.py): אותה המרה בדיוק (מונו, 24 קילוהרץ, קצב קבוע, Opus 20,
# עוצמה אחידה: RMS של הדיבור ≈ ‎-19 dBFS, השיא עד ‎-0.3 dBFS) ואותו מבנה lines: הטקסט המדויק → {קול: [שניות, base64]}. נוסף: חיתוך שקט בקצוות (עד 0.2 שנ׳).
# שורה נכנסת רק עם תמלול תקין (asr_side_*.out.json, ok), או מתיקון ידני ב-fix_dir (fix_req09.py — רשימה FIXED). ריצה חוזרת אחרי הקלטה נוספת — אותה פקודה.
# python make_data_side.py <voice_lines_side.json> <seg_dir> <fix_dir> <checks_dir> <oggdir> <out.js> [kbps]
import sys, os, json, glob, subprocess, base64, hashlib
import numpy as np, scipy.io.wavfile as wf
vlp, segd, fixd, chkd, oggdir, out = sys.argv[1:7]; kbps = int(sys.argv[7]) if len(sys.argv) > 7 else 20
FIXED = {'S‑A‑007', 'S‑A‑008', 'S‑A‑009', 'S‑A‑010', 'S‑A‑051'}   # בקשה 09 — החיתוך תוקן ביד (fix_req09.py), התמלול של החיתוך הישן לא תקף להן
VL = json.load(open(vlp, encoding='utf-8'))
# שלוש דמויות של הסיפור בלי game_id ב-voice_lines_side.json (פרקים 5 / 6 עוד לא בנויים; הדסה — רק קול): המזהה במשחק לפי הסיפור (st-hadassah — 074zd; ‏st-gedalya — story/draft/ch5_draft.js; ‏st-baruch — לפי השם, לאישורך)
GID = {'gadi': 'st-gedalya', 'ron': 'st-baruch', 'hadassah': 'st-hadassah'}
for k, c in VL['cast'].items():
    if not c.get('game_id') and k in GID: c['game_id'] = GID[k]
for l in VL['lines']:
    if not l.get('game_id') and l['who'] in GID: l['game_id'] = GID[l['who']]
os.makedirs(os.path.join(oggdir, '_norm'), exist_ok=True)
asr = {}
for f in glob.glob(os.path.join(chkd, 'asr_side_*.out.json')):
    for r in json.load(open(f, encoding='utf-8')): asr[r['id'].split('|')[0]] = r
fname = lambda l: l['voice'] + '_sd_' + l['id'].replace('‑', '_') + '.wav'
aid = lambda i: i.replace('‑', '-')
def trim(a, sr):
    h = int(sr * 0.02); e = np.array([np.sqrt(np.mean(a[k:k + h] ** 2)) for k in range(0, max(1, len(a) - h), h)])
    v = np.nonzero(e > 0.004)[0]
    if not len(v): return a
    s = max(0, v[0] * h - int(0.2 * sr)); t = min(len(a), (v[-1] + 1) * h + int(0.2 * sr)); return a[s:t]
def enc(l, w):
    sr, a = wf.read(w); a = a.astype(np.float32) / 32768
    if a.ndim > 1: a = a.mean(axis=1)
    a = trim(a, sr)
    x = np.abs(a); v2 = a[x > 0.02]; rms = float(np.sqrt(np.mean(v2 * v2))) if len(v2) else 0.1
    a = a * min(0.112 / max(rms, 1e-4), 0.97 / max(1e-4, float(x.max())))
    k = os.path.basename(w)[:-4]
    n = os.path.join(oggdir, '_norm', k + '.wav'); wf.write(n, sr, (a * 32767).astype(np.int16)); o = os.path.join(oggdir, k + '.ogg')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', n, '-ac', '1', '-ar', '24000', '-c:a', 'libopus', '-b:a', '%dk' % kbps, '-vbr', 'off',
                    '-application', 'audio', '-frame_duration', '20', '-map_metadata', '-1', '-fflags', '+bitexact', '-flags:a', '+bitexact', o], check=True)
    return open(o, 'rb').read(), len(a) / sr
res = {}; ids = {}; tot = 0; sec = 0; per = {}; fixed = []; skip = []; rows = []; by = {}; mis = {}
for l in VL['lines']:
    if '{' in l['text']: skip.append((l['id'], 'שם השחקן')); continue
    w = os.path.join(fixd, fname(l)); fx = l['id'] in FIXED and os.path.exists(w)
    if fx: fixed.append(l['id'])
    else: w = os.path.join(segd, fname(l))
    if not os.path.exists(w): skip.append((l['id'], 'עוד לא הוקלט')); continue
    r = asr.get(l['id'])
    if not fx and (not r or not r.get('ok')): skip.append((l['id'], 'אין תמלול' if not r else 'התמלול לא תואם (%.2f)' % r.get('sim', 0))); continue
    if l['text'] in res and l['voice'] in res[l['text']]: skip.append((l['id'], 'כפול')); continue
    b, d = enc(l, w); tot += len(b); sec += d; per[l['voice']] = per.get(l['voice'], 0) + len(b)
    res.setdefault(l['text'], {})[l['voice']] = [round(d, 2), base64.b64encode(b).decode('ascii')]; ids[aid(l['id'])] = l['text']
    g = l['game_id']; by.setdefault(g, {}).setdefault(l['kind'], []).append(aid(l['id']))
    if l['kind'] == 'mission': mis[l['ref']] = [g, aid(l['id'])]
    rows.append((l['id'], l['voice'], round(d, 2), len(b)))
cast = {c['game_id']: c['voice'] for c in VL['cast'].values()}; names = {c['game_id']: c['name'] for c in VL['cast'].values()}
info = {'recs': len(rows), 'of': len(VL['lines']), 'texts': len(res), 'bytes': tot, 'b64': sum(len(x[1]) for r in res.values() for x in r.values()), 'sec': round(sec, 1),
        'kbps_real': round(tot * 8 / max(sec, 1) / 1000, 1), 'per_voice': per, 'fixed': fixed, 'contacts': len(by), 'missions': len(mis),
        'skip_n': len(skip), 'skip_why': {k: sum(1 for s in skip if s[1].startswith(k)) for k in ('עוד לא הוקלט', 'אין תמלול', 'התמלול לא תואם', 'כפול', 'שם השחקן')}}
print(json.dumps(info, ensure_ascii=False))
json.dump({'info': info, 'skip': skip, 'rows': rows}, open(os.path.join(oggdir, 'make_data_side.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
body = {'v': 2, 'kind': 'side', 'fmt': 'audio/ogg; codecs=opus', 'kbps': kbps, 'bytes': tot, 'sec': info['sec'], 'cast': cast, 'names': names, 'by': by, 'mis': mis, 'ids': ids, 'lines': res}
head = ('/* 17.11 · TCVREC_SIDE — קול 3: השורות המוקלטות של החברים, אנשי הקשר ונותני משימות הצד (%d הקלטות מתוך %d שורות · %.1f שניות · Ogg Opus מונו %d קילוביט לשנייה · %s בתים לפני base64).\n'
        '   קולות של Gemini (גוגל), הוקלטו 12.11–17.11 (deliver/2026-11-11/voice3, ‏run_side_voice.sh; התמלול — רק שורות תקינות). נוצר בכלי W/deliver/2026-11-17/voiceint/tools/make_data_side.py — לא עורכים ביד.\n'
        '   lines: הטקסט המדויק → {קול: [שניות, Ogg Opus ב-base64]} (המבנה של TCVREC_DATA.lines) · ids: המזהה (S-A-001) → הטקסט · cast: איש הקשר במשחק → הקול · names: השם\n'
        '   by: איש קשר → {call: פתיחות של שיחה, trait: שורות משלו, thanks: תודה בסוף משימה} · mis: משימה → [הנותן, השורה בהתחלה]. החיבור — בחלק הבא (074zv_side_vrec.js). */\n') % (
        info['recs'], info['of'], info['sec'], kbps, format(tot, ','))
js = head + 'var TCVREC_SIDE=' + json.dumps(body, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(out, 'w', encoding='utf-8', newline='').write(js); bb = js.encode('utf-8')
print('נכתב', out, format(len(bb), ','), 'בתים', hashlib.sha1(bb).hexdigest()[:12])
