# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [v2025.3.24] - 2025-03-24

[v2025.3.24]: https://github.com/miarec/miarec_s3fs/compare/v2025.3.23...v2025.3.24

### Changed

- Do not check a presense of parent directory when opening files in non-strict mode
    As directories in S3 are a virtual concept, they may not exist as individual objects.

## [v2025.3.23] - 2025-03-23

[v2025.3.23]: https://github.com/miarec/miarec_s3fs/compare/v2024.1.1...v2025.3.23

### Changed

- Improve scandir() behavior when strict mode is disabled.
    No need to create empty object for directories.


## [v2024.1.1] - 2024-01-15

[v2024.1.1]: https://github.com/miarec/miarec_s3fs/compare/v2024.1.0...v2024.1.1    

### Changed

- Add unit tests with using Moto mock library
- Update code to be compatible with the latest PyFilesystems2 version (2.4)
- Add `config_arg` parameter to `S3FS` constructor. Can be used to customize S3 client behavior as documented in [botocore.config](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html)
- Fix race condition when `S3FS` is accessed from multiple theads.
- Pass `upload_args` to `copy()` method (required when server-side encryption is enforced)
- Fix bug with incomplete upload to S3 when the file object is destroyed by garbage collector without calling `close()` method
- Convert boto-specific exceptions to `FSError` when error is encountered in `remove()` method

## [v2024.1.0] - 2024-01-06

[v2024.1.1]: https://github.com/miarec/miarec_s3fs/compare/v1.1.1...v2024.1.0    

- Forked from [fs-s3fs](https://github.com/PyFilesystem/s3fs) version 1.1.1 (released on 2019-08-14)
- Rename package to `miarec_sftp` and re-organize files

## [v1.1.1] - 2019-08-14

The latest release of the original (forked) [fs-s3fs](https://github.com/PyFilesystem/s3fs) repo
