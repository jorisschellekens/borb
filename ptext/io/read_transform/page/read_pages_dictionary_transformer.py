import io
import typing
from typing import Optional, List, Any, Union, Dict

from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.types import (
    Dictionary,
    List,
    AnyPDFType,
)
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadPagesDictionaryTransformer(ReadBaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Dict) and "Type" in object and object["Type"] == "Pages"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        assert isinstance(object_to_transform, Dictionary)
        assert "Kids" in object_to_transform
        assert isinstance(object_to_transform["Kids"], List)

        # find Catalog
        catalog = parent_object
        while not isinstance(catalog, Dictionary) or not catalog["Type"] == "Catalog":
            try:
                catalog = catalog.get_parent()  # type: ignore [attr-defined]
            except:
                assert False

        # convert everything in /Kids
        for p in object_to_transform["Kids"]:
            page_out = self.get_root_transformer().transform(p, context)
            # TODO
