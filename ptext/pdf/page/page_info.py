from typing import Optional, Tuple

from ptext.io.read_transform.types import Dictionary
from ptext.pdf.page.page_size import PageSize


class PageInfo(Dictionary):
    def __init__(self, page: "Page"):  # type: ignore [name-defined]
        super(PageInfo, self).__init__()
        self.page = page

    def get_width(self) -> Optional[int]:
        """
        Return the width of the MediaBox. This is a rectangle (see 7.9.5, "Rectangles"),
        expressed in default user space units, that shall define the
        boundaries of the physical medium on which the page shall be
        displayed or printed (see 14.11.2, "Page Boundaries").
        """
        return self.page["MediaBox"][2]

    def get_height(self) -> Optional[int]:
        """
        Return the height of the MediaBox. This is a rectangle (see 7.9.5, "Rectangles"),
        expressed in default user space units, that shall define the
        boundaries of the physical medium on which the page shall be
        displayed or printed (see 14.11.2, "Page Boundaries").
        """
        return self.page["MediaBox"][3]

    def get_size(self) -> Tuple[int, int]:
        return self.get_width() or 0, self.get_height() or 0

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

    def get_page_number(self) -> Optional[int]:
        kids = self.page.get_parent()
        l = int(self.page.get_parent().get("Length"))
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
        return "ImageC" in self.page["Resources"]["ProcSet"]

    def uses_grayscale_images(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "ImageB" procedure set.
        """
        return "ImageB" in self.page["Resources"]["ProcSet"]

    def uses_indexed_images(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "ImageI" procedure set.
        """
        return "ImageI" in self.page["Resources"]["ProcSet"]

    def uses_painting_and_graphics_state(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "PDF" procedure set.
        """
        return "PDF" in self.page["Resources"]["ProcSet"]

    def uses_text(self) -> Optional[bool]:
        """
        The PDF operators used in content streams are grouped into categories of related operators called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing the implementations of
        the operators in that procedure set. The ProcSet entry in a content stream’s resource dictionary (see 7.8.3,
        “Resource Dictionaries”) shall hold an array consisting of the names of the procedure sets used in that content
        stream.
        This method returns whether this PDF uses operators from the "Text" procedure set.
        """
        return "Text" in self.page["Resources"]["ProcSet"]
