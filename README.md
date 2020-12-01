
# pText

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Corpus Coverage : 95.6%](https://img.shields.io/badge/corpus%20coverage-95.6%25-green)]()

pText is a library for creating and manipulating PDF files in python.

## 1.0 Low-level model

pText offers a low-level model for representing a PDF document that is a strict implementation of the PDF specification.

### 1.1 Example : low-level model

    with open("input.pdf", "rb") as pdf_file_handle:
        
        doc = PDF.loads(pdf_file_handle)
        author = doc["XRef"]["Trailer"]["Info"]["Author"]
        print("The author of this PDF is %s" % author)
        
## 2. High-level model

pText also offers a high-level model that represents a PDF document as a more intuitive concept of pages, paragraphs, images, etc.

## 3. Extracting meta-information

### 3.1 Example : Extracting document information
    
    with open("input.pdf", "rb") as pdf_file_handle:
        
        doc = PDF.loads(pdf_file_handle)
        doc_info = doc.get_document_info()
        print("title   : %s" % doc_info.get_title())
        print("author  : %s" % doc_info.get_author())
        print("creator : %s" % doc_info.get_creator())
        print("producer: %s" % doc_info.get_producer())
        print("pages   : %s" % doc_info.get_number_of_pages())
        print("size    : %d" % doc_info.get_file_size())
        print("ids     : %s" % doc_info.get_ids())

### 3.2 Example : Extracting page information

    with open("input.pdf", "rb") as pdf_file_handle:
        
        doc = PDF.loads(pdf_file_handle)
        doc_info = doc.get_document_info()

        # print page information
        for i in range(0, doc_info.get_number_of_pages()):
            page_info = doc.get_page(i).get_page_info()
            print("page %d" % i)
            print("width   : %f" % page_info.get_width())
            print("height  : %f" % page_info.get_height())
            print("size    : %s" % str(page_info.get_size()))

### 3.3 Example : Extracting the color palette

    with open(file, "rb") as pdf_file_handle:
        l = ColorSpectrumExtraction()
        
        doc = PDF.loads(pdf_file_handle, [l])
        
        for t in l.get_colors_per_page(0, limit=16):
            print("rgb(%d, %d, %d) : %d" % (t[0].red, t[0].green, t[0].blue, t[1]))

   
This should print something like:

    rgb(245, 245, 245) : 1191
    rgb(245, 250, 245) : 1261
    rgb(5, 10, 20) : 1408
    rgb(250, 250, 245) : 3239
    rgb(5, 5, 15) : 10734
    rgb(5, 5, 20) : 24100
    rgb(250, 250, 250) : 46224
    rgb(125, 125, 125) : 86218
   
You could easily adapt this example to check whether a PDF uses colors that might be problematic for those with some form of color blindness.    
   
### 3.4 Example : Extracting the fonts

    with open("input.pdf", "rb") as pdf_file_handle:
        l = FontExtraction()
        
        doc = PDF.loads(pdf_file_handle, [l])
        
        for fn in l.get_font_names_per_page(0):
            print(fn)   
   
This should print something like this:   

    Times#20New#20Roman
    Arial,Bold
    Arial
    Arial,BoldItalic
    Arial
    Arial,Italic
  
## 4. Extracting text from a PDF

### 4.1 Example : Extracting text from pages

    with open("input.pdf", "rb") as pdf_file_handle:
            
        # create EventListener
        l = SimpleTextExtraction()
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle, [l])
            
        # print text (as processed by the SimpleTextExtraction EventListener)
        print(l.get_text_per_page(0))
    
### 4.2 Example : Matching a regular expression

    with open("input.pdf", "rb") as pdf_file_handle:
        l = RegularExpressionTextExtraction("[hH]ealth")
        doc = PDF.loads(pdf_file_handle, [l])

        # export matches
        output_file = self.output_dir / (file.stem + ".json")
        with open(output_file, "w") as json_file_handle:
            obj = [{"text": x.get_text(), 
                    "x0": x.get_baseline().x0, 
                    "y0":x.get_baseline().y0, 
                    "x1": x.get_baseline().x1, 
                    "y1":x.get_baseline().y1} for x in l.get_matched_text_render_info_events_per_page(0)]
            json_file_handle.write(json.dumps(obj, indent=4))

This should produce a file like this:

    [
        ...
        {
        "text": "he",
        "x0": 138.54864,
        "y0": 419.47,
        "x1": 150.82512,
        "y1": 419.47
        },
        {
            "text": "al",
            "x0": 150.85824,
            "y0": 419.47,
            "x1": 159.44736,
            "y1": 419.47
        },
        {
            "text": "t",
            "x0": 159.5136,
            "y0": 419.47,
            "x1": 162.58272,
            "y1": 419.47
        },
        ...
    ]

### 4.3 Example : Extract keywords using TF-IDF

    with open("input.pdf", "rb") as pdf_file_handle:
        l = TFIDFKeywordExtraction()
        doc = PDF.loads(pdf_file_handle, [l])

        print(l.get_text(0))
        for k in l.get_keywords_per_page(0, 5):
            print(k)
            
This should print something like this:

    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='SAFE', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='WITHOUT', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='ON', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='RESPONSIBILITIES', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='T', words_on_page=533, tf_idf=-0.0058864975)
   
## 5. Exporting a PDF

### 5.1 Example : Exporting a PDF as JSON   
 
    with open("input.pdf", "rb") as pdf_file_handle:
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle)
            
        # export to json
        with open("output.json", "w") as json_file_handle:
            json_file_handle.write(json.dumps(doc.as_dict(), indent=4))
                           
            
### 5.2 Example : Exporting a page to SVG format

    with open("input.pdf", "rb") as pdf_file_handle:
            
        # create EventListener
        l = SVGExport()
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle, [l])
            
        # export to svg
        with open("output.svg", "wb") as svg_file_handle:
            svg_file_handle.write(ET.tostring(l.get_svg_per_page(0)))

### 5.3 Example : Extracting all images from a page
    
    with open("input.pdf", "rb") as pdf_file_handle:
        l = SimpleImageExtraction()
        
        doc = PDF.loads(pdf_file_handle, [l])

        for i, img in enumerate(l.get_images_per_page(0)):
            output_file = "image_from_pdf_" + str(i) + ".jpg"
            with open(output_file, "wb") as image_file_handle:
                img.save(image_file_handle)

### 5.4 Example : Audio Export

    with open(file, "rb") as pdf_file_handle:
        l = AudioExport()
        
        # It is important to add SimpleStructureExtraction
        # This will ensure the AudioExport listener actually has paragraphs to work with
        doc = PDF.loads(pdf_file_handle, [SimpleStructureExtraction(), l])
        
        l.get_audio_file_per_page(0, output_file)
    
    
## 6. Structure Recognition

Data inside a PDF document is typically not structured. 
You should think of PDF more like a language for describing typesetting than a content-format.
It is possible however to attempt to build structure in this kind of document.

    with open("input.pdf", "rb") as pdf_file_handle:
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle, [SimpleStructureRecognition()])
            
SimpleStructureRecognition performs the following tasks:

1. Bundle TextRenderEvent objects in LineRenderEvent objects
2. Bundle LineRenderEvent objects in ParagraphRenderEvent objects
3. Bundle ParagraphRenderEvent objects in OrderedlistEvent objects (where applicable)
4. Bundle ParagraphRenderEvent objects in BulletlistEvent objects (where applicable)
5. Alert the EventListeners of the Page with the new Event objects
