#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The page "דוח יומי טורבו סיטי" (the owner, 29.10.2026 03:14, §8): what was done, what waits for him, the review agent's report,
the quota, the risks, and what was done with every external review finding. Updated by 08:00 and by 20:00 (same file path → same link).
The content is in daily.json (edited at every update); this script only renders it.  usage: python3 daily.py → daily_report.html"""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'daily.json'), encoding='utf-8'))
E = lambda s: html.escape(str(s), quote=False)
def lis(items): return ''.join('<li>%s</li>' % E(i) for i in items)
def table(head, rows, cls=''):
    return ('<div class="tw"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (cls, ''.join('<th>%s</th>' % E(h) for h in head), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % E(c) for c in r) for r in rows)))

def pkg_html():   # 30.10 · R-30 / R-27: the packages of 4–6 h with the quota checkpoints, what was delivered / moved / next, and the daily line
    P = D.get('packages')
    if not P: return ''
    rows = ''.join(('<tr style="font-weight:700"><td></td><td colspan="4">%s</td><td>%s</td><td></td></tr>' % (E(r['gate']), E(r['when']))) if r.get('gate') else
                   ('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(E(r.get(k, '')) for k in ('n', 'name', 'see', 'build', 'h', 'when', 'state'))) for r in P['rows'])
    mv = ''.join('<li><b>%s</b> %s</li>' % (E(k), E(v)) for k, v in P.get('moves', []))
    dl = table(['היום', 'מגרסה לגרסה', 'נוספו', 'נעשו', 'סך הכול', 'הגרסה הסופית', 'למה'], P['daily']) if P.get('daily') else ''
    return ('<section class="card"><h2>המנות של 4–6 שעות (R-30)</h2>' + ('<ul>%s</ul>' % mv if mv else '') +
            '<div class="tw"><table><thead><tr><th>#</th><th>המנה</th><th>מה תראה בסוף</th><th>בנייה</th><th>שעות</th><th>מתי</th><th>מצב</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            '<h2>השורה היומית (R-27)</h2>' + dl + '<p class="note">' + E(P.get('note', '')) + '</p></section>')
SEV = {'חוסם': 'b', 'חשוב': 'm', 'קטן': 'n', 'נסגר': 'ok'}
rev = ''.join('<tr><td class="id">%s</td><td><span class="chip c-%s">%s</span></td><td>%s</td><td>%s</td><td>%s</td></tr>'
              % (E(r['id']), SEV.get(r['sev'], 'n'), E(r['sev']), E(r['what']), E(r['done']), E(r['state'])) for r in D['review'])
page = '''<title>דוח יומי טורבו סיטי</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{--bg:#f1f2ee;--panel:#fbfbf8;--ink:#1a2026;--muted:#5a6570;--line:#d8dcd5;--accent:#0f5f8f;--accent-soft:#e1edf5;--b:#a3261d;--bb:#f8e3e0;--m:#94530b;--mb:#f5e7d3;--n:#4b5866;--nb:#e8ecef;--ok:#23704a;--okb:#e1f0e6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#13171b;--panel:#1a1f24;--ink:#e5e9ec;--muted:#9aa5ae;--line:#2c333a;--accent:#7cc0ea;--accent-soft:#17324a;--b:#f08a80;--bb:#3d1d1a;--m:#e6a25a;--mb:#3a2a16;--n:#b5c0cc;--nb:#252c33;--ok:#63c48f;--okb:#173325;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13171b;--panel:#1a1f24;--ink:#e5e9ec;--muted:#9aa5ae;--line:#2c333a;--accent:#7cc0ea;--accent-soft:#17324a;--b:#f08a80;--bb:#3d1d1a;--m:#e6a25a;--mb:#3a2a16;--n:#b5c0cc;--nb:#252c33;--ok:#63c48f;--okb:#173325;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15.5px/1.65 "Segoe UI","Noto Sans Hebrew","Arial Hebrew",Arial,sans-serif;direction:rtl}
.page{max-width:980px;margin:0 auto;padding-block:22px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:16px}
h1{margin:0;font-size:28px;text-wrap:balance}
h2{margin:0 0 4px;font-size:19px;text-wrap:balance}
.stamp{display:flex;flex-wrap:wrap;gap:4px 18px;color:var(--muted);font-size:14px}
.stamp b{color:var(--ink);font-variant-numeric:tabular-nums}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px;min-width:0}
ul,ol{margin:0;padding-inline-start:22px;display:flex;flex-direction:column;gap:4px;max-width:86ch}
.tw{overflow-x:auto}
table{border-collapse:collapse;font-size:14px;width:100%;min-width:560px}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:start;vertical-align:top}
th{color:var(--muted);font-weight:600;white-space:nowrap}
td.id{font-family:ui-monospace,Consolas,monospace;white-space:nowrap}
.chip{display:inline-block;font-size:12.5px;font-weight:700;padding:1px 9px;border-radius:999px;white-space:nowrap}
.c-b{color:var(--b);background:var(--bb)}.c-m{color:var(--m);background:var(--mb)}.c-n{color:var(--n);background:var(--nb)}.c-ok{color:var(--ok);background:var(--okb)}
.links{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.lk{border:1px solid var(--line);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:2px;min-width:0}
.lk a{color:var(--accent);font-weight:700;text-decoration:none;word-break:break-all}
.lk span{font-size:13px;color:var(--muted)}
.note{color:var(--muted);font-size:14px;margin:0;max-width:86ch}
</style>
<div class="page">
<header style="display:flex;flex-direction:column;gap:6px">
 <h1>דוח יומי טורבו סיטי</h1>
 <div class="stamp"><span>עודכן: <b>''' + E(D['updated']) + '''</b></span><span>העדכון הבא: <b>''' + E(D['next']) + '''</b></span><span>הבנייה האחרונה: <b>''' + E(D['build']) + '''</b></span><span>התוכנית: <b>''' + E(D['plan']) + '''</b></span></div>
</header>
<section class="card"><h2>מה נעשה</h2><ul>''' + lis(D['done']) + '''</ul></section>
<section class="card"><h2>מה בעבודה עכשיו</h2>''' + table(['#', 'משימה', 'מי', 'מצב'], D['work']) + '''</section>
''' + pkg_html() + '''<section class="card"><h2>מחכה לך — לפי חשיבות</h2><ol>''' + lis(D['waiting']) + '''</ol></section>
''' + (('<section class="card"><h2>' + E(D['approved']['title']) + '</h2>' + table(D['approved']['head'], D['approved']['rows']) + '</section>') if D.get('approved') else '') + '''
<section class="card"><h2>הביקורת החיצונית — מה נעשה בכל ממצא</h2><div class="tw"><table><thead><tr><th>ממצא</th><th>חומרה</th><th>מה</th><th>מה נעשה</th><th>מצב</th></tr></thead><tbody>''' + rev + '''</tbody></table></div></section>
<section class="card"><h2>דוח סוכן הביקורת</h2><ul>''' + lis(D['agent3']) + '''</ul></section>
<section class="card"><h2>המכסה</h2><ul>''' + lis(D['quota']) + '''</ul></section>
<section class="card"><h2>סיכונים</h2><ul>''' + lis(D['risks']) + '''</ul></section>
<section class="card"><h2>הבניות שנמסרו</h2>''' + table(['בנייה', 'sha1', 'גודל (בתים)', 'מצב'], D['builds']) + '''<p class="note">''' + E(D['buildsNote']) + '''</p></section>
''' + ''.join('<section class="card"><h2>' + E(D[k]['title']) + '</h2>' + table(D[k]['head'], D[k]['rows']) + '</section>' for k in ('predeliver', 'perf') if D.get(k)) + (('<section class="card"><h2>' + E(D['xw76']['title']) + '</h2>' + table(['אזור', 'המעבר', 'הכביש', 'לאן', 'למה'], D['xw76']['rows']) + '<p class="note">' + E(D['xw76'].get('note', '')) + '</p></section>') if D.get('xw76') else '') + (('<section class="card"><h2>מה פורסם בדפים הקבועים (R-75) — אותו sha1 ואותו גודל כמו הקובץ שנשלח</h2>' + table(['הדף הקבוע', 'הקובץ', 'sha1', 'גודל (בתים)', 'פורסם', 'הקישור'], D['published']) + '</section>') if D.get('published') else '') + '''<section class="card"><h2>הדפים הקבועים</h2><div class="links">''' + ''.join('<div class="lk"><b>%s</b><a href="%s">%s</a><span>%s</span></div>' % (E(l[0]), E(l[1]), E(l[1]), E(l[2])) for l in D['links']) + '''</div></section>
</div>
'''
open(os.path.join(HERE, 'daily_report.html'), 'w', encoding='utf-8').write(page)
print('daily_report.html', len(page.encode('utf-8')))
