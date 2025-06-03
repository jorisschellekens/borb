import unittest


class TestScreenshot(unittest.TestCase):

    def test_screenshot(self):
        # snippet_06_10.ipynb
        from borb.pdf import (
            Document,
            FlexibleColumnWidthTable,
            Image,
            Page,
            PageLayout,
            Paragraph,
            PDF,
            SingleColumnLayout,
            Standard14Fonts,
        )

        # Create an empty Document
        d: Document = Document()

        # Create an empty Page
        p: Page = Page()
        d.append_page(p)

        # Create a PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # Add a FlexibleColumnWidthTable
        l.append_layout_element(
            FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3)
            .append_layout_element(
                Paragraph("Painting", font=Standard14Fonts.get("Helvetica-Bold"))
            )
            .append_layout_element(
                Paragraph("Title", font=Standard14Fonts.get("Helvetica-Bold"))
            )
            .append_layout_element(
                Paragraph("Artist", font=Standard14Fonts.get("Helvetica-Bold"))
            )
            .append_layout_element(
                Image(
                    "https://uploads5.wikiart.org/00362/images/gerolamo-induno/6605-la-partenza-per-il-campo-1866.jpg!Large.jpg",
                    size=(200, 100),
                )
            )
            .append_layout_element(Paragraph("Guernica"))
            .append_layout_element(Paragraph("Pablo Picasso"))
            .append_layout_element(
                Image(
                    "https://uploads5.wikiart.org/00362/images/gerolamo-induno/6605-la-partenza-per-il-campo-1866.jpg!Large.jpg",
                    size=(200, 200),
                )
            )
            .append_layout_element(
                Paragraph("Composition in red, yellow, blue and black")
            )
            .append_layout_element(Paragraph("Piet Mondrian"))
        )

        # Write the PDF
        PDF.write(
            what=d, where_to="/home/joris-schellekens/Downloads/snippet_06_10.pdf"
        )
