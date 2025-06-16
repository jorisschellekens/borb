#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from borb.pdf.color.cmyk_color import CMYKColor
from borb.pdf.color.color import Color
from borb.pdf.color.color_scheme import ColorScheme
from borb.pdf.color.farrow_and_ball_color import FarrowAndBallColor
from borb.pdf.color.grayscale_color import GrayscaleColor
from borb.pdf.color.hex_color import HexColor
from borb.pdf.color.hsv_color import HSVColor
from borb.pdf.color.pantone_color import PantoneColor
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.document_layout.a4_portrait import A4Portrait
from borb.pdf.document_layout.a4_portrait_invoice import A4PortraitInvoice
from borb.pdf.document_layout.a4_portrait_resume import A4PortraitResume
from borb.pdf.document_layout.document_layout import DocumentLayout
from borb.pdf.document_layout.slideshow import Slideshow
from borb.pdf.font.composite_font.composite_font import CompositeFont
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.simple_font import SimpleFont
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.font.simple_font.true_type.google_true_type_font import GoogleTrueTypeFont
from borb.pdf.font.simple_font.true_type.true_type_font import TrueTypeFont
from borb.pdf.font.simple_font.type_1_font import Type1Font
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.annotation.circle_annotation import CircleAnnotation
from borb.pdf.layout_element.annotation.free_text_annotation import FreeTextAnnotation
from borb.pdf.layout_element.annotation.highlight_annotation import HighlightAnnotation
from borb.pdf.layout_element.annotation.ink_annotation import InkAnnotation
from borb.pdf.layout_element.annotation.line_annotation import LineAnnotation
from borb.pdf.layout_element.annotation.link_annotation import LinkAnnotation
from borb.pdf.layout_element.annotation.poly_line_annotation import PolyLineAnnotation
from borb.pdf.layout_element.annotation.polygon_annotation import PolygonAnnotation
from borb.pdf.layout_element.annotation.redact_annotation import RedactAnnotation
from borb.pdf.layout_element.annotation.remote_go_to_annotation import RemoteGoToAnnotation
from borb.pdf.layout_element.annotation.rubber_stamp_annotation import RubberStampAnnotation
from borb.pdf.layout_element.annotation.sound_annotation import SoundAnnotation
from borb.pdf.layout_element.annotation.square_annotation import SquareAnnotation
from borb.pdf.layout_element.annotation.squiggly_annotation import SquigglyAnnotation
from borb.pdf.layout_element.annotation.strike_out_annotation import StrikeOutAnnotation
from borb.pdf.layout_element.annotation.text_annotation import TextAnnotation
from borb.pdf.layout_element.form.button import Button
from borb.pdf.layout_element.form.check_box import CheckBox
from borb.pdf.layout_element.form.country_drop_down_list import CountryDropDownList
from borb.pdf.layout_element.form.drop_down_list import DropDownList
from borb.pdf.layout_element.form.form_field import FormField
from borb.pdf.layout_element.form.gender_drop_down_list import GenderDropDownList
from borb.pdf.layout_element.form.javascript_button import JavascriptButton
from borb.pdf.layout_element.form.radio_button import RadioButton
from borb.pdf.layout_element.form.text_area import TextArea
from borb.pdf.layout_element.form.text_box import TextBox
from borb.pdf.layout_element.image.avatar import Avatar
from borb.pdf.layout_element.image.barcode import Barcode
from borb.pdf.layout_element.image.chart import Chart
from borb.pdf.layout_element.image.dall_e import DallE
from borb.pdf.layout_element.image.emoji import Emoji
from borb.pdf.layout_element.image.equation import Equation
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.image.qr_code import QRCode
from borb.pdf.layout_element.image.screenshot import Screenshot
from borb.pdf.layout_element.image.unsplash import Unsplash
from borb.pdf.layout_element.image.watermark import Watermark
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.abc_ordered_list import ABCOrderedList
from borb.pdf.layout_element.list.list import List
from borb.pdf.layout_element.list.ordered_list import OrderedList
from borb.pdf.layout_element.list.roman_numeral_ordered_list import RomanNumeralOrderedList
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.progress_bar.progress_bar import ProgressBar
from borb.pdf.layout_element.progress_bar.progress_square import ProgressSquare
from borb.pdf.layout_element.shape.horizontal_break import HorizontalBreak
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.shape.map import Map
from borb.pdf.layout_element.shape.map_of_africa import MapOfAfrica
from borb.pdf.layout_element.shape.map_of_asia import MapOfAsia
from borb.pdf.layout_element.shape.map_of_europe import MapOfEurope
from borb.pdf.layout_element.shape.map_of_north_america import MapOfNorthAmerica
from borb.pdf.layout_element.shape.map_of_oceania import MapOfOceania
from borb.pdf.layout_element.shape.map_of_south_america import MapOfSouthAmerica
from borb.pdf.layout_element.shape.map_of_the_contiguous_united_states_of_america import MapOfTheContiguousUnitedStatesOfAmerica
from borb.pdf.layout_element.shape.map_of_the_united_states_of_america import MapOfTheUnitedStatesOfAmerica
from borb.pdf.layout_element.shape.map_of_the_world import MapOfTheWorld
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.layout_element.smart_art.smart_art import SmartArt
from borb.pdf.layout_element.space.space import Space
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.table.table_util import TableUtil
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.code_snippet import CodeSnippet
from borb.pdf.layout_element.text.heading import Heading
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.layout_element.text.homogeneous_paragraph import HomogeneousParagraph
from borb.pdf.layout_element.text.markdown_paragraph import MarkdownParagraph
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.license.license import License
from borb.pdf.license.usage_statistics import UsageStatistics
from borb.pdf.license.version import Version
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.page_layout.multi_column_layout import MultiColumnLayout
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.page_layout.three_column_layout import ThreeColumnLayout
from borb.pdf.page_layout.two_column_layout import TwoColumnLayout
from borb.pdf.page_size import PageSize
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.filter.above.above import Above
from borb.pdf.toolkit.filter.above.above_image import AboveImage
from borb.pdf.toolkit.filter.above.above_text import AboveText
from borb.pdf.toolkit.filter.below.below import Below
from borb.pdf.toolkit.filter.below.below_image import BelowImage
from borb.pdf.toolkit.filter.below.below_text import BelowText
from borb.pdf.toolkit.filter.font.by_font import ByFont
from borb.pdf.toolkit.filter.font.by_font_color import ByFontColor
from borb.pdf.toolkit.filter.font.by_font_size import ByFontSize
from borb.pdf.toolkit.filter.inside.inside import Inside
from borb.pdf.toolkit.filter.left.left_of import LeftOf
from borb.pdf.toolkit.filter.left.left_of_image import LeftOfImage
from borb.pdf.toolkit.filter.left.left_of_text import LeftOfText
from borb.pdf.toolkit.filter.page.even_pages import EvenPages
from borb.pdf.toolkit.filter.page.odd_pages import OddPages
from borb.pdf.toolkit.filter.right.right_of import RightOf
from borb.pdf.toolkit.filter.right.right_of_image import RightOfImage
from borb.pdf.toolkit.filter.right.right_of_text import RightOfText
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_colors import GetColors
from borb.pdf.toolkit.sink.get_document_as_graphml import GetDocumentAsGraphML
from borb.pdf.toolkit.sink.get_events_as_json import GetEventsAsJSON
from borb.pdf.toolkit.sink.get_images import GetImages
from borb.pdf.toolkit.sink.get_keywords_by_pagewise_tf_idf import GetKeywordsByPagewiseTFIDF
from borb.pdf.toolkit.sink.get_regular_expression import GetRegularExpression
from borb.pdf.toolkit.sink.get_text import GetText
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.operator.source import Source
from borb.pdf.visitor.pdf import PDF
# fmt: on
