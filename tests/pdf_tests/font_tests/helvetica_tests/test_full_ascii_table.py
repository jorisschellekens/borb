import math
import typing
import unittest

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    PageLayout,
    FixedColumnWidthTable,
    Paragraph,
    Table,
    PDF,
)


class TestFullASCIITable(unittest.TestCase):

    def __add_table_to_document(
        self, layout: PageLayout, characters: str, character_names: typing.List[str]
    ):

        # determine the number of rows
        nof_rows: int = math.ceil(len(characters) / 10) * 2

        # create Table
        t: Table = FixedColumnWidthTable(number_of_columns=10, number_of_rows=nof_rows)

        # add characters and names
        for i in range(0, len(characters), 10):
            k = len(characters[i : i + 10])
            for c in characters[i : i + 10]:
                t.append_layout_element(Paragraph(c))
            for _ in range(0, 10 - k):
                t.append_layout_element(Paragraph(""))
            for c in character_names[i : i + 10]:
                t.append_layout_element(Paragraph(c, font_size=6))
            for _ in range(0, 10 - k):
                t.append_layout_element(Paragraph("", font_size=6))

        # set properties
        t.set_padding_on_all_cells(
            padding_bottom=3, padding_left=3, padding_right=3, padding_top=3
        )

        # add to layout
        layout.append_layout_element(t)

    def test_full_ascii_table(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: PageLayout = SingleColumnLayout(page)

        # printable ascii characters
        layout.append_layout_element(
            Paragraph("ASCII", font="Helvetica-Bold", font_size=16)
        )
        layout.append_layout_element(
            Paragraph("Printable ASCII Characters (1)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="!\"#$%&'()*+,-./",
            character_names=[
                "exclamation mark",
                "quotation mark",
                "number sign",
                "dollar sign",
                "percent sign",
                "ampersand",
                "apostrophe",
                "round brackets",
                "round brackets",
                "asterisk",
                "plus sign",
                "comma",
                "hyphen",
                "dot",
                "slash",
            ],
        )

        # digits
        layout.append_layout_element(Paragraph("Digits", font="Helvetica-Bold"))
        self.__add_table_to_document(
            layout=layout,
            characters="0123456789",
            character_names=[
                "zero",
                "one",
                "two",
                "three",
                "four",
                "five",
                "six",
                "seven",
                "eight",
                "nine",
            ],
        )

        # printable ascii characters
        layout.append_layout_element(
            Paragraph("Printable ASCII Characters (2)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters=":;<=>?@",
            character_names=[
                "colon",
                "semicolon",
                "less-than sign",
                "equals sign",
                "greater-than sign",
                "question mark",
                "at sign",
            ],
        )

        # capital letters
        layout.append_layout_element(
            Paragraph("Capital Letters", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            character_names=[
                "capital letter a",
                "capital letter b",
                "capital letter c",
                "capital letter d",
                "capital letter e",
                "capital letter f",
                "capital letter g",
                "capital letter h",
                "capital letter i",
                "capital letter j",
                "capital letter k",
                "capital letter l",
                "capital letter m",
                "capital letter n",
                "capital letter o",
                "capital letter p",
                "capital letter q",
                "capital letter r",
                "capital letter s",
                "capital letter t",
                "capital letter u",
                "capital letter v",
                "capital letter w",
                "capital letter x",
                "capital letter y",
                "capital letter z",
            ],
        )

        # printable ascii characters
        layout.append_layout_element(
            Paragraph("Printable ASCII Characters (3)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="[\\]^_`",
            character_names=[
                "square brackets",
                "backslash",
                "square brackets",
                "caret",
                "underscore",
                "grave accent",
            ],
        )

        # capital letters
        layout.append_layout_element(
            Paragraph("Lowercase Letters", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="abcdefghijklmnopqrstuvwxyz",
            character_names=[
                "lowercase letter a",
                "lowercase letter b",
                "lowercase letter c",
                "lowercase letter d",
                "lowercase letter e",
                "lowercase letter f",
                "lowercase letter g",
                "lowercase letter h",
                "lowercase letter i",
                "lowercase letter j",
                "lowercase letter k",
                "lowercase letter l",
                "lowercase letter m",
                "lowercase letter n",
                "lowercase letter o",
                "lowercase letter p",
                "lowercase letter q",
                "lowercase letter r",
                "lowercase letter s",
                "lowercase letter t",
                "lowercase letter u",
                "lowercase letter v",
                "lowercase letter w",
                "lowercase letter x",
                "lowercase letter y",
                "lowercase letter z",
            ],
        )

        # printable ascii characters
        layout.append_layout_element(
            Paragraph("Printable ASCII Characters (4)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="{|}~",
            character_names=[
                "curly brackets",
                "vertical bar",
                "curly brackets",
                "tilde",
            ],
        )

        # extended ascii characters
        tmp = "128Ç129ü130é131â132ä133à134å135ç136ê137ë138è139ï140î141ì142Ä143Å144É145æ146Æ147ô148ö149ò150û151ù152ÿ153Ö154Ü155ø156£157Ø158×159ƒ160á161í162ó163ú164ñ165Ñ166ª167º168¿169®170¬171½172¼173¡174«175»176░177▒178▓179│180┤181Á182Â183À184©185╣186║187╗188╝189¢190¥191┐192└193┴194┬195├196─197┼198ã199Ã200╚201╔202╩203╦204╠205═206╬207¤208ð209Ð210Ê211Ë212È213ı214Í215Î216Ï217┘218┌219█220▄221¦222Ì223▀224Ó225ß226Ô227Ò228õ229Õ230µ231þ232Þ233Ú234Û235Ù236ý237Ý238¯239´240≡241±242‗243¾244¶245§246÷247¸248°249¨250·251¹252³253²254■"
        tmp = [c for i, c in enumerate(tmp) if i % 4 == 3]

        # extended ascii characters
        layout.append_layout_element(
            Paragraph("Extended ASCII Characters (1)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø",
            character_names=[
                "majuscule c-cedilla",
                "u with diaeresis",
                "e with acute accent",
                "a with circumflex accent",
                "a with diaeresis",
                "a with grave accent",
                "a with a ring",
                "minuscule c-cedilla",
                "e with circumflex accent",
                "e with diaeresis",
                "e with grave accent",
                "i with diaeresis",
                "i with circumflex accent",
                "i with grave accent",
                "A with diaeresis",
                "A with ring",
                "E with acute accent",
                "latin diphthong ae",
                "latin diphthong AE",
                "o with circumflex accent",
                "o with diaeresis",
                "o with grave accent",
                "u with circumflex accent",
                "u with grave accent",
                "y with diaeresis",
                "O with diaeresis",
                "U with diaeresis",
                "slashed zero",
                "pound sign",
                "slashed zero",
            ],
        )

        # ×ƒáíóúñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗
        layout.append_layout_element(
            Paragraph("Extended ASCII Characters (2)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="× áíóúñÑªº¿®¬½¼¡«»     ÁÂÀ©   ",
            character_names=[
                "multiplication sign",
                "function sign",
                "a with acute accent",
                "i with acute accent",
                "o with acute accent",
                "u with acute accent",
                "n with tilde",
                "N with tilde",
                "feminine ordinal indicator",
                "masculine ordinal indicator",
                "inverted question mark",
                "registered trademark",
                "logical negation mark",
                "one half",
                "one fourth",
                "inverted exclamation mark",
                "angle quotes",
                "angle quotes",
                "light shade",
                "medium shade",
                "dark shade",
                "box drawings light vertical",
                "box drawings light vertical and left",
                "A with acute accent",
                "A with circumflex accent",
                "A with grave accent",
                "copyright symbol",
                "box drawings double vertical and left",
                "box drawings double vertical",
                "box drawings double down and left",
            ],
        )

        layout.append_layout_element(
            Paragraph("Extended ASCII Characters (3)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters=" ¢¥       ãÃ       ¤ðÐÊËÈ ÍÎÏ ",
            character_names=[
                "box drawings double up and left",
                "cent symbol",
                "yen symbol",
                "box drawings light down and left",
                "box drawings light up and right",
                "box drawings light up and horizontal",
                "box drawings light down and horizontal",
                "box drawings light right and vertical",
                "box drawings light horizontal",
                "box drawings light horizontal and vertical",
                "a with tilde",
                "A with tilde",
                "box drawings double up and right",
                "box drawings double down and right",
                "box drawings double up and horizontal",
                "box drawings double down and horizontal",
                "box drawings double right and vertical",
                "box drawings double horizontal",
                "box drawings double horizontal and vertical",
                "generic currency sign",
                "latin lowercase letter eth",
                "latin uppercase letter eth",
                "E with circumflex accent",
                "E with umlaut",
                "E with grave accent",
                "lowercase dot less i",
                "I with acute accent",
                "I with circumflex accent",
                "I with umlaut",
                "box drawings light up and left",
            ],
        )

        #
        layout.append_layout_element(
            Paragraph("Extended ASCII Characters (4)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="   ¦Ì ÓßÔÒõÕµþÞÚÛÙýÝ¯´ ± ¾¶§÷",
            character_names=[
                "box drawings light down and right",
                "full block",
                "lower half block",
                "broken bar",
                "I with grave accent",
                "upper half block",
                "O with acute accent",
                "sharp S",
                "O with circumflex accent",
                "O with grave accent",
                "o with tilde",
                "O with tilde",
                "mu",
                "lowercase letter thorn",
                "uppercase letter thorn",
                "U with acute accent",
                "U with circumflex accent",
                "U with grave accent",
                "y with acute accent",
                "Y with acute accent",
                "macron symbol",
                "acute accent",
                "hyphen",
                "plus-minus sign",
                "underline",
                "three quarters",
                "paragraph sign",
                "section sign",
                "division sign",
            ],
        )

        layout.append_layout_element(
            Paragraph("Extended ASCII Characters (5)", font="Helvetica-Bold")
        )
        self.__add_table_to_document(
            layout=layout,
            characters="¸°¨·¹³² ",
            character_names=[
                "cedila",
                "degree sign",
                "diaeresis",
                "interpunct",
                "superscript 1",
                "superscript 3",
                "superscript 2",
                "black square",
            ],
        )

        # store
        PDF.write(what=doc, where_to="assets/test_full_ascii_table_001.pdf")
