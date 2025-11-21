# Dremio v26 Parameter Binding Test Results

**Test Date:** 2025-11-21
**Dremio Version:** 26.0 (latest OSS)
**PyArrow Version:** 17.0.0 → **22.0.0** (upgraded and retested)
**SQLAlchemy-Dremio Version:** 3.0.4

## Executive Summary

**Finding:** Parameter binding **DOES NOT WORK** in Dremio v26 via Python Flight SQL driver, despite v26 release notes indicating support for parameterized prepared statements.

**Conclusion:** The v26 parameterized prepared statements feature appears to be **JDBC-only** and is not available through the PyArrow Flight SQL driver used by Python applications.

## Test Results

### Test Environment

- **Dremio Version:** OSS v26.0 (Docker: `dremio/dremio-oss:26.0`)
- **Connection:** Flight SQL via PyArrow (`dremio+flight://localhost:32010`)
- **Test Framework:** pytest with SQLModel/SQLAlchemy
- **Test Data:** Custom products table with 20 products across 4 groups

### Package Versions

```
pyarrow                   22.0.0 (initially tested with 17.0.0, upgraded to 22.0.0 - no difference)
sqlalchemy_dremio         3.0.4
```

**Note:** Tests were initially run with PyArrow 17.0.0, then PyArrow was upgraded to the latest version (22.0.0) and tests were re-run. Results were **identical** with both versions, confirming the limitation is server-side (Dremio) not client-side (PyArrow).

### Test Results Summary

| Test Case | Result | Error Type | Notes |
|-----------|--------|------------|-------|
| Basic parameter binding (`name == "value"`) | ❌ FAILED | RexDynamicParam | Same as v24.3, v25.1.0 |
| Complex conditions (LIKE patterns) | ❌ FAILED | Illegal use of dynamic parameter | Same as v24.3, v25.1.0 |
| IN clauses (`id.in_([1,2,3])`) | ❌ FAILED | RexDynamicParam | Same as v24.3, v25.1.0 |
| Dynamic sorting | ✅ PASSED | N/A | Works as expected |

**Result:** 1 passed, 3 failed out of 4 tests

### Detailed Test Failures

#### 1. test_get_product_by_name - Basic Parameter Binding

**Test Code:**
```python
statement = select(Product).where(Product.name == "T. Bee 13")
result = session.exec(statement)
```

**Error:**
```
pyarrow._flight.FlightInternalError: Flight returned internal error,
with message: Cannot convert RexNode to equivalent Dremio expression.
RexNode Class: org.apache.calcite.rex.RexDynamicParam, RexNode Digest: ?0
```

**Analysis:** Identical error to v24.3 and v25.1.0. Dremio's Calcite SQL parser still cannot handle dynamic parameters in basic WHERE clauses.

#### 2. test_filter_products_by_multiple_conditions - Complex Conditions with LIKE

**Test Code:**
```python
statement = select(Product).where(
    and_(
        Product.product_group_name == "13 aziaat",
        Product.name.contains("13")
    )
)
result = session.exec(statement)
```

**Generated SQL:**
```sql
SELECT "Vines".products.id, "Vines".products.name,
       "Vines".products.product_group_id, "Vines".products.product_group_name
FROM "Vines"."products"
WHERE "Vines".products.product_group_name = ?
  AND ("Vines".products.name LIKE '%' || ? || '%')
```

**Error:**
```
pyarrow._flight.FlightInternalError: Flight returned internal error,
with message: At line 3, column 86: Illegal use of dynamic parameter
```

**Analysis:** Same error as previous versions. Combining parameters with LIKE and concatenation operators is not supported.

#### 3. test_filter_products_by_id_list - IN Clause with Parameters

**Test Code:**
```python
product_ids = [1, 2, 3]
statement = select(Product).where(Product.id.in_(product_ids))
result = session.exec(statement)
```

**Error:**
```
pyarrow._flight.FlightInternalError: Flight returned internal error,
with message: Cannot convert RexNode to equivalent Dremio expression.
RexNode Class: org.apache.calcite.rex.RexDynamicParam, RexNode Digest: ?0
```

**Analysis:** IN clauses with parameter binding remain unsupported, same as v24.3 and v25.1.0.

#### 4. test_dynamic_sort_products - Dynamic Sorting

**Test Code:**
```python
statement = select(Product).order_by(Product.name)
result = session.exec(statement)
```

**Result:** ✅ PASSED

**Analysis:** Sorting works correctly, as it doesn't involve parameter binding.

## Investigation Findings

### 1. Dremio v26 Release Notes Analysis

The v26 release notes state:

> "Dremio v26 introduced support for parameterized prepared statements in Arrow Flight SQL JDBC, enabling parameterized queries with prepared statements to prevent SQL injection and leverage client tools that support parameterized prepared statements. This enhancement currently supports SELECT statements."

**Key observations:**
- Explicitly mentions "**Arrow Flight SQL JDBC**"
- No mention of Python Flight SQL driver support
- Feature is limited to JDBC connections

### 2. Python Flight SQL Driver Limitations

Our testing uses:
- **PyArrow 22.0.0** - Latest Arrow Flight SQL client for Python (also tested with 17.0.0)
- **sqlalchemy-dremio 3.0.4** - Latest Dremio dialect for SQLAlchemy
- **Connection Protocol:** Flight SQL (not JDBC)

**Hypothesis confirmed:** The parameterized prepared statements feature is implemented at the JDBC driver level and is not exposed through the Arrow Flight SQL protocol that PyArrow uses.

**PyArrow version testing:** We tested with both PyArrow 17.0.0 and 22.0.0 (latest). Results were **identical**, proving the limitation is on Dremio's server-side SQL parser, not in the PyArrow client library.

### 3. Dremio Logs

No relevant errors or warnings about parameter binding found in Dremio server logs. The server simply rejects the parameterized queries with the same errors as previous versions.

## Comparison with Previous Versions

| Feature | v24.3 | v25.1.0 | v26.0 |
|---------|-------|---------|-------|
| Basic parameter binding | ❌ | ❌ | ❌ |
| LIKE with parameters | ❌ | ❌ | ❌ |
| IN clause with parameters | ❌ | ❌ | ❌ |
| Dynamic sorting | ✅ | ✅ | ✅ |
| Error messages | RexDynamicParam / Illegal use | NullPointerException / Illegal use | RexDynamicParam / Illegal use |

**Conclusion:** No improvement in parameter binding support for Python Flight SQL users from v24.3 through v26.0.

## Why v26 Prepared Statements Don't Help

The v26 feature is likely:

1. **JDBC-specific implementation** - Added only to the JDBC driver layer
2. **Not protocol-level** - Not implemented in the core Arrow Flight SQL protocol handling
3. **Java-focused** - Targets Java/JDBC clients, not Python/PyArrow clients

For Python users:
- SQLAlchemy generates parameterized SQL with `?` placeholders
- This is sent via PyArrow's Flight SQL client
- Dremio's Flight SQL server receives it
- Dremio's Calcite parser still cannot convert `RexDynamicParam` nodes
- Same errors occur as in previous versions

## Implications

### For Our Project

1. **No Immediate Solution:** v26 does not resolve our parameter binding limitations
2. **Workarounds Still Required:** Must continue using string interpolation or raw SQL
3. **SQLModel Limitations Persist:** Cannot use clean SQLModel query syntax
4. **Security Concerns:** Must carefully handle SQL injection risks in our workarounds

### For Future Development

1. **Monitor Python Driver Updates:** Watch for updates to PyArrow or sqlalchemy-dremio
2. **Track Dremio Development:** Check if future versions extend prepared statements to Flight SQL
3. **Consider JDBC Bridge:** Could investigate using Jython or JPype to use JDBC driver from Python (not recommended due to complexity)
4. **Alternative Query Patterns:** Continue refining hybrid approach with raw SQL for complex queries

## Recommendations

### Short Term (Current State)

1. **Continue with existing workarounds** documented in `dremio-sqlmodel-solutions.md`
2. **Use raw SQL with string formatting** for complex queries requiring parameter binding
3. **Implement proper SQL injection prevention** in our query builders
4. **Document limitations clearly** for team members

### Medium Term (Next 6 months)

1. **Monitor these channels:**
   - PyArrow Flight SQL updates
   - sqlalchemy-dremio releases
   - Dremio community discussions
   - Dremio release notes for Flight SQL improvements

2. **Engage with Dremio community:**
   - Ask in community forums if Flight SQL prepared statements are planned
   - File feature request for Python/PyArrow support
   - Share our use case and requirements

3. **Consider query builder approach:**
   - Build type-safe wrapper around raw SQL
   - Create utilities for common query patterns
   - Maintain SQLModel-like API where possible

### Long Term (Future)

1. **Re-evaluate when:**
   - Dremio announces Flight SQL prepared statement support
   - PyArrow adds prepared statement handling
   - Alternative Dremio Python drivers emerge

2. **Consider alternatives if needed:**
   - Different query engine (e.g., Trino, Presto)
   - Different connection method (if available)
   - Custom dialect implementation

## Next Steps

1. ✅ Document v26 test results (this document)
2. ⬜ Update `testing-dremio-versions.md` with v26 comparison
3. ⬜ Update `dremio-parameter-binding-analysis.md` with v26 findings
4. ⬜ Review and update `dremio-sqlmodel-solutions.md` based on v26 results
5. ⬜ Create issue/discussion in Dremio community about Python Flight SQL support
6. ⬜ Document best practices for our workaround approach

## References

- [Dremio v26 Release Notes](https://docs.dremio.com/current/release-notes/version-260-release/)
- [Previous analysis: Parameter Binding Analysis](dremio-parameter-binding-analysis.md)
- [Previous analysis: Version Testing Guide](testing-dremio-versions.md)
- [Test suite: test_products_ideal.py](../../tests/integration/test_products_ideal.py)
- [PyArrow Flight SQL Documentation](https://arrow.apache.org/docs/python/api/flight.html)
- [SQLAlchemy-Dremio GitHub](https://github.com/dremio/dremio-sqllchemy)

## Appendix: Full Test Output

```
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-8.3.3, pluggy-1.5.0
cachedir: .pytest_cache
rootdir: /Users/marijn/dev/serraict/vine-app
configfile: pyproject.toml
plugins: asyncio-0.24.0, cov-5.0.0, anyio-4.6.2.post1
collecting ... collected 4 items

tests/integration/test_products_ideal.py::test_get_product_by_name FAILED [ 25%]
tests/integration/test_products_ideal.py::test_filter_products_by_multiple_conditions FAILED [ 50%]
tests/integration/test_products_ideal.py::test_filter_products_by_id_list FAILED [ 75%]
tests/integration/test_products_ideal.py::test_dynamic_sort_products PASSED [100%]

======================== 3 failed, 1 passed in 1.30s ==========================
```
