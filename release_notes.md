# :mega: pText release 1.8.9

This release features a few non-essential updates to the pText codebase that are mostly related to testing.
This includes:
- All tests have been refactored to follow the same format, with a small table atop the resulting `PDF` describing the test, when the test was run, etc
- All tests (attempt to) follow the same color-scheme (making them look more professional and consistent)
- Tests against the entire corpus have been limited to the essentials, with extensive reporting

## :arrow_up: Performance Boost

There are a few minor tweaks that have boosted the performance of `pText` as a whole.
This includes the copy-behaviour of `Font` objects in the `CanvasGraphicsState`. This has caused a speed-up of nearly 33%.

## :page_facing_up: Fonts

I have also implemented some minor fixes to the whole `Font` logic, ensuring font-sizes are now handled properly, 
regardless of whether they are passed as an argument to the `Tf` operator or via the text-matrix in the `CanvasGraphicsState`.

I have also started implementing OCR. But more on that in a future release.

## :lock: Redaction

Finally, this release includes everything needed to perform redaction.
This is the process of:
- marking content to be removed (but not removing it, enabling review by a third party)
- removing content that has been marked

This functionality integrates nicely in the existing `pText` framework of `Page` annotations.
Check the examples for more details (look for "adding redaction annotations to a PDF")