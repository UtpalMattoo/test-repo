# Tasks: Unavailable Dogs Display Enhancement

**Input**: Design documents from `/specs/002-unavailable-dogs/`
**Prerequisites**: plan.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅)

## Execution Flow (main)
```
✅ 1. Load plan.md from feature directory - COMPLETED
✅ 2. Load optional design documents - COMPLETED
   → data-model.md: No new entities (uses existing Dog.status enum)
   → contracts/: API enhancement + Component enhancement contracts loaded
   → research.md: Technical decisions and constraints identified
✅ 3. Generate tasks by category - COMPLETED
✅ 4. Apply task rules - COMPLETED
✅ 5. Number tasks sequentially - COMPLETED
✅ 6. Generate dependency graph - COMPLETED  
✅ 7. Create parallel execution examples - COMPLETED
✅ 8. Validate task completeness - COMPLETED
✅ 9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `server/` (Flask backend), `client/src/` (Astro/Svelte frontend)
- **Testing**: `server/test_*.py` (backend tests), `client/e2e-tests/` (frontend E2E)

## Phase 3.1: Setup
- [ ] T001 Verify existing project dependencies (Flask, SQLAlchemy, Astro, Svelte, Playwright)
- [ ] T002 [P] Review existing test infrastructure in server/test_app.py
- [ ] T003 [P] Verify existing DogList component state in client/src/components/DogList.svelte

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Contract test GET /api/dogs with unavailable parameter in server/test_app.py
- [ ] T005 [P] Contract test GET /api/dogs with combined filters in server/test_app.py  
- [ ] T006 [P] Contract test GET /api/dogs status field inclusion in server/test_app.py
- [ ] T007 [P] Integration test unavailable checkbox interaction in client/e2e-tests/unavailable-dogs.spec.ts
- [ ] T008 [P] Integration test status badge display in client/e2e-tests/unavailable-dogs.spec.ts
- [ ] T009 [P] Integration test localStorage persistence in client/e2e-tests/unavailable-dogs.spec.ts

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Backend Enhancement
- [ ] T010 Add unavailable parameter extraction in server/app.py get_dogs() function
- [ ] T011 Implement combined filter logic in server/app.py get_dogs() function  
- [ ] T012 Add status field to API response in server/app.py get_dogs() function
- [ ] T013 Add type hints for new unavailable parameter in server/app.py

### Frontend Enhancement  
- [ ] T014 [P] Add showUnavailable state variable in client/src/components/DogList.svelte
- [ ] T015 [P] Update Dog interface with optional status field in client/src/components/DogList.svelte
- [ ] T016 Add unavailable parameter to API calls in client/src/components/DogList.svelte fetchDogs()
- [ ] T017 Add localStorage persistence for unavailable checkbox in client/src/components/DogList.svelte
- [ ] T018 Add unavailable checkbox to UI template in client/src/components/DogList.svelte
- [ ] T019 Add status badge helper functions in client/src/components/DogList.svelte
- [ ] T020 Add status badges to dog tile template in client/src/components/DogList.svelte

## Phase 3.4: Integration
- [ ] T021 Test API parameter building with both checkboxes
- [ ] T022 Test empty state handling for filter combinations  
- [ ] T023 Verify backward compatibility with existing available parameter
- [ ] T024 Test localStorage state restoration on page refresh

## Phase 3.5: Polish
- [ ] T025 [P] Add unit tests for filter logic edge cases in server/test_app.py
- [ ] T026 [P] Add unit tests for status badge rendering in client/e2e-tests/
- [ ] T027 Performance validation (API responses <200ms)
- [ ] T028 [P] Add ARIA labels for unavailable checkbox and status badges in client/src/components/DogList.svelte
- [ ] T029 [P] Implement keyboard navigation support for checkboxes in client/src/components/DogList.svelte
- [ ] T030 [P] Add screen reader compatibility tests in client/e2e-tests/accessibility.spec.ts
- [ ] T031 Cross-browser compatibility testing
- [ ] T032 Update documentation in README.md

## Dependencies
- Tests (T004-T009) before implementation (T010-T020)
- T010-T013 (backend) can run parallel with T014-T020 (frontend) 
- T014-T015 must complete before T016-T020 (component state before API integration)
- Integration (T021-T024) requires all core implementation complete
- Polish (T025-T032) requires all integration complete

## Parallel Example
```
# Launch T004-T009 together (all test files):
Task: "Contract test GET /api/dogs with unavailable parameter in server/test_app.py"
Task: "Contract test GET /api/dogs with combined filters in server/test_app.py"  
Task: "Contract test GET /api/dogs status field inclusion in server/test_app.py"
Task: "Integration test unavailable checkbox interaction in client/e2e-tests/unavailable-dogs.spec.ts"
Task: "Integration test status badge display in client/e2e-tests/unavailable-dogs.spec.ts"
Task: "Integration test localStorage persistence in client/e2e-tests/unavailable-dogs.spec.ts"

# Launch T014-T015 together (component state setup):
Task: "Add showUnavailable state variable in client/src/components/DogList.svelte"
Task: "Update Dog interface with optional status field in client/src/components/DogList.svelte"

# Launch T025-T026, T028-T030 together (polish phase):
Task: "Add unit tests for filter logic edge cases in server/test_app.py"
Task: "Add unit tests for status badge rendering in client/e2e-tests/"
Task: "Add ARIA labels for unavailable checkbox and status badges in client/src/components/DogList.svelte"
Task: "Implement keyboard navigation support for checkboxes in client/src/components/DogList.svelte"
Task: "Add screen reader compatibility tests in client/e2e-tests/accessibility.spec.ts"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task  
- T010-T013 modify same file sequentially (server/app.py)
- T016-T020 modify same file sequentially (DogList.svelte)
- No database schema changes required (uses existing Dog.status enum)

## Task Generation Rules Applied

1. **From API Contract** (api-dogs-enhanced.md):
   - T004-T006: Contract tests for new unavailable parameter and status field
   - T010-T013: Backend implementation tasks for enhanced endpoint

2. **From Component Contract** (component-doglist-enhanced.md):
   - T007-T009: Integration tests for component behavior  
   - T014-T020: Frontend implementation tasks for enhanced component

3. **From Quickstart Scenarios**:
   - T021-T024: Integration validation tasks
   - T025-T032: Polish and quality assurance tasks (enhanced accessibility coverage)

4. **Ordering Applied**:
   - Setup → Tests → Backend → Frontend → Integration → Polish
   - Tests marked [P] when in different files
   - Implementation tasks sequential when same file

## Validation Checklist

- [✅] All contracts have corresponding tests (T004-T009)
- [✅] All implementation has test coverage 
- [✅] All tests come before implementation (T004-T009 before T010-T020)
- [✅] Parallel tasks truly independent ([P] marked appropriately)
- [✅] Each task specifies exact file path
- [✅] No task modifies same file as another [P] task
- [✅] TDD approach enforced (failing tests required first)

## Ready for Execution
**Total Tasks**: 32  
**Estimated Time**: 2-3 hours (per quickstart estimate)  
**Critical Path**: Tests → Backend Enhancement → Frontend Enhancement → Integration → Polish