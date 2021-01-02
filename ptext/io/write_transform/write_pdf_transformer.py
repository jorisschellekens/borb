import datetime
from typing import Any, Optional

from ptext.io.read_transform.types import AnyPDFType, Dictionary, String
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    TransformerWriteContext,
)
from ptext.pdf.document import Document


class WritePDFTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Document)

    def transform(
        self,
        object_to_transform: Any,
        context: Optional[TransformerWriteContext] = None,
    ):
        # write header
        assert context is not None
        assert context.destination is not None
        context.destination.write(b"%PDF-1.7\n")

        # create Info dictionary if needed
        if "Info" not in object_to_transform["XRef"]["Trailer"]:
            object_to_transform["XRef"]["Trailer"]["Info"] = Dictionary()
        # set CreationDate
        now = datetime.datetime.now()
        modification_date = "D:%d%d%d%d%d%d+00" % (
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
        )
        if "CreationDate" not in object_to_transform["XRef"]["Trailer"]["Info"]:
            object_to_transform["XRef"]["Trailer"]["Info"][
                "CreationDate"
            ] = modification_date
        # set ModDate
        object_to_transform["XRef"]["Trailer"]["Info"]["ModDate"] = String(
            modification_date
        )
        # set Producer
        object_to_transform["XRef"]["Trailer"]["Info"]["Producer"] = String("pText")

        # transform XREF
        self.get_root_transformer().transform(object_to_transform["XRef"], context)
