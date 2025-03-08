<script>
  import { getfoods } from "../../script";
  import { onMount } from "svelte";

  let data = []; // Full dataset
  let filteredData = []; // Stores filtered items
  let loading = true;
  let categoryFilter = ""; // Stores user input for filtering

  const doFetch = async () => {
    data = await getfoods();
    data.sort((a, b) => a.hours - b.hours);

    filterData(); // Apply filter after fetching
    loading = false;
  };

  const filterData = () => {
    if (categoryFilter.trim() === "") {
      filteredData = data; // Show all if no filter is applied
    } else {
      filteredData = data.filter(
        (item) => item.category.toLowerCase() === categoryFilter.toLowerCase()
      );
    }
  };

  onMount(() => {
    doFetch();
  });
</script>

<!-- Input for category filter -->
<label>Filter by Category:</label>
<input type="text" bind:value={categoryFilter} on:input={filterData} />

{#if loading}
  <p>Loading...</p>
{:else}
  <div class="cards">
    {#each filteredData as item}
      <div class="card">
        <h3>{item.name}</h3>
        <p><strong>Hours:</strong> {item.lifespan}</p>
        <p><strong>Category:</strong> {item.category}</p>
        <p><strong>Quantity:</strong> {item.quantity}</p>
        <p><strong>Tags:</strong> {item.tags}</p>
      </div>
    {/each}
  </div>
{/if}
