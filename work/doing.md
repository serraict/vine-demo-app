# Doing

Goal: Test Dremio v26 OSS for SQLModel Parameter Binding Support

## Summary of Findings

**Test Date:** 2025-11-21
**Test Result:** ❌ **PARAMETER BINDING STILL DOES NOT WORK IN v26**

Despite Dremio v26 release notes claiming support for "parameterized prepared statements in Arrow Flight SQL JDBC", this feature is **JDBC-only** and does NOT work via Python's PyArrow Flight SQL driver.

**Test Results:** 1 passed, 3 failed (identical to v24.3 and v25.1.0)
- ❌ Basic parameter binding: Same "RexDynamicParam" error
- ❌ LIKE patterns: Same "Illegal use of dynamic parameter" error
- ❌ IN clauses: Same "RexDynamicParam" error
- ✅ Dynamic sorting: Still works

**PyArrow Version Testing:** Upgraded from 17.0.0 → 22.0.0 (latest) and retested. **No difference** - confirms limitation is server-side (Dremio) not client-side (PyArrow).

**Conclusion:** We must continue using workarounds (raw SQL with string formatting) for SQLModel queries. The v26 prepared statements feature provides no benefit to Python users.

**Documentation Created:**
- Comprehensive test results: `docs/dremio-parameter-binding/testing-v26-results.md`
- Updated version comparison: `docs/dremio-parameter-binding/testing-dremio-versions.md`
- Updated technical analysis: `docs/dremio-parameter-binding/dremio-parameter-binding-analysis.md`

## Context

Previous testing (documented in docs/dremio-parameter-binding/) revealed that Dremio versions 24.3 and 25.1.0 did not support parameterized queries with SQLModel, causing errors like:

- "Cannot convert RexNode to equivalent Dremio expression. RexNode Class: org.apache.calcite.rex.RexDynamicParam"
- "Illegal use of dynamic parameter"

**CRITICAL NEW FINDING**: Dremio v26 release notes indicate support for "parameterized prepared statements in Arrow Flight SQL JDBC" was added, specifically to "prevent SQL injection and leverage client tools that support parameterized prepared statements." This currently supports SELECT statements.

This could potentially resolve our parameter binding limitations!

## Analysis & Design

### What We're Testing

1. **Basic Parameter Binding** (previously failed in v24.3 and v25.1.0):
   - Simple equality: `Product.name == "value"`
   - Comparison operators: `Product.id > 5`

2. **Complex Conditions** (previously failed):
   - LIKE patterns: `Product.name.contains("search")`
   - Combined conditions with AND/OR
   - LIKE with concatenation: `name LIKE '%' || ? || '%'`

3. **IN Clauses** (previously failed):
   - `Product.id.in_([1, 2, 3])`

4. **Sorting** (previously worked):
   - `order_by(Product.name)` - verify still works

### Expected Outcomes

**Hypothesis**: The new parameterized prepared statements support in v26 should allow our SQLModel queries to work correctly with parameter binding.

**Alternative outcome**: If parameter binding still fails, we need to investigate:

- Whether the feature is JDBC-only and not available via Python's Flight SQL driver
- If additional configuration is needed
- If SQLAlchemy-Dremio dialect needs updates to leverage this feature

## Steps

### 1. Environment Setup

- [x] Update docker-compose.yml to use Dremio OSS v26 (change image tag from 25.1.0 to 26.0.2 or latest v26)
- [x] Start fresh Dremio v26 instance: `docker compose up -d`
- [x] Verify Dremio is running at <http://localhost:9047>
- [x] Create initial admin user in UI

### 2. Test Data Setup

- [x] Add data source "test_data" pointing to `/opt/dremio/data/test_data` (File System)
- [x] Format products.csv as table named "Products"
- [x] Set schema to 'Vines': `ALTER TABLE test_data.Products SET SCHEMA 'Vines';`
- [x] Verify data loads correctly: `SELECT * FROM Vines.Products ORDER BY id;`
- [x] Confirm 20 products across 4 groups are present

### 3. Run Existing Test Suite

- [x] Set environment: `export VINEAPP_DB_CONNECTION="dremio+flight://user:password@localhost:32010/dremio"`
- [x] Run parameter binding tests: `INCLUDE_DREMIO_LIMITATIONS_TESTS=1 pytest tests/integration/test_products_ideal.py -v`
- [x] Document which tests pass/fail
- [x] Compare results with previous testing (v24.3 and v25.1.0)

**Results:** 1 passed, 3 failed - Same failures as v24.3 and v25.1.0

### 4. Detailed Test Analysis

For each test case that previously failed:

- [x] **test_get_product_by_name**: Basic equality parameter binding
  - Record: ❌ FAILED
  - Error: "Cannot convert RexNode to equivalent Dremio expression. RexNode Class: org.apache.calcite.rex.RexDynamicParam"
  - Same error as v24.3

- [x] **test_filter_products_by_multiple_conditions**: Complex conditions with LIKE
  - Record: ❌ FAILED
  - Error: "Illegal use of dynamic parameter"
  - Generated SQL: `WHERE "Vines".products.product_group_name = ? AND ("Vines".products.name LIKE '%' || ? || '%')`
  - Same error as v24.3 and v25.1.0

- [x] **test_filter_products_by_id_list**: IN clause with parameters
  - Record: ❌ FAILED
  - Error: "Cannot convert RexNode to equivalent Dremio expression. RexNode Class: org.apache.calcite.rex.RexDynamicParam"
  - Same error as v24.3

- [x] **test_dynamic_sort_products**: Verify sorting still works
  - Record: ✅ PASSED
  - Works as expected (no parameter binding involved)

### 5. Additional Investigation (if tests still fail)

- [x] Check PyArrow version compatibility: `pip list | grep pyarrow`
  - pyarrow 17.0.0 (latest)
- [x] Check sqlalchemy-dremio version: `pip list | grep dremio`
  - sqlalchemy_dremio 3.0.4 (latest)
- [x] Review Dremio logs for detailed errors: `docker-compose logs dremio`
  - No parameter-related errors in logs
- [ ] Test direct SQL with parameters via Python Flight SQL driver
- [ ] Check if feature requires specific configuration flags
- [x] Review Dremio v26 documentation for Flight SQL driver requirements
  - **Finding:** Prepared statements feature is explicitly JDBC-only

### 6. Documentation

- [x] Create new document: `docs/dremio-parameter-binding/testing-v26-results.md`
- [x] Update version comparison table in `testing-dremio-versions.md`
- [x] Document any configuration changes needed (none - same errors)
- [x] Update `dremio-parameter-binding-analysis.md` with v26 findings
- [ ] If successful, update `dremio-sqlmodel-solutions.md` with recommended approach
- [ ] If unsuccessful, document investigation findings and next steps

### 7. Release Notes Review

- [x] Review full v26 release notes at <https://docs.dremio.com/current/release-notes/version-260-release/>
- [x] Check for any other SQL/Flight SQL improvements
  - Found: Window function fixes, COUNT(*) optimization, JOIN improvements
  - **Key finding:** Prepared statements feature explicitly mentions "JDBC" only
- [x] Note any Calcite version updates
  - No Calcite version changes noted in release notes
- [x] Document any breaking changes or migration notes
  - No breaking changes affecting our use case

### 8. Cleanup

- [ ] Stop Dremio: `docker-compose down`
- [ ] (Optional) Remove volumes if needed: `docker-compose down -v`

## Test Data Reference

The test data (data/products.csv) contains:

- 20 products across 4 product groups
- Group 1: "13 aziaat" - T. Bee series (IDs 1-5)
- Group 2: "21 europees" - H. Bee series (IDs 6-10)
- Group 3: "31 afrikaans" - B. Bee series (IDs 11-15)
- Group 4: "41 amerikaans" - M. Bee series (IDs 16-20)

## Key Files

- Docker setup: `docker-compose.yml`
- Test suite: `tests/integration/test_products_ideal.py`
- Previous analysis: `docs/dremio-parameter-binding/dremio-parameter-binding-analysis.md`
- Version testing guide: `docs/dremio-parameter-binding/testing-dremio-versions.md`
- Test data: `data/products.csv`

## Success Criteria

**Full Success**: All parameter binding tests pass in v26, allowing clean SQLModel usage without workarounds.

**Partial Success**: Some parameter binding scenarios work (e.g., basic equality) but complex ones still fail. Would inform a hybrid approach.

**No Change**: Parameter binding still fails completely. Would need to investigate if feature is JDBC-only or requires additional integration work.

## Next Actions

1. Start with Step 1: Update docker-compose.yml for v26
2. Proceed through steps sequentially
3. Document findings as we go
4. Update existing documentation with v26 results
