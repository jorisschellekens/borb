
# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/readme_img/logo/borb_64.png) borb


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Corpus Coverage : 99.0%](https://img.shields.io/badge/corpus%20coverage-99.0%25-green)]()
[![Text Extraction : 88.6%](https://img.shields.io/badge/text%20extraction-88.6%25-orange)]()
[![Public Method Documentation : 100%](https://img.shields.io/badge/public%20method%20documentation-100%25-green)]()


`borb` is a library for creating and manipulating PDF files in python.

## 0. About borb

`borb` is a pure python library to read, write and manipulate PDF documents. It represents a PDF document as a JSON-like datastructure of nested lists, dictionaries and primitives (numbers, string, booleans, etc)

This is currently a one-man project, so the focus will always be to support those use-cases that are more common in favor of those that are rare.

## 1. About the Examples

Most examples double as tests, you can find them in the 'tests' directory.  
They include; 

- Reading a PDF and extracting meta-information
- Changing meta-information  
- Extracting text from a PDF
- Extracting images from a PDF
- Changing images in a PDF
- Adding annotations (notes, links, etc) to a PDF
- Adding text to a PDF
- Adding tables to a PDF
- Adding lists to a PDF
- Using a PageLayout manager

 and much more
 
### 1.1 Hello World

To give you an immediate idea of the way `borb` works, this is the classic `Hello World` example, in `borb`:

```python
from pathlib import Path

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

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
```

## 2. License

`borb` is dual licensed as AGPL/Commercial software.

AGPL is a free / open source software license.
This doesn't mean the software is [gratis](https://en.wikipedia.org/wiki/Gratis_versus_libre)!

Buying a license is mandatory as soon as you develop commercial activities distributing the borb software inside your product or deploying it on a network without disclosing the source code of your own applications under the AGPL license. 
These activities include:

- Offering paid services to customers as an ASP
- Serving PDFs on the fly in the cloud or in a web application
- Shipping `borb` with a closed source product

Contact sales for more info.

## 3. Acknowledgements

I would like to thank the following people, for their contributions / advice with regards to developing `borb`:
- Aleksander Banasik
- Benoît Lagae
- Michael Klink
