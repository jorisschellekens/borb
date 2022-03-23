# :mega: borb release 2.0.22

This release is a small feature release:

- Test have been added corresponding to issues on GitHub.
- More documentation has been added in general. No undocumented public methods!
- Unsplash API has been added, to ensure you can build rapid prototypes for Documents by just specifying keywords for images, rather than having to look for the perfect `Image`
- Small bugfix w.r.t. annotation names
- Small improvement in writing a PDF to bytes, inline array objects no longer have trailing newline character
- Small bugfix to fix layout of `FormField` objects using `FlexibleWidthColumnTable`
- Added some imports to `borb/pdf/__init__.py` to make it easier to import `borb` objects in general
- Added the EURion symbol to the `LineArtFactory`
- Added methods to rotate `Shape` and `DisjointShape`