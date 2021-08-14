# :mega: borb release 2.0.8

This release features:

- Small bugfix in `Page.pop_page` function; `/Count` was not being updated properly 

- Convenient method to rotate `Page` clockwise and counterclockwise 90 degrees

- Refactor of all `EventListener` implementations

    - All methods that **get** something after an `EventListener` processes a `Document` now follow the naming convention `get_xxx_for_page`
    - e.g: `get_text_for_page`, `get_images_for_page`, `get_colors_for_page` etc
    
- Refactor of the `Color` API

    - All `Color` instances are now constructed with values `0..1`
    
        - Except `HexColor`, `Pantone` and `X11Color` (which are constructed with `str` objects)
        
    - Extra utility methods in `HSVColor`:
    
        - `complementary` : produces the complementary `Color` of the given `Color`
        - `analogous` : produces 2 `Color` objects that are similar to the given `Color`
        - `split_complementary`: produces 2 `Color` objects that are similar to the complementary of the given `Color`, thus forming a split complementary color group
        - `triadic` : produces 2 `Color` objects that form a triad with a given `Color`
        - `tetradic_rectangle`: produces 3 `Color` objects; a `Color` that is analogous to the given `Color` and the complementary pair of this pair
        - `tetradic_square`: produces 3 `Color` objects that form a tetradic square with the given `Color`
        
    - More tests (for aforementioned functionality)
    
- Improved testing 

    - Tests can now visually compare their output to a ground truth PNG
    
        - Output PDF of the test is converted to PNG (using GhostScript)
        - If a ground_truth.png file is present, its pixels are compared to the test output.png
        - Almost full automation of the entire test-suite   

- (the start of) Forms

    - FormField class represents a common base class for anything you might find on a form (checkbox, textfield, dropdown, etc)

        - Implementation of TextField
        - Implementation of DropDownList
        - Convenience implementation of CountryDropDownList
        - Implementation of CheckBox

    - Further releases will improve the way the layout algorithm handles these LayoutElement implementations
    
        - margin
        - padding
        - font_color
        - font
        - background_color
        - font_size
    
    - Once FormField objects can be added:
    
        - Retrieve fields (and in particular their values) from Page
        - Set value for each field (using Page)
        - "Flatten" (remove field, keep value) FormField             