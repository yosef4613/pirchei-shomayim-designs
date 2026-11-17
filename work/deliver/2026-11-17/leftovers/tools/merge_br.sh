#!/bin/bash
# merge_br.sh <שם> <commit/tag> <msg> — מיזוג של master (או תגית) לענף t17_<שם> בעותק שלו (leftovers, 17.11). התנגשות רק ב-manifest.json — בכלי (manifest_tool.py merge); התנגשות בכל קובץ אחר — יציאה 3 בלי abort (לבדיקה ביד).
# LO_DIR=<תיקייה> — עותק אחר (עותק זמני, detached, לבדיקה מעל int303 לפני שיש תגית S7F303)
W=/home/user/tc_root/tc/pkg/work; S=${LO_DIR:-$W/src_game_t17_$1}; C=$2; MSG=$3; cd $S || exit 2
git -c user.name='בונה' -c user.email='builder@turbo.city' merge --no-ff --no-commit $C 2>&1 | tail -5
U=$(git diff --name-only --diff-filter=U)
if [ -n "$U" ]; then
  O=$(echo "$U" | grep -v '^manifest.json$')
  if [ -n "$O" ]; then echo "התנגשות מחוץ ל-manifest: $O"; exit 3; fi
  T=$(mktemp -d $W/deliver/2026-11-17/leftovers/tools/mf_XXXX); git show :1:manifest.json > $T/base.json; git show :2:manifest.json > $T/ours.json; git show :3:manifest.json > $T/theirs.json
  python3 $W/tools_pack/manifest_tool.py merge $S $T/ours.json $T/theirs.json $T/base.json || { echo "manifest_tool נכשל"; exit 4; }
  git add manifest.json; mv $T $W/_to_delete/ 2>/dev/null; echo "manifest: בכלי"
else
  python3 $W/tools_pack/manifest_tool.py refresh $S; git add manifest.json
fi
git -c user.name='בונה' -c user.email='builder@turbo.city' commit -q -m "$MSG" && git log --oneline -1 | cut -c1-140
echo "kiss: $(grep -ril kiss parts/ | tr '\n' ' ')"
