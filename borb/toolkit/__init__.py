"""
    This file is part of the borb (TM) project.
    Copyright (c) 2020-2040 borb (EZ)
    Authors: Joris Schellekens, et al.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License version 3
    as published by the Free Software Foundation with the addition of the
    following permission added to Section 15 as permitted in Section 7(a):
    FOR ANY PART OF THE COVERED WORK IN WHICH THE COPYRIGHT IS OWNED BY
    BORB GROUP. BORB GROUP DISCLAIMS THE WARRANTY OF NON INFRINGEMENT
    OF THIRD PARTY RIGHTS

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.

    See the GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program; if not, see http://www.gnu.org/licenses or write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA, 02110-1301 USA.

    The interactive user interfaces in modified source and object code versions
    of this program must display Appropriate Legal Notices, as required under
    Section 5 of the GNU Affero General Public License.
    In accordance with Section 7(b) of the GNU Affero General Public License,
    a covered work must retain the producer line in every PDF that is created
    or manipulated using borb.

    You can be released from the requirements of the license by purchasing
    a commercial license. Buying such a license is mandatory as soon as you
    develop commercial activities involving the borb software without
    disclosing the source code of your own applications.

    These activities include: offering paid services to customers as an ASP,
    serving PDFs on the fly in a web application, shipping borb with a closed
    source product.

    For more information, please contact borb Software Corp. at this
    address: joris.schellekens.1989@gmail.com
"""

# color
from .color.color_extraction import ColorExtraction

# export
from .export.html_to_pdf.html_to_pdf import HTMLToPDF

try:
    from .export.markdown_to_pdf.markdown_to_pdf import MarkdownToPDF
except:
    pass
try:
    from .export.pdf_to_mp3 import PDFToMP3
except:
    pass
from .export.pdf_to_jpg import PDFToJPG
from .export.pdf_to_svg import PDFToSVG

# image
from .image.image_extraction import ImageExtraction
from .image.image_format_optimization import ImageFormatOptimization

# location
from .location.location_filter import LocationFilter

# ocr
try:
    from .ocr.ocr_as_optional_content_group import OCRAsOptionalContentGroup
    from .ocr.ocr_image_render_event_listener import (
        OCREvent,
        OCRImageRenderEventListener,
    )
except:
    pass

# table
from .table.table_detection_by_lines import TableDetectionByLines

# text
from .text.simple_text_extraction import SimpleTextExtraction
from .text.simple_non_ligature_text_extraction import SimpleNonLigatureTextExtraction
from .text.simple_find_replace import SimpleFindReplace

# text (structure)
from .text.simple_paragraph_extraction import SimpleParagraphExtraction
from .text.simple_line_of_text_extraction import SimpleLineOfTextExtraction
from .text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
    PDFMatch,
)

# text (filter)
from .text.font_color_filter import FontColorFilter
from .text.font_extraction import FontExtraction
from .text.font_name_filter import FontNameFilter

# text (keywords, NLP)
try:
    from .text.text_rank_keyword_extraction import TextRankKeywordExtraction
except:
    pass
from .text.tf_idf_keyword_extraction import TFIDFKeywordExtraction
from .text.stop_words import FRENCH_STOP_WORDS, ENGLISH_STOP_WORDS
