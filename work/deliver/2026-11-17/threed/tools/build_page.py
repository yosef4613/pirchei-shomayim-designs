# בונה את דף האב־טיפוס: esbuild מאחד את הקוד + Three.js לקובץ אחד, והוא מוטמע בדף. עוצר אם יש תמונה או קישור שנטען.
import subprocess, sys, os, re, hashlib
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NM = os.path.join(D, 'tools', 'nm')
out_js = os.path.join(D, 'out', 'app.bundle.js')
env = dict(os.environ, NODE_PATH=os.path.join(NM, 'node_modules'))
r = subprocess.run([os.path.join(NM, 'node_modules', '.bin', 'esbuild'), os.path.join(D, 'src', 'app', 'main.js'), '--bundle', '--minify', '--format=iife',
                    '--legal-comments=none', '--target=es2020', '--loader:.json=json', '--outfile=' + out_js, '--log-level=warning'], capture_output=True, text=True, cwd=NM, env=env)
print(r.stdout, r.stderr)
if r.returncode: sys.exit(1)
js = open(out_js, encoding='utf-8').read().replace('</script', '<\\/script')
lic = '/* three.js r186 — MIT License, Copyright © 2010-2025 three.js authors. Turbo City B4 3D — קוד שלנו. */\n'
page = open(os.path.join(D, 'src', 'shell.html'), encoding='utf-8').read().replace('/*@@APP@@*/', lic + js)
bad = [m for m in ['data:image', '<img', 'new Image(', '.png', '.jpg', 'url(http'] if m in page]
if bad: print('אסור בדף:', bad); sys.exit(2)
outp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'Threed_B4_proto.html')
open(outp, 'w', encoding='utf-8').write(page)
print(outp, len(page.encode()), hashlib.sha1(page.encode()).hexdigest()[:12], 'js', len(js))
