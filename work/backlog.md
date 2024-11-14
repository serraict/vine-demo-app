# Backlog

## Doing

### Project Template

- [ ] Create cookiecutter template based on this project
  - [ ] Setup template structure in repository
    - [ ] Create `template` directory
    - [ ] Setup cookiecutter configuration
    - [ ] Create template README with usage instructions
  - [ ] Analyze current project structure and identify components to modularize
    - [ ] Map out core components (web, console, Fibery, Dremio)
    - [ ] Identify shared infrastructure (Docker, Python setup)
    - [ ] Document dependencies between components
  - [ ] Design cookiecutter variables and options
    - [ ] Define project type options (web/console/both)
    - [ ] Define integration options (Fibery/Dremio/both)
    - [ ] Define optional features (cronjobs)
  - [ ] Create template content
    - [ ] Extract core project files (Docker, Python version, CI/CD)
    - [ ] Create conditional component directories
    - [ ] Setup modular test infrastructure
    - [ ] Ensure template stays in sync with main project
  - [ ] Implement template logic
    - [ ] Create cookiecutter.json with variables
    - [ ] Implement conditional file inclusion
    - [ ] Setup GitHub Actions workflows
  - [ ] Setup versioning strategy
    - [ ] Add template version tracking
    - [ ] Document template-project compatibility
    - [ ] Include upgrade instructions
  - [ ] Create example outputs
    - [ ] Generate basic console app example
    - [ ] Generate web app with Dremio example
    - [ ] Generate full integration example
  - [ ] Write template documentation
    - [ ] Document available options
    - [ ] Add usage examples
    - [ ] Include best practices
    - [ ] Document how template relates to main project

## Next

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
