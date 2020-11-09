from ptext.primitive.pdf_object import PDFObject


class PDFNull(PDFObject):
    """
    A single object of type null, denoted by the keyword null, and having a type and value that are unequal to those
    of any other object
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "null"

    def __eq__(self, other):
        return isinstance(other, PDFNull)
