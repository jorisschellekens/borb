#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseTransformer is responsible for reading a Font object
"""
import io
import typing

from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Dictionary
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.font.composite_font.cid_font_type_0 import CIDType0Font
from borb.pdf.canvas.font.composite_font.cid_font_type_2 import CIDType2Font
from borb.pdf.canvas.font.composite_font.font_type_0 import Type0Font
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.font.simple_font.font_type_1 import Type1Font
from borb.pdf.canvas.font.simple_font.font_type_3 import Type3Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont


class FontDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a Font object
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(FontDictionaryTransformer, self).__init__()
        self._accept_true_type_standard_14_fonts: bool = True

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed is a /Font Dictionary
        :param object:  the object to be transformed
        :return:        True if the object is a /Font Dictionary, False otherwise
        """
        return (
            isinstance(object, dict)
            and not isinstance(object, Stream)
            and "Type" in object
            and object["Type"] == "Font"
        )

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a /Font Dictionary into a Font Object
        :param object_to_transform:     the /Font Dictionary to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a Font Object
        """

        # convert dictionary like structure
        assert isinstance(object_to_transform, Dictionary)
        subtype_name = object_to_transform["Subtype"]

        font_obj: typing.Optional[Font] = None

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
        font_obj.set_parent(parent_object)

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
