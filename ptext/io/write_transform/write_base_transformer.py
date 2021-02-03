import io
import typing
from typing import Optional

from ptext.io.read_transform.types import AnyPDFType, Reference


class WriteTransformerContext:
    def __init__(
        self,
        destination: Optional[typing.Union[io.BufferedIOBase, io.RawIOBase]] = None,
        root_object: Optional[AnyPDFType] = None,
    ):
        self.destination = (
            destination  # this is the destination to write to (file, byte-buffer, etc)
        )
        self.root_object: Optional[
            AnyPDFType
        ] = root_object  # this is the root object (PDF)
        self.indirect_objects: typing.Dict[
            int, typing.List[AnyPDFType]
        ] = {}  # these are all the indirect objects
        self.resolved_references: typing.List[
            Reference
        ] = []  # these references have already been written


class WriteBaseTransformer:
    def __init__(self):
        self.handlers = []
        self.parent = None

    def add_child_transformer(
        self, handler: "BaseWriteTransformer"  # type: ignore [name-defined]
    ) -> "WriteBaseTransformer":  # type: ignore [name-defined]
        self.handlers.append(handler)
        handler.parent = self
        return self

    def get_root_transformer(self) -> "WriteBaseTransformer":  # type: ignore [name-defined]
        p = self
        while p.parent is not None:
            p = p.parent
        return p

    def can_be_transformed(self, any: AnyPDFType):
        return False

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
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
        context: Optional[WriteTransformerContext],
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
        context: Optional[WriteTransformerContext],
    ):
        # write endobj
        assert context is not None
        assert context.destination is not None
        context.destination.write(bytes("endobj\n\n", "latin1"))

    def get_reference(
        self, object: AnyPDFType, context: WriteTransformerContext
    ) -> Reference:

        # look through existing indirect objects
        obj_hash: int = hash(object)
        if obj_hash in context.indirect_objects:
            for obj in context.indirect_objects[obj_hash]:
                if obj == object:
                    ref = obj.get_reference()  # type: ignore [union-attr]
                    assert ref is not None
                    assert isinstance(ref, Reference)
                    return ref

        # generate new object number
        existing_obj_numbers = set(
            [
                item.get_reference().object_number  # type: ignore [union-attr]
                for sublist in [v for k, v in context.indirect_objects.items()]
                for item in sublist
            ]
        )
        obj_number = len(existing_obj_numbers) + 1
        while obj_number in existing_obj_numbers:  # type: ignore [union-attr]
            obj_number += 1

        # build reference
        ref = Reference(object_number=obj_number)
        object.set_reference(ref)  # type: ignore [union-attr]

        # insert into context
        if obj_hash in context.indirect_objects:
            context.indirect_objects[obj_hash].append(object)
        else:
            context.indirect_objects[obj_hash] = [object]

        # return
        return ref
