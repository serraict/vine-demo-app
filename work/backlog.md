# Backlog

## Doing

Connect to the Fibery environment.

- [x] Create a web page that shows link to the Fibery knowledge base
  - [x] Create a new route /kb
  - [x] Add a page component that uses our model_card for displaying Fibery info
    Fibery URL to be retrieved from env var.
  - [x] Add link to the Fibery knowledge base using our URL field handling
  - [x] The space name should be set as an env var too.
    - [x] From the space name and the base url create link to:
      - [x] Space homepage
      - [x] Api base address
      - [x] Link to graphql app
  - [ ] Add list of Fibery databases with links.
    - [x] Fibery exposes a graphql interface. We can use it to discover the types (=databases in Fibery).
    - [ ] Add database links to the KB page
  - [x] Add navigation link in the menu
  - [x] Add tests for the new page
- [ ] Output process segments to the command line.
- [ ] Store process segments in the mongodb.

## Next

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
