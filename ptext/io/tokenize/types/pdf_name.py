import enum

from ptext.io.tokenize.types.pdf_object import PDFObject


class PDFName(PDFObject):
    """
    Beginning with PDF 1.2 a name object is an atomic symbol uniquely defined by a sequence of any characters
    (8-bit values) except null (character code 0). Uniquely defined means that any two name objects made up of
    the same sequence of characters denote the same object. Atomic means that a name has no internal structure;
    although it is defined by a sequence of characters, those characters are not considered elements of the name.
    """

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __eq__(self, other):
        if isinstance(other, enum.Enum):
            return other.value == self
        return isinstance(other, PDFName) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "/" + self.name
