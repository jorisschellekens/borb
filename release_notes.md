# :mega: borb release 2.1.1

This release is a feature release:
- `HTMLToPDF` has been updated to ensure even more HTML syntax is supported
  - `HTMLToPDF` allows you to specify a `typing.List[Font]` of fallback fonts
  - This allows you to use non-western characters in HTML and markdown
- `MarkdownToPDF` now uses `HTMLToPDF` (making it easier for me to maintain the code)
- Added `BlockFlow` and `InlineFlow` elements
- Added `SingleColumnLayoutWithOverflow` to enable certain `LayoutElement` implementations to be split across multiple `Page` objects. Currently only splitting of `Table` is supported.