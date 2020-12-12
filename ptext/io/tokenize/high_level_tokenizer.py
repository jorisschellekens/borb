import re
from typing import Optional

from ptext.exception.pdf_exception import PDFEOFError, PDFTypeError, PDFSyntaxError
from ptext.io.tokenize.low_level_tokenizer import LowLevelTokenizer, TokenType
from ptext.io.tokenize.types.pdf_array import PDFArray
from ptext.io.tokenize.types.pdf_boolean import PDFBoolean
from ptext.io.tokenize.types.pdf_canvas_operator_name import PDFCanvasOperatorName
from ptext.io.tokenize.types.pdf_dictionary import PDFDictionary
from ptext.io.tokenize.types.pdf_indirect_reference import PDFIndirectReference
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_number import PDFInt, PDFFloat
from ptext.io.tokenize.types.pdf_object import PDFObject, PDFIndirectObject
from ptext.io.tokenize.types.pdf_stream import PDFStream
from ptext.io.tokenize.types.pdf_string import PDFHexString, PDFLiteralString


class HighLevelTokenizer(LowLevelTokenizer):
    def read_array(self) -> PDFArray:
        """
        This method processes the next tokens and returns a PDFArray.
        It fails and throws various errors if the next tokens do not represent a PDFArray.
        """
        token = self.next_non_comment_token()
        if token is None:
            raise PDFEOFError()
        if token.token_type != TokenType.START_ARRAY:
            raise PDFSyntaxError(message="invalid array", byte_offset=token.byte_offset)

        out = PDFArray()

        while True:
            token = self.next_non_comment_token()
            if token is None:
                raise PDFEOFError()
            if token.token_type == TokenType.END_ARRAY:
                break
            if token.token_type == TokenType.END_DICT:
                raise PDFSyntaxError(
                    message="unexpected end of dictionary",
                    byte_offset=token.byte_offset,
                )

            # go back
            self.seek(token.byte_offset)

            # read
            obj = self.read_object()

            # append
            out.append(obj)

        # return
        return out

    def read_dictionary(self) -> PDFDictionary:
        """
        This method processes the next tokens and returns a PDFDictionary.
        It fails and throws various errors if the next tokens do not represent a PDFDictionary.
        """
        token = self.next_non_comment_token()
        if token is None:
            raise PDFEOFError()
        if token.token_type != TokenType.START_DICT:
            raise PDFSyntaxError(
                message="invalid dictionary", byte_offset=token.byte_offset
            )

        out_dict = PDFDictionary()
        while True:

            # attempt to read name token
            token = self.next_non_comment_token()
            if token is None:
                raise PDFEOFError()
            if token.token_type == TokenType.END_DICT:
                break
            if token.token_type != TokenType.NAME:
                raise PDFSyntaxError(
                    message="dictionary key must be a name",
                    byte_offset=token.byte_offset,
                )

            # store name
            name = PDFName(token.text[1:])

            # attempt to read value
            value = self.read_object()
            if value is None:
                raise PDFSyntaxError(
                    message="unexpected end of dictionary",
                    byte_offset=token.byte_offset,
                )

            # store in dict object
            if name is not None:
                out_dict[name] = value

        return out_dict

    def read_indirect_object(self) -> Optional[PDFObject]:
        """
        This method processes the next tokens and returns an indirect PDFObject.
        It fails and throws various errors if the next tokens do not represent an indirect PDFObject.
        """

        # read object number
        token = self.next_non_comment_token()
        if token.token_type != TokenType.NUMBER or not re.match("^[0-9]+$", token.text):
            return None
        object_number = PDFInt(int(token.text))

        # read generation number
        token = self.next_non_comment_token()
        byte_offset = token.byte_offset
        if token.token_type != TokenType.NUMBER or not re.match("^[0-9]+$", token.text):
            self.seek(byte_offset)
            return None
        generation_number = PDFInt(int(token.text))

        # read 'obj'
        token = self.next_non_comment_token()
        if token.token_type != TokenType.OTHER or token.text != "obj":
            self.seek(byte_offset)
            return None

        # read obj
        return PDFIndirectObject(
            object=self.read_object(),
            indirect_reference=PDFIndirectReference(
                object_number=object_number, generation_number=generation_number
            ),
        )

    def read_indirect_reference(self) -> Optional[PDFObject]:
        """
        This method processes the next tokens and returns an indirect reference.
        It fails and throws various errors if the next tokens do not represent an indirect reference.
        """

        # read object number
        token = self.next_non_comment_token()
        if token.token_type != TokenType.NUMBER or not re.match("^[0-9]+$", token.text):
            return None
        object_number = PDFInt(int(token.text))

        # read generation number
        token = self.next_non_comment_token()
        byte_offset = token.byte_offset
        if token.token_type != TokenType.NUMBER or not re.match("^[0-9]+$", token.text):
            self.seek(byte_offset)
            return None
        generation_number = PDFInt(int(token.text))

        # read 'R'
        token = self.next_non_comment_token()
        if token.token_type != TokenType.OTHER or token.text != "R":
            self.seek(byte_offset)
            return None

        # return
        return PDFIndirectReference(
            object_number=object_number,
            generation_number=generation_number,
        )

    def read_object(self, xref: Optional["XREF"] = None) -> Optional[PDFObject]:

        token = self.next_non_comment_token()
        if token is None or len(token.text) == 0:
            return None

        if token.token_type == TokenType.START_DICT:
            self.seek(token.byte_offset)  # go to start of dictionary
            return self.read_dictionary()

        if token.token_type == TokenType.START_ARRAY:
            self.seek(token.byte_offset)  # go to start of array
            return self.read_array()

        # <number> <number> "R"
        if token.token_type == TokenType.NUMBER:
            self.seek(token.byte_offset)  # go to start of indirect reference
            potential_indirect_reference = self.read_indirect_reference()
            if potential_indirect_reference is not None:
                return potential_indirect_reference

        # <number> <number> "obj"
        # <<dictionary>>
        # "stream"
        # <bytes>
        # "endstream"
        if token.token_type == TokenType.NUMBER:
            self.seek(token.byte_offset)
            potential_stream = self.read_stream(xref)
            if potential_stream is not None:
                return potential_stream

        # <number> <number> "obj"
        if token.token_type == TokenType.NUMBER:
            self.seek(token.byte_offset)
            potential_indirect_object = self.read_indirect_object()
            if potential_indirect_object is not None:
                return potential_indirect_object

        # numbers
        if token.token_type == TokenType.NUMBER:
            if "." in token.text:
                return PDFFloat(float(token.text))
            else:
                return PDFInt(int(token.text))

        # boolean
        if token.token_type == TokenType.OTHER and token.text in ["true", "false"]:
            return PDFBoolean(True) if token.text == "true" else PDFBoolean(False)

        # canvas operators
        if (
            token.token_type == TokenType.OTHER
            and token.text in PDFCanvasOperatorName.NAMES
        ):
            return PDFCanvasOperatorName(token.text)

        # names
        if token.token_type == TokenType.NAME:
            return PDFName(token.text[1:])

        # literal strings and hex strings
        if token.token_type in [TokenType.STRING, TokenType.HEX_STRING]:
            if token.token_type == TokenType.STRING:
                return PDFLiteralString(token.text[1:-1])
            else:
                return PDFHexString(token.text[1:-1])

    def read_stream(self, xref: Optional["XREF"] = None) -> Optional[PDFObject]:

        byte_offset = self.tell()

        # attempt to read <number> <number> obj
        # followed by dictionary
        optional_stream_dictionary = self.read_indirect_object()
        if optional_stream_dictionary is None or not isinstance(
            optional_stream_dictionary, PDFIndirectObject
        ):
            self.seek(byte_offset)
            return None

        # separate indirect reference
        indirect_reference = optional_stream_dictionary.indirect_reference
        optional_stream_dictionary = optional_stream_dictionary.get_object()

        # attempt to read keyword "stream"
        stream_token = self.next_non_comment_token()
        if stream_token.token_type != TokenType.OTHER or stream_token.text != "stream":
            self.seek(byte_offset)
            return None

        # process \Length
        length_name = PDFName("Length")
        if length_name not in optional_stream_dictionary:
            raise PDFTypeError(received_type=None, expected_type=PDFInt)
        if (
            isinstance(optional_stream_dictionary[length_name], PDFIndirectReference)
            and xref is not None
        ):
            # store current position
            pos_before = self.tell()
            # read length (indirect reference)
            length_of_stream = (
                xref.get_object_for_indirect_reference(
                    optional_stream_dictionary[length_name], self.io_source, self
                )
                .get_object()
                .get_int_value()
            )
            # restore current position
            self.seek(pos_before)
        else:
            length_of_stream = optional_stream_dictionary[length_name].get_int_value()

        # process newline
        ch = self._next_char()
        if ch not in ["\r", "\n"]:
            raise PDFSyntaxError(
                "The keyword stream that follows the stream dictionary shall be followed by an end-of-line marker consisting of either a CARRIAGE RETURN and a LINE FEED or just a LINE FEED, and not by a CARRIAGE RETURN alone.",
                byte_offset=self.tell(),
            )
        if ch == "\r":
            ch = self._next_char()
            if ch != "\n":
                raise PDFSyntaxError(
                    "The keyword stream that follows the stream dictionary shall be followed by an end-of-line marker consisting of either a CARRIAGE RETURN and a LINE FEED or just a LINE FEED, and not by a CARRIAGE RETURN alone.",
                    byte_offset=self.tell(),
                )

        bytes = self.io_source.read(length_of_stream)

        # attempt to read token "endstream"
        end_of_stream_token = self.next_non_comment_token()
        if (
            end_of_stream_token.token_type != TokenType.OTHER
            or end_of_stream_token.text != "endstream"
        ):
            raise PDFSyntaxError(
                "A stream shall consist of a dictionary followed by zero or more bytes bracketed between the keywords stream (followed by newline) and endstream",
                byte_offset=self.tell(),
            )

        # return PDFStream
        return PDFIndirectObject(
            object=PDFStream(
                stream_dictionary=optional_stream_dictionary,
                raw_byte_array=bytes,
            ),
            indirect_reference=indirect_reference,
        )
