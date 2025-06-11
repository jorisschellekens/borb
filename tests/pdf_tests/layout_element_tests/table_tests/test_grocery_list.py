import typing
import unittest

from borb.pdf import (
    Document,
    Page,
    MultiColumnLayout,
    PageLayout,
    Table,
    FlexibleColumnWidthTable,
    Paragraph,
    PDF,
    Space,
    X11Color,
)


class TestGroceryList(unittest.TestCase):

    @staticmethod
    def __create_table_from_str_list(s: typing.List[str]) -> Table:
        nof_columns: int = 3 if any([x.startswith("\t") for x in s]) else 2
        nof_rows: int = len(s)
        t: Table = FlexibleColumnWidthTable(
            number_of_columns=nof_columns, number_of_rows=nof_rows
        )
        i: int = 0
        while i < len(s):
            # chicken
            # \t breasts
            # \t tenders
            # \t nuggets
            if (i + 1) < len(s) and s[i + 1].startswith("\t"):
                nof_rows_in_group: int = 0
                while nof_rows_in_group + 1 + i < len(s) and s[
                    nof_rows_in_group + 1 + i
                ].startswith("\t"):
                    nof_rows_in_group += 1
                nof_rows_in_group += 1
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(12, 12)),
                        background_color=X11Color.GRAY,
                        row_span=nof_rows_in_group,
                        column_span=1,
                    )
                )
                t.append_layout_element(
                    Table.TableCell(
                        Paragraph(s[i], font_size=8), column_span=2, row_span=1
                    )
                )
                i += 1
                while i < len(s) and s[i].startswith("\t"):
                    t.append_layout_element(Space(size=(12, 12)))
                    t.append_layout_element(Paragraph(s[i], font_size=8))
                    i += 1
            # sausage
            # steak
            # bacon
            else:
                t.append_layout_element(Space(size=(12, 12)))
                t.append_layout_element(
                    Table.TableCell(
                        Paragraph(s[i], font_size=8),
                        column_span=nof_columns - 1,
                        row_span=1,
                    )
                )
                i += 1

        # set some properties
        t.set_padding_on_all_cells(3, 3, 3, 3)

        # return
        return t

    def test_grocery_list(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: MultiColumnLayout = MultiColumnLayout(page=page, number_of_columns=4)

        layout.append_layout_element(
            Paragraph("produce", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "mushroom",
                    "spinach",
                    "spring mix",
                    "green onion",
                    "onion",
                    "garlic",
                    "cherry tomatoes",
                    "potato",
                    "poblano",
                    "cauliflower",
                    "asparagus",
                ]
            )
        )

        layout.append_layout_element(
            Paragraph("deli", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "hummus",
                    "sliced meat",
                    "special cheese",
                    "bread",
                    "\tbroad loaf",
                    "\tround loaf",
                    "\thoagies",
                    "\tburger buns",
                ]
            )
        )

        layout.append_layout_element(
            Paragraph("deli-adjacent", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "pb",
                    "jelly",
                    "pasta",
                    "\tegg noodle",
                    "\tditalini",
                    "\tfarfalle",
                    "\tpenne",
                    "\tsauce",
                    "\trice noodle",
                ]
            )
        )

        layout.append_layout_element(
            Paragraph("baking", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "yeast",
                    "agave",
                    "breadcrumb",
                    "flour",
                    "\tall purpose",
                    "\tbread",
                    "vinegar",
                    "oil",
                    "\tpeanut",
                    "\tolive",
                ]
            )
        )

        layout.append_layout_element(
            Paragraph("soup", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "hominy",
                    "garbonzo",
                    "soup",
                    "broth",
                    "\tchicken",
                    "\tbeef",
                    "\tveggie",
                    "tomato",
                    "\tpaste",
                    "\tsauce",
                    "\tcrushed",
                    "tortilla",
                ]
            )
        )

        layout.next_column()
        layout.append_layout_element(
            Paragraph("sauce", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "ranch dressing",
                    "salsa",
                    "enchilado",
                    "cocomilk",
                    "green curry paste",
                    "sambal chili saus",
                    "kinder's bbq",
                    "worcester",
                    "mustard",
                    "black olive",
                    "pickles",
                    "capers",
                ]
            )
        )

        layout.append_layout_element(
            Paragraph("meat", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "chicken (fresh)",
                    "ground beef",
                    "ground turkey",
                    "pork shoulder",
                    "meatball",
                    "sausage",
                    "steak",
                    "bacon",
                    "kielbasa",
                ]
            )
        )

        layout.next_column()
        layout.append_layout_element(
            Paragraph("fridge", font_size=16, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            TestGroceryList.__create_table_from_str_list(
                [
                    "milk",
                    "sour cream",
                    "eggs",
                    "butter",
                    "\tspread",
                    "\treal",
                    "yoghurt",
                    "cheese",
                    "\tcheddar blend",
                    '\tmozzarella',
                    '\tparmesan',
                    'juice',
                    '\torange',
                    '\tzero'
                ]
            )
        )

        PDF.write(what=doc, where_to="assets/test_grocery_list.pdf")
