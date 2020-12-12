from decimal import Decimal
from typing import Union

from ptext.io.tokenize.types.pdf_object import PDFObject


class PDFNumber(PDFObject):
    """
    PDF provides two types of numeric objects: integer and real. Integer objects represent mathematical integers.
    Real objects represent mathematical real numbers. The range and precision of numbers may be limited by the
    internal representations used in the computer on which the conforming reader is running; Annex C gives these
    limits for typical implementations.
    """

    def __init__(self, value: Union[int, float]):
        super().__init__()
        self.value = value

    def get_float_value(self):
        return float(self.value)

    def get_int_value(self):
        return int(self.value)

    def get_decimal_value(self):
        return Decimal(self.get_float_value())

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return self.value.__hash__()


class PDFInt(PDFNumber):
    """
    An integer shall be written as one or more decimal digits optionally preceded by a sign. The value shall be
    interpreted as a signed decimal integer and shall be converted to an integer object.
    """

    def __init__(self, value: int):
        super().__init__(value)

    def set_int_value(self, value: int):
        self.value = value
        return self

    def __eq__(self, other):
        return isinstance(other, PDFInt) and other.value == self.value

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return self.value.__hash__()


class PDFFloat(PDFNumber):
    """
    A real value shall be written as one or more decimal digits with an optional sign and a leading, trailing, or
    embedded PERIOD (2Eh) (decimal point). The value shall be interpreted as a real number and shall be
    converted to a real object.
    """

    def __init__(self, value: float):
        super().__init__(value)

    def set_float_value(self, value: float):
        self.value = value
        return self

    def __eq__(self, other):
        return isinstance(other, PDFFloat) and other.value == self.value

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return self.value.__hash__()
