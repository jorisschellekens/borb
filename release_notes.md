# :mega: borb release notes

## This release is a maintenance release.
- `FormField` elements behave more like `LayoutElement` now
- Add more `SmartArt`
- Add automated testing using GitHub actions
- Add `Version` class to have 1 point of reference for getting version/author/producer information

## Usage Statistics

Recently, `borb` has gone into the early stages of finding a reseller.
This is a very exciting step that I am sure will bring positive things for all of us, both `borb` and its users.

Understandably, the marketing/sales team would like some data to figure out what our target audience is, where to invest effort and resources, and more.
So I have added `UsageStatistics` to `borb`. This class gathers the following data:

- anonymous user ID (This is a randomly generated UUID, it is persisted in the installation directory of `borb` to ensure consistency between calls)
- city
- country name
- country code
- system platform (the operating system on which `borb` is running)
- state
- utc time in ms
- version (the version of `borb` that is running)

These statistics are periodically sent to our server(s). I have done my best to ensure this does not hinder the performance of `borb` in any way.
I urge to look at the source code of the `License` package to reassure yourself of the fact that we are gathering only the bare minimum of data.

Nevertheless, I fully understand that you may prefer not to send this information. 
You can turn it off by calling `UsageStatistics.disable()`.