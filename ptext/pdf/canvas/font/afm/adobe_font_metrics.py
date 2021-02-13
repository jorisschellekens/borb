#!/usr/bin/env python

import os
import pathlib
import re
import typing
from typing import Optional

from ptext.io.read.types import List, Name, Decimal
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.font_descriptor import FontDescriptor


class AdobeFontMetrics:
    """
    ASCII text-based font format developed by Adobe; stores font metric data for a Type 1 PostScript file;
    contains the master design of a specific font, which defines the way each character of the font looks.
    """

    _font_cache: typing.Dict[str, Optional[Font]] = {}

    @staticmethod
    def get(name: str) -> Optional[Font]:
        """
        Get the Font (only the metrics will be filled in) with a given name
        """
        # standardize names
        canonical_name = re.sub("[^A-Z]+", "", name.upper())

        # find all available afm files
        parent_dir = pathlib.Path(__file__).parent
        available_font_metrics = {
            re.sub("[^A-Z]+", "", x.upper()[:-4]): x
            for x in os.listdir(parent_dir)
            if x.endswith(".afm")
        }

        # check whether given name is present
        afm_file_name: Optional[str] = available_font_metrics.get(canonical_name, None)
        if afm_file_name is None:
            return None
        assert afm_file_name is not None

        # read file
        if afm_file_name not in AdobeFontMetrics._font_cache:
            with open(parent_dir / afm_file_name, "r") as afm_file_handle:
                AdobeFontMetrics._font_cache[
                    afm_file_name
                ] = AdobeFontMetrics._read_file(afm_file_handle)

        # read cache
        if afm_file_name in AdobeFontMetrics._font_cache:
            return AdobeFontMetrics._font_cache[afm_file_name]

        # default
        return None

    @staticmethod
    def _read_file(input: typing.TextIO) -> Optional[Font]:
        lines: typing.List[str] = [x for x in input.readlines()]
        lines = [x for x in lines if not x.startswith("Comment")]
        lines = [x[:-1] if x.endswith("\n") else x for x in lines]

        # check first/last line
        if not lines[0].startswith("StartFontMetrics") or not lines[-1].startswith(
            "EndFontMetrics"
        ):
            return None

        out_font = Font()

        # FontDescriptor
        out_font_descriptor = FontDescriptor().set_parent(out_font)  # type: ignore [attr-defined]
        out_font_descriptor[Name("FontName")] = Name(
            AdobeFontMetrics._find_and_parse_as_string(lines, "FontName")
        )
        out_font_descriptor[Name("FontFamily")] = Name(
            AdobeFontMetrics._find_and_parse_as_string(lines, "FamilyName")
        )
        # FontStretch
        # FontWeight
        # Flags
        # FontBBox
        # ItalicAngle
        # Ascent
        ascent = AdobeFontMetrics._find_and_parse_as_float(lines, "Ascender")
        if ascent:
            out_font_descriptor[Name("Ascent")] = Decimal(ascent)
        # Descent
        descent = AdobeFontMetrics._find_and_parse_as_float(lines, "Descender")
        if descent:
            out_font_descriptor[Name("Descent")] = Decimal(descent)
        # Leading
        # CapHeight
        capheight = AdobeFontMetrics._find_and_parse_as_float(lines, "CapHeight")
        if capheight:
            out_font_descriptor[Name("CapHeight")] = Decimal(capheight)
        # XHeight
        xheight = AdobeFontMetrics._find_and_parse_as_float(lines, "XHeight")
        if xheight:
            out_font_descriptor[Name("XHeight")] = Decimal(xheight)

        # StemV
        stemv = AdobeFontMetrics._find_and_parse_as_float(lines, "StemV")
        if stemv:
            assert stemv is not None
            out_font_descriptor[Name("StemV")] = Decimal(stemv)

        # StemH
        stemh = AdobeFontMetrics._find_and_parse_as_float(lines, "StemH")
        if stemh:
            assert stemh is not None
            out_font_descriptor[Name("StemH")] = Decimal(stemh)

        # AvgWidth
        avgwidth = AdobeFontMetrics._find_and_parse_as_float(lines, "AvgWidth")
        if avgwidth:
            assert avgwidth is not None
            out_font_descriptor[Name("AvgWidth")] = Decimal(avgwidth)

        # MaxWidth
        maxwidth = AdobeFontMetrics._find_and_parse_as_float(lines, "MaxWidth")
        if maxwidth:
            assert maxwidth is not None
            out_font_descriptor[Name("MaxWidth")] = Decimal(maxwidth)

        # MissingWidth
        missingwidth = AdobeFontMetrics._find_and_parse_as_float(lines, "MissingWidth")
        if missingwidth:
            assert missingwidth is not None
            out_font_descriptor[Name("MissingWidth")] = Decimal(missingwidth)

        # CharSet
        charset = AdobeFontMetrics._find_and_parse_as_float(lines, "CharSet")
        if charset:
            assert charset is not None
            out_font_descriptor[Name("CharSet")] = Decimal(charset)

        # Font
        out_font[Name("Type")] = Name("Font")
        out_font[Name("Subtype")] = Name("Type1")
        out_font[Name("Name")] = out_font_descriptor["FontName"]
        out_font[Name("BaseFont")] = out_font_descriptor["FontName"]

        widths = List().set_parent(out_font)  # type: ignore [attr-defined]
        avg_char_width: float = 0
        avg_char_width_norm: float = 0
        first_char = None
        last_char = None

        char_metrics_lines = lines[
            lines.index(
                [x for x in lines if x.startswith("StartCharMetrics")][0]
            ) : lines.index("EndCharMetrics")
            + 1
        ]
        char_metrics_lines = char_metrics_lines[1:-1]
        for cml in char_metrics_lines:
            tmp = {
                y.split(" ")[0]: y.split(" ")[1]
                for y in [x.strip() for x in cml.split(";")]
                if " " in y
            }

            # determine char
            ch = -1
            if "C" in tmp:
                ch = int(tmp["C"])
            if "CH" in tmp:
                ch = int(tmp["CH"][1:-1], 16)

            if (first_char is None or ch < first_char) and ch != -1:
                first_char = ch
            if (last_char is None or ch > last_char) and ch != -1:
                last_char = ch

            w = float(tmp["WX"])
            if ch != -1 and w != 0:
                avg_char_width += w
                avg_char_width_norm += 1

            widths.append(Decimal(w))

        assert first_char is not None
        assert last_char is not None

        out_font[Name("FirstChar")] = Decimal(first_char)
        out_font[Name("LastChar")] = Decimal(last_char)
        out_font[Name("Widths")] = widths

        if avgwidth is None:
            out_font_descriptor[Name("AvgWidth")] = Decimal(
                round(Decimal(avg_char_width / avg_char_width_norm), 2)
            )
        if maxwidth is None:
            out_font_descriptor[Name("MaxWidth")] = Decimal(max(widths))
        out_font[Name("FontDescriptor")] = out_font_descriptor

        # return
        return out_font

    @staticmethod
    def _find_line(lines: typing.List[str], key: str) -> Optional[str]:
        relevant_lines: typing.List[str] = [x for x in lines if x.startswith(key)]
        if len(relevant_lines) == 0:
            return None
        relevant_line = relevant_lines[0][len(key) :]
        # trim white space
        while relevant_line[0] in [" ", "\t"]:
            relevant_line = relevant_line[1:]
        return relevant_line

    @staticmethod
    def _find_and_parse_as_string(lines: typing.List[str], key: str) -> Optional[str]:
        return AdobeFontMetrics._find_line(lines, key)

    @staticmethod
    def _find_and_parse_as_integer(lines: typing.List[str], key: str) -> Optional[int]:
        relevant_line = AdobeFontMetrics._find_line(lines, key)
        return int(relevant_line) if relevant_line is not None else None

    @staticmethod
    def _find_and_parse_as_float(lines: typing.List[str], key: str) -> Optional[float]:
        relevant_line = AdobeFontMetrics._find_line(lines, key)
        return float(relevant_line) if relevant_line is not None else None

    @staticmethod
    def _find_and_parse_as_bool(lines: typing.List[str], key: str) -> Optional[bool]:
        relevant_line = AdobeFontMetrics._find_line(lines, key)
        return (relevant_line.upper() == "TRUE") if relevant_line is not None else None
