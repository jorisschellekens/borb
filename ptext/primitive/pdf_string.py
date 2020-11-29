from typing import List

from ptext.object.canvas.font.latin_text_encoding import StandardEncoding
from ptext.primitive.pdf_object import PDFObject


class PDFString(PDFObject):
    """
    A string object shall consist of a series of zero or more bytes. String objects are not integer objects, but are
    stored in a more compact format. The length of a string may be subject to implementation limits; see Annex C.
    """

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def get_text(self) -> str:
        return self.text

    def get_content_bytes(self) -> List[int]:
        return []

    def get_value_bytes(self) -> List[int]:
        # TODO : check parent to determine encoding
        return [StandardEncoding().code_to_unicode(b) for b in self.get_content_bytes()]

    def __eq__(self, other):
        return other.text == self.text if isinstance(other, PDFString) else False

    def __hash__(self):
        return hash(self.text)

    def __len__(self):
        return len(self.text) if self.text is not None else 0


class PDFLiteralString(PDFString):
    """
     As a sequence of literal characters enclosed in parentheses ( ) (using LEFT PARENTHESIS (28h) and
    RIGHT PARENTHESIS (29h)); see 7.3.4.2, "Literal Strings."
    """

    def __init__(self, text: str):
        super().__init__(text)

    def __eq__(self, other) -> bool:
        return other.text == self.text if isinstance(other, PDFLiteralString) else False

    def __str__(self) -> str:
        return "(" + self.text + ")"

    def get_content_bytes(self) -> bytearray:
        txt = ""
        i = 0
        while i < len(self.text):
            if self.text[i] == "\\":
                c = self.text[i + 1]
                if c == "n":
                    txt += "\n"
                elif c == "r":
                    txt += "\r"
                elif c == "t":
                    txt += "\t"
                elif c == "b":
                    txt += "\b"
                elif c == "f":
                    txt += "\f"
                i += 2
                continue
            txt += self.text[i]
            i += 1
        return bytearray(txt, encoding="UTF-8")


class PDFHexString(PDFString):
    """
    As hexadecimal data enclosed in angle brackets < > (using LESS-THAN SIGN (3Ch) and GREATER-
    THAN SIGN (3Eh)); see 7.3.4.3, "Hexadecimal Strings."
    """

    def __init__(self, text: str):
        super().__init__(text)
        text = text if len(text) % 2 == 0 else (text + "0")
        self.bytes = [
            int(text[i * 2 : i * 2 + 2], 16) for i in range(0, int(len(text) / 2))
        ]

    def __eq__(self, other) -> bool:
        return other.text == self.text if isinstance(other, PDFHexString) else False

    def __str__(self) -> str:
        return "<" + self.text + ">"

    def get_content_bytes(self) -> bytearray:
        arr = bytearray()
        for i in range(0, len(self.text), 2):
            arr.append(int(self.text[i : i + 2], 16))
        return arr
