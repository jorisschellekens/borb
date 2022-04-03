# :mega: borb release 2.0.23

This release is a small feature release.
- rounded corners are available on `LayoutElement` and all its children
- all properties of `LayoutElement` are now available on all its children
  - with the exception of `FormField`
  - with the exception of nonsensical properties
    - e.g.: `font_size` on `Shape`
- `PDFToJPG` can now locate fonts on Windows and Mac
- `OCRImageRenderEventListener` has been made more resillient to bad input