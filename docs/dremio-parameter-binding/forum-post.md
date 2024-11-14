# Parameter Binding Support in Dremio Flight SQL with SQLModel/SQLAlchemy

Hi Dremio community,

We've been working on integrating Dremio with SQLModel (a Python ORM built on SQLAlchemy) and have encountered some limitations with parameter binding support in Dremio Flight SQL. We've done extensive testing and analysis of this issue across versions 24.3 and 25.1.0, and I wanted to share our findings and ask about future plans for parameter binding support.

## Current Behavior

When using SQLModel's standard parameter binding patterns (which work with most databases), we encounter the following issues:

1. Basic parameter binding fails:
```python
select(Product).where(Product.name == "value")
# In 24.3:
# Error: Cannot convert RexNode to equivalent Dremio expression. 
# RexNode Class: org.apache.calcite.rex.RexDynamicParam
# In 25.1.0:
# Error: Flight returned internal error with message: NullPointerException
```

2. Complex conditions with LIKE patterns fail:
```python
select(Product).where(
    and_(
        Product.name.contains("value"),
        Product.id > 5
    )
)
# In both 24.3 and 25.1.0:
# Error: Illegal use of dynamic parameter
# SQL: WHERE product_group_name = ? AND (name LIKE '%' || ? || '%')
```

3. IN clauses fail:
```python
select(Product).where(Product.id.in_([1, 2, 3]))
# In 24.3:
# Error: Cannot convert RexNode to equivalent Dremio expression
# RexNode Class: org.apache.calcite.rex.RexDynamicParam
# In 25.1.0:
# Error: Flight returned internal error with message: NullPointerException
```

## Technical Analysis

We've traced this through several layers:
1. SQLModel/SQLAlchemy generates standard parameterized queries
2. The Flight SQL protocol specification supports parameters
3. Apache Calcite (used by Dremio) supports parameters via RexDynamicParam
4. But Dremio's implementation appears to not fully support this feature

The error messages have changed between versions 24.3 and 25.1.0, but the core limitation remains: parameter binding is not supported. In 24.3, we see explicit RexDynamicParam errors, while in 25.1.0 these have become NullPointerExceptions, though the LIKE pattern limitation remains consistent across versions.

We've documented our complete analysis and test cases here:
[Parameter Binding Analysis](https://github.com/serraict/vine-app/tree/main/docs/dremio-parameter-binding)

## Questions

1. Is parameter binding support planned for future Dremio releases?
2. Are there any known workarounds besides string interpolation?
3. Are there specific reasons why parameter binding isn't currently supported?
4. Is the change in error messages from 24.3 to 25.1.0 related to any underlying changes in how parameters are handled?

## Current Workaround

Currently, we're working around this by converting parameters to literals before they reach Dremio, but this isn't ideal as it:
- Reduces type safety
- Requires careful SQL injection prevention
- Makes the code more complex

Any insights from the Dremio team or community would be greatly appreciated. We're happy to contribute our findings or help test any future parameter binding support.

Thanks!
