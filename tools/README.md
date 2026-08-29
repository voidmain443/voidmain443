# tools

The prerequisite map and the book covers in the profile README are generated, not drawn.
Editing the course table and re-running the scripts is the whole workflow.

```bash
pip install fonttools
cd tools
python curriculum.py     # -> ../img/curriculum-light.svg, ../img/curriculum-dark.svg
python covers.py         # -> ../img/cover-*.svg
```

Both scripts write into `../img/`, so run them from this directory. `curriculum.py` prints
the faces it resolved and audits the table before drawing; read that output rather than
assuming it worked.

## Editing the map

`curriculum.py` holds one table at the top:

```python
("MATH", "수학", [
    #  code        english title    korean title   stage  status  level
    ("MATH 110", "Linear Algebra", "선형대수학",      2,   "pub",  "ug"),
    ...
]),
```

- **stage** is prerequisite depth, 1–6, not the course number. A course sits one stage to the
  right of its deepest prerequisite. Stacking inside a lane is automatic; the widest stage
  sets that lane's height.
- **status** is `pub` (solid node), `wip` (outlined) or `plan` (hairline).
- **level** is `base`, `ug` or `grad`, printed in the node's top-right corner as 기초 · 학부 ·
  대학원. It is independent of stage: a volume can be shallow in the graph and still be
  written at graduate level, which is exactly what `ECON 510` is.
- `EDGES` are prerequisites inside one department, `CROSS` are the dashed ones between
  departments. Keep `CROSS` short — every entry adds a line that sweeps across the whole
  figure. The map draws the primary prerequisite only; the README table may list more.

`audit()` runs on every build and refuses to stay quiet about duplicate course codes or an
edge that does not move left to right. An edge pointing backwards would draw as a loop, so
fix the stage numbers rather than the drawing code.

Adding a course is three lines: the row in `LANES`, its edge, and the row in the README
table. Nothing else needs touching.

## Editing the covers

`covers.py` holds one dict per volume in `BOOKS` and one drawing function per cover. A new
volume needs a `BOOKS` entry and a `fig_*` function that draws inside `x:[60,400]`,
`y:[196,430]` in white strokes. Department colour comes from `DEPT[...]`.

## Why the SVGs are large

Every glyph is flattened to a path, so the files carry no font reference and render the same
whether or not the reader has a Korean font installed — including inside GitHub's image
sandbox, which strips `<style>` and blocks `@font-face`. The cost is that a repeated
character is a repeated outline: the map is about 700 KB raw and about 215 KB over the wire,
and each cover about 29 KB raw. Changing a title changes the paths, so always regenerate
rather than hand-editing an SVG.

## Fonts

`svgtext.py` resolves Noto Sans KR and DejaVu Sans Mono, falling back to Apple SD Gothic Neo
/ Menlo on macOS and Malgun Gothic / Consolas on Windows. Different fonts change metrics, so
regenerate both the map and the covers together to keep them consistent.

Noto ships on Windows only as `NotoSansKR-VF.ttf`, a variable font whose default instance is
Thin — drawing from it directly would render every run hairline. `svgtext.py` instances it to
400 / 500 / 700 before taking outlines, so a variable font and three static weights give the
same result. `python -c "import svgtext; print(svgtext.describe())"` prints what a machine
actually resolved.

On Debian or Ubuntu:

```bash
sudo apt install fonts-noto-cjk fonts-dejavu-core
```
