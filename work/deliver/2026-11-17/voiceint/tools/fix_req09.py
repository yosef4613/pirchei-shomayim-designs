# fix_req09.py — בקשה 09 (Rasalgethi: שמעון ×6, משה ×3) נחתכה בהיסט (g2_split איחד את 007+008, ופיצל את 053) — התמלול: 9 חשודות.
# מה שאפשר להחזיר בלי ספק, לפי התמלול ולפי השקטים (1.0 שנ׳ של שקט מלא בין השורות):
#   S‑A‑007 ← seg 007 עד 5.70 שנ׳ · S‑A‑008 ← seg 007 מ-5.70 שנ׳ · S‑A‑009 ← seg 008 · S‑A‑010 ← seg 009 · S‑A‑051 ← seg 011.
# S‑A‑011 / 012 / 052 / 053 — הגבול לא ודאי: לא נכנסים (קול הדפדפן, כמו היום). כותב ל-<fix_dir> באותם שמות של seg (כמו fix_dir של storyvoice).
import sys, os, numpy as np, scipy.io.wavfile as wf
seg, fix = sys.argv[1:3]; os.makedirs(fix, exist_ok=True)
R = lambda n: wf.read(os.path.join(seg, 'Rasalgethi_sd_S_A_%03d.wav' % n))
def W(n, sr, a): wf.write(os.path.join(fix, 'Rasalgethi_sd_S_A_%03d.wav' % n), sr, a); print(n, round(len(a) / sr, 2))
sr, a = R(7); k = int(5.70 * sr); W(7, sr, a[:k]); W(8, sr, a[k:])
for dst, src in ((9, 8), (10, 9), (51, 11)): sr, a = R(src); W(dst, sr, a)
