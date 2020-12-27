from ptext.exception.pdf_exception import PDFSyntaxError
from ptext.pdf.canvas.font.adobe_glyph_dictionary import ADOBE_GLYPH_DICTIONARY


class Encoding:
    def __init__(self):
        self._unicode_to_code = {}
        self._code_to_unicode = {}
        self._differences = {}
        # self._unicode_differences = {}
        self._base_encoding = None

    def unicode_to_code(self, unicode: int) -> int:
        return self._unicode_to_code[unicode]

    def code_to_unicode(self, code: int) -> int:
        if 0 <= code < 256:
            return self._code_to_unicode[code]

    def add_symbol(self, code: int, glyph_name: str):
        if 0 <= code < 256 and glyph_name in ADOBE_GLYPH_DICTIONARY:
            unicode = ADOBE_GLYPH_DICTIONARY.get(glyph_name)[0]
            self._unicode_to_code[unicode] = code
            self._code_to_unicode[code] = unicode
            self._differences[code] = glyph_name
        return self

    def can_encode_unicode(self, unicode: int) -> bool:
        if not chr(unicode).isprintable():
            return True
        return (
            unicode in self._unicode_to_code
            and self._unicode_to_code[unicode] != -1
            and self._unicode_to_code[unicode] != None
        )

    def can_encode_character_code(self, character_code: int) -> bool:
        return (
            character_code in self._code_to_unicode
            and self._code_to_unicode[character_code] != -1
            and self._code_to_unicode[character_code] != None
        )


class WingDings(Encoding):
    def __init__(self):
        super(WingDings, self).__init__()
        # fmt: off
        self.table = [
            0x00, 0x23, 0x22, 0x00, 0x00, 0x00, 0x29, 0x3E, 0x51, 0x2A, 0x00, 0x00, 0x41, 0x3F, 0x00, 0x00,
            0x00, 0x00, 0x00, 0xFC, 0x00, 0x00, 0x00, 0xFB, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x56, 0x00,
            0x58, 0x59, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB5, 0x00, 0x00, 0x00, 0x00, 0x00,
            0xB6, 0x00, 0x00, 0x00, 0xAD, 0xAF, 0xAC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C,
            0x7B, 0x00, 0x00, 0x00, 0x54, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA6, 0x00, 0x00,
            0x00, 0x71, 0x72, 0x00, 0x00, 0x00, 0x75, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7D, 0x7E, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95,
            0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x91,
            0x92, 0x93, 0x94, 0x95, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0xE8, 0xD8, 0x00, 0x00, 0xC4, 0xC6, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0xDC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ]
        # fmt: on

    def code_to_unicode(self, code: int) -> int:
        if chr(code) == " ":
            return code
        elif 9985 <= code <= 10174:
            new_code = code - 9984
            if new_code in self.table:
                return self.table[new_code]
        return 0


class WinAnsi(Encoding):
    """
    The regular encodings
    used for Latin-text fonts on Mac OS and Windows systems shall be named MacRomanEncoding and
    WinAnsiEncoding, respectively. An encoding named MacExpertEncoding may be used with “expert” fonts
    that contain additional characters useful for sophisticated typography. Complete details of these encodings and
    of the characters present in typical fonts are provided in Annex D.
    """

    def __init__(self):
        super().__init__()
        # fmt: off
        self.table = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
            48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
            64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
            80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
            96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
            112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
             8364,  65533,  8218,  402,  8222,  8230,  8224,  8225,  710,  8240,  352,  8249,  338,  65533,  381,  65533,
             65533,  8216,  8217,  8220,  8221,  8226,  8211,  8212,  732,  8482,  353,  8250,  339,  65533,  382,  376,
             160,  161,  162,  163,  164,  165,  166,  167,  168,  169,  170,  171,  172,  173,  174,  175,
             176,  177,  178,  179,  180,  181,  182,  183,  184,  185,  186,  187,  188,  189,  190,  191,
             192,  193,  194,  195,  196,  197,  198,  199,  200,  201,  202,  203,  204,  205,  206,  207,
             208,  209,  210,  211,  212,  213,  214,  215,  216,  217,  218,  219,  220,  221,  222,  223,
             224,  225,  226,  227,  228,  229,  230,  231,  232,  233,  234,  235,  236,  237,  238,  239,
             240,  241,  242,  243,  244,  245,  246,  247,  248,  249,  250,  251,  252,  253,  254,  255
        ]
        # fmt: on
        for i in range(0, len(self.table)):
            uc = self.table[i]
            self._unicode_to_code[uc] = i
            self._code_to_unicode[i] = uc


class StandardEncoding(Encoding):
    """
    Adobe standard Latin-text encoding. This is the built-in encoding defined
    in Type 1 Latin-text font programs (but generally not in TrueType font
    programs). Conforming readers shall not have a predefined encoding
    named StandardEncoding. However, it is necessary to describe this
    encoding, since a font’s built-in encoding can be used as the base
    encoding from which differences may be specified in an encoding
    dictionary.
    """

    def __init__(self):
        super().__init__()
        # fmt: off
        self.table = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
            48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
            64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
            80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
            8216, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
            112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 161, 162, 163, 8260, 165, 402, 167, 164, 39, 8220, 171, 8249, 8250, 64257, 64258,
            0, 8211, 8224, 8225, 183, 0, 182, 8226, 8218, 8222, 8221, 187, 8230, 8240, 0, 191,
            0, 96, 180, 710, 732, 175, 728, 729, 168, 0, 730, 184, 0, 733, 731, 711,
            8212, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 198, 0, 170, 0, 0, 0, 0, 321, 216, 338, 186, 0, 0, 0, 0,
            0, 230, 0, 0, 0, 305, 0, 0, 322, 248, 339, 223, 0, 0, 0, 0
        ]
        # fmt: on
        for i in range(0, len(self.table)):
            uc = self.table[i]
            self._unicode_to_code[uc] = i
            self._code_to_unicode[i] = uc


class PDFDoc(Encoding):
    """
    Encoding for text strings in a PDF document outside the document’s
    content streams. This is one of two encodings (the other being Unicode)
    that may be used to represent text strings; see 7.9.2.2, "Text String
    Type". PDF does not have a predefined encoding named
    PDFDocEncoding; it is not customary to use this encoding to show text
    from fonts.
    """

    def __init__(self):
        super().__init__()
        # fmt: off
        self.table = [
             0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10,  11,  12,  13,  14,  15,
             16,  17,  18,  19,  20,  21,  22,  23,  24, 25,  26,  27,  28,  29,  30,  31,
             32,  33,  34,  35,  36,  37,  38,  39,  40, 41,  42,  43,  44,  45,  46,  47,
             48,  49,  50,  51,  52,  53,  54,  55,  56, 57,  58,  59,  60,  61,  62,  63,
             64,  65,  66,  67,  68,  69,  70,  71,  72, 73,  74,  75,  76,  77,  78,  79,
             80,  81,  82,  83,  84,  85,  86,  87,  88, 89,  90,  91,  92,  93,  94,  95,
             96,  97,  98,  99,  100,  101,  102,  103,  104, 105,  106,  107,  108,  109,  110,  111,
             112,  113,  114,  115,  116,  117,  118,  119,  120, 121,  122,  123,  124,  125,  126,  127,
             0x2022,  0x2020,  0x2021,  0x2026,  0x2014,  0x2013,  0x0192, 0x2044,  0x2039,  0x203a,  0x2212,  0x2030,  0x201e,  0x201c, 0x201d,  0x2018,
             0x2019,  0x201a,  0x2122,  0xfb01,  0xfb02,  0x0141,  0x0152, 0x0160,  0x0178,  0x017d,  0x0131,  0x0142,  0x0153,  0x0161, 0x017e,  65533,
             0x20ac,  161,  162,  163,  164,  165,  166,  167, 168,  169,  170,  171,  172,  173,  174,  175,
             176,  177,  178,  179,  180,  181,  182,  183,  184, 185,  186,  187,  188,  189,  190,  191,
             192,  193,  194,  195,  196,  197,  198,  199,  200, 201,  202,  203,  204,  205,  206,  207,
             208,  209,  210,  211,  212,  213,  214,  215,  216, 217,  218,  219,  220,  221,  222,  223,
             224,  225,  226,  227,  228,  229,  230,  231,  232, 233,  234,  235,  236,  237,  238,  239,
             240,  241,  242,  243,  244,  245,  246,  247,  248, 249,  250,  251,  252,  253,  254,  255
        ]
        # fmt: on
        for i in range(0, len(self.table)):
            uc = self.table[i]
            self._unicode_to_code[uc] = i
            self._code_to_unicode[i] = uc


class MacRoman(Encoding):
    def __init__(self):
        super().__init__()
        # TODO : right now this is a copy, replace by actual MacRoman encoding
        # fmt: off
        self.table = [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
                64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
                96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
                0x2022, 0x2020, 0x2021, 0x2026, 0x2014, 0x2013, 0x0192, 0x2044, 0x2039, 0x203A, 0x2212, 0x2030, 0x201E, 0x201C, 0x201D, 0x2018,
                0x2019, 0x201A, 0x2122, 0xFB01, 0xFB02, 0x0141, 0x0152, 0x0160, 0x0178, 0x017D, 0x0131, 0x0142, 0x0153, 0x0161, 0x017E, 65533,
                0x20AC, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
                176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191,
                192, 193, 194, 195, 196, 197, 174, 199, 200, 201, 202, 203, 204, 205, 206, 207,
                208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223,
        ]
        # fmt: on
        for i in range(0, len(self.table)):
            uc = self.table[i]
            self._unicode_to_code[uc] = i
            self._code_to_unicode[i] = uc


#
# convenience method
#


def get_encoding(encoding_name: str) -> Encoding:
    encoding_upper = encoding_name.upper()
    if encoding_upper in ["WINANSI", "WINANSIENCODING"]:
        return WinAnsi()
    elif encoding_upper in ["PDF", "PDFDOCENCODING"]:
        return PDFDoc()
    elif encoding_upper in ["MACROMAN", "MACROMANENCODING"]:
        return MacRoman()
    elif encoding_upper in ["WINGDINGS"]:
        return WingDings()
    else:
        raise PDFSyntaxError("unknown byte-to-char encoding %s" % encoding_name)
