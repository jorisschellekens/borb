import argparse
import datetime
import json
import typing
from argparse import RawTextHelpFormatter
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.page_layout.multi_column_layout import \
    SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.image.simple_image_extraction import SimpleImageExtraction
from borb.toolkit.ocr.ocr_as_optional_content_group import \
    OCRAsOptionalContentGroup
from borb.toolkit.text.regular_expression_text_extraction import \
    RegularExpressionTextExtraction
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


def _build_output_path(input_file: Path, extension: str = "pdf") -> Path:
    """
    This function returns an output Path, based on (the directory of) the input Path
    :param input_file:  the input Path
    :return:            the output Path
    """
    now = datetime.datetime.now()
    return input_file.parent / (
        "output_%d_%d_%d.%s" % (now.year, now.month, now.day, extension)
    )


def _ocr(input_file: Path, tesseract_data_dir: Path, output: typing.Optional[Path]):
    """
    This method performs OCR
    :param input_file:          The PDF to be OCR-ed
    :param tesseract_data_dir:  The tesseract data directory
    :param output:              The output PDF
    :return:                    None
    """
    if output is None:
        output = _build_output_path(input_file)
    with open(input_file, "rb") as pdf_file_handle:
        l = OCRAsOptionalContentGroup(tesseract_data_dir)
        doc = PDF.loads(pdf_file_handle, [l])
    with open(output, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)


def _extract_text(input_file: Path, output: typing.Optional[Path]):
    """
    This method performs text-extraction
    :param input_file:          The PDF to be read
    :param output:              The output TXT file
    :return:                    None
    """
    if output is None:
        output = _build_output_path(input_file, "txt")
    with open(input_file, "rb") as pdf_file_handle:
        l = SimpleTextExtraction()
        doc = PDF.loads(pdf_file_handle, [l])
    with open(output, "w") as txt_file_handle:
        number_of_pages: typing.Optional[
            Decimal
        ] = doc.get_document_info().get_number_of_pages()
        assert number_of_pages is not None
        for i in range(0, int(number_of_pages)):
            txt_file_handle.write(l.get_text(i))


def _extract_images(input_file: Path, output_dir: typing.Optional[Path]):
    """
    This method performs image-extraction
    :param input_file:          The PDF to be read
    :param output_dir:          The output directory
    :return:                    None
    """
    assert output_dir.exists() and output_dir.is_dir()
    with open(input_file, "rb") as pdf_file_handle:
        l = SimpleImageExtraction()
        doc = PDF.loads(pdf_file_handle, [l])
    for i, img in enumerate(l.get_images_per_page(0)):
        with open(output_dir / ("image_%d.jpg" % i), "wb") as image_file_handle:
            img.save(image_file_handle)


def _extract_files(input_file: Path, output_dir: typing.Optional[Path]):
    """
    This method performs file-extraction
    :param input_file:          The PDF to be read
    :param output_dir:          The output directory
    :return:                    None
    """
    assert output_dir.exists() and output_dir.is_dir()
    with open(input_file, "rb") as pdf_file_handle:
        l = SimpleImageExtraction()
        doc = PDF.loads(pdf_file_handle, [l])
    i: int = 0
    for _, content in doc.get_embedded_files().items():
        i += 1
        with open(output_dir / ("image_%d.jpg" % i), "wb") as file_handle:
            file_handle.write(content)


def _extract_regex(input_file: Path, pattern: str, output: typing.Optional[Path]):
    """
    This method performs file-extraction
    :param input_file:          The PDF to be read
    :param pattern:             The pattern to be used
    :param output:              The output directory
    :return:                    None
    """
    if output is None:
        output = _build_output_path(input_file, "json")
    with open(input_file, "rb") as pdf_file_handle:
        l = RegularExpressionTextExtraction(pattern)
        doc = PDF.loads(pdf_file_handle, [l])
    json_dict = []
    number_of_pages: typing.Optional[
        Decimal
    ] = doc.get_document_info().get_number_of_pages()
    assert number_of_pages is not None
    for i in range(0, int(number_of_pages)):
        for m in l.get_all_matches(i):
            json_dict.append(
                {
                    "string": m.string,
                    "start": m.start(),
                    "end": m.end(),
                    "bounding_boxes": [
                        {
                            float(x.get_x()),
                            float(x.get_y()),
                            float(x.get_width()),
                            float(x.get_height()),
                        }
                        for x in m.get_bounding_boxes()
                    ],
                }
            )
    with open(output, "w") as json_file_handle:
        json_file_handle.write(json.dumps(json_dict, indent=4))


def _redact_regex(input_file: Path, pattern: str, output: typing.Optional[Path]):
    """
    This method performs regex-based redaction
    :param input_file:          The PDF to be read and redacted
    :param pattern:             The pattern to be used
    :param output:              The output file
    :return:                    None
    """
    if output is None:
        output = _build_output_path(input_file, "pdf")
    with open(input_file, "rb") as pdf_file_handle:
        l = RegularExpressionTextExtraction(pattern)
        doc = PDF.loads(pdf_file_handle, [l])
    number_of_pages: typing.Optional[Decimal] = doc.get_document_info().get_number_of_pages()
    assert number_of_pages is not None
    for i in range(0, int(number_of_pages)):
        page: Page = doc.get_page(i)
        for m in l.get_all_matches(i):
            for b in m.get_bounding_boxes():
                page.append_redact_annotation(b.grow(Decimal(1)))
    with open(output, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

def _text_to_pdf(input_file: Path, output: typing.Optional[Path]):
    """
    This method generates a PDF with the given text
    :param input_file:          The plaintext file to be read
    :param output:              The output file
    :return:                    None
    """

    if output is None:
        output = _build_output_path(input_file, "pdf")

    text: str = ""
    with open(input_file, "r") as txt_file_handle:
        text = txt_file_handle.read()

    pdf_doc: Document = Document()

    page: Page = Page()
    pdf_doc.append_page(page)

    layout: PageLayout = SingleColumnLayout(page)

    for paragraph_text in text.split("\n\n"):
        layout.add(Paragraph(paragraph_text))

    with open(output, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf_doc)


def _images_to_pdf(input: Path, output: typing.Optional[Path]):
    pass


def main():

    # build main parser
    parser = argparse.ArgumentParser(
        description="borb", formatter_class=RawTextHelpFormatter
    )
    command_sub_parser = parser.add_subparsers(dest="command", help="Command Name")

    # extract files
    #fmt: off
    extract_files_arg_parser = command_sub_parser.add_parser('extract-files')
    extract_files_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    extract_files_arg_parser.add_argument('-o', help='output directory', default=None, required=False)
    #fmt: on

    # extract images
    #fmt: off
    extract_image_arg_parser = command_sub_parser.add_parser('extract-images')
    extract_image_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    extract_image_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    #fmt: on

    # extract regex
    #fmt: off
    extract_regex_arg_parser = command_sub_parser.add_parser('extract-regex')
    extract_regex_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    extract_regex_arg_parser.add_argument('-p', help='input regex', default=None, required=True)
    extract_regex_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    #fmt: on

    # extract text
    #fmt: off
    extract_text_arg_parser = command_sub_parser.add_parser('extract-text')
    extract_text_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    extract_text_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    #fmt: on

    # text to pdf
    #fmt: off
    image_to_pdf_arg_parser = command_sub_parser.add_parser('image-to-pdf')
    image_to_pdf_arg_parser.add_argument('-i', help='input file or directory', default=None, required=True)
    image_to_pdf_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    # fmt: on

    # OCR
    # fmt: off
    ocr_arg_parser = command_sub_parser.add_parser('ocr')
    ocr_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    ocr_arg_parser.add_argument('-t', help='tesseract data dir', default=None, required=True)
    ocr_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    #fmt: on

    # redact regex
    #fmt: off
    redact_regex_arg_parser = command_sub_parser.add_parser('redact-regex')
    redact_regex_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    redact_regex_arg_parser.add_argument('-p', help='input regex', default=None, required=True)
    redact_regex_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    #fmt: on

    # text to pdf
    #fmt: off
    text_to_pdf_arg_parser = command_sub_parser.add_parser('text-to-pdf')
    text_to_pdf_arg_parser.add_argument('-i', help='input file', default=None, required=True)
    text_to_pdf_arg_parser.add_argument('-o', help='output file', default=None, required=False)
    #fmt: on

    # parse
    args = parser.parse_args()

    # execute command
    if args.command == "extract-files":
        _extract_files(Path(args.i), Path(args.o) if args.o else None)
    elif args.command == "extract-images":
        _extract_images(Path(args.i), Path(args.o) if args.o else None)
    elif args.command == "extract-regex":
        _extract_regex(Path(args.i), args.p, Path(args.o) if args.o else None)
    elif args.command == "extract-text":
        _extract_text(Path(args.i), Path(args.o) if args.o else None)
    elif args.command == "ocr":
        _ocr(Path(args.i), Path(args.t), Path(args.o) if args.o else None)
    elif args.command == "redact-regex":
        _redact_regex(Path(args.i), args.p, Path(args.o) if args.o else None)
    elif args.command == "text-to-pdf":
        _text_to_pdf(Path(args.i), Path(args.o) if args.o else None)

if __name__ == "__main__":
    main()
