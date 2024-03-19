#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class is the base implementation of a transformer pattern.
It reads bytes from a PDF document, and converts it to JSON-like datastructures.
"""
import io
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Reference


class WriteTransformerState:
    """
    This class represents all the meta-information used in the process of persisting a PDF document.
    This includes:
    - the root object (the Document itself)
    - a cache of indirect objects (by id and hash)
    - references that have been resolved (to avoid endless loops)
    - the default compression level
    - etc
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        destination: typing.Optional[
            typing.Union[io.BufferedIOBase, io.RawIOBase]
        ] = None,
        root_object: typing.Optional[AnyPDFType] = None,
    ):
        # fmt: off
        self.destination = destination                                                      # this is the destination to write to (file, byte-buffer, etc)
        self.root_object: typing.Optional[AnyPDFType] = root_object                         # this is the root object (PDF)
        self.indirect_objects_by_id: typing.Dict[int, AnyPDFType] = {}                      # these are the indirect objects (by id)
        self.indirect_objects_by_hash: typing.Dict[int, typing.List[AnyPDFType]] = {}       # these are the indirect objects (by hash)
        self.resolved_references: typing.List[Reference] = []                               # these references have already been written
        self.compression_level: int = 9                                                     # default compression level
        self.apply_font_subsetting: bool = False                                            # whether to apply Font subsetting or not
        # fmt: on

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #


class Transformer:
    """
    This class represents the base transformer for persisting a PDF Document.
    It allows you to add child BaseWriteTransformer implementations to handle specific cases,
    such as persisting Image objects, or Dictionary objects, etc.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._handlers: typing.List["Transformer"] = []
        self._parent: typing.Optional["Transformer"] = None

    #
    # PRIVATE
    #

    def _end_object(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState],
    ):
        """
        This function writes the "endobj" bytes whenever a direct object needs to be closed
        """
        # write endobj
        # fmt: off
        assert context is not None, "A WriteTransformerState must be defined in order to write indirect objects."
        assert context.destination is not None, "A WriteTransformerState must be defined in order to write indirect objects."
        # fmt: on
        context.destination.write(bytes("endobj\n\n", "latin1"))

    @staticmethod
    def _hash(obj: typing.Any) -> int:
        h: typing.Optional[int] = None
        # hash
        try:
            h = hash(obj)
        except:
            pass
        # __hash__
        try:
            h = obj.__hash__()
        except:
            pass
        if h is None:
            raise TypeError("unhashable type: %s" % obj.__class__.__name__)
        return h

    def _start_object(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState],
    ):
        """
        This function starts a new direct object by writing
        its reference number followed by "obj" (e.g. "12 0 obj").
        It also does some bookkeeping to ensure the byte offset is stored in the XREF
        """
        # get offset position
        # fmt: off
        assert context is not None, "A WriteTransformerState must be defined in order to write indirect objects."
        assert context.destination is not None, "A WriteTransformerState must be defined in order to write indirect objects."
        # fmt: on
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

    #
    # PUBLIC
    #

    def add_child_transformer(
        self, handler: "Transformer"  # type: ignore [name-defined]
    ) -> "Transformer":  # type: ignore [name-defined]
        """
        This function adds a BaseWriteTransformer to this WriteBaseTransformer.
        Children of this WriteBaseTransformer will be called in turn, and their
        `can_be_transformed` method should return True if the child WriteBaseTransformer
        can handle the object to be transformed. The first child to return True will have its
        `transform` method called.
        This function returns self.
        """
        self._handlers.append(handler)
        handler._parent = self
        return self

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if this WriteBaseTransformer can transform the input object,
        false otherwise
        """
        return False

    def get_reference(
        self, object: AnyPDFType, context: WriteTransformerState
    ) -> Reference:
        """
        This function builds a Reference for the input object
        References are re-used whenever possible (hashing is used to detect duplicate objects)
        """
        is_unique: bool = False
        try:
            is_unique = object.is_unique()
        except:
            pass

        # look up object by ID
        obj_id = id(object)
        if obj_id in context.indirect_objects_by_id:
            cached_indirect_object: AnyPDFType = context.indirect_objects_by_id[obj_id]
            assert not isinstance(cached_indirect_object, Reference)
            ref: typing.Optional[Reference] = cached_indirect_object.get_reference()
            assert ref is not None
            assert isinstance(ref, Reference)
            return ref

        # look through existing indirect object hashes
        obj_hash: int = self._hash(object)
        if (not is_unique) and obj_hash in context.indirect_objects_by_hash:
            for obj in context.indirect_objects_by_hash[obj_hash]:
                if obj == object:
                    ref = obj.get_reference()
                    assert ref is not None
                    assert isinstance(ref, Reference)
                    object.set_reference(ref)
                    return ref

        # generate new object number
        existing_obj_numbers = set(
            [
                item.get_reference().object_number  # type: ignore[union-attr]
                for sublist in [v for k, v in context.indirect_objects_by_hash.items()]
                for item in sublist
            ]
        )
        obj_number = len(existing_obj_numbers) + 1
        while obj_number in existing_obj_numbers:  # type: ignore[union-attr]
            obj_number += 1

        # build reference
        ref = Reference(object_number=obj_number)
        object.set_reference(ref)

        # insert into context.indirect_objects_by_hash
        if obj_hash in context.indirect_objects_by_hash:
            context.indirect_objects_by_hash[obj_hash].append(object)
        else:
            context.indirect_objects_by_hash[obj_hash] = [object]

        # insert into context.indirect_objects_by_id
        context.indirect_objects_by_id[obj_id] = object

        # return
        return ref

    def get_root_transformer(self) -> "Transformer":
        """
        This function returns the WriteBaseTransformer at the root of this WriteBaseTransformer hierarchy.
        This allows child WriteBaseTransformer implementations to call the root transformer.
        This is useful for instance when transforming a dictionary, where each key/value would then be transformed
        by delegating the call to the root WriteBaseTransformer.
        """
        p: typing.Optional["Transformer"] = self
        while p is not None and p._parent is not None:
            p = p._parent
        assert p is not None
        return p

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This method writes an object (of type AnyPDFType) to a byte stream (specified in the WriteTransformerState)
        """
        # transform object
        return_value = None
        for h in self._handlers:
            if h.can_be_transformed(object_to_transform):
                return_value = h.transform(
                    object_to_transform,
                    context=context,
                )
                break

        # return
        return return_value
