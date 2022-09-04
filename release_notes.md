# :mega: borb release 2.1.0

This release is a feature release:
- The `LayoutElement` framework has had a major upgrade
  - Each `LayoutElement` now offers a `get_layout_box` method which tells you how much space a `LayoutElement` takes up
  - Each `LayoutElement` now offers a `paint` method which renders the `LayoutElement` on a `Page` 
  - `LayoutElement` only adds its own content to the `Page` (previously it would change the order of page content to ensure backgrounds get drawn first)
- As a result of these changes, layout is a bit faster in this release, compared to previous releases
- All tests have been checked and changed to take into account the new behaviour
- Tests that perform visual comparison ignore `HexColor("00ff00")`, which allows me to add the date of the test in the output, and still compare only the relevant pixels
- `MarkdownToPDF` has been refactored to convert `Markdown` to `HTML`
- `HTMLToPDF` still needs work to produce PDF documents