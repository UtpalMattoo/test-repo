<script lang="ts">
    import { onMount } from "svelte";
    import { debounce } from "lodash-es";

    interface Dog {
        id: number;
        name: string;
        breed: string;
    }

    interface DogResponse {
        dogs: Dog[];
        total: number;
        pages: number;
        current_page: number;
    }

    interface Breed {
        id: number;
        name: string;
    }

    export let dogs: Dog[] = [];
    let loading = true;
    let error: string | null = null;
    let searchTerm = '';
    let currentPage = 1;
    let totalPages = 1;
    let totalDogs = 0;

    // Breed dropdown state
    let breeds: Breed[] = [];
    let selectedBreedId: string = '';
    // Availability checkbox state
    let availableOnly: boolean = false;

    // Load persisted filter state
    onMount(() => {
        const savedSearch = localStorage.getItem('dogSearchTerm');
        if (savedSearch) searchTerm = savedSearch;
        const savedBreed = localStorage.getItem('dogSelectedBreedId');
        if (savedBreed) selectedBreedId = savedBreed;
        const savedAvailable = localStorage.getItem('dogAvailableOnly');
        if (savedAvailable) availableOnly = savedAvailable === 'true';

        fetchBreeds();
        fetchDogs();
    });

    const fetchBreeds = async () => {
        try {
            const res = await fetch('/api/breeds');
            if (res.ok) {
                breeds = await res.json();
            }
        } catch {}
    };

    const debouncedSearch = debounce(async () => {
        currentPage = 1;
        localStorage.setItem('dogSearchTerm', searchTerm);
        localStorage.setItem('dogSelectedBreedId', selectedBreedId);
        localStorage.setItem('dogAvailableOnly', availableOnly ? 'true' : 'false');
        await fetchDogs();
    }, 300);

    $: searchTerm, debouncedSearch();
    $: selectedBreedId, debouncedSearch();
    $: availableOnly, debouncedSearch();

    const fetchDogs = async () => {
        loading = true;
        try {
            const params = new URLSearchParams({
                search: searchTerm,
                page: currentPage.toString(),
                per_page: '12'
            });
            if (selectedBreedId) params.append('breed_id', selectedBreedId);
            if (availableOnly) params.append('available', 'true');

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

    const handlePageChange = async (newPage: number) => {
        if (newPage >= 1 && newPage <= totalPages) {
            currentPage = newPage;
            await fetchDogs();
        }
    };
</script>

<div>
    <div class="mb-6 space-y-4">
        <h2 class="text-2xl font-medium text-slate-100">Available Dogs</h2>
        <!-- Search input -->
        <div class="relative mb-2">
            <input
                type="text"
                bind:value={searchTerm}
                placeholder="Search dogs by name or breed..."
                class="w-full px-4 py-2 bg-slate-800/60 border border-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-slate-100 placeholder-slate-400"
            />
            {#if searchTerm}
                <button
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                    on:click={() => { searchTerm = ''; }}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                </button>
            {/if}
        </div>
        <!-- Breed dropdown -->
        <div class="mb-2">
            <select
                bind:value={selectedBreedId}
                class="w-full px-4 py-2 bg-slate-800/60 border border-slate-700 rounded-lg text-slate-100"
            >
                <option value="">All breeds</option>
                {#each breeds as breed}
                    <option value={breed.id}>{breed.name}</option>
                {/each}
            </select>
        </div>
        <!-- Availability checkbox -->
        <div class="flex items-center mb-2">
            <input
                type="checkbox"
                bind:checked={availableOnly}
                id="availableOnly"
                class="mr-2 accent-blue-500"
            />
            <label for="availableOnly" class="text-slate-300">Show only available dogs</label>
        </div>
    </div>

    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-6"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if dogs.length === 0}
        <!-- no dogs found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No dogs available at the moment.</p>
        </div>
    {:else}
        <!-- dog list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each dogs as dog (dog.id)}
                <a 
                    href={`/dog/${dog.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors">{dog.name}</h3>
                            <p class="text-slate-400 mb-4">{dog.breed}</p>
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}

    <!-- Pagination -->
    {#if !loading && !error && totalPages > 1}
        <div class="mt-8 flex justify-center space-x-2">
            <button
                class="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-700"
                disabled={currentPage === 1}
                on:click={() => handlePageChange(currentPage - 1)}
            >
                Previous
            </button>
            <span class="px-4 py-2 text-slate-300">
                Page {currentPage} of {totalPages}
            </span>
            <button
                class="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-700"
                disabled={currentPage === totalPages}
                on:click={() => handlePageChange(currentPage + 1)}
            >
                Next
            </button>
        </div>
    {/if}
</div>