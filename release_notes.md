# :mega: borb release 2.0.18

This release is a cleanup release.

- The library (previously called `ptext`) still had some imports being renamed as `pDecimal` or `pString` or `pList`.
  These occurences have been completely removed from the code.
- `borb` can now create PDF documents that are almost PDF/A-1b valid. Some effort for fonts remains.