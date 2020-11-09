import io
import os
from typing import Union, Optional, List

from ptext.exception.pdf_exception import PDFCommentTokenNotFoundError
from ptext.io.tokenizer.high_level_tokenizer import HighLevelTokenizer
from ptext.object.document.document import Document
from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.object.xref.plaintext_xref import PlainTextXREF
from ptext.object.xref.stream_xref import StreamXREF
from ptext.primitive.pdf_number import PDFInt
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultXREFTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.tokenizer = None

    def can_be_transformed(self, object: Union[io.IOBase, PDFObject]) -> bool:
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: Union[io.IOBase, PDFObject],
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        # update context
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
        context.root_object.set("FileSize", PDFInt(file_length))

        # build XREF object
        self._read_xref(context)

        # transform trailer dictionary
        xref = context.root_object.get("XRef")
        trailer = self.get_root_transformer().transform(
            context.root_object.get(["XRef", "Trailer"]),
            context.root_object,
            context,
            [],
        )
        xref.set("Trailer", trailer)

        # return
        return context.root_object

    def _remove_prefix(self, context: TransformerContext) -> None:

        src = context.source

        # read first 2 Kb
        bytes_near_sof = "".join(
            [src.read(1).decode("latin-1") for _ in range(0, 2048)]
        )
        src.seek(0)

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
            most_recent_xref.parent = self
            most_recent_xref.read(src, tok, initial_offset)
            if doc.has_key("XRef"):
                doc.set(
                    "XRef",
                    doc.get("XRef").merge_references(most_recent_xref),
                )
            else:
                doc.set("XRef", most_recent_xref)
        except Exception as ex0:
            most_recent_xref = None
            exceptions_to_rethrow.append(ex0)

        # attempt to read stream XREF
        if most_recent_xref is None:
            try:
                most_recent_xref = StreamXREF()
                most_recent_xref.parent = self
                most_recent_xref.read(src, tok, initial_offset)
                if doc.has_key("XRef"):
                    doc.set(
                        "XRef",
                        doc.get("XRef").merge_references(most_recent_xref),
                    )
                else:
                    doc.set("XRef", most_recent_xref)
            except Exception as ex0:
                most_recent_xref = None
                exceptions_to_rethrow.append(ex0)

        # unable to read XREF
        # re-throw exceptions
        if most_recent_xref is None:
            for e in exceptions_to_rethrow:
                raise e
