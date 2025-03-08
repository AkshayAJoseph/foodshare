<script>
  import { getCoords, getDistance, getfoods } from "../../script";
  import { onMount } from "svelte";

  let selectedValue = $state(0); // Default integer value

  let data = $state([]);
  let loading = $state(true);

  const doFetch = async () => {
    data = await getfoods();
    console.log("Before Sorting:", data);
    const ucoords = await getCoords();
    const lonu = ucoords.longitude;
    const latu = ucoords.latitude;
    console.log(ucoords);

    data = data.map((item) => ({
      ...item,
      distance: getDistance(latu, lonu, item.latitude, item.longitude),
    }));
    data.sort((a, b) => a.distance - b.distance);
    console.log("After Sorting:", data);
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
        <p><strong>Distance:</strong> {item.distance}</p>
        <p><strong>Category:</strong> {item.category}</p>
        <p><strong>Quantity:</strong> {item.quantity}</p>
        <p><strong>Tags:</strong> {item.tags}</p>
      </div>
    {/each}
  </div>
{/if}
