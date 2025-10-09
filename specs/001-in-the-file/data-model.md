# Data Model: Dog Adoption Application Form

## Entities and Relationships

### AdoptionApplication (New Entity)
**Purpose**: Stores adoption interest submissions from prospective adopters

**Fields**:
- `id`: Integer, Primary Key, Auto-increment
- `dog_id`: Integer, Foreign Key to dogs.id, NOT NULL
- `applicant_name`: String(50), NOT NULL
- `applicant_email`: String(320), NOT NULL (max email length per RFC 5321)
- `applicant_phone`: String(15), NOT NULL (formatted US phone number storage)
- `submission_timestamp`: DateTime, NOT NULL, Default: current timestamp
- `application_status`: String(20), Default: 'PENDING'

**Constraints**:
- Unique constraint on (dog_id) - enforces one application per dog
- Email format validation at application level
- Phone format validation at application level (US format)
- Name length limit: 50 characters (as clarified)

**Relationships**:
- Many-to-One with Dog entity (dog_id → dogs.id)

### Dog (Existing Entity - Updates)
**Existing Fields**: id, name, breed_id, age, gender, description, status, intake_date, adoption_date

**New Relationships**:
- One-to-Many with AdoptionApplication (applications relationship)

**Computed Properties** (for form display logic):
- `has_application`: Boolean derived from applications relationship
- Application count for business logic validation

## Database Schema

### New Table: adoption_applications
```sql
CREATE TABLE adoption_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    applicant_name VARCHAR(50) NOT NULL,
    applicant_email VARCHAR(320) NOT NULL,
    applicant_phone VARCHAR(15) NOT NULL,
    submission_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    application_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY (dog_id) REFERENCES dogs (id),
    UNIQUE (dog_id)
);
```

### Updated dogs table
No schema changes required - relationship handled at ORM level

## Validation Rules

### AdoptionApplication Validation
- **applicant_name**: 
  - Required, non-empty
  - Maximum 50 characters
  - Minimum 2 characters (following existing Dog.name pattern)
  
- **applicant_email**:
  - Required, non-empty
  - Valid email format (RFC 5322 compliant)
  - Maximum 320 characters
  
- **applicant_phone**:
  - Required, non-empty
  - US phone format: 10 digits
  - Accept formats: xxx-xxx-xxxx, (xxx) xxx-xxxx, xxxxxxxxxx
  - Store in normalized format
  
- **dog_id**:
  - Must reference existing dog
  - Dog must have status 'AVAILABLE'
  - Must not already have an application (unique constraint)

## State Transitions

### Application Lifecycle
1. **Created**: Initial state when form submitted
2. **PENDING**: Default status for new applications (read-only for staff)

Note: Advanced status management (APPROVED, REJECTED, etc.) is out of scope per constitutional simplicity requirements.

## Data Access Patterns

### Form Display Logic
```
Query: Check if dog has application
IF dog.status != 'AVAILABLE' OR dog.has_application:
    Hide form, show appropriate message
ELSE:
    Display adoption form
```

### Application Submission
```
1. Validate all fields
2. Check dog availability and no existing application
3. Create new AdoptionApplication record
4. Return success confirmation
```

### Staff Application Review
```
Query: SELECT applications with dog details
Display: Read-only list view (as clarified)
Order: By submission_timestamp DESC (most recent first)
```

## Database Migration Strategy

Since this is a workshop project with existing SQLite database:
1. Add new table creation to existing database initialization
2. Update seed data scripts if needed
3. Ensure backward compatibility with existing data