# Backlog

## Doing

### Project Template

- [ ] Create cookiecutter template based on this project
  - [x] Setup template structure in repository
    - [x] Create `template` directory
    - [x] Setup cookiecutter configuration
    - [x] Create template README with usage instructions
  - [x] Analyze current project structure and identify components to modularize
    - [x] Map out core components (web, console, Fibery, Dremio)
    - [x] Identify shared infrastructure (Docker, Python setup)
    - [x] Document dependencies between components
  - [ ] Design cookiecutter variables and options
    - [x] Define project type options (web/console/both)
    - [x] Define integration options (Fibery/Dremio/both)
    - [ ] Define optional features (cronjobs)
  - [ ] Create template content
    - [x] Setup minimal working template
      - [x] Create basic project structure
      - [x] Add minimal pyproject.toml
      - [x] Add simple CLI entrypoint
      - [x] Test template generation
    - [ ] Add Docker support
      - [ ] Add Dockerfile
      - [ ] Add docker-compose.yml
      - [ ] Test Docker build and run
    - [ ] Add core components incrementally
      - [ ] Add products module
        - [ ] Extract base models
        - [ ] Test with SQLite
      - [ ] Add web interface
        - [ ] Extract base pages
        - [ ] Test local serving
      - [ ] Add Dremio integration
        - [ ] Extract repository pattern
        - [ ] Test with Docker Dremio
      - [ ] Add Fibery integration
        - [ ] Extract GraphQL client
        - [ ] Test with mock server
    - [ ] Setup conditional rendering
      - [ ] Implement component selection logic
      - [ ] Test different combinations
    - [ ] Add development tooling
      - [ ] Add pre-commit hooks
      - [ ] Add development scripts
      - [ ] Test development workflow
  - [ ] Implement template logic
    - [x] Create cookiecutter.json with variables
    - [ ] Implement conditional file inclusion
    - [ ] Setup GitHub Actions workflows
  - [ ] Setup versioning strategy
    - [ ] Add SCM versioning to the genereated project (not to the template)
      - [ ] Add setuptools_scm configuration
      - [ ] Update documentation for git requirements
      - [ ] Test version detection
    - [ ] Add template version tracking
    - [ ] Document template-project compatibility
    - [ ] Include upgrade instructions
  - [ ] Create example outputs
    - [ ] Generate basic console app example
    - [ ] Generate web app with Dremio example
    - [ ] Generate full integration example
  - [ ] Write template documentation
    - [x] Document available options
    - [x] Add usage examples
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
