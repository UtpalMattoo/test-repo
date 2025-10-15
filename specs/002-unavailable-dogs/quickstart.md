# Quickstart: Unavailable Dogs Display Enhancement

**Feature**: Add unavailable dogs filtering with always-visible status labels  
**Complexity**: Intermediate - Enhances existing filtering system with new checkbox and status display  
**Time Estimate**: 2-3 hours implementation + testing

## Feature Overview
This feature adds an "Show Unavailable Dogs" checkbox to the landing page alongside the existing "Show Available Dogs" checkbox, and displays status badges on all dog tiles regardless of filter state. Users can independently control both checkboxes to view available dogs, unavailable dogs, or all dogs with clear visual status indicators.

## Prerequisites  
- Flask backend running with existing dog shelter database
- Astro frontend with Svelte components operational  
- Existing dog listing and filtering functionality working
- Existing `/api/dogs/unavailable` endpoint available (unused)

## Implementation Steps

### Backend Enhancement (30 minutes)

#### Step 1: Enhance /api/dogs Endpoint
**File**: `server/app.py`

**Current Logic**:
```python
if available == 'true':
    query = query.filter(Dog.status == 'AVAILABLE')
```

**Enhanced Logic**:
```python
# Add after existing parameter extraction
unavailable: Optional[str] = request.args.get('unavailable')

# Replace existing available filter logic with:
if available == 'true' and unavailable == 'true':
    # Both checked - show all dogs (no status filter)
    pass
elif available == 'true' and unavailable != 'true':
    # Available only (existing behavior)
    query = query.filter(Dog.status == 'AVAILABLE') 
elif unavailable == 'true' and available != 'true':
    # Unavailable only (new functionality)  
    query = query.filter(Dog.status != 'AVAILABLE')
# else: neither checked - show all dogs (or empty, based on UX decision)
```

**Response Enhancement** - Add status to response:
```python
# In dogs_list comprehension, add:
dogs_list: List[Dict[str, Any]] = [
    {
        'id': dog.id,
        'name': dog.name, 
        'breed': dog.breed,
        'status': dog.status.name  # Add this line
    }
    for dog in paginated_dogs.items
]
```

#### Step 2: Add Backend Unit Tests  
**File**: `server/test_app.py` (or create new test file)

**Test Cases**:
```python
def test_get_dogs_unavailable_only():
    """Test unavailable=true parameter returns only unavailable dogs"""
    response = client.get('/api/dogs?unavailable=true')
    assert response.status_code == 200
    data = response.get_json()
    for dog in data['dogs']:
        assert dog['status'] in ['PENDING', 'ADOPTED']

def test_get_dogs_both_filters():
    """Test available=true&unavailable=true returns all dogs"""  
    response = client.get('/api/dogs?available=true&unavailable=true')
    assert response.status_code == 200
    data = response.get_json()
    # Should contain dogs with any status
    statuses = {dog['status'] for dog in data['dogs']}
    assert len(statuses) > 1  # Multiple statuses present

def test_get_dogs_includes_status():
    """Test that all dogs include status field"""
    response = client.get('/api/dogs')
    assert response.status_code == 200
    data = response.get_json()
    for dog in data['dogs']:
        assert 'status' in dog
        assert dog['status'] in ['AVAILABLE', 'PENDING', 'ADOPTED']
```

### Frontend Enhancement (60 minutes)

#### Step 3: Update DogList Component State
**File**: `client/src/components/DogList.svelte`

**Add State Variable** (after existing declarations):
```typescript
// Add new state variable
let showUnavailable: boolean = false;

// Update Dog interface (if needed)
interface Dog {
    id: number;
    name: string; 
    breed: string;
    status?: 'AVAILABLE' | 'PENDING' | 'ADOPTED';  // Add optional status
}
```

**Add localStorage Restoration** (in onMount):
```typescript
// Add after existing localStorage restoration
const savedUnavailable = localStorage.getItem('dogShowUnavailable');
if (savedUnavailable) showUnavailable = savedUnavailable === 'true';
```

**Add Reactive Dependency**:
```typescript  
// Add after existing reactive statements
$: showUnavailable, debouncedSearch();
```

#### Step 4: Update API Parameter Building
**In fetchDogs method**, add unavailable parameter:
```typescript
// Add after existing parameter logic
if (showUnavailable) params.append('unavailable', 'true');
```

**Update localStorage persistence** (in debouncedSearch):
```typescript
// Add after existing localStorage.setItem calls  
localStorage.setItem('dogShowUnavailable', showUnavailable ? 'true' : 'false');
```

#### Step 5: Add Unavailable Checkbox to UI
**In template**, add checkbox after existing available checkbox:
```svelte
<!-- After existing availability checkbox -->
<div class="flex items-center mb-2">
    <input
        type="checkbox" 
        bind:checked={showUnavailable}
        id="showUnavailable"
        class="mr-2 accent-blue-500"
    />
    <label for="showUnavailable" class="text-slate-300">Show unavailable dogs</label>
</div>
```

#### Step 6: Add Status Badges to Dog Tiles
**Add helper functions** (in script section):
```typescript
const getStatusBadgeClass = (status: string): string => {
    switch (status) {
        case 'AVAILABLE': return 'bg-green-500/20 text-green-400';
        case 'PENDING': return 'bg-amber-500/20 text-amber-400';  
        case 'ADOPTED': return 'bg-red-500/20 text-red-400';
        default: return 'bg-slate-500/20 text-slate-400';
    }
};

const getStatusBadgeText = (status: string): string => {
    switch (status) {
        case 'AVAILABLE': return 'Available';
        case 'PENDING': return 'Pending';
        case 'ADOPTED': return 'Adopted'; 
        default: return 'Unknown';
    }
};
```

**Update dog tile template** - add status badge to header:
```svelte
<!-- In dog tile template, update header section -->
<div class="flex justify-between items-start mb-2">
    <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors">{dog.name}</h3>
    
    <!-- Add status badge -->
    {#if dog.status}
        <span class="text-sm px-3 py-1 rounded-full {getStatusBadgeClass(dog.status)}">
            {getStatusBadgeText(dog.status)}
        </span>
    {/if}
</div>
```

### Testing & Validation (30 minutes)

#### Step 7: Frontend Testing  
**Manual Test Scenarios**:
1. **Default State**: Page loads with available dogs checkbox checked, unavailable unchecked
2. **Show Unavailable Only**: Check unavailable, uncheck available → see only pending/adopted dogs
3. **Show All Dogs**: Check both checkboxes → see all dogs with status badges
4. **Filter Persistence**: Refresh page → checkbox states restored from localStorage
5. **Empty States**: Test combinations that yield no results → appropriate messages

#### Step 8: API Testing
**Manual API Tests**:
```bash
# Test unavailable filter
curl "http://localhost:5100/api/dogs?unavailable=true"

# Test combined filters  
curl "http://localhost:5100/api/dogs?available=true&unavailable=true"

# Test status field inclusion
curl "http://localhost:5100/api/dogs" | jq '.dogs[0].status'
```

#### Step 9: Run Existing Tests
```bash
# Backend tests
cd server && python -m pytest test_app.py -v

# Frontend E2E tests (if applicable)  
cd client && npm run test:e2e
```

## Success Criteria
✅ Users can toggle "Show Unavailable Dogs" checkbox independently  
✅ Both checkboxes can be checked simultaneously to show all dogs  
✅ Status badges appear on all dog tiles regardless of filter state  
✅ Checkbox states persist across page refreshes via localStorage  
✅ API returns consistent response format with status information  
✅ Empty states show appropriate context-aware messages  
✅ All existing functionality continues to work unchanged  
✅ Backend unit tests pass for new parameter handling  

## Troubleshooting

### Common Issues

**Issue**: Unavailable checkbox doesn't affect results  
**Solution**: Check API parameter building in fetchDogs() method - ensure `unavailable=true` parameter is added when checkbox checked

**Issue**: Status badges not appearing on dog tiles  
**Solution**: Verify API response includes `status` field, and check conditional rendering `{#if dog.status}` in template

**Issue**: Checkbox states not persisting  
**Solution**: Check localStorage key naming consistency between save/restore operations

**Issue**: Empty state shows generic message  
**Solution**: Implement context-aware empty state messaging based on checkbox combinations

### Performance Verification
- API responses should remain under 200ms
- Page interactions should feel immediate with debounced API calls  
- No console errors during checkbox interactions
- Smooth transitions for loading states

## Next Steps
After successful implementation:
1. **Add Playwright E2E tests** for checkbox interaction workflows
2. **Performance monitoring** to validate response time requirements
3. **Accessibility audit** to ensure screen reader compatibility  
4. **Cross-browser testing** for checkbox and badge rendering consistency

---

**Quickstart Status**: ✅ READY FOR IMPLEMENTATION  
**Estimated Total Time**: 2-3 hours including testing  
**Dependencies**: No external dependencies required - uses existing tech stack