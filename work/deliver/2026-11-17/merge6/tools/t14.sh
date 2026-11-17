#!/bin/bash
# t14.sh <cand.html> — merge6 (17.11, גל 6ב — הבית; עותק של t13.sh): דף בדיקת הסינון לבעלים — split_any 1.3 → nftest/r306 + nftest/t14.html (כמו t13), ובדיקה שהחלקים יחד = הבנייה. בלי commit (נעשה אחרי).
set -e
W=/home/user/tc_root/tc/pkg/work; G=$(readlink -f "$1"); R=/home/user/pirchei-shomayim-designs/turbo-city/nftest; O=$R/r306
rm -rf $O; mkdir -p $O; python3 $W/tools_pack/split_any.py $G $O 1.3 | tail -3
N=$(ls $O | grep -c '^g[0-9]*\.txt$'); F=$(python3 -c "import json;print(json.dumps(['r306/g%d.txt'%i for i in range(1,$N+1)]).replace('\",\"','\", \"'))")
python3 - "$R/t13.html" "$R/t14.html" "$F" <<'PY'
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
old='בדיקת סינון — S7F305 (cand305x: S7F304 + גל המיזוג 6, משוחרר — בלי הערות, שמע בקידוד hex) — 25 החלקים'; assert old in s
s=s.replace(old,'בדיקת סינון — S7F306 (cand306h: S7F305 + הבית HOME-02 בקידוד + תוספות קטנות, משוחרר — בלי הערות, שמע בקידוד hex) — %d החלקים'%len(eval(sys.argv[3])))
s=re.sub(r'const F=\[[^\]]*\];','const F='+sys.argv[3]+';',s); s=s.replace('r305/loader.html','r306/loader.html').replace("'?v=13'","'?v=14'")
assert 'r305' not in s and 'S7F306' in s and '?v=14' in s
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
cat $(for i in $(seq 1 $N); do echo $O/g$i.txt; done) | cmp - $G && echo "החלקים יחד = הבנייה ($N חלקים)"
