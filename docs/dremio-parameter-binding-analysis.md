# Dremio Parameter Binding Technical Analysis

This document analyzes where and why parameter binding fails when using SQLModel with Dremio Flight SQL, based on error stack traces and implementation details.

## Error Flow Analysis

The parameter binding failure can be traced through several layers:

### 1. SQLModel/SQLAlchemy Layer
```python
sqlmodel/orm/session.py -> sqlalchemy/orm/session.py -> sqlalchemy/orm/context.py
```

At this level, SQLModel (through SQLAlchemy) generates a parameterized query with placeholders (?). This is standard SQL parameter binding behavior that works with most databases.

### 2. Dremio SQLAlchemy Dialect Layer
```python
sqlalchemy_dremio/db.py -> sqlalchemy_dremio/query.py
```

The dialect attempts to convert the SQLAlchemy query structure to Dremio Flight SQL. This includes translating the parameter placeholders.

### 3. PyArrow Flight SQL Layer
```python
pyarrow/_flight.pyx -> pyarrow/error.pxi
```

The final layer where the query is sent to Dremio's server and where the errors surface.

## Error Types

We observe two distinct types of parameter binding errors:

### 1. Simple Parameter Binding
```
pyarrow._flight.FlightInternalError: Cannot convert RexNode to equivalent Dremio expression. 
RexNode Class: org.apache.calcite.rex.RexDynamicParam
```

This error occurs with basic parameter binding (e.g., `WHERE column = ?`). The reference to "RexNode" and "Calcite" indicates that Dremio's SQL parser (which uses Apache Calcite) cannot handle dynamic parameters.

### 2. Complex Parameter Binding (LIKE Patterns)
```
pyarrow.lib.ArrowInvalid: Flight returned invalid argument error with message: 
Illegal use of dynamic parameter
```

Generated SQL showing where it fails:
```sql
WHERE "Vines".products.product_group_name = ? 
  AND ("Vines".products.name LIKE '%' || ? || '%')
```

This error occurs with more complex parameter usage, particularly when combining parameters with SQL functions or operators.

## Root Cause

The core issue lies in Dremio's Flight SQL implementation, which uses Apache Calcite for SQL parsing. The error messages suggest that:

1. Dremio's Calcite-based SQL parser doesn't support dynamic parameter binding
2. The limitation exists at the server side, not in the Python client libraries
3. The issue affects both simple and complex parameter usage

## Technical Implications

This analysis has several implications for potential solutions:

### Server-Side Fix
Would require:
- Enhancing Dremio's Flight SQL implementation
- Adding parameter binding support to Dremio's Calcite SQL parser
- Server-side changes to handle parameter substitution

### Client-Side Workaround
Would require:
- Converting parameterized queries to literal SQL before PyArrow
- Implementing parameter substitution in the SQLAlchemy dialect
- Careful handling of SQL injection risks

## Impact on Query Types

Different query patterns are affected differently:

1. **Simple Equality**
   ```python
   Product.name == "value"  # Fails
   ```

2. **Complex Conditions**
   ```python
   and_(
       Product.name.contains("value"),  # Fails
       Product.id > 5  # Fails
   )
   ```

3. **IN Clauses**
   ```python
   Product.id.in_([1, 2, 3])  # Fails
   ```

4. **Sorting**
   ```python
   order_by(Product.name)  # Works
   ```

## Conclusion

The parameter binding limitation is fundamental to Dremio's current Flight SQL implementation. Any solution will need to either:

1. Wait for Dremio to add parameter binding support (server-side fix)
2. Implement parameter substitution before queries reach Dremio (client-side workaround)
3. Use alternative query patterns that avoid parameter binding

This understanding helps inform the solution approaches detailed in `dremio-sqlmodel-solutions.md`.

## References

- [Apache Calcite Documentation](https://calcite.apache.org/docs/)
- [Dremio Flight SQL Documentation](https://docs.dremio.com/software/drivers/flight-sql/)
- [SQLAlchemy Parameter Binding](https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql)
- Our test cases: `tests/integration/test_products_ideal.py`
