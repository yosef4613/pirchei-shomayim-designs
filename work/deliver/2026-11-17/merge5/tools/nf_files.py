# nf_files.py — merge5 (17.11, גל 5): ציון nf_score לכל קובץ של 1.3 מ"ב (gN.txt) — ישנה מול חדשה, מתוך הפלט של nf_score.py --mb 1.3 --pieces 1.
# usage: python3 nf_files.py <old.txt> <new.txt> <שם ישנה> <שם חדשה>
import sys, re
R = re.compile(r'^\s+(g\d+)_1\s+[\d,]+ ב׳\s+([\d.]+)')
def L(f): return {m.group(1): float(m.group(2)) for m in (R.match(l) for l in open(f, encoding='utf-8')) if m}
a, b = L(sys.argv[1]), L(sys.argv[2]); ks = sorted(set(a) | set(b), key=lambda k: int(k[1:]))
print('ציון לכל קובץ של 1.3 מ"ב (gN.txt) — %s / %s: ' % (sys.argv[3], sys.argv[4]) + ' · '.join('%s %s/%s' % (k, a.get(k, '—'), b.get(k, '—')) for k in ks))
d = [(b[k] - a[k], k) for k in ks if k in a and k in b]
print('המקסימום: %s %.1f · %s %.1f · ההפרש הגדול ביותר בקובץ: %+.1f (%s) · קבצים: %d / %d' % (sys.argv[3], max(a.values()), sys.argv[4], max(b.values()), max(d)[0], max(d)[1], len(a), len(b)))
