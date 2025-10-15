# Component Contract: Enhanced DogList

**Component**: `client/src/components/DogList.svelte`  
**Feature**: Unavailable Dogs Display Enhancement  
**Type**: Enhanced Svelte component with new filtering capabilities

## Component Interface

### Props (Unchanged)
```typescript
export let dogs: Dog[] = [];  // External dogs array (optional initialization)
```

### Internal State (Enhanced)
```typescript
// Existing state (preserved)
let loading = true;
let error: string | null = null; 
let searchTerm = '';
let currentPage = 1;
let totalPages = 1;
let totalDogs = 0;
let breeds: Breed[] = [];
let selectedBreedId: string = '';
let availableOnly: boolean = true;   // Default: show available dogs (backward compatibility)

// New state  
let showUnavailable: boolean = false;  // NEW - controls unavailable checkbox
```

### Enhanced Dog Interface
```typescript
interface Dog {
  id: number;
  name: string;
  breed: string;
  status?: 'AVAILABLE' | 'PENDING' | 'ADOPTED';  // NEW - optional status field
}

interface DogResponse {
  dogs: Dog[];
  total: number;
  pages: number;
  current_page: number;
}
```

## State Management Contract

### Default States
| State Variable | Default Value | Persistence Key |
|---------------|---------------|-----------------|
| `searchTerm` | `""` | `'dogSearchTerm'` |
| `selectedBreedId` | `""` | `'dogSelectedBreedId'` |
| `availableOnly` | `true` | `'dogAvailableOnly'` |
| `showUnavailable` | `false` | `'dogShowUnavailable'` (NEW) |

### State Restoration Logic  
```typescript
onMount(() => {
  // Existing restoration (preserved)
  const savedSearch = localStorage.getItem('dogSearchTerm');
  if (savedSearch) searchTerm = savedSearch;
  
  const savedBreed = localStorage.getItem('dogSelectedBreedId');
  if (savedBreed) selectedBreedId = savedBreed;
  
  const savedAvailable = localStorage.getItem('dogAvailableOnly');
  if (savedAvailable) availableOnly = savedAvailable === 'true';
  
  // New restoration
  const savedUnavailable = localStorage.getItem('dogShowUnavailable');
  if (savedUnavailable) showUnavailable = savedUnavailable === 'true';
  
  fetchBreeds();
  fetchDogs();
});
```

### State Persistence Logic
```typescript
const debouncedSearch = debounce(async () => {
  currentPage = 1;
  // Existing persistence (preserved)
  localStorage.setItem('dogSearchTerm', searchTerm);
  localStorage.setItem('dogSelectedBreedId', selectedBreedId);  
  localStorage.setItem('dogAvailableOnly', availableOnly ? 'true' : 'false');
  
  // New persistence
  localStorage.setItem('dogShowUnavailable', showUnavailable ? 'true' : 'false');
  
  await fetchDogs();
}, 300);
```

## API Integration Contract

### Enhanced fetchDogs Method
```typescript
const fetchDogs = async () => {
  loading = true;
  try {
    const params = new URLSearchParams({
      search: searchTerm,
      page: currentPage.toString(), 
      per_page: '12'
    });
    
    // Existing parameter logic (preserved)
    if (selectedBreedId) params.append('breed_id', selectedBreedId);
    if (availableOnly) params.append('available', 'true');
    
    // New parameter logic
    if (showUnavailable) params.append('unavailable', 'true');

    const response = await fetch(`/api/dogs?${params}`);
    if(response.ok) {
      const data: DogResponse = await response.json();
      dogs = data.dogs;
      totalPages = data.pages;
      totalDogs = data.total;
    } else {
      error = `Failed to fetch data: ${response.status} ${response.statusText}`;
    }
  } catch (err) {
    error = `Error: ${err instanceof Error ? err.message : String(err)}`;
  } finally {
    loading = false;
  }
};
```

### Reactive Dependencies (Enhanced)
```typescript
// Existing reactivity (preserved)
$: searchTerm, debouncedSearch();
$: selectedBreedId, debouncedSearch();  
$: availableOnly, debouncedSearch();

// New reactivity
$: showUnavailable, debouncedSearch();
```

## UI Template Contract

### Enhanced Filter Controls Section
```svelte
<div class="mb-6 space-y-4">
  <!-- Search input (unchanged) -->
  <div class="relative mb-2">
    <input
      type="text"
      bind:value={searchTerm}
      placeholder="Search dogs by name or breed..."
      class="w-full px-4 py-2 bg-slate-800/60 border border-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-slate-100 placeholder-slate-400"
    />
    <!-- Clear button logic unchanged -->
  </div>
  
  <!-- Breed dropdown (unchanged) -->
  <div class="mb-2">
    <select bind:value={selectedBreedId} class="w-full px-4 py-2 bg-slate-800/60 border border-slate-700 rounded-lg text-slate-100">
      <option value="">All breeds</option>
      {#each breeds as breed}
        <option value={breed.id}>{breed.name}</option>
      {/each}
    </select>
  </div>
  
  <!-- Enhanced checkbox section -->
  <div class="flex flex-col space-y-2 mb-2">
    <!-- Existing available checkbox (preserved) -->
    <div class="flex items-center">
      <input
        type="checkbox"
        bind:checked={availableOnly}
        id="availableOnly"
        class="mr-2 accent-blue-500"
      />
      <label for="availableOnly" class="text-slate-300">Show available dogs</label>
    </div>
    
    <!-- New unavailable checkbox -->  
    <div class="flex items-center">
      <input
        type="checkbox"
        bind:checked={showUnavailable}
        id="showUnavailable"
        class="mr-2 accent-blue-500"
      />
      <label for="showUnavailable" class="text-slate-300">Show unavailable dogs</label>
    </div>
  </div>
</div>
```

### Enhanced Dog Tile Template  
```svelte
<!-- Dog list section -->
{#each dogs as dog (dog.id)}
  <a 
    href={`/dog/${dog.id}`} 
    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
  >
    <div class="p-6 relative">
      <!-- Existing content (preserved) -->
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      <div class="relative z-10">
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors">{dog.name}</h3>
          
          <!-- New status badge (always visible when status available) -->
          {#if dog.status}
            <span class="text-sm px-3 py-1 rounded-full {getStatusBadgeClass(dog.status)}">
              {getStatusBadgeText(dog.status)}
            </span>
          {/if}
        </div>
        <p class="text-slate-400 mb-4">{dog.breed}</p>
        <!-- Existing hover effects preserved -->
      </div>
    </div>
  </a>
{/each}
```

### Status Badge Helper Functions
```typescript
const getStatusBadgeClass = (status: string): string => {
  switch (status) {
    case 'AVAILABLE': 
      return 'bg-green-500/20 text-green-400';
    case 'PENDING':
      return 'bg-amber-500/20 text-amber-400';  
    case 'ADOPTED':
      return 'bg-red-500/20 text-red-400';
    default:
      return 'bg-slate-500/20 text-slate-400';
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

## Empty State Handling Contract

### Context-Aware Empty Messages
```typescript
const getEmptyStateMessage = (): string => {
  if (availableOnly && !showUnavailable) {
    return "No available dogs found.";
  } else if (!availableOnly && showUnavailable) {
    return "No unavailable dogs found.";  
  } else if (availableOnly && showUnavailable) {
    return "No dogs match your search criteria.";
  } else {
    return "No dogs found.";
  }
};
```

### Empty State Template
```svelte
{:else if dogs.length === 0}
  <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
    <p class="text-slate-300">{getEmptyStateMessage()}</p>
  </div>
```

## Accessibility Contract

### ARIA Labels and Screen Reader Support
```svelte
<!-- Enhanced checkbox accessibility -->
<input
  type="checkbox"
  bind:checked={showUnavailable}
  id="showUnavailable"
  class="mr-2 accent-blue-500"
  aria-label="Show unavailable dogs checkbox"
/>

<!-- Enhanced status badge accessibility -->
{#if dog.status}
  <span 
    class="text-sm px-3 py-1 rounded-full {getStatusBadgeClass(dog.status)}"
    aria-label="Dog adoption status: {getStatusBadgeText(dog.status)}"
  >
    {getStatusBadgeText(dog.status)}
  </span>
{/if}
```

### Keyboard Navigation
- All checkboxes accessible via Tab navigation
- Enter/Space activates checkboxes  
- Focus indicators visible on all interactive elements
- Screen reader announces filter state changes

## Performance Contract

### Debouncing and Request Management
- **Debounce delay**: 300ms for all filter changes
- **Request cancellation**: Previous requests cancelled on new filter application
- **Loading states**: Immediate feedback on checkbox state changes
- **Error handling**: Graceful recovery from API failures

### Memory Management
- **localStorage cleanup**: Invalid values reset to defaults
- **Component cleanup**: Debounced functions properly disposed
- **Event listeners**: Proper cleanup on component destruction

---

**Component Contract Status**: ✅ COMPLETED  
**Backward Compatible**: Yes, all existing props and behavior preserved  
**New Capabilities**: Unavailable dog filtering, status badge display, enhanced empty states