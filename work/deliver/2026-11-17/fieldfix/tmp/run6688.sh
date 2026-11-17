cd /home/user/tc_root/tc/pkg/work; D=deliver/2026-11-17/fieldfix
bash tools_pack/bslot.sh node $D/tools/probe_mx.js clean_r2b_025637/out/_try/try6688.html $D/shots/mx mx6688 > $D/qa/mx6688.log 2>&1
bash $D/tools/gate2.sh try6688
