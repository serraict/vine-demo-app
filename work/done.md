# Done

## Connect to Serra Vine

* Setup local dataset by exporting parquet files and importing to local Serra Vine instance
* Introduce typer
  * about command that displays an information box and the current version number
* Setup tests
  * We can run the cli app
  * Display version number
* Display a table with all products
  * list them on the command line
  * Add CLI command documentation

## Connect to Dremio

1. Setup Dremio connection
   * Add sqlalchemy-dremio dependency
   * Create configuration module for Dremio settings
   * Add connection string handling

2. Update Product Repository
   * Add connection configuration
   * Update repository to handle both SQLite and Dremio connections

3. Integration Tests
   * Setup test configuration for Dremio credentials
   * Add integration tests for Dremio connection
   * Add tests for error cases
   * Add test for retrieving products
