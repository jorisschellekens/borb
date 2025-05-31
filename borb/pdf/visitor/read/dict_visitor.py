#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing dictionary objects in a PDF byte stream.

`DictVisitor` is specialized to locate and interpret PDF dictionary objects,
defined by `<< >>` delimiters. Using the visitor pattern, `DictVisitor` traverses
nodes in a PDF document, extracting key-value pairs within dictionaries and
converting them to Python dictionaries for structured processing.

This class:
- Identifies dictionary delimiters (`<<` and `>>`) in the PDF byte stream.
- Parses and decodes each key-value pair according to PDF encoding rules.
- Supports nested dictionaries, allowing for recursive parsing of complex objects.

`DictVisitor` is intended to facilitate structured handling of metadata, resources,
and other dictionary-based elements in the PDF.
"""
import typing

from borb.pdf.primitives import PDFType, name
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class DictVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing dictionary objects in a PDF byte stream.

    `DictVisitor` is specialized to locate and interpret PDF dictionary objects,
    defined by `<< >>` delimiters. Using the visitor pattern, `DictVisitor` traverses
    nodes in a PDF document, extracting key-value pairs within dictionaries and
    converting them to Python dictionaries for structured processing.

    This class:
    - Identifies dictionary delimiters (`<<` and `>>`) in the PDF byte stream.
    - Parses and decodes each key-value pair according to PDF encoding rules.
    - Supports nested dictionaries, allowing for recursive parsing of complex objects.

    `DictVisitor` is intended to facilitate structured handling of metadata, resources,
    and other dictionary-based elements in the PDF.
    """

    __DICT_CLOSE_BRACKETS = b">>"
    __DICT_OPEN_BRACKETS = b"<<"
    __SPACE = b" "

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __convert_to_font_courier(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Courier":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Courier")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_courier_bold(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Courier-Bold":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Courier-Bold")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_courier_bold_italic(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Courier-BoldOblique":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Courier-BoldOblique")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_courier_italic(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Courier-Oblique":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Courier-Oblique")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_helvetica(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Helvetica":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Helvetica")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_helvetica_bold(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Helvetica-Bold":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Helvetica-Bold")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_helvetica_bold_italic(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Helvetica-BoldOblique":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Helvetica-BoldOblique")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_helvetica_italic(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Helvetica-Oblique":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Helvetica-Oblique")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_symbol(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Symbol":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Symbol")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_times(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Times-Roman":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Times-Roman")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_times_bold(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Times-Bold":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Times-Bold")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_times_bold_italic(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Times-BoldItalic":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Times-BoldItalic")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_times_italic(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "Times-Italic":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("Times-Italic")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_font_zapfdingbats(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("BaseFont", None) != "ZapfDingbats":
            return d
        from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts

        retval: Font = Standard14Fonts.get("ZapfDingbats")  # type: ignore[assignment]
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_page(d: dict) -> "Page":  # type: ignore[name-defined]
        if isinstance(d, dict) and "Type" in d and d["Type"] == "Page":
            from borb.pdf.page import Page

            retval = Page()
            for k, v in d.items():
                retval[k] = v
            return retval
        return d

    @staticmethod
    def __convert_to_true_type_font(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if isinstance(d, Font):
            return d
        if not isinstance(d, dict):
            return d
        if d.get("Type", None) != "Font":
            return d
        if d.get("Subtype", None) != "TrueType":
            return d
        from borb.pdf.font.simple_font.true_type.true_type_font import TrueTypeFont

        retval: Font = TrueTypeFont()
        for k, v in d.items():
            retval[k] = v
        return retval

    @staticmethod
    def __convert_to_type_0_font(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if (
            isinstance(d, dict)
            and not isinstance(d, Font)
            and "Type" in d
            and d["Type"] == "Font"
            and "Subtype" in d
            and d["Subtype"] == "Type0"
        ):
            from borb.pdf.font.composite_font.composite_font import CompositeFont

            retval = CompositeFont()
            for k, v in d.items():
                retval[k] = v
            return retval
        return d

    @staticmethod
    def __convert_to_type_1_font(d: dict) -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if (
            isinstance(d, dict)
            and not isinstance(d, Font)
            and "Type" in d
            and d["Type"] == "Font"
            and "Subtype" in d
            and d["Subtype"] == "Type1"
        ):
            from borb.pdf.font.simple_font.type_1_font import Type1Font

            retval = Type1Font()
            for k, v in d.items():
                retval[k] = v
            return retval
        return d

    @staticmethod
    def __convert_to_unicode_to_cmap_in_font(f: "Font") -> "Font":  # type: ignore[name-defined]
        from borb.pdf.font.font import Font

        if not isinstance(f, Font):
            return f
        if "ToUnicode" in f:
            try:
                from borb.pdf.font.cmap import CMap

                f["ToUnicode"] = CMap(f["ToUnicode"])
            except:
                pass
        return f

    #
    # PUBLIC
    #

    def visit(
        self, node: typing.Union[int, bytes]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        if not isinstance(node, int):
            return None
        if self.get_bytes()[node : node + 2] != DictVisitor.__DICT_OPEN_BRACKETS:
            return None

        retval: typing.Dict[typing.Union[name, str], "PDFType"] = {}
        i: int = node + 2
        expect_key: bool = True
        previous_key: typing.Optional[name] = None
        while i < len(self.get_bytes()):

            # IF we see __DICT_CLOSE_BRACKETS
            # THEN break
            if self.get_bytes()[i : i + 2] == DictVisitor.__DICT_CLOSE_BRACKETS:
                i += 2
                break

            # IF we see a space
            # THEN skip
            if self.get_bytes()[i : i + 1] == DictVisitor.__SPACE:
                i += 1
                continue

            # IF we see a newline (\n\r)
            # THEN skip
            if self.get_bytes()[i : i + 2] == b"\n\r":
                i += 2
                continue
            if self.get_bytes()[i : i + 2] == b"\r\n":
                i += 2
                continue
            if self.get_bytes()[i : i + 1] == b"\n":
                i += 1
                continue
            if self.get_bytes()[i : i + 1] == b"\r":
                i += 1
                continue

            # read a key
            if expect_key:
                previous_key_and_i = self.root_generic_visit(i)
                assert previous_key_and_i is not None
                assert isinstance(previous_key_and_i[0], name)
                previous_key, i = previous_key_and_i  # type: ignore[assignment]
                expect_key = False
                continue

            # read a value (could be anything)
            if not expect_key:
                previous_value_and_i = self.root_generic_visit(i)
                assert previous_value_and_i is not None
                assert previous_key is not None
                previous_value, i = previous_value_and_i
                retval[previous_key] = previous_value
                expect_key = True

        # /font/courier
        retval = DictVisitor.__convert_to_font_courier(retval)
        retval = DictVisitor.__convert_to_font_courier_bold(retval)
        retval = DictVisitor.__convert_to_font_courier_bold_italic(retval)
        retval = DictVisitor.__convert_to_font_courier_italic(retval)

        # /font/helvetica
        retval = DictVisitor.__convert_to_font_helvetica(retval)
        retval = DictVisitor.__convert_to_font_helvetica_bold(retval)
        retval = DictVisitor.__convert_to_font_helvetica_bold_italic(retval)
        retval = DictVisitor.__convert_to_font_helvetica_italic(retval)

        # /font/symbol
        retval = DictVisitor.__convert_to_font_symbol(retval)

        # /font/times
        retval = DictVisitor.__convert_to_font_times(retval)
        retval = DictVisitor.__convert_to_font_times_bold(retval)
        retval = DictVisitor.__convert_to_font_times_bold_italic(retval)
        retval = DictVisitor.__convert_to_font_times_italic(retval)

        # /font/zapfdingbats
        retval = DictVisitor.__convert_to_font_zapfdingbats(retval)

        # /font/TrueTypeFont
        retval = DictVisitor.__convert_to_true_type_font(retval)

        # Type0Font
        retval = DictVisitor.__convert_to_type_0_font(retval)

        # Type1Font
        retval = DictVisitor.__convert_to_type_1_font(retval)
        retval = DictVisitor.__convert_to_unicode_to_cmap_in_font(retval)

        # page
        retval = DictVisitor.__convert_to_page(retval)

        # return
        return retval, i
