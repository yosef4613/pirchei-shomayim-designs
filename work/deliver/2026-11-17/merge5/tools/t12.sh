#!/bin/bash
# t12.sh <cand.html> — merge5 (17.11, גל 5; עותק של merge4/tools/t11.sh): דף בדיקת הסינון לבעלים — split_any 1.3 → nftest/r304 + nftest/t12.html (כמו t11), ובדיקה שהחלקים יחד = הבנייה. בלי commit (נעשה אחרי).
set -e
W=/home/user/tc_root/tc/pkg/work; G=$(readlink -f "$1"); R=/home/user/pirchei-shomayim-designs/turbo-city/nftest; O=$R/r304
rm -rf $O; mkdir -p $O; python3 $W/tools_pack/split_any.py $G $O 1.3 | tail -3
N=$(ls $O | grep -c '^g[0-9]*\.txt$'); F=$(python3 -c "import json;print(json.dumps(['r304/g%d.txt'%i for i in range(1,$N+1)]).replace('\",\"','\", \"'))")
python3 - "$R/t11.html" "$R/t12.html" "$F" <<'PY'
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
old='בדיקת סינון — S7F303 (cand303x: S7F302 + גל המיזוג 4, משוחרר — בלי הערות, שמע בקידוד hex) — 24 החלקים'; assert old in s
s=s.replace(old,'בדיקת סינון — S7F304 (cand304x: S7F303 + גל המיזוג 5, משוחרר — בלי הערות, שמע בקידוד hex) — %d החלקים'%len(eval(sys.argv[3])))
s=re.sub(r'const F=\[[^\]]*\];','const F='+sys.argv[3]+';',s); s=s.replace('r303/loader.html','r304/loader.html').replace("'?v=11'","'?v=12'")
assert 'r303' not in s and 'S7F304' in s and '?v=12' in s
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
cat $(for i in $(seq 1 $N); do echo $O/g$i.txt; done) | cmp - $G && echo "החלקים יחד = הבנייה ($N חלקים)"
