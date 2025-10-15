// Simple validation script to test our implementation logic

console.log("Testing getStatusBadge function logic...");

// Simulate the getStatusBadge function from our component
const getStatusBadge = (dog) => {
    if (!dog.status) return { text: 'AVAILABLE', class: 'bg-green-600' };
    
    switch (dog.status) {
        case 'AVAILABLE':
            return { text: 'AVAILABLE', class: 'bg-green-600' };
        case 'PENDING':
            return { text: 'PENDING', class: 'bg-yellow-600' };
        case 'ADOPTED':
            return { text: 'ADOPTED', class: 'bg-gray-600' };
        default:
            return { text: 'AVAILABLE', class: 'bg-green-600' };
    }
};

// Test cases
const testDogs = [
    { id: 1, name: "Buddy", breed: "Labrador", status: "AVAILABLE" },
    { id: 2, name: "Max", breed: "Golden Retriever", status: "PENDING" },
    { id: 3, name: "Charlie", breed: "Beagle", status: "ADOPTED" },
    { id: 4, name: "Bella", breed: "Poodle" }, // No status field
];

console.log("\nTesting status badge generation:");
testDogs.forEach(dog => {
    const badge = getStatusBadge(dog);
    console.log(`${dog.name}: ${badge.text} (${badge.class})`);
});

// Test URL parameter building logic
console.log("\nTesting URL parameter building logic:");

const buildParams = (searchTerm, availableOnly, showUnavailable, selectedBreedId, currentPage) => {
    const params = new URLSearchParams({
        search: searchTerm,
        page: currentPage.toString(),
        per_page: '12'
    });
    if (selectedBreedId) params.append('breed_id', selectedBreedId);
    if (availableOnly) params.append('available', 'true');
    if (showUnavailable) params.append('unavailable', 'true');
    return params.toString();
};

// Test different parameter combinations
const testCases = [
    { searchTerm: '', availableOnly: true, showUnavailable: false, selectedBreedId: '', currentPage: 1 },
    { searchTerm: '', availableOnly: false, showUnavailable: true, selectedBreedId: '', currentPage: 1 },
    { searchTerm: '', availableOnly: true, showUnavailable: true, selectedBreedId: '', currentPage: 1 },
    { searchTerm: 'buddy', availableOnly: true, showUnavailable: false, selectedBreedId: '5', currentPage: 2 },
];

testCases.forEach((test, index) => {
    const params = buildParams(test.searchTerm, test.availableOnly, test.showUnavailable, test.selectedBreedId, test.currentPage);
    console.log(`Test ${index + 1}: ${params}`);
});

console.log("\n✅ All function logic tests completed!");