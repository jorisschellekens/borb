#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Document objects
"""
import logging
import random
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Dictionary
from borb.io.read.types import HexadecimalString
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState
from borb.pdf.document.document import Document

logger = logging.getLogger(__name__)


class DocumentTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Document objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _build_empty_document_info_dictionary(
        self, object_to_transform: Dictionary
    ) -> None:
        # create Info dictionary if needed
        trailer: typing.Any = object_to_transform["XRef"]["Trailer"]
        assert isinstance(trailer, Dictionary)
        if "Info" not in trailer:
            trailer[Name("Info")] = Dictionary()
        trailer["Info"].set_parent(trailer)

    @staticmethod
    def _invalidate_all_references(object: AnyPDFType) -> None:
        objects_done: typing.List[AnyPDFType] = []
        objects_todo: typing.List[AnyPDFType] = [object]
        while len(objects_todo) > 0:
            obj = objects_todo.pop(0)
            if obj in objects_done:
                continue
            objects_done.append(obj)
            try:
                obj.set_reference(None)
            except Exception as ex:
                logger.debug(str(ex))
                pass
            if isinstance(obj, List):
                # fmt: off
                assert isinstance(obj, List), "unexpected error while performing _invalidate_all_references"
                # fmt: on
                for v in obj:
                    objects_todo.append(v)
                continue
            if isinstance(obj, Dictionary):
                # fmt: off
                assert isinstance(obj, Dictionary), "unexpected error while performing _invalidate_all_references"
                # fmt: on
                for k, v in obj.items():
                    objects_todo.append(k)
                    objects_todo.append(v)
                continue

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is a Document
        :param object:  the object to be transformed
        :return:        True if the object is a Document, False otherwise
        """
        return isinstance(object, Document)

    def transform(
        self,
        object_to_transform: typing.Any,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a Document into a byte stream
        :param object_to_transform:     the /Catalog Dictionary to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Document
        """

        # write header
        # fmt: off
        assert context is not None, "A WriteTransformerState must be defined in order to write Document objects."
        assert context.destination is not None, "A WriteTransformerState must be defined in order to write Document objects."
        # fmt: on

        context.destination.write(b"%PDF-1.7\n")
        context.destination.write(b"%")
        context.destination.write(bytes([226, 227, 207, 211]))
        context.destination.write(b"\n")

        # invalidate all references
        DocumentTransformer._invalidate_all_references(object_to_transform)

        # set /ID
        random_id = HexadecimalString("%032x" % random.randrange(16 ** 32))
        if "ID" not in object_to_transform["XRef"]["Trailer"]:
            # fmt: off
            object_to_transform["XRef"]["Trailer"][Name("ID")] = List()
            object_to_transform["XRef"]["Trailer"][Name("ID")].set_is_inline(True)
            object_to_transform["XRef"]["Trailer"]["ID"].append(random_id)
            object_to_transform["XRef"]["Trailer"]["ID"].append(random_id)
            # fmt: on
        else:
            object_to_transform["XRef"]["Trailer"]["ID"][1] = random_id
            object_to_transform["XRef"]["Trailer"]["ID"].set_is_inline(True)

        # /Info
        self._build_empty_document_info_dictionary(object_to_transform)

        # transform XREF
        self.get_root_transformer().transform(object_to_transform["XRef"], context)
