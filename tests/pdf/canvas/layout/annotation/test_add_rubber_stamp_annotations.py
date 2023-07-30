from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.rubber_stamp_annotation import (
    RubberStampAnnotation,
)
from borb.pdf.canvas.layout.annotation.rubber_stamp_annotation import (
    RubberStampAnnotationIconType,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddRubberStampAnnotations(TestCase):
    def _build_pdf_using_rubberstamp_annotation(
        self, icon_type: RubberStampAnnotationIconType
    ):

        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description=f"This test adds a RubberStampAnnotation using RubberStampAnnotationIconType {icon_type.name} to a PDF"
            )
        )
        pdf.get_page(0).add_annotation(
            RubberStampAnnotation(
                name=icon_type,
                contents="Approved by Joris Schellekens",
                color=HexColor("56cbf9"),
                bounding_box=Rectangle(
                    page.get_page_info().get_width() / Decimal(2) - Decimal(32),
                    page.get_page_info().get_width() / Decimal(2) - Decimal(32),
                    Decimal(32),
                    Decimal(32),
                ),
            )
        )
        return pdf

    def test_add_rubberstampannotation_using_name_approved(self):
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.APPROVED
                ),
            )
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_rubberstampannotation_using_name_as_is(self):
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.AS_IS
                ),
            )
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_rubberstampannotation_using_name_confidential(self):
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.CONFIDENTIAL
                ),
            )
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_rubberstampannotation_using_name_departmental(self):
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.DEPARTMENTAL
                ),
            )
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_rubberstampannotation_using_name_draft(self):
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.DRAFT
                ),
            )
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_rubberstampannotation_using_name_experimental(self):
        with open(self.get_sixth_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.EXPERIMENTAL
                ),
            )
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_rubberstampannotation_using_name_expired(self):
        with open(self.get_seventh_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.EXPIRED
                ),
            )
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_rubberstampannotation_using_name_final(self):
        with open(self.get_eight_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.FINAL
                ),
            )
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_add_rubberstampannotation_using_name_for_comment(self):
        with open(self.get_nineth_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.FOR_COMMENT
                ),
            )
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())

    def test_add_rubberstampannotation_using_name_for_public_release(self):
        with open(self.get_tenth_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.FOR_PUBLIC_RELEASE
                ),
            )
        self.compare_visually_to_ground_truth(self.get_tenth_output_file())
        self.check_pdf_using_validator(self.get_tenth_output_file())

    def test_add_rubberstampannotation_using_name_not_approved(self):
        with open(self.get_eleventh_output_file(), "wb") as fh:
            PDF.dumps(
                fh,
                self._build_pdf_using_rubberstamp_annotation(
                    icon_type=RubberStampAnnotationIconType.NOT_APPROVED
                ),
            )
        self.compare_visually_to_ground_truth(self.get_eleventh_output_file())
        self.check_pdf_using_validator(self.get_eleventh_output_file())
