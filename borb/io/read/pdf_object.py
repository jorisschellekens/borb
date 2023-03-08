#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This object represents the base class for everything related to IO in borb.
It has some convenience methods that allow you to specify how the object
should be persisted, as well as some methods to traverse the object-graph.
"""
import copy
import typing
from types import MethodType

import PIL


class PDFObject:
    """
    This object represents the base class for everything related to IO in borb.
    It has some convenience methods that allow you to specify how the object
    should be persisted, as well as some methods to traverse the object-graph.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._parent: typing.Optional["PDFObject"] = None
        self._is_inline: bool = False
        self._is_unique: bool = False
        self._reference: typing.Optional["Reference"] = None

    #
    # PRIVATE
    #

    @staticmethod
    def _to_json(self, memo_dict={}) -> typing.Any:

        # bool
        if isinstance(self, bool):
            return self

        # Boolean
        from borb.io.read.types import Boolean

        if isinstance(self, Boolean):
            return bool(self)

        # CanvasOperatorName
        from borb.io.read.types import CanvasOperatorName

        if isinstance(self, CanvasOperatorName):
            return str(self)

        # (borb) Decimal
        from borb.io.read.types import Decimal

        if isinstance(self, Decimal):
            return float(self)

        # (decimal) Decimal
        from decimal import Decimal as oDecimal

        if isinstance(self, oDecimal):
            return float(self)

        # float, int
        if isinstance(self, float) or isinstance(self, int):
            return self

        # bytes
        if isinstance(self, bytes):
            return str(self)

        # Dictionary
        from borb.io.read.types import Dictionary

        if isinstance(self, Dictionary):
            out: typing.Dict[str, typing.Any] = {}
            memo_dict[id(self)] = out
            for k, v in self.items():
                out[str(k)] = PDFObject._to_json(v, memo_dict)
            return out

        # dict
        if isinstance(self, dict):
            dict_out: typing.Dict[str, typing.Any] = {}
            memo_dict[id(self)] = dict_out
            for k, v in self.items():
                dict_out[str(k)] = PDFObject._to_json(v, memo_dict)
            return dict_out

        # Element
        from borb.io.read.types import Element

        if isinstance(self, Element):
            from borb.io.read.types import ET

            return str(ET.tostring(self))

        # Name
        from borb.io.read.types import Name

        if isinstance(self, Name):
            return str(self)

        # Stream
        # DUPLICATE: Dictionary

        # Function
        # DUPLICATE: Dictionary

        # String
        from borb.io.read.types import String

        if isinstance(self, String):
            return str(self)

        # HexadecimalString
        # DUPLICATE: String

        # List
        from borb.io.read.types import List

        if isinstance(self, List):
            list_out: typing.List[typing.Any] = []
            memo_dict[id(self)] = list_out
            for v in self:
                list_out += [PDFObject._to_json(v, memo_dict)]
            return list_out

        # Reference
        from borb.io.read.types import Reference

        if isinstance(self, Reference):
            return "%d %d R" % (self.generation_number or 0, self.object_number or 0)

        # PIL.Image.Image
        # TODO

        # default
        return None

    #
    # PUBLIC
    #

    @staticmethod
    def add_pdf_object_methods(non_borb_object: typing.Any) -> typing.Any:
        """
        This method allows you to pretend an object is actually a PDFObject.
        It adds all the methods that are present for a PDFObject.
        It also adds a utility hashing method for images (since PIL normally does not hash images)
        :param non_borb_object:
        :return:
        """

        def _deepcopy_and_add_methods(self, memodict={}):
            prev_function_ptr = self.__deepcopy__
            self.__deepcopy__ = None
            out = copy.deepcopy(self, memodict)
            self.__deepcopy__ = prev_function_ptr
            PDFObject.add_pdf_object_methods(out)
            return out

        def _get_parent(self) -> typing.Optional[PDFObject]:
            if "_parent" not in vars(self):
                setattr(self, "_parent", None)
            return self._parent

        def _get_reference(self) -> typing.Optional["Reference"]:  # type: ignore[name-defined]
            if "_reference" not in vars(self):
                setattr(self, "_reference", None)
            return self._reference

        def _get_root(self) -> PDFObject:
            p = self
            while p.get_parent() is not None:
                p = p.get_parent()
            return p

        def _is_inline(self) -> bool:
            if "_is_inline" not in vars(self):
                setattr(self, "_is_inline", False)
            return self._is_inline

        def _is_unique(self) -> bool:
            if "_is_unique" not in vars(self):
                setattr(self, "_is_unique", False)
            return self._is_unique

        def _pil_image_hash(self):
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

        def _set_is_inline(self, is_inline: bool) -> PDFObject:
            if "_is_inline" not in vars(self):
                setattr(self, "_is_inline", False)
            self._is_inline = is_inline
            return self

        def _set_is_unique(self, is_unique: bool) -> PDFObject:
            if "_is_unique" not in vars(self):
                setattr(self, "_is_unique", False)
            self._is_unique = is_unique
            return self

        def _set_parent(self, parent: PDFObject) -> PDFObject:
            if "_parent" not in vars(self):
                setattr(self, "_parent", None)
            self._parent = parent
            return self

        def _set_reference(self, reference: "Reference") -> PDFObject:  # type: ignore[name-defined]
            if "_reference" not in vars(self):
                setattr(self, "_reference", None)
            self._reference = reference
            return self

        # inject these methods in the object
        non_borb_object.set_parent = MethodType(_set_parent, non_borb_object)
        non_borb_object.get_parent = MethodType(_get_parent, non_borb_object)
        non_borb_object.get_root = MethodType(_get_root, non_borb_object)
        non_borb_object.set_reference = MethodType(_set_reference, non_borb_object)
        non_borb_object.get_reference = MethodType(_get_reference, non_borb_object)
        non_borb_object.set_is_inline = MethodType(_set_is_inline, non_borb_object)
        non_borb_object.is_inline = MethodType(_is_inline, non_borb_object)
        non_borb_object.set_is_unique = MethodType(_set_is_unique, non_borb_object)
        non_borb_object.is_unique = MethodType(_is_unique, non_borb_object)
        non_borb_object.__deepcopy__ = MethodType(
            _deepcopy_and_add_methods, non_borb_object
        )

        # add a __hash__ method for PIL.Image.Image
        if isinstance(non_borb_object, PIL.Image.Image):
            non_borb_object.__hash__ = MethodType(_pil_image_hash, non_borb_object)  # type: ignore [assignment]

        # return
        return non_borb_object

    def get_parent(self) -> typing.Optional["PDFObject"]:
        """
        This function returns the parent of this PDFObject, or None if no such PDFObject exists
        :return:    the parent of this PDFObject
        """
        return self._parent

    def get_reference(self) -> typing.Optional["Reference"]:  # type: ignore[name-defined]
        """
        This function gets the Reference being used for this PDFObject
        :return:    the Reference being used for this PDFObject
        """
        return self._reference

    def get_root(self) -> typing.Optional["PDFObject"]:
        """
        This function returns the root (of the parent hierarchy) of this PDFObject, or None if no such PDFObject exists
        :return:    the root of this PDFObject
        """
        p: typing.Optional["PDFObject"] = self
        while p is not None and p.get_parent() is not None:
            p = p.get_parent()
        return p

    def is_inline(self) -> bool:
        """
        This function returns True if this PDFObject should be persisted inline, False otherwise
        :return:    whether this PDFObject should be persisted online
        """
        return self._is_inline

    def is_unique(self) -> bool:
        """
        This function returns True if this PDFObject should always be treated
        as if it is unique (for IO purposes), regardless of hashing equality.
        :return:    whether this PDFObject is unique
        """
        return self._is_unique

    def set_is_inline(self, is_inline: bool) -> "PDFObject":
        """
        This function sets the is_inline flag of this PDFObject.
        An inline object is always persisted immediately when needed, it is never turned into a reference.
        :param is_inline:   whether this PDFObject should be persisted inline, or not
        :return:            self
        """
        self._is_inline = is_inline
        return self

    def set_is_unique(self, is_unique: bool) -> "PDFObject":
        """
        This function sets the is_unique flag of this PDFObject.
        A unique object is always persisted as itself,
        or its own reference even if it should be equal to another PDFObject.
        :param is_unique:   whether this PDFObject should be unique or not
        :return:            self
        """
        self._is_unique = is_unique
        return self

    def set_parent(self, parent: "PDFObject") -> "PDFObject":
        """
        This function sets the parent (PDFObject) of this PDFObject
        :param parent:  the parent (PDFObject)
        :return:        self
        """
        self._parent = parent
        return self

    def set_reference(self, reference: "Reference") -> "PDFObject":  # type: ignore[name-defined]
        """
        This function sets the Reference to be used for this PDFObject
        :param reference:   the Reference to be used for this PDFObject
        :return:            self
        """
        self._reference = reference
        return self

    def to_json(self) -> typing.Any:
        """
        This function converts this PDFObject into a set of nested dictionaries, lists and primitives
        :return:    a JSON-like object
        """
        return PDFObject._to_json(self)
