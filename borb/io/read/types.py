#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module defines all the base types used in processing PDFs
e.g. Boolean, CanvasOperatorName, Decimal, Dictionary, Element, Name, Stream, String, ..
"""
import copy
import typing
import xml.etree.ElementTree
from decimal import Decimal as oDecimal
import math

from borb.io.read.pdf_object import PDFObject
from borb.io.read.postfix.postfix_eval import PostScriptEval


class Boolean(PDFObject):
    """
    Boolean objects represent the logical values of true and false. They appear in PDF files using the keywords
    true and false.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, value: bool):
        super(Boolean, self).__init__()
        self._value = value

    #
    # PRIVATE
    #

    def __bool__(self):
        return self._value

    def __eq__(self, other):
        if isinstance(other, bool):
            return other == self._value
        if isinstance(other, Boolean):
            return other._value == self._value
        return False

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        if self._value:
            return "True"
        else:
            return "False"

    #
    # PUBLIC
    #


class CanvasOperatorName(PDFObject):
    """
    This class represents a canvas operator name in PDF syntax
    """

    # fmt: off
    VALID_NAMES = [
        "b", "B", "b*", "B*", "BDC", "BI", "BMC", "BT", "BX",
        "c", "cm", "cs", "CS",
        "d", "d0", "d1", "Do", "DP",
        "EI", "EMC", "ET", "EX",
        "f", "F", "f*",
        "g", "G", "gs",
        "h",
        "i", "ID",
        "j", "J",
        "k", "K",
        "l",
        "m", "M", "MP",
        "n",
        "q", "Q",
        "re", "RG", "rg", "ri",
        "s", "S", "sc", "SC", "SCN", "scn", "sh",
        "T*", "Tc", "Td", "TD", "Tf", "Tj", "TJ", "TL", "Tm", "Tr", "Ts", "Tw", "Tz",
        "v",
        "w", "W", "W*",
        "y",
        "'",
        '"',
    ]
    # fmt: on

    #
    # CONSTRUCTOR
    #

    def __init__(self, text: str):
        super(CanvasOperatorName, self).__init__()
        self._text = text

    #
    # PRIVATE
    #

    def __eq__(self, other):
        if isinstance(other, CanvasOperatorName):
            return other._text == self._text
        if isinstance(other, str):
            return other == self._text
        return False

    def __hash__(self):
        return self._text.__hash__()

    def __str__(self):
        return self._text

    #
    # PUBLIC
    #


class Decimal(PDFObject, oDecimal):  # type: ignore[no-redef]
    """
    PDF provides two types of numeric objects: integer and real. Integer objects represent mathematical integers.
    Real objects represent mathematical real numbers. The range and precision of numbers may be limited by the
    internal representations used in the computer on which the conforming reader is running; Annex C gives these
    limits for typical implementations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, obj: typing.Union[str, float, int, oDecimal]):
        super(Decimal, self).__init__()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #


class Dictionary(PDFObject, dict):
    """
    A dictionary object is an associative table containing pairs of objects, known as the dictionary’s entries. The first
    element of each entry is the key and the second element is the value. The key shall be a name (unlike
    dictionary keys in PostScript, which may be objects of any type). The value may be any kind of object, including
    another dictionary. A dictionary entry whose value is null (see 7.3.9, "Null Object") shall be treated the same as
    if the entry does not exist. (This differs from PostScript, where null behaves like any other object as the value
    of a dictionary entry.) The number of entries in a dictionary shall be subject to an implementation limit; see
    Annex C. A dictionary may have zero entries.

    The entries in a dictionary represent an associative table and as such shall be unordered even though an
    arbitrary order may be imposed upon them when written in a file. That ordering shall be ignored.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(Dictionary, self).__init__()

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        out = type(self).__new__(type(self))
        Dictionary.__init__(out)
        for k, v in self.items():
            out[copy.deepcopy(k, memodict)] = copy.deepcopy(v, memodict)
        return out

    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode

    def __setitem__(self, key, value):
        assert isinstance(key, Name)
        super(Dictionary, self).__setitem__(key, value)

    #
    # PUBLIC
    #


class Element(PDFObject, xml.etree.ElementTree.Element):
    """
    An XML element.

    This class is the reference implementation of the Element interface.

    An element's length is its number of subelements.  That means if you
    want to check if an element is truly empty, you should check BOTH
    its length AND its text attribute.

    The element tag, attribute names, and attribute values can be either
    bytes or strings.

    *tag* is the element name.  *attrib* is an optional dictionary containing
    element attributes. *extra* are additional element attributes given as
    keyword arguments.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, tag, **extra):
        super().__init__()
        # super(Element, self).__init__(tag, **extra)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #


class Function(Dictionary):
    """
    A function object may be a dictionary or a stream, depending on the type of function. The term function
    dictionary is used generically in this sub-clause to refer to either a dictionary object or the dictionary portion of a
    stream object. A function dictionary specifies the function’s representation, the set of attributes that
    parameterize that representation, and the additional data needed by that representation. Four types of
    functions are available, as indicated by the dictionary’s FunctionType entry.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(Function, self).__init__()

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        out: Function = Function()
        for k, v in self.items():
            out[k] = copy.deepcopy(v, memodict)
        return out

    def _get_sample(self, sample_number: int) -> typing.List[oDecimal]:
        # fmt: off
        n: int = int(len(self["Range"]) / 2)
        bps: int = int(self["BitsPerSample"])
        byte_start_index: int = math.floor((sample_number * bps * n) / 8)
        byte_stop_index: int = min(byte_start_index + math.ceil((n * bps) / 8), len(self["DecodedBytes"]))
        bit_offset: int = (sample_number * bps * n) - byte_start_index * 8
        # fmt: on

        # fmt: off
        bytes_to_use: bytes = self["DecodedBytes"][byte_start_index:byte_stop_index]
        byte_str: str = "".join([bin(x)[2:].zfill(8) for x in bytes_to_use])[bit_offset : (bit_offset + n * bps)]
        ys: typing.List[oDecimal] = [Decimal(int(byte_str[i : i + bps], 2)) for i in range(0, len(byte_str), bps)]
        # fmt: on

        # return
        return ys

    def _get_sample_number(self, sample: typing.List[oDecimal]) -> typing.Optional[int]:
        size: typing.List[int] = [int(x) for x in self["Size"]]
        N: int = 1
        for s in size:
            N *= s
        F: typing.List[int] = [int(N / size[0])]
        for i in range(1, len(size)):
            F[i] = int(F[i - 1] / size[i])
        return sum([F[i] * int(sample[i]) for i in range(0, len(sample))])

    @staticmethod
    def _interpolate(
        x: oDecimal, x_min: oDecimal, x_max: oDecimal, y_min: oDecimal, y_max: oDecimal
    ) -> oDecimal:
        return y_min + (x - x_min) * ((y_max - y_min) / (x_max - x_min))

    #
    # PUBLIC
    #

    def evaluate(self, xs: typing.List[oDecimal]) -> typing.List[oDecimal]:
        """
        This function evaluates this Function in the given arguments, returning a typing.List[Decimal] as output
        """
        # Type 0 functions use a sequence of sample values (contained in a stream) to provide an approximation for
        # functions whose domains and ranges are bounded. The samples are organized as an m-dimensional table in
        # which each entry has n components.
        if "FunctionType" in self and int(self["FunctionType"]) == 0:
            size: typing.List[oDecimal] = self["Size"]
            bps: int = int(self["BitsPerSample"])
            m: int = len(size)
            domain: typing.List[oDecimal] = self["Domain"]
            encode: typing.List[oDecimal] = []
            decode: typing.List[oDecimal] = []
            range2: typing.List[oDecimal] = self["Range"]
            if "Encode" in self:
                encode = self["Encode"]
            else:
                encode = [
                    oDecimal(0) if (i % 2 == 0) else size[int((i - 1) / 2)]
                    for i in range(0, 2 * m)
                ]
            if "Decode" in self:
                decode = self["Decode"]
            else:
                decode = range2

            # When a sampled function is called, each input value xi , for 0 £ i < m, shall be clipped to the domain:
            xs_prime = [
                min(max(xs[i], domain[2 * i]), domain[2 * i + 1]) for i in range(0, m)
            ]

            # That value shall be encoded:
            es = [
                Function._interpolate(
                    xs_prime[i],
                    domain[2 * i],
                    domain[2 * i + 1],
                    encode[2 * i],
                    encode[2 * i + 1],
                )
                for i in range(0, m)
            ]

            # That value shall be clipped to the size of the sample table in that dimension:
            es_prime = [
                min(max(es[i], oDecimal(0)), size[i] - 1) for i in range(0, len(es))
            ]

            # The encoded input values shall be real numbers, not restricted to integers. Interpolation shall be used to
            # determine output values from the nearest surrounding values in the sample table.
            sample_number: typing.Optional[int] = self._get_sample_number(es_prime)
            assert sample_number is not None
            rs = self._get_sample(sample_number)

            # Each output value rj, for 0 £ j < n, shall then be decoded:
            rs_prime: typing.List[oDecimal] = [
                Function._interpolate(
                    rs[j], oDecimal(0), 2 ** bps - 1, decode[2 * j], decode[2 * j + 1]
                )
                for j in range(0, len(rs))
            ]

            # Finally, each decoded value shall be clipped to the range:
            ys = [
                min(max(rs_prime[j], range2[2 * j]), range2[2 * j + 1])
                for j in range(0, len(rs_prime))
            ]

            # return
            return ys

        # Type 2 functions (PDF 1.3) include a set of parameters that define an exponential interpolation of one input
        # value and n output values:
        if "FunctionType" in self and int(self["FunctionType"]) == 2:
            assert len(xs) == 1
            if xs[0] == oDecimal(0):
                return self["C0"]
            if xs[0] == Decimal(1):
                return self["C1"]
            n: int = len(self["C0"])
            N: oDecimal = self["N"]
            c0: typing.List[oDecimal] = self["C0"]
            c1: typing.List[oDecimal] = self["C1"]
            return [(c0[j] + xs[0] ** N * (c1[j] - c0[j])) for j in range(0, n)]

        if "FunctionType" in self and int(self["FunctionType"]) == 3:
            # TODO : implement stitching function
            pass

        if "FunctionType" in self and int(self["FunctionType"]) == 4:
            return PostScriptEval.evaluate(self["DecodedBytes"].decode("latin1"), xs)

        # this should be impossible
        assert False


class List(PDFObject, list):
    """
    An array object is a one-dimensional collection of objects arranged sequentially. Unlike arrays in many other
    computer languages, PDF arrays may be heterogeneous; that is, an array’s elements may be any combination
    of numbers, strings, dictionaries, or any other objects, including other arrays. An array may have zero
    elements.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(List, self).__init__()

    #
    # PRIVATE
    #

    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode

    #
    # PUBLIC
    #


class Name(PDFObject):
    """
    Beginning with PDF 1.2 a name object is an atomic symbol uniquely defined by a sequence of any characters
    (8-bit values) except null (character code 0). Uniquely defined means that any two name objects made up of
    the same sequence of characters denote the same object. Atomic means that a name has no internal structure;
    although it is defined by a sequence of characters, those characters are not considered elements of the name.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, text: str):
        super().__init__()
        self._text = text

    #
    # PRIVATE
    #

    def __eq__(self, other):
        if isinstance(other, Name):
            return other._text == self._text
        if isinstance(other, str):
            return other == self._text
        return False

    def __ge__(self, other):
        if isinstance(other, Name):
            return self._text >= other._text
        if isinstance(other, str):
            return self._text >= other
        assert False

    def __gt__(self, other):
        if isinstance(other, Name):
            return self._text > other._text
        if isinstance(other, str):
            return self._text > other
        assert False

    def __hash__(self):
        return self._text.__hash__()

    def __le__(self, other):
        if isinstance(other, Name):
            return self._text <= other._text
        if isinstance(other, str):
            return self._text <= other
        assert False

    def __lt__(self, other):
        if isinstance(other, Name):
            return self._text < other._text
        if isinstance(other, str):
            return self._text < other
        assert False

    def __str__(self):
        return self._text

    #
    # PUBLIC
    #


class Reference(PDFObject):
    """
    Any object in a PDF file may be labelled as an indirect object. This gives the object a unique object identifier by
    which other objects can refer to it (for example, as an element of an array or as the value of a dictionary entry).

    The object identifier shall consist of two parts:

    •   A positive integer object number. Indirect objects may be numbered sequentially within a PDF file, but this
        is not required; object numbers may be assigned in any arbitrary order.

    •   A non-negative integer generation number. In a newly created file, all indirect objects shall have generation
        numbers of 0. Nonzero generation numbers may be introduced when the file is later updated; see sub-
        clauses 7.5.4, "Cross-Reference Table" and 7.5.6, "Incremental Updates."

    Together, the combination of an object number and a generation number shall uniquely identify an indirect
    object.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        object_number: typing.Optional[int] = None,
        generation_number: typing.Optional[int] = None,
        parent_stream_object_number: typing.Optional[int] = None,
        index_in_parent_stream: typing.Optional[int] = None,
        byte_offset: typing.Optional[int] = None,
        is_in_use: bool = True,
        document: typing.Optional["Document"] = None,  # type: ignore[name-defined]
    ):
        self.object_number = object_number
        self.generation_number = generation_number
        self.parent_stream_object_number = parent_stream_object_number
        self.index_in_parent_stream = index_in_parent_stream
        self.byte_offset = byte_offset
        self.is_in_use = is_in_use
        self.document = document

    #
    # PRIVATE
    #

    def __eq__(self, other):
        if not isinstance(other, Reference):
            return False
        return (
            self.object_number == other.object_number
            and self.generation_number == other.generation_number
            and self.parent_stream_object_number == other.parent_stream_object_number
            and self.index_in_parent_stream == other.index_in_parent_stream
            and self.byte_offset == other.byte_offset
        )

    def __hash__(self):
        hashcode: int = 1
        hashcode = hashcode * 31 + (
            self.object_number if self.object_number is not None else 0
        )
        hashcode = hashcode * 31 + (
            self.generation_number if self.generation_number is not None else 0
        )
        hashcode = hashcode * 31 + (
            self.parent_stream_object_number
            if self.parent_stream_object_number is not None
            else 0
        )
        hashcode = hashcode * 31 + (
            self.index_in_parent_stream
            if self.index_in_parent_stream is not None
            else 0
        )
        hashcode = hashcode * 31 + (
            self.byte_offset if self.byte_offset is not None else 0
        )
        return hashcode

    #
    # PUBLIC
    #


class Stream(Dictionary):
    """
    A stream object, like a string object, is a sequence of bytes. Furthermore, a stream may be of unlimited length,
    whereas a string shall be subject to an implementation limit. For this reason, objects with potentially large
    amounts of data, such as images and page descriptions, shall be represented as streams.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(Stream, self).__init__()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #


class String(PDFObject):
    """
    A literal string shall be written as an arbitrary number of characters enclosed in parentheses. Any characters
    may appear in a string except unbalanced parentheses (LEFT PARENHESIS (28h) and RIGHT
    PARENTHESIS (29h)) and the backslash (REVERSE SOLIDUS (5Ch)), which shall be treated specially as
    described in this sub-clause. Balanced pairs of parentheses within a string require no special treatment.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, bts: typing.Union[bytes, str]):  # type: ignore[name-defined]
        super().__init__()
        if isinstance(bts, str):
            self._text: str = bts
        if isinstance(bts, bytes):
            self._text = [(b & 0xFF) for b in bts]

    #
    # PRIVATE
    #

    def __eq__(self, other):
        if isinstance(other, String):
            return other._text == self._text
        if isinstance(other, str):
            return other == self._text
        return False

    def __getitem__(self, item):
        return self._text[item]

    def __hash__(self):
        return self._text.__hash__()

    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text

    #
    # PUBLIC
    #

    def get_content_bytes(self) -> bytearray:
        """
        This function returns the bytes that represent the *interpreted* content (as it was present in the PDF)
        of this String. For hexadecimal Strings, this content includes resolving the hexadecimal codes to their
        byte counterparts.
        """
        txt = ""
        i = 0
        while i < len(self):
            if self[i] == "\\":
                c = self[i + 1]
                if c == "n":
                    txt += "\n"
                elif c == "\\":
                    txt += "\\"
                elif c == "r":
                    txt += "\r"
                elif c == "t":
                    txt += "\t"
                elif c == "b":
                    txt += "\b"
                elif c == "f":
                    txt += "\f"

                elif c == "(" or c == ")" or c == "\\":
                    txt += c
                    i += 2
                    continue

                elif c == "\r":
                    if i + 2 < len(self) and self[i + 2] == "\n":
                        i += 3
                    else:
                        i += 2
                    continue

                elif c == "\n":
                    i += 2
                    continue

                else:
                    # We have read <SLASH>
                    # Is the next character <OCTAL> ?
                    # YES:  continue reading as <OCTAL> (max 2 more chars)
                    # NO:   do not process next char
                    if c < "0" or c > "7":
                        txt += c
                        i += 2  # processed <SLASH> <any> (pretend it's a useless escape sequence)
                        continue

                    # we have read <SLASH> <OCTAL>
                    # Is the next character <OCTAL> ?
                    # YES:  continue reading <OCTAL> (max 1 more char)
                    # NO:   do not process next char
                    octal = ord(c) - ord("0")
                    c = self[i + 2]

                    if c < "0" or c > "7":
                        txt += chr(octal)
                        i += 2  # processed <SLASH> <OCTAL>
                        continue

                    # we have read <SLASH> <OCTAL> <OCTAL>
                    octal = (octal << 3) + ord(c) - ord("0")
                    c = self[i + 3]
                    if c < "0" or c > "7":
                        txt += chr(octal)
                        i += 3  # processed <SLASH> <OCTAL> <OCTAL>
                        continue

                    # we have read <SLASH> <OCTAL> <OCTAL> <OCTAL>
                    octal = (octal << 3) + ord(c) - ord("0")
                    txt += chr(octal)
                    i += 4
                    continue

                i += 2
                continue
            txt += self[i]
            i += 1
        return bytearray(txt, encoding="latin1")

    def get_value_bytes(self):
        """
        This function returns the bytes that represent the content (as it was present in the PDF)
        of this String
        """
        return [b for b in self.get_content_bytes()]


class HexadecimalString(String):
    """
    Strings may also be written in hexadecimal form, which is useful for including arbitrary binary data in a PDF file.
    A hexadecimal string shall be written as a sequence of hexadecimal digits (0–9 and either A–F or a–f) encoded
    as ASCII characters and enclosed within angle brackets (using LESS-THAN SIGN (3Ch) and GREATER-
    THAN SIGN (3Eh)).
    """

    def __init__(self, text: str, encoding: typing.Optional["Encoding"] = None):  # type: ignore[name-defined]
        if len(text) % 2 == 1:
            text += "0"
        self.encoding = encoding
        super(HexadecimalString, self).__init__(text)

    def get_content_bytes(self) -> bytearray:
        """
        This function returns the bytes that represent the *interpreted* content (as it was present in the PDF)
        of this String. For hexadecimal Strings, this content includes resolving the hexadecimal codes to their
        byte counterparts.
        """
        arr = bytearray()
        for i in range(0, len(self), 2):
            arr.append(int(self[i : i + 2], 16))
        return arr


AnyPDFType = typing.Union[
    Boolean,
    CanvasOperatorName,
    Decimal,
    Dictionary,
    Element,
    HexadecimalString,
    Name,
    List,
    Reference,
    String,
]
