import io
from typing import Optional, List, Union

from ptext.exception.pdf_exception import (
    PDFSyntaxError,
)
from ptext.io.read_transform.types import Reference, Dictionary
from ptext.io.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.tokenize.low_level_tokenizer import TokenType
from ptext.pdf.xref.xref import XREF


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
        src: Union[io.BufferedIOBase, io.RawIOBase],
        tok: HighLevelTokenizer,
        initial_offset: Optional[int] = None,
    ) -> "XREF":

        if initial_offset is not None:
            src.seek(initial_offset)
        else:
            self._seek_to_xref_token(src, tok)

        # now we should be back to the start of XREF
        token = tok.next_non_comment_token()
        assert token is not None
        assert token.text == "xref"

        # read xref sections
        while True:
            xref_section = self._read_section(src, tok)
            if len(xref_section) == 0:
                break
            else:
                for r in xref_section:
                    self.append(r)

        # process trailer
        self["Trailer"] = self._read_trailer(src, tok)

        # return self
        return self

    def _read_section(self, src: io.IOBase, tok: HighLevelTokenizer) -> List[Reference]:

        tokens = [tok.next_non_comment_token() for _ in range(0, 2)]
        assert tokens[0] is not None
        assert tokens[1] is not None
        if tokens[0].text in ["trailer", "startxref"]:
            src.seek(tokens[0].byte_offset)
            return []
        assert tokens[0].token_type == TokenType.NUMBER
        assert tokens[1].token_type == TokenType.NUMBER

        start_object_number = int(tokens[0].text)
        number_of_objects = int(tokens[1].text)
        indirect_references = []

        # read subsection
        for i in range(0, number_of_objects):
            tokens = [tok.next_non_comment_token() for _ in range(0, 3)]
            assert tokens[0] is not None
            assert tokens[1] is not None
            assert tokens[2] is not None
            if tokens[0].text in ["trailer", "startxref"]:
                raise PDFSyntaxError(
                    byte_offset=tokens[0].byte_offset,
                    message="unexpected EOF while processing XREF",
                )
            if (
                tokens[0].token_type != TokenType.NUMBER
                or tokens[1].token_type != TokenType.NUMBER
                or tokens[2].token_type != TokenType.OTHER
                or tokens[2].text not in ["f", "n"]
            ):
                raise PDFSyntaxError(
                    byte_offset=tokens[0].byte_offset,
                    message="invalid XREF line",
                )

            indirect_references.append(
                Reference(
                    object_number=start_object_number + i,
                    byte_offset=int(tokens[0].text),
                    generation_number=int(tokens[1].text),
                    is_in_use=(tokens[2].text == "n"),
                )
            )

        # return
        return indirect_references

    def _read_trailer(self, src: io.IOBase, tok: HighLevelTokenizer) -> Dictionary:

        # return None if there is no trailer
        token = tok.next_non_comment_token()
        assert token is not None
        if token.text != "trailer":
            return Dictionary()

        # if there is a keyword "trailer" the next token should be TokenType.START_DICT
        token = tok.next_non_comment_token()
        assert token is not None
        if token.token_type != TokenType.START_DICT:
            raise PDFSyntaxError(
                byte_offset=tok.tell(),
                message="invalid XREF trailer",
            )

        # go back 2 chars "<<"
        src.seek(-2, io.SEEK_CUR)

        # read dictionary as trailer
        trailer_dict = tok.read_dictionary()

        # process startxref
        token = tok.next_non_comment_token()
        assert token is not None
        if token.token_type != TokenType.OTHER or token.text != "startxref":
            raise PDFSyntaxError(
                byte_offset=token.byte_offset,
                message="start of XREF not found",
            )

        # return
        return trailer_dict
