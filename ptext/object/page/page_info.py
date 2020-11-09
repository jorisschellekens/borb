from typing import Optional, Tuple

from ptext.object.page.page_size import PageSize
from ptext.object.pdf_high_level_object import PDFHighLevelObject
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_number import PDFFloat, PDFNumber


class PageInfo(PDFHighLevelObject):
    def __init__(self, page: "Page"):
        self.page = page

    def get_width(self) -> Optional[int]:
        """
        Return the width of the MediaBox. This is a rectangle (see 7.9.5, "Rectangles"),
        expressed in default user space units, that shall define the
        boundaries of the physical medium on which the page shall be
        displayed or printed (see 14.11.2, "Page Boundaries").
        """
        i = self.page.get(["MediaBox", 2])
        return (
            i.get_int_value() if i != PDFNull() and isinstance(i, PDFNumber) else None
        )

    def get_height(self) -> int:
        """
        Return the height of the MediaBox. This is a rectangle (see 7.9.5, "Rectangles"),
        expressed in default user space units, that shall define the
        boundaries of the physical medium on which the page shall be
        displayed or printed (see 14.11.2, "Page Boundaries").
        """
        i = self.page.get(["MediaBox", 3])
        return (
            i.get_int_value() if i != PDFNull() and isinstance(i, PDFNumber) else None
        )

    def get_size(self) -> Tuple[int, int]:
        return self.get_width(), self.get_height()

    def get_size_as_enum(self) -> Optional[PageSize]:
        """
        Return the size of the MediaBox as a convenient, well-known,
        well-defined property (e.g. A4_PORTRAIT).
        This is a rectangle (see 7.9.5, "Rectangles"),
        expressed in default user space units, that shall define the
        boundaries of the physical medium on which the page shall be
        displayed or printed (see 14.11.2, "Page Boundaries").
        """
        w, h = self.get_width(), self.get_height()
        if w is None or h is None:
            return None
        for m0_offset in [-1, 0, 1]:
            for m1_offset in [-1, 0, 1]:
                try:
                    return PageSize((int(w + m0_offset), int(h + m1_offset)))
                except ValueError:
                    pass
        return None

    def get_page_number(self) -> int:
        kids = self.page.get_parent()
        l = self.page.get_parent().get("Length").get_int_value()
        for i in range(0, l):
            if kids.get(i) == self:
                return i
        return None

    def uses_color_images(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "ImageC" procedure set.
        """
        return self.page.get(["Resources", "ProcSet"]).has_value(PDFName("ImageC"))

    def uses_grayscale_images(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "ImageB" procedure set.
        """
        return self.page.get(["Resources", "ProcSet"]).has_value(PDFName("ImageB"))

    def uses_indexed_images(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "ImageI" procedure set.
        """
        return self.page.get(["Resources", "ProcSet"]).has_value(PDFName("ImageI"))

    def uses_painting_and_graphics_state(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "PDF" procedure set.
        """
        return self.page.get(["Resources", "ProcSet"]).has_value(PDFName("PDF"))

    def uses_text(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "Text" procedure set.
        """
        return self.page.get(["Resources", "ProcSet"]).has_value(PDFName("Text"))
