#!/bin/bash
# pages_chk.sh — merge4: הקבצים של דף הסינון t11 ב-GitHub Pages זהים לקבצים שנדחפו (24 חלקים, loader, t11) והחלקים יחד = המועמד.
B=https://yosef4613.github.io/pirchei-shomayim-designs/turbo-city/nftest; L=/home/user/pirchei-shomayim-designs/turbo-city/nftest; T=$(mktemp -d /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/pg_XXXX); ok=0; bad=0
for f in t11.html r303/loader.html $(for i in $(seq 1 24); do echo r303/g$i.txt; done); do
  curl -sS -o $T/x "$B/$f?x=$(date +%s%N)" && cmp -s $T/x $L/$f && ok=$((ok+1)) || { bad=$((bad+1)); echo "שונה: $f"; }
done
echo "זהים: $ok · שונים: $bad"
