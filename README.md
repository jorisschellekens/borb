# pText

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

pText is a library for creating and manipulating PDF files in python.

## low-level model

pText offers a low-level model for representing a PDF document that is a strict implementation of the PDF specification.

## high-level model

pText also offers a high-level model that represents a PDF document as a more intuitive concept of pages, paragraphs, images, etc.

## Extracting meta-information

### Extracting document information
    
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

### Extracting page information

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
   
## Extracting text from a PDF

### Extracting text from pages

    with open("input.pdf", "rb") as pdf_file_handle:
            
        # create EventListener
        l = SimpleTextExtraction()
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle, [l])
            
        # print text (as processed by the SimpleTextExtraction EventListener)
        print(l.get_text(0))
    
## Matching a regular expression

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

## Extract keywords using TF-IDF

    with open("input.pdf", "rb") as pdf_file_handle:
        l = TFIDFKeywordExtraction()
        doc = PDF.loads(pdf_file_handle, [l])

        print(l.get_text(0))
        for k in l.get_keywords(0, 5):
            print(k)
            
This should print something like this:

    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='SAFE', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='WITHOUT', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='ON', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='RESPONSIBILITIES', words_on_page=533, tf_idf=-0.0058864975)
    TFIDFKeyword(number_of_pages=1, occurs_on_pages=[0], term_frequency=4, text='T', words_on_page=533, tf_idf=-0.0058864975)
   
## Exporting a PDF

### Exporting a PDF as JSON   
 
    with open("input.pdf", "rb") as pdf_file_handle:
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle)
            
        # export to json
        with open("output.json", "w") as json_file_handle:
            json_file_handle.write(json.dumps(doc.as_dict(), indent=4))
                           
            
### Exporting a page to SVG format

    with open("input.pdf", "rb") as pdf_file_handle:
            
        # create EventListener
        l = SVGExport()
            
        # read/parse the document
        doc = PDF.loads(pdf_file_handle, [l])
            
        # export to svg
        with open("output.svg", "wb") as svg_file_handle:
            svg_file_handle.write(ET.tostring(l.get_svg(0)))
                