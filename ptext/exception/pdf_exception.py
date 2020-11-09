from typing import Optional, Type, Any

from ptext.primitive.pdf_indirect_reference import PDFIndirectReference
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject, PDFIndirectObject


class PDFException(Exception):
    """
    All built-in, PDF-related, non-system-exiting exceptions are derived from this class.
    All user-defined, PDF-related, exceptions should also be derived from this class.
    """

    def __init__(
        self, byte_offset: Optional[int] = None, message: Optional[str] = None
    ):
        super().__init__(message or "")
        self.byte_offset = byte_offset

    def set_byte_offset(self, byte_offset: int) -> "PDFException":
        self.byte_offset = byte_offset
        return self

    def get_byte_offset(self) -> Optional[int]:
        return self.byte_offset


class PDFTypeError(PDFException, TypeError):
    """
    PDFTypeError is thrown when an operation or function is applied to an object of an inappropriate type.
    """

    def __init__(
        self,
        received_type: Type,
        expected_type: Type,
        byte_offset: Optional[int] = None,
    ):
        super(PDFTypeError, self).__init__(
            byte_offset=byte_offset,
            message="must be %s, not %s"
            % (expected_type.__name__, received_type.__name__),
        )


class PDFValueError(PDFException, ValueError):
    """
    PDFValueError is thrown when a function's argument is of an inappropriate type.
    """

    def __init__(
        self,
        received_value_description: str,
        expected_value_description: str,
        byte_offset: Optional[int] = None,
    ):
        super(PDFValueError, self).__init__(
            byte_offset=byte_offset,
            message="must be %s, not %s"
            % (expected_value_description, received_value_description),
        )


class PDFTokenNotFoundError(PDFException):
    def __init__(
        self, byte_offset: Optional[int] = None, message: Optional[str] = None
    ):
        super(PDFTokenNotFoundError, self).__init__(
            byte_offset=byte_offset, message=message
        )


class PDFCommentTokenNotFoundError(PDFTokenNotFoundError):
    """
    PDFCommentTokenNotFoundError is thrown when a PDF does not contain the magic comment '%PDF-X.X'
    """

    def __init__(self, byte_offset: Optional[int] = None):
        super(PDFCommentTokenNotFoundError, self).__init__(
            byte_offset=byte_offset,
            message="No token found that starts with %PDF-",
        )


class StartXREFTokenNotFoundError(PDFTokenNotFoundError):
    """
    StartXREFTokenNotFoundError is thrown when a PDF does not contain the token 'startxref'
    """

    def __init__(self, byte_offset: Optional[int] = None):
        super(StartXREFTokenNotFoundError, self).__init__(
            byte_offset=byte_offset,
            message="No startxref token found",
        )


class XREFTokenNotFoundError(PDFTokenNotFoundError):
    """
    XREFTokenNotFoundError is thrown when a PDF does not contain the token 'xref'
    """

    def __init__(self, byte_offset: Optional[int] = None):
        super(XREFTokenNotFoundError, self).__init__(
            byte_offset=byte_offset,
            message="No xref token found",
        )


class PDFEOFError(PDFException, EOFError):
    """
    PDFEOFError is thrown when the input (unexpectedly) hits the end-of-file condition.
    """

    def __init__(self, byte_offset: Optional[int] = None):
        super(PDFEOFError, self).__init__(
            byte_offset=byte_offset, message="Unexpectedly reached EOF"
        )


class IllegalGraphicsStateError(PDFException):
    def __init__(
        self, byte_offset: Optional[int] = None, message: Optional[str] = None
    ):
        super(IllegalGraphicsStateError, self).__init__(
            byte_offset=byte_offset, message=message
        )
