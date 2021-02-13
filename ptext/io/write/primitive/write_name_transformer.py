from typing import Optional

from ptext.io.read.types import AnyPDFType, Name
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteNameTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Name objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Name)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Name)

        context.destination.write(bytes("/" + object_to_transform, "latin1"))
