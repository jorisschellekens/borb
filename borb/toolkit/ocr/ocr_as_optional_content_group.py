#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class adds performs OCR and adds recognized text in an optional content group on the PDF.
    This enables the user to have a searchable PDF, whilst being able to turn on/off OCR features.
"""
# FIX: circular imports (1/2)
from __future__ import annotations

import datetime
import typing
import zlib
from decimal import Decimal
import pathlib

# FIX: circular imports (2/2)
from typing import TYPE_CHECKING

from borb.datastructure.disjoint_set import disjointset
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.ocr.ocr_image_render_event_listener import OCREvent
from borb.toolkit.ocr.ocr_image_render_event_listener import OCRImageRenderEventListener

EndDocumentEvent = type(None)
if TYPE_CHECKING:
    pass


class OCRAsOptionalContentGroup(OCRImageRenderEventListener):
    """
    This class adds performs OCR and adds recognized text in an optional content group on the PDF.
    This enables the user to have a searchable PDF, whilst being able to turn on/off OCR features.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        tesseract_data_dir: pathlib.Path,
        minimal_confidence: Decimal = Decimal(0.75),
    ):
        super(OCRAsOptionalContentGroup, self).__init__(
            tesseract_data_dir, minimal_confidence
        )
        self._ocr_events: typing.List[OCREvent] = []

    #
    # PRIVATE
    #

    def _add_ocr_optional_content_group(self, document: Document) -> None:
        # add OCProperties to Document (if needed)
        if "OCProperties" not in document["XRef"]["Trailer"]["Root"]:
            # The optional OCProperties entry in the document catalog (see 7.7.2, "Document Catalog") shall contain, when
            # present, the optional content properties dictionary, which contains a list of all the optional content groups in the
            # document, as well as information about the default and alternate configurations for optional content.
            document["XRef"]["Trailer"]["Root"][Name("OCProperties")] = Dictionary()

            # (Required) An array of indirect references to all the optional content
            # groups in the document (see 8.11.2, "Optional Content Groups"), in any
            # order. Every optional content group shall be included in this array.
            document["XRef"]["Trailer"]["Root"]["OCProperties"][Name("OCGs")] = List()

            # (Required) The default viewing optional content configuration dictionary
            # (see 8.11.4.3, "Optional Content Configuration Dictionaries").
            document["XRef"]["Trailer"]["Root"]["OCProperties"][
                Name("D")
            ] = Dictionary()

        # create an Optional Content Group Dictionary
        ocg_dict: Dictionary = Dictionary()
        ocg_dict[Name("Type")] = Name("OCG")
        ocg_dict[Name("Name")] = String("OCR by borb")
        ocg_dict[Name("Intent")] = Name("View")
        document["XRef"]["Trailer"]["Root"]["OCProperties"][Name("OCGs")].append(
            ocg_dict
        )

        # add to /Resources Dictionary of the Page
        now = datetime.datetime.now()
        ocr_layer_internal_name: str = "ocr%d%d%d" % (now.year, now.month, now.day)
        number_of_pages: typing.Optional[
            Decimal
        ] = document.get_document_info().get_number_of_pages()
        assert number_of_pages is not None
        for page_nr in range(0, int(number_of_pages)):
            page: Page = document.get_page(page_nr)
            if "Resources" not in page:
                page[Name("Resources")] = Dictionary
            if "Properties" not in page["Resources"]:
                page["Resources"][Name("Properties")] = Dictionary()
            page["Resources"]["Properties"][Name(ocr_layer_internal_name)] = ocg_dict

            # do nothing if no events are processed for this Page
            # fmt: off
            ocr_events_per_page: typing.List[OCREvent] = [x for x in self._ocr_events if x.get_page() == page]
            if len(ocr_events_per_page) == 0:
                continue
            # fmt: on

            # re-align events
            # fmt: off
            ds: disjointset = disjointset()
            for e in ocr_events_per_page:
                ds.add(e)
            for e1 in ocr_events_per_page:
                for e2 in ocr_events_per_page:
                    if e1 == e2:
                        continue
                    if self._overlaps_vertically(e1.get_bounding_box(), e2.get_bounding_box()):
                        ds.union(e1, e2)
            for es in ds.sets():
                avg_y: Decimal = Decimal(sum([x.get_bounding_box().get_y() for x in es]) / len(es))
                for e in es:
                    e.get_bounding_box().y = avg_y
            # fmt: on

            # change Page content stream
            # fmt: off
            page["Contents"][Name("DecodedBytes")] += ("\n/OC /%s BDC\n" % ocr_layer_internal_name).encode("latin1")
            for e in ocr_events_per_page:
                ChunkOfText(e.get_text(),
                            e.get_font(),
                            e.get_font_size(),
                            e.get_font_color()).paint(page, e.get_bounding_box())
            page["Contents"][Name("DecodedBytes")] += "\nEMC".encode("latin1")
            page["Contents"][Name("Bytes")] = zlib.compress(page["Contents"]["DecodedBytes"], 9)
            page["Contents"][Name("Length")] = bDecimal(len(page["Contents"][Name("Bytes")]))
            # fmt: on

    def _end_document(self):
        if len(self._ocr_events) == 0:
            return
        document: Document = self._ocr_events[0].get_page().get_document()
        self._add_ocr_optional_content_group(document)

    def _event_occurred(self, event: Event) -> None:
        super(OCRAsOptionalContentGroup, self)._event_occurred(event)
        # TODO: find a better way to solve this
        if event.__class__.__name__ == "EndDocumentEvent":
            self._end_document()

    def _ocr_text_occurred(self, event: OCREvent):
        self._ocr_events.append(event)

    def _overlaps_vertically(self, r0: Rectangle, r1: Rectangle) -> bool:
        """
        This function returns True iff two Rectangle objects overlap vertically, False otherwise.
        """
        return (
            int(r0.get_y()) <= int(r1.get_y()) <= int(r0.get_y() + r0.get_height())
        ) or (int(r1.get_y()) <= int(r0.get_y()) <= int(r1.get_y() + r1.get_height()))

    #
    # PUBLIC
    #
