# :mega: borb release 2.0.10

This release features:

- Changes to layout of text LayoutElement(s)
  - Support for `multiplied_leading`
  - Support for `fixed_leading`
  - Small fix to text justification algorithm

- Updated the test to comply with the new behaviour

- Added legal stuff to the library
  - BORB_CONTRIBUTOR_LICENSE_AGREEMENT.md
  - CONTRIBUTING.md

- Added an extra test/showcase
  - Creating a flyer using PDF graphics
  
- Removed EventListener options on PDF objects
  - EventListeners are now part of the parsing process, rather than the object
  - EventListeners are passed around during parsing
  - Objects are more lightweight

