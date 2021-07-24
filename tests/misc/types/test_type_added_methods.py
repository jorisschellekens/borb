import copy
import unittest

import requests
from PIL import Image as PILImage  # type: ignore [import]

from borb.io.read.types import add_base_methods


class TestTypeAddedMethods(unittest.TestCase):
    def test_type_methods(self):

        im0 = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                stream=True,
            ).raw
        )
        im0._parent = None

        im1 = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                stream=True,
            ).raw
        )

        # add methods
        add_base_methods(im1)

        # set _parent
        im1.set_parent(im0)

        # copy
        im2 = copy.deepcopy(im1)

        # check
        assert im1.get_parent() == im0
