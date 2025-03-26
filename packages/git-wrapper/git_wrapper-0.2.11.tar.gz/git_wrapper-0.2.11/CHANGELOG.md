# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.11] - 2025-03-25
### Changed
- Remove remote for re-creating it if url has changed.
- Fix the format of the readthedocs config file.
- Update deprecated action versions.
- Removed incorrect version references.
- Update github action versions.

## [0.2.10] - 2022-09-30
### Changed
- Add function to convert a commit reference to a commit hexsha.

## [0.2.9] - 2022-06-30
### Changed
- Added Prune Functionality To Fetch.
- Added Information About Integration Tests To Docs.
- Update mergify config to use queue instead of merge.
- Fixes for publish job.
- Update documentation to support new 'autochangelog' setup.
- Initial automation of changelog generation.
- Commit_format should be an internal-only method.
- Remove dangling reference to Python 2.7, no longer supported.
- Replace %s string substitutions with f-strings.
- Switch to f-string over .format method.
- Limit to run only on master.
- Remove python 2-specific code.
- Use tox for make test target.
- Change fetch-depth to get correct tag info for builds.
- Change how we generate version for test pypi builds.
- Fix deploy job.
- Improvements to publish github action.
- Fix typo in readme.
- Revamp our build process to be more in line with our other projects.

## [0.2.8] - 2021-07-29
### Changed
- Prep for version 0.2.8 release.
- Add publish action.
- Tweaks to workflow.
- Modify to allow tag listing.
- [#GH-75] Create GitHub Action CI job for twine check.
- Mergify update (#81).

## [0.2.7] - 2021-04-28
### Changed
- Prepare 0.2.7 release.
- Ensure apply_diff also includes new files when committing changes.
- Fix branch names in github action (#79).
- Use Github Actions to run the tests and remove Travis (#78).

## [0.2.6] - 2021-02-11
### Changed
- Prepare 0.2.6 release.
- Provide new helper related to the log.
- Move property initialisation to __init__.

## [0.2.5] - 2021-01-12
### Changed
- Preps for 0.2.5 release.

## [0.2.4.1] - 2021-01-11
### Changed
- Update __version__ to 0.2.4.1.
- Fix RST formatting error preventing uploads to Pypi.

## [0.2.4] - 2021-01-11
### Changed
- Prep for 0.2.4 release.
- Add function to grep logs (#71).
- Add function to cherry-pick a commit.
- Preserve square brackets in commit messages when applying patches.

## [0.2.3] - 2020-12-15
### Changed
- Prep for 0.2.3 release.
- Add option to checkout newly created branches.
- Add option to run the integration tests with podman.
- Update README with new release instructions.

## [0.2.2] - 2020-07-20
### Changed
- Prepare 0.2.2 release.
- New function to check if a commit exists on a given remote branch.

## [0.2.1] - 2019-04-16
### Changed
- Prep for version 0.2.1 release.
- Add tagging functions.
- Add function to compare commit references.
- Check reference exists in commit.describe.
- Update travis url so mergify works.
- Update mergify config for v2 api.

## [0.2.0] - 2019-01-18
### Changed
- Prep for version 0.2.0 release.
- Add convenience method for creating a branch.
- Add convenience method for checking if a branch exists.
- Fix broken doc string.
- Add functionality to refresh a repository's remotes.
- Add --bare cloning option.
- Add log diff functionality.
- Allow customised commit message for reverts.
- Integration tests for some GitCommit/GitBranch functions.
- Improve a few doc strings.
- Removing python 3.5 tests.
- Add a couple of examples to the usage doc.
- Move describe to GitCommit.
- Move apply and reverse functions to GitBranch.
- Rename GitWrapperCommit into GitCommit.
- Move cherry functions into GitBranch.
- Move rebase functionality into GitBranch.
- Move clone functionality into base GitRepo.
- Move Remote functions into their own class.
- GitWrapperBase becomes GitRepo.
- Logging setup improvements.
- Minor string formatting improvements.
- Add functionality to destroy a repo and reclone it.
- Add git clone support.
- Add Tox & Travis support for py37.
- Skeleton code for integration tests.
- Add back support for Python 2.7.
- Add support for applying a diff.
- Add support for applying a patch.
- Add support for basic committing and commit revert.
- Refactor branch/hash checks into a decorator.
- Fix rebasing on branch issue.
- Adding contributors.
- Drop py34 from Travis environments.
- Move setup to use pbr.
- Add coverage in tests reports.
- Avoid sending git CommandError back to the user.
- Unify 'mock' imports.
- Drop py34.
- Add basic logging in more places.
- Fix several doc strings formatting.
- Fixing readthedocs not generating api information.
- Add support for basic rebase + abort.
- Fix a couple of typos.
- Fixing inconsistent quote marks in doc strings.
- Removing the Travis CI python2.7 config.
- Removing python 2 support.
- Adding the wrapt dependency to simplify the Python 2 code for the.
- Signature() is Python 3.5 only. inspect.getcallargs() doesn't.

## [0.1.0] - 2018-07-05
### Changed
- Preping of tag 0.1.0.
- Fixing mergify config file whitespace (#12).
- Correcting the HISTORY.rst file.
- Adding a mergify config (#10).
- Moving away from pipenv. (#5).
- Fixing tox.ini flake8 for tests.
- Merge pull request #6 from jpichon/fix-make-lint.
- 'Make lint' should match the tox setup.
- Adding GitWrapperCherry (#4).

## [0.0.1] - 2018-06-20
### Changed
- Adding a wrapper base class and unit tests. (#3).
- Fixing travis-ci badge. (#2).
- Initial project structure (#1).
- Initial commit of README.rst.

[Unreleased]: https://github.com/release-depot/git_wrapper/compare/0.2.11...HEAD
[0.2.11]: https://github.com/release-depot/git_wrapper/compare/0.2.10...0.2.11
[0.2.10]: https://github.com/release-depot/git_wrapper/compare/0.2.9...0.2.10
[0.2.9]: https://github.com/release-depot/git_wrapper/compare/0.2.8...0.2.9
[0.2.8]: https://github.com/release-depot/git_wrapper/compare/0.2.7...0.2.8
[0.2.7]: https://github.com/release-depot/git_wrapper/compare/0.2.6...0.2.7
[0.2.6]: https://github.com/release-depot/git_wrapper/compare/0.2.5...0.2.6
[0.2.5]: https://github.com/release-depot/git_wrapper/compare/0.2.4.1...0.2.5
[0.2.4.1]: https://github.com/release-depot/git_wrapper/compare/0.2.4...0.2.4.1
[0.2.4]: https://github.com/release-depot/git_wrapper/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/release-depot/git_wrapper/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/release-depot/git_wrapper/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/release-depot/git_wrapper/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/release-depot/git_wrapper/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/release-depot/git_wrapper/compare/0.0.1...0.1.0
[0.0.1]: https://github.com/release-depot/git_wrapper/releases/tag/0.0.1
