# :mega: borb release 2.0.9

This release features:

- A small fix in `ChunksOfText` ensuring the `LayoutElement` does make unneeded copies
    - I also added a few tests for the new behaviour
    
- More documentation in the `Page` class (some minor work on annotations)

- A new annotation type (or rather a convenience method for an existing annotation type): remote-go-to
    - This enables you to embed links to websites in your PDF's.
    - I also added a few tests for this new method.
    
- Fixed a fair amount of MyPy warnings

- Added TextRank keyword-extraction algorithm
    - Implemented `BigramPartOfSpeechTagger`
    - Added test(s)    