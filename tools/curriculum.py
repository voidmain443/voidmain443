"""Generates the prerequisite map SVG (light + dark) for the profile README."""

from svgtext import Sheet, NOTO_R, NOTO_M, NOTO_B, MONO_R, MONO_B

# ---------------------------------------------------------------- data
# (code, en title, ko title, stage, status, level)
#   stage  : prerequisite depth 1-6, not the course number
#   status : pub | wip | plan
#   level  : base | ug | grad      (기초 · 학부 · 대학원)
LANES = [
    ("MATH", "수학", [
        ("MATH 100", "Math Rebuild",        "수학 재건",     1, "pub",  "base"),
        ("MATH 150", "Proof and Logic",     "증명법",        2, "pub",  "base"),
        ("MATH 101", "Calculus",            "미적분학",      2, "wip",  "ug"),
        ("MATH 110", "Linear Algebra",      "선형대수학",    2, "pub",  "ug"),
        ("MATH 120", "Probability & Stats", "확률통계",      3, "plan", "ug"),
        ("MATH 201", "Real Analysis",       "해석학",        3, "wip",  "ug"),
        ("MATH 210", "Differential Eqns",   "미분방정식",    3, "plan", "ug"),
        ("MATH 230", "Discrete & Combin.",  "이산·조합론",   3, "plan", "ug"),
        ("MATH 220", "Multivariable",       "다변수해석",    4, "plan", "ug"),
        ("MATH 240", "Numerical Analysis",  "수치해석",      4, "plan", "ug"),
        ("MATH 260", "Optimization",        "최적화",        4, "plan", "ug"),
        ("MATH 301", "Measure & Prob.",     "측도·확률론",   5, "plan", "grad"),
        ("MATH 320", "Functional Analysis", "함수해석",      5, "plan", "grad"),
        ("MATH 310", "Stochastic Processes", "확률과정",     6, "plan", "grad"),
        ("MATH 330", "Statistical Inference", "통계적 추론", 6, "plan", "grad"),
    ]),
    ("ECON", "경제학", [
        ("ECON 100", "Python for Economists", "경제학 파이썬", 1, "pub",  "base"),
        ("ECON 101", "Principles",            "경제학원론",    2, "pub",  "base"),
        ("ECON 201", "Microeconomics",        "미시경제이론",  3, "plan", "ug"),
        ("ECON 202", "Macroeconomics",        "거시경제이론",  3, "plan", "ug"),
        ("ECON 510", "Math for Economists",   "경제수학",      3, "wip",  "grad"),
        ("ECON 301", "Econometrics",          "계량경제학",    4, "plan", "ug"),
        ("ECON 311", "Game Theory",           "게임이론",      4, "plan", "ug"),
        ("ECON 320", "Industrial Org.",       "산업조직론",    4, "plan", "ug"),
        ("ECON 520", "Mathematical Econ.",    "수리경제학",    4, "plan", "grad"),
        ("ECON 401", "Time Series",           "시계열분석",    5, "plan", "ug"),
        ("ECON 601", "Advanced Micro",        "미시이론",      5, "plan", "grad"),
        ("ECON 602", "Advanced Macro",        "거시이론",      5, "plan", "grad"),
        ("ECON 620", "Computational Econ.",   "계산경제학",    5, "plan", "grad"),
        ("ECON 610", "Econometric Theory",    "계량이론",      6, "plan", "grad"),
        ("ECON 630", "Financial Economics",   "금융경제학",    6, "plan", "grad"),
    ]),
    ("NETS", "네트워크 과학", [
        ("NETS 201", "Introduction to Networks", "네트워크 기초", 3, "plan", "ug"),
        ("NETS 301", "Network Science",       "네트워크 과학",   4, "wip",  "ug"),
        ("NETS 310", "Statistical Physics",   "통계물리",        4, "plan", "ug"),
        ("NETS 320", "Random Graphs",         "랜덤그래프",      5, "plan", "grad"),
        ("NETS 330", "Network Dynamics",      "네트워크 동역학", 5, "plan", "grad"),
        ("NETS 510", "Complex Systems",       "복잡계",          5, "plan", "grad"),
        ("NETS 410", "Network Economics",     "네트워크경제학",  6, "plan", "grad"),
        ("NETS 520", "Econophysics",          "경제물리학",      6, "plan", "grad"),
        ("NETS 530", "Inference on Networks", "네트워크 추론",   6, "plan", "grad"),
    ]),
    ("AI", "인공지능", [
        ("AI 100", "SQL Professional",     "SQL 전문가",     2, "wip",  "base"),
        ("AI 200", "AI-Assisted Study",    "AI 활용 학습",   2, "plan", "base"),
        ("AI 110", "Data Analysis",        "판다스 분석",    3, "plan", "base"),
        ("AI 301", "Machine Learning",     "머신러닝",       4, "plan", "ug"),
        ("AI 310", "Deep Learning",        "딥러닝",         5, "plan", "ug"),
        ("AI 520", "Reinforcement Learning", "강화학습",     5, "plan", "grad"),
        ("AI 410", "Graph Neural Nets",    "그래프 신경망",  6, "plan", "grad"),
        ("AI 501", "Learning Theory",      "통계적 학습이론", 6, "plan", "grad"),
        ("AI 530", "Causal Inference",     "인과추론",       6, "plan", "grad"),
    ]),
]

EDGES = [  # (src, dst) inside one department; always left to right
    ("MATH 100", "MATH 150"), ("MATH 100", "MATH 101"), ("MATH 100", "MATH 110"),
    ("MATH 101", "MATH 120"), ("MATH 150", "MATH 201"), ("MATH 101", "MATH 210"),
    ("MATH 150", "MATH 230"),
    ("MATH 101", "MATH 220"), ("MATH 110", "MATH 240"), ("MATH 110", "MATH 260"),
    ("MATH 201", "MATH 301"), ("MATH 201", "MATH 320"),
    ("MATH 301", "MATH 310"), ("MATH 301", "MATH 330"),

    ("ECON 100", "ECON 101"),
    ("ECON 101", "ECON 201"), ("ECON 101", "ECON 202"), ("ECON 100", "ECON 510"),
    ("ECON 201", "ECON 301"), ("ECON 202", "ECON 301"),
    ("ECON 201", "ECON 311"), ("ECON 201", "ECON 320"), ("ECON 510", "ECON 520"),
    ("ECON 301", "ECON 401"), ("ECON 520", "ECON 601"), ("ECON 520", "ECON 602"),
    ("ECON 510", "ECON 620"),
    ("ECON 301", "ECON 610"), ("ECON 601", "ECON 630"),

    ("NETS 201", "NETS 301"),
    ("NETS 301", "NETS 320"), ("NETS 310", "NETS 320"), ("NETS 301", "NETS 330"),
    ("NETS 310", "NETS 510"),
    ("NETS 301", "NETS 410"), ("NETS 510", "NETS 520"), ("NETS 320", "NETS 530"),

    ("AI 100", "AI 110"), ("AI 110", "AI 301"),
    ("AI 301", "AI 310"), ("AI 301", "AI 520"),
    ("AI 310", "AI 410"), ("AI 310", "AI 501"), ("AI 301", "AI 530"),
]

CROSS = [  # dashed, cross-department
    ("MATH 110", "ECON 510"),
    ("MATH 110", "NETS 201"),
    ("MATH 120", "ECON 301"),
    ("MATH 120", "NETS 310"),
    ("MATH 120", "AI 301"),
    ("MATH 240", "ECON 620"),
    ("MATH 260", "AI 310"),
    ("MATH 301", "ECON 610"),
    ("ECON 100", "AI 200"),
    ("ECON 100", "AI 110"),
    ("ECON 201", "NETS 410"),
    ("ECON 301", "AI 530"),
    ("NETS 301", "AI 410"),
]

LEVEL_KO = {"base": "기초", "ug": "학부", "grad": "대학원"}

THEMES = {
    "light": dict(
        bg="#ffffff", ink="#1f2328", muted="#656d76", hair="#d1d9e0",
        dept={"MATH": "#2f6f4f", "ECON": "#1a4f7a", "NETS": "#5f4b8b", "AI": "#8a5622"},
        on_dept="#ffffff", tint=0.10,
    ),
    "dark": dict(
        bg="#0d1117", ink="#e6edf3", muted="#8b949e", hair="#30363d",
        dept={"MATH": "#4fbe93", "ECON": "#6cb6ff", "NETS": "#b39ddb", "AI": "#dda15e"},
        on_dept="#0d1117", tint=0.16,
    ),
}

# ---------------------------------------------------------------- geometry
W = 1240
GUT = 106            # left gutter for lane labels
PAD_R = 28
HEAD = 118
FOOT = 82
NODE_W = 172
NODE_H = 52
ROW_GAP = 12
LANE_GAP = 34
STAGES = 6

CONTENT_W = W - GUT - PAD_R
PITCH = CONTENT_W / STAGES


def stage_x(s):
    return GUT + (s - 1) * PITCH


def build(theme_name):
    T = THEMES[theme_name]
    sh = Sheet()
    body = []

    # --- lane vertical extents -------------------------------------------
    lanes = []
    y = HEAD
    for code, ko, courses in LANES:
        rows = max(
            sum(1 for c in courses if c[3] == s) for s in range(1, STAGES + 1)
        )
        h = rows * NODE_H + (rows - 1) * ROW_GAP
        lanes.append(dict(code=code, ko=ko, courses=courses, y=y, h=h, rows=rows))
        y += h + LANE_GAP
    H = y - LANE_GAP + FOOT

    # --- node placement ---------------------------------------------------
    pos = {}
    for L in lanes:
        for s in range(1, STAGES + 1):
            col = [c for c in L["courses"] if c[3] == s]
            if not col:
                continue
            k = len(col)
            top = L["y"] + (L["h"] - (k * NODE_H + (k - 1) * ROW_GAP)) / 2
            for i, c in enumerate(col):
                pos[c[0]] = dict(
                    x=stage_x(s), y=top + i * (NODE_H + ROW_GAP),
                    lane=L["code"], course=c,
                )

    body.append(f'<rect width="{W}" height="{H:.0f}" fill="{T["bg"]}"/>')

    # --- header -----------------------------------------------------------
    t, _ = sh.text("PREREQUISITE MAP", MONO_B, "mb", 13, GUT, 38, T["ink"], tracking=1.9)
    body.append(t)
    t, _ = sh.text("선수과목 지도 · 기초에서 대학원까지, 네 학과가 서로를 어떻게 떠받치는가",
                   NOTO_R, "nr", 12.5, GUT, 60, T["muted"])
    body.append(t)

    # legend, right aligned
    lx = W - PAD_R
    leg = [("plan", "planned", "예정"), ("wip", "in progress", "제작 중"),
           ("pub", "published", "게시됨")]
    for status, en, ko in leg:
        label = f"{en} · {ko}"
        wlab = sh.measure(label, NOTO_R, "nr", 11.5)
        lx -= wlab
        t, _ = sh.text(label, NOTO_R, "nr", 11.5, lx, 45, T["muted"])
        body.append(t)
        lx -= 10
        sw = 22
        lx -= sw
        c = T["ink"]
        if status == "pub":
            body.append(f'<rect x="{lx:.1f}" y="34" width="{sw}" height="13" rx="2" fill="{c}"/>')
        elif status == "wip":
            body.append(f'<rect x="{lx:.1f}" y="34" width="{sw}" height="13" rx="2" fill="{c}" fill-opacity="{T["tint"]}" stroke="{c}" stroke-width="1.2"/>')
        else:
            body.append(f'<rect x="{lx:.1f}" y="34" width="{sw}" height="13" rx="2" fill="none" stroke="{T["hair"]}" stroke-width="1"/>')
        lx -= 26

    # stage axis
    ay = HEAD - 30
    body.append(f'<line x1="{GUT}" y1="{ay}" x2="{W-PAD_R}" y2="{ay}" stroke="{T["hair"]}" stroke-width="1"/>')
    t, _ = sh.text("STAGE", MONO_R, "mr", 9.5, GUT - 14, ay - 7, T["muted"], anchor="end", tracking=1.2)
    body.append(t)
    for s in range(1, STAGES + 1):
        x = stage_x(s)
        body.append(f'<line x1="{x:.1f}" y1="{ay-5}" x2="{x:.1f}" y2="{ay}" stroke="{T["hair"]}" stroke-width="1"/>')
        t, _ = sh.text(str(s), MONO_R, "mr", 9.5, x + 5, ay - 7, T["muted"])
        body.append(t)

    # --- lane rules and labels -------------------------------------------
    for L in lanes:
        c = T["dept"][L["code"]]
        body.append(
            f'<rect x="{GUT-26}" y="{L["y"]:.1f}" width="2.5" height="{L["h"]:.1f}" fill="{c}" rx="1.25"/>'
        )
        t, _ = sh.text(L["code"], MONO_B, "mb", 12.5, GUT - 40, L["y"] + 13, c,
                       anchor="end", tracking=1.1)
        body.append(t)
        t, _ = sh.text(L["ko"], NOTO_R, "nr", 10.5, GUT - 40, L["y"] + 29, T["muted"],
                       anchor="end")
        body.append(t)

    # --- edges (drawn under nodes) ---------------------------------------
    edge_svg = []

    def curve(a, b, color, dashed):
        p, q = pos[a], pos[b]
        x1, y1 = p["x"] + NODE_W, p["y"] + NODE_H / 2
        x2, y2 = q["x"], q["y"] + NODE_H / 2
        dx = max(34.0, (x2 - x1) * 0.55)
        d = f"M {x1:.1f} {y1:.1f} C {x1+dx:.1f} {y1:.1f} {x2-dx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"
        dash = ' stroke-dasharray="4.5 3.5"' if dashed else ""
        op = "0.42" if dashed else "0.55"
        edge_svg.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.1" opacity="{op}"{dash}/>'
        )
        edge_svg.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2.4" fill="{color}" opacity="0.75"/>')

    for a, b in EDGES:
        curve(a, b, T["dept"][pos[b]["lane"]], False)
    for a, b in CROSS:
        curve(a, b, T["dept"][pos[b]["lane"]], True)
    body.extend(edge_svg)

    # --- nodes ------------------------------------------------------------
    for name, p in pos.items():
        code, en, ko, s, status, level = p["course"]
        c = T["dept"][p["lane"]]
        x, y = p["x"], p["y"]
        # opaque plate so edges never run across a node
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{NODE_W}" height="{NODE_H}" rx="3" fill="{T["bg"]}"/>')
        if status == "pub":
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{NODE_W}" height="{NODE_H}" rx="3" fill="{c}"/>')
            c_code, c_title = T["on_dept"], T["on_dept"]
            op_title = 0.88
        elif status == "wip":
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{NODE_W}" height="{NODE_H}" rx="3" fill="{c}" fill-opacity="{T["tint"]}" stroke="{c}" stroke-width="1.3"/>')
            c_code, c_title = c, T["ink"]
            op_title = 1
        else:
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{NODE_W}" height="{NODE_H}" rx="3" fill="none" stroke="{T["hair"]}" stroke-width="1"/>')
            c_code, c_title = T["muted"], T["muted"]
            op_title = 1
        t, _ = sh.text(code, MONO_B, "mb", 10.5, x + 12, y + 18, c_code, tracking=0.5)
        body.append(t)
        # level, right aligned on the code line
        t, _ = sh.text(LEVEL_KO[level], NOTO_R, "nr", 9, x + NODE_W - 12, y + 18,
                       c_code, anchor="end", opacity=0.72)
        body.append(t)
        ko_size = sh.fit(ko, NOTO_M, "nm", 13, NODE_W - 24, floor=10.5)
        t, _ = sh.text(ko, NOTO_M, "nm", ko_size, x + 12, y + 35, c_title, opacity=op_title)
        body.append(t)
        en_size = sh.fit(en, NOTO_R, "nr", 9.5, NODE_W - 24, floor=7.5, step=0.5)
        t, _ = sh.text(en, NOTO_R, "nr", en_size, x + 12, y + 47, c_title, opacity=0.60)
        body.append(t)

    # --- footer -----------------------------------------------------------
    fy = H - 38
    body.append(f'<line x1="{GUT}" y1="{fy-22}" x2="{W-PAD_R}" y2="{fy-22}" stroke="{T["hair"]}" stroke-width="1"/>')
    t, _ = sh.text("dashed edge = prerequisite from another department · 점선은 타 학과 선수과목",
                   NOTO_R, "nr", 11, GUT, fy, T["muted"])
    body.append(t)
    t, _ = sh.text("node corner = 기초 · 학부 · 대학원, the level the volume is written to",
                   NOTO_R, "nr", 11, GUT, fy + 18, T["muted"])
    body.append(t)
    t, _ = sh.text("github.com/voidmain443", MONO_R, "mr", 10.5, W - PAD_R, fy, T["muted"],
                   anchor="end", tracking=0.4)
    body.append(t)

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" '
        f'viewBox="0 0 {W} {H:.0f}" role="img" '
        f'aria-label="Prerequisite map across Mathematics, Economics, Network Science and AI">'
        + sh.defs_block() + "".join(body) + "</svg>"
    )
    return svg


def audit():
    """Structural checks: unique codes, edges pointing forward, no orphan stages."""
    stage = {}
    for _, _, courses in LANES:
        for code, en, ko, s, status, level in courses:
            if code in stage:
                raise ValueError(f"duplicate course code: {code}")
            stage[code] = s
    problems = []
    for a, b in EDGES + CROSS:
        if a not in stage or b not in stage:
            problems.append(f"unknown course in edge {a} -> {b}")
        elif stage[a] >= stage[b]:
            problems.append(f"edge does not move right: {a}(s{stage[a]}) -> {b}(s{stage[b]})")
    return stage, problems


if __name__ == "__main__":
    import os
    import svgtext

    stage, problems = audit()
    for p in problems:
        print("PROBLEM:", p)
    counts = {}
    for _, _, courses in LANES:
        for c in courses:
            counts[c[4]] = counts.get(c[4], 0) + 1
    print(svgtext.describe())
    print(f"{len(stage)} courses  " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"{len(EDGES)} edges  {len(CROSS)} cross-department")

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "img")
    os.makedirs(out, exist_ok=True)
    for name in ("light", "dark"):
        svg = build(name)
        path = os.path.join(out, f"curriculum-{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"{path}  {len(svg)/1024:.1f} KB")
