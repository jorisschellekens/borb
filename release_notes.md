# :mega: borb release notes

This release refactors the testing in `borb`.
- All tests have been refactored into directories corresponding the main functionality they test
  - E.g. tests for `Equation` (in `borb.pdf.canvas.layout.equation`) can be found in `tests.pdf.canvas.layout.equation`
  - Tests derive from `TestCase`
    - `TestCase` offers some utility methods to standardize output files
    - `TestCase` offers the methods to visually compare an output
    - `TestCase` offers the methods to check a PDF using a validator