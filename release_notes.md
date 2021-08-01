# :mega: borb release 2.0.7

This release features:

- `Table` detection
- fix quite a few `mypy` warnings
- rebranding of all examples
- rename `BaseTable` to `Table`
- `Chart` objects now have `horizontal_alignment` and `vertical_alignment`
- Update `README.md`

## Table Detection

This feature enables you to scan a `Page` (using the `TableDetectionByLines` implementation of `EventListener`) for content that is likely to be a `Table`.
You can then retrieve:

- the coordinates of the bounding box of the `Table`
- the coordinates of each cell (including those cells that may have `row_span` and/or `column_span`)

## Rename `BaseTable` to `Table`

I saw this inconsistency when I was writing a tutorial.
`List` has two implementations `OrderedList` and `UnorderedList`, it makes sense to rename `BaseTable` to `Table`.
Perhaps in future, more of these renames will occur as I try to achieve consistency over the entire library.

## Rebranding of all examples

Now that `borb` has a logo and theme-colors it makes sense to ensure every example uses these colors.
