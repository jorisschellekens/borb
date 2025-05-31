import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.rubber_stamp_annotation import (
    RubberStampAnnotation,
)
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestRubberStampAnnotation(unittest.TestCase):

    def test_rubber_stamp_annotation_approved(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.APPROVED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_approved.pdf")

    def test_rubber_stamp_annotation_as_is(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.AS_IS,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_as_is.pdf")

    def test_rubber_stamp_annotation_confidential(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.CONFIDENTIAL,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_confidential.pdf"
        )

    def test_rubber_stamp_annotation_departmental(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.DEPARTMENTAL,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_departmental.pdf"
        )

    def test_rubber_stamp_annotation_draft(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.DRAFT,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_draft.pdf")

    def test_rubber_stamp_annotation_experimental(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.EXPERIMENTAL,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_experimental.pdf"
        )

    def test_rubber_stamp_annotation_expired(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.EXPIRED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_expired.pdf")

    def test_rubber_stamp_annotation_final(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.FINAL,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_final.pdf")

    def test_rubber_stamp_annotation_for_comment(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.FOR_COMMENT,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_for_comment.pdf"
        )

    def test_rubber_stamp_annotation_for_public_release(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.FOR_PUBLIC_RELEASE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_rubber_stamp_annotation_for_public_release.pdf",
        )

    def test_rubber_stamp_annotation_not_approved(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.NOT_APPROVED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_not_approved.pdf"
        )

    def test_rubber_stamp_annotation_not_for_public_release(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.NOT_FOR_PUBLIC_RELEASE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_rubber_stamp_annotation_not_for_public_release.pdf",
        )

    def test_rubber_stamp_annotation_sold(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.SOLD,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_sold.pdf")

    def test_rubber_stamp_annotation_top_secret(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            size=(100, 100),
            rubber_stamp_annotation_type=RubberStampAnnotation.RubberStampAnnotationType.TOP_SECRET,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_top_secret.pdf")
