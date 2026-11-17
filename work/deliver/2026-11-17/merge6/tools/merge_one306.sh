#!/bin/bash
# merge_one.sh <commit> <msg> — מיזוג של ענף אחד ל-int306 (המיזוג 17.11, גל 6ב (int306); עותק של merge_one.sh של int305, ובסיס אמיתי ל-manifest).
# התנגשות רק ב-manifest.json — בכלי (manifest_tool.py merge) מול בסיס אמיתי: אם יש כמה בסיסי מיזוג (criss-cross) — הבסיס הווירטואלי של git (:1) לא בשימוש; עוברים על git merge-base --all ולוקחים את הראשון שהכלי מצליח איתו.
# התנגשות בכל קובץ אחר — abort ויציאה 3 (לא פותרים ביד).
W=/home/user/tc_root/tc/pkg/work; S=$W/src_game_int306; C=$1; MSG=$2; cd $S
git -c user.name='בונה' -c user.email='builder@turbo.city' merge --no-ff --no-commit $C 2>&1 | tail -5
U=$(git diff --name-only --diff-filter=U)
if [ -n "$U" ]; then
  O=$(echo "$U" | grep -v '^manifest.json$')
  if [ -n "$O" ]; then echo "התנגשות מחוץ ל-manifest: $O"; git merge --abort; exit 3; fi
  T=$(mktemp -d $W/deliver/2026-11-17/merge6/tools/mf_XXXX); git show :2:manifest.json > $T/ours.json; git show :3:manifest.json > $T/theirs.json
  BASES=$(git merge-base --all HEAD $C); NB=$(echo "$BASES" | wc -l); ok=0
  if [ "$NB" = 1 ]; then git show :1:manifest.json > $T/base.json; python3 $W/tools_pack/manifest_tool.py merge $S $T/ours.json $T/theirs.json $T/base.json && ok=1
  else echo "בסיסים: $NB (criss-cross) — בסיס אמיתי"; for B in $BASES; do git show $B:manifest.json > $T/base.json; cp $T/ours.json manifest.json
    if python3 $W/tools_pack/manifest_tool.py merge $S $T/ours.json $T/theirs.json $T/base.json; then echo "בסיס: ${B:0:7}"; ok=1; break; fi; done; fi
  [ $ok = 1 ] || { echo "manifest_tool נכשל"; git merge --abort; exit 4; }
  git add manifest.json; mkdir -p $W/_to_delete; mv $T $W/_to_delete/ 2>/dev/null; echo "manifest: בכלי"
else
  python3 $W/tools_pack/manifest_tool.py refresh $S; git add manifest.json
fi
git -c user.name='בונה' -c user.email='builder@turbo.city' commit -q -m "$MSG" && git log --oneline -1 | cut -c1-140
