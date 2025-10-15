# API Contract: Enhanced Dogs Endpoint

**Endpoint**: `GET /api/dogs`  
**Feature**: Unavailable Dogs Display Enhancement  
**Version**: Enhanced with unavailable parameter support

## Request Specification

### URL Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search` | string | No | `""` | Search term for dog name, breed, or description |
| `page` | integer | No | `1` | Page number for pagination (minimum: 1) |
| `per_page` | integer | No | `12` | Items per page (maximum: 50) |
| `breed_id` | integer | No | None | Filter by specific breed ID |
| `available` | string | No | None | Filter for available dogs (`"true"` or `"false"`) |
| `unavailable` | string | No | None | **NEW** - Filter for unavailable dogs (`"true"` or `"false"`) |

### Parameter Validation Rules
- **`available`**: Only accepts `"true"`, `"false"`, or None. Invalid values ignored.
- **`unavailable`**: Only accepts `"true"`, `"false"`, or None. Invalid values ignored.
- **Combined Logic**: Both `available` and `unavailable` can be `"true"` simultaneously
- **Page bounds**: `page` minimum value is 1, automatically clamped
- **Per-page limits**: `per_page` maximum value is 50, automatically clamped

### Filter Logic Matrix
| available | unavailable | Filter Applied | Dogs Returned |
|-----------|-------------|----------------|---------------|
| `"true"` | `None` or `"false"` | `Dog.status == 'AVAILABLE'` | Available only (existing behavior) |
| `None` or `"false"` | `"true"` | `Dog.status != 'AVAILABLE'` | Unavailable only (new) |
| `"true"` | `"true"` | No status filter | All dogs (new) |
| `None` or `"false"` | `None` or `"false"` | No status filter | All dogs (default) |

## Response Specification

### Success Response (200 OK)
```json
{
  "dogs": [
    {
      "id": 1,
      "name": "Buddy",
      "breed": "Golden Retriever", 
      "status": "AVAILABLE"
    },
    {
      "id": 2,
      "name": "Max", 
      "breed": "German Shepherd",
      "status": "PENDING"
    }
  ],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `dogs` | Array\<Dog\> | Array of dog objects matching filter criteria |
| `dogs[].id` | integer | Unique dog identifier |
| `dogs[].name` | string | Dog's name |
| `dogs[].breed` | string | Breed name (joined from breeds table) |
| `dogs[].status` | string | **ENHANCED** - Dog's adoption status |
| `total` | integer | Total number of dogs matching filter (before pagination) |
| `pages` | integer | Total number of pages available |
| `current_page` | integer | Current page number |

### Dog Status Values
| Status | Description | Filtered By |
|--------|-------------|-------------|
| `"AVAILABLE"` | Dog is available for adoption | `available="true"` |
| `"PENDING"` | Adoption application in process | `unavailable="true"` |
| `"ADOPTED"` | Dog has been adopted | `unavailable="true"` |

### Empty Result Response (200 OK)
```json
{
  "dogs": [],
  "total": 0,
  "pages": 0,
  "current_page": 1
}
```

## Error Responses

### Bad Request (400)
**Scenario**: Invalid pagination parameters
```json
{
  "error": "Invalid page or per_page parameter"
}
```

### Internal Server Error (500)
**Scenario**: Database connection issues
```json
{
  "error": "Internal server error"
}
```

## Backward Compatibility

### Existing Behavior Preserved
- **No parameters**: Returns all dogs (unchanged)
- **`available="true"` only**: Returns available dogs only (unchanged)
- **Response format**: All existing fields maintained
- **Pagination**: Logic and response structure unchanged

### New Functionality
- **`unavailable` parameter**: Additive enhancement, doesn't break existing clients
- **`status` field**: Added to all dog objects in response
- **Combined filtering**: New capability for showing all dogs when both parameters true

## Performance Characteristics

### Response Time Requirements
- **Target**: < 200ms for typical queries
- **With filtering**: Status filtering adds minimal overhead
- **With pagination**: Performance scales with page size, not total dataset

### Query Optimization
- **Existing indexes**: Leverages current database indexes on `dogs.breed_id`
- **Status filtering**: Uses existing enum column, no additional indexes required
- **Sort order**: Maintains `ORDER BY Dog.name` for consistency

## Client Implementation Notes

### Frontend Parameter Building
```typescript
const buildApiParams = (searchTerm: string, selectedBreedId: string, 
                       availableOnly: boolean, showUnavailable: boolean,
                       currentPage: number): URLSearchParams => {
  const params = new URLSearchParams({
    search: searchTerm,
    page: currentPage.toString(),
    per_page: '12'
  });
  
  if (selectedBreedId) params.append('breed_id', selectedBreedId);
  if (availableOnly) params.append('available', 'true');
  if (showUnavailable) params.append('unavailable', 'true');
  
  return params;
};
```

### Response Processing
```typescript
interface ApiResponse {
  dogs: Array<{
    id: number;
    name: string; 
    breed: string;
    status: 'AVAILABLE' | 'PENDING' | 'ADOPTED';
  }>;
  total: number;
  pages: number;
  current_page: number;
}

const processResponse = async (response: Response): Promise<ApiResponse> => {
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  return await response.json();
};
```

## Testing Contract

### Unit Test Scenarios
1. **Parameter validation**: Test valid/invalid parameter combinations
2. **Filter logic**: Verify each filter combination produces correct results
3. **Pagination**: Test page boundaries and per_page limits
4. **Status inclusion**: Verify status field present in all responses
5. **Backward compatibility**: Ensure existing behavior unchanged

### Integration Test Scenarios  
1. **Frontend-backend**: Test parameter passing and response processing
2. **Database queries**: Verify correct SQL generation for filters
3. **Performance**: Validate response times meet requirements
4. **Error handling**: Test graceful failure scenarios

---

**Contract Status**: ✅ COMPLETED  
**Backward Compatible**: Yes, all existing functionality preserved  
**New Capabilities**: Unavailable dog filtering, combined filter support, status information