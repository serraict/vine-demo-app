# SQLModel and Dremio Flight SQL Parameter Binding

This documentation covers our investigation into parameter binding limitations when using SQLModel with Dremio Flight SQL.

## Overview

We've identified and documented limitations in parameter binding support when using SQLModel with Dremio Flight SQL. This documentation set provides a comprehensive analysis of the issue and potential solutions.

## Documentation Structure

### 1. [Parameter Binding Analysis](parameter-binding-analysis.md)
Technical deep-dive into the parameter binding issue:
- Error flow analysis through all layers
- Detailed error types and messages
- Flight SQL specification findings
- Calcite implementation details
- Version comparison (24.3 vs 25.1.0)

### 2. [SQLModel Limitations](sqlmodel-limitations.md)
Current limitations and their impact:
- What doesn't work (parameter binding scenarios)
- What works (alternative approaches)
- Impact on common query patterns
- Examples of affected code

### 3. [Potential Solutions](sqlmodel-solutions.md)
Exploration of possible solutions:
- Client-side parameter substitution
- Custom SQLAlchemy dialect
- Alternative query patterns
- Pros and cons of each approach

### 4. [Version Testing Guide](testing-dremio-versions.md)
How to test different Dremio versions:
- Docker setup instructions
- Test data and configuration
- Running test cases
- Comparing results between versions

## Quick Links

- [Test Cases](../../tests/integration/test_products_ideal.py) - Example tests showing ideal SQLModel usage
- [Product Model](../../src/vineapp/products/models.py) - Current implementation with workarounds
- [Docker Setup](../../docker-compose.yml) - Test environment configuration

## Contributing

When adding to this documentation:
1. Technical details go in parameter-binding-analysis.md
2. New limitations should be documented in sqlmodel-limitations.md
3. Solution approaches belong in sqlmodel-solutions.md
4. Testing procedures go in testing-dremio-versions.md

## References

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Dremio Flight SQL Documentation](https://docs.dremio.com/software/drivers/flight-sql/)
- [Apache Arrow Flight SQL Specification](https://arrow.apache.org/docs/format/FlightSql.html)
- [Apache Calcite Documentation](https://calcite.apache.org/docs/)
