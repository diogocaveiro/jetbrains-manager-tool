# Changelog

All notable changes to this project will be documented in this file.

## [0.4.1] - 2024-02-16

### Added

- Application install/removal logging (commit [d036b0a](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/d036b0af5f8134c300999922ba123952c7ed0bca)).
- Build script also changes project's version in pyproject.toml (commit [12e3dee](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/12e3dee910e3c2c907c37e710b2439919b192745)).
- Message alerting the script finished running (commit [dad0f78](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/dad0f78974a37a37f491539125d717717ce31aa9)).

### Changed

- Rename help_docs.md to help_pages.md (commit [d036b0a](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/d036b0af5f8134c300999922ba123952c7ed0bca)).

### Fixed

- Confirmation message now supports both update and install (commit [6d7de43](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/6d7de437735c41c56d11e6ad15154c9790572309)).
- Build.sh was replacing version in pyproject.toml incorrectly.

## [0.4.0] - 2023-12-07

### Added

- Build script to automate the build process (commit [12e2695](https://github.com/diogocaveiro/jetbrains-manager-tool/tree/12e3dee910e3c2c907c37e710b2439919b192745)).
- Custom path configuration flag (commit [417198f](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/417198f737bf4c86740ae9b7ba114e7dc0d530d5)).

### Changed

- Improve error handling (commit [4c4560b](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/4c4560b21bd97755895aa6523f46cd568ae1d6d6)).

## [0.3.0] - 2023-12-03

### Added

- List installed apps configuration flag (commit [2eaa424](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/2eaa42470a07c96134a006bc3409edec373520d9)).
- Help flag to show documentation in the terminal (commit [9ed7f2e](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/9ed7f2ec968fdf1860df954bb498d4a744e4eee7)).
- Application logging (commit [de93d65](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/de93d6584cab6432457fcbbe890dcc99b61d8f79)).

### Fixed

- Verbose mode not working as intended (commit [8f27b71](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/8f27b71dc44c456afce62292cd1bb2bfc552d2d2)).

## [0.2.0] - 2023-11-28

### Added

- Verbosity configuration flag (commit [afb8942](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/afb8942ef80384b977fbf9b0ed37f2185dc5027d)).
- Arch Linux packaging (commit [508e23d](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/508e23dc776ad7e97065c74472ec69675f40996d)).

### Changed

- Update mimetypes flag (commit [afb8942](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/afb8942ef80384b977fbf9b0ed37f2185dc5027d)).

### Fixed

- Issue trying to locate app_data.json file (commit [22f3916](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/22f3916dd6782352eec6564c36f520e33e4dce12)).
- Issue trying to locate the symlink path (commit [22f3916](https://github.com/diogocaveiro/jetbrains-manager-tool/commit/22f3916dd6782352eec6564c36f520e33e4dce12)).
