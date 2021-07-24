#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts tables from a PDF Document
"""
import typing

from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.layout.table.base_table import BaseTable
from borb.toolkit.structure.simple_paragraph_extraction import (
    SimpleParagraphExtraction,
)


class SimpleTableExtraction(SimpleParagraphExtraction):
    """
    This implementation of EventListener extracts tables from a PDF Document
    """

    def __init__(self):
        super(SimpleTableExtraction, self).__init__()
        self._chunks_of_text: typing.List[ChunkOfTextRenderEvent] = []
        self._minimum_number_of_rows: int = 2
        self._minimum_number_of_cols: int = 2
        self._tables_per_page: typing.Dict[int, typing.List[BaseTable]] = {}
