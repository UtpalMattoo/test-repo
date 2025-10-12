# Dog Shelter Application

This is a full-stack dog adoption application that helps users find and adopt dogs. It's built as a monorepo with a Flask-based backend API and an Astro + Svelte frontend, designed for educational workshops and real-world usage.

## Project Structure

### Core Application
- **Backend**: `server/` - Flask API with SQLAlchemy ORM
- **Frontend**: `client/` - Astro framework with Svelte components
- **Backend Models**: `backend/` - Additional backend utilities and models
- **Database**: SQLite with seeded sample data (dogs, breeds, adoption applications)

### Supporting Infrastructure
- **Components**: `components/` - Reusable UI components
- **Content**: `content/` - Educational materials and workshop guides
- **Pages**: `pages/` - Static pages and documentation
- **Styles**: `styles/` - Global stylesheets and design tokens
- **Scripts**: `scripts/` - Build and deployment automation scripts
- **Specs**: `specs/` - Technical specifications and planning documents

### Configuration & Tooling
- **Root Files**: 
  - `pyproject.toml` - Python project configuration and dependencies
  - `package.json` - Node.js dependencies and scripts
  - `dog_validator.py` - Standalone validation utilities
  - `run_tests.py` - Test execution script
- **Development**: 
  - `.devcontainer/` - VS Code development container configuration
  - `.vscode/` - VS Code workspace settings
  - `.specify/` - Project specifications and requirements

## Backend Guidelines

### Framework & Architecture
- Built using Flask with SQLAlchemy ORM
- RESTful API design with proper HTTP status codes
- Database models in `server/models/` directory
- API routes organized in `server/routes/` directory
- Utility functions in `server/utils/`

### Code Standards
- **Always use type hints** for function parameters and return types
- Follow PEP8 conventions for Python code formatting
- Use descriptive variable names for educational clarity
- Include docstrings for all classes and functions
- Implement proper error handling with meaningful error messages

### Database
- Use SQLAlchemy models with proper relationships
- Implement database migrations when schema changes
- Seed data should be realistic and diverse for demonstration

## Frontend Guidelines

### Framework & Architecture
- Built using Astro static site generator with Svelte components
- Component-based architecture in `client/src/components/`
- Pages in `client/src/pages/`
- Shared layouts in `client/src/layouts/`

### Code Standards
- **TypeScript should use arrow functions** rather than the function keyword
- Use TypeScript for type safety across all components
- Implement proper component props typing
- Follow Astro's island architecture principles

### Design & UX
- **Pages should be in dark mode** with a modern look and feel
- Responsive design that works on mobile and desktop
- Accessible components with proper ARIA labels
- Clean, intuitive navigation and user experience
- Use consistent spacing and typography

## Testing Requirements

### Backend Testing
- Unit tests are mandatory for all API routes using pytest
- Test files should be co-located with the code being tested
- Use proper database mocking and fixtures
- Test both success and error scenarios
- Maintain test coverage above 80%

### Frontend Testing
- End-to-end tests using Playwright in `client/e2e-tests/`
- Test user workflows and critical paths
- API integration testing for frontend-backend communication
- Component unit tests for complex business logic

## Development Workflow

### Code Quality
- All code should be educational and well-commented for workshop participants
- Use meaningful commit messages following conventional commit format
- Implement proper validation for all user inputs
- Handle edge cases gracefully with user-friendly error messages

### API Design
- RESTful endpoints with consistent naming conventions
- Proper HTTP methods (GET, POST, PUT, DELETE)
- JSON request/response format with clear data structures
- API documentation should be clear and comprehensive

### Performance
- Optimize database queries to avoid N+1 problems
- Implement proper caching strategies where appropriate
- Minimize bundle sizes for frontend assets
- Use lazy loading for images and non-critical components
