from typing import Optional

from ptext.io.read_transform.types import AnyPDFType, Dictionary, Name, Reference
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    TransformerWriteContext,
)
from ptext.pdf.xref.xref import XREF


class WriteXREFTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, XREF)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[TransformerWriteContext] = None,
    ):
        assert isinstance(object_to_transform, XREF)
        assert "Trailer" in object_to_transform
        assert isinstance(object_to_transform["Trailer"], Dictionary)
        assert context is not None
        assert context.destination is not None

        # transform Trailer dictionary (replacing objects by references)
        trailer_out = Dictionary()
        trailer_out[Name("Root")] = self.get_reference(
            object_to_transform["Trailer"]["Root"], context
        )
        trailer_out[Name("Info")] = self.get_reference(
            object_to_transform["Trailer"]["Info"], context
        )
        trailer_out[Name("Size")] = object_to_transform["Trailer"]["Size"]
        trailer_out[Name("ID")] = self.get_reference(
            object_to_transform["Trailer"]["ID"], context
        )

        # write Root object
        self.get_root_transformer().transform(
            object_to_transform["Trailer"]["Root"], context
        )

        # write Info object
        self.get_root_transformer().transform(
            object_to_transform["Trailer"]["Info"], context
        )

        # write ID object
        self.get_root_transformer().transform(
            object_to_transform["Trailer"]["ID"], context
        )

        # write XREF
        start_of_xref = context.destination.tell()
        context.destination.write(bytes("xref\n", "latin1"))
        for section in self._section_xref(context):
            context.destination.write(
                bytes("%d %d\n" % (section[0].object_number, len(section)), "latin1")
            )
            for r in section:
                if r.is_in_use:
                    context.destination.write(
                        bytes("{0:010d} 00000 n\n".format(r.byte_offset), "latin1")
                    )
                else:
                    context.destination.write(
                        bytes("{0:010d} 00000 f\n".format(r.byte_offset), "latin1")
                    )

        # write Trailer
        context.destination.write(bytes("trailer\n", "latin1"))
        self.get_root_transformer().transform(trailer_out, context)
        context.destination.write(bytes("startxref\n", "latin1"))

        # write byte offset of last cross-reference section
        context.destination.write(bytes(str(start_of_xref) + "\n", "latin1"))

        # write EOF
        context.destination.write(bytes("%%EOF", "latin1"))

    def _section_xref(self, context: Optional[TransformerWriteContext] = None):
        assert context is not None

        # get all references
        references = []
        for obj in context.indirect_objects:
            ref = obj.get_reference()  # type: ignore [union-attr]
            if ref is not None:
                references.append(ref)
        # sort
        references.sort(key=lambda x: x.object_number)

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
            if ref.object_number == prev_object_number + 1:
                sections[-1].append(ref)
            else:
                sections.append([ref])

        # return
        return sections
