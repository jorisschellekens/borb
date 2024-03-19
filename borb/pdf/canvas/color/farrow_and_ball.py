#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Farrow & Ball is a British manufacturer of paints and wallpapers largely based upon historic colour palettes and archives.
The company is particularly well known for the unusual names of its products.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.color import RGBColor


class FarrowAndBall(HexColor):
    """
    Farrow & Ball is a British manufacturer of paints and wallpapers largely based upon historic colour palettes and archives.
    The company is particularly well known for the unusual names of its products.
    """

    COLOR_DEFINITION = {
        "all-white": "#faf9ef",
        "pointing": "#f9f3e3",
        "james-white": "#ece9d7",
        "white-tie": "#f2ead6",
        "clunch": "#e5dcc8",
        "blackened": "#dfdfdb",
        "tallow": "#f5ead2",
        "dimity": "#ece2d2",
        "great-white": "#e6e1dc",
        "strong-white": "#e9e7dd",
        "slipper-satin": "#eae4d3",
        "shaded-white": "#dad4c2",
        "new-white": "#f4e9d0",
        "lime-white": "#e9dfc9",
        "ringworld-ground": "#efe0c5",
        "matchstick": "#e6d8be",
        "house-white": "#f2e7c9",
        "off-white": "#e0d6c0",
        "string": "#dcceb0",
        "savage-ground": "#d7c5a9",
        "cord": "#d6c39f",
        "cream": "#e3cea7",
        "hay": "#d8c194",
        "light-stone": "#d1c1a0",
        "joas-white": "#e2d4be",
        "archive": "#decbb3",
        "stony-ground": "#cdc2ad",
        "cornforth-white": "#d4cfc7",
        "elephants-breath": "#cdc3b7",
        "lamp-room-gray": "#b7b6ae",
        "light-blue": "#b9beb5",
        "hardwick-white": "#b6b1a1",
        "blue-gray": "#b5b7a7",
        "french-gray": "#b4b19a",
        "pigeon": "#9fa195",
        "card-room-green": "#899081",
        "old-white": "#cdc3ad",
        "bone": "#cdc4ae",
        "fawn": "#ccbfa5",
        "biscuit": "#bca783",
        "light-gray": "#b2a894",
        "mouses-back": "#968975",
        "smoked-trout": "#bea895",
        "dead-salmon": "#b09b8c",
        "london-stone": "#b2a18d",
        "buff": "#b59e82",
        "drab": "#9b8a6f",
        "dauphin": "#928069",
        "pink-ground": "#ecd8ca",
        "calamine": "#e8d6d1",
        "setting-plaster": "#dbc2b0",
        "dutch-pink": "#d5b08a",
        "entrance-hall-pink": "#c39e80",
        "flower-pink": "#d6a787",
        "pintment-pink": "#c7997e",
        "red-earth": "#bb7b69",
        "porphyry-pink": "#b17b6c",
        "fox-red": "#a8725d",
        "loggia": "#aa6d5b",
        "blazer": "#ac514c",
        "book-room-red": "#a3695b",
        "picture-gallery-red": "#975b4f",
        "rectory-red": "#99434c",
        "radiocchio": "#8f4a51",
        "etruscan-red": "#7e534a",
        "eating-room-red": "#864e4f",
        "pale-hound": "#e6ddb8",
        "hound-lemon": "#e2d2a4",
        "farrows-cream": "#e8d4b0",
        "dayroom-yellow": "#f2dc9e",
        "dorset-cream": "#eacfa2",
        "gervase-yellow": "#dcc98f",
        "yellow-ground": "#efca89",
        "citron": "#eecc81",
        "ciara-yellow": "#e1c17e",
        "straw": "#d7b37e",
        "print-room-yellow": "#dbb678",
        "babouche": "#eabe67",
        "sudbury-yellow": "#d9b475",
        "octagon-yellow": "#d1ae72",
        "orangery": "#e0ae6c",
        "india-yellow": "#c09759",
        "cane": "#caa26c",
        "sand": "#ba9166",
        "green-ground": "#dbd8b6",
        "cooking-apple-green": "#c4c3a2",
        "vert-de-terre": "#babca4",
        "ball-green": "#bab393",
        "stone-white": "#b3ac8c",
        "green-stone": "#a59c78",
        "lichen": "#9e9f87",
        "olive": "#8b896b",
        "sutcliffe-green": "#899677",
        "pea-green": "#849779",
        "calke-green": "#77866a",
        "minster-green": "#586552",
        "powder-blue": "#acbdb4",
        "chappell-green": "#93a595",
        "saxon-green": "#99a680",
        "folly-green": "#95aa86",
        "breakfast-room-green": "#94a588",
        "arsenic": "#88b49b",
        "pale-powder": "#dde1d5",
        "borrowed-light": "#d8dfdc",
        "skylight": "#c6ccc7",
        "teresas-green": "#c2cfc2",
        "green-blue": "#aebdb1",
        "castle-gray": "#8d988c",
        "blue-ground": "#a7c9c8",
        "dix-blue": "#9ab1ab",
        "ballroom-blue": "#8faba7",
        "sugar-bag-light": "#81a09a",
        "oval-room-blue": "#8b9d9b",
        "berrington-blue": "#7e9495",
        "parma-gray": "#b1c0c2",
        "lulworth-blue": "#a2b8c7",
        "stone-blue": "#77989f",
        "chinese-blue": "#6f96a6",
        "cooks-blue": "#6f94b3",
        "pitch-blue": "#61718e",
        "wainscot": "#7e634e",
        "down-pipe": "#626665",
        "hague-blue": "#3e4e56",
        "brinjal": "#5a4348",
        "mahogany": "#524947",
        "off-black": "#424548",
        "green-smoke": "#717b70",
        "monkey-puzzle": "#4b5853",
        "caggiage-green": "#434c47",
        "railings": "#43474a",
        "studio-green": "#474d4a",
        "black-blue": "#3d4345",
    }

    #
    # CONSTRUCTOR
    #

    def __init__(self, color_name: str):
        assert color_name in FarrowAndBall.COLOR_DEFINITION
        self.color_name: str = color_name
        super(FarrowAndBall, self).__init__(FarrowAndBall.COLOR_DEFINITION[color_name])

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return FarrowAndBall(self.color_name)

    #
    # PUBLIC
    #

    @staticmethod
    def find_nearest_farrow_and_ball_color(color: Color) -> "FarrowAndBall":
        """
        This function find the nearest FarrowAndBall equivalent for a given Color
        :param color:   the input Color
        :return:        the (nearest) FarrowAndBall Color
        """
        rgb_color_001: RGBColor = color.to_rgb()
        min_dist: typing.Optional[Decimal] = None
        color_with_min_dist: typing.Optional[str] = None
        for n, c in FarrowAndBall.COLOR_DEFINITION.items():
            rgb_color_002: RGBColor = HexColor(c)
            d: Decimal = (
                (rgb_color_001.red - rgb_color_002.red) ** 2
                + (rgb_color_001.green - rgb_color_002.green) ** 2
                + (rgb_color_001.blue - rgb_color_002.blue) ** 2
            )
            if min_dist is None or d < min_dist:
                min_dist = d
                color_with_min_dist = n
        assert min_dist is not None
        assert color_with_min_dist is not None
        return FarrowAndBall(color_with_min_dist)

    def get_name(self) -> str:
        """
        This function returns the name of this FarrowAndBall color
        :return:    the name of this FarrowAndBall Color
        """
        return self.color_name
