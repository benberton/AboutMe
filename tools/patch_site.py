#!/usr/bin/env python3
"""Patch index.html with the generated seed-7 panorama."""
import re
import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-benberton-Documents-School-Spring-2026-AI--Law--and-Policy-AILawAndPolicy/86c5bc71-41b2-4c93-95d6-c159d8fdb997/scratchpad")
from genridge import gen, scene

SEED = 7
INDEX = "/Users/benberton/Documents/School/Projects/AboutMe/docs/index.html"

g = gen(SEED)
hero_inner = scene(g, "h", gondola=True, classes=True)
footer_inner = scene(g, "f", train=True)

svg_open = '<svg viewBox="0 0 2880 220" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg">'

html = open(INDEX).read()

# Hero: the ridge div with data-parallax
pat_hero = re.compile(r'(<div class="ridge" aria-hidden="true" data-parallax>\s*)<svg.*?</svg>', re.S)
if not pat_hero.search(html):
    sys.exit("hero svg block not found")
html = pat_hero.sub(lambda m: m.group(1) + svg_open + "\n" + hero_inner + "\n</svg>", html, count=1)

# Footer: the plain ridge div
pat_footer = re.compile(r'(<div class="ridge" aria-hidden="true">\s*)<svg.*?</svg>', re.S)
if not pat_footer.search(html):
    sys.exit("footer svg block not found")
html = pat_footer.sub(lambda m: m.group(1) + svg_open + "\n" + footer_inner + "\n</svg>", html, count=1)

# Gondola keyframes from generated cable geometry
x1, y1, mx, my, x2, y2 = g["cable"]
kf = ("@keyframes gondola-run {\n"
      "            0%%   { transform: translate(8px, 2px); }\n"
      "            50%%  { transform: translate(%.0fpx, %.0fpx); }\n"
      "            100%% { transform: translate(%.0fpx, %.0fpx); }\n"
      "        }") % ((x2 - x1) / 2, my - y1, x2 - x1 - 8, y2 - y1)
pat_kf = re.compile(r'@keyframes gondola-run \{.*?\n        \}', re.S)
if not pat_kf.search(html):
    sys.exit("gondola keyframes not found")
html = pat_kf.sub(kf, html, count=1)

open(INDEX, "w").write(html)
print("patched with seed", SEED)
print("cable:", g["cable"])
