#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts tables from a PDF Document
"""
import typing

from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.layout.table import Table
from ptext.toolkit.structure.simple_paragraph_extraction import (
    SimpleParagraphExtraction,
)


class SimpleTableExtraction(SimpleParagraphExtraction):
    """
    This implementation of EventListener extracts tables from a PDF Document
    """

    def __init__(self):
        super(SimpleTableExtraction, self).__init__()
        self.chunks_of_text: typing.List[ChunkOfTextRenderEvent] = []
        self.minimum_number_of_rows: int = 2
        self.minimum_number_of_cols: int = 2
        self.tables_per_page: typing.Dict[int, typing.List[Table]] = {}
