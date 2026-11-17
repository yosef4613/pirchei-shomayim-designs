#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""4.11 00:45 · live_f9fix — the owner (00:32): in the zone page of A5 the F9 button "משחק עכשיו עם קהל" could not be seen — the bar of the zone
(tcZoneBar, top right) and the bar of day and night (tcStoryBar, top left) sat over the panel (z-index 2147483000 against 65), over its first card and its close button.
The fix: while the F9 panel is open, the two bars step aside (hidden), and come back when it closes. Every zone page from now on — with this script.
usage: python3 live_f9fix.py <live_page.html> <out.html>   (a new name; the source is not changed)"""
import sys, os
src, out = sys.argv[1], sys.argv[2]
if os.path.exists(out): sys.exit('exists: ' + out)
H = open(src, encoding='utf-8').read()
TAG = '/* live_f9fix */'
assert TAG not in H, 'already fixed'
assert 'id="tcZoneBar"' in H or 'id="tcStoryBar"' in H, 'not a zone page'
S = ('<script>' + TAG + '(function(){var ids=["tcZoneBar","tcStoryBar"];setInterval(function(){var f=document.getElementById("tcF9"),'
     'open=!!(f&&getComputedStyle(f).display!=="none");ids.forEach(function(i){var e=document.getElementById(i);if(e)e.style.visibility=open?"hidden":"visible"})},250)})();</script>')
k = H.rfind('</body>')
H = H[:k] + S + H[k:] if k > 0 else H + S
open(out, 'w', encoding='utf-8').write(H); print(out, len(H.encode('utf-8')))
