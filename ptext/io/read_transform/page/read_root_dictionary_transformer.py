import io
import typing
from typing import Optional, List, Any, Union, Dict

from ptext.io.read_transform.object.read_dictionary_transformer import (
    ReadDictionaryTransformer,
)
from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read_transform.types import (
    Dictionary,
    List,
    AnyPDFType,
    Decimal,
)
from ptext.io.read_transform.types import List as pList
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.page.page import Page


class ReadRootDictionaryTransformer(ReadBaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Dict)
            and "Type" in object
            and object["Type"] == "Catalog"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        assert isinstance(object_to_transform, Dictionary)

        # convert using Dictionary transformer
        transformed_root_dictionary: Optional[Dictionary] = None
        for t in self.get_root_transformer().children:
            if isinstance(t, ReadDictionaryTransformer):
                transformed_root_dictionary = t.transform(
                    object_to_transform, parent_object, context, event_listeners
                )
                break

        assert transformed_root_dictionary is not None
        assert isinstance(transformed_root_dictionary, Dictionary)

        #
        # rebuild /Pages if needed
        #

        # list to hold Page objects (in order)
        pages_in_order: typing.List[Page] = []

        # stack to explore Page(s) DFS
        stack_to_handle: typing.List[AnyPDFType] = []
        stack_to_handle.extend(transformed_root_dictionary["Pages"]["Kids"])

        # DFS
        while len(stack_to_handle) > 0:
            obj = stack_to_handle.pop(0)
            if isinstance(obj, Page):
                pages_in_order.append(obj)
            if (
                isinstance(obj, Dictionary)
                and "Type" in obj
                and obj["Type"] == "Pages"
                and "Kids" in obj
                and isinstance(obj["Kids"], List)
            ):
                for k in obj["Kids"]:
                    stack_to_handle.insert(0, k)

        # change
        transformed_root_dictionary["Pages"]["Kids"] = pList()
        for p in pages_in_order:
            transformed_root_dictionary["Pages"]["Kids"].append(p)
        transformed_root_dictionary["Pages"]["Count"] = Decimal(len(pages_in_order))

        # return
        return transformed_root_dictionary
