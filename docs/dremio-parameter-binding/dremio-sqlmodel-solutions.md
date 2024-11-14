# Potential Solutions for SQLModel-Dremio Integration

This document explores potential solutions to the limitations we face when using SQLModel with Dremio Flight SQL, particularly around parameter binding and complex queries.

## Solution Categories

### 1. Custom SQLModel Dialect

**Approach**: Create a custom SQLModel/SQLAlchemy dialect for Dremio that handles parameter binding differently.

**Implementation Ideas**:

- Extend the current Dremio dialect to convert parameterized queries into literal SQL
- Implement parameter substitution at the dialect level before sending to Dremio
- Handle special cases like IN clauses and LIKE patterns

**Pros**:

- Maintains SQLModel's clean API
- Type safety through SQLModel remains intact
- Transparent to application code

**Cons**:

- Complex implementation
- Need to maintain compatibility with SQLAlchemy/SQLModel updates
- Potential security concerns with SQL injection if not done carefully

**Required Investigation**:

- [ ] Study SQLAlchemy dialect implementation
- [ ] Research how other databases handle parameter binding
- [ ] Investigate Dremio Flight SQL protocol details

### 2. Query Builder Wrapper

**Approach**: Create a wrapper around SQLModel that converts its expressions to Dremio-compatible SQL.

**Implementation Ideas**:

```python
class DremioQueryBuilder:
    def __init__(self, model_class):
        self.model = model_class
        self._conditions = []
    
    def filter_by(self, **kwargs):
        for k, v in kwargs.items():
            # Convert to literal SQL
            self._conditions.append(f"{k} = '{v}'")
        return self
    
    def execute(self, session):
        # Build and execute raw SQL
        pass
```

**Pros**:

- Maintains some type safety through Python
- Can optimize specifically for Dremio
- Easier to implement than a full dialect

**Cons**:

- Different API from standard SQLModel
- Need to implement all query features
- Potential for SQL injection if not careful

### 3. Raw SQL with Type Safety

**Approach**: Use raw SQL but wrap it in type-safe functions.

**Implementation Ideas**:

```python
from typing import TypeVar, List

T = TypeVar('T', bound=SQLModel)

def get_by_name(session: Session, model: Type[T], name: str) -> Optional[T]:
    sql = f"SELECT * FROM {model.__tablename__} WHERE name = '{name}'"
    result = session.exec(text(sql))
    return result.first()
```

**Pros**:

- Works reliably with Dremio
- Type hints provide some safety
- Straightforward implementation

**Cons**:

- Loses SQLModel's query building features
- More boilerplate code
- Manual SQL string building

### 4. Hybrid Approach

**Approach**: Use SQLModel for simple queries and raw SQL for complex ones.

**Implementation Ideas**:

```python
class ProductRepository:
    def get_all(self) -> List[Product]:
        # Use SQLModel for simple queries
        return select(Product)
    
    def filter_complex(self, **criteria):
        # Use raw SQL for complex queries
        sql = self._build_complex_query(criteria)
        return text(sql)
```

**Pros**:

- Best of both worlds
- Can optimize complex queries
- Gradual migration path

**Cons**:

- Inconsistent API
- Need to maintain two query systems
- Potential confusion for developers

## Evaluating Solutions

When choosing between these solutions, consider the following factors:

### Project Requirements

1. **Development Speed**:
   - Hybrid Approach: Fastest to implement
   - Raw SQL: Quick but requires more code
   - Query Builder: Medium effort
   - Custom Dialect: Significant investment

2. **Maintainability**:
   - Custom Dialect: Most maintainable once implemented
   - Query Builder: Good maintainability with clear patterns
   - Hybrid: Requires careful documentation
   - Raw SQL: Most prone to maintenance issues

3. **Type Safety**:
   - Custom Dialect: Full SQLModel type safety
   - Query Builder: Good type safety
   - Raw SQL with Types: Basic type safety
   - Hybrid: Mixed type safety

### Team Considerations

1. **Team Experience**:
   - Raw SQL: Requires SQL expertise
   - SQLModel: Requires Python/ORM expertise
   - Custom Dialect: Requires deep SQLAlchemy knowledge

2. **Learning Curve**:
   - Raw SQL: Minimal for SQL experts
   - Hybrid: Moderate
   - Query Builder: Moderate
   - Custom Dialect: Steep

### Technical Factors

1. **Performance**:
   - Raw SQL: Best performance (direct control)
   - Custom Dialect: Good performance
   - Query Builder: Good performance
   - Hybrid: Varies by implementation

2. **Security**:
   - Custom Dialect: Can implement proper escaping
   - Query Builder: Need careful parameter handling
   - Raw SQL: Most vulnerable to SQL injection
   - Hybrid: Mixed security concerns

## Recommended Approach

Based on these considerations, we recommend a phased implementation:

1. **Phase 1**: Start with the Hybrid Approach
   - Quick to implement
   - Allows immediate progress
   - Provides time to learn more about the system

2. **Phase 2**: Develop Query Builder
   - Build on lessons from Hybrid Approach
   - Implement common query patterns
   - Improve type safety

3. **Phase 3**: Consider Custom Dialect
   - Long-term solution if needed
   - Depends on project success and requirements
   - Monitor Dremio development for native solutions

## Next Steps

1. **Immediate Solutions**:
   - Implement the Hybrid Approach
   - Document patterns for both SQLModel and raw SQL usage
   - Add type safety wrappers for raw SQL

2. **Medium Term**:
   - Develop the Query Builder Wrapper
   - Create utility functions for common query patterns
   - Build test suite for query generation

3. **Long Term**:
   - Investigate custom dialect implementation
   - Contribute improvements to sqlalchemy-dremio
   - Monitor Dremio Flight SQL development for parameter binding support

## Research Topics

1. **Dremio Development**:
   - Track Dremio Flight SQL roadmap
   - Monitor for parameter binding support
   - Investigate alternative Dremio connection methods

2. **SQLAlchemy/SQLModel**:
   - Study dialect implementation
   - Understand parameter binding internals
   - Research similar database adapters

3. **Security**:
   - SQL injection prevention
   - Parameter sanitization
   - Best practices for raw SQL

## References

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Dialects](https://docs.sqlalchemy.org/en/14/dialects/)
- [Dremio Flight SQL Documentation](https://docs.dremio.com/software/drivers/flight-sql/)
- Our test cases: `tests/integration/test_products_ideal.py`
