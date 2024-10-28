# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## \[Unreleased\]

### Added

- Integration tests for Dremio connection and product retrieval
- UI tests for web interface navigation using NiceGUI's testing framework

### Changed

- Restructured product management into dedicated package
- Extracted application metadata into standalone app_info module
- Refactored CLI to use new module structure

## \[0.2\] - 2024-10-25

### Changed

- Connect to Serra Vine's Dremio instance to list products.

## \[0.2.0\] - 2024-03-25

### Added

- CLI application with 'about' command showing package metadata
