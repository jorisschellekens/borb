# :mega: borb release notes

## This release is a feature release.

- Introducing `SimpleFindReplace` which enables you to find and replace text in a PDF
    - For examples on how to use it, check the examples repository
    - You can also check the `tests` directory in this project 


## This release fixes inconsistencies in `toolkit`

Most of the classes in the following table implement `EventListener` and are part of the package `toolkit`.
They have a class method (which you can call if you instantiate them and add them as `EventListener` to a PDF).
They also have a static method that you can call. The class method and static method typically return the same type/thing.

The static method has the advantage that it allows you to work with a `Document`, whereas the class method only works with a PDF that is being loaded.
Or, to put it simply, the static method can be used at any point in the life-cycle of `Document`, whereas the class method can only be used when reading an existing PDF.

This table gives you an overview of the available classes in `toolkit` and their methods:

| class                             | class method               | static method                        | status             |
|-----------------------------------|----------------------------|--------------------------------------|--------------------|
| `ColorExtraction`                 | `get_color`                | `get_color_from_pdf`                 | :heavy_check_mark: |
| `FontExtraction`                  | `get_fonts`                |                                      |                    |
| `FontExtraction`                  | `get_font_names`           |                                      |                    |
| `HTMLToPDF`                       |                            | `convert_html_to_layout_element`     | :heavy_check_mark: |
| `HTMLToPDF`                       |                            | `convert_html_to_pdf`                | :heavy_check_mark: |
| `ImageExtraction`                 | `get_images`               | `get_images_from_pdf`                | :heavy_check_mark: |
| `MarkdownToPDF`                   |                            | `convert_markdown_to_layout_element` | :heavy_check_mark: |
| `MarkdownToPDF`                   |                            | `convert_markdown_to_pdf`            | :heavy_check_mark: |
| `PDFToJPG`                        | `convert_to_jpg`           | `convert_pdf_to_jpg`                 | :heavy_check_mark: |
| `PDFToMP3`                        | `convert_to_mp3`           | `convert_pdf_to_mp3`                 | :heavy_check_mark: |
| `PDFToSVG`                        | `convert_to_svg`           | `convert_pdf_to_svg`                 | :heavy_check_mark: |
| `RegularExpressionTextExtraction` | `get_matches`              | `get_matches_for_pdf`                | :heavy_check_mark: |
| `SimpleLineOfTextExtraction`      | `get_lines_of_text`        | `get_lines_of_text_from_pdf`         | :heavy_check_mark: |
| `SimpleNonLigatureTextExtraction` | `get_text`                 | `get_text_from_pdf`                  | :heavy_check_mark: |
| `SimpleParagraphExtraction`       | `get_paragraphs`           | `get_paragraphs_from_pdf`            | :heavy_check_mark: |
| `SimpleTextExtraction`            | `get_text`                 | `get_text_from_pdf`                  | :heavy_check_mark: |
| `TableDetectionByLines`           | `get_tables`               |                                      |                    |
| `TableDetectionByLines`           | `get_table_bounding_boxes` |                                      |                    |
| `TextRankKeywordExtraction`       | `get_keywords`             | `get_keywords_from_pdf`              | :heavy_check_mark: |
| `TFIDFKeywordExtraction`          | `get_keywords`             | `get_keywords_from_pdf`              | :heavy_check_mark: |