# :mega: borb release notes

This release is a **beauty pageant** release:
- Classes have been split in 3 parts:
  - `CONSTRUCTOR`
  - `PRIVATE`
  - `PUBLIC`
- :+1: **All** class-methods in the `borb` package have been sorted (in their respective part)
- :+1: **All** public methods have been documented
- :+1: The vast majority of `mypy` warnings have been taken care of

Although the majority of the work has been done, this will always be an ongoing task.
As new development adds code, I may need this kind of release from time to time to ensure the quality of the code
stays up.

This release includes the following **minor fixes**:
- minor fix in `DisconnectedShape` (method names related to scaling were not analoguous to `ConnectedShape`)
