from typing import Optional

from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_object import PDFObject, PDFIndirectObject


class PDFDictionary(PDFObject):
    """
    A dictionary object is an associative table containing pairs of objects, known as the dictionary’s entries. The first
    element of each entry is the key and the second element is the value. The key shall be a name (unlike
    dictionary keys in PostScript, which may be objects of any type). The value may be any kind of object, including
    another dictionary. A dictionary entry whose value is null (see 7.3.9, "Null Object") shall be treated the same as
    if the entry does not exist. (This differs from PostScript, where null behaves like any other object as the value
    of a dictionary entry.) The number of entries in a dictionary shall be subject to an implementation limit; see
    Annex C. A dictionary may have zero entries.

    The entries in a dictionary represent an associative table and as such shall be unordered even though an
    arbitrary order may be imposed upon them when written in a file. That ordering shall be ignored.
    """

    def __init__(self):
        super().__init__()
        self.dictionary = {}

    def get(
        self,
        name: PDFName,
        default_value: Optional[PDFObject] = None,
        resolve_indirect_object: bool = True,
    ) -> Optional[PDFObject]:
        if name not in self.dictionary:
            return None
        obj = self.dictionary[name]
        while isinstance(obj, PDFIndirectObject):
            obj = obj.get_object()
        return obj

    def __contains__(self, item):
        return item in self.dictionary

    def __getitem__(self, item):
        return self.dictionary[item]

    def __len__(self):
        return len(self.dictionary)

    def __setitem__(self, key, value):
        self.dictionary[key] = value

    def __str__(self):
        return (
            "<<\n"
            + "".join(
                [(str(k) + " " + str(v) + "\n") for k, v in self.dictionary.items()]
            )
            + ">>"
        )

    def items(self):
        return self.dictionary.items()
