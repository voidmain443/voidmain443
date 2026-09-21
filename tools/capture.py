"""Captures a published site for the README gallery.

    cd tools
    python capture.py <name> <url>               # -> ../img/shots/<name>.jpg   (1440x900 viewport, 1200px wide JPEG)
    python capture.py --gif <name> <url> [<url> ...]   # -> ../img/shots/<name>.gif  (720px, crossfade slideshow)

Needs Google Chrome (headless) and Pillow: pip install pillow.
Captures are taken at 1440x900 so that Jupyter Book / MyST sidebars render in the desktop layout.
"""

import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "img", "shots")
CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
]


def chrome():
    for c in CHROME:
        if os.path.exists(c):
            return c
    raise SystemExit("Chrome not found; edit CHROME in capture.py")


def shot(url, path, w=1440, h=900):
    subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--virtual-time-budget=12000",
                    f"--screenshot={path}", url], check=True, capture_output=True)
    return Image.open(path).convert("RGB")


def frame(im, color=(139, 148, 158), px=2):
    """Bakes a thin border into the capture so it keeps an edge on GitHub's dark theme, where
    README images get no CSS of their own and a light UI would otherwise float as a white slab."""
    from PIL import ImageOps
    return ImageOps.expand(im, border=px, fill=color)


def jpeg(name, url, width=1200, quality=82):
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        im = shot(url, os.path.join(t, "s.png"))
    im = frame(im.resize((width - 4, int(im.height * (width - 4) / im.width)), Image.LANCZOS))
    p = os.path.join(OUT, f"{name}.jpg")
    im.save(p, "JPEG", quality=quality, optimize=True, progressive=True)
    print(p, im.size, f"{os.path.getsize(p) / 1024:.0f} KB")


def gif(name, urls, width=720, hold=1700, colors=96):
    os.makedirs(OUT, exist_ok=True)
    frames = []
    with tempfile.TemporaryDirectory() as t:
        for i, u in enumerate(urls):
            im = shot(u, os.path.join(t, f"{i}.png"))
            frames.append(frame(im.resize((width - 4, int(im.height * (width - 4) / im.width)), Image.LANCZOS)))
    seq, dur = [], []
    for i, f in enumerate(frames):
        seq.append(f); dur.append(hold)
        seq.append(Image.blend(f, frames[(i + 1) % len(frames)], 0.5)); dur.append(70)
    q = [s.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for s in seq]
    p = os.path.join(OUT, f"{name}.gif")
    q[0].save(p, save_all=True, append_images=q[1:], duration=dur, loop=0, optimize=True)
    print(p, f"{len(seq)} frames", f"{os.path.getsize(p) / 1024:.0f} KB")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    if a[0] == "--gif":
        gif(a[1], a[2:])
    else:
        jpeg(a[0], a[1])
