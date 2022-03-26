# :mega: borb release 2.0.22.2

This release is a small bugfix release.
By adding al lot of imports to `borb/pdf/__init__.py` suddenly all imports for `Chart` were imported.
This included `matplotlib.pyplot`. This import is only needed when working with `Chart`.
I changed the code in `Chart` to only declare the type, but not do the import (as it didn't really need to in the first place).