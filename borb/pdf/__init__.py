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

# fmt: off
from .canvas.color.color import CMYKColor
from .canvas.color.color import Color
from .canvas.color.color import GrayColor
from .canvas.color.color import HexColor
from .canvas.color.color import HSVColor
from .canvas.color.color import RGBColor
from .canvas.color.color import X11Color
from .canvas.color.farrow_and_ball import FarrowAndBall
from .canvas.color.pantone import Pantone
from .canvas.font.google_true_type_font import GoogleTrueTypeFont
from .canvas.font.simple_font.font_type_1 import StandardType1Font
from .canvas.font.simple_font.true_type_font import TrueTypeFont
from .canvas.layout.annotation.annotation import Annotation
from .canvas.layout.annotation.caret_annotation import CaretAnnotation
from .canvas.layout.annotation.circle_annotation import CircleAnnotation
from .canvas.layout.annotation.file_attachment_annotation import FileAttachmentAnnotation
from .canvas.layout.annotation.free_text_annotation import FreeTextAnnotation
from .canvas.layout.annotation.highlight_annotation import HighlightAnnotation
from .canvas.layout.annotation.ink_annotation import InkAnnotation
from .canvas.layout.annotation.line_annotation import LineAnnotation
from .canvas.layout.annotation.link_annotation import LinkAnnotation
from .canvas.layout.annotation.movie_annotation import MovieAnnotation
from .canvas.layout.annotation.polygon_annotion import PolygonAnnotation
from .canvas.layout.annotation.polyline_annotation import PolylineAnnotation
from .canvas.layout.annotation.popup_annotation import PopupAnnotation
from .canvas.layout.annotation.printer_mark_annotation import PrinterMarkAnnotation
from .canvas.layout.annotation.redact_annotation import RedactAnnotation
from .canvas.layout.annotation.remote_go_to_annotation import RemoteGoToAnnotation
from .canvas.layout.annotation.rubber_stamp_annotation import RubberStampAnnotation
from .canvas.layout.annotation.screen_annotation import ScreenAnnotation
from .canvas.layout.annotation.sound_annotation import SoundAnnotation
from .canvas.layout.annotation.square_annotation import SquareAnnotation
from .canvas.layout.annotation.squiggly_annotation import SquigglyAnnotation
from .canvas.layout.annotation.strike_out_annotation import StrikeOutAnnotation
from .canvas.layout.annotation.text_annotation import TextAnnotation
from .canvas.layout.annotation.three_d_annotation import ThreeDAnnotation
from .canvas.layout.annotation.trap_net_annotation import TrapNetAnnotation
from .canvas.layout.annotation.underline_annotation import UnderlineAnnotation
from .canvas.layout.annotation.watermark_annotation import WatermarkAnnotation
from .canvas.layout.annotation.widget_annotation import WidgetAnnotation
from .canvas.layout.emoji.emoji import Emoji
from .canvas.layout.emoji.emoji import Emojis
from .canvas.layout.equation.equation import Equation
from .canvas.layout.forms.check_box import CheckBox
from .canvas.layout.forms.country_drop_down_list import CountryDropDownList
from .canvas.layout.forms.drop_down_list import DropDownList
from .canvas.layout.forms.form_field import FormField
from .canvas.layout.forms.push_button import JavaScriptPushButton
from .canvas.layout.forms.push_button import PushButton
from .canvas.layout.forms.text_area import TextArea
from .canvas.layout.forms.text_field import TextField
from .canvas.layout.geography.map_of_europe import MapOfEurope
from .canvas.layout.geography.map_of_the_united_states import MapOfTheUnitedStates
from .canvas.layout.geography.map_of_the_world import MapOfTheWorld
from .canvas.layout.hyphenation.hyphenation import Hyphenation
from .canvas.layout.image.barcode import Barcode
from .canvas.layout.image.barcode import BarcodeType
from .canvas.layout.image.chart import Chart
from .canvas.layout.image.image import Image
from .canvas.layout.image.screenshot import ScreenShot
from .canvas.layout.image.unsplash import Unsplash
from .canvas.layout.image.watermark import Watermark
from .canvas.layout.layout_element import Alignment
from .canvas.layout.list.list import List
from .canvas.layout.list.ordered_list import OrderedList
from .canvas.layout.list.roman_numeral_ordered_list import RomanNumeralOrderedList
from .canvas.layout.list.unordered_list import UnorderedList
from .canvas.layout.page_layout.block_flow import BlockFlow
from .canvas.layout.page_layout.inline_flow import InlineFlow
from .canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
from .canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from .canvas.layout.page_layout.multi_column_layout import ThreeColumnLayout
from .canvas.layout.page_layout.multi_column_layout import TwoColumnLayout
from .canvas.layout.page_layout.page_layout import PageLayout
from .canvas.layout.page_layout.single_column_layout_with_overflow import SingleColumnLayoutWithOverflow
from .canvas.layout.shape.connected_shape import ConnectedShape
from .canvas.layout.shape.disconnected_shape import DisconnectedShape
from .canvas.layout.shape.gradient_colored_disconnected_shape import GradientColoredDisconnectedShape
from .canvas.layout.shape.progressbar import ProgressBar
from .canvas.layout.shape.progressbar import ProgressSquare
from .canvas.layout.shape.shapes import Shapes
from .canvas.layout.smart_art.smart_art import SmartArt
from .canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from .canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from .canvas.layout.table.table import Table
from .canvas.layout.table.table import TableCell
from .canvas.layout.table.table_util import TableUtil
from .canvas.layout.text.chunk_of_text import ChunkOfText
from .canvas.layout.text.codeblock import CodeBlock
from .canvas.layout.text.codeblock_with_syntax_highlighting import CodeBlockWithSyntaxHighlighting
from .canvas.layout.text.heading import Heading
from .canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from .canvas.layout.text.line_of_text import LineOfText
from .canvas.layout.text.paragraph import Paragraph
from .canvas.line_art.line_art_factory import LineArtFactory
from .canvas.lipsum.lipsum import Lipsum
from .document.document import Document
from .page.page import Page
from .pdf import PDF
from .template.a4_2_column_portrait_template import A42ColumnPortraitTemplate
from .template.a4_portrait_invoice_template import A4PortraitInvoiceTemplate
from .template.a4_portrait_resume_template import A4PortraitResumeTemplate
from .template.a4_portrait_template import A4PortraitTemplate
from .template.slide_template import SlideTemplate
# fmt: on
