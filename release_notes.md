
# :mega: borb release notes

- Added pretty much all the `LayoutElement` implementations to the easy imports.
- Added a `LayoutElement` called `Map` with implementations `MapOfEurope`, `MapOfTheUnitedStates` and `MapOfTheWorld`. These `LayoutElement` instances draw a map of their respective territories, and allow you to mark one or multiple components with a different `fill_color`, `stroke_color` and `line_width`.
- Fixed tests related to unsplash API.
- Added tests for `A4PortraitTemplate`.
- Added tests for `A42ColumnPortraitTemplate`.
- Added tests for `SlideTemplate`.
- Added `TestCreateFullSlideTemplate`. Check out this `TestCase` if you want a concrete example of how to use `SlideTemplate` to produce a beautiful slideshow in PDF.