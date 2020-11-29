from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import ListWithParentAttribute


class DefaultArrayTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFArray to a List
    """

    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFArray)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # create root object
        tmp = ListWithParentAttribute().set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform child(ren)
        for i in range(0, len(object_to_transform)):
            tmp.append(
                self.get_root_transformer().transform(
                    object_to_transform[i], tmp, context, []
                )
            )

        # return
        return tmp
