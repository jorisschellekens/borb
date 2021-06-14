# :mega: pText release 1.9.0

This release features quite a few new functionalities:
- OCR
- Pantone colors
- Markdown to PDF conversion

It also features some minor improvements to general layout logic:
- `Tables` are now automatically completed (with empty `Paragraph` objects)
- support for heterogeneous paragraphs (see `ChunksOfText` object)
- layout package refactor to separate classes

## OCR

Using `Tesseract` (or rather `pytesseract`), `pText` is now able to handle scanned images in a PDF.
Typically, a scanned document will present itself as a PDF, without containing any content other than the image of the page.
`pText` can now restore text to such PDF documents.

The OCR capabilities have been integrated nicely with the existing `EventListener` framework. New events have been added to represent scanned text being recognized.
Two extra implementations of `EventListener` deal with OCR:

- `OCRImageRenderEventListener` : is triggered whenever an image is detected in the PDF, scans the image, and produces `OCREvent` objects
- `OCRAsOptionalContentGroup` : extends `OCRImageRenderEventListener` and adds optional (invisible) content to the PDF, representing the recognized text    

`pytesseract` is not added as a dependency in the setup script.
If you do choose to use OCR, you should install `pytesseract` and download the `Tesseract` data directories.

## Pantone colors

Pantone colors are now supported, similar to `X11Color`, `Pantone` has a dictionary of names, mapped to hexadecimal strings.
When constructing a `Pantone` object, simply pass a valid color-name, and you'll receive its corresponding `HexColor` object.

## Markdown to PDF

`pText` can now convert (simple) Markdown to PDF.
It does not (yet) support HTML, since that would require an entire HTML engine.

`pText` supports:
- Headers
- Tables
- Ordered lists (not nested)
- Unordered lists (not nested)
- Code snippet (by indent, and fenced)
- Blockquote
- Images
- Paragraphs
- Horizontal rules

Check the examples and tests to get a better idea of what is supported, and find a demo-document and its matching output.