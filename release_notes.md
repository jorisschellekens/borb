
# :mega: borb release notes

- add `Watermark` `LayoutElement`, representing a piece of text laid out over the entire `Page`. Users can specify the text, font_size, font_color, rotation, and transparency
- add `Watermark` to easy imports
- add tests for `Watermark`
- re-implement `MultiColumnLayout`, with better handling of headers and footers
- update `requirements.txt` where possible
- reworked a couple of tests, ensuring they can run without dependencies as well
- added a **fair use** warning to ensure people know the difference between using `borb` in an open-source vs. commercial setting. This warning is only triggered when producing a high volume of PDF documents.
