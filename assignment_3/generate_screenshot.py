"""Draw a preview of the dashboard's narrow (phone) layout with PIL."""
from PIL import Image, ImageDraw, ImageFont

W, H = 430, 960
PADDING = 22
RADIUS = 12
WHITE = (255, 255, 255)
CARD = (244, 246, 245)
ACCENT = (45, 106, 79)
TEXT = (30, 30, 30)
GREY = (130, 130, 130)


def font(size, bold=False):
    for name in ("SF Compact", "Helvetica Neue", "Helvetica", "Arial"):
        try:
            return ImageFont.truetype(f"/System/Library/Fonts/{name}.ttf", size)
        except OSError:
            continue
    return ImageFont.load_default()


f_appbar = font(20, bold=True)
f_section = font(17, bold=True)
f_chip_label = font(12)
f_chip_value = font(19, bold=True)
f_card_value = font(20, bold=True)
f_card_label = font(12)
f_item = font(14)
f_time = font(11)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

y = 26
d.text((PADDING, y), "Store Dashboard", font=f_appbar, fill=TEXT)
y += 52

# Summary chips row (Expanded x 3)
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

# Stat cards grid (GridView, 2 columns)
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

# Activity feed (ListView)
activity = [
    ("Priya placed order #1284", "2 min ago"),
    ("Refund issued for order #1201", "18 min ago"),
    ("New customer signup: Arjun", "44 min ago"),
    ("Order #1279 shipped", "1 hr ago"),
    ("Weekly report generated", "3 hrs ago"),
]
row_h = 44
for title, time in activity:
    d.ellipse([PADDING, y + 18, PADDING + 8, y + 26], fill=ACCENT)
    d.text((PADDING + 20, y + 12), title, font=f_item, fill=TEXT)
    tw = d.textlength(time, font=f_time)
    d.text((W - PADDING - tw, y + 15), time, font=f_time, fill=GREY)
    y += row_h
    d.line([PADDING, y, W - PADDING, y], fill=(235, 235, 235), width=1)

img.save("assets/screenshot.png")
print(f"Saved assets/screenshot.png ({W}x{H})")
