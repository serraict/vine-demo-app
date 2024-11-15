# Backlog

## Doing

### Project Template

We will create a cookiecutter template based on this project,
so that developers can get started quickly with
building an application that targets the Serra Vine platform.

- [x] Create cookiecutter template based on this project
  - [x] Create template content
    - [x] Publish the template
      - [x] Create new GitHub repository 'cookiecutter-vine-app'
      - [x] Copy files to new repository:
        - [x] template/ directory
        - [x] scripts/ directory
        - [x] work/ directory
        - [x] Move template/README.md to root README.md
        - [x] Update installation instructions:
          ```
          # Install
          cookiecutter gh:serraict/cookiecutter-vine-app

          # Or for a specific version
          cookiecutter gh:serraict/cookiecutter-vine-app --checkout v1.0.0
          ```
      - [x] Tag initial release v0.1.0
    - [ ] Add core components incrementally
      - [ ] Add Fibery module
        - [ ] Create fibery package structure
          - [ ] Add __init__.py
          - [ ] Add models.py
          - [ ] Add graphql.py
        - [ ] Add tests
          - [ ] Add test_fibery_models.py
          - [ ] Add test_fibery_graphql.py
        - [ ] Add requests to dependencies in pyproject.toml
        - [ ] Add environment variables to .env.example
  - [ ] Design cookiecutter variables and options
    - [ ] Define optional features (cronjobs)
  - [ ] Setup conditional rendering
    - [ ] Implement component selection logic
    - [ ] Test different combinations
  - [ ] Setup versioning strategy
    - [ ] Add SCM versioning to the generated project (not to the template)
      - [ ] Add setuptools_scm configuration
      - [ ] Update documentation for git requirements
      - [ ] Test version detection
    - [ ] Add template version tracking
  - [ ] Create example outputs
    - [ ] Generate basic console app example
    - [ ] Generate web app with Dremio example
    - [ ] Generate full integration example
  - [ ] Write template documentation
    - [ ] Include best practices
    - [ ] Document how template relates to main project

## Later

### Data Visualization

- [ ] Integrate with Serra Vine's Superset
  - [ ] Add Superset dashboard embedding
  - [ ] Configure product analytics views
  - [ ] Setup dashboard linking from product pages

### Documentation

- [ ] Setup documentation build pipeline
  - [ ] Configure documentation generator for GitHub Pages
  - [ ] Setup automatic documentation deployment
- [ ] Write concise documentation that allow players to make the next move in their game:
  - [ ] Installation and setup guides
  - [ ] API documentation
  - [ ] Usage examples

### Automated Specifications

- [ ] Implement specifications by example
  - [ ] Setup Robot Framework
  - [ ] Write acceptance tests as living documentation
  - [ ] Integrate with existing test suite

### Monitoring and Performance

- [ ] Add application monitoring
  - [ ] Implement performance metrics collection
  - [ ] Add query performance tracking
  - [ ] Create monitoring dashboard
  - [ ] Setup alerting system

### Security

- [ ] Implement security features
  - [ ] Add (audit-) logging
  - [ ] Implement secure configuration management
