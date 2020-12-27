import io
from typing import Any, Optional


class TransformerWriteContext:
    def __init__(
        self,
        destination: Optional[io.IOBase] = None,
        root_object: Optional[Any] = None,
    ):
        self.destination = destination
        self.root_object = root_object
        self.object_number_dictionary = {}


class PDFTransformer:
    def can_be_transformed(self, any: Any):
        return True

    def transform(
        self,
        object_to_transform: Any,
        context: Optional[TransformerWriteContext] = None,
    ):
        # write header
        context.destination.write(b"%PDF-1.7")

        # write root
        root = object_to_transform["XRef"]["Trailer"]["Root"]

        # write xref
        xref = object_to_transform["XRef"]

        # write trailer
        pass
