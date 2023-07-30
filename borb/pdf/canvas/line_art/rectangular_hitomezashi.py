#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sashiko (刺し子, lit. "little stabs") is a type of traditional Japanese embroidery or stitching used for the decorative and/or functional reinforcement of cloth and clothing.

Owing to the relatively cheap nature of white cotton thread and the abundant nature of cheap, indigo-dyed blue cloth in historical Japan,
sashiko has a distinctive appearance of white-on-blue embroidery, though some decorative pieces may also use red thread.

First coming into existence in the Edo period (1603-1867), sashiko embroidery was first applied to clothing out of a practical need,
and would have been used to strengthen the homespun clothes of olden times.
Worn out clothes were pieced together to make new garments by using simple running stitches.

These clothes increased their strength with this durable embroidery.
By the Meiji period (1868-1912), sashiko had been established enough that it had evolved into winter work in northern farming communities,
when it was too cold to work outside.

Sashiko was commonly used to reinforce already-patched clothing around points of wear,
but would also be used to attach patches to clothing, making the fabric ultimately stronger.
It would also be used to layer thin fabrics to create warmth, and, in the case of some garments such as the coats of firemen (hikeshibanten),
to create a thick and absorbent material that would be soaked in water before carrying out duties as a fireman.

Though most sashiko utilises only a plain running stitch technique, sashiko is commonly used to create decorative and repeated embroidered patterns,
and may be used for purely decorative purposes, such as in the creation of quilts and embroidery samplers.

Sashiko utilises mostly geometric patterns, which fall into two main styles; moyōzashi,
in which patterns are created with long lines of running stitches; and hitomezashi,
where the pattern emerges from the alignment of single stitches made on a grid.

Common sashiko motifs are waves, mountains, bamboo, arrow feathers, shippō-tsunagi, pampas grass and interlocking geometric shapes,
amongst others; sashiko embroidery is traditionally applied with the use of specialist needles and thread,
though modern day sashiko may use modern embroidery threads and embroidery needles.
"""
import random
import typing
from decimal import Decimal


class RectangularHitomezashi:
    """
    Sashiko (刺し子, lit. "little stabs") is a type of traditional Japanese embroidery or stitching used for the decorative and/or functional reinforcement of cloth and clothing.

    Owing to the relatively cheap nature of white cotton thread and the abundant nature of cheap, indigo-dyed blue cloth in historical Japan,
    sashiko has a distinctive appearance of white-on-blue embroidery, though some decorative pieces may also use red thread.

    First coming into existence in the Edo period (1603-1867), sashiko embroidery was first applied to clothing out of a practical need,
    and would have been used to strengthen the homespun clothes of olden times.
    Worn out clothes were pieced together to make new garments by using simple running stitches.

    These clothes increased their strength with this durable embroidery.
    By the Meiji period (1868-1912), sashiko had been established enough that it had evolved into winter work in northern farming communities,
    when it was too cold to work outside.

    Sashiko was commonly used to reinforce already-patched clothing around points of wear,
    but would also be used to attach patches to clothing, making the fabric ultimately stronger.
    It would also be used to layer thin fabrics to create warmth, and, in the case of some garments such as the coats of firemen (hikeshibanten),
    to create a thick and absorbent material that would be soaked in water before carrying out duties as a fireman.

    Though most sashiko utilises only a plain running stitch technique, sashiko is commonly used to create decorative and repeated embroidered patterns,
    and may be used for purely decorative purposes, such as in the creation of quilts and embroidery samplers.

    Sashiko utilises mostly geometric patterns, which fall into two main styles; moyōzashi,
    in which patterns are created with long lines of running stitches; and hitomezashi,
    where the pattern emerges from the alignment of single stitches made on a grid.

    Common sashiko motifs are waves, mountains, bamboo, arrow feathers, shippō-tsunagi, pampas grass and interlocking geometric shapes,
    amongst others; sashiko embroidery is traditionally applied with the use of specialist needles and thread,
    though modern day sashiko may use modern embroidery threads and embroidery needles.
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
    def hitomezashi(
        horizontal_seed: typing.List[bool] = [
            random.choice([True, False, False]) for _ in range(0, 32)
        ],
        vertical_seed: typing.List[bool] = [
            random.choice([True, False, False]) for _ in range(0, 32)
        ],
    ):
        """
        This function generates a rectangular Hitomezashi grid pattern
        :param horizontal_seed:     a typing.List[bool] to be used as the horizontal seed
        :param vertical_seed:       a typing.List[bool] to be used as the vertical seed
        :return:                    a rectangular Hitomezashi pattern, represented as a typing.List[typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]]
        """

        # keep track of lines
        lines: typing.List[
            typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]
        ] = []

        # build grid
        w: int = len(horizontal_seed)
        h: int = len(vertical_seed)
        for i in range(0, w):
            for j in range(0, h):
                x: Decimal = Decimal(i * 10)
                y: Decimal = Decimal(j * 10)

                # draw line?
                f0: bool = (i % 2 == 0) if vertical_seed[j] else (i % 2 == 1)
                if f0:
                    lines.append(((x, y), (x + 10, y)))

                # draw line?
                f1: bool = (j % 2 == 0) if horizontal_seed[i] else (j % 2 == 1)
                if f1:
                    lines.append(((x, y), (x, y + 10)))

        # return
        return lines
