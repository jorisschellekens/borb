#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a CIDFont Type 0 in a PDF.

The `CIDType0Font` class models a CIDFont of Type 0, a descendant font type used in
composite fonts within PDF documents. CIDFonts (Character Identifier Fonts) are designed
to support large glyph sets through the use of CIDs, which are numeric glyph identifiers
that decouple character codes from glyph representations.

CIDType0 fonts are typically used for representing CJK (Chinese, Japanese, Korean) scripts
and other large character sets where the traditional 8-bit font encodings are insufficient.
These fonts are used in conjunction with a CMap that defines the mapping between character
codes and CIDs.

This class extends the `Font` base class with additional mechanisms for handling CID
mappings, font descriptors, and system-specific attributes essential for rendering
multi-byte encoded text.
"""
import typing

from borb.pdf.font.font import Font


class CIDType0Font(Font):
    """
    Represents a CIDFont Type 0 in a PDF.

    The `CIDType0Font` class models a CIDFont of Type 0, a descendant font type used in
    composite fonts within PDF documents. CIDFonts (Character Identifier Fonts) are designed
    to support large glyph sets through the use of CIDs, which are numeric glyph identifiers
    that decouple character codes from glyph representations.

    CIDType0 fonts are typically used for representing CJK (Chinese, Japanese, Korean) scripts
    and other large character sets where the traditional 8-bit font encodings are insufficient.
    These fonts are used in conjunction with a CMap that defines the mapping between character
    codes and CIDs.

    This class extends the `Font` base class with additional mechanisms for handling CID
    mappings, font descriptors, and system-specific attributes essential for rendering
    multi-byte encoded text.
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

    def get_width(
        self,
        text: typing.List[typing.Tuple[int, str]],  # type: ignore[override]
        character_spacing: float = 0,
        font_size: float = 12,
        word_spacing: float = 0,
    ) -> int:
        """
        Return the total width of a text string when rendered with the font at a specific size.

        This function calculates the width of the given text string when rendered with the font
        at the specified font size.

        :param font_size:           The font size to be used for rendering.
        :param text:                The text (cid and their corresponding character name) to calculate the width for.
        :param word_spacing:        The word spacing to be used for rendering
        :param character_spacing:   The character spacing to be used for rendering
        :return:                    The width (in points) of the text in the specified font size.
        """
        # Default value: none (the DW value shall be used for all glyphs).
        if "W" not in self:
            return self.get("DW", 1000)

        assert "W" in self
        W: typing.List[typing.Union[int, typing.List[int]]] = self.get("W", [])

        # loop over cids to determine widths
        cid_width_cache: typing.Dict[int, float] = {}
        cid_widths: typing.List[float] = []
        for cid, character_name in text:

            # IF the item is cached
            # THEN use the cache
            if cid in cid_width_cache:
                cid_widths += [cid_width_cache[cid]]
                continue

            # <cid> [<width> ... <width>]
            index: typing.Optional[int] = next(
                iter(
                    [
                        i
                        for i in range(0, len(W))
                        if isinstance(W[i], int)
                        and (i + 1) < len(W)
                        and isinstance(W[i + 1], list)
                        and W[i] <= cid < W[i] + len(W[i + 1])  # type: ignore[arg-type, operator]
                    ]
                ),
                None,
            )
            if index is not None:
                cid_widths += [W[index + 1][cid - W[index]]]  # type: ignore[index, operator]
                cid_width_cache[cid] = cid_widths[-1]
                continue

            # <cid> <cid> <width>
            index = next(
                iter(
                    [
                        i
                        for i in range(0, len(W))
                        if isinstance(W[i], int)
                        and (i + 1) < len(W)
                        and (isinstance(W[i + 1], float) or isinstance(W[i + 1], int))
                        and (i + 2) < len(W)
                        and (isinstance(W[i + 2], float) or isinstance(W[i + 2], int))
                        and W[i] <= cid <= W[i + 1]  # type: ignore[operator]
                    ]
                )
            )
            if index is not None:
                cid_widths += [W[index + 2]]  # type: ignore[list-item]
                cid_width_cache[cid] = cid_widths[-1]
                continue

            # DW
            cid_widths += [self.get("DW", 1000)]
            cid_width_cache[cid] = cid_widths[-1]

        # normalize
        cid_widths = [w / 1000 for w in cid_widths]

        # apply character spacing
        cid_widths = [(w + character_spacing) for w in cid_widths]
        cid_widths[-1] -= character_spacing

        # apply word spacing
        cid_widths = [
            (cid_widths[i] + word_spacing) if text[i][1] == "space" else cid_widths[i]
            for i in range(0, len(text))
        ]

        # apply font size
        import math

        return math.ceil(sum(cid_widths) * font_size)
