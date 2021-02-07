# Examples

## 1. Annotations

    An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF
    document, or provides a way to interact with the user by means of the mouse and keyboard. PDF includes a
    wide variety of standard annotation types, described in detail in 12.5.6, “Annotation Types.”

### 1.0 Adding all possible rubber stamp annotations to an existing PDF

    A rubber stamp annotation (PDF 1.3) displays text or graphics intended to look as if they were stamped on the
    page with a rubber stamp. When opened, it shall display a pop-up window containing the text of the associated
    note. Table 181 shows the annotation dictionary entries specific to this type of annotation.

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

We now define a `List[str]` to hold all valid types of rubber stamp annotations, 
we iterate over it, and add them to the document one at a time:

        # add annotation
        for index, name in enumerate(
            [
                "Approved",
                "Experimental",
                "NotApproved",
                "Asis",
                "Expired",
                "NotForPublicRelease",
                "Confidential",
                "Final",
                "Sold",
                "Departmental",
                "ForComment",
                "TopSecret",
                "Draft",
                "ForPublicRelease",
            ]
        ):
            doc.get_page(0).append_stamp_annotation(
                name=name,
                contents="Approved by Joris Schellekens",
                color=X11Color("White"),
                rectangle=Rectangle(
                    Decimal(128), Decimal(128 + index * 34), Decimal(64), Decimal(32)
                ),
            )

There are some parameters we can set here:
- `name`: indicates the kind of stamp (e.g. 'Approved' or 'Draft' etc)
- `contents`: this is the text shown when the annotation is clicked in a PDF reader
- `color`: this is the `Color` of the pop-up that displays the aforementioned text
- `rectangle`: this is where the annotation is to be placed

Note that you do not have control over the appearance of this particular annotation.
The specific appearance is down to the implementation of the PDF reader (e.g. Adobe Acrobat Reader).

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:

![adding an annotation to an existing pdf](readme_img/adding_all_rubber_stamp_annotations_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.1 Adding a circle annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Now we can add the annotation:

        # add annotation
        doc.get_page(0).append_circle_annotation(
            rectangle=Rectangle(Decimal(128), Decimal(128), Decimal(64), Decimal(64)),
            stroke_color=X11Color("Plum"),
            fill_color=X11Color("Crimson"),
        )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:

![adding an annotation to an existing pdf](readme_img/adding_a_circle_annotation_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.


### 1.2 Adding a highlight annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Next we add the annotation:

        # add annotation
        doc.get_page(0).append_highlight_annotation(
            rectangle=Rectangle(
                Decimal(72.86), Decimal(486.82), Decimal(129), Decimal(13)
            ),
            contents="Lorem Ipsum Dolor Sit Amet",
            color=X11Color("Yellow"),
        )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:

![adding an annotation to an existing pdf](readme_img/adding_a_highlight_annotation_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.3 Adding a link annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Next we add the annotation:

        doc.get_page(0).append_link_annotation(
            page=Decimal(0),
            location_on_page="Fit",
            color=X11Color("AliceBlue"),
            rectangle=Rectangle(Decimal(128), Decimal(128), Decimal(64), Decimal(64)),
        )
        
There are some parameters we can set here:
- `page`: indicates the page number of the page you would like to link to
- `location_on_page`: In this case 'Fit' means 'show the entire page, and force the viewer to zoom until it fits'
        
Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

### 1.4 Adding a polygon annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Next we add the annotation:

        doc.get_page(0).append_polygon_annotation(
            points=[
                (Decimal(72), Decimal(390)),
                (Decimal(242), Decimal(500)),
                (Decimal(156), Decimal(390)),
            ],
            color=X11Color("Crimson"),
        )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:

![adding an annotation to an existing pdf](readme_img/adding_a_polygon_annotation_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.5 Adding a polyline annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Next we add the annotation:

        doc.get_page(0).append_polyline_annotation(
            points=[
                (Decimal(72), Decimal(390)),
                (Decimal(242), Decimal(500)),
                (Decimal(156), Decimal(390)),
            ],
            color=X11Color("Crimson"),
        )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

### 1.6 Adding a redact annotation to an existing PDF

### 1.7 Adding a rubber stamp annotation to an existing PDF

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
- `name`: conforming readers should support at least the following values for the `name` parameter: Approved, Experimental, NotApproved, AsIs, Expired, NotForPublicRelease, Confidential, Final, Sold, Departmental, ForComment, TopSecret, Draft, ForPublicRelease
- `contents`: is the text that should appear in the pop-up window when the stamp annotation is clicked
- `color`: is the `Color` of the pop-up window
- `rectangle`: denotes the coordinates of the rubber stamp annotation

Finally, we store the output:

        # attempt to store PDF
        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)


The result should be something like this (keep in mind the rendering of the rubber stamp is the responsability of the PDF reader you happen to be using. Your result may differ accordingly.):

![adding an annotation to an existing pdf](readme_img/adding_a_rubber_stamp_annotation_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.8 Adding a square annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Now we can add the annotation:

        # add annotation
        doc.get_page(0).append_square_annotation(
            rectangle=Rectangle(Decimal(128), Decimal(128), Decimal(64), Decimal(64)),
            stroke_color=X11Color("Plum"),
            fill_color=X11Color("Crimson"),
        )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:

![adding an annotation to an existing pdf](readme_img/adding_a_square_annotation_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.9 Adding a square annotation around a regular expression match to an existing PDF

We start by reading the PDF:

        doc = None
        l = RegularExpressionTextExtraction("[sS]orbitol")        
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

Notice that we are passing an `EventListener` instance to the `PDF.loads` method.
This `EventListener` will be notified every time a rendering instruction takes place.
The `RegularExpressionTextExtraction` implementation will use these instructions to determine whether a given regular expression has been matched.

Next we are going to add annotations (in this case square annotations) around every `TextRenderEvent` that belongs to a regular expression match.

        for e in l.get_matched_text_render_info_events_per_page(0):
            baseline = e.get_baseline()
            doc.get_page(0).append_square_annotation(
                rectangle=Rectangle(
                    Decimal(baseline.x0),
                    Decimal(baseline.y0 - 2),
                    Decimal(baseline.x1 - baseline.x0),
                    Decimal(12),
                ),
                stroke_color=X11Color("Firebrick"),
            )
            
Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:

![adding an annotation to an existing pdf](readme_img/adding_an_annotation_around_a_regular_expression_match_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.


### 1.10 Adding a square annotation in the free space of a page to an existing PDF

Sometimes the position of the annotation does not matter that much, 
as long as it does not block any other visible content.

Finding the available free space on a `Page` can be tricky, 
it would involve re-parsing all the content to figure out where existing content intersects with the desired location of the annotation.
That is why `pText` comes with `FreeSpaceFinder`, this class searches for an `Rectangle` of a given size, nearest to a given point (in Euclidean space).

Let's see it in action.
We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Next we instantiate the `FreeSpaceFinder` with a given page as argument.

        # determine free space
        space_finder = FreeSpaceFinder(doc.get_page(0))

Now we can attempt to add the annotation. 
We call the method `find_free_space` passing it the ideal `Rectangle` where we would like to place the annotation (or any other object really).
`find_free_space` returns an `Optional[Rectangle]` (sometimes the `Page` is full).

        # add annotation
        w, h = doc.get_page(0).get_page_info().get_size()
        free_rect = space_finder.find_free_space(
            Rectangle(
                Decimal(w / Decimal(2)),
                Decimal(h * Decimal(0.1)),
                Decimal(64),
                Decimal(64),
            )
        )
        
If there is room on the `Page` for the annotation, we can now add it. 
Notice that we wanted to add the annotation to the bottom center of the page.        
        
        if free_rect is not None:
            doc.get_page(0).append_square_annotation(
                rectangle=free_rect,
                stroke_color=HexColor("#F75C03"),
                fill_color=HexColor("#04A777"),
            )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The end result (at least the annotations) should look something like this:
Notice how our use of `FreeSpaceFinder` meant that the annotation did not collide with the existing page-number on the bottom of the `Page`.

![adding an annotation to an existing pdf](readme_img/adding_a_square_annotation_in_free_space_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.11 Adding a collection of annotations shaped like super mario to an existing PDF

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
In this case we specify that we want the annotation to link to `Page` 0, and to force the pdf-viewer (e.g. Adobe Reader)
to fit the `Page` (potentially zooming in/out).

We also specify a `Rectangle` (this is where the user would click to activate the link), 
and a `Color` (this is the color of the aforementioned rectangle).

In our case, we calculate the `Color` and position based on our earlier grid of super-mario.

As a final step we need to store the resulting PDF document.

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

The result should be something like this:

![adding an annotation to an existing pdf](readme_img/adding_multiple_annotations_shaped_like_super_mario_to_an_existing_pdf.png)

Check out the `tests` directory to find more tests like this one, and discover what you can do with pText.

### 1.12 Adding a text annotation to an existing PDF

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Now we can add the annotation:

        # add annotation
        doc.get_page(0).append_text_annotation(
            contents="The quick brown fox ate the lazy mouse",
            rectangle=Rectangle(Decimal(128), Decimal(128), Decimal(64), Decimal(64)),
            name_of_icon="Key",
            open=True,
            color=X11Color("Orange"),
        )

Finally, we need to store the resulting PDF document.

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)


### 1.13 Adding a watermark annotation to an existing PDF

### 1.14 Adding an annotation using a shape from the `LineArtFactory` to an existing PDF

The `LineArtFactory` class allows you to easily create shapes (defined as `List[Tuple[Decimal,Decimal]]` ), it contains everything you need to render:
- triangles (right sided triangle, isoceles triangles)
- stars (with convenience methods for 4-sided stars, 5-sided stars, 6-sided stars)
- 4-gons (paralellogram, trapezoid, diamond)
- regular n-gons (with convenience methods for pentagon, hexagon, heptagon, octagon)
- fractions of circles (with convenience methods for half a circle and three quarters of a circle)
- arrows (left, right, up, down)
- misc. (droplet, sticky note, etc)

We start by reading the PDF:

        doc = None
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

Now we can add the annotation:

        # get the shape
        shape = LineArtFactory.droplet(
            Rectangle(Decimal(128), Decimal(128), Decimal(64), Decimal(64))
        )

        # add annotation
        doc.get_page(0).append_polyline_annotation(
            points=shape,
            stroke_color=X11Color("Salmon"),
        )

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

### 1.15 Get all annotations from an existing PDF

Getting all annotations from a PDF is easy, if you know where to look.
Let's start by opening the PDF document:

        with open("input.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            page = doc.get_page(0)

Annotations are defined in the \Page dictionary of whatever page the annotation appears at.
Let's check the first `Page`.

            if "Annots" in page:
                print("%s has %d annotations" % (file.stem, len(page["Annots"])))


## 2. Meta-information

### 2.1 Getting the author of an existing PDF

A PDF document can have an \Info dictionary entry, containing meta-information.
Because this entry is optional, we need to check at every step of the way whether the path we attempt to navigate exists.

We start by opening the document:

        with open("input.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            
Then we check whether the document has an XRef table (it should, unless the document is corrupt)          

            if "XRef" not in doc:
                return False

Next we check whether the XRef table has a \Trailer (it should).
                
            if "Trailer" not in doc["XRef"]:
                return False

In the \Trailer dictionary, we may find an \Info dictionary.
This dictionary could contain an entry for \Author.
                
            if (
                "Info" in doc["XRef"]["Trailer"]
                and "Author" in doc["XRef"]["Trailer"]["Info"]
            ):
                author = doc["XRef"]["Trailer"]["Info"]["Author"]
                print("The author of this PDF is %s" % author)

### 2.2 Getting all meta-information of an existing PDF using `DocumentInfo` 

`DocumentInfo` represents a convenience class to easily extract all meta-information in the document catalog's \Info dictionary.
You can use it to quickly query the meta-information.

        with open("input.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            doc_info = doc.get_document_info()
            print("title    : %s" % doc_info.get_title())
            print("author   : %s" % doc_info.get_author())
            print("creator  : %s" % doc_info.get_creator())
            print("producer : %s" % doc_info.get_producer())
            print("ids      : %s" % doc_info.get_ids())
            print("language : %s" % doc_info.get_language())

### 2.3 Changing the author of an existing PDF

Let's start by reading the PDF document.

        doc = None
        with open("input.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

Now we check whether the PDF has an XRef, containing a \Trailer

        if "XRef" not in doc:
            return False
        if "Trailer" not in doc["XRef"]:
            return False

If there is no \Info dictionary in the \Trailer, we create it

        if "Info" not in doc["XRef"]["Trailer"]:
            doc["XRef"]["Trailer"][Name("Info")] = Dictionary()

Let's set the \Author entry in the \Info dictionary

        # change author
        doc["XRef"]["Trailer"]["Info"]["Author"] = String("Joris Schellekens")

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

### 2.4 Changing the producer of an existing PDF

Let's start by reading the PDF document.

        doc = None
        with open("input.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

Now we check whether the PDF has an XRef, containing a \Trailer

        if "XRef" not in doc:
            return False
        if "Trailer" not in doc["XRef"]:
            return False

If there is no \Info dictionary in the \Trailer, we create it

        if "Info" not in doc["XRef"]["Trailer"]:
            doc["XRef"]["Trailer"][Name("Info")] = Dictionary()

Let's set the \Producer entry in the \Info dictionary

        # change author
        doc["XRef"]["Trailer"]["Info"]["Producer"] = String("pText")

Now we can store the PDF document again:

        with open("output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

### 2.5 Reading the XMP metadata of an existing PDF

This example is similar to the earlier example involving `DocumentInfo`.
But in stead, we will use `XMPDocumentInfo`. This class offers even more methods to get information from a PDF document.
Keep in mind that XMP is not a requirement for a PDF document to be valid. So you may find these methods return `None` when you test them on a document that does not have embedded XMP data.

        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            doc_info = doc.get_xmp_document_info()
            print("title                : %s" % doc_info.get_title())
            print("author               : %s" % doc_info.get_author())
            print("creator              : %s" % doc_info.get_creator())
            print("producer             : %s" % doc_info.get_producer())
            print("ids                  : %s" % doc_info.get_ids())
            print("language             : %s" % doc_info.get_language())
            print("document-ID          : %s" % doc_info.get_document_id())
            print("original document-ID : %s" % doc_info.get_original_document_id())
            print("creation date        : %s" % doc_info.get_creation_date())
            print("modification date    : %s" % doc_info.get_modification_date())
            print("metadata date        : %s" % doc_info.get_metadata_date())
            print("")

I tried this on a document with XMP meta-data, and it printed the following:

    title                : None
    author               : None
    creator              : None
    producer             : Adobe PDF Library 15.0
    ids                  : ['0952B683A7F340E48FD2F5409F3E6D08', 'AF7A23737C7A664D93DF2CBE97397150']
    language             : en-GB
    document-ID          : xmp.id:54e5adca-494c-4c10-983a-daa03cdae65a
    original document-ID : xmp.did:b857e947-9e0d-4cd3-aff9-40a81c991e7a
    creation date        : 2017-12-15T15:38:40+01:00
    modification date    : 2017-12-15T16:23:53+01:00
    metadata date        : 2017-12-15T16:23:53+01:00

## 3. Extracting Text

### 3.1 Extract text from a PDF using `SimpleTextExtraction`

Let's start by reading the PDF document.

        with open("input.pdf", "rb") as pdf_file_handle:
            l = SimpleTextExtraction()
            doc = PDF.loads(pdf_file_handle, [l])

Notice that we are passing an `EventListener` instance to the `PDF.loads` method.
This `EventListener` will be notified every time a rendering instruction takes place.
`SimpleTextExtraction` processes those rendering instructions related to displaying text, 
and attempts to build the resulting text on the `Page` using some (simple) heuristics.

Now that we've processed the `Page`, we can get the resulting text and store it.

            # export txt
            with open("output.txt", "w") as txt_file_handle:
                txt_file_handle.write(l.get_text(0))

### 3.2 Extract text from a PDF using `SimpleNonLigatureTextExtraction`

In writing and typography, a ligature occurs where two or more graphemes or letters are joined as a single glyph. An example is the character æ as used in English, in which the letters a and e are joined. The common ampersand (&) developed from a ligature in which the handwritten Latin letters e and t (spelling et, Latin for and) were combined.

Dealing with ligatures can make text-parsing challenging. You never know whether your PDF document is going to contain "ﬁ" (ligature) or "fi" (two separate characters).

And although these characters might look the same, a regular expression that matches "if" (two separate characters) will not match "ﬁ" (ligature).

Hence `SimpleNonLigatureTextExtraction`, it works much like `SimpleTextExtraction`, replacing every ligature in the resultant text with its separate characters, 
ensuring text that is easy to process afterwards.

Let's start by reading the PDF document.

        with open("input.pdf", "rb") as pdf_file_handle:
            l = SimpleNonLigatureTextExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            
Once the document is done processing, we can easily obtain and store the text:           

            # export txt
            with open("output.txt", "w") as txt_file_handle:
                txt_file_handle.write(l.get_text(0))

### 3.3 Match a regular expression in a PDF using `RegularExpressionTextExtraction`

We start by reading the PDF:

        doc = None
        l = RegularExpressionTextExtraction("[sS]orbitol")        
        with open("input.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

Notice that we are passing an `EventListener` instance to the `PDF.loads` method.
This `EventListener` will be notified every time a rendering instruction takes place.
The `RegularExpressionTextExtraction` implementation will use these instructions to determine whether a given regular expression has been matched.

We can access this information in the following manner:

            # export matches
            with open("sorbitol_matches.json", "w") as json_file_handle:
                obj = [
                    {
                        "text": x.get_text(),
                        "x0": int(x.get_baseline().x0),
                        "y0": int(x.get_baseline().y0),
                        "x1": int(x.get_baseline().x1),
                        "y1": int(x.get_baseline().y1),
                    }
                    for x in l.get_matched_text_render_info_events_per_page(0)
                ]
                json_file_handle.write(json.dumps(obj, indent=4))
            
This should store the coordinates of the individual letters that matched the regular expression.           
In my example document, this was the output:

    [
    {
        "text": "S",
        "x0": 73,
        "y0": 265,
        "x1": 78,
        "y1": 265
    },
    {
        "text": "o",
        "x0": 78,
        "y0": 265,
        "x1": 84,
        "y1": 265
    },
    {
        "text": "r",
        "x0": 84,
        "y0": 265,
        "x1": 87,
        "y1": 265
    },
    ...

### 3.4 Extract all keywords from a PDF using `TFIDFKeywordExtraction`

## 4. PDF Creation

### 4.1 Creating an empty PDF

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # write
        with open("output.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

### 4.2 Creating a 'Hello World' PDF

This example describes how to create a PDF from scratch. 
This example focuses on giving the reader an understanding of the underlying PDF syntax. 
This is definitely not the easiest way to write a PDF.

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

This is where the actual content generation begins. To get content on a page we need to alter its content-stream.
First we'll create a content stream, and then we'll set its bytes to the appropriate operators to write 'Hello World!'

        # create content stream
        content_stream = Stream()
        content_stream[
            Name("DecodedBytes")
        ] = b"""
            q
            BT
            /F1 24 Tf            
            100 742 Td            
            (Hello World!) Tj
            ET
            Q
        """

The `q` and `Q` operator define a context in which we can work. these operators respectively push and pop the entire graphics state unto/from a stack.
By doing so, we can ensure our content will not interfere with other content that may exist on the page.

Next we have the `BT` (begin text) and `ET` (end text) operators. They set up everything to enable us to write text.
`Tf` sets the font (in this case `F1`) and font-size.

`Td` determines the position at which we will draw text.
`Tj` writes a string (enclosed in round brackets) to the PDF.

Next we need to set the properties of the content-stream to match its content. 
In this example we'll encode the bytes using `FlateDecode`. 
Thus we need to provide a `Filter` property (so the reader knows which decompression algorithm to use), 
and provide a `Length` (so the reader knows how long our encoded byte-stream is).


        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Filter")] = Name("FlateDecode")
        content_stream[Name("Length")] = Decimal(len(content_stream["Bytes"]))

Next we can set this `Stream` to be the `Contents` of the `Page`

        # set content of page
        page[Name("Contents")] = content_stream

In the following code-snippet, we set every property related to the font we used.
We need to specify the font used by the `Tj` operator in the `Resources` dictionary of the `Page`.

        # set Font
        page[Name("Resources")] = Dictionary()
        page["Resources"][Name("Font")] = Dictionary()
        page["Resources"]["Font"][Name("F1")] = Dictionary()
        page["Resources"]["Font"]["F1"][Name("Type")] = Name("Font")
        page["Resources"]["Font"]["F1"][Name("Subtype")] = Name("Type1")
        page["Resources"]["Font"]["F1"][Name("Name")] = Name("F1")
        page["Resources"]["Font"]["F1"][Name("BaseFont")] = Name("Helvetica")
        page["Resources"]["Font"]["F1"][Name("Encoding")] = Name("MacRomanEncoding")

In this example I chose Helvetica, because the reader is supposed to know all the details of this font (width of every glyph, bouding box, etc).
That means we don't have to specify all the details. In the above code-snippet, we only really mentioned the name and character encoding.

Next we store the PDF.

        # attempt to store PDF
        with open("output.pdf", "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)


### 4.3 Creating a 'Hello World' PDF, the easier way

Luckily, there is an easier way to get content on a PDF.
Let's look at the convenience classes `pText` provides.

We'll start similar to our previous example, by creating an empty `Document` and `Page`.

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

Now instead of having to figure out all these instructions ourselves, we can let `pText` do the heavy lifting.
Here we add a `ChunkOfText` to the `Page`, but other classes allow you to add lines of text, paragraphs, tables, etc.

        ChunkOfText(
            "Hello World!", font_size=Decimal(24), color=X11Color("YellowGreen")
        ).layout(
            page, Rectangle(Decimal(100), Decimal(724), Decimal(100), Decimal(100))
        )

`ChunkOfText` allows us to specify the `font_size`, `Color` and `font`. If not provided, `ChunkOfText` defaults to black Helvetica, size 12.
We then call `layout` on this object to have it put on the `Page`.

Finally, we can store the PDF.

        # attempt to store PDF
        with open("output.pdf", "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)


### 4.4 Creating a colorful 'Hello World' PDF

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        for i, c in enumerate(
            [
                X11Color("Red"),
                X11Color("Orange"),
                X11Color("Yellow"),
                X11Color("YellowGreen"),
                X11Color("Blue"),
                X11Color("Purple"),
            ]
        ):
            ChunkOfText("Hello World!", font_size=Decimal(24), color=c).layout(
                page,
                Rectangle(
                    Decimal(100 + i * 30), Decimal(724 - i * 30), Decimal(100), Decimal(100)
                ),
            )

        # attempt to store PDF
        with open("output.pdf", "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)