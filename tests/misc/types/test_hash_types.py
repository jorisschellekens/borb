import types
import unittest
from decimal import Decimal

import requests
from PIL import Image as PILImage  # type: ignore [import]

from ptext.io.read.types import (
    Dictionary,
    Name,
    Reference,
    Boolean,
    List,
    add_base_methods,
)


class TestHashTypes(unittest.TestCase):
    def test_hash_types(self):

        obj0 = Dictionary()
        obj0[Name("Root")] = Reference(object_number=10)
        obj0[Name("Marked")] = Boolean(True)

        obj1 = List()
        obj1.append(Name("Red"))
        obj1.append(Decimal(0.5))

        print(hash(obj1))

    def test_hash_image(self):

        im0 = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                stream=True,
            ).raw
        )
        add_base_methods(im0)

        # add hash method
        def img_hash(self):
            return hash(tuple(vars(self)))

        def img_eq(self, other):
            return self == other

        im0.__hash__ = types.MethodType(img_hash, im0)
        im0.__eq__ = types.MethodType(img_eq, im0)

        # attempt to calculate hash
        print(im0.__hash__())

        d = {}
        d[im0] = 1

        assert d[im0] == 1
