import copy

from ptext.pdf.canvas.font.font_type_1 import FontType1


class TrueTypeFont(FontType1):
    """
    The TrueType font format was developed by Apple Computer, Inc., and has been adopted as a standard font
    format for the Microsoft Windows operating system. Specifications for the TrueType font file format are
    available in Apple’s TrueType Reference Manual and Microsoft’s TrueType 1.0 Font Files Technical
    Specification (see Bibliography).

    A TrueType font dictionary may contain the same entries as a Type 1 font dictionary (see Table 111), with these
    differences:
    • The value of Subtype shall be TrueType.
    • The value of Encoding is subject to limitations that are described in 9.6.6, "Character Encoding".
    • The value of BaseFont is derived differently.

    The PostScript name for the value of BaseFont may be determined in one of two ways:
    • If the TrueType font program's “name” table contains a PostScript name, it shall be used.
    • In the absence of such an entry in the “name” table, a PostScript name shall be derived from the name by
    which the font is known in the host operating system. On a Windows system, the name shall be based on
    the lfFaceName field in a LOGFONT structure; in the Mac OS, it shall be based on the name of the FOND
    resource. If the name contains any SPACEs, the SPACEs shall be removed.
    """

    def __deepcopy__(self, memodict={}):
        copy_out = TrueTypeFont()
        for k in ["Type", "Subtype", "BaseFont"]:
            copy_out[k] = self[k]
        for k in ["Name", "FirstChar", "LastChar"]:
            if k in self:
                copy_out[k] = self.get(k)
        for k in ["Widths", "FontDescriptor", "Encoding", "ToUnicode"]:
            if k in self:
                copy_out[k] = copy.deepcopy(self.get(k), memodict)
        # return
        return copy_out
