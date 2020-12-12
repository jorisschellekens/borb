import io
from typing import Optional, List

from ptext.exception.pdf_exception import (
    XREFTokenNotFoundError,
    PDFValueError,
)
from ptext.io.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.tokenize.low_level_tokenizer import TokenType
from ptext.pdf.xref.xref import XREF
from ptext.io.tokenize.types.pdf_boolean import PDFBoolean
from ptext.io.tokenize.types.pdf_dictionary import PDFDictionary
from ptext.io.tokenize.types.pdf_indirect_reference import PDFIndirectReference
from ptext.io.tokenize.types.pdf_number import PDFInt


class PlainTextXREF(XREF):
    """
    The cross-reference table contains information that permits random access to indirect objects within the file so
    that the entire file need not be read to locate any particular object. The table shall contain a one-line entry for
    each indirect object, specifying the byte offset of that object within the body of the file. (Beginning with PDF 1.5,
    some or all of the cross-reference information may alternatively be contained in cross-reference streams; see
    7.5.8, "Cross-Reference Streams.")

    NOTE 1
    The cross-reference table is the only part of a PDF file with a fixed format, which permits entries in the table to
    be accessed randomly.
    The table comprises one or more cross-reference sections. Initially, the entire table consists of a single section
    (or two sections if the file is linearized; see Annex F). One additional section shall be added each time the file is
    incrementally updated (see 7.5.6, "Incremental Updates").

    Each cross-reference section shall begin with a line containing the keyword xref. Following this line shall be
    one or more cross-reference subsections, which may appear in any order. For a file that has never been
    incrementally updated, the cross-reference section shall contain only one subsection, whose object numbering
    begins at 0.
    """

    def __init__(self):
        super().__init__()

    def read(
        self,
        src: io.IOBase,
        tok: HighLevelTokenizer,
        initial_offset: Optional[int] = None,
    ) -> "PDFHighLevelObject":

        if initial_offset is not None:
            src.seek(initial_offset)
        else:
            self._seek_to_xref_token(src, tok)

        # now we should be back to the start of XREF
        token = tok.next_non_comment_token()
        if token.text != "xref":
            raise XREFTokenNotFoundError()

        # read xref sections
        while True:
            xref_section = self._read_section(src, tok)
            if len(xref_section) == 0:
                break
            else:
                for r in xref_section:
                    self.add_indirect_reference(r)

        # process trailer
        trailer = self._read_trailer(src, tok)
        self["Trailer"] = trailer

        # return self
        return self

    def _read_section(
        self, src: io.IOBase, tok: HighLevelTokenizer
    ) -> List[PDFIndirectReference]:

        tokens = [tok.next_non_comment_token() for _ in range(0, 2)]
        if tokens[0].text in ["trailer", "startxref"]:
            src.seek(tokens[0].byte_offset)
            return []
        if tokens[0].token_type != TokenType.NUMBER:
            raise PDFValueError(
                expected_type_description="number", received_type_description=tokens[0]
            )
        if tokens[1].token_type != TokenType.NUMBER:
            raise PDFValueError(
                expected_type_description="number", received_type_description=tokens[1]
            )

        start_object_number = int(tokens[0].text)
        number_of_objects = int(tokens[1].text)
        indirect_references = []

        # read subsection
        for i in range(0, number_of_objects):
            tokens = [tok.next_non_comment_token() for _ in range(0, 3)]
            if tokens[0].text in ["trailer", "startxref"]:
                raise UnexpectedEndOfXREF(
                    start_byte_position=tokens[0].byte_offset,
                    stop_byte_position=tokens[0].byte_offset,
                )
            if (
                tokens[0].token_type != TokenType.NUMBER
                or tokens[1].token_type != TokenType.NUMBER
                or tokens[2].token_type != TokenType.OTHER
                or tokens[2].text not in ["f", "n"]
            ):
                raise InvalidXREFLine(
                    start_byte_position=tokens[0].byte_offset,
                    stop_byte_position=tokens[2].byte_offset,
                )

            indirect_references.append(
                PDFIndirectReference(
                    object_number=PDFInt(start_object_number + i),
                    byte_offset=PDFInt(int(tokens[0].text)),
                    generation_number=PDFInt(int(tokens[1].text)),
                    is_in_use=PDFBoolean(tokens[2].text == "n"),
                )
            )

        # return
        return indirect_references

    def _read_trailer(self, src: io.IOBase, tok: HighLevelTokenizer) -> PDFDictionary:

        # return None if there is no trailer
        if tok.next_non_comment_token().text != "trailer":
            return PDFDictionary()

        # if there is a keyword "trailer" the next token should be TokenType.START_DICT
        if tok.next_non_comment_token().token_type != TokenType.START_DICT:
            raise MalFormedTrailer(
                start_byte_position=self.tokenizer.tell(),
                stop_byte_position=self.tokenizer.tell(),
            )

        # go back 2 chars "<<"
        src.seek(-2, io.SEEK_CUR)

        # read dictionary as trailer
        trailer_dict = tok.read_dictionary()

        # process startxref
        end_of_xref_token = tok.next_non_comment_token()
        if (
            end_of_xref_token.token_type != TokenType.OTHER
            or end_of_xref_token.text != "startxref"
        ):
            raise StartXREFTokenNotFound()

        # return
        return trailer_dict
