#!/bin/bash
# pages_chk.sh — merge6: הקבצים של דף הסינון t14 ב-GitHub Pages זהים לקבצים שנדחפו (החלקים, loader, t12). N=<מספר החלקים> (ברירת מחדל 24).
B=https://yosef4613.github.io/pirchei-shomayim-designs/turbo-city/nftest; L=/home/user/pirchei-shomayim-designs/turbo-city/nftest; T=$(mktemp -d /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/pg_XXXX); ok=0; bad=0
for f in t14.html r306/loader.html $(for i in $(seq 1 ${N:-24}); do echo r306/g$i.txt; done); do
  curl -sS -o $T/x "$B/$f?x=$(date +%s%N)" && cmp -s $T/x $L/$f && ok=$((ok+1)) || { bad=$((bad+1)); echo "שונה: $f"; }
done
echo "זהים: $ok · שונים: $bad"
