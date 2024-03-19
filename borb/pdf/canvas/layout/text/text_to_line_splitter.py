#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class is responsible for splitting text (to be fit into a Paragraph)
"""
import re
import typing
from decimal import Decimal

from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.glyph_line import GlyphLine
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation


class TextToLineSplitter:
    """
    This class is responsible for splitting text (to be fit into a Paragraph)
    """

    HYPHENATION_CHARACTER: str = "-"

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
    def text_to_lines(
        bounding_box: Rectangle,
        font: Font,
        font_size: Decimal,
        text: str,
        hyphenation: typing.Optional[Hyphenation] = None,
        respect_newlines: bool = False,
        respect_spaces: bool = False,
    ) -> typing.List[str]:
        """
        This function splits a large str into smaller parts for layout.
        :param bounding_box:        the bounding box in which the str(s) must fit
        :param font:                the Font in which to render the str(s)
        :param font_size:           the font_size in which to render the str(s)
        :param text:                the text to split
        :param hyphenation:         a Hyphenation object, or None (default None)
        :param respect_newlines:    whether to respect newline characters in the input (default False)
        :param respect_spaces:      whether to respect spaces in the input (default False)
        :return:

        """
        # trivial case(s)
        if text == "":
            return [""]
        if text == " ":
            return [" "] if respect_spaces else [""]

        # handle newlines
        if "\n" in text:
            if respect_newlines:
                tmp01: typing.List[str] = []
                for partial_text in text.split("\n"):
                    tmp01.extend(
                        TextToLineSplitter.text_to_lines(
                            bounding_box=bounding_box,
                            font=font,
                            font_size=font_size,
                            text=partial_text,
                            respect_spaces=respect_spaces,
                            respect_newlines=False,
                        )
                    )
                return tmp01
            else:
                text = re.sub("\n+", " ", text)

        # IF not respect_spaces
        # THEN remove multiple consecutive spaces
        if not respect_spaces:
            text = re.sub("[ \t]+", " ", text)
            text = text.strip()

        # build output list
        out: typing.List[typing.List[str]] = []
        chars_per_line_estimate: int = max(
            int(bounding_box.get_width() / (Decimal(0.5) * font_size)), 1
        )

        # split into tokens (keep delimiter)
        tokens: typing.List[str] = []
        for c in text:
            if c.isspace():
                tokens.append(c)
                tokens.append("")
            else:
                if len(tokens) == 0:
                    tokens.append(c)
                else:
                    tokens[-1] += c

        # main loop
        while len(tokens) > 0:
            # initial estimate
            tokens_in_line: typing.List[str] = []
            while (
                len(tokens)
                and sum([len(x) for x in tokens_in_line]) < chars_per_line_estimate
            ):
                # IF the first token is a space (and we are not respecting spaces)
                # THEN drop the space character
                if (
                    not respect_spaces
                    and tokens[0].isspace()
                    and len(tokens_in_line) == 0
                ):
                    tokens.pop(0)
                    continue

                # default
                tokens_in_line.append(tokens[0])
                tokens.pop(0)

            # actually measure line
            # fmt: off
            line_width: Decimal = GlyphLine.from_str("".join(tokens_in_line), font, font_size).get_width_in_text_space()
            free_line_width: Decimal = Decimal(round(bounding_box.width - line_width, 2))
            # fmt: on

            # IF free_line_width == 0
            # THEN  everything goes straight to tokens_in_line
            if free_line_width == 0:
                out.append(tokens_in_line)
                continue

            # IF free_line_width > 0
            # THEN  add more tokens from "tokens" until text just fits
            #       update estimate
            future_tokens_in_line: typing.List[str] = []
            max_hyphenation_index: typing.Optional[int] = None
            token_parts: typing.List[str] = []
            if free_line_width > 0:
                while free_line_width > 0 and len(tokens) > 0:
                    future_tokens_in_line = tokens_in_line + [tokens[0]]

                    # calculate (future) free_line_width
                    # fmt: off
                    future_line_width = GlyphLine.from_str("".join(future_tokens_in_line), font, font_size).get_width_in_text_space()
                    future_free_line_width = Decimal(round(bounding_box.width - future_line_width, 2))
                    # fmt: on

                    # if it fits, add it
                    if future_free_line_width >= 0:
                        free_line_width = future_line_width
                        tokens_in_line = future_tokens_in_line
                        tokens.pop(0)
                    else:
                        break

                #
                # hyphenation (AFTER UNDERFLOW)
                #
                future_tokens_in_line = []
                max_hyphenation_index = None
                token_parts = []
                if hyphenation is not None and len(tokens) > 0:
                    token_parts = hyphenation.hyphenate(tokens[0]).split(chr(173))
                    max_hyphenation_index = None

                    # check every split
                    for i in range(1, len(token_parts) + 1):
                        future_tokens_in_line = (
                            tokens_in_line
                            + token_parts[:i]
                            + [TextToLineSplitter.HYPHENATION_CHARACTER]
                        )

                        # calculate (future) free_line_width
                        # fmt: off
                        future_line_width = GlyphLine.from_str("".join(future_tokens_in_line), font, font_size).get_width_in_text_space()
                        future_free_line_width = Decimal(round(bounding_box.width - future_line_width, 2))
                        # fmt: on

                        # if it fits, add it
                        if future_free_line_width >= 0:
                            max_hyphenation_index = i

                    # IF it is possible to hyphenate
                    # THEN do it at the appropriate (max) index
                    if max_hyphenation_index is not None:
                        tokens_in_line += hyphenation.hyphenate(tokens[0]).split(
                            chr(173)
                        )[:max_hyphenation_index] + [
                            TextToLineSplitter.HYPHENATION_CHARACTER
                        ]
                        tokens = (
                            hyphenation.hyphenate(tokens[0]).split(chr(173))[
                                max_hyphenation_index:
                            ]
                            + tokens[1:]
                        )

                # store output
                out.append(tokens_in_line)

                # update estimate
                chars_per_line_estimate = max(
                    sum([sum([len(t) for t in l]) for l in out]) // len(out), 1
                )

                # move to next iteration
                continue

            # IF free_line_width < 0
            # THEN  put tokens back until free_line_width >= 0
            #       update estimate
            if free_line_width < 0:
                while free_line_width < 0:
                    # move token back to "tokens"
                    tokens.insert(0, tokens_in_line[-1])
                    tokens_in_line.pop(-1)

                    # re-calculate free_line_width
                    # fmt: off
                    line_width = GlyphLine.from_str("".join(tokens_in_line), font, font_size).get_width_in_text_space()
                    free_line_width = Decimal(round(bounding_box.width - line_width, 2))
                    # fmt: on

                #
                # hyphenation (AFTER OVERFLOW)
                #

                if hyphenation is not None and len(tokens) > 0:
                    token_parts = hyphenation.hyphenate(tokens[0]).split(chr(173))
                    max_hyphenation_index = None

                    # check every split
                    for i in range(1, len(token_parts) + 1):
                        future_tokens_in_line = (
                            tokens_in_line
                            + token_parts[:i]
                            + [TextToLineSplitter.HYPHENATION_CHARACTER]
                        )

                        # calculate (future) free_line_width
                        # fmt: off
                        future_line_width = GlyphLine.from_str("".join(future_tokens_in_line), font, font_size).get_width_in_text_space()
                        future_free_line_width = Decimal(round(bounding_box.width - future_line_width, 2))
                        # fmt: on

                        # if it fits, add it
                        if future_free_line_width >= 0:
                            max_hyphenation_index = i

                    # IF it is possible to hyphenate
                    # THEN do it at the appropriate (max) index
                    if max_hyphenation_index is not None:
                        tokens_in_line += hyphenation.hyphenate(tokens[0]).split(
                            chr(173)
                        )[:max_hyphenation_index] + [
                            TextToLineSplitter.HYPHENATION_CHARACTER
                        ]
                        tokens = (
                            hyphenation.hyphenate(tokens[0]).split(chr(173))[
                                max_hyphenation_index:
                            ]
                            + tokens[1:]
                        )

                # IF tokens_in_line == 0
                # IT MEANS  we previously had tokens on this line, otherwise free_line_width would be positive
                #           we currently have no tokens on this line
                #           there is 1 token on this line that is too big for this line
                # THEN      raise AssertionErrors
                if len(tokens_in_line) == 0:
                    assert (
                        False
                    ), f"Text '{text}' can not be split to inside the given bounds ({bounding_box.width}, {bounding_box.height})"

                # store output
                out.append(tokens_in_line)

                # update estimate
                chars_per_line_estimate = max(
                    sum([sum([len(t) for t in l]) for l in out]) // len(out), 1
                )

                # move to next iteration
                continue

        # IF we do not respect spaces
        # THEN remove any trailing spaces from each line
        # (this has a huge impact on text that is aligned JUSTIFIED)
        if not respect_spaces:
            for i in range(0, len(out)):
                while len(out) > 0 and out[i][-1] == " ":
                    out[i] = out[i][:-1]

        # IF we do not respect newlines
        # THEN remove any trailing newlines
        if not respect_newlines:
            while len(out) > 0 and len(out[-1]) == 1 and out[-1][-1] == "":
                out.pop(-1)

        # return
        return ["".join(l) for l in out]
