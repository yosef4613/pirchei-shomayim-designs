#!/bin/bash
# snap.sh <dir> — צילום של אתר המעצב (turbo-city-set7-share) להשוואה. המתאם, 17.11.
# שימוש: bash snap.sh base_1810 ; bash snap.sh now_XXXX ; diff <(cd base_1810 && sha1sum *) <(cd now_XXXX && sha1sum *)
S=https://turbo-city-set7-share.wavyjet8.chatgpt.site
D=$(dirname "$0")/$1; mkdir -p "$D"; cd "$D" || exit 1
for p in index.html refined.html refined/catalog.js refined/plan.json brand-review.html city-signs.html airport.html posters.html set6.html set7.html set8.html set9.html set10.html list/ \
         airport/airport.css airport/report.md airport/sign_inventory.json city-signs/coverage.json city-signs/sign_inventory.json city-signs/ui.css \
         library/README_HE.txt library/catalog_id_to_brand_key.json library/master.css favicon-code.js downloads/Turbo_City_Airport_S7F298_Code_Only.html; do
  f=$(echo "$p" | sed 's#/$#/index.html#; s#/#__#g')
  curl -sS -L --max-time 60 -o "$f" -w "%{http_code} %{size_download} $p\n" "$S/$p"
done
for f in *; do grep -v "__CF" "$f" | sha1sum | cut -c1-12 | tr -d "\n"; echo "  $f"; done > ../$(basename "$D").sha1
