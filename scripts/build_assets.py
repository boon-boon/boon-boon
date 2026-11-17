#!/usr/bin/env python3
"""Generates every image the profile README uses, in a dark and a light variant.

    python3 scripts/build_assets.py

Edit the content at the bottom of this file, run it, commit assets/.
Only system fonts are used, because an SVG shown through <img> cannot load web fonts.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(bg="#0e0e13", panel="#15151c", line="#2b2b38", text="#f0efe9",
                 muted="#9494a8", dim="#55556a", accent="#ffb454", mint="#7fd1c1",
                 on_accent="#0e0e13"),
    "light": dict(bg="#ffffff", panel="#f5f5f8", line="#d9d9e2", text="#16161d",
                  muted="#5f5f72", dim="#a3a3b3", accent="#a85f00", mint="#0f7f6c",
                  on_accent="#ffffff"),
}

MONO = "ui-monospace,SFMono-Regular,'SF Mono','Cascadia Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def t(x, y, s, size, fill, font=MONO, weight=400, anchor="start", spacing=0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{ls}>{escape(s)}</text>')


def rect(x, y, w, h, fill="none", stroke="none", r=0, sw=1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, stroke, sw=1.5):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>'


def arrow(x1, y, x2, c):
    return line(x1, y, x2 - 2, y, c) + f'<path d="M{x2-8} {y-5} L{x2} {y} L{x2-8} {y+5}" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>\n')


def node(x, y, w, label, sub, c, hot=False):
    stroke = c["accent"] if hot else c["line"]
    return (rect(x, y, w, 44, c["panel"], stroke, 8, 1.5)
            + t(x + w / 2, y + 27, label, 14, c["accent"] if hot else c["text"], weight=600, anchor="middle")
            + t(x + w / 2, y + 68, sub, 13, c["muted"], anchor="middle"))


# ---------------------------------------------------------------- hero
def hero(c, d):
    W, H = 1200, 500
    b = rect(0.5, 0.5, W - 1, H - 1, c["bg"], c["line"], 14)
    # title bar
    b += "".join(f'<circle cx="{28 + i * 18}" cy="23" r="5" fill="{c["line"]}"/>' for i in range(3))
    b += t(96, 28, d["file"], 15, c["muted"])
    pw = len(d["status"]) * 8.4 + 44
    b += rect(W - 24 - pw, 9, pw, 28, "none", c["line"], 14)
    b += f'<circle cx="{W - 24 - pw + 18}" cy="23" r="4" fill="{c["mint"]}"/>'
    b += t(W - 24 - pw + 30, 28, d["status"], 14, c["text"])
    b += line(0, 46, W, 46, c["line"], 1)
    # gutter
    for n, y in enumerate((112, 196, 252, 296), 1):
        b += t(56, y, str(n), 14, c["dim"], anchor="end")
    b += line(74, 70, 74, 318, c["line"], 1)
    # code
    b += t(100, 112, "// " + d["comment"], 20, c["muted"])
    b += t(100, 204, d["name"], 80, c["text"], weight=800, spacing=-3)
    cx = 100 + len(d["name"]) * (80 * 0.6 - 3) + 14
    b += (f'<rect x="{cx}" y="144" width="18" height="66" fill="{c["accent"]}">'
          '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    b += (f'<text x="100" y="296" xml:space="preserve" font-family="{MONO}" font-size="20"><tspan fill="{c["mint"]}">rule</tspan>'
          f'<tspan fill="{c["muted"]}"> = </tspan><tspan fill="{c["accent"]}">"{escape(d["rule"])}"</tspan></text>')
    # statement, right column
    for i, s in enumerate(d["statement"]):
        b += t(800, 112 + i * 30, s, 20, c["text"] if i < 2 else c["muted"], font=SANS)
    # facts
    b += line(0, 340, W, 340, c["line"], 1)
    cw = W / len(d["facts"])
    for i, (label, value) in enumerate(d["facts"]):
        x = i * cw
        if i:
            b += line(x, 340, x, 456, c["line"], 1)
        b += t(x + 32, 374, label, 14, c["muted"], spacing=1)
        b += t(x + 32, 430, value, 40, c["text"], weight=700, spacing=-1)
    # status bar
    b += f'<path d="M0.5 456 H{W-0.5} V{H-14.5} a14 14 0 0 1 -14 14 H14.5 a14 14 0 0 1 -14 -14 Z" fill="{c["panel"]}" stroke="{c["line"]}"/>'
    x = 32
    for s in d["bar"]:
        b += t(x, 484, s, 15, c["muted"])
        x += len(s) * 9 + 32
    b += t(W - 32, 484, d["bar_right"], 15, c["muted"], anchor="end")
    return svg(W, H, b, f'{d["name"]}, {d["comment"]}. {d["status"]}.')


# ---------------------------------------------------------------- project cards
def card(c, p):
    W, H = 1200, 280
    b = rect(0.5, 0.5, W - 1, H - 1, c["panel"], c["line"], 14)
    b += t(48, 62, p["kicker"], 14, c["accent"], weight=600, spacing=2)
    b += t(48, 122, p["title"], 46, c["text"], font=SANS, weight=700, spacing=-1)
    for i, s in enumerate(p["tagline"]):
        b += t(48, 166 + i * 30, s, 21, c["muted"], font=SANS)
    b += t(48, 246, p["stack"], 15, c["muted"])
    b += rect(600, 28, 572, 224, c["bg"], c["line"], 10)
    b += f'<g transform="translate(600 28)">{p["diagram"](c)}</g>'
    return svg(W, H, b, f'{p["title"]}: {" ".join(p["tagline"])}')


def d_pipeline(c):
    b = t(20, 34, "cron  08:00 MYT  every day", 13, c["muted"])
    xs = [10, 154, 298, 442]
    data = [("Claude", "picks + writes", False), ("article JSON", "source of truth", True),
            ("Python", "templates HTML", False), ("GitHub Pages", "hosts", False)]
    for x, (l, s, hot) in zip(xs, data):
        b += node(x, 86, 120, l, s, c, hot)
    for x in xs[:-1]:
        b += arrow(x + 124, 108, x + 141, c["muted"])
    b += t(286, 200, "everything right of the JSON is rebuilt from it", 13, c["muted"], anchor="middle")
    return b


HAND = {  # 21 MediaPipe landmarks, laid out by hand
    0: (75, 165), 1: (50, 145), 2: (32, 122), 3: (22, 100), 4: (14, 82),
    5: (55, 95), 6: (50, 62), 7: (47, 42), 8: (45, 24),
    9: (75, 90), 10: (75, 54), 11: (75, 30), 12: (75, 10),
    13: (94, 95), 14: (98, 62), 15: (100, 42), 16: (101, 26),
    17: (110, 105), 18: (118, 80), 19: (122, 62), 20: (125, 48),
}
BONES = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12),
         (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (17, 18), (18, 19), (19, 20), (0, 17)]


def d_hand(c):
    ox, oy = 34, 22
    b = "".join(line(HAND[a][0] + ox, HAND[a][1] + oy, HAND[z][0] + ox, HAND[z][1] + oy, c["muted"], 1.5) for a, z in BONES)
    b += "".join(f'<circle cx="{x + ox}" cy="{y + oy}" r="4" fill="{c["accent"]}"/>' for x, y in HAND.values())
    b += t(104, 212, "MediaPipe: 21 landmarks", 13, c["muted"], anchor="middle")
    b += arrow(196, 112, 250, c["muted"])
    b += rect(262, 90, 112, 44, c["panel"], c["accent"], 8, 1.5) + t(318, 117, "no raw pixels", 13, c["accent"], weight=600, anchor="middle")
    for i, name in enumerate(("SVM", "MLP", "Random Forest")):
        y = 34 + i * 56
        b += f'<path d="M374 112 C398 112 394 {y + 22} 418 {y + 22}" fill="none" stroke="{c["muted"]}" stroke-width="1.5"/>'
        b += rect(418, y, 136, 44, c["panel"], c["line"], 8, 1.5) + t(486, y + 28, name, 14, c["text"], weight=600, anchor="middle")
    b += t(486, 212, "compared head to head", 13, c["muted"], anchor="middle")
    return b


def d_mvvm(c):
    b = t(20, 34, "MVVM", 13, c["muted"], spacing=1.5)
    xs = [30, 216, 402]
    data = [("View", "UI only", False), ("ViewModel", "holds state", True), ("Firebase", "realtime data", False)]
    for x, (l, s, hot) in zip(xs, data):
        b += node(x, 86, 140, l, s, c, hot)
    for x in xs[:-1]:
        b += arrow(x + 144, 100, x + 182, c["muted"])
        b += line(x + 148, 116, x + 182, 116, c["mint"]) + f'<path d="M{x+152} 111 L{x+144} 116 L{x+152} 121" fill="none" stroke="{c["mint"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    b += t(286, 200, "updates flow back to the UI as they happen", 13, c["muted"], anchor="middle")
    return b


def d_editor(c):
    b = rect(24, 24, 300, 176, c["panel"], c["line"], 8)
    b += line(24, 48, 324, 48, c["line"], 1) + line(96, 48, 96, 200, c["line"], 1)
    for i, w in enumerate((44, 36, 50, 30)):
        b += rect(36, 62 + i * 18, w, 6, c["line"], r=3)
    for i, (w, col) in enumerate(((120, "muted"), (170, "accent"), (90, "muted"), (150, "mint"), (110, "muted"))):
        b += rect(112 + (16 if i in (1, 2, 3) else 0), 64 + i * 20, w, 6, c[col], r=3)
    b += rect(118, 150, 190, 36, c["bg"], c["accent"], 8, 1.5) + t(132, 173, "Ctrl+K  go to file", 13, c["text"])
    b += t(352, 44, ":root { --tokens }", 13, c["muted"])
    for i, col in enumerate((c["accent"], c["mint"], c["muted"], c["text"])):
        b += rect(352 + i * 50, 62, 38, 38, col, r=8)
    b += t(352, 130, "4 themes, 1 block each", 13, c["text"], weight=600)
    b += t(352, 156, "no framework", 13, c["muted"]) + t(352, 178, "no build step", 13, c["muted"])
    return b


# ---------------------------------------------------------------- small pieces
def button(c, label, primary):
    w = int(len(label) * 9.2 + 44)
    if primary:
        b = rect(0, 0, w, 40, c["accent"], r=20) + t(w / 2, 26, label, 15, c["on_accent"], weight=700, anchor="middle")
    else:
        b = rect(0.75, 0.75, w - 1.5, 38.5, c["bg"], c["line"], 19.25, 1.5) + t(w / 2, 26, label, 15, c["text"], weight=600, anchor="middle")
    return svg(w, 40, b, label)


def contact(c, d):
    W, H = 1200, 180
    b = rect(0.5, 0.5, W - 1, H - 1, c["panel"], c["line"], 14)
    b += f'<circle cx="54" cy="58" r="5" fill="{c["mint"]}"/>' + t(70, 63, d["kicker"], 14, c["muted"], spacing=2)
    b += t(48, 126, d["headline"], 46, c["text"], font=SANS, weight=700, spacing=-1)
    w = len(d["email"]) * 10.8 + 56
    b += rect(W - 48 - w, 62, w, 56, c["accent"], r=28) + t(W - 48 - w / 2, 97, d["email"], 18, c["on_accent"], weight=700, anchor="middle")
    return svg(W, H, b, f'{d["headline"]} {d["email"]}')


# ---------------------------------------------------------------- content
HERO = dict(
    file="boon-boon / README.md",
    status="open to internships",
    comment="software engineer in the making",
    name="Lee Boon Yew",
    rule="Keep the source of truth small. Generate the rest.",
    statement=["Android in Kotlin and Firebase.", "Algorithms in Java and C++.", "Lately: AI agents and", "computer vision."],
    facts=[("CGPA", "3.80"), ("PROJECTS BELOW", "6"), ("LIVE RIGHT NOW", "3"), ("BLOG REBUILDS ITSELF", "08:00 MYT")],
    bar=["main", "0 problems", "UTF-8", "Kotlin"],
    bar_right="Degree in Software Engineering @ TAR UMT",
)

PROJECTS = {
    "daily-tech-pulse": dict(kicker="NEWS BLOG · AUTOMATED · LIVE", title="Daily Tech Pulse",
                             tagline=["A blog nobody types. It publishes itself", "every morning."],
                             stack="TypeScript · Python · Claude · GitHub Pages", diagram=d_pipeline),
    "msl-recognition": dict(kicker="MACHINE LEARNING · TEAM · LIVE DEMO", title="MSL Recognition",
                            tagline=["Reads Malaysian Sign Language letters", "and numbers from hand landmarks."],
                            stack="Python · MediaPipe · scikit-learn · Streamlit", diagram=d_hand),
    "odyssey-travel": dict(kicker="ANDROID · TEAM", title="Odyssey Travel",
                           tagline=["Browse and book travel packages,", "with data that updates in real time."],
                           stack="Kotlin · Android · Firebase", diagram=d_mvvm),
    "portfolio": dict(kicker="WEB · LIVE", title="Portfolio",
                      tagline=["A portfolio you scroll through like files", "in a code editor."],
                      stack="HTML · CSS · JavaScript", diagram=d_editor),
}

BUTTONS = {"portfolio": ("Portfolio", True), "resume": ("Résumé", False),
           "linkedin": ("LinkedIn", False), "repos": ("Repositories", False)}

CONTACT = dict(kicker="OPEN TO INTERNSHIPS", headline="Have a role in mind?", email="leeboonyew06@gmail.com")


def main():
    OUT.mkdir(exist_ok=True)
    for name, c in THEMES.items():
        files = {"hero": hero(c, HERO), "contact": contact(c, CONTACT)}
        files.update({f"project-{k}": card(c, p) for k, p in PROJECTS.items()})
        files.update({f"btn-{k}": button(c, *v) for k, v in BUTTONS.items()})
        for stem, body in files.items():
            (OUT / f"{stem}-{name}.svg").write_text(body, encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
