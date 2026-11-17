cd /home/user/pirchei-shomayim-designs && (python3 -m http.server 8765 --bind 127.0.0.1 >/dev/null 2>&1 &) ; sleep 1
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/tools
bash /home/user/tc_root/tc/pkg/work/tools_pack/bslot.sh node measure.js file:///home/user/pirchei-shomayim-designs/turbo-city-b4/index.html /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/out/old_b4.png /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/out/old_b4.json "document.getElementById('loading').hidden"
bash /home/user/tc_root/tc/pkg/work/tools_pack/bslot.sh node measure.js http://127.0.0.1:8765/turbo-city-downtown/index.html /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/out/old_dt.png /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/out/old_dt.json "document.getElementById('loading').hidden"
bash /home/user/tc_root/tc/pkg/work/tools_pack/bslot.sh node measure.js file:///home/user/pirchei-shomayim-designs/turbo-city-three-small/index.html /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/out/old_ts.png /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/threed/out/old_ts.json "window.SmallCity&&window.SmallCity.ready"
pkill -f "http.server 8765"
