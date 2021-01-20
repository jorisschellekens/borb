import datetime
import random
import typing
from typing import Any, Optional

from ptext.io.read_transform.types import (
    AnyPDFType,
    Dictionary,
    String,
    Name,
    List,
    HexadecimalString,
)
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)
from ptext.pdf.document import Document


class WritePDFTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Document)

    def transform(
        self,
        object_to_transform: Any,
        context: Optional[WriteTransformerContext] = None,
    ):
        # write header
        assert context is not None
        assert context.destination is not None

        context.destination.write(b"%PDF-1.7\n")
        context.destination.write(b"%")
        context.destination.write(bytes([226, 227, 207, 211]))
        context.destination.write(b"\n")

        # invalidate all references
        WritePDFTransformer._invalidate_all_references(object_to_transform)

        # create Info dictionary if needed
        if "Info" not in object_to_transform["XRef"]["Trailer"]:
            object_to_transform["XRef"]["Trailer"][Name("Info")] = Dictionary()

        # set /ID
        random_id = HexadecimalString("%032x" % random.randrange(16 ** 32))
        if "ID" not in object_to_transform["XRef"]["Trailer"]:
            object_to_transform["XRef"]["Trailer"][
                Name("ID")
            ] = List().set_can_be_referenced(  # type: ignore [attr-defined]
                False
            )
            object_to_transform["XRef"]["Trailer"]["ID"].append(random_id)
            object_to_transform["XRef"]["Trailer"]["ID"].append(random_id)
        else:
            object_to_transform["XRef"]["Trailer"]["ID"][1] = random_id

        # set CreationDate
        modification_date = WritePDFTransformer._timestamp_to_str()
        if "CreationDate" not in object_to_transform["XRef"]["Trailer"][Name("Info")]:
            object_to_transform["XRef"]["Trailer"][Name("Info")][
                Name("CreationDate")
            ] = String(modification_date)

        # set ModDate
        object_to_transform["XRef"]["Trailer"]["Info"][Name("ModDate")] = String(
            modification_date
        )

        # set Producer
        object_to_transform["XRef"]["Trailer"]["Info"][Name("Producer")] = String(
            "pText"
        )

        # transform XREF
        self.get_root_transformer().transform(object_to_transform["XRef"], context)

    @staticmethod
    def _timestamp_to_str() -> str:
        timestamp_str = "D:"
        now = datetime.datetime.now()
        for n in [now.year, now.month, now.day, now.hour, now.minute, now.second]:
            timestamp_str += "{0:02}".format(n)
        timestamp_str += "+00"
        return timestamp_str

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
                obj.set_reference(None)  # type: ignore [union-attr]
            except:
                pass
            if isinstance(obj, List):
                assert isinstance(obj, List)
                for v in obj:
                    objects_todo.append(v)
                continue
            if isinstance(obj, Dictionary):
                assert isinstance(obj, Dictionary)
                for k, v in obj.items():
                    objects_todo.append(k)
                    objects_todo.append(v)
                continue
