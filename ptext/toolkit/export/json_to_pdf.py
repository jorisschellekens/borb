#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class converts JSON to PDF.
    The JSON document defines the layout elements, their nesting (e.g. paragraphs in tables) and their position.
"""
import logging
import typing
from decimal import Decimal

from ptext.io.read.types import Dictionary, Name, String
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.layout_element import LayoutElement, Alignment
from ptext.pdf.canvas.layout.list import OrderedList, UnorderedList
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.canvas.line_art.blob_factory import BlobFactory
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page

logger = logging.getLogger(__name__)


class JSONToPDF:
    """
    This class converts JSON to PDF.
    The JSON document defines the layout elements, their nesting (e.g. paragraphs in tables) and their position.
    """

    @staticmethod
    def _add_to_parent(
        layout_element: LayoutElement,
        json_params: dict,
        page: typing.Optional[Page],
        layout: typing.Optional[typing.Union[SingleColumnLayout, MultiColumnLayout]],
        list: typing.Optional[typing.Union[UnorderedList, OrderedList]],
        table: typing.Optional[Table],
    ):
        # page
        if layout is None and list is None and table is None:
            logger.debug("adding %s to Page" % layout_element.__class__.__name__)
            assert page is not None
            assert "bounding_box" in json_params
            assert isinstance(json_params["bounding_box"], typing.List)
            assert len(json_params["bounding_box"]) == 4
            bounding_box = Rectangle(
                Decimal(json_params["bounding_box"][0]),
                Decimal(json_params["bounding_box"][1]),
                Decimal(json_params["bounding_box"][2]),
                Decimal(json_params["bounding_box"][3]),
            )
            layout_element.layout(page, bounding_box)
            return layout_element

        # layout
        if layout is not None:
            logger.debug(
                "adding %s to %s"
                % (layout_element.__class__.__name__, layout.__class__.__name__)
            )
            layout.add(layout_element)
            return layout_element

        # list
        if list is not None:
            logger.debug(
                "adding %s to %s"
                % (layout_element.__class__.__name__, list.__class__.__name__)
            )
            list.add(layout_element)
            return layout_element

        # table
        if table is not None:
            logger.debug("adding %s to Table" % layout_element.__class__.__name__)
            row_span = int(json_params.get("row_span", "1"))
            col_span = int(json_params.get("col_span", "1"))
            border_top = bool(json_params.get("border_top", "True"))
            border_right = bool(json_params.get("border_right", "True"))
            border_bottom = bool(json_params.get("border_bottom", "True"))
            border_left = bool(json_params.get("border_left", "True"))
            background_color = (
                HexColor(json_params["background_color"])
                if "background_color" in json_params
                else None
            )
            cell = TableCell(
                layout_element,
                row_span=row_span,
                col_span=col_span,
                background_color=background_color,
                border_top=border_top,
                border_right=border_right,
                border_bottom=border_bottom,
                border_left=border_left,
            )
            table.add(cell)
            return cell

    @staticmethod
    def _convert_element(
        json_root,
        parent_doc: typing.Optional[Document] = None,
        parent_page: typing.Optional[Page] = None,
        parent_layout: typing.Optional[
            typing.Union[SingleColumnLayout, MultiColumnLayout]
        ] = None,
        parent_table: typing.Optional[Table] = None,
        parent_list: typing.Optional[typing.Union[OrderedList, UnorderedList]] = None,
    ) -> typing.Any:
        assert isinstance(json_root, dict)
        k, v = [x for x in json_root.items()][0]

        if k == "document":
            assert isinstance(v, dict)
            doc = Document()
            for page in v["body"]:
                JSONToPDF._convert_element(page, parent_doc=doc)
            # info
            doc["XRef"]["Trailer"][Name("Info")] = Dictionary()
            doc["XRef"]["Trailer"]["Info"][Name("Author")] = String(v.get("author", ""))
            doc["XRef"]["Trailer"]["Info"][Name("Producer")] = String(
                v.get("producer", "pText")
            )
            doc["XRef"]["Trailer"]["Info"][Name("Producer")] = String(
                v.get("producer", "")
            )
            doc["XRef"]["Trailer"]["Info"][Name("Keywords")] = String(
                v.get("keywords", "")
            )
            return doc

        elif k == "page":
            assert parent_doc is not None
            w = (
                Decimal(v["width"])
                if isinstance(v, dict) and "width" in v
                else Decimal(595)
            )
            h = (
                Decimal(v["height"])
                if isinstance(v, dict) and "height" in v
                else Decimal(842)
            )
            page = Page(width=w, height=h)
            logger.debug("adding Page to Document")
            parent_doc.append_page(page)
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_page=page)
            return page

        elif k == "single_column_layout":
            assert parent_page is not None
            logger.debug("adding SingleColumnLayout to Page")
            single_column_layout = SingleColumnLayout(parent_page)
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_layout=single_column_layout)
            return single_column_layout

        elif k == "2_column_layout":
            assert parent_page is not None
            logger.debug("adding MultiColumnLayout to Page")
            multi_column_layout = MultiColumnLayout(parent_page)
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_layout=multi_column_layout)
            return multi_column_layout

        elif k == "3_column_layout":
            assert parent_page is not None
            logger.debug("adding MultiColumnLayout to Page")
            layout = MultiColumnLayout(parent_page, number_of_columns=3)
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_layout=layout)
            return layout

        elif k == "paragraph":
            text = v["text"]
            font_size = Decimal(v.get("font_size", "12"))
            font_family = v.get("font_family", "Helvetica")
            font_color = HexColor(v.get("font_color", "#000000"))
            text_alignment = Alignment[v.get("text_alignment", "LEFT")]
            background_color = (
                HexColor(v.get("background_color")) if "background_color" in v else None
            )
            paragraph = Paragraph(
                text=text,
                font_size=font_size,
                font=font_family,
                font_color=font_color,
                background_color=background_color,
                text_alignment=text_alignment,
            )
            return JSONToPDF._add_to_parent(
                paragraph,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

        elif k == "table":
            number_of_rows = int(v["number_of_rows"])
            number_of_columns = int(v["number_of_columns"])
            border_top = None
            border_right = None
            border_bottom = None
            border_left = None
            borders_explictly_set = False
            if (
                "border_top" in v
                or "border_right" in v
                or "border_bottom" in v
                or "border_left" in v
            ):
                borders_explictly_set = True
                border_top = bool(v.get("border_top", "True"))
                border_right = bool(v.get("border_right", "True"))
                border_bottom = bool(v.get("border_bottom", "True"))
                border_left = bool(v.get("border_left", "True"))
            table = Table(
                number_of_rows=number_of_rows, number_of_columns=number_of_columns
            )
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_table=table)
            table.set_padding_on_all_cells(
                Decimal(5), Decimal(5), Decimal(5), Decimal(5)
            )
            if borders_explictly_set:
                assert border_top is not None
                assert border_right is not None
                assert border_bottom is not None
                assert border_left is not None
                table.set_borders_on_all_cells(
                    border_top, border_right, border_bottom, border_left
                )
            return JSONToPDF._add_to_parent(
                table,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

        elif k == "unordered_list":
            unordered_list = UnorderedList()
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_list=unordered_list)
            return JSONToPDF._add_to_parent(
                unordered_list,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

        elif k == "ordered_list":
            ordered_list = OrderedList()
            for e in v["body"]:
                JSONToPDF._convert_element(e, parent_list=ordered_list)
            return JSONToPDF._add_to_parent(
                ordered_list,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

        elif k == "image":
            image_url = v["image_url"]
            width = Decimal(v["width"]) if "width" in v else None
            height = Decimal(v["width"]) if "width" in v else None
            image = Image(image_url, width=width, height=height)
            return JSONToPDF._add_to_parent(
                image,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

        elif k == "layout_column_break":
            assert parent_layout is not None
            assert isinstance(parent_layout, MultiColumnLayout)
            parent_layout.switch_to_next_column()
            return None

        elif k == "barcode":
            data = v["data"]
            stroke_color = HexColor(v.get("stroke_color", "#000000"))
            fill_color = HexColor(v.get("fill_color", "#ffffff"))
            width = Decimal(v["width"]) if "width" in v else None
            height = Decimal(v["height"]) if "height" in v else None
            barcode_type = v["type"]
            barcode = Barcode(
                data=data,
                type=BarcodeType[barcode_type],
                stroke_color=stroke_color,
                fill_color=fill_color,
                width=width,
                height=height,
            )
            return JSONToPDF._add_to_parent(
                barcode,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

        elif k == "shape" and "name" in v:
            stroke_color = HexColor(v.get("stroke_color", "#000000"))
            fill_color = HexColor(v.get("fill_color", "#ffffff"))
            line_width = Decimal(v.get("line_width", "1"))
            shape_name = v["name"]
            shape_bounding_box = Rectangle(
                Decimal(0), Decimal(0), Decimal(100), Decimal(100)
            )
            shape_points = {
                # arrows
                "arrow_left": LineArtFactory.arrow_left(shape_bounding_box),
                "arrow_right": LineArtFactory.arrow_right(shape_bounding_box),
                "arrow_up": LineArtFactory.arrow_up(shape_bounding_box),
                "arrow_down": LineArtFactory.arrow_down(shape_bounding_box),
                # regular n-gons
                "pentagon": LineArtFactory.pentagon(shape_bounding_box),
                "5_gon": LineArtFactory.pentagon(shape_bounding_box),
                "hexagon": LineArtFactory.hexagon(shape_bounding_box),
                "6_gon": LineArtFactory.hexagon(shape_bounding_box),
                "heptagon": LineArtFactory.heptagon(shape_bounding_box),
                "7_gon": LineArtFactory.heptagon(shape_bounding_box),
                "octagon": LineArtFactory.octagon(shape_bounding_box),
                "8_gon": LineArtFactory.octagon(shape_bounding_box),
                # stars
                "5_pointed_star": LineArtFactory.five_pointed_star(shape_bounding_box),
                "6_pointed_star": LineArtFactory.six_pointed_star(shape_bounding_box),
                "7_pointed_star": LineArtFactory.n_pointed_star(shape_bounding_box, 7),
                "8_pointed_star": LineArtFactory.n_pointed_star(shape_bounding_box, 8),
                # fractions of circle
                "quarter_circle": LineArtFactory.fraction_of_circle(
                    shape_bounding_box, Decimal(0.25)
                ),
                "half_circle": LineArtFactory.fraction_of_circle(
                    shape_bounding_box, Decimal(0.5)
                ),
                "three_quarter_circle": LineArtFactory.fraction_of_circle(
                    shape_bounding_box, Decimal(0.75)
                ),
                "circle": LineArtFactory.circle(shape_bounding_box),
                # blob
                "blob": BlobFactory.blob(3),
                "3_sided_blob": BlobFactory.blob(3),
                "4_sided_blob": BlobFactory.blob(4),
                "5_sided_blob": BlobFactory.blob(5),
                "6_sided_blob": BlobFactory.blob(6),
                # misc.
                "cross": LineArtFactory.cross(shape_bounding_box),
                "droplet": LineArtFactory.droplet(shape_bounding_box),
                "heart": LineArtFactory.heart(shape_bounding_box),
                "sticky_note": LineArtFactory.sticky_note(shape_bounding_box),
                # flowchart
                "flowchart_card": LineArtFactory.flowchart_card(shape_bounding_box),
                "flowchart_collate": LineArtFactory.flowchart_collate(
                    shape_bounding_box
                ),
                "flowchart_data": LineArtFactory.flowchart_data(shape_bounding_box),
                "flowchart_database": LineArtFactory.flowchart_database(
                    shape_bounding_box
                ),
                "flowchart_decision": LineArtFactory.flowchart_decision(
                    shape_bounding_box
                ),
                "flowchart_delay": LineArtFactory.flowchart_delay(shape_bounding_box),
                "flowchart_direct_data": LineArtFactory.flowchart_direct_data(
                    shape_bounding_box
                ),
                "flowchart_document": LineArtFactory.flowchart_document(
                    shape_bounding_box
                ),
                "flowchart_extract": LineArtFactory.flowchart_extract(
                    shape_bounding_box
                ),
                "flowchart_internal_storage": LineArtFactory.flowchart_internal_storage(
                    shape_bounding_box
                ),
                "flowchart_loop_limit": LineArtFactory.flowchart_loop_limit(
                    shape_bounding_box
                ),
                "flowchart_manual_input": LineArtFactory.flowchart_manual_input(
                    shape_bounding_box
                ),
                "flowchart_manual_operation": LineArtFactory.flowchart_manual_operation(
                    shape_bounding_box
                ),
                "flowchart_merge": LineArtFactory.flowchart_merge(shape_bounding_box),
                "flowchart_multiple_documents": LineArtFactory.flowchart_multiple_documents(
                    shape_bounding_box
                ),
                "flowchart_off_page_reference": LineArtFactory.flowchart_off_page_reference(
                    shape_bounding_box
                ),
                "flowchart_on_page_reference": LineArtFactory.flowchart_on_page_reference(
                    shape_bounding_box
                ),
                "flowchart_or": LineArtFactory.flowchart_or(shape_bounding_box),
                "flowchart_paper_tape": LineArtFactory.flowchart_paper_tape(
                    shape_bounding_box
                ),
                "flowchart_predefined_document": LineArtFactory.flowchart_predefined_document(
                    shape_bounding_box
                ),
                "flowchart_predefined_process": LineArtFactory.flowchart_predefined_process(
                    shape_bounding_box
                ),
                "flowchart_process": LineArtFactory.flowchart_process(
                    shape_bounding_box
                ),
                "flowchart_process_iso_9000": LineArtFactory.flowchart_process_iso_9000(
                    shape_bounding_box
                ),
                "flowchart_sort": LineArtFactory.flowchart_sort(shape_bounding_box),
                "flowchart_summing_junction": LineArtFactory.flowchart_summing_junction(
                    shape_bounding_box
                ),
                "flowchart_termination": LineArtFactory.flowchart_termination(
                    shape_bounding_box
                ),
                "flowchart_transport": LineArtFactory.flowchart_transport(
                    shape_bounding_box
                ),
            }[shape_name]
            shape = Shape(
                points=shape_points,
                stroke_color=stroke_color,
                fill_color=fill_color,
                line_width=line_width,
            )
            shape.scale_up(Decimal(100), Decimal(100))
            return JSONToPDF._add_to_parent(
                shape,
                json_params=v,
                page=parent_page,
                layout=parent_layout,
                list=parent_list,
                table=parent_table,
            )

    @staticmethod
    def convert_json_to_pdf(json_root) -> Document:
        """
        This function converts a JSON document to a PDF Document
        """
        return JSONToPDF._convert_element(json_root)
