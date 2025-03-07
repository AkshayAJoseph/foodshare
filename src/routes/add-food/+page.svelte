<script>
  import { Storage } from "@capacitor/storage";
  import { onMount } from "svelte";
  import { Geolocation } from "@capacitor/geolocation";
  import {
    addfood,
    getArr,
    handleBackButton,
    login,
    takephoto,
  } from "../../script";

  let items = [];

  async function fetchData() {
    items = await getArr();
  }

  const addSection = async () => {
    items = await takephoto();
    console.log(items);
  };

  const clear = async () => {
    await Storage.remove({ key: "foodItems" });
  };

  const handleSubmit = async (index) => {
    const data = await Geolocation.getCurrentPosition();
    const { latitude, longitude } = data.coords;
    console.log(data);
    console.log("Submitting:", JSON.stringify(items[index]));
    addfood(items[index], longitude, latitude);
    console.log(index);
    if (items.length == 1) {
      items = [];
      Storage.remove({ key: "foodItems" });
    }
    items.splice(index, 1);
    items = items;
    await Storage.set({
      key: "foodItems",
      value: JSON.stringify(items),
    });
  };

  onMount(() => {
    fetchData();
  });

  handleBackButton("/");
</script>

{#each items as item, index}
  <div class="card">
    <label>Name</label>
    <input type="text" bind:value={item.name} />
    <label>Lifespan</label>
    <input type="text" bind:value={item.lifespan} />
    <label>Quantity</label>
    <input type="text" bind:value={item.quantity} />
    <label>Category</label>
    <input type="text" bind:value={item.category} />
    <label>Tags</label>
    <input type="text" bind:value={item.tags} />
    <button onclick={() => handleSubmit(index)}>Submit</button>
  </div>
{/each}

<br />
<button onclick={addSection}>Add</button>
<button onclick={clear}>clear</button>
