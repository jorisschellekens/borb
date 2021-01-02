import io
import typing
from typing import Optional

from ptext.io.read_transform.types import AnyPDFType, Reference


class TransformerWriteContext:
    def __init__(
        self,
        destination: Optional[typing.Union[io.BufferedIOBase, io.RawIOBase]] = None,
        root_object: Optional[AnyPDFType] = None,
    ):
        self.destination = destination
        self.root_object: Optional[AnyPDFType] = root_object
        self.indirect_objects: typing.List[AnyPDFType] = []
        self.duplicate_references: typing.List[Reference] = []


class WriteBaseTransformer:
    def __init__(self):
        self.handlers = []
        self.parent = None

    def add_child_transformer(
        self, handler: "BaseWriteTransformer"  # type: ignore [name-defined]
    ) -> "BaseWriteTransformer":  # type: ignore [name-defined]
        self.handlers.append(handler)
        handler.parent = self
        return self

    def get_root_transformer(self) -> "BaseWriteTransformer":  # type: ignore [name-defined]
        p = self
        while p.parent is not None:
            p = p.parent
        return p

    def can_be_transformed(self, any: AnyPDFType):
        return False

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[TransformerWriteContext] = None,
    ):
        # transform object
        return_value = None
        for h in self.handlers:
            if h.can_be_transformed(object_to_transform):
                return_value = h.transform(
                    object_to_transform,
                    context=context,
                )
                break

        # return
        return return_value

    def start_object(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[TransformerWriteContext],
    ):

        # get offset position
        assert context is not None
        assert context.destination is not None
        byte_offset = context.destination.tell()

        # update offset
        ref = object_to_transform.get_reference()  # type: ignore [union-attr]
        assert ref is not None
        assert isinstance(ref, Reference)
        ref.byte_offset = byte_offset

        # write <object number> <generation number> obj
        assert ref.object_number is not None
        context.destination.write(
            bytes(
                "%d %d obj\n" % (ref.object_number, ref.generation_number or 0),
                "latin1",
            )
        )

    def end_object(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[TransformerWriteContext],
    ):
        # write endobj
        assert context is not None
        assert context.destination is not None
        context.destination.write(bytes("endobj\n\n", "latin1"))

    def get_reference(
        self, object: AnyPDFType, context: TransformerWriteContext
    ) -> Reference:
        # look through existing indirect objects
        for obj in context.indirect_objects:
            if obj == object:
                ref = obj.get_reference()  # type: ignore [union-attr]
                assert ref is not None
                assert isinstance(ref, Reference)
                return ref

        # generate new object number
        obj_number = 1
        while obj_number in [x.get_reference().object_number for x in context.indirect_objects]:  # type: ignore [union-attr]
            obj_number += 1

        # insert
        ref = Reference(object_number=obj_number)
        context.indirect_objects.append(object.set_reference(ref))  # type: ignore [union-attr]

        # return
        return ref
