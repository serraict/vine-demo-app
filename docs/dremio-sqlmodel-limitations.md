# SQLModel and Dremio Flight Limitations

This document outlines the current limitations and challenges when using SQLModel with Dremio Flight SQL, based on our testing and investigation.

## Overview

While SQLModel provides a clean, type-safe way to work with SQL databases in Python, certain features are not fully compatible with Dremio Flight's SQL implementation. The main limitation is around parameter binding, which affects several common query patterns.

## Specific Limitations

### 1. Basic Parameter Binding

Simple equality conditions that would normally use parameter binding fail:

```python
# This natural SQLModel pattern doesn't work:
select(Product).where(Product.name == "some_name")

# Error:
# Cannot convert RexNode to equivalent Dremio expression. 
# RexNode Class: org.apache.calcite.rex.RexDynamicParam
```

### 2. Complex Conditions with LIKE

Combining conditions and using LIKE patterns with parameter binding is not supported:

```python
# This common pattern fails:
select(Product).where(
    and_(
        Product.product_group_name == "group",
        Product.name.contains("search")
    )
)

# Generated SQL that fails:
# WHERE product_group_name = ? AND (name LIKE '%' || ? || '%')
# Error: Illegal use of dynamic parameter
```

### 3. IN Clause Parameters

Using the IN operator with a list of parameters is not supported:

```python
# This common pattern fails:
select(Product).where(Product.id.in_([1, 2, 3]))

# Error:
# Cannot convert RexNode to equivalent Dremio expression
```

### 4. Working Features

Not all SQLModel features are affected. The following works as expected:

- Dynamic sorting with ORDER BY clauses
- Basic column selection
- Table joins (untested but likely to work without parameters)

## Current Workarounds

In the current implementation (`src/vineapp/products/models.py`), we work around these limitations by:

1. Using string interpolation for query conditions
2. Building queries manually when needed
3. Avoiding parameter binding

While these workarounds are functional, they come with drawbacks:

- Less type safety
- Potential SQL injection risks
- More complex and error-prone code
- Loss of SQLModel's clean query interface

## Next Steps

Potential approaches to improve the situation:

1. Investigate if newer versions of Dremio Flight support parameter binding
2. Consider implementing a query builder that converts SQLModel expressions to Dremio-compatible SQL
3. Explore alternative query patterns that avoid parameter binding
4. Consider using a different database interface for complex queries

## References

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Dremio Flight SQL Documentation](https://docs.dremio.com/software/drivers/flight-sql/)
- Test cases demonstrating these limitations: `tests/integration/test_products_ideal.py`
