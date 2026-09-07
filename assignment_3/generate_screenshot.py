"""Render the project screenshots: dashboard preview, code capture, terminal capture."""
import re

from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)
CARD = (244, 246, 245)
ACCENT = (45, 106, 79)
TEXT = (30, 30, 30)
GREY = (130, 130, 130)


def font(size, mono=False):
    if mono:
        for path in (
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/SFMono-Regular.otf",
            "/System/Library/Fonts/Courier.ttc",
        ):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    for name in ("SF Compact", "Helvetica Neue", "Helvetica", "Arial"):
        try:
            return ImageFont.truetype(f"/System/Library/Fonts/{name}.ttf", size)
        except OSError:
            continue
    return ImageFont.load_default()


# ---------------------------------------------------------------- dashboard

def draw_dashboard():
    W, H = 430, 960
    PADDING, RADIUS = 22, 12
    f_appbar = font(20)
    f_section = font(17)
    f_chip_label = font(12)
    f_chip_value = font(19)
    f_card_value = font(20)
    f_card_label = font(12)
    f_item = font(14)
    f_time = font(11)

    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    y = 26
    d.text((PADDING, y), "Store Dashboard", font=f_appbar, fill=TEXT)
    y += 52

    chips = [("Today", "Rs 12,480"), ("This week", "Rs 86,120"), ("This month", "Rs 4.2L")]
    gap = 12
    chip_w = (W - 2 * PADDING - 2 * gap) // 3
    for i, (label, value) in enumerate(chips):
        x = PADDING + i * (chip_w + gap)
        d.rounded_rectangle([x, y, x + chip_w, y + 64], RADIUS, fill=ACCENT)
        d.text((x + 12, y + 10), label, font=f_chip_label, fill=(255, 255, 255))
        d.text((x + 12, y + 30), value, font=f_chip_value, fill=(255, 255, 255))
    y += 64 + 24

    d.text((PADDING, y), "Overview", font=f_section, fill=TEXT)
    y += 32

    stats = [
        ("Revenue", "Rs 4.2L"), ("Orders", "1,284"), ("Customers", "856"),
        ("Refunds", "12"), ("Conversion", "3.4%"), ("Avg. Order", "Rs 327"),
    ]
    card_w = (W - 2 * PADDING - gap) // 2
    card_h = 96
    for i, (title, value) in enumerate(stats):
        row, col = divmod(i, 2)
        x = PADDING + col * (card_w + gap)
        cy = y + row * (card_h + gap)
        d.rounded_rectangle([x, cy, x + card_w, cy + card_h], RADIUS, fill=CARD)
        d.ellipse([x + 14, cy + 14, x + 26, cy + 26], outline=ACCENT, width=2)
        d.text((x + 14, cy + 42), value, font=f_card_value, fill=TEXT)
        d.text((x + 14, cy + 70), title, font=f_card_label, fill=GREY)
    y += 3 * card_h + 2 * gap + 24

    d.text((PADDING, y), "Recent activity", font=f_section, fill=TEXT)
    y += 32

    activity = [
        ("Priya placed order #1284", "2 min ago"),
        ("Refund issued for order #1201", "18 min ago"),
        ("New customer signup: Arjun", "44 min ago"),
        ("Order #1279 shipped", "1 hr ago"),
        ("Weekly report generated", "3 hrs ago"),
    ]
    for title, time in activity:
        d.ellipse([PADDING, y + 18, PADDING + 8, y + 26], fill=ACCENT)
        d.text((PADDING + 20, y + 12), title, font=f_item, fill=TEXT)
        tw = d.textlength(time, font=f_time)
        d.text((W - PADDING - tw, y + 15), time, font=f_time, fill=GREY)
        y += 44
        d.line([PADDING, y, W - PADDING, y], fill=(235, 235, 235), width=1)

    img.save("assets/screenshot.png")
    print(f"Saved assets/screenshot.png ({W}x{H})")


# -------------------------------------------------------------------- code

KEYWORDS = {
    "import", "class", "extends", "final", "const", "return", "void",
    "static", "super", "required", "this", "child", "true", "false",
    "Widget", "BuildContext", "StatelessWidget",
}
C_BG = (43, 43, 43)
C_TEXT = (220, 220, 220)
C_KEYWORD = (204, 120, 50)
C_STRING = (106, 135, 89)
C_COMMENT = (128, 128, 128)
C_LINENO = (110, 110, 110)
C_TITLE = (60, 60, 60)


def draw_code(src_path, out_path, max_lines=90):
    with open(src_path) as f:
        lines = f.read().splitlines()[:max_lines]

    fs = 15
    lh = 24
    pad = 18
    bar = 34
    gutter = 46
    f_mono = font(fs, mono=True)
    f_num = font(12, mono=True)

    width = 1000
    height = bar + pad * 2 + lh * len(lines)
    img = Image.new("RGB", (width, height), C_BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, width, bar], fill=C_TITLE)
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse([16 + i * 22, 12, 28 + i * 22, 24], fill=c)
    title = "lib/main.dart"
    tw = d.textlength(title, font=f_num)
    d.text(((width - tw) / 2, 11), title, font=f_num, fill=(200, 200, 200))

    token_re = re.compile(r"('[^']*'|\w+|.)")

    y = bar + pad
    for n, line in enumerate(lines, 1):
        num = str(n)
        nw = d.textlength(num, font=f_num)
        d.text((gutter - nw - 10, y + 3), num, font=f_num, fill=C_LINENO)
        x = gutter + 14
        stripped = line.lstrip()
        if stripped.startswith("//"):
            d.text((x, y), line, font=f_mono, fill=C_COMMENT)
        else:
            for tok in token_re.findall(line):
                if tok.startswith("'") and tok.endswith("'") and len(tok) > 1:
                    color = C_STRING
                elif tok in KEYWORDS:
                    color = C_KEYWORD
                else:
                    color = C_TEXT
                d.text((x, y), tok, font=f_mono, fill=color)
                x += d.textlength(tok, font=f_mono)
        y += lh

    img.save(out_path)
    print(f"Saved {out_path} ({width}x{height}, {len(lines)} lines)")


# ---------------------------------------------------------------- terminal

def draw_terminal(txt_path, out_path):
    import os
    if not os.path.exists(txt_path):
        print(f"Skipped {out_path} ({txt_path} not found yet)")
        return
    with open(txt_path) as f:
        lines = f.read().splitlines()

    fs, lh, pad, bar = 15, 24, 20, 34
    f_mono = font(fs, mono=True)
    f_title = font(12, mono=True)

    width = 1000
    height = bar + pad * 2 + lh * len(lines)
    img = Image.new("RGB", (width, height), (30, 30, 30))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, width, bar], fill=C_TITLE)
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse([16 + i * 22, 12, 28 + i * 22, 24], fill=c)
    title = "zsh — assignment_3"
    tw = d.textlength(title, font=f_title)
    d.text(((width - tw) / 2, 11), title, font=f_title, fill=(200, 200, 200))

    y = bar + pad
    for line in lines:
        if line.startswith("$"):
            d.text((pad, y), line, font=f_mono, fill=(120, 220, 120))
        elif "Saved" in line or line.startswith("[") or "create mode" in line:
            d.text((pad, y), line, font=f_mono, fill=(150, 200, 255))
        else:
            d.text((pad, y), line, font=f_mono, fill=(230, 230, 230))
        y += lh

    img.save(out_path)
    print(f"Saved {out_path} ({width}x{height}, {len(lines)} lines)")


if __name__ == "__main__":
    draw_dashboard()
    draw_code("lib/main.dart", "assets/code_main.png")
    draw_terminal("assets/terminal_output.txt", "assets/terminal.png")
