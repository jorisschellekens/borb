# :mega: borb release 2.0.25

This release is a small feature release.
- Small fix in `TextAnnotation`.
- Small fix(es) in tests related to redaction.
- All tests that produce a PDF now check the validity of that PDF using an external validator.
  - The default profile of this validator checks against the latest version of the PDF spec. `borb` was built to adhere to iso32000.
    Most notable difference is the embedding of the standard 14 fonts. I made a separate profile that checks only against the iso32000 spec.
  - `CheckBox` should be debugged. The validator marks it as a bad PDF.
  - For PDF A1/b to really match the spec, the fonts (even standard 14) need to be embedded.
- You can now specify `multiplied_inter_column_spacing` in `MultiColumnLayout`.
- `x or Decimal(y)` evaluates to `Decimal(y)` when `x == Decimal(0)`. This was unintended. I only wanted it to evaluate to `Decimal(y)` when `x is None`. I fixed all unwanted occurrences. This mostly affected the `LayoutElement` classes.
- Add `Alignment` to easy imports
- Add `LoremIpsum` class to quickly generate dummy text (using a markov chain)