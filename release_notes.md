# :mega: borb release 2.0.19

This release is a small feature release.

- Forms have been extended with `PushButton`, which enables you to place a `PushButton` in a PDF and tie an action to it.

- Tests for `PushButton` have been added to the repository.

- Examples for `PushButton` have been added to the examples repository.

- A test was added for issue #69 on GitHub, which deals with adding 500 `Heading` objects to a PDF.
Turns out recursive parsing has its limits :face_with_spiral_eyes:

- A small fix was introduced for issue #71 on GitHub

- `Annotation` now is its own proper class, each seperate `Annotation` has its own subclass. This makes the `Page` class a lot lighter (where the code previously resided).

- `Document` level JavaScript is now supported, examples and tests have been added to the corresponding repositories. 

- Both embedded files and JavaScript use the concept of a `NameTree` which is now its own separate class.

In order to make sure your code runs smoothly, check your imports when upgrading to the latest version.