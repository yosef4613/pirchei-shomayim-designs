#!/bin/bash
# merge_one.sh <commit> <msg> — מיזוג של ענף אחד ל-int302 (המיזוג 17.11, גל 3; עותק של merge2/tools/merge_one.sh — ההבדל: int302). התנגשות רק ב-manifest.json — בכלי (manifest_tool.py merge); התנגשות בכל קובץ אחר — abort ויציאה 3 (לא פותרים ביד).
W=/home/user/tc_root/tc/pkg/work; S=$W/src_game_int302; C=$1; MSG=$2; cd $S
git -c user.name='בונה' -c user.email='builder@turbo.city' merge --no-ff --no-commit $C 2>&1 | tail -5
U=$(git diff --name-only --diff-filter=U)
if [ -n "$U" ]; then
  O=$(echo "$U" | grep -v '^manifest.json$')
  if [ -n "$O" ]; then echo "התנגשות מחוץ ל-manifest: $O"; git merge --abort; exit 3; fi
  T=$(mktemp -d $W/deliver/2026-11-17/merge3/tools/mf_XXXX); git show :1:manifest.json > $T/base.json; git show :2:manifest.json > $T/ours.json; git show :3:manifest.json > $T/theirs.json
  python3 $W/tools_pack/manifest_tool.py merge $S $T/ours.json $T/theirs.json $T/base.json || { echo "manifest_tool נכשל"; git merge --abort; exit 4; }
  git add manifest.json; mv $T $W/_to_delete/ 2>/dev/null; echo "manifest: בכלי"
else
  python3 $W/tools_pack/manifest_tool.py refresh $S; git add manifest.json
fi
git -c user.name='בונה' -c user.email='builder@turbo.city' commit -q -m "$MSG" && git log --oneline -1 | cut -c1-140
