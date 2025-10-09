# Research: Dog Adoption Application Form

## Technical Decisions

### Database Schema Design
**Decision**: Add new `adoption_applications` table with foreign key to existing `dogs` table  
**Rationale**: Clean separation of concerns, maintains referential integrity, allows for future application status tracking  
**Alternatives considered**: Adding fields directly to dogs table (rejected - violates normalization), separate applications database (rejected - unnecessary complexity for workshop scope)

### Form Validation Strategy
**Decision**: Client-side validation for UX + server-side validation for security  
**Rationale**: Constitutional requirement for user-friendly error handling while maintaining data integrity  
**Alternatives considered**: Server-side only (rejected - poor UX), client-side only (rejected - security risk)

### Phone Number Validation
**Decision**: US phone format validation (10 digits) with flexible formatting acceptance  
**Rationale**: Clarified in spec - supports common US formats while maintaining data consistency  
**Alternatives considered**: International format (rejected - out of scope), no validation (rejected - data quality issues)

### One Application Per Dog Enforcement
**Decision**: Database unique constraint + application check before form display  
**Rationale**: Data integrity at DB level + UX optimization by hiding unavailable forms  
**Alternatives considered**: Allow duplicates with post-processing (rejected - confusing UX), client-side only check (rejected - race conditions)

### UI/UX Loading States
**Decision**: Loading spinner with disabled submit button during form processing  
**Rationale**: Clarified in spec - prevents duplicate submissions while providing user feedback  
**Alternatives considered**: Redirect immediately (rejected - no user feedback), form overlay (rejected - overly complex)

## Technology Integration Patterns

### Flask-SQLAlchemy Model Design
- Follow existing project patterns in `server/models/`
- Use `BaseModel` class as seen in `dog.py`
- Implement proper relationships with existing `Dog` model
- Include validation methods following constitutional type hint requirements

### Svelte Component Architecture
- Create reusable `AdoptionForm.svelte` component
- Integrate into existing `DogDetails.svelte` component
- Follow constitutional arrow function requirements for TypeScript
- Maintain dark mode styling consistency with existing components

### API Endpoint Design
- RESTful endpoints following existing `server/app.py` patterns
- POST `/api/dogs/{id}/applications` for form submission
- GET `/api/applications` for staff view (read-only as clarified)
- Error handling consistent with existing error response patterns

### Testing Strategy
- Backend: Unit tests with database mocking (constitutional requirement)
- Frontend: Playwright E2E tests covering form submission flows
- Follow existing test patterns in `test_app.py` and `e2e-tests/`

## Constitutional Compliance Verification

### Code Quality Standards
- Python type hints: Required for all new backend code
- TypeScript arrow functions: Required for all new frontend code
- Dark mode design: Must integrate with existing terminal-inspired theme
- PEP8 compliance: Required for Python code

### Testing Requirements
- Backend routes: Unit tests with mocked database calls
- Frontend workflows: E2E tests with Playwright
- Test-driven development: Write failing tests first

### Educational Value
- Code must be approachable for workshop participants
- Demonstrate modern web development best practices
- Showcase GitHub Copilot integration capabilities
- Support guided learning objectives