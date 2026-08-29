"""Generates the book cover cards used in the README gallery.

The published sites are Jupyter Book / MyST pages; a 170px-wide screenshot of one
is unreadable, so each volume gets a drawn cover instead: department colour,
course code, title, and a line figure taken from the book's own subject matter.
"""

import math
from svgtext import Sheet, NOTO_R, NOTO_M, NOTO_B, MONO_R, MONO_B

W, H = 460, 620
PAD = 40

DEPT = {"MATH": "#2f6f4f", "ECON": "#1a4f7a", "NETS": "#5f4b8b", "AI": "#8a5622"}

# ------------------------------------------------------------------ figures
# Every figure draws inside the box x:[60,400], y:[196,430].

def fig_rebuild():
    """Four ascending strata; a dashed probe drops to the layer below the block."""
    o = []
    x0, y0, w, h = 78, 206, 304, 218
    step_w, step_h = w / 4, h / 4
    # staircase
    pts = []
    for i in range(4):
        pts.append((x0 + i * step_w, y0 + h - i * step_h))
        pts.append((x0 + (i + 1) * step_w, y0 + h - i * step_h))
        pts.append((x0 + (i + 1) * step_w, y0 + h - (i + 1) * step_h))
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="2" opacity="0.9" stroke-linejoin="round"/>')
    # horizontal strata rules
    for i in range(1, 4):
        y = y0 + h - i * step_h
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+w}" y2="{y:.1f}" stroke="#fff" stroke-width="0.9" opacity="0.28" stroke-dasharray="3 4"/>')
    # stuck point on the top step, probe dropping two layers
    px, py = x0 + 3.5 * step_w, y0 + h - 3 * step_h - 16
    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#fff" opacity="0.95"/>')
    o.append(f'<path d="M {px:.1f} {py+12:.1f} L {px:.1f} {y0+h-step_h-10:.1f}" stroke="#fff" stroke-width="1.6" opacity="0.75" stroke-dasharray="5 4"/>')
    o.append(f'<path d="M {px-5:.1f} {y0+h-step_h-16:.1f} L {px:.1f} {y0+h-step_h-8:.1f} L {px+5:.1f} {y0+h-step_h-16:.1f}" fill="none" stroke="#fff" stroke-width="1.6" opacity="0.75"/>')
    o.append(f'<circle cx="{px:.1f}" cy="{y0+h-step_h-2:.1f}" r="3.6" fill="none" stroke="#fff" stroke-width="1.6" opacity="0.75"/>')
    return "".join(o)


def fig_calculus():
    """Inscribed rectangles under a curve — area first, derivative second."""
    o = []
    x0, y0, w, h = 78, 200, 304, 218
    base = y0 + h - 22

    def f(t):  # t in [0,1] -> height fraction
        return 0.30 + 0.62 * (0.5 - 0.5 * math.cos(math.pi * (0.15 + 0.9 * t))) ** 0.75

    # rectangles
    n = 9
    for i in range(n):
        t = (i + 0.5) / n
        hh = f(t) * (h - 46)
        rx = x0 + i * w / n
        o.append(f'<rect x="{rx:.1f}" y="{base-hh:.1f}" width="{w/n-2:.1f}" height="{hh:.1f}" fill="#fff" fill-opacity="0.14" stroke="#fff" stroke-width="0.9" stroke-opacity="0.45"/>')
    # curve
    pts = [(x0 + w * (i / 80), base - f(i / 80) * (h - 46)) for i in range(81)]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="2.2" opacity="0.95"/>')
    # axes
    o.append(f'<line x1="{x0-10}" y1="{base:.1f}" x2="{x0+w+10}" y2="{base:.1f}" stroke="#fff" stroke-width="1.4" opacity="0.6"/>')
    o.append(f'<line x1="{x0-10}" y1="{y0-4}" x2="{x0-10}" y2="{base+10:.1f}" stroke="#fff" stroke-width="1.4" opacity="0.6"/>')
    return "".join(o)


def fig_proof():
    """Three premises converge on one hinge, and the chain closes on the QED square."""
    o = []
    px, hx, hy = 96, 216, 306
    prem = (236, 306, 376)
    for y in prem:
        o.append(f'<circle cx="{px}" cy="{y}" r="7" fill="#fff" fill-opacity="0.16" stroke="#fff" stroke-width="1.8" stroke-opacity="0.9"/>')
        o.append(f'<path d="M {px+10} {y} C {px+52} {y} {hx-56} {hy} {hx-13} {hy}" fill="none" stroke="#fff" stroke-width="1.5" opacity="0.6"/>')
    o.append(f'<circle cx="{hx}" cy="{hy}" r="13" fill="#fff" fill-opacity="0.18" stroke="#fff" stroke-width="2" stroke-opacity="0.95"/>')
    # hinge -> conclusion
    o.append(f'<line x1="{hx+15}" y1="{hy}" x2="292" y2="{hy}" stroke="#fff" stroke-width="1.8" opacity="0.9"/>')
    o.append(f'<path d="M 286 {hy-6} L 294 {hy} L 286 {hy+6}" fill="none" stroke="#fff" stroke-width="1.8" opacity="0.9"/>')
    o.append(f'<rect x="298" y="{hy-30}" width="80" height="60" rx="3" fill="#fff" fill-opacity="0.16" stroke="#fff" stroke-width="2" stroke-opacity="0.95"/>')
    # QED
    o.append(f'<rect x="360" y="404" width="15" height="15" fill="#fff" opacity="0.95"/>')
    o.append(f'<line x1="78" y1="411.5" x2="346" y2="411.5" stroke="#fff" stroke-width="1" opacity="0.28" stroke-dasharray="3 4"/>')
    return "".join(o)


def fig_subspaces():
    """Strang's four fundamental subspaces."""
    o = []
    cx1, cx2, cy = 138, 322, 312
    rw, rh = 46, 96

    def spindle(cx, split_up_h, label_gap=0):
        # two triangles meeting at the centre line
        return (f'<path d="M {cx-rw} {cy-split_up_h} L {cx} {cy-rh} L {cx+rw} {cy-split_up_h} Z" '
                f'fill="#fff" fill-opacity="0.16" stroke="#fff" stroke-width="1.6" stroke-opacity="0.85"/>'
                f'<path d="M {cx-rw} {cy+split_up_h} L {cx} {cy+rh} L {cx+rw} {cy+split_up_h} Z" '
                f'fill="#fff" fill-opacity="0.07" stroke="#fff" stroke-width="1.4" stroke-opacity="0.55"/>')

    o.append(spindle(cx1, 10))
    o.append(spindle(cx2, 10))
    # centre lines
    for cx in (cx1, cx2):
        o.append(f'<line x1="{cx-rw-14}" y1="{cy}" x2="{cx+rw+14}" y2="{cy}" stroke="#fff" stroke-width="1" opacity="0.35" stroke-dasharray="4 4"/>')
    # A : row space -> column space
    o.append(f'<path d="M {cx1+rw-6} {cy-52} C {cx1+70} {cy-70} {cx2-70} {cy-70} {cx2-rw+6} {cy-52}" fill="none" stroke="#fff" stroke-width="1.8" opacity="0.9"/>')
    o.append(f'<path d="M {cx2-rw+1} {cy-58} L {cx2-rw+9} {cy-51} L {cx2-rw-1} {cy-46}" fill="#fff" opacity="0.9"/>')
    # nullspace -> 0
    o.append(f'<path d="M {cx1+rw-6} {cy+54} C {cx1+80} {cy+78} {cx2-40} {cy+40} {cx2-2} {cy+6}" fill="none" stroke="#fff" stroke-width="1.4" opacity="0.55" stroke-dasharray="5 4"/>')
    o.append(f'<circle cx="{cx2}" cy="{cy}" r="4.5" fill="#fff" opacity="0.9"/>')
    return "".join(o)


def fig_regression():
    """Scatter with a fitted line — data first, theory after."""
    o = []
    x0, y0, w, h = 84, 204, 292, 208
    o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#fff" stroke-width="1.2" opacity="0.4"/>')
    for i in range(1, 4):
        o.append(f'<line x1="{x0}" y1="{y0+i*h/4:.1f}" x2="{x0+w}" y2="{y0+i*h/4:.1f}" stroke="#fff" stroke-width="0.7" opacity="0.16"/>')
    pts = [(0.05, 0.78), (0.11, 0.86), (0.18, 0.66), (0.24, 0.72), (0.31, 0.58),
           (0.37, 0.63), (0.43, 0.49), (0.49, 0.55), (0.55, 0.41), (0.62, 0.46),
           (0.68, 0.33), (0.74, 0.39), (0.81, 0.24), (0.88, 0.31), (0.94, 0.18)]
    for t, v in pts:
        o.append(f'<circle cx="{x0+t*w:.1f}" cy="{y0+v*h:.1f}" r="4.2" fill="#fff" fill-opacity="0.55"/>')
    o.append(f'<line x1="{x0+4:.1f}" y1="{y0+0.80*h:.1f}" x2="{x0+w-4:.1f}" y2="{y0+0.20*h:.1f}" stroke="#fff" stroke-width="2.4" opacity="0.95"/>')
    return "".join(o)


def fig_supply_demand():
    """Supply and demand crossing at equilibrium."""
    o = []
    x0, y0, w, h = 92, 200, 280, 212
    base, left = y0 + h, x0
    o.append(f'<line x1="{left}" y1="{y0-6}" x2="{left}" y2="{base+8}" stroke="#fff" stroke-width="1.4" opacity="0.6"/>')
    o.append(f'<line x1="{left-8}" y1="{base}" x2="{x0+w+8}" y2="{base}" stroke="#fff" stroke-width="1.4" opacity="0.6"/>')
    # demand (down) and supply (up)
    o.append(f'<path d="M {x0+8} {y0+10} C {x0+w*0.45} {y0+h*0.42} {x0+w*0.62} {y0+h*0.74} {x0+w-6} {base-14}" fill="none" stroke="#fff" stroke-width="2.4" opacity="0.95"/>')
    o.append(f'<path d="M {x0+8} {base-14} C {x0+w*0.42} {y0+h*0.72} {x0+w*0.58} {y0+h*0.36} {x0+w-6} {y0+10}" fill="none" stroke="#fff" stroke-width="2.4" opacity="0.7"/>')
    ex, ey = x0 + w * 0.5, y0 + h * 0.5
    o.append(f'<line x1="{left}" y1="{ey:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#fff" stroke-width="1.1" opacity="0.55" stroke-dasharray="5 4"/>')
    o.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{ex:.1f}" y2="{base}" stroke="#fff" stroke-width="1.1" opacity="0.55" stroke-dasharray="5 4"/>')
    o.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6.5" fill="#fff" opacity="0.95"/>')
    return "".join(o)


# ------------------------------------------------------------------ books
BOOKS = [
    dict(key="premath", dept="MATH", code="MATH 100",
         ko="수학 재건", en="Foundations before calculus",
         meta="43 chapters · 4 parts", tech="Jupyter Book", status="PUBLISHED", fig=fig_rebuild),
    dict(key="proof", dept="MATH", code="MATH 150",
         ko="증명법", en="Where proof begins",
         meta="논리 · 집합 · 증명 전략", tech="Jupyter Book", status="PUBLISHED", fig=fig_proof),
    dict(key="calculus", dept="MATH", code="MATH 101",
         ko="미적분학", en="Calculus, after Apostol",
         meta="79 sessions · 6 parts", tech="Jupyter Book", status="IN PROGRESS", fig=fig_calculus),
    dict(key="linalg", dept="MATH", code="MATH 110",
         ko="선형대수학", en="Linear algebra, 18.06 rebuilt",
         meta="34 lectures · 9 acts", tech="MyST · NumPy", status="PUBLISHED", fig=fig_subspaces),
    dict(key="econpy", dept="ECON", code="ECON 100",
         ko="경제학 파이썬", en="Python for economists",
         meta="8 weeks · notebooks", tech="Quarto", status="PUBLISHED", fig=fig_regression),
    dict(key="econ101", dept="ECON", code="ECON 101",
         ko="경제학원론", en="Principles of economics",
         meta="15 chapters · 4 parts", tech="MyST · open data", status="PUBLISHED", fig=fig_supply_demand),
]


def build(b):
    sh = Sheet()
    c = DEPT[b["dept"]]
    o = [f'<rect width="{W}" height="{H}" fill="{c}"/>']
    o.append(f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#fff" stroke-width="1" opacity="0.22"/>')

    t, _ = sh.text(b["code"], MONO_B, "mb", 15, PAD, 76, "#ffffff", tracking=2.2, opacity=0.85)
    o.append(t)
    t, _ = sh.text(b["ko"], NOTO_B, "nb", 31, PAD, 126, "#ffffff")
    o.append(t)
    t, _ = sh.text(b["en"], NOTO_R, "nr", 14.5, PAD, 154, "#ffffff", opacity=0.72)
    o.append(t)

    o.append(b["fig"]())

    o.append(f'<line x1="{PAD}" y1="512" x2="{W-PAD}" y2="512" stroke="#fff" stroke-width="1" opacity="0.3"/>')
    t, _ = sh.text(b["meta"], NOTO_R, "nr", 14, PAD, 542, "#ffffff", opacity=0.8)
    o.append(t)
    t, _ = sh.text(b["tech"], NOTO_R, "nr", 12.5, PAD, 566, "#ffffff", opacity=0.55)
    o.append(t)
    t, _ = sh.text(b["status"], MONO_B, "mb", 10.5, W - PAD, 542, "#ffffff",
                   anchor="end", tracking=1.8, opacity=0.85)
    o.append(t)

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="{b["code"]} {b["en"]}">'
            + sh.defs_block() + "".join(o) + "</svg>")


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "img")
    os.makedirs(out, exist_ok=True)
    for b in BOOKS:
        svg = build(b)
        p = os.path.join(out, f"cover-{b['key']}.svg")
        open(p, "w").write(svg)
        print(f"{p}  {len(svg)/1024:.1f} KB")
