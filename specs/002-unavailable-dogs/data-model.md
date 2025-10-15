# Data Model: Unavailable Dogs Display Enhancement

**Feature**: Unavailable Dogs Display Enhancement  
**Date**: October 12, 2025  
**Phase**: 1 - Data Model & Contracts

## Data Entities

### Existing Models (No Changes Required)

#### Dog Model
**Location**: `server/models/dog.py`  
**Schema**: Existing SQLAlchemy model with status enum
```python
class Dog(BaseModel):
    __tablename__ = 'dogs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id'))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    description = db.Column(db.Text)
    status = db.Column(db.Enum(AdoptionStatus), default=AdoptionStatus.AVAILABLE)  # KEY FIELD
    intake_date = db.Column(db.DateTime, default=datetime.now)
    adoption_date = db.Column(db.DateTime, nullable=True)
```

#### AdoptionStatus Enum  
**Location**: `server/models/dog.py`
**Values**: Existing enum supports all required status types
```python
class AdoptionStatus(Enum):
    AVAILABLE = 'Available'      # Filterable: available=true
    ADOPTED = 'Adopted'          # Filterable: unavailable=true  
    PENDING = 'Pending'          # Filterable: unavailable=true
```

## Data Access Patterns

### Enhanced Query Logic
**Current Pattern** (Available Dogs Only):
```python
if available == 'true':
    query = query.filter(Dog.status == 'AVAILABLE')
```

**Enhanced Pattern** (Available + Unavailable Support):
```python
# New logic to handle both parameters
if available == 'true' and unavailable == 'true':
    # Show all dogs - no status filter
    pass
elif available == 'true' and unavailable != 'true':  
    # Show only available dogs (existing behavior)
    query = query.filter(Dog.status == 'AVAILABLE')
elif unavailable == 'true' and available != 'true':
    # Show only unavailable dogs (new functionality)
    query = query.filter(Dog.status != 'AVAILABLE')  
else:
    # Neither checked - show empty or default behavior
    # Could show all or none based on UX requirements
    pass
```

### Database Performance Considerations
**Existing Indexes**: 
- Primary key index on `dogs.id`
- Foreign key index on `dogs.breed_id`  
- **Status filtering relies on existing enum column** (no additional index needed for small datasets)

**Query Performance**:
- Status filtering adds minimal overhead to existing queries
- Existing `ORDER BY Dog.name` maintained for consistency
- Pagination logic unchanged

## API Data Contracts

### Enhanced GET /api/dogs Response
**Extended Response Structure**:
```json
{
  "dogs": [
    {
      "id": 1,
      "name": "Buddy", 
      "breed": "Golden Retriever",
      "status": "AVAILABLE"        // ← Enhanced field (always included)
    },
    {
      "id": 2, 
      "name": "Max",
      "breed": "German Shepherd", 
      "status": "PENDING"          // ← Enhanced field (always included)
    }
  ],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

**Status Field Mapping**:
- Database enum value → API response value (same format)
- `AdoptionStatus.AVAILABLE` → `"AVAILABLE"`
- `AdoptionStatus.PENDING` → `"PENDING"` 
- `AdoptionStatus.ADOPTED` → `"ADOPTED"`

### Request Parameter Validation
**Parameter Types**:
```python
available: Optional[str] = request.args.get('available')      # 'true'|'false'|None
unavailable: Optional[str] = request.args.get('unavailable')  # 'true'|'false'|None (NEW)
search: str = request.args.get('search', '').strip()         # unchanged
breed_id: Optional[str] = request.args.get('breed_id')       # unchanged  
page: int = max(1, int(request.args.get('page', 1)))         # unchanged
per_page: int = min(50, int(request.args.get('per_page', 12))) # unchanged
```

## Frontend Data Models

### Component State Model
**DogList.svelte Enhanced State**:
```typescript
interface Dog {
  id: number;
  name: string;
  breed: string;
  status?: 'AVAILABLE' | 'PENDING' | 'ADOPTED';  // ← Enhanced optional field
}

interface DogResponse {
  dogs: Dog[];
  total: number;
  pages: number; 
  current_page: number;
}

// Component state variables
let availableOnly: boolean = true;     // existing
let showUnavailable: boolean = false;  // NEW
let dogs: Dog[] = [];                  // enhanced with status
```

### LocalStorage Data Model
**Enhanced Persistence Keys**:
```typescript
// Existing keys (maintained)
'dogSearchTerm': string           // search input value
'dogSelectedBreedId': string      // selected breed filter  
'dogAvailableOnly': 'true'|'false'  // available checkbox state

// New key
'dogShowUnavailable': 'true'|'false'  // unavailable checkbox state (NEW)
```

## Data Flow Patterns

### Filter State to API Parameters
**Checkbox State → API Parameters Mapping**:

| availableOnly | showUnavailable | API Parameters | Result |
|---------------|-----------------|----------------|---------|
| `true` | `false` | `available=true` | Available dogs only (existing) |
| `false` | `true` | `unavailable=true` | Unavailable dogs only (new) |
| `true` | `true` | `available=true&unavailable=true` | All dogs (new) |
| `false` | `false` | *(no parameters)* | Empty state or all dogs (UX decision) |

### API Response to UI Rendering
**Status Value → Badge Rendering**:
```typescript
const getStatusBadge = (status: string) => {
  switch (status) {
    case 'AVAILABLE': 
      return { text: 'Available', class: 'bg-green-500/20 text-green-400' };
    case 'PENDING':
      return { text: 'Pending Adoption', class: 'bg-amber-500/20 text-amber-400' };
    case 'ADOPTED':
      return { text: 'Adopted', class: 'bg-red-500/20 text-red-400' };
    default:
      return { text: 'Unknown', class: 'bg-slate-500/20 text-slate-400' };
  }
};
```

## Data Validation Rules

### Backend Validation
**Parameter Validation**:
- `available` parameter: accept only 'true', 'false', or None
- `unavailable` parameter: accept only 'true', 'false', or None  
- Invalid values ignored (fail gracefully, don't error)
- Maintain existing validation for other parameters

**Response Validation**:
- All dogs must have valid status enum values
- Status field included in all responses when dogs are present
- Empty arrays when no dogs match filter criteria

### Frontend Validation  
**State Consistency**:
- Checkbox states must be boolean values
- localStorage values validated before restoration
- Invalid localStorage values reset to defaults
- API parameter building handles undefined/null states gracefully

## Migration Strategy

### Backward Compatibility
**Existing API Behavior**:
- No parameters → All dogs (no change to existing behavior)
- `available=true` only → Available dogs only (no change)
- New parameters ignored by older clients (graceful degradation)

**Database Compatibility**:
- No schema migration required
- All existing data has valid status enum values
- Seeded data includes mix of status types for testing

### Frontend Compatibility
**Progressive Enhancement**:  
- Existing dog tiles continue to work without status badges
- Status information added when available in API response
- New checkbox functionality optional enhancement
- Existing localStorage keys preserved and functional

---

**Data Model Status**: ✅ COMPLETED  
**Key Insight**: Leveraging existing Dog.status enum eliminates need for schema changes while providing all required functionality.
**Next**: API contracts and component specifications