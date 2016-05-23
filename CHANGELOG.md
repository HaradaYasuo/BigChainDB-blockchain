# Change Log (Release Notes)
All _notable_ changes to this project will be documented in this file (`CHANGELOG.md`).
This project adheres to [Semantic Versioning](http://semver.org/) (or at least we try).
Contributors to this file, please follow the guidelines on [keepachangelog.com](http://keepachangelog.com/).
Note that each version (or "release") is the name of a [Git _tag_](https://git-scm.com/book/en/v2/Git-Basics-Tagging) of a particular commit, so the associated date and time are the date and time of that commit (as reported by GitHub), _not_ the "Uploaded on" date listed on PyPI (which may differ).
For reference, the possible headings are:

* **Added** for new features.
* **Changed** for changes in existing functionality.
* **Deprecated** for once-stable features removed in upcoming releases.
* **Removed** for deprecated features removed in this release.
* **Fixed** for any bug fixes.
* **Security** to invite users to upgrade in case of vulnerabilities.
* **External Contributors** to list contributors outside of ascribe GmbH.
* **Notes**


## [Unreleased] - YYYY-MM-DD
Tag name: 
= commit: 
committed: 

### Added
- Caching of calls to `load_consensus_plugin()`, using [`@lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache). This speeds up the instantiation of `Bigchain` objects and greatly improves overall performance. [Pull Request #271](https://github.com/bigchaindb/bigchaindb/pull/271)
- New `Dockerfile-dev` Docker file to make it easier for developers to _develop_ BigchainDB with Docker. One can run all unit tests with Docker again. [Pull Request #313](https://github.com/bigchaindb/bigchaindb/pull/313)
- Transactions in invalid blocks are copied to the backlog: [Pull Request #221](https://github.com/bigchaindb/bigchaindb/pull/221).
- New `bigchaindb` command to set the number of RethinkDB shards (in both tables): [Pull Request #258](https://github.com/bigchaindb/bigchaindb/pull/258)
- Better handling of an outdated `setuptools`: [Pull Request #279](https://github.com/bigchaindb/bigchaindb/pull/279)

### Changed
- The block processes now use GroupProcess: [Pull Request #267](https://github.com/bigchaindb/bigchaindb/pull/267)
- Replaced the `json` Python package with `rapidjson` (a Python wrapper for a fast JSON parser/generator written in C++), to speed up JSON serialization and deserialization: [Pull Request #318](https://github.com/bigchaindb/bigchaindb/pull/318)
- Overhauled `ROADMAP.md` and moved it to [the bigchaindb/org repository](https://github.com/bigchaindb/org): Pull Requests 
[#282](https://github.com/bigchaindb/bigchaindb/pull/282),
[#306](https://github.com/bigchaindb/bigchaindb/pull/306),
[#308](https://github.com/bigchaindb/bigchaindb/pull/308),
[#325](https://github.com/bigchaindb/bigchaindb/pull/325)
- AWS deployment has better support for [New Relic Server Monitoring](https://newrelic.com/server-monitoring): [Pull Request #316](https://github.com/bigchaindb/bigchaindb/pull/316)
- AWS deployment script now reads from a configuration file: [Pull Request #291](https://github.com/bigchaindb/bigchaindb/pull/291)
- AWS deployment script doesn't auto-start the BigchainDB servers anymore: [Pull Request #257](https://github.com/bigchaindb/bigchaindb/pull/257)

### Fixed
- Bug related to transaction malleability: [Pull Request #281](https://github.com/bigchaindb/bigchaindb/pull/281)

### Notes
You can now see a big-picture view of all BigchainDB repositories on [a waffle.io board](https://waffle.io/bigchaindb/org).


## [0.3.0] - 2016-05-03
Tag name: v0.3.0
= commit: a97c54e82be954a1411e5bfe0f09a9c631309f1e
committed: May 3, 2016, 11:52 AM GMT+2

### Added
- Crypto-conditions specs according to the Interledger protocol: [Pull Request #174](https://github.com/bigchaindb/bigchaindb/pull/174)
- Added support for anonymous hashlocked conditions and fulfillments: [Pull Request #211](https://github.com/bigchaindb/bigchaindb/pull/211)

### Changed
- Several improvements to the AWS deployment scripts: [Pull Request #227](https://github.com/bigchaindb/bigchaindb/pull/227)

### Fixed
- Bug related to block validation: [Pull Request #233](https://github.com/bigchaindb/bigchaindb/pull/233)

### Notes
This release completely refactored the structure of the transactions and broke compatibility with older versions
of BigchainDB. The refactor of the transactions was made in order to add support for multiple inputs/outputs and
the crypto-conditions specs from the Interledger protocol.

We also updated the RethinkDB Python drivers so you need to upgrade to RethinkDB v2.3+


## [0.2.0] - 2016-04-26
Tag name: v0.2.0
= commit: 0c4a2b380aabdcf50fa2d7fb351c290aaedc3db7
committed: April 26, 2016, 11:09 AM GMT+2

### Added
- Ability to use environment variables to set (or partially set) configuration settings: [Pull Request #153](https://github.com/bigchaindb/bigchaindb/pull/153)
- `bigchaindb --export-my-pubkey`: [Pull Request #186](https://github.com/bigchaindb/bigchaindb/pull/186)
- `bigchaindb --version`, and one central source for the current version (`version.py`): [Pull Request #208](https://github.com/bigchaindb/bigchaindb/pull/208)
- AWS deployment scripts: Pull Requests 
[#160](https://github.com/bigchaindb/bigchaindb/pull/160),
[#166](https://github.com/bigchaindb/bigchaindb/pull/166),
[#172](https://github.com/bigchaindb/bigchaindb/pull/172),
[#203](https://github.com/bigchaindb/bigchaindb/pull/203)
- `codecov.yml`: [Pull Request #161](https://github.com/bigchaindb/bigchaindb/pull/161)
- `CHANGELOG.md` (this file): [Pull Request #117](https://github.com/bigchaindb/bigchaindb/pull/117)
- Signatures using Ed25519: Pull Requests 
[#138](https://github.com/bigchaindb/bigchaindb/pull/138),
[#152](https://github.com/bigchaindb/bigchaindb/pull/152)
- Multisig support: [Pull Request #107](https://github.com/bigchaindb/bigchaindb/pull/107)
- HTTP Server & Web API: Pull Requests 
[#102](https://github.com/bigchaindb/bigchaindb/pull/102),
[#150](https://github.com/bigchaindb/bigchaindb/pull/150),
[#155](https://github.com/bigchaindb/bigchaindb/pull/155),
[#183](https://github.com/bigchaindb/bigchaindb/pull/183)
- Python driver/SDK/API: [Pull Request #102](https://github.com/bigchaindb/bigchaindb/pull/102)
- Python Style Guide: [Pull Request #89](https://github.com/bigchaindb/bigchaindb/pull/89)
- Monitoring & dashboard tools: Pull Requests
[#72](https://github.com/bigchaindb/bigchaindb/pull/72),
[#181](https://github.com/bigchaindb/bigchaindb/pull/181)

### Changed
- Rewrote [`README.md`](README.md) into four sets of links: Pull Requests [#80](https://github.com/bigchaindb/bigchaindb/pull/80) and [#115](https://github.com/bigchaindb/bigchaindb/pull/115)

### Fixed
- Bug related to config overwrite: [Pull Request #97](https://github.com/bigchaindb/bigchaindb/pull/97)
- Bug related to running the `bigchaindb-benchmark load` on docker [Pull Request #225](https://github.com/bigchaindb/bigchaindb/pull/225)

## External Contributors
- [@thedoctor](https://github.com/thedoctor): Pull Requests 
[#99](https://github.com/bigchaindb/bigchaindb/pull/99),
[#136](https://github.com/bigchaindb/bigchaindb/pull/136)
- [@roderik](https://github.com/roderik): [Pull Request #162](https://github.com/bigchaindb/bigchaindb/pull/162)


## [0.1.5] - 2016-04-20
Tag name: v0.1.5
= commit: 9f62cddbaf44167692cfee71db707bce93e3395f
committed: April 20, 2016, 3:31 PM GMT+2

### Fixed
- [Issue #71](https://github.com/bigchaindb/bigchaindb/issues/71) (Voter is not validating blocks correctly when checking for double spends) in [Pull Request #76](https://github.com/bigchaindb/bigchaindb/pull/76)


## [0.1.4] - 2016-02-22
Tag name: v0.1.4 
= commit: c4c850f480bc9ae72df2a54f81c0825b6fb4ed62 
committed: Feb 22, 2016, 11:51 AM GMT+1

### Added
- Added to `classifiers` to setup.py

### Changed
- Allow running pytest tests in parallel (using [xdist](http://pytest.org/latest/xdist.html)): [Pull Request #65](https://github.com/bigchaindb/bigchaindb/pull/65)
- Allow non-interactive first start: [Pull Request #64](https://github.com/bigchaindb/bigchaindb/pull/64) to resolve [Issue #58](https://github.com/bigchaindb/bigchaindb/issues/58)


## [0.1.3] - 2016-02-16
Tag name: v0.1.3
= commit 8926e3216c1ee39b9bc332e5ef1df2a8901262dd
committed Feb 16, 2016, 11:37 AM GMT+1

### Changed
- Changed from using Git Flow to GitHub flow (but with `develop` as the default branch).


## [0.1.2] - 2016-02-15
Tag name: v0.1.2 
= commit d2ff24166d69dda68dd7b4a24a88279b1d37e222 
committed Feb 15, 2016, 2:23 PM GMT+1

### Added
- Various tests

### Fixed
- Fix exception when running `start`: [Pull Request #32](https://github.com/bigchaindb/bigchaindb/pull/32) resolved [Issue #35]

## [0.1.1] - 2016-02-15
Tag name: v0.1.1 
= commit 2a025448b29fe7056760de1039c73bbcfe992461 
committed Feb 15, 2016, 10:48 AM GMT+1

### Added
- "release 0.1.1": [Pull Request #37](https://github.com/bigchaindb/bigchaindb/pull/37)

### Removed
- `tox.ini` [Pull Request #18](https://github.com/bigchaindb/bigchaindb/pull/18)
- `requirements.txt` in the root directory, and the entire `requirements/` directory: [Pull Request #14](https://github.com/bigchaindb/bigchaindb/pull/14)

### Fixed
- Hotfix for AttributeError, fixed [Issue #27](https://github.com/bigchaindb/bigchaindb/issues/27)


## [0.1.0] - 2016-02-10
Tag name: v0.1.0
= commit 8539e8dc2d036a4e0a866a3fb9e55889503254d5
committed Feb 10, 2016, 10:04 PM GMT+1

The first public release of BigchainDB, including:

- Initial BigchainDB Server code, including many tests and some code for benchmarking.
- Initial documentation (in `bigchaindb/docs`).
- Initial `README.md`, `ROADMAP.md`, `CODE_OF_CONDUCT.md`, and `CONTRIBUTING.md`.
- Packaging for PyPI, including `setup.py` and `setup.cfg`.
- Initial `Dockerfile` and `docker-compose.yml` (for deployment using Docker and Docker Compose).
- Initial `.gitignore` (list of things for git to ignore).
- Initial `.travis.yml` (used by Travis CI).
