import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.form.drop_down_list import DropDownList
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestDropDownListDefaultValue(unittest.TestCase):

    def test_drop_down_list_default_value(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        DropDownList(
            options=["Lorem", "Ipsum", "Dolor", "Sit", "Amet"],
            padding_top=5,
            padding_bottom=5,
            padding_right=5,
            padding_left=5,
            default_value="Lorem",
        ).paint(available_space=(x, y, w, h), page=p)

        PDF.write(what=d, where_to="assets/test_drop_down_list_default_value.pdf")
