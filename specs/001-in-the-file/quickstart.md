# Quickstart: Dog Adoption Application Form

## Feature Overview
This feature adds an adoption application form to dog detail pages, allowing users to express interest in adopting available dogs by providing their contact information.

## Prerequisites
- Flask backend running with existing dog shelter database
- Astro frontend with Svelte components
- Existing dog detail pages functional

## Quick Test Scenarios

### Scenario 1: Successful Application Submission
**Setup**: Navigate to an available dog's detail page
**Steps**:
1. Verify adoption form is visible
2. Fill in valid data:
   - Name: "John Doe" (≤50 chars)
   - Email: "john.doe@example.com" (valid format)
   - Phone: "(555) 123-4567" (US format)
3. Click submit
4. Observe loading spinner and disabled button
5. Verify "submission accepted" confirmation message

**Expected Result**: Application stored in database, form replaced with success message

### Scenario 2: Form Validation Errors
**Setup**: Navigate to an available dog's detail page
**Steps**:
1. Fill in invalid data:
   - Name: "" (empty)
   - Email: "invalid-email" (invalid format)  
   - Phone: "123" (invalid US format)
2. Click submit
3. Observe validation error messages

**Expected Result**: Clear error messages shown, form remains editable

### Scenario 3: Dog Already Has Application
**Setup**: Dog with existing application in database
**Steps**:
1. Navigate to dog detail page
2. Look for adoption form

**Expected Result**: No form displayed, "Has an application" message shown

### Scenario 4: Staff Application Review
**Setup**: Applications exist in database
**Steps**:
1. Navigate to staff applications endpoint/page
2. Verify read-only list view shows:
   - Dog name and breed
   - Applicant contact information
   - Submission timestamp
   - Application status

**Expected Result**: All applications visible in chronological order (newest first)

## API Testing

### Test Application Submission
```bash
curl -X POST http://localhost:5000/api/dogs/1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_name": "John Doe",
    "applicant_email": "john.doe@example.com", 
    "applicant_phone": "(555) 123-4567"
  }'
```
**Expected**: 201 Created with `{"message": "submission accepted", "application_id": N}`

### Test Validation Errors
```bash
curl -X POST http://localhost:5000/api/dogs/1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_name": "",
    "applicant_email": "invalid-email",
    "applicant_phone": "123"
  }'
```
**Expected**: 400 Bad Request with validation error details

### Test Duplicate Application
```bash
# First application succeeds
curl -X POST http://localhost:5000/api/dogs/1/applications \
  -H "Content-Type: application/json" \
  -d '{"applicant_name": "John Doe", "applicant_email": "john@example.com", "applicant_phone": "(555) 123-4567"}'

# Second application fails  
curl -X POST http://localhost:5000/api/dogs/1/applications \
  -H "Content-Type: application/json" \
  -d '{"applicant_name": "Jane Doe", "applicant_email": "jane@example.com", "applicant_phone": "(555) 987-6543"}'
```
**Expected**: Second request returns 409 Conflict

### Test Staff Applications View
```bash
curl http://localhost:5000/api/applications
```
**Expected**: 200 OK with array of all applications including dog and applicant details

## Database Verification

### Check Application Storage
```sql
SELECT a.*, d.name as dog_name, b.name as breed_name 
FROM adoption_applications a
JOIN dogs d ON a.dog_id = d.id  
JOIN breeds b ON d.breed_id = b.id
ORDER BY a.submission_timestamp DESC;
```

### Verify Unique Constraint
```sql
-- This should work (first application for dog)
INSERT INTO adoption_applications (dog_id, applicant_name, applicant_email, applicant_phone) 
VALUES (1, 'Test User', 'test@example.com', '5551234567');

-- This should fail (duplicate dog_id)
INSERT INTO adoption_applications (dog_id, applicant_name, applicant_email, applicant_phone) 
VALUES (1, 'Another User', 'another@example.com', '5559876543');
```

## Frontend Verification

### Component Integration Test
1. Open dog detail page for available dog
2. Verify `AdoptionForm.svelte` component renders
3. Check form follows dark mode styling
4. Verify TypeScript arrow functions in component code
5. Test form submission with network throttling

### E2E Test Coverage
Run Playwright tests covering:
- Form display logic based on dog availability
- Form validation and error states  
- Successful submission flow
- Loading states during submission
- Staff applications view

## Constitutional Compliance Checklist

- [ ] Python backend code uses type hints
- [ ] TypeScript frontend code uses arrow functions  
- [ ] Dark mode styling maintained
- [ ] Unit tests written with database mocking
- [ ] E2E tests cover user workflows
- [ ] Educational value preserved (clear, learnable code)
- [ ] GitHub Copilot compatibility maintained

## Success Criteria
✅ Users can apply for available dogs via web form  
✅ One application per dog enforced  
✅ All form data validated (email, phone, name length)  
✅ Loading states prevent duplicate submissions  
✅ Success confirmation shown after submission  
✅ Applications stored and reviewable by staff  
✅ Constitutional code quality standards met