#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A composite font, also called a Type 0 font, is one whose glyphs are obtained from a fontlike object called a
CIDFont. A composite font shall be represented by a font dictionary whose Subtype value is Type0. The Type
0 font is known as the root font, and its associated CIDFont is called its descendant.
"""
import logging
import typing
from pathlib import Path

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import List, Name, Stream
from borb.pdf.canvas.font.font import Font

logger = logging.getLogger(__name__)


class Type0Font(Font):
    """
    A composite font, also called a Type 0 font, is one whose glyphs are obtained from a fontlike object called a
    CIDFont. A composite font shall be represented by a font dictionary whose Subtype value is Type0. The Type
    0 font is known as the root font, and its associated CIDFont is called its descendant.
    """

    def __init__(self):
        super(Type0Font, self).__init__()
        self[Name("Type")] = Name("Font")
        self[Name("Subtype")] = Name("Type0")
        self._character_identifier_to_unicode_lookup: typing.Dict[int, str] = {}
        self._unicode_lookup_to_character_identifier: typing.Dict[str, int] = {}
        self._byte_to_char_identifier: typing.Dict[int, int] = {}

    def _read_to_unicode(self):
        if len(self._unicode_lookup_to_character_identifier) > 0:
            return
        assert "ToUnicode" in self
        assert "DecodedBytes" in self["ToUnicode"]
        cmap_bytes: bytes = self["ToUnicode"]["DecodedBytes"]
        self._character_identifier_to_unicode_lookup = self._read_cmap(cmap_bytes)
        self._unicode_lookup_to_character_identifier: typing.Dict[str, int] = {}
        for k, v in self._character_identifier_to_unicode_lookup.items():
            if v not in self._unicode_lookup_to_character_identifier:
                self._unicode_lookup_to_character_identifier[v] = k

    def _read_encoding_cmap(self):
        if len(self._byte_to_char_identifier) > 0:
            return
        assert "Encoding" in self
        assert "DecodedBytes" in self["Encoding"]
        cmap_bytes: bytes = self["Encoding"]["DecodedBytes"]
        self._byte_to_char_identifier = {
            k: v for k, v in self._read_cmap(cmap_bytes).items()
        }
        self._char_to_byte_identifier = {
            v: k for k, v in self._byte_to_char_identifier.items()
        }

    def character_identifier_to_unicode(
        self, character_identifier: int
    ) -> typing.Optional[str]:
        """
        This function maps a character identifier to its unicode str.
        If no such mapping exists, this function returns None.
        """

        # If the font dictionary contains a ToUnicode CMap (see 9.10.3, "ToUnicode CMaps"), use that CMap to
        # convert the character code to Unicode.
        if Name("ToUnicode") in self:
            self._read_to_unicode()
            return self._character_identifier_to_unicode_lookup.get(
                character_identifier
            )

        if Name("Encoding") in self:

            # a) Map the character code to a character identifier (CID) according to the font’s CMap.
            cid: typing.Optional[int] = None
            if isinstance(self["Encoding"], Name):
                encoding_name: str = str(self["Encoding"])
                assert encoding_name in ["Identity", "Identity-H"]
                cid = character_identifier
            if isinstance(self["Encoding"], Stream):
                self._read_encoding_cmap()
                cid = self._byte_to_char_identifier.get(character_identifier)
            if cid is None:
                return None
            assert cid is not None

            # d) Obtain the CMap with the name constructed in step (c) (available from the ASN Web site; see the
            # Bibliography).
            # https://github.com/adobe-type-tools/cmap-resources
            if len(self._character_identifier_to_unicode_lookup) == 0:
                self._character_identifier_to_unicode_lookup = (
                    Type0Font._find_best_matching_predefined_cmap(self._get_cmap_name())
                )
                self._unicode_lookup_to_character_identifier = {
                    v: k
                    for k, v in self._character_identifier_to_unicode_lookup.items()
                }

            # e) Map the CID obtained in step (a) according to the CMap obtained in step (d), producing a
            # Unicode value.
            return self._character_identifier_to_unicode_lookup.get(cid, None)

        # default
        return None

    def _get_cmap_name(self) -> str:
        # b) Obtain the registry and ordering of the character collection used by the font’s CMap
        # (for example, Adobe and Japan1) from its CIDSystemInfo dictionary.
        assert "DescendantFonts" in self
        assert isinstance(self["DescendantFonts"], List)
        assert len(self["DescendantFonts"]) == 1
        assert "CIDSystemInfo" in self["DescendantFonts"][0]
        assert "Registry" in self["DescendantFonts"][0]["CIDSystemInfo"]
        assert "Ordering" in self["DescendantFonts"][0]["CIDSystemInfo"]
        registry: str = str(self["DescendantFonts"][0]["CIDSystemInfo"]["Registry"])
        ordering: str = str(self["DescendantFonts"][0]["CIDSystemInfo"]["Ordering"])

        # c) Construct a second CMap name by concatenating the registry and ordering obtained in step (b) in
        # the format registry–ordering–UCS2 (for example, Adobe–Japan1–UCS2).
        cmap_name: str = "".join([registry, "-", ordering, "-", "UCS2"])

        return cmap_name

    @staticmethod
    def _find_best_matching_predefined_cmap(cmap_name: str) -> typing.Dict[int, str]:
        cmap_dir: Path = Path(__file__).parent / "cmaps"
        assert cmap_dir.exists()
        predefined_cmaps: typing.List[str] = [x.name for x in cmap_dir.iterdir()]

        # pseudo match
        if cmap_name not in predefined_cmaps:

            if cmap_name == "Adobe-Identity-UCS2":
                # fmt: off
                logger.info("Encoding Adobe-Identity-UCS2 was specified, using Adobe-Identity-H in stead")
                cmap_name = "Adobe-Identity-H"
                # fmt: on

            if cmap_name == "Adobe-Japan1-UCS2":
                # fmt: off
                logger.info("Encoding Adobe-Identity-UCS2 was specified, using Adobe-Japan1-0 in stead")
                cmap_name = "Adobe-Japan1-0"
                # fmt: on

            if cmap_name not in predefined_cmaps:
                # fmt: off
                logger.info("Encoding %s was specified, defaulting to Adobe-Identity-H in stead" % cmap_name)
                cmap_name = "Adobe-Identity-H"
                # fmt: on

        # read predefined cmap
        cmap_bytes: typing.Optional[bytes] = None
        with open(cmap_dir / cmap_name, "rb") as cmap_file_handle:
            cmap_bytes = cmap_file_handle.read()
        assert cmap_bytes is not None

        # use Font._read_cmap to process (and return)
        return Font._read_cmap(cmap_bytes)

    def unicode_to_character_identifier(self, unicode: str) -> typing.Optional[int]:
        """
        This function maps a unicode str to its character identifier.
        If no such mapping exists, this function returns None.
        """
        if Name("ToUnicode") in self:
            self._read_to_unicode()
            return self._unicode_lookup_to_character_identifier.get(unicode)

        if Name("Encoding") in self:
            assert str(self["Encoding"]) in [
                "Identity",
                "Identity-H",
            ], "Only Identity and Identity-H are currently supported."
            if len(self._character_identifier_to_unicode_lookup) == 0:
                self._character_identifier_to_unicode_lookup = (
                    Type0Font._find_best_matching_predefined_cmap(self._get_cmap_name())
                )
                self._unicode_lookup_to_character_identifier = {
                    v: k
                    for k, v in self._character_identifier_to_unicode_lookup.items()
                }

            # e) Map the CID obtained in step (a) according to the CMap obtained in step (d), producing a
            # Unicode value.
            return self._unicode_lookup_to_character_identifier.get(unicode, None)

        # default
        return None

    def get_width(self, character_identifier: int) -> typing.Optional[bDecimal]:
        """
        This function returns the width (in text space) of a given character identifier.
        If this Font is unable to represent the glyph that corresponds to the character identifier,
        this function returns None
        """
        assert "DescendantFonts" in self
        assert isinstance(self["DescendantFonts"], List)
        assert len(self["DescendantFonts"]) == 1
        descendant_font: Font = self["DescendantFonts"][0]
        return descendant_font.get_width(character_identifier)

    def get_ascent(self) -> bDecimal:
        """
        This function returns the maximum height above the baseline reached by glyphs in this font.
        The height of glyphs for accented characters shall be excluded.
        """
        assert "DescendantFonts" in self
        assert isinstance(self["DescendantFonts"], List)
        assert len(self["DescendantFonts"]) == 1
        descendant_font: Font = self["DescendantFonts"][0]
        return descendant_font.get_ascent()

    def get_descent(self) -> bDecimal:
        """
        This function returns the maximum depth below the baseline reached by glyphs in this font.
        The value shall be a negative number.
        """
        assert "DescendantFonts" in self
        assert isinstance(self["DescendantFonts"], List)
        assert len(self["DescendantFonts"]) == 1
        descendant_font: Font = self["DescendantFonts"][0]
        return descendant_font.get_descent()

    def _empty_copy(self) -> "Font":
        return Type0Font()

    def __deepcopy__(self, memodict={}):
        # fmt: off
        f_out: Type0Font = super(Type0Font, self).__deepcopy__(memodict)
        f_out[Name("Subtype")] = Name("Type0")
        f_out._character_identifier_to_unicode_lookup: typing.Dict[int, str] = {k: v for k, v in self._character_identifier_to_unicode_lookup.items()}
        f_out._unicode_lookup_to_character_identifier: typing.Dict[str, int] = {k: v for k, v in self._unicode_lookup_to_character_identifier.items()}
        return f_out
        # fmt: on
