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

### Running Parameter Binding Tests

The `test_products_ideal.py` file contains tests that demonstrate how we'd like to use SQLModel with Dremio:

```bash
# Run the parameter binding tests
INCLUDE_DREMIO_LIMITATIONS_TESTS=1 pytest tests/integration/test_products_ideal.py -v
```

### Test Cases

The tests verify different parameter binding scenarios:

1. Basic Parameter Binding:
   ```python
   select(Product).where(Product.name == "value")
   ```

2. Complex Conditions:
   ```python
   and_(
       Product.name.contains("value"),
       Product.id > 5
   )
   ```

3. IN Clauses:
   ```python
   Product.id.in_([1, 2, 3])
   ```

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
