from pathlib import Path

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


def main():

    # create an empty Document
    pdf = Document()

    # add an empty Page
    page = Page()
    pdf.append_page(page)

    # use a PageLayout (SingleColumnLayout in this case)
    layout = SingleColumnLayout(page)

    # add a Paragraph object
    layout.add(Paragraph("Hello World!"))

    # store the PDF
    with open(Path("output.pdf"), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)


if __name__ == "__main__":
    main()
