#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing XREF objects
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState
from borb.pdf.xref.xref import XREF


class XREFTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing XREF objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _section_xref(self, context: typing.Optional[WriteTransformerState] = None):
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write XREF objects."

        # get all references
        indirect_objects: typing.List[AnyPDFType] = [
            item
            for sublist in [v for k, v in context.indirect_objects_by_hash.items()]
            for item in sublist
        ]
        references: typing.List[Reference] = []
        for obj in indirect_objects:
            ref = obj.get_reference()  # type: ignore [union-attr]
            if ref is not None:
                references.append(ref)
        # sort
        references.sort(key=lambda x: (x.object_number or 0))

        # insert magic entry if needed
        if len(references) == 0 or references[0].generation_number != 65535:
            references.insert(
                0,
                Reference(
                    generation_number=65535,
                    object_number=0,
                    byte_offset=0,
                    is_in_use=False,
                ),
            )

        # divide into sections
        sections = [[references[0]]]
        for i in range(1, len(references)):
            ref = references[i]
            prev_object_number = sections[-1][-1].object_number
            assert prev_object_number is not None
            if ref.object_number == prev_object_number + 1:
                sections[-1].append(ref)
            else:
                sections.append([ref])

        # return
        return sections

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is an XREF table
        :param object:  the object to be transformed
        :return:        True if the object is an XREF table, False otherwise
        """
        return isinstance(object, XREF)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms an XREF Object into a byte stream
        :param object_to_transform:     the XREF Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) XREF Object
        """
        assert isinstance(object_to_transform, XREF)
        assert "Trailer" in object_to_transform
        assert isinstance(object_to_transform["Trailer"], Dictionary)
        # fmt: off
        assert context is not None, "A WriteTransformerState must be defined in order to write XREF objects."
        assert context.destination is not None, "A WriteTransformerState must be defined in order to write XREF objects."
        # fmt: on

        # Transform the Trailer dictionary (replacing objects by references)
        # we do this upfront because the normal write_dictionary_transformer will write the dictionary first,
        # and the references afterwards. This would cause the /Trailer dictionary to not be the last.
        trailer_out = Dictionary()

        # /Root
        # fmt: off
        trailer_out[Name("Root")] = self.get_reference(object_to_transform["Trailer"]["Root"], context)
        # fmt: on

        # /Info
        # fmt: off
        if "Info" in object_to_transform["Trailer"]:
            trailer_out[Name("Info")] = self.get_reference(object_to_transform["Trailer"]["Info"], context)
        # fmt: on

        # /Size
        # fmt: off
        if ("Trailer" in object_to_transform and "Size" in object_to_transform["Trailer"]):
            trailer_out[Name("Size")] = object_to_transform["Trailer"]["Size"]
        else:
            trailer_out[Name("Size")] = bDecimal(0)  # we'll recalculate this later anyway
        # fmt: on

        # /ID
        if "ID" in object_to_transform["Trailer"]:
            trailer_out[Name("ID")] = object_to_transform["Trailer"]["ID"]

        # write /Info object
        # fmt: off
        if "Info" in object_to_transform["Trailer"]:
            self.get_root_transformer().transform(object_to_transform["Trailer"]["Info"], context)
        # fmt: on

        # write /Root /StructTreeRoot
        # TODO

        # write /Root object
        # fmt: off
        self.get_root_transformer().transform(object_to_transform["Trailer"]["Root"], context)
        # fmt: on

        # write /XREF
        start_of_xref = context.destination.tell()
        context.destination.write(bytes("xref\n", "latin1"))
        for section in self._section_xref(context):
            context.destination.write(
                bytes("%d %d\n" % (section[0].object_number, len(section)), "latin1")
            )
            for r in section:
                if r.is_in_use:
                    context.destination.write(
                        bytes("{0:010d} 00000 n\r\n".format(r.byte_offset), "latin1")
                    )
                else:
                    context.destination.write(
                        bytes("{0:010d} 00000 f\r\n".format(r.byte_offset), "latin1")
                    )

        # update /Size
        trailer_out[Name("Size")] = bDecimal(
            sum([len(v) for k, v in context.indirect_objects_by_hash.items()]) + 1
        )

        # write /Trailer
        context.destination.write(bytes("trailer\n", "latin1"))
        self.get_root_transformer().transform(trailer_out, context)
        context.destination.write(bytes("startxref\n", "latin1"))

        # write byte offset of last cross-reference section
        context.destination.write(bytes(str(start_of_xref) + "\n", "latin1"))

        # write EOF
        context.destination.write(bytes("%%EOF", "latin1"))
