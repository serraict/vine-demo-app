# Backlog

## Doing

Refactor code and write down architectural guidelines.

Review the code and write down guidelines on how to ...

- Create pages using nicegui
- Write repository function

## Next

### Tech questions

Does using an ODBC connection allow us to use parameterized queries?
That would make SQLModel repositories more straightforward.

### Deployment

- [ ] Create deployable packages
  - [ ] Github workflow for creating container on release
  - [ ] Create production Docker container
    - [ ] upload to ghcr
  - [ ] Create development Docker container
  - [ ] Add container documentation and examples


## Later

### tech stack

- [ ] Remove unused pages.
- [ ] Use Pydantic instead of data class

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

### Plugin System

- [ ] Design plugin architecture
  - [ ] Create plugin interface for data sources
  - [ ] Add plugin support for visualization types
  - [ ] Support custom CLI commands via plugins
  - [ ] Support custom web pages via plugins

### Monitoring and Performance

- [ ] Add application monitoring
  - [ ] Implement performance metrics collection
  - [ ] Add query performance tracking
  - [ ] Create monitoring dashboard
  - [ ] Setup alerting system

### Security

- [ ] Implement security features
  - [ ] Add authentication system
  - [ ] Implement role-based access control
  - [ ] Add audit logging
  - [ ] Implement secure configuration management

### Logging
