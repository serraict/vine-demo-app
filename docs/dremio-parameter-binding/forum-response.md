# Response to "Is parameterized SQL not supported by Dremio?"

Following up on this thread about parameter binding support in Dremio. We've been specifically working with SQLModel (built on SQLAlchemy) and have done some detailed testing across Dremio versions 24.3 and 25.1.0. Here are our findings that might help others:

## Version Comparison (24.3 vs 25.1.0)

We've observed some interesting changes in how parameter binding errors are reported:

1. Basic parameter binding:
```python
select(Product).where(Product.name == "value")
# In 24.3:
# Error: Cannot convert RexNode to equivalent Dremio expression. 
# RexNode Class: org.apache.calcite.rex.RexDynamicParam
# In 25.1.0:
# Error: Flight returned internal error with message: NullPointerException
```

2. LIKE patterns (consistent across versions):
```python
select(Product).where(Product.name.contains("value"))
# In both versions:
# Error: Illegal use of dynamic parameter
# SQL: WHERE name LIKE '%' || ? || '%'
```

3. IN clauses:
```python
select(Product).where(Product.id.in_([1, 2, 3]))
# In 24.3:
# Error: Cannot convert RexNode to equivalent Dremio expression
# In 25.1.0:
# Error: Flight returned internal error with message: NullPointerException
```

## Technical Investigation

We've traced this through the stack:
1. SQLModel/SQLAlchemy correctly generates parameterized queries
2. The Flight SQL protocol supports parameters (per spec)
3. Apache Calcite supports parameters via RexDynamicParam
4. The limitation appears to be in Dremio's implementation

We've documented our complete analysis here:
[Parameter Binding Analysis](https://github.com/serraict/vine-app/tree/main/docs/dremio-parameter-binding)

## Questions

1. The error messages have changed from explicit RexDynamicParam errors to NullPointerException in 25.1.0 - does this reflect any underlying changes in how parameters are handled?
2. Are there plans to support parameter binding in future releases?

## Current Approach

For now, we're using string interpolation with careful SQL injection prevention, but we'd love to use proper parameter binding when it becomes available.

We've set up a test suite and documentation for this issue, and we're happy to help test any future parameter binding support.
