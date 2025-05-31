#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'BDC' operator: Begin a marked-content sequence with an associated property list.

The 'BDC' operator is used to begin a marked-content sequence in a PDF content stream,
with an associated property list. The operator is followed by a tag (a name object that
indicates the role or significance of the sequence) and a properties list (which can either
be an inline dictionary or a name object associated with the property list in the Properties
subdictionary of the current resource dictionary).

The marked-content sequence is terminated by a balancing 'EMC' operator.

Note:
    The 'tag' argument specifies the role or significance of the marked-content sequence.
    The 'properties' argument can either be a dictionary containing the property list or a
    name object referring to it in the current resource dictionary. For more details, refer to
    section 14.6.2, "Property Lists" of the PDF specification.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorBDC(Operator):
    """
    The 'BDC' operator: Begin a marked-content sequence with an associated property list.

    The 'BDC' operator is used to begin a marked-content sequence in a PDF content stream,
    with an associated property list. The operator is followed by a tag (a name object that
    indicates the role or significance of the sequence) and a properties list (which can either
    be an inline dictionary or a name object associated with the property list in the Properties
    subdictionary of the current resource dictionary).

    The marked-content sequence is terminated by a balancing 'EMC' operator.

    Note:
        The 'tag' argument specifies the role or significance of the marked-content sequence.
        The 'properties' argument can either be a dictionary containing the property list or a
        name object referring to it in the current resource dictionary. For more details, refer to
        section 14.6.2, "Property Lists" of the PDF specification.
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
        return "BDC"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
