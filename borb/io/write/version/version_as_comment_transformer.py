#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing ASCII art in every PDF
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Stream
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState
from borb.license.version import Version


class VersionAsCommentTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing the borb version in every PDF
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__()
        self._has_been_used: bool = False

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True once per Document (on the first Stream object) and embeds some ASCII art
        This is used to embed the current version in each Document
        :param object:  the object to be transformed
        :return:        True if the object is a Stream AND the version has not yet been serialized, False otherwise
        """
        return isinstance(object, Stream) and not self._has_been_used

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This method writes the (borb) version to the byte stream.
        It does so by hijacking the Stream serialization.
        :param object_to_transform:     the Stream Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Stream Object
        """
        # fmt: off
        assert (context is not None), "context must be defined to write ASCII art (borb meta-info)"
        assert (context.destination is not None), "context.destination must be defined to write ASCII art (borb meta-info)"
        assert isinstance(object_to_transform, Stream)
        # fmt: on

        # build
        version_as_comment_str: typing.List[str] = [
            Version.get_producer() + " " + Version.get_version(),
            Version.get_author(),
        ]

        # convert to latin1
        version_as_comment_bytes = [
            bytes("% " + x + "\n", "utf8") for x in version_as_comment_str
        ]

        self._has_been_used = True
        for x in version_as_comment_bytes:
            context.destination.write(x)
        context.destination.write(bytes("\n", "utf8"))

        self.get_root_transformer().transform(object_to_transform, context)
