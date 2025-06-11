import unittest

from borb.pdf import Document, PageLayout, SingleColumnLayout, Paragraph, Page, PDF


class TestWriteChineseUsingHelvetica(unittest.TestCase):

    def test_write_chinese_using_helvetica(self):

        # new Document
        d: Document = Document()

        # new Page
        p: Page = Page()
        d.append_page(p)

        # PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # attempt to insert character 龙
        with self.assertRaises(UnicodeEncodeError) as context:
            l.append_layout_element(Paragraph("龙"))

        # we should have gotten an error
        assert context.exception is not None
        assert isinstance(context.exception, UnicodeEncodeError)

        # write
        PDF.write(what=d, where_to="assets/test_write_chinese_using_helvetica.pdf")
