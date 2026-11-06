#!/usr/bin/env python3
"""README visuals for dsh-ppap-check, derived from the plugin's real pipeline.

Two figures, both read off the shipped material rather than a generic template:

  hero 1440x576 (Pillow, 4 files: zh/en x light/dark)
      A PPAP submission register as a cover sheet. The part number and the
      customer-set submission level sit at the top (the level is a stamp, because
      the customer sets it and the plugin never embeds a level -> element map),
      five element rows carry their submission state, and two rows show the two
      differences the sample run produces: row 2 has required=yes but no
      submitted record (PP-001), row 4 is a controlled element with no version
      (PP-003). The report line keeps the verdict with the reviewer.

  flow 1100x660 (hand-written SVG, 2 files: light/dark)
      A proof sheet, not a node chain and not a rule x field matrix:
        * every column of the register is named, and three condition closures are
          drawn as labelled arrows over the column labels (PP-001 required ->
          submitted, PP-002 submitted -> date, PP-003 controlled element ->
          version);
        * the two empty cells are hatched in place;
        * each finding is written in the page margin, aligned with the row it
          belongs to, and carries its locator (row + field);
        * header-level rules sit in the rail at the header's height (PP-004
          passes, PP-005 skips because its vocabulary ships empty), column-level
          scans PP-006 / PP-007 are the footnote, and the footer splits
          issues[] / skipped[] before the reviewer.

Values come from the repository's own material, not from imagination:
  samples/quickstart/input/PP-001-unsafe.json  (partNo P-2026-001, partName
      前支架, level Level 3, row 1 设计记录 submitted, row 2 尺寸结果 not)
  rules/ppap-check.yaml                         (PP-001..PP-007, checks, severities)
  src/shared/rows.ts                            (locatorOf(row, conditionField);
      conditionalPresence reports row N, field = the condition column)

Run:      python scripts/gen-readme-assets.py
Requires: Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
Chrome is only used for the visual self-check, not by this script.
"""
from __future__ import annotations

import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}

# --------------------------------------------------------------------- palette
SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", green="#16a34a",
        pill="#ece7f9", band="#f5f2fb", rule="#e3dfee",
        mark="#b45309", mark_bg="#fdf3e9", mark_edge="#ecd3b6",
        shadow=(38, 29, 74), shadow_hex="#3a2c66", glow="#7a68c9",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", green="#3fb950",
        pill="#242d42", band="#202839", rule="#2a3346",
        mark="#d9a441", mark_bg="#2a2216", mark_edge="#5c4a24",
        shadow=(0, 0, 0), shadow_hex="#000000", glow="#8496f5",
    ),
}


def hx(s) -> tuple[int, int, int]:
    if isinstance(s, tuple):
        return s
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def font(size: float, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], int(round(size)))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.12 * (y / h) + 0.88 * (y / h) ** 1.3
        d.line([(0, y), (w, y)],
               fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int = 34) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=c + (int(alpha * (1 - i / 11)),))
    layer = layer.filter(ImageFilter.GaussianBlur(26))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = 22, shadow: int = 24) -> Image.Image:
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -2):
        sd.rounded_rectangle([x0 - i // 6, y0 + i // 2, x1 + i // 6, y1 + i],
                             radius=radius + i // 4,
                             fill=hx(s["shadow"]) + (int(8 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(s["card"]),
                        outline=hx(s["edge"]), width=2)
    return base.convert("RGB")


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: float, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float, what: str) -> None:
    w = measure(text, size, kind)
    if w > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs {w:.1f}px > {max_w}px")


def pill(img: Image.Image, xy: tuple[int, int], text: str, s: dict,
         size: float = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> tuple[int, int]:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = int(size + 20)
    d.rounded_rectangle([x, y, x + w + 30, y + h], radius=h // 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 15, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return int(x + w + 30), int(y + h)


def chip(img: Image.Image, xy: tuple[int, int], text: str, fg: str, bg: str,
         size: float = 11, kind: str = "cjk_bold", padx: int = 9,
         height: int = 20) -> int:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + w + padx * 2, y + height],
                        radius=height // 2, fill=hx(bg))
    d.text((x + padx, y + height / 2), text, font=f, fill=hx(fg), anchor="lm")
    return int(w + padx * 2)


def icon_check(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float,
               fg: str, bg: str) -> None:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hx(fg))
    lw = max(2, int(round(r * 0.30)))
    d.line([(cx - r * 0.44, cy + r * 0.02), (cx - r * 0.10, cy + r * 0.36),
            (cx + r * 0.48, cy - r * 0.34)], fill=hx(bg), width=lw,
           joint="curve")


def icon_alert(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float,
               color: str) -> None:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=hx(color), width=2)
    lw = max(2, int(round(r * 0.26)))
    d.line([(cx, cy - r * 0.46), (cx, cy + r * 0.12)], fill=hx(color), width=lw)
    d.ellipse([cx - lw / 2, cy + r * 0.34, cx + lw / 2, cy + r * 0.34 + lw + 1],
              fill=hx(color))


def stamp(img: Image.Image, center: tuple[int, int], main: str, sub: str,
          s: dict, angle: float = -7.0, w: int = 176, h: int = 82) -> None:
    pad = 26
    layer = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = pad, pad
    col = hx(s["accent"])
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12,
                        outline=col + (215,), width=3)
    d.rounded_rectangle([x0 + 6, y0 + 6, x0 + w - 6, y0 + h - 6], radius=8,
                        outline=col + (90,), width=1)
    d.text((x0 + w / 2, y0 + 31), main, font=font(21, "mono_bold"),
           fill=col + (235,), anchor="mm")
    d.text((x0 + w / 2, y0 + 57), sub, font=font(12, "cjk_bold"),
           fill=col + (220,), anchor="mm")
    d.line([(x0 + 24, y0 + 44), (x0 + w - 24, y0 + 44)], fill=col + (70,),
           width=1)
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.paste(layer, (int(center[0] - layer.width / 2),
                      int(center[1] - layer.height / 2)), layer)


def richtext(img: Image.Image, xy: tuple[float, float], segs: list[tuple],
             anchor: str = "ls") -> None:
    """Draw (text, size, kind, color) runs as one line, anchored l/r/m."""
    d = ImageDraw.Draw(img)
    widths = [measure(seg[0], seg[1], seg[2]) for seg in segs]
    total = sum(widths)
    x, y = xy
    if anchor[0] == "r":
        x -= total
    elif anchor[0] == "m":
        x -= total / 2
    for seg, w in zip(segs, widths):
        d.text((x, y), seg[0], font=font(seg[1], seg[2]), fill=hx(seg[3]),
               anchor="ls")
        x += w


# =========================================================================== hero
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 核查器",
        value1="七条规则，逐行核对",
        value2="差异落到行号与栏名",
        sub1="只列材料内部能指认的差异：要求→提交、提交→日期、受控→版本；",
        sub2="不判合规、不认定责任——结论永远留给审核人。",
        meta="PP-001..PP-007 · 规则包即数据 · skipped 逐条说明",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        card_title="PPAP 提交要素清单",
        card_chip="rows[] · 只读",
        part="P-2026-001",
        sub="前支架 · 某某零部件有限公司",
        stamp_main="Level 3",
        stamp_sub="顾客指定",
        rows=[
            ("设计记录", "已提交 · 2026-03-05 · 版本 B", "ok", None),
            ("尺寸结果", "是否提交：空", "diff", "PP-001"),
            ("控制计划", "已提交 · 2026-03-05 · 版本 C", "ok", None),
            ("PFMEA", "版本：空 · 受控要素", "diff", "PP-003"),
            ("PSW", "已提交 · 2026-03-12 · 版本 A", "ok", None),
        ],
        foot_left=[("2 条差异", 14, "cjk_bold", "mark"),
                   (" · ", 14, "cjk", "faint"),
                   ("1 条未执行", 14, "cjk", "sub")],
        foot_right="结论留给审核人",
        caption="示例清单 · 结构同 quickstart 样例，非真实提交材料",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · checker",
        value1="Seven rules, one register",
        value2="each gap lands on a row",
        sub1="Required → submitted → date, controlled element → version;",
        sub2="no compliance verdict — the reviewer decides.",
        meta="PP-001..PP-007 · rules are data · skipped always explained",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        card_title="PPAP submission register",
        card_chip="rows[] · read-only",
        part="P-2026-001",
        sub="Front bracket · Some Components Ltd.",
        stamp_main="Level 3",
        stamp_sub="customer-set",
        rows=[
            ("Design records", "submitted · 2026-03-05 · rev B", "ok", None),
            ("Dimensional results", "no submission record", "diff", "PP-001"),
            ("Control plan", "submitted · 2026-03-05 · rev C", "ok", None),
            ("PFMEA", "no version · controlled element", "diff", "PP-003"),
            ("PSW", "submitted · 2026-03-12 · rev A", "ok", None),
        ],
        foot_left=[("2 differences", 14, "cjk_bold", "mark"),
                   (" · ", 14, "cjk", "faint"),
                   ("1 not executed", 14, "cjk", "sub")],
        foot_right="verdict stays with the reviewer",
        caption="Sample register · same shape as the quickstart sample, not a real submission",
    ),
}


def hero(lang: str, skin: str) -> str:
    s = SKIN[skin]
    t = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1210, 54, 420, s["glow"], 30 if skin == "light" else 22)
    img = glow(img, 150, 560, 380, s["glow"], 22 if skin == "light" else 16)

    # ---- left column ------------------------------------------------------
    require_w(t["kicker"], 16, "cjk_bold", 430, "kicker")
    pill(img, (88, 78), t["kicker"], s, size=16)
    require_w("dsh-ppap-check", 64, "mono_bold", 640, "title")
    ImageDraw.Draw(img).text((88, 178), "dsh-ppap-check", font=font(64, "mono_bold"),
                             fill=hx(s["text"]), anchor="ls")
    for i, line in enumerate((t["value1"], t["value2"])):
        require_w(line, 30, "cjk_bold", 620, "value line")
        ImageDraw.Draw(img).text((88, 252 + i * 46), line,
                                 font=font(30, "cjk_bold"), fill=hx(s["text"]),
                                 anchor="ls")
    for i, line in enumerate((t["sub1"], t["sub2"])):
        require_w(line, 18, "cjk", 640, "subtitle")
        ImageDraw.Draw(img).text((88, 350 + i * 28), line, font=font(18),
                                 fill=hx(s["sub"]), anchor="ls")
    require_w(t["meta"], 16, "cjk", 640, "meta")
    ImageDraw.Draw(img).text((88, 442), t["meta"], font=font(16),
                             fill=hx(s["faint"]), anchor="ls")
    require_w(t["foot"], 14.5, "cjk", 630, "footer")
    ImageDraw.Draw(img).text((88, 514), t["foot"], font=font(14.5),
                             fill=hx(s["faint"]), anchor="ls")

    # ---- register cover card ---------------------------------------------
    img = card(img, (744, 64, 1368, 520), s, radius=22)
    d = ImageDraw.Draw(img)
    x0, x1 = 776, 1336
    require_w(t["card_title"], 17, "cjk_bold", 420, "card title")
    d.text((x0, 106), t["card_title"], font=font(17, "cjk_bold"),
           fill=hx(s["text"]), anchor="ls")
    cw = measure(t["card_chip"], 11, "cjk") + 20
    d.rounded_rectangle([x1 - cw, 88, x1, 110], radius=11, fill=hx(s["band"]))
    d.text((x1 - cw / 2, 99), t["card_chip"], font=font(11, "cjk"),
           fill=hx(s["faint"]), anchor="mm")
    require_w(t["part"], 30, "mono_bold", 430, "part number")
    d.text((x0, 150), t["part"], font=font(30, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    require_w(t["sub"], 13, "cjk", 420, "card sub")
    d.text((x0, 174), t["sub"], font=font(13), fill=hx(s["faint"]), anchor="ls")

    stamp(img, (1250, 150), t["stamp_main"], t["stamp_sub"], s)

    d.line([(x0, 200), (x1, 200)], fill=hx(s["rule"]), width=1)

    row_h = 44
    y = 214
    for i, (name, detail, status, rule) in enumerate(t["rows"]):
        diff = status == "diff"
        if diff:
            d.rounded_rectangle([x0 - 2, y + 1, x1 + 2, y + row_h - 3],
                                radius=10, fill=hx(s["mark_bg"]))
            d.rounded_rectangle([x0 - 2, y + 7, x0, y + row_h - 9],
                                radius=1, fill=hx(s["mark"]))
        require_w(name, 15, "cjk_bold", 400, "row name")
        d.text((x0 + 16, y + 17), name, font=font(15, "cjk_bold"),
               fill=hx(s["text"]), anchor="ls")
        require_w(detail, 11.5, "cjk", 400, "row detail")
        d.text((x0 + 16, y + 34), detail, font=font(11.5),
               fill=hx(s["mark"] if diff else s["sub"]), anchor="ls")
        if rule is not None:
            cwid = chip(img, (x1 - 146, y + 10), rule, s["mark"],
                        s["card"], size=11, kind="mono_bold", padx=8,
                        height=19)
            if x1 - 146 + cwid > x1 - 36:
                raise SystemExit("FATAL: hero rule chip overlaps the icon")
        if diff:
            icon_alert(d, x1 - 18, y + 20, 8, s["mark"])
        else:
            icon_check(d, x1 - 18, y + 20, 8, s["green"], s["card"])
        if i < len(t["rows"]) - 1:
            d.line([(x0, y + row_h - 1), (x1, y + row_h - 1)],
                   fill=hx(s["rule"]), width=1)
        y += row_h

    d.line([(x0, 446), (x1, 446)], fill=hx(s["rule"]), width=1)
    richtext(img, (x0, 480), [(seg[0], seg[1], seg[2],
                               s[seg[3]]) for seg in t["foot_left"]])
    require_w(t["foot_right"], 13, "cjk_bold", 380, "hero footer right")
    d.text((x1, 480), t["foot_right"], font=font(13, "cjk_bold"),
           fill=hx(s["green"]), anchor="rs")
    require_w(t["caption"], 12, "cjk", 560, "caption")
    d.text((x0, 548), t["caption"], font=font(12), fill=hx(s["faint"]),
           anchor="ls")

    name = f"dsh-ppap-check-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    return name


# ======================================================================= SVG kit
CJK_FAMILY = ("'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',"
              "'Source Han Sans SC',sans-serif")
MONO_FAMILY = "'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace"


class Svg:
    def __init__(self, s: dict):
        self.s = s
        self.parts: list[str] = []
        self.overflows: list[str] = []

    def add(self, text: str) -> None:
        self.parts.append(text)

    def _check(self, text: str, size: float, mono: bool, bold: bool,
               max_w: float | None) -> float:
        kind = ("mono_bold" if bold else "mono") if mono else (
            "cjk_bold" if bold else "cjk")
        w = measure(text, size, kind)
        if max_w is not None and w > max_w + 0.8:
            self.overflows.append(f"{text!r} {w:.1f} > {max_w:.0f}")
        return w

    def text(self, x: float, y: float, text: str, size: float, color: str,
             *, mono: bool = False, bold: bool = False, anchor: str = "start",
             max_w: float | None = None, opacity: float | None = None,
             spacing: float | None = None) -> None:
        self._check(text, size, mono, bold, max_w)
        fam = MONO_FAMILY if mono else CJK_FAMILY
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{color}"',
                 f'font-family="{fam}"', f'font-size="{size:g}"']
        if bold:
            attrs.append('font-weight="700"')
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if spacing is not None:
            attrs.append(f'letter-spacing="{spacing:g}"')
        self.add(f'<text {" ".join(attrs)}>{escape(text)}</text>')

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1,
             opacity: float | None = None, shadow: bool = False,
             dash: str | None = None) -> None:
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'width="{w:g}"', f'height="{h:g}"',
                 f'rx="{rx:g}"', f'fill="{fill}"']
        if stroke is not None:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw:g}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        if dash is not None:
            attrs.append(f'stroke-dasharray="{dash}"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1, dash: str | None = None,
             opacity: float | None = None, cap: str = "round") -> None:
        attrs = [f'x1="{x1:g}"', f'y1="{y1:g}"', f'x2="{x2:g}"', f'y2="{y2:g}"',
                 f'stroke="{stroke}" stroke-width="{sw:g}"',
                 f'stroke-linecap="{cap}"']
        if dash is not None:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def path(self, dd: str, *, stroke: str | None = None, fill: str = "none",
             sw: float = 1, dash: str | None = None,
             opacity: float | None = None, marker: bool = False) -> None:
        attrs = [f'd="{dd}"', f'fill="{fill}"']
        if stroke is not None:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw:g}"')
            attrs.append('stroke-linecap="round" stroke-linejoin="round"')
        if dash is not None:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if marker:
            attrs.append('marker-end="url(#arr)"')
        self.add(f'<path {" ".join(attrs)}/>')

    def circle(self, cx: float, cy: float, r: float, *, fill: str = "none",
               stroke: str | None = None, sw: float = 1,
               opacity: float | None = None) -> None:
        attrs = [f'cx="{cx:g}"', f'cy="{cy:g}"', f'r="{r:g}"', f'fill="{fill}"']
        if stroke is not None:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw:g}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        self.add(f'<circle {" ".join(attrs)}/>')

    def chip(self, x: float, y: float, text: str, *, fg: str, bg: str,
             size: float = 11, mono: bool = True, h: float = 18,
             pad: float = 7, bold: bool = True, rx: float | None = None) -> float:
        w = self._check(text, size, mono, bold, None) + pad * 2
        r = h / 2 if rx is None else rx
        self.rect(x, y, w, h, fill=bg, rx=r)
        self.text(x + pad, y + h / 2 + size * 0.35, text, size, fg, mono=mono,
                  bold=bold)
        return w

    def svg(self, w: int, h: int, aria: str) -> str:
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-label="{escape(aria)}">',
                f'<title>{escape(aria)}</title>']
        return "\n".join(head + self.parts + ["</svg>"]) + "\n"


# ====================================================================== flow v5
FLOW_W, FLOW_H = 1100, 660

# The register shown is the quickstart sample plus three more element rows so the
# two rule kinds (row-closure, column-scan) both have something to show.
COLUMNS = [
    ("序号", 54, "elementNo"),
    ("提交要素", 172, "element"),
    ("是否要求", 94, "required"),
    ("是否提交", 102, "submitted"),
    ("提交日期", 118, "submittedAt"),
    ("版本", 96, "version"),
]
ROWS = [
    ("1", "设计记录", "是", "是", "2026-03-05", "B"),
    ("2", "尺寸结果", "是", "", "2026-03-05", "B"),
    ("3", "控制计划", "是", "是", "2026-03-05", "C"),
    ("4", "PFMEA", "是", "是", "2026-03-12", ""),
    ("5", "PSW", "是", "是", "2026-03-12", "A"),
]
TABLE_X, TABLE_W = 64, 636
ROW_TOP, ROW_H = 280, 42


def _cols() -> list[tuple[float, float]]:
    out, x = [], TABLE_X
    for _, w, _ in COLUMNS:
        out.append((x, x + w))
        x += w
    return out


def _cell_center(i: int) -> float:
    x0, x1 = _cols()[i]
    return (x0 + x1) / 2


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    v = Svg(s)
    c = {k: s[k] for k in ("text", "sub", "faint", "accent", "green",
                           "mark", "mark_bg", "mark_edge", "band", "rule",
                           "card", "edge")}
    v.add('<defs>')
    v.add('<linearGradient id="bg" x1="0" y1="0" x2="0.15" y2="1">'
          f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    v.add('<filter id="soft" x="-25%" y="-25%" width="150%" height="160%">'
          f'<feDropShadow dx="0" dy="6" stdDeviation="8" '
          f'flood-color="{s["shadow_hex"]}" '
          f'flood-opacity="{0.10 if skin == "light" else 0.40}"/></filter>')
    v.add('<marker id="arr" viewBox="0 0 10 10" refX="8.6" refY="5" '
          'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
          f'<path d="M1 1 L9 5 L1 9 z" fill="{c["accent"]}"/></marker>')
    v.add('<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" '
          'patternTransform="rotate(45)">'
          f'<line x1="0" y1="0" x2="0" y2="9" stroke="{c["mark"]}" '
          'stroke-width="1.6" opacity="0.30"/></pattern>')
    v.add('</defs>')

    v.rect(0, 0, FLOW_W, FLOW_H, fill="url(#bg)", rx=22)

    # ---------------------------------------------------------------- header
    v.text(44, 46, "dsh-ppap-check", 17, c["text"], mono=True, bold=True)
    v.text(212, 46, "结构图 · 清单页 + 页边批注", 12.5, c["faint"])
    v.text(1056, 44, "rules/ppap-check.yaml · 7 条 · 2026.1", 11.5, c["faint"],
           anchor="end")
    v.text(44, 74,
           "file / material → parseMaterial()：表头 2 条 · 行内 3 条 · 整列 2 条，"
           "七条规则各读清单的一栏；差异带行号与栏名，没能执行的进 skipped。",
           12.5, c["sub"], max_w=1012)
    v.line(44, 90, 1056, 90, stroke=c["rule"], sw=1)

    # ------------------------------------------------------------ proof sheet
    v.rect(44, 104, 676, 448, fill=c["card"], rx=20, stroke=c["edge"], sw=1.5,
           shadow=True)
    v.text(64, 138, "提交要素清单", 15.5, c["text"], bold=True)
    v.text(64 + measure("提交要素清单", 15.5, "cjk_bold") + 10, 140, "rows[]",
           11.5, c["faint"], mono=True)
    chip_w = measure("JSON / YAML · 只读", 11, "cjk") + 20
    v.rect(700 - chip_w, 118, chip_w, 22, fill=c["band"], rx=11)
    v.text(700 - chip_w / 2, 133, "JSON / YAML · 只读", 11, c["faint"],
           anchor="middle")

    # header band: the two fields PP-004 checks, and level (PP-005)
    v.rect(64, 150, 636, 46, fill=c["band"], rx=12)
    v.text(80, 171, "partNo", 11, c["faint"], mono=True)
    v.text(80 + 46, 171, "P-2026-001", 12.5, c["text"], mono=True)
    v.text(272, 171, "level", 11, c["faint"], mono=True)
    v.text(272 + 38, 171, "Level 3", 12.5, c["text"], mono=True)
    v.text(430, 171, "partName", 11, c["faint"], mono=True)
    v.text(430 + 60, 171, "前支架", 12.5, c["text"])
    v.text(80, 190, "supplier", 11, c["faint"], mono=True)
    v.text(80 + 58, 190, "某某零部件有限公司", 11.5, c["sub"])
    v.text(276, 190, "· 5 行提交要素", 11.5, c["faint"])
    # condition closures over the header: condition column -> required column
    closures = [
        ("PP-003", _cell_center(1), _cell_center(5), 206),
        ("PP-001", _cell_center(2), _cell_center(3), 224),
        ("PP-002", _cell_center(3), _cell_center(4), 242),
    ]
    for rid, xa, xb, yy in closures:
        v.line(xa, yy - 4, xa, yy + 4, stroke=c["accent"], sw=1.4, opacity=0.75)
        v.path(f"M{xa + 4:g} {yy:g} H{xb - 5:g}", stroke=c["accent"], sw=1.4,
               opacity=0.75, marker=True)
        w = measure(rid, 11, "mono_bold") + 12
        v.rect((xa + xb) / 2 - w / 2, yy - 8, w, 16, fill=c["card"], rx=8,
               stroke=c["edge"], sw=1)
        v.text((xa + xb) / 2, yy + 4, rid, 11, c["accent"], mono=True,
               bold=True, anchor="middle")

    # column labels
    for (label, _, _), (x0, x1) in zip(COLUMNS, _cols()):
        v.text((x0 + x1) / 2, 270, label, 12.5, c["sub"], anchor="middle")
    v.line(TABLE_X, 278, TABLE_X + TABLE_W, 278, stroke=c["rule"], sw=1)

    # table grid + rows
    bounds = _cols()
    for bi, (x0, _) in enumerate(bounds[1:], start=1):
        v.line(x0, ROW_TOP, x0, ROW_TOP + ROW_H * len(ROWS), stroke=c["rule"],
               sw=1, opacity=0.55)
    for i, row in enumerate(ROWS):
        top = ROW_TOP + i * ROW_H
        if i % 2 == 1:
            v.rect(TABLE_X, top, TABLE_W, ROW_H, fill=c["band"], opacity=0.5)
        v.line(TABLE_X, top, TABLE_X + TABLE_W, top, stroke=c["rule"], sw=1,
               opacity=0.75)
        for j, (value, (x0, x1)) in enumerate(zip(row, bounds)):
            cx = (x0 + x1) / 2
            if value == "":
                v.rect(x0 + 4, top + 4, (x1 - x0) - 8, ROW_H - 8, fill="url(#hatch)",
                       rx=6, stroke=c["mark"], sw=1.1, dash="4 3")
                v.text(cx, top + ROW_H / 2 + 4, "空", 12, c["mark"],
                       anchor="middle")
                continue
            if j == 1:
                v.text(x0 + 18, top + ROW_H / 2 + 4.5, value, 13, c["text"])
            elif j == 4:
                v.text(cx, top + ROW_H / 2 + 4.5, value, 12.5, c["text"],
                       mono=True, anchor="middle")
            else:
                v.text(cx, top + ROW_H / 2 + 4.5, value, 13, c["text"],
                       mono=(j == 0 or j == 5), anchor="middle")
    v.line(TABLE_X, ROW_TOP + ROW_H * len(ROWS), TABLE_X + TABLE_W,
           ROW_TOP + ROW_H * len(ROWS), stroke=c["rule"], sw=1)

    # footnote: whole-column scans
    v.line(64, 498, 700, 498, stroke=c["rule"], sw=1)
    v.text(64, 516,
           "整列扫描：PP-007 序号唯一 · PP-006 提交要素占位符 —— 本次均无差异",
           11.5, c["sub"], max_w=632)
    v.text(64, 534,
           "条件闭合：PP-001 要求→提交 · PP-002 提交→日期 · PP-003 受控要素→版本"
           "（箭头指向必填栏）", 11.5, c["faint"], max_w=632)

    # ------------------------------------------------------------- page margin
    v.text(736, 126, "页边批注", 11.5, c["faint"], spacing=1.5)
    v.line(736, 136, 1056, 136, stroke=c["rule"], sw=1)

    # header status (PP-004 passes, PP-005 cannot run)
    v.text(752, 160, "表头 · header", 11, c["faint"])
    v.circle(758, 177, 7, fill=c["green"])
    v.path("M754.4 177.2 L756.9 179.6 L761.8 174.2", stroke=c["card"], sw=1.7)
    v.text(772, 181, "PP-004 表头齐备", 12.5, c["text"], max_w=270)
    v.line(753, 198, 764, 198, stroke=c["faint"], sw=1.4)
    v.text(772, 202, "PP-005 未执行 · values 空", 12, c["sub"], max_w=270)

    # two located findings, each aligned with its row
    notes = [
        (310, "PP-001", "第 2 行", "是否要求=是，是否提交 为空",
         "issues[] · locator row 2 / required"),
        (394, "PP-003", "第 4 行", "PFMEA 受控，版本 为空",
         "issues[] · locator row 4 / element"),
    ]
    for y0, rid, where, found, loc in notes:
        v.rect(736, y0, 320, 68, fill=c["card"], rx=18, stroke=c["mark_edge"],
               sw=1.2, shadow=True)
        v.rect(750, y0 + 12, 3, 44, fill=c["mark"], rx=1.5)
        w = v.chip(762, y0 + 10, rid, fg=c["mark"], bg=c["mark_bg"], size=11,
                   h=18, pad=7)
        v.text(762 + w + 8, y0 + 23, "warn", 11, c["mark"], mono=True,
               opacity=0.85)
        v.text(1042, y0 + 24, where, 11, c["faint"], anchor="end")
        v.text(762, y0 + 44, found, 12.5, c["text"], max_w=272)
        v.text(762, y0 + 61, loc, 11, c["faint"], max_w=272)

    v.text(752, 486, "第 1 · 3 · 5 行：本次无差异", 11.5, c["faint"], max_w=280)
    v.text(752, 512, "未执行的检查不并入通过；空 issues 不等于没问题", 11.5,
           c["faint"], max_w=280)

    # leader lines from the sheet edge to each margin note
    for yy, color in ((181, c["faint"]), (344, c["mark"]), (428, c["mark"])):
        v.line(720, yy, 734, yy, stroke=color, sw=1.2, dash="3 3")
        v.circle(721, yy, 2, fill=color)

    # ------------------------------------------------------------------ footer
    v.line(44, 568, 1056, 568, stroke=c["rule"], sw=1)
    v.circle(48, 588, 3.2, fill=c["mark"])
    v.text(58, 592, "issues[] 2 条 · 第 2 / 4 行", 12.5, c["text"], max_w=240)
    v.line(300, 581, 300, 597, stroke=c["rule"], sw=1)
    v.circle(314, 588, 3.2, fill="none", stroke=c["faint"], sw=1.4)
    v.text(324, 592, "skipped[] 1 条 · PP-005 values 空", 12.5, c["sub"],
           max_w=360)
    v.text(1056, 592, "审核人 · 只列差异，不作结论", 12.5, c["green"],
           anchor="end", max_w=340)
    v.text(44, 618,
           "buildView() → markdown + reportJson · 措辞守卫 + 免责声明 · 只读材料 · "
           "无网络 · 不调用模型", 11.5, c["faint"], max_w=1012)

    if v.overflows:
        raise SystemExit("FATAL: SVG label overflow:\n  " + "\n  ".join(v.overflows))
    return v.svg(
        FLOW_W, FLOW_H,
        "dsh-ppap-check 结构图：一份 PPAP 提交要素清单的清样。表头由 PP-004 核对、"
        "PP-005 因 values 为空未执行；三条行内条件闭合画在列标上方（PP-001 是否要求→"
        "是否提交、PP-002 是否提交→提交日期、PP-003 受控要素→版本）；第 2 行与第 4 行的"
        "空单元格以斜线标出，差异以页边批注回到行号与栏名；整列扫描 PP-006、PP-007 在页脚"
        "注明本次无差异；页脚分成 issues[] 2 条与 skipped[] 1 条两条通道，结论留给审核人。")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    written = []
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            written.append(hero(lang, skin))
        name = f"dsh-ppap-check-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(flow_svg(skin))
        written.append(name)
    for name in written:
        path = os.path.join(OUT, name)
        print(f"wrote {name} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()
