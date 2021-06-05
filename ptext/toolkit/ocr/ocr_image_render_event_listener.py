from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle

try:
    import pytesseract  # type: ignore [import]
    from pytesseract import Output  # type: ignore [import]
except ImportError:
    assert False, "Unable to import pytesseract"


class OCRImageRenderEventListener(EventListener):
    """
    This implementation of EventListener attempts to perform OCR on Image objects inside a PDF.
    If text has been found, OCRImageRenderEventListener will add optional content to ensure
    the PDF can now be searched for the recognized text.
    """

    def __init__(
        self, tesseract_data_dir: Path, minimal_confidence: Decimal = Decimal(0.75)
    ):
        assert tesseract_data_dir.exists()
        assert tesseract_data_dir.is_dir()
        self._tesseract_data_dir: Path = tesseract_data_dir
        self._minimal_confidence: Decimal = minimal_confidence

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ImageRenderEvent):
            data = pytesseract.image_to_data(
                event.get_image(),
                lang="eng",
                config='--tessdata-dir "%s"' % str(self._tesseract_data_dir.absolute()),
                output_type=Output.DICT,
            )
            number_of_boxes: int = len(data["level"])
            for i in range(0, number_of_boxes):

                # convert bounding box to Rectangle object
                bounding_box: Rectangle = Rectangle(
                    Decimal(data["left"][i]),
                    Decimal(data["top"][i]),
                    Decimal(data["width"][i]),
                    Decimal(data["height"][i]),
                )

                # get text in bounding box
                text_in_bounding_box: str = data["text"][i]
                if text_in_bounding_box.strip() == "":
                    continue

                # get confidence
                confidence: Decimal = Decimal(data["conf"][i])
                if confidence < self._minimal_confidence:
                    continue

                # delegate call
                self._ocr_text_occurred(bounding_box, text_in_bounding_box, confidence)

    def _ocr_text_occurred(
        self, bounding_box: Rectangle, text: str, confidence: Decimal
    ):
        pass
