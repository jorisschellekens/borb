#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a customizable cartoon avatar for insertion into PDF documents.

This class extends the functionality of the Image class, allowing users to create and customize
a cartoon avatar by selecting various attributes such as skin color, hair color, facial features,
clothing, and accessories. The avatar can be easily rendered as an image and inserted into PDF documents,
providing a fun and personalized touch to reports, profiles, or any PDF content.
"""
import enum
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hex_color import HexColor
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class Avatar(Image):
    """
    Represents a customizable cartoon avatar for insertion into PDF documents.

    This class extends the functionality of the Image class, allowing users to create and customize
    a cartoon avatar by selecting various attributes such as skin color, hair color, facial features,
    clothing, and accessories. The avatar can be easily rendered as an image and inserted into PDF documents,
    providing a fun and personalized touch to reports, profiles, or any PDF content.
    """

    class BackgroundStyleType(enum.Enum):
        """An enumeration representing different styles for the avatar background."""

        CIRCLE = 2
        NO_CIRCLE = 3

    class SkinColorType(enum.Enum):
        """An enumeration representing different skin color types for a cartoon avatar."""

        BLACK = 2
        BROWN = 3
        DARK_BROWN = 5
        LIGHT = 7
        PALE = 11
        TANNED = 13
        OLIVE = 17

    class HairColorType(enum.Enum):
        """An enumeration representing different hair color types for a cartoon avatar."""

        AUBURN = 2
        BLACK = 3
        BLONDE = 5
        BROWN = 7
        DARK_BROWN = 11
        GOLDEN_BLONDE = 13
        PASTEL_PINK = 17
        PLATINUM = 19
        RED = 23
        SILVER = 29

    class FacialHairType(enum.Enum):
        """An enumeration representing different facial hair styles for a cartoon avatar."""

        BEARD_LIGHT = 2
        BEARD_MAJESTIC = 3
        BEARD_MEDIUM = 5
        MUSTACHE_FANCY = 7
        MUSTACHE_MAGNUM = 11
        NONE = 13

    class MouthType(enum.Enum):
        """An enumeration representing different mouth expressions or styles for a cartoon avatar."""

        CONCERNED = 2
        DEFAULT = 3
        DISBELIEF = 5
        EATING = 7
        GRIMACE = 11
        SAD = 13
        SCREAM_OPEN = 17
        SERIOUS = 23
        SMILE = 29
        TONGUE = 31
        TWINKLE = 37
        VOMIT = 41

    class TopOfHeadType(enum.Enum):
        """An enumeration representing different styles for the top of the head on a cartoon avatar."""

        EYE_PATCH = 2
        HAT = 3
        HIJAB = 5
        LONG_HAIR_BIG_HAIR = 7
        LONG_HAIR_BOB = 11
        LONG_HAIR_BUN = 13
        LONG_HAIR_CURLY = 17
        LONG_HAIR_CURVY = 19
        LONG_HAIR_DREADS = 23
        LONG_HAIR_FRIDA = 29
        LONG_HAIR_FRO = 31
        LONG_HAIR_FRO_BAND = 37
        LONG_HAIR_MIA_WALLACE = 41
        LONG_HAIR_NOT_TOO_LONG = 43
        LONG_HAIR_SHAVED_SIDES = 47
        LONG_HAIR_STRAIGHT_01 = 53
        LONG_HAIR_STRAIGHT_02 = 59
        LONG_HAIR_STRAIGHT_STRAND = 61
        NO_HAIR = 67
        SHORT_HAIR_DREADS_01 = 71
        SHORT_HAIR_DREADS_02 = 73
        SHORT_HAIR_FRIZZLE = 79
        SHORT_HAIR_SHAGGY_MULLET = 83
        SHORT_HAIR_SHORT_CURLY = 89
        SHORT_HAIR_SHORT_FLAT = 97
        SHORT_HAIR_SHORT_ROUND = 101
        SHORT_HAIR_SHORT_WAVED = 103
        SHORT_HAIR_SIDES = 107
        SHORT_HAIR_THE_CAESAR = 109
        SHORT_HAIR_THE_CAESAR_SIDE_PART = 113
        TURBAN = 127
        WINTER_HAT_01 = 131
        WINTER_HAT_02 = 137
        WINTER_HAT_03 = 139
        WINTER_HAT_04 = 149

    class EyeType(enum.Enum):
        """An enumeration representing different eye shapes or expressions for a cartoon avatar."""

        DEFAULT = 2
        CLOSE = 3
        CRYING = 5
        DIZZY = 7
        EYE_ROLL = 11
        HAPPY = 13
        HEARTS = 17
        SIDE = 19
        SQUINT = 23
        SURPRISED = 29
        WINK_01 = 31
        WINK_02 = 37

    class EyebrowType(enum.Enum):
        """An enumeration representing different eyebrow shapes or expressions for a cartoon avatar."""

        ANGRY = 2
        ANGRY_NATURAL = 3
        DEFAULT = 5
        DEFAULT_NATURAL = 7
        FLAT_NATURAL = 11
        FROWN_NATURAL = 13
        RAISED_EXCITED = 15
        RAISED_EXCITED_NATURAL = 17
        SAD_CONCERNED = 19
        SAD_CONCERNED_NATURAL = 23
        UNI_BROW_NATURAL = 29
        UP_DOWN = 31
        UP_DOWN_NATURAL = 37

    class GlassesType(enum.Enum):
        """An enumeration representing different styles of glasses for a cartoon avatar."""

        KURT_COBAIN = 2
        NONE = 3
        PRESCRIPTION_BLACK = 5
        PRESCRIPTION_WHITE = 7
        ROUND = 11
        SUNGLASSES = 13
        WAYFARERS = 17

    class ClothingType(enum.Enum):
        """An enumeration representing different types of clothing styles for a cartoon avatar."""

        BLAZER_AND_SHIRT = 2
        BLAZER_AND_SWEATER = 3
        COLLAR_SWEATER = 5
        HOODIE = 7
        OVERALL = 11
        SHIRT_CREW_NECK = 13
        SHIRT_SCOOP_NECK = 17
        SHIRT_V_NECK = 19
        TSHIRT = 23

    class ShirtLogoType(enum.Enum):
        """An enumeration representing different logo types for shirts in a cartoon avatar."""

        BAT = 2
        BEAR = 3
        CUMBIA = 5
        DEER = 7
        DIAMOND = 11
        HOLA = 13
        PIZZA = 17
        RESIST = 19
        SELENA = 23
        SKULL = 29
        SKULL_OUTLINE = 31

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_circle_color: typing.Optional[Color] = None,
        background_color: typing.Optional[Color] = None,
        background_style_type: BackgroundStyleType = BackgroundStyleType.CIRCLE,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        clothing_type: ClothingType = ClothingType.HOODIE,
        eyebrow_type: EyebrowType = EyebrowType.DEFAULT,
        eye_type: EyeType = EyeType.DEFAULT,
        facial_hair_type: FacialHairType = FacialHairType.BEARD_MEDIUM,
        glasses_type: GlassesType = GlassesType.PRESCRIPTION_BLACK,
        hair_color_type: HairColorType = HairColorType.BROWN,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        mouth_type: MouthType = MouthType.SMILE,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        shirt_logo_type: ShirtLogoType = ShirtLogoType.BEAR,
        size: typing.Tuple[int, int] = (64, 64),
        skin_color_type: SkinColorType = SkinColorType.LIGHT,
        top_of_head_type: TopOfHeadType = TopOfHeadType.SHORT_HAIR_SIDES,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize an Avatar instance with customizable attributes for appearance and layout.

        :param background_color:        The color of the avatar's background. Defaults to None (transparent).
        :param background_style_type:   The style of the background behind the avatar. Defaults to BackgroundStyleType.CIRCLE.
        :param border_color:            The color of the avatar's border. Defaults to None (no border).
        :param border_dash_pattern:     A list defining the dash pattern for the border. Defaults to an empty list (solid border).
        :param border_dash_phase:       The phase for the dash pattern. Defaults to 0.
        :param border_width_bottom:     The width of the bottom border in pixels. Defaults to 0 (no border).
        :param border_width_left:       The width of the left border in pixels. Defaults to 0 (no border).
        :param border_width_right:      The width of the right border in pixels. Defaults to 0 (no border).
        :param border_width_top:        The width of the top border in pixels. Defaults to 0 (no border).
        :param clothing_type:           The type of clothing the avatar wears. Defaults to ClothingType.HOODIE.
        :param eyebrow_type:            The style of the avatar's eyebrows. Defaults to EyebrowType.DEFAULT.
        :param eye_type:                The style of the avatar's eyes. Defaults to EyeType.DEFAULT.
        :param facial_hair_type:        The type of facial hair on the avatar. Defaults to FacialHairType.BEARD_MEDIUM.
        :param glasses_type:            The type of glasses the avatar wears. Defaults to GlassesType.PRESCRIPTION_BLACK.
        :param hair_color_type:         The color of the avatar's hair. Defaults to HairColorType.BROWN.
        :param horizontal_alignment:    The horizontal alignment of the avatar within its container. Defaults to LayoutElement.HorizontalAlignment.LEFT.
        :param margin_bottom:           The bottom margin in pixels. Defaults to 0.
        :param margin_left:             The left margin in pixels. Defaults to 0.
        :param margin_right:            The right margin in pixels. Defaults to 0.
        :param margin_top:              The top margin in pixels. Defaults to 0.
        :param mouth_type:              The expression of the avatar's mouth. Defaults to MouthType.SMILE.
        :param padding_bottom:          The bottom padding in pixels. Defaults to 0.
        :param padding_left:            The left padding in pixels. Defaults to 0.
        :param padding_right:           The right padding in pixels. Defaults to 0.
        :param padding_top:             The top padding in pixels. Defaults to 0.
        :param shirt_logo_type:         The logo displayed on the avatar's shirt. Defaults to ShirtLogoType.BEAR.
        :param size:                    The size of the avatar as a tuple (width, height) in pixels. Defaults to (64, 64).
        :param skin_color_type:         The skin color of the avatar. Defaults to SkinColorType.LIGHT.
        :param top_of_head_type:        The style of hair or headwear on the avatar. Defaults to TopOfHeadType.SHORT_HAIR_SIDES.
        :param vertical_alignment:      The vertical alignment of the avatar within its container. Defaults to LayoutElement.VerticalAlignment.TOP.
        """
        self.__background_circle_color: typing.Optional[Color] = background_circle_color
        self.__background_style_type: Avatar.BackgroundStyleType = background_style_type
        self.__skin_color_type: Avatar.SkinColorType = skin_color_type
        self.__hair_color_type: Avatar.HairColorType = hair_color_type
        self.__facial_hair_type: Avatar.FacialHairType = facial_hair_type
        self.__mouth_type: Avatar.MouthType = mouth_type
        self.__top_of_head_type: Avatar.TopOfHeadType = top_of_head_type
        self.__eye_type: Avatar.EyeType = eye_type
        self.__eyebrow_type: Avatar.EyebrowType = eyebrow_type
        self.__glasses_type: Avatar.GlassesType = glasses_type
        self.__clothing_type: Avatar.ClothingType = clothing_type
        self.__shirt_logo_type: Avatar.ShirtLogoType = shirt_logo_type
        super().__init__(
            bytes_path_pil_image_or_url=self.__get_image_bytes(),
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            size=size,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __get_closest_matching_avataaars_color(c: typing.Optional[Color]) -> typing.Any:
        try:
            import py_avataaars  # type: ignore[import-untyped, import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'py_avataaars' library to use the Avatar class. "
                "You can install it with 'pip install py_avataaars'."
            )

        if c is None:
            return py_avataaars.Color.BLUE_01
        py_avataaars_colors = {
            py_avataaars.Color.BLACK: HexColor("#262E33"),
            py_avataaars.Color.BLUE_01: HexColor("#65C9FF"),
            py_avataaars.Color.BLUE_02: HexColor("#5199E4"),
            py_avataaars.Color.BLUE_03: HexColor("#25557C"),
            py_avataaars.Color.GRAY_01: HexColor("#E6E6E6"),
            py_avataaars.Color.GRAY_02: HexColor("#929598"),
            py_avataaars.Color.HEATHER: HexColor("#3C4F5C"),
            py_avataaars.Color.PASTEL_BLUE: HexColor("#B1E2FF"),
            py_avataaars.Color.PASTEL_GREEN: HexColor("#A7FFC4"),
            py_avataaars.Color.PASTEL_ORANGE: HexColor("#FFDEB5"),
            py_avataaars.Color.PASTEL_RED: HexColor("#FFAFB9"),
            py_avataaars.Color.PASTEL_YELLOW: HexColor("#FFFFB1"),
            py_avataaars.Color.PINK: HexColor("#FF488E"),
            py_avataaars.Color.RED: HexColor("#FF5C5C"),
            py_avataaars.Color.WHITE: HexColor("#FFFFFF"),
        }
        c_as_rgb_color: RGBColor = c.to_rgb_color()
        c_min: typing.Optional[py_avataaars.Color] = None
        d_min: typing.Optional[float] = None
        for k, v in py_avataaars_colors.items():
            d: float = (
                (c_as_rgb_color.get_red() - v.get_red()) ** 2
                + (c_as_rgb_color.get_green() - v.get_green()) ** 2
                + (c_as_rgb_color.get_blue() - v.get_blue()) ** 2
            )
            if d_min is None or d < d_min:
                d_min = d
                c_min = k
        assert c_min is not None
        return c_min

    def __get_image_bytes(self) -> bytes:
        try:
            import py_avataaars  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Please install the 'py_avataaars' library to use the Avatar class. "
                "You can install it with 'pip install py_avataaars'."
            )

        return py_avataaars.PyAvataaar(
            style={
                Avatar.BackgroundStyleType.CIRCLE: py_avataaars.AvatarStyle.CIRCLE,
                Avatar.BackgroundStyleType.NO_CIRCLE: py_avataaars.AvatarStyle.TRANSPARENT,
            }[self.__background_style_type],
            background_color=Avatar.__get_closest_matching_avataaars_color(
                self.__background_circle_color
            ),
            skin_color={
                Avatar.SkinColorType.BLACK: py_avataaars.SkinColor.BLACK,
                Avatar.SkinColorType.BROWN: py_avataaars.SkinColor.BROWN,
                Avatar.SkinColorType.DARK_BROWN: py_avataaars.SkinColor.DARK_BROWN,
                Avatar.SkinColorType.LIGHT: py_avataaars.SkinColor.LIGHT,
                Avatar.SkinColorType.PALE: py_avataaars.SkinColor.PALE,
                Avatar.SkinColorType.TANNED: py_avataaars.SkinColor.TANNED,
                Avatar.SkinColorType.OLIVE: py_avataaars.SkinColor.YELLOW,
            }[self.__skin_color_type],
            hair_color={
                Avatar.HairColorType.AUBURN: py_avataaars.HairColor.AUBURN,
                Avatar.HairColorType.BLACK: py_avataaars.HairColor.BLACK,
                Avatar.HairColorType.BLONDE: py_avataaars.HairColor.BLONDE,
                Avatar.HairColorType.GOLDEN_BLONDE: py_avataaars.HairColor.BLONDE_GOLDEN,
                Avatar.HairColorType.BROWN: py_avataaars.HairColor.BROWN,
                Avatar.HairColorType.DARK_BROWN: py_avataaars.HairColor.BROWN_DARK,
                Avatar.HairColorType.PASTEL_PINK: py_avataaars.HairColor.PASTEL_PINK,
                Avatar.HairColorType.PLATINUM: py_avataaars.HairColor.PLATINUM,
                Avatar.HairColorType.RED: py_avataaars.HairColor.RED,
                Avatar.HairColorType.SILVER: py_avataaars.HairColor.SILVER_GRAY,
            }[self.__hair_color_type],
            facial_hair_type={
                Avatar.FacialHairType.BEARD_LIGHT: py_avataaars.FacialHairType.BEARD_LIGHT,
                Avatar.FacialHairType.BEARD_MAJESTIC: py_avataaars.FacialHairType.BEARD_MAJESTIC,
                Avatar.FacialHairType.BEARD_MEDIUM: py_avataaars.FacialHairType.BEARD_MEDIUM,
                Avatar.FacialHairType.MUSTACHE_FANCY: py_avataaars.FacialHairType.MOUSTACHE_FANCY,
                Avatar.FacialHairType.MUSTACHE_MAGNUM: py_avataaars.FacialHairType.MOUSTACHE_MAGNUM,
                Avatar.FacialHairType.NONE: py_avataaars.FacialHairType.DEFAULT,
            }[self.__facial_hair_type],
            top_type={
                Avatar.TopOfHeadType.EYE_PATCH: py_avataaars.TopType.EYE_PATCH,
                Avatar.TopOfHeadType.HAT: py_avataaars.TopType.HAT,
                Avatar.TopOfHeadType.HIJAB: py_avataaars.TopType.HIJAB,
                Avatar.TopOfHeadType.LONG_HAIR_BIG_HAIR: py_avataaars.TopType.LONG_HAIR_BIG_HAIR,
                Avatar.TopOfHeadType.LONG_HAIR_BOB: py_avataaars.TopType.LONG_HAIR_BOB,
                Avatar.TopOfHeadType.LONG_HAIR_BUN: py_avataaars.TopType.LONG_HAIR_BUN,
                Avatar.TopOfHeadType.LONG_HAIR_CURLY: py_avataaars.TopType.LONG_HAIR_CURLY,
                Avatar.TopOfHeadType.LONG_HAIR_CURVY: py_avataaars.TopType.LONG_HAIR_CURVY,
                Avatar.TopOfHeadType.LONG_HAIR_DREADS: py_avataaars.TopType.LONG_HAIR_DREADS,
                Avatar.TopOfHeadType.LONG_HAIR_FRIDA: py_avataaars.TopType.LONG_HAIR_FRIDA,
                Avatar.TopOfHeadType.LONG_HAIR_FRO: py_avataaars.TopType.LONG_HAIR_FRO,
                Avatar.TopOfHeadType.LONG_HAIR_FRO_BAND: py_avataaars.TopType.LONG_HAIR_FRO_BAND,
                Avatar.TopOfHeadType.LONG_HAIR_MIA_WALLACE: py_avataaars.TopType.LONG_HAIR_MIA_WALLACE,
                Avatar.TopOfHeadType.LONG_HAIR_NOT_TOO_LONG: py_avataaars.TopType.LONG_HAIR_NOT_TOO_LONG,
                Avatar.TopOfHeadType.LONG_HAIR_SHAVED_SIDES: py_avataaars.TopType.LONG_HAIR_SHAVED_SIDES,
                Avatar.TopOfHeadType.LONG_HAIR_STRAIGHT_01: py_avataaars.TopType.LONG_HAIR_STRAIGHT,
                Avatar.TopOfHeadType.LONG_HAIR_STRAIGHT_02: py_avataaars.TopType.LONG_HAIR_STRAIGHT2,
                Avatar.TopOfHeadType.LONG_HAIR_STRAIGHT_STRAND: py_avataaars.TopType.LONG_HAIR_STRAIGHT_STRAND,
                Avatar.TopOfHeadType.NO_HAIR: py_avataaars.TopType.NO_HAIR,
                Avatar.TopOfHeadType.SHORT_HAIR_DREADS_01: py_avataaars.TopType.SHORT_HAIR_DREADS_01,
                Avatar.TopOfHeadType.SHORT_HAIR_DREADS_02: py_avataaars.TopType.SHORT_HAIR_DREADS_02,
                Avatar.TopOfHeadType.SHORT_HAIR_FRIZZLE: py_avataaars.TopType.SHORT_HAIR_FRIZZLE,
                Avatar.TopOfHeadType.SHORT_HAIR_SHAGGY_MULLET: py_avataaars.TopType.SHORT_HAIR_SHAGGY_MULLET,
                Avatar.TopOfHeadType.SHORT_HAIR_SHORT_CURLY: py_avataaars.TopType.SHORT_HAIR_SHORT_CURLY,
                Avatar.TopOfHeadType.SHORT_HAIR_SHORT_FLAT: py_avataaars.TopType.SHORT_HAIR_SHORT_FLAT,
                Avatar.TopOfHeadType.SHORT_HAIR_SHORT_ROUND: py_avataaars.TopType.SHORT_HAIR_SHORT_ROUND,
                Avatar.TopOfHeadType.SHORT_HAIR_SHORT_WAVED: py_avataaars.TopType.SHORT_HAIR_SHORT_WAVED,
                Avatar.TopOfHeadType.SHORT_HAIR_SIDES: py_avataaars.TopType.SHORT_HAIR_SIDES,
                Avatar.TopOfHeadType.SHORT_HAIR_THE_CAESAR: py_avataaars.TopType.SHORT_HAIR_THE_CAESAR,
                Avatar.TopOfHeadType.SHORT_HAIR_THE_CAESAR_SIDE_PART: py_avataaars.TopType.SHORT_HAIR_THE_CAESAR_SIDE_PART,
                Avatar.TopOfHeadType.TURBAN: py_avataaars.TopType.TURBAN,
                Avatar.TopOfHeadType.WINTER_HAT_01: py_avataaars.TopType.WINTER_HAT1,
                Avatar.TopOfHeadType.WINTER_HAT_02: py_avataaars.TopType.WINTER_HAT2,
                Avatar.TopOfHeadType.WINTER_HAT_03: py_avataaars.TopType.WINTER_HAT3,
                Avatar.TopOfHeadType.WINTER_HAT_04: py_avataaars.TopType.WINTER_HAT4,
            }[self.__top_of_head_type],
            mouth_type={
                Avatar.MouthType.CONCERNED: py_avataaars.MouthType.CONCERNED,
                Avatar.MouthType.DEFAULT: py_avataaars.MouthType.DEFAULT,
                Avatar.MouthType.DISBELIEF: py_avataaars.MouthType.DISBELIEF,
                Avatar.MouthType.EATING: py_avataaars.MouthType.EATING,
                Avatar.MouthType.GRIMACE: py_avataaars.MouthType.GRIMACE,
                Avatar.MouthType.SAD: py_avataaars.MouthType.SAD,
                Avatar.MouthType.SCREAM_OPEN: py_avataaars.MouthType.SCREAM_OPEN,
                Avatar.MouthType.SERIOUS: py_avataaars.MouthType.SERIOUS,
                Avatar.MouthType.SMILE: py_avataaars.MouthType.SMILE,
                Avatar.MouthType.TONGUE: py_avataaars.MouthType.TONGUE,
                Avatar.MouthType.TWINKLE: py_avataaars.MouthType.TWINKLE,
                Avatar.MouthType.VOMIT: py_avataaars.MouthType.VOMIT,
            }[self.__mouth_type],
            eye_type={
                Avatar.EyeType.DEFAULT: py_avataaars.EyesType.DEFAULT,
                Avatar.EyeType.CLOSE: py_avataaars.EyesType.CLOSE,
                Avatar.EyeType.CRYING: py_avataaars.EyesType.CRY,
                Avatar.EyeType.DIZZY: py_avataaars.EyesType.DIZZY,
                Avatar.EyeType.EYE_ROLL: py_avataaars.EyesType.EYE_ROLL,
                Avatar.EyeType.HAPPY: py_avataaars.EyesType.HAPPY,
                Avatar.EyeType.HEARTS: py_avataaars.EyesType.HEARTS,
                Avatar.EyeType.SIDE: py_avataaars.EyesType.SIDE,
                Avatar.EyeType.SQUINT: py_avataaars.EyesType.SQUINT,
                Avatar.EyeType.SURPRISED: py_avataaars.EyesType.SURPRISED,
                Avatar.EyeType.WINK_01: py_avataaars.EyesType.WINK,
                Avatar.EyeType.WINK_02: py_avataaars.EyesType.WINK_WACKY,
            }[self.__eye_type],
            eyebrow_type={
                Avatar.EyebrowType.ANGRY: py_avataaars.EyebrowType.ANGRY,
                Avatar.EyebrowType.ANGRY_NATURAL: py_avataaars.EyebrowType.ANGRY_NATURAL,
                Avatar.EyebrowType.DEFAULT: py_avataaars.EyebrowType.DEFAULT,
                Avatar.EyebrowType.DEFAULT_NATURAL: py_avataaars.EyebrowType.DEFAULT_NATURAL,
                Avatar.EyebrowType.FLAT_NATURAL: py_avataaars.EyebrowType.FLAT_NATURAL,
                Avatar.EyebrowType.FROWN_NATURAL: py_avataaars.EyebrowType.FROWN_NATURAL,
                Avatar.EyebrowType.RAISED_EXCITED: py_avataaars.EyebrowType.RAISED_EXCITED,
                Avatar.EyebrowType.RAISED_EXCITED_NATURAL: py_avataaars.EyebrowType.RAISED_EXCITED_NATURAL,
                Avatar.EyebrowType.SAD_CONCERNED: py_avataaars.EyebrowType.SAD_CONCERNED,
                Avatar.EyebrowType.SAD_CONCERNED_NATURAL: py_avataaars.EyebrowType.SAD_CONCERNED_NATURAL,
                Avatar.EyebrowType.UNI_BROW_NATURAL: py_avataaars.EyebrowType.UNI_BROW_NATURAL,
                Avatar.EyebrowType.UP_DOWN: py_avataaars.EyebrowType.UP_DOWN,
                Avatar.EyebrowType.UP_DOWN_NATURAL: py_avataaars.EyebrowType.UP_DOWN_NATURAL,
            }[self.__eyebrow_type],
            nose_type=py_avataaars.NoseType.DEFAULT,
            accessories_type={
                Avatar.GlassesType.KURT_COBAIN: py_avataaars.AccessoriesType.KURT,
                Avatar.GlassesType.NONE: py_avataaars.AccessoriesType.DEFAULT,
                Avatar.GlassesType.PRESCRIPTION_BLACK: py_avataaars.AccessoriesType.PRESCRIPTION_02,
                Avatar.GlassesType.PRESCRIPTION_WHITE: py_avataaars.AccessoriesType.PRESCRIPTION_01,
                Avatar.GlassesType.ROUND: py_avataaars.AccessoriesType.ROUND,
                Avatar.GlassesType.SUNGLASSES: py_avataaars.AccessoriesType.ROUND,
                Avatar.GlassesType.WAYFARERS: py_avataaars.AccessoriesType.WAYFARERS,
            }[self.__glasses_type],
            clothe_type={
                Avatar.ClothingType.BLAZER_AND_SHIRT: py_avataaars.ClotheType.BLAZER_SHIRT,
                Avatar.ClothingType.BLAZER_AND_SWEATER: py_avataaars.ClotheType.BLAZER_SWEATER,
                Avatar.ClothingType.COLLAR_SWEATER: py_avataaars.ClotheType.COLLAR_SWEATER,
                Avatar.ClothingType.HOODIE: py_avataaars.ClotheType.HOODIE,
                Avatar.ClothingType.OVERALL: py_avataaars.ClotheType.OVERALL,
                Avatar.ClothingType.SHIRT_CREW_NECK: py_avataaars.ClotheType.SHIRT_CREW_NECK,
                Avatar.ClothingType.SHIRT_SCOOP_NECK: py_avataaars.ClotheType.SHIRT_SCOOP_NECK,
                Avatar.ClothingType.SHIRT_V_NECK: py_avataaars.ClotheType.SHIRT_V_NECK,
                Avatar.ClothingType.TSHIRT: py_avataaars.ClotheType.GRAPHIC_SHIRT,
            }[self.__clothing_type],
            clothe_graphic_type={
                Avatar.ShirtLogoType.BAT: py_avataaars.ClotheGraphicType.BAT,
                Avatar.ShirtLogoType.BEAR: py_avataaars.ClotheGraphicType.BEAR,
                Avatar.ShirtLogoType.CUMBIA: py_avataaars.ClotheGraphicType.CUMBIA,
                Avatar.ShirtLogoType.DEER: py_avataaars.ClotheGraphicType.DEER,
                Avatar.ShirtLogoType.DIAMOND: py_avataaars.ClotheGraphicType.DIAMOND,
                Avatar.ShirtLogoType.HOLA: py_avataaars.ClotheGraphicType.HOLA,
                Avatar.ShirtLogoType.PIZZA: py_avataaars.ClotheGraphicType.PIZZA,
                Avatar.ShirtLogoType.RESIST: py_avataaars.ClotheGraphicType.RESIST,
                Avatar.ShirtLogoType.SELENA: py_avataaars.ClotheGraphicType.SELENA,
                Avatar.ShirtLogoType.SKULL: py_avataaars.ClotheGraphicType.SKULL,
                Avatar.ShirtLogoType.SKULL_OUTLINE: py_avataaars.ClotheGraphicType.SKULL_OUTLINE,
            }[self.__shirt_logo_type],
        ).render_png()

    #
    # PUBLIC
    #
