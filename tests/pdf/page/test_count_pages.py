import random
import typing

from borb.pdf import Document
from borb.pdf import Lipsum
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestCountPages(TestCase):
    def test_create_dummy_pdf_document(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a simple dummy PDF."
            )
        )
        random.seed(2048)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 20)
        ]:
            layout.add(Paragraph(s))
        pdf.pop_page(0)
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_get_page_number(self):
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as file_handle:
            doc = PDF.loads(file_handle)
        assert doc is not None
        N: int = int(doc.get_document_info().get_number_of_pages())
        for i in range(0, N):
            page_object = doc.get_page(i)
            page_nr = page_object.get_page_info().get_page_number()
            assert page_nr == i

    def test_get_number_of_pages(self):
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as file_handle:
            doc = PDF.loads(file_handle)
        assert doc is not None
        assert doc.get_document_info().get_number_of_pages() == 4
