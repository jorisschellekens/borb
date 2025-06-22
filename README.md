
# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/logo/borb_square_64_64.png) borb

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Public Method Documentation: 100%](https://img.shields.io/badge/public%20method%20documentation-100%25-green)]()
[![Tests: 1400+](https://img.shields.io/badge/tests-1400%2B-green)]()
[![Python Versions: 3.10, 3.11, 3.12](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-green)]()
[![Type Checking: 100%](https://img.shields.io/badge/type%20checking-100%25-green)]()
[![Downloads](https://pepy.tech/badge/borb)](https://pepy.tech/project/borb)
[![Monthly Downloads](https://pepy.tech/badge/borb/month)](https://pepy.tech/project/borb)

`borb` is a powerful and flexible Python library for creating and manipulating PDF files.

## 📖 Overview

`borb` provides a pure Python solution for PDF document management, allowing users to read, write, and manipulate PDFs. It models PDF files in a JSON-like structure, using nested lists, dictionaries, and primitives (numbers, strings, booleans, etc.). Created and maintained as a solo project, `borb` prioritizes common PDF use cases for practical and straightforward usage.

## ✨ Features

Explore `borb`’s capabilities in the [examples repository](https://github.com/jorisschellekens/borb-examples) for practical, real-world applications, including:

- PDF Metadata Management (reading, editing)
- Text and Image Extraction
- Adding Annotations (notes, links)
- Content Manipulation (adding text, images, tables, lists)
- Page Layout Management with `PageLayout`

…and much more!

## 🚀 Installation

Install `borb` directly via `pip`:

```bash
pip install borb
```

To ensure you have the latest version, consider the following commands:

```bash
pip uninstall borb
pip install --no-cache borb
```

## 👋 Getting Started: Hello World

Create your first PDF in just a few lines of code with `borb`:

```python
from pathlib import Path
from borb.pdf import Document, Page, PageLayout, SingleColumnLayout, Paragraph, PDF

# Create an empty Document
d: Document = Document()

# Create an empty Page
p: Page = Page()
d.append_page(p)

# Create a PageLayout
l: PageLayout = SingleColumnLayout(p)

# Add a Paragraph
l.append_layout_element(Paragraph('Hello World!'))

# Write the PDF
PDF.write(what=d, where_to="assets/output.pdf")

```

## 🛠 License

`borb` is dual-licensed under AGPL and a commercial license. 

The AGPL (Affero General Public License) is an open-source license, but commercial use cases require a paid license, especially if you intend to:

- Offer paid PDF services (e.g., PDF generation in cloud applications)
- Use `borb` in closed-source projects
- Distribute `borb` in any closed-source product

For more information, [contact our sales team](https://borbpdf.com/).

## 🙏 Acknowledgements

Special thanks to:

- Aleksander Banasik
- Benoît Lagae
- Michael Klink

Your contributions and guidance have been invaluable to `borb`'s development.