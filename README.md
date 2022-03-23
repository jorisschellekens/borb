
# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/logo/borb_64.png) borb


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Corpus Coverage : 99.0%](https://img.shields.io/badge/corpus%20coverage-99.0%25-green)]()
[![Text Extraction : 88.6%](https://img.shields.io/badge/text%20extraction-88.6%25-orange)]()
[![Public Method Documentation : 100%](https://img.shields.io/badge/public%20method%20documentation-100%25-green)]()

[![Downloads](https://pepy.tech/badge/borb)](https://pepy.tech/project/borb)
[![Downloads](https://pepy.tech/badge/borb/month)](https://pepy.tech/project/borb)

`borb` is a library for creating and manipulating PDF files in python.

## 0. About borb

`borb` is a pure python library to read, write and manipulate PDF documents. 
It represents a PDF document as a JSON-like datastructure of nested lists, dictionaries and primitives (numbers, string, booleans, etc)

This is currently a one-man project, so the focus will always be to support those use-cases that are more common in favor of those that are rare.

## 1. About the Examples

The examples can be found in a separate repository.
This ensures the `borb` repository stays relatively small, whilst still providing a thorough knowledgebase of code-samples, screenshots and explanatory text.

[Check out the examples repository here!](https://github.com/jorisschellekens/borb-examples)

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
 
### 1.0 Installing `borb`

`borb` can be installed using `pip`

    pip install borb

If you have installed `borb` before, and you want to ensure `pip` downloads the latest version (rather than using its internal cache) you can use the following commands:

    pip uninstall borb
    pip install --no-cache borb

### 1.1 Hello World

To give you an immediate idea of the way `borb` works, 
this is the classic `Hello World` example, in `borb`:

```python
from pathlib import Path

from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF

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

[Contact sales](https://borbpdf.com/) for more information.

## 3. Acknowledgements

I would like to thank the following people, for their contributions / advice with regards to developing `borb`:
- Aleksander Banasik
- Benoît Lagae
- Michael Klink
