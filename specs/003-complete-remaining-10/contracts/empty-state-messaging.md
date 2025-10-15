# Empty State Messaging Contract: Context-Aware User Experience

**Contract Type**: UX Enhancement  
**Target**: `client/src/components/DogList.svelte`  
**Scope**: Implement filter-aware empty state messages

## Contract Requirements

### Input Contract (Current State Analysis)
```typescript
// Available state data (already implemented)
dogs: Dog[] = [];              // Empty when no results
availableOnly: boolean;        // Filter state
showUnavailable: boolean;      // Filter state
searchTerm: string;           // Search state
totalDogs: number;            // Result count
loading: boolean;             // Loading state
```

### Output Contract (Required Enhancement)
```svelte
<!-- REQUIRED: Context-aware empty state messages -->
{#if !loading && dogs.length === 0}
  <div class="text-center py-12 text-slate-400">
    {@const emptyMessage = getEmptyStateMessage(availableOnly, showUnavailable, searchTerm, totalDogs)}
    <p class="text-lg mb-2">{emptyMessage.title}</p>
    <p class="text-sm">{emptyMessage.subtitle}</p>
  </div>
{/if}
```

### Message Logic Contract
```typescript
// REQUIRED: Context-aware message generation function
const getEmptyStateMessage = (
  availableOnly: boolean, 
  showUnavailable: boolean, 
  searchTerm: string,
  totalDogs: number
): { title: string; subtitle: string } => {
  
  // Filter context analysis
  if (availableOnly && !showUnavailable) {
    return {
      title: "No available dogs found",
      subtitle: searchTerm ? 
        `Try adjusting your search or check "Show unavailable dogs"` :
        `Check "Show unavailable dogs" to see all dogs`
    };
  }
  
  if (showUnavailable && !availableOnly) {
    return {
      title: "No unavailable dogs found", 
      subtitle: "All dogs are currently available for adoption!"
    };
  }
  
  if (availableOnly && showUnavailable) {
    return {
      title: "No dogs found",
      subtitle: searchTerm ? 
        "Try adjusting your search terms" :
        "No dogs match your current filters"
    };
  }
  
  // Both filters off (should not happen in normal flow)
  return {
    title: "No dogs found",
    subtitle: "Try selecting availability filters above"
  };
};
```

## Context Mapping Contract

### Filter State → Message Mapping
| Available | Unavailable | Search | Message Context |
|-----------|-------------|---------|-----------------|
| ✅ | ❌ | ❌ | "No available dogs found" |
| ✅ | ❌ | ✅ | "No available dogs match search" |
| ❌ | ✅ | ❌ | "No unavailable dogs found" |  
| ❌ | ✅ | ✅ | "No unavailable dogs match search" |
| ✅ | ✅ | ❌ | "No dogs found" |
| ✅ | ✅ | ✅ | "No dogs match search" |
| ❌ | ❌ | * | "Select availability filters" |

### User Experience Contract
```typescript
// Message tone and helpfulness requirements
interface MessageRequirements {
  clarity: "Messages must clearly explain why no results appear";
  actionability: "Messages should suggest next steps where appropriate";  
  consistency: "Message format consistent with existing dark mode design";
  context: "Messages must reflect active filter and search state";
}
```

## Integration Contract

### State Management Integration ✅ EXISTING
```typescript
// Filter states already reactive and persistent
$: availableOnly, debouncedSearch();     // Already implemented
$: showUnavailable, debouncedSearch();   // Already implemented  
$: searchTerm, debouncedSearch();        // Already implemented
```

### API Response Integration ✅ EXISTING
```typescript
// Result data already available
interface DogResponse {
  dogs: Dog[];        // Empty array when no results
  total: number;      // 0 when no results  
  pages: number;      // 0 when no results
  current_page: number;
}
```

### Styling Integration Contract
```css
/* Empty state styling (consistent with existing patterns) */
.text-center .py-12 .text-slate-400   /* Container styling */
.text-lg .mb-2                        /* Title styling */  
.text-sm                              /* Subtitle styling */
```

## Error State Contract

### Loading State Handling ✅ EXISTING
```svelte
<!-- Must not show empty message during loading -->
{#if !loading && dogs.length === 0}
  <!-- Empty state message -->
{/if}
```

### Network Error Handling ✅ EXISTING  
```typescript
// Existing error handling preserved
error: string | null = null;  // Already implemented
// Network errors show separate error UI, not empty state
```

## Accessibility Contract

### Screen Reader Requirements
```html
<!-- REQUIRED: Semantic HTML for empty states -->
<div role="status" aria-live="polite" class="text-center py-12 text-slate-400">
  <p class="text-lg mb-2">{emptyMessage.title}</p>
  <p class="text-sm">{emptyMessage.subtitle}</p>
</div>
```

### Keyboard Navigation
- ✅ Empty state content must be readable by screen readers
- ✅ Focus management unaffected by empty state display
- ✅ Tab navigation continues to work normally

## Performance Contract

### Computation Efficiency
```typescript  
// Message computation must be lightweight
// Use reactive statements for optimal Svelte performance
$: emptyMessage = getEmptyStateMessage(availableOnly, showUnavailable, searchTerm, totalDogs);
```

### Memory Usage
- ✅ No additional state storage required
- ✅ Messages computed on-demand from existing state
- ✅ No caching or persistence needed

## Testing Contract

### Manual Testing Scenarios
```gherkin
Scenario: Available only filter with no results
  Given I check "Show only available dogs"  
  And I uncheck "Show unavailable dogs"
  When no available dogs exist
  Then I see "No available dogs found"

Scenario: Unavailable only filter with no results  
  Given I uncheck "Show only available dogs"
  And I check "Show unavailable dogs"  
  When no unavailable dogs exist
  Then I see "No unavailable dogs found"

Scenario: Search with no results
  Given I have both filters enabled
  When I search for "nonexistent"
  Then I see "No dogs match search"
```

### E2E Test Integration
```typescript
// Tests must validate contextual messaging
test('Empty state shows appropriate message for active filters', async ({ page }) => {
  // Test implementation validates message content matches filter state
});
```

## Acceptance Criteria
1. ✅ Empty state messages reflect active filter context
2. ✅ Messages provide helpful guidance to users
3. ✅ Message display only when not loading and no results
4. ✅ Messages accessible to screen readers  
5. ✅ Styling consistent with dark mode design
6. ✅ No performance impact on normal usage
7. ✅ All filter combinations have appropriate messages

**Implementation Size**: 20-30 lines (helper function + template integration)
**Risk Level**: Low (pure UX enhancement)  
**Dependencies**: Existing filter state variables