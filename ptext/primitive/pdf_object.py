class PDFObject:
    def __init__(self):
        pass


class PDFDirectObject(PDFObject):
    def __init_(self):
        super().__init__()


class PDFIndirectObject(PDFObject):
    """
    Any object in a PDF file may be labelled as an indirect object. This gives the object a unique object identifier by
    which other objects can refer to it (for example, as an element of an array or as the value of a dictionary entry).
    The object identifier shall consist of two parts:
    • A positive integer object number. Indirect objects may be numbered sequentially within a PDF file, but this
    is not required; object numbers may be assigned in any arbitrary order.
    • A non-negative integer generation number. In a newly created file, all indirect objects shall have generation
    numbers of 0. Nonzero generation numbers may be introduced when the file is later updated; see sub-
    clauses 7.5.4, "Cross-Reference Table" and 7.5.6, "Incremental Updates."
    """

    def __init__(self, object: PDFObject, indirect_reference: PDFObject):
        super().__init__()
        self.indirect_reference = indirect_reference
        self.object = object

    def get_object(self) -> PDFObject:
        return self.object

    def get_indirect_reference(self) -> PDFObject:
        return self.indirect_reference

    def __eq__(self, other):
        return (
            other.indirect_reference == self.indirect_reference
            if isinstance(other, PDFIndirectObject)
            else False
        )

    def __hash__(self):
        return hash(self.indirect_reference)
