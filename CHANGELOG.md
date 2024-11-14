# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3] - 2024-11-14

### Added

- GraphQL client for Fibery API integration with token-based authentication
- Knowledge base page showing Fibery environment information and database links
- Database detail pages showing schema information and example entities
- FiberyEntity model for consistent entity representation
- Navigation link to Knowledge Base from homepage
- Computed URL fields in FiberyInfo model for KB API and GraphQL endpoints
- Enhanced model_card component to display computed fields as clickable links
- Product detail view showing detailed information for individual products
- Clickable product names in table linking to detail view
- Integration tests for Dremio connection and product retrieval
- Reusable model_card component for displaying Pydantic models in a consistent format
- Support for both singular and plural GraphQL field names (e.g., findAction vs findLearnings)
- Proper handling of RichField descriptions in database entities
- Error handling for GraphQL queries with informative error messages
- Support for overriding Fibery space name without modifying environment variables
- Docker container support with cron job capabilities
- GitHub Actions workflow for continuous integration and testing
- GitHub Actions workflow for building and publishing Docker images
- Code coverage reporting to Codecov

### Changed

- Improved UI layout with consistent navigation card-based design across all pages
- Converted ApplicationInfo to Pydantic model for consistent model handling
- Unified model display approach using shared model_card component across pages
- Enhanced ApplicationInfo model with proper URL type validation
- Improved FiberyField model to better match GraphQL schema behavior
- Refactored Fibery models to use configured space_name consistently instead of hardcoding "Public"
- Updated FiberyDatabase to require space_name parameter for explicit space handling
- Enhanced get_fibery_info to support optional space name override
- Improved GraphQL client to handle space name overrides
- Fixed case sensitivity handling in database type filtering
- Removed hardcoded database list from FiberyInfo model in favor of dynamic GraphQL schema queries
- Separated Docker Compose configurations for development and production

### Deprecated

### Removed

### Fixed

### Security

## [0.2] - 2024-10-25

### Changed

- Connect to Serra Vine's Dremio instance to list products.

## [0.2.0] - 2024-03-25

### Added
