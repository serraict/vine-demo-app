# AI/LLM Contributing Guidelines for Vine App

This guide supplements CONTRIBUTING.md with specific guidelines for AI/LLM contributors.
Follow both this guide and the main CONTRIBUTING.md when making changes.

## Context Understanding

Before making changes:

1. Analyze project structure:
   - `src/vineapp/` - Main application code
   - `tests/` - Unit tests
   - `tests/integration/` - Integration tests
   - `work/` - Project management artifacts

2. Review related files:
   - Check similar files for patterns and conventions
   - Review test files to understand expected behavior
   - Look for project-specific idioms

3. Quality standards:
   - Use type hints for function parameters and return values
   - Include docstrings for modules, classes, and functions
   - Keep functions focused and under 20 lines
   - Keep cyclomatic complexity low (max 10)
   - Follow existing code style

## Making Changes

1. Test-Driven Development:
   - Write failing test first
   - Implement minimum code to pass
   - Refactor while keeping tests green
   - Keep test code simple and readable
   - Avoid unnecessary assertions

2. Documentation:
   - Update docstrings
   - Add inline comments for complex logic
   - Update CHANGELOG.md following Keep a Changelog format

3. Quality Checks:
   - Run `make quality` for linting and formatting
   - Ensure all tests pass
   - Verify changes meet project standards

## Version Control

1. Make atomic commits representing single logical changes

2. Follow Conventional Commits format:
   ```
   <type>[optional scope]: <description>
   ```
   Types:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation
   - style: Code style
   - refactor: Code restructuring
   - test: Test changes
   - chore: Build/tool changes

3. Commit messages should:
   - Clearly explain the change
   - Include context and reasoning
   - Reference related issues/PRs

## Quality Checklist

Before completing task:

1. Code Quality
   - [ ] Follows project structure and patterns
   - [ ] Includes appropriate type hints
   - [ ] Has necessary docstrings
   - [ ] Passes linting and formatting

2. Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests if needed
   - [ ] All tests pass
   - [ ] Test coverage maintained

3. Documentation
   - [ ] Code is self-documenting
   - [ ] Complex logic explained
   - [ ] CHANGELOG.md updated

4. Version Control
   - [ ] Changes are atomic
   - [ ] Commit messages follow convention
   - [ ] Changes are properly scoped

## Framework-Specific Guidelines

### NiceGUI Testing

When testing NiceGUI components:

1. Use the `@pytest.mark.module_under_test(__web__)` decorator to register pages for testing

2. For tables, use the elements property to verify content:
   ```python
   table = user.find(ui.table).elements.pop()
   assert table.columns == [...]  # Verify column structure
   assert table.rows == [...]     # Verify row data
   ```

3. For text content, use should_see:
   ```python
   await user.should_see("Some Text")  # Check visible text
   ```

4. For links and interactions:
   ```python
   await user.should_see("Link Text")
   user.find("Link Text").click()
   ```

Remember that NiceGUI's testing module provides specific ways to verify UI elements. Don't try to access internal properties directly, but use the provided testing utilities.
