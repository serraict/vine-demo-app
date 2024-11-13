# Dremio Parameter Binding Technical Analysis

[Previous content remains the same until "Flight SQL Specification Findings" section, then add:]

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

## Revised Root Cause

Based on our investigation of both Flight SQL and Calcite, we can now better understand the parameter binding issue:

1. **Protocol Support**:
   - Flight SQL protocol supports parameters
   - Calcite framework supports dynamic parameters
   - SQLModel/SQLAlchemy correctly generates parameterized queries

2. **Implementation Gap**:
   - Dremio's implementation appears to not fully implement the parameter binding capabilities
   - The error occurs when Dremio tries to convert SQLAlchemy's parameterized query into Calcite's RexDynamicParam
   - This suggests the issue is in Dremio's layer between Flight SQL and Calcite

3. **Specific Issues**:
   - Basic parameters fail with "Cannot convert RexNode" error
   - Complex parameters (LIKE, IN) fail with "Illegal use of dynamic parameter"
   - But Calcite itself supports these features through RexDynamicParam

[Rest of the document remains the same]
