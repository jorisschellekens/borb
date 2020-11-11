from typing import Optional, List

from ptext.object.pdf_high_level_object import PDFHighLevelObject
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_number import PDFInt
from ptext.primitive.pdf_string import PDFString


class DocumentInfo(PDFHighLevelObject):
    def __init__(self, document: "Document"):
        super().__init__()
        self.document = document

    def get_title(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The document’s title.
        """
        i = self.document.get(["XRef", "Trailer", "Info", "Title"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_creator(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that created the original document
        from which it was converted.
        """
        i = self.document.get(["XRef", "Trailer", "Info", "Creator"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_author(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The name of the person who created the document.
        """
        i = self.document.get(["XRef", "Trailer", "Info", "Author"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_creation_date(self) -> Optional[str]:
        """
        (Optional) The date and time the document was created, in human-
        readable form (see 7.9.4, “Dates”).
        """
        i = self.document.get(["XRef", "Trailer", "Info", "CreationDate"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_modification_date(self) -> Optional[str]:
        """
        Required if PieceInfo is present in the document catalogue;
        otherwise optional; PDF 1.1) The date and time the document was
        most recently modified, in human-readable form (see 7.9.4, “Dates”).
        """
        i = self.document.get(["XRef", "Trailer", "Info", "ModDate"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_subject(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The subject of the document.
        """
        i = self.document.get(["XRef", "Trailer", "Info", "Subject"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_keywords(self) -> Optional[List[str]]:
        """
        (Optional; PDF 1.1) Keywords associated with the document.
        """
        i = self.document.get(["XRef", "Trailer", "Info", "Keywords"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_producer(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that converted it to PDF.
        """
        i = self.document.get(["XRef", "Trailer", "Info", "Producer"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None

    def get_number_of_pages(self) -> Optional[int]:
        i = self.document.get(["XRef", "Trailer", "Root", "Pages", "Count"])
        return i.get_int_value() if i != PDFNull() and isinstance(i, PDFInt) else None

    def get_file_size(self) -> Optional[int]:
        return self.document.get("FileSize").get_int_value()

    def get_ids(self) -> Optional[List[str]]:
        """
        File identifiers shall be defined by the optional ID entry in a PDF file’s trailer dictionary (see 7.5.5, “File Trailer”).
        The ID entry is optional but should be used. The value of this entry shall be an array of two byte strings. The
        first byte string shall be a permanent identifier based on the contents of the file at the time it was originally
        created and shall not change when the file is incrementally updated. The second byte string shall be a
        changing identifier based on the file’s contents at the time it was last updated. When a file is first written, both
        identifiers shall be set to the same value. If both identifiers match when a file reference is resolved, it is very
        likely that the correct and unchanged file has been found. If only the first identifier matches, a different version
        of the correct file has been found.
        """
        i = self.document.get(["XRef", "Trailer", "ID"])
        return [i.get(0).get_text(), i.get(1).get_text()] if i != PDFNull() else None

    def get_language(self) -> Optional[str]:
        """
        (Optional; PDF 1.4) A language identifier that shall specify the
        natural language for all text in the document except where
        overridden by language specifications for structure elements or
        marked content (see 14.9.2, "Natural Language Specification"). If
        this entry is absent, the language shall be considered unknown.
        """
        i = self.document.get(["XRef", "Trailer", "Root", "Lang"])
        return i.get_text() if i != PDFNull() and isinstance(i, PDFString) else None
