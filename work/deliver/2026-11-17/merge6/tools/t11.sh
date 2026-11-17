#!/bin/bash
# t11.sh <cand.html> — merge4 (17.11, גל 4): דף בדיקת הסינון לבעלים — split_any 1.3 → nftest/r303 + nftest/t11.html (כמו t10), ובדיקה שהחלקים יחד = הבנייה. בלי commit (נעשה אחרי).
set -e
W=/home/user/tc_root/tc/pkg/work; G=$(readlink -f "$1"); R=/home/user/pirchei-shomayim-designs/turbo-city/nftest; O=$R/r303
mkdir -p $O; python3 $W/tools_pack/split_any.py $G $O 1.3 | tail -3
N=$(ls $O | grep -c '^g[0-9]*\.txt$'); F=$(python3 -c "import json;print(json.dumps(['r303/g%d.txt'%i for i in range(1,$N+1)]).replace('\",\"','\", \"'))")
python3 - "$R/t10.html" "$R/t11.html" "$F" <<'PY'
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
s=s.replace('בדיקת סינון — S7F302 (cand302x: S7F301 + גל המיזוג 3, משוחרר — בלי הערות, שמע בקידוד hex) — 24 החלקים','בדיקת סינון — S7F303 (cand303x: S7F302 + גל המיזוג 4, משוחרר — בלי הערות, שמע בקידוד hex) — %d החלקים'%len(eval(sys.argv[3])))
s=re.sub(r'const F=\[[^\]]*\];','const F='+sys.argv[3]+';',s); s=s.replace('r302/loader.html','r303/loader.html').replace("'?v=10'","'?v=11'")
assert 'r302' not in s and 'S7F303' in s and '?v=11' in s
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
cat $(for i in $(seq 1 $N); do echo $O/g$i.txt; done) | cmp - $G && echo "החלקים יחד = הבנייה ($N חלקים)"
