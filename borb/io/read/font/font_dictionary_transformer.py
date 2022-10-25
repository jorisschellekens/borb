#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseTransformer is responsible for reading a Font object
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Dictionary, Stream
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.font.composite_font.cid_font_type_0 import CIDType0Font
from borb.pdf.canvas.font.composite_font.cid_font_type_2 import CIDType2Font
from borb.pdf.canvas.font.composite_font.font_type_0 import Type0Font
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font, Type1Font
from borb.pdf.canvas.font.simple_font.font_type_3 import Type3Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont


class FontDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a Font object
    """

    def __init__(self):
        super(FontDictionaryTransformer, self).__init__()
        self._accept_true_type_standard_14_fonts: bool = True

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a /Font Dictionary
        """
        return (
            isinstance(object, dict)
            and not isinstance(object, Stream)
            and "Type" in object
            and object["Type"] == "Font"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a /Font Dictionary from a byte stream
        """

        # convert dictionary like structure
        assert isinstance(object_to_transform, Dictionary)
        subtype_name = object_to_transform["Subtype"]

        font_obj: Optional[Font] = None

        # TrueType Font
        if subtype_name == "TrueType":
            font_obj = TrueTypeFont()
            # Some libraries prefer to mark the standard 14 fonts as TrueType fonts
            # These libraries should be punished for their crimes against humanity.
            # But in the interest of pleasing the user, we explicitly catch these errors and guide
            # those wayward lambs back into the fold.
            if (
                self._accept_true_type_standard_14_fonts
                and "BaseFont" in object_to_transform
                and StandardType1Font.is_standard_14_font_name(
                    str(object_to_transform["BaseFont"])
                )
            ):
                font_obj = StandardType1Font(str(object_to_transform["BaseFont"]))

        # Type 0 Font
        elif subtype_name == "Type0":
            font_obj = Type0Font()

        # Type 1 Font
        elif subtype_name == "Type1":
            base_font: str = str(object_to_transform["BaseFont"])
            if StandardType1Font.is_standard_14_font_name(base_font):
                font_obj = StandardType1Font(base_font)
            else:
                font_obj = Type1Font()

        # Type 3 Font
        elif subtype_name == "Type3":
            font_obj = Type3Font()

        elif subtype_name == "CIDFontType0":
            font_obj = CIDType0Font()
        elif subtype_name == "CIDFontType2":
            font_obj = CIDType2Font()
        else:
            font_obj = StandardType1Font("Helvetica")

        # None
        if font_obj is None:
            return None

        # set parent
        assert font_obj is not None
        font_obj.set_parent(parent_object)  # type: ignore [union-attr]

        # convert key/value pair(s)
        assert isinstance(object_to_transform, Dictionary)
        for k, v in object_to_transform.items():
            if k == "Parent":
                continue
            v = self.get_root_transformer().transform(v, font_obj, context, [])
            if v is not None:
                font_obj[k] = v

        # return
        assert isinstance(font_obj, Font)
        return font_obj
