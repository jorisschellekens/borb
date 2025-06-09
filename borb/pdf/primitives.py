#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF Document Structure Module.

This module defines classes and types for managing fundamental components of
PDF documents. It includes representations for name objects and stream objects,
which are essential for handling data and metadata within the PDF structure.
"""
import datetime
import typing


class datestr(str):
    """A string subclass for parsing PDF-style date strings into datetime objects."""

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def to_datetime(self) -> typing.Optional[datetime.datetime]:
        """
        Parse the date string into a timezone-aware datetime object.

        :return: A `datetime.datetime` object if parsing is successful, otherwise `None`.
        """
        # Remove the leading 'D:' if present
        import copy

        s = str(copy.deepcopy(self))
        if s.startswith("D:"):
            s = s[2:]

        # Regular expression to extract parts
        import re

        match = re.match(
            r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})([+\-Z])?(\d{2})?'?(\d{2})?'?",
            s,
        )
        if not match:
            return None

        # extract parts
        year, month, day, hour, minute, second, tz_sign, tz_hour, tz_minute = (
            match.groups()
        )

        # Build naive datetime
        dt: datetime.datetime = datetime.datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second),
        )

        # Timezone handling
        if tz_sign:
            tz_hour = tz_hour or "00"
            tz_minute = tz_minute or "00"
            offset = datetime.timedelta(hours=int(tz_hour), minutes=int(tz_minute))
            if tz_sign == "-":
                offset = -offset
                dt = dt.replace(tzinfo=datetime.timezone(offset))
            else:
                dt = dt.replace(tzinfo=datetime.timezone.utc)

        # return
        return dt


class name(str):
    """
    Represents a name object in a PDF document.

    The `Name` class is used to define and manage name objects within the PDF
    structure. Name objects are typically used to represent identifiers or labels
    that are unique within the context of a PDF document, such as resource names,
    keys in dictionaries, or annotations.
    """

    pass


class reference:
    """
    Represents a reference to an object in a PDF document.

    The `Reference` class models a PDF object reference, which includes:
    an object number, a generation number, and an optional byte offset within the
    PDF file. This information uniquely identifies an object in the PDF and is
    used to locate and retrieve it as needed.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        object_nr: int,
        generation_nr: int,
        byte_offset: typing.Optional[int] = None,
        id: typing.Optional[int] = None,
        index_in_parent_stream: typing.Optional[int] = None,
        is_in_use: bool = True,
        parent_stream_object_nr: typing.Optional[int] = None,
        referenced_object: typing.Optional["PDFType"] = None,
    ):
        """
        Initialize a `Reference` instance with object number, generation number, and an optional byte offset.

        This constructor creates a reference to a PDF object, defined by an object number and a generation number.
        An optional byte offset can also be provided, which specifies the location of the object in the PDF byte
        stream for efficient access.

        :param object_nr:       The unique object number of the PDF reference. Must be a non-negative integer.
        :param generation_nr:   The generation number of the object in the PDF, allowing version tracking.
                                Must be a non-negative integer.
        :param byte_offset:     The byte offset of the object in the PDF stream, if known. Must be non-negative or `None`.
        :param id:              The id of the object being referenced, if known.
        """
        assert object_nr >= 0
        assert generation_nr >= 0
        assert byte_offset is None or byte_offset >= 0
        self.__object_nr: int = object_nr
        self.__generation_nr: int = generation_nr
        self.__byte_offset: typing.Optional[int] = byte_offset
        self.__id: typing.Optional[int] = id
        self.__referenced_object: typing.Optional["PDFType"] = referenced_object
        self.__is_in_use: bool = is_in_use
        self.__index_in_parent_stream: typing.Optional[int] = index_in_parent_stream
        self.__parent_stream_object_nr: typing.Optional[int] = parent_stream_object_nr

    #
    # PRIVATE
    #

    def __repr__(self):
        """Return repr(self)."""
        if self.__byte_offset is not None:
            return f"{self.__object_nr} {self.__generation_nr} R @ {self.__byte_offset}"
        return f"{self.__object_nr} {self.__generation_nr} R"

    #
    # PUBLIC
    #

    def get_byte_offset(self) -> typing.Optional[int]:
        """
        Retrieve the byte offset of the referenced PDF object, if available.

        This method returns the byte offset of the object in the PDF stream, which
        represents the location of the object for direct access during PDF parsing.

        :return: The byte offset of the object as an integer, or `None` if no offset is set.
        """
        return self.__byte_offset

    def get_generation_nr(self) -> int:
        """
        Retrieve the generation number of the referenced PDF object.

        This method returns the generation number, which is part of the unique identifier
        for a PDF object. The combination of object number and generation number uniquely
        identifies an object in a PDF file, with generation numbers often used to track
        updates to objects within the file.

        :return: The generation number of the PDF object as an integer.
        """
        return self.__generation_nr

    def get_id(self) -> typing.Optional[int]:
        """
        Retrieve the unique identifier (ID) of the referenced PDF object, if available.

        This ID corresponds to the result of calling `id()` on the object being
        referenced, which provides a unique identifier for the object's memory location.
        This can be useful for tracking specific instances of PDF objects, especially
        when working with large or complex documents that contain numerous references.

        :return: An integer representing the unique ID of the referenced object if
                 available, or `None` if no ID is set.
        """
        return self.__id

    def get_index_in_parent_stream(self) -> typing.Optional[int]:
        """
        Retrieve the index of this object within its parent object stream, if applicable.

        In PDF files, objects may be embedded within an object stream for efficiency. This method
        returns the index of the object within such a stream, or `None` if the object is not part
        of an object stream.

        :return: The index of the object in its parent object stream, or `None` if not applicable.
        """
        return self.__index_in_parent_stream

    def get_object_nr(self) -> int:
        """
        Retrieve the object number of the referenced PDF object.

        This method returns the object number, which, together with the generation
        number, uniquely identifies an object within a PDF file. The object number
        is a critical part of referencing and locating objects in the PDF structure.

        :return: The object number of the PDF object as an integer.
        """
        return self.__object_nr

    def get_parent_stream_object_nr(self) -> typing.Optional[int]:
        """
        Retrieve the object number of the parent stream containing this object, if applicable.

        In PDF files, some objects are stored within object streams for efficiency. This method
        returns the object number of the stream that contains this object, or `None` if the
        object is not part of an object stream.

        :return: The object number of the parent stream, or `None` if not applicable.
        """
        return self.__parent_stream_object_nr

    def get_referenced_object(self) -> typing.Optional["PDFType"]:
        """
        Retrieve the PDF object being referenced directly, if available.

        This method returns the actual referenced PDF object, which can be useful
        during serialization or when working with the object graph of a PDF document.
        If set, this allows direct access to the referenced object rather than just
        its identifier or positional information in the document.

        :return: The referenced PDF object as an instance of `PDFType`, or `None`
                 if no direct reference is set.
        """
        return self.__referenced_object

    def is_in_use(self) -> bool:
        """
        Determine whether the referenced PDF object is currently marked as 'in use'.

        In a PDF document, objects can be marked as 'in use' or 'free' in the cross-reference table.
        This method returns a boolean indicating whether this object is currently active (i.e., not
        deleted or free). This information is critical during serialization, garbage collection,
        and cross-reference table generation.

        :return: `True` if the object is in use; `False` if it is free.
        """
        return self.__is_in_use


class hexstr(str):
    """
    Represents a string containing only hexadecimal characters in a PDF.

    The `hexstr` class is a specialized string type used in PDF processing to represent
    strings that consist exclusively of hexadecimal characters (`0-9` and `A-F/a-f`). These
    strings are typically used to encode binary data in a compact textual format, adhering
    to the conventions of the PDF specification.

    This class behaves like a standard Python string but imposes constraints to ensure the
    content is valid hexadecimal data.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, value):
        """
        Initialize a hexstr instance with the given value.

        Ensures that the provided value is a valid hexadecimal string containing only
        characters `0-9`, `A-F`, and `a-f`. If the value does not meet this requirement,
        an assertion error is raised.

        :param value: The string value to be stored as a hexstr.
        """
        assert all([c in "0123456789abcdefABCDEF" for c in value])
        super().__init__()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def to_bytes(self) -> bytes:
        """
        Convert the hexadecimal string to a `bytes` object.

        This method interprets the `hexstr` instance as a sequence of hexadecimal-encoded
        byte values and converts it into a `bytes` object. Each pair of hexadecimal characters
        in the string is decoded into its corresponding byte.

        :return: A `bytes` object representing the binary data encoded in the hexadecimal string.
        """
        return bytes([int(self[i : i + 2], 16) for i in range(0, len(self), 2)])


class stream(dict):
    """
    Represents a stream object in a PDF document.

    The `Stream` class is used to encapsulate a sequence of bytes, which can represent
    various types of data within a PDF, such as images, font data, or content streams
    for pages. Streams are a fundamental part of the PDF structure, allowing for efficient
    storage and retrieval of large amounts of data.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, d: typing.Optional[dict] = None):
        """
        Initialize a new PDF stream object.

        The `Stream` class represents a stream object in a PDF file,
        which is used to store large sequences of binary data such as images, font data, or page content.
        """
        super().__init__()
        self[name("Bytes")] = b""
        self[name("Length")] = 0
        self[name("Filter")] = name("FlateDecode")
        if d is not None:
            for k, v in d.items():
                self[k] = v

    #
    # PRIVATE
    #

    def __getitem__(self, item):
        """Return self[key]."""
        # IF the requested item is not /Bytes or /DecodedBytes
        if item not in [name("Bytes"), name("DecodedBytes")]:
            return super().__getitem__(item)

        # IF the stream is compressed using anything other that FlateDecode
        # THEN don't perform auto-sync between /Bytes and /DecodedBytes
        filter: typing.Optional[name] = self.get("Filter", None)  # type: ignore[annotation-unchecked]
        if filter not in [name("FL"), name("FlateDecode")]:
            return super().__getitem__(item)

        # IF the item being requested is /Bytes
        # THEN update (by using /DecodedBytes) if needed
        if item == "Bytes":
            if self.__bytes_is_up_to_date:
                return super().__getitem__(item)
            else:
                import zlib

                self["Bytes"] = zlib.compress(self["DecodedBytes"], 9)
                self.__bytes_is_up_to_date = True
                self.__decoded_bytes_is_up_to_date = True
                return super().__getitem__(item)

        # IF the item being requested is /DecodedBytes
        # THEN update (by using /Bytes) if needed
        if item == "DecodedBytes":
            if self.__decoded_bytes_is_up_to_date:
                return super().__getitem__(item)
            else:
                import zlib

                self["DecodedBytes"] = (
                    b"" if len(self["Bytes"]) == 0 else zlib.decompress(self["Bytes"])
                )
                self.__bytes_is_up_to_date = True
                self.__decoded_bytes_is_up_to_date = True
                return super().__getitem__(item)

        # default
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        """Set self[key] to value."""
        if key == "Bytes":
            self.__bytes_is_up_to_date = True
            self.__decoded_bytes_is_up_to_date = False
            return super().__setitem__(key, value)
        elif key == "DecodedBytes":
            self.__bytes_is_up_to_date = False
            self.__decoded_bytes_is_up_to_date = True
            return super().__setitem__(key, value)
        else:
            return super().__setitem__(key, value)

    #
    # PUBLIC
    #


PDFType: typing.TypeAlias = typing.Union[
    bool,
    float,
    int,
    name,
    reference,
    str,
    stream,
    typing.Dict[typing.Union[name, str], "PDFType"],
    typing.List["PDFType"],
]
