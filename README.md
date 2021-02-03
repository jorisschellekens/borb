
# pText

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Corpus Coverage : 98.2%](https://img.shields.io/badge/corpus%20coverage-98.2%25-green)]()
[![Text Extraction : 70.7%](https://img.shields.io/badge/text%20extraction-70.7%25-orange)]()

pText is a library for creating and manipulating PDF files in python.

## 0. About pText

pText is a pure python library to read, write and manipulate PDF documents. It represents a PDF document as a JSON-like datastructure of nested lists, dictionaries and primitives (numbers, string, booleans, etc)

This is currently a one-man project, so the focus will always be to support those use-cases that are more common in favor of those that are rare.

## 1. About the Examples

Most examples double as tests, you can find them in the 'tests' directory.  
They include; 
- reading a PDF and extracting meta-information
- changing meta-information  
- extracting text from a PDF
- extracting images from a PDF
- changing images in a PDF
- adding annotations (notes, links, etc) to a PDF
 and much more
 
## 2. Featured Example(s)

### 2.0 Adding a rubber stamp annotation to an existing PDF

From the spec:

    An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF
    document, or provides a way to interact with the user by means of the mouse and keyboard. PDF includes a
    wide variety of standard annotation types, described in detail in 12.5.6, “Annotation Types.”

    [...]

    A rubber stamp annotation (PDF 1.3) displays text or graphics intended to look as if they were stamped on the
    page with a rubber stamp. When opened, it shall display a pop-up window containing the text of the associated
    note. Table 181 shows the annotation dictionary entries specific to this type of annotation.

We start by reading the document:   

        # attempt to read PDF
        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Then we add the annotation:

        # add annotation
        doc.get_page(0).append_stamp_annotation(
            name="Confidential",
            contents="Approved by Joris Schellekens",
            color=X11Color("White"),
            rectangle=(Decimal(128), Decimal(128), Decimal(32), Decimal(64)),
        )

There are various parameters we can set here; 
- conforming readers should support at least the following values for the `name` parameter: Approved, Experimental, NotApproved, AsIs, Expired, NotForPublicRelease, Confidential, Final, Sold, Departmental, ForComment, TopSecret, Draft, ForPublicRelease
- contents is the text that should appear in the pop-up window when the stamp annotation is clicked
- color is the color of the pop-up window
- rectangle denotes the coordinates of the rubber stamp annotation

Finally, we store the output:

        # attempt to store PDF
        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)


The result should be something like this (keep in mind the rendering of the rubber stamp is the responsability of the PDF reader you happen to be using. Your result may differ accordingly.):

![adding an annotation to an existing pdf](readme_img/adding_a_rubber_stamp_annotation_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 2.1 Annotations

### 2.1.1 Adding multiple annotations (shaped like super Mario) to an existing PDF

From the spec:

    An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF
    document, or provides a way to interact with the user by means of the mouse and keyboard. PDF includes a
    wide variety of standard annotation types, described in detail in 12.5.6, “Annotation Types.”
    
    [...]        
    
    A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
    “Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
    entries specific to this type of annotation.

Let's add a few annotations to an existing PDF, shaped like super-mario.

First we start by defining the pixel-art grid, and the colors:


        m = [
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 2, 2, 2, 3, 3, 2, 3, 0, 0, 0, 0],
            [0, 0, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 0, 0],
            [0, 0, 2, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 0],
            [0, 0, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0],
            [0, 0, 0, 1, 1, 4, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 4, 1, 1, 4, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 0],
            [0, 3, 3, 1, 4, 5, 4, 4, 5, 4, 1, 3, 3, 0],
            [0, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 0],
            [0, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 4, 4, 4, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 0, 0],
            [0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0],
        ]
        c = [
            None,
            X11Color("Red"),
            X11Color("Black"),
            X11Color("Tan"),
            X11Color("Blue"),
            X11Color("White"),
        ]
        
Next we need to read an existing PDF document:

        doc = None
        with open('input.pdf', "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)
            
Now we can simply add all the annotations by calling the appropriate method on the `Page` object

        # add annotation
        pixel_size = 2
        for i in range(0, len(m)):
            for j in range(0, len(m[i])):
                if m[i][j] == 0:
                    continue
                x = pixel_size * j
                y = pixel_size * (len(m) - i)
                doc.get_page(0).append_link_annotation(
                    page=Decimal(0),
                    color=c[m[i][j]],
                    location_on_page="Fit",
                    rectangle=(
                        Decimal(x),
                        Decimal(y),
                        Decimal(x + pixel_size),
                        Decimal(y + pixel_size),
                    ),
                )

When adding a link annotation, we need to specify some arguments related to *what* we are linking to. 
In this case we specify that we want the annotation to link to page 0, and to force the pdf-viewer (e.g. Adobe Reader)
to fit the page (potentially zooming in/out).

We also specify a rectangle (this is where the user would click to activate the link), 
and a color (this is the color of the aforementioned rectangle).

In our case, we calculate the color and position based on our earlier grid of super-mario.

As a final step we need to store the resulting PDF document.

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The result should be something like this:

![adding an annotation to an existing pdf](readme_img/adding_multiple_annotations_shaped_like_super_mario_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 2.2 Exporting a PDF

### 2.2.1 Exporting an existing PDF as SVG image      

Scalable Vector Graphics (SVG) is an Extensible Markup Language (XML)-based vector image format for two-dimensional graphics with support for interactivity and animation. The SVG specification is an open standard developed by the World Wide Web Consortium (W3C) since 1999.

SVG images and their behaviors are defined in XML text files. This means that they can be searched, indexed, scripted, and compressed. As XML files, SVG images can be created and edited with any text editor, as well as with drawing software.

To export a page of a PDF document, we start by reading the input document:

        with open('input.pdf', "rb") as pdf_file_handle:
            l = SVGExport()
            doc = PDF.loads(pdf_file_handle, [l])
            with open('output.svg', "wb") as svg_file_handle:
                svg_file_handle.write(ET.tostring(l.get_svg_per_page(0)))

Line 2 of code creates an `EventListener` (an SVGExport in this case). 
`EventListeners` are a core component of `pText`. `EventListeners` are notified of rendering instructions
during the parsing step of a PDF document. The `SVGExport` listener will convert the rendering instructions it receives 
(drawing text, changing the active color, inserting an image, etc) to the corresponding XML/SVG syntax.

Line 3 loads the document, thus forcing the pages to be processed. The second argument of the static `PDF.loads` method
is a list of `EventListener` implementations.

Line 4 and 5 deal with saving the SVG file to disk.