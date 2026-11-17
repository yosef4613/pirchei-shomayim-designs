D=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/posters; cd /home/user/tc_root/tc/pkg/work
bash tools_pack/bslot.sh node $D/tools/busrender.js clean_r2b_025637/out/_try/try6886.html /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/br6886.png > $D/qa/br6886.out 2>&1
echo RENDERDONE >> $D/qa/br6886.out
bash $D/tools/gate.sh try6886
