# :mega: borb release 2.0.27

This release is a small bugfix release.
- fixed `RunLengthDecode`
- fixed `ImageTransformer` to allow reading (JPEG) images, even when the `/Type` and `/Subtype` entry are not set
- fixed `DocumentInfo.get_file_size()`