from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import re

DOC_PATH = 'DOCUMENTATION.md'
OUT_PATH = 'DOCUMENTATION.docx'
IMG_PATH = 'assets/screenshot.png'


def set_code_style(doc):
    style = doc.styles.add_style('CodeStyle', WD_STYLE_TYPE.PARAGRAPH)
    font = style.font
    font.name = 'Consolas'
    font.size = Pt(9)
    font.color.rgb = RGBColor(50, 50, 50)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.left_indent = Inches(0.2)


def add_formatted_text(paragraph, text):
    """Add text with bold markers **bold** to a paragraph."""
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        run = paragraph.add_run()
        if part.startswith('**') and part.endswith('**'):
            run.text = part[2:-2]
            run.bold = True
        else:
            run.text = part


def parse_table(lines, start_idx):
    """Parse a markdown table and return (rows, next_index)."""
    rows = []
    i = start_idx
    while i < len(lines) and lines[i].strip().startswith('|'):
        cells = [c.strip() for c in lines[i].split('|')[1:-1]]
        # Skip separator line
        if not all(set(c) <= set('- ') for c in cells):
            rows.append(cells)
        i += 1
    return rows, i


def build_doc():
    doc = Document()

    # Title styling
    title = doc.add_heading('Community Board Game Lending Library', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle with name and roll no
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Assignment 1 — Dart Console Application\n')
    run.bold = True
    run.font.size = Pt(12)
    run = subtitle.add_run('Name: Soumitra Deshpande\nRoll No: 150096724035\nEnvironment: Dart SDK 3.x')
    run.font.size = Pt(11)

    doc.add_paragraph()  # spacer

    set_code_style(doc)

    with open(DOC_PATH, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    i = 0
    in_code = False
    code_lines = []
    code_lang = ''

    while i < len(lines):
        line = lines[i]

        # Skip the title line (already handled)
        if i == 0 and line.startswith('# '):
            i += 1
            continue

        # Code blocks
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_lang = line.strip()[3:].strip()
                code_lines = []
            else:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.2)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run('\n'.join(code_lines))
                run.font.name = 'Consolas'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(50, 50, 50)
                in_code = False
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Headings
        if line.startswith('## '):
            doc.add_heading(line[3:], level=1)
            i += 1
            continue
        if line.startswith('### '):
            doc.add_heading(line[4:], level=2)
            i += 1
            continue
        if line.startswith('#### '):
            doc.add_heading(line[5:], level=3)
            i += 1
            continue

        # Tables
        if line.strip().startswith('|'):
            rows, i = parse_table(lines, i)
            if rows:
                table = doc.add_table(rows=1, cols=len(rows[0]))
                table.style = 'Light Grid Accent 1'
                hdr_cells = table.rows[0].cells
                for col_idx, cell_text in enumerate(rows[0]):
                    hdr_cells[col_idx].text = cell_text
                for row in rows[1:]:
                    row_cells = table.add_row().cells
                    for col_idx, cell_text in enumerate(row):
                        row_cells[col_idx].text = cell_text
            continue

        # Image placeholder in markdown: ![alt](path)
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img_match:
            alt, path = img_match.groups()
            doc.add_paragraph(alt, style='Intense Quote')
            try:
                doc.add_picture(IMG_PATH, width=Inches(5.8))
                last_paragraph = doc.paragraphs[-1]
                last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception as e:
                doc.add_paragraph(f'[Image not inserted: {path} - {e}]')
            i += 1
            continue

        # Regular paragraphs
        if line.strip():
            p = doc.add_paragraph()
            add_formatted_text(p, line)
        else:
            # Add small spacer instead of blank paragraph
            pass

        i += 1

    doc.save(OUT_PATH)
    print(f'Saved {OUT_PATH}')


if __name__ == '__main__':
    build_doc()
