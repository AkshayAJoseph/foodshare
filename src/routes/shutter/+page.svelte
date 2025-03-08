<script>
  import { onMount } from "svelte";
  import { checkUser, logout } from "../../script";
  import { takephoto } from "../../script";
  import { Storage } from "@capacitor/storage";
  import { Geolocation } from "@capacitor/geolocation";
  import { addfood } from "../../script";
  let data;
  let loading = $state(true);
  let photoData = [];
  let items = $state([]);

  const getArr = () => {};

  async function fetchData() {
    items = await getArr();
    loading = false;
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

  const doCheck = async () => {
    data = await checkUser();
    if (data) {
    }
  };

  onMount(() => {
    doCheck();
  });

  fetchData();

  import Header from "$lib/Header.svelte";
  import Navigation from "$lib/Navigation.svelte";
</script>

<main>
  {#if loading}
    <p>Loading...</p>
  {:else}
    {#each items as item, index}
      <Header h1="Item" h5={index} />
      <div class="box">
        <div class="card">
          <div class="card__title">
            <h1>Contribute a food item</h1>
            <h5>AI Scan</h5>
          </div>
          <div class="form">
            <div class="form__row">
              <label>Title</label>
              <input placeholder="Laddu" bind:value={item.name} required />
            </div>
            <div class="form__row">
              <label>Category</label>
              <div class="flex">
                <div class="form__option">
                  <h5>Veg</h5>
                </div>
                <div class="form__option">
                  <h5>Non Veg</h5>
                </div>
              </div>
            </div>
            <div class="form__row">
              <label>Lifespan</label>
              <input
                placeholder="60Hours"
                bind:value={item.lifespan}
                required
              />
            </div>
            <div class="form__row">
              <label>Count</label>
              <input placeholder="3" required bind:value={item.quantity} />
            </div>
            <div class="form__row">
              <label>Category</label>
              <input placeholder="VEG" bind:value={item.category} required />
            </div>
            <div class="form__row">
              <label>Tags</label>
              <input placeholder="FRESH" bind:value={item.tags} required />
            </div>
            <a href="/home">
              <div
                class="btn--black"
                onclick={() => {
                  handleSubmit(index);
                }}
              >
                Contribute
              </div>
            </a>
          </div>
        </div>
      </div>
      <br />
    {/each}
  {/if}

  <br />
  <button onclick={addSection}>Add</button>
  <button onclick={clear}>clear</button>
  <Navigation />
</main>
