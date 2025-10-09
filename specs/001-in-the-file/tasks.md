# Tasks: Dog Adoption Application Form

**Input**: De- [x] T011 [P] AdoptionApplication model in server/models/adoption_application.py
- [x] T012 Update Dog model relationships in server/models/dog.pygn documents from `/specs/001-in-the-file/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory ✓
   → Tech stack: Python 3.12 (backend), TypeScript (frontend)
   → Libraries: Flask, SQLAlchemy, Astro, Svelte, Playwright
   → Structure: server/ (backend), client/ (frontend)
2. Load optional design documents: ✓
   → data-model.md: AdoptionApplication entity
   → contracts/: POST /api/dogs/{id}/applications, GET /api/applications, updated GET /api/dogs/{id}
   → research.md: Database strategy, validation approach, UI patterns
3. Generate tasks by category: ✓
   → Setup: database schema, dependencies
   → Tests: contract tests, integration tests  
   → Core: models, API endpoints, form components
   → Integration: form validation, UI integration
   → Polish: E2E tests, error handling refinements
4. Apply task rules: ✓
   → Different files = [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...) ✓
6. Generate dependency graph ✓
7. Create parallel execution examples ✓
8. Validate task completeness: ✓
   → All contracts have tests ✓
   → All entities have models ✓
   → All endpoints implemented ✓
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup
- [x] T001 Create adoption_applications table in server/models/__init__.py database initialization
- [x] T002 [P] Update server/requirements.txt with any new dependencies (if needed)
- [x] T003 [P] Update client/package.json with any new dependencies (if needed)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T004 [P] Contract test POST /api/dogs/{dog_id}/applications in server/test_adoption_applications.py
- [x] T005 [P] Contract test GET /api/applications in server/test_adoption_applications.py
- [x] T006 [P] Contract test updated GET /api/dogs/{id} with has_application field in server/test_app.py
- [x] T007 [P] Integration test successful application submission in client/e2e-tests/adoption-form.spec.ts
- [x] T008 [P] Integration test form validation errors in client/e2e-tests/adoption-form.spec.ts
- [x] T009 [P] Integration test dog with existing application in client/e2e-tests/adoption-form.spec.ts
- [x] T010 [P] Integration test staff applications view in client/e2e-tests/adoption-form.spec.ts

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T011 [P] AdoptionApplication model in server/models/adoption_application.py
- [ ] T012 Update Dog model relationships in server/models/dog.py
- [x] T013 POST /api/dogs/{dog_id}/applications endpoint in server/app.py
- [x] T014 GET /api/applications endpoint in server/app.py  
- [x] T015 Update GET /api/dogs/{id} endpoint with has_application field in server/app.py
- [x] T016 [P] AdoptionForm.svelte component in client/src/components/AdoptionForm.svelte
- [x] T017 Update DogDetails.svelte component to integrate adoption form in client/src/components/DogDetails.svelte
- [x] T018 [P] Form styling for dark mode in client/src/styles/global.css

## Phase 3.4: Integration & Validation
- [x] T019 Email validation function in server/utils/validation.py
- [x] T020 Phone validation function (US format) in server/utils/validation.py
- [x] T021 Form field validation in client/src/components/AdoptionForm.svelte
- [x] T022 Loading state and error handling in client/src/components/AdoptionForm.svelte
- [x] T023 Success message display in client/src/components/AdoptionForm.svelte
- [x] T024 "Has an application" message display in client/src/components/DogDetails.svelte

## Phase 3.5: Polish
- [x] T025 [P] Additional unit tests for AdoptionApplication model validation in server/test_adoption_applications.py
- [x] T026 [P] Additional unit tests for validation utilities in server/test_validation.py
- [x] T027 [P] Edge case E2E tests (network errors, long inputs) in client/e2e-tests/adoption-form.spec.ts
- [x] T028 [P] Update client/README.md with new component documentation
- [x] T029 Manual testing following quickstart.md scenarios
- [x] T030 Code review and refactoring for constitutional compliance

## Dependencies
- Setup (T001-T003) before all other tasks
- Tests (T004-T010) before implementation (T011-T018)
- T011 (AdoptionApplication model) before T013, T014 (endpoints using the model)
- T012 (Dog model update) before T015 (endpoint using has_application)
- T016 (AdoptionForm component) before T017 (DogDetails integration)
- T016, T017 before T021-T024 (validation and UI behavior)
- Core implementation (T011-T018) before integration (T019-T024)
- All implementation before polish (T025-T030)

## Parallel Execution Examples

### Tests Phase (T004-T010) - All can run together:
```
Task: "Contract test POST /api/dogs/{dog_id}/applications in server/test_adoption_applications.py"
Task: "Contract test GET /api/applications in server/test_adoption_applications.py"  
Task: "Contract test updated GET /api/dogs/{id} with has_application field in server/test_app.py"
Task: "Integration test successful application submission in client/e2e-tests/adoption-form.spec.ts"
Task: "Integration test form validation errors in client/e2e-tests/adoption-form.spec.ts"
Task: "Integration test dog with existing application in client/e2e-tests/adoption-form.spec.ts"
Task: "Integration test staff applications view in client/e2e-tests/adoption-form.spec.ts"
```

### Core Models Phase (T011, T016, T018) - Different files, can run together:
```
Task: "AdoptionApplication model in server/models/adoption_application.py"
Task: "AdoptionForm.svelte component in client/src/components/AdoptionForm.svelte"
Task: "Form styling for dark mode in client/src/styles/global.css"
```

### Polish Phase (T025-T028) - Documentation and additional tests:
```
Task: "Additional unit tests for AdoptionApplication model validation in server/test_adoption_applications.py"
Task: "Additional unit tests for validation utilities in server/test_validation.py" 
Task: "Edge case E2E tests (network errors, long inputs) in client/e2e-tests/adoption-form.spec.ts"
Task: "Update client/README.md with new component documentation"
```

## Constitutional Compliance Requirements
- All Python code must use type hints (T011, T012, T013, T014, T015, T019, T020)
- All TypeScript code must use arrow functions (T016, T017, T021, T022, T023, T024)
- All backend tests must mock database calls (T004, T005, T006, T025, T026)
- Frontend must maintain dark mode design (T016, T017, T018)
- All validation follows clarified requirements (email format, US phone, 50 char name limit)

## Notes
- [P] tasks = different files, no dependencies between them
- Verify all tests fail before implementing (TDD requirement)
- Commit after each completed task
- Follow existing code patterns in server/app.py and client/src/components/
- Phone validation: Accept (555) 123-4567, 555-123-4567, 5551234567 formats
- Name validation: 2-50 characters as clarified in spec
- One application per dog enforced via database unique constraint + UI logic

## Validation Checklist
*GATE: Checked before execution*

- [x] All contracts have corresponding tests (T004, T005, T006)
- [x] All entities have model tasks (T011 for AdoptionApplication)
- [x] All tests come before implementation (T004-T010 before T011-T018)
- [x] Parallel tasks truly independent (different files marked [P])
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
- [x] All clarifications from spec incorporated (phone format, field limits, messages)
- [x] Constitutional requirements specified for each task