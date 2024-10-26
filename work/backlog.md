# Backlog

## Doing

### Connect to Dremio

1. Setup Dremio connection
   * [x] Add sqlalchemy-dremio dependency
   * [x] Create configuration module for Dremio settings
   * [x] Add connection string handling

2. Update Product Repository
   * [x] Add connection configuration
   * [x] Update repository to handle both SQLite and Dremio connections
   * [ ] Add error handling for connection issues

3. Integration Tests
   * [x] Setup test configuration for Dremio credentials
   * [x] Add integration tests for Dremio connection
   * [x] Add tests for error cases
   * [x] Add test for retrieving products

## Next

### Goal: Connect to Serra Vine

* [x] Setup local dataset by exporting parquet files and importing to local Serra Vine instance
* [x] Introduce typer
  * [x] about command that displays an information box and the current version number
* [x] Setup tests
  * [x] We can run the cli app
  * [x] Display version number
* [x] Display a table with all products.
  * [x] list them on the command line
  * [x] Add CLI command documentation
* [ ] Display a public chart.

## Later
