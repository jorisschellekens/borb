#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'DP' operator: Designate a marked-content point with an associated property list.

The 'DP' operator is used in a PDF content stream to designate a marked-content point, which is a point in the content stream where a marked-content sequence begins. This operator is used to associate a property list with the marked-content point.

The operand `tag` is a name object that indicates the role or significance of the marked-content point. The `properties` operand shall be either:

- An inline dictionary containing the property list.
- A name object that is associated with a property list in the `Properties` subdictionary of the current resource dictionary (for details, see section 14.6.2, "Property Lists").

The `DP` operator is commonly used to label specific points in a PDF document with associated properties, making it possible to reference these points later in the content stream for various purposes, such as styling, annotation, or metadata.

For more details on property lists and their use in marked-content sequences, refer to section 14.6.2, "Property Lists."
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorDP(Operator):
    """
    The 'DP' operator: Designate a marked-content point with an associated property list.

    The 'DP' operator is used in a PDF content stream to designate a marked-content point, which is a point in the content stream where a marked-content sequence begins. This operator is used to associate a property list with the marked-content point.

    The operand `tag` is a name object that indicates the role or significance of the marked-content point. The `properties` operand shall be either:

    - An inline dictionary containing the property list.
    - A name object that is associated with a property list in the `Properties` subdictionary of the current resource dictionary (for details, see section 14.6.2, "Property Lists").

    The `DP` operator is commonly used to label specific points in a PDF document with associated properties, making it possible to reference these points later in the content stream for various purposes, such as styling, annotation, or metadata.

    For more details on property lists and their use in marked-content sequences, refer to section 14.6.2, "Property Lists."
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

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
        assert isinstance(operands[0], name)
        assert isinstance(operands[1], dict) or isinstance(operands[1], name)
        tag: name = operands[0]
        property_dictionary: typing.Dict[name, PDFType] = {}
        if isinstance(operands[1], dict):
            property_dictionary = operands[1]  # type: ignore[assignment]
        if isinstance(operands[1], name):
            property_dictionary = (
                page.get("Resources", {}).get("Properties", {}).get(operands[0][1:], {})
            )
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "DP"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
