#!/bin/bash
# t13.sh <cand.html> — merge6 (17.11, גל 6; עותק של merge5/tools/t12.sh): דף בדיקת הסינון לבעלים — split_any 1.3 → nftest/r305 + nftest/t13.html (כמו t12), ובדיקה שהחלקים יחד = הבנייה. בלי commit (נעשה אחרי).
set -e
W=/home/user/tc_root/tc/pkg/work; G=$(readlink -f "$1"); R=/home/user/pirchei-shomayim-designs/turbo-city/nftest; O=$R/r305
rm -rf $O; mkdir -p $O; python3 $W/tools_pack/split_any.py $G $O 1.3 | tail -3
N=$(ls $O | grep -c '^g[0-9]*\.txt$'); F=$(python3 -c "import json;print(json.dumps(['r305/g%d.txt'%i for i in range(1,$N+1)]).replace('\",\"','\", \"'))")
python3 - "$R/t12.html" "$R/t13.html" "$F" <<'PY'
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
old='בדיקת סינון — S7F304 (cand304x: S7F303 + גל המיזוג 5, משוחרר — בלי הערות, שמע בקידוד hex) — 24 החלקים'; assert old in s
s=s.replace(old,'בדיקת סינון — S7F305 (cand305x: S7F304 + גל המיזוג 6, משוחרר — בלי הערות, שמע בקידוד hex) — %d החלקים'%len(eval(sys.argv[3])))
s=re.sub(r'const F=\[[^\]]*\];','const F='+sys.argv[3]+';',s); s=s.replace('r304/loader.html','r305/loader.html').replace("'?v=12'","'?v=13'")
assert 'r304' not in s and 'S7F305' in s and '?v=13' in s
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
cat $(for i in $(seq 1 $N); do echo $O/g$i.txt; done) | cmp - $G && echo "החלקים יחד = הבנייה ($N חלקים)"
