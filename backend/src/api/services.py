import io
from pathlib import Path

from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.page_layout.multi_column_layout import (
    SingleColumnLayout,)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

from foodgram.settings import FONT_NAME, STATIC_ROOT


def create_pdf(shop_list):
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    layout = SingleColumnLayout(page)
    font_path: Path = Path(STATIC_ROOT) / FONT_NAME
    font: Font = TrueTypeFont.true_type_font_from_file(font_path)
    for item in shop_list:
        text = (f'• {item["ingredient__name"]} '
                f'({item["ingredient__measurement_unit"]}) - '
                f'{item["amount__sum"]}')
        layout.add(Paragraph(text, font=font))
    buffer = io.BytesIO()
    PDF.dumps(buffer, pdf)
    buffer.seek(0)
    return buffer
