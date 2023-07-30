import unittest

from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.stop_words import ENGLISH_STOP_WORDS
from borb.toolkit.text.text_rank_keyword_extraction import TextRankKeywordExtraction
from borb.toolkit.text.tf_idf_keyword_extraction import TFIDFKeywordExtraction
from tests.test_case import TestCase


unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractKeywords(TestCase):
    """
    This test attempts to extract the keywords (TF-IDF)
    from each PDF in the corpus
    """

    def test_create_dummy_pdf(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an empty Page, and a Paragraph of text. "
                "A subsequent test will attempt to extract the keywords from this text."
            )
        )

        layout.add(
            Paragraph(
                """
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
            when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 
            It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
            and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
            """
            )
        )

        layout.add(
            Paragraph(
                """
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. 
            The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, 
            as opposed to using 'Content here, content here', making it look like readable English. 
            Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, 
            and a search for 'lorem ipsum' will uncover many web sites still in their infancy. 
            Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
            """
            )
        )

        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_extract_keywords_using_tf_idf_from_document(self):

        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            l = TFIDFKeywordExtraction(ENGLISH_STOP_WORDS)
            doc = PDF.loads(pdf_file_handle, [l])

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an empty Page, "
                "and adds the keywords it found in the previously made PDF."
            )
        )

        # add list
        layout.add(Paragraph("Following keywords were found:"))
        ul: UnorderedList = UnorderedList()
        for k in l.get_keywords()[0][:5]:
            ul.add(Paragraph(k[0]))
        layout.add(ul)

        # attempt to store PDF
        with open(self.get_second_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_extract_keywords_using_textrank_from_document(self):

        l = TextRankKeywordExtraction()
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l])

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an empty Page, and adds the keywords it found"
                "in the previously made PDF."
            )
        )

        # add list
        layout.add(Paragraph("Following keywords were found:"))
        ul: UnorderedList = UnorderedList()
        for k in l.get_keywords()[0][:5]:
            ul.add(Paragraph(k[0]))
        layout.add(ul)

        # attempt to store PDF
        with open(self.get_third_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.check_pdf_using_validator(self.get_third_output_file())


if __name__ == "__main__":
    unittest.main()
