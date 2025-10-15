# Frontend Component Contract: DogList.svelte Enhancement

**Contract Type**: Template Enhancement  
**Target**: `client/src/components/DogList.svelte`  
**Scope**: Complete status badge rendering (lines ~222-225)

## Contract Requirements

### Input Contract ✅ STABLE (No Changes)
```typescript
// Component receives dogs array from API
dogs: Dog[] = [
  {
    id: number,
    name: string, 
    breed: string,
    status?: 'AVAILABLE' | 'PENDING' | 'ADOPTED'  // Already available
  }
]

// Helper function available
getStatusBadge(dog: Dog): { text: string; class: string }  // Already implemented
```

### Output Contract (Template Enhancement Required)
```svelte
<!-- REQUIRED: Add status badge to each dog tile -->
{#each dogs as dog (dog.id)}
  <a href={`/dog/${dog.id}`} class="group block ...">
    <div class="p-6 relative">
      <div class="relative z-10">
        <h3 class="text-xl font-semibold text-slate-100 mb-2 ...">
          {dog.name}
        </h3>
        <p class="text-slate-400 mb-4">{dog.breed}</p>
        
        <!-- NEW REQUIREMENT: Status badge rendering -->
        <div class="mb-3">
          {@const badge = getStatusBadge(dog)}
          <span class="inline-block px-2 py-1 rounded-full text-xs font-medium text-white {badge.class}">
            {badge.text}
          </span>
        </div>
        
        <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
          <span>View details</span>
          <!-- ... existing arrow SVG ... -->
        </div>
      </div>
    </div>
  </a>
{/each}
```

### Styling Contract
```css
/* Badge Classes (already defined in getStatusBadge helper) */
.bg-green-600  /* AVAILABLE status */
.bg-yellow-600 /* PENDING status */  
.bg-gray-600   /* ADOPTED status */

/* Layout Classes (Tailwind - already available) */
.inline-block .px-2 .py-1 .rounded-full .text-xs .font-medium .text-white .mb-3
```

### Behavioral Contract
- **Badge Display**: Must appear on ALL dog tiles regardless of filter state
- **Status Fallback**: Show "AVAILABLE" when `dog.status` is undefined
- **Visual Consistency**: Follow existing dark mode design patterns
- **Accessibility**: Use semantic HTML with clear text labels

## Integration Points

### API Integration Contract ✅ COMPLETE
```typescript
// Dogs array populated from API with status field
fetchDogs() → dogs: Dog[] (with status field included)
```

### State Management Contract ✅ COMPLETE  
```typescript
// Filter states already working
availableOnly: boolean     // Controls "available=true" API parameter
showUnavailable: boolean   // Controls "unavailable=true" API parameter
```

### Helper Function Contract ✅ COMPLETE
```typescript
// Badge generator already implemented
getStatusBadge(dog: Dog): { text: string; class: string }
// Returns appropriate badge styling based on dog.status
```

## Error Handling Contract
```typescript
// Handle missing status gracefully (already implemented in helper)
if (!dog.status) return { text: 'AVAILABLE', class: 'bg-green-600' };
```

## Performance Contract
- **Rendering**: Use Svelte's `{@const}` for efficient computed values
- **No Re-computation**: Badge calculation only when dog data changes
- **Memory**: No additional state variables required

## Testing Contract Requirements
```typescript
// E2E test validation (existing tests in unavailable-dogs.spec.ts)
test('Status badges appear on all dog cards') // Must pass after implementation
test('Badge colors match status values')      // Must pass after implementation
test('Badges visible regardless of filters') // Must pass after implementation
```

## Acceptance Criteria
1. ✅ Status badge appears on every dog tile
2. ✅ Badge text shows correct status ("AVAILABLE", "PENDING", "ADOPTED")
3. ✅ Badge color matches status (green/yellow/gray)
4. ✅ Badges display regardless of active filter checkboxes
5. ✅ Default "AVAILABLE" badge for dogs without status
6. ✅ Existing functionality unchanged
7. ✅ Dark mode styling maintained
8. ✅ E2E tests pass after implementation

**Implementation Size**: 4-5 lines of Svelte template code
**Risk Level**: Minimal (template-only change)
**Dependencies**: None (all prerequisites complete)