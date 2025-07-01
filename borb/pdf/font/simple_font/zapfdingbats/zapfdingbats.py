#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the ZapfDingbats typeface and its properties.

The ZapfDingbats class encapsulates the metrics and characteristics of the
ZapfDingbats typeface, a widely used symbol font. This class is typically used
to render text in PDF documents where ZapfDingbats is required.

It provides access to font-specific properties such as width, height, and
character mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class ZapfDingbats(StandardType1Font):
    """
    Represents the ZapfDingbats typeface and its properties.

    The ZapfDingbats class encapsulates the metrics and characteristics of the
    ZapfDingbats typeface, a widely used symbol font. This class is typically used
    to render text in PDF documents where ZapfDingbats is required.

    It provides access to font-specific properties such as width, height, and
    character mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the ZapfDingbats font class.

        This constructor sets up the necessary internal mappings and data structures to enable the retrieval of
        character IDs (CIDs) for the ZapfDingbats font. The class provides functionality to map Unicode characters
        to their corresponding CIDs within this specialized symbol font.
        """
        super().__init__()
        self["Type"] = name("Font")
        self["Subtype"] = name("Type1")
        self["BaseFont"] = name("ZapfDingbats")
        self["Encoding"] = name("ZapfDingbats")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 278, 'scissorsupperblade': 793, 'scissorsblack': 794, 'scissorslowerblade': 816, 'scissorswhite': 823, 'telephoneblack': 789, 'telephonelocationsign': 841, 'tapedrive': 823, 'airplane': 833, 'envelope': 816, 'pointingindexrightblack': 831, 'pointingindexrightwhite': 923, 'hvictory': 744, 'hwriting': 723, 'pencillowerright': 749, 'pencil': 790, 'pencilupperright': 792, 'nibwhite': 695, 'nibblack': 776, 'check': 768, 'checkheavy': 792, 'multiplicationx': 759, 'multiplicationxheavy': 707, 'ballotx': 708, 'ballotxheavy': 682, 'greekcrossoutlined': 701, 'greekcrossheavy': 826, 'crosscentreopen': 815, 'crosscentreopenheavy': 789, 'latincross': 789, 'latincrossshadowedwhite': 707, 'latincrossoutlined': 687, 'maltesecross': 696, 'starofdavid': 689, 'asteriskteardropfour': 786, 'asteriskballoonfour': 787, 'asteriskballoonheavyfour': 713, 'asteriskclubfour': 791, 'starpointedblackfour': 785, 'starpointedwhitefour': 791, 'starblack': 873, 'staroutlinedstresswhite': 761, 'starcircledwhite': 762, 'starcentreopenblack': 759, 'starcentreblackwhite': 892, 'staroutlinedblack': 892, 'staroutlinedblackheavy': 788, 'starpinwheel': 784, 'starshadowedwhite': 0, 'asteriskheavy': 438, 'asteriskcentreopen': 138, 'spokedasteriskeight': 277, 'starpointedblackeight': 415, 'starpointedpinwheeleight': 509, 'starpointedblacksix': 410, 'compasstarpointedblackeight': 234, 'compasstarpointedblackheavyeight': 234, 'starpointedblacktwelve': 390, 'asteriskpointedsixteen': 390, 'asteriskteardrop': 276, 'asteriskteardropcentreopen': 276, 'asteriskteardropheavy': 317, 'florettepetalledblackwhitesix': 317, 'floretteblack': 334, 'florettewhite': 334, 'floretteoutlinedpetalledblackeight': 392, 'starcentreopenpointedcircledeight': 392, 'asteriskteardroppinwheelheavy': 668, 'snowflake': 668, 'snowflaketight': 732, 'chevronsnowflakeheavy': 544, 'sparkle': 544, 'sparkleheavy': 910, 'asteriskballoon': 911, 'asteriskteardroppropellereight': 667, 'asteriskteardroppropellerheavyeight': 760, 'circleblack': 760, 'circleshadowedwhite': 626, 'squareblack': 694, 'squareshadowlowerrightwhite': 595, 'squareshadowupperrightwhite': 776, 'squarelowerrightshadowedwhite': 0, 'squareupperrightshadowedwhite': 0, 'triangleupblack': 0, 'triangledownblack': 0, 'gmtr:diamondblack': 690, 'diamondminusxblackwhite': 791, 'halfcirclerightblack': 790, 'verticalbarlight': 788, 'verticalbarmedium': 788, 'verticalbarheavy': 788, 'commaheavyturnedornament': 788, 'commaheavyornament': 788, 'commaheavydoubleturnedornament': 788, 'commaheavydoubleornament': 788, 'curvedstemparagraphsignornament': 838, 'exclamationheavyornament': 924, 'heartexclamationheavyornament': 1016, 'heartblackheavy': 458, 'heartbulletrotatedblackheavy': 924, 'floralheart': 918, 'floralheartbulletrotated': 927, 'clubblack': 928, 'misc:diamondblack': 928, 'heartblack': 834, 'spadeblack': 873, 'onecircle': 828, 'twocircle': 924, 'threecircle': 917, 'fourcircle': 930, 'fivecircle': 931, 'sixcircle': 463, 'sevencircle': 883, 'eightcircle': 836, 'ninecircle': 867, 'tencircle': 696, 'onenegativecircled': 874, 'twonegativecircled': 760, 'threenegativecircled': 946, 'fournegativecircled': 865, 'fivenegativecircled': 967, 'sixnegativecircled': 831, 'sevennegativecircled': 873, 'eightnegativecircled': 927, 'ninenegativecircled': 970, 'tennegativecircled': 918, 'onesanscircled': 748, 'twosanscircled': 836, 'threesanscircled': 771, 'foursanscircled': 888, 'fivesanscircled': 748, 'sixsanscircled': 771, 'sevensanscircled': 888, 'eightsanscircled': 867, 'ninesanscircled': 696, 'tensanscircled': 874, 'onesansnegativecircled': 974, 'twosansnegativecircled': 762, 'threesansnegativecircled': 759, 'foursansnegativecircled': 509, 'fivesansnegativecircled': 410, 'sixsansnegativecircled': 0, 'sevensansnegativecircled': 0, 'eightsansnegativecircled': 0, 'ninesansnegativecircled': 0, 'tensansnegativecircled': 0, 'arrowrightwideheavy': 0, 'arrowright': 0, 'arrowleftright': 0, 'arrowupdown': 0, 'arrowheavySE': 0, 'arrowrightheavy': 0, 'arrowheavyNE': 0, 'arrowrightpointed': 0, 'arrowrightroundheavy': 0, 'arrowrighttriangle': 0, 'arrowrighttriangleheavy': 0, 'arrowrighttriangledashed': 0, 'arrowrighttriangledashedheavy': 0, 'arrowrightblack': 0, 'arrowheadrightthreeDtoplight': 0, 'arrowheadrightthreeDbottomlight': 0, 'arrowheadrightblack': 0, 'arrowrightcurvedownblackheavy': 0, 'arrowrightcurveupblackheavy': 0, 'arrowrightsquatblack': 0, 'arrowrightpointedblackheavy': 0, 'arrowrightrightshadedwhite': 0, 'arrowrightleftshadedwhite': 0, 'arrowrightbacktiltedshadowedwhite': 0, 'arrowrightfronttiltedshadowedwhite': 0, 'arrowshadowrightlowerwhiteheavy': 0, 'arrowshadowrightupperwhiteheavy': 0, 'arrowshadowrightnotchedlowerwhite': 0, 'arrowshadowrightnotchedupperwhite': 0, 'arrowrightcircledwhiteheavy': 0, 'arrowrightfeatheredwhite': 0, 'arrowfeatheredblackSE': 0, 'arrowrightfeatheredblack': 0, 'arrowfeatheredblackNE': 0, 'arrowfeatheredblackheavySE': 0, 'arrowrightfeatheredblackheavy': 0, 'arrowfeatheredblackheavyNE': 0, 'arrowteardropright': 0, 'arrowteardroprightheavy': 0, 'arrowrightwedge': 0, 'arrowrightwedgeheavy': 0, 'arrowrightoutlinedopen': 0} # type: ignore[annotation-unchecked]
        # fmt: on

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_width(
        self,
        text: str,
        character_spacing: float = 0,
        font_size: float = 12,
        word_spacing: float = 0,
    ) -> int:
        """
        Return the total width of a text string when rendered with the font at a specific size.

        This function calculates the width of the given text string when rendered with the font
        at the specified font size.

        :param font_size:           The font size to be used for rendering.
        :param text:                The text string to calculate the width for.
        :param word_spacing:        The word spacing to be used for rendering
        :param character_spacing:   The character spacing to be used for rendering
        :return:                    The width (in points) of the text in the specified font size.
        """
        if self.get("FontDescriptor", {}).get("Widths", None) is not None:
            return super().get_width(
                text=text,
                character_spacing=character_spacing,
                font_size=font_size,
                word_spacing=word_spacing,
            )

        # default
        if len(text) == 0:
            return 0
        character_names: typing.List[str] = [
            AdobeGlyphList.ADOBE_CHARACTER_TO_CHARACTER_NAME.get(c, ".notdef")
            for c in text
        ]

        character_width: typing.List[float] = [
            self.__character_name_to_width.get(x, 0) for x in character_names
        ]
        character_width = [w / 1000 for w in character_width]

        # apply character spacing
        character_width = [(w + character_spacing) for w in character_width]
        character_width[-1] -= character_spacing

        # apply word spacing
        character_width = [
            (w + word_spacing) if character_names[i] == "space" else w
            for i, w in enumerate(character_width)
        ]

        # apply font size
        import math

        return math.ceil(sum(character_width) * font_size)
