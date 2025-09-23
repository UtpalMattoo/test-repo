# 

Background: https://github.com/UtpalMattoo/test-repo/blob/main/content/1-hour/4-add-feature.md


Change history 
## 
Testing(test_app.py)

What changed:

Initial issue: The test mocks returned MagicMock objects, which are not JSON serializable, causing Flask's jsonify to fail.
First suggestion: Change mocks to return dictionaries. This caused an AttributeError because the backend expects objects with attributes (e.g., dog.id), not dictionary keys (e.g., dog['id']).
Final fix: Introduced a simple SimpleDog class with the required attributes (id, name, breed, status). The tests now use instances of this class for mocking, which matches the backend's expectations and resolves both serialization and attribute access errors.

Summary:

The test mocks now use objects with attributes, making them compatible with both Flask's serialization and the backend's attribute access.

##
Frontend (DogList.svelte)

Frontend (DogList.svelte):

Add a breed dropdown and an availability checkbox for filtering dogs.
Persist search term, selected breed, and availability filter in localStorage.
Combine all filters (search, breed, availability) and send them as query parameters to the backend.
Update the dog list dynamically based on filters and pagination.
Maintain dark mode and modern UI, using arrow functions for TypeScript.

##

Backend(app.py):

Update /api/dogs endpoint to accept and filter by breed_id and available query parameters.
Filter dogs by breed and availability status if those parameters are provided.
Sort the returned dog list alphabetically by name.
Support search and pagination