from PIL import Image, ImageDraw, ImageFont
import textwrap

# Load terminal output
with open('assets/terminal_output.txt', 'r') as f:
    output = f.read()

# Configuration
bg_color = (30, 30, 30)
title_bar_color = (50, 50, 50)
text_color = (240, 240, 240)
prompt_color = (100, 200, 100)
accent_color = (70, 130, 180)
width = 900
padding = 24
line_height = 22
title_bar_height = 36
border_radius = 12

# Try to load a monospace font
font_size = 14
try:
    font = ImageFont.truetype("PTMono-Regular.ttf", font_size)
except:
    try:
        font = ImageFont.truetype("Andale Mono.ttf", font_size)
    except:
        font = ImageFont.load_default()

# Wrap lines to fit width
char_width = font.getlength('M')
max_chars = int((width - 2 * padding) // char_width)
lines = []
for raw_line in output.splitlines():
    if len(raw_line) <= max_chars:
        lines.append(raw_line)
    else:
        wrapped = textwrap.wrap(raw_line, width=max_chars)
        lines.extend(wrapped)

height = title_bar_height + 2 * padding + len(lines) * line_height + 20

# Create image
img = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(img)

# Title bar
draw.rounded_rectangle([(0, 0), (width, title_bar_height)], radius=border_radius, fill=title_bar_color)
draw.rectangle([(0, title_bar_height - border_radius), (width, title_bar_height)], fill=title_bar_color)

# Window buttons
draw.ellipse([(20, 12), (32, 24)], fill=(255, 95, 86))    # close
draw.ellipse([(42, 12), (54, 24)], fill=(255, 189, 46))   # minimize
draw.ellipse([(64, 12), (76, 24)], fill=(39, 201, 63))    # maximize

# Title
draw.text((width // 2, title_bar_height // 2), "Terminal — dart run lib/main.dart", font=font, fill=(180, 180, 180), anchor="mm")

# Terminal prompt line
draw.text((padding, title_bar_height + padding), "assignment_1 $ dart run lib/main.dart", font=font, fill=prompt_color)

# Output lines
y = title_bar_height + padding + line_height + 8
for line in lines:
    # Color section headers subtly
    color = text_color
    if line.startswith('==='):
        color = accent_color
    draw.text((padding, y), line, font=font, fill=color)
    y += line_height

# Cursor
draw.text((padding, y), "_", font=font, fill=prompt_color)

img.save('assets/screenshot.png')
print('Screenshot saved to assets/screenshot.png')
