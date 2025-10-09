<!--
Sync Impact Report:
- Updated: 2025-10-05
- Project: Tailspin Shelter
- Impact: Initial constitution creation from project analysis
- Dependencies: .github/copilot-instructions.md aligned
- Status: All placeholders filled, ready for use
-->

# Tailspin Shelter Constitution

## Core Principles

### I. Monorepo Architecture
The project maintains a single repository structure containing both backend (Flask/SQLAlchemy) and frontend (Astro/Svelte) components. All code organization follows clear separation of concerns with dedicated directories for server, client, content, and shared utilities. Legacy directories (backend/, components/, pages/, styles/) may exist but active development focuses on server/ and client/ structure.

### II. Code Quality Standards (NON-NEGOTIABLE)
Python backend code must use type hints throughout and follow PEP8 standards. TypeScript/JavaScript frontend code must use arrow functions rather than the function keyword. All backend routes require unit tests with database calls properly mocked. Frontend components must maintain dark mode design with modern terminal-inspired aesthetics using Tailwind CSS.

### III. Learning-First Development
All development decisions prioritize educational value and workshop compatibility. Code must be approachable for learners while demonstrating industry best practices. Features should showcase GitHub Copilot capabilities, DevOps workflows, and modern web development patterns. Documentation must support both guided learning and independent exploration.

### IV. Test-Driven Quality Assurance
Backend unit tests are mandatory for all API routes with proper database mocking. Frontend requires Playwright end-to-end tests covering user workflows and API integration. Tests must be maintained alongside feature development and serve as living documentation of expected behavior.

### V. AI-Assisted Development
The project leverages GitHub Copilot and SpeckKit for specification-driven development. All code must align with .github/copilot-instructions.md standards. AI tools should accelerate development while maintaining code quality and educational clarity. Prompt engineering and context management are key project competencies.

## Technology Stack Requirements

**Backend Stack**: Flask (Python web framework), SQLAlchemy (ORM), type hints mandatory, PEP8 compliance required. Unit testing with mocked database calls using Python unittest framework.

**Frontend Stack**: Astro (static site generator), Svelte (UI framework), TypeScript with arrow functions, Tailwind CSS for styling. Dark mode design mandatory with modern terminal-inspired aesthetics. Playwright for end-to-end testing.

**DevOps & Automation**: GitHub Actions for CI/CD workflows, Dependabot for dependency management, VS Code settings for development consistency. All changes managed via pull requests with automated testing gates.

## Development Workflow

**Code Organization**: Active development in server/ (backend) and client/ (frontend) directories. Legacy structures (backend/, components/, pages/, styles/) maintained for compatibility but not actively developed.

**Quality Gates**: All backend routes require unit tests with database mocking. Frontend changes require E2E test coverage. Code must pass automated linting and type checking before merge.

**Learning Integration**: All features must include workshop-compatible documentation. Changes should demonstrate best practices suitable for educational content. GitHub Copilot suggestions must align with established coding standards.

## Governance

This constitution supersedes all other development practices and guidelines. All pull requests and code reviews must verify compliance with these principles. Contributors must follow CONTRIBUTING.md and CODE_OF_CONDUCT.md while adhering to constitutional requirements.

**Amendment Process**: Constitutional changes require documentation of rationale, impact assessment, and migration plan. Major principle changes require maintainer consensus via GitHub issues and pull request discussion.

**Enforcement**: Automated tooling (GitHub Actions, linting, testing) enforces technical standards. Human review ensures adherence to learning-first and code quality principles. Use .github/copilot-instructions.md for day-to-day development guidance.

**Conflict Resolution**: When conflicts arise between educational value and technical best practices, prioritize learning outcomes while maintaining code quality. Complex decisions require discussion in project issues with maintainer input.

**Version**: 1.0.0 | **Ratified**: 2025-10-05 | **Last Amended**: 2025-10-05