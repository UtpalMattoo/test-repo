# GitHub Copilot Instructions: Unavailable Dogs Display Enhancement

**Feature Context**: Enhancing dog listing functionality with unavailable dog filtering and status display  
**Implementation Scope**: Backend API enhancement + Frontend component modification  
**Educational Focus**: Progressive enhancement of existing filtering system

## Implementation Guidelines for GitHub Copilot

### Backend Development Focus (`server/app.py`)

#### Enhance GET /api/dogs Endpoint
**Pattern to Follow**:
- Add `unavailable` parameter handling alongside existing `available` parameter  
- Implement combined filter logic: both checkboxes can be checked simultaneously
- Maintain backward compatibility - existing `available=true` behavior unchanged
- Include `status` field in response JSON for all dogs

**Code Quality Standards**:
- **Type hints mandatory**: All new parameters and variables must have type annotations
- **PEP8 compliance**: Follow existing code formatting and naming conventions  
- **Error handling**: Graceful parameter validation, ignore invalid values
- **Educational clarity**: Comments explaining filter logic for workshop participants

**Expected Enhancement Pattern**:
```python
# Add to parameter extraction section
unavailable: Optional[str] = request.args.get('unavailable')

# Filter logic enhancement  
if available == 'true' and unavailable == 'true':
    # Show all dogs - no status filter needed
elif available == 'true' and unavailable != 'true':  
    query = query.filter(Dog.status == 'AVAILABLE')
elif unavailable == 'true' and available != 'true':
    query = query.filter(Dog.status != 'AVAILABLE')
```

#### Unit Testing Requirements
- Test new `unavailable` parameter handling in isolation
- Test combined `available=true&unavailable=true` scenario  
- Verify `status` field inclusion in response JSON
- Use proper database mocking following existing test patterns

### Frontend Development Focus (`client/src/components/DogList.svelte`)

#### Component State Enhancement  
**Pattern to Follow**:
- Add `showUnavailable: boolean = false` state variable
- Extend localStorage persistence to include unavailable preference
- Follow existing checkbox patterns for UI consistency  
- Maintain dark mode styling with Tailwind CSS classes

**TypeScript Standards**:  
- **Arrow functions mandatory**: Use arrow functions, not function keyword
- **Interface enhancement**: Add optional `status` field to Dog interface
- **Type safety**: Ensure proper typing for new state variables and API responses

**Expected State Management Pattern**:
```typescript
// New state variable
let showUnavailable: boolean = false;

// Enhanced Dog interface
interface Dog {
    id: number;
    name: string;
    breed: string;  
    status?: 'AVAILABLE' | 'PENDING' | 'ADOPTED';  // New optional field
}

// Reactive dependency for new checkbox
$: showUnavailable, debouncedSearch();
```

#### UI Enhancement Requirements
- Add second checkbox following existing styling patterns
- Implement always-visible status badges on dog tiles  
- Use green (available), amber (pending), red (adopted) color scheme
- Position status badges in top-right corner of dog tiles
- Maintain responsive design and hover effects

**Expected Template Pattern**:
```svelte
<!-- New checkbox following existing pattern -->
<div class="flex items-center mb-2">
    <input type="checkbox" bind:checked={showUnavailable} id="showUnavailable" class="mr-2 accent-blue-500" />
    <label for="showUnavailable" class="text-slate-300">Show unavailable dogs</label>
</div>

<!-- Status badge on dog tiles -->  
{#if dog.status}
    <span class="text-sm px-3 py-1 rounded-full {getStatusBadgeClass(dog.status)}">
        {getStatusBadgeText(dog.status)}
    </span>
{/if}
```

### Integration Requirements

#### API Parameter Building
- Extend existing parameter building logic in `fetchDogs()` method
- Add `unavailable=true` parameter when `showUnavailable` checkbox checked
- Maintain all existing parameters (search, breed_id, available, pagination)
- Follow existing URLSearchParams pattern

#### localStorage Persistence  
- Add `'dogShowUnavailable'` key for unavailable checkbox state
- Follow existing boolean to string conversion pattern (`'true'|'false'`)  
- Restore state on component mount following existing patterns
- Update persistence in debounced search function

#### Status Badge Implementation
- Create helper functions for badge styling and text  
- Use existing Tailwind color classes with `/20` opacity backgrounds
- Implement consistent with existing DogDetails component badge styling
- Ensure accessibility with proper aria-labels

### Testing Integration

#### Backend Testing Patterns
- Follow existing test structure in `server/test_app.py`  
- Use proper database mocking with existing fixtures
- Test parameter combinations systematically
- Verify response format consistency

#### Frontend Testing Patterns  
- Extend existing Playwright E2E tests if present
- Test checkbox interaction workflows
- Verify localStorage persistence across page refreshes
- Test empty state scenarios with different filter combinations

### Educational Workshop Compatibility

#### Code Clarity for Learning
- Add explanatory comments for filter logic decisions  
- Use descriptive variable names for checkbox states and API parameters
- Implement progressive enhancement - new features build on existing patterns
- Maintain clear separation between available and unavailable filtering logic

#### GitHub Copilot Showcase Opportunities  
- Demonstrate API enhancement patterns
- Show component state management best practices
- Illustrate localStorage persistence techniques  
- Highlight TypeScript interface evolution

### Performance and Accessibility

#### Performance Requirements
- Maintain existing API response times (<200ms target)  
- Use debounced search pattern for checkbox changes (300ms delay)
- Preserve pagination performance with enhanced filtering
- Minimize re-renders through proper reactive dependencies

#### Accessibility Standards
- Include proper ARIA labels for new checkboxes and status badges
- Maintain keyboard navigation support  
- Use text + color indicators for status (not color alone)
- Ensure screen reader compatibility for status announcements

### Implementation Sequence for Copilot

1. **Backend First**: Enhance `/api/dogs` endpoint with `unavailable` parameter and `status` field
2. **Backend Testing**: Add unit tests for new parameter handling  
3. **Frontend State**: Add `showUnavailable` state and localStorage integration
4. **Frontend UI**: Add unavailable checkbox to filter controls  
5. **Frontend Display**: Implement status badges on dog tiles
6. **Integration Testing**: Verify end-to-end functionality and edge cases

### Common Pitfalls to Avoid
- **Don't break existing behavior**: `available=true` alone must still work as before
- **Don't ignore empty states**: Handle scenarios where filters return no results  
- **Don't forget accessibility**: Include ARIA labels and screen reader support
- **Don't skip localStorage**: New checkbox state must persist across sessions
- **Don't hardcode colors**: Use existing Tailwind color scheme patterns

---

**GitHub Copilot Focus**: Progressive enhancement of existing filtering system with educational clarity and workshop compatibility. Maintain all constitutional requirements while demonstrating modern web development patterns.