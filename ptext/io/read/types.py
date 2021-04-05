# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module defines all the base types used in processing PDFs
    e.g. Boolean, CanvasOperatorName, Decimal, Dictionary, Element, Name, Stream, String, ..
"""
import copy
import types
import typing
import xml.etree.ElementTree as ET
from decimal import Decimal as oDecimal
from typing import Union, Optional

from PIL.Image import Image  # type: ignore [import]

from ptext.pdf.canvas.event.event_listener import EventListener


def add_base_methods(object: typing.Any) -> typing.Any:
    def _to_json_serializable(to_convert=None):
        """
        Convert this object to a representation that
        can be serialized as JSON
        """
        if isinstance(to_convert, dict):
            return {
                to_json_serializable(k): to_json_serializable(v)
                for k, v in to_convert.items()
            }
        if isinstance(to_convert, list):
            return [to_json_serializable(x) for x in to_convert]
        if isinstance(to_convert, Decimal):
            return float(to_convert)
        if (
            isinstance(to_convert, HexadecimalString)
            or isinstance(to_convert, String)
            or isinstance(to_convert, Name)
            or isinstance(to_convert, CanvasOperatorName)
        ):
            return str(to_convert)
        return None

    def to_json_serializable(self):
        return _to_json_serializable(self)

    def image_hash_method(self):
        w = self.width
        h = self.height
        pixels = [
            self.getpixel((0, 0)),
            self.getpixel((0, h - 1)),
            self.getpixel((w - 1, 0)),
            self.getpixel((w - 1, h - 1)),
        ]
        hashcode = 1
        for p in pixels:
            if isinstance(p, typing.List) or isinstance(p, typing.Tuple):
                hashcode += 32 * hashcode + sum(p)
            else:
                hashcode += 32 * hashcode + p
        return hashcode

    def deepcopy_mod(self, memodict={}):
        print("copying %s" % self.__class__.__name__)
        prev_function_ptr = self.__deepcopy__
        self.__deepcopy__ = None
        # copy
        out = copy.deepcopy(self, memodict)
        # restore
        self.__deepcopy__ = prev_function_ptr
        # add base methods
        add_base_methods(out)
        # return
        return out

    # get_parent
    def get_parent(self):
        if "_parent" not in vars(self):
            setattr(self, "_parent", None)
        return self._parent

    # set_parent
    def set_parent(self, parent):
        if "_parent" not in vars(self):
            setattr(self, "_parent", None)
        self._parent = parent
        return self

    # get_root
    def get_root(self):
        e = self
        while e.get_parent() is not None:
            e = e.get_parent()
        return e

    # add_event_listener
    def add_event_listener(self, event_listener: "EventListener"):
        if "_event_listeners" not in vars(self):
            setattr(self, "_event_listeners", [])
        self._event_listeners.append(event_listener)
        return self

    # get_event_listener
    def get_event_listeners(self) -> typing.List["EventListener"]:
        if "_event_listeners" not in vars(self):
            setattr(self, "_event_listeners", [])
        return self._event_listeners

    # event_occurred
    def event_occurred(self, event: "Event"):  # type: ignore [name-defined]
        if "_event_listeners" not in vars(self):
            setattr(self, "_event_listeners", [])
        for l in self._event_listeners:
            l.event_occurred(event)
        if self.get_parent() is not None:
            self.get_parent().event_occurred(event)
        return self

    # set_reference
    def set_reference(self, reference: "Reference"):
        if "_reference" not in vars(self):
            setattr(self, "_reference", None)
        assert (
            self._reference is None
            or reference is None
            or self._reference.object_number == reference.object_number
            or (
                self._reference.parent_stream_object_number
                == reference.parent_stream_object_number
                and self._reference.index_in_parent_stream
                == reference.index_in_parent_stream
            )
        )
        self._reference = reference
        return self

    # get_reference
    def get_reference(self) -> typing.Optional["Reference"]:
        if "_reference" not in vars(self):
            setattr(self, "_reference", None)
        return self._reference

    # set_can_be_referenced
    def set_can_be_referenced(self, a_flag: bool):
        if "_can_be_referenced" not in vars(self):
            setattr(self, "_can_be_referenced", None)
        self._can_be_referenced = a_flag
        return self

    # can_be_referenced
    def can_be_referenced(self) -> bool:
        if "_can_be_referenced" not in vars(self):
            setattr(self, "_can_be_referenced", True)
        return self._can_be_referenced

    object.set_parent = types.MethodType(set_parent, object)
    object.get_parent = types.MethodType(get_parent, object)
    object.get_root = types.MethodType(get_root, object)
    object.add_event_listener = types.MethodType(add_event_listener, object)
    object.get_event_listeners = types.MethodType(get_event_listeners, object)
    object.event_occurred = types.MethodType(event_occurred, object)
    object.set_reference = types.MethodType(set_reference, object)
    object.get_reference = types.MethodType(get_reference, object)
    object.set_can_be_referenced = types.MethodType(set_can_be_referenced, object)
    object.can_be_referenced = types.MethodType(can_be_referenced, object)
    object.to_json_serializable = types.MethodType(to_json_serializable, object)
    if isinstance(object, Image):
        object.__deepcopy__ = types.MethodType(deepcopy_mod, object)
        object.__hash__ = types.MethodType(image_hash_method, object)


class Boolean:
    def __init__(self, value: bool):
        super(Boolean, self).__init__()
        self.value = value

    def __bool__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, bool):
            return other == self.value
        if isinstance(other, Boolean):
            return other.value == self.value
        return False

    def __str__(self):
        if self.value:
            return "True"
        else:
            return "False"


class CanvasOperatorName:
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
        "''",
        '"',
    ]
    # fmt: on

    def __init__(self, text: str):
        super(CanvasOperatorName, self).__init__()
        self.text = text
        add_base_methods(self)

    def __eq__(self, other):
        if isinstance(other, CanvasOperatorName):
            return other.text == self.text
        if isinstance(other, str):
            return other == self.text
        return False

    def __hash__(self):
        return self.text.__hash__()

    def __str__(self):
        return self.text


class Decimal(oDecimal):  # type: ignore [no-redef]
    """Floating point class for decimal arithmetic."""

    def __init__(self, obj: typing.Union[str, float, int, oDecimal]):
        super(Decimal, self).__init__()
        add_base_methods(self)


class Dictionary(dict):
    def __init__(self):
        super(Dictionary, self).__init__()
        add_base_methods(self)

    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode

    def __setitem__(self, key, value):
        assert isinstance(key, Name)
        super(Dictionary, self).__setitem__(key, value)

    def __deepcopy__(self, memodict={}):
        out = Dictionary()
        for k, v in self.items():
            out[copy.deepcopy(k, memodict)] = copy.deepcopy(v, memodict)
        return out


class Element(ET.Element):
    def __init__(self, tag, **extra):
        super(Element, self).__init__(tag, **extra)
        add_base_methods(self)


class Name:
    def __init__(self, text: str):
        self.text = text
        add_base_methods(self)

    def __eq__(self, other):
        if isinstance(other, Name):
            return other.text == self.text
        if isinstance(other, str):
            return other == self.text
        return False

    def __hash__(self):
        return self.text.__hash__()

    def __str__(self):
        return self.text


class Stream(Dictionary):
    def __init__(self):
        super(Stream, self).__init__()


class String:
    def __init__(self, text: str, encoding: Optional["Encoding"] = None):  # type: ignore [name-defined]
        self.text = text
        self.encoding = encoding
        add_base_methods(self)

    def __eq__(self, other):
        if isinstance(other, String):
            return other.text == self.text
        if isinstance(other, str):
            return other == self.text
        return False

    def __hash__(self):
        return self.text.__hash__()

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        return self.text[item]

    def get_content_bytes(self) -> bytearray:
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
        return bytearray(txt, encoding="latin-1")

    def get_value_bytes(self):
        if self.encoding is None:
            return [b for b in self.get_content_bytes()]
        # TODO
        return None


class HexadecimalString(String):
    def __init__(self, text: str, encoding: Optional["Encoding"] = None):  # type: ignore [name-defined]
        if len(text) % 2 == 1:
            text += "0"
        self.encoding = encoding
        super(HexadecimalString, self).__init__(text)

    def get_content_bytes(self) -> bytearray:
        arr = bytearray()
        for i in range(0, len(self), 2):
            arr.append(int(self[i : i + 2], 16))
        return arr


class List(list):
    def __init__(self):
        super(List, self).__init__()
        add_base_methods(self)

    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode


class Reference:
    object_number: Optional[int]
    generation_number: Optional[int]
    parent_stream_object_number: Optional[int]
    index_in_parent_stream: Optional[int]
    byte_offset: Optional[int]
    is_in_use: bool
    document: "Document"  # type: ignore [name-defined]

    def __init__(
        self,
        object_number: Optional[int] = None,
        generation_number: Optional[int] = None,
        parent_stream_object_number: Optional[int] = None,
        index_in_parent_stream: Optional[int] = None,
        byte_offset: Optional[int] = None,
        is_in_use: bool = True,
        document: Optional["Document"] = None,  # type: ignore [name-defined]
    ):
        self.object_number = object_number
        self.generation_number = generation_number
        self.parent_stream_object_number = parent_stream_object_number
        self.index_in_parent_stream = index_in_parent_stream
        self.byte_offset = byte_offset
        self.is_in_use = is_in_use
        self.document = document
        add_base_methods(self)

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


AnyPDFType = Union[
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
