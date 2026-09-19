"""Render the project screenshots: code capture and terminal capture."""
import re

from PIL import Image, ImageDraw, ImageFont


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


# -------------------------------------------------------------------- code

KEYWORDS = {
    "import", "class", "extends", "final", "const", "return", "void",
    "static", "super", "required", "this", "child", "true", "false",
    "Widget", "BuildContext", "StatelessWidget", "StatefulWidget", "State",
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
    title = "zsh — assignment_8"
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
    draw_code("lib/main.dart", "assets/code_main.png", max_lines=150)
    draw_terminal("assets/terminal_output.txt", "assets/terminal.png")
