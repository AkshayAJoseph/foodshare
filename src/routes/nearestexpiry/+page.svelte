<script>
  import { getfoods } from "../../script";
  import { onMount } from "svelte";

  let data = [];
  let loading = true;

  const doFetch = async () => {
    data = await getfoods();
    data.sort((a, b) => a.hours - b.hours);

    loading = false;
  };

  onMount(() => {
    doFetch();
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else}
  <div class="cards">
    {#each data as item}
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
