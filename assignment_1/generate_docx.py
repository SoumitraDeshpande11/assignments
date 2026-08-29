from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re

DOC_PATH = 'DOCUMENTATION.md'
OUT_PATH = 'DOCUMENTATION.docx'
IMG_PATH = 'assets/screenshot.png'

# Black + gold palette
BLACK = (10, 10, 10)
DARK_GRAY = (30, 30, 30)
GOLD = (212, 175, 55)
LIGHT_GOLD = (255, 223, 128)
WHITE = (255, 255, 255)
OFF_WHITE = (230, 230, 230)


def set_cell_shading(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), '%02x%02x%02x' % color)
    tcPr.append(shd)


def set_cell_border(cell, color, size='4'):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_el = OxmlElement(f'w:{edge}')
        edge_el.set(qn('w:val'), 'single')
        edge_el.set(qn('w:sz'), size)
        edge_el.set(qn('w:color'), '%02x%02x%02x' % color)
        tcBorders.append(edge_el)
    tcPr.append(tcBorders)


def set_run_font(run, name='Arial', size=11, color=OFF_WHITE, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(*color)
    run.bold = bold


def add_page_number(section):
    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    set_run_font(run, size=9, color=GOLD)


def add_formatted_text(paragraph, text):
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        run = paragraph.add_run()
        if part.startswith('**') and part.endswith('**'):
            run.text = part[2:-2]
            set_run_font(run, bold=True, color=LIGHT_GOLD)
        else:
            run.text = part
            set_run_font(run)


def parse_table(lines, start_idx):
    rows = []
    i = start_idx
    while i < len(lines) and lines[i].strip().startswith('|'):
        cells = [c.strip() for c in lines[i].split('|')[1:-1]]
        if not all(set(c) <= set('- ') for c in cells):
            rows.append(cells)
        i += 1
    return rows, i


def set_page_background(section, color):
    sectPr = section._sectPr
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), '%02x%02x%02x' % color)
    shd.set(qn('w:val'), 'clear')
    sectPr.append(shd)


def build_doc():
    doc = Document()

    # Page setup
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    set_page_background(section, BLACK)
    add_page_number(section)

    # Default styles
    styles = doc.styles
    for style_name in ['Normal']:
        style = styles[style_name]
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        style.font.color.rgb = RGBColor(*OFF_WHITE)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.15

    # Heading styles
    for i, size in enumerate([20, 16, 13, 12], start=1):
        style = styles[f'Heading {i}']
        style.font.name = 'Arial'
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(*GOLD)
        style.font.bold = True
        style.paragraph_format.space_before = Pt(14)
        style.paragraph_format.space_after = Pt(8)

    # Cover page (black background via table trick)
    cover_table = doc.add_table(rows=1, cols=1)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_cell = cover_table.cell(0, 0)
    cover_cell.width = Inches(6)
    set_cell_shading(cover_cell, BLACK)
    set_cell_border(cover_cell, GOLD, size='12')

    cover_para = cover_cell.paragraphs[0]
    cover_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover_para.add_run('\n\nCOMMUNITY BOARD GAME\nLENDING LIBRARY\n')
    set_run_font(run, name='Arial', size=28, color=GOLD, bold=True)

    run = cover_para.add_run('Dart Console Application\n\n')
    set_run_font(run, name='Arial', size=16, color=LIGHT_GOLD, bold=True)

    run = cover_para.add_run('Name: Soumitra Deshpande\n')
    set_run_font(run, size=13, color=OFF_WHITE)
    run = cover_para.add_run('Roll No: 150096724035\n')
    set_run_font(run, size=13, color=OFF_WHITE)
    run = cover_para.add_run('Environment: Dart SDK 3.x\n\n')
    set_run_font(run, size=12, color=OFF_WHITE)

    run = cover_para.add_run('August 2026\n\n')
    set_run_font(run, size=11, color=GOLD)

    doc.add_page_break()

    with open(DOC_PATH, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        # Skip the title line (already on cover)
        if i == 0 and line.startswith('# '):
            i += 1
            continue

        # Code blocks
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                # Code block as styled table
                code_table = doc.add_table(rows=1, cols=1)
                code_table.alignment = WD_TABLE_ALIGNMENT.LEFT
                code_cell = code_table.cell(0, 0)
                code_cell.width = Inches(6)
                set_cell_shading(code_cell, DARK_GRAY)
                set_cell_border(code_cell, GOLD, size='4')
                code_para = code_cell.paragraphs[0]
                run = code_para.add_run('\n'.join(code_lines))
                set_run_font(run, name='Consolas', size=9, color=OFF_WHITE)
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
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                table.style = 'Table Grid'
                hdr_cells = table.rows[0].cells
                for col_idx, cell_text in enumerate(rows[0]):
                    set_cell_shading(hdr_cells[col_idx], GOLD)
                    set_cell_border(hdr_cells[col_idx], GOLD, size='6')
                    hdr_cells[col_idx].text = ''
                    run = hdr_cells[col_idx].paragraphs[0].add_run(cell_text)
                    set_run_font(run, bold=True, color=BLACK)
                for row in rows[1:]:
                    row_cells = table.add_row().cells
                    for col_idx, cell_text in enumerate(row):
                        set_cell_shading(row_cells[col_idx], DARK_GRAY)
                        set_cell_border(row_cells[col_idx], GOLD, size='4')
                        row_cells[col_idx].text = ''
                        run = row_cells[col_idx].paragraphs[0].add_run(cell_text)
                        set_run_font(run, color=OFF_WHITE)
            continue

        # Images
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img_match:
            alt, path = img_match.groups()
            caption = doc.add_paragraph()
            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = caption.add_run(alt)
            set_run_font(run, size=10, color=GOLD, bold=True)
            try:
                doc.add_picture(IMG_PATH, width=Inches(5.8))
                last_paragraph = doc.paragraphs[-1]
                last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception as e:
                err = doc.add_paragraph()
                run = err.add_run(f'[Image not inserted: {path} - {e}]')
                set_run_font(run, color=(255, 0, 0))
            i += 1
            continue

        # Regular paragraphs
        if line.strip():
            p = doc.add_paragraph()
            add_formatted_text(p, line)

        i += 1

    doc.save(OUT_PATH)
    print(f'Saved {OUT_PATH}')


if __name__ == '__main__':
    build_doc()
