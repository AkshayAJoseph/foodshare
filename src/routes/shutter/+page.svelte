<script>
    import { onMount } from "svelte";
    import { checkUser, logout } from "../../script";
    import { takephoto } from "../../script";
    let data;
    let loading = true;
    let photoData = [];

    const getArr = () => {};

  async function fetchData() {
    items = await getArr();
    loading = false;
  }

    onMount(() => {
        doCheck();
        console.log(photoData);
    });
  };

    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";
</script>

<main>
    {#if loading}
        <p>Loading...</p>
    {:else}
        <Header h1="Welcome," h5={data.name} />
        <div class="box">
            <div class="card">
                <div class="card__title">
                    <h1>Contribute a food item</h1>
                    <h5>AI Scan</h5>
                </div>
                <div class="form">
                    <div class="form__row">
                        <label>Title</label>
                        <input placeholder="Laddu" required />
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
                        <input placeholder="60Hours" required />
                    </div>
                    <div class="form__row">
                        <label>Count</label>
                        <input placeholder="3" required />
                    </div>
                    <div class="form__row">
                        <label>Tags</label>
                        <input placeholder="FRESH" required />
                    </div>
                    <a href="/home">
                        <div class="btn--black">Contribute</div>
                    </a>
                </div>
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
