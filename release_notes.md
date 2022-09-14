# :mega: borb release 2.1.3

This release is a minor bugfix release:
- Following the large refactor of `LayoutElement`, some minor classes still needed to be updated to work with the new framework. 
  Most notable among these is HTMLToPDF`.

- `GradientColoredDisjointShape` has become `GradientColoredDisconnectedShape` to follow suit with the rename of `DisjointShape` to `DisconnectedShape`.

- `InlineFlow` and `BlockFlow` have been moved to `page_layout`. Easy imports have been provided for them.

- More convenient imports have been made possible for `FormField` elements.

- The documentation of `borb` (to be found in the examples repository) has been given a major check. 
There is also a script that will automatically attempt to run each example code snippet. 
This should make it easier to detect when a new release breaks something in the examples repository. 
