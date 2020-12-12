from typing import Union

from ptext.io.tokenize.types.pdf_object import PDFObject


class PDFBoolean(PDFObject):
    """
    Boolean objects represent the logical values of true and false. They appear in PDF files using the keywords
    true and false.
    """

    def __init__(self, val: Union[str, bool]):
        super().__init__()
        self.value = False
        if isinstance(val, str):
            self.value = True if val in ["true", "True"] else False
        if isinstance(val, bool):
            self.value = val

    def __eq__(self, other):
        return other.value == self.value if isinstance(other, PDFBoolean) else False

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return "true" if self.value else "false"
