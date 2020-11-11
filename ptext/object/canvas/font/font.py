from typing import Optional

from ptext.object.canvas.geometry.matrix import Matrix
from ptext.object.pdf_high_level_object import PDFHighLevelObject
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_number import PDFInt, PDFFloat
from ptext.primitive.pdf_string import PDFString


class Font(PDFHighLevelObject):
    def __init__(self):
        super().__init__()

    def get_average_character_width(self) -> Optional[float]:
        # easy way
        i = self.get(["FontDescriptor", "AvgWidth"])
        if i != PDFNull():
            return i.get_float_value()
        # calculate average width
        # default
        return 0

    def get_font_matrix(self) -> Matrix:
        # TODO
        return Matrix.identity_matrix()

    def get_width(self, text: PDFString) -> float:

        widths = self.get("Widths")
        if widths == PDFNull():
            return 0

        widths_len = widths.get("Length").get_int_value()
        first_char = self.get("FirstChar").get_int_value()

        # get text
        text = text.get_text()

        # sum all widths
        sum = 0
        for i in range(0, len(text)):
            j = ord(text[i]) - first_char
            if j < 0 or j >= widths_len:
                sum += 0
            else:
                sum += widths.get(j).get_float_value()
        return sum * self.get_font_matrix()[0][0]

    def get_font_name(self) -> Optional[str]:

        # BaseFont
        i = self.get("BaseFont")
        if isinstance(i, PDFName):
            return i.name.replace("#20", " ")

        # FontDescriptor / FontName
        i = self.get(["FontDescriptor", "FontName"])
        if isinstance(i, PDFName):
            return i.name.replace("#20", " ")

        # default
        return None

    def __deepcopy__(self, memodict={}):
        out = Font()
        for k in ["Type", "SubType", "Name", "BaseFont"]:
            if self.has_key(k):
                out.set(k, PDFName(self.get(k).name))

        for k in ["FirstChar", "LastChar"]:
            if self.has_key(k):
                out.set(k, PDFInt(self.get(k).get_int_value()))

        # Widths
        if self.has_key("Widths"):
            l = self.get(["Widths", "Length"]).get_int_value()
            widths_arr = PDFHighLevelObject()
            for i in range(0, l):
                widths_arr.set(i, PDFFloat(self.get(["Widths", i]).get_float_value()))
            widths_arr.set("Type", PDFName("Array"))
            widths_arr.set("Length", PDFInt(l))
            out.set("Widths", widths_arr)

        # FontDescriptor
        if self.has_key("FontDescriptor"):
            out.set(
                "FontDescriptor",
                self.__deepcopy_fontdescriptor__(self.get("FontDescriptor")),
            )

        # TODO : Encoding
        # TODO : ToUnicode

        # return
        return out

    def __deepcopy_fontdescriptor__(
        self, font_descriptor: PDFHighLevelObject
    ) -> PDFHighLevelObject:
        out = PDFHighLevelObject()
        for k in ["Type", "FontName"]:
            if font_descriptor.has_key(k):
                out.set(k, PDFName(font_descriptor.get(k).name))

        for k in [
            "Flags",
            "ItalicAngle",
            "Ascent",
            "Descent",
            "CapHeight",
            "AvgWidth",
            "MaxWidth",
            "FontWeight",
            "XHeight",
            "StemV",
        ]:
            if font_descriptor.has_key(k):
                out.set(k, PDFInt(font_descriptor.get(k).get_int_value()))

        # FontBox
        if font_descriptor.has_key("FontBox"):
            l = font_descriptor.get(["FontBox", "Length"]).get_int_value()
            fontbox_arr = PDFHighLevelObject()
            for i in range(0, l):
                fontbox_arr.set(
                    i, PDFFloat(font_descriptor.get(["Widths", i]).get_float_value())
                )
            fontbox_arr.set("Type", PDFName("Array"))
            fontbox_arr.set("Length", PDFInt(l))
            out.set("FontBox", fontbox_arr)

        # return
        return out
