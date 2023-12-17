
# :mega: borb release notes

- Added support for (some) password-protected PDF documents
- Added test to check whether all imports are fully qualified
- Added test to check whether all imports are in the requirements
- Added test to check whether all imports are single line
- Added `CodeBlockWithSyntaxHighlighting` `LayoutElement`
- Ran `black`
- Ran `optimize imports`
- Removed dependency on `lxml`, which is only needed for `HTMLToPDF` 