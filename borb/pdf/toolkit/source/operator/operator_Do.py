#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Do' operator: Paint the specified XObject.

The 'Do' operator is used in a PDF content stream to paint an XObject (external object), which could be an image, a form, or a PostScript object.
The operand of this operator is the name of the XObject, which must be a key in the XObject subdictionary of the current resource dictionary.

The associated value for this key in the resource dictionary must be a stream whose `Type` entry, if present, is set to `XObject`.
The specific behavior of the operator depends on the value of the XObject’s `Subtype` entry, which can take one of the following values:

- **Image**: Refers to an image XObject (for details, see section 8.9.5, "Image Dictionaries").
- **Form**: Refers to a form XObject, which represents a reusable graphical object or group of objects (for details, see section 8.10, "Form XObjects").
- **PS (PostScript)**: Refers to a PostScript XObject, which represents PostScript code to be executed (for details, see section 8.8.2, "PostScript XObjects").

The effect of the 'Do' operator depends on the `Subtype` of the XObject, as it determines the type of content that will be rendered on the page.

For more information about XObjects and how they are used, refer to section 7.8.3, "Resource Dictionaries," and the appropriate sections on XObject types (Image, Form, and PostScript).
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorDo(Operator):
    """
    The 'Do' operator: Paint the specified XObject.

    The 'Do' operator is used in a PDF content stream to paint an XObject (external object), which could be an image, a form, or a PostScript object.
    The operand of this operator is the name of the XObject, which must be a key in the XObject subdictionary of the current resource dictionary.

    The associated value for this key in the resource dictionary must be a stream whose `Type` entry, if present, is set to `XObject`.
    The specific behavior of the operator depends on the value of the XObject’s `Subtype` entry, which can take one of the following values:

    - **Image**: Refers to an image XObject (for details, see section 8.9.5, "Image Dictionaries").
    - **Form**: Refers to a form XObject, which represents a reusable graphical object or group of objects (for details, see section 8.10, "Form XObjects").
    - **PS (PostScript)**: Refers to a PostScript XObject, which represents PostScript code to be executed (for details, see section 8.8.2, "PostScript XObjects").

    The effect of the 'Do' operator depends on the `Subtype` of the XObject, as it determines the type of content that will be rendered on the page.

    For more information about XObjects and how they are used, refer to section 7.8.3, "Resource Dictionaries," and the appropriate sections on XObject types (Image, Form, and PostScript).
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __cross(
        m: typing.List[typing.List[float]], v: typing.List[float]
    ) -> typing.List[float]:
        x: float = v[0]
        y: float = v[1]
        z: float = v[2]
        x2 = x * m[0][0] + y * m[1][0] + z * m[2][0]
        y2 = x * m[0][1] + y * m[1][1] + z * m[2][1]
        z2 = x * m[0][2] + y * m[1][2] + z * m[2][2]
        return [x2, y2, z2]

    #
    # PUBLIC
    #

    def apply(
        self,
        operands: typing.List[PDFType],
        page: Page,
        source: Source,
    ) -> None:
        """
        Apply the operator's logic to the given `Page`.

        This method executes the operator using the provided operands, applying its
        effects to the specified `Page` via the `Source` processor. Subclasses should
        override this method to implement specific operator behavior.

        :param page: The `Page` object to which the operator is applied.
        :param source: The `Source` object managing the content stream.
        :param operands: A list of `PDFType` objects representing the operator's operands.
        """
        # look up XObject
        assert isinstance(operands[0], name)
        xobject_resource_name: name = operands[0]
        xobject: typing.Optional[PDFType] = (
            page.get("Resources", {})
            .get("XObject", {})
            .get(xobject_resource_name[1:], None)
        )

        # /Image
        if (
            xobject is not None
            and isinstance(xobject, dict)
            and xobject.get("Subtype", None) == "Image"
        ):

            # calculate position
            v: typing.List[float] = OperatorDo.__cross(
                m=source.transformation_matrix, v=[0, 0, 1]
            )
            x: float = v[0]
            y: float = v[1]

            # calculate display size
            v = OperatorDo.__cross(m=source.transformation_matrix, v=[1, 1, 0])
            width: float = max(abs(v[0]), 1)
            height: float = max(abs(v[1]), 1)

            # call rendering method
            source.image(
                x=x,
                y=y,
                width=width,
                height=height,
                image=xobject["Bytes"],
                xobject_resource=xobject_resource_name,
            )
            return

        # /Form
        # TODO

        # /PS
        # TODO

        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Do"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
