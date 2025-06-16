#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility class providing static methods for generating predefined shape objects for line art.

The `LineArt` class offers methods to create common shapes such as arrows, regular n-gons,
and other geometric figures. These shape objects are suitable for use in various drawing
or graphic applications and can be further customized or manipulated.
"""

import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.shape.shape import Shape


class LineArt:
    """
    Utility class providing static methods for generating predefined shape objects for line art.

    The `LineArt` class offers methods to create common shapes such as arrows, regular n-gons,
    and other geometric figures. These shape objects are suitable for use in various drawing
    or graphic applications and can be further customized or manipulated.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def arrow_down(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a downward arrow.

        This function creates and returns a Shape object that visually represents
        a downward-pointing arrow.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0, 38),
                (19, 38),
                (19, 100),
                (62, 100),
                (62, 38),
                (81, 38),
                (40.5, 0.0),
                (0, 38),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def arrow_left(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a leftward arrow.

        This function creates and returns a Shape object that visually represents
        a leftward-pointing arrow.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (38.0, 0.0),
                (38.0, -19.0),
                (100.0, -19.0),
                (100.0, -62.0),
                (38.0, -62.0),
                (38.0, -81.0),
                (0.0, -40.5),
                (38.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def arrow_right(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a rightward arrow.

        This function creates and returns a Shape object that visually represents
        a rightward-pointing arrow.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (-38.0, 0.0),
                (-38.0, 19.0),
                (-100.0, 19.0),
                (-100.0, 62.0),
                (-38.0, 62.0),
                (-38.0, 81.0),
                (0.0, 40.5),
                (-38.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def arrow_up(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an upward arrow.

        This function creates and returns a Shape object that visually represents
        an upward-pointing arrow.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, -38.0),
                (-19.0, -38.0),
                (-19.0, -100.0),
                (-62.0, -100.0),
                (-62.0, -38.0),
                (-81.0, -38.0),
                (-40.5, -0.0),
                (0.0, -38.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def blob(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an (ink) blob.

        This function creates and returns a Shape object that visually represents
        an (ink) blob.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        import math
        import random

        n = random.choice([3, 4, 4, 5])
        cs: typing.List[typing.Tuple[float, float]] = [
            (math.cos(math.radians(i)) * r, math.sin(math.radians(i)) * r)
            for i, r in zip(
                range(0, 360, 360 // n),
                [random.choice([50, 100, 100, 100, 150]) for _ in range(0, n)],
            )
        ]
        cs += [cs[0]]
        return (
            Shape(
                coordinates=cs,
                stroke_color=stroke_color,
                fill_color=fill_color,
                line_width=line_width,
                dash_pattern=dash_pattern,
                dash_phase=dash_phase,
            )
            .smooth()
            .scale_to_fit(size=(100, 100))
        )

    @staticmethod
    def circle(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a circle.

        This function creates and returns a Shape object that visually represents
        a circle.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (50.0, 0.0),
                (49.99238476, 0.87262032),
                (49.96954135, 1.74497484),
                (49.93147674, 2.61679781),
                (49.87820251, 3.48782369),
                (49.8097349, 4.35778714),
                (49.72609477, 5.22642316),
                (49.62730758, 6.09346717),
                (49.51340344, 6.95865505),
                (49.38441703, 7.82172325),
                (49.24038765, 8.68240888),
                (49.08135917, 9.54044977),
                (48.90738004, 10.39558454),
                (48.71850324, 11.24755272),
                (48.51478631, 12.09609478),
                (48.29629131, 12.94095226),
                (48.0630848, 13.78186779),
                (47.8152378, 14.61858524),
                (47.55282581, 15.45084972),
                (47.27592878, 16.27840772),
                (46.98463104, 17.10100717),
                (46.67902132, 17.91839748),
                (46.35919273, 18.73032967),
                (46.02524267, 19.53655642),
                (45.67727288, 20.33683215),
                (45.31538935, 21.13091309),
                (44.93970231, 21.91855734),
                (44.55032621, 22.69952499),
                (44.14737964, 23.47357814),
                (43.73098536, 24.24048101),
                (43.30127019, 25.0),
                (42.85836504, 25.75190375),
                (42.40240481, 26.49596321),
                (41.9335284, 27.23195175),
                (41.45187863, 27.95964517),
                (40.95760221, 28.67882182),
                (40.45084972, 29.38926261),
                (39.9317755, 30.09075116),
                (39.40053768, 30.78307377),
                (38.85729807, 31.46601955),
                (38.30222216, 32.13938048),
                (37.73547901, 32.80295145),
                (37.15724127, 33.45653032),
                (36.56768508, 34.099918),
                (35.96699002, 34.73291852),
                (35.35533906, 35.35533906),
                (34.73291852, 35.96699002),
                (34.099918, 36.56768508),
                (33.45653032, 37.15724127),
                (32.80295145, 37.73547901),
                (32.13938048, 38.30222216),
                (31.46601955, 38.85729807),
                (30.78307377, 39.40053768),
                (30.09075116, 39.9317755),
                (29.38926261, 40.45084972),
                (28.67882182, 40.95760221),
                (27.95964517, 41.45187863),
                (27.23195175, 41.9335284),
                (26.49596321, 42.40240481),
                (25.75190375, 42.85836504),
                (25.0, 43.30127019),
                (24.24048101, 43.73098536),
                (23.47357814, 44.14737964),
                (22.69952499, 44.55032621),
                (21.91855734, 44.93970231),
                (21.13091309, 45.31538935),
                (20.33683215, 45.67727288),
                (19.53655642, 46.02524267),
                (18.73032967, 46.35919273),
                (17.91839748, 46.67902132),
                (17.10100717, 46.98463104),
                (16.27840772, 47.27592878),
                (15.45084972, 47.55282581),
                (14.61858524, 47.8152378),
                (13.78186779, 48.0630848),
                (12.94095226, 48.29629131),
                (12.09609478, 48.51478631),
                (11.24755272, 48.71850324),
                (10.39558454, 48.90738004),
                (9.54044977, 49.08135917),
                (8.68240888, 49.24038765),
                (7.82172325, 49.38441703),
                (6.95865505, 49.51340344),
                (6.09346717, 49.62730758),
                (5.22642316, 49.72609477),
                (4.35778714, 49.8097349),
                (3.48782369, 49.87820251),
                (2.61679781, 49.93147674),
                (1.74497484, 49.96954135),
                (0.87262032, 49.99238476),
                (0.0, 50.0),
                (-0.87262032, 49.99238476),
                (-1.74497484, 49.96954135),
                (-2.61679781, 49.93147674),
                (-3.48782369, 49.87820251),
                (-4.35778714, 49.8097349),
                (-5.22642316, 49.72609477),
                (-6.09346717, 49.62730758),
                (-6.95865505, 49.51340344),
                (-7.82172325, 49.38441703),
                (-8.68240888, 49.24038765),
                (-9.54044977, 49.08135917),
                (-10.39558454, 48.90738004),
                (-11.24755272, 48.71850324),
                (-12.09609478, 48.51478631),
                (-12.94095226, 48.29629131),
                (-13.78186779, 48.0630848),
                (-14.61858524, 47.8152378),
                (-15.45084972, 47.55282581),
                (-16.27840772, 47.27592878),
                (-17.10100717, 46.98463104),
                (-17.91839748, 46.67902132),
                (-18.73032967, 46.35919273),
                (-19.53655642, 46.02524267),
                (-20.33683215, 45.67727288),
                (-21.13091309, 45.31538935),
                (-21.91855734, 44.93970231),
                (-22.69952499, 44.55032621),
                (-23.47357814, 44.14737964),
                (-24.24048101, 43.73098536),
                (-25.0, 43.30127019),
                (-25.75190375, 42.85836504),
                (-26.49596321, 42.40240481),
                (-27.23195175, 41.9335284),
                (-27.95964517, 41.45187863),
                (-28.67882182, 40.95760221),
                (-29.38926261, 40.45084972),
                (-30.09075116, 39.9317755),
                (-30.78307377, 39.40053768),
                (-31.46601955, 38.85729807),
                (-32.13938048, 38.30222216),
                (-32.80295145, 37.73547901),
                (-33.45653032, 37.15724127),
                (-34.099918, 36.56768508),
                (-34.73291852, 35.96699002),
                (-35.35533906, 35.35533906),
                (-35.96699002, 34.73291852),
                (-36.56768508, 34.099918),
                (-37.15724127, 33.45653032),
                (-37.73547901, 32.80295145),
                (-38.30222216, 32.13938048),
                (-38.85729807, 31.46601955),
                (-39.40053768, 30.78307377),
                (-39.9317755, 30.09075116),
                (-40.45084972, 29.38926261),
                (-40.95760221, 28.67882182),
                (-41.45187863, 27.95964517),
                (-41.9335284, 27.23195175),
                (-42.40240481, 26.49596321),
                (-42.85836504, 25.75190375),
                (-43.30127019, 25.0),
                (-43.73098536, 24.24048101),
                (-44.14737964, 23.47357814),
                (-44.55032621, 22.69952499),
                (-44.93970231, 21.91855734),
                (-45.31538935, 21.13091309),
                (-45.67727288, 20.33683215),
                (-46.02524267, 19.53655642),
                (-46.35919273, 18.73032967),
                (-46.67902132, 17.91839748),
                (-46.98463104, 17.10100717),
                (-47.27592878, 16.27840772),
                (-47.55282581, 15.45084972),
                (-47.8152378, 14.61858524),
                (-48.0630848, 13.78186779),
                (-48.29629131, 12.94095226),
                (-48.51478631, 12.09609478),
                (-48.71850324, 11.24755272),
                (-48.90738004, 10.39558454),
                (-49.08135917, 9.54044977),
                (-49.24038765, 8.68240888),
                (-49.38441703, 7.82172325),
                (-49.51340344, 6.95865505),
                (-49.62730758, 6.09346717),
                (-49.72609477, 5.22642316),
                (-49.8097349, 4.35778714),
                (-49.87820251, 3.48782369),
                (-49.93147674, 2.61679781),
                (-49.96954135, 1.74497484),
                (-49.99238476, 0.87262032),
                (-50.0, 0.0),
                (-49.99238476, -0.87262032),
                (-49.96954135, -1.74497484),
                (-49.93147674, -2.61679781),
                (-49.87820251, -3.48782369),
                (-49.8097349, -4.35778714),
                (-49.72609477, -5.22642316),
                (-49.62730758, -6.09346717),
                (-49.51340344, -6.95865505),
                (-49.38441703, -7.82172325),
                (-49.24038765, -8.68240888),
                (-49.08135917, -9.54044977),
                (-48.90738004, -10.39558454),
                (-48.71850324, -11.24755272),
                (-48.51478631, -12.09609478),
                (-48.29629131, -12.94095226),
                (-48.0630848, -13.78186779),
                (-47.8152378, -14.61858524),
                (-47.55282581, -15.45084972),
                (-47.27592878, -16.27840772),
                (-46.98463104, -17.10100717),
                (-46.67902132, -17.91839748),
                (-46.35919273, -18.73032967),
                (-46.02524267, -19.53655642),
                (-45.67727288, -20.33683215),
                (-45.31538935, -21.13091309),
                (-44.93970231, -21.91855734),
                (-44.55032621, -22.69952499),
                (-44.14737964, -23.47357814),
                (-43.73098536, -24.24048101),
                (-43.30127019, -25.0),
                (-42.85836504, -25.75190375),
                (-42.40240481, -26.49596321),
                (-41.9335284, -27.23195175),
                (-41.45187863, -27.95964517),
                (-40.95760221, -28.67882182),
                (-40.45084972, -29.38926261),
                (-39.9317755, -30.09075116),
                (-39.40053768, -30.78307377),
                (-38.85729807, -31.46601955),
                (-38.30222216, -32.13938048),
                (-37.73547901, -32.80295145),
                (-37.15724127, -33.45653032),
                (-36.56768508, -34.099918),
                (-35.96699002, -34.73291852),
                (-35.35533906, -35.35533906),
                (-34.73291852, -35.96699002),
                (-34.099918, -36.56768508),
                (-33.45653032, -37.15724127),
                (-32.80295145, -37.73547901),
                (-32.13938048, -38.30222216),
                (-31.46601955, -38.85729807),
                (-30.78307377, -39.40053768),
                (-30.09075116, -39.9317755),
                (-29.38926261, -40.45084972),
                (-28.67882182, -40.95760221),
                (-27.95964517, -41.45187863),
                (-27.23195175, -41.9335284),
                (-26.49596321, -42.40240481),
                (-25.75190375, -42.85836504),
                (-25.0, -43.30127019),
                (-24.24048101, -43.73098536),
                (-23.47357814, -44.14737964),
                (-22.69952499, -44.55032621),
                (-21.91855734, -44.93970231),
                (-21.13091309, -45.31538935),
                (-20.33683215, -45.67727288),
                (-19.53655642, -46.02524267),
                (-18.73032967, -46.35919273),
                (-17.91839748, -46.67902132),
                (-17.10100717, -46.98463104),
                (-16.27840772, -47.27592878),
                (-15.45084972, -47.55282581),
                (-14.61858524, -47.8152378),
                (-13.78186779, -48.0630848),
                (-12.94095226, -48.29629131),
                (-12.09609478, -48.51478631),
                (-11.24755272, -48.71850324),
                (-10.39558454, -48.90738004),
                (-9.54044977, -49.08135917),
                (-8.68240888, -49.24038765),
                (-7.82172325, -49.38441703),
                (-6.95865505, -49.51340344),
                (-6.09346717, -49.62730758),
                (-5.22642316, -49.72609477),
                (-4.35778714, -49.8097349),
                (-3.48782369, -49.87820251),
                (-2.61679781, -49.93147674),
                (-1.74497484, -49.96954135),
                (-0.87262032, -49.99238476),
                (-0.0, -50.0),
                (0.87262032, -49.99238476),
                (1.74497484, -49.96954135),
                (2.61679781, -49.93147674),
                (3.48782369, -49.87820251),
                (4.35778714, -49.8097349),
                (5.22642316, -49.72609477),
                (6.09346717, -49.62730758),
                (6.95865505, -49.51340344),
                (7.82172325, -49.38441703),
                (8.68240888, -49.24038765),
                (9.54044977, -49.08135917),
                (10.39558454, -48.90738004),
                (11.24755272, -48.71850324),
                (12.09609478, -48.51478631),
                (12.94095226, -48.29629131),
                (13.78186779, -48.0630848),
                (14.61858524, -47.8152378),
                (15.45084972, -47.55282581),
                (16.27840772, -47.27592878),
                (17.10100717, -46.98463104),
                (17.91839748, -46.67902132),
                (18.73032967, -46.35919273),
                (19.53655642, -46.02524267),
                (20.33683215, -45.67727288),
                (21.13091309, -45.31538935),
                (21.91855734, -44.93970231),
                (22.69952499, -44.55032621),
                (23.47357814, -44.14737964),
                (24.24048101, -43.73098536),
                (25.0, -43.30127019),
                (25.75190375, -42.85836504),
                (26.49596321, -42.40240481),
                (27.23195175, -41.9335284),
                (27.95964517, -41.45187863),
                (28.67882182, -40.95760221),
                (29.38926261, -40.45084972),
                (30.09075116, -39.9317755),
                (30.78307377, -39.40053768),
                (31.46601955, -38.85729807),
                (32.13938048, -38.30222216),
                (32.80295145, -37.73547901),
                (33.45653032, -37.15724127),
                (34.099918, -36.56768508),
                (34.73291852, -35.96699002),
                (35.35533906, -35.35533906),
                (35.96699002, -34.73291852),
                (36.56768508, -34.099918),
                (37.15724127, -33.45653032),
                (37.73547901, -32.80295145),
                (38.30222216, -32.13938048),
                (38.85729807, -31.46601955),
                (39.40053768, -30.78307377),
                (39.9317755, -30.09075116),
                (40.45084972, -29.38926261),
                (40.95760221, -28.67882182),
                (41.45187863, -27.95964517),
                (41.9335284, -27.23195175),
                (42.40240481, -26.49596321),
                (42.85836504, -25.75190375),
                (43.30127019, -25.0),
                (43.73098536, -24.24048101),
                (44.14737964, -23.47357814),
                (44.55032621, -22.69952499),
                (44.93970231, -21.91855734),
                (45.31538935, -21.13091309),
                (45.67727288, -20.33683215),
                (46.02524267, -19.53655642),
                (46.35919273, -18.73032967),
                (46.67902132, -17.91839748),
                (46.98463104, -17.10100717),
                (47.27592878, -16.27840772),
                (47.55282581, -15.45084972),
                (47.8152378, -14.61858524),
                (48.0630848, -13.78186779),
                (48.29629131, -12.94095226),
                (48.51478631, -12.09609478),
                (48.71850324, -11.24755272),
                (48.90738004, -10.39558454),
                (49.08135917, -9.54044977),
                (49.24038765, -8.68240888),
                (49.38441703, -7.82172325),
                (49.51340344, -6.95865505),
                (49.62730758, -6.09346717),
                (49.72609477, -5.22642316),
                (49.8097349, -4.35778714),
                (49.87820251, -3.48782369),
                (49.93147674, -2.61679781),
                (49.96954135, -1.74497484),
                (49.99238476, -0.87262032),
                (49.99238476, -0.87262032),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def cross(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a cross.

        This function creates and returns a Shape object that visually represents
        a cross.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 33.33333333),
                (0.0, 66.66666667),
                (33.33333333, 66.66666667),
                (33.33333333, 100.0),
                (66.66666667, 100.0),
                (66.66666667, 66.66666667),
                (100.0, 66.66666667),
                (100.0, 33.33333333),
                (66.66666667, 33.33333333),
                (66.66666667, 0.0),
                (33.33333333, 0.0),
                (33.33333333, 33.33333333),
                (0.0, 33.33333333),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def dragon_curve(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        number_of_iterations: int = 5,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a Heighway dragon curve.

        This function creates and returns a Shape object that visually represents
        a Heighway dragon (also known as the Harter–Heighway dragon, or the Jurassic Park dragon)

        :param number_of_iterations:    the number of iterations used to draw the curve (default 5)
        :param stroke_color:            the color in which to draw the Shape
        :param fill_color:              the color in which to fill the Shape
        :param line_width:              the line width of the Shape
        :param dash_pattern:            the dash pattern to be used when drawing the Shape
        :param dash_phase:              the dash phase to be used when starting to draw the Shape
        :return:                        a Shape
        """
        seq: typing.List[int] = [1]
        for _ in range(0, number_of_iterations):
            seq.append(1)
            m: int = int(len(seq) / 2) - 1
            for i, v in enumerate(seq[0:-1]):
                if i == m:
                    seq.append(1 - v)
                else:
                    seq.append(v)
        step_size: int = 10
        direction: int = 0
        x: int = 0
        y: int = 0
        points: typing.List[typing.Tuple[float, float]] = []
        for turn in seq:

            # go forward
            if direction == 0:
                y += step_size
            elif direction == 1:
                x += step_size
            elif direction == 2:
                y -= step_size
            elif direction == 3:
                x -= step_size

            # store point
            points.append((x, y))

            # make turn
            if turn == 0:
                direction = (direction + 1) % 4
            elif turn == 1:
                direction = (direction + 3) % 4

        return Shape(
            coordinates=points,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def five_pointed_star(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a five-pointed star.

        This function creates and returns a Shape object that visually represents
        a five-pointed star.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_pointed_star(
            number_of_points=5,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def flowchart_card(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an card vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a card vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (25.0, 100.0),
                (100.0, 100.0),
                (75.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_collate(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a collate vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a collate vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (100.0, 100.0),
                (0.0, 100.0),
                (100.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_data(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an data vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a data vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (25.0, 100.0),
                (100.0, 100.0),
                (75.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_database(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a database vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a database vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (100.0, 83.33333333),
                (99.99238476, 83.04245989),
                (99.96954135, 82.75167505),
                (99.93147674, 82.4610674),
                (99.87820251, 82.17072544),
                (99.8097349, 81.88073762),
                (99.72609477, 81.59119228),
                (99.62730758, 81.30217761),
                (99.51340344, 81.01378165),
                (99.38441703, 80.72609225),
                (99.24038765, 80.43919704),
                (99.08135917, 80.15318341),
                (98.90738004, 79.86813849),
                (98.71850324, 79.58414909),
                (98.51478631, 79.30130174),
                (98.29629131, 79.01968258),
                (98.0630848, 78.7393774),
                (97.8152378, 78.46047159),
                (97.55282581, 78.18305009),
                (97.27592878, 77.90719743),
                (96.98463104, 77.63299761),
                (96.67902132, 77.36053417),
                (96.35919273, 77.08989011),
                (96.02524267, 76.82114786),
                (95.67727288, 76.55438928),
                (95.31538935, 76.28969564),
                (94.93970231, 76.02714755),
                (94.55032621, 75.766825),
                (94.14737964, 75.50880729),
                (93.73098536, 75.253173),
                (93.30127019, 75.0),
                (92.85836504, 74.74936542),
                (92.40240481, 74.5013456),
                (91.9335284, 74.25601608),
                (91.45187863, 74.01345161),
                (90.95760221, 73.77372606),
                (90.45084972, 73.53691246),
                (89.9317755, 73.30308295),
                (89.40053768, 73.07230874),
                (88.85729807, 72.84466015),
                (88.30222216, 72.62020651),
                (87.73547901, 72.39901618),
                (87.15724127, 72.18115656),
                (86.56768508, 71.966694),
                (85.96699002, 71.75569383),
                (85.35533906, 71.54822031),
                (84.73291852, 71.34433666),
                (84.099918, 71.14410497),
                (83.45653032, 70.94758624),
                (82.80295145, 70.75484033),
                (82.13938048, 70.56592595),
                (81.46601955, 70.38090064),
                (80.78307377, 70.19982077),
                (80.09075116, 70.0227415),
                (79.38926261, 69.84971676),
                (78.67882182, 69.68079926),
                (77.95964517, 69.51604046),
                (77.23195175, 69.35549053),
                (76.49596321, 69.1991984),
                (75.75190375, 69.04721165),
                (75.0, 68.8995766),
                (74.24048101, 68.75633821),
                (73.47357814, 68.61754012),
                (72.69952499, 68.4832246),
                (71.91855734, 68.35343256),
                (71.13091309, 68.22820355),
                (70.33683215, 68.10757571),
                (69.53655642, 67.99158578),
                (68.73032967, 67.88026909),
                (67.91839748, 67.77365956),
                (67.10100717, 67.67178965),
                (66.27840772, 67.57469041),
                (65.45084972, 67.4823914),
                (64.61858524, 67.39492073),
                (63.78186779, 67.31230507),
                (62.94095226, 67.23456956),
                (62.09609478, 67.1617379),
                (61.24755272, 67.09383225),
                (60.39558454, 67.03087332),
                (59.54044977, 66.97288028),
                (58.68240888, 66.91987078),
                (57.82172325, 66.87186099),
                (56.95865505, 66.82886552),
                (56.09346717, 66.79089747),
                (55.22642316, 66.75796841),
                (54.35778714, 66.73008837),
                (53.48782369, 66.70726583),
                (52.61679781, 66.68950775),
                (51.74497484, 66.67681955),
                (50.87262032, 66.66920508),
                (50.0, 66.66666667),
                (49.12737968, 66.66920508),
                (48.25502516, 66.67681955),
                (47.38320219, 66.68950775),
                (46.51217631, 66.70726583),
                (45.64221286, 66.73008837),
                (44.77357684, 66.75796841),
                (43.90653283, 66.79089747),
                (43.04134495, 66.82886552),
                (42.17827675, 66.87186099),
                (41.31759112, 66.91987078),
                (40.45955023, 66.97288028),
                (39.60441546, 67.03087332),
                (38.75244728, 67.09383225),
                (37.90390522, 67.1617379),
                (37.05904774, 67.23456956),
                (36.21813221, 67.31230507),
                (35.38141476, 67.39492073),
                (34.54915028, 67.4823914),
                (33.72159228, 67.57469041),
                (32.89899283, 67.67178965),
                (32.08160252, 67.77365956),
                (31.26967033, 67.88026909),
                (30.46344358, 67.99158578),
                (29.66316785, 68.10757571),
                (28.86908691, 68.22820355),
                (28.08144266, 68.35343256),
                (27.30047501, 68.4832246),
                (26.52642186, 68.61754012),
                (25.75951899, 68.75633821),
                (25.0, 68.8995766),
                (24.24809625, 69.04721165),
                (23.50403679, 69.1991984),
                (22.76804825, 69.35549053),
                (22.04035483, 69.51604046),
                (21.32117818, 69.68079926),
                (20.61073739, 69.84971676),
                (19.90924884, 70.0227415),
                (19.21692623, 70.19982077),
                (18.53398045, 70.38090064),
                (17.86061952, 70.56592595),
                (17.19704855, 70.75484033),
                (16.54346968, 70.94758624),
                (15.900082, 71.14410497),
                (15.26708148, 71.34433666),
                (14.64466094, 71.54822031),
                (14.03300998, 71.75569383),
                (13.43231492, 71.966694),
                (12.84275873, 72.18115656),
                (12.26452099, 72.39901618),
                (11.69777784, 72.62020651),
                (11.14270193, 72.84466015),
                (10.59946232, 73.07230874),
                (10.0682245, 73.30308295),
                (9.54915028, 73.53691246),
                (9.04239779, 73.77372606),
                (8.54812137, 74.01345161),
                (8.0664716, 74.25601608),
                (7.59759519, 74.5013456),
                (7.14163496, 74.74936542),
                (6.69872981, 75.0),
                (6.26901464, 75.253173),
                (5.85262036, 75.50880729),
                (5.44967379, 75.766825),
                (5.06029769, 76.02714755),
                (4.68461065, 76.28969564),
                (4.32272712, 76.55438928),
                (3.97475733, 76.82114786),
                (3.64080727, 77.08989011),
                (3.32097868, 77.36053417),
                (3.01536896, 77.63299761),
                (2.72407122, 77.90719743),
                (2.44717419, 78.18305009),
                (2.1847622, 78.46047159),
                (1.9369152, 78.7393774),
                (1.70370869, 79.01968258),
                (1.48521369, 79.30130174),
                (1.28149676, 79.58414909),
                (1.09261996, 79.86813849),
                (0.91864083, 80.15318341),
                (0.75961235, 80.43919704),
                (0.61558297, 80.72609225),
                (0.48659656, 81.01378165),
                (0.37269242, 81.30217761),
                (0.27390523, 81.59119228),
                (0.1902651, 81.88073762),
                (0.12179749, 82.17072544),
                (0.06852326, 82.4610674),
                (0.03045865, 82.75167505),
                (0.00761524, 83.04245989),
                (0.0, 83.33333333),
                (0.00761524, 83.62420677),
                (0.03045865, 83.91499161),
                (0.06852326, 84.20559927),
                (0.12179749, 84.49594123),
                (0.1902651, 84.78592905),
                (0.27390523, 85.07547439),
                (0.37269242, 85.36448906),
                (0.48659656, 85.65288502),
                (0.61558297, 85.94057442),
                (0.75961235, 86.22746963),
                (0.91864083, 86.51348326),
                (1.09261996, 86.79852818),
                (1.28149676, 87.08251757),
                (1.48521369, 87.36536493),
                (1.70370869, 87.64698409),
                (1.9369152, 87.92728926),
                (2.1847622, 88.20619508),
                (2.44717419, 88.48361657),
                (2.72407122, 88.75946924),
                (3.01536896, 89.03366906),
                (3.32097868, 89.30613249),
                (3.64080727, 89.57677656),
                (3.97475733, 89.84551881),
                (4.32272712, 90.11227738),
                (4.68461065, 90.37697103),
                (5.06029769, 90.63951911),
                (5.44967379, 90.89984166),
                (5.85262036, 91.15785938),
                (6.26901464, 91.41349367),
                (6.69872981, 91.66666667),
                (7.14163496, 91.91730125),
                (7.59759519, 92.16532107),
                (8.0664716, 92.41065058),
                (8.54812137, 92.65321506),
                (9.04239779, 92.89294061),
                (9.54915028, 93.1297542),
                (10.0682245, 93.36358372),
                (10.59946232, 93.59435792),
                (11.14270193, 93.82200652),
                (11.69777784, 94.04646016),
                (12.26452099, 94.26765048),
                (12.84275873, 94.48551011),
                (13.43231492, 94.69997267),
                (14.03300998, 94.91097284),
                (14.64466094, 95.11844635),
                (15.26708148, 95.32233001),
                (15.900082, 95.52256169),
                (16.54346968, 95.71908042),
                (17.19704855, 95.91182634),
                (17.86061952, 96.10074072),
                (18.53398045, 96.28576602),
                (19.21692623, 96.46684589),
                (19.90924884, 96.64392517),
                (20.61073739, 96.81694991),
                (21.32117818, 96.9858674),
                (22.04035483, 97.15062621),
                (22.76804825, 97.31117613),
                (23.50403679, 97.46746827),
                (24.24809625, 97.61945501),
                (25.0, 97.76709006),
                (25.75951899, 97.91032845),
                (26.52642186, 98.04912655),
                (27.30047501, 98.18344207),
                (28.08144266, 98.3132341),
                (28.86908691, 98.43846312),
                (29.66316785, 98.55909096),
                (30.46344358, 98.67508089),
                (31.26967033, 98.78639758),
                (32.08160252, 98.89300711),
                (32.89899283, 98.99487701),
                (33.72159228, 99.09197626),
                (34.54915028, 99.18427527),
                (35.38141476, 99.27174593),
                (36.21813221, 99.3543616),
                (37.05904774, 99.4320971),
                (37.90390522, 99.50492877),
                (38.75244728, 99.57283441),
                (39.60441546, 99.63579335),
                (40.45955023, 99.69378639),
                (41.31759112, 99.74679588),
                (42.17827675, 99.79480568),
                (43.04134495, 99.83780115),
                (43.90653283, 99.87576919),
                (44.77357684, 99.90869826),
                (45.64221286, 99.9365783),
                (46.51217631, 99.95940084),
                (47.38320219, 99.97715891),
                (48.25502516, 99.98984712),
                (49.12737968, 99.99746159),
                (50.0, 100.0),
                (50.87262032, 99.99746159),
                (51.74497484, 99.98984712),
                (52.61679781, 99.97715891),
                (53.48782369, 99.95940084),
                (54.35778714, 99.9365783),
                (55.22642316, 99.90869826),
                (56.09346717, 99.87576919),
                (56.95865505, 99.83780115),
                (57.82172325, 99.79480568),
                (58.68240888, 99.74679588),
                (59.54044977, 99.69378639),
                (60.39558454, 99.63579335),
                (61.24755272, 99.57283441),
                (62.09609478, 99.50492877),
                (62.94095226, 99.4320971),
                (63.78186779, 99.3543616),
                (64.61858524, 99.27174593),
                (65.45084972, 99.18427527),
                (66.27840772, 99.09197626),
                (67.10100717, 98.99487701),
                (67.91839748, 98.89300711),
                (68.73032967, 98.78639758),
                (69.53655642, 98.67508089),
                (70.33683215, 98.55909096),
                (71.13091309, 98.43846312),
                (71.91855734, 98.3132341),
                (72.69952499, 98.18344207),
                (73.47357814, 98.04912655),
                (74.24048101, 97.91032845),
                (75.0, 97.76709006),
                (75.75190375, 97.61945501),
                (76.49596321, 97.46746827),
                (77.23195175, 97.31117613),
                (77.95964517, 97.15062621),
                (78.67882182, 96.9858674),
                (79.38926261, 96.81694991),
                (80.09075116, 96.64392517),
                (80.78307377, 96.46684589),
                (81.46601955, 96.28576602),
                (82.13938048, 96.10074072),
                (82.80295145, 95.91182634),
                (83.45653032, 95.71908042),
                (84.099918, 95.52256169),
                (84.73291852, 95.32233001),
                (85.35533906, 95.11844635),
                (85.96699002, 94.91097284),
                (86.56768508, 94.69997267),
                (87.15724127, 94.48551011),
                (87.73547901, 94.26765048),
                (88.30222216, 94.04646016),
                (88.85729807, 93.82200652),
                (89.40053768, 93.59435792),
                (89.9317755, 93.36358372),
                (90.45084972, 93.1297542),
                (90.95760221, 92.89294061),
                (91.45187863, 92.65321506),
                (91.9335284, 92.41065058),
                (92.40240481, 92.16532107),
                (92.85836504, 91.91730125),
                (93.30127019, 91.66666667),
                (93.73098536, 91.41349367),
                (94.14737964, 91.15785938),
                (94.55032621, 90.89984166),
                (94.93970231, 90.63951911),
                (95.31538935, 90.37697103),
                (95.67727288, 90.11227738),
                (96.02524267, 89.84551881),
                (96.35919273, 89.57677656),
                (96.67902132, 89.30613249),
                (96.98463104, 89.03366906),
                (97.27592878, 88.75946924),
                (97.55282581, 88.48361657),
                (97.8152378, 88.20619508),
                (98.0630848, 87.92728926),
                (98.29629131, 87.64698409),
                (98.51478631, 87.36536493),
                (98.71850324, 87.08251757),
                (98.90738004, 86.79852818),
                (99.08135917, 86.51348326),
                (99.24038765, 86.22746963),
                (99.38441703, 85.94057442),
                (99.51340344, 85.65288502),
                (99.62730758, 85.36448906),
                (99.72609477, 85.07547439),
                (99.8097349, 84.78592905),
                (99.87820251, 84.49594123),
                (99.93147674, 84.20559927),
                (99.96954135, 83.91499161),
                (99.99238476, 83.62420677),
                (100.0, 83.33333333),
                (99.99238476, 83.04245989),
                (99.96954135, 82.75167505),
                (99.93147674, 82.4610674),
                (99.87820251, 82.17072544),
                (99.8097349, 81.88073762),
                (99.72609477, 81.59119228),
                (99.62730758, 81.30217761),
                (99.51340344, 81.01378165),
                (99.38441703, 80.72609225),
                (99.24038765, 80.43919704),
                (99.08135917, 80.15318341),
                (98.90738004, 79.86813849),
                (98.71850324, 79.58414909),
                (98.51478631, 79.30130174),
                (98.29629131, 79.01968258),
                (98.0630848, 78.7393774),
                (97.8152378, 78.46047159),
                (97.55282581, 78.18305009),
                (97.27592878, 77.90719743),
                (96.98463104, 77.63299761),
                (96.67902132, 77.36053417),
                (96.35919273, 77.08989011),
                (96.02524267, 76.82114786),
                (95.67727288, 76.55438928),
                (95.31538935, 76.28969564),
                (94.93970231, 76.02714755),
                (94.55032621, 75.766825),
                (94.14737964, 75.50880729),
                (93.73098536, 75.253173),
                (93.30127019, 75.0),
                (92.85836504, 74.74936542),
                (92.40240481, 74.5013456),
                (91.9335284, 74.25601608),
                (91.45187863, 74.01345161),
                (90.95760221, 73.77372606),
                (90.45084972, 73.53691246),
                (89.9317755, 73.30308295),
                (89.40053768, 73.07230874),
                (88.85729807, 72.84466015),
                (88.30222216, 72.62020651),
                (87.73547901, 72.39901618),
                (87.15724127, 72.18115656),
                (86.56768508, 71.966694),
                (85.96699002, 71.75569383),
                (85.35533906, 71.54822031),
                (84.73291852, 71.34433666),
                (84.099918, 71.14410497),
                (83.45653032, 70.94758624),
                (82.80295145, 70.75484033),
                (82.13938048, 70.56592595),
                (81.46601955, 70.38090064),
                (80.78307377, 70.19982077),
                (80.09075116, 70.0227415),
                (79.38926261, 69.84971676),
                (78.67882182, 69.68079926),
                (77.95964517, 69.51604046),
                (77.23195175, 69.35549053),
                (76.49596321, 69.1991984),
                (75.75190375, 69.04721165),
                (75.0, 68.8995766),
                (74.24048101, 68.75633821),
                (73.47357814, 68.61754012),
                (72.69952499, 68.4832246),
                (71.91855734, 68.35343256),
                (71.13091309, 68.22820355),
                (70.33683215, 68.10757571),
                (69.53655642, 67.99158578),
                (68.73032967, 67.88026909),
                (67.91839748, 67.77365956),
                (67.10100717, 67.67178965),
                (66.27840772, 67.57469041),
                (65.45084972, 67.4823914),
                (64.61858524, 67.39492073),
                (63.78186779, 67.31230507),
                (62.94095226, 67.23456956),
                (62.09609478, 67.1617379),
                (61.24755272, 67.09383225),
                (60.39558454, 67.03087332),
                (59.54044977, 66.97288028),
                (58.68240888, 66.91987078),
                (57.82172325, 66.87186099),
                (56.95865505, 66.82886552),
                (56.09346717, 66.79089747),
                (55.22642316, 66.75796841),
                (54.35778714, 66.73008837),
                (53.48782369, 66.70726583),
                (52.61679781, 66.68950775),
                (51.74497484, 66.67681955),
                (50.87262032, 66.66920508),
                (50.0, 66.66666667),
                (49.12737968, 66.66920508),
                (48.25502516, 66.67681955),
                (47.38320219, 66.68950775),
                (46.51217631, 66.70726583),
                (45.64221286, 66.73008837),
                (44.77357684, 66.75796841),
                (43.90653283, 66.79089747),
                (43.04134495, 66.82886552),
                (42.17827675, 66.87186099),
                (41.31759112, 66.91987078),
                (40.45955023, 66.97288028),
                (39.60441546, 67.03087332),
                (38.75244728, 67.09383225),
                (37.90390522, 67.1617379),
                (37.05904774, 67.23456956),
                (36.21813221, 67.31230507),
                (35.38141476, 67.39492073),
                (34.54915028, 67.4823914),
                (33.72159228, 67.57469041),
                (32.89899283, 67.67178965),
                (32.08160252, 67.77365956),
                (31.26967033, 67.88026909),
                (30.46344358, 67.99158578),
                (29.66316785, 68.10757571),
                (28.86908691, 68.22820355),
                (28.08144266, 68.35343256),
                (27.30047501, 68.4832246),
                (26.52642186, 68.61754012),
                (25.75951899, 68.75633821),
                (25.0, 68.8995766),
                (24.24809625, 69.04721165),
                (23.50403679, 69.1991984),
                (22.76804825, 69.35549053),
                (22.04035483, 69.51604046),
                (21.32117818, 69.68079926),
                (20.61073739, 69.84971676),
                (19.90924884, 70.0227415),
                (19.21692623, 70.19982077),
                (18.53398045, 70.38090064),
                (17.86061952, 70.56592595),
                (17.19704855, 70.75484033),
                (16.54346968, 70.94758624),
                (15.900082, 71.14410497),
                (15.26708148, 71.34433666),
                (14.64466094, 71.54822031),
                (14.03300998, 71.75569383),
                (13.43231492, 71.966694),
                (12.84275873, 72.18115656),
                (12.26452099, 72.39901618),
                (11.69777784, 72.62020651),
                (11.14270193, 72.84466015),
                (10.59946232, 73.07230874),
                (10.0682245, 73.30308295),
                (9.54915028, 73.53691246),
                (9.04239779, 73.77372606),
                (8.54812137, 74.01345161),
                (8.0664716, 74.25601608),
                (7.59759519, 74.5013456),
                (7.14163496, 74.74936542),
                (6.69872981, 75.0),
                (6.26901464, 75.253173),
                (5.85262036, 75.50880729),
                (5.44967379, 75.766825),
                (5.06029769, 76.02714755),
                (4.68461065, 76.28969564),
                (4.32272712, 76.55438928),
                (3.97475733, 76.82114786),
                (3.64080727, 77.08989011),
                (3.32097868, 77.36053417),
                (3.01536896, 77.63299761),
                (2.72407122, 77.90719743),
                (2.44717419, 78.18305009),
                (2.1847622, 78.46047159),
                (1.9369152, 78.7393774),
                (1.70370869, 79.01968258),
                (1.48521369, 79.30130174),
                (1.28149676, 79.58414909),
                (1.09261996, 79.86813849),
                (0.91864083, 80.15318341),
                (0.75961235, 80.43919704),
                (0.61558297, 80.72609225),
                (0.48659656, 81.01378165),
                (0.37269242, 81.30217761),
                (0.27390523, 81.59119228),
                (0.1902651, 81.88073762),
                (0.12179749, 82.17072544),
                (0.06852326, 82.4610674),
                (0.03045865, 82.75167505),
                (0.00761524, 83.04245989),
                (0.00761524, 16.37579323),
                (0.03045865, 16.08500839),
                (0.06852326, 15.79440073),
                (0.12179749, 15.50405877),
                (0.1902651, 15.21407095),
                (0.27390523, 14.92452561),
                (0.37269242, 14.63551094),
                (0.48659656, 14.34711498),
                (0.61558297, 14.05942558),
                (0.75961235, 13.77253037),
                (0.91864083, 13.48651674),
                (1.09261996, 13.20147182),
                (1.28149676, 12.91748243),
                (1.48521369, 12.63463507),
                (1.70370869, 12.35301591),
                (1.9369152, 12.07271074),
                (2.1847622, 11.79380492),
                (2.44717419, 11.51638343),
                (2.72407122, 11.24053076),
                (3.01536896, 10.96633094),
                (3.32097868, 10.69386751),
                (3.64080727, 10.42322344),
                (3.97475733, 10.15448119),
                (4.32272712, 9.88772262),
                (4.68461065, 9.62302897),
                (5.06029769, 9.36048089),
                (5.44967379, 9.10015834),
                (5.85262036, 8.84214062),
                (6.26901464, 8.58650633),
                (6.69872981, 8.33333333),
                (7.14163496, 8.08269875),
                (7.59759519, 7.83467893),
                (8.0664716, 7.58934942),
                (8.54812137, 7.34678494),
                (9.04239779, 7.10705939),
                (9.54915028, 6.8702458),
                (10.0682245, 6.63641628),
                (10.59946232, 6.40564208),
                (11.14270193, 6.17799348),
                (11.69777784, 5.95353984),
                (12.26452099, 5.73234952),
                (12.84275873, 5.51448989),
                (13.43231492, 5.30002733),
                (14.03300998, 5.08902716),
                (14.64466094, 4.88155365),
                (15.26708148, 4.67766999),
                (15.900082, 4.47743831),
                (16.54346968, 4.28091958),
                (17.19704855, 4.08817366),
                (17.86061952, 3.89925928),
                (18.53398045, 3.71423398),
                (19.21692623, 3.53315411),
                (19.90924884, 3.35607483),
                (20.61073739, 3.18305009),
                (21.32117818, 3.0141326),
                (22.04035483, 2.84937379),
                (22.76804825, 2.68882387),
                (23.50403679, 2.53253173),
                (24.24809625, 2.38054499),
                (25.0, 2.23290994),
                (25.75951899, 2.08967155),
                (26.52642186, 1.95087345),
                (27.30047501, 1.81655793),
                (28.08144266, 1.6867659),
                (28.86908691, 1.56153688),
                (29.66316785, 1.44090904),
                (30.46344358, 1.32491911),
                (31.26967033, 1.21360242),
                (32.08160252, 1.10699289),
                (32.89899283, 1.00512299),
                (33.72159228, 0.90802374),
                (34.54915028, 0.81572473),
                (35.38141476, 0.72825407),
                (36.21813221, 0.6456384),
                (37.05904774, 0.5679029),
                (37.90390522, 0.49507123),
                (38.75244728, 0.42716559),
                (39.60441546, 0.36420665),
                (40.45955023, 0.30621361),
                (41.31759112, 0.25320412),
                (42.17827675, 0.20519432),
                (43.04134495, 0.16219885),
                (43.90653283, 0.12423081),
                (44.77357684, 0.09130174),
                (45.64221286, 0.0634217),
                (46.51217631, 0.04059916),
                (47.38320219, 0.02284109),
                (48.25502516, 0.01015288),
                (49.12737968, 0.00253841),
                (50.0, 0.0),
                (50.87262032, 0.00253841),
                (51.74497484, 0.01015288),
                (52.61679781, 0.02284109),
                (53.48782369, 0.04059916),
                (54.35778714, 0.0634217),
                (55.22642316, 0.09130174),
                (56.09346717, 0.12423081),
                (56.95865505, 0.16219885),
                (57.82172325, 0.20519432),
                (58.68240888, 0.25320412),
                (59.54044977, 0.30621361),
                (60.39558454, 0.36420665),
                (61.24755272, 0.42716559),
                (62.09609478, 0.49507123),
                (62.94095226, 0.5679029),
                (63.78186779, 0.6456384),
                (64.61858524, 0.72825407),
                (65.45084972, 0.81572473),
                (66.27840772, 0.90802374),
                (67.10100717, 1.00512299),
                (67.91839748, 1.10699289),
                (68.73032967, 1.21360242),
                (69.53655642, 1.32491911),
                (70.33683215, 1.44090904),
                (71.13091309, 1.56153688),
                (71.91855734, 1.6867659),
                (72.69952499, 1.81655793),
                (73.47357814, 1.95087345),
                (74.24048101, 2.08967155),
                (75.0, 2.23290994),
                (75.75190375, 2.38054499),
                (76.49596321, 2.53253173),
                (77.23195175, 2.68882387),
                (77.95964517, 2.84937379),
                (78.67882182, 3.0141326),
                (79.38926261, 3.18305009),
                (80.09075116, 3.35607483),
                (80.78307377, 3.53315411),
                (81.46601955, 3.71423398),
                (82.13938048, 3.89925928),
                (82.80295145, 4.08817366),
                (83.45653032, 4.28091958),
                (84.099918, 4.47743831),
                (84.73291852, 4.67766999),
                (85.35533906, 4.88155365),
                (85.96699002, 5.08902716),
                (86.56768508, 5.30002733),
                (87.15724127, 5.51448989),
                (87.73547901, 5.73234952),
                (88.30222216, 5.95353984),
                (88.85729807, 6.17799348),
                (89.40053768, 6.40564208),
                (89.9317755, 6.63641628),
                (90.45084972, 6.8702458),
                (90.95760221, 7.10705939),
                (91.45187863, 7.34678494),
                (91.9335284, 7.58934942),
                (92.40240481, 7.83467893),
                (92.85836504, 8.08269875),
                (93.30127019, 8.33333333),
                (93.73098536, 8.58650633),
                (94.14737964, 8.84214062),
                (94.55032621, 9.10015834),
                (94.93970231, 9.36048089),
                (95.31538935, 9.62302897),
                (95.67727288, 9.88772262),
                (96.02524267, 10.15448119),
                (96.35919273, 10.42322344),
                (96.67902132, 10.69386751),
                (96.98463104, 10.96633094),
                (97.27592878, 11.24053076),
                (97.55282581, 11.51638343),
                (97.8152378, 11.79380492),
                (98.0630848, 12.07271074),
                (98.29629131, 12.35301591),
                (98.51478631, 12.63463507),
                (98.71850324, 12.91748243),
                (98.90738004, 13.20147182),
                (99.08135917, 13.48651674),
                (99.24038765, 13.77253037),
                (99.38441703, 14.05942558),
                (99.51340344, 14.34711498),
                (99.62730758, 14.63551094),
                (99.72609477, 14.92452561),
                (99.8097349, 15.21407095),
                (99.87820251, 15.50405877),
                (99.93147674, 15.79440073),
                (99.96954135, 16.08500839),
                (99.99238476, 16.37579323),
                (100.0, 16.66666667),
                (100.0, 83.33333333),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_decision(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an decision vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a decision vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (50.0, 0.0),
                (100.0, 50.0),
                (50.0, 100.0),
                (0.0, 50.0),
                (50.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_delay(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a delay vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a delay vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (50.0, 100.0),
                (50.43631016, 99.99238476),
                (50.87248742, 99.96954135),
                (51.30839891, 99.93147674),
                (51.74391184, 99.87820251),
                (52.17889357, 99.8097349),
                (52.61321158, 99.72609477),
                (53.04673359, 99.62730758),
                (53.47932752, 99.51340344),
                (53.91086163, 99.38441703),
                (54.34120444, 99.24038765),
                (54.77022488, 99.08135917),
                (55.19779227, 98.90738004),
                (55.62377636, 98.71850324),
                (56.04804739, 98.51478631),
                (56.47047613, 98.29629131),
                (56.8909339, 98.0630848),
                (57.30929262, 97.8152378),
                (57.72542486, 97.55282581),
                (58.13920386, 97.27592878),
                (58.55050358, 96.98463104),
                (58.95919874, 96.67902132),
                (59.36516484, 96.35919273),
                (59.76827821, 96.02524267),
                (60.16841608, 95.67727288),
                (60.56545654, 95.31538935),
                (60.95927867, 94.93970231),
                (61.34976249, 94.55032621),
                (61.73678907, 94.14737964),
                (62.12024051, 93.73098536),
                (62.5, 93.30127019),
                (62.87595187, 92.85836504),
                (63.24798161, 92.40240481),
                (63.61597588, 91.9335284),
                (63.97982259, 91.45187863),
                (64.33941091, 90.95760221),
                (64.69463131, 90.45084972),
                (65.04537558, 89.9317755),
                (65.39153688, 89.40053768),
                (65.73300978, 88.85729807),
                (66.06969024, 88.30222216),
                (66.40147572, 87.73547901),
                (66.72826516, 87.15724127),
                (67.049959, 86.56768508),
                (67.36645926, 85.96699002),
                (67.67766953, 85.35533906),
                (67.98349501, 84.73291852),
                (68.28384254, 84.099918),
                (68.57862064, 83.45653032),
                (68.86773951, 82.80295145),
                (69.15111108, 82.13938048),
                (69.42864904, 81.46601955),
                (69.70026884, 80.78307377),
                (69.96588775, 80.09075116),
                (70.22542486, 79.38926261),
                (70.47880111, 78.67882182),
                (70.72593931, 77.95964517),
                (70.9667642, 77.23195175),
                (71.2012024, 76.49596321),
                (71.42918252, 75.75190375),
                (71.65063509, 75.0),
                (71.86549268, 74.24048101),
                (72.07368982, 73.47357814),
                (72.2751631, 72.69952499),
                (72.46985116, 71.91855734),
                (72.65769468, 71.13091309),
                (72.83863644, 70.33683215),
                (73.01262134, 69.53655642),
                (73.17959636, 68.73032967),
                (73.33951066, 67.91839748),
                (73.49231552, 67.10100717),
                (73.63796439, 66.27840772),
                (73.77641291, 65.45084972),
                (73.9076189, 64.61858524),
                (74.0315424, 63.78186779),
                (74.14814566, 62.94095226),
                (74.25739316, 62.09609478),
                (74.35925162, 61.24755272),
                (74.45369002, 60.39558454),
                (74.54067959, 59.54044977),
                (74.62019383, 58.68240888),
                (74.69220851, 57.82172325),
                (74.75670172, 56.95865505),
                (74.81365379, 56.09346717),
                (74.86304738, 55.22642316),
                (74.90486745, 54.35778714),
                (74.93910126, 53.48782369),
                (74.96573837, 52.61679781),
                (74.98477068, 51.74497484),
                (74.99619238, 50.87262032),
                (75.0, 50.0),
                (74.99619238, 49.12737968),
                (74.98477068, 48.25502516),
                (74.96573837, 47.38320219),
                (74.93910126, 46.51217631),
                (74.90486745, 45.64221286),
                (74.86304738, 44.77357684),
                (74.81365379, 43.90653283),
                (74.75670172, 43.04134495),
                (74.69220851, 42.17827675),
                (74.62019383, 41.31759112),
                (74.54067959, 40.45955023),
                (74.45369002, 39.60441546),
                (74.35925162, 38.75244728),
                (74.25739316, 37.90390522),
                (74.14814566, 37.05904774),
                (74.0315424, 36.21813221),
                (73.9076189, 35.38141476),
                (73.77641291, 34.54915028),
                (73.63796439, 33.72159228),
                (73.49231552, 32.89899283),
                (73.33951066, 32.08160252),
                (73.17959636, 31.26967033),
                (73.01262134, 30.46344358),
                (72.83863644, 29.66316785),
                (72.65769468, 28.86908691),
                (72.46985116, 28.08144266),
                (72.2751631, 27.30047501),
                (72.07368982, 26.52642186),
                (71.86549268, 25.75951899),
                (71.65063509, 25.0),
                (71.42918252, 24.24809625),
                (71.2012024, 23.50403679),
                (70.9667642, 22.76804825),
                (70.72593931, 22.04035483),
                (70.47880111, 21.32117818),
                (70.22542486, 20.61073739),
                (69.96588775, 19.90924884),
                (69.70026884, 19.21692623),
                (69.42864904, 18.53398045),
                (69.15111108, 17.86061952),
                (68.86773951, 17.19704855),
                (68.57862064, 16.54346968),
                (68.28384254, 15.900082),
                (67.98349501, 15.26708148),
                (67.67766953, 14.64466094),
                (67.36645926, 14.03300998),
                (67.049959, 13.43231492),
                (66.72826516, 12.84275873),
                (66.40147572, 12.26452099),
                (66.06969024, 11.69777784),
                (65.73300978, 11.14270193),
                (65.39153688, 10.59946232),
                (65.04537558, 10.0682245),
                (64.69463131, 9.54915028),
                (64.33941091, 9.04239779),
                (63.97982259, 8.54812137),
                (63.61597588, 8.0664716),
                (63.24798161, 7.59759519),
                (62.87595187, 7.14163496),
                (62.5, 6.69872981),
                (62.12024051, 6.26901464),
                (61.73678907, 5.85262036),
                (61.34976249, 5.44967379),
                (60.95927867, 5.06029769),
                (60.56545654, 4.68461065),
                (60.16841608, 4.32272712),
                (59.76827821, 3.97475733),
                (59.36516484, 3.64080727),
                (58.95919874, 3.32097868),
                (58.55050358, 3.01536896),
                (58.13920386, 2.72407122),
                (57.72542486, 2.44717419),
                (57.30929262, 2.1847622),
                (56.8909339, 1.9369152),
                (56.47047613, 1.70370869),
                (56.04804739, 1.48521369),
                (55.62377636, 1.28149676),
                (55.19779227, 1.09261996),
                (54.77022488, 0.91864083),
                (54.34120444, 0.75961235),
                (53.91086163, 0.61558297),
                (53.47932752, 0.48659656),
                (53.04673359, 0.37269242),
                (52.61321158, 0.27390523),
                (52.17889357, 0.1902651),
                (51.74391184, 0.12179749),
                (51.30839891, 0.06852326),
                (50.87248742, 0.03045865),
                (50.43631016, 0.00761524),
                (0.0, 0.00761524),
                (0.0, 100.0),
                (50.0, 100.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_direct_data(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a direct data vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a direct data vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.flowchart_database(
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
            fill_color=fill_color,
            line_width=line_width,
            stroke_color=stroke_color,
        ).rotate(angle_in_degrees=90)

    @staticmethod
    def flowchart_display(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an display vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a display vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (90.0, 100.0),
                (90.17452406, 99.99238476),
                (90.34899497, 99.96954135),
                (90.52335956, 99.93147674),
                (90.69756474, 99.87820251),
                (90.87155743, 99.8097349),
                (91.04528463, 99.72609477),
                (91.21869343, 99.62730758),
                (91.39173101, 99.51340344),
                (91.56434465, 99.38441703),
                (91.73648178, 99.24038765),
                (91.90808995, 99.08135917),
                (92.07911691, 98.90738004),
                (92.24951054, 98.71850324),
                (92.41921896, 98.51478631),
                (92.58819045, 98.29629131),
                (92.75637356, 98.0630848),
                (92.92371705, 97.8152378),
                (93.09016994, 97.55282581),
                (93.25568154, 97.27592878),
                (93.42020143, 96.98463104),
                (93.5836795, 96.67902132),
                (93.74606593, 96.35919273),
                (93.90731128, 96.02524267),
                (94.06736643, 95.67727288),
                (94.22618262, 95.31538935),
                (94.38371147, 94.93970231),
                (94.539905, 94.55032621),
                (94.69471563, 94.14737964),
                (94.8480962, 93.73098536),
                (95.0, 93.30127019),
                (95.15038075, 92.85836504),
                (95.29919264, 92.40240481),
                (95.44639035, 91.9335284),
                (95.59192903, 91.45187863),
                (95.73576436, 90.95760221),
                (95.87785252, 90.45084972),
                (96.01815023, 89.9317755),
                (96.15661475, 89.40053768),
                (96.29320391, 88.85729807),
                (96.4278761, 88.30222216),
                (96.56059029, 87.73547901),
                (96.69130606, 87.15724127),
                (96.8199836, 86.56768508),
                (96.9465837, 85.96699002),
                (97.07106781, 85.35533906),
                (97.193398, 84.73291852),
                (97.31353702, 84.099918),
                (97.43144825, 83.45653032),
                (97.5470958, 82.80295145),
                (97.66044443, 82.13938048),
                (97.77145961, 81.46601955),
                (97.88010754, 80.78307377),
                (97.9863551, 80.09075116),
                (98.09016994, 79.38926261),
                (98.19152044, 78.67882182),
                (98.29037573, 77.95964517),
                (98.38670568, 77.23195175),
                (98.48048096, 76.49596321),
                (98.57167301, 75.75190375),
                (98.66025404, 75.0),
                (98.74619707, 74.24048101),
                (98.82947593, 73.47357814),
                (98.91006524, 72.69952499),
                (98.98794046, 71.91855734),
                (99.06307787, 71.13091309),
                (99.13545458, 70.33683215),
                (99.20504853, 69.53655642),
                (99.27183855, 68.73032967),
                (99.33580426, 67.91839748),
                (99.39692621, 67.10100717),
                (99.45518576, 66.27840772),
                (99.51056516, 65.45084972),
                (99.56304756, 64.61858524),
                (99.61261696, 63.78186779),
                (99.65925826, 62.94095226),
                (99.70295726, 62.09609478),
                (99.74370065, 61.24755272),
                (99.78147601, 60.39558454),
                (99.81627183, 59.54044977),
                (99.84807753, 58.68240888),
                (99.87688341, 57.82172325),
                (99.90268069, 56.95865505),
                (99.92546152, 56.09346717),
                (99.94521895, 55.22642316),
                (99.96194698, 54.35778714),
                (99.9756405, 53.48782369),
                (99.98629535, 52.61679781),
                (99.99390827, 51.74497484),
                (99.99847695, 50.87262032),
                (100.0, 50.0),
                (99.99847695, 49.12737968),
                (99.99390827, 48.25502516),
                (99.98629535, 47.38320219),
                (99.9756405, 46.51217631),
                (99.96194698, 45.64221286),
                (99.94521895, 44.77357684),
                (99.92546152, 43.90653283),
                (99.90268069, 43.04134495),
                (99.87688341, 42.17827675),
                (99.84807753, 41.31759112),
                (99.81627183, 40.45955023),
                (99.78147601, 39.60441546),
                (99.74370065, 38.75244728),
                (99.70295726, 37.90390522),
                (99.65925826, 37.05904774),
                (99.61261696, 36.21813221),
                (99.56304756, 35.38141476),
                (99.51056516, 34.54915028),
                (99.45518576, 33.72159228),
                (99.39692621, 32.89899283),
                (99.33580426, 32.08160252),
                (99.27183855, 31.26967033),
                (99.20504853, 30.46344358),
                (99.13545458, 29.66316785),
                (99.06307787, 28.86908691),
                (98.98794046, 28.08144266),
                (98.91006524, 27.30047501),
                (98.82947593, 26.52642186),
                (98.74619707, 25.75951899),
                (98.66025404, 25.0),
                (98.57167301, 24.24809625),
                (98.48048096, 23.50403679),
                (98.38670568, 22.76804825),
                (98.29037573, 22.04035483),
                (98.19152044, 21.32117818),
                (98.09016994, 20.61073739),
                (97.9863551, 19.90924884),
                (97.88010754, 19.21692623),
                (97.77145961, 18.53398045),
                (97.66044443, 17.86061952),
                (97.5470958, 17.19704855),
                (97.43144825, 16.54346968),
                (97.31353702, 15.900082),
                (97.193398, 15.26708148),
                (97.07106781, 14.64466094),
                (96.9465837, 14.03300998),
                (96.8199836, 13.43231492),
                (96.69130606, 12.84275873),
                (96.56059029, 12.26452099),
                (96.4278761, 11.69777784),
                (96.29320391, 11.14270193),
                (96.15661475, 10.59946232),
                (96.01815023, 10.0682245),
                (95.87785252, 9.54915028),
                (95.73576436, 9.04239779),
                (95.59192903, 8.54812137),
                (95.44639035, 8.0664716),
                (95.29919264, 7.59759519),
                (95.15038075, 7.14163496),
                (95.0, 6.69872981),
                (94.8480962, 6.26901464),
                (94.69471563, 5.85262036),
                (94.539905, 5.44967379),
                (94.38371147, 5.06029769),
                (94.22618262, 4.68461065),
                (94.06736643, 4.32272712),
                (93.90731128, 3.97475733),
                (93.74606593, 3.64080727),
                (93.5836795, 3.32097868),
                (93.42020143, 3.01536896),
                (93.25568154, 2.72407122),
                (93.09016994, 2.44717419),
                (92.92371705, 2.1847622),
                (92.75637356, 1.9369152),
                (92.58819045, 1.70370869),
                (92.41921896, 1.48521369),
                (92.24951054, 1.28149676),
                (92.07911691, 1.09261996),
                (91.90808995, 0.91864083),
                (91.73648178, 0.75961235),
                (91.56434465, 0.61558297),
                (91.39173101, 0.48659656),
                (91.21869343, 0.37269242),
                (91.04528463, 0.27390523),
                (90.87155743, 0.1902651),
                (90.69756474, 0.12179749),
                (90.52335956, 0.06852326),
                (90.34899497, 0.03045865),
                (90.17452406, 0.00761524),
                (10.0, 0.0),
                (0.0, 50.0),
                (10.0, 100.0),
                (90.0, 100.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_document(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a document vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a document vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (62.5, -4.57531755),
                (62.91666667, -4.68274634),
                (63.33333333, -4.78684491),
                (63.75, -4.88758155),
                (64.16666667, -4.98492558),
                (64.58333333, -5.07884734),
                (65.0, -5.16931822),
                (65.41666667, -5.25631067),
                (65.83333333, -5.33979818),
                (66.25, -5.41975533),
                (66.66666667, -5.49615776),
                (67.08333333, -5.56898219),
                (67.5, -5.63820645),
                (67.91666667, -5.70380945),
                (68.33333333, -5.7657712),
                (68.75, -5.82407283),
                (69.16666667, -5.87869658),
                (69.58333333, -5.92962581),
                (70.0, -5.97684501),
                (70.41666667, -6.02033979),
                (70.83333333, -6.06009691),
                (71.25, -6.09610426),
                (71.66666667, -6.12835086),
                (72.08333333, -6.1568269),
                (72.5, -6.18152369),
                (72.91666667, -6.20243373),
                (73.33333333, -6.21955063),
                (73.75, -6.23286918),
                (74.16666667, -6.24238534),
                (74.58333333, -6.24809619),
                (75.0, -6.25),
                (75.41666667, -6.24809619),
                (75.83333333, -6.24238534),
                (76.25, -6.23286918),
                (76.66666667, -6.21955063),
                (77.08333333, -6.20243373),
                (77.5, -6.18152369),
                (77.91666667, -6.1568269),
                (78.33333333, -6.12835086),
                (78.75, -6.09610426),
                (79.16666667, -6.06009691),
                (79.58333333, -6.02033979),
                (80.0, -5.97684501),
                (80.41666667, -5.92962581),
                (80.83333333, -5.87869658),
                (81.25, -5.82407283),
                (81.66666667, -5.7657712),
                (82.08333333, -5.70380945),
                (82.5, -5.63820645),
                (82.91666667, -5.56898219),
                (83.33333333, -5.49615776),
                (83.75, -5.41975533),
                (84.16666667, -5.33979818),
                (84.58333333, -5.25631067),
                (85.0, -5.16931822),
                (85.41666667, -5.07884734),
                (85.83333333, -4.98492558),
                (86.25, -4.88758155),
                (86.66666667, -4.78684491),
                (87.08333333, -4.68274634),
                (87.5, -4.57531755),
                (87.91666667, -4.46459126),
                (88.33333333, -4.3506012),
                (88.75, -4.2333821),
                (89.16666667, -4.11296966),
                (89.58333333, -3.98940055),
                (90.0, -3.86271243),
                (90.41666667, -3.73294388),
                (90.83333333, -3.60013442),
                (91.25, -3.46432452),
                (91.66666667, -3.32555554),
                (92.08333333, -3.18386975),
                (92.5, -3.03931032),
                (92.91666667, -2.89192127),
                (93.33333333, -2.7417475),
                (93.75, -2.58883476),
                (94.16666667, -2.43322963),
                (94.58333333, -2.2749795),
                (95.0, -2.11413258),
                (95.41666667, -1.95073786),
                (95.83333333, -1.78484512),
                (96.25, -1.61650489),
                (96.66666667, -1.44576844),
                (97.08333333, -1.27268779),
                (97.5, -1.09731565),
                (97.91666667, -0.91970545),
                (98.33333333, -0.73991129),
                (98.75, -0.55798794),
                (99.16666667, -0.3739908),
                (99.58333333, -0.18797594),
                (100.0, -0.0),
                (100.41666667, 0.18987975),
                (100.83333333, 0.38160547),
                (101.25, 0.57511875),
                (101.66666667, 0.77036067),
                (102.08333333, 0.96727173),
                (102.5, 1.16579196),
                (102.91666667, 1.36586089),
                (103.33333333, 1.56741758),
                (103.75, 1.77040063),
                (104.16666667, 1.97474821),
                (104.58333333, 2.18039807),
                (105.0, 2.38728757),
                (105.41666667, 2.59535369),
                (105.83333333, 2.80453305),
                (106.25, 3.01476194),
                (106.66666667, 3.22597631),
                (107.08333333, 3.43811182),
                (107.5, 3.65110386),
                (107.91666667, 3.86488756),
                (108.33333333, 4.07939778),
                (108.75, 4.29456919),
                (109.16666667, 4.51033624),
                (109.58333333, 4.72663321),
                (110.0, 4.94339421),
                (110.41666667, 5.16055322),
                (110.83333333, 5.37804408),
                (111.25, 5.59580055),
                (111.66666667, 5.81375629),
                (112.08333333, 6.03184492),
                (112.5, 6.25),
                (112.91666667, 6.46815508),
                (113.33333333, 6.68624371),
                (113.75, 6.90419945),
                (114.16666667, 7.12195592),
                (114.58333333, 7.33944678),
                (115.0, 7.55660579),
                (115.41666667, 7.77336679),
                (115.83333333, 7.98966376),
                (116.25, 8.20543081),
                (116.66666667, 8.42060222),
                (117.08333333, 8.63511244),
                (117.5, 8.84889614),
                (117.91666667, 9.06188818),
                (118.33333333, 9.27402369),
                (118.75, 9.48523806),
                (119.16666667, 9.69546695),
                (119.58333333, 9.90464631),
                (120.0, 10.11271243),
                (120.41666667, 10.31960193),
                (120.83333333, 10.52525179),
                (121.25, 10.72959937),
                (121.66666667, 10.93258242),
                (122.08333333, 11.13413911),
                (122.5, 11.33420804),
                (122.91666667, 11.53272827),
                (123.33333333, 11.72963933),
                (123.75, 11.92488125),
                (124.16666667, 12.11839453),
                (124.58333333, 12.31012025),
                (125.0, 12.5),
                (125.41666667, 12.68797594),
                (125.83333333, 12.8739908),
                (126.25, 13.05798794),
                (126.66666667, 13.23991129),
                (127.08333333, 13.41970545),
                (127.5, 13.59731565),
                (127.91666667, 13.77268779),
                (128.33333333, 13.94576844),
                (128.75, 14.11650489),
                (129.16666667, 14.28484512),
                (129.58333333, 14.45073786),
                (130.0, 14.61413258),
                (130.41666667, 14.7749795),
                (130.83333333, 14.93322963),
                (131.25, 15.08883476),
                (131.66666667, 15.2417475),
                (132.08333333, 15.39192127),
                (132.5, 15.53931032),
                (132.91666667, 15.68386975),
                (133.33333333, 15.82555554),
                (133.75, 15.96432452),
                (134.16666667, 16.10013442),
                (134.58333333, 16.23294388),
                (135.0, 16.36271243),
                (135.41666667, 16.48940055),
                (135.83333333, 16.61296966),
                (136.25, 16.7333821),
                (136.66666667, 16.8506012),
                (137.08333333, 16.96459126),
                (137.5, 17.07531755),
                (137.91666667, 17.18274634),
                (138.33333333, 17.28684491),
                (138.75, 17.38758155),
                (139.16666667, 17.48492558),
                (139.58333333, 17.57884734),
                (140.0, 17.66931822),
                (140.41666667, 17.75631067),
                (140.83333333, 17.83979818),
                (141.25, 17.91975533),
                (141.66666667, 17.99615776),
                (142.08333333, 18.06898219),
                (142.5, 18.13820645),
                (142.91666667, 18.20380945),
                (143.33333333, 18.2657712),
                (143.75, 18.32407283),
                (144.16666667, 18.37869658),
                (144.58333333, 18.42962581),
                (145.0, 18.47684501),
                (145.41666667, 18.52033979),
                (145.83333333, 18.56009691),
                (146.25, 18.59610426),
                (146.66666667, 18.62835086),
                (147.08333333, 18.6568269),
                (147.5, 18.68152369),
                (147.91666667, 18.70243373),
                (148.33333333, 18.71955063),
                (148.75, 18.73286918),
                (149.16666667, 18.74238534),
                (149.58333333, 18.74809619),
                (150.0, 18.75),
                (150.41666667, 18.74809619),
                (150.83333333, 18.74238534),
                (151.25, 18.73286918),
                (151.66666667, 18.71955063),
                (152.08333333, 18.70243373),
                (152.5, 18.68152369),
                (152.91666667, 18.6568269),
                (153.33333333, 18.62835086),
                (153.75, 18.59610426),
                (154.16666667, 18.56009691),
                (154.58333333, 18.52033979),
                (155.0, 18.47684501),
                (155.41666667, 18.42962581),
                (155.83333333, 18.37869658),
                (156.25, 18.32407283),
                (156.66666667, 18.2657712),
                (157.08333333, 18.20380945),
                (157.5, 18.13820645),
                (157.91666667, 18.06898219),
                (158.33333333, 17.99615776),
                (158.75, 17.91975533),
                (159.16666667, 17.83979818),
                (159.58333333, 17.75631067),
                (160.0, 17.66931822),
                (160.41666667, 17.57884734),
                (160.83333333, 17.48492558),
                (161.25, 17.38758155),
                (161.66666667, 17.28684491),
                (162.08333333, 17.18274634),
                (162.08333333, 100.0),
                (62.5, 100.0),
                (62.5, -4.57531755),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def flowchart_extract(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an extract vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        an extract vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (50.0, 100.0),
                (100.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_internal_storage(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an internal storage vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        an internal storage vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 100.0),
                (100.0, 100.0),
                (100.0, 0.0),
                (0.0, 0.0),
                (10.0, 0.0),
                (10.0, 100.0),
                (0.0, 100.0),
                (0.0, 90.0),
                (100.0, 90.0),
                (0.0, 90.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_loop_limit(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a loop limit vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a loop limit vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 75.0),
                (25.0, 100.0),
                (75.0, 100.0),
                (100.0, 75.0),
                (100.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_manual_input(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a manual input vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a manual input vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 80.0),
                (100.0, 100.0),
                (100.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_manual_operation(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a manual operation vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a manual operation vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 100.0),
                (100.0, 80.0),
                (100.0, 20.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_merge(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a merge vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a merge vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 100.0),
                (50.0, 0.0),
                (100.0, 100.0),
                (0.0, 100.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_multiple_documents(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a multiple documents vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a multiple documents vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (62.5, -4.57531755),
                (62.91666667, -4.68274634),
                (63.33333333, -4.78684491),
                (63.75, -4.88758155),
                (64.16666667, -4.98492558),
                (64.58333333, -5.07884734),
                (65.0, -5.16931822),
                (65.41666667, -5.25631067),
                (65.83333333, -5.33979818),
                (66.25, -5.41975533),
                (66.66666667, -5.49615776),
                (67.08333333, -5.56898219),
                (67.5, -5.63820645),
                (67.91666667, -5.70380945),
                (68.33333333, -5.7657712),
                (68.75, -5.82407283),
                (69.16666667, -5.87869658),
                (69.58333333, -5.92962581),
                (70.0, -5.97684501),
                (70.41666667, -6.02033979),
                (70.83333333, -6.06009691),
                (71.25, -6.09610426),
                (71.66666667, -6.12835086),
                (72.08333333, -6.1568269),
                (72.5, -6.18152369),
                (72.91666667, -6.20243373),
                (73.33333333, -6.21955063),
                (73.75, -6.23286918),
                (74.16666667, -6.24238534),
                (74.58333333, -6.24809619),
                (75.0, -6.25),
                (75.41666667, -6.24809619),
                (75.83333333, -6.24238534),
                (76.25, -6.23286918),
                (76.66666667, -6.21955063),
                (77.08333333, -6.20243373),
                (77.5, -6.18152369),
                (77.91666667, -6.1568269),
                (78.33333333, -6.12835086),
                (78.75, -6.09610426),
                (79.16666667, -6.06009691),
                (79.58333333, -6.02033979),
                (80.0, -5.97684501),
                (80.41666667, -5.92962581),
                (80.83333333, -5.87869658),
                (81.25, -5.82407283),
                (81.66666667, -5.7657712),
                (82.08333333, -5.70380945),
                (82.5, -5.63820645),
                (82.91666667, -5.56898219),
                (83.33333333, -5.49615776),
                (83.75, -5.41975533),
                (84.16666667, -5.33979818),
                (84.58333333, -5.25631067),
                (85.0, -5.16931822),
                (85.41666667, -5.07884734),
                (85.83333333, -4.98492558),
                (86.25, -4.88758155),
                (86.66666667, -4.78684491),
                (87.08333333, -4.68274634),
                (87.5, -4.57531755),
                (87.91666667, -4.46459126),
                (88.33333333, -4.3506012),
                (88.75, -4.2333821),
                (89.16666667, -4.11296966),
                (89.58333333, -3.98940055),
                (90.0, -3.86271243),
                (90.41666667, -3.73294388),
                (90.83333333, -3.60013442),
                (91.25, -3.46432452),
                (91.66666667, -3.32555554),
                (92.08333333, -3.18386975),
                (92.5, -3.03931032),
                (92.91666667, -2.89192127),
                (93.33333333, -2.7417475),
                (93.75, -2.58883476),
                (94.16666667, -2.43322963),
                (94.58333333, -2.2749795),
                (95.0, -2.11413258),
                (95.41666667, -1.95073786),
                (95.83333333, -1.78484512),
                (96.25, -1.61650489),
                (96.66666667, -1.44576844),
                (97.08333333, -1.27268779),
                (97.5, -1.09731565),
                (97.91666667, -0.91970545),
                (98.33333333, -0.73991129),
                (98.75, -0.55798794),
                (99.16666667, -0.3739908),
                (99.58333333, -0.18797594),
                (100.0, -0.0),
                (100.41666667, 0.18987975),
                (100.83333333, 0.38160547),
                (101.25, 0.57511875),
                (101.66666667, 0.77036067),
                (102.08333333, 0.96727173),
                (102.5, 1.16579196),
                (102.91666667, 1.36586089),
                (103.33333333, 1.56741758),
                (103.75, 1.77040063),
                (104.16666667, 1.97474821),
                (104.58333333, 2.18039807),
                (105.0, 2.38728757),
                (105.41666667, 2.59535369),
                (105.83333333, 2.80453305),
                (106.25, 3.01476194),
                (106.66666667, 3.22597631),
                (107.08333333, 3.43811182),
                (107.5, 3.65110386),
                (107.91666667, 3.86488756),
                (108.33333333, 4.07939778),
                (108.75, 4.29456919),
                (109.16666667, 4.51033624),
                (109.58333333, 4.72663321),
                (110.0, 4.94339421),
                (110.41666667, 5.16055322),
                (110.83333333, 5.37804408),
                (111.25, 5.59580055),
                (111.66666667, 5.81375629),
                (112.08333333, 6.03184492),
                (112.5, 6.25),
                (112.91666667, 6.46815508),
                (113.33333333, 6.68624371),
                (113.75, 6.90419945),
                (114.16666667, 7.12195592),
                (114.58333333, 7.33944678),
                (115.0, 7.55660579),
                (115.41666667, 7.77336679),
                (115.83333333, 7.98966376),
                (116.25, 8.20543081),
                (116.66666667, 8.42060222),
                (117.08333333, 8.63511244),
                (117.5, 8.84889614),
                (117.91666667, 9.06188818),
                (118.33333333, 9.27402369),
                (118.75, 9.48523806),
                (119.16666667, 9.69546695),
                (119.58333333, 9.90464631),
                (120.0, 10.11271243),
                (120.41666667, 10.31960193),
                (120.83333333, 10.52525179),
                (121.25, 10.72959937),
                (121.66666667, 10.93258242),
                (122.08333333, 11.13413911),
                (122.5, 11.33420804),
                (122.91666667, 11.53272827),
                (123.33333333, 11.72963933),
                (123.75, 11.92488125),
                (124.16666667, 12.11839453),
                (124.58333333, 12.31012025),
                (125.0, 12.5),
                (125.41666667, 12.68797594),
                (125.83333333, 12.8739908),
                (126.25, 13.05798794),
                (126.66666667, 13.23991129),
                (127.08333333, 13.41970545),
                (127.5, 13.59731565),
                (127.91666667, 13.77268779),
                (128.33333333, 13.94576844),
                (128.75, 14.11650489),
                (129.16666667, 14.28484512),
                (129.58333333, 14.45073786),
                (130.0, 14.61413258),
                (130.41666667, 14.7749795),
                (130.83333333, 14.93322963),
                (131.25, 15.08883476),
                (131.66666667, 15.2417475),
                (132.08333333, 15.39192127),
                (132.5, 15.53931032),
                (132.91666667, 15.68386975),
                (133.33333333, 15.82555554),
                (133.75, 15.96432452),
                (134.16666667, 16.10013442),
                (134.58333333, 16.23294388),
                (135.0, 16.36271243),
                (135.41666667, 16.48940055),
                (135.83333333, 16.61296966),
                (136.25, 16.7333821),
                (136.66666667, 16.8506012),
                (137.08333333, 16.96459126),
                (137.5, 17.07531755),
                (137.91666667, 17.18274634),
                (138.33333333, 17.28684491),
                (138.75, 17.38758155),
                (139.16666667, 17.48492558),
                (139.58333333, 17.57884734),
                (140.0, 17.66931822),
                (140.41666667, 17.75631067),
                (140.83333333, 17.83979818),
                (141.25, 17.91975533),
                (141.66666667, 17.99615776),
                (142.08333333, 18.06898219),
                (142.5, 18.13820645),
                (142.91666667, 18.20380945),
                (143.33333333, 18.2657712),
                (143.75, 18.32407283),
                (144.16666667, 18.37869658),
                (144.58333333, 18.42962581),
                (145.0, 18.47684501),
                (145.41666667, 18.52033979),
                (145.83333333, 18.56009691),
                (146.25, 18.59610426),
                (146.66666667, 18.62835086),
                (147.08333333, 18.6568269),
                (147.5, 18.68152369),
                (147.91666667, 18.70243373),
                (148.33333333, 18.71955063),
                (148.75, 18.73286918),
                (149.16666667, 18.74238534),
                (149.58333333, 18.74809619),
                (150.0, 18.75),
                (150.41666667, 18.74809619),
                (150.83333333, 18.74238534),
                (151.25, 18.73286918),
                (151.66666667, 18.71955063),
                (152.08333333, 18.70243373),
                (152.5, 18.68152369),
                (152.91666667, 18.6568269),
                (153.33333333, 18.62835086),
                (153.75, 18.59610426),
                (154.16666667, 18.56009691),
                (154.58333333, 18.52033979),
                (155.0, 18.47684501),
                (155.41666667, 18.42962581),
                (155.83333333, 18.37869658),
                (156.25, 18.32407283),
                (156.66666667, 18.2657712),
                (157.08333333, 18.20380945),
                (157.5, 18.13820645),
                (157.91666667, 18.06898219),
                (158.33333333, 17.99615776),
                (158.75, 17.91975533),
                (159.16666667, 17.83979818),
                (159.58333333, 17.75631067),
                (160.0, 17.66931822),
                (160.41666667, 17.57884734),
                (160.83333333, 17.48492558),
                (161.25, 17.38758155),
                (161.66666667, 17.28684491),
                (162.08333333, 17.18274634),
                (162.08333333, 100.0),
                (62.5, 100.0),
                (62.5, -4.57531755),
                (62.5, 0),
                (52.5, 0),
                (52.5, 110),
                (152.5, 110),
                (152.5, 100),
                (62.5, 100),
                (62.5, 0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def flowchart_off_page_reference(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an off page reference vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        an off page reference vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (100, 0),
                (100, -62),
                (50, -100),
                (0, -62),
                (0, 0),
            ],
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
            fill_color=fill_color,
            line_width=line_width,
            stroke_color=stroke_color,
        )

    @staticmethod
    def flowchart_on_page_reference(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an on page reference vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        an on page reference vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.circle(
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
            fill_color=fill_color,
            line_width=line_width,
            stroke_color=stroke_color,
        )

    @staticmethod
    def flowchart_or(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a logical OR vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a logical OR vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (50.0, 100.0),
                (50.0, 0.0),
                (50.0, 100.0),
                (50.87262032, 99.99238476),
                (51.74497484, 99.96954135),
                (52.61679781, 99.93147674),
                (53.48782369, 99.87820251),
                (54.35778714, 99.8097349),
                (55.22642316, 99.72609477),
                (56.09346717, 99.62730758),
                (56.95865505, 99.51340344),
                (57.82172325, 99.38441703),
                (58.68240888, 99.24038765),
                (59.54044977, 99.08135917),
                (60.39558454, 98.90738004),
                (61.24755272, 98.71850324),
                (62.09609478, 98.51478631),
                (62.94095226, 98.29629131),
                (63.78186779, 98.0630848),
                (64.61858524, 97.8152378),
                (65.45084972, 97.55282581),
                (66.27840772, 97.27592878),
                (67.10100717, 96.98463104),
                (67.91839748, 96.67902132),
                (68.73032967, 96.35919273),
                (69.53655642, 96.02524267),
                (70.33683215, 95.67727288),
                (71.13091309, 95.31538935),
                (71.91855734, 94.93970231),
                (72.69952499, 94.55032621),
                (73.47357814, 94.14737964),
                (74.24048101, 93.73098536),
                (75.0, 93.30127019),
                (75.75190375, 92.85836504),
                (76.49596321, 92.40240481),
                (77.23195175, 91.9335284),
                (77.95964517, 91.45187863),
                (78.67882182, 90.95760221),
                (79.38926261, 90.45084972),
                (80.09075116, 89.9317755),
                (80.78307377, 89.40053768),
                (81.46601955, 88.85729807),
                (82.13938048, 88.30222216),
                (82.80295145, 87.73547901),
                (83.45653032, 87.15724127),
                (84.099918, 86.56768508),
                (84.73291852, 85.96699002),
                (85.35533906, 85.35533906),
                (85.96699002, 84.73291852),
                (86.56768508, 84.099918),
                (87.15724127, 83.45653032),
                (87.73547901, 82.80295145),
                (88.30222216, 82.13938048),
                (88.85729807, 81.46601955),
                (89.40053768, 80.78307377),
                (89.9317755, 80.09075116),
                (90.45084972, 79.38926261),
                (90.95760221, 78.67882182),
                (91.45187863, 77.95964517),
                (91.9335284, 77.23195175),
                (92.40240481, 76.49596321),
                (92.85836504, 75.75190375),
                (93.30127019, 75.0),
                (93.73098536, 74.24048101),
                (94.14737964, 73.47357814),
                (94.55032621, 72.69952499),
                (94.93970231, 71.91855734),
                (95.31538935, 71.13091309),
                (95.67727288, 70.33683215),
                (96.02524267, 69.53655642),
                (96.35919273, 68.73032967),
                (96.67902132, 67.91839748),
                (96.98463104, 67.10100717),
                (97.27592878, 66.27840772),
                (97.55282581, 65.45084972),
                (97.8152378, 64.61858524),
                (98.0630848, 63.78186779),
                (98.29629131, 62.94095226),
                (98.51478631, 62.09609478),
                (98.71850324, 61.24755272),
                (98.90738004, 60.39558454),
                (99.08135917, 59.54044977),
                (99.24038765, 58.68240888),
                (99.38441703, 57.82172325),
                (99.51340344, 56.95865505),
                (99.62730758, 56.09346717),
                (99.72609477, 55.22642316),
                (99.8097349, 54.35778714),
                (99.87820251, 53.48782369),
                (99.93147674, 52.61679781),
                (99.96954135, 51.74497484),
                (99.99238476, 50.87262032),
                (100.0, 50.0),
                (0.0, 50.0),
                (100.0, 50.0),
                (99.99238476, 49.12737968),
                (99.96954135, 48.25502516),
                (99.93147674, 47.38320219),
                (99.87820251, 46.51217631),
                (99.8097349, 45.64221286),
                (99.72609477, 44.77357684),
                (99.62730758, 43.90653283),
                (99.51340344, 43.04134495),
                (99.38441703, 42.17827675),
                (99.24038765, 41.31759112),
                (99.08135917, 40.45955023),
                (98.90738004, 39.60441546),
                (98.71850324, 38.75244728),
                (98.51478631, 37.90390522),
                (98.29629131, 37.05904774),
                (98.0630848, 36.21813221),
                (97.8152378, 35.38141476),
                (97.55282581, 34.54915028),
                (97.27592878, 33.72159228),
                (96.98463104, 32.89899283),
                (96.67902132, 32.08160252),
                (96.35919273, 31.26967033),
                (96.02524267, 30.46344358),
                (95.67727288, 29.66316785),
                (95.31538935, 28.86908691),
                (94.93970231, 28.08144266),
                (94.55032621, 27.30047501),
                (94.14737964, 26.52642186),
                (93.73098536, 25.75951899),
                (93.30127019, 25.0),
                (92.85836504, 24.24809625),
                (92.40240481, 23.50403679),
                (91.9335284, 22.76804825),
                (91.45187863, 22.04035483),
                (90.95760221, 21.32117818),
                (90.45084972, 20.61073739),
                (89.9317755, 19.90924884),
                (89.40053768, 19.21692623),
                (88.85729807, 18.53398045),
                (88.30222216, 17.86061952),
                (87.73547901, 17.19704855),
                (87.15724127, 16.54346968),
                (86.56768508, 15.900082),
                (85.96699002, 15.26708148),
                (85.35533906, 14.64466094),
                (84.73291852, 14.03300998),
                (84.099918, 13.43231492),
                (83.45653032, 12.84275873),
                (82.80295145, 12.26452099),
                (82.13938048, 11.69777784),
                (81.46601955, 11.14270193),
                (80.78307377, 10.59946232),
                (80.09075116, 10.0682245),
                (79.38926261, 9.54915028),
                (78.67882182, 9.04239779),
                (77.95964517, 8.54812137),
                (77.23195175, 8.0664716),
                (76.49596321, 7.59759519),
                (75.75190375, 7.14163496),
                (75.0, 6.69872981),
                (74.24048101, 6.26901464),
                (73.47357814, 5.85262036),
                (72.69952499, 5.44967379),
                (71.91855734, 5.06029769),
                (71.13091309, 4.68461065),
                (70.33683215, 4.32272712),
                (69.53655642, 3.97475733),
                (68.73032967, 3.64080727),
                (67.91839748, 3.32097868),
                (67.10100717, 3.01536896),
                (66.27840772, 2.72407122),
                (65.45084972, 2.44717419),
                (64.61858524, 2.1847622),
                (63.78186779, 1.9369152),
                (62.94095226, 1.70370869),
                (62.09609478, 1.48521369),
                (61.24755272, 1.28149676),
                (60.39558454, 1.09261996),
                (59.54044977, 0.91864083),
                (58.68240888, 0.75961235),
                (57.82172325, 0.61558297),
                (56.95865505, 0.48659656),
                (56.09346717, 0.37269242),
                (55.22642316, 0.27390523),
                (54.35778714, 0.1902651),
                (53.48782369, 0.12179749),
                (52.61679781, 0.06852326),
                (51.74497484, 0.03045865),
                (50.87262032, 0.00761524),
                (50.0, 0.0),
                (49.12737968, 0.00761524),
                (48.25502516, 0.03045865),
                (47.38320219, 0.06852326),
                (46.51217631, 0.12179749),
                (45.64221286, 0.1902651),
                (44.77357684, 0.27390523),
                (43.90653283, 0.37269242),
                (43.04134495, 0.48659656),
                (42.17827675, 0.61558297),
                (41.31759112, 0.75961235),
                (40.45955023, 0.91864083),
                (39.60441546, 1.09261996),
                (38.75244728, 1.28149676),
                (37.90390522, 1.48521369),
                (37.05904774, 1.70370869),
                (36.21813221, 1.9369152),
                (35.38141476, 2.1847622),
                (34.54915028, 2.44717419),
                (33.72159228, 2.72407122),
                (32.89899283, 3.01536896),
                (32.08160252, 3.32097868),
                (31.26967033, 3.64080727),
                (30.46344358, 3.97475733),
                (29.66316785, 4.32272712),
                (28.86908691, 4.68461065),
                (28.08144266, 5.06029769),
                (27.30047501, 5.44967379),
                (26.52642186, 5.85262036),
                (25.75951899, 6.26901464),
                (25.0, 6.69872981),
                (24.24809625, 7.14163496),
                (23.50403679, 7.59759519),
                (22.76804825, 8.0664716),
                (22.04035483, 8.54812137),
                (21.32117818, 9.04239779),
                (20.61073739, 9.54915028),
                (19.90924884, 10.0682245),
                (19.21692623, 10.59946232),
                (18.53398045, 11.14270193),
                (17.86061952, 11.69777784),
                (17.19704855, 12.26452099),
                (16.54346968, 12.84275873),
                (15.900082, 13.43231492),
                (15.26708148, 14.03300998),
                (14.64466094, 14.64466094),
                (14.03300998, 15.26708148),
                (13.43231492, 15.900082),
                (12.84275873, 16.54346968),
                (12.26452099, 17.19704855),
                (11.69777784, 17.86061952),
                (11.14270193, 18.53398045),
                (10.59946232, 19.21692623),
                (10.0682245, 19.90924884),
                (9.54915028, 20.61073739),
                (9.04239779, 21.32117818),
                (8.54812137, 22.04035483),
                (8.0664716, 22.76804825),
                (7.59759519, 23.50403679),
                (7.14163496, 24.24809625),
                (6.69872981, 25.0),
                (6.26901464, 25.75951899),
                (5.85262036, 26.52642186),
                (5.44967379, 27.30047501),
                (5.06029769, 28.08144266),
                (4.68461065, 28.86908691),
                (4.32272712, 29.66316785),
                (3.97475733, 30.46344358),
                (3.64080727, 31.26967033),
                (3.32097868, 32.08160252),
                (3.01536896, 32.89899283),
                (2.72407122, 33.72159228),
                (2.44717419, 34.54915028),
                (2.1847622, 35.38141476),
                (1.9369152, 36.21813221),
                (1.70370869, 37.05904774),
                (1.48521369, 37.90390522),
                (1.28149676, 38.75244728),
                (1.09261996, 39.60441546),
                (0.91864083, 40.45955023),
                (0.75961235, 41.31759112),
                (0.61558297, 42.17827675),
                (0.48659656, 43.04134495),
                (0.37269242, 43.90653283),
                (0.27390523, 44.77357684),
                (0.1902651, 45.64221286),
                (0.12179749, 46.51217631),
                (0.06852326, 47.38320219),
                (0.03045865, 48.25502516),
                (0.00761524, 49.12737968),
                (0.0, 50.0),
                (0.00761524, 50.87262032),
                (0.03045865, 51.74497484),
                (0.06852326, 52.61679781),
                (0.12179749, 53.48782369),
                (0.1902651, 54.35778714),
                (0.27390523, 55.22642316),
                (0.37269242, 56.09346717),
                (0.48659656, 56.95865505),
                (0.61558297, 57.82172325),
                (0.75961235, 58.68240888),
                (0.91864083, 59.54044977),
                (1.09261996, 60.39558454),
                (1.28149676, 61.24755272),
                (1.48521369, 62.09609478),
                (1.70370869, 62.94095226),
                (1.9369152, 63.78186779),
                (2.1847622, 64.61858524),
                (2.44717419, 65.45084972),
                (2.72407122, 66.27840772),
                (3.01536896, 67.10100717),
                (3.32097868, 67.91839748),
                (3.64080727, 68.73032967),
                (3.97475733, 69.53655642),
                (4.32272712, 70.33683215),
                (4.68461065, 71.13091309),
                (5.06029769, 71.91855734),
                (5.44967379, 72.69952499),
                (5.85262036, 73.47357814),
                (6.26901464, 74.24048101),
                (6.69872981, 75.0),
                (7.14163496, 75.75190375),
                (7.59759519, 76.49596321),
                (8.0664716, 77.23195175),
                (8.54812137, 77.95964517),
                (9.04239779, 78.67882182),
                (9.54915028, 79.38926261),
                (10.0682245, 80.09075116),
                (10.59946232, 80.78307377),
                (11.14270193, 81.46601955),
                (11.69777784, 82.13938048),
                (12.26452099, 82.80295145),
                (12.84275873, 83.45653032),
                (13.43231492, 84.099918),
                (14.03300998, 84.73291852),
                (14.64466094, 85.35533906),
                (15.26708148, 85.96699002),
                (15.900082, 86.56768508),
                (16.54346968, 87.15724127),
                (17.19704855, 87.73547901),
                (17.86061952, 88.30222216),
                (18.53398045, 88.85729807),
                (19.21692623, 89.40053768),
                (19.90924884, 89.9317755),
                (20.61073739, 90.45084972),
                (21.32117818, 90.95760221),
                (22.04035483, 91.45187863),
                (22.76804825, 91.9335284),
                (23.50403679, 92.40240481),
                (24.24809625, 92.85836504),
                (25.0, 93.30127019),
                (25.75951899, 93.73098536),
                (26.52642186, 94.14737964),
                (27.30047501, 94.55032621),
                (28.08144266, 94.93970231),
                (28.86908691, 95.31538935),
                (29.66316785, 95.67727288),
                (30.46344358, 96.02524267),
                (31.26967033, 96.35919273),
                (32.08160252, 96.67902132),
                (32.89899283, 96.98463104),
                (33.72159228, 97.27592878),
                (34.54915028, 97.55282581),
                (35.38141476, 97.8152378),
                (36.21813221, 98.0630848),
                (37.05904774, 98.29629131),
                (37.90390522, 98.51478631),
                (38.75244728, 98.71850324),
                (39.60441546, 98.90738004),
                (40.45955023, 99.08135917),
                (41.31759112, 99.24038765),
                (42.17827675, 99.38441703),
                (43.04134495, 99.51340344),
                (43.90653283, 99.62730758),
                (44.77357684, 99.72609477),
                (45.64221286, 99.8097349),
                (46.51217631, 99.87820251),
                (47.38320219, 99.93147674),
                (48.25502516, 99.96954135),
                (49.12737968, 99.99238476),
                (50.0, 100.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_paper_tape(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a paper tape vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a paper tape vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (62.5, -4.57531755),
                (62.91666667, -4.68274634),
                (63.33333333, -4.78684491),
                (63.75, -4.88758155),
                (64.16666667, -4.98492558),
                (64.58333333, -5.07884734),
                (65.0, -5.16931822),
                (65.41666667, -5.25631067),
                (65.83333333, -5.33979818),
                (66.25, -5.41975533),
                (66.66666667, -5.49615776),
                (67.08333333, -5.56898219),
                (67.5, -5.63820645),
                (67.91666667, -5.70380945),
                (68.33333333, -5.7657712),
                (68.75, -5.82407283),
                (69.16666667, -5.87869658),
                (69.58333333, -5.92962581),
                (70.0, -5.97684501),
                (70.41666667, -6.02033979),
                (70.83333333, -6.06009691),
                (71.25, -6.09610426),
                (71.66666667, -6.12835086),
                (72.08333333, -6.1568269),
                (72.5, -6.18152369),
                (72.91666667, -6.20243373),
                (73.33333333, -6.21955063),
                (73.75, -6.23286918),
                (74.16666667, -6.24238534),
                (74.58333333, -6.24809619),
                (75.0, -6.25),
                (75.41666667, -6.24809619),
                (75.83333333, -6.24238534),
                (76.25, -6.23286918),
                (76.66666667, -6.21955063),
                (77.08333333, -6.20243373),
                (77.5, -6.18152369),
                (77.91666667, -6.1568269),
                (78.33333333, -6.12835086),
                (78.75, -6.09610426),
                (79.16666667, -6.06009691),
                (79.58333333, -6.02033979),
                (80.0, -5.97684501),
                (80.41666667, -5.92962581),
                (80.83333333, -5.87869658),
                (81.25, -5.82407283),
                (81.66666667, -5.7657712),
                (82.08333333, -5.70380945),
                (82.5, -5.63820645),
                (82.91666667, -5.56898219),
                (83.33333333, -5.49615776),
                (83.75, -5.41975533),
                (84.16666667, -5.33979818),
                (84.58333333, -5.25631067),
                (85.0, -5.16931822),
                (85.41666667, -5.07884734),
                (85.83333333, -4.98492558),
                (86.25, -4.88758155),
                (86.66666667, -4.78684491),
                (87.08333333, -4.68274634),
                (87.5, -4.57531755),
                (87.91666667, -4.46459126),
                (88.33333333, -4.3506012),
                (88.75, -4.2333821),
                (89.16666667, -4.11296966),
                (89.58333333, -3.98940055),
                (90.0, -3.86271243),
                (90.41666667, -3.73294388),
                (90.83333333, -3.60013442),
                (91.25, -3.46432452),
                (91.66666667, -3.32555554),
                (92.08333333, -3.18386975),
                (92.5, -3.03931032),
                (92.91666667, -2.89192127),
                (93.33333333, -2.7417475),
                (93.75, -2.58883476),
                (94.16666667, -2.43322963),
                (94.58333333, -2.2749795),
                (95.0, -2.11413258),
                (95.41666667, -1.95073786),
                (95.83333333, -1.78484512),
                (96.25, -1.61650489),
                (96.66666667, -1.44576844),
                (97.08333333, -1.27268779),
                (97.5, -1.09731565),
                (97.91666667, -0.91970545),
                (98.33333333, -0.73991129),
                (98.75, -0.55798794),
                (99.16666667, -0.3739908),
                (99.58333333, -0.18797594),
                (100.0, -0.0),
                (100.41666667, 0.18987975),
                (100.83333333, 0.38160547),
                (101.25, 0.57511875),
                (101.66666667, 0.77036067),
                (102.08333333, 0.96727173),
                (102.5, 1.16579196),
                (102.91666667, 1.36586089),
                (103.33333333, 1.56741758),
                (103.75, 1.77040063),
                (104.16666667, 1.97474821),
                (104.58333333, 2.18039807),
                (105.0, 2.38728757),
                (105.41666667, 2.59535369),
                (105.83333333, 2.80453305),
                (106.25, 3.01476194),
                (106.66666667, 3.22597631),
                (107.08333333, 3.43811182),
                (107.5, 3.65110386),
                (107.91666667, 3.86488756),
                (108.33333333, 4.07939778),
                (108.75, 4.29456919),
                (109.16666667, 4.51033624),
                (109.58333333, 4.72663321),
                (110.0, 4.94339421),
                (110.41666667, 5.16055322),
                (110.83333333, 5.37804408),
                (111.25, 5.59580055),
                (111.66666667, 5.81375629),
                (112.08333333, 6.03184492),
                (112.5, 6.25),
                (112.91666667, 6.46815508),
                (113.33333333, 6.68624371),
                (113.75, 6.90419945),
                (114.16666667, 7.12195592),
                (114.58333333, 7.33944678),
                (115.0, 7.55660579),
                (115.41666667, 7.77336679),
                (115.83333333, 7.98966376),
                (116.25, 8.20543081),
                (116.66666667, 8.42060222),
                (117.08333333, 8.63511244),
                (117.5, 8.84889614),
                (117.91666667, 9.06188818),
                (118.33333333, 9.27402369),
                (118.75, 9.48523806),
                (119.16666667, 9.69546695),
                (119.58333333, 9.90464631),
                (120.0, 10.11271243),
                (120.41666667, 10.31960193),
                (120.83333333, 10.52525179),
                (121.25, 10.72959937),
                (121.66666667, 10.93258242),
                (122.08333333, 11.13413911),
                (122.5, 11.33420804),
                (122.91666667, 11.53272827),
                (123.33333333, 11.72963933),
                (123.75, 11.92488125),
                (124.16666667, 12.11839453),
                (124.58333333, 12.31012025),
                (125.0, 12.5),
                (125.41666667, 12.68797594),
                (125.83333333, 12.8739908),
                (126.25, 13.05798794),
                (126.66666667, 13.23991129),
                (127.08333333, 13.41970545),
                (127.5, 13.59731565),
                (127.91666667, 13.77268779),
                (128.33333333, 13.94576844),
                (128.75, 14.11650489),
                (129.16666667, 14.28484512),
                (129.58333333, 14.45073786),
                (130.0, 14.61413258),
                (130.41666667, 14.7749795),
                (130.83333333, 14.93322963),
                (131.25, 15.08883476),
                (131.66666667, 15.2417475),
                (132.08333333, 15.39192127),
                (132.5, 15.53931032),
                (132.91666667, 15.68386975),
                (133.33333333, 15.82555554),
                (133.75, 15.96432452),
                (134.16666667, 16.10013442),
                (134.58333333, 16.23294388),
                (135.0, 16.36271243),
                (135.41666667, 16.48940055),
                (135.83333333, 16.61296966),
                (136.25, 16.7333821),
                (136.66666667, 16.8506012),
                (137.08333333, 16.96459126),
                (137.5, 17.07531755),
                (137.91666667, 17.18274634),
                (138.33333333, 17.28684491),
                (138.75, 17.38758155),
                (139.16666667, 17.48492558),
                (139.58333333, 17.57884734),
                (140.0, 17.66931822),
                (140.41666667, 17.75631067),
                (140.83333333, 17.83979818),
                (141.25, 17.91975533),
                (141.66666667, 17.99615776),
                (142.08333333, 18.06898219),
                (142.5, 18.13820645),
                (142.91666667, 18.20380945),
                (143.33333333, 18.2657712),
                (143.75, 18.32407283),
                (144.16666667, 18.37869658),
                (144.58333333, 18.42962581),
                (145.0, 18.47684501),
                (145.41666667, 18.52033979),
                (145.83333333, 18.56009691),
                (146.25, 18.59610426),
                (146.66666667, 18.62835086),
                (147.08333333, 18.6568269),
                (147.5, 18.68152369),
                (147.91666667, 18.70243373),
                (148.33333333, 18.71955063),
                (148.75, 18.73286918),
                (149.16666667, 18.74238534),
                (149.58333333, 18.74809619),
                (150.0, 18.75),
                (150.41666667, 18.74809619),
                (150.83333333, 18.74238534),
                (151.25, 18.73286918),
                (151.66666667, 18.71955063),
                (152.08333333, 18.70243373),
                (152.5, 18.68152369),
                (152.91666667, 18.6568269),
                (153.33333333, 18.62835086),
                (153.75, 18.59610426),
                (154.16666667, 18.56009691),
                (154.58333333, 18.52033979),
                (155.0, 18.47684501),
                (155.41666667, 18.42962581),
                (155.83333333, 18.37869658),
                (156.25, 18.32407283),
                (156.66666667, 18.2657712),
                (157.08333333, 18.20380945),
                (157.5, 18.13820645),
                (157.91666667, 18.06898219),
                (158.33333333, 17.99615776),
                (158.75, 17.91975533),
                (159.16666667, 17.83979818),
                (159.58333333, 17.75631067),
                (160.0, 17.66931822),
                (160.41666667, 17.57884734),
                (160.83333333, 17.48492558),
                (161.25, 17.38758155),
                (161.66666667, 17.28684491),
                (162.08333333, 17.18274634),
                (162.08333333, 117.18274634),
                (161.66666667, 117.28684491),
                (161.25, 117.38758155),
                (160.83333333, 117.48492558),
                (160.41666667, 117.57884734),
                (160.0, 117.66931822),
                (159.58333333, 117.75631067),
                (159.16666667, 117.83979818),
                (158.75, 117.91975533),
                (158.33333333, 117.99615776),
                (157.91666667, 118.06898219),
                (157.5, 118.13820645),
                (157.08333333, 118.20380945),
                (156.66666667, 118.2657712),
                (156.25, 118.32407283),
                (155.83333333, 118.37869658),
                (155.41666667, 118.42962581),
                (155.0, 118.47684501),
                (154.58333333, 118.52033979),
                (154.16666667, 118.56009691),
                (153.75, 118.59610426),
                (153.33333333, 118.62835086),
                (152.91666667, 118.6568269),
                (152.5, 118.68152369),
                (152.08333333, 118.70243373),
                (151.66666667, 118.71955063),
                (151.25, 118.73286918),
                (150.83333333, 118.74238534),
                (150.41666667, 118.74809619),
                (150.0, 118.75),
                (149.58333333, 118.74809619),
                (149.16666667, 118.74238534),
                (148.75, 118.73286918),
                (148.33333333, 118.71955063),
                (147.91666667, 118.70243373),
                (147.5, 118.68152369),
                (147.08333333, 118.6568269),
                (146.66666667, 118.62835086),
                (146.25, 118.59610426),
                (145.83333333, 118.56009691),
                (145.41666667, 118.52033979),
                (145.0, 118.47684501),
                (144.58333333, 118.42962581),
                (144.16666667, 118.37869658),
                (143.75, 118.32407283),
                (143.33333333, 118.2657712),
                (142.91666667, 118.20380945),
                (142.5, 118.13820645),
                (142.08333333, 118.06898219),
                (141.66666667, 117.99615776),
                (141.25, 117.91975533),
                (140.83333333, 117.83979818),
                (140.41666667, 117.75631067),
                (140.0, 117.66931822),
                (139.58333333, 117.57884734),
                (139.16666667, 117.48492558),
                (138.75, 117.38758155),
                (138.33333333, 117.28684491),
                (137.91666667, 117.18274634),
                (137.5, 117.07531755),
                (137.08333333, 116.96459126),
                (136.66666667, 116.8506012),
                (136.25, 116.7333821),
                (135.83333333, 116.61296966),
                (135.41666667, 116.48940055),
                (135.0, 116.36271243),
                (134.58333333, 116.23294388),
                (134.16666667, 116.10013442),
                (133.75, 115.96432452),
                (133.33333333, 115.82555554),
                (132.91666667, 115.68386975),
                (132.5, 115.53931032),
                (132.08333333, 115.39192127),
                (131.66666667, 115.2417475),
                (131.25, 115.08883476),
                (130.83333333, 114.93322963),
                (130.41666667, 114.7749795),
                (130.0, 114.61413258),
                (129.58333333, 114.45073786),
                (129.16666667, 114.28484512),
                (128.75, 114.11650489),
                (128.33333333, 113.94576844),
                (127.91666667, 113.77268779),
                (127.5, 113.59731565),
                (127.08333333, 113.41970545),
                (126.66666667, 113.23991129),
                (126.25, 113.05798794),
                (125.83333333, 112.8739908),
                (125.41666667, 112.68797594),
                (125.0, 112.5),
                (124.58333333, 112.31012025),
                (124.16666667, 112.11839453),
                (123.75, 111.92488125),
                (123.33333333, 111.72963933),
                (122.91666667, 111.53272827),
                (122.5, 111.33420804),
                (122.08333333, 111.13413911),
                (121.66666667, 110.93258242),
                (121.25, 110.72959937),
                (120.83333333, 110.52525179),
                (120.41666667, 110.31960193),
                (120.0, 110.11271243),
                (119.58333333, 109.90464631),
                (119.16666667, 109.69546695),
                (118.75, 109.48523806),
                (118.33333333, 109.27402369),
                (117.91666667, 109.06188818),
                (117.5, 108.84889614),
                (117.08333333, 108.63511244),
                (116.66666667, 108.42060222),
                (116.25, 108.20543081),
                (115.83333333, 107.98966376),
                (115.41666667, 107.77336679),
                (115.0, 107.55660579),
                (114.58333333, 107.33944678),
                (114.16666667, 107.12195592),
                (113.75, 106.90419945),
                (113.33333333, 106.68624371),
                (112.91666667, 106.46815508),
                (112.5, 106.25),
                (112.08333333, 106.03184492),
                (111.66666667, 105.81375629),
                (111.25, 105.59580055),
                (110.83333333, 105.37804408),
                (110.41666667, 105.16055322),
                (110.0, 104.94339421),
                (109.58333333, 104.72663321),
                (109.16666667, 104.51033624),
                (108.75, 104.29456919),
                (108.33333333, 104.07939778),
                (107.91666667, 103.86488756),
                (107.5, 103.65110386),
                (107.08333333, 103.43811182),
                (106.66666667, 103.22597631),
                (106.25, 103.01476194),
                (105.83333333, 102.80453305),
                (105.41666667, 102.59535369),
                (105.0, 102.38728757),
                (104.58333333, 102.18039807),
                (104.16666667, 101.97474821),
                (103.75, 101.77040063),
                (103.33333333, 101.56741758),
                (102.91666667, 101.36586089),
                (102.5, 101.16579196),
                (102.08333333, 100.96727173),
                (101.66666667, 100.77036067),
                (101.25, 100.57511875),
                (100.83333333, 100.38160547),
                (100.41666667, 100.18987975),
                (100.0, 100.0),
                (99.58333333, 99.81202406),
                (99.16666667, 99.6260092),
                (98.75, 99.44201206),
                (98.33333333, 99.26008871),
                (97.91666667, 99.08029455),
                (97.5, 98.90268435),
                (97.08333333, 98.72731221),
                (96.66666667, 98.55423156),
                (96.25, 98.38349511),
                (95.83333333, 98.21515488),
                (95.41666667, 98.04926214),
                (95.0, 97.88586742),
                (94.58333333, 97.7250205),
                (94.16666667, 97.56677037),
                (93.75, 97.41116524),
                (93.33333333, 97.2582525),
                (92.91666667, 97.10807873),
                (92.5, 96.96068968),
                (92.08333333, 96.81613025),
                (91.66666667, 96.67444446),
                (91.25, 96.53567548),
                (90.83333333, 96.39986558),
                (90.41666667, 96.26705612),
                (90.0, 96.13728757),
                (89.58333333, 96.01059945),
                (89.16666667, 95.88703034),
                (88.75, 95.7666179),
                (88.33333333, 95.6493988),
                (87.91666667, 95.53540874),
                (87.5, 95.42468245),
                (87.08333333, 95.31725366),
                (86.66666667, 95.21315509),
                (86.25, 95.11241845),
                (85.83333333, 95.01507442),
                (85.41666667, 94.92115266),
                (85.0, 94.83068178),
                (84.58333333, 94.74368933),
                (84.16666667, 94.66020182),
                (83.75, 94.58024467),
                (83.33333333, 94.50384224),
                (82.91666667, 94.43101781),
                (82.5, 94.36179355),
                (82.08333333, 94.29619055),
                (81.66666667, 94.2342288),
                (81.25, 94.17592717),
                (80.83333333, 94.12130342),
                (80.41666667, 94.07037419),
                (80.0, 94.02315499),
                (79.58333333, 93.97966021),
                (79.16666667, 93.93990309),
                (78.75, 93.90389574),
                (78.33333333, 93.87164914),
                (77.91666667, 93.8431731),
                (77.5, 93.81847631),
                (77.08333333, 93.79756627),
                (76.66666667, 93.78044937),
                (76.25, 93.76713082),
                (75.83333333, 93.75761466),
                (75.41666667, 93.75190381),
                (75.0, 93.75),
                (74.58333333, 93.75190381),
                (74.16666667, 93.75761466),
                (73.75, 93.76713082),
                (73.33333333, 93.78044937),
                (72.91666667, 93.79756627),
                (72.5, 93.81847631),
                (72.08333333, 93.8431731),
                (71.66666667, 93.87164914),
                (71.25, 93.90389574),
                (70.83333333, 93.93990309),
                (70.41666667, 93.97966021),
                (70.0, 94.02315499),
                (69.58333333, 94.07037419),
                (69.16666667, 94.12130342),
                (68.75, 94.17592717),
                (68.33333333, 94.2342288),
                (67.91666667, 94.29619055),
                (67.5, 94.36179355),
                (67.08333333, 94.43101781),
                (66.66666667, 94.50384224),
                (66.25, 94.58024467),
                (65.83333333, 94.66020182),
                (65.41666667, 94.74368933),
                (65.0, 94.83068178),
                (64.58333333, 94.92115266),
                (64.16666667, 95.01507442),
                (63.75, 95.11241845),
                (63.33333333, 95.21315509),
                (62.91666667, 95.31725366),
                (62.5, 95.42468245),
                (62.5, -4.57531755),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def flowchart_predefined_document(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a predefined document vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a predefined document vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (62.5, -4.57531755),
                (62.91666667, -4.68274634),
                (63.33333333, -4.78684491),
                (63.75, -4.88758155),
                (64.16666667, -4.98492558),
                (64.58333333, -5.07884734),
                (65.0, -5.16931822),
                (65.41666667, -5.25631067),
                (65.83333333, -5.33979818),
                (66.25, -5.41975533),
                (66.66666667, -5.49615776),
                (67.08333333, -5.56898219),
                (67.5, -5.63820645),
                (67.91666667, -5.70380945),
                (68.33333333, -5.7657712),
                (68.75, -5.82407283),
                (69.16666667, -5.87869658),
                (69.58333333, -5.92962581),
                (70.0, -5.97684501),
                (70.41666667, -6.02033979),
                (70.83333333, -6.06009691),
                (71.25, -6.09610426),
                (71.66666667, -6.12835086),
                (72.08333333, -6.1568269),
                (72.5, -6.18152369),
                (72.5, 100),
                (72.5, -6.18152369),
                (72.91666667, -6.20243373),
                (73.33333333, -6.21955063),
                (73.75, -6.23286918),
                (74.16666667, -6.24238534),
                (74.58333333, -6.24809619),
                (75.0, -6.25),
                (75.41666667, -6.24809619),
                (75.83333333, -6.24238534),
                (76.25, -6.23286918),
                (76.66666667, -6.21955063),
                (77.08333333, -6.20243373),
                (77.5, -6.18152369),
                (77.91666667, -6.1568269),
                (78.33333333, -6.12835086),
                (78.75, -6.09610426),
                (79.16666667, -6.06009691),
                (79.58333333, -6.02033979),
                (80.0, -5.97684501),
                (80.41666667, -5.92962581),
                (80.83333333, -5.87869658),
                (81.25, -5.82407283),
                (81.66666667, -5.7657712),
                (82.08333333, -5.70380945),
                (82.5, -5.63820645),
                (82.91666667, -5.56898219),
                (83.33333333, -5.49615776),
                (83.75, -5.41975533),
                (84.16666667, -5.33979818),
                (84.58333333, -5.25631067),
                (85.0, -5.16931822),
                (85.41666667, -5.07884734),
                (85.83333333, -4.98492558),
                (86.25, -4.88758155),
                (86.66666667, -4.78684491),
                (87.08333333, -4.68274634),
                (87.5, -4.57531755),
                (87.91666667, -4.46459126),
                (88.33333333, -4.3506012),
                (88.75, -4.2333821),
                (89.16666667, -4.11296966),
                (89.58333333, -3.98940055),
                (90.0, -3.86271243),
                (90.41666667, -3.73294388),
                (90.83333333, -3.60013442),
                (91.25, -3.46432452),
                (91.66666667, -3.32555554),
                (92.08333333, -3.18386975),
                (92.5, -3.03931032),
                (92.91666667, -2.89192127),
                (93.33333333, -2.7417475),
                (93.75, -2.58883476),
                (94.16666667, -2.43322963),
                (94.58333333, -2.2749795),
                (95.0, -2.11413258),
                (95.41666667, -1.95073786),
                (95.83333333, -1.78484512),
                (96.25, -1.61650489),
                (96.66666667, -1.44576844),
                (97.08333333, -1.27268779),
                (97.5, -1.09731565),
                (97.91666667, -0.91970545),
                (98.33333333, -0.73991129),
                (98.75, -0.55798794),
                (99.16666667, -0.3739908),
                (99.58333333, -0.18797594),
                (100.0, -0.0),
                (100.41666667, 0.18987975),
                (100.83333333, 0.38160547),
                (101.25, 0.57511875),
                (101.66666667, 0.77036067),
                (102.08333333, 0.96727173),
                (102.5, 1.16579196),
                (102.91666667, 1.36586089),
                (103.33333333, 1.56741758),
                (103.75, 1.77040063),
                (104.16666667, 1.97474821),
                (104.58333333, 2.18039807),
                (105.0, 2.38728757),
                (105.41666667, 2.59535369),
                (105.83333333, 2.80453305),
                (106.25, 3.01476194),
                (106.66666667, 3.22597631),
                (107.08333333, 3.43811182),
                (107.5, 3.65110386),
                (107.91666667, 3.86488756),
                (108.33333333, 4.07939778),
                (108.75, 4.29456919),
                (109.16666667, 4.51033624),
                (109.58333333, 4.72663321),
                (110.0, 4.94339421),
                (110.41666667, 5.16055322),
                (110.83333333, 5.37804408),
                (111.25, 5.59580055),
                (111.66666667, 5.81375629),
                (112.08333333, 6.03184492),
                (112.5, 6.25),
                (112.91666667, 6.46815508),
                (113.33333333, 6.68624371),
                (113.75, 6.90419945),
                (114.16666667, 7.12195592),
                (114.58333333, 7.33944678),
                (115.0, 7.55660579),
                (115.41666667, 7.77336679),
                (115.83333333, 7.98966376),
                (116.25, 8.20543081),
                (116.66666667, 8.42060222),
                (117.08333333, 8.63511244),
                (117.5, 8.84889614),
                (117.91666667, 9.06188818),
                (118.33333333, 9.27402369),
                (118.75, 9.48523806),
                (119.16666667, 9.69546695),
                (119.58333333, 9.90464631),
                (120.0, 10.11271243),
                (120.41666667, 10.31960193),
                (120.83333333, 10.52525179),
                (121.25, 10.72959937),
                (121.66666667, 10.93258242),
                (122.08333333, 11.13413911),
                (122.5, 11.33420804),
                (122.91666667, 11.53272827),
                (123.33333333, 11.72963933),
                (123.75, 11.92488125),
                (124.16666667, 12.11839453),
                (124.58333333, 12.31012025),
                (125.0, 12.5),
                (125.41666667, 12.68797594),
                (125.83333333, 12.8739908),
                (126.25, 13.05798794),
                (126.66666667, 13.23991129),
                (127.08333333, 13.41970545),
                (127.5, 13.59731565),
                (127.91666667, 13.77268779),
                (128.33333333, 13.94576844),
                (128.75, 14.11650489),
                (129.16666667, 14.28484512),
                (129.58333333, 14.45073786),
                (130.0, 14.61413258),
                (130.41666667, 14.7749795),
                (130.83333333, 14.93322963),
                (131.25, 15.08883476),
                (131.66666667, 15.2417475),
                (132.08333333, 15.39192127),
                (132.5, 15.53931032),
                (132.91666667, 15.68386975),
                (133.33333333, 15.82555554),
                (133.75, 15.96432452),
                (134.16666667, 16.10013442),
                (134.58333333, 16.23294388),
                (135.0, 16.36271243),
                (135.41666667, 16.48940055),
                (135.83333333, 16.61296966),
                (136.25, 16.7333821),
                (136.66666667, 16.8506012),
                (137.08333333, 16.96459126),
                (137.5, 17.07531755),
                (137.91666667, 17.18274634),
                (138.33333333, 17.28684491),
                (138.75, 17.38758155),
                (139.16666667, 17.48492558),
                (139.58333333, 17.57884734),
                (140.0, 17.66931822),
                (140.41666667, 17.75631067),
                (140.83333333, 17.83979818),
                (141.25, 17.91975533),
                (141.66666667, 17.99615776),
                (142.08333333, 18.06898219),
                (142.5, 18.13820645),
                (142.91666667, 18.20380945),
                (143.33333333, 18.2657712),
                (143.75, 18.32407283),
                (144.16666667, 18.37869658),
                (144.58333333, 18.42962581),
                (145.0, 18.47684501),
                (145.41666667, 18.52033979),
                (145.83333333, 18.56009691),
                (146.25, 18.59610426),
                (146.66666667, 18.62835086),
                (147.08333333, 18.6568269),
                (147.5, 18.68152369),
                (147.91666667, 18.70243373),
                (148.33333333, 18.71955063),
                (148.75, 18.73286918),
                (149.16666667, 18.74238534),
                (149.58333333, 18.74809619),
                (150.0, 18.75),
                (150.41666667, 18.74809619),
                (150.83333333, 18.74238534),
                (151.25, 18.73286918),
                (151.66666667, 18.71955063),
                (152.08333333, 18.70243373),
                (152.08333333, 100),
                (152.08333333, 18.70243373),
                (152.5, 18.68152369),
                (152.91666667, 18.6568269),
                (153.33333333, 18.62835086),
                (153.75, 18.59610426),
                (154.16666667, 18.56009691),
                (154.58333333, 18.52033979),
                (155.0, 18.47684501),
                (155.41666667, 18.42962581),
                (155.83333333, 18.37869658),
                (156.25, 18.32407283),
                (156.66666667, 18.2657712),
                (157.08333333, 18.20380945),
                (157.5, 18.13820645),
                (157.91666667, 18.06898219),
                (158.33333333, 17.99615776),
                (158.75, 17.91975533),
                (159.16666667, 17.83979818),
                (159.58333333, 17.75631067),
                (160.0, 17.66931822),
                (160.41666667, 17.57884734),
                (160.83333333, 17.48492558),
                (161.25, 17.38758155),
                (161.66666667, 17.28684491),
                (162.08333333, 17.18274634),
                (162.08333333, 100.0),
                (62.5, 100.0),
                (62.5, -4.57531755),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def flowchart_predefined_process(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a predefined process vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a predefined process vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 100.0),
                (100.0, 100.0),
                (100.0, 0.0),
                (90.0, 0.0),
                (90.0, 100.0),
                (90.0, 0.0),
                (10.0, 0.0),
                (10.0, 100.0),
                (10.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_preparation(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a preparation vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a preparation vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 50.0),
                (25.0, 100.0),
                (75.0, 100.0),
                (100.0, 50.0),
                (75.0, 0.0),
                (25.0, 0.0),
                (0.0, 50.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_process(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a process vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a process vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (100.0, 0.0),
                (100.0, 100.0),
                (0.0, 100.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_process_iso_9000(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an ISO-9000 process vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        an ISO-9000 process vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (20.0, 50.0),
                (0.0, 100.0),
                (80.0, 100.0),
                (100.0, 50.0),
                (80.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_sequential_data(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a sequential data vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a sequential data vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (50.0, 0.0),
                (49.12737968, 0.00761524),
                (48.25502516, 0.03045865),
                (47.38320219, 0.06852326),
                (46.51217631, 0.12179749),
                (45.64221286, 0.1902651),
                (44.77357684, 0.27390523),
                (43.90653283, 0.37269242),
                (43.04134495, 0.48659656),
                (42.17827675, 0.61558297),
                (41.31759112, 0.75961235),
                (40.45955023, 0.91864083),
                (39.60441546, 1.09261996),
                (38.75244728, 1.28149676),
                (37.90390522, 1.48521369),
                (37.05904774, 1.70370869),
                (36.21813221, 1.9369152),
                (35.38141476, 2.1847622),
                (34.54915028, 2.44717419),
                (33.72159228, 2.72407122),
                (32.89899283, 3.01536896),
                (32.08160252, 3.32097868),
                (31.26967033, 3.64080727),
                (30.46344358, 3.97475733),
                (29.66316785, 4.32272712),
                (28.86908691, 4.68461065),
                (28.08144266, 5.06029769),
                (27.30047501, 5.44967379),
                (26.52642186, 5.85262036),
                (25.75951899, 6.26901464),
                (25.0, 6.69872981),
                (24.24809625, 7.14163496),
                (23.50403679, 7.59759519),
                (22.76804825, 8.0664716),
                (22.04035483, 8.54812137),
                (21.32117818, 9.04239779),
                (20.61073739, 9.54915028),
                (19.90924884, 10.0682245),
                (19.21692623, 10.59946232),
                (18.53398045, 11.14270193),
                (17.86061952, 11.69777784),
                (17.19704855, 12.26452099),
                (16.54346968, 12.84275873),
                (15.900082, 13.43231492),
                (15.26708148, 14.03300998),
                (14.64466094, 14.64466094),
                (14.03300998, 15.26708148),
                (13.43231492, 15.900082),
                (12.84275873, 16.54346968),
                (12.26452099, 17.19704855),
                (11.69777784, 17.86061952),
                (11.14270193, 18.53398045),
                (10.59946232, 19.21692623),
                (10.0682245, 19.90924884),
                (9.54915028, 20.61073739),
                (9.04239779, 21.32117818),
                (8.54812137, 22.04035483),
                (8.0664716, 22.76804825),
                (7.59759519, 23.50403679),
                (7.14163496, 24.24809625),
                (6.69872981, 25.0),
                (6.26901464, 25.75951899),
                (5.85262036, 26.52642186),
                (5.44967379, 27.30047501),
                (5.06029769, 28.08144266),
                (4.68461065, 28.86908691),
                (4.32272712, 29.66316785),
                (3.97475733, 30.46344358),
                (3.64080727, 31.26967033),
                (3.32097868, 32.08160252),
                (3.01536896, 32.89899283),
                (2.72407122, 33.72159228),
                (2.44717419, 34.54915028),
                (2.1847622, 35.38141476),
                (1.9369152, 36.21813221),
                (1.70370869, 37.05904774),
                (1.48521369, 37.90390522),
                (1.28149676, 38.75244728),
                (1.09261996, 39.60441546),
                (0.91864083, 40.45955023),
                (0.75961235, 41.31759112),
                (0.61558297, 42.17827675),
                (0.48659656, 43.04134495),
                (0.37269242, 43.90653283),
                (0.27390523, 44.77357684),
                (0.1902651, 45.64221286),
                (0.12179749, 46.51217631),
                (0.06852326, 47.38320219),
                (0.03045865, 48.25502516),
                (0.00761524, 49.12737968),
                (0.0, 50.0),
                (0.00761524, 50.87262032),
                (0.03045865, 51.74497484),
                (0.06852326, 52.61679781),
                (0.12179749, 53.48782369),
                (0.1902651, 54.35778714),
                (0.27390523, 55.22642316),
                (0.37269242, 56.09346717),
                (0.48659656, 56.95865505),
                (0.61558297, 57.82172325),
                (0.75961235, 58.68240888),
                (0.91864083, 59.54044977),
                (1.09261996, 60.39558454),
                (1.28149676, 61.24755272),
                (1.48521369, 62.09609478),
                (1.70370869, 62.94095226),
                (1.9369152, 63.78186779),
                (2.1847622, 64.61858524),
                (2.44717419, 65.45084972),
                (2.72407122, 66.27840772),
                (3.01536896, 67.10100717),
                (3.32097868, 67.91839748),
                (3.64080727, 68.73032967),
                (3.97475733, 69.53655642),
                (4.32272712, 70.33683215),
                (4.68461065, 71.13091309),
                (5.06029769, 71.91855734),
                (5.44967379, 72.69952499),
                (5.85262036, 73.47357814),
                (6.26901464, 74.24048101),
                (6.69872981, 75.0),
                (7.14163496, 75.75190375),
                (7.59759519, 76.49596321),
                (8.0664716, 77.23195175),
                (8.54812137, 77.95964517),
                (9.04239779, 78.67882182),
                (9.54915028, 79.38926261),
                (10.0682245, 80.09075116),
                (10.59946232, 80.78307377),
                (11.14270193, 81.46601955),
                (11.69777784, 82.13938048),
                (12.26452099, 82.80295145),
                (12.84275873, 83.45653032),
                (13.43231492, 84.099918),
                (14.03300998, 84.73291852),
                (14.64466094, 85.35533906),
                (15.26708148, 85.96699002),
                (15.900082, 86.56768508),
                (16.54346968, 87.15724127),
                (17.19704855, 87.73547901),
                (17.86061952, 88.30222216),
                (18.53398045, 88.85729807),
                (19.21692623, 89.40053768),
                (19.90924884, 89.9317755),
                (20.61073739, 90.45084972),
                (21.32117818, 90.95760221),
                (22.04035483, 91.45187863),
                (22.76804825, 91.9335284),
                (23.50403679, 92.40240481),
                (24.24809625, 92.85836504),
                (25.0, 93.30127019),
                (25.75951899, 93.73098536),
                (26.52642186, 94.14737964),
                (27.30047501, 94.55032621),
                (28.08144266, 94.93970231),
                (28.86908691, 95.31538935),
                (29.66316785, 95.67727288),
                (30.46344358, 96.02524267),
                (31.26967033, 96.35919273),
                (32.08160252, 96.67902132),
                (32.89899283, 96.98463104),
                (33.72159228, 97.27592878),
                (34.54915028, 97.55282581),
                (35.38141476, 97.8152378),
                (36.21813221, 98.0630848),
                (37.05904774, 98.29629131),
                (37.90390522, 98.51478631),
                (38.75244728, 98.71850324),
                (39.60441546, 98.90738004),
                (40.45955023, 99.08135917),
                (41.31759112, 99.24038765),
                (42.17827675, 99.38441703),
                (43.04134495, 99.51340344),
                (43.90653283, 99.62730758),
                (44.77357684, 99.72609477),
                (45.64221286, 99.8097349),
                (46.51217631, 99.87820251),
                (47.38320219, 99.93147674),
                (48.25502516, 99.96954135),
                (49.12737968, 99.99238476),
                (50.0, 100.0),
                (50.87262032, 99.99238476),
                (51.74497484, 99.96954135),
                (52.61679781, 99.93147674),
                (53.48782369, 99.87820251),
                (54.35778714, 99.8097349),
                (55.22642316, 99.72609477),
                (56.09346717, 99.62730758),
                (56.95865505, 99.51340344),
                (57.82172325, 99.38441703),
                (58.68240888, 99.24038765),
                (59.54044977, 99.08135917),
                (60.39558454, 98.90738004),
                (61.24755272, 98.71850324),
                (62.09609478, 98.51478631),
                (62.94095226, 98.29629131),
                (63.78186779, 98.0630848),
                (64.61858524, 97.8152378),
                (65.45084972, 97.55282581),
                (66.27840772, 97.27592878),
                (67.10100717, 96.98463104),
                (67.91839748, 96.67902132),
                (68.73032967, 96.35919273),
                (69.53655642, 96.02524267),
                (70.33683215, 95.67727288),
                (71.13091309, 95.31538935),
                (71.91855734, 94.93970231),
                (72.69952499, 94.55032621),
                (73.47357814, 94.14737964),
                (74.24048101, 93.73098536),
                (75.0, 93.30127019),
                (75.75190375, 92.85836504),
                (76.49596321, 92.40240481),
                (77.23195175, 91.9335284),
                (77.95964517, 91.45187863),
                (78.67882182, 90.95760221),
                (79.38926261, 90.45084972),
                (80.09075116, 89.9317755),
                (80.78307377, 89.40053768),
                (81.46601955, 88.85729807),
                (82.13938048, 88.30222216),
                (82.80295145, 87.73547901),
                (83.45653032, 87.15724127),
                (84.099918, 86.56768508),
                (84.73291852, 85.96699002),
                (85.35533906, 85.35533906),
                (85.96699002, 84.73291852),
                (86.56768508, 84.099918),
                (87.15724127, 83.45653032),
                (87.73547901, 82.80295145),
                (88.30222216, 82.13938048),
                (88.85729807, 81.46601955),
                (89.40053768, 80.78307377),
                (89.9317755, 80.09075116),
                (90.45084972, 79.38926261),
                (90.95760221, 78.67882182),
                (91.45187863, 77.95964517),
                (91.9335284, 77.23195175),
                (92.40240481, 76.49596321),
                (92.85836504, 75.75190375),
                (93.30127019, 75.0),
                (93.73098536, 74.24048101),
                (94.14737964, 73.47357814),
                (94.55032621, 72.69952499),
                (94.93970231, 71.91855734),
                (95.31538935, 71.13091309),
                (95.67727288, 70.33683215),
                (96.02524267, 69.53655642),
                (96.35919273, 68.73032967),
                (96.67902132, 67.91839748),
                (96.98463104, 67.10100717),
                (97.27592878, 66.27840772),
                (97.55282581, 65.45084972),
                (97.8152378, 64.61858524),
                (98.0630848, 63.78186779),
                (98.29629131, 62.94095226),
                (98.51478631, 62.09609478),
                (98.71850324, 61.24755272),
                (98.90738004, 60.39558454),
                (99.08135917, 59.54044977),
                (99.24038765, 58.68240888),
                (99.38441703, 57.82172325),
                (99.51340344, 56.95865505),
                (99.62730758, 56.09346717),
                (99.72609477, 55.22642316),
                (99.8097349, 54.35778714),
                (99.87820251, 53.48782369),
                (99.93147674, 52.61679781),
                (99.96954135, 51.74497484),
                (99.99238476, 50.87262032),
                (100.0, 50.0),
                (99.99238476, 49.12737968),
                (99.96954135, 48.25502516),
                (99.93147674, 47.38320219),
                (99.87820251, 46.51217631),
                (99.8097349, 45.64221286),
                (99.72609477, 44.77357684),
                (99.62730758, 43.90653283),
                (99.51340344, 43.04134495),
                (99.38441703, 42.17827675),
                (99.24038765, 41.31759112),
                (99.08135917, 40.45955023),
                (98.90738004, 39.60441546),
                (98.71850324, 38.75244728),
                (98.51478631, 37.90390522),
                (98.29629131, 37.05904774),
                (98.0630848, 36.21813221),
                (97.8152378, 35.38141476),
                (97.55282581, 34.54915028),
                (97.27592878, 33.72159228),
                (96.98463104, 32.89899283),
                (96.67902132, 32.08160252),
                (96.35919273, 31.26967033),
                (96.02524267, 30.46344358),
                (95.67727288, 29.66316785),
                (95.31538935, 28.86908691),
                (94.93970231, 28.08144266),
                (94.55032621, 27.30047501),
                (94.14737964, 26.52642186),
                (93.73098536, 25.75951899),
                (93.30127019, 25.0),
                (92.85836504, 24.24809625),
                (92.40240481, 23.50403679),
                (91.9335284, 22.76804825),
                (91.45187863, 22.04035483),
                (90.95760221, 21.32117818),
                (90.45084972, 20.61073739),
                (89.9317755, 19.90924884),
                (89.40053768, 19.21692623),
                (88.85729807, 18.53398045),
                (88.30222216, 17.86061952),
                (87.73547901, 17.19704855),
                (87.15724127, 16.54346968),
                (86.56768508, 15.900082),
                (85.96699002, 15.26708148),
                (85.35533906, 14.64466094),
                (84.73291852, 14.03300998),
                (84.099918, 13.43231492),
                (83.45653032, 12.84275873),
                (82.80295145, 12.26452099),
                (100.0, 12.26452099),
                (100.0, 0.0),
                (50.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_sort(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a sort vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a sort vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 50.0),
                (100.0, 50.0),
                (0.0, 50.0),
                (50.0, 100.0),
                (100.0, 50.0),
                (50.0, 0.0),
                (0.0, 50.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_stored_data(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a stored data vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a stored data vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (10.0, 0.0),
                (9.82547594, 0.00761524),
                (9.65100503, 0.03045865),
                (9.47664044, 0.06852326),
                (9.30243526, 0.12179749),
                (9.12844257, 0.1902651),
                (8.95471537, 0.27390523),
                (8.78130657, 0.37269242),
                (8.60826899, 0.48659656),
                (8.43565535, 0.61558297),
                (8.26351822, 0.75961235),
                (8.09191005, 0.91864083),
                (7.92088309, 1.09261996),
                (7.75048946, 1.28149676),
                (7.58078104, 1.48521369),
                (7.41180955, 1.70370869),
                (7.24362644, 1.9369152),
                (7.07628295, 2.1847622),
                (6.90983006, 2.44717419),
                (6.74431846, 2.72407122),
                (6.57979857, 3.01536896),
                (6.4163205, 3.32097868),
                (6.25393407, 3.64080727),
                (6.09268872, 3.97475733),
                (5.93263357, 4.32272712),
                (5.77381738, 4.68461065),
                (5.61628853, 5.06029769),
                (5.460095, 5.44967379),
                (5.30528437, 5.85262036),
                (5.1519038, 6.26901464),
                (5.0, 6.69872981),
                (4.84961925, 7.14163496),
                (4.70080736, 7.59759519),
                (4.55360965, 8.0664716),
                (4.40807097, 8.54812137),
                (4.26423564, 9.04239779),
                (4.12214748, 9.54915028),
                (3.98184977, 10.0682245),
                (3.84338525, 10.59946232),
                (3.70679609, 11.14270193),
                (3.5721239, 11.69777784),
                (3.43940971, 12.26452099),
                (3.30869394, 12.84275873),
                (3.1800164, 13.43231492),
                (3.0534163, 14.03300998),
                (2.92893219, 14.64466094),
                (2.806602, 15.26708148),
                (2.68646298, 15.900082),
                (2.56855175, 16.54346968),
                (2.4529042, 17.19704855),
                (2.33955557, 17.86061952),
                (2.22854039, 18.53398045),
                (2.11989246, 19.21692623),
                (2.0136449, 19.90924884),
                (1.90983006, 20.61073739),
                (1.80847956, 21.32117818),
                (1.70962427, 22.04035483),
                (1.61329432, 22.76804825),
                (1.51951904, 23.50403679),
                (1.42832699, 24.24809625),
                (1.33974596, 25.0),
                (1.25380293, 25.75951899),
                (1.17052407, 26.52642186),
                (1.08993476, 27.30047501),
                (1.01205954, 28.08144266),
                (0.93692213, 28.86908691),
                (0.86454542, 29.66316785),
                (0.79495147, 30.46344358),
                (0.72816145, 31.26967033),
                (0.66419574, 32.08160252),
                (0.60307379, 32.89899283),
                (0.54481424, 33.72159228),
                (0.48943484, 34.54915028),
                (0.43695244, 35.38141476),
                (0.38738304, 36.21813221),
                (0.34074174, 37.05904774),
                (0.29704274, 37.90390522),
                (0.25629935, 38.75244728),
                (0.21852399, 39.60441546),
                (0.18372817, 40.45955023),
                (0.15192247, 41.31759112),
                (0.12311659, 42.17827675),
                (0.09731931, 43.04134495),
                (0.07453848, 43.90653283),
                (0.05478105, 44.77357684),
                (0.03805302, 45.64221286),
                (0.0243595, 46.51217631),
                (0.01370465, 47.38320219),
                (0.00609173, 48.25502516),
                (0.00152305, 49.12737968),
                (0.0, 50.0),
                (0.00152305, 50.87262032),
                (0.00609173, 51.74497484),
                (0.01370465, 52.61679781),
                (0.0243595, 53.48782369),
                (0.03805302, 54.35778714),
                (0.05478105, 55.22642316),
                (0.07453848, 56.09346717),
                (0.09731931, 56.95865505),
                (0.12311659, 57.82172325),
                (0.15192247, 58.68240888),
                (0.18372817, 59.54044977),
                (0.21852399, 60.39558454),
                (0.25629935, 61.24755272),
                (0.29704274, 62.09609478),
                (0.34074174, 62.94095226),
                (0.38738304, 63.78186779),
                (0.43695244, 64.61858524),
                (0.48943484, 65.45084972),
                (0.54481424, 66.27840772),
                (0.60307379, 67.10100717),
                (0.66419574, 67.91839748),
                (0.72816145, 68.73032967),
                (0.79495147, 69.53655642),
                (0.86454542, 70.33683215),
                (0.93692213, 71.13091309),
                (1.01205954, 71.91855734),
                (1.08993476, 72.69952499),
                (1.17052407, 73.47357814),
                (1.25380293, 74.24048101),
                (1.33974596, 75.0),
                (1.42832699, 75.75190375),
                (1.51951904, 76.49596321),
                (1.61329432, 77.23195175),
                (1.70962427, 77.95964517),
                (1.80847956, 78.67882182),
                (1.90983006, 79.38926261),
                (2.0136449, 80.09075116),
                (2.11989246, 80.78307377),
                (2.22854039, 81.46601955),
                (2.33955557, 82.13938048),
                (2.4529042, 82.80295145),
                (2.56855175, 83.45653032),
                (2.68646298, 84.099918),
                (2.806602, 84.73291852),
                (2.92893219, 85.35533906),
                (3.0534163, 85.96699002),
                (3.1800164, 86.56768508),
                (3.30869394, 87.15724127),
                (3.43940971, 87.73547901),
                (3.5721239, 88.30222216),
                (3.70679609, 88.85729807),
                (3.84338525, 89.40053768),
                (3.98184977, 89.9317755),
                (4.12214748, 90.45084972),
                (4.26423564, 90.95760221),
                (4.40807097, 91.45187863),
                (4.55360965, 91.9335284),
                (4.70080736, 92.40240481),
                (4.84961925, 92.85836504),
                (5.0, 93.30127019),
                (5.1519038, 93.73098536),
                (5.30528437, 94.14737964),
                (5.460095, 94.55032621),
                (5.61628853, 94.93970231),
                (5.77381738, 95.31538935),
                (5.93263357, 95.67727288),
                (6.09268872, 96.02524267),
                (6.25393407, 96.35919273),
                (6.4163205, 96.67902132),
                (6.57979857, 96.98463104),
                (6.74431846, 97.27592878),
                (6.90983006, 97.55282581),
                (7.07628295, 97.8152378),
                (7.24362644, 98.0630848),
                (7.41180955, 98.29629131),
                (7.58078104, 98.51478631),
                (7.75048946, 98.71850324),
                (7.92088309, 98.90738004),
                (8.09191005, 99.08135917),
                (8.26351822, 99.24038765),
                (8.43565535, 99.38441703),
                (8.60826899, 99.51340344),
                (8.78130657, 99.62730758),
                (8.95471537, 99.72609477),
                (9.12844257, 99.8097349),
                (9.30243526, 99.87820251),
                (9.47664044, 99.93147674),
                (9.65100503, 99.96954135),
                (9.82547594, 99.99238476),
                (99.82547594, 99.99238476),
                (99.65100503, 99.96954135),
                (99.47664044, 99.93147674),
                (99.30243526, 99.87820251),
                (99.12844257, 99.8097349),
                (98.95471537, 99.72609477),
                (98.78130657, 99.62730758),
                (98.60826899, 99.51340344),
                (98.43565535, 99.38441703),
                (98.26351822, 99.24038765),
                (98.09191005, 99.08135917),
                (97.92088309, 98.90738004),
                (97.75048946, 98.71850324),
                (97.58078104, 98.51478631),
                (97.41180955, 98.29629131),
                (97.24362644, 98.0630848),
                (97.07628295, 97.8152378),
                (96.90983006, 97.55282581),
                (96.74431846, 97.27592878),
                (96.57979857, 96.98463104),
                (96.4163205, 96.67902132),
                (96.25393407, 96.35919273),
                (96.09268872, 96.02524267),
                (95.93263357, 95.67727288),
                (95.77381738, 95.31538935),
                (95.61628853, 94.93970231),
                (95.460095, 94.55032621),
                (95.30528437, 94.14737964),
                (95.1519038, 93.73098536),
                (95.0, 93.30127019),
                (94.84961925, 92.85836504),
                (94.70080736, 92.40240481),
                (94.55360965, 91.9335284),
                (94.40807097, 91.45187863),
                (94.26423564, 90.95760221),
                (94.12214748, 90.45084972),
                (93.98184977, 89.9317755),
                (93.84338525, 89.40053768),
                (93.70679609, 88.85729807),
                (93.5721239, 88.30222216),
                (93.43940971, 87.73547901),
                (93.30869394, 87.15724127),
                (93.1800164, 86.56768508),
                (93.0534163, 85.96699002),
                (92.92893219, 85.35533906),
                (92.806602, 84.73291852),
                (92.68646298, 84.099918),
                (92.56855175, 83.45653032),
                (92.4529042, 82.80295145),
                (92.33955557, 82.13938048),
                (92.22854039, 81.46601955),
                (92.11989246, 80.78307377),
                (92.0136449, 80.09075116),
                (91.90983006, 79.38926261),
                (91.80847956, 78.67882182),
                (91.70962427, 77.95964517),
                (91.61329432, 77.23195175),
                (91.51951904, 76.49596321),
                (91.42832699, 75.75190375),
                (91.33974596, 75.0),
                (91.25380293, 74.24048101),
                (91.17052407, 73.47357814),
                (91.08993476, 72.69952499),
                (91.01205954, 71.91855734),
                (90.93692213, 71.13091309),
                (90.86454542, 70.33683215),
                (90.79495147, 69.53655642),
                (90.72816145, 68.73032967),
                (90.66419574, 67.91839748),
                (90.60307379, 67.10100717),
                (90.54481424, 66.27840772),
                (90.48943484, 65.45084972),
                (90.43695244, 64.61858524),
                (90.38738304, 63.78186779),
                (90.34074174, 62.94095226),
                (90.29704274, 62.09609478),
                (90.25629935, 61.24755272),
                (90.21852399, 60.39558454),
                (90.18372817, 59.54044977),
                (90.15192247, 58.68240888),
                (90.12311659, 57.82172325),
                (90.09731931, 56.95865505),
                (90.07453848, 56.09346717),
                (90.05478105, 55.22642316),
                (90.03805302, 54.35778714),
                (90.0243595, 53.48782369),
                (90.01370465, 52.61679781),
                (90.00609173, 51.74497484),
                (90.00152305, 50.87262032),
                (90.0, 50.0),
                (90.00152305, 49.12737968),
                (90.00609173, 48.25502516),
                (90.01370465, 47.38320219),
                (90.0243595, 46.51217631),
                (90.03805302, 45.64221286),
                (90.05478105, 44.77357684),
                (90.07453848, 43.90653283),
                (90.09731931, 43.04134495),
                (90.12311659, 42.17827675),
                (90.15192247, 41.31759112),
                (90.18372817, 40.45955023),
                (90.21852399, 39.60441546),
                (90.25629935, 38.75244728),
                (90.29704274, 37.90390522),
                (90.34074174, 37.05904774),
                (90.38738304, 36.21813221),
                (90.43695244, 35.38141476),
                (90.48943484, 34.54915028),
                (90.54481424, 33.72159228),
                (90.60307379, 32.89899283),
                (90.66419574, 32.08160252),
                (90.72816145, 31.26967033),
                (90.79495147, 30.46344358),
                (90.86454542, 29.66316785),
                (90.93692213, 28.86908691),
                (91.01205954, 28.08144266),
                (91.08993476, 27.30047501),
                (91.17052407, 26.52642186),
                (91.25380293, 25.75951899),
                (91.33974596, 25.0),
                (91.42832699, 24.24809625),
                (91.51951904, 23.50403679),
                (91.61329432, 22.76804825),
                (91.70962427, 22.04035483),
                (91.80847956, 21.32117818),
                (91.90983006, 20.61073739),
                (92.0136449, 19.90924884),
                (92.11989246, 19.21692623),
                (92.22854039, 18.53398045),
                (92.33955557, 17.86061952),
                (92.4529042, 17.19704855),
                (92.56855175, 16.54346968),
                (92.68646298, 15.900082),
                (92.806602, 15.26708148),
                (92.92893219, 14.64466094),
                (93.0534163, 14.03300998),
                (93.1800164, 13.43231492),
                (93.30869394, 12.84275873),
                (93.43940971, 12.26452099),
                (93.5721239, 11.69777784),
                (93.70679609, 11.14270193),
                (93.84338525, 10.59946232),
                (93.98184977, 10.0682245),
                (94.12214748, 9.54915028),
                (94.26423564, 9.04239779),
                (94.40807097, 8.54812137),
                (94.55360965, 8.0664716),
                (94.70080736, 7.59759519),
                (94.84961925, 7.14163496),
                (95.0, 6.69872981),
                (95.1519038, 6.26901464),
                (95.30528437, 5.85262036),
                (95.460095, 5.44967379),
                (95.61628853, 5.06029769),
                (95.77381738, 4.68461065),
                (95.93263357, 4.32272712),
                (96.09268872, 3.97475733),
                (96.25393407, 3.64080727),
                (96.4163205, 3.32097868),
                (96.57979857, 3.01536896),
                (96.74431846, 2.72407122),
                (96.90983006, 2.44717419),
                (97.07628295, 2.1847622),
                (97.24362644, 1.9369152),
                (97.41180955, 1.70370869),
                (97.58078104, 1.48521369),
                (97.75048946, 1.28149676),
                (97.92088309, 1.09261996),
                (98.09191005, 0.91864083),
                (98.26351822, 0.75961235),
                (98.43565535, 0.61558297),
                (98.60826899, 0.48659656),
                (98.78130657, 0.37269242),
                (98.95471537, 0.27390523),
                (99.12844257, 0.1902651),
                (99.30243526, 0.12179749),
                (99.47664044, 0.06852326),
                (99.65100503, 0.03045865),
                (99.82547594, 0.00761524),
                (100.0, 0.0),
                (10.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_summing_junction(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a summing junction vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a summing junction vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (50.0, 100.0),
                (50.87262032, 99.99238476),
                (51.74497484, 99.96954135),
                (52.61679781, 99.93147674),
                (53.48782369, 99.87820251),
                (54.35778714, 99.8097349),
                (55.22642316, 99.72609477),
                (56.09346717, 99.62730758),
                (56.95865505, 99.51340344),
                (57.82172325, 99.38441703),
                (58.68240888, 99.24038765),
                (59.54044977, 99.08135917),
                (60.39558454, 98.90738004),
                (61.24755272, 98.71850324),
                (62.09609478, 98.51478631),
                (62.94095226, 98.29629131),
                (63.78186779, 98.0630848),
                (64.61858524, 97.8152378),
                (65.45084972, 97.55282581),
                (66.27840772, 97.27592878),
                (67.10100717, 96.98463104),
                (67.91839748, 96.67902132),
                (68.73032967, 96.35919273),
                (69.53655642, 96.02524267),
                (70.33683215, 95.67727288),
                (71.13091309, 95.31538935),
                (71.91855734, 94.93970231),
                (72.69952499, 94.55032621),
                (73.47357814, 94.14737964),
                (74.24048101, 93.73098536),
                (75.0, 93.30127019),
                (75.75190375, 92.85836504),
                (76.49596321, 92.40240481),
                (77.23195175, 91.9335284),
                (77.95964517, 91.45187863),
                (78.67882182, 90.95760221),
                (79.38926261, 90.45084972),
                (80.09075116, 89.9317755),
                (80.78307377, 89.40053768),
                (81.46601955, 88.85729807),
                (82.13938048, 88.30222216),
                (82.80295145, 87.73547901),
                (83.45653032, 87.15724127),
                (84.099918, 86.56768508),
                (84.73291852, 85.96699002),
                (85.35533906, 85.35533906),
                (14.64466094, 14.64466094),
                (85.35533906, 85.35533906),
                (85.96699002, 84.73291852),
                (86.56768508, 84.099918),
                (87.15724127, 83.45653032),
                (87.73547901, 82.80295145),
                (88.30222216, 82.13938048),
                (88.85729807, 81.46601955),
                (89.40053768, 80.78307377),
                (89.9317755, 80.09075116),
                (90.45084972, 79.38926261),
                (90.95760221, 78.67882182),
                (91.45187863, 77.95964517),
                (91.9335284, 77.23195175),
                (92.40240481, 76.49596321),
                (92.85836504, 75.75190375),
                (93.30127019, 75.0),
                (93.73098536, 74.24048101),
                (94.14737964, 73.47357814),
                (94.55032621, 72.69952499),
                (94.93970231, 71.91855734),
                (95.31538935, 71.13091309),
                (95.67727288, 70.33683215),
                (96.02524267, 69.53655642),
                (96.35919273, 68.73032967),
                (96.67902132, 67.91839748),
                (96.98463104, 67.10100717),
                (97.27592878, 66.27840772),
                (97.55282581, 65.45084972),
                (97.8152378, 64.61858524),
                (98.0630848, 63.78186779),
                (98.29629131, 62.94095226),
                (98.51478631, 62.09609478),
                (98.71850324, 61.24755272),
                (98.90738004, 60.39558454),
                (99.08135917, 59.54044977),
                (99.24038765, 58.68240888),
                (99.38441703, 57.82172325),
                (99.51340344, 56.95865505),
                (99.62730758, 56.09346717),
                (99.72609477, 55.22642316),
                (99.8097349, 54.35778714),
                (99.87820251, 53.48782369),
                (99.93147674, 52.61679781),
                (99.96954135, 51.74497484),
                (99.99238476, 50.87262032),
                (100.0, 50.0),
                (99.99238476, 49.12737968),
                (99.96954135, 48.25502516),
                (99.93147674, 47.38320219),
                (99.87820251, 46.51217631),
                (99.8097349, 45.64221286),
                (99.72609477, 44.77357684),
                (99.62730758, 43.90653283),
                (99.51340344, 43.04134495),
                (99.38441703, 42.17827675),
                (99.24038765, 41.31759112),
                (99.08135917, 40.45955023),
                (98.90738004, 39.60441546),
                (98.71850324, 38.75244728),
                (98.51478631, 37.90390522),
                (98.29629131, 37.05904774),
                (98.0630848, 36.21813221),
                (97.8152378, 35.38141476),
                (97.55282581, 34.54915028),
                (97.27592878, 33.72159228),
                (96.98463104, 32.89899283),
                (96.67902132, 32.08160252),
                (96.35919273, 31.26967033),
                (96.02524267, 30.46344358),
                (95.67727288, 29.66316785),
                (95.31538935, 28.86908691),
                (94.93970231, 28.08144266),
                (94.55032621, 27.30047501),
                (94.14737964, 26.52642186),
                (93.73098536, 25.75951899),
                (93.30127019, 25.0),
                (92.85836504, 24.24809625),
                (92.40240481, 23.50403679),
                (91.9335284, 22.76804825),
                (91.45187863, 22.04035483),
                (90.95760221, 21.32117818),
                (90.45084972, 20.61073739),
                (89.9317755, 19.90924884),
                (89.40053768, 19.21692623),
                (88.85729807, 18.53398045),
                (88.30222216, 17.86061952),
                (87.73547901, 17.19704855),
                (87.15724127, 16.54346968),
                (86.56768508, 15.900082),
                (85.96699002, 15.26708148),
                (85.35533906, 14.64466094),
                (14.64466094, 85.35533906),
                (85.35533906, 14.64466094),
                (84.73291852, 14.03300998),
                (84.099918, 13.43231492),
                (83.45653032, 12.84275873),
                (82.80295145, 12.26452099),
                (82.13938048, 11.69777784),
                (81.46601955, 11.14270193),
                (80.78307377, 10.59946232),
                (80.09075116, 10.0682245),
                (79.38926261, 9.54915028),
                (78.67882182, 9.04239779),
                (77.95964517, 8.54812137),
                (77.23195175, 8.0664716),
                (76.49596321, 7.59759519),
                (75.75190375, 7.14163496),
                (75.0, 6.69872981),
                (74.24048101, 6.26901464),
                (73.47357814, 5.85262036),
                (72.69952499, 5.44967379),
                (71.91855734, 5.06029769),
                (71.13091309, 4.68461065),
                (70.33683215, 4.32272712),
                (69.53655642, 3.97475733),
                (68.73032967, 3.64080727),
                (67.91839748, 3.32097868),
                (67.10100717, 3.01536896),
                (66.27840772, 2.72407122),
                (65.45084972, 2.44717419),
                (64.61858524, 2.1847622),
                (63.78186779, 1.9369152),
                (62.94095226, 1.70370869),
                (62.09609478, 1.48521369),
                (61.24755272, 1.28149676),
                (60.39558454, 1.09261996),
                (59.54044977, 0.91864083),
                (58.68240888, 0.75961235),
                (57.82172325, 0.61558297),
                (56.95865505, 0.48659656),
                (56.09346717, 0.37269242),
                (55.22642316, 0.27390523),
                (54.35778714, 0.1902651),
                (53.48782369, 0.12179749),
                (52.61679781, 0.06852326),
                (51.74497484, 0.03045865),
                (50.87262032, 0.00761524),
                (50.0, 0.0),
                (49.12737968, 0.00761524),
                (48.25502516, 0.03045865),
                (47.38320219, 0.06852326),
                (46.51217631, 0.12179749),
                (45.64221286, 0.1902651),
                (44.77357684, 0.27390523),
                (43.90653283, 0.37269242),
                (43.04134495, 0.48659656),
                (42.17827675, 0.61558297),
                (41.31759112, 0.75961235),
                (40.45955023, 0.91864083),
                (39.60441546, 1.09261996),
                (38.75244728, 1.28149676),
                (37.90390522, 1.48521369),
                (37.05904774, 1.70370869),
                (36.21813221, 1.9369152),
                (35.38141476, 2.1847622),
                (34.54915028, 2.44717419),
                (33.72159228, 2.72407122),
                (32.89899283, 3.01536896),
                (32.08160252, 3.32097868),
                (31.26967033, 3.64080727),
                (30.46344358, 3.97475733),
                (29.66316785, 4.32272712),
                (28.86908691, 4.68461065),
                (28.08144266, 5.06029769),
                (27.30047501, 5.44967379),
                (26.52642186, 5.85262036),
                (25.75951899, 6.26901464),
                (25.0, 6.69872981),
                (24.24809625, 7.14163496),
                (23.50403679, 7.59759519),
                (22.76804825, 8.0664716),
                (22.04035483, 8.54812137),
                (21.32117818, 9.04239779),
                (20.61073739, 9.54915028),
                (19.90924884, 10.0682245),
                (19.21692623, 10.59946232),
                (18.53398045, 11.14270193),
                (17.86061952, 11.69777784),
                (17.19704855, 12.26452099),
                (16.54346968, 12.84275873),
                (15.900082, 13.43231492),
                (15.26708148, 14.03300998),
                (14.64466094, 14.64466094),
                (14.03300998, 15.26708148),
                (13.43231492, 15.900082),
                (12.84275873, 16.54346968),
                (12.26452099, 17.19704855),
                (11.69777784, 17.86061952),
                (11.14270193, 18.53398045),
                (10.59946232, 19.21692623),
                (10.0682245, 19.90924884),
                (9.54915028, 20.61073739),
                (9.04239779, 21.32117818),
                (8.54812137, 22.04035483),
                (8.0664716, 22.76804825),
                (7.59759519, 23.50403679),
                (7.14163496, 24.24809625),
                (6.69872981, 25.0),
                (6.26901464, 25.75951899),
                (5.85262036, 26.52642186),
                (5.44967379, 27.30047501),
                (5.06029769, 28.08144266),
                (4.68461065, 28.86908691),
                (4.32272712, 29.66316785),
                (3.97475733, 30.46344358),
                (3.64080727, 31.26967033),
                (3.32097868, 32.08160252),
                (3.01536896, 32.89899283),
                (2.72407122, 33.72159228),
                (2.44717419, 34.54915028),
                (2.1847622, 35.38141476),
                (1.9369152, 36.21813221),
                (1.70370869, 37.05904774),
                (1.48521369, 37.90390522),
                (1.28149676, 38.75244728),
                (1.09261996, 39.60441546),
                (0.91864083, 40.45955023),
                (0.75961235, 41.31759112),
                (0.61558297, 42.17827675),
                (0.48659656, 43.04134495),
                (0.37269242, 43.90653283),
                (0.27390523, 44.77357684),
                (0.1902651, 45.64221286),
                (0.12179749, 46.51217631),
                (0.06852326, 47.38320219),
                (0.03045865, 48.25502516),
                (0.00761524, 49.12737968),
                (0.0, 50.0),
                (0.00761524, 50.87262032),
                (0.03045865, 51.74497484),
                (0.06852326, 52.61679781),
                (0.12179749, 53.48782369),
                (0.1902651, 54.35778714),
                (0.27390523, 55.22642316),
                (0.37269242, 56.09346717),
                (0.48659656, 56.95865505),
                (0.61558297, 57.82172325),
                (0.75961235, 58.68240888),
                (0.91864083, 59.54044977),
                (1.09261996, 60.39558454),
                (1.28149676, 61.24755272),
                (1.48521369, 62.09609478),
                (1.70370869, 62.94095226),
                (1.9369152, 63.78186779),
                (2.1847622, 64.61858524),
                (2.44717419, 65.45084972),
                (2.72407122, 66.27840772),
                (3.01536896, 67.10100717),
                (3.32097868, 67.91839748),
                (3.64080727, 68.73032967),
                (3.97475733, 69.53655642),
                (4.32272712, 70.33683215),
                (4.68461065, 71.13091309),
                (5.06029769, 71.91855734),
                (5.44967379, 72.69952499),
                (5.85262036, 73.47357814),
                (6.26901464, 74.24048101),
                (6.69872981, 75.0),
                (7.14163496, 75.75190375),
                (7.59759519, 76.49596321),
                (8.0664716, 77.23195175),
                (8.54812137, 77.95964517),
                (9.04239779, 78.67882182),
                (9.54915028, 79.38926261),
                (10.0682245, 80.09075116),
                (10.59946232, 80.78307377),
                (11.14270193, 81.46601955),
                (11.69777784, 82.13938048),
                (12.26452099, 82.80295145),
                (12.84275873, 83.45653032),
                (13.43231492, 84.099918),
                (14.03300998, 84.73291852),
                (14.64466094, 85.35533906),
                (15.26708148, 85.96699002),
                (15.900082, 86.56768508),
                (16.54346968, 87.15724127),
                (17.19704855, 87.73547901),
                (17.86061952, 88.30222216),
                (18.53398045, 88.85729807),
                (19.21692623, 89.40053768),
                (19.90924884, 89.9317755),
                (20.61073739, 90.45084972),
                (21.32117818, 90.95760221),
                (22.04035483, 91.45187863),
                (22.76804825, 91.9335284),
                (23.50403679, 92.40240481),
                (24.24809625, 92.85836504),
                (25.0, 93.30127019),
                (25.75951899, 93.73098536),
                (26.52642186, 94.14737964),
                (27.30047501, 94.55032621),
                (28.08144266, 94.93970231),
                (28.86908691, 95.31538935),
                (29.66316785, 95.67727288),
                (30.46344358, 96.02524267),
                (31.26967033, 96.35919273),
                (32.08160252, 96.67902132),
                (32.89899283, 96.98463104),
                (33.72159228, 97.27592878),
                (34.54915028, 97.55282581),
                (35.38141476, 97.8152378),
                (36.21813221, 98.0630848),
                (37.05904774, 98.29629131),
                (37.90390522, 98.51478631),
                (38.75244728, 98.71850324),
                (39.60441546, 98.90738004),
                (40.45955023, 99.08135917),
                (41.31759112, 99.24038765),
                (42.17827675, 99.38441703),
                (43.04134495, 99.51340344),
                (43.90653283, 99.62730758),
                (44.77357684, 99.72609477),
                (45.64221286, 99.8097349),
                (46.51217631, 99.87820251),
                (47.38320219, 99.93147674),
                (48.25502516, 99.96954135),
                (49.12737968, 99.99238476),
                (50.0, 100.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_termination(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a termination vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a termination vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (-0.43631016, 0.00761524),
                (-0.87248742, 0.03045865),
                (-1.30839891, 0.06852326),
                (-1.74391184, 0.12179749),
                (-2.17889357, 0.1902651),
                (-2.61321158, 0.27390523),
                (-3.04673359, 0.37269242),
                (-3.47932752, 0.48659656),
                (-3.91086163, 0.61558297),
                (-4.34120444, 0.75961235),
                (-4.77022488, 0.91864083),
                (-5.19779227, 1.09261996),
                (-5.62377636, 1.28149676),
                (-6.04804739, 1.48521369),
                (-6.47047613, 1.70370869),
                (-6.8909339, 1.9369152),
                (-7.30929262, 2.1847622),
                (-7.72542486, 2.44717419),
                (-8.13920386, 2.72407122),
                (-8.55050358, 3.01536896),
                (-8.95919874, 3.32097868),
                (-9.36516484, 3.64080727),
                (-9.76827821, 3.97475733),
                (-10.16841608, 4.32272712),
                (-10.56545654, 4.68461065),
                (-10.95927867, 5.06029769),
                (-11.34976249, 5.44967379),
                (-11.73678907, 5.85262036),
                (-12.12024051, 6.26901464),
                (-12.5, 6.69872981),
                (-12.87595187, 7.14163496),
                (-13.24798161, 7.59759519),
                (-13.61597588, 8.0664716),
                (-13.97982259, 8.54812137),
                (-14.33941091, 9.04239779),
                (-14.69463131, 9.54915028),
                (-15.04537558, 10.0682245),
                (-15.39153688, 10.59946232),
                (-15.73300978, 11.14270193),
                (-16.06969024, 11.69777784),
                (-16.40147572, 12.26452099),
                (-16.72826516, 12.84275873),
                (-17.049959, 13.43231492),
                (-17.36645926, 14.03300998),
                (-17.67766953, 14.64466094),
                (-17.98349501, 15.26708148),
                (-18.28384254, 15.900082),
                (-18.57862064, 16.54346968),
                (-18.86773951, 17.19704855),
                (-19.15111108, 17.86061952),
                (-19.42864904, 18.53398045),
                (-19.70026884, 19.21692623),
                (-19.96588775, 19.90924884),
                (-20.22542486, 20.61073739),
                (-20.47880111, 21.32117818),
                (-20.72593931, 22.04035483),
                (-20.9667642, 22.76804825),
                (-21.2012024, 23.50403679),
                (-21.42918252, 24.24809625),
                (-21.65063509, 25.0),
                (-21.86549268, 25.75951899),
                (-22.07368982, 26.52642186),
                (-22.2751631, 27.30047501),
                (-22.46985116, 28.08144266),
                (-22.65769468, 28.86908691),
                (-22.83863644, 29.66316785),
                (-23.01262134, 30.46344358),
                (-23.17959636, 31.26967033),
                (-23.33951066, 32.08160252),
                (-23.49231552, 32.89899283),
                (-23.63796439, 33.72159228),
                (-23.77641291, 34.54915028),
                (-23.9076189, 35.38141476),
                (-24.0315424, 36.21813221),
                (-24.14814566, 37.05904774),
                (-24.25739316, 37.90390522),
                (-24.35925162, 38.75244728),
                (-24.45369002, 39.60441546),
                (-24.54067959, 40.45955023),
                (-24.62019383, 41.31759112),
                (-24.69220851, 42.17827675),
                (-24.75670172, 43.04134495),
                (-24.81365379, 43.90653283),
                (-24.86304738, 44.77357684),
                (-24.90486745, 45.64221286),
                (-24.93910126, 46.51217631),
                (-24.96573837, 47.38320219),
                (-24.98477068, 48.25502516),
                (-24.99619238, 49.12737968),
                (-25.0, 50.0),
                (-24.99619238, 50.87262032),
                (-24.98477068, 51.74497484),
                (-24.96573837, 52.61679781),
                (-24.93910126, 53.48782369),
                (-24.90486745, 54.35778714),
                (-24.86304738, 55.22642316),
                (-24.81365379, 56.09346717),
                (-24.75670172, 56.95865505),
                (-24.69220851, 57.82172325),
                (-24.62019383, 58.68240888),
                (-24.54067959, 59.54044977),
                (-24.45369002, 60.39558454),
                (-24.35925162, 61.24755272),
                (-24.25739316, 62.09609478),
                (-24.14814566, 62.94095226),
                (-24.0315424, 63.78186779),
                (-23.9076189, 64.61858524),
                (-23.77641291, 65.45084972),
                (-23.63796439, 66.27840772),
                (-23.49231552, 67.10100717),
                (-23.33951066, 67.91839748),
                (-23.17959636, 68.73032967),
                (-23.01262134, 69.53655642),
                (-22.83863644, 70.33683215),
                (-22.65769468, 71.13091309),
                (-22.46985116, 71.91855734),
                (-22.2751631, 72.69952499),
                (-22.07368982, 73.47357814),
                (-21.86549268, 74.24048101),
                (-21.65063509, 75.0),
                (-21.42918252, 75.75190375),
                (-21.2012024, 76.49596321),
                (-20.9667642, 77.23195175),
                (-20.72593931, 77.95964517),
                (-20.47880111, 78.67882182),
                (-20.22542486, 79.38926261),
                (-19.96588775, 80.09075116),
                (-19.70026884, 80.78307377),
                (-19.42864904, 81.46601955),
                (-19.15111108, 82.13938048),
                (-18.86773951, 82.80295145),
                (-18.57862064, 83.45653032),
                (-18.28384254, 84.099918),
                (-17.98349501, 84.73291852),
                (-17.67766953, 85.35533906),
                (-17.36645926, 85.96699002),
                (-17.049959, 86.56768508),
                (-16.72826516, 87.15724127),
                (-16.40147572, 87.73547901),
                (-16.06969024, 88.30222216),
                (-15.73300978, 88.85729807),
                (-15.39153688, 89.40053768),
                (-15.04537558, 89.9317755),
                (-14.69463131, 90.45084972),
                (-14.33941091, 90.95760221),
                (-13.97982259, 91.45187863),
                (-13.61597588, 91.9335284),
                (-13.24798161, 92.40240481),
                (-12.87595187, 92.85836504),
                (-12.5, 93.30127019),
                (-12.12024051, 93.73098536),
                (-11.73678907, 94.14737964),
                (-11.34976249, 94.55032621),
                (-10.95927867, 94.93970231),
                (-10.56545654, 95.31538935),
                (-10.16841608, 95.67727288),
                (-9.76827821, 96.02524267),
                (-9.36516484, 96.35919273),
                (-8.95919874, 96.67902132),
                (-8.55050358, 96.98463104),
                (-8.13920386, 97.27592878),
                (-7.72542486, 97.55282581),
                (-7.30929262, 97.8152378),
                (-6.8909339, 98.0630848),
                (-6.47047613, 98.29629131),
                (-6.04804739, 98.51478631),
                (-5.62377636, 98.71850324),
                (-5.19779227, 98.90738004),
                (-4.77022488, 99.08135917),
                (-4.34120444, 99.24038765),
                (-3.91086163, 99.38441703),
                (-3.47932752, 99.51340344),
                (-3.04673359, 99.62730758),
                (-2.61321158, 99.72609477),
                (-2.17889357, 99.8097349),
                (-1.74391184, 99.87820251),
                (-1.30839891, 99.93147674),
                (-0.87248742, 99.96954135),
                (-0.43631016, 99.99238476),
                (50.0, 100.0),
                (50.43631016, 99.99238476),
                (50.87248742, 99.96954135),
                (51.30839891, 99.93147674),
                (51.74391184, 99.87820251),
                (52.17889357, 99.8097349),
                (52.61321158, 99.72609477),
                (53.04673359, 99.62730758),
                (53.47932752, 99.51340344),
                (53.91086163, 99.38441703),
                (54.34120444, 99.24038765),
                (54.77022488, 99.08135917),
                (55.19779227, 98.90738004),
                (55.62377636, 98.71850324),
                (56.04804739, 98.51478631),
                (56.47047613, 98.29629131),
                (56.8909339, 98.0630848),
                (57.30929262, 97.8152378),
                (57.72542486, 97.55282581),
                (58.13920386, 97.27592878),
                (58.55050358, 96.98463104),
                (58.95919874, 96.67902132),
                (59.36516484, 96.35919273),
                (59.76827821, 96.02524267),
                (60.16841608, 95.67727288),
                (60.56545654, 95.31538935),
                (60.95927867, 94.93970231),
                (61.34976249, 94.55032621),
                (61.73678907, 94.14737964),
                (62.12024051, 93.73098536),
                (62.5, 93.30127019),
                (62.87595187, 92.85836504),
                (63.24798161, 92.40240481),
                (63.61597588, 91.9335284),
                (63.97982259, 91.45187863),
                (64.33941091, 90.95760221),
                (64.69463131, 90.45084972),
                (65.04537558, 89.9317755),
                (65.39153688, 89.40053768),
                (65.73300978, 88.85729807),
                (66.06969024, 88.30222216),
                (66.40147572, 87.73547901),
                (66.72826516, 87.15724127),
                (67.049959, 86.56768508),
                (67.36645926, 85.96699002),
                (67.67766953, 85.35533906),
                (67.98349501, 84.73291852),
                (68.28384254, 84.099918),
                (68.57862064, 83.45653032),
                (68.86773951, 82.80295145),
                (69.15111108, 82.13938048),
                (69.42864904, 81.46601955),
                (69.70026884, 80.78307377),
                (69.96588775, 80.09075116),
                (70.22542486, 79.38926261),
                (70.47880111, 78.67882182),
                (70.72593931, 77.95964517),
                (70.9667642, 77.23195175),
                (71.2012024, 76.49596321),
                (71.42918252, 75.75190375),
                (71.65063509, 75.0),
                (71.86549268, 74.24048101),
                (72.07368982, 73.47357814),
                (72.2751631, 72.69952499),
                (72.46985116, 71.91855734),
                (72.65769468, 71.13091309),
                (72.83863644, 70.33683215),
                (73.01262134, 69.53655642),
                (73.17959636, 68.73032967),
                (73.33951066, 67.91839748),
                (73.49231552, 67.10100717),
                (73.63796439, 66.27840772),
                (73.77641291, 65.45084972),
                (73.9076189, 64.61858524),
                (74.0315424, 63.78186779),
                (74.14814566, 62.94095226),
                (74.25739316, 62.09609478),
                (74.35925162, 61.24755272),
                (74.45369002, 60.39558454),
                (74.54067959, 59.54044977),
                (74.62019383, 58.68240888),
                (74.69220851, 57.82172325),
                (74.75670172, 56.95865505),
                (74.81365379, 56.09346717),
                (74.86304738, 55.22642316),
                (74.90486745, 54.35778714),
                (74.93910126, 53.48782369),
                (74.96573837, 52.61679781),
                (74.98477068, 51.74497484),
                (74.99619238, 50.87262032),
                (75.0, 50.0),
                (74.99619238, 49.12737968),
                (74.98477068, 48.25502516),
                (74.96573837, 47.38320219),
                (74.93910126, 46.51217631),
                (74.90486745, 45.64221286),
                (74.86304738, 44.77357684),
                (74.81365379, 43.90653283),
                (74.75670172, 43.04134495),
                (74.69220851, 42.17827675),
                (74.62019383, 41.31759112),
                (74.54067959, 40.45955023),
                (74.45369002, 39.60441546),
                (74.35925162, 38.75244728),
                (74.25739316, 37.90390522),
                (74.14814566, 37.05904774),
                (74.0315424, 36.21813221),
                (73.9076189, 35.38141476),
                (73.77641291, 34.54915028),
                (73.63796439, 33.72159228),
                (73.49231552, 32.89899283),
                (73.33951066, 32.08160252),
                (73.17959636, 31.26967033),
                (73.01262134, 30.46344358),
                (72.83863644, 29.66316785),
                (72.65769468, 28.86908691),
                (72.46985116, 28.08144266),
                (72.2751631, 27.30047501),
                (72.07368982, 26.52642186),
                (71.86549268, 25.75951899),
                (71.65063509, 25.0),
                (71.42918252, 24.24809625),
                (71.2012024, 23.50403679),
                (70.9667642, 22.76804825),
                (70.72593931, 22.04035483),
                (70.47880111, 21.32117818),
                (70.22542486, 20.61073739),
                (69.96588775, 19.90924884),
                (69.70026884, 19.21692623),
                (69.42864904, 18.53398045),
                (69.15111108, 17.86061952),
                (68.86773951, 17.19704855),
                (68.57862064, 16.54346968),
                (68.28384254, 15.900082),
                (67.98349501, 15.26708148),
                (67.67766953, 14.64466094),
                (67.36645926, 14.03300998),
                (67.049959, 13.43231492),
                (66.72826516, 12.84275873),
                (66.40147572, 12.26452099),
                (66.06969024, 11.69777784),
                (65.73300978, 11.14270193),
                (65.39153688, 10.59946232),
                (65.04537558, 10.0682245),
                (64.69463131, 9.54915028),
                (64.33941091, 9.04239779),
                (63.97982259, 8.54812137),
                (63.61597588, 8.0664716),
                (63.24798161, 7.59759519),
                (62.87595187, 7.14163496),
                (62.5, 6.69872981),
                (62.12024051, 6.26901464),
                (61.73678907, 5.85262036),
                (61.34976249, 5.44967379),
                (60.95927867, 5.06029769),
                (60.56545654, 4.68461065),
                (60.16841608, 4.32272712),
                (59.76827821, 3.97475733),
                (59.36516484, 3.64080727),
                (58.95919874, 3.32097868),
                (58.55050358, 3.01536896),
                (58.13920386, 2.72407122),
                (57.72542486, 2.44717419),
                (57.30929262, 2.1847622),
                (56.8909339, 1.9369152),
                (56.47047613, 1.70370869),
                (56.04804739, 1.48521369),
                (55.62377636, 1.28149676),
                (55.19779227, 1.09261996),
                (54.77022488, 0.91864083),
                (54.34120444, 0.75961235),
                (53.91086163, 0.61558297),
                (53.47932752, 0.48659656),
                (53.04673359, 0.37269242),
                (52.61321158, 0.27390523),
                (52.17889357, 0.1902651),
                (51.74391184, 0.12179749),
                (51.30839891, 0.06852326),
                (50.87248742, 0.03045865),
                (50.43631016, 0.00761524),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def flowchart_transport(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a transport vertex (in flowcharts).

        This function creates and returns a Shape object that visually represents
        a transport vertex (in flowcharts).

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.arrow_right(
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
            fill_color=fill_color,
            line_width=line_width,
            stroke_color=stroke_color,
        )

    @staticmethod
    def four_pointed_star(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a four-pointed star.

        This function creates and returns a Shape object that visually represents
        a four-pointed star.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_pointed_star(
            number_of_points=4,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def fraction_of_circle(
        angle_in_degrees: int,
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a fraction of a circle.

        This function creates and returns a Shape object that visually represents
        a fraction of a circle.

        :param angle_in_degrees:    the fraction of the circle to draw
        :param stroke_color:        the color in which to draw the Shape
        :param fill_color:          the color in which to fill the Shape
        :param line_width:          the line width of the Shape
        :param dash_pattern:        the dash pattern to be used when drawing the Shape
        :param dash_phase:          the dash phase to be used when starting to draw the Shape
        :return:                    a Shape
        """
        assert 1 <= angle_in_degrees <= 360
        if angle_in_degrees == 360:
            return LineArt.circle(
                stroke_color=stroke_color,
                fill_color=fill_color,
                line_width=line_width,
                dash_pattern=dash_pattern,
                dash_phase=dash_phase,
            )
        coords_0: typing.List[typing.Tuple[float, float]] = [
            (math.cos(math.radians(i)) * 50, math.sin(math.radians(i)) * 50)
            for i in range(0, angle_in_degrees)
        ]
        coords_0 = [(0, 0)] + coords_0 + [(0, 0)]
        return Shape(
            coordinates=coords_0,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def half_of_circle(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting half of a circle.

        This function creates and returns a Shape object that visually represents
        half of a circle.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.fraction_of_circle(
            angle_in_degrees=180,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def heart(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a heart.

        This function creates and returns a Shape object that visually represents
        a heart.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 50.0),
                (0.00380762, 50.43631016),
                (0.01522932, 50.87248742),
                (0.03426163, 51.30839891),
                (0.06089874, 51.74391184),
                (0.09513255, 52.17889357),
                (0.13695262, 52.61321158),
                (0.18634621, 53.04673359),
                (0.24329828, 53.47932752),
                (0.30779149, 53.91086163),
                (0.37980617, 54.34120444),
                (0.45932041, 54.77022488),
                (0.54630998, 55.19779227),
                (0.64074838, 55.62377636),
                (0.74260684, 56.04804739),
                (0.85185434, 56.47047613),
                (0.9684576, 56.8909339),
                (1.0923811, 57.30929262),
                (1.22358709, 57.72542486),
                (1.36203561, 58.13920386),
                (1.50768448, 58.55050358),
                (1.66048934, 58.95919874),
                (1.82040364, 59.36516484),
                (1.98737866, 59.76827821),
                (2.16136356, 60.16841608),
                (2.34230532, 60.56545654),
                (2.53014884, 60.95927867),
                (2.7248369, 61.34976249),
                (2.92631018, 61.73678907),
                (3.13450732, 62.12024051),
                (3.34936491, 62.5),
                (3.57081748, 62.87595187),
                (3.7987976, 63.24798161),
                (4.0332358, 63.61597588),
                (4.27406069, 63.97982259),
                (4.52119889, 64.33941091),
                (4.77457514, 64.69463131),
                (5.03411225, 65.04537558),
                (5.29973116, 65.39153688),
                (5.57135096, 65.73300978),
                (5.84888892, 66.06969024),
                (6.13226049, 66.40147572),
                (6.42137936, 66.72826516),
                (6.71615746, 67.049959),
                (7.01650499, 67.36645926),
                (7.32233047, 67.67766953),
                (7.63354074, 67.98349501),
                (7.950041, 68.28384254),
                (8.27173484, 68.57862064),
                (8.59852428, 68.86773951),
                (8.93030976, 69.15111108),
                (9.26699022, 69.42864904),
                (9.60846312, 69.70026884),
                (9.95462442, 69.96588775),
                (10.30536869, 70.22542486),
                (10.66058909, 70.47880111),
                (11.02017741, 70.72593931),
                (11.38402412, 70.9667642),
                (11.75201839, 71.2012024),
                (12.12404813, 71.42918252),
                (12.5, 71.65063509),
                (12.87975949, 71.86549268),
                (13.26321093, 72.07368982),
                (13.65023751, 72.2751631),
                (14.04072133, 72.46985116),
                (14.43454346, 72.65769468),
                (14.83158392, 72.83863644),
                (15.23172179, 73.01262134),
                (15.63483516, 73.17959636),
                (16.04080126, 73.33951066),
                (16.44949642, 73.49231552),
                (16.86079614, 73.63796439),
                (17.27457514, 73.77641291),
                (17.69070738, 73.9076189),
                (18.1090661, 74.0315424),
                (18.52952387, 74.14814566),
                (18.95195261, 74.25739316),
                (19.37622364, 74.35925162),
                (19.80220773, 74.45369002),
                (20.22977512, 74.54067959),
                (20.65879556, 74.62019383),
                (21.08913837, 74.69220851),
                (21.52067248, 74.75670172),
                (21.95326641, 74.81365379),
                (22.38678842, 74.86304738),
                (22.82110643, 74.90486745),
                (23.25608816, 74.93910126),
                (23.69160109, 74.96573837),
                (24.12751258, 74.98477068),
                (24.56368984, 74.99619238),
                (25.0, 75.0),
                (25.43631016, 74.99619238),
                (25.87248742, 74.98477068),
                (26.30839891, 74.96573837),
                (26.74391184, 74.93910126),
                (27.17889357, 74.90486745),
                (27.61321158, 74.86304738),
                (28.04673359, 74.81365379),
                (28.47932752, 74.75670172),
                (28.91086163, 74.69220851),
                (29.34120444, 74.62019383),
                (29.77022488, 74.54067959),
                (30.19779227, 74.45369002),
                (30.62377636, 74.35925162),
                (31.04804739, 74.25739316),
                (31.47047613, 74.14814566),
                (31.8909339, 74.0315424),
                (32.30929262, 73.9076189),
                (32.72542486, 73.77641291),
                (33.13920386, 73.63796439),
                (33.55050358, 73.49231552),
                (33.95919874, 73.33951066),
                (34.36516484, 73.17959636),
                (34.76827821, 73.01262134),
                (35.16841608, 72.83863644),
                (35.56545654, 72.65769468),
                (35.95927867, 72.46985116),
                (36.34976249, 72.2751631),
                (36.73678907, 72.07368982),
                (37.12024051, 71.86549268),
                (37.5, 71.65063509),
                (37.87595187, 71.42918252),
                (38.24798161, 71.2012024),
                (38.61597588, 70.9667642),
                (38.97982259, 70.72593931),
                (39.33941091, 70.47880111),
                (39.69463131, 70.22542486),
                (40.04537558, 69.96588775),
                (40.39153688, 69.70026884),
                (40.73300978, 69.42864904),
                (41.06969024, 69.15111108),
                (41.40147572, 68.86773951),
                (41.72826516, 68.57862064),
                (42.049959, 68.28384254),
                (42.36645926, 67.98349501),
                (42.67766953, 67.67766953),
                (42.98349501, 67.36645926),
                (43.28384254, 67.049959),
                (43.57862064, 66.72826516),
                (43.86773951, 66.40147572),
                (44.15111108, 66.06969024),
                (44.42864904, 65.73300978),
                (44.70026884, 65.39153688),
                (44.96588775, 65.04537558),
                (45.22542486, 64.69463131),
                (45.47880111, 64.33941091),
                (45.72593931, 63.97982259),
                (45.9667642, 63.61597588),
                (46.2012024, 63.24798161),
                (46.42918252, 62.87595187),
                (46.65063509, 62.5),
                (46.86549268, 62.12024051),
                (47.07368982, 61.73678907),
                (47.2751631, 61.34976249),
                (47.46985116, 60.95927867),
                (47.65769468, 60.56545654),
                (47.83863644, 60.16841608),
                (48.01262134, 59.76827821),
                (48.17959636, 59.36516484),
                (48.33951066, 58.95919874),
                (48.49231552, 58.55050358),
                (48.63796439, 58.13920386),
                (48.77641291, 57.72542486),
                (48.9076189, 57.30929262),
                (49.0315424, 56.8909339),
                (49.14814566, 56.47047613),
                (49.25739316, 56.04804739),
                (49.35925162, 55.62377636),
                (49.45369002, 55.19779227),
                (49.54067959, 54.77022488),
                (49.62019383, 54.34120444),
                (49.69220851, 53.91086163),
                (49.75670172, 53.47932752),
                (49.81365379, 53.04673359),
                (49.86304738, 52.61321158),
                (49.90486745, 52.17889357),
                (49.93910126, 51.74391184),
                (49.96573837, 51.30839891),
                (49.98477068, 50.87248742),
                (49.99619238, 50.43631016),
                (50.0, 50.0),
                (50.00380762, 50.43631016),
                (50.01522932, 50.87248742),
                (50.03426163, 51.30839891),
                (50.06089874, 51.74391184),
                (50.09513255, 52.17889357),
                (50.13695262, 52.61321158),
                (50.18634621, 53.04673359),
                (50.24329828, 53.47932752),
                (50.30779149, 53.91086163),
                (50.37980617, 54.34120444),
                (50.45932041, 54.77022488),
                (50.54630998, 55.19779227),
                (50.64074838, 55.62377636),
                (50.74260684, 56.04804739),
                (50.85185434, 56.47047613),
                (50.9684576, 56.8909339),
                (51.0923811, 57.30929262),
                (51.22358709, 57.72542486),
                (51.36203561, 58.13920386),
                (51.50768448, 58.55050358),
                (51.66048934, 58.95919874),
                (51.82040364, 59.36516484),
                (51.98737866, 59.76827821),
                (52.16136356, 60.16841608),
                (52.34230532, 60.56545654),
                (52.53014884, 60.95927867),
                (52.7248369, 61.34976249),
                (52.92631018, 61.73678907),
                (53.13450732, 62.12024051),
                (53.34936491, 62.5),
                (53.57081748, 62.87595187),
                (53.7987976, 63.24798161),
                (54.0332358, 63.61597588),
                (54.27406069, 63.97982259),
                (54.52119889, 64.33941091),
                (54.77457514, 64.69463131),
                (55.03411225, 65.04537558),
                (55.29973116, 65.39153688),
                (55.57135096, 65.73300978),
                (55.84888892, 66.06969024),
                (56.13226049, 66.40147572),
                (56.42137936, 66.72826516),
                (56.71615746, 67.049959),
                (57.01650499, 67.36645926),
                (57.32233047, 67.67766953),
                (57.63354074, 67.98349501),
                (57.950041, 68.28384254),
                (58.27173484, 68.57862064),
                (58.59852428, 68.86773951),
                (58.93030976, 69.15111108),
                (59.26699022, 69.42864904),
                (59.60846312, 69.70026884),
                (59.95462442, 69.96588775),
                (60.30536869, 70.22542486),
                (60.66058909, 70.47880111),
                (61.02017741, 70.72593931),
                (61.38402412, 70.9667642),
                (61.75201839, 71.2012024),
                (62.12404813, 71.42918252),
                (62.5, 71.65063509),
                (62.87975949, 71.86549268),
                (63.26321093, 72.07368982),
                (63.65023751, 72.2751631),
                (64.04072133, 72.46985116),
                (64.43454346, 72.65769468),
                (64.83158392, 72.83863644),
                (65.23172179, 73.01262134),
                (65.63483516, 73.17959636),
                (66.04080126, 73.33951066),
                (66.44949642, 73.49231552),
                (66.86079614, 73.63796439),
                (67.27457514, 73.77641291),
                (67.69070738, 73.9076189),
                (68.1090661, 74.0315424),
                (68.52952387, 74.14814566),
                (68.95195261, 74.25739316),
                (69.37622364, 74.35925162),
                (69.80220773, 74.45369002),
                (70.22977512, 74.54067959),
                (70.65879556, 74.62019383),
                (71.08913837, 74.69220851),
                (71.52067248, 74.75670172),
                (71.95326641, 74.81365379),
                (72.38678842, 74.86304738),
                (72.82110643, 74.90486745),
                (73.25608816, 74.93910126),
                (73.69160109, 74.96573837),
                (74.12751258, 74.98477068),
                (74.56368984, 74.99619238),
                (75.0, 75.0),
                (75.43631016, 74.99619238),
                (75.87248742, 74.98477068),
                (76.30839891, 74.96573837),
                (76.74391184, 74.93910126),
                (77.17889357, 74.90486745),
                (77.61321158, 74.86304738),
                (78.04673359, 74.81365379),
                (78.47932752, 74.75670172),
                (78.91086163, 74.69220851),
                (79.34120444, 74.62019383),
                (79.77022488, 74.54067959),
                (80.19779227, 74.45369002),
                (80.62377636, 74.35925162),
                (81.04804739, 74.25739316),
                (81.47047613, 74.14814566),
                (81.8909339, 74.0315424),
                (82.30929262, 73.9076189),
                (82.72542486, 73.77641291),
                (83.13920386, 73.63796439),
                (83.55050358, 73.49231552),
                (83.95919874, 73.33951066),
                (84.36516484, 73.17959636),
                (84.76827821, 73.01262134),
                (85.16841608, 72.83863644),
                (85.56545654, 72.65769468),
                (85.95927867, 72.46985116),
                (86.34976249, 72.2751631),
                (86.73678907, 72.07368982),
                (87.12024051, 71.86549268),
                (87.5, 71.65063509),
                (87.87595187, 71.42918252),
                (88.24798161, 71.2012024),
                (88.61597588, 70.9667642),
                (88.97982259, 70.72593931),
                (89.33941091, 70.47880111),
                (89.69463131, 70.22542486),
                (90.04537558, 69.96588775),
                (90.39153688, 69.70026884),
                (90.73300978, 69.42864904),
                (91.06969024, 69.15111108),
                (91.40147572, 68.86773951),
                (91.72826516, 68.57862064),
                (92.049959, 68.28384254),
                (92.36645926, 67.98349501),
                (92.67766953, 67.67766953),
                (92.98349501, 67.36645926),
                (93.28384254, 67.049959),
                (93.57862064, 66.72826516),
                (93.86773951, 66.40147572),
                (94.15111108, 66.06969024),
                (94.42864904, 65.73300978),
                (94.70026884, 65.39153688),
                (94.96588775, 65.04537558),
                (95.22542486, 64.69463131),
                (95.47880111, 64.33941091),
                (95.72593931, 63.97982259),
                (95.9667642, 63.61597588),
                (96.2012024, 63.24798161),
                (96.42918252, 62.87595187),
                (96.65063509, 62.5),
                (96.86549268, 62.12024051),
                (97.07368982, 61.73678907),
                (97.2751631, 61.34976249),
                (97.46985116, 60.95927867),
                (97.65769468, 60.56545654),
                (97.83863644, 60.16841608),
                (98.01262134, 59.76827821),
                (98.17959636, 59.36516484),
                (98.33951066, 58.95919874),
                (98.49231552, 58.55050358),
                (98.63796439, 58.13920386),
                (98.77641291, 57.72542486),
                (98.9076189, 57.30929262),
                (99.0315424, 56.8909339),
                (99.14814566, 56.47047613),
                (99.25739316, 56.04804739),
                (99.35925162, 55.62377636),
                (99.45369002, 55.19779227),
                (99.54067959, 54.77022488),
                (99.62019383, 54.34120444),
                (99.69220851, 53.91086163),
                (99.75670172, 53.47932752),
                (99.81365379, 53.04673359),
                (99.86304738, 52.61321158),
                (99.90486745, 52.17889357),
                (99.93910126, 51.74391184),
                (99.96573837, 51.30839891),
                (99.98477068, 50.87248742),
                (99.99619238, 50.43631016),
                (49.99619238, 0.0),
                (0.0, 50.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def heptagon(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a heptagon.

        This function creates and returns a Shape object that visually represents
        a heptagon.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_gon(
            number_of_sides=7,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def hexagon(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a hexagon.

        This function creates and returns a Shape object that visually represents
        a hexagon.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_gon(
            number_of_sides=6,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def isosceles_triangle(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an isosceles triangle.

        This function creates and returns a Shape object that visually represents
        an isosceles triangle.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_gon(
            number_of_sides=3,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def lissajours(
        x_frequency: int,
        y_frequency: int,
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a lissajours figure.

        This function creates and returns a Shape object that visually represents
        a lissajours figure.

        :param x_frequency:
        :param y_frequency:
        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        coords_0: typing.List[typing.Tuple[float, float]] = [
            (
                math.cos(math.radians(i * x_frequency)) * 100,
                math.sin(math.radians(i * y_frequency)) * 100,
            )
            for i in range(0, 360 * x_frequency * y_frequency)
        ]
        coords_0 += [coords_0[0]]
        return Shape(
            coordinates=coords_0,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def n_gon(
        number_of_sides: int,
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a regular n-gon.

        This function creates and returns a Shape object that visually represents
        a regular n-gon.

        :param number_of_sides: the number of vertices in the n-gon
        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        assert isinstance(number_of_sides, int)
        assert number_of_sides >= 3
        coords_0: typing.List[typing.Tuple[float, float]] = [
            (
                math.cos(math.radians(i * 360 // number_of_sides)) * 100,
                math.sin(math.radians(i * 360 // number_of_sides)) * 100,
            )
            for i in range(0, number_of_sides)
        ]
        coords_0 += [coords_0[0]]
        return Shape(
            coordinates=coords_0,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def n_pointed_star(
        number_of_points: int,
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an n-pointed star.

        This function creates and returns a Shape object that visually represents
        an n-pointed star.

        :param number_of_points:    the number of vertices in the star
        :param stroke_color:        the color in which to draw the Shape
        :param fill_color:          the color in which to fill the Shape
        :param line_width:          the line width of the Shape
        :param dash_pattern:        the dash pattern to be used when drawing the Shape
        :param dash_phase:          the dash phase to be used when starting to draw the Shape
        :return:                    a Shape
        """
        assert isinstance(number_of_points, int)
        assert number_of_points >= 3
        m: int = number_of_points * 2
        coords_0: typing.List[typing.Tuple[float, float]] = [
            (
                math.cos(math.radians(i * 360 // m)) * (50 if i % 2 == 0 else 30) - 50,
                math.sin(math.radians(i * 360 // m)) * (50 if i % 2 == 0 else 30) - 50,
            )
            for i in range(0, m)
        ]
        coords_0 += [coords_0[0]]

        return Shape(
            coordinates=coords_0,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def n_toothed_gear(
        number_of_teeth: int,
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an n-toothed gear.

        This function creates and returns a Shape object that visually represents
        an n-toothed gear.

        :param number_of_teeth: the number of gear teeth
        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        assert isinstance(number_of_teeth, int)
        assert number_of_teeth >= 3
        m: int = number_of_teeth * 4
        coords_0: typing.List[typing.Tuple[float, float]] = [
            (
                math.cos(math.radians(i * 360 // m)) * (50 if i % 4 in [0, 3] else 30)
                - 50,
                math.sin(math.radians(i * 360 // m)) * (50 if i % 4 in [0, 3] else 30)
                - 50,
            )
            for i in range(0, m)
        ]
        coords_0 += [coords_0[0]]

        # ring
        coords_1: typing.List[typing.Tuple[float, float]] = [
            (math.cos(math.radians(i)) * 20 - 50, math.sin(math.radians(i)) * 20 - 50)
            for i in range(0, 360)
        ]
        coords_1 += [coords_1[0]]
        return Shape(
            coordinates=[coords_0, coords_1],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def octagon(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting an octagon.

        This function creates and returns a Shape object that visually represents
        an octagon.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_gon(
            number_of_sides=8,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def parallelogram(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a parallelogram.

        This function creates and returns a Shape object that visually represents
        a parallelogram.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (75.0, 0.0),
                (100.0, 100.0),
                (25.0, 100.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def pentagon(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a pentagon.

        This function creates and returns a Shape object that visually represents
        a pentagon.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_gon(
            number_of_sides=5,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def rectangle(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a rectangle.

        This function creates and returns a Shape object that visually represents
        a rectangle.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 61.72839506),
                (100.0, 61.72839506),
                (100.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def rectangular_maze(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        horizontal_scale: int = 10,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
        vertical_scale: int = 10,
    ) -> Shape:
        """
        Return a Shape object depicting a rectangular maze.

        This function creates and returns a Shape object that visually represents
        a rectangular maze.

        :param horizontal_scale:    the horizontal number of cells (a parameter of the maze generation algorithm)
        :param vertical_scale:      the vertical number of cells (a parameter of the maze generation algorithm)
        :param stroke_color:        the color in which to draw the Shape
        :param fill_color:          the color in which to fill the Shape
        :param line_width:          the line width of the Shape
        :param dash_pattern:        the dash pattern to be used when drawing the Shape
        :param dash_phase:          the dash phase to be used when starting to draw the Shape
        :return:                    a Shape
        """
        import random

        walls = [
            [(True, True, True, True) for _ in range(0, vertical_scale)]
            for _ in range(0, horizontal_scale)
        ]
        stk = [(horizontal_scale // 2, vertical_scale // 2)]
        while len(stk) > 0:
            cx, cy = stk[-1]
            nbs = []
            # left
            if cx - 1 >= 0 and walls[cx - 1][cy] == (True, True, True, True):
                nbs += [(cx - 1, cy)]
            # right
            if cx + 1 < len(walls) and walls[cx + 1][cy] == (True, True, True, True):
                nbs += [(cx + 1, cy)]
            # bottom
            if cy - 1 >= 0 and walls[cx][cy - 1] == (True, True, True, True):
                nbs += [(cx, cy - 1)]
            # top
            if cy + 1 < len(walls[0]) and walls[cx][cy + 1] == (True, True, True, True):
                nbs += [(cx, cy + 1)]

            # IF there are no intact neighbours left
            # THEN backtrack
            if len(nbs) == 0:
                stk.pop(-1)
                continue

            # select random neighbour
            nx, ny = random.choice(nbs)
            stk += [(nx, ny)]

            # break down walls
            # left
            if cx - 1 == nx:
                walls[cx][cy] = (
                    walls[cx][cy][0],
                    walls[cx][cy][1],
                    walls[cx][cy][2],
                    False,
                )
                walls[nx][ny] = (
                    walls[nx][ny][0],
                    False,
                    walls[nx][ny][2],
                    walls[nx][ny][3],
                )
            # right
            if cx + 1 == nx:
                walls[cx][cy] = (
                    walls[cx][cy][0],
                    False,
                    walls[cx][cy][2],
                    walls[cx][cy][3],
                )
                walls[nx][ny] = (
                    walls[nx][ny][0],
                    walls[nx][ny][1],
                    walls[nx][ny][2],
                    False,
                )
            # bottom
            if cy - 1 == ny:
                walls[cx][cy] = (
                    walls[cx][cy][0],
                    walls[cx][cy][1],
                    False,
                    walls[cx][cy][3],
                )
                walls[nx][ny] = (
                    False,
                    walls[nx][ny][1],
                    walls[nx][ny][2],
                    walls[nx][ny][3],
                )
            # top
            if cy + 1 == ny:
                walls[cx][cy] = (
                    False,
                    walls[cx][cy][1],
                    walls[cx][cy][2],
                    walls[cx][cy][3],
                )
                walls[nx][ny] = (
                    walls[nx][ny][0],
                    walls[nx][ny][1],
                    False,
                    walls[nx][ny][3],
                )

        # use walls to draw shape
        lines = []
        N: int = len(walls) + 1
        for i in range(0, len(walls)):
            for j in range(0, len(walls[0])):
                # top
                if walls[i][j][0]:
                    lines += [
                        [
                            (i * 10.0, j * 10.0 + 10.0),
                            (i * 10.0 + 10.0, j * 10.0 + 10.0),
                        ]
                    ]
                # right
                if walls[i][j][1]:
                    lines += [
                        [
                            (i * 10.0 + 10.0, j * 10.0 + 10.0),
                            (i * 10.0 + 10.0, j * 10.0),
                        ]
                    ]
                # bottom
                if walls[i][j][2]:
                    lines += [[(i * 10.0, j * 10.0), (i * 10.0 + 10.0, j * 10.0)]]
                # left
                if walls[i][j][3]:
                    lines += [[(i * 10.0, j * 10.0 + 10.0), (i * 10.0, j * 10.0)]]
        return Shape(
            coordinates=lines,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        ).scale_to_fit(size=(100, 100))

    @staticmethod
    def right_angled_triangle(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a right-angled triangle.

        This function creates and returns a Shape object that visually represents
        a right-angled triangle.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[(0.0, 0.0), (0, 100), (100, 0), (0, 0)],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def six_pointed_star(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a six-pointed star.

        This function creates and returns a Shape object that visually represents
        a six-pointed star.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.n_pointed_star(
            number_of_points=6,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_phase=dash_phase,
            dash_pattern=dash_pattern,
        )

    @staticmethod
    def square(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a square.

        This function creates and returns a Shape object that visually represents
        a square.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[(0.0, 0.0), (0, 100), (100, 100), (100, 0), (0, 0)],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def sticky_note(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a sticky note.

        This function creates and returns a Shape object that visually represents
        a sticky note.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[
                (0.0, 0.0),
                (0.0, 100.0),
                (100.0, 100.0),
                (100.0, 10.0),
                (90.0, 10.0),
                (90.0, 0.0),
                (100.0, 10.0),
                (90.0, 0.0),
                (0.0, 0.0),
            ],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def three_quarters_of_circle(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting three quarters of a circle.

        This function creates and returns a Shape object that visually represents
        three quarters of a circle.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return LineArt.fraction_of_circle(
            angle_in_degrees=270,
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )

    @staticmethod
    def trapezoid(
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        line_width: int = 1,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
    ) -> Shape:
        """
        Return a Shape object depicting a trapezoid.

        This function creates and returns a Shape object that visually represents
        a trapezoid.

        :param stroke_color:    the color in which to draw the Shape
        :param fill_color:      the color in which to fill the Shape
        :param line_width:      the line width of the Shape
        :param dash_pattern:    the dash pattern to be used when drawing the Shape
        :param dash_phase:      the dash phase to be used when starting to draw the Shape
        :return:                a Shape
        """
        return Shape(
            coordinates=[(0.0, 0.0), (19, 100), (81, 100), (100, 0), (0, 0)],
            stroke_color=stroke_color,
            fill_color=fill_color,
            line_width=line_width,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
        )
