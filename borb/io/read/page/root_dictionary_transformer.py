#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading the /Catalog object
"""
import io
import typing

from borb.io.read.object.dictionary_transformer import DictionaryTransformer
from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List as bList
from borb.io.read.types import Name
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.page.page import Page


class RootDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading the /Catalog object
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _re_order_pages(self, root_dictionary: dict) -> None:
        # list to hold Page objects (in order)
        pages_in_order: typing.List[Page] = []

        # stack to explore Page(s) DFS
        stack_to_handle: typing.List[AnyPDFType] = []
        stack_to_handle.append(root_dictionary["Pages"])

        # DFS
        while len(stack_to_handle) > 0:
            obj = stack_to_handle.pop(0)
            if isinstance(obj, Page):
                pages_in_order.append(obj)
            # /Pages
            if (
                isinstance(obj, Dictionary)
                and "Type" in obj
                and obj["Type"] == "Pages"
                and "Kids" in obj
                and isinstance(obj["Kids"], typing.List)
            ):
                for k in obj["Kids"]:
                    stack_to_handle.append(k)

        # change
        root_dictionary["Pages"][Name("Kids")] = bList()
        for p in pages_in_order:
            root_dictionary["Pages"]["Kids"].append(p)
        root_dictionary["Pages"][Name("Count")] = bDecimal(len(pages_in_order))

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
        This function returns True if the object to be transformed is a /Catalog Dictionary
        :param object:  the object to be transformed
        :return:        True if the object is a /Catalog Dictionary, False otherwise
        """
        return (
            isinstance(object, typing.Dict)
            and "Type" in object
            and object["Type"] == "Catalog"
        )

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms an /Catalog Dictionary
        :param object_to_transform:     the /Catalog Dictionary to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a /Catalog Dictionary
        """

        # fmt: off
        assert isinstance(object_to_transform, Dictionary), "object_to_transform must be of type Dictionary"
        # fmt: on

        # convert using Dictionary transformer
        transformed_root_dictionary: typing.Optional[Dictionary] = None
        for t in self.get_root_transformer().get_children():
            if isinstance(t, DictionaryTransformer):
                transformed_root_dictionary = t.transform(
                    object_to_transform, parent_object, context, event_listeners
                )
                break

        assert transformed_root_dictionary is not None
        assert isinstance(transformed_root_dictionary, Dictionary)

        #
        # rebuild /Pages if needed
        #
        self._re_order_pages(transformed_root_dictionary)

        # return
        return transformed_root_dictionary
