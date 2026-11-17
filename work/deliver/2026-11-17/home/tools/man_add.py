#!/usr/bin/env python3
# הוספת חלק חדש ל-manifest.json אחרי חלק קיים (אותו block), ואז manifest_tool.py refresh מחשב את השאר.
# שימוש: python3 man_add.py <src_dir> <new_part> <after_part>
import json, sys, subprocess, os
src, new, after = sys.argv[1:4]
p = os.path.join(src, 'manifest.json'); m = json.load(open(p, encoding='utf-8'))
names = [q['name'] for q in m['parts']]
if new not in names:
    i = names.index(after); m['parts'].insert(i + 1, {'name': new, 'block': m['parts'][i]['block']})
    json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')
subprocess.run(['python3', '/home/user/tc_root/tc/pkg/work/tools_pack/manifest_tool.py', 'refresh', src], check=True)
