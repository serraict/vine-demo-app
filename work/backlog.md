# Backlog

## Doing

## Next

### Goal: Create Web Application with NiceGUI

1. Implement Core Features
   - [x] Create shared code module for CLI and web app
     - [x] Refactor product listing logic into dedicated package
     - [x] Extract about/version information into standalone module
   - [x] Create about page
     - [x] Show version and app information
     - [x] Match CLI about command information
     - [x] Add links to documentation and GitHub
   - [x] Review nicegui testing strategy
   - [ ] Enhance product listing page
     - [x] Display products in a table
     - [x] Add basic sorting
     - [ ] Add filtering capabilities
       - [ ] Add search box for filtering by name
       - [ ] Add dropdown for filtering by product group
     - [x] Implement basic server-side pagination
     - [ ] Add product details view
       - [ ] Create product detail route (/products/<id>)
       - [ ] Show detailed product information

## Later

### tech stack

- [ ] Remove unused pages.
- [ ] Use Pydantic instead of data class

### Data Visualization

- [ ] Integrate with Serra Vine's Superset
  - [ ] Add Superset dashboard embedding
  - [ ] Configure product analytics views
  - [ ] Setup dashboard linking from product pages

### Deployment

- [ ] Create deployable packages
  - [ ] Configure PyPI package setup
  - [ ] Create production Docker container
  - [ ] Create development Docker container
  - [ ] Add container documentation and examples

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
