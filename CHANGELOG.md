# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Product detail view showing detailed information for individual products
- Clickable product names in table linking to detail view
- Integration tests for Dremio connection and product retrieval
- UI tests for web interface navigation using NiceGUI's testing framework
- About page showing application information and links to documentation
- Navigation link to About page from homepage
- Sorting functionality for products table (by name and product group)
- Server-side pagination for products table with configurable page size
- Reusable model_card component for displaying Pydantic models in a consistent format

### Changed

- Enhanced products table to include ID column
- Restructured product management into dedicated package
- Extracted application metadata into standalone app_info module
- Refactored CLI to use new module structure
- Enhanced product repository to support paginated queries
- Removed ProductService class in favor of using ProductRepository directly
- Improved UI layout with consistent navigation card-based design across all pages
- Converted ApplicationInfo to Pydantic model for consistent model handling
- Unified model display approach using shared model_card component across pages

## [0.2] - 2024-10-25

### Changed

- Connect to Serra Vine's Dremio instance to list products.

## [0.2.0] - 2024-03-25

### Added

- CLI application with 'about' command showing package metadata
