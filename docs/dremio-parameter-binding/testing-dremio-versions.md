# Testing Dremio Parameter Binding with Different Versions

This document describes how to test SQLModel parameter binding behavior with different versions of Dremio.

## Current Setup

We're currently using Dremio version 24.3 in production, where we've identified limitations with parameter binding (see `dremio-parameter-binding-analysis.md`).

## Testing with Dremio 25.1.0

A Docker Compose configuration is provided to test with Dremio 25.1.0:

```bash
# Start Dremio
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Initial Setup

1. Wait for Dremio to start (check http://localhost:9047)
2. Create initial admin user
3. Configure your environment:
   ```bash
   export VINEAPP_DB_CONNECTION="dremio+flight://user:password@localhost:32010/dremio"
   ```

### Loading Test Data

1. In the Dremio UI (http://localhost:9047):
   - Click "Add Data Lake"
   - Choose "File System (File)"
   - Name it "test_data"
   - Set path to `/opt/dremio/data/test_data`
   - The test data is automatically mapped into this location

2. Create the Products table:
   - Navigate to test_data source
   - Select products.csv
   - Click "Format as Table"
   - Set table name to "Products"
   - Under "Format Settings":
     - Format: CSV
     - Extract Header Row: Yes
     - Field Delimiter: Comma
   - Click "Save"
   - In the SQL Editor, run:
     ```sql
     ALTER TABLE test_data.Products 
     SET SCHEMA 'Vines';
     ```

3. Verify the data:
   ```sql
   SELECT * FROM Vines.Products 
   ORDER BY id;
   ```
   You should see 20 products across 4 product groups.

### Running Parameter Binding Tests

The `test_products_ideal.py` file contains tests that demonstrate how we'd like to use SQLModel with Dremio:

```bash
# Run the parameter binding tests
INCLUDE_DREMIO_LIMITATIONS_TESTS=1 pytest tests/integration/test_products_ideal.py -v
```

### Test Cases

The tests verify different parameter binding scenarios using our test data:

1. Basic Parameter Binding:
   ```python
   select(Product).where(Product.name == "T. Bee 13")  # Should find product ID 1
   ```

2. Complex Conditions:
   ```python
   and_(
       Product.product_group_name == "13 aziaat",  # Should find 5 products
       Product.name.contains("13")                 # Should find product ID 1
   )
   ```

3. IN Clauses:
   ```python
   Product.id.in_([1, 2, 3])  # Should find first three T. Bee products
   ```

### Test Data Structure

The test data (`data/products.csv`) contains:
- 20 products across 4 product groups
- Groups:
  1. 13 aziaat (T. Bee series, IDs 1-5)
  2. 21 europees (H. Bee series, IDs 6-10)
  3. 31 afrikaans (B. Bee series, IDs 11-15)
  4. 41 amerikaans (M. Bee series, IDs 16-20)
- Consistent naming patterns for testing different query types

### Cleanup

```bash
# Stop Dremio
docker-compose down

# Remove volumes (optional)
docker-compose down -v
```

## Testing Other Versions

To test with a different Dremio version:

1. Update the image tag in `docker-compose.yml`:
   ```yaml
   image: dremio/dremio-oss:YOUR_VERSION
   ```

2. Rebuild and restart:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Version History

| Version | Parameter Binding Status | Notes |
|---------|-------------------------|-------|
| 24.3    | Not supported          | Current production version |
| 25.1.0  | Testing in progress    | Latest version we're testing |

## References

- [Dremio Parameter Binding Analysis](dremio-parameter-binding-analysis.md)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Dremio Release Notes](https://docs.dremio.com/software/release-notes/)
