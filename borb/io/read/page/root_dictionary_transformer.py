#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading the /Catalog object
"""
import io
import typing
from typing import Any, Dict, List, Optional, Union

from borb.io.read.object.dictionary_transformer import DictionaryTransformer
from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Decimal, Dictionary
from borb.io.read.types import List as bList
from borb.io.read.types import Name
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.page.page import Page


class RootDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading the /Catalog object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be converted represents a /Catalog Dictionary
        """
        return (
            isinstance(object, Dict)
            and "Type" in object
            and object["Type"] == "Catalog"
        )

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
                and isinstance(obj["Kids"], List)
            ):
                for k in obj["Kids"]:
                    stack_to_handle.append(k)

        # change
        root_dictionary["Pages"][Name("Kids")] = bList()
        for p in pages_in_order:
            root_dictionary["Pages"]["Kids"].append(p)
        root_dictionary["Pages"][Name("Count")] = Decimal(len(pages_in_order))

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a /Catalog Dictionary from a byte stream
        """
        assert isinstance(object_to_transform, Dictionary)

        # convert using Dictionary transformer
        transformed_root_dictionary: Optional[Dictionary] = None
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
