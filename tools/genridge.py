#!/usr/bin/env python3
"""Generate natural alpine panorama SVG via midpoint-displacement ridgelines."""
import random
import sys

W = 2880
H = 220

def displace(anchors, amp, decay, levels, rng, ymin, ymax):
    pts = list(anchors)
    for _ in range(levels):
        new = []
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            mx = (x0 + x1) / 2
            my = (y0 + y1) / 2 + rng.uniform(-amp, amp)
            new += [(x0, y0), (mx, my)]
        new.append(pts[-1])
        pts = new
        amp *= decay
    return [(x, max(ymin, min(ymax, y))) for x, y in pts]

def sharpen(pts, strength):
    """Pull local maxima up and minima down slightly -> craggier crests."""
    out = list(pts)
    for i in range(1, len(pts) - 1):
        y_prev, y, y_next = pts[i-1][1], pts[i][1], pts[i+1][1]
        if y < y_prev and y < y_next:      # summit (smaller y = higher)
            out[i] = (pts[i][0], y - strength)
        elif y > y_prev and y > y_next:    # notch
            out[i] = (pts[i][0], y + strength * 0.5)
    return out

def insert_matterhorn(pts, x_from, x_to, base_summit=70):
    """Replace a window of points with the iconic hooked pyramid."""
    left = [p for p in pts if p[0] < x_from]
    right = [p for p in pts if p[0] > x_to]
    yl = left[-1][1] if left else 130
    yr = right[0][1] if right else 130
    horn = [
        (x_from, yl),
        (x_from + 22, (yl + 100) / 2),
        (x_from + 44, 98),
        (x_from + 60, 82),
        (x_from + 71, base_summit + 4),
        (x_from + 68, base_summit + 1),
        (x_from + 82, base_summit),
        (x_from + 94, base_summit + 12),
        (x_from + 91, base_summit + 22),
        (x_from + 108, base_summit + 44),
        (x_from + 128, (yr + 120) / 2),
        (x_to, yr),
    ]
    return left + horn + right

def sample(pts, x):
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0) if x1 > x0 else 0
            return y0 + t * (y1 - y0)
    return pts[-1][1]

def path(pts, dec=1):
    d = "M{:.{p}f} {:.{p}f} ".format(pts[0][0], pts[0][1], p=dec)
    d += " ".join("L{:.{p}f} {:.{p}f}".format(x, y, p=dec) for x, y in pts[1:])
    d += " L{} {} L0 {} Z".format(W, H, H)
    return d

def crest_line(pts, dec=1):
    d = "M{:.{p}f} {:.{p}f} ".format(pts[0][0], pts[0][1], p=dec)
    d += " ".join("L{:.{p}f} {:.{p}f}".format(x, y, p=dec) for x, y in pts[1:])
    return d

def tree(x, y, h, w):
    return '<path d="M{:.0f} {:.1f} L{:.0f} {:.1f} L{:.0f} {:.1f} Z"/>'.format(
        x - w / 2, y, x, y - h, x + w / 2, y)

def gen(seed):
    rng = random.Random(seed)

    # L1: the snow chain on the horizon (highest, farthest)
    snow_anchors = [(0, 126), (280, 98), (560, 122), (840, 86), (1120, 114),
                    (1400, 118), (1680, 94), (1960, 124), (2240, 90),
                    (2520, 120), (2880, 102)]
    snow = displace(snow_anchors, 24, 0.55, 5, rng, 74, 150)
    snow = sharpen(snow, 4)
    snow = insert_matterhorn(snow, 1420, 1580)

    # L1b: rocky spurs directly in front of the snow
    spur_anchors = [(0, 148), (400, 126), (800, 146), (1200, 122),
                    (1600, 142), (2000, 124), (2400, 146), (2880, 130)]
    spur = displace(spur_anchors, 18, 0.55, 5, rng, 108, 165)
    spur = sharpen(spur, 3)

    # L2: hazy mid ridge
    mid_anchors = [(0, 162), (480, 142), (960, 160), (1440, 138),
                   (1920, 158), (2400, 140), (2880, 160)]
    mid = displace(mid_anchors, 12, 0.55, 5, rng, 128, 176)

    # L3: dark forested ridge (gondola valley carved near centre)
    dark_anchors = [(0, 178), (400, 162), (800, 176), (1140, 154),
                    (1290, 172), (1440, 152), (1800, 172), (2200, 158),
                    (2600, 176), (2880, 166)]
    dark = displace(dark_anchors, 9, 0.55, 5, rng, 146, 190)

    # L4: near forest hill
    near_anchors = [(0, 196), (600, 184), (1200, 194), (1800, 182),
                    (2400, 194), (2880, 188)]
    near = displace(near_anchors, 7, 0.55, 5, rng, 176, 205)

    # L5: meadow
    meadow_anchors = [(0, 208), (720, 202), (1440, 206), (2160, 200), (2880, 206)]
    meadow = displace(meadow_anchors, 3, 0.5, 4, rng, 196, 214)

    # Gondola cable across the carved valley on L3
    cx1, cx2 = 1150, 1430
    cy1, cy2 = sample(dark, cx1) - 2, sample(dark, cx2) - 2
    midx, midy = (cx1 + cx2) / 2, max(cy1, cy2) + 16

    # Trees on L3 (small) and L4 (large, grouped per cluster so they can sway)
    t_small, t_big_clusters = [], []
    for cx in (760, 2180):
        for i in range(4):
            x = cx + i * 15 + rng.uniform(-3, 3)
            t_small.append(tree(x, sample(dark, x) + 2, 11, 9))
    for cx in (340, 1080, 1660, 2520):
        cluster = []
        for i in range(5):
            x = cx + i * 17 + rng.uniform(-4, 4)
            cluster.append(tree(x, sample(near, x) + 2, 16, 13))
        t_big_clusters.append("".join(cluster))

    return {
        "snow": snow, "spur": spur, "mid": mid, "dark": dark,
        "near": near, "meadow": meadow,
        "cable": (cx1, cy1, midx, midy, cx2, cy2),
        "t_small": "\n".join(t_small), "t_big_clusters": t_big_clusters,
    }

COLORS = {
    "snow": "#EDF2F6", "snow_line": "#C3CFDA",
    "spur": "#CBD6DF", "mid": "#AEBEB4",
    "dark": "#879C8D", "near": "#71876B", "meadow_a": "#A9B69A",
    "t_small": "#5E7466", "t_big": "#4C6152",
}

def scene(g, ids, gondola=False, train=False, classes=False):
    c = COLORS
    cls = lambda n: ' class="rl-{}"'.format(n) if classes else ""
    x1, y1, mx, my, x2, y2 = g["cable"]
    parts = []
    parts.append(
        '<defs>'
        '<radialGradient id="glow-{p}">'
        '<stop offset="0" stop-color="#E4A05E" stop-opacity="0.32"/>'
        '<stop offset="0.5" stop-color="#E4A05E" stop-opacity="0.12"/>'
        '<stop offset="1" stop-color="#E4A05E" stop-opacity="0"/>'
        '</radialGradient>'
        '<radialGradient id="warm-{p}">'
        '<stop offset="0" stop-color="#E2A878" stop-opacity="0.16"/>'
        '<stop offset="1" stop-color="#E2A878" stop-opacity="0"/>'
        '</radialGradient>'
        '</defs>'.format(p=ids))
    parts.append('<g class="sun-glow"><circle cx="1760" cy="102" r="84" fill="url(#glow-{p})"/></g>'.format(p=ids))
    parts.append('<circle class="sun" cx="1760" cy="102" r="30" fill="var(--accent)" opacity="0.14"/>')
    parts.append('<g{}>'.format(cls(1)))
    parts.append('<path fill="{}" d="{}"/>'.format(c["snow"], path(g["snow"])))
    parts.append('<path fill="none" stroke="{}" stroke-width="1.2" opacity="0.65" stroke-linejoin="round" stroke-linecap="round" d="{}"/>'.format(
        c["snow_line"], crest_line(g["snow"])))
    parts.append('</g>')
    parts.append('<g{}><path fill="{}" d="{}"/></g>'.format(cls(2), c["spur"], path(g["spur"])))
    # Warm golden-hour wash over the distant ranges only.
    # Must fade out before the canvas top edge or it clips to a hard line.
    parts.append('<ellipse cx="1760" cy="114" rx="560" ry="102" fill="url(#warm-{p})"/>'.format(p=ids))
    parts.append('<g{}><path fill="{}" d="{}"/></g>'.format(cls(3), c["mid"], path(g["mid"])))
    parts.append('<g{}>'.format(cls(4)))
    parts.append('<path fill="{}" d="{}"/>'.format(c["dark"], path(g["dark"])))
    parts.append('<g fill="{}" opacity="0.8">{}</g>'.format(c["t_small"], g["t_small"]))
    if gondola:
        parts.append('<path d="M{:.0f} {:.1f} Q {:.0f} {:.1f} {:.0f} {:.1f}" stroke="rgba(29,42,40,0.45)" stroke-width="1" fill="none"/>'.format(x1, y1, mx, my, x2, y2))
        parts.append('<circle cx="{:.0f}" cy="{:.1f}" r="1.5" fill="rgba(29,42,40,0.5)"/>'.format(x1, y1))
        parts.append('<circle cx="{:.0f}" cy="{:.1f}" r="1.5" fill="rgba(29,42,40,0.5)"/>'.format(x2, y2))
        parts.append('<g transform="translate({:.0f}, {:.1f})"><g class="gondola">'.format(x1, y1))
        parts.append('<path d="M0 0 V4" stroke="rgba(29,42,40,0.6)" stroke-width="0.8"/>')
        parts.append('<rect x="-3.5" y="4" width="7" height="6" rx="1.5" fill="#3A4644" opacity="0.9"/>')
        parts.append('</g></g>')
    parts.append('</g>')
    parts.append('<g{}>'.format(cls(5)))
    parts.append('<path fill="{}" d="{}"/>'.format(c["near"], path(g["near"])))
    for i, cluster in enumerate(g["t_big_clusters"]):
        parts.append('<g class="sway" style="--sd: {:.1f}s; animation-delay: -{:.1f}s" fill="{}" opacity="0.85">{}</g>'.format(
            4.4 + i * 0.7, i * 1.3, c["t_big"], cluster))
    parts.append('</g>')
    if train:
        parts.append('<g transform="translate(0, 196) scale(1.5)"><g class="train">')
        parts.append('<rect x="0" y="0" width="16" height="6" rx="1.6" fill="var(--accent)" opacity="0.82"/>')
        parts.append('<rect x="19" y="0.6" width="13" height="5.4" rx="1.4" fill="var(--accent)" opacity="0.78"/>')
        parts.append('<rect x="35" y="0.6" width="13" height="5.4" rx="1.4" fill="var(--accent)" opacity="0.78"/>')
        parts.append('<rect x="51" y="0.6" width="13" height="5.4" rx="1.4" fill="var(--accent)" opacity="0.78"/>')
        parts.append('</g></g>')
    parts.append('<path fill="{}" d="{}"/>'.format(c["meadow_a"], path(g["meadow"])))
    return "\n".join(parts)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "test":
        rows = []
        for seed in (7, 23, 51):
            g = gen(seed)
            inner = scene(g, "t%d" % seed, gondola=True)
            rows.append(
                '<p style="font:12px sans-serif;margin:8px 0 2px">seed {} (full)</p>'
                '<svg viewBox="0 0 2880 220" style="width:100%;background:#FAFAF7;display:block">{}</svg>'
                '<p style="font:12px sans-serif;margin:8px 0 2px">seed {} (center crop, as on mobile)</p>'
                '<svg viewBox="900 0 1100 220" style="width:100%;background:#FAFAF7;display:block" preserveAspectRatio="xMidYMax slice">{}</svg>'
                .format(seed, inner, seed, inner))
        html = ('<!doctype html><meta name="viewport" content="width=device-width">'
                '<style>:root{--accent:#C13B33}body{margin:0;padding:8px;background:#fff}</style>'
                + "\n".join(rows))
        out = "/Users/benberton/Documents/School/Projects/AboutMe/docs/_ridge_test.html"
        with open(out, "w") as f:
            f.write(html)
        print("wrote", out)
    else:
        seed = int(mode)
        g = gen(seed)
        print("=== HERO ===")
        print(scene(g, "h", gondola=True, classes=True))
        print("=== FOOTER ===")
        print(scene(g, "f", train=True))
        x1, y1, mx, my, x2, y2 = g["cable"]
        print("=== GONDOLA KEYFRAMES ===")
        print("0%: translate(8px, 2px)")
        print("50%: translate({:.0f}px, {:.0f}px)".format((x2-x1)/2, my - y1))
        print("100%: translate({:.0f}px, {:.0f}px)".format(x2-x1-8, y2-y1))
