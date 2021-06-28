# :mega: pText release 2.0.0

This release features:
- Small bugfixes in the setup.py script (ensuring some dependencies that are present by default on Linux get installed on Windows)
- Refactor of the `LayoutElement` implementations
- Allowing users access to previously internal parameters of `PageLayout` implementations (such as margins)
- Improvements to `ChunksOfText` (now `HeterogeneousParagraph`, representing a heterogeneous paragraph)
- New text-layout class `Span` (similar to `HeterogeneousParagraph`, without default top/bottom margin)
- `LayoutElement` implementations have margins now (which was needed for HTML), you may expect some layout differences between this version of `pText` and former versions.
- A new PageLayout mechanism: `BrowserLayout`
- A new implementation of `BaseTable`.
    - `FlexibleColumnWidthTable`    (which behaves more like tables in HTML)
    - `FixedColumnWidthTable`       (which assigns a fixed width to every column)
- `HTMLToPDF` supports a lot more tags:
    - `body`
    - `head`
    - `meta`
    - `title`
    - `h1` to `h6`
    - `ħr`
    - `img`
    - `ul`, `ol`, `li`
    - `address`
    - `main`
    - `section`
    - `table`, `tbody`, `td`, `th`, `tr`
    - `b`, `strong`
    - `i`, `em`
    - `a`
    - `abbr`
    - `br`
    - `code`
    - `mark`
    - `p`

Check the examples and tests for more information.
A dozen or so documents have been provided as examples for `HTMLToPDF`.
