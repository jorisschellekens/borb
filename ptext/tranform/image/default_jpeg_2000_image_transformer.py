import io
from typing import Optional, List

from ptext.object.canvas.xobject.jpeg_image import JPEGImage
from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.primitive.pdf_stream import PDFStream
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultJPEG2000ImageTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return (
            isinstance(object, PDFStream)
            and (
                (
                    PDFName("Type") in object.stream_dictionary
                    and object.stream_dictionary[PDFName("Type")] == PDFName("XObject")
                )
                or PDFName("Type") not in object.stream_dictionary
            )
            and PDFName("Subtype") in object.stream_dictionary
            and object.stream_dictionary[PDFName("Subtype")] == PDFName("Image")
            and PDFName("Filter") in object.stream_dictionary
            and (
                object.stream_dictionary[PDFName("Filter")] == PDFName("JPXDecode")
                or (
                    isinstance(object.stream_dictionary[PDFName("Filter")], PDFArray)
                    and object.stream_dictionary[PDFName("Filter")][0]
                    == PDFName("JPXDecode")
                )
            )
        )

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        tmp = JPEGImage()
        tmp.parent = parent_object

        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform key/value pair(s)
        for k, v in object_to_transform.stream_dictionary.items():
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v != PDFNull():
                tmp.set(k.name, v)

        # read image bytes
        tmp.read(io.BytesIO(object_to_transform.raw_byte_array))

        # return
        return tmp
