
# :mega: borb release notes

This release is more of an aesthetic release.
- The imports have been reviewed, 
- a lot of code comments have been reviewed (adding parameters where needed)

A new feature (related to redaction) was added.
- `FaceDetectionEventListener` runs through a `Document` and triggers `_face_occurred` whenever a face is detected (in an image)
- `FaceEraserEventListener` (based on `FaceDetectionEventListener`) adds the typical (pixelated) blur to any detected face 