Changes
=======

Version 2.0.1 (released 2024-09-20)

- Removes implicit dependency on setuptools and use importlib-metadata instead of the
  deprecated pkg_resources module

Version 2.0.0 (released 2024-03-04)

- Removes dependency on node-semver package
- Changes the NPM dependencies merging algorithm to fail when conflicting
  major versions of the same package are found.

Version 1.2.0 (released 2021-01-21)

- Fixes an issue where if you were using WebpackBundleProject with
  the LinkStorage to make symlinks, you would end up having your source
  package.json overwritten.

Version 1.1.0 (released 2020-05-25)

- Adds support for collecting aliases from bundles.
- Restore Python 2 compatibility.

Version 1.0.4 (released 2020-05-25)

- Python commands now fail when the NPM processes exit with an error.

Version 1.0.3 (released 2020-05-12)

- Fixes issue with incorrect parsing of webpack-bundle-tracker manifests.

Version 1.0.2 (released 2020-04-28)

- Adds a ``depth`` parameter to LinkStorage to allow for higher level
  symlinking on the folder-level.

Version 1.0.1 (released 2020-02-14)

- Adds support for having bundles that are callables in
  bundles_from_entry_point.

Version 1.0.0 (released 2018-10-29)

- Adds documentation and extra tests.

Version 0.1.2 (released 2017-11-06)

- Fix invalid closing of </link> tag.

Version 0.1.1 (released 2017-05-29)

- Fix problem with package.json not being updated.
- Fix merging of package.json dependencies.
- Increase test coverage.

Version 0.1.0 (released 2017-05-16)

- Initial public release.
