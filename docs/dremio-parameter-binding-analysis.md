# Dremio Parameter Binding Technical Analysis

[Previous content remains the same until "Revised Root Cause" section, then add:]

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

We're currently using Dremio version 24.3, and reviewing release notes through version 25.x reveals:

1. **No Direct Parameter Binding Improvements**:
   - No specific fixes or improvements for Flight SQL parameter binding
   - No changes to Calcite integration regarding RexDynamicParam handling
   - Parameter binding limitations appear to persist through recent versions

2. **Related Improvements**:
   - Query planning and execution optimizations
   - Database connector improvements
   - Memory management enhancements
   - Better error handling for various query types

3. **Implications**:
   - The parameter binding limitation appears to be a fundamental design choice rather than a bug
   - No indication in release notes of planned support for parameter binding
   - Need to design our solution assuming this limitation will persist

## Revised Root Cause

Based on our investigation of Flight SQL, Calcite, and version analysis:

1. **Protocol Support**:
   - Flight SQL protocol supports parameters
   - Calcite framework supports dynamic parameters
   - SQLModel/SQLAlchemy correctly generates parameterized queries

2. **Implementation Gap**:
   - Dremio's implementation appears to not fully implement the parameter binding capabilities
   - The error occurs when Dremio tries to convert SQLAlchemy's parameterized query into Calcite's RexDynamicParam
   - This limitation persists through recent versions (24.3 to 25.x)

3. **Specific Issues**:
   - Basic parameters fail with "Cannot convert RexNode" error
   - Complex parameters (LIKE, IN) fail with "Illegal use of dynamic parameter"
   - But Calcite itself supports these features through RexDynamicParam

[Rest of the document remains the same]
