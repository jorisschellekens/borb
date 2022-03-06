#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading the XRef object
"""
import io
import os
import typing
from decimal import Decimal
from typing import Any, Optional, Union

from borb.io.read.encryption.standard_security_handler import StandardSecurityHandler
from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Dictionary, Name
from borb.pdf.canvas.event.event_listener import Event, EventListener
from borb.pdf.document.document import Document
from borb.pdf.xref.plaintext_xref import PlainTextXREF
from borb.pdf.xref.rebuilt_xref import RebuiltXREF
from borb.pdf.xref.stream_xref import StreamXREF
from borb.pdf.xref.xref import XREF


class BeginDocumentEvent(Event):
    """
    This implementation of Event is triggered right before the Document is processed
    """

    pass


class EndDocumentEvent(Event):
    """
    This implementation of Event is triggered right after the Document was processed
    """

    pass


class XREFTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading the XRef object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be converted represents a cross-reference table
        """
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a cross-reference table from a byte stream
        """

        # update context
        assert context is not None
        assert isinstance(object_to_transform, io.BufferedIOBase) or isinstance(
            object_to_transform, io.RawIOBase
        )
        context.root_object = Document()
        context.source = object_to_transform
        context.tokenizer = HighLevelTokenizer(context.source)

        # add listener(s)
        for l in event_listeners:
            l._event_occurred(BeginDocumentEvent())  # type: ignore [attr-defined]

        # remove prefix
        XREFTransformer._remove_prefix(context)

        # check header
        XREFTransformer._check_header(context)

        # file size
        context.source.seek(0, os.SEEK_END)
        file_length = context.source.tell()
        context.source.seek(0)
        context.root_object[Name("FileSize")] = Decimal(file_length)

        # build XREF object
        self._read_xref(context)

        # transform trailer dictionary
        xref = context.root_object.get("XRef")
        assert xref is not None
        assert isinstance(xref, XREF)

        # check for password protected PDF
        if "Trailer" in xref and "Encrypt" in xref["Trailer"]:

            # transform /Encrypt dictionary
            # fmt: off
            xref["Trailer"][Name("Encrypt")] = self.get_root_transformer().transform(xref["Trailer"]["Encrypt"], xref["Trailer"], context, event_listeners)
            # fmt: on

            # build encryption handler
            v: int = int(xref["Trailer"]["Encrypt"].get("V", Decimal(0)))
            r: int = int(xref["Trailer"]["Encrypt"]["R"])
            if r != 2 and r != 3:
                assert (
                    False
                ), "R is not 2 or 3. A number specifying which revision of the standard security handler shall be used to interpret this dictionary."
            if v == 0:
                assert False, (
                    "V is 0. An algorithm that is undocumented. "
                    "This value shall not be used."
                )
            if v == 1:
                context.security_handler = StandardSecurityHandler(
                    xref["Trailer"]["Encrypt"], context.password
                )
            if v == 2:
                context.security_handler = StandardSecurityHandler(
                    xref["Trailer"]["Encrypt"], context.password
                )
            if v == 3:
                assert False, (
                    "V is 3. (PDF 1.4) An unpublished algorithm that permits encryption key lengths ranging from 40 to 128 bits. "
                    "This value shall not appear in a conforming PDF file."
                )
            if v == 4:
                assert False, "V is 4. Currently unsupported encryption dictionary."

            # raise error
            raise NotImplementedError(
                "password-protected PDFs are currently not supported"
            )

        # transform /Trailer
        trailer = self.get_root_transformer().transform(
            context.root_object["XRef"]["Trailer"],
            context.root_object,
            context,
            event_listeners,
        )

        assert trailer is not None
        assert isinstance(trailer, Dictionary)
        xref[Name("Trailer")] = trailer
        for k in ["DecodeParms", "Filter", "Index", "Length", "Prev", "W"]:
            if k in xref["Trailer"]:
                xref["Trailer"].pop(k)

        # notify
        for l in event_listeners:
            l._event_occurred(EndDocumentEvent())  # type: ignore [attr-defined]

        # return
        return context.root_object

    @staticmethod
    def _remove_prefix(context: ReadTransformerState) -> None:

        assert context is not None
        assert context.source is not None
        assert context.tokenizer is not None

        # read first 2 Kb
        bytes_near_sof = context.source.read(2048)
        assert bytes_near_sof is not None
        text_near_sof = bytes_near_sof.decode("latin-1")
        context.source.seek(0)

        # find %PDF-
        index_of_pdf_comment = -1
        try:
            index_of_pdf_comment = text_near_sof.index("%PDF")
        except ValueError:
            pass

        # truncate
        if index_of_pdf_comment > 0:
            # determine end of file
            end_of_file = context.source.seek(0, os.SEEK_END)
            context.source.seek(0)
            # build byte array
            bts = context.source.read(end_of_file)
            assert bts is not None
            bts = bts[index_of_pdf_comment:end_of_file]
            # reset values in context
            context.source = io.BytesIO(bts)
            context.tokenizer._io_source = context.source

    @staticmethod
    def _check_header(context: ReadTransformerState) -> None:
        """
        This function checks whether or not the first bytes in the document contain the text %PDF
        :param context: the TransformerContext (containing the io source)
        :type context: TransformerContext
        """
        assert context is not None
        assert context.source is not None
        assert context.tokenizer is not None
        context.source.seek(0)
        arr = [
            t
            for t in [context.tokenizer.next_token() for _ in range(0, 10)]
            if t is not None
        ]
        assert len(arr) > 0
        assert any([t.get_text().startswith("%PDF") for t in arr])

    def _read_xref(
        self, context: ReadTransformerState, initial_offset: Optional[int] = None
    ) -> None:
        """
        This function attempts to read the XREF table, first as plaintext, then as a stream
        :param context:         the TransformerContext (containing the io source)
        :type context:          TransformerContext
        :param initial_offset:  the initial byte offset at which to read (set to None to allow this method to find the XREF)
        :type initial_offset:   int
        """
        assert context is not None
        assert context.root_object is not None
        assert context.source is not None
        assert context.tokenizer is not None

        doc = context.root_object
        src = context.source
        tok = context.tokenizer

        most_recent_xref: Optional[XREF] = None
        exceptions_to_rethrow = []

        # attempt to read plaintext XREF
        try:
            most_recent_xref = PlainTextXREF()
            assert most_recent_xref is not None
            most_recent_xref.set_parent(doc)  # type: ignore [attr-defined]
            most_recent_xref.read(src, tok, initial_offset)
            if "XRef" in doc:
                doc[Name("XRef")] = doc["XRef"].merge(most_recent_xref)
            else:
                doc[Name("XRef")] = most_recent_xref
        except Exception as ex0:
            most_recent_xref = None
            exceptions_to_rethrow.append(ex0)

        # attempt to read stream XREF
        if most_recent_xref is None:
            try:
                most_recent_xref = StreamXREF()
                assert most_recent_xref is not None
                most_recent_xref.set_parent(doc)  # type: ignore [attr-defined]
                most_recent_xref.read(src, tok, initial_offset)
                if "XRef" in doc:
                    doc[Name("XRef")] = doc["XRef"].merge(most_recent_xref)
                else:
                    doc[Name("XRef")] = most_recent_xref
            except Exception as ex0:
                most_recent_xref = None
                exceptions_to_rethrow.append(ex0)

        # attempt to rebuild XREF from document
        if most_recent_xref is None:
            try:
                most_recent_xref = RebuiltXREF()
                assert most_recent_xref is not None
                most_recent_xref.set_parent(doc)
                most_recent_xref.read(src, tok)
                if "XRef" in doc:
                    doc[Name("XRef")] = doc["XRef"].merge(most_recent_xref)
                else:
                    doc[Name("XRef")] = most_recent_xref
            except Exception as ex0:
                most_recent_xref = None
                exceptions_to_rethrow.append(ex0)

        # unable to read XREF
        # re-throw exceptions
        if most_recent_xref is None:
            for e in exceptions_to_rethrow:
                raise e

        # handle Prev, Previous
        assert most_recent_xref is not None
        prev = None
        if "Prev" in most_recent_xref["Trailer"]:
            prev = int(most_recent_xref["Trailer"]["Prev"])
        if "Previous" in most_recent_xref["Trailer"]:
            prev = int(most_recent_xref["Trailer"]["Previous"])
        if prev is not None:
            self._read_xref(context, initial_offset=prev)
