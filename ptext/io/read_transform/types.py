from decimal import Decimal
from typing import Union, Optional


def add_base_methods(cls):
    """
    This decorator adds a variety of methods to an object to ensure
    it can be used by a BaseTransformer. These methods include:
    setting/getting a parent, getting the root in hierarchy,
    adding an EventListener,
    and notifying an object that an event has occurred.
    """

    def get_parent(self):
        """
        Get the parent object of this object
        """
        return getattr(self, "_parent")

    def set_parent(self, parent):
        """
        Set the parent object of this object
        """
        setattr(self, "_parent", parent)
        return self

    def get_root(self):
        """
        Get the root object of this object
        """
        tmp = self
        while (
            tmp is not None
            and hasattr(tmp, "_parent")
            and getattr(tmp, "_parent") is not None
        ):
            tmp = getattr(tmp, "_parent")
        return tmp

    def set_reference(self, reference: "Reference"):
        setattr(self, "_reference", reference)
        return self

    def get_reference(self):
        if not hasattr(self, "_reference"):
            setattr(self, "_reference", None)
        return getattr(self, "_reference")

    def can_be_referenced(self):
        if not hasattr(self, "_can_be_referenced"):
            setattr(self, "_can_be_referenced", True)
        return getattr(self, "_can_be_referenced")

    def set_can_be_referenced(self, a_flag: bool):
        setattr(self, "_can_be_referenced", a_flag)
        return self

    def add_event_listener(self, event_listener):
        """
        Add an EventListener to this object
        """
        if not hasattr(self, "_event_listeners"):
            setattr(self, "_event_listeners", [])
        getattr(self, "_event_listeners").append(event_listener)
        return self

    def event_occurred(self, event):
        """
        Notify the EventListeners registered
        to this object that an Event has occurred
        """
        if not hasattr(self, "_event_listeners"):
            setattr(self, "_event_listeners", [])
        for l in getattr(self, "_event_listeners"):
            l.event_occurred(event)
        return self

    def to_json_serializable(self, to_convert=None):
        """
        Convert this object to a representation that
        can be serialized as JSON
        """
        if isinstance(to_convert, dict):
            return {
                self.to_json_serializable(k): self.to_json_serializable(v)
                for k, v in to_convert.items()
            }
        if isinstance(to_convert, list):
            return [self.to_json_serializable(x) for x in to_convert]
        if isinstance(to_convert, Decimal):
            return float(to_convert)
        if (
            isinstance(to_convert, HexadecimalString)
            or isinstance(to_convert, String)
            or isinstance(to_convert, Name)
            or isinstance(to_convert, CanvasOperatorName)
        ):
            return to_convert
        return None

    # linkage methods
    setattr(cls, "get_parent", get_parent)
    setattr(cls, "set_parent", set_parent)
    setattr(cls, "get_root", get_root)
    # event listener methods
    setattr(cls, "add_event_listener", add_event_listener)
    setattr(cls, "event_occurred", event_occurred)
    # pdf methods
    setattr(cls, "set_reference", set_reference)
    setattr(cls, "get_reference", get_reference)
    setattr(cls, "can_be_referenced", can_be_referenced)
    setattr(cls, "set_can_be_referenced", set_can_be_referenced)
    # serialization methods
    setattr(cls, "to_json_serializable", to_json_serializable)
    # initialize fields
    setattr(cls, "_parent", None)
    setattr(cls, "_event_listeners", [])
    setattr(cls, "_can_be_referenced", True)
    return cls


@add_base_methods
class Decimal(Decimal):  # type: ignore [no-redef]
    pass


@add_base_methods
class String(str):
    def __new__(cls, value: str, encoding: Optional["Encoding"] = None):  # type: ignore [name-defined]
        s = str.__new__(cls, value)  # type: ignore [call-arg]
        s.encoding = encoding
        return s

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


@add_base_methods
class Name(str):
    def __new__(cls, value):
        return str.__new__(cls, value)


class CanvasOperatorName(str):
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

    def __new__(cls, value):
        return str.__new__(cls, value)  # type: ignore [call-arg]


@add_base_methods
class HexadecimalString(String):
    def __new__(cls, value: str, encoding: Optional["Encoding"] = None):  # type: ignore [name-defined]
        if len(value) % 2 == 1:
            s = str.__new__(cls, value + "0")  # type: ignore [call-arg]
        else:
            s = str.__new__(cls, value)  # type: ignore [call-arg]
        s.encoding = encoding
        return s

    def get_content_bytes(self) -> bytearray:
        arr = bytearray()
        for i in range(0, len(self), 2):
            arr.append(int(self[i : i + 2], 16))
        return arr


@add_base_methods
class List(list):
    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode


@add_base_methods
class Dictionary(dict):
    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode


@add_base_methods
class Stream(Dictionary):
    pass


@add_base_methods
class Boolean:
    def __init__(self, value: bool):
        self.value = value

    def __bool__(self):
        return self.value

    def __str__(self):
        if self.value:
            return "True"
        else:
            return "False"


@add_base_methods
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
    HexadecimalString,
    Name,
    List,
    Reference,
    String,
]
