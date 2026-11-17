#!/bin/bash
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ord; mkdir -p $SP
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools
i=0; for o in "$@"; do i=$((i+1)); timeout 900 python3 ft_gen.py ${WORLD:-sim_base2.json} sim_base2.json $SP/$TAG$i.json $o > $SP/$TAG$i.log 2>&1; echo "$TAG$i $o :: $(tail -1 $SP/$TAG$i.log)"; done
