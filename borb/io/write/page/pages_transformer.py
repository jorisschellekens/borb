#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible
for writing Dictionary objects of /Type /Pages
"""
import logging
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.write.object.dictionary_transformer import DictionaryTransformer
from borb.io.write.transformer import WriteTransformerState

logger = logging.getLogger(__name__)


class PagesTransformer(DictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of /Type /Pages
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is a /Pages Dictionary
        :param object:  the object to be transformed
        :return:        True if the object is a /Pages Dictionary, False otherwise
        """
        return (
            isinstance(object, Dictionary)
            and "Type" in object
            and object["Type"] == "Pages"
        )

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a /Pages Dictionary into a byte stream
        :param object_to_transform:     the /Pages Dictionary to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) /Pages Dictionary
        """
        # fmt: off
        assert isinstance(object_to_transform, Dictionary)
        assert context is not None, "A WriteTransformerState must be defined in order to write Pages Dictionary objects."
        # fmt: on

        # /Kids can be written immediately
        object_to_transform[Name("Kids")].set_is_inline(True)

        # queue writing of /Page objects
        queue: typing.List[AnyPDFType] = []
        for i, k in enumerate(object_to_transform["Kids"]):
            queue.append(k)
            object_to_transform["Kids"][i] = self.get_reference(k, context)

        # delegate to super
        super(PagesTransformer, self).transform(object_to_transform, context)

        # write /Page objects
        for p in queue:
            self.get_root_transformer().transform(p, context)

        # restore /Kids
        for i, k in enumerate(queue):
            object_to_transform["Kids"][i] = k
