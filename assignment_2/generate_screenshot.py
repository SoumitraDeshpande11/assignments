from PIL import Image, ImageDraw, ImageFont
import textwrap

with open('assets/terminal_output.txt', 'r') as f:
    output = f.read()

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

font_size = 14
try:
    font = ImageFont.truetype("PTMono-Regular.ttf", font_size)
except:
    try:
        font = ImageFont.truetype("Andale Mono.ttf", font_size)
    except:
        font = ImageFont.load_default()

char_width = font.getlength('M')
max_chars = int((width - 2 * padding) // char_width)
lines = []
for raw_line in output.splitlines():
    if len(raw_line) <= max_chars:
        lines.append(raw_line)
    else:
        lines.extend(textwrap.wrap(raw_line, width=max_chars))

height = title_bar_height + 2 * padding + len(lines) * line_height + 20

img = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(img)

draw.rounded_rectangle([(0, 0), (width, title_bar_height)], radius=border_radius, fill=title_bar_color)
draw.rectangle([(0, title_bar_height - border_radius), (width, title_bar_height)], fill=title_bar_color)
draw.ellipse([(20, 12), (32, 24)], fill=(255, 95, 86))
draw.ellipse([(42, 12), (54, 24)], fill=(255, 189, 46))
draw.ellipse([(64, 12), (76, 24)], fill=(39, 201, 63))
draw.text((width // 2, title_bar_height // 2), "Terminal — dart run lib/main.dart", font=font, fill=(180, 180, 180), anchor="mm")

draw.text((padding, title_bar_height + padding), "assignment_2 $ dart run lib/main.dart", font=font, fill=prompt_color)

y = title_bar_height + padding + line_height + 8
for line in lines:
    color = accent_color if line.startswith('===') else text_color
    draw.text((padding, y), line, font=font, fill=color)
    y += line_height

draw.text((padding, y), "_", font=font, fill=prompt_color)

img.save('assets/screenshot.png')
print('Screenshot saved to assets/screenshot.png')
