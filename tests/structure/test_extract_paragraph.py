import logging

from ptext.functionality.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)
from ptext.functionality.structure.simple_structure_extraction import (
    SimpleStructureExtraction,
)
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../smoke/test-extract-first-paragraph.log", level=logging.DEBUG
)


class MyListener(EventListener):
    def event_occurred(self, event: Event) -> None:
        if isinstance(event, ParagraphRenderEvent):
            t = event.get_text()
            print(t)


class TestExtractFirstParagraph(Test):
    def test_corpus(self):
        super(TestExtractFirstParagraph, self).test_corpus()

    def test_document(self, file):
        l = MyListener()
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [SimpleStructureExtraction(), l])
        return True
