from typing import Optional

from ptext.io.tokenize.types.pdf_boolean import PDFBoolean
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class PDFIndirectReference(PDFObject):
    """
    Any object in a PDF file may be labelled as an indirect object. This gives the object a unique object identifier by
    which other objects can refer to it (for example, as an element of an array or as the value of a dictionary entry).
    The object identifier shall consist of two parts:
    • A positive integer object number. Indirect objects may be numbered sequentially within a PDF file, but this
    is not required; object numbers may be assigned in any arbitrary order.
    • A non-negative integer generation number. In a newly created file, all indirect objects shall have generation
    numbers of 0. Nonzero generation numbers may be introduced when the file is later updated; see sub-
    clauses 7.5.4, "Cross-Reference Table" and 7.5.6, "Incremental Updates."
    Together, the combination of an object number and a generation number shall uniquely identify an indirect
    object.

    The object may be referred to from elsewhere in the file by an indirect reference. Such indirect references shall
    consist of the object number, the generation number, and the keyword R (with white space separating each
    part)
    """

    def __init__(
        self,
        document: Optional["Document"] = None,
        byte_offset: Optional[PDFNumber] = None,
        object_number: Optional[PDFNumber] = None,
        generation_number: Optional[PDFNumber] = None,
        parent_stream_object_number: Optional[PDFNumber] = None,
        index_in_parent_stream_object: Optional[PDFNumber] = None,
        is_in_use: Optional[PDFBoolean] = PDFBoolean(True),
    ):
        super().__init__()
        self.document = document
        self.byte_offset = byte_offset
        self.object_number = object_number
        self.generation_number = generation_number
        self.parent_stream_object_number = parent_stream_object_number
        self.index_in_parent_stream_object = index_in_parent_stream_object
        self.is_in_use = is_in_use

    def get_generation_number(self) -> Optional[PDFNumber]:
        return self.generation_number

    def get_index_in_stream(self) -> Optional[PDFNumber]:
        return self.index_in_parent_stream_object

    def get_is_in_use(self) -> Optional[PDFBoolean]:
        return self.is_in_use

    def get_object_number(self) -> Optional[PDFNumber]:
        return self.object_number

    def get_parent_stream_number(self) -> Optional[PDFNumber]:
        return self.parent_stream_object_number

    def __eq__(self, other):
        if not isinstance(other, PDFIndirectReference):
            return False

        if self.byte_offset is not None and other.byte_offset is not None:
            return self.byte_offset.get_int_value() == other.byte_offset.get_int_value()

        if (
            self.object_number is not None
            and other.object_number is not None
            and self.generation_number is not None
            and other.generation_number is not None
        ):
            return (
                other.object_number.get_int_value()
                == self.object_number.get_int_value()
                and other.generation_number.get_int_value()
                == self.generation_number.get_int_value()
            )

        return False

    def __hash__(self):
        prime = 97
        h = 0
        h += (
            prime * self.byte_offset.get_int_value()
            if self.byte_offset is not None
            else 0
        )
        h += (
            prime * self.object_number.get_int_value()
            if self.object_number is not None
            else 0
        )
        h += (
            prime * self.generation_number.get_int_value()
            if self.generation_number is not None
            else 0
        )
        return h

    def __str__(self):
        if self.byte_offset is not None:
            return (
                str(self.byte_offset)
                + " "
                + str(self.generation_number)
                + " "
                + ("n" if self.is_in_use == PDFBoolean(True) else "f")
            )
        else:
            return str(self.object_number) + " " + str(self.generation_number) + " R"
