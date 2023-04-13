# :mega: borb release notes

This release is a feature release:
- Added `Equation` to the `LayoutElement` hierarchy
  - `Equation` allows you to easily add mathematical expressions to a PDF
  - Determine the `font`, `font_size`, `font_color` and many other attributes
  - `Equation` behaves just like any other `LayoutElement`
  
- Fix minor issue in `SimpleFindReplace`

- Fix minor issue in `Image` (present for `Image` objects with mode `LA`)

- Fix `vertical_alignment` for `Table` implementations
  - `vertical_alignment` is now relative to the `Table` rather than to the `Page`
  - This approach does incur the cost of having to determine the tallest `LayoutElement` in the row