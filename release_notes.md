
# :mega: borb release notes

This release features `GoogleTrueTypeFont` which enables users to access the Google Font API,
to directly use a `TrueTypeFont` in `borb` by specifying its name.

Tests have been added for this feature:

- `test_add_paragraphs_using_jacquard_12`
- `test_add_paragraphs_using_pacifico`
- `test_add_paragraphs_using_shadows_into_light`

Some tests have been added to guard code quality:

- `TestCodeFilesContainSortedMethods`
- `TestCodeFilesContainVisibilityComments`
- `TestCodeFilesDoNotContainNumbersInMethods`
- `TestCodeFilesNeverUseKeyring`