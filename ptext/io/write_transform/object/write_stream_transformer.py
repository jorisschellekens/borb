import typing
from typing import Optional

from ptext.io.read_transform.types import (
    AnyPDFType,
    Dictionary,
    Stream,
    Reference,
    List,
)
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    TransformerWriteContext,
)


class WriteStreamTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Stream)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[TransformerWriteContext] = None,
    ):
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Stream)

        # start object if needed
        started_object = False
        ref = object_to_transform.get_reference()  # type: ignore [attr-defined]
        if ref is not None:
            assert isinstance(ref, Reference)
            if ref in context.duplicate_references:
                return
            if ref.object_number is not None and ref.byte_offset is None:
                started_object = True
                self.start_object(object_to_transform, context)
            context.duplicate_references.append(ref)

        # build stream dictionary
        stream_dictionary = Dictionary()

        # objects to turn into reference
        queue: typing.List[AnyPDFType] = []
        for k, v in object_to_transform.items():
            if k in ["Bytes", "DecodedBytes"]:
                continue
            if (
                isinstance(v, Dictionary)
                or isinstance(v, List)
                or isinstance(v, Stream)
            ):
                stream_dictionary[k] = self.get_reference(v, context)
                queue.append(v)
            else:
                stream_dictionary[k] = v

        # write stream dictionary
        self.get_root_transformer().transform(stream_dictionary, context)

        # write "stream"
        context.destination.write(bytes("stream\n", "latin1"))

        # write bytes
        context.destination.write(object_to_transform["Bytes"])

        # write "endstream"
        context.destination.write(bytes("\nendstream\n", "latin1"))

        # end object if needed
        if started_object:
            self.end_object(object_to_transform, context)

        for e in queue:
            self.get_root_transformer().transform(e, context)
