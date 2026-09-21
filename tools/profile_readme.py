"""Generates the profile README drafts from the tables at the top of this file.

    cd tools
    python profile_readme.py            # -> ../drafts/README-A-gallery.md, ../drafts/README-F-journal.md
    python profile_readme.py --final A  # -> ../README.md from draft A (or F)

Adding a textbook is one row in BOOKS plus one capture in ../img/shots (see capture.py)
and one row in curriculum.py. Adding a project is one row in PROJ plus a GIF or JPEG.
Adding a journal entry is one row at the top of JOURNAL. Nothing else needs touching.

Link policy: repositories that are private are never linked, only their public Pages
site. Rethink is a blog, not a project; its engine is private and is not described here.
"""

import os
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- links
L = dict(
    linkedin="https://www.linkedin.com/in/junha-park-592630193/",
    x="https://x.com/voidmain443",
    mail="mailto:voidmain443@gmail.com",
    gh="https://github.com/voidmain443",
    rethink="https://voidmain443.github.io/github_blog_engine/",
    rethink_post="https://voidmain443.github.io/github_blog_engine/posts/2026-09-yield-curve/index.html",
    awesome="https://github.com/voidmain443/awesome-economic",
)

# ---------------------------------------------------------------- blog (top card; the engine itself is private)
BLOG = dict(
    name="Rethink", tagline="숫자로 재고, 역사에 놓고, 다시 생각한다.",
    desc="경제학과 세상을 잇는 글을 써 보는 시도입니다. 현안을 데이터로 읽고, 역사와 경제학의 눈으로 다시 생각해 봅니다.",
    img="img/shots/rethink-card.jpg",
)

# ---------------------------------------------------------------- projects (public material only)
PROJ = [
    dict(gif="img/shots/econmap.gif", url="https://voidmain443.github.io/econometrics-map/",
         title="Econometrics Archive", ko="교과서 뒤의 논문들",
         desc="교과서의 모든 방법은 논문에서 왔다. 10권 · 189장을 그 뒤의 논문 298편과 793개 링크로 잇고, 11개 계보 띠 위에 200년의 지도로 그렸다. 정본 논문 48편은 금테.",
         links=[("지도", "https://voidmain443.github.io/econometrics-map/map.html"),
                ("타임라인", "https://voidmain443.github.io/econometrics-map/timeline.html"),
                ("교과서에서 시작", "https://voidmain443.github.io/econometrics-map/textbooks.html")],
         tech=[("Python", "python", "3776AB"), ("Obsidian vault", "obsidian", "7C3AED"), ("GitHub Pages", "githubpages", "222222")]),
    dict(gif="img/shots/overleaf.gif", url="https://github.com/voidmain443/overleaf_study_guide",
         title="Overleaf와 LaTeX으로 경제학 논문 쓰기", ko="서지에서 투고까지",
         desc="빈 파일에서 투고 패키지까지, 학술지 서식으로 조판된 22쪽 논문 한 편을 끝까지 만든다. 교안 39쪽 · 슬라이드 116장 · 시작 프로젝트 · 완성 원고 · 장별 스냅샷 12개.",
         links=[("저장소", "https://github.com/voidmain443/overleaf_study_guide"),
                ("교안 PDF", "https://github.com/voidmain443/overleaf_study_guide/blob/main/guide/latex-paper-guide.pdf"),
                ("시작 프로젝트", "https://github.com/voidmain443/overleaf_study_guide/tree/main/starter")],
         tech=[("LaTeX", "latex", "008080"), ("Overleaf", "overleaf", "47A141"), ("v01", None, "2f6f4f")]),
]
TOOLS = [  # (label, message, color, logo, url, description)
    ("Oracle 26ai", "dataset generator", "F80000", "oracle", "https://github.com/voidmain443/oracle_db_tutorial",
     "SQLP 실습용 이커머스 데이터셋 생성기. HR 실습 이후에 쓰는 규모의 표와 인덱스 실험 데이터."),
    ("TDF crawler", "KOFIA → SQLite", "003B57", "sqlite", "https://github.com/voidmain443/TDF_project_AX_P",
     "국내 타깃데이트펀드의 기준가 · 설정액 · 자금 유출입을 매일 수집하는 멱등 크롤러. 역할별 문서와 팀 학습 트랙."),
    ("Git & GitHub", "for project managers", "F05032", "git", "https://github.com/voidmain443/git-github_for_PM_Tutorial_docs",
     "비개발 팀을 Git 과 프로젝트 도구 위에 세우는 튜토리얼. PMI 스터디 그룹 교재로 제작 중."),
]

# ---------------------------------------------------------------- textbooks by department
DEPT = {
    "MATH": dict(ko="수학", color="2f6f4f", blurb="증명 수준의 기초. 나머지 셋이 그 위에 선다."),
    "ECON": dict(ko="경제학", color="1a4f7a", blurb="원론에서 계산경제학과 네트워크경제학까지."),
    "NETS": dict(ko="네트워크 과학", color="5f4b8b", blurb="네트워크의 통계물리와 수학. 제 연구가 있는 자리."),
    "AI":   dict(ko="인공지능", color="8a5622", blurb="데이터 기초에서 그래프 신경망까지. 넷이 모이는 곳."),
}
# status: pub | wip | plan.  url None = private, no site yet.  shot/cover = file stems under img/.
BOOKS = [
    dict(dept="MATH", code="MATH 100", cover="premath", shot="premath", url="https://voidmain443.github.io/pre_math_lecture_jupyter/intro.html",
         ko="수학 재건", en="Foundations before Calculus", shape="43 chapters · 4 parts", status="pub",
         line="arithmetic, algebra and single-variable calculus rebuilt out of a 36-week study group; every chapter carries the errors people actually made."),
    dict(dept="MATH", code="MATH 150", cover="proof", shot="proof", url="https://voidmain443.github.io/pre_book_of_proof/intro.html",
         ko="차근히 시작하는 증명법", en="Where Proof Begins", shape="90 weeks · 3 stages", status="pub",
         line="logic, sets, induction and the standard strategies, worked slowly enough that a first proof course stops being a wall: Hammack, then Solow, then Chartrand."),
    dict(dept="MATH", code="MATH 101", cover="calculus", shot="calculus", url="https://voidmain443.github.io/Calculus_apostol_jupyterbook/intro.html",
         ko="미적분학 79회", en="Calculus, after Apostol", shape="79 sessions · 6 parts", status="wip",
         line="integration before differentiation, aimed the whole way at ∫<sub>Ω</sub> dω = ∫<sub>∂Ω</sub> ω."),
    dict(dept="MATH", code="MATH 110", cover="linalg", shot="linalg", url="https://voidmain443.github.io/linear_algebra_gilbert/",
         ko="선형대수 — 서술과 파이썬 구현", en="Linear Algebra, 18.06 rebuilt", shape="34 lectures · 9 acts", status="pub",
         line="each lecture split into a written argument and a NumPy notebook, with a fixed colour convention for domain, codomain, error and subspace."),
    dict(dept="MATH", code="MATH 211", cover="linalg2", shot="lafb", url="https://voidmain443.github.io/linear_algebra_foundation_book/",
         ko="선형대수학, 다시 그리고 깊게", en="Linear Algebra, Again and Deeper", shape="60 chapters · 9 parts · 45 weeks", status="wip",
         line="the sequel to 18.06: matrices demoted to coordinate representations, a numerical footnote on every theory chapter, econometrics recovered as projection in Part VI."),
    dict(dept="ECON", code="ECON 100", cover="econpy", shot="econpy", url="https://voidmain443.github.io/ECONO_000/",
         ko="경제학과 1학년을 위한 파이썬 (2판)", en="Python for Economists", shape="8 weeks · 11 chapters", status="pub",
         line="from variables and loops to supply-and-demand models in Matplotlib; second edition rewritten from a semester of student feedback."),
    dict(dept="ECON", code="ECON 101", cover="econ101", shot="econ101", url="https://voidmain443.github.io/economic_principle_book/",
         ko="경제학원론", en="Principles of Economics", shape="15 chapters · 4 parts", status="pub",
         line="taught against open data (Maddison, World Bank, OWID, Penn World Table) instead of drawn diagrams."),
    dict(dept="ECON", code="ECON 510", cover="eqdiary", shot="eqdiary-w04", url="https://voidmain443.github.io/Equation_diary/",
         ko="식 일기", en="Understanding World on Equation", shape="24 weeks · 3 parts", status="wip",
         line="a math camp on reading, not solving: what each symbol names, which assumption each line leans on, where undergraduate and graduate readings part ways."),
    dict(dept="NETS", code="NETS 301", cover=None, shot=None, url=None,
         ko="네트워크 과학의 수학", en="Mathematics of Network Science", shape="64-page manuscript", status="wip",
         line="the bridge from economics toward AI; graphs, measures, random graphs and the statistical physics behind them."),
    dict(dept="AI", code="AI 105", cover="builddb", shot="bdb", url="https://voidmain443.github.io/building_database/",
         ko="Oracle 을 파이썬으로 처음부터 만들며 이해하기", en="Build a Database", shape="19 units · 3 volumes · 10,980 lines", status="pub",
         line="a learner who only knows <code>SELECT</code> builds Oracle's storage and instance structure one line at a time, up to crash recovery and row locks."),
    dict(dept="AI", code="AI 100", cover=None, shot=None, url=None,
         ko="SQLP 합격에서 Hero까지", en="SQL deepdive", shape="8 weeks · 1,100+ items · 12 lectures", status="wip",
         line="exam preparation, then the principles behind execution plans, then a performance lab on Oracle 23ai."),
    dict(dept="AI", code="AI 110", cover=None, shot=None, url=None,
         ko="ADP 실습 교재", en="Data Analysis with pandas", shape="5 projects · 69 notebooks · 105 problems", status="wip",
         line="read, analyse and report: access audits, ledger reconciliation, checkout funnels, return distributions, delivery sampling."),
    dict(dept="AI", code="AI 200", cover=None, shot=None, url="https://github.com/voidmain443/8week_AI_with_GeminiAPI",
         ko="8주 생성형 AI 집중 과정", en="Generative AI, local edition", shape="8 weeks · Gemini API", status="pub",
         line="Google × Kaggle's intensives redesigned as eight Thursday sessions: prompting, embeddings, RAG, function calling, agents, fine-tuning, MLOps."),
]
PLANNED = {
    "MATH": "MATH 120 확률통계 · MATH 201 해석학 (◐) · MATH 210 미분방정식 · MATH 220 다변수해석 · MATH 230 이산·조합론 · MATH 240 수치해석 · MATH 260 최적화 · MATH 301 측도·확률론 · MATH 310 확률과정 · MATH 320 함수해석 · MATH 330 통계적 추론",
    "ECON": "ECON 201 미시 · ECON 202 거시 · ECON 301 계량 · ECON 311 게임이론 · ECON 320 산업조직 · ECON 401 시계열 · ECON 520 수리경제 · ECON 601/602 미시·거시이론 · ECON 610 계량이론 · ECON 620 계산경제학 · ECON 630 금융경제학",
    "NETS": "NETS 201 네트워크 기초 · NETS 310 통계물리 · NETS 320 랜덤그래프 · NETS 330 네트워크 동역학 · NETS 410 네트워크경제학 · NETS 510 복잡계 · NETS 520 경제물리학 · NETS 530 네트워크 추론",
    "AI": "AI 301 머신러닝 · AI 310 딥러닝 · AI 410 그래프 신경망 · AI 501 통계적 학습이론 · AI 520 강화학습 · AI 530 인과추론",
}
# figures pulled from the books themselves (img/figs); (file, link, dept code, caption)
FIGS = [
    ("lafb-filters", "https://voidmain443.github.io/linear_algebra_foundation_book/book/p4-part-iv-linear-algebra-on-a/n4-the-numerics-of-least-squares-and.html", "MATH 211", "작은 특잇값을 얼마나 남기는가: ridge · TSVD · Landweber"),
    ("calc-riemann", "https://voidmain443.github.io/Calculus_apostol_jupyterbook/part1/L07_lab.html", "MATH 101", "하합과 상합이 b³/3 으로 조여드는 과정, n = 4 · 10 · 40"),
    ("linalg-det", "https://voidmain443.github.io/linear_algebra_gilbert/l18-lab", "MATH 110", "행렬식은 넓이이고 부호는 방향이다"),
    ("eqdiary-envelope", "https://voidmain443.github.io/Equation_diary/w05-envelope", "ECON 510", "포락선 정리: 가치함수는 직선들의 상포락선이다"),
    ("econ101-gdp-co2", "https://voidmain443.github.io/economic_principle_book/chapter10", "ECON 101", "1인당 GDP 와 1인당 CO₂, 로그–로그"),
    ("bdb-structure", "https://voidmain443.github.io/building_database/#/map", "AI 105", "인스턴스와 데이터베이스, 상자마다 그것을 만드는 단원"),
]

# ---------------------------------------------------------------- archives: reading lists only (not textbooks, not projects)
ARCH = [  # (simpleicons slug, colour, url, title, description html)
    ("awesomelists", "fc60a8", L["awesome"], "Awesome Economics",
     "an annotated map of academic economics: what to read for each field, in what order, and what each book is bad at. Micro from Varian to MWG and where Kreps patches it; econometrics split between estimator theory and design-based causal inference.<br/><sub>학술 경제학 자료를 \"왜 이 자료인가\"와 함께 정리한 목록</sub>"),
    ("databricks", "FF3621", L["awesome"] + "/tree/main/database", "Databases and panels",
     "PSID, NLSY, HRS, SIPP and Add Health each written up in full, mapped onto their Korean counterparts (KLIPS, KOWEPS, KLoSA, 가계금융복지조사).<br/><sub>미시 패널 데이터 접근 경로와 설계 철학</sub>"),
    ("bookstack", "0288D1", L["awesome"] + "/blob/main/01.Methodenstreit.md", "Debates in the history of thought",
     " · ".join(f'<a href="{L["awesome"]}/blob/main/{f}">{t}</a>' for f, t in [
         ("01.Methodenstreit.md", "Methodenstreit"), ("02.Socialist_Calculation_Debate.md", "Socialist Calculation"),
         ("03.Keynes_vs_Hayek.md", "Keynes vs Hayek"), ("04.Cambridge%20Capital%20Controversy.md", "Cambridge Capital Controversy"),
         ("05.Friedman_LUcas.md", "Friedman and Lucas"), ("06.Stimulus_and_Austerity.md", "Stimulus and Austerity"), ("07.Mark_Blaug.md", "Mark Blaug")])),
    ("jupyter", "F37626", "https://voidmain443.github.io/Reasearch_A/", "사회과학을 위한 파이썬 통계 분석",
     "statistics with Python for social science majors, 2023.<br/><sub>학습자료 제작 중단 · 보관용</sub>"),
]

WORKSHOP = [
    "**학부연구생을 위한 데이터분석 3달 과정** — 범죄수사 시나리오로 한 줄씩 점증하는 형식으로 전면 개정 중.",
    "**Mini-Bloomberg로 배우는 Python for Engineering** — 20주, 매주 산출물이 `mbg.*` 라이브러리로 쌓인다.",
    "**「차근히 시작하는 증명법」 LaTeX 판** — 1권 50주를 한 권(약 420쪽)으로 엮은 인쇄본 소스.",
    "**KIS · Knowledge Information System** — 경제·정책 분석가의 정보원 928건 카탈로그와 수집 설계.",
]

# newest first; (date, image, html)
JOURNAL = [
    ("2026-09-21", "img/shots/overleaf.gif", '<b><a href="https://github.com/voidmain443/overleaf_study_guide">Overleaf와 LaTeX으로 경제학 논문 쓰기</a></b> v01 완성 — 교안 39쪽, 슬라이드 116장, 시작 프로젝트와 완성 원고, 장별 스냅샷 12개.'),
    ("2026-09-21", "img/shots/lafb.gif", '<b><a href="https://voidmain443.github.io/linear_algebra_foundation_book/">선형대수학, 다시 그리고 깊게</a></b> <sub><code>MATH 211</code></sub> — 60장 사이트 배포, 주차별 제작 설계서 45개. 계속 집필 중.'),
    ("2026-09-21", "img/shots/bdb.jpg", '<b><a href="https://voidmain443.github.io/building_database/">Oracle 을 파이썬으로 처음부터 만들며 이해하기</a></b> <sub><code>AI 105</code></sub> — 19단원 릴레이 완성, 누적 테스트 99개 통과, 인터랙티브 책 배포.'),
    ("2026-09-18", "img/shots/econmap.jpg", '<b><a href="https://voidmain443.github.io/econometrics-map/">Econometrics Archive</a></b> — 논문 298편 · 교과서 10권 · 793개 링크의 지도와 타임라인 배포.'),
    ("2026-09-18", "img/shots/eqdiary-w04.jpg", '<b><a href="https://voidmain443.github.io/Equation_diary/">식 일기 · Understanding World on Equation</a></b> <sub><code>ECON 510</code></sub> — 1부 회차와 실습 노트북 공개, 부록(기호 대장 · 간극 21항목) 갱신.'),
    ("2026-09-10", "img/shots/rethink-post.jpg", f'<b><a href="{L["rethink"]}">Rethink</a></b> 블로그 열기 — 경제학과 세상을 잇는 글을 써 보는 시도.'),
    ("2026-09-02", "img/shots/calculus.jpg", '<b><a href="https://voidmain443.github.io/Calculus_apostol_jupyterbook/intro.html">미적분학 79회</a></b> <sub><code>MATH 101</code></sub> — 재배포. 지도 A(두 개의 무한 연산)와 집필 진행표 추가.'),
    ("2026-08-28", "img/shots/proof.jpg", '<b><a href="https://voidmain443.github.io/pre_book_of_proof/intro.html">차근히 시작하는 증명법</a></b> <sub><code>MATH 150</code></sub> — 90주 3단계 구성으로 사이트 배포. 인쇄용 LaTeX 판은 별도 제작 중.'),
    ("2026-08-26", "img/shots/linalg.jpg", '<b><a href="https://voidmain443.github.io/pre_math_lecture_jupyter/intro.html">수학 재건</a></b> <sub><code>MATH 100</code></sub> 과 <b><a href="https://voidmain443.github.io/linear_algebra_gilbert/">선형대수 — 서술과 파이썬 구현</a></b> <sub><code>MATH 110</code></sub> 배포.'),
    ("2026-07-30", "img/shots/econpy.jpg", '<b><a href="https://voidmain443.github.io/ECONO_000/">경제학과 1학년을 위한 파이썬</a></b> <sub><code>ECON 100</code></sub> 2판 — 한 학기 피드백을 반영해 강의록을 교재로 다시 씀.'),
]
JOURNAL_VISIBLE = 6   # rows shown open; the rest fold into <details>

# ================================================================ rendering helpers
def _s(t):
    return quote(t.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="")

def badge(label, msg, color, logo=None, style="flat-square"):
    url = f"https://img.shields.io/badge/{_s(label)}-{_s(msg)}-{color}?style={style}"
    return url + (f"&logo={logo}&logoColor=white" if logo else "")

def badge1(msg, color, logo=None, style="flat-square"):
    url = f"https://img.shields.io/badge/{_s(msg)}-{color}?style={style}"
    return url + (f"&logo={logo}&logoColor=white" if logo else "")

def ib(href, label, msg, color, logo=None, alt=None):
    return f'<a href="{href}"><img src="{badge(label, msg, color, logo)}" alt="{alt or (label + " · " + msg)}"/></a>'

def icon(slug, color, size=22):
    return f'<img src="https://cdn.simpleicons.org/{slug}/{color}" width="{size}" height="{size}" alt=""/>'

ST = {"pub": "●", "wip": "◐", "plan": "○"}
ST_WORD = {"pub": "published · 게시됨", "wip": "in progress · 제작 중", "plan": "planned · 예정"}

# ---------------------------------------------------------------- blocks
def header():
    return f"""<div align="center">
  <img src="https://avatars.githubusercontent.com/u/83549147?v=4" width="104" height="104" alt="Junha Park"/>
  <h2>Junha Park · 박준하</h2>
  <p>
    {ib(L['linkedin'], 'LinkedIn', 'junha-park', '0A66C2', 'linkedin')}
    {ib(L['x'], 'X', '@voidmain443', '000000', 'x')}
    {ib(L['mail'], 'Mail', 'voidmain443', 'EA4335', 'gmail')}
  </p>
</div>

<table align="center">
<tr>
<td width="280"><a href="{L['rethink']}"><img src="{BLOG['img']}" width="280" alt="{BLOG['name']} blog"/></a></td>
<td valign="middle">
<b><a href="{L['rethink']}">{BLOG['name']}</a></b> — {BLOG['tagline']}<br/>
<sub>{BLOG['desc']}</sub>
</td>
</tr>
</table>

<p align="center"><sub><a href="#projects">Projects · 프로젝트</a> &nbsp;·&nbsp; <a href="#books">Textbooks · 교재</a> &nbsp;·&nbsp; <a href="#archives">Archives · 아카이브</a> &nbsp;·&nbsp; <a href="#contact">Contact · 연락</a></sub></p>
"""

INTRO = f"""
Learning and DEV journey, 공부할 교재들과 부족했던 부분들을 과외하면서 일부만 빼서 경제학공부에 도움이 될 만한 부분들을 정리한 깃허브입니다. 다른 백앤드와 APP개발등등을 해오면서 필요했고 좀더 깊게 이해한 내용들의 일부만 이곳에 아카이빙합니다.

경제학을 공부하면서 궁금했던 식, 세상, 모델링 등을 계량경제학과 생산자 추정 모형등에 관심이 많았고, 세상을 일반적인 사회과학보다는 자연법칙 내에서의 제약으로 다루고싶습니다. 일반적인 사회과학내의 경제학이 아닌 게임이론 속에서 인간의 선택이 더 나은 공간이길 바라며 자유시장이 좀더 오래지속하길 바라는 마음으로 공부를 지속합니다.

수학에서의 "공간"의 개념을 좋아하고, 물리학에서 "측정"과 "측도"로 경제적 질문에 대답하고 논의하는 걸 좋아합니다. 다학제적 관점에서 접근하고 바라보는것이 현재의 "탐험"입니다.

-장막속에서 길을 그리며-

<sub>커피챗 좋아합니다. 위의 프로필 링크로 연락주시면 공동연구 및 업무등에 있어서 논의하면 재미있을 것 같습니다.</sub>
"""

TOUR = """
<p align="center"><a href="#books"><img src="img/shots/tour.gif" width="100%" alt="Five of the published sites, in turn"/></a></p>
<p align="center"><sub>생성물 일부 · some of the things built</sub></p>
"""

def proj_card(p):
    tech = " ".join(f'<img src="{badge1(t[0], t[2], t[1])}" alt="{t[0]}"/>' for t in p["tech"])
    links = " · ".join(f'<a href="{u}">{n}</a>' for n, u in p["links"])
    return (f'<a href="{p["url"]}"><img src="{p["gif"]}" alt="{p["title"]}"/></a>\n'
            f'<h4><a href="{p["url"]}">{p["title"]}</a> <sub>{p["ko"]}</sub></h4>\n'
            f'<p>{p["desc"]}</p>\n<p><sub>{links}</sub><br/>{tech}</p>')

def tools_list():
    return "\n".join(f'- {ib(u, lab, msg, col, logo)} — {d}' for lab, msg, col, logo, u, d in TOOLS) + "\n"

def projects(compact=False):
    head = """
<a id="projects"></a>

## Projects · 프로젝트

사람들에게 도움될 만한 자료를 만들어보고 있습니다. 참고하시면 좋겠습니다.
"""
    if compact:
        cells = "".join(f'<td width="50%" valign="top"><a href="{p["url"]}"><img src="{p["gif"]}" alt="{p["title"]}"/></a><br/><b><a href="{p["url"]}">{p["title"]}</a></b> <sub>{p["ko"]}</sub><br/><sub>{" · ".join(f"<a href={chr(39)}{u}{chr(39)}>{n}</a>" for n, u in p["links"])}</sub></td>' for p in PROJ)
        return head + f"\n<table>\n<tr>\n{cells}\n</tr>\n</table>\n\n<h4>Smaller tools · 작은 도구들</h4>\n\n" + tools_list()
    cells = "".join(f'<td width="50%" valign="top">{proj_card(p)}</td>\n' for p in PROJ)
    return head + f"\n<table>\n<tr>\n{cells}</tr>\n</table>\n\n<h4>Smaller tools · 작은 도구들</h4>\n\n" + tools_list()

ROADMAP = """
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="img/curriculum-dark.svg">
    <img src="img/curriculum-light.svg" width="100%" alt="Prerequisite map across Mathematics, Economics, Network Science and Artificial Intelligence"/>
  </picture>
</p>
<p align="center"><sub>● published 게시됨 &nbsp; ◐ in progress 제작 중 &nbsp; ○ planned 예정 &nbsp;&nbsp;|&nbsp;&nbsp; 왼쪽에서 오른쪽이 선수 관계, 점선은 학과를 건너는 선수과목</sub></p>
"""

SOURCE_NOTE = f"""
> **원고가 필요하신가요?** 교재의 원고 저장소(노트북 · LaTeX · 그림 코드)는 비공개입니다. 강의나 스터디에 쓰고 싶으시면 {ib(L['mail'], 'Mail', '초대 요청', 'EA4335', 'gmail', alt='메일로 초대 요청')} 으로 연락 주세요. 저장소에 협업자로 초대해 드립니다. 사이트는 누구나 읽을 수 있습니다.
"""

def dept_head(d):
    D = DEPT[d]
    return f'<h3><img src="{badge(d, D["ko"], D["color"])}" alt="{d} · {D["ko"]}"/> &nbsp;{D["ko"]} <sub>{D["blurb"]}</sub></h3>\n'

def book_cell(b):
    if b["shot"]:
        img = f'<a href="{b["url"]}"><img src="img/shots/{b["shot"]}.jpg" alt="{b["ko"]} 사이트"/></a><br/>'
    else:
        img = f'<img src="{badge1(ST_WORD[b["status"]].split(" · ")[0], "9aa4ad" if b["status"] == "plan" else "b08800")}" alt="{ST_WORD[b["status"]]}"/><br/>'
    title = f'<b><a href="{b["url"]}">{b["ko"]}</a></b>' if b["url"] else f'<b>{b["ko"]}</b>'
    return f'{img}{title} <sub><code>{b["code"]}</code> {ST[b["status"]]}</sub><br/><sub>{b["en"]} · {b["shape"]}</sub>'

MAX_CARDS = 4   # per department; the rest of the department is listed in one line each

def dept_cards(d, per_row=2):
    bs = [b for b in BOOKS if b["dept"] == d]
    cards, rest = bs[:MAX_CARDS], bs[MAX_CARDS:]
    rows = []
    for i in range(0, len(cards), per_row):
        cells = "".join(f'<td width="{100 // per_row}%" valign="top">{book_cell(b)}</td>' for b in cards[i:i + per_row])
        rows.append(f"<tr>{cells}</tr>")
    out = "<table>\n" + "\n".join(rows) + "\n</table>\n"
    for b in rest:
        name = f'**[{b["ko"]} · {b["en"]}]({b["url"]})**' if b["url"] else f'**{b["ko"]} · {b["en"]}**'
        out += f'- {name} — {b["line"]}<br/><sub>`{b["code"]}` · {b["shape"]} · {ST[b["status"]]}</sub>\n'
    return out

def dept_covers(d):
    bs = [b for b in BOOKS if b["dept"] == d and b["cover"]]
    if not bs:
        return ""
    return '<p align="center">' + " ".join(f'<a href="{b["url"]}"><img src="img/cover-{b["cover"]}.svg" width="15%" alt="{b["ko"]}"/></a>' for b in bs) + "</p>\n"

def dept_lines(d):
    out = []
    for b in [b for b in BOOKS if b["dept"] == d]:
        name = f'**[{b["ko"]} · {b["en"]}]({b["url"]})**' if b["url"] else f'**{b["ko"]} · {b["en"]}**'
        out.append(f'- {name} — {b["line"]}<br/><sub>`{b["code"]}` · {b["shape"]} · {ST[b["status"]]}</sub>')
    return "\n".join(out) + "\n"

def dept_plan(d):
    return f'<details><summary><sub>전체 계획 · planned volumes in {d}</sub></summary><br/><sub>{PLANNED[d]}</sub></details>\n'

def figures():
    cells = []
    for f, u, code, cap in FIGS:
        cells.append(f'<td width="33%" valign="top"><a href="{u}"><img src="img/figs/{f}.png" alt="{cap}"/></a><br/><sub><code>{code}</code> · {cap}</sub></td>')
    return ("<h3>Figures · 책 속의 그림</h3>\n<p><sub>교재는 그림을 그리는 코드까지 싣습니다. 여섯 권에서 한 장씩. 그림을 누르면 그 장으로 갑니다.</sub></p>\n<table>\n<tr>"
            + "".join(cells[:3]) + "</tr>\n<tr>" + "".join(cells[3:]) + "</tr>\n</table>\n")

def textbooks(style):
    parts = ["""
<a id="books"></a>

## Textbooks · 교재

네 학과로 나누어 씁니다. 지도가 먼저, 그다음 학과별로. 완성되는 순서대로 카드가 늘어나고, 예정된 권은 지도와 접힌 목록에 있습니다.
""", ROADMAP, SOURCE_NOTE]
    if style == "cards":
        parts.append(figures())
    for d in ["MATH", "ECON", "NETS", "AI"]:
        parts.append(dept_head(d))
        if style == "cards":
            parts.append(dept_cards(d))
        else:
            parts.append(dept_covers(d))
            parts.append(dept_lines(d))
        parts.append(dept_plan(d))
    return "\n".join(parts)

def archives(style):
    head = "\n<a id=\"archives\"></a>\n\n## Archives & reading lists · 아카이브\n\n교재도 프로젝트도 아닌 것. 읽을 목록과 보관 자료.\n\n"
    if style == "table":
        rows = "\n".join(f'<tr><td align="center" width="44"><a href="{u}">{icon(slug, col)}</a></td><td><b><a href="{u}">{t}</a></b><br/>{d}</td></tr>' for slug, col, u, t, d in ARCH)
        return head + f"<table>\n{rows}\n</table>\n"
    return head + "\n".join(f'- <a href="{u}"><img src="{badge1(t, col, slug)}" alt="{t}"/></a> — {d}' for slug, col, u, t, d in ARCH) + "\n"

def workshop():
    return "\n## Workshop · 비공개 제작 중\n\n공개 전 단계의 원고들. 링크는 없고, 완성되면 위 학과 카드에 올라갑니다.\n\n" + "\n".join(f"- {w}" for w in WORKSHOP) + "\n"

CONTACT = f"""
<a id="contact"></a>

## Contact · 연락

Open to collaboration on network analysis and computational economics — [voidmain443@gmail.com]({L['mail']}). 교재 원고 저장소 초대 요청도 같은 주소로.

<sub>네트워크 분석·계산경제학 협업 환영. 비공개로 제작 중인 원고(학부연구생 데이터분석 과정, Mini-Bloomberg Python, 증명법 LaTeX 판, KIS)는 협업 문의로 열어 드립니다.</sub>
"""

def journal():
    def row(date, img, html):
        return f'<tr><td width="200" valign="top"><img src="{img}" alt=""/></td><td valign="top"><sub>{date}</sub><br/>{html}</td></tr>'
    rows = [row(*e) for e in JOURNAL]
    open_rows = "\n".join(rows[:JOURNAL_VISIBLE])
    more = ""
    if len(rows) > JOURNAL_VISIBLE:
        more = f'\n<details><summary><sub>이전 항목 {len(rows) - JOURNAL_VISIBLE}개 · earlier</sub></summary>\n<table>\n' + "\n".join(rows[JOURNAL_VISIBLE:]) + "\n</table>\n</details>\n"
    return f"""
## Last 60 days · 최근 60일

날짜는 마지막 배포 기준입니다. 새 항목이 위에 붙습니다.

<table>
{open_rows}
</table>
{more}"""

# ================================================================ drafts
def draft_A():
    return header() + INTRO + TOUR + projects() + textbooks("cards") + archives("table") + workshop() + CONTACT

def draft_F():
    return header() + INTRO + journal() + projects(compact=True) + textbooks("covers") + archives("badges") + workshop() + CONTACT

def draft_M():
    """A from the top down to the roadmap, F from the roadmap down."""
    return header() + INTRO + TOUR + projects() + textbooks("covers") + archives("badges") + CONTACT

DRAFTS = {"M": ("README-merged.md", draft_M), "A": ("README-A-gallery.md", draft_A), "F": ("README-F-journal.md", draft_F)}

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--final":
        name, fn = DRAFTS[sys.argv[2].upper()]
        p = os.path.join(ROOT, "README.md")
        open(p, "w", encoding="utf-8", newline="\n").write(fn().lstrip("\n"))
        print(p)
    else:
        out = os.path.join(ROOT, "drafts")
        os.makedirs(out, exist_ok=True)
        for key, (name, fn) in DRAFTS.items():
            p = os.path.join(out, name)
            txt = fn().lstrip("\n")
            open(p, "w", encoding="utf-8", newline="\n").write(txt)
            print(p, f"{len(txt) / 1024:.1f} KB")
