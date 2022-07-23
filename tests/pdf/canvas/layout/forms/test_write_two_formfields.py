import unittest
from pathlib import Path

import typing

from borb.io.read.types import Name
from borb.pdf import Document, Page, SingleColumnLayout, PageLayout, PDF
from borb.pdf.canvas.layout.forms.check_box import CheckBox
from borb.pdf.canvas.layout.forms.drop_down_list import DropDownList
from borb.pdf.canvas.layout.forms.text_area import TextArea
from borb.pdf.canvas.layout.forms.text_field import TextField
from tests.test_util import check_pdf_using_validator


class TestWriteTwoFormFields(unittest.TestCase):
    """
    This test attempts to insert two FormField objects in a PDF
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_write_two_textfields(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.add_page(p)

        # create PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # add
        for _ in range(0, 2):
            l.add(TextField())

        # store
        out_file: Path = self.output_dir / "output_001.pdf"
        with open(out_file, "wb") as fh:
            PDF.dumps(fh, d)

        # check PDF syntax
        check_pdf_using_validator(out_file)

        # load
        with open(out_file, "rb") as fh:
            d = PDF.loads(fh)

        # get AcroForm/Fields
        fields: typing.List[typing.Dict[Name, typing.Any]] = d["XRef"]["Trailer"][
            "Root"
        ]["AcroForm"]["Fields"]

        # get object number of each /AP
        aps: typing.List[int] = [
            x.get_reference().object_number for x in fields if "AP" in x
        ]

        # check whether each /AP is unique
        assert len(aps) == len(set(aps))

    def test_write_two_textareas(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.add_page(p)

        # create PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # add
        for _ in range(0, 2):
            l.add(TextArea())

        # store
        out_file: Path = self.output_dir / "output_002.pdf"
        with open(out_file, "wb") as fh:
            PDF.dumps(fh, d)

        # check PDF syntax
        check_pdf_using_validator(out_file)

        # load
        with open(out_file, "rb") as fh:
            d = PDF.loads(fh)

        # get AcroForm/Fields
        fields: typing.List[typing.Dict[Name, typing.Any]] = d["XRef"]["Trailer"][
            "Root"
        ]["AcroForm"]["Fields"]

        # get object number of each /AP
        aps: typing.List[int] = [
            x.get_reference().object_number for x in fields if "AP" in x
        ]

        # check whether each /AP is unique
        assert len(aps) == len(set(aps))

    def test_write_two_checkboxes(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.add_page(p)

        # create PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # add
        for _ in range(0, 2):
            l.add(CheckBox())

        # store
        out_file: Path = self.output_dir / "output_003.pdf"
        with open(out_file, "wb") as fh:
            PDF.dumps(fh, d)

        # check PDF syntax
        check_pdf_using_validator(out_file)

        # load
        with open(out_file, "rb") as fh:
            d = PDF.loads(fh)

        # get AcroForm/Fields
        fields: typing.List[typing.Dict[Name, typing.Any]] = d["XRef"]["Trailer"][
            "Root"
        ]["AcroForm"]["Fields"]

        # get object number of each /AP
        aps: typing.List[int] = [
            x.get_reference().object_number for x in fields if "AP" in x
        ]

        # check whether each /AP is unique
        assert len(aps) == len(set(aps))

    def test_write_two_dropdownlists(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.add_page(p)

        # create PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # add
        for _ in range(0, 2):
            l.add(DropDownList())

        # store
        out_file: Path = self.output_dir / "output_004.pdf"
        with open(out_file, "wb") as fh:
            PDF.dumps(fh, d)

        # check PDF syntax
        check_pdf_using_validator(out_file)

        # load
        with open(out_file, "rb") as fh:
            d = PDF.loads(fh)

        # get AcroForm/Fields
        fields: typing.List[typing.Dict[Name, typing.Any]] = d["XRef"]["Trailer"][
            "Root"
        ]["AcroForm"]["Fields"]

        # get object number of each /AP
        aps: typing.List[int] = [
            x.get_reference().object_number for x in fields if "AP" in x
        ]

        # check whether each /AP is unique
        assert len(aps) == len(set(aps))
