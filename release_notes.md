# :mega: borb release 2.0.13

With this release, `borb` is one step closer to being able to write a PDF/A-1b document.
We still need to create an `\OutputIntents` Dictionary in the document to be fully compliant.
This is planned for the next release.

This release features:

- Minor bugfix to estimating width of a space character
  - Useful in text extraction
- Bugfix in `TrueTypeFont` to build a proper `\Widths` array and `cmap`
- Fixes in `XMPDocumentInfo` class
	- Title
	- Author
	- Creator
	- CreatorTool	
- Separate logic that writes `\Info` `Dictionary`
	- This class now also writes the `XMP` `\Metadata` when needed
	- Enables PDF/A-1b
	- Added tests for PDF/A-1b (preservation of metadata)

