# Dremio Parameter Binding Technical Analysis

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

## Flight SQL Specification Findings

The Arrow Flight SQL specification actually includes support for prepared statements and parameter binding:

1. **Prepared Statements**:
   - The protocol supports creating and managing prepared statements
   - Includes commands like `ActionCreatePreparedStatementRequest` and `ActionClosePreparedStatementRequest`
   - Supports bind parameters in prepared statements

2. **Parameter Binding**:
   - The specification acknowledges bind parameters without specific types
   - Example given: `SELECT ?` as a valid parameterized query
   - Suggests using union types or NULL types for handling parameters

3. **Implementation Gap**:
   - While the Flight SQL protocol supports parameters, Dremio's implementation appears to not fully support this feature
   - The error messages suggest Dremio's Calcite SQL parser cannot convert parameterized queries into its internal representation

## Calcite Implementation Details

Looking at Calcite's source code, we found that parameter binding is actually supported through the `RexDynamicParam` class:

1. **Implementation Structure**:
   ```java
   public class RexDynamicParam extends RexVariable {
       private final int index;
       
       @Override 
       public SqlKind getKind() {
           return SqlKind.DYNAMIC_PARAM;
       }
   }
   ```

2. **Core Components**:
   - Extends `RexVariable` for expression handling
   - Uses `SqlKind.DYNAMIC_PARAM` as a specific parameter type
   - Supports visitor pattern for transformations
   - Maintains parameter index for binding

3. **Integration Points**:
   - Parameters are represented as dynamic references in row-expressions
   - Supports type inference for parameters
   - Includes visitor pattern support for query transformations

This implementation in Calcite suggests that the framework itself supports parameter binding, but Dremio's integration with Calcite might not fully implement the parameter binding capabilities.

## Version Analysis

We've tested Dremio versions 24.3, 25.1.0, and 26.0 for parameter binding support:

1. **No Parameter Binding Support Across All Versions**:
   - Parameter binding limitations persist in all tested versions (24.3, 25.1.0, 26.0)
   - Core functionality remains unsupported for Python Flight SQL users
   - Error patterns vary slightly but failures are consistent

2. **Error Message Changes by Version**:

   **Version 24.3:**
   - Basic parameters: "Cannot convert RexNode to equivalent Dremio expression"
   - LIKE patterns: "Illegal use of dynamic parameter"
   - IN clauses: RexDynamicParam errors
   - Dynamic sorting: Works

   **Version 25.1.0:**
   - Basic parameters: NullPointerException
   - LIKE patterns: "Illegal use of dynamic parameter"
   - IN clauses: NullPointerException
   - Dynamic sorting: Works

   **Version 26.0 (Tested 2025-11-21):**
   - Basic parameters: "Cannot convert RexNode to equivalent Dremio expression"
   - LIKE patterns: "Illegal use of dynamic parameter"
   - IN clauses: RexDynamicParam errors
   - Dynamic sorting: Works
   - **Error pattern reverted to v24.3 style**

3. **Version 26.0 Prepared Statements Feature**:
   - **Release notes claim**: "Parameterized prepared statements in Arrow Flight SQL JDBC"
   - **Reality for Python users**: Feature is **JDBC-only**, does NOT work via PyArrow Flight SQL
   - **Test results**: All parameter binding tests still fail with same errors as v24.3
   - **Conclusion**: No improvement for Python/SQLModel users
   - See [testing-v26-results.md](testing-v26-results.md) for detailed analysis

4. **Query Planning & Execution Improvements**:
   - Memory arbiter enabled by default for monitoring key operators (25.0)
   - Improved handling of complex queries and joins
   - Better support for query planning with partition filters
   - Enhanced error handling for concurrent operations
   - Reduced memory usage for query execution

5. **Database Connectivity**:
   - Updates to various database connectors
   - Improved handling of connection pooling
   - Better error handling for connection issues
   - Enhanced support for authentication methods

6. **Implications for Our Use Case**:
   - Parameter binding limitation remains a fundamental design choice
   - Error handling has changed but core limitations persist
   - Memory and performance improvements don't address parameter binding
   - Need to design our solution assuming this limitation will continue
   - Could leverage improved error handling in our workaround

## Root Cause Analysis

Based on our investigation of Flight SQL, Calcite, and version analysis:

1. **Protocol Support**:
   - Flight SQL protocol supports parameters
   - Calcite framework supports dynamic parameters
   - SQLModel/SQLAlchemy correctly generates parameterized queries

2. **Implementation Gap**:
   - Dremio's implementation appears to not fully implement the parameter binding capabilities
   - The error occurs when Dremio tries to convert SQLAlchemy's parameterized query into Calcite's RexDynamicParam
   - This limitation persists through recent versions (24.3 to 25.x)
   - No plans for implementation visible in recent releases

3. **Specific Issues**:
   - Basic parameters fail with "Cannot convert RexNode" error
   - Complex parameters (LIKE, IN) fail with "Illegal use of dynamic parameter"
   - But Calcite itself supports these features through RexDynamicParam
   - Recent versions improve error handling but don't address root cause

4. **Performance Context**:
   - Recent versions include memory management improvements
   - Better handling of complex queries and joins
   - Enhanced support for concurrent operations
   - These improvements might help with alternative query approaches

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

The parameter binding limitation stems from a gap between the Flight SQL protocol specification (which supports parameters) and Dremio's current implementation (which doesn't fully support this feature). Any solution will need to either:

1. Wait for Dremio to implement full parameter binding support as specified in the Flight SQL protocol
2. Implement parameter substitution before queries reach Dremio's Calcite parser
3. Use alternative query patterns that avoid parameter binding

## References

- [Apache Arrow Flight SQL Specification](https://arrow.apache.org/docs/format/FlightSql.html)
- [Apache Calcite Documentation](https://calcite.apache.org/docs/)
- [Dremio Flight SQL Documentation](https://docs.dremio.com/software/drivers/flight-sql/)
- [SQLAlchemy Parameter Binding](https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql)
- Our test cases: `tests/integration/test_products_ideal.py`
