# 8.11 · הטבלה של mem_zones.js: לכל בנייה — בפתיחה, אחרי סיבוב, והתוספת של כל אזור (JS heap וקנבסים), ‏10 הגורמים הגדולים
# (מי הקצה את מה שנשאר ב-heap — מהדגימה; המבנים שגדלו — מהספירה; הקנבסים לפי הפונקציה שיצרה אותם).
# python3 qa_tools/mem_zones_table.py <out.json> [more.json …]   → מדפיס טבלאות (markdown, עברית)
import json, sys

def load(fs):
    runs = []
    for f in fs:
        for r in json.load(open(f))['runs']: runs.append(r)
    return runs

def main():
    runs = load(sys.argv[1:])
    print('| בנייה | JS בפתיחה | JS אחרי סיבוב | עלייה | הגבוה בסיבוב | קנבסים בפתיחה (מ״ב / מספר) | קנבסים אחרי סיבוב | PSS אחרי סיבוב | חיכה לבד (ש׳) |')
    print('|---|---|---|---|---|---|---|---|---|')
    for r in runs:
        o, f = r['open'], r['final']
        pk = max([z['js'] for z in r['zones']] + [o['js']])
        print('| %s | %.1f | %.1f | %+.1f | %.1f | %.1f / %d | %.1f / %d | %d | %s |' % (r['tag'], o['js'], f['js'], f['js'] - o['js'], pk, o['cv']['mb'], o['cv']['n'], f['cv']['mb'], f['cv']['n'], f['pss']['total'], r.get('pausedS', '')))
        if r.get('perf'): print('  הזמן לפריים (חציון / אחוזון 90): ' + ' · '.join('%s %s / %s' % (k, v['med'], v['p90']) for k, v in r['perf']['places'].items()))
    # per zone: ΔJS of every build side by side
    tags = [r['tag'] for r in runs]; Z = {}
    for r in runs:
        for z in r['zones']: Z.setdefault(z['z'], {})[r['tag']] = z
    print('\n| אזור | בנוי | ' + ' | '.join('Δ JS ' + t for t in tags) + ' | ' + ' | '.join('Δ קנבס ' + t for t in tags) + ' |')
    print('|---|---|' + '---|' * (2 * len(tags)))
    for k in sorted(Z, key=lambda k: (int(k[1:]), k[0])):
        row = Z[k]; b = any(v.get('built') for v in row.values())
        print('| %s | %s | ' % (k, 'כן' if b else '') + ' | '.join('%+.1f' % row[t]['dJs'] if t in row else '' for t in tags) + ' | ' + ' | '.join('%+.1f' % row[t]['dCv'] if t in row else '' for t in tags) + ' |')
    for r in runs:
        print('\n### %s — הקנבסים אחרי הסיבוב לפי הפונקציה שיצרה אותם (מ״ב)' % r['tag'])
        o = {k: (n, mb) for k, n, mb in r['open']['cv']['by']}
        for k, n, mb in r['final']['cv']['by'][:14]:
            n0, m0 = o.get(k, (0, 0))
            print('- %s: %d קנבסים, %.1f מ״ב (בפתיחה %d, %.1f)' % (k, n, mb, n0, m0))
        if r.get('sample'):
            print('\n### %s — מה שנשאר ב-heap מהפתיחה עד הסוף, לפי מי שהקצה (הדגימה, מ״ב; סה״כ %.1f)' % (r['tag'], r['sample']['totalMB']))
            for k, v in r['sample']['named'][:20]: print('- %s: %.1f' % (k, v))
        if r.get('census0') and r.get('census1'):
            c0, c1 = r['census0'], r['census1']
            g = sorted(((c1[k] - c0.get(k, 0), k) for k in c1), reverse=True)[:20]
            print('\n### %s — המבנים הגלובליים שגדלו (מספר איברים, פתיחה → סוף)' % r['tag'])
            for d, k in g:
                if d > 0: print('- %s: %d → %d (%+d)' % (k, c0.get(k, 0), c1[k], d))

main()
