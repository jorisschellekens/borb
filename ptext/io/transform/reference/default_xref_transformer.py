import io
import os
import typing
from decimal import Decimal
from typing import Union, Optional, Any

from ptext.exception.pdf_exception import PDFCommentTokenNotFoundError
from ptext.io.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.document import Document
from ptext.pdf.xref.plaintext_xref import PlainTextXREF
from ptext.pdf.xref.stream_xref import StreamXREF


class DefaultXREFTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.tokenizer = None

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

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
            context.root_object.add_event_listener(l)

        # remove prefix
        self._remove_prefix(context)

        # check header
        self._check_header(context)

        # file size
        context.source.seek(0, os.SEEK_END)
        file_length = context.source.tell()
        context.source.seek(0)
        context.root_object["FileSize"] = Decimal(file_length)

        # build XREF object
        self._read_xref(context)

        # transform trailer dictionary
        xref = context.root_object.get("XRef")

        if "Trailer" in xref and "Encrypt" in xref["Trailer"]:
            # TODO
            raise NotImplementedError(
                "password-protected PDFs are currently not supported"
            )
        trailer = self.get_root_transformer().transform(
            context.root_object["XRef"]["Trailer"],
            context.root_object,
            context,
            [],
        )

        xref["Trailer"] = trailer
        for k in ["DecodeParms", "Filter", "Index", "Length", "Prev", "W"]:
            if k in xref["Trailer"]:
                xref["Trailer"].pop(k)

        # return
        return context.root_object

    def _remove_prefix(self, context: TransformerContext) -> None:

        assert context is not None
        assert context.source is not None

        # read first 2 Kb
        bytes_near_sof = "".join(
            [context.source.read(1).decode("latin-1") for _ in range(0, 2048)]
        )
        context.source.seek(0)

        # find %PDF-
        index_of_pdf_comment = -1
        try:
            index_of_pdf_comment = bytes_near_sof.index("%PDF")
        except ValueError:
            pass

        # truncate
        if index_of_pdf_comment > 0:
            # determine end of file
            end_of_file = context.source.seek(0, os.SEEK_END)
            context.source.seek(0)
            # build byte array
            bts = context.source.read(end_of_file)[index_of_pdf_comment:end_of_file]
            # reset values in context
            context.source = io.BytesIO(bts)
            context.tokenizer.io_source = context.source

    def _check_header(self, context: TransformerContext) -> None:
        """
        This function checks whether or not the first bytes in the document contain the text %PDF
        :param context: the TransformerContext (containing the io source)
        :type context: TransformerContext
        """
        src = context.source
        tok = context.tokenizer
        src.seek(0)
        arr = [t for t in [tok.next_token() for _ in range(0, 10)] if t is not None]
        if len(arr) == 0:
            raise PDFCommentTokenNotFoundError(byte_offset=0)
        if not any([t.text.startswith("%PDF") for t in arr]):
            raise PDFCommentTokenNotFoundError(byte_offset=0)

    def _read_xref(
        self, context: TransformerContext, initial_offset: Optional[int] = None
    ) -> None:
        """
        This function attempts to read the XREF table, first as plaintext, then as a stream
        :param context:         the TransformerContext (containing the io source)
        :type context:          TransformerContext
        :param initial_offset:  the initial byte offset at which to read (set to None to allow this method to find the XREF)
        :type initial_offset:   int
        """
        doc = context.root_object
        src = context.source
        tok = context.tokenizer

        most_recent_xref = None
        exceptions_to_rethrow = []

        # attempt to read plaintext XREF
        try:
            most_recent_xref = PlainTextXREF()
            most_recent_xref.parent = doc
            most_recent_xref.read(src, tok, initial_offset)
            if "XRef" in doc:
                doc["XRef"] = doc["XRef"].merge(most_recent_xref)
            else:
                doc["XRef"] = most_recent_xref
        except Exception as ex0:
            most_recent_xref = None
            exceptions_to_rethrow.append(ex0)

        # attempt to read stream XREF
        if most_recent_xref is None:
            try:
                most_recent_xref = StreamXREF()
                most_recent_xref.parent = doc
                most_recent_xref.read(src, tok, initial_offset)
                if "XRef" in doc:
                    doc["XRef"] = doc["XRef"].merge(most_recent_xref)
                else:
                    doc["XRef"] = most_recent_xref
            except Exception as ex0:
                raise ex0
                most_recent_xref = None
                exceptions_to_rethrow.append(ex0)

        # unable to read XREF
        # re-throw exceptions
        if most_recent_xref is None:
            for e in exceptions_to_rethrow:
                raise e

        # handle Prev, Previous
        prev = None
        if "Prev" in most_recent_xref["Trailer"]:
            prev = int(most_recent_xref["Trailer"]["Prev"])
        if "Previous" in most_recent_xref["Trailer"]:
            prev = int(most_recent_xref["Trailer"]["Previous"])
        if prev is not None:
            self._read_xref(context, initial_offset=prev)
