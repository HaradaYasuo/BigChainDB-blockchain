# Our Release Process

The release process for BigchainDB server differs slightly depending on whether it's a minor or a patch release.

BigchainDB follows [semantic versioning](http://semver.org/) (i.e. MAJOR.MINOR.PATCH), taking into account
that [major version 0.x does not export a stable API](http://semver.org/#spec-item-4).

## Minor release

A minor release is preceeded by a feature freeze and created from the 'master' branch. This is a summary of the steps we go through to release a new minor version of BigchainDB Server.

1. Update the `CHANGELOG.md` file in master
1. Create and checkout a new branch for the release, named after the minor version, without a preceeding 'v', e.g. `git checkout -b 0.9`
1. In `bigchaindb/version.py`, update `__version__` and `__short_version__`, e.g. to `0.9` and `0.9.0` (with no `.dev` on the end)
1. Commit changes and push new branch to Github
1. Follow steps outlined in [Common Steps](#common-steps)
1. In 'master' branch, Edit `bigchaindb/version.py`, increment the minor version to the next planned release, e.g. `0.10.0.dev'.
This is so people reading the latest docs will know that they're for the latest (master branch)
version of BigchainDB Server, not the docs at the time of the most recent release (which are also
available).

Congratulations, you have released BigchainDB!

## Patch release

A patch release is similar to a minor release, but piggybacks on an existing minor release branch:

1. Check out the minor release branch
1. Apply the changes you want, ie using `git cherry-pick`.
1. Update the `CHANGELOG.md` file
1. Increment the patch version in `bigchaindb/version.py`, e.g. "0.9.1"
1. Follow steps outlined in [Common Steps](#common-steps)

## Common steps

These steps are common between minor and patch releases:

1. Go to the [bigchaindb/bigchaindb Releases page on GitHub](https://github.com/bigchaindb/bigchaindb/releases)
   and click the "Draft a new release" button
1. Fill in the details:
   - Tag version: version number preceeded by 'v', e.g. "v0.9.1"
   - Target: the release branch that was just pushed
   - Title: Same as tag name
   - Description: The body of the changelog entry (Added, Changed etc)
1. Publish the release on Github
1. Generate the release tarball with `python setup.py sdist`. Upload the release to Pypi.
1. Login to readthedocs.org as a maintainer of the BigchainDB Server docs.
   Go to Admin --> Versions and under **Choose Active Versions**, make sure that the new version's tag is
   "Active" and "Public", and make sure the new version's branch
   (without the 'v' in front) is _not_ active
1. Also in readthedocs.org, go to Admin --> Advanced Settings
   and make sure that "Default branch:" (i.e. what "latest" points to)
   is set to the new release's tag, e.g. `v0.9.1`. (Don't miss the 'v' in front.)
