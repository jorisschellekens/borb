#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a font object in a PDF document.

The `Font` class serves as a superclass for various font-related classes,
encapsulating properties and behaviors common to all fonts used in PDF documents.
This class provides a foundation for defining font attributes such as name, size,
style, and encoding, which are essential for rendering text correctly in a PDF.
"""
import typing

from borb.pdf.primitives import name, PDFType


class Font(dict):
    """
    Represents a font object in a PDF document.

    The `Font` class serves as a superclass for various font-related classes,
    encapsulating properties and behaviors common to all fonts used in PDF documents.
    This class provides a foundation for defining font attributes such as name, size,
    style, and encoding, which are essential for rendering text correctly in a PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a new `Font` object for representing a font in a PDF document.

        This constructor initializes the font properties by creating an empty dictionary
        that can hold various attributes related to the font. The `Font` class serves as a
        base for defining more specific font types and settings, allowing for easy extension
        and customization of font-related functionalities.

        This class does not take any parameters and relies on the dictionary structure
        to store font attributes such as name, size, style, and encoding, which are essential
        for rendering text correctly in a PDF.

        Usage of this constructor allows for the creation of font objects that can be
        populated with specific font attributes later.
        """
        super().__init__()
        self[name("Type")] = name("Font")
        self.__character_code_to_character: typing.Dict[int, str] = {}  # type: ignore[annotation-unchecked]
        self.__character_to_character_code: typing.Dict[str, int] = {}  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    def __build_character_encoding_dictionaries(self) -> None:

        if len(self.__character_to_character_code) > 0:
            return

        # 9.10.2
        # Mapping Character Codes to Unicode Values
        # A conforming reader can use these methods, in the priority given, to map a character code to a Unicode value.
        # Tagged PDF documents, in particular, shall provide at least one of these methods (see 14.8.2.4.2, "Unicode
        # Mapping in Tagged PDF"):
        # •If the font dictionary contains a ToUnicode CMap (see 9.10.3, "ToUnicode CMaps"), use that CMap to
        # convert the character code to Unicode.
        if self.get("ToUnicode", None) is not None:
            cmap = self.get("ToUnicode")
            from borb.pdf.font.cmap import CMap

            assert isinstance(cmap, CMap)
            for k in range(cmap.first_character_code(), cmap.last_character_code() + 1):
                try:
                    v: str = cmap.get_character(character_code=k)  # type: ignore[no-redef]
                    if v in self.__character_to_character_code:
                        continue
                    self.__character_code_to_character[k] = v
                    self.__character_to_character_code[v] = k
                except:
                    pass
            return

        # •If the font is a simple font that uses one of the predefined encodings MacRomanEncoding,
        # MacExpertEncoding, or WinAnsiEncoding, or that has an encoding whose Differences array includes
        # only character names taken from the Adobe standard Latin character set and the set of named characters
        # in the Symbol font (see Annex D):
        from borb.pdf.font.simple_font.simple_font import SimpleFont

        if isinstance(self, SimpleFont) and self.get_encoding_or_base_encoding() in [
            "MacRomanEncoding",
            "MacExpertEncoding",
            "StandardEncoding",
            "Symbol",
            "WinAnsiEncoding",
            "ZapfDingbats",
        ]:

            # fmt: off
            from borb.pdf.font.common_font_encondings import CommonFontEncodings
            encoding_name: str = self.get_encoding_or_base_encoding()
            encoding_character_code_to_name: typing.Dict[int, str] = {}
            if encoding_name == "MacRomanEncoding":
                encoding_character_code_to_name = CommonFontEncodings.MACROMAN_CHARACTER_CODE_TO_CHARACTER_NAME
            elif encoding_name == "MacExpertEncoding":
                encoding_character_code_to_name = CommonFontEncodings.MACEXPERT_CHARACTER_CODE_TO_CHARACTER_NAME
            elif encoding_name == "StandardEncoding":
                encoding_character_code_to_name = CommonFontEncodings.STANDARD_ENCODING_CHARACTER_CODE_TO_CHARACTER_NAME
            elif encoding_name == "Symbol":
                encoding_character_code_to_name = CommonFontEncodings.SYMBOL_CHARACTER_CODE_TO_CHARACTER_NAME
            elif encoding_name == "WinAnsiEncoding":
                encoding_character_code_to_name = CommonFontEncodings.WINANSI_CHARACTER_CODE_TO_CHARACTER_NAME
            elif encoding_name == "ZapfDingbats":
                encoding_character_code_to_name = CommonFontEncodings.ZAPFDINGBATS_CHARACTER_CODE_TO_CHARACTER_NAME
            # fmt: on

            # fmt: off
            differences_character_code_to_name: typing.Dict[int, str] = {}
            differences: typing.List[PDFType] = []
            if isinstance(self.get('Encoding', None), dict) and isinstance(self.get('Encoding', {}).get('Differences', None), typing.List):
                differences = self.get("Encoding", {}).get("Differences", [])
            i: int = 0
            while i < len(differences):
                assert isinstance(differences[i], int)
                j: int = i + 1
                while j < len(differences) and isinstance(differences[j], name):
                    k: int = differences[i] + (j - i - 1)                   # type: ignore[no-redef, operator]
                    differences_character_code_to_name[k] = differences[j]  # type: ignore[assignment]
                    j += 1
                i = j
            # fmt: on

            from borb.pdf.font.adobe_glyph_list import AdobeGlyphList

            first_char: int = self.get("FirstChar", 0)
            last_char: int = self.get("LastChar", 255)
            for k in range(first_char, last_char + 1):
                # a) Map the character code to a character name according to Table D.1 and the font’s Differences
                # array.
                # fmt: off
                v_name: str = differences_character_code_to_name.get(k, None) or encoding_character_code_to_name.get(k, ".notdef")  # type: ignore[arg-type]
                # fmt: on

                # b) Look up the character name in the Adobe Glyph List (see the Bibliography) to obtain the
                # corresponding Unicode value.
                # fmt: off
                v: str = AdobeGlyphList.ADOBE_CHARACTER_NAME_TO_CHARACTER.get(v_name, "�")  # type: ignore[no-redef]
                self._Font__character_code_to_character[k] = v  # type: ignore[attr-defined]
                self._Font__character_to_character_code[v] = k  # type: ignore[attr-defined]
                # fmt: on

            return

        # If the font is a composite font that uses one of the predefined CMaps listed in Table 118 (except Identity–H
        # and Identity–V) or whose descendant CIDFont uses the Adobe-GB1, Adobe-CNS1, Adobe-Japan1, or
        # Adobe-Korea1 character collection:
        # a) Map the character code to a character identifier (CID) according to the font’s CMap.
        # b) Obtain the registry and ordering of the character collection used by the font’s CMap (for example,
        # Adobe and Japan1) from its CIDSystemInfo dictionary.
        # c) Construct a second CMap name by concatenating the registry and ordering obtained in step (b) in
        # the format registry–ordering–UCS2 (for example, Adobe–Japan1–UCS2).
        # d) Obtain the CMap with the name constructed in step (c) (available from the ASN Web site; see the
        # Bibliography).
        # e) Map the CID obtained in step (a) according to the CMap obtained in step (d), producing a
        # Unicode value.
        # NOTE
        # Type 0 fonts whose descendant CIDFonts use the Adobe-GB1, Adobe-CNS1, Adobe-Japan1, or Adobe-
        # Korea1 character collection (as specified in the CIDSystemInfo dictionary) shall have a supplement number
        # corresponding to the version of PDF supported by the conforming reader. See Table 3 for a list of the character
        # collections corresponding to a given PDF version. (Other supplements of these character collections can be
        # used, but if the supplement is higher-numbered than the one corresponding to the supported PDF version,
        # only the CIDs in the latter supplement are considered to be standard CIDs.)
        # If these methods fail to produce a Unicode value, there is no way to determine what the character code
        # represents in which case a conforming reader may choose a character code of their choosing.
        # TODO

    #
    # PUBLIC
    #

    def get_character(self, character_code: int) -> str:
        """
        Retrieve the character corresponding to a given character code in a Simple Font.

        This method resolves the character associated with a character code using the following
        prioritized sources of encoding information:
        1. `/ToUnicode` CMap: A mapping that explicitly defines the Unicode value for character codes.
        2. `/Encoding` (with `/Differences`): The font's base encoding, modified by the `/Differences`
           array, if specified. This step is used if no `/ToUnicode` mapping exists.

        By following this prioritized order, the method ensures accurate decoding of character codes
        based on the font's defined encoding mechanisms.

        :param character_code: The character code to resolve (an integer value).
        :return: The Unicode character corresponding to the given character code.
        :raises KeyError: If the character code cannot be resolved using the available encoding information.
        """
        self.__build_character_encoding_dictionaries()
        return self.__character_code_to_character.get(character_code, "�")

    def get_character_code(self, character: str) -> int:
        """
        Retrieve the character code corresponding to a given Unicode character in a Simple Font.

        This method resolves the character code associated with a Unicode character using the following
        prioritized sources of encoding information:
        1. `/ToUnicode` CMap: If a reverse mapping is defined in the `/ToUnicode` CMap, it is used to
           identify the character code.
        2. `/Encoding` (with `/Differences`): If no `/ToUnicode` mapping exists, the method checks the
           base encoding and the `/Differences` array for the character code.

        This method allows for encoding text into the font's character encoding scheme, ensuring compatibility
        with the font's defined mappings.

        :param character: The Unicode character to resolve (a single-character string).
        :return: The character code corresponding to the given Unicode character.
        :raises KeyError: If the Unicode character cannot be resolved using the available encoding information.
        """
        self.__build_character_encoding_dictionaries()
        return self.__character_to_character_code.get(character, -1)

    def get_unicode(self, character_id: int) -> str:
        """
        Retrieve the Unicode representation of a character based on its character ID.

        This method should be implemented in subclasses to provide the mapping from a
        character ID (specific to the font encoding) to its corresponding Unicode character.
        By default, this method raises an `AssertionError`, indicating it is not implemented.

        :param character_id:    The character ID to map to a Unicode character.
        :return:                The Unicode character as a string.
        """
        # Courier, Helvetica, Times
        if self.get("Encoding", None) == "WinAnsiEncoding":
            return bytes([character_id]).decode("cp1252")

        # Symbol
        if self.get("Encoding", None) == "Symbol":
            if character_id in self.__cid_to_unicode:  # type: ignore[attr-defined]
                return self.__cid_to_unicode[character_id]  # type: ignore[attr-defined]

        # ZapfDingbats
        if self.get("Encoding", None) == "ZapfDingbats":
            if character_id in self.__cid_to_unicode:  # type: ignore[attr-defined]
                return self.__cid_to_unicode[character_id]  # type: ignore[attr-defined]

        # Differences
        encoding: name = self.get("Encoding", {}).get(
            "BaseEncoding", name("StandardEncoding")
        )
        differences = self.get("Encoding", {}).get("Differences", [])

        # default
        assert False

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
        return 0
