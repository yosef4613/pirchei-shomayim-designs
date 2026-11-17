#!/usr/bin/env python3
# בונה את דף ההשוואה: התבנית + הקוד הישן (מחולץ) + G2 + Zdog + SVG.js + page.js — הכול בתוך הדף, בלי קישורים חיצוניים.
import os, json, re, hashlib, subprocess, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
S = os.path.join(D, 'src'); V = os.path.join(D, 'vendor')
subprocess.run([sys.executable, os.path.join(D, 'tools', 'extract_old.py')], check=True)
g2 = ['g2_core.js', 'g2_car.js', 'g2_plane.js', 'g2_ped.js']
sizes = {f: os.path.getsize(os.path.join(S, f)) for f in g2}
old = open(os.path.join(S, 'old_libs.js'), encoding='utf8').read()
osz = json.loads(re.search(r'window\.__OLD_SIZES=(\{.*?\});', old).group(1))
lib = {'zdog': os.path.join(V, 'zdog-1.1.3/package/dist/zdog.dist.min.js'), 'svg': os.path.join(V, 'svgdotjs-svg.js-3.2.8/package/dist/svg.min.js')}
def sc(code): return '<script>\n' + code.replace('</script', '<\\/script') + '\n</script>\n'
parts = [sc('window.TurboCity={get:()=>null};window.__G2_SIZES=' + json.dumps(sizes) + ';'), sc(old)]
parts += [sc(open(os.path.join(S, f), encoding='utf8').read()) for f in g2]
parts += [sc(open(lib['zdog'], encoding='utf8').read()), sc(open(lib['svg'], encoding='utf8').read())]
parts += [sc(open(os.path.join(S, 'zd_models.js'), encoding='utf8').read())]
kb = lambda n: '%.0f' % (n / 1024)
g2t = sum(sizes.values()); ot = sum(osz.values())
sizeline = 'גודל הקוד: הישן (C34 + A34 + P34) %s ק"ב · החדש (G2: ליבה %s + מכונית %s + מטוס %s + אדם %s) %s ק"ב · Zdog ‏29 ק"ב · SVG.js ‏91 ק"ב.' % (kb(ot), kb(sizes['g2_core.js']), kb(sizes['g2_car.js']), kb(sizes['g2_plane.js']), kb(sizes['g2_ped.js']), kb(g2t))
parts += [sc('document.getElementById("sizes").textContent=' + json.dumps(sizeline) + ';')]
parts += [sc(open(os.path.join(S, 'page.js'), encoding='utf8').read())]
html = open(os.path.join(S, 'tpl', 'compare.html'), encoding='utf8').read().replace('/*@@SCRIPTS@@*/', ''.join(parts))
assert 'data:image' not in html, 'data:image in the page'
assert not re.search(r'<img|src\s*=\s*["\']https?:|url\(\s*["\']?(?:https?:|data:|//)', html), 'external resource / image in the page'
out = os.path.join(D, 'Gfxlib_compare.html'); open(out, 'w', encoding='utf8').write(html)
print(out, len(html.encode()), hashlib.sha1(html.encode()).hexdigest()[:12], sizeline)
