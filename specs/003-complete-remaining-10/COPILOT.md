# GitHub Copilot Instructions: Complete Unavailable Dogs Feature (Final 10%)

**Context**: This document provides specific guidance for GitHub Copilot to assist with completing the final 10% of the unavailable dogs feature implementation.

## Current Implementation Status ✅

### Completed (90%)
- ✅ Backend API enhanced with `unavailable` parameter support
- ✅ Backend unit tests passing (3 new contract tests)  
- ✅ Frontend checkbox implementation and state management
- ✅ API integration with parameter passing
- ✅ localStorage persistence for filter states
- ✅ TypeScript interfaces updated with status field
- ✅ Helper function `getStatusBadge()` implemented
- ✅ E2E test scenarios written in `unavailable-dogs.spec.ts`

### Remaining Tasks (10%)
1. **Status Badge Rendering**: Add 4-5 lines to dog tile template
2. **Playwright Configuration**: Fix Windows compatibility (1-line change)  
3. **Empty State Messages**: Context-aware messaging (helper function + template)

## Implementation Guidelines

### 1. Status Badge Rendering
**File**: `client/src/components/DogList.svelte`  
**Location**: Dog tile template (around line 222-225)

```svelte
<!-- Add status badge after breed, before "View details" -->
<div class="mb-3">
  {@const badge = getStatusBadge(dog)}
  <span class="inline-block px-2 py-1 rounded-full text-xs font-medium text-white {badge.class}">
    {badge.text}
  </span>
</div>
```

**Copilot Prompt**: "Add status badge rendering to dog tile using existing getStatusBadge helper"

### 2. Playwright Configuration Fix
**File**: `client/playwright.config.ts`  
**Target**: Replace bash script with npm command

```typescript
// Change from:
command: 'cd .. && ./scripts/start-app.sh',
// To:
command: 'npm run dev',
```

**Copilot Prompt**: "Fix webServer command in playwright.config.ts for Windows compatibility"

### 3. Empty State Messages  
**File**: `client/src/components/DogList.svelte`

```typescript
// Add helper function for context-aware messages
const getEmptyStateMessage = (availableOnly: boolean, showUnavailable: boolean, searchTerm: string) => {
  // Return appropriate message based on filter context
};
```

```svelte
<!-- Update empty state template -->
{#if !loading && dogs.length === 0}
  <div class="text-center py-12 text-slate-400">
    {@const emptyMessage = getEmptyStateMessage(availableOnly, showUnavailable, searchTerm)}
    <p class="text-lg mb-2">{emptyMessage.title}</p>
    <p class="text-sm">{emptyMessage.subtitle}</p>
  </div>
{/if}
```

**Copilot Prompt**: "Add context-aware empty state messages based on active filter state"

## Code Quality Standards

### TypeScript/Svelte Requirements ✅
- **Arrow Functions**: Use arrow functions for all new function definitions
- **Dark Mode**: Maintain existing Tailwind CSS dark theme classes
- **Type Safety**: Use existing TypeScript interfaces (Dog, DogResponse)
- **Reactivity**: Leverage Svelte's reactive statements (`$:`, `{@const}`)

### Constitutional Compliance ✅
- **No Breaking Changes**: All modifications are additive only
- **Test Coverage**: E2E tests already exist, just need to execute
- **Educational Value**: Changes demonstrate template completion and config fixes
- **Performance**: Minimal impact, client-side only enhancements

## Testing Strategy

### Manual Testing
```bash
# Ensure servers running
cd server && python app.py     # http://localhost:5100
cd client && npm run dev       # http://localhost:4321

# Browser testing at http://localhost:4321
- Test all checkbox combinations
- Verify status badges on all dogs  
- Check empty state messages
```

### Automated Testing
```bash
# After Playwright fix
cd client && npx playwright test e2e-tests/unavailable-dogs.spec.ts
```

## Copilot Context Optimization

### Key Context Points
- **Feature Scope**: Completing existing implementation, not adding new features
- **Time Constraint**: ~1 hour total implementation
- **Risk Level**: Minimal (template + config changes only)
- **Dependencies**: All backend work complete, helper functions exist

### Suggested Copilot Workflow
1. **Status Badges**: Focus on template integration of existing helper
2. **Playwright Fix**: Simple configuration change for cross-platform support  
3. **Empty States**: Context-aware UX improvement without functionality changes
4. **Validation**: Ensure no regressions to existing 90% implementation

### Files NOT to Modify
- ❌ `server/app.py` (backend complete)
- ❌ `server/test_app.py` (tests passing)  
- ❌ Backend models or database schema
- ❌ API endpoints or data structures
- ❌ Component props or state variables

### Files to Focus On
- ✅ `client/src/components/DogList.svelte` (template completion)
- ✅ `client/playwright.config.ts` (configuration fix)

## Success Criteria for Copilot

### Visual Completion
- Status badges visible on every dog tile
- Correct color coding (green/yellow/gray)
- Consistent with dark mode design

### Testing Infrastructure  
- E2E tests execute without Windows compatibility errors
- All existing test scenarios pass

### User Experience
- Context-appropriate empty state messages
- Filter-aware messaging based on active checkboxes
- No confusion when filters return no results

**Implementation Constraint**: Stay within the 10% completion scope - no new features, no architectural changes, focus on finishing existing work.