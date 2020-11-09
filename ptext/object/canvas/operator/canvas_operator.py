from typing import List

from ptext.primitive.pdf_object import PDFObject


class CanvasOperator:
    def __init__(self, text: str, number_of_operands: int):
        self.text = text
        self.number_of_operands = number_of_operands

    def get_text(self) -> str:
        return self.text

    def get_number_of_operands(self) -> int:
        return self.number_of_operands

    def invoke(self, canvas: "PDFCanvas", operands: List[PDFObject] = []):
        pass
