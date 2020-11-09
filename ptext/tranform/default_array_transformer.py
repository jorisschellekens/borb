from typing import Optional, List

from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_number import PDFInt
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultArrayTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFArray)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        # create root object
        tmp = PDFHighLevelObject()
        tmp.parent = parent_object

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform child(ren)
        for i in range(0, len(object_to_transform)):
            tmp.set(
                i,
                self.get_root_transformer().transform(
                    object_to_transform[i], tmp, context, []
                ),
            )

        # add meta properties
        tmp.set("Type", PDFName("Array"))
        tmp.set("Length", PDFInt(len(object_to_transform)))

        # return
        return tmp
