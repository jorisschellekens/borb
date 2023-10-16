
# :mega: borb release notes

- Added some utility methods in `LayoutElement`
  - `get_golden_ratio_landscape_box`
  - `get_golden_ratio_portrait_box`
  - `get_largest_landscape_box`
  - `get_smallest_landscape_box`
- Removed `_calculate_min_and_max_layout_box` from `TableCell`
- Added tests for `get_golden_ratio_landscape_box`
- Added tests for `get_golden_ratio_portrait_box`
- Added utility class `A4PortraitTemplate`
  - This class represents an `A4_PORTRAIT` `Document`
  - It contains methods that allow you to directly add content to it
  - All the content-adding methods have sensible defaults (`font`, `font_size`, `font_color`, etc)
  - This class has a utility method to immediately `save` the `Document`
- Added tests for `A4PortraitTemplate`
- Fixed small bug in `add_outline` in `Document`