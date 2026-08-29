"""Text -> SVG path engine.

Every text run is flattened into a single <path> with the glyph outlines already
transformed into place. No <defs>, no <use>, no @font-face: the result survives
GitHub's SVG sanitiser and renders identically on any machine, whether or not a
Korean font is installed there.

A font spec is ``(path, font_number, weight)``. ``weight`` is None for a static
face and a ``wght`` axis value for a variable font, which is instanced to that
weight before any glyph is drawn -- Noto Sans KR VF defaults to Thin, so an
uninstanced variable font would silently render every run hairline.
"""

import os
import glob as _glob

from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib import instancer

REGULAR, MEDIUM, BOLD = 400, 500, 700


def _mpl_fontdir():
    """matplotlib ships DejaVu; on Windows it is usually the only copy present."""
    try:
        import matplotlib
    except Exception:
        return None
    return os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")


def _first(pattern, prefer_korean=False):
    """First existing font matching `pattern`; for .ttc, the Korean sub-font index."""
    for path in sorted(_glob.glob(os.path.expanduser(pattern), recursive=True)):
        if not path.lower().endswith(".ttc"):
            return (path, 0)
        try:
            coll = TTCollection(path, lazy=True)
        except Exception:
            continue
        for i, f in enumerate(coll.fonts):
            name = f["name"].getDebugName(4) or ""
            if not prefer_korean or ("KR" in name and "Mono" not in name):
                return (path, i)
        return (path, 0)
    return None


# Korean + Latin in one family, so the two scripts never disagree on weight.
# Ordered best-first; ("var", ...) entries are instanced to the requested weight.
_KO_NAMED = {REGULAR: "Regular", MEDIUM: "Medium", BOLD: "Bold"}
_KO_FALLBACK_NAMED = {REGULAR: "Regular", MEDIUM: "Regular", BOLD: "Bold"}


def _ko_candidates(weight):
    w = _KO_NAMED[weight]
    fallback = _KO_FALLBACK_NAMED[weight]
    out = []
    for name in dict.fromkeys((w, fallback)):          # Medium -> Regular if absent
        out += [
            ("static", f"/usr/share/fonts/opentype/noto/NotoSansCJK-{name}.ttc"),
            ("static", f"/usr/share/fonts/**/NotoSansCJK*-{name}.ttc"),
            ("static", f"/usr/share/fonts/**/NotoSansKR-{name}.*"),
            ("static", f"~/Library/Fonts/NotoSansKR-{name}.*"),
        ]
    out += [
        ("var", "/usr/share/fonts/**/NotoSansKR[-_]VF.ttf"),
        ("var", "~/Library/Fonts/NotoSansKR[-_]VF.ttf"),
        ("var", "C:/Windows/Fonts/NotoSansKR-VF.ttf"),
        ("static", "/System/Library/Fonts/AppleSDGothicNeo.ttc"),
        ("static", "C:/Windows/Fonts/malgunbd.ttf" if weight == BOLD
                   else "C:/Windows/Fonts/malgun.ttf"),
    ]
    return out


def _mono_candidates(weight):
    suffix = "-Bold" if weight == BOLD else ""
    out = [
        ("static", f"/usr/share/fonts/truetype/dejavu/DejaVuSansMono{suffix}.ttf"),
        ("static", f"/usr/share/fonts/**/DejaVuSansMono{suffix}.ttf"),
    ]
    mpl = _mpl_fontdir()
    if mpl:
        out.append(("static", os.path.join(mpl, f"DejaVuSansMono{suffix}.ttf")))
    out += [
        ("static", "/System/Library/Fonts/Menlo.ttc"),
        ("static", "C:/Windows/Fonts/consolab.ttf" if weight == BOLD
                   else "C:/Windows/Fonts/consola.ttf"),
    ]
    return out


def _resolve(candidates, weight, prefer_korean=False):
    for kind, pattern in candidates:
        hit = _first(pattern, prefer_korean=prefer_korean)
        if hit:
            return (hit[0], hit[1], weight if kind == "var" else None)
    raise FileNotFoundError(f"no font matched: {[p for _, p in candidates]}")


NOTO_R = _resolve(_ko_candidates(REGULAR), REGULAR, prefer_korean=True)
NOTO_M = _resolve(_ko_candidates(MEDIUM), MEDIUM, prefer_korean=True)
NOTO_B = _resolve(_ko_candidates(BOLD), BOLD, prefer_korean=True)
MONO_R = _resolve(_mono_candidates(REGULAR), REGULAR)
MONO_B = _resolve(_mono_candidates(BOLD), BOLD)


def describe():
    """Which faces this machine actually resolved -- print before regenerating."""
    rows = [("NOTO_R", NOTO_R), ("NOTO_M", NOTO_M), ("NOTO_B", NOTO_B),
            ("MONO_R", MONO_R), ("MONO_B", MONO_B)]
    return "\n".join(
        f"{tag:7} {os.path.basename(p)}"
        + (f"  #{n}" if n else "")
        + (f"  wght={w}" if w else "")
        for tag, (p, n, w) in rows
    )


def _ntos(v):
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    return s


class Face:
    _open = {}

    def __init__(self, spec):
        path, num, weight = spec
        key = (path, num, weight)
        if key not in Face._open:
            lazy = weight is None
            f = TTFont(path, fontNumber=num, lazy=lazy)
            if weight is not None and "fvar" in f:
                instancer.instantiateVariableFont(
                    f, {"wght": weight}, inplace=True, updateFontNames=False
                )
            Face._open[key] = f
        self.f = Face._open[key]
        self.cmap = self.f.getBestCmap()
        self.gs = self.f.getGlyphSet()
        self.upem = self.f["head"].unitsPerEm
        self.hmtx = self.f["hmtx"]

    def gname(self, ch):
        return self.cmap.get(ord(ch))

    def advance(self, ch, size):
        gn = self.gname(ch) or self.cmap.get(0x20)
        return self.hmtx[gn][0] * size / self.upem


class Sheet:
    def __init__(self):
        self.faces = {}

    def face(self, spec, tag):
        if tag not in self.faces:
            self.faces[tag] = Face(spec)
        return self.faces[tag]

    def measure(self, s, spec, tag, size, tracking=0.0):
        face = self.face(spec, tag)
        w = sum(face.advance(c, size) for c in s)
        return w + tracking * max(0, len(s) - 1)

    def fit(self, s, spec, tag, size, limit, floor=7.0, step=0.25):
        """Largest size <= `size` whose run fits in `limit`."""
        while size > floor and self.measure(s, spec, tag, size) > limit:
            size -= step
        return size

    def text(self, s, spec, tag, size, x, y, fill="#000",
             anchor="start", tracking=0.0, opacity=None):
        """Return (svg_fragment, width) with the run's baseline at (x, y)."""
        face = self.face(spec, tag)
        width = self.measure(s, spec, tag, size, tracking)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        scale = size / face.upem
        spen = SVGPathPen(face.gs, ntos=_ntos)
        cx = x
        for ch in s:
            gn = face.gname(ch)
            if gn and ch != " ":
                face.gs[gn].draw(TransformPen(spen, (scale, 0, 0, -scale, cx, y)))
            cx += face.advance(ch, size) + tracking
        d = spen.getCommands()
        if not d:
            return "", width
        op = f' opacity="{opacity}"' if opacity is not None else ""
        return f'<path d="{d}" fill="{fill}"{op}/>', width

    def defs_block(self):
        # kept for call-site compatibility; nothing to emit any more
        return ""
