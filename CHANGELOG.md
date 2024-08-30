# Changelog

## [0.4.4] - 2024-08-30

### Added

- [Improve build.sh to use version number as an argument.](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/ae4b83dfa8b21ea3d449b87d61a7f0d13bd67d43)

### Fixed

- [Fix Android Studio download link not being correctly created.](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/1263403fb693e55d40c62fc5c3aa9f04abac40b2)
- [Fix application menu shortcuts.](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/ae4b83dfa8b21ea3d449b87d61a7f0d13bd67d43)

## [0.4.3] - 2024-07-04

### Fixed

- [Update CVE-2024-39689 vulnerability](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/44da7c8c0218280c6791ec3c956f2b3d6d1395b9)

## [0.4.2] - 2024-06-26

### Fixed

- [Update CVE-2024-37891 vulnerability](https://github.com/diogocaveiro/jetbrains-manager-tool/tree/4cf01388334614f7a8a3c081b65cebc1195ac43e)
- [Update CVE-2024-35195 vulnerability](https://github.com/diogocaveiro/jetbrains-manager-tool/tree/cb44273e300d0cc25afd9b5bed5e75e3d3a04575)
- [Update CVE-2024-3651 vulnerability](https://github.com/diogocaveiro/jetbrains-manager-tool/tree/abb2fcb6a83026e3bb0ceaeadabb3b696dd06b5d)

## [0.4.1] - 2024-02-16

### Added

- [Application install/removal logging](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/d036b0af5f8134c300999922ba123952c7ed0bca).
- [Build script also changes project's version in pyproject.toml](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/12e3dee910e3c2c907c37e710b2439919b192745).
- [Message alerting the script finished running](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/dad0f78974a37a37f491539125d717717ce31aa9).

### Changed

- [Rename help_docs.md to help_pages.md](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/d036b0af5f8134c300999922ba123952c7ed0bca).

### Fixed

- [Confirmation message now supports both update and install](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/6d7de437735c41c56d11e6ad15154c9790572309).
- [Build.sh was replacing version in pyproject.toml incorrectly](https://github.com/diogocaveiro/jetbrains-manager-tool/tree/2442ca2e45acf5d2096967b8920c1d8df653cf4d).

## [0.4.0] - 2023-12-07

### Added

- [Build script to automate the build process](https://github.com/diogocaveiro/jetbrains-manager-tool/tree/12e3dee910e3c2c907c37e710b2439919b192745).
- [Custom path configuration flag](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/417198f737bf4c86740ae9b7ba114e7dc0d530d5).

### Changed

- [Improve error handling](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/4c4560b21bd97755895aa6523f46cd568ae1d6d6).

## [0.3.0] - 2023-12-03

### Added

- [List installed apps configuration flag](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/2eaa42470a07c96134a006bc3409edec373520d9).
- [Help flag to show documentation in the terminal](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/9ed7f2ec968fdf1860df954bb498d4a744e4eee7).
- [Application logging](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/de93d6584cab6432457fcbbe890dcc99b61d8f79).

### Fixed

- [Verbose mode not working as intended](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/8f27b71dc44c456afce62292cd1bb2bfc552d2d2).

## [0.2.0] - 2023-11-28

### Added

- [Verbosity configuration flag](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/afb8942ef80384b977fbf9b0ed37f2185dc5027d).
- [Arch Linux packaging](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/508e23dc776ad7e97065c74472ec69675f40996d).

### Changed

- [Update mimetypes flag](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/afb8942ef80384b977fbf9b0ed37f2185dc5027d).

### Fixed

- [Issue trying to locate app_data.json file](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/22f3916dd6782352eec6564c36f520e33e4dce12).
- [Issue trying to locate the symlink path](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/22f3916dd6782352eec6564c36f520e33e4dce12).
